#!/usr/bin/env python3
"""Sign Build Run reel builder.

Usage:  python3 sbr_build.py job.json

Turns a JSON description (spoken lines + scenes of visual elements) plus an ElevenLabs
voice MP3 into a finished 9:16 reel: motion graphics timed to the voice, original lo-fi
music ducked under the voice, cut whooshes, film grain, progress bar, series tag.

Timing: the voice is sped up (atempo), split into speech chunks with silencedetect and
aligned to `lines`. Every element has `at` (index into lines) + optional `dt` seconds;
it appears when that line starts being spoken. Each scene starts at its `from` line.

Outputs (next to `out`):
  <out>                 1080x1920 master (for your own use)
  <out>_upload.mp4      720x1280 under `max_mb` MB (default 9.0, Chrome upload limit 10)
  <out>_sync.jpg        one frame 0.45 s after each line starts (check it!)
  <out>_timing.json     line start/end times actually used
"""
import sys, os, json, math, re, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
BG = (14, 15, 19); BG2 = (22, 24, 31)
COL = {"w": (245, 245, 240), "y": (255, 214, 64), "r": (240, 72, 72), "g": (70, 210, 120),
       "b": (80, 150, 255), "grey": (150, 153, 165), "dark": (14, 15, 19)}
CARD = (30, 32, 42); EDGE = (55, 58, 72)
LEAD = 0.10

_fc = {}
def font(path, size):
    k = (path, int(size))
    if k not in _fc: _fc[k] = ImageFont.truetype(path, max(8, int(size)))
    return _fc[k]
def C(c): return COL[c] if isinstance(c, str) else tuple(c)
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def prog(t, s, d): return clamp((t - s) / d)
def mix(a, b, k): return tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))
def rrect(d, box, r, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = box
    if x1 <= x0 or y1 <= y0: return
    d.rounded_rectangle(box, radius=max(0, min(r, (x1 - x0) / 2, (y1 - y0) / 2)), fill=fill, outline=outline, width=width)

def rich_line(d, y, segs, size, alpha=1.0, fontpath=FB, bg=BG):
    f = font(fontpath, size)
    ws = [d.textlength(s, font=f) for s, _ in segs]
    if sum(ws) > W - 120:
        size *= (W - 120) / sum(ws); f = font(fontpath, size); ws = [d.textlength(s, font=f) for s, _ in segs]
    x = W / 2 - sum(ws) / 2
    for (s, c), w in zip(segs, ws):
        d.text((x, y), s, font=f, fill=mix(bg, C(c), alpha), anchor="lm"); x += w

def pop_text(d, t, st, y, segs, size, fontpath=FB, bg=BG):
    p = prog(t, st, 0.28)
    if p <= 0: return
    rich_line(d, y + (1 - ease_out(p)) * 40, segs, size * (0.82 + 0.18 * ease_back(p)), ease_out(p), fontpath, bg)

def chip(d, t, st, cx, cy, text, fill, tc, size=44, pad=34, outline=None):
    p = prog(t, st, 0.3)
    if p <= 0: return
    s = ease_back(p); f = font(FB, size * s); tw = d.textlength(text, font=f); h = size * 0.9 * s
    rrect(d, (cx - tw / 2 - pad, cy - h, cx + tw / 2 + pad, cy + h), int(h), fill=C(fill) if fill else None,
          outline=C(outline) if outline else None, width=4)
    d.text((cx, cy), text, font=f, fill=C(tc), anchor="mm")

def phone_frame(d, x, y, w, h, fill=(245, 245, 242)):
    rrect(d, (x, y, x + w, y + h), 56, fill=fill, outline=(60, 63, 75), width=10)
    rrect(d, (x + w / 2 - 70, y + 22, x + w / 2 + 70, y + 50), 14, fill=(20, 20, 24))

# ------------------------------------------------------------------ elements
# Each: fn(d, img, t, T, e) where T(e) gives the element's start time.

def el_text(d, img, t, st, e):
    pop_text(d, t, st, e["y"], e["segs"], e.get("size", 80), FM if e.get("weight") == "medium" else FB,
             C(e.get("bg", "dark")) if e.get("bg") else BG)

def el_chip(d, img, t, st, e):
    chip(d, t, st, e.get("x", W // 2), e["y"], e["text"], e.get("fill", "y"), e.get("color", "dark"),
         e.get("size", 44), e.get("pad", 34), e.get("outline"))

def el_bignum(d, img, t, st, e):
    p = prog(t, st, 0.3)
    if p > 0: d.text((W // 2, e["y"]), e["text"], font=font(FB, e.get("size", 300) * ease_back(p)), fill=C(e.get("color", "y")), anchor="mm")

def el_search(d, img, t, st, e):
    p = prog(t, st, 0.35)
    if p <= 0: return
    y = e["y"] + (1 - ease_out(p)) * 60
    rrect(d, (130, y, 950, y + 120), 60, fill=COL["w"])
    d.ellipse((170, y + 35, 220, y + 85), outline=(120, 120, 130), width=6)
    d.line((212, y + 77, 236, y + 100), fill=(120, 120, 130), width=7)
    q = e.get("query", "roof repair near me"); n = int(clamp((t - st - 0.3) / e.get("type_dur", 1.2)) * len(q))
    d.text((265, y + 60), q[:n] + ("|" if int(t * 3) % 2 == 0 and n < len(q) else ""), font=font(FM, 46), fill=(40, 40, 50), anchor="lm")

def el_arrow(d, img, t, st, e):
    p = prog(t, st, 0.4)
    if p <= 0: return
    y0, y1 = e["y"], e["y2"]
    d.line((W // 2, y0, W // 2, y0 + (y1 - y0 - 30) * ease_out(p)), fill=COL["grey"], width=8)
    if p >= 1: d.polygon([(W // 2 - 24, y1 - 30), (W // 2 + 24, y1 - 30), (W // 2, y1)], fill=COL["grey"])

def el_crossphone(d, img, t, st, e):
    q = prog(t, st, 0.3)
    if q <= 0: return
    s = ease_back(q); cx, cy = W // 2, e["y"]; g = COL["grey"]
    rrect(d, (cx - 70 * s, cy - 120 * s, cx + 70 * s, cy + 120 * s), int(26 * s), outline=g, width=10)
    d.ellipse((cx - 10, cy + 80 * s, cx + 10, cy + 100 * s), fill=g)
    k = ease_out(prog(t, st + 0.3, 0.25))
    if k > 0: d.line((cx - 140, cy - 140, cx - 140 + 280 * k, cy - 140 + 280 * k), fill=COL["r"], width=16)

def el_phone_call(d, img, t, st, e):
    """Incoming call from unknown number, declined at T(decline_at)."""
    px, py, pw, ph = W // 2 - 190, e["y"], 380, 720
    rrect(d, (px, py, px + pw, py + ph), 60, fill=(28, 30, 38), outline=(60, 63, 75), width=6)
    dec = e["_decline"]; declined = t > dec
    d.text((W // 2, py + 150), "Unknown number", font=font(FM, 38), fill=COL["grey"], anchor="mm")
    d.text((W // 2, py + 220), "Call declined" if declined else "+1 (555) 010-2233", font=font(FB, 40), fill=COL["r"] if declined else COL["w"], anchor="mm")
    if not declined:
        ph_ = (t * 2.2) % 1; r = 60 + ph_ * 70
        d.ellipse((W // 2 - r, py + 400 - r, W // 2 + r, py + 400 + r), outline=mix(BG2, COL["g"], 1 - ph_), width=5)
    d.ellipse((W // 2 - 60, py + 340, W // 2 + 60, py + 460), fill=(50, 53, 64))
    d.text((W // 2, py + 400), "?", font=font(FB, 70), fill=COL["grey"], anchor="mm")
    by = py + 600; r1 = 50 * (1 + (0.25 * math.sin(prog(t, dec - 0.3, 0.3) * math.pi) if dec - 0.3 < t < dec else 0))
    d.ellipse((W // 2 - 110 - r1, by - r1, W // 2 - 110 + r1, by + r1), fill=COL["r"])
    d.line((W // 2 - 128, by - 18, W // 2 - 92, by + 18), fill=COL["w"], width=8)
    d.line((W // 2 - 128, by + 18, W // 2 - 92, by - 18), fill=COL["w"], width=8)
    if not declined:
        d.ellipse((W // 2 + 60, by - 50, W // 2 + 160, by + 50), fill=COL["g"])
        d.arc((W // 2 + 85, by - 25, W // 2 + 135, by + 25), 200, 340, fill=COL["w"], width=8)

def el_steps(d, img, t, st, e):
    """Numbered boxes appearing one by one (items: [{text, at, dt}]); optional big red X at T(strike)."""
    for i, it in enumerate(e["items"]):
        p = prog(t, it["_t"], 0.3)
        if p <= 0: continue
        y = e["y"] + i * 200; x0 = 170 - (1 - ease_out(p)) * 300
        rrect(d, (x0, y, x0 + 740, y + 150), 28, fill=CARD, outline=EDGE, width=3)
        d.text((x0 + 50, y + 75), it["text"], font=font(FB, 56), fill=COL["w"], anchor="lm")
    if "_strike" in e:
        y0, y1 = e["y"] - 30, e["y"] + len(e["items"]) * 200 - 20
        for k, (a, b) in enumerate([((130, y1), (950, y0)), ((130, y0), (950, y1))]):
            sp = ease_out(prog(t, e["_strike"] + k * 0.2, 0.3))
            if sp > 0: d.line((a[0], a[1], a[0] + (b[0] - a[0]) * sp, a[1] + (b[1] - a[1]) * sp), fill=COL["r"], width=18)

def el_battery(d, img, t, st, e):
    bp = prog(t, st, 1.2); bx, by = W // 2 - 170, e["y"]
    rrect(d, (bx, by, bx + 320, by + 120), 18, outline=COL["grey"], width=6)
    d.rectangle((bx + 320, by + 38, bx + 340, by + 82), fill=COL["grey"])
    d.rectangle((bx + 14, by + 14, bx + 14 + 292 * (0.35 * (1 - ease_out(bp)) + 0.05), by + 106), fill=COL["r"])
    d.text((W // 2, by + 180), e.get("label", "social battery"), font=font(FM, 40), fill=COL["grey"], anchor="mm")

def el_browser(d, img, t, st, e):
    """Browser window whose page blocks build in one by one."""
    bx, by, bw, bh = 110, e["y"], 860, 880
    rrect(d, (bx, by, bx + bw, by + bh), 30, fill=(250, 250, 248))
    rrect(d, (bx, by, bx + bw, by + 90), 30, fill=(232, 233, 236)); d.rectangle((bx, by + 45, bx + bw, by + 90), fill=(232, 233, 236))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((bx + 36 + i * 42, by + 32, bx + 62 + i * 42, by + 58), fill=c)
    rrect(d, (bx + 180, by + 25, bx + bw - 40, by + 65), 20, fill=COL["w"])
    d.text((bx + 205, by + 45), e.get("url", "roofrepair-smalltown.com"), font=font(FM, 28), fill=(90, 90, 100), anchor="lm")
    blocks = [((bx + 40, by + 130, bx + bw - 40, by + 360), (30, 40, 60), e.get("title", "Roof Repair in Smalltown"), COL["w"], 44),
              ((bx + 40, by + 390, bx + 500, by + 450), (220, 222, 228), None, None, 0),
              ((bx + 40, by + 470, bx + 420, by + 530), (220, 222, 228), None, None, 0),
              ((bx + 40, by + 580, bx + 440, by + 690), COL["y"], e.get("button", "Get a free quote"), (20, 20, 20), 40),
              ((bx + 40, by + 730, bx + 250, by + 840), (225, 228, 236), None, None, 0),
              ((bx + 290, by + 730, bx + 540, by + 840), (225, 228, 236), None, None, 0),
              ((bx + 580, by + 730, bx + bw - 40, by + 840), (225, 228, 236), None, None, 0)]
    for i, (box, col, txt, tc, ts) in enumerate(blocks):
        p = prog(t, st + i * 0.28, 0.25)
        if p <= 0: continue
        x0, y0, x1, y1 = box; cy = (y0 + y1) / 2; hh = (y1 - y0) / 2 * ease_out(p)
        rrect(d, (x0, cy - hh, x1, cy + hh), 16, fill=col)
        if txt and p > 0.8: d.text(((x0 + x1) / 2 if i == 0 else x0 + 30, cy), txt, font=font(FB, ts), fill=tc, anchor="mm" if i == 0 else "lm")

def el_mappin(d, img, t, st, e):
    p = prog(t, st, 0.35)
    if p <= 0: return
    cy0 = e["y"]
    for k in range(6):
        d.line((200, cy0 - 90 + k * 60, 880, cy0 - 110 + k * 70), fill=(40, 43, 55), width=3)
        d.line((260 + k * 120, cy0 - 140, 220 + k * 130, cy0 + 270), fill=(40, 43, 55), width=3)
    cx, cy = W // 2, cy0 + (1 - ease_back(p)) * -200
    d.ellipse((cx - 70, cy - 150, cx + 70, cy - 10), fill=COL["r"])
    d.polygon([(cx - 58, cy - 55), (cx + 58, cy - 55), (cx, cy + 60)], fill=COL["r"])
    d.ellipse((cx - 28, cy - 108, cx + 28, cy - 52), fill=BG)

def el_flow(d, img, t, st, e):
    """Vertical flowchart; nodes: [{label, color, at, dt}]."""
    for i, nd in enumerate(e["nodes"]):
        s0 = nd["_t"]; p = prog(t, s0, 0.3)
        if p <= 0: continue
        y = e["y"] + i * e.get("gap", 240)
        if i > 0:
            ap = prog(t, s0 - 0.25, 0.25)
            d.line((W // 2, y - 90, W // 2, y - 90 + 80 * ease_out(ap)), fill=COL["grey"], width=8)
            if ap >= 1: d.polygon([(W // 2 - 20, y - 25), (W // 2 + 20, y - 25), (W // 2, y - 5)], fill=COL["grey"])
        s = ease_back(p); hw, hh = 400 * s, 70 * s; c = C(nd.get("color", "w"))
        rrect(d, (W // 2 - hw, y + 70 - hh, W // 2 + hw, y + 70 + hh), int(34 * s), fill=CARD, outline=c, width=5)
        d.ellipse((W // 2 - hw + 40, y + 55, W // 2 - hw + 70, y + 85), fill=c)
        d.text((W // 2 + 20, y + 70), nd["label"], font=font(FB, 42 * s), fill=COL["w"], anchor="mm")

def el_google_phone(d, img, t, st, e):
    """Phone with Google search typing `query`."""
    px, py, pw, ph = 190, e["y"], 700, 1140
    p = prog(t, st, 0.35)
    if p <= 0: return
    oy = (1 - ease_out(p)) * 300
    phone_frame(d, px, py + oy, pw, ph)
    d.text((W // 2, py + oy + 170), "Google", font=font(FB, 90), fill=COL["b"], anchor="mm")
    rrect(d, (px + 50, py + oy + 260, px + pw - 50, py + oy + 350), 45, fill=COL["w"], outline=(210, 210, 215), width=3)
    q = e.get("query", "roof repair near me"); n = int(clamp((t - st - 0.8) / 1.6) * len(q))
    d.text((px + 90, py + oy + 305), q[:n] + ("|" if int(t * 3) % 2 == 0 else ""), font=font(FM, 40), fill=(40, 40, 50), anchor="lm")

def el_results(d, img, t, st, e):
    """Phone showing search results; items [[domain,title,sub]]; `mine` index highlighted."""
    px, py, pw, ph = 190, e["y"], 700, 1220
    phone_frame(d, px, py, pw, ph)
    rrect(d, (px + 50, py + 90, px + pw - 50, py + 170), 40, fill=COL["w"], outline=(210, 210, 215), width=3)
    d.text((px + 90, py + 130), e.get("query", "roof repair near me"), font=font(FM, 36), fill=(40, 40, 50), anchor="lm")
    mine = e.get("mine", 0)
    for i, (dom, title, sub) in enumerate(e["items"]):
        q = prog(t, st + i * 0.15, 0.3)
        if q <= 0: continue
        y = py + 230 + i * 250 + (1 - ease_out(q)) * 40; hl = i == mine
        rrect(d, (px + 40, y, px + pw - 40, y + 210), 24, fill=(255, 246, 205) if hl else COL["w"], outline=COL["y"] if hl else (225, 225, 230), width=6 if hl else 2)
        d.text((px + 80, y + 60), dom, font=font(FM, 26), fill=(30, 120, 60), anchor="lm")
        d.text((px + 80, y + 110), title, font=font(FB, 36), fill=(26, 60, 170), anchor="lm")
        d.text((px + 80, y + 160), sub, font=font(FM, 30), fill=(90, 90, 100), anchor="lm")
    if e.get("label"): chip(d, t, st + 0.6, W // 2 + 170, py + 215 + mine * 250, e["label"], "y", "dark", 34, 24)

def el_form(d, img, t, st, e):
    """Quote form: fields [[label,value]] type in, button flashes, optional notification."""
    bx, by, bw = 150, e["y"], 780
    rrect(d, (bx, by, bx + bw, by + 1000), 34, fill=(250, 250, 248))
    d.text((bx + 60, by + 90), e.get("title", "Get a free roof quote"), font=font(FB, 50), fill=(25, 30, 45), anchor="lm")
    for i, (lab, val) in enumerate(e["fields"]):
        y = by + 190 + i * 210
        d.text((bx + 60, y), lab, font=font(FM, 32), fill=(90, 90, 100), anchor="lm")
        rrect(d, (bx + 60, y + 35, bx + bw - 60, y + 135), 18, fill=COL["w"], outline=(210, 210, 216), width=3)
        n = int(clamp((t - st - 0.15 - i * 0.3) / 0.3) * len(val))
        d.text((bx + 90, y + 85), val[:n], font=font(FM, 38), fill=(30, 30, 40), anchor="lm")
    sp = prog(t, st + 1.05, 0.15)
    rrect(d, (bx + 60, by + 820, bx + bw - 60, by + 930), 24, fill=mix(COL["y"], (230, 180, 20), math.sin(sp * math.pi)))
    d.text((W // 2, by + 875), e.get("button", "Send my quote request"), font=font(FB, 42), fill=BG, anchor="mm")
    if e.get("notif"):
        q = prog(t, st + 1.2, 0.3)
        if q > 0:
            y = by + 1070 + (1 - ease_back(q)) * 120
            rrect(d, (140, y, 940, y + 150), 34, fill=CARD, outline=COL["g"], width=5)
            d.ellipse((180, y + 50, 230, y + 100), fill=COL["g"])
            d.text((260, y + 55), e["notif"][0], font=font(FB, 44), fill=COL["w"], anchor="lm")
            d.text((260, y + 105), e["notif"][1], font=font(FM, 32), fill=COL["grey"], anchor="lm")

def el_chat(d, img, t, st, e):
    """Chat window with the USER's own outgoing messages only (never invent replies)."""
    y0 = e["y"]
    rrect(d, (120, y0, 960, y0 + 1020), 40, fill=(24, 26, 34), outline=EDGE, width=3)
    d.ellipse((170, y0 + 40, 250, y0 + 120), fill=(70, 90, 130))
    d.text((210, y0 + 80), e.get("name", "Local Roofer")[0], font=font(FB, 44), fill=COL["w"], anchor="mm")
    d.text((280, y0 + 63), e.get("name", "Local Roofer"), font=font(FB, 40), fill=COL["w"], anchor="lm")
    d.text((280, y0 + 105), e.get("sub", ""), font=font(FM, 28), fill=COL["grey"], anchor="lm")
    d.line((120, y0 + 160, 960, y0 + 160), fill=EDGE, width=2)
    y = y0 + 220
    for k, m in enumerate(e["messages"]):
        q = prog(t, st + 0.2 + k * 0.8, 0.3)
        if q <= 0: continue
        f = font(FM, 38); lines = m.split("\n")
        bw = max(d.textlength(l, font=f) for l in lines) + 70; bh = 60 * len(lines) + 40; s = ease_back(q)
        rrect(d, (920 - bw, y, 920, y + bh * s), 30, fill=COL["b"])
        if s > 0.8:
            for j, l in enumerate(lines): d.text((955 - bw, y + 50 + j * 60), l, font=f, fill=COL["w"], anchor="lm")
        y += bh + 40

def el_cards(d, img, t, st, e):
    """Stacked outcome cards: items [{head,big,sub,color,at,dt}]."""
    for i, c in enumerate(e["items"]):
        q = prog(t, c["_t"], 0.3)
        if q <= 0: continue
        s = ease_back(q); y = e["y"] + i * e.get("gap", 560); col = C(c.get("color", "g"))
        rrect(d, (130, y, 950, y + 460 * s), 40, fill=CARD, outline=col, width=6)
        if s > 0.8:
            d.text((W // 2, y + 90), c["head"], font=font(FB, 56), fill=COL["w"], anchor="mm")
            d.text((W // 2, y + 250), c["big"], font=font(FB, 190), fill=col, anchor="mm")
            d.text((W // 2, y + 390), c.get("sub", ""), font=font(FM, 44), fill=COL["grey"], anchor="mm")

def el_calendar(d, img, t, st, e):
    labels = e.get("labels", ["M1", "M2", "M3"]); n = len(labels)
    for i, lab in enumerate(labels):
        cp = prog(t, st + i * 0.3, 0.25)
        if cp <= 0: continue
        s = ease_back(cp); x = W // 2 - (n - 1) * 120 + i * 240; y = e["y"]
        rrect(d, (x - 90 * s, y - 100 * s, x + 90 * s, y + 100 * s), 18, fill=(245, 245, 240))
        d.rectangle((x - 90 * s, y - 100 * s, x + 90 * s, y - 50 * s), fill=COL["r"])
        d.text((x, y + 20), lab, font=font(FB, 60 * s), fill=(30, 30, 30), anchor="mm")

def el_shield(d, img, t, st, e):
    q = prog(t, st, 0.3)
    if q <= 0: return
    s = ease_back(q); cx, cy = W // 2, e["y"]
    d.polygon([(cx - 110 * s, cy - 120 * s), (cx + 110 * s, cy - 120 * s), (cx + 110 * s, cy + 10 * s), (cx, cy + 130 * s), (cx - 110 * s, cy + 10 * s)], fill=COL["g"])
    d.line((cx - 50 * s, cy, cx - 10 * s, cy + 40 * s, cx + 60 * s, cy - 50 * s), fill=BG, width=max(1, int(18 * s)), joint="curve")

def el_checklist(d, img, t, st, e):
    """Items [{text, ok(bool), at, dt}] with green check / red x."""
    for i, it in enumerate(e["items"]):
        p = prog(t, it["_t"], 0.3)
        if p <= 0: continue
        y = e["y"] + i * 170; x0 = 150 - (1 - ease_out(p)) * 200
        rrect(d, (x0, y, x0 + 780, y + 130), 26, fill=CARD, outline=EDGE, width=3)
        ok = it.get("ok", True); c = COL["g"] if ok else COL["r"]
        d.ellipse((x0 + 35, y + 35, x0 + 95, y + 95), fill=c)
        if ok: d.line((x0 + 50, y + 66, x0 + 62, y + 80, x0 + 82, y + 50), fill=BG, width=8)
        else:
            d.line((x0 + 52, y + 52, x0 + 78, y + 78), fill=BG, width=8); d.line((x0 + 52, y + 78, x0 + 78, y + 52), fill=BG, width=8)
        d.text((x0 + 125, y + 65), it["text"], font=font(FB, 46), fill=COL["w"], anchor="lm")

def el_versus(d, img, t, st, e):
    """Two columns: left (bad, red) vs right (good, green); rows [[left,right]]."""
    lh, rh = e.get("heads", ["Them", "Me"])
    p = prog(t, st, 0.3)
    if p <= 0: return
    y0 = e["y"]
    for k, (hd, col, x) in enumerate([(lh, COL["r"], 290), (rh, COL["g"], 790)]):
        rrect(d, (x - 230, y0, x + 230, y0 + 100), 30, fill=col)
        d.text((x, y0 + 50), hd, font=font(FB, 44), fill=BG, anchor="mm")
    for i, (a, b) in enumerate(e["rows"]):
        q = prog(t, st + 0.3 + i * e.get("step", 0.5), 0.3)
        if q <= 0: continue
        y = y0 + 150 + i * 150
        for txt, x in ((a, 290), (b, 790)):
            f = font(FM, 38)
            if d.textlength(txt, font=f) > 440: f = font(FM, 38 * 440 / d.textlength(txt, font=f))
            d.text((x, y + 50), txt, font=f, fill=mix(BG, COL["w"], ease_out(q)), anchor="mm")
        d.line((W // 2, y, W // 2, y + 100), fill=EDGE, width=3)

ELEMENTS = {"text": el_text, "chip": el_chip, "bignum": el_bignum, "search": el_search, "arrow": el_arrow,
            "crossphone": el_crossphone, "phone_call": el_phone_call, "steps": el_steps, "battery": el_battery,
            "browser": el_browser, "mappin": el_mappin, "flow": el_flow, "google_phone": el_google_phone,
            "results": el_results, "form": el_form, "chat": el_chat, "cards": el_cards, "calendar": el_calendar,
            "shield": el_shield, "checklist": el_checklist, "versus": el_versus}

# ------------------------------------------------------------------ timing
def run(cmd): return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def speech_chunks(wav, noise, dur_min):
    r = run(f'ffmpeg -hide_banner -i "{wav}" -af silencedetect=n={noise}dB:d={dur_min} -f null -')
    total = float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{wav}"').stdout)
    ev = re.findall(r"silence_(start|end): ([0-9.]+)", r.stderr)
    chunks, cur = [], 0.0
    for kind, v in ev:
        v = float(v)
        if kind == "start":
            if v - cur > 0.12: chunks.append([cur, v])
        else: cur = v
    if total - cur > 0.12: chunks.append([cur, total])
    return chunks, total

def align(chunks, lines):
    """Group consecutive chunks into len(lines) groups; expected duration ∝ words; prefer big gaps."""
    n, m = len(lines), len(chunks)
    words = [max(1, len(re.findall(r"[A-Za-z0-9$%']+", l))) for l in lines]
    speech = sum(e - s for s, e in chunks); k = speech / sum(words)
    INF = 1e18; dp = [[INF] * (m + 1) for _ in range(n + 1)]; bk = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        for j in range(i, m + 1):
            for p in range(i - 1, j):
                if dp[i - 1][p] >= INF: continue
                dur = chunks[j - 1][1] - chunks[p][0]
                gap = (chunks[j][0] - chunks[j - 1][1]) if j < m else 0.6
                c = dp[i - 1][p] + ((dur - k * words[i - 1]) / (k * words[i - 1] + 0.3)) ** 2 - 0.8 * min(gap, 0.8)
                if c < dp[i][j]: dp[i][j] = c; bk[i][j] = p
    spans, j = [], m
    for i in range(n, 0, -1):
        p = bk[i][j]; spans.append([chunks[p][0], chunks[j - 1][1]]); j = p
    return spans[::-1]

def resolve_times(job, spans):
    starts = [s + LEAD for s, _ in spans]
    def T(e):
        if "at" not in e: return None
        return starts[e["at"]] + e.get("dt", 0.0)
    return starts, T

# ------------------------------------------------------------------ main
def main(jobpath):
    job = json.load(open(jobpath)); jdir = os.path.dirname(os.path.abspath(jobpath))
    out = os.path.join(jdir, job["out"]) if not os.path.isabs(job["out"]) else job["out"]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    base = os.path.splitext(out)[0]
    tmp = tempfile.mkdtemp(prefix="sbr_")
    voice = job["voice"] if os.path.isabs(job["voice"]) else os.path.join(jdir, job["voice"])
    fast = os.path.join(tmp, "vo_fast.wav")
    run(f'ffmpeg -v error -y -i "{voice}" -af atempo={job.get("atempo", 1.1)} -ac 1 -ar 44100 "{fast}"')
    lines = job["lines"]
    if job.get("spans"):
        spans = job["spans"]; total = float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{fast}"').stdout)
    else:
        spans = None
        for noise, dmin in [(-35, 0.12), (-35, 0.08), (-32, 0.08), (-30, 0.06)]:
            chunks, total = speech_chunks(fast, noise, dmin)
            if len(chunks) >= len(lines): spans = align(chunks, lines); break
        if spans is None:
            print("ERROR: fewer speech chunks than lines. Chunks found:")
            for c in chunks: print(f"  {c[0]:.2f}-{c[1]:.2f}")
            print("Merge lines in the job or pass \"spans\": [[start,end],...] by hand."); sys.exit(2)
    starts, T = resolve_times(job, spans)
    DUR = round(max(total + LEAD, spans[-1][1] + LEAD) + job.get("tail", 0.9), 2)

    # resolve scenes and element times
    scenes = job["scenes"]
    for k, sc in enumerate(scenes):
        sc["_s"] = 0.0 if k == 0 else starts[sc["from"]] - 0.15
    for k, sc in enumerate(scenes):
        sc["_e"] = scenes[k + 1]["_s"] if k + 1 < len(scenes) else 999
        for e in sc["elements"]:
            e["_st"] = T(e) if "at" in e else sc["_s"] + e.get("dt", 0.15)
            for key in ("items", "nodes"):
                for it in e.get(key, []) if isinstance(e.get(key), list) else []:
                    if isinstance(it, dict): it["_t"] = T(it) if "at" in it else e["_st"] + it.get("dt", 0)
            if "decline_at" in e: e["_decline"] = starts[e["decline_at"]] + e.get("decline_dt", 0.3)
            if e.get("type") == "phone_call" and "_decline" not in e: e["_decline"] = e["_st"] + 2.0
            if "strike_at" in e: e["_strike"] = starts[e["strike_at"]] + e.get("strike_dt", 0.2)
    cuts = [sc["_s"] for sc in scenes[1:]]
    flash = [sc["_s"] for sc in scenes if sc.get("bg") == "yellow"]

    # background
    yy = np.linspace(0, 1, H)[:, None]; bgarr = np.zeros((H, W, 3), np.float32)
    for i in range(3): bgarr[..., i] = BG[i] * (1 - yy * 0.3) + BG2[i] * (yy * 0.3)
    xx = np.linspace(-1, 1, W)[None, :]; y2 = np.linspace(-1, 1, H)[:, None]
    bgarr = (bgarr * (1 - 0.35 * np.clip(xx ** 2 + y2 ** 2 * 0.6, 0, 1))[..., None]).astype(np.uint8)
    rng = np.random.default_rng(7); grains = [np.clip(rng.normal(0, 7, (H // 2, W // 2)), -20, 20).astype(np.int16) for _ in range(6)]
    series = job.get("series")

    def frame(i):
        t = i / FPS
        img = Image.fromarray(bgarr.copy()); d = ImageDraw.Draw(img)
        for sc in scenes:
            if sc["_s"] <= t < sc["_e"]:
                if sc.get("bg") == "yellow":
                    img.paste(mix(BG, COL["y"], ease_out(prog(t, sc["_s"], 0.15))), (0, 0, W, H)); d = ImageDraw.Draw(img)
                for e in sc["elements"]:
                    if t >= e["_st"] - 0.001:
                        ELEMENTS[e["type"]](d, img, t, e["_st"], e)
                break
        if series:
            f = font(FB, 30); tw = d.textlength(series, font=f)
            rrect(d, (W / 2 - tw / 2 - 26, 110, W / 2 + tw / 2 + 26, 170), 30, outline=(80, 83, 98), width=3)
            d.text((W // 2, 140), series, font=f, fill=COL["grey"], anchor="mm")
        d.rectangle((0, 0, W, 10), fill=(40, 42, 52)); d.rectangle((0, 0, int(W * t / DUR), 10), fill=COL["y"])
        arr = np.asarray(img)
        since = min([t - c for c in cuts if t >= c] or [99])
        if since < 0.18:
            z = 1 + 0.04 * (1 - since / 0.18); cw, ch = int(W / z), int(H / z); x0, y0 = (W - cw) // 2, (H - ch) // 2
            arr = np.asarray(Image.fromarray(arr).crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR))
        g = np.repeat(np.repeat(grains[i % 6], 2, 0), 2, 1)
        return np.clip(arr.astype(np.int16) + g[..., None], 0, 255).astype(np.uint8)

    vid = os.path.join(tmp, "video.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", vid],
                         stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); p.wait()

    # music
    tm = os.path.join(tmp, "timing.json")
    json.dump({"total": DUR, "cuts": cuts, "flip": flash[0] if flash else (cuts[0] if cuts else 3.0)}, open(tm, "w"))
    mus = os.path.join(tmp, "music.wav")
    r = subprocess.run([sys.executable, os.path.join(HERE, "sbr_music.py")], cwd=tmp, env={**os.environ, "OUT": mus}, capture_output=True, text=True)
    if r.returncode: print(r.stderr); sys.exit(1)

    mixf = (f'[1:a]adelay={int(LEAD*1000)}|{int(LEAD*1000)},aresample=44100,aformat=channel_layouts=stereo,highpass=f=70,'
            f'acompressor=threshold=-20dB:ratio=3:attack=8:release=160:makeup=3,apad=whole_dur={DUR},asplit=2[voc][sc];'
            f'[2:a]volume={job.get("music_vol", 0.45)}[mus];[mus][sc]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=400[duck];'
            f'[voc][duck]amix=inputs=2:normalize=0,alimiter=limit=0.92[a]')
    master = out
    run(f'ffmpeg -v error -y -i "{vid}" -i "{fast}" -i "{mus}" -filter_complex "{mixf}" -map 0:v -map "[a]" -c:v libx264 -preset slow '
        f'-b:v 5M -maxrate 6M -bufsize 12M -vf hqdn3d=2:2:3:3 -pix_fmt yuv420p -c:a aac -b:a 192k -t {DUR} -movflags +faststart "{master}"')
    # upload version (<max_mb) 720x1280, two-pass
    up = base + "_upload.mp4"; mb = job.get("max_mb", 9.0)
    br = int(mb * 8 * 1024 / DUR - 140)
    vf = "scale=720:1280:flags=lanczos,hqdn3d=4:4:6:6"
    pl = os.path.join(tmp, "pass")
    run(f'ffmpeg -v error -y -i "{master}" -vf "{vf}" -c:v libx264 -preset slow -b:v {br}k -maxrate {br*3//2}k -bufsize {br*2}k -pass 1 -passlogfile "{pl}" -an -f null /dev/null')
    run(f'ffmpeg -v error -y -i "{master}" -vf "{vf}" -c:v libx264 -preset slow -b:v {br}k -maxrate {br*3//2}k -bufsize {br*2}k -pass 2 -passlogfile "{pl}" -c:a aac -b:a 128k -movflags +faststart "{up}"')
    # sync sheet
    thumbs = []
    for k, s in enumerate(starts):
        fp = os.path.join(tmp, f"s{k:02d}.png")
        run(f'ffmpeg -v error -y -ss {s + 0.45:.2f} -i "{master}" -frames:v 1 -vf scale=216:-1 "{fp}"')
        if os.path.exists(fp):
            im = Image.open(fp).convert("RGB"); dd = ImageDraw.Draw(im)
            dd.rectangle((0, 330, 216, 384), fill=(0, 0, 0)); txt = lines[k]
            dd.text((4, 334), f"{k}: {txt[:34]}", font=font(FM, 12), fill=(255, 214, 64))
            dd.text((4, 352), txt[34:70], font=font(FM, 12), fill=(255, 214, 64))
            thumbs.append(im)
    if thumbs:
        cols = 8; rows = math.ceil(len(thumbs) / cols); sh = Image.new("RGB", (216 * cols, 384 * rows))
        for k, im in enumerate(thumbs): sh.paste(im, ((k % cols) * 216, (k // cols) * 384))
        sh.save(base + "_sync.jpg", quality=85)
    json.dump({"duration": DUR, "lines": [{"i": k, "text": lines[k], "start": round(s, 2), "end": round(spans[k][1] + LEAD, 2)} for k, s in enumerate(starts)]},
              open(base + "_timing.json", "w"), indent=1)
    size = os.path.getsize(up) / 1e6
    print(f"OK duration={DUR:.1f}s master={master} upload={up} ({size:.1f} MB) sync={base}_sync.jpg")

if __name__ == "__main__":
    main(sys.argv[1])
