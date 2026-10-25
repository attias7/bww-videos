#!/usr/bin/env python3
"""Build the daily upload email for one Israel date.
Usage: python3 uploads/render_email.py YYYY-MM-DD [--check] [--unsent]
Writes /tmp/upload_email.json = {"subject", "html", "text", "count", "missing", "keys"}.
--check   HEADs every download link and lists the ones that don't return 200.
--unsent  only items not yet listed in uploads/sent.jsonl (after sending, run uploads/mark_sent.py).
"""
import datetime, html, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = os.path.join(ROOT, "uploads", "queue.jsonl")
RAW = "https://raw.githubusercontent.com/attias7/bww-videos/main/"
COLORS = {"Sign Build Run": "#1f6feb", "Unscouted": "#2da44e", "Remodel in 360": "#bf8700", "SetToRank": "#0a7ea4", "Subletli": "#d99a00"}

def ok(url):
    try:
        out = subprocess.run(["curl", "-sI", "-o", "/dev/null", "-w", "%{http_code}", url],
                             capture_output=True, text=True, timeout=60).stdout
        return out.strip() == "200"
    except Exception:
        return False

def main():
    day = sys.argv[1]
    check = "--check" in sys.argv
    unsent = "--unsent" in sys.argv
    S = os.path.join(ROOT, "uploads", "sent.jsonl")
    sent = set()
    if unsent and os.path.exists(S):
        sent = {json.loads(l)["key"] for l in open(S) if l.strip()}
    key = lambda i: f'{i["date"]}|{i["brand"]}|{i["kind"]}'
    items = []
    if os.path.exists(Q):
        items = [json.loads(l) for l in open(Q) if l.strip()]
    items = sorted([i for i in items if i["date"] == day and key(i) not in sent], key=lambda i: (i["time"], i["brand"]))
    already = unsent and any(k.startswith(day + "|") for k in sent)
    d = datetime.date.fromisoformat(day)
    nice = d.strftime("%a %-d %b")
    n = len(items)
    subject = (f"➕ More to upload today – {nice} ({n} new post{'s' if n != 1 else ''})" if already
               else f"📲 Upload today – {nice} ({n} post{'s' if n != 1 else ''})")
    missing = []
    h, t = [], []
    h.append('<div style="font-family:-apple-system,Segoe UI,Arial,sans-serif;max-width:640px;color:#1f2328;line-height:1.45">')
    h.append(f'<h2 style="margin:0 0 4px">Upload today – {html.escape(nice)}</h2>')
    h.append('<p style="margin:0 0 16px;color:#59636e">Download → open Instagram / TikTok → add a trending sound '
             '(keep the voice at 100%, the music low, around 5–15%) → paste the caption → post or schedule in the app.</p>')
    t.append(f"Upload today – {nice}\n")
    if not items:
        h.append("<p>Nothing queued for today.</p>")
        t.append("Nothing queued for today.")
    for i in items:
        c = COLORS.get(i["brand"], "#59636e")
        label = "Reel" if i["kind"] == "reel" else "Carousel"
        h.append(f'<div style="border:1px solid #d1d9e0;border-left:5px solid {c};border-radius:8px;padding:12px 14px;margin:0 0 16px">')
        h.append(f'<div style="font-size:13px;color:{c};font-weight:700;text-transform:uppercase">{html.escape(i["brand"])} · {label}'
                 + (f' · Ep {i["ep"]}' if i.get("ep") else "") + "</div>")
        h.append(f'<div style="font-size:20px;font-weight:700;margin:2px 0">Post at {html.escape(i["time"])}</div>')
        h.append(f'<div style="color:#59636e;margin-bottom:8px">{html.escape(" + ".join(i["platforms"]))}</div>')
        t.append(f"\n== {i['brand']} · {label}" + (f" · Ep {i['ep']}" if i.get('ep') else "") + f" — post at {i['time']}")
        t.append("Where: " + " + ".join(i["platforms"]))
        links = []
        for f in i["files"]:
            url = RAW + f
            if check and not ok(url):
                missing.append(f)
            name = os.path.basename(f)
            if f.endswith(".zip"):
                name = "⬇ all slides (.zip)"
            links.append((name, url))
        auto = []
        if i.get("ig_file"):
            auto.append(f"✅ Instagram posts automatically at {i['time']} — don't post it there yourself.")
        if i.get("tiktok_draft"):
            auto.append("📥 TikTok: the draft is in your TikTok inbox the morning before — add the sound and schedule it "
                        f"for {i['date']} {i['time']} (or post it whenever you can that day).")
        if i.get("buffer"):
            auto.append(f"✅ Scheduled in Buffer for {i['date']} {i['time']} on Instagram + TikTok (built-in music) — nothing to do.")
        for a in auto:
            h.append(f'<div style="margin:0 0 8px;padding:6px 10px;background:#eef6ee;border-radius:6px;font-size:14px">{html.escape(a)}</div>')
            t.append(a)
        if i["kind"] == "reel":
            h.append(f'<a href="{links[0][1]}" style="display:inline-block;background:{c};color:#fff;text-decoration:none;'
                     f'padding:9px 14px;border-radius:6px;font-weight:600">⬇ Download video</a>')
        else:
            h.append('<div>' + " ".join(
                f'<a href="{u}" style="display:inline-block;margin:0 6px 6px 0;padding:5px 9px;border:1px solid {c};'
                f'border-radius:6px;color:{c};text-decoration:none;font-size:14px">{html.escape(nm)}</a>' for nm, u in links) + '</div>')
        for nm, u in links:
            t.append(f"{nm}: {u}")
        if i.get("tiktok_title"):
            h.append(f'<div style="margin-top:10px"><b>TikTok title:</b> {html.escape(i["tiktok_title"])}</div>')
            t.append("TikTok title: " + i["tiktok_title"])
        for k, lab in (("sound_tiktok", "🎵 TikTok sound"), ("sound_instagram", "🎵 Instagram sound")):
            if i.get(k):
                h.append(f'<div style="margin-top:6px"><b>{lab}:</b> {html.escape(i[k])}</div>')
                t.append(f"{lab}: {i[k]}")
        if i.get("music"):
            h.append(f'<div style="margin-top:6px"><b>Music:</b> {html.escape(i["music"])}</div>')
            t.append("Music: " + i["music"])
        h.append('<div style="margin-top:10px;font-weight:700">Caption</div>')
        h.append(f'<div style="white-space:pre-wrap;background:#f6f8fa;border-radius:6px;padding:10px;font-size:15px">{html.escape(i["caption"])}</div>')
        t.append("Caption:\n" + i["caption"])
        if i.get("notes"):
            h.append(f'<div style="margin-top:8px;color:#59636e;font-size:14px">{html.escape(i["notes"])}</div>')
            t.append("Notes: " + i["notes"])
        h.append("</div>")
    h.append("</div>")
    out = {"subject": subject, "html": "".join(h), "text": "\n".join(t), "count": n, "missing": missing,
           "keys": [key(i) for i in items]}
    json.dump(out, open("/tmp/upload_email.json", "w"), ensure_ascii=False)
    print(json.dumps({"subject": subject, "count": n, "missing": missing}, ensure_ascii=False))

if __name__ == "__main__":
    main()
