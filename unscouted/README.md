# Unscouted reel kit

Football motion-graphics reels for the Unscouted Instagram/TikTok (players 15-21 not in an academy).
Built on the Sign Build Run builder (`../sbr/kit/sbr_build.py`), re-skinned in lime with football elements.

- `kit/us_build.py job.json` builds one reel (same job format as `../sbr/README.md`, plus elements below).
- `kit/preview.py job.json out.png t1 t2 ...` renders still frames without audio (layout check, 2.2 s per line).
- `kit/carousel.py job.json ../carousels/epNN_slug` makes the 4:5 Instagram carousel from a reel job (one slide per scene, final state, start positions + arrows; max 10). Check `_sheet.jpg`.
- Voice: ElevenLabs `eleven_v3`, **Archie - English teen youth** `kmSVBPu7loj4ayNinwWM`, atempo 1.1.
- `episodes.csv` log (source of truth for post dates and used hooks). `videos/` = public upload MP4s Buffer pulls from (raw.githubusercontent). `voices/` and `out/` are git-ignored.
- Lesson notes live on the Mac only (not in this public repo): `~/Downloads/Unscouted Reels/notes/*-library.html`.
- Hook rules + bank: `HOOKS.md`. Captions: `captions.md`. Hook-scene example (lime scene 0): `jobs/pd01_v2.json`.

## Extra elements
| type | keys |
|---|---|
| pitch | y, h, zoom (0.42 = just the box), players[{id, team us/them/me, x, y, label, at, dt, path[{to:[x,y], at, dt, dur}]}], ball{x, y, with, path[{to or with, at, dt, dur}]}, arrows[{from, to, color, at, dt, label, dashed}], pause{at, dt} |
| options | y, items[{key, text, at, dt}], reveal{at, dt, correct} |
| scoreboard | y, home, away, score, minute |
| countdown | y, n, dur |

Pitch coordinates 0..1: x left→right, y 0 = the goal we attack (top), 1 = halfway line.
Put the answer reveal in its own scene (options re-listed) so "Comment A, B or C" doesn't overlap it.

## Formats
- **Pause & Decide** (series "PAUSE & DECIDE · #N"): situation on the pitch → PAUSE → A/B/C → "comment" + countdown → my pick → why (score/time/context) → "no perfect answer" → CTA free test.
- **Player breakdown** ("PLAYER BREAKDOWN · NAME"): only lessons from the user's own notes (addons/_lib/*-library.html). No match footage, no player likeness, names in text only.

## Rules
- Never use real broadcast footage or AI likenesses of real players. Tactics board only.
- The author is anonymous: no name. Say "UPSL team", never the club name.
- No promises of contracts/trials. Training content is not medical advice.
- CTA: "Free analysis test · link in bio" (unscouted site /free-test/).
