# Upload queue (manual posting with trending music)

Since 2026-10-21 Adi posts every reel / carousel himself from his phone so he can add
trending music. The batch runs (Sign Build Run, Unscouted, Remodel in 360) no longer
schedule anything in Buffer / Publer / Metricool. Instead they:

1. Commit the finished file(s) to this public repo (videos < 15 MB, carousel JPGs + `slides.zip`).
2. Append ONE line per post to `uploads/queue.jsonl` (see format below), commit + push.

The "Daily upload email" scheduled task runs every morning, runs
`python3 uploads/render_email.py <today>` and emails Adi everything due that day
(download links, caption ready to copy, TikTok title, posting time, platforms).

## queue.jsonl — one JSON object per line

```json
{"date": "2026-10-25", "time": "19:00", "brand": "Unscouted", "kind": "reel",
 "ep": 16, "platforms": ["Instagram @unscouted.football", "TikTok @unscouted.football"],
 "files": ["unscouted/videos/US_ep16_pd08_winger.mp4"],
 "caption": "full caption incl. hashtags (newlines allowed)",
 "tiktok_title": "short hook title (optional)",
 "music": "short mood hint for the trending sound, e.g. 'calm/tense build, low under the voice'",
 "notes": "optional: cover frame tip, anything special"}
```

- `date` / `time` = Israel date/time Adi should post it (Remodel in 360: post time for the US evening, e.g. 02:30 Israel; also give "7:30 PM US Eastern" in notes).
- `brand` one of: `Sign Build Run`, `Unscouted`, `Remodel in 360`.
- `kind`: `reel` or `carousel` (carousel `files` = the slide JPGs in order, plus the `slides.zip` as the LAST entry).
- Never queue the same brand+kind+date twice — check the file first (the queue is the source of truth for "is this day filled").
- Use `python3 uploads/queue_add.py '<json>'` to append safely (validates fields + that the files exist in the repo).
