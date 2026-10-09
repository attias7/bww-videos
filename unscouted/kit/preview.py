"""Render still frames of a job without audio: python3 preview.py job.json out.png t1 t2 ...
Assumes each line lasts `sec` seconds (default 2.2) - only for layout checks."""
import sys, os, json
sys.argv_saved = list(sys.argv)
import us_build as U
S = U.S
from PIL import Image, ImageDraw
job = json.load(open(sys.argv[1])); outp = sys.argv[2]; times = [float(x) for x in sys.argv[3:]] or [1.0]
for sc in job["scenes"]:
    for e in sc["elements"]:
        if e["type"] == "pitch":
            nested = []
            for pl in e.get("players", []): nested.append(pl); nested += pl.get("path", [])
            if e.get("ball"): nested += e["ball"].get("path", [])
            nested += e.get("arrows", []);
            if e.get("pause"): nested.append(e["pause"])
            e["items"] = nested
        if e["type"] == "options" and e.get("reveal"): e["nodes"] = [e["reveal"]]
sec = 2.2; starts = [i * sec + 0.1 for i in range(len(job["lines"]))]
T = lambda e: starts[e["at"]] + e.get("dt", 0.0)
scenes = job["scenes"]
for k, sc in enumerate(scenes): sc["_s"] = 0.0 if k == 0 else starts[sc["from"]] - 0.15
for k, sc in enumerate(scenes):
    sc["_e"] = scenes[k + 1]["_s"] if k + 1 < len(scenes) else 999
    for e in sc["elements"]:
        e["_st"] = T(e) if "at" in e else sc["_s"] + e.get("dt", 0.15)
        for key in ("items", "nodes"):
            for it in e.get(key, []) if isinstance(e.get(key), list) else []:
                if isinstance(it, dict): it["_t"] = T(it) if "at" in it else e["_st"] + it.get("dt", 0)
tiles = []
for t in times:
    img = Image.new("RGB", (S.W, S.H), S.BG); d = ImageDraw.Draw(img)
    for sc in scenes:
        if sc["_s"] <= t < sc["_e"]:
            for e in sc["elements"]:
                if t >= e["_st"] - 0.001: S.ELEMENTS[e["type"]](d, img, t, e["_st"], e)
            break
    d.text((20, 1880), f"t={t}", font=S.font(S.FB, 30), fill=(255, 255, 0))
    tiles.append(img.resize((360, 640)))
sh = Image.new("RGB", (360 * len(tiles), 640))
for i, im in enumerate(tiles): sh.paste(im, (i * 360, 0))
sh.save(outp)
