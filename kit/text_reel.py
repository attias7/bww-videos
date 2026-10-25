#!/usr/bin/env python3
"""Text-only vertical reel (no voice) — built for Subletli (Hebrew, right-to-left). Adi adds a trending song in TikTok.

Usage: python3 text_reel.py job.json
Job:
  {"out": "../out/sbl_ep01_<slug>.mp4", "accent": [r,g,b], "dark": [r,g,b] (dark background), "rtl": true,
   "footer": "סאבלטלי · subletli.com",
   "scenes": [
     {"dur": 2.6, "bg": "accent|dark|light", "kicker": "small line on top",
      "text": "big text, *highlighted words* in accent", "size": 120,
      "sub": "smaller line under it",
      "items": [{"t": "text", "ok": true|false}],      # checklist (✓ green / ✗ red), revealed one by one
      "chip": "subletli.com"}                          # pill at the bottom of the scene
   ]}
Writes <out> (1080x1920, 30 fps, silent AAC track), <out>_upload.mp4 (720x1280, < max_mb) and <out>_sync.jpg
(one frame per scene, taken after its text has appeared).
"""
import json, os, re, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "Heebo.ttf")
W, H, FPS = 1080, 1920, 30
DARK, LIGHT, INK = (14, 15, 19), (246, 244, 238), (20, 22, 28)
GREEN, RED, GREY = (60, 200, 110), (235, 75, 75), (150, 153, 165)
_fc = {}

def font(size, weight="ExtraBold"):
    k = (int(size), weight)
    if k not in _fc:
        f = ImageFont.truetype(FONT, max(8, int(size)))
        f.set_variation_by_name(weight)
        _fc[k] = f
    return _fc[k]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def mix(a, b, k): return tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))

def words(text):
    """'a *b c* d' -> [(a,False),(b,True),(c,True),(d,False)]"""
    out, hl = [], False
    for tok in re.split(r"(\*)", text):
        if tok == "*": hl = not hl; continue
        out += [(w, hl) for w in tok.split()]
    return out

def wrap(d, ws, f, maxw):
    lines, cur = [], []
    for w in ws:
        test = cur + [w]
        if cur and d.textlength(" ".join(x for x, _ in test), font=f, direction=DIR) > maxw:
            lines.append(cur); cur = [w]
        else:
            cur = test
    if cur: lines.append(cur)
    return lines

def draw_words(d, line, cy, f, col, hcol, alpha_bg, k):
    """Draw one line centred at cy; words placed right-to-left when RTL."""
    sp = d.textlength(" ", font=f)
    wl = [d.textlength(w, font=f, direction=DIR) for w, _ in line]
    total = sum(wl) + sp * (len(line) - 1)
    x = W / 2 + total / 2 if RTL else W / 2 - total / 2
    for (w, hl), lw in zip(line, wl):
        x0 = x - lw if RTL else x
        c = mix(alpha_bg, hcol if hl else col, k)
        d.text((x0, cy), w, font=f, fill=c, anchor="lm", direction=DIR)
        x = x0 - sp if RTL else x0 + lw + sp

def scene_frame(sc, t, accent, footer, p_total):
    bgname = sc.get("bg", "dark")
    bg = tuple(accent) if bgname == "accent" else LIGHT if bgname == "light" else DARK
    fg = INK if bgname in ("accent", "light") else (245, 245, 240)
    hc = INK if bgname == "accent" else tuple(accent)
    if bgname == "accent": hc = (255, 255, 255)
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    y = 520 if sc.get("items") else 760
    if sc.get("kicker"):
        k = ease(t / 0.35)
        f = font(46, "Bold")
        d.text((W / 2, y - 170 + 20 * (1 - k)), sc["kicker"], font=f, fill=mix(bg, GREY if bgname == "dark" else INK, k),
               anchor="mm", direction=DIR)
    size = sc.get("size", 118)
    f = font(size)
    lines = wrap(d, words(sc.get("text", "")), f, W - 140)
    while len(lines) > 4 and size > 70:
        size -= 8; f = font(size); lines = wrap(d, words(sc["text"]), f, W - 140)
    lh = size * 1.22
    top = y - lh * (len(lines) - 1) / 2
    for n, line in enumerate(lines):
        k = ease((t - 0.08 - n * 0.12) / 0.35)
        draw_words(d, line, top + n * lh + 30 * (1 - k), f, fg, hc, bg, k)
    yb = top + lh * len(lines) + 40
    if sc.get("sub"):
        k = ease((t - 0.45) / 0.35)
        fs = font(54, "Medium")
        for n, line in enumerate(wrap(d, words(sc["sub"]), fs, W - 180)):
            draw_words(d, line, yb + n * 72, fs, mix(bg, fg, 0.8), hc, bg, k)
            yb += 0
        yb += 72 * len(wrap(d, words(sc["sub"]), fs, W - 180)) + 30
    for n, it in enumerate(sc.get("items", [])):
        k = ease((t - 0.5 - n * 0.45) / 0.3)
        if k <= 0: continue
        cy = yb + 40 + n * 150
        x1, x0 = W - 110, 110
        box = (x0, cy - 60, x1, cy + 60)
        d.rounded_rectangle(box, radius=28, fill=mix(bg, (30, 32, 42) if bgname == "dark" else (255, 255, 255), k))
        ok = it.get("ok", True)
        ic = GREEN if ok else RED
        icx = x1 - 70 if RTL else x0 + 70
        d.ellipse((icx - 34, cy - 34, icx + 34, cy + 34), fill=mix(bg, ic, k))
        if ok:
            d.line([(icx - 15, cy + 1), (icx - 4, cy + 13), (icx + 17, cy - 12)], fill=(255, 255, 255), width=8)
        else:
            d.line([(icx - 13, cy - 13), (icx + 13, cy + 13)], fill=(255, 255, 255), width=8)
            d.line([(icx - 13, cy + 13), (icx + 13, cy - 13)], fill=(255, 255, 255), width=8)
        fi = font(52, "Bold")
        tx = (icx - 70) if RTL else (icx + 70)
        d.text((tx, cy), it["t"], font=fi, fill=mix(bg, fg, k), anchor="rm" if RTL else "lm", direction=DIR)
    if sc.get("chip"):
        k = ease((t - 0.6) / 0.35)
        fc = font(60, "ExtraBold")
        tw = d.textlength(sc["chip"], font=fc)
        cy = max(yb + 120, 1450)
        cbg = INK if bgname == "accent" else tuple(accent)
        ctx = (255, 255, 255) if bgname == "accent" else INK
        d.rounded_rectangle((W / 2 - tw / 2 - 50, cy - 60, W / 2 + tw / 2 + 50, cy + 60), radius=60, fill=mix(bg, cbg, k))
        d.text((W / 2, cy), sc["chip"], font=fc, fill=mix(bg, ctx, k), anchor="mm")
    # footer + progress bar
    ff = font(38, "Bold")
    d.text((W / 2, 1700), footer, font=ff, fill=mix(bg, fg, 0.55), anchor="mm", direction=DIR)
    d.rectangle((0, H - 14, W, H), fill=mix(bg, (0, 0, 0), 0.25))
    pw = int(W * p_total)
    if RTL: d.rectangle((W - pw, H - 14, W, H), fill=INK if bgname == "accent" else tuple(accent))
    else: d.rectangle((0, H - 14, pw, H), fill=INK if bgname == "accent" else tuple(accent))
    return im

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-800:]); sys.exit(1)

def main(path):
    global RTL, DIR, DARK
    job = json.load(open(path)); base_dir = os.path.dirname(os.path.abspath(path))
    RTL = job.get("rtl", True); DIR = "rtl" if RTL else "ltr"
    if job.get("dark"): DARK = tuple(job["dark"])
    accent = job.get("accent", [255, 196, 0]); footer = job.get("footer", "")
    scenes = job["scenes"]
    out = os.path.normpath(os.path.join(base_dir, job["out"])); os.makedirs(os.path.dirname(out), exist_ok=True)
    base = out[:-4]
    starts, acc = [], 0.0
    for s in scenes: starts.append(acc); acc += s.get("dur", 2.5)
    dur = acc
    tmp = tempfile.mkdtemp()
    vid = os.path.join(tmp, "v.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", vid],
                         stdin=subprocess.PIPE)
    thumbs = []
    for i in range(int(dur * FPS)):
        t = i / FPS
        n = max(k for k, s in enumerate(starts) if s <= t + 1e-9)
        im = scene_frame(scenes[n], t - starts[n], accent, footer, t / dur)
        p.stdin.write(im.tobytes())
        if abs((t - starts[n]) - min(scenes[n].get("dur", 2.5) - 0.1, 0.6 + 0.45 * len(scenes[n].get("items", [])) + 0.4)) < 0.5 / FPS:
            thumbs.append(im.resize((216, 384)))
    p.stdin.close(); p.wait()
    run(f'ffmpeg -v error -y -i "{vid}" -f lavfi -i anullsrc=r=44100:cl=stereo -c:v copy -c:a aac -b:a 64k -shortest -movflags +faststart "{out}"')
    mb = job.get("max_mb", 8.0); br = int(mb * 8 * 1024 / dur - 80)
    run(f'ffmpeg -v error -y -i "{out}" -vf scale=720:1280:flags=lanczos -c:v libx264 -preset slow -b:v {br}k -maxrate {br*3//2}k '
        f'-bufsize {br*2}k -c:a aac -b:a 64k -movflags +faststart "{base}_upload.mp4"')
    if thumbs:
        cols = min(6, len(thumbs)); rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 216, rows * 384), (0, 0, 0))
        for k, th in enumerate(thumbs): sheet.paste(th, ((k % cols) * 216, (k // cols) * 384))
        sheet.save(base + "_sync.jpg", quality=85)
    print("OK", out, f"{dur:.1f}s", f"{len(scenes)} scenes")

if __name__ == "__main__":
    main(sys.argv[1])
