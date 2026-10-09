#!/usr/bin/env python3
"""Unscouted reel builder: the Sign Build Run builder (../../sbr/kit/sbr_build.py) re-skinned in
Unscouted lime, plus football elements.

Usage: python3 us_build.py job.json      (same job format as sbr; see ../README.md)

Extra element types:
  pitch      y, h(1000), players[{id, team us|them|me, x, y, label, path:[{to:[x,y], at, dt, dur}]}],
             ball{x, y, with(player id), path:[{to:[x,y]|with:id, at, dt, dur}]},
             arrows[{from:[x,y], to:[x,y], color, at, dt, label, dashed}], pause{at, dt}
             Coordinates 0..1: x left→right, y 0 = goal we attack (top), 1 = halfway line.
  options    y, items[{key, text, at, dt}], reveal{at, dt, correct}
  scoreboard y, home, away, score, minute
  countdown  y, n(3), dur(seconds per number)
"""
import os, sys, math, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sbr_build", os.path.join(HERE, "..", "..", "sbr", "kit", "sbr_build.py"))
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
from PIL import ImageDraw

LIME = (200, 242, 58)
S.COL["y"] = LIME            # every "y" highlight, chip and the progress bar become Unscouted lime
S.COL["lime"] = LIME
GRASS, GRASS2, LINE = (17, 44, 28), (20, 51, 32), (205, 222, 208)
RED = S.COL["r"]

def _pos(obj, t, ids=None, depth=0):
    """Position of a player/ball at time t following its path."""
    x, y = obj.get("x", 0.5), obj.get("y", 0.5)
    if obj.get("with") and ids and depth < 3:
        px, py = _pos(ids[obj["with"]], t, ids, depth + 1); x, y = px + 0.035, py - 0.02
    for seg in obj.get("path", []):
        st = seg["_t"]; dur = seg.get("dur", 0.6)
        if t <= st: break
        k = S.ease_out(S.clamp((t - st) / dur))
        if "with" in seg and ids:
            tx, ty = _pos(ids[seg["with"]], t, ids, depth + 1); tx += 0.035; ty -= 0.02
        else:
            tx, ty = seg["to"]
        x, y = x + (tx - x) * k, y + (ty - y) * k
    return x, y

def el_pitch(d0, img, t, st, e):
    p = S.prog(t, st, 0.35)
    if p <= 0: return
    from PIL import Image
    x0, x1 = 110, 970; w = x1 - x0; top = e["y"] + (1 - S.ease_out(p)) * 80; hv = e.get("h", 1000)
    z = e.get("zoom", 1.0); h = hv / z            # zoom<1 shows only the top part of the half (the box)
    layer = Image.new("RGBA", (S.W, S.H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    P = lambda x, y: (x0 + x * w, top + y * h)
    S.rrect(d, (x0 - 20, top - 40, x1 + 20, top + hv + 20), 30, fill=GRASS)
    for k in range(6):
        if k % 2: d.rectangle((x0, top + k * hv / 6, x1, top + (k + 1) * hv / 6), fill=GRASS2)
    lw = 5
    d.line((x0, top, x1, top), fill=LINE, width=lw); d.line((x0, top, x0, top + hv), fill=LINE, width=lw); d.line((x1, top, x1, top + hv), fill=LINE, width=lw)
    if z >= 0.999: d.line((x0, top + h, x1, top + h), fill=LINE, width=lw)
    d.rectangle((*P(0.2, 0), *P(0.8, 0.30)), outline=LINE, width=lw)
    d.rectangle((*P(0.37, 0), *P(0.63, 0.10)), outline=LINE, width=lw)
    d.rectangle((*P(0.44, -0.035), *P(0.56, 0)), outline=LINE, width=lw)
    sx, sy = P(0.5, 0.21); d.ellipse((sx - 6, sy - 6, sx + 6, sy + 6), fill=LINE)
    r = 0.135 * w; d.arc((sx - r, sy - r, sx + r, sy + r), 40, 140, fill=LINE, width=lw)
    cx, cy = P(0.5, 1.0); d.arc((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=LINE, width=lw)
    ids = {pl["id"]: pl for pl in e.get("players", []) if "id" in pl}
    # arrows (under players)
    for a in e.get("arrows", []):
        q = S.prog(t, a["_t"], 0.45)
        if q <= 0: continue
        (ax, ay), (bx, by) = P(*a["from"]), P(*a["to"]); k = S.ease_out(q)
        ex, ey = ax + (bx - ax) * k, ay + (by - ay) * k; col = S.C(a.get("color", "w"))
        if a.get("dashed"):
            n = 14
            for i in range(n):
                if i % 2: continue
                f0, f1 = i / n * k, min(k, (i + 1) / n * k)
                d.line((ax + (bx - ax) * f0, ay + (by - ay) * f0, ax + (bx - ax) * f1, ay + (by - ay) * f1), fill=col, width=8)
        else:
            d.line((ax, ay, ex, ey), fill=col, width=9)
        if q >= 1:
            ang = math.atan2(by - ay, bx - ax); L = 34
            d.polygon([(bx, by), (bx - L * math.cos(ang - 0.45), by - L * math.sin(ang - 0.45)),
                       (bx - L * math.cos(ang + 0.45), by - L * math.sin(ang + 0.45))], fill=col)
            if a.get("label"):
                S.chip(d, t, a["_t"] + 0.45, (ax + bx) / 2, (ay + by) / 2 - 10, a["label"], a.get("color", "w"), "dark", 32, 20)
    # players
    for pl in e.get("players", []):
        q = S.prog(t, pl.get("_t", st), 0.3)
        if q <= 0: continue
        x, y = P(*_pos(pl, t, ids)); s = S.ease_back(q); R = 30 * s; team = pl.get("team", "us")
        if team == "me":
            ph = (t * 1.6) % 1; rr = R + 10 + ph * 30
            d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=S.mix(GRASS, LIME, 1 - ph), width=5)
        fill = LIME if team in ("us", "me") else RED
        d.ellipse((x - R, y - R, x + R, y + R), fill=fill, outline=(15, 15, 15), width=4)
        if pl.get("label") and s > 0.8:
            f = S.font(S.FB, 30); tw = d.textlength(pl["label"], font=f)
            S.rrect(d, (x - tw / 2 - 14, y + R + 8, x + tw / 2 + 14, y + R + 52), 18, fill=(10, 12, 9))
            d.text((x, y + R + 30), pl["label"], font=f, fill=LIME if team != "them" else (255, 160, 160), anchor="mm")
    b = e.get("ball")
    if b:
        x, y = P(*_pos(b, t, ids))
        d.ellipse((x - 15, y - 15, x + 15, y + 15), fill=(250, 250, 250), outline=(20, 20, 20), width=3)
    pz = e.get("pause")
    if pz and t >= pz["_t"]:
        q = S.ease_back(S.prog(t, pz["_t"], 0.25)); cx, cy = x1 - 70, top + 30
        S.rrect(d, (cx - 150 * q, cy - 44 * q, cx + 50 * q, cy + 44 * q), int(40 * q), fill=(10, 12, 9), outline=LIME, width=4)
        if q > 0.8:
            d.rectangle((cx - 120, cy - 20, cx - 108, cy + 20), fill=LIME); d.rectangle((cx - 98, cy - 20, cx - 86, cy + 20), fill=LIME)
            d.text((cx - 25, cy), "PAUSE", font=S.font(S.FB, 30), fill=LIME, anchor="mm")
    _paste(img, layer, top - 40, top + hv + 20)

def _paste(img, layer, ya, yb):
    ya, yb = int(max(0, ya)), int(min(S.H, yb))
    box = (0, ya, S.W, yb); crop = layer.crop(box)
    img.paste(crop, box, crop)

def el_options(d, img, t, st, e):
    rv = e.get("reveal"); rt = rv["_t"] if rv else 1e9; correct = rv.get("correct") if rv else None
    for i, it in enumerate(e["items"]):
        q = S.prog(t, it["_t"], 0.3)
        if q <= 0: continue
        y = e["y"] + i * e.get("gap", 170); x0 = 130 - (1 - S.ease_out(q)) * 200
        r = S.prog(t, rt, 0.3); good = it["key"] == correct
        fill = S.mix(S.CARD, (40, 58, 18), r) if good else S.CARD
        edge = S.mix(S.EDGE, LIME, r) if good else S.EDGE
        tc = S.COL["w"] if (good or r <= 0) else S.mix(S.COL["w"], S.COL["grey"], r)
        S.rrect(d, (x0, y, x0 + 820, y + 140), 28, fill=fill, outline=edge, width=5 if good and r > 0 else 3)
        d.ellipse((x0 + 30, y + 30, x0 + 110, y + 110), fill=LIME if (good and r > 0) else (55, 58, 72))
        d.text((x0 + 70, y + 70), it["key"], font=S.font(S.FB, 44), fill=(15, 15, 15) if (good and r > 0) else S.COL["w"], anchor="mm")
        f = S.font(S.FB, 44)
        if d.textlength(it["text"], font=f) > 640: f = S.font(S.FB, 44 * 640 / d.textlength(it["text"], font=f))
        d.text((x0 + 140, y + 70), it["text"], font=f, fill=tc, anchor="lm")

def el_scoreboard(d, img, t, st, e):
    q = S.prog(t, st, 0.3)
    if q <= 0: return
    y = e["y"] - (1 - S.ease_out(q)) * 40; cx = S.W // 2
    S.rrect(d, (cx - 330, y, cx + 330, y + 96), 22, fill=(10, 12, 9), outline=(60, 64, 52), width=3)
    f = S.font(S.FB, 40)
    d.text((cx - 300, y + 48), e.get("home", "YOU"), font=f, fill=S.COL["w"], anchor="lm")
    S.rrect(d, (cx - 80, y + 14, cx + 80, y + 82), 14, fill=LIME)
    d.text((cx, y + 48), e.get("score", "1-0"), font=f, fill=(15, 15, 15), anchor="mm")
    d.text((cx + 300, y + 48), e.get("away", "THEM"), font=f, fill=S.COL["w"], anchor="rm")
    S.rrect(d, (cx - 70, y + 104, cx + 70, y + 154), 14, fill=RED)
    d.text((cx, y + 129), e.get("minute", "80'"), font=S.font(S.FB, 32), fill=S.COL["w"], anchor="mm")

def el_countdown(d, img, t, st, e):
    n = e.get("n", 3); dur = e.get("dur", 0.7); k = int((t - st) / dur)
    if k >= n: return
    frac = (t - st) / dur - k; cx, cy = S.W // 2, e["y"]; R = 110
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(55, 58, 72), width=12)
    d.arc((cx - R, cy - R, cx + R, cy + R), -90, -90 + 360 * (1 - frac), fill=LIME, width=12)
    d.text((cx, cy), str(n - k), font=S.font(S.FB, 120 * (0.85 + 0.15 * S.ease_back(min(1, frac * 4)))), fill=S.COL["w"], anchor="mm")

S.ELEMENTS.update({"pitch": el_pitch, "options": el_options, "scoreboard": el_scoreboard, "countdown": el_countdown})

# The sbr builder resolves at/dt -> _t only for dicts listed under "items"/"nodes". We list the pitch's
# nested objects there (same Python objects), and hand the builder our in-memory job.
import json as _json
class _JsonShim:
    def __init__(self, job): self.job = job
    def load(self, f): f.close(); return self.job
    def dump(self, *a, **k): return _json.dump(*a, **k)

def main(jobpath):
    job = _json.load(open(jobpath))
    for sc in job["scenes"]:
        for e in sc["elements"]:
            if e["type"] == "pitch":
                nested = []
                for pl in e.get("players", []):
                    nested.append(pl); nested += pl.get("path", [])
                if e.get("ball"): nested += e["ball"].get("path", [])
                nested += e.get("arrows", [])
                if e.get("pause"): nested.append(e["pause"])
                e["items"] = nested
            if e["type"] == "options" and e.get("reveal"):
                e["nodes"] = [e["reveal"]]
    S.json = _JsonShim(job)
    S.main(jobpath)

if __name__ == "__main__":
    main(sys.argv[1])
