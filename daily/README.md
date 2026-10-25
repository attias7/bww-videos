# Daily 4-brand run (cloud only)

Every morning one scheduled task makes **one new reel for each of the 4 accounts** and emails Adi
(adiattias2003@gmail.com) the pack before **09:30 Israel time**: download link, caption, TikTok title,
and a trending sound for TikTok and for Instagram.
Since 2026-10-25 (Adi: "each day post in those 6 accounts"): Sign Build Run, Remodel in 360 and SetToRank post
themselves at their time on **Instagram (Reel published, built-in music)** and **TikTok (draft sent to the account's
inbox; Adi adds the trending sound and taps Post)** via the "Auto-post due videos" task. Unscouted stays manual (email).

## Skills to load (if available in the run)
- `hormozi-hooks`: every hook (draft 5, keep the best).
- `sign-build-run-reels`: Sign Build Run script + brand rules (ignore its Publer/scheduling/voice-download steps).
- `tiktok-studio`: what the TikTok algorithm rewards now (first 2 s, retention, length, caption/title) for all 4 brands.
- `humanizer`: one pass over every caption so it doesn't read like AI.
- `grand-slam-offer` / `landing-page-copy`: only for the occasional soft product-mention reel (offer wording).
Ignore any step in a skill that posts, schedules, uses Buffer/Publer/Metricool, the Mac, Chrome or device tools.
Started 2026-10-25. It replaces the old Sunday/Wednesday batch runs and the old Mac/Chrome download step.

Everything runs in the cloud container. **Never use the Mac, Chrome, computer use or device tools.**
ElevenLabs audio is downloaded with plain `curl` from the `content_url` (storage.googleapis.com works).
The daily run never posts itself. Posting happens only through `social/publish_due.py` (the "Auto-post due videos" task),
for the accounts listed in social/SETUP.md. Never use Buffer, Publer or Metricool.

## The 4 brands

| brand | builder | voice (ElevenLabs) | job folder | series / accent | post time (Israel) |
|---|---|---|---|---|---|
| Sign Build Run | `sbr/kit/sbr_build.py` | Arthur `sfJopaWaOtauCD3HKX6Q`, `eleven_v4`, lines end `...` | `sbr/jobs/epNN.json` | `NO COLD CALLS · EP. N`, yellow | 19:00 |
| Unscouted | `unscouted/kit/us_build.py` | Archie `kmSVBPu7loj4ayNinwWM`, `eleven_v3`, lines end `...` | `unscouted/jobs/epNN.json` | `PAUSE & DECIDE · #N` or `PLAYER BREAKDOWN · NAME`, lime | 19:00 |
| Remodel in 360 | `kit/brand_build.py` | Arlo `RckSZHfvva0yOVRPzRfv`, `eleven_multilingual_v2`, `<break time="0.8s" />` between lines | `r360/jobs/dNNN.json` | `KITCHEN & BATH CONTRACTORS`, accent `[255,128,82]` | 23:00 (afternoon US Eastern) |
| SetToRank | `kit/brand_build.py` | Matt `3iY0r3RaYmOh6WfIwMIH`, `eleven_v4`, lines end `...` | `settorank/jobs/epNN.json` | `RANK & RENT · BUILD FASTER`, accent `[64,200,255]` | 23:00 (afternoon US Eastern) |

Job format and every element type: `sbr/README.md` (football elements: `unscouted/README.md`).
Good examples to copy: `sbr/jobs/ep29.json`, `unscouted/jobs/ep16.json`, `r360/jobs/d001.json`, `settorank/jobs/ep01.json`.
Always set `"music_vol": 0` (voice only, so Adi's trending sound is the music).
Avoid arrow glyphs (→) in on-screen text: Poppins has none, they render as boxes. Frame 1080x1920, keep text between y≈300 and y≈1600. Big elements: browser is 880 px tall, form 1000 px,
cards 460 px each, steps 200 px per item, checklist 170 px per item; don't stack them over other elements.

## Brand rules (short — the full rules are in each brand's files)

**Sign Build Run** (signbuildrun.com, $37 Rank & Rent Starter Kit). ICP: 18–28, introvert, dreads selling; wants own income
without sales calls. Story: "building an online business without becoming a salesman". Follow `sbr/HOOKS.md` and the
`sign-build-run-reels` skill rules: no income claims or $ earned, no fake proof, never "easy", be honest (months to rank,
first lead took ~1–3 months, leads don't always close). Real facts only: Adi is 22, introvert, 27 contractors commented
on one Facebook group post. Rotate the weekly mix (pain / tech fear / suspicion / education / talking-to-owners fear /
build-in-public / enemy or soft $37 kit mention, max 1 product mention a week). 12–18 lines, 70–110 words.
Hashtags: #rankandrent #localseo #introvert #onlinebusiness #seo #leadgeneration #sidebusiness #buildinpublic

**Unscouted** (unscoutedfootball.com). Players 15–21 without an academy. Alternate PAUSE & DECIDE and PLAYER BREAKDOWN
(never two of the same in a row; breakdowns need Adi's notes, which only live on his Mac — if you don't have them,
do PAUSE & DECIDE or THE NUMBERS instead). Follow `unscouted/HOOKS.md` + `unscouted/README.md` rules (no real footage or
player likeness, no promises of trials, never name Adi or his club). Last line:
"Follow for the next one. The free analysis test is in my bio."
Hashtags: #football #soccer #footballtips #footballtraining #soccerplayer #footballiq #<position> #unscouted

**Remodel in 360** (remodelin360.com, SaaS: 2 phone photos → 360° before/after tour, first tour free). Audience: owner-operated
US kitchen & bath remodelers. Every reel = ONE pain point, made concrete with example math ("say you give ten estimates
a month…"), product only at the end. Rotate: (1) everyone buys more leads, nobody closes more of the ones they have;
(2) losing to the cheaper bid because the client can't picture it; (3) "we'll think about it" then silence;
(4) free design as a lead magnet is too expensive; (5) late-night estimates that go nowhere. Only claim:
"our own remodeling company went from three in ten to five or six in ten". Never name that company. CTA: first tour free, link in bio.
Hashtags: #contractor #kitchenremodel #bathroomremodel #remodeling #contractorlife

**SetToRank** (settorank.com, new account, started 2026-10-25). Builds complete local-SEO WordPress lead sites for
rank-and-rent operators from a niche + city: a page per service and per nearby city (unique, not copies), titles, FAQs,
local schema, cost calculator, quote form, click-to-call, publishes to their own WordPress and routes leads by email.
Building and previewing is free; plans $47/$97/$197 a month. Audience: rank-and-rent builders (often non-technical)
who build sites by hand. Angles to rotate: time spent building by hand; duplicate "city pages" that never rank;
generic AI builders that invent reviews/licenses (SetToRank never does); owning your site (real WordPress, move it any
time); what a rank-and-rent site needs (checklists); picking a niche + nearby cities; lead routing to the renter.
Honest: it builds the site, it doesn't guarantee rankings; no invented stats, testimonials or income claims.
CTA: "Build one free. Link in bio."
Hashtags: #rankandrent #localseo #wordpress #seo #leadgeneration

## Trending sounds (in every email)

Research once per run, for TikTok and Instagram separately: WebSearch (mode extended) for "TikTok trending sounds this week
<month year>" and "Instagram trending audio this week <month year>". Only use sources dated in the last ~7 days and note the
source + date in the run log. Pick per brand a sound that fits under a voiceover (calm piano/lo-fi for Sign Build Run,
cinematic/energetic for Unscouted, calm/serious for Remodel in 360 and SetToRank). Remodel in 360 and SetToRank
are brand accounts — if they're Business accounts only the commercial library shows, so prefer sounds a source says are
cleared for business use, and always add "if it's not in your library: search <mood> in the Commercial Music Library".
Write them as `"sound_tiktok": "<Song> – <Artist> (why it fits)"`, `"sound_instagram": "..."`.
Never invent a sound or a usage count.

## Daily steps

1. D = today's Israel date. Check `runs/D_daily.done` (exists → stop, "Already done today") and `runs/D_daily.lock`
   (less than 100 min old → stop, "Previous attempt still running"). Otherwise write the lock (ISO time), commit + push.
2. For each brand, skip it if `uploads/queue.jsonl` already has a line with date D, that brand and kind "reel".
3. Numbering: SBR / Unscouted next ep = max ep in their `episodes.csv` + 1; Remodel in 360 next id = max `dNNN` in
   `r360/episodes.csv` + 1; SetToRank next ep = max in `settorank/episodes.csv` + 1. Read the last ~10 rows of each log
   and the HOOKS files first so hooks/topics/pain points never repeat.
4. If a job file for the next episode already exists but has no video in `<brand>/videos/` yet (e.g. unscouted/jobs/ep17–19.json written
   by the old batch run on 2026-10-25), reuse its lines/scenes instead of writing a new script (set "music_vol": 0).
   Write all 4 scripts (hook = Hormozi method: WHO + RESULT + EASE/OBJECTION REMOVAL, under ~10 spoken words, draft 5,
   keep the best). Then generate the 4 voices (`generations_count: 1`; poll `creative_get_flow_run_status`;
   concurrency error → wait 2 min and try once more; never re-run a success). Download each `content_url` with curl
   into `<brand>/voices/`.
5. Write the 4 jobs (for Sign Build Run, Remodel in 360 and SetToRank add `"both_mixes": true` — the builder then also
   writes `<out>_music_upload.mp4`, the Instagram version with built-in music), then build at most 2 at a time in the background
   (`cd <brand>/jobs && nohup python3 <builder> <job>.json > /tmp/<id>.log 2>&1 &`), poll until the log prints `OK`.
   "fewer speech chunks than lines" → merge lines or pass "spans" and rebuild.
6. Check every `<out>_sync.jpg` (each tile shows its own line; nothing cut or overlapping) and the frame at 0.5 s (hook).
   Fix and rebuild if needed.
7. Copy each `<out>_upload.mp4` to `<brand>/videos/<file>.mp4` (sbr/videos/sbr_epNN_<slug>.mp4,
   unscouted/videos/US_epNN_<slug>.mp4, r360/videos/r360_dNNN_<slug>.mp4, settorank/videos/str_epNN_<slug>.mp4; < 15 MB).
   For the 3 auto-posted brands also copy `<out>_music_upload.mp4` to the same name with `_ig` before `.mp4`
   (e.g. r360/videos/r360_dNNN_<slug>_ig.mp4). Commit + push, `curl -sI` each raw.githubusercontent URL → 200.
8. Queue each with `python3 uploads/queue_add.py '<json>'`: {"date": D, "time": <post time>, "brand", "kind": "reel", "ep",
   "platforms": ["Instagram (Reel)", "TikTok"], "files": [<video>], "caption", "tiktok_title": <hook>,
   "sound_tiktok", "sound_instagram", "music": "voice at 100%, sound at 5–15%",
   "notes": "TikTok: turn on the AI-generated content label (AI voice). Cover: the first frame (hook card)."}.
   Caption: line 1 = the hook, 1–3 short lines, a question or CTA, then the brand hashtags.
   AUTO-POSTING (see social/SETUP.md): for Sign Build Run, Remodel in 360 and SetToRank add `"ig_file": "<the _ig.mp4>"`
   (Instagram publishes it automatically at its time), and add `"tiktok_draft": true` only for brands with a TikTok login
   (`python3 social/tokens.py status` lists them). The separate "Auto-post due videos" task publishes them at their
   time — the daily run never posts. Unscouted stays manual (no ig_file / tiktok_draft).
   Also run `python3 social/post.py refresh` once per run (rotates the Instagram + TikTok tokens) and commit
   `social/tokens.enc` if it changed.
9. Log a row per brand in its episodes.csv (SBR/Unscouted keep their columns; r360/settorank:
   id/ep, post_date, angle, hook, topic, file, status, processed_at, notes). Mark hooks ✅ in HOOKS files where they exist.
10. `python3 uploads/render_email.py D --check --unsent` → if `missing` is empty, send with `mcp__Gmail__send_message`
    to ["adiattias2003@gmail.com"], subject/htmlBody/body from /tmp/upload_email.json; confirm with get_message;
    `python3 uploads/mark_sent.py <message id>`. If count is 0 because another task already emailed today's items, that's fine.
11. Write `runs/D_daily.done` (2–3 lines: what was made, credits used, sound sources), delete the lock, commit + push
    with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".
If something breaks partway: queue + email what's ready, delete the lock, push, and say what's missing
(the next hourly attempt only makes what's missing).
