# Weekly TikTok run (make + schedule 7 videos for one brand)

Adi, 2026-10-27: "one today, 2 tomorrow, 3 the day after. Plan for a week and repeat it each week. Use /tiktok-studio
and make it relevant to each one." Plus: "add a trending sound — it can fit the video or be ~15%, we need it for reach.
No Hebrew songs."

| weekday (Israel) | brand | TikTok account (check!) | Chrome profile | covers |
|---|---|---|---|---|
| Tuesday | Sign Build Run | `sign.build.run` | attiasadi2003@gmail.com | Wed → next Tue |
| Wednesday | Remodel in 360 | `remodelin360` (Business account: commercial / Unlimited sounds only) | adiattias2003@gmail.com | Thu → next Wed |
| Thursday | SetToRank | `settorank` | generalcontractorsaltlake@gmail.com | Fri → next Thu |

One post per day at **23:00 Israel** (5 pm US Eastern), dates D+1 … D+7. First weeks: SBR 2026-10-28→11-03 (done
2026-10-27), R360 from 2026-10-29, SetToRank from 2026-10-30.

## 0. Gate
- D = today (Israel). If `runs/D_tt_<slug>.done` exists → stop ("Already done today"). If `runs/D_tt_<slug>.lock` is
  < 150 min old → stop. Else write the lock, commit, push.
- Check TikTok Studio → Posts for this account: any of D+1…D+7 already scheduled (alarm icon with that date) → skip those days.

## 1. Plan + scripts (tiktok-studio skill, BUILD mode, steps 2–5)
- Load skills if listed: `tiktok-studio`, `hormozi-hooks`, `humanizer`, and for SBR `sign-build-run-reels`
  (ignore their Publer/Buffer/posting steps).
- Research once (WebSearch, sources dated in the last ~7 days, note them in the .done file): what's working on TikTok now
  for this niche + "trending TikTok sounds this week" (US/global lists: Buffer, Metricool, SocialPilot, NewEngen).
- Brand rules, voices, builders, hashtags: `daily/README.md` ("The 4 brands" + "Brand rules"). Hooks: `sbr/HOOKS.md`
  for SBR; check the brand's `episodes.csv` so hooks/topics never repeat. SBR weekly mix: pain / tech fear / suspicion /
  education / talking-to-owners fear / build-in-public / enemy or soft $37 kit (max 1 product mention a week).
- 7 scripts, 12 lines each, ~90–100 words (≈34–37 s), hook = line 1 under 10 words, honest caveat line, soft CTA.
  Captions: hook first line, 1–2 short lines, hashtags; one humanizer pass.

## 2. Voices (ElevenLabs connector)
- `creative_generate_speech`, `generations_count: 1`, the brand's voice/model, lines end with `...`, sparse tags
  (`[intrigued]` first line, `[honest]` before "Real talk", `[warmly]` last). Several can run in parallel on one flow.
- The cloud container CAN'T download storage.googleapis.com (proxy 403). Download through Chrome instead: open the
  `content_url` in a tab, javascript_tool
  `const r=await fetch(location.href);const b=await r.blob();const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='<slug>_epNN.mp3';document.body.appendChild(a);a.click();b.size`
  → `device_stage_files` "/Users/gilattias/Downloads/<slug>_epNN.mp3" → copy from /mnt/user-data/uploads/Downloads/ into
  `<brand>/voices/epNN.mp3`. (Needs the Downloads folder connected — request it once.)

## 3. Build + check
- Jobs like `sbr/jobs/ep31.json`…`ep37.json` (SBR) or the brand's example in daily/README.md. `"music_vol": 0` (TikTok
  sound added in Studio). Build with nohup, max 2–3 at a time (2-core container), poll for `OK` in the log.
- Read every `_sync.jpg`. Known overlaps: `results` phone is ~1050 px tall (use 2 items if text sits under it),
  `calendar` is ±100 px around its y, `browser` 880 px, `form` 1000 px. Text between y 300 and 1600. Fix + rebuild.
- Check the hook frame at ~1.6 s.

## 4. Schedule in TikTok Studio (Claude in Chrome)
- `list_connected_browsers`; for each, `select_browser` and check the account with
  `fetch('https://www.tiktok.com/passport/web/account/info/?aid=1988',{credentials:'include'}).then(r=>r.json())`
  → `data.username`. Use the browser whose username matches the table. None matches / logged out → stop and report.
  Never log out, never switch accounts, never type a password; login check / code / captcha → stop and report.
- Put the video on the Mac: copy `<out>_upload.mp4` to /mnt/user-data/outputs/<slug>/<date>.mp4 →
  `device_commit_files` → "/Users/gilattias/Downloads/TikTok batch/<Brand>/<date>.mp4" → `device_stage_files` that path
  → `file_upload` from "/mnt/user-data/uploads/Downloads/TikTok batch/<Brand>/<date>.mp4" (file_upload only accepts the
  uploads folder) into the page's `input[type=file]` at tiktok.com/tiktokstudio/upload.
- Popups: "Turn on automatic content checks?" → **Cancel** (don't change settings). "New editing features" / "Phone mode"
  → Got it.
- Description: click it, cmd+a, Delete, type the caption, Escape (closes the hashtag list). Verify with
  `document.querySelector('[contenteditable=true]').innerText`.
- Sounds (right panel) → the For You tab is Israel-skewed (Hebrew/Arabic songs): **never Hebrew**. Search a sound from the
  week's US trending lists that fits the mood (SBR: upbeat/chill; R360 + SetToRank: calm/serious, Business account →
  commercial/Unlimited library only), or an English/instrumental one from For You. Click + → in Audio set Volume
  **-16 dB** (≈15%), check the original video track stays **0 dB** → Save.
- Show more → **AI-generated content** ON → "Turn on".
- When to post → **Schedule** → date picker → day; time picker: click hour items (list scrolls as you click) to reach
  23, minute 00. TikTok shows Israel time (check the default time ≈ now + 15 min).
- Button must read **Schedule** → click. Never "Post". Then Posts list → the row must show the alarm icon with
  "<Mon DD>, 11:00 PM". (A "Video published" toast also appears for scheduled posts — trust the alarm icon.)

## 5. Log + finish
- episodes.csv row per post (status "scheduled 23:00 TT (Studio)", sound used), hooks ✅ in HOOKS files.
- `runs/D_tt_<slug>.done`: table date | time | scheduled yes/no | sound, plus research sources. Delete lock, commit, push
  (Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>). Close tabs you opened.
- End with the table so Adi gets it in the push notification. If stopped partway: say exactly which dates are left.
