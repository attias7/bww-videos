#!/usr/bin/env python3
"""Instagram carousel (1080x1350, 4:5) from an Unscouted reel job.

Usage: python3 carousel.py ../jobs/pd01_v2.json ../carousels/ep01_pd01   [--skip 3,5]

One slide per scene, drawn in its final state (all animations finished). Countdown elements are
dropped. The lime hook scene becomes the cover ("Swipe →"); the last scene is the CTA slide.
Output: <out_dir>/01.jpg ... NN.jpg + _sheet.jpg (contact sheet to check). Max 10 slides.
"""
import os, sys, json, copy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import us_build as U
S = U.S
from PIL import Image, ImageDraw, ImageChops

CW, CH = 1080, 1350
TOP, BOT = 150, 1225          # content area on the slide
SEC = 6.0                     # fake seconds per line: long enough that every animation has finished


def prep(job):
    for sc in job["scenes"]:
        sc["elements"] = [e for e in sc["elements"] if e["type"] != "countdown"]
        for e in sc["elements"]:
            if e["type"] == "pitch":
                nested = []
                for pl in e.get("players", []): pl.pop("path", None); nested.append(pl)   # still = start positions
                if e.get("ball"): e["ball"].pop("path", None)
                nested += e.get("arrows", [])
                e.pop("pause", None)                       # no pause overlay on a still
                e["items"] = nested
            if e["type"] == "options" and e.get("reveal"): e["nodes"] = [e["reveal"]]
    starts = [i * SEC + 0.1 for i in range(len(job["lines"]))]
    T = lambda e: starts[e["at"]] + e.get("dt", 0.0)
    sc_ = job["scenes"]
    for k, sc in enumerate(sc_): sc["_s"] = 0.0 if k == 0 else starts[sc["from"]] - 0.15
    for k, sc in enumerate(sc_):
        sc["_e"] = sc_[k + 1]["_s"] if k + 1 < len(sc_) else starts[-1] + SEC
        for e in sc["elements"]:
            e["_st"] = T(e) if "at" in e else sc["_s"] + e.get("dt", 0.15)
            for key in ("items", "nodes"):
                for it in e.get(key, []) if isinstance(e.get(key), list) else []:
                    if isinstance(it, dict): it["_t"] = T(it) if "at" in it else e["_st"] + it.get("dt", 0)


def render_scene(sc):
    t = sc["_e"] - 0.01
    yellow = sc.get("bg") == "yellow"
    bg = S.COL["y"] if yellow else S.BG
    img = Image.new("RGB", (S.W, S.H), bg); d = ImageDraw.Draw(img)
    for e in sc["elements"]:
        if t >= e["_st"] - 0.001: S.ELEMENTS[e["type"]](d, img, t, e["_st"], e)
    diff = ImageChops.difference(img, Image.new("RGB", img.size, bg)).convert("L").point(lambda v: 255 if v > 18 else 0)
    box = diff.getbbox() or (0, 0, S.W, S.H)
    return img, box, bg, yellow


def slide(sc, n, N, series, last):
    img, (x0, y0, x1, y1), bg, yellow = render_scene(sc)
    pad = 30
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(S.W, x1 + pad), min(S.H, y1 + pad)
    crop = img.crop((x0, y0, x1, y1))
    k = min(1.0, (CW - 60) / crop.width, (BOT - TOP) / crop.height)
    if k < 1: crop = crop.resize((int(crop.width * k), int(crop.height * k)), Image.LANCZOS)
    out = Image.new("RGB", (CW, CH), bg); d = ImageDraw.Draw(out)
    out.paste(crop, ((CW - crop.width) // 2, TOP + (BOT - TOP - crop.height) // 2))
    ink = S.BG if yellow else S.COL["w"]; accent = S.BG if yellow else S.COL["y"]
    grey = S.mix(ink, bg, 0.45)
    f_small = S.font(S.FB, 34)
    d.text((60, 62), series, font=f_small, fill=accent)
    tw = d.textlength(f"{n}/{N}", font=f_small); d.text((CW - 60 - tw, 62), f"{n}/{N}", font=f_small, fill=grey)
    d.text((60, CH - 92), "@unscouted.football", font=f_small, fill=grey)
    if not last:
        lab = "Swipe"; f = S.font(S.FB, 40); tw = d.textlength(lab, font=f) + 54
        col = accent
        if yellow:
            S.rrect(d, (CW - 100 - tw, CH - 112, CW - 40, CH - 40), 36, fill=S.BG); col = S.COL["y"]; xr = CW - 70
        else:
            xr = CW - 60
        d.text((xr - tw, CH - 101), lab, font=f, fill=col)
        ax, ay = xr - 4, CH - 74
        d.line((ax - 36, ay, ax, ay), fill=col, width=6); d.line((ax - 14, ay - 13, ax, ay), fill=col, width=6); d.line((ax - 14, ay + 13, ax, ay), fill=col, width=6)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    skip = set()
    if "--skip" in sys.argv: skip = {int(x) for x in sys.argv[sys.argv.index("--skip") + 1].split(",")}
    args = [a for a in args if not (skip and a == sys.argv[sys.argv.index("--skip") + 1])]
    jobp, outd = args[0], args[1]
    job = json.load(open(jobp)); job = copy.deepcopy(job); prep(job)
    scenes = [sc for i, sc in enumerate(job["scenes"]) if i not in skip][:10]
    os.makedirs(outd, exist_ok=True)
    for f in os.listdir(outd):
        if f.endswith(".jpg"): os.remove(os.path.join(outd, f))
    series = job.get("series", "UNSCOUTED")
    tiles = []
    for i, sc in enumerate(scenes):
        im = slide(sc, i + 1, len(scenes), series, i == len(scenes) - 1)
        p = os.path.join(outd, f"{i + 1:02d}.jpg"); im.save(p, quality=90); tiles.append(im)
    sh = Image.new("RGB", (270 * len(tiles), 338))
    for i, im in enumerate(tiles): sh.paste(im.resize((270, 338)), (i * 270, 0))
    sh.save(os.path.join(outd, "_sheet.jpg"), quality=85)
    print(f"{len(tiles)} slides → {outd}")


if __name__ == "__main__":
    main()
