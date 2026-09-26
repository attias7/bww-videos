# Sign Build Run reel kit

Motion-graphics reels for the Sign Build Run Instagram, voiced with ElevenLabs.
Used by the weekly "Sign Build Run Sunday run" scheduled task and the `sign-build-run-reels` skill.

- `kit/sbr_build.py job.json` builds one reel (see the docstring). Needs ffmpeg, Pillow, numpy, Poppins fonts.
- `kit/sbr_music.py` original lo-fi bed (called by the builder).
- `jobs/ep02_example.json` full example job (Ep. 2). Copy its structure.
- `episodes.csv` log of every episode (source of truth for numbering and for not repeating topics/hooks).
- `../runs/<date>_sbr.lock|.done` hourly-retry markers for the scheduled run.
- `out/` and `voices/` are git-ignored (videos go to Publer, not GitHub).

## Job format

```
{ "episode": 3, "series": "NO COLD CALLS · EP. 3", "hook": "...",
  "voice": "../voices/ep03.mp3", "atempo": 1.1, "out": "../out/ep03_slug.mp4",
  "lines": ["spoken line 0", "spoken line 1", ...],          # exactly what the voice says, one per pause
  "scenes": [ {"from": 0, "bg": "yellow"?, "elements": [ {...}, ... ]}, ... ] }
```

- The voice script should put `...` after every line so each line is its own speech chunk.
  The builder aligns chunks to `lines` automatically (word-count DP). If it can't, pass
  `"spans": [[start,end], ...]` (seconds in the sped-up audio).
- A scene starts 0.15 s before its `from` line is spoken and lasts until the next scene.
- Every element: `"type"`, `"at"` (line index, when it appears) + optional `"dt"` (seconds offset).
- Colors: `w` white, `y` yellow, `r` red, `g` green, `b` blue, `grey`, `dark`.
- Frame is 1080x1920. Keep text between y≈300 and y≈1600. Series tag sits at y 110–170.

| type | keys |
|---|---|
| text | y, segs [[text,color],...], size (60–120), weight "medium" |
| chip | y, text, fill, color, size, x, outline |
| bignum | y, text, size, color |
| search | y, query (search bar typing) |
| arrow | y, y2 |
| crossphone | y (phone icon crossed out) |
| phone_call | y, decline_at (line idx), decline_dt — incoming unknown call that gets declined |
| steps | y, items [{text, at, dt}], strike_at, strike_dt (big red X) |
| battery | y, label |
| browser | y, url, title, button (site blocks build in) |
| mappin | y (map grid + dropping pin) |
| flow | y, gap, nodes [{label, color, at, dt}] |
| google_phone | y, query |
| results | y, query, items [[domain,title,sub]], mine (index), label |
| form | y, title, fields [[label,value]], button, notif [title, sub] |
| chat | y, name, sub, messages [...] — ONLY the creator's own outgoing messages |
| cards | y, gap, items [{head, big, sub, color, at, dt}] |
| calendar | y, labels ["M1","M2","M3"] |
| shield | y |
| checklist | y, items [{text, ok, at, dt}] |
| versus | y, heads [left,right], rows [[left,right],...], step |

Outputs: master mp4, `_upload.mp4` (720x1280, ≤9 MB for the Chrome upload), `_sync.jpg`
(one frame 0.45 s after each line starts, labelled — check every tile matches its line) and `_timing.json`.
A build takes ~6–7 minutes.
