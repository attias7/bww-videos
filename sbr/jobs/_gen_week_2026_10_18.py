#!/usr/bin/env python3
"""Generates jobs ep22..ep28 (Sunday run 2026-10-18). Run from sbr/jobs."""
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


# ---------------- EP 22 · PAIN (every path ends in a call) ----------------
J[22] = job(22, "now_get_on_a_call", "Every side hustle ends with: now get on a call.", [
 "Every side hustle ends with: now get on a call.",
 "Agency? Get on a call.",
 "Freelancing? Get on a call.",
 "Closing? That's literally the call.",
 "If that makes your stomach drop, same.",
 "So I flipped it.",
 "Instead of finding customers, they find me.",
 "A homeowner searches roof repair in Smalltown.",
 "He finds my small site and asks for a quote.",
 "I pass that lead to a local contractor.",
 "He pays ten percent, only if he closes the job.",
 "Real talk.",
 "Getting a site to rank takes months.",
 "And plenty of leads don't close.",
 "But there's no pitch. No call.",
 "Follow. Ep. twenty-three is your first site."], [
 {"from": 0, "elements": [
   T(0, 520, [["Every side hustle", "w"]], 96),
   T(0, 640, [["ends with:", "w"]], 96, dt=0.4),
   E("phone_call", 0, 760, dt=0.8),
   T(0, 1560, [["\"Now get on a call.\"", "r"]], 92, dt=1.4)]},
 {"from": 1, "elements": [
   E("checklist", 1, 560, items=[
     {"text": "Agency = call", "ok": False, "at": 1},
     {"text": "Freelancing = call", "ok": False, "at": 2},
     {"text": "Closing = the call", "ok": False, "at": 3}]),
   T(4, 1200, [["Stomach drop? ", "w"], ["Same.", "y"]], 88)]},
 {"from": 5, "elements": [
   T(5, 560, [["So I ", "w"], ["flipped it.", "y"]], 110),
   T(6, 820, [["The customer", "w"]], 92),
   T(6, 940, [["finds ", "w"], ["me.", "g"]], 120, dt=0.6),
   E("arrow", 6, 1120, y2=1300, dt=0.2)]},
 {"from": 7, "elements": [
   E("google_phone", 7, 380, query="roof repair smalltown")]},
 {"from": 8, "elements": [
   E("form", 8, 380, title="Get a free roof quote",
     fields=[["Name", "J. ••••••"], ["Town", "Smalltown"], ["Job", "Leak over the kitchen"]], button="Request quote"),
   CH(8, 1470, "illustrative example", fill=None, color="grey", size=34, outline="grey", dt=0.8)]},
 {"from": 9, "elements": [
   E("flow", 9, 440, gap=240, nodes=[
     {"label": "Lead comes in", "color": "y", "at": 9},
     {"label": "Goes to a local contractor", "color": "b", "at": 9, "dt": 0.8},
     {"label": "Job closes?", "color": "w", "at": 10}]),
   T(10, 1280, [["He pays ", "w"], ["10%", "g"]], 100, dt=0.5),
   T(10, 1400, [["only if he closes.", "w"]], 70, dt=0.9)]},
 {"from": 11, "elements": [
   realtalk(11),
   E("calendar", 12, 700, labels=["M1", "M2", "M3"]),
   T(12, 940, [["Ranking takes ", "w"], ["months.", "y"]], 80, dt=0.5),
   T(13, 1080, [["Plenty of leads ", "w"], ["don't close.", "r"]], 72)]},
 {"from": 14, "elements": [
   T(14, 660, [["No pitch.", "w"]], 110),
   T(14, 800, [["No call.", "y"]], 110, dt=0.4)] + outro(15, "Ep. 23: your first site", y=1080)}])

# ---------------- EP 23 · FEAR (tech) ----------------
J[23] = job(23, "never_built_a_website", "If you've never built a website, start here.", [
 "If you've never built a website, start here.",
 "Don't start with the website.",
 "Start with one service and one small town.",
 "Like gutter cleaning in Smalltown.",
 "Search it on Google first.",
 "Old sites and directories? Good sign.",
 "Then the site is just three things.",
 "A page that says what you do and where.",
 "A page about the service.",
 "And a quote form.",
 "AI can help you write it and set it up.",
 "Real talk.",
 "The site is the easy part.",
 "Getting Google to show it takes months, and it might not.",
 "But you don't need to know code to begin.",
 "Follow. Ep. twenty-four is month one."], [
 {"from": 0, "elements": [
   T(0, 540, [["Never built", "w"]], 120),
   T(0, 680, [["a website?", "y"]], 120, dt=0.3),
   T(0, 900, [["Start ", "w"], ["here.", "g"]], 110, dt=0.9),
   E("arrow", 0, 1080, y2=1300, dt=1.2)]},
 {"from": 1, "elements": [
   T(1, 520, [["Don't start with", "w"]], 84),
   T(1, 630, [["the website.", "r"]], 96, dt=0.3),
   T(2, 880, [["1 service", "g"]], 110),
   T(2, 1020, [["1 small town", "g"]], 110, dt=0.5),
   CH(3, 1250, "gutter cleaning · Smalltown", size=48)]},
 {"from": 4, "elements": [
   E("results", 4, 360, query="gutter cleaning smalltown", items=[
     ["example-directory.com", "Gutter Cleaners near Smalltown", "Directory listing"],
     ["oldsite-example.com", "Smalltown Gutters", "Last updated years ago"]], mine=-1, label=""),
   CH(4, 1300, "illustrative results", fill=None, color="grey", size=34, outline="grey", dt=0.8)]},
 {"from": 5, "elements": [
   T(5, 640, [["Old sites +", "w"]], 96),
   T(5, 760, [["directories", "w"]], 96, dt=0.3),
   T(5, 920, [["= good sign", "g"]], 110, dt=0.7)]},
 {"from": 6, "elements": [
   T(6, 400, [["The site = ", "w"], ["3 things", "y"]], 96),
   E("steps", 7, 600, items=[
     {"text": "1. What + where", "at": 7},
     {"text": "2. The service", "at": 8},
     {"text": "3. Quote form", "at": 9}])]},
 {"from": 10, "elements": [
   E("browser", 10, 380, url="gutters-smalltown.com", title="Gutter Cleaning in Smalltown", button="Get a free quote"),
   T(10, 1340, [["AI", "y"], [" helps write + set up.", "w"]], 76, dt=0.6),
   CH(10, 1520, "example site · illustrative", fill=None, color="grey", size=34, outline="grey", dt=1.0)]},
 {"from": 11, "elements": [
   realtalk(11),
   T(12, 660, [["The site = the ", "w"], ["easy", "g"], [" part.", "w"]], 80),
   E("calendar", 13, 860),
   T(13, 1090, [["Google takes ", "w"], ["months.", "y"]], 80, dt=0.6),
   T(13, 1200, [["It might not show it.", "r"]], 70, dt=1.4)]},
 {"from": 14, "elements": [
   T(14, 640, [["No code needed", "w"]], 92),
   T(14, 760, [["to begin.", "g"]], 100, dt=0.4)] + outro(15, "Ep. 24: month one", y=1080)}])

# ---------------- EP 24 · SUSPICION (honest timeline) ----------------
J[24] = job(24, "month_one_nothing", "Month one, nothing happens. Here's why that's normal.", [
 "Month one, nothing happens. Here's why that's normal.",
 "Gurus show the screenshot.",
 "They skip the boring part.",
 "When your site is new, Google doesn't know it.",
 "It's a stranger.",
 "So month one, you get almost no visits.",
 "No calls. No forms. Nothing.",
 "That's where most people quit.",
 "What you do instead: make the page more useful.",
 "Answer the questions people in that town actually search.",
 "My first lead took about one to three months.",
 "Real talk.",
 "Some sites never rank at all.",
 "And a lead isn't money until a job closes.",
 "But now you know month one isn't failure.",
 "Follow. Ep. twenty-five is why contractors say yes."], [
 {"from": 0, "elements": [
   T(0, 520, [["Month one:", "y"]], 120),
   T(0, 680, [["nothing happens.", "w"]], 96, dt=0.5),
   E("calendar", 0, 900, dt=0.9, labels=["M1", "M2", "M3"]),
   T(0, 1160, [["Here's why that's ", "w"], ["normal.", "g"]], 72, dt=1.6)]},
 {"from": 1, "elements": [
   CH(1, 560, "income screenshot", fill="grey", color="w", size=52),
   T(1, 700, [["= what they show", "w"]], 76, dt=0.3),
   T(2, 920, [["They skip the", "w"]], 84),
   T(2, 1030, [["boring part.", "r"]], 100, dt=0.3)]},
 {"from": 3, "elements": [
   T(3, 520, [["New site?", "y"]], 110),
   T(3, 670, [["Google doesn't know it.", "w"]], 76, dt=0.5),
   E("search", 3, 880, dt=0.8, query="roof repair smalltown"),
   T(4, 1150, [["It's a ", "w"], ["stranger.", "y"]], 100)]},
 {"from": 5, "elements": [
   T(5, 520, [["Month one:", "y"]], 100),
   T(5, 650, [["almost no visits.", "w"]], 84, dt=0.4),
   E("checklist", 6, 840, items=[
     {"text": "No calls", "ok": False, "at": 6},
     {"text": "No forms", "ok": False, "at": 6, "dt": 0.5}]),
   T(7, 1240, [["Where most people ", "w"], ["quit.", "r"]], 76)]},
 {"from": 8, "elements": [
   T(8, 480, [["Instead:", "y"]], 100),
   T(8, 610, [["make the page more useful.", "w"]], 68, dt=0.5),
   E("steps", 9, 780, items=[
     {"text": "What's the price?", "at": 9},
     {"text": "Can you come today?", "at": 9, "dt": 0.6},
     {"text": "Serve my street?", "at": 9, "dt": 1.2}])]},
 {"from": 10, "elements": [
   T(10, 640, [["My first lead:", "w"]], 92),
   E("bignum", 10, 780, dt=0.4, text="1-3", size=240, color="y"),
   T(10, 1110, [["months.", "w"]], 100, dt=0.8)]},
 {"from": 11, "elements": [
   realtalk(11),
   T(12, 660, [["Some sites ", "w"], ["never rank.", "r"]], 84),
   T(13, 820, [["A lead isn't money", "w"]], 76),
   T(13, 930, [["until a job ", "w"], ["closes.", "y"]], 76, dt=0.4)]},
 {"from": 14, "elements": [
   T(14, 600, [["Month one", "w"]], 100),
   T(14, 730, [["isn't failure.", "g"]], 100, dt=0.4)] + outro(15, "Ep. 25: why contractors say yes", y=1060)}])

# ---------------- EP 25 · EDUCATION (pay-on-close from the contractor's side) ----------------
J[25] = job(25, "why_contractors_say_yes", "Why contractors say yes to: pay only if it closes.", [
 "Why contractors say yes to: pay only if it closes.",
 "Think about it from his side.",
 "Ads? He pays before he knows if anyone calls.",
 "Lead sellers? He pays per lead, even bad ones.",
 "Now your offer.",
 "Here's a homeowner who wants a quote.",
 "You only pay me ten percent if you get the job.",
 "If it doesn't close, he pays nothing.",
 "So you don't need to be a smooth talker.",
 "The offer does the convincing.",
 "Real talk.",
 "Some contractors still say no, or never reply.",
 "And you have to trust him to tell you it closed.",
 "The risk is on you, not him.",
 "Follow. Ep. twenty-six: no phone needed."], [
 {"from": 0, "elements": [
   T(0, 520, [["Why contractors", "w"]], 100),
   T(0, 640, [["say ", "w"], ["yes", "g"], [" to:", "w"]], 100, dt=0.4),
   CH(0, 860, "pay only if it closes", size=60, dt=1.0)]},
 {"from": 1, "elements": [
   T(1, 400, [["From ", "w"], ["his", "y"], [" side:", "w"]], 96),
   E("cards", 2, 580, gap=500, items=[
     {"head": "Ads: he pays", "big": "first", "sub": "even if nobody calls", "color": "r", "at": 2},
     {"head": "Lead sellers: he pays", "big": "each", "sub": "lead, even bad ones", "color": "r", "at": 3}])]},
 {"from": 4, "elements": [
   T(4, 400, [["Your offer:", "y"]], 100),
   E("chat", 5, 560, name="Smalltown Roofing", sub="illustrative", messages=[
     "I have a homeowner in Smalltown\nwho wants a roof quote.",
     "You only pay me 10%\nif you get the job."])]},
 {"from": 7, "elements": [
   T(7, 560, [["Doesn't close?", "w"]], 100),
   E("bignum", 7, 700, dt=0.4, text="$0", size=240, color="g"),
   T(8, 1060, [["No smooth talking.", "w"]], 84),
   T(9, 1180, [["The ", "w"], ["offer", "y"], [" convinces.", "w"]], 92)]},
 {"from": 10, "elements": [
   realtalk(10),
   T(11, 660, [["Some say ", "w"], ["no.", "r"], [" Some never reply.", "w"]], 66),
   T(12, 840, [["You have to ", "w"], ["trust", "y"], [" him", "w"]], 76),
   T(12, 950, [["to tell you it closed.", "w"]], 72, dt=0.4)]},
 {"from": 13, "elements": [
   T(13, 620, [["Risk on ", "w"], ["you,", "y"]], 100),
   T(13, 750, [["not him.", "g"]], 100, dt=0.4)] + outro(14, "Ep. 26: no phone needed", y=1060)}])

# ---------------- EP 26 · FEAR (talking to business owners) ----------------
J[26] = job(26, "contractor_without_phone", "Find a contractor without picking up the phone.", [
 "Find a contractor without picking up the phone.",
 "When a quote request comes in, you need a contractor.",
 "You can do that all in writing.",
 "One. Post in a local contractor Facebook group.",
 "I posted once, and twenty-seven contractors commented.",
 "Two. Use the contact form on their website.",
 "Three. Email the address on their Google listing.",
 "Keep it short.",
 "I have a homeowner in your town who wants a quote.",
 "You only pay if you close the job.",
 "Real talk.",
 "Comments aren't customers.",
 "Plenty won't reply, and some just say no.",
 "But nobody made me pick up the phone.",
 "Follow. Ep. twenty-seven is built for introverts."], [
 {"from": 0, "elements": [
   T(0, 520, [["Find a contractor", "w"]], 96),
   E("crossphone", 0, 820, dt=0.5),
   T(0, 1140, [["no phone", "r"], [" needed.", "w"]], 96, dt=1.0)]},
 {"from": 1, "elements": [
   E("form", 1, 340, title="New quote request",
     fields=[["Town", "Smalltown"], ["Job", "Gutter cleaning"]], button="Request quote"),
   T(1, 1470, [["Who gets it?", "y"]], 92, dt=1.0)]},
 {"from": 2, "elements": [
   T(2, 640, [["All in", "w"]], 110),
   T(2, 780, [["writing.", "g"]], 120, dt=0.3),
   E("crossphone", 2, 1100, dt=0.6)]},
 {"from": 3, "elements": [
   E("steps", 3, 420, items=[
     {"text": "1. Facebook group", "at": 3},
     {"text": "2. Contact form", "at": 5},
     {"text": "3. Email from Maps", "at": 6}]),
   E("bignum", 4, 1110, text="27", size=200, color="y"),
   T(4, 1320, [["contractors commented", "w"]], 66, dt=0.5),
   CH(4, 1440, "on one post", fill=None, color="grey", size=36, outline="grey", dt=0.9)]},
 {"from": 7, "elements": [
   T(7, 380, [["Keep it ", "w"], ["short.", "y"]], 100),
   E("chat", 8, 540, name="Smalltown Gutters", sub="illustrative", messages=[
     "I have a homeowner in your\ntown who wants a quote.",
     "You only pay if you\nclose the job."])]},
 {"from": 10, "elements": [
   realtalk(10),
   T(11, 660, [["Comments ", "w"], ["aren't", "r"], [" customers.", "w"]], 80),
   T(12, 800, [["Plenty won't reply.", "w"]], 76),
   T(12, 910, [["Some say ", "w"], ["no.", "r"]], 76, dt=0.6)]},
 {"from": 13, "elements": [
   T(13, 600, [["Nobody made me", "w"]], 92),
   T(13, 720, [["pick up the phone.", "g"]], 92, dt=0.4)] + outro(14, "Ep. 27: built for introverts", y=1060)}])

# ---------------- EP 27 · PERSONAL ----------------
J[27] = job(27, "built_around_introvert", "How I built a business around being an introvert.", [
 "How I built a business around being an introvert.",
 "I'm twenty-two, and calls drain me.",
 "So I stopped trying to fix that.",
 "And designed around it.",
 "Rule one. Customers find me on Google. I don't chase them.",
 "Rule two. I reach contractors in writing, not on calls.",
 "Rule three. Pay only if it closes, so there's nothing to pitch.",
 "Real talk.",
 "It's not zero talking. I still message people.",
 "And it's slow. My first lead took about one to three months.",
 "But I'm not pretending to be someone I'm not.",
 "If you're wired like me, you can build around it too.",
 "Follow. Ep. twenty-eight: skip learn sales first."], [
 {"from": 0, "elements": [
   T(0, 520, [["How I built", "w"]], 110),
   T(0, 650, [["a business around", "w"]], 92, dt=0.4),
   T(0, 800, [["being an introvert.", "y"]], 92, dt=0.9),
   E("battery", 0, 1080, dt=1.4, label="social battery")]},
 {"from": 1, "elements": [
   E("bignum", 1, 520, text="22", size=240, color="y"),
   T(1, 820, [["Calls ", "w"], ["drain", "r"], [" me.", "w"]], 96, dt=0.5),
   T(2, 1040, [["Stopped trying to fix it.", "w"]], 72),
   T(3, 1160, [["Designed ", "g"], ["around it.", "w"]], 92)]},
 {"from": 4, "elements": [
   E("steps", 4, 460, items=[
     {"text": "1. Customers find me", "at": 4},
     {"text": "2. Write, don't call", "at": 5},
     {"text": "3. Pay only on close", "at": 6}]),
   E("crossphone", 5, 1250, dt=0.5)]},
 {"from": 7, "elements": [
   realtalk(7),
   T(8, 660, [["Not ", "w"], ["zero", "r"], [" talking.", "w"]], 92),
   T(8, 780, [["I still message people.", "w"]], 70, dt=0.6),
   T(9, 960, [["First lead:", "w"]], 80),
   T(9, 1070, [["1-3 months.", "y"]], 100, dt=0.4)]},
 {"from": 10, "elements": [
   T(10, 560, [["Not pretending", "w"]], 96),
   T(10, 680, [["to be someone else.", "w"]], 80, dt=0.4),
   T(11, 880, [["Wired like me?", "y"]], 92),
   T(11, 1000, [["Build ", "w"], ["around it.", "g"]], 92, dt=0.5)] + outro(12, "Ep. 28: skip 'learn sales'", y=1220)}])

# ---------------- EP 28 · ENEMY + soft product ----------------
J[28] = job(28, "learn_sales_bad_advice", "Learn sales first is terrible advice for introverts.", [
 "Learn sales first is terrible advice for introverts.",
 "Every guru says it.",
 "Get good at the phone. Do a hundred cold calls.",
 "For some people that works.",
 "For people like me, it's why we never start.",
 "So skip the part you dread and change the model.",
 "Let Google bring the customer.",
 "Reach contractors in writing.",
 "Offer pay only if the job closes.",
 "Real talk.",
 "You'll still write messages, and some will say no.",
 "And ranking takes months.",
 "I put the whole process in the thirty-seven dollar Starter Kit. No calls, no upsell.",
 "Follow. Ep. twenty-nine next week."], [
 {"from": 0, "elements": [
   T(0, 520, [["\"Learn sales first\"", "y"]], 92),
   T(0, 660, [["is terrible advice", "w"]], 88, dt=0.6),
   T(0, 780, [["for introverts.", "r"]], 96, dt=1.1),
   E("crossphone", 0, 1100, dt=1.5)]},
 {"from": 1, "elements": [
   T(1, 520, [["Every guru says it:", "w"]], 84),
   E("checklist", 2, 700, items=[
     {"text": "Get good at the phone", "ok": False, "at": 2},
     {"text": "100 cold calls", "ok": False, "at": 2, "dt": 0.8}]),
   T(3, 1100, [["Works for ", "w"], ["some.", "g"]], 84),
   T(4, 1220, [["For me? Why we ", "w"], ["never start.", "r"]], 66)]},
 {"from": 5, "elements": [
   T(5, 420, [["Skip what you dread.", "w"]], 80),
   T(5, 530, [["Change the ", "w"], ["model.", "y"]], 92, dt=0.5),
   E("flow", 6, 700, gap=230, nodes=[
     {"label": "Google brings the customer", "color": "y", "at": 6},
     {"label": "Contractors in writing", "color": "b", "at": 7},
     {"label": "Pay only if it closes", "color": "g", "at": 8}])]},
 {"from": 9, "elements": [
   realtalk(9),
   T(10, 660, [["You still write messages.", "w"]], 70),
   T(10, 770, [["Some say ", "w"], ["no.", "r"]], 76, dt=0.6),
   T(11, 920, [["Ranking takes ", "w"], ["months.", "y"]], 80),
   E("calendar", 11, 1100, dt=0.4)]},
 {"from": 12, "elements": [
   T(12, 440, [["The whole process:", "w"]], 76),
   T(12, 570, [["Starter Kit", "y"]], 120, dt=0.5),
   E("bignum", 12, 760, dt=1.0, text="$37", size=200, color="g"),
   E("checklist", 12, 1000, dt=1.8, items=[
     {"text": "No calls", "ok": True, "at": 12, "dt": 1.8},
     {"text": "No upsell", "ok": True, "at": 12, "dt": 2.3}])] + outro(13, "Ep. 29 next week", y=1300)}])

for ep, j in J.items():
    n = len(j["lines"]); words = sum(len(l.split()) for l in j["lines"])
    for sc in j["scenes"]:
        for e in sc["elements"]:
            ats = [e["at"]] + [i.get("at", e["at"]) for i in e.get("items", []) + e.get("nodes", []) if isinstance(i, dict)]
            assert all(0 <= a < n for a in ats), (ep, e)
    with open(f"ep{ep}.json", "w") as f: json.dump(j, f, indent=1, ensure_ascii=False)
    print(ep, n, "lines", words, "words")
