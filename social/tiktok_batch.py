#!/usr/bin/env python3
"""Weekly TikTok batches scheduled by Adi with Claude Cowork in TikTok Studio (desktop), one account per weekday.

Each brand has a batch weekday. On that day Cowork schedules the brand's TikToks for the next 7 days
(batch day +1 … +7), picking a trending sound in TikTok Studio's Sounds panel. This script writes one page per brand,
social/tiktok_batches/<slug>.md, listing exactly those 7 posts (download link, time, caption, sound mood/suggestion),
so Cowork can work from a public URL.

Usage: python3 social/tiktok_batch.py [YYYY-MM-DD]   (default: today, Israel) — run by the daily task after building.
"""
import datetime, json, os, sys
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
Q = os.path.join(ROOT, "uploads", "queue.jsonl")
OUT = os.path.join(HERE, "tiktok_batches")
RAW = "https://raw.githubusercontent.com/attias7/bww-videos/main/"
PAGE = "https://github.com/attias7/bww-videos/blob/main/social/tiktok_batches/"
# Python weekday: Mon=0 … Sun=6
BATCH = {"Sign Build Run": (6, "sign-build-run", "Sign Build Run"),
         "Subletli": (0, "subletli", "@subletli"),
         "Remodel in 360": (1, "remodel-in-360", "@remodelin360"),
         "SetToRank": (2, "settorank", "SetToRank")}
# First post date each brand's weekly batch covers (Adi chose weekly Cowork batches on 2026-10-27). Before it, the old
# daily TikTok inbox drafts keep running ("tiktok_draft": true in the queue line).
FIRST_COVERED = {"Sign Build Run": "2026-11-02", "Subletli": "2026-11-03", "Remodel in 360": "2026-11-04", "SetToRank": "2026-11-05"}

def uses_batch(brand, date):
    """True if this brand's TikTok on this date is scheduled by the weekly Cowork batch (so: no inbox draft)."""
    return brand in FIRST_COVERED and date >= FIRST_COVERED[brand]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def next_batch_day(brand, today):
    """The next batch day (today included) whose 7-day window starts on/after the brand's first covered date."""
    wd = BATCH[brand][0]
    bd = today + datetime.timedelta(days=(wd - today.weekday()) % 7)
    while (bd + datetime.timedelta(days=1)).isoformat() < FIRST_COVERED[brand]:
        bd += datetime.timedelta(days=7)
    return bd

def batch_today(today):
    """Brands whose batch day is today."""
    return [b for b in BATCH if next_batch_day(b, today) == today]

def main():
    today = (datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1
             else datetime.datetime.now(ZoneInfo("Asia/Jerusalem")).date())
    items = [json.loads(l) for l in open(Q) if l.strip()]
    os.makedirs(OUT, exist_ok=True)
    for brand, (wd, slug, account) in BATCH.items():
        bd = next_batch_day(brand, today)
        dates = [(bd + datetime.timedelta(days=k)).isoformat() for k in range(1, 8)]
        rows = {i["date"]: i for i in items if i["brand"] == brand and i["kind"] == "reel" and i["date"] in dates}
        L = [f"# TikTok batch – {brand} ({account})", "",
             f"Schedule on **{DAYS[wd]} {bd.isoformat()}** in TikTok Studio (tiktok.com/tiktokstudio/upload), logged into **{account}**.",
             f"Covers {dates[0]} → {dates[-1]} (Israel time). Ready: {len(rows)}/7.", "",
             "For every post: download the video → Upload → paste the caption into Description → Edit video → Sounds →",
             ("pick a sound that is trending right now (For You tab / search) and fits the mood. This account has NO voiceover — "
              "the sound is the only audio, so keep it at normal volume; Hebrew trending songs are preferred → Save →") if brand == "Subletli" else
             "pick a sound that is trending right now (For You tab / search) and fits the mood → keep the voice loud, sound low (~10%) → Save →",
             "Settings: AI-generated content ON (not needed for Subletli) → Schedule → set the date and time below (Israel time) → Schedule.", ""]
        for d in dates:
            i = rows.get(d)
            if not i:
                L += [f"## {d} — NOT READY YET (skip; it will be in next week's list or the daily email)", ""]
                continue
            L += [f"## {d} at {i['time']} (Israel time)",
                  f"- Video: {RAW + i['files'][0]}",
                  f"- Sound mood: {i.get('music', '')}",
                  f"- Sound suggestion (from the trend reports when it was made): {i.get('sound_tiktok', '—')}",
                  "- Caption (paste exactly):", "", "```", i["caption"], "```", ""]
        open(os.path.join(OUT, slug + ".md"), "w").write("\n".join(L))
        print(f"{brand}: batch {bd} covers {dates[0]}..{dates[-1]} ready {len(rows)}/7 → {PAGE}{slug}.md")

if __name__ == "__main__":
    main()
