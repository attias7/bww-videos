#!/usr/bin/env python3
"""Black & White Wisdom carousel builder (Instagram 4:5, 1080x1350).

Usage: python3 bww_carousel.py carousel.json
carousel.json:
  input        : source mp4 (the original pack video, for the visuals)
  hook         : {"kicker": "...", "line1": "...", "line2": "..."}   (cover slide)
  slides       : [{"text": "one idea per slide", "t": seconds-in-source-video-for-the-visual}, ...]
  caption_band : [y, h] of the source's caption text in 720x1280 coords, masked out of the visual
                 (bottom captions ~[860,110]; top captions ~[250,110])
  handle       : "@black_white_wisdom1"
  out_dir      : folder for slide_01.jpg ... slide_NN.jpg
"""
import json, os, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

job = json.load(open(sys.argv[1]))
W, H = 1080, 1350
FB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
FR = '/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf'
FL = '/usr/share/fonts/truetype/google-fonts/Poppins-Light.ttf'
if not os.path.exists(FL): FL = FR
out = job['out_dir']; os.makedirs(out, exist_ok=True)
handle = job.get('handle', '@black_white_wisdom1')
band = job.get('caption_band', [860, 110])
slides = job['slides']
N = len(slides) + 2

def font(p, s): return ImageFont.truetype(p, s)

def glow_text(img, xy_lines, blur=14):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for (x, y, txt, f, col) in xy_lines: d.text((x, y), txt, font=f, fill=col)
    g = layer.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(g); img.alpha_composite(layer)

def centered_lines(lines, f, y0, gap, col, d):
    res = []; y = y0
    for ln in lines:
        w = d.textlength(ln, font=f); res.append(((W - w) / 2, y, ln, f, col)); y += gap
    return res, y

def chrome(img, i):
    d = ImageDraw.Draw(img)
    d.text((60, H - 80), handle, font=font(FR, 26), fill=(150, 150, 150, 255))
    pg = f'{i}/{N}'; w = d.textlength(pg, font=font(FR, 26))
    d.text((W - 60 - w, H - 80), pg, font=font(FR, 26), fill=(150, 150, 150, 255))
    # thin progress line
    d.rectangle([60, H - 40, 60 + (W - 120) * i / N, H - 37], fill=(255, 255, 255, 255))
    d.rectangle([60 + (W - 120) * i / N, H - 40, W - 60, H - 37], fill=(60, 60, 60, 255))

def frame_at(t):
    p = os.path.join(out, f'_f{t:.2f}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', job['input'], '-frames:v', '1',
                    '-vf', 'scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2', p], check=True)
    im = Image.open(p).convert('RGB'); os.remove(p)
    ImageDraw.Draw(im).rectangle([0, band[0] - 20, 720, band[0] + band[1] + 20], fill=(0, 0, 0))  # hide old caption
    # visual region = the part of the frame away from the caption band
    if band[0] < 640: ry0, ry1 = band[0] + band[1] + 30, 1200
    else: ry0, ry1 = 80, band[0] - 30
    reg = im.crop((0, ry0, 720, ry1))
    g = reg.convert('L').point(lambda v: 255 if v > 40 else 0)
    bb = g.getbbox() or (0, 0, 720, ry1 - ry0)
    pad = 70
    x0, y0, x1, y1 = max(0, bb[0] - pad), max(0, bb[1] - pad), min(720, bb[2] + pad), min(ry1 - ry0, bb[3] + pad)
    # keep a sensible minimum size so tiny dots don't get blown up
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; mw, mh = max(x1 - x0, 380), max(y1 - y0, 320)
    x0, x1 = max(0, cx - mw / 2), min(720, cx + mw / 2); y0, y1 = max(0, cy - mh / 2), min(ry1 - ry0, cy + mh / 2)
    return reg.crop((int(x0), int(y0), int(x1), int(y1)))

def base():
    return Image.new('RGBA', (W, H), (0, 0, 0, 255))

# ---- cover ----
img = base(); d = ImageDraw.Draw(img); hk = job['hook']
kick, y = centered_lines([hk['kicker'].upper()], font(FR, 34), 470, 60, (190, 190, 190, 255), d)
big, y = centered_lines([hk['line1'].upper(), hk['line2'].upper()], font(FB, 92), y + 10, 110, (255, 255, 255, 255), d)
glow_text(img, kick + big, 16)
sw, _ = centered_lines(['swipe  >>>'], font(FR, 30), y + 70, 40, (150, 150, 150, 255), d)
glow_text(img, sw, 4)
chrome(img, 1); img.convert('RGB').save(os.path.join(out, 'slide_01.jpg'), quality=93)

# ---- content slides ----
for k, s in enumerate(slides):
    img = base(); d = ImageDraw.Draw(img)
    vis = frame_at(s['t'])
    maxw, maxh = 760, 620
    sc = min(maxw / vis.width, maxh / vis.height, 1.4)
    vis = vis.resize((int(vis.width * sc), int(vis.height * sc)), Image.LANCZOS)
    img.paste(vis, ((W - vis.width) // 2, 110 + (maxh - vis.height) // 2))
    txt = s['text']
    size = 58 if len(txt) < 70 else 50 if len(txt) < 110 else 44
    f = font(FB, size); per = int(1700 / size)
    lines = textwrap.wrap(txt, width=per)
    ls, _ = centered_lines(lines, f, 800 if len(lines) < 4 else 770, int(size * 1.3), (255, 255, 255, 255), d)
    glow_text(img, ls, 10)
    chrome(img, k + 2)
    img.convert('RGB').save(os.path.join(out, f'slide_{k + 2:02d}.jpg'), quality=93)

# ---- CTA ----
img = base(); d = ImageDraw.Draw(img)
a, y = centered_lines(['SAVE THIS'], font(FB, 110), 460, 130, (255, 255, 255, 255), d)
b, y = centered_lines(['FOR A HARD DAY'], font(FB, 64), y, 90, (255, 255, 255, 255), d)
c, y = centered_lines([f'follow {handle} for daily wisdom'], font(FR, 34), y + 60, 50, (170, 170, 170, 255), d)
glow_text(img, a + b + c, 16)
chrome(img, N); img.convert('RGB').save(os.path.join(out, f'slide_{N:02d}.jpg'), quality=93)

# contact sheet for checking
ims = [Image.open(os.path.join(out, f'slide_{i:02d}.jpg')).resize((270, 338)) for i in range(1, N + 1)]
cols = 4; rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * 280, rows * 348), (40, 40, 40))
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 280 + 5, (i // cols) * 348 + 5))
sheet.save(os.path.join(out, '_sheet.jpg'))
print(json.dumps({'slides': N, 'out_dir': out, 'sheet': os.path.join(out, '_sheet.jpg')}))
