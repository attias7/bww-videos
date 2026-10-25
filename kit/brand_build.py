#!/usr/bin/env python3
"""Generic reel builder for the brands without their own kit (Remodel in 360, SetToRank).
It is the Sign Build Run builder (../sbr/kit/sbr_build.py) with the accent colour swapped.

Usage: python3 brand_build.py job.json      (same job format as ../sbr/README.md)

Extra job key:
  "accent": [r, g, b]   replaces the yellow highlight / hook-card / progress-bar colour.
Set "music_vol": 0 for a voice-only track (the trending sound is added in the app).
"""
import os, sys, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sbr_build", os.path.join(HERE, "..", "sbr", "kit", "sbr_build.py"))
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)

if __name__ == "__main__":
    job = json.load(open(sys.argv[1]))
    if job.get("accent"):
        S.COL["y"] = tuple(job["accent"])
    S.main(sys.argv[1])
