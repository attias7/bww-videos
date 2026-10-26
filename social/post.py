#!/usr/bin/env python3
"""Post one finished video: Instagram Reel (published) and/or TikTok draft (sent to the account's inbox).

Usage:
  python3 social/post.py ig <brand> <repo-relative mp4> <caption-file>     → publishes a Reel, prints the media id
  python3 social/post.py tiktok <brand> <repo-relative mp4>                → sends a draft to the TikTok inbox
  python3 social/post.py refresh                                           → refreshes every saved token (run once per day)
brand = sbr | r360 | str | sbl (Subletli: TikTok only).  Unscouted goes through Buffer.

Credentials: env IG_TOKEN_SBR / IG_TOKEN_R360 / IG_TOKEN_STR (seed tokens), TIKTOK_CLIENT_KEY / _SECRET,
SOCIAL_TOKEN_KEY (unlocks social/tokens.enc). Never print a token.
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from tokens import load, save

RAW = "https://raw.githubusercontent.com/attias7/bww-videos/main/"
IG = "https://graph.instagram.com/v21.0"
TT = "https://open.tiktokapis.com/v2"
IG_ENV = {"sbr": "IG_TOKEN_SBR", "r360": "IG_TOKEN_R360", "str": "IG_TOKEN_STR"}

def _req(url, data=None, headers=None, method=None, timeout=60):
    r = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        return json.load(urllib.request.urlopen(r, timeout=timeout))
    except urllib.error.HTTPError as e:
        try:
            return json.load(e)
        except Exception:
            return {"error": {"message": f"HTTP {e.code}"}}

def ig_token(store, brand):
    saved = store.get("instagram", {}).get(brand, {}).get("access_token")
    return saved or os.environ[IG_ENV[brand]]

def tt_token(store, brand):
    t = store.get("tiktok", {}).get(brand)
    if not t:
        sys.exit(f"TikTok not connected for {brand}")
    return t["access_token"]

def refresh():
    store = load()
    for brand in IG_ENV:
        if not os.environ.get(IG_ENV[brand]) and brand not in store.get("instagram", {}):
            continue
        d = _req(IG.replace("/v21.0", "") + "/refresh_access_token?" + urllib.parse.urlencode(
            {"grant_type": "ig_refresh_token", "access_token": ig_token(store, brand)}))
        if "access_token" in d:
            store.setdefault("instagram", {})[brand] = {"access_token": d["access_token"], "refreshed": int(time.time())}
            print(f"ig {brand}: refreshed")
        else:
            print(f"ig {brand}: refresh failed: {d.get('error', {}).get('message', '?')[:120]}")
    for brand, t in list(store.get("tiktok", {}).items()):
        d = _req(TT + "/oauth/token/", data=urllib.parse.urlencode({
            "client_key": os.environ["TIKTOK_CLIENT_KEY"], "client_secret": os.environ["TIKTOK_CLIENT_SECRET"],
            "grant_type": "refresh_token", "refresh_token": t["refresh_token"]}).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"})
        if "access_token" in d:
            store["tiktok"][brand] = d
            print(f"tiktok {brand}: refreshed")
        else:
            print(f"tiktok {brand}: refresh failed: {d.get('error_description') or d.get('error')}")
    save(store)

def ig_post(brand, path, caption):
    store = load(); tok = ig_token(store, brand)
    me = _req(IG + "/me?" + urllib.parse.urlencode({"fields": "user_id,username", "access_token": tok}))
    uid = me["user_id"]
    # safety net: never publish the same caption twice in 36 h (e.g. if social/posted.jsonl couldn't be pushed)
    recent = _req(IG + f"/{uid}/media?" + urllib.parse.urlencode({"fields": "id,caption,timestamp,permalink", "limit": 10,
                                                                   "access_token": tok})).get("data", [])
    for m in recent:
        ts = time.mktime(time.strptime(m.get("timestamp", "1970-01-01T00:00:00+0000")[:19], "%Y-%m-%dT%H:%M:%S")) - time.timezone
        if (m.get("caption") or "").strip() == caption.strip() and time.time() - ts < 36 * 3600:
            print(json.dumps({"brand": brand, "account": me.get("username"), "media_id": m["id"],
                              "permalink": m.get("permalink", ""), "already_posted": True})); return
    c = _req(IG + f"/{uid}/media", data=urllib.parse.urlencode({
        "media_type": "REELS", "video_url": RAW + path, "caption": caption, "share_to_feed": "true",
        "access_token": tok}).encode())
    if "id" not in c:
        sys.exit("ig container failed: " + json.dumps(c.get("error", c))[:300])
    for _ in range(60):
        s = _req(IG + f"/{c['id']}?" + urllib.parse.urlencode({"fields": "status_code,status", "access_token": tok}))
        if s.get("status_code") == "FINISHED":
            break
        if s.get("status_code") in ("ERROR", "EXPIRED"):
            sys.exit("ig processing failed: " + str(s.get("status")))
        time.sleep(10)
    else:
        sys.exit("ig processing timed out")
    p = _req(IG + f"/{uid}/media_publish", data=urllib.parse.urlencode({"creation_id": c["id"], "access_token": tok}).encode())
    if "id" not in p:
        sys.exit("ig publish failed: " + json.dumps(p.get("error", p))[:300])
    link = _req(IG + f"/{p['id']}?" + urllib.parse.urlencode({"fields": "permalink", "access_token": tok})).get("permalink", "")
    print(json.dumps({"brand": brand, "account": me.get("username"), "media_id": p["id"], "permalink": link}))

def tiktok_draft(brand, path):
    store = load(); tok = tt_token(store, brand)
    f = os.path.join(ROOT, path); size = os.path.getsize(f)
    h = {"Authorization": "Bearer " + tok, "Content-Type": "application/json; charset=UTF-8"}
    d = _req(TT + "/post/publish/inbox/video/init/", data=json.dumps({"source_info": {
        "source": "FILE_UPLOAD", "video_size": size, "chunk_size": size, "total_chunk_count": 1}}).encode(), headers=h)
    if d.get("error", {}).get("code") != "ok":
        sys.exit("tiktok init failed: " + json.dumps(d.get("error"))[:300])
    up = urllib.request.Request(d["data"]["upload_url"], data=open(f, "rb").read(), method="PUT", headers={
        "Content-Type": "video/mp4", "Content-Range": f"bytes 0-{size-1}/{size}", "Content-Length": str(size)})
    urllib.request.urlopen(up, timeout=300)
    pid = d["data"]["publish_id"]
    for _ in range(30):
        s = _req(TT + "/post/publish/status/fetch/", data=json.dumps({"publish_id": pid}).encode(), headers=h)
        st = s.get("data", {}).get("status")
        if st in ("SEND_TO_USER_INBOX", "PUBLISH_COMPLETE"):
            print(json.dumps({"brand": brand, "tiktok": st, "publish_id": pid})); return
        if st == "FAILED":
            sys.exit("tiktok failed: " + str(s["data"].get("fail_reason")))
        time.sleep(10)
    sys.exit("tiktok status timed out")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "refresh":
        refresh()
    elif cmd == "ig":
        ig_post(sys.argv[2], sys.argv[3], open(sys.argv[4]).read())
    elif cmd == "tiktok":
        tiktok_draft(sys.argv[2], sys.argv[3])
