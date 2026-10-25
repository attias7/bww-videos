#!/usr/bin/env python3
"""Publish every queued post that is due now (run by the "Auto-post due videos" scheduled task).

For each line in uploads/queue.jsonl with date == today (Israel) and time <= now + 10 min:
  - Instagram: if the item has "ig_file" and the brand has an Instagram token → publish the Reel (social/post.py ig).
  - TikTok:    if the item has "tiktok_draft": true and the brand has a TikTok login in tokens.enc → send the draft.
Each success is logged in social/posted.jsonl ({key, platform, id/permalink, at}) so nothing is posted twice.
Usage: python3 social/publish_due.py [--dry-run]
Prints one JSON line per action; exit code 1 if anything failed.
"""
import datetime, json, os, subprocess, sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
Q = os.path.join(ROOT, "uploads", "queue.jsonl")
LOG = os.path.join(HERE, "posted.jsonl")
BRAND = {"Sign Build Run": "sbr", "Remodel in 360": "r360", "SetToRank": "str"}
IG_ENV = {"sbr": "IG_TOKEN_SBR", "r360": "IG_TOKEN_R360", "str": "IG_TOKEN_STR"}

def tiktok_connected():
    sys.path.insert(0, HERE)
    from tokens import load
    try:
        return set(load().get("tiktok", {}))
    except SystemExit:
        return set()

def main():
    dry = "--dry-run" in sys.argv
    now = datetime.datetime.now(ZoneInfo("Asia/Jerusalem"))
    today = now.strftime("%Y-%m-%d"); soon = now + datetime.timedelta(minutes=10)
    limit = soon.strftime("%H:%M") if soon.date() == now.date() else "23:59"  # 23:52 run must still see 23:30 items
    done = set()
    if os.path.exists(LOG):
        done = {(json.loads(l)["key"], json.loads(l)["platform"]) for l in open(LOG) if l.strip()}
    items = [json.loads(l) for l in open(Q) if l.strip()]
    tt = tiktok_connected()
    failed = False
    for i in items:
        b = BRAND.get(i["brand"])
        if not b or i["date"] != today or i["time"] > limit:
            continue
        key = f'{i["date"]}|{i["brand"]}|{i["kind"]}'
        jobs = []
        if i.get("ig_file") and os.environ.get(IG_ENV[b]) and (key, "instagram") not in done:
            jobs.append(("instagram", ["ig", b, i["ig_file"]]))
        if i.get("tiktok_draft") and b in tt and (key, "tiktok") not in done:
            jobs.append(("tiktok", ["tiktok", b, i["files"][0]]))
        for platform, args in jobs:
            if dry:
                print(json.dumps({"would_post": platform, "key": key})); continue
            cap = None
            if platform == "instagram":
                cap = os.path.join("/tmp", f"cap_{b}.txt"); open(cap, "w").write(i["caption"]); args = args + [cap]
            r = subprocess.run([sys.executable, os.path.join(HERE, "post.py"), *args], capture_output=True, text=True, timeout=900)
            if r.returncode == 0:
                res = json.loads(r.stdout.strip().splitlines()[-1])
                with open(LOG, "a") as fh:
                    fh.write(json.dumps({"key": key, "platform": platform, "result": res, "at": now.isoformat()}) + "\n")
                print(json.dumps({"posted": platform, "key": key, **res}))
            else:
                failed = True
                print(json.dumps({"failed": platform, "key": key, "error": (r.stderr or r.stdout).strip()[-300:]}))
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
