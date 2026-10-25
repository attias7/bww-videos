#!/usr/bin/env python3
"""Append one post to uploads/queue.jsonl after validating it.
Usage: python3 uploads/queue_add.py '<json object>'   (run from the repo root or anywhere)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = os.path.join(ROOT, "uploads", "queue.jsonl")
BRANDS = {"Sign Build Run", "Unscouted", "Remodel in 360", "SetToRank"}

def main():
    item = json.loads(sys.argv[1])
    for k in ("date", "time", "brand", "kind", "platforms", "files", "caption"):
        if not item.get(k):
            sys.exit(f"missing field: {k}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", item["date"]):
        sys.exit("date must be YYYY-MM-DD")
    if not re.fullmatch(r"\d{2}:\d{2}", item["time"]):
        sys.exit("time must be HH:MM")
    if item["brand"] not in BRANDS:
        sys.exit(f"brand must be one of {BRANDS}")
    if item["kind"] not in ("reel", "carousel"):
        sys.exit("kind must be reel or carousel")
    for f in item["files"]:
        p = os.path.join(ROOT, f)
        if not os.path.isfile(p):
            sys.exit(f"file not in repo: {f}")
        if os.path.getsize(p) > 15 * 1024 * 1024 and not f.endswith(".zip"):
            sys.exit(f"file over 15 MB: {f}")
    existing = []
    if os.path.exists(Q):
        existing = [json.loads(l) for l in open(Q) if l.strip()]
    for e in existing:
        if (e["date"], e["brand"], e["kind"]) == (item["date"], item["brand"], item["kind"]):
            sys.exit(f"already queued: {item['brand']} {item['kind']} {item['date']}")
    with open(Q, "a") as fh:
        fh.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"queued: {item['date']} {item['time']} {item['brand']} {item['kind']}")

if __name__ == "__main__":
    main()
