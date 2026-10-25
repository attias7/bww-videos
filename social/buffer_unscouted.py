#!/usr/bin/env python3
"""Schedule queued Unscouted reels in Buffer (Instagram Reel + TikTok @unscouted.football), built-in music, no trending sound.

For each line in uploads/queue.jsonl with brand "Unscouted", kind "reel", no "buffer" field and date+time (Israel) at least
30 minutes in the future: create the two Buffer posts (customScheduled at that time) and write
"buffer": {"instagram": id, "tiktok": id} back into the line. A post that already exists in Buffer for that channel and
time is reused, never duplicated.
Usage: python3 social/buffer_unscouted.py [--dry-run]
Credentials: env BUFFER_API_KEY (never printed). Prints one JSON line per action; exit code 1 if anything failed.
"""
import datetime, json, os, sys, urllib.error, urllib.request
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
Q = os.path.join(ROOT, "uploads", "queue.jsonl")
API = os.environ.get("BUFFER_API_URL", "https://api.buffer.com")
RAW = "https://raw.githubusercontent.com/attias7/bww-videos/main/"
ORG = "669c489747415c2a80261cc5"
IG, TT = "6ac8ebeb6a5c39ccb661692a", "6ab6bbbcea19ca0bdee8df8a"
TZ = ZoneInfo("Asia/Jerusalem")

def gql(query, variables):
    r = urllib.request.Request(API, data=json.dumps({"query": query, "variables": variables}).encode(), headers={
        "Authorization": "Bearer " + os.environ["BUFFER_API_KEY"], "Content-Type": "application/json"})
    try:
        d = json.load(urllib.request.urlopen(r, timeout=60))
    except urllib.error.HTTPError as e:
        sys.exit(f"buffer HTTP {e.code}: {e.read()[:300]!r}")
    if d.get("errors"):
        sys.exit("buffer error: " + json.dumps(d["errors"])[:300])
    return d["data"]

POSTS = """query($input: PostsInput!) { posts(first: 20, input: $input) { edges { node { id channelId dueAt status } } } }"""
CREATE = """mutation($input: CreatePostInput!) { createPost(input: $input) {
  ... on PostActionSuccess { post { id dueAt status } }
  ... on MutationError { message } } }"""

def existing(channel, due):
    lo, hi = due - datetime.timedelta(minutes=5), due + datetime.timedelta(minutes=5)
    d = gql(POSTS, {"input": {"organizationId": ORG, "filter": {"channelIds": [channel],
            "status": ["scheduled", "sending", "sent"], "dueAt": {"start": lo.isoformat(), "end": hi.isoformat()}}}})
    edges = d["posts"]["edges"] or []
    return edges[0]["node"]["id"] if edges else None

def create(channel, text, video, due, meta):
    d = gql(CREATE, {"input": {"channelId": channel, "schedulingType": "automatic", "mode": "customScheduled",
            "dueAt": due.isoformat(), "text": text, "assets": [{"video": {"url": video}}], "metadata": meta}})
    p = d["createPost"]
    if "post" not in p:
        sys.exit("buffer createPost failed: " + p.get("message", "?")[:300])
    return p["post"]["id"]

def main():
    dry = "--dry-run" in sys.argv
    now = datetime.datetime.now(TZ)
    lines = [json.loads(l) for l in open(Q) if l.strip()]
    changed = False
    for i in lines:
        if i["brand"] != "Unscouted" or i["kind"] != "reel" or i.get("buffer"):
            continue
        due = datetime.datetime.fromisoformat(f'{i["date"]}T{i["time"]}').replace(tzinfo=TZ)
        if due < now + datetime.timedelta(minutes=30):
            continue
        video = RAW + i["files"][0]
        if dry:
            print(json.dumps({"would_schedule": i["date"] + " " + i["time"], "video": i["files"][0]})); continue
        ids = {}
        ids["instagram"] = existing(IG, due) or create(IG, i["caption"], video, due,
            {"instagram": {"type": "reel", "shouldShareToFeed": True, "isAiGenerated": True}})
        ids["tiktok"] = existing(TT, due) or create(TT, i["caption"].replace(" #soccerplayer", ""), video, due,
            {"tiktok": {"title": i.get("tiktok_title", "")[:150], "isAiGenerated": True}})
        i["buffer"] = ids; changed = True
        print(json.dumps({"scheduled": i["date"] + " " + i["time"], **ids}))
    if changed:
        open(Q, "w").write("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in lines))

if __name__ == "__main__":
    main()
