# Auto-posting setup (decided 2026-10-25)

Adi chose: **TikTok → drafts in the TikTok inbox** (he picks the trending sound and taps Post) and
**Instagram → published automatically** through Meta's API, with original music built into the video.
No Buffer / Publer / Metricool.

## Accounts
| brand | TikTok (draft to inbox) | Instagram (auto-publish Reel) |
|---|---|---|
| Sign Build Run | yes | yes |
| Unscouted | **skipped for now (2026-10-25)** – stays on the daily email, posted by hand | skipped for now |
| Remodel in 360 | yes (@remodelin360) | yes |
| SetToRank | yes (login saved 2026-10-25) | yes (new) |

## Credentials (never in chat, never in git in plain text)
Environment variables in the cloud environment settings:
`TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `IG_APP_ID`, `IG_APP_SECRET`, `IG_TOKEN_SBR`, `IG_TOKEN_R360`, `IG_TOKEN_STR`,
`SOCIAL_TOKEN_KEY` (any long random passphrase). (No Unscouted token for now.)
Per-account refresh/long-lived tokens are stored **encrypted with SOCIAL_TOKEN_KEY** in `social/tokens.enc`
(so the daily run can rotate them). Without the env vars nothing can be decrypted.

## TikTok (Content Posting API, upload to inbox)
- App at developers.tiktok.com with Login Kit + Content Posting API, scope `video.upload`. Sandbox mode with the
  4 TikTok accounts added as sandbox target users; test there first. (Direct Post is not used: unaudited apps can only
  post private and need all accounts set to private.)
- Flow: `POST https://open.tiktokapis.com/v2/post/publish/inbox/video/init/` with `source: FILE_UPLOAD` → PUT the MP4
  to `upload_url` → poll `/v2/post/publish/status/fetch/`. Adi gets an inbox notification in TikTok → adds sound → Post.
- Access tokens last 24 h; refresh with the refresh token (valid ~1 year) at every run.

## Instagram (Instagram API with Instagram Login)
- Meta app (developers.facebook.com), product "Instagram API with Instagram login", permissions
  `instagram_business_basic`, `instagram_business_content_publish`. Development mode: each IG account (Business or
  Creator) added under App roles → Instagram testers and the invite accepted in Instagram settings. No App Review needed
  for Adi's own accounts.
- Flow: `POST /{ig-user-id}/media` with `media_type=REELS`, `video_url=<raw.githubusercontent URL>`, `caption`,
  `share_to_feed=true` → poll the container `status_code` until FINISHED → `POST /{ig-user-id}/media_publish`.
- Long-lived tokens last 60 days; refresh at every run (`/refresh_access_token`).
- Video for Instagram gets built-in original music (`music_vol` 0.45, the builder's lo-fi bed); the TikTok draft uses the
  voice-only version so the trending sound is the music.

## Status
- [x] Adi created both apps with 3 accounts (SBR, R360, SetToRank) on 2026-10-25; Unscouted skipped for now
- [x] Env vars added in the environment settings (2026-10-25, plain env vars: the network-secret form only injects headers, which TikTok token exchange and 3 IG accounts on one host can't use)
- [x] TikTok logins for sbr + r360 saved in tokens.enc (2026-10-25; refresh valid 1 year). SetToRank TikTok: later.
- [x] Instagram tokens checked: @signbuildrun (creator), @remodelin360 (business), @settorank (creator); publish quota 100/day each
- [x] Adi lengthened SOCIAL_TOKEN_KEY (2026-10-25). The 2 TikTok logins were made under the old key, so they must be redone ONCE in a new session (links: social/SETUP.md) → tokens.enc is then committed with the new key. Until then the publisher skips TikTok (drafts stay on the email).
- [x] All 3 TikTok logins redone under the new key (2026-10-25): sbr (Sign Build Run), r360 (Remodelin360), str (settorank) → tokens.enc
- [x] TikTok draft test: sbr_ep29 → SEND_TO_USER_INBOX in sandbox (2026-10-25) — inbox upload works without audit
- [x] Instagram Reel test: @remodelin360 published 2026-10-25 https://www.instagram.com/reel/De6_tIuFTZw/
- [x] Switch the daily run (2026-10-25): daily/README.md step 5/8 builds both mixes and queues `ig_file` + `tiktok_draft`
  for SBR, R360, SetToRank → 6 accounts posted every day. All 6 tokens refreshed OK 2026-10-25. First auto-posted day: 2026-10-26.
- [x] publish_due.py: the 23:52 run now also sees 23:30 items (the +10 min limit no longer wraps past midnight).

## TikTok login links (state = brand key)
Make sure the browser is logged into THAT TikTok account (or use "Switch account" / incognito), click Continue, and send
back the address you land on. Then run `python3 social/connect_tiktok.py "<address>"`.
- sbr:  https://www.tiktok.com/v2/auth/authorize/?client_key=sbawrt6b7sea88xixk&scope=user.info.basic%2Cvideo.upload&response_type=code&redirect_uri=https%3A%2F%2Fsignbuildrun.com%2F&state=sbr
- r360: https://www.tiktok.com/v2/auth/authorize/?client_key=sbawrt6b7sea88xixk&scope=user.info.basic%2Cvideo.upload&response_type=code&redirect_uri=https%3A%2F%2Fsignbuildrun.com%2F&state=r360
- str:  https://www.tiktok.com/v2/auth/authorize/?client_key=sbawrt6b7sea88xixk&scope=user.info.basic%2Cvideo.upload&response_type=code&redirect_uri=https%3A%2F%2Fsignbuildrun.com%2F&state=str

## Posting times (Israel)
All 3 auto-posted brands at 23:00 Israel (US afternoon; research in daily/README.md "Posting time"), Instagram and
TikTok together. The "Auto-post due videos" task fires at 22:52 (posts what's due by 23:02) and 23:52 (retry / anything
due later that day) and posts anything not in social/posted.jsonl yet.
