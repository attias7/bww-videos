#!/usr/bin/env python3
"""Finish a TikTok login: python3 social/connect_tiktok.py "<the full https://signbuildrun.com/?code=...&state=sbr address>"
Exchanges the one-time code (needs TIKTOK_CLIENT_KEY/SECRET), checks the account name and saves it in tokens.enc."""
import os, sys, json, urllib.parse, urllib.request
url=sys.argv[1]; out="/tmp/tt_new.json"
q=urllib.parse.parse_qs(urllib.parse.urlparse(url).query); key=q["state"][0]
body=urllib.parse.urlencode({"client_key":os.environ["TIKTOK_CLIENT_KEY"],"client_secret":os.environ["TIKTOK_CLIENT_SECRET"],"code":q["code"][0],"grant_type":"authorization_code","redirect_uri":"https://signbuildrun.com/"}).encode()
r=urllib.request.Request("https://open.tiktokapis.com/v2/oauth/token/",data=body,headers={"Content-Type":"application/x-www-form-urlencoded"})
try: d=json.load(urllib.request.urlopen(r,timeout=30))
except urllib.error.HTTPError as e: d=json.load(e)
if "access_token" not in d: sys.exit("ERROR "+json.dumps({k:d.get(k) for k in("error","error_description")}))
u=urllib.request.Request("https://open.tiktokapis.com/v2/user/info/?fields=open_id,display_name",headers={"Authorization":"Bearer "+d["access_token"]})
ui=json.load(urllib.request.urlopen(u,timeout=30))
json.dump({"tiktok":{key:d}},open(out,"w"))
print("OK",key,"scope=",d.get("scope"),"user=",ui["data"]["user"]["display_name"])
import subprocess
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tokens.py"), "merge", out], check=True)
