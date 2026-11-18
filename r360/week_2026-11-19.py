#!/usr/bin/env python3
"""R360 TikTok week 2026-11-19..11-25 (d024..d030). Writes jobs/dNNN.json + week_2026-11-19.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ACC = [255, 128, 82]
TAGS = "#contractor #kitchenremodel #bathroomremodel #remodeling #contractorlife"
OWN = "Our own remodeling company went from three in ten to five or six in ten."
CTA = "Your first tour is free. Link in bio."

def T(y, txt, col="w", size=96, dt=0.0):
    return {"type": "text", "y": y, "segs": [[txt, col]], "size": size, "dt": dt}
def N(y, txt, col="w", size=220, dt=0.0):
    return {"type": "bignum", "y": y, "text": txt, "size": size, "color": col, "dt": dt}
def C(y, txt, fill="w", col="dark", size=52, dt=0.0):
    return {"type": "chip", "y": y, "text": txt, "fill": fill, "color": col, "size": size, "dt": dt}

REAL = lambda a, b: [C(560, "REAL TALK"), T(780, a, "w", 92, 0.3), T(910, b, "w", 92, 0.5)]
OWN_S = [T(420, "OUR OWN REMODELING COMPANY", "grey", 50), N(700, "3 / 10", "w", 200),
         N(1050, "5–6 / 10", "y", 187, 1.6), T(1300, "CLOSE RATE", "grey", 50, 1.8)]
CTA_S = [T(760, "FIRST TOUR", "w", 110), T(900, "FREE.", "y", 130, 0.2),
         C(1180, "Link in bio · remodelin360.com", "y", "dark", 48, 0.6)]

POSTS = [
 dict(id="d024", date="2026-11-19", angle="pain 1", slug="salesperson", topic="hire a salesperson vs close one more",
  hook_card=[("BEFORE YOU HIRE", "dark"), ("A SALESPERSON,", "dark"), ("DO THIS", "dark"), ("MATH.", "w")],
  lines=["Before you hire a salesperson, do this math.",
   "A good one costs you around five grand a month.",
   "Say you give ten estimates a month at twenty-five thousand each.",
   "You close three. Seventy-five thousand.",
   "Close just one more, and that's another twenty-five.",
   "Same leads. Same crew. No new salary.",
   "Real talk, at some point you do need help selling.",
   "But first, look at why the other seven say no.",
   "Most of them couldn't picture the finished room.",
   "Show them their own room, finished, before you leave.", OWN, CTA],
  scenes=[None,
   [T(560, "A SALESPERSON", "grey", 64), N(780, "$5K", "r", 240, 0.2), T(1000, "A MONTH", "w", 80, 0.4)],
   [N(700, "10", "w", 260), T(920, "ESTIMATES × $25,000", "y", 76, 0.4)],
   [T(560, "YOU CLOSE 3", "grey", 64), N(780, "$75K", "w", 240, 0.2)],
   [C(520, "+1 JOB", "y", "dark", 54), N(760, "+$25K", "g", 240, 0.4)],
   [T(650, "SAME LEADS.", "w", 96), T(790, "SAME CREW.", "w", 96, 0.3), T(930, "NO NEW SALARY.", "y", 96, 0.6)],
   REAL("YOU MAY NEED", "HELP SELLING."),
   [T(700, "WHY DO", "w", 100), T(850, "SEVEN SAY NO?", "r", 100, 0.4)],
   [T(700, "THEY COULDN'T", "w", 100), T(850, "PICTURE IT.", "y", 110, 0.4)],
   [T(600, "SHOW THEM", "w", 96), T(750, "THEIR ROOM,", "y", 110, 0.3), T(900, "FINISHED.", "y", 120, 0.5)],
   OWN_S, CTA_S],
  caption="Before you hire a salesperson, do this math.\n10 estimates at $25k, you close 3 = $75k. One more yes = +$25k. Same leads, no new salary.\nFirst tour free, link in bio."),
 dict(id="d025", date="2026-11-20", angle="pain 3", slug="after_holidays", topic="we'll decide after the holidays",
  hook_card=[("\"WE'LL DECIDE", "dark"), ("AFTER THE", "dark"), ("HOLIDAYS.\"", "dark"), ("DO THIS MATH.", "w")],
  lines=["\"We'll decide after the holidays.\" Do this math.",
   "Say you've got six open bids right now.",
   "Average job, twenty-eight thousand.",
   "That's a hundred sixty-eight thousand sitting on hold.",
   "In January, maybe two of them call back.",
   "The rest started over with someone else.",
   "Real talk, some people really do wait for the new year.",
   "But \"after the holidays\" usually means \"I'm not sure yet.\"",
   "Not sure, because they can't picture it.",
   "Show them their own room, finished, before the holidays hit.", OWN, CTA],
  scenes=[None,
   [N(700, "6", "w", 280), T(940, "OPEN BIDS", "w", 90, 0.3)],
   [T(560, "AVERAGE JOB", "grey", 64), N(780, "$28,000", "w", 190, 0.2)],
   [N(700, "$168K", "r", 230), T(930, "ON HOLD", "w", 90, 0.4)],
   [N(700, "2", "y", 280), T(940, "CALL BACK IN JANUARY", "w", 70, 0.3)],
   [T(700, "THE REST", "w", 100), T(850, "STARTED OVER.", "r", 100, 0.4)],
   REAL("SOME REALLY DO", "WAIT FOR JANUARY."),
   [T(700, "\"AFTER THE HOLIDAYS\"", "w", 76), T(850, "= \"NOT SURE YET.\"", "y", 84, 0.5)],
   [T(700, "NOT SURE,", "w", 100), T(850, "CAN'T PICTURE IT.", "y", 90, 0.4)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "FINISHED,", "y", 120, 0.3), T(900, "BEFORE THE HOLIDAYS.", "w", 76, 0.6)],
   OWN_S, CTA_S],
  caption="\"We'll decide after the holidays.\" Do this math.\n6 open bids at $28k = $168k on hold. In January, maybe 2 call back.\nFirst tour free, link in bio."),
 dict(id="d026", date="2026-11-21", angle="pain 5", slug="saturday_estimates", topic="weekend estimate hours",
  hook_card=[("SPENT YOUR", "dark"), ("SATURDAY ON", "dark"), ("ESTIMATES?", "dark"), ("COUNT IT.", "w")],
  lines=["Spent your Saturday writing estimates? Count it.",
   "Say it's two estimates every weekend.",
   "Four hours each. Pricing, layouts, the write-up.",
   "That's eight hours a weekend. Thirty-two a month.",
   "You close three in ten.",
   "So about twenty-two of those hours go nowhere.",
   "Real talk, estimates are part of the job.",
   "But most of the no's come from the same place.",
   "They see a number and can't picture the room.",
   "Show them their own room, finished, and your weekends start to count.", OWN, CTA],
  scenes=[None,
   [N(700, "2", "w", 280), T(940, "ESTIMATES EVERY WEEKEND", "w", 66, 0.3)],
   [N(700, "4 HRS", "y", 200), T(920, "PRICING · LAYOUTS · WRITE-UP", "grey", 52, 0.4)],
   [N(700, "32 HRS", "r", 200), T(920, "A MONTH. ON WEEKENDS.", "w", 72, 0.4)],
   [T(560, "YOU CLOSE", "grey", 64), N(780, "3 / 10", "w", 220, 0.2)],
   [N(700, "~22 HRS", "r", 190), T(930, "GO NOWHERE.", "w", 90, 0.4)],
   REAL("ESTIMATES ARE", "PART OF THE JOB."),
   [T(700, "MOST NO'S", "w", 100), T(850, "SAME PLACE.", "y", 110, 0.4)],
   [T(700, "THEY SEE A NUMBER.", "w", 84), T(850, "NOT THE ROOM.", "r", 100, 0.5)],
   [T(600, "SHOW THEM", "w", 96), T(750, "THEIR ROOM,", "y", 110, 0.3), T(900, "FINISHED.", "y", 120, 0.5)],
   OWN_S, CTA_S],
  caption="Spent your Saturday writing estimates? Count it.\n2 a weekend, 4 hours each = 32 hours a month. At 3 in 10, about 22 of those hours go nowhere.\nFirst tour free, link in bio."),
 dict(id="d027", date="2026-11-22", angle="pain 2", slug="line_items", topic="40 line items, they read the total",
  hook_card=[("YOUR BID HAS", "dark"), ("40 LINE ITEMS.", "dark"), ("THEY READ", "dark"), ("ONE.", "w")],
  lines=["Your bid has forty line items. They read one.",
   "The total at the bottom.",
   "Yours says thirty-eight five.",
   "The other bid says thirty-three nine.",
   "Forty-six hundred dollars apart.",
   "Your soft-close drawers and better tile? Line twenty-seven.",
   "Real talk, a clear breakdown still matters.",
   "But nobody gets excited about a spreadsheet.",
   "They get excited when they see the room.",
   "Show them their own kitchen, finished, next to your price.", OWN, CTA],
  scenes=[None,
   [T(700, "THE TOTAL.", "y", 120), T(860, "AT THE BOTTOM.", "w", 84, 0.3)],
   [T(560, "YOUR BID", "grey", 64), N(780, "$38,500", "w", 190, 0.2)],
   [T(560, "THEIR BID", "grey", 64), N(780, "$33,900", "y", 190, 0.2)],
   [N(700, "$4,600", "r", 210), T(930, "APART.", "w", 96, 0.4)],
   [T(650, "SOFT-CLOSE DRAWERS?", "w", 80), T(780, "BETTER TILE?", "w", 84, 0.3), T(940, "LINE 27.", "r", 120, 0.6)],
   REAL("A CLEAR BREAKDOWN", "STILL MATTERS."),
   [T(700, "NOBODY GETS EXCITED", "w", 80), T(850, "ABOUT A SPREADSHEET.", "r", 78, 0.5)],
   [T(700, "THEY GET EXCITED", "w", 88), T(850, "BY THE ROOM.", "y", 110, 0.4)],
   [T(600, "THEIR KITCHEN,", "w", 100), T(750, "FINISHED,", "y", 120, 0.3), T(900, "NEXT TO YOUR PRICE.", "w", 78, 0.6)],
   OWN_S, CTA_S],
  caption="Your bid has 40 line items. They read one.\n$38,500 vs $33,900. Your better tile is on line 27, and they only read the total.\nFirst tour free, link in bio."),
 dict(id="d028", date="2026-11-23", angle="pain 4", slug="design_revisions", topic="free design revisions before signing",
  hook_card=[("3 FREE DESIGN", "dark"), ("REVISIONS BEFORE", "dark"), ("THEY SIGN?", "dark"), ("COUNT THEM.", "w")],
  lines=["Three free design revisions before they sign? Count them.",
   "Say each revision takes you four hours.",
   "That's twelve hours per prospect.",
   "Five prospects a month asking for changes.",
   "Sixty hours of design work. Unpaid.",
   "And half of them still don't sign.",
   "Real talk, some revisions are just good service.",
   "But most come from one thing. They can't picture it.",
   "So they keep asking for one more version.",
   "Show them their own room, finished, the first time.", OWN, CTA],
  scenes=[None,
   [N(700, "4 HRS", "y", 200), T(920, "PER REVISION", "w", 80, 0.3)],
   [N(700, "12 HRS", "r", 200), T(920, "PER PROSPECT", "w", 80, 0.3)],
   [N(700, "5", "w", 280), T(940, "PROSPECTS A MONTH", "w", 76, 0.3)],
   [N(700, "60 HRS", "r", 200), T(920, "UNPAID.", "w", 100, 0.4)],
   [T(700, "HALF STILL", "w", 100), T(850, "DON'T SIGN.", "r", 110, 0.4)],
   REAL("SOME REVISIONS ARE", "GOOD SERVICE."),
   [T(700, "THEY CAN'T", "w", 100), T(850, "PICTURE IT.", "y", 110, 0.4)],
   [T(700, "\"ONE MORE", "w", 100), T(850, "VERSION?\"", "y", 110, 0.4)],
   [T(600, "THEIR ROOM,", "w", 100), T(750, "FINISHED,", "y", 120, 0.3), T(900, "THE FIRST TIME.", "w", 90, 0.6)],
   OWN_S, CTA_S],
  caption="Three free design revisions before they sign? Count them.\n4 hours each = 12 hours per prospect. 5 prospects a month = 60 hours unpaid, and half still don't sign.\nFirst tour free, link in bio."),
 dict(id="d029", date="2026-11-24", angle="pain 2", slug="look_different", topic="'I thought it would look different' redo cost",
  hook_card=[("\"I THOUGHT IT", "dark"), ("WOULD LOOK", "dark"), ("DIFFERENT.\"", "dark"), ("COUNT THE COST.", "w")],
  lines=["\"I thought it would look different.\" Count what that costs.",
   "Cabinets are in. The client hates the color.",
   "Say redoing it costs you eighteen hundred dollars.",
   "Plus two days your crew isn't on the next job.",
   "If that happens three times a year, that's fifty-four hundred.",
   "And six lost crew days.",
   "Real talk, some clients change their minds no matter what.",
   "But most just never saw it before you built it.",
   "A color chip isn't a kitchen.",
   "Show them their own room, finished, before you order a thing.", OWN, CTA],
  scenes=[None,
   [T(700, "CABINETS ARE IN.", "w", 92), T(850, "THEY HATE THE COLOR.", "r", 82, 0.5)],
   [T(560, "THE REDO", "grey", 64), N(780, "$1,800", "r", 210, 0.2)],
   [N(700, "2 DAYS", "y", 200), T(920, "CREW OFF THE NEXT JOB", "w", 64, 0.4)],
   [T(560, "3 TIMES A YEAR", "grey", 64), N(780, "$5,400", "r", 210, 0.3)],
   [N(700, "6", "r", 280), T(940, "LOST CREW DAYS", "w", 84, 0.3)],
   REAL("SOME CLIENTS CHANGE", "THEIR MINDS ANYWAY."),
   [T(700, "THEY NEVER SAW IT", "w", 84), T(850, "BEFORE YOU BUILT IT.", "y", 80, 0.5)],
   [T(700, "A COLOR CHIP", "w", 100), T(850, "ISN'T A KITCHEN.", "y", 96, 0.4)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "FINISHED,", "y", 120, 0.3), T(900, "BEFORE YOU ORDER.", "w", 80, 0.6)],
   OWN_S, CTA_S],
  caption="\"I thought it would look different.\" Count what that costs.\n$1,800 redo + 2 crew days, 3 times a year = $5,400 and 6 lost days.\nFirst tour free, link in bio."),
 dict(id="d030", date="2026-11-25", angle="pain 3", slug="two_more_quotes", topic="let me get two more quotes",
  hook_card=[("\"LET ME GET", "dark"), ("TWO MORE", "dark"), ("QUOTES.\"", "dark"), ("HERE'S WHAT'S NEXT.", "w")],
  lines=["\"Let me get two more quotes.\" Here's what happens next.",
   "They call two other contractors.",
   "That's two more weeks of visits and waiting.",
   "By then, your bid is just a PDF in their inbox.",
   "Say you give twelve estimates a month.",
   "Five of them say this. Maybe one comes back.",
   "Real talk, getting three quotes is fair. You'd do it too.",
   "But they'll pick the one they can picture.",
   "Right now, that's nobody.",
   "Show them their own room, finished, before they call anyone else.", OWN, CTA],
  scenes=[None,
   [N(700, "+2", "y", 260), T(940, "MORE CONTRACTORS", "w", 80, 0.3)],
   [N(700, "2 WEEKS", "r", 190), T(920, "VISITS & WAITING", "w", 76, 0.4)],
   [T(700, "YOUR BID =", "w", 100), T(850, "A PDF IN THEIR INBOX.", "r", 74, 0.4)],
   [N(700, "12", "w", 260), T(920, "ESTIMATES A MONTH", "w", 80, 0.3)],
   [N(640, "5", "r", 260), T(860, "SAY IT.", "w", 90, 0.3), T(1000, "1 COMES BACK.", "y", 90, 0.7)],
   REAL("3 QUOTES IS FAIR.", "YOU'D DO IT TOO."),
   [T(700, "THEY PICK THE ONE", "w", 88), T(850, "THEY CAN PICTURE.", "y", 88, 0.4)],
   [T(700, "RIGHT NOW,", "w", 100), T(850, "THAT'S NOBODY.", "r", 110, 0.4)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "FINISHED,", "y", 120, 0.3), T(900, "BEFORE THE NEXT CALL.", "w", 76, 0.6)],
   OWN_S, CTA_S],
  caption="\"Let me get two more quotes.\" Here's what happens next.\n12 estimates, 5 say it, maybe 1 comes back. They pick the one they can picture.\nFirst tour free, link in bio."),
]

def hook_scene(card):
    els = [dict(C(420, "KITCHEN & BATH CONTRACTORS", "dark", "w", 40), at=0)]
    y = 580
    for i, (txt, col) in enumerate(card):
        size = min(104, int(1550 / len(txt)))
        els.append({"type": "text", "at": 0, "y": y, "segs": [[txt, col]], "size": size, "dt": round(-0.3 + 0.3 * i, 2)})
        y += 140
    return {"from": 0, "bg": "yellow", "elements": els}

def main():
    week = {"note": "R360 TikTok week 2026-11-19..11-25", "posts": []}
    for p in POSTS:
        assert len(p["lines"]) == 12 and len(p["scenes"]) == 12, p["id"]
        scenes = [hook_scene(p["hook_card"])]
        for i, els in enumerate(p["scenes"][1:], start=1):
            scenes.append({"from": i, "elements": [dict(e, at=i) for e in els]})
        job = {"episode": p["id"], "series": "KITCHEN & BATH CONTRACTORS", "hook": p["lines"][0], "accent": ACC,
               "voice": f"../voices/{p['id']}.mp3", "atempo": 1.05, "music_vol": 0,
               "out": f"../out/{p['id']}_{p['slug']}.mp4", "lines": p["lines"], "scenes": scenes}
        json.dump(job, open(os.path.join(HERE, "jobs", p["id"] + ".json"), "w"), indent=1)
        words = sum(len(l.split()) for l in p["lines"])
        week["posts"].append({k: p[k] for k in ("id", "date", "angle", "slug", "topic")} |
                             {"time": "23:00", "hook": p["lines"][0], "words": words,
                              "caption": p["caption"] + "\n" + TAGS,
                              "voice_text": ' <break time="0.8s" /> '.join(p["lines"])})
        print(p["id"], words)
    json.dump(week, open(os.path.join(HERE, "week_2026-11-19.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
