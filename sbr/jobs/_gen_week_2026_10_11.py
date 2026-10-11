#!/usr/bin/env python3
"""Generates jobs ep15..ep21 (Sunday run 2026-10-11). Run from sbr/jobs."""
import json

def T(at, y, segs, size=80, dt=None, **kw):
    e = {"type": "text", "at": at, "y": y, "size": size, "segs": segs}
    if dt is not None: e["dt"] = dt
    e.update(kw); return e
def CH(at, y, text, fill="y", color="dark", size=46, dt=None, **kw):
    e = {"type": "chip", "at": at, "y": y, "text": text, "fill": fill, "color": color, "size": size}
    if dt is not None: e["dt"] = dt
    e.update(kw); return e
def E(type_, at, y, dt=None, **kw):
    e = {"type": type_, "at": at, "y": y}
    if dt is not None: e["dt"] = dt
    e.update(kw); return e
def realtalk(at): return CH(at, 470, "REAL TALK", fill="r", color="w", size=48)
def outro(at, nxt, y=1180):
    return [CH(at, y, f"Follow · {nxt}", size=44, pad=40),
            T(at, y + 170, [["Sign Build Run", "y"]], 70, dt=0.5)]

def job(ep, slug, hook, lines, scenes):
    return {"episode": ep, "series": f"NO COLD CALLS · EP. {ep}", "hook": hook,
            "voice": f"../voices/ep{ep}.mp3", "atempo": 1.1, "out": f"../out/ep{ep}_{slug}.mp4",
            "lines": lines, "scenes": scenes}

J = {}

# ---------------- EP 15 · PAIN (sales dread) ----------------
J[15] = job(15, "introverts_no_sales_calls", "Introverts: get contractors to pay you, no sales calls.", [
 "Introverts: get contractors to pay you, no sales calls.",
 "Every make money online thing ends the same way.",
 "Now get on a call.",
 "Agency? Sales calls. Freelancing? Sales calls.",
 "So I looked for a model where the customer finds you.",
 "It's called rank and rent.",
 "You build a small site for one service in one small town.",
 "Like roof repair in Smalltown.",
 "A homeowner searches Google, finds your site, and asks for a quote.",
 "You send that lead to a local contractor.",
 "He pays ten percent only if he closes the job.",
 "Real talk.",
 "Ranking takes months, and plenty of leads don't close.",
 "But nobody has to be convinced on a call.",
 "Follow. Ep. sixteen is building the site without code."], [
 {"from": 0, "elements": [
   T(0, 560, [["Introverts:", "y"]], 120),
   T(0, 720, [["get contractors", "w"]], 92, dt=0.5),
   T(0, 830, [["to pay you", "g"]], 92, dt=0.9),
   E("crossphone", 0, 1150, dt=1.3),
   T(0, 1400, [["no sales calls.", "r"]], 96, dt=1.6)]},
 {"from": 1, "elements": [
   T(1, 520, [["Every \"make money online\"", "w"]], 70),
   T(1, 620, [["thing ends the same way:", "w"]], 70, dt=0.4),
   E("phone_call", 2, 720, decline_at=2, decline_dt=1.0),
   T(2, 1540, [["\"Now get on a call.\"", "r"]], 92, dt=0.1)]},
 {"from": 3, "elements": [
   E("checklist", 3, 620, items=[
     {"text": "Agency = sales calls", "ok": False, "at": 3},
     {"text": "Freelancing = sales calls", "ok": False, "at": 3, "dt": 1.0}]),
   T(4, 1100, [["A model where the", "w"]], 76),
   T(4, 1210, [["customer finds you.", "g"]], 92, dt=0.5)]},
 {"from": 5, "elements": [
   T(5, 520, [["Rank & rent", "y"]], 120),
   T(6, 700, [["1 service · 1 small town", "w"]], 72),
   E("browser", 6, 820, dt=0.4, url="roofrepair-smalltown.com", title="Roof Repair in Smalltown"),
   CH(7, 1770, "example site · illustrative", fill=None, color="grey", size=34, outline="grey")]},
 {"from": 8, "elements": [
   T(8, 330, [["Homeowner ", "w"], ["searches Google", "y"]], 70),
   E("form", 8, 450, dt=0.6, title="Get a free roof quote",
     fields=[["Name", "J. ••••••"], ["Town", "Smalltown"], ["What's going on?", "Leak over the kitchen"]],
     notif=["New quote request", "Roof repair · Smalltown"])]},
 {"from": 9, "elements": [
   E("flow", 9, 420, gap=240, nodes=[
     {"label": "Homeowner asks for a quote", "color": "y", "at": 9},
     {"label": "You send it to a contractor", "color": "b", "at": 9, "dt": 0.8},
     {"label": "Job closes?", "color": "w", "at": 10}]),
   T(10, 1260, [["He pays ", "w"], ["10%", "g"]], 100, dt=0.5),
   T(10, 1380, [["only if he closes the job.", "w"]], 66, dt=0.9)]},
 {"from": 11, "elements": [
   realtalk(11),
   E("calendar", 12, 760, labels=["M1", "M2", "M3"]),
   T(12, 980, [["Ranking takes ", "w"], ["months.", "y"]], 80, dt=0.6),
   T(12, 1090, [["Plenty of leads ", "w"], ["don't close.", "r"]], 72, dt=1.4),
   T(13, 1300, [["But nobody gets ", "w"]], 76),
   T(13, 1410, [["convinced on a call.", "g"]], 84, dt=0.5)]},
 {"from": 14, "elements": [
   T(14, 700, [["No cold calls.", "w"]], 100),
   T(14, 830, [["No sales calls.", "y"]], 100, dt=0.3)] + outro(14, "Ep. 16: a site without code")}])

# ---------------- EP 16 · FEAR (tech) ----------------
J[16] = job(16, "no_code_site", "Never built a site? Build one without code.", [
 "Never built a site? Build one without code.",
 "A lead site is way smaller than you think.",
 "One service. One town.",
 "A home page, a services page, and a quote form.",
 "That's basically it.",
 "The page just says what you do and where.",
 "Roof repair in Smalltown. Get a free quote.",
 "AI can help you write the pages and set it up.",
 "No code. No designer.",
 "Real talk.",
 "Building it is the smaller part.",
 "Getting it to rank on Google takes months.",
 "And some sites never rank.",
 "But the tech isn't what should stop you.",
 "Follow. Ep. seventeen is what rank and rent actually takes."], [
 {"from": 0, "elements": [
   T(0, 560, [["Never built", "w"]], 120),
   T(0, 700, [["a site?", "y"]], 120, dt=0.3),
   T(0, 920, [["Build one ", "w"], ["without code.", "g"]], 84, dt=1.0),
   CH(0, 1150, "</>  not needed", fill="r", color="w", size=50, dt=1.4)]},
 {"from": 1, "elements": [
   T(1, 520, [["A lead site is way", "w"]], 80),
   T(1, 630, [["smaller", "y"], [" than you think.", "w"]], 80, dt=0.4),
   T(2, 900, [["1 service", "g"]], 110),
   T(2, 1040, [["1 town", "g"]], 110, dt=0.5)]},
 {"from": 3, "elements": [
   E("steps", 3, 520, items=[
     {"text": "1. Home page", "at": 3},
     {"text": "2. Services page", "at": 3, "dt": 0.6},
     {"text": "3. Quote form", "at": 3, "dt": 1.3}]),
   T(4, 1250, [["That's basically it.", "y"]], 92)]},
 {"from": 5, "elements": [
   T(5, 330, [["Says ", "w"], ["what", "y"], [" you do + ", "w"], ["where.", "y"]], 76),
   E("browser", 6, 480, url="roofrepair-smalltown.com", title="Roof Repair in Smalltown", button="Get a free quote"),
   CH(6, 1440, "example site · illustrative", fill=None, color="grey", size=34, outline="grey", dt=1.5)]},
 {"from": 7, "elements": [
   T(7, 560, [["AI", "y"], [" helps you write", "w"]], 92),
   T(7, 680, [["the pages + set it up.", "w"]], 76, dt=0.4),
   E("checklist", 8, 880, items=[
     {"text": "No code", "ok": True, "at": 8},
     {"text": "No designer", "ok": True, "at": 8, "dt": 0.6}])]},
 {"from": 9, "elements": [
   realtalk(9),
   T(10, 660, [["Building it = the ", "w"], ["smaller", "y"], [" part.", "w"]], 72),
   T(11, 820, [["Ranking takes ", "w"], ["months.", "r"]], 84),
   E("calendar", 11, 1050, dt=0.5),
   T(12, 1290, [["Some sites ", "w"], ["never rank.", "r"]], 80)]},
 {"from": 13, "elements": [
   T(13, 640, [["The tech isn't what", "w"]], 80),
   T(13, 750, [["should stop you.", "g"]], 96, dt=0.5)] + outro(14, "Ep. 17: what it really takes", y=1060)}])

# ---------------- EP 17 · SUSPICION (anti-guru honesty) ----------------
J[17] = job(17, "honest_version", "Sick of income screenshots? Here's the honest version.", [
 "Sick of income screenshots? Here's the honest version.",
 "Rank and rent isn't fast money.",
 "Here's what it actually takes.",
 "One. Months of waiting.",
 "A new site is a stranger to Google.",
 "Two. Some sites never rank at all.",
 "Three. Leads that don't close.",
 "A homeowner asks for a quote, then picks someone else.",
 "My first lead took about one to three months.",
 "So when a course shows you a screenshot and a car,",
 "ask what they're not showing you.",
 "Real talk.",
 "I'd rather you start slow and know the truth.",
 "Follow. Ep. eighteen is SEO in thirty seconds."], [
 {"from": 0, "elements": [
   T(0, 520, [["Sick of", "w"]], 110),
   T(0, 660, [["income screenshots?", "r"]], 96, dt=0.3),
   E("crossphone", 0, 950, dt=0.8),
   T(0, 1230, [["Here's the ", "w"], ["honest", "g"], [" version.", "w"]], 80, dt=1.3)]},
 {"from": 1, "elements": [
   T(1, 640, [["Rank & rent", "y"]], 110),
   T(1, 780, [["is ", "w"], ["not", "r"], [" fast money.", "w"]], 92, dt=0.4),
   T(2, 1050, [["What it actually takes:", "w"]], 72)]},
 {"from": 3, "elements": [
   E("bignum", 3, 440, text="1", size=220, color="r"),
   T(3, 660, [["Months of waiting.", "w"]], 88, dt=0.3),
   E("calendar", 3, 900, dt=0.8),
   T(4, 1150, [["A new site is a", "w"]], 72),
   T(4, 1250, [["stranger to Google.", "y"]], 84, dt=0.5)]},
 {"from": 5, "elements": [
   E("bignum", 5, 440, text="2", size=220, color="r"),
   T(5, 660, [["Some sites ", "w"], ["never rank.", "r"]], 84, dt=0.3)]},
 {"from": 6, "elements": [
   E("bignum", 6, 440, text="3", size=220, color="r"),
   T(6, 660, [["Leads that ", "w"], ["don't close.", "r"]], 84, dt=0.3),
   E("flow", 7, 820, gap=240, nodes=[
     {"label": "Asks for a quote", "color": "y", "at": 7},
     {"label": "Picks someone else", "color": "r", "at": 7, "dt": 1.2}])]},
 {"from": 8, "elements": [
   T(8, 560, [["My first lead took", "w"]], 80),
   T(8, 680, [["~1–3 months.", "y"]], 110, dt=0.5),
   E("calendar", 8, 920, dt=1.0),
   T(9, 1180, [["Screenshot + a car?", "w"]], 80),
   T(10, 1300, [["Ask what they're", "w"]], 76),
   T(10, 1400, [["not showing you.", "r"]], 84, dt=0.4)]},
 {"from": 11, "elements": [
   realtalk(11),
   T(12, 680, [["Start ", "w"], ["slow.", "y"]], 110),
   T(12, 820, [["Know the ", "w"], ["truth.", "g"]], 110, dt=0.8)] + outro(13, "Ep. 18: SEO in 30 sec", y=1100)}])

# ---------------- EP 18 · EDUCATION (SEO compounds) ----------------
J[18] = job(18, "seo_30_seconds", "Never heard of SEO? Here it is in thirty seconds.", [
 "Never heard of SEO? Here it is in thirty seconds.",
 "SEO just means getting found on Google.",
 "When someone searches roof repair Smalltown,",
 "Google picks which pages to show.",
 "It mostly looks at three things.",
 "One. Does the page clearly answer the search?",
 "Two. Is it actually useful?",
 "Three. Do other sites mention or link to it?",
 "Here's why it's worth learning.",
 "A post dies in a day. A ranking page can keep showing up.",
 "Real talk.",
 "It's slow. Months, not days. And nobody controls Google.",
 "But it's a skill that stacks.",
 "Follow. Ep. nineteen is messaging contractors when you're shy."], [
 {"from": 0, "elements": [
   T(0, 540, [["Never heard of", "w"]], 100),
   T(0, 690, [["SEO?", "y"]], 160, dt=0.3),
   T(0, 900, [["Here it is in", "w"]], 80, dt=1.0),
   E("bignum", 0, 1120, dt=1.3, text="30 sec", size=180, color="g")]},
 {"from": 1, "elements": [
   T(1, 330, [["SEO = getting ", "w"], ["found on Google.", "y"]], 70),
   E("google_phone", 2, 470, query="roof repair smalltown"),
   T(3, 1720, [["Google picks which pages to show.", "w"]], 58)]},
 {"from": 4, "elements": [
   T(4, 460, [["It mostly looks at ", "w"], ["3 things:", "y"]], 76),
   E("checklist", 5, 640, items=[
     {"text": "Answers the search?", "ok": True, "at": 5},
     {"text": "Actually useful?", "ok": True, "at": 6},
     {"text": "Other sites link to it?", "ok": True, "at": 7}])]},
 {"from": 8, "elements": [
   T(8, 460, [["Why it's ", "w"], ["worth learning:", "y"]], 80),
   E("versus", 9, 640, heads=["A post", "A ranking page"], rows=[["dies in a day", "keeps showing up"]], step=1.2),
   T(9, 1100, [["It ", "w"], ["stacks.", "g"]], 110, dt=1.8)]},
 {"from": 10, "elements": [
   realtalk(10),
   T(11, 660, [["Slow. ", "w"], ["Months,", "y"], [" not days.", "w"]], 84),
   T(11, 780, [["Nobody controls Google.", "r"]], 76, dt=1.4),
   T(12, 1000, [["But it's a skill", "w"]], 84),
   T(12, 1110, [["that stacks.", "g"]], 110, dt=0.4)]},
 {"from": 13, "elements": [
   T(13, 700, [["Next: messaging contractors", "w"]], 64),
   T(13, 800, [["when you're shy.", "y"]], 84, dt=0.4)] + outro(13, "Ep. 19 next", y=1050)}])

# ---------------- EP 19 · FEAR (talking to business owners) ----------------
J[19] = job(19, "message_contractors_shy", "Scared to message a business owner? Same.", [
 "Scared to message a business owner? Same.",
 "Here's how I reach contractors without a call.",
 "Everything is written.",
 "I posted once in a contractor Facebook group.",
 "Twenty-seven contractors commented.",
 "Comments aren't customers. But it taught me something.",
 "The offer does the talking.",
 "Here's the idea of the message.",
 "I have a site that gets quote requests in your area.",
 "Want the next one? You pay ten percent only if you close it.",
 "No pitch. No call. Just a yes or no.",
 "Real talk.",
 "Some won't reply. Some leads won't close.",
 "And you'll still talk to people. Just in writing.",
 "Follow. Ep. twenty is for anyone who feels behind."], [
 {"from": 0, "elements": [
   T(0, 560, [["Scared to message a", "w"]], 80),
   T(0, 680, [["business owner?", "y"]], 104, dt=0.3),
   T(0, 960, [["Same.", "g"]], 160, dt=1.4)]},
 {"from": 1, "elements": [
   T(1, 520, [["How I reach contractors", "w"]], 72),
   E("crossphone", 1, 820, dt=0.3),
   T(1, 1060, [["without a call.", "r"]], 92, dt=0.6),
   T(2, 1260, [["Everything is ", "w"], ["written.", "y"]], 92)]},
 {"from": 3, "elements": [
   T(3, 480, [["I posted ", "w"], ["once", "y"], [" in a", "w"]], 80),
   T(3, 590, [["contractor Facebook group.", "w"]], 70, dt=0.4),
   E("bignum", 4, 880, text="27", size=300, color="y"),
   T(4, 1100, [["contractors commented.", "w"]], 76, dt=0.3),
   T(5, 1300, [["Comments aren't customers.", "r"]], 76),
   CH(5, 1450, "real post · no results claimed", fill=None, color="grey", size=34, outline="grey", dt=0.6)]},
 {"from": 6, "elements": [
   T(6, 620, [["The ", "w"], ["offer", "y"], [" does", "w"]], 110),
   T(6, 760, [["the talking.", "w"]], 110, dt=0.4),
   T(7, 1000, [["The idea of the message:", "grey"]], 64)]},
 {"from": 8, "elements": [
   E("chat", 8, 340, name="Local Roofer", sub="example · illustrative", messages=[
     "I have a site that gets\nquote requests in your area.",
     "Want the next one?\nYou pay 10% only if\nyou close it."]),
   T(10, 1460, [["No pitch. No call.", "w"]], 84),
   T(10, 1570, [["Just a yes or no.", "g"]], 84, dt=0.6)]},
 {"from": 11, "elements": [
   realtalk(11),
   T(12, 660, [["Some won't reply.", "w"]], 84),
   T(12, 770, [["Some leads won't close.", "r"]], 80, dt=0.8),
   T(13, 960, [["You still talk to people.", "w"]], 74),
   T(13, 1070, [["Just in writing.", "y"]], 92, dt=0.8)]},
 {"from": 14, "elements": outro(14, "Ep. 20: if you feel behind", y=860)}])

# ---------------- EP 20 · PERSONAL (build in public) ----------------
J[20] = job(20, "feel_behind", "If you feel behind, start with one small thing.", [
 "If you feel behind, start with one small thing.",
 "I'm twenty-two. And I'm an introvert.",
 "Everything I found online ended in a sales call.",
 "So I stopped looking for something big.",
 "One service. One small town. One site.",
 "That's the whole project.",
 "No ads. No camera. No cold calls.",
 "My first lead took about one to three months.",
 "Real talk.",
 "It's slow, and it might not work the first time.",
 "But one small real thing beats ten plans in your notes app.",
 "You don't have to catch up to anyone.",
 "You just have to start one thing.",
 "Follow. Ep. twenty-one is what a two thousand dollar course won't fix."], [
 {"from": 0, "elements": [
   T(0, 560, [["Feel ", "w"], ["behind?", "r"]], 120),
   T(0, 760, [["Start with", "w"]], 92, dt=0.9),
   T(0, 880, [["one small thing.", "g"]], 100, dt=1.2)]},
 {"from": 1, "elements": [
   E("bignum", 1, 620, text="22", size=320, color="y"),
   T(1, 900, [["and an ", "w"], ["introvert.", "y"]], 92, dt=0.8),
   T(2, 1150, [["Everything I found ended in", "w"]], 64),
   T(2, 1270, [["a sales call.", "r"]], 92, dt=0.6),
   E("crossphone", 2, 1500, dt=1.0)]},
 {"from": 3, "elements": [
   T(3, 480, [["So I stopped looking", "w"]], 80),
   T(3, 590, [["for something ", "w"], ["big.", "r"]], 80, dt=0.4),
   E("cards", 4, 760, gap=0, items=[]),
   T(4, 820, [["1 service", "g"]], 100),
   T(4, 960, [["1 small town", "g"]], 100, dt=0.5),
   T(4, 1100, [["1 site", "g"]], 100, dt=1.0),
   T(5, 1320, [["That's the whole project.", "y"]], 76)]},
 {"from": 6, "elements": [
   E("checklist", 6, 520, items=[
     {"text": "No ads", "ok": True, "at": 6},
     {"text": "No camera", "ok": True, "at": 6, "dt": 0.5},
     {"text": "No cold calls", "ok": True, "at": 6, "dt": 1.0}]),
   T(7, 1120, [["First lead: ", "w"], ["~1–3 months.", "y"]], 80),
   E("calendar", 7, 1350, dt=0.6)]},
 {"from": 8, "elements": [
   realtalk(8),
   T(9, 660, [["Slow. Might not work", "w"]], 80),
   T(9, 770, [["the first time.", "r"]], 84, dt=0.6),
   E("versus", 10, 960, heads=["10 plans", "1 real thing"], rows=[["in your notes app", "actually live"]], step=1.0)]},
 {"from": 11, "elements": [
   T(11, 600, [["You don't have to", "w"]], 84),
   T(11, 710, [["catch up to anyone.", "y"]], 88, dt=0.5),
   T(12, 900, [["Start ", "w"], ["one", "g"], [" thing.", "w"]], 110)] + outro(13, "Ep. 21 next", y=1150)}])
# drop the empty cards placeholder
J[20]["scenes"][2]["elements"] = [e for e in J[20]["scenes"][2]["elements"] if e["type"] != "cards"]

# ---------------- EP 21 · ENEMY + soft product ----------------
J[21] = job(21, "course_wont_fix_shy", "A two thousand dollar course won't make you less shy.", [
 "A two thousand dollar course won't make you less shy.",
 "A lot of them still end the same way.",
 "Book a call. Cold call. DM fifty owners.",
 "If you're an introvert, that's where you quit.",
 "So build around it instead.",
 "Let Google bring the homeowner to your site.",
 "Send the lead to a contractor in writing.",
 "He pays ten percent only if the job closes.",
 "I put the whole process in the thirty-seven dollar Starter Kit.",
 "No calls. No upsell.",
 "Real talk.",
 "It's not fast, and results vary.",
 "Ranking takes months. Plenty of leads don't close.",
 "But you won't have to become a salesman to try.",
 "Follow. Ep. twenty-two drops next week."], [
 {"from": 0, "elements": [
   T(0, 520, [["A ", "w"], ["$2,000", "r"], [" course", "w"]], 110),
   T(0, 680, [["won't make you", "w"]], 92, dt=0.6),
   T(0, 800, [["less shy.", "y"]], 120, dt=1.0)]},
 {"from": 1, "elements": [
   T(1, 420, [["A lot still end the same way:", "w"]], 64),
   E("steps", 2, 560, items=[
     {"text": "Book a call", "at": 2},
     {"text": "Cold call", "at": 2, "dt": 0.6},
     {"text": "DM 50 owners", "at": 2, "dt": 1.2}], strike_at=3),
   T(3, 1280, [["Introverts quit ", "w"], ["here.", "r"]], 88, dt=0.4)]},
 {"from": 4, "elements": [
   T(4, 420, [["Build ", "w"], ["around", "y"], [" it.", "w"]], 100),
   E("flow", 5, 600, gap=240, nodes=[
     {"label": "Google brings the homeowner", "color": "y", "at": 5},
     {"label": "Lead goes to a contractor", "color": "b", "at": 6},
     {"label": "Pays 10% only if it closes", "color": "g", "at": 7}])]},
 {"from": 8, "elements": [
   T(8, 560, [["The whole process:", "w"]], 76),
   T(8, 700, [["Starter Kit", "y"]], 120, dt=0.6),
   E("bignum", 8, 920, dt=1.2, text="$37", size=220, color="g"),
   E("checklist", 9, 1120, items=[
     {"text": "No calls", "ok": True, "at": 9},
     {"text": "No upsell", "ok": True, "at": 9, "dt": 0.5}])]},
 {"from": 10, "elements": [
   realtalk(10),
   T(11, 660, [["Not fast. ", "w"], ["Results vary.", "r"]], 80),
   E("calendar", 12, 900),
   T(12, 1120, [["Plenty of leads ", "w"], ["don't close.", "r"]], 72, dt=0.8)]},
 {"from": 13, "elements": [
   T(13, 640, [["You won't have to become", "w"]], 70),
   T(13, 750, [["a salesman to try.", "g"]], 92, dt=0.5)] + outro(14, "Ep. 22 next week", y=1050)}])

for ep, j in J.items():
    n = len(j["lines"]); words = sum(len(l.split()) for l in j["lines"])
    for sc in j["scenes"]:
        for e in sc["elements"]:
            ats = [e["at"]] + [i.get("at", e["at"]) for i in e.get("items", []) + e.get("nodes", [])]
            assert all(0 <= a < n for a in ats), (ep, e)
    with open(f"ep{ep}.json", "w") as f: json.dump(j, f, indent=1, ensure_ascii=False)
    print(ep, n, "lines", words, "words")
