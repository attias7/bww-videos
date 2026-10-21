#!/usr/bin/env python3
"""After the email is sent: record its items so they aren't emailed twice.
Usage: python3 uploads/mark_sent.py <gmail message id>"""
import datetime, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open("/tmp/upload_email.json"))
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
with open(os.path.join(ROOT, "uploads", "sent.jsonl"), "a") as fh:
    for k in d["keys"]:
        fh.write(json.dumps({"key": k, "sent_at": now, "message_id": sys.argv[1]}) + "\n")
print(f"marked {len(d['keys'])} sent")
