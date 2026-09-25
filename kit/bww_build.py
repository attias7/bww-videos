#!/usr/bin/env python3
"""Black & White Wisdom reel builder.

Usage:  python3 bww_build.py job.json
job.json fields:
  input      : source mp4 (minimalist narrated reel)
  voice      : ElevenLabs mp3 (whole script, one take, sentences separated by '...')
  cuts       : list of source-video times, one per sentence start, plus the video end as last item
               (time the sentence's first caption appears minus ~0.2 s; first item 0)
  hook       : {"kicker": "...", "line1": "...", "line2": "..."}
  out        : output mp4 path
  speed      : voice tempo (default 1.15)
  spans      : optional [[start,end],...] speech spans in the SPED-UP voice; auto-detected if omitted
  max_mb     : output size cap (default 9.5, for Buffer web upload)
  hook_pos   : "top" (default, captions at bottom) or "bottom" (use when the video's captions are at the top)
  caption_band: [y, h] in 720x1280 output pixels for the sync sheet (default [820,170]; top captions ~[240,130])
Writes <out>, <out>.sync.jpg (caption at each sentence start, for checking) and prints a summary.
"""
import json, subprocess, sys, os, wave, numpy as np

class sf:  # minimal replacement for the soundfile package (not always installable)
    @staticmethod
    def read(path, dtype='float32'):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-'], capture_output=True, check=True).stdout
        sr = int(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=sample_rate',
                                 '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip())
        return np.frombuffer(raw, np.float32).copy(), sr
    @staticmethod
    def write(path, data, sr):
        d = np.asarray(data, np.float32)
        ch = 1 if d.ndim == 1 else d.shape[1]
        with wave.open(path, 'wb') as w:
            w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes((np.clip(d, -1, 1) * 32767).astype('<i2').tobytes())
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bww_music import make as make_music

job = json.load(open(sys.argv[1]))
WD = os.path.splitext(job['out'])[0] + '_work'; os.makedirs(WD, exist_ok=True)
P = lambda n: os.path.join(WD, n)
SPEED = job.get('speed', 1.15); MAXMB = job.get('max_mb', 9.5)
cuts = job['cuts']; nsent = len(cuts) - 1
run = lambda c: subprocess.run(c, check=True)
FB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
FR = '/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf'
W, H = 720, 1280

# ---------- hook + end card ----------
def ctext(d, y, t, f, fill):
    w = d.textlength(t, font=f); d.text(((W - w) / 2, y), t, font=f, fill=fill)
def glow(draw_fn, r):
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(base))
    return Image.alpha_composite(base.filter(ImageFilter.GaussianBlur(r)), base)
hk = job['hook']
Y0 = 0 if job.get('hook_pos', 'top') == 'top' else 830
def dh(d):
    ctext(d, Y0 + 140, hk['kicker'].upper(), ImageFont.truetype(FR, 26), (200, 200, 200, 255))
    f = ImageFont.truetype(FB, 50)
    ctext(d, Y0 + 185, hk['line1'].upper(), f, (255, 255, 255, 255))
    ctext(d, Y0 + 245, hk['line2'].upper(), f, (255, 255, 255, 255))
glow(dh, 12).save(P('hook.png'))
def de(d):
    ctext(d, 560, 'SAVE THIS', ImageFont.truetype(FB, 64), (255, 255, 255, 255))
    ctext(d, 640, 'FOR A HARD DAY', ImageFont.truetype(FB, 40), (255, 255, 255, 255))
    ctext(d, 740, 'follow for more', ImageFont.truetype(FR, 28), (180, 180, 180, 255))
Image.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, 255)), glow(de, 16)).convert('RGB').save(P('endcard.png'))

# ---------- voice: speed up + split ----------
run(['ffmpeg', '-v', 'error', '-y', '-i', job['voice'], '-af', f'atempo={SPEED}', '-ac', '1', '-ar', '24000', P('voice_fast.wav')])
a, SR = sf.read(P('voice_fast.wav'), dtype='float32')
dur = len(a) / SR

def silences(path, d, n=-40, ss=None, t=None):
    cmd = ['ffmpeg', '-hide_banner']
    if ss is not None: cmd += ['-ss', str(ss), '-t', str(t)]
    cmd += ['-i', path, '-af', f'silencedetect=n={n}dB:d={d}', '-f', 'null', '-']
    out = subprocess.run(cmd, capture_output=True, text=True).stderr
    st = [float(l.split('silence_start: ')[1].split()[0]) for l in out.splitlines() if 'silence_start' in l]
    en = [float(l.split('silence_end: ')[1].split()[0]) for l in out.splitlines() if 'silence_end' in l]
    off = ss or 0
    return [(s + off, e + off) for s, e in zip(st, en)]

def speech_spans(gaps, total):
    spans, cur = [], 0.0
    for s, e in gaps:
        if s - cur > 0.15: spans.append([cur, s])
        cur = e
    if total - cur > 0.15: spans.append([cur, total])
    return spans

spans = job.get('spans')
if not spans:
    gaps = silences(P('voice_fast.wav'), 0.4)
    spans = speech_spans(gaps, dur)
    slots = [cuts[i + 1] - cuts[i] for i in range(nsent)]
    def cost(sp):  # how unevenly voice durations fit caption slots (only meaningful at equal counts)
        r = np.log([(e - s + 0.45) / o for (s, e), o in zip(sp, slots)])
        return float(np.var(r))
    def best_by_cost(cands, target):
        # pad/truncate evaluation when counts still differ: compare on the first min(len) items
        def c(sp):
            if len(sp) == nsent: return cost(sp)
            m = min(len(sp), nsent)
            return cost(sp[:m]) + 1.0 * abs(len(sp) - nsent)
        return min(cands, key=c)
    # too few: try splitting every span at each internal short pause, keep the best-fitting result
    while len(spans) < nsent:
        cands = []
        for i, (s, e) in enumerate(spans):
            sub = silences(P('voice_fast.wav'), 0.12, -42, s, e - s)
            for g in sub:
                if g[0] > s + 0.3 and g[1] < e - 0.3:
                    cands.append(spans[:i] + [[s, g[0]], [g[1], e]] + spans[i + 1:])
        if not cands: break
        spans = best_by_cost(cands, nsent)
    # too many: try every merge, keep the best-fitting result
    while len(spans) > nsent:
        cands = [spans[:i] + [[spans[i][0], spans[i + 1][1]]] + spans[i + 2:] for i in range(len(spans) - 1)]
        spans = best_by_cost(cands, nsent)
if len(spans) != nsent:
    sys.exit(f'ERROR: found {len(spans)} speech chunks for {nsent} sentences. Pass "spans" manually. spans={spans}')

clips = [a[max(0, int((s - 0.05) * SR)): int((e + 0.14) * SR)] for s, e in spans]
LEAD, TAIL = 0.08, 0.30
segs, t, voice = [], 0.0, []
for i, c in enumerate(clips):
    od = cuts[i + 1] - cuts[i]
    nd = max(LEAD + len(c) / SR + TAIL, od * 0.8)
    segs.append((cuts[i], cuts[i + 1], nd / od)); voice.append((t + LEAD, c)); t += nd
MAIN = t; TOTAL = MAIN + 1.6
out = np.zeros(int((TOTAL + 1) * SR), np.float32)
for st, c in voice:
    s = int(st * SR); out[s:s + len(c)] += c
sf.write(P('voice.wav'), out[:int(TOTAL * SR)] / np.max(np.abs(out)) * 0.9, SR)
make_music(P('music.wav'), TOTAL + 0.2, [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 65]], 92, [0, 2, 1, 3, 4, 2, 3, 1], kick_from=2.0)

# room impulse response
n = int(0.7 * 44100); tt = np.arange(n) / 44100
ir = np.random.default_rng(1).standard_normal((n, 2)) * np.exp(-tt * 7.5)[:, None] * 0.25; ir[0] = [1, 1]
sf.write(P('room_ir.wav'), ir / np.max(np.abs(ir)), 44100)

# ---------- render ----------
pieces, O = [], 0.0
for s0, s1, f in segs:
    pieces.append((s0, s1, f, O)); O += (s1 - s0) * f
expr = f"({pieces[-1][3]:.4f}+(T-{pieces[-1][0]})*{pieces[-1][2]:.4f})"
for s0, s1, f, o in reversed(pieces[:-1]):
    expr = f"if(lt(T\\,{s1})\\,{o:.4f}+(T-{s0})*{f:.4f}\\,{expr})"
fc = (f"[0:v]setpts='{expr}/TB',fps=30,scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,trim=duration={MAIN:.3f}[m];"
      f"[m]scale=w='trunc(720*(1+0.07*t/{MAIN:.3f})/2)*2':h=-2:eval=frame,crop=720:1280,eq=contrast=1.08:brightness=0.01,setsar=1[v0];"
      f"[2:v]format=rgba,fade=out:st=2.7:d=0.4:alpha=1[hk];[v0][hk]overlay=0:0:shortest=1[v1];"
      f"[1:v]fps=30,scale=720:1280,setsar=1,fade=in:st=0:d=0.35[ec];"
      f"[v1][ec]concat=n=2:v=1:a=0,noise=alls=3:allf=t,vignette=PI/5[v2];"
      f"[v2][5:v]overlay=x='-W+W*t/{TOTAL:.3f}':y=H-6[v];"
      f"[3:a]aresample=44100,aformat=channel_layouts=stereo,highpass=f=70,equalizer=f=120:t=q:w=1:g=1,"
      f"acompressor=threshold=-20dB:ratio=3:attack=8:release=160:makeup=3[vd];"
      f"[6:a]aresample=44100[irr];[vd]asplit=2[dry][wetin];[wetin][irr]afir=dry=10:wet=10[wet];"
      f"[dry][wet]amix=inputs=2:weights='1 0.15':normalize=0,apad=whole_dur={TOTAL:.3f},aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,asplit=2[voc][sc];"
      f"[4:a]aresample=44100,aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,volume=0.5[mus];[mus][sc]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=450[duck];"
      f"[duck]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[duck2];[voc][duck2]amix=inputs=2:normalize=0,alimiter=limit=0.9[a]")
inputs = ['-i', job['input'], '-loop', '1', '-t', '1.6', '-framerate', '30', '-i', P('endcard.png'),
          '-loop', '1', '-framerate', '30', '-t', f'{MAIN:.3f}', '-i', P('hook.png'),
          '-i', P('voice.wav'), '-i', P('music.wav'),
          '-f', 'lavfi', '-i', f'color=white:s=720x6:r=30:d={TOTAL:.3f}', '-i', P('room_ir.wav')]
abr = 128
vbr = int((MAXMB * 8 * 1024 * 0.96) / TOTAL - abr)  # kbit/s
vbr = max(600, min(vbr, 6000))
common = inputs + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium',
                   '-b:v', f'{vbr}k', '-pix_fmt', 'yuv420p', '-t', f'{TOTAL:.3f}']
plog = P('x264pass')
run(['ffmpeg', '-v', 'error', '-y'] + common + ['-pass', '1', '-passlogfile', plog, '-an', '-f', 'mp4', os.devnull])
run(['ffmpeg', '-v', 'error', '-y'] + common + ['-pass', '2', '-passlogfile', plog, '-c:a', 'aac', '-b:a', f'{abr}k',
                                                '-movflags', '+faststart', job['out']])
size = os.path.getsize(job['out']) / 1048576

# ---------- sync sheet ----------
BAND = job.get('caption_band', [820, 170])
tt, frames = 0.0, []
for i, (s0, s1, f) in enumerate(segs):
    x = tt + 0.45; tt += (s1 - s0) * f
    fp = P(f'sync_{i:02d}.png')
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{x:.3f}', '-i', job['out'], '-frames:v', '1',
         '-vf', f"crop=720:{BAND[1]}:0:{BAND[0]},scale=360:-1", fp])
    frames.append(fp)
ims = [Image.open(f) for f in frames]
sheet = Image.new('RGB', (360, sum(i.height for i in ims)))
y = 0
for im in ims: sheet.paste(im, (0, y)); y += im.height
sheet.save(job['out'] + '.sync.jpg')
print(json.dumps({'out': job['out'], 'seconds': round(TOTAL, 2), 'mb': round(size, 2), 'sentences': nsent,
                  'stretch': [round(s[2], 2) for s in segs], 'sync_sheet': job['out'] + '.sync.jpg'}))
