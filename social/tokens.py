#!/usr/bin/env python3
"""Encrypted token store for the auto-posting run.

social/tokens.enc = AES-256 (openssl, pbkdf2) of a JSON dict, keyed by env SOCIAL_TOKEN_KEY.
  {"tiktok": {"sbr": {...token response...}, "r360": {...}, "str": {...}},
   "instagram": {"sbr": {"access_token": ..., "user_id": ...}, ...}}

Usage from other scripts:  from tokens import load, save
CLI:  python3 social/tokens.py status      (prints which accounts have tokens, never the tokens)
      python3 social/tokens.py merge FILE  (merges a plain JSON file into the store, then deletes FILE)
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENC = os.path.join(HERE, "tokens.enc")

def _ssl(args, data):
    env = {**os.environ}
    if not env.get("SOCIAL_TOKEN_KEY"):
        sys.exit("SOCIAL_TOKEN_KEY is not set")
    r = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-salt",
                        "-pass", "env:SOCIAL_TOKEN_KEY", *args], input=data, capture_output=True, env=env)
    if r.returncode:
        sys.exit("openssl failed: " + r.stderr.decode()[:200])
    return r.stdout

def load():
    if not os.path.exists(ENC):
        return {}
    return json.loads(_ssl(["-d"], open(ENC, "rb").read()))

def save(store):
    open(ENC, "wb").write(_ssl([], json.dumps(store).encode()))

def merge(path):
    store = load(); new = json.load(open(path))
    for k, v in new.items():
        store.setdefault(k, {}).update(v)
    save(store); os.remove(path)

if __name__ == "__main__":
    if sys.argv[1:2] == ["merge"]:
        merge(sys.argv[2])
    s = load()
    print({k: sorted(v) for k, v in s.items()})
