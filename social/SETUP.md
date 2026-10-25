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
| SetToRank | yes (new) | yes (new) |

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
- [ ] New session: one-time login per account → tokens.enc
- [ ] Test with Sign Build Run (1 TikTok draft + 1 IG Reel)
- [ ] Switch the daily run: build two audio versions, post, keep a short summary email
