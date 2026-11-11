#!/usr/bin/env python3
"""R360 TikTok week 2026-11-12..11-18 (d017..d023). Writes jobs/dNNN.json + week_2026-11-12.json."""
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
 dict(id="d017", date="2026-11-12", angle="pain 3", slug="ghosted", topic="ghosted after estimate hours",
  hook_card=[("GHOSTED AFTER", "dark"), ("THE ESTIMATE?", "dark"), ("COUNT WHAT", "dark"), ("IT COST YOU.", "w")],
  lines=["Ghosted after the estimate? Count what it cost you.",
   "Say you give ten estimates a month.",
   "Four of them just go quiet.",
   "Each one took about three hours. Visit, measure, write up.",
   "That's twelve hours a month for nothing.",
   "Almost a hundred and fifty hours a year.",
   "Real talk, some of them were never buying.",
   "But most go quiet because they can't picture it.",
   "Silence is easier than saying no to a guess.",
   "Show them their own room, finished, before you leave.", OWN, CTA],
  scenes=[None,
   [N(700, "10", "w", 260), T(920, "ESTIMATES A MONTH", "w", 80)],
   [N(700, "4", "r", 280), T(940, "GO QUIET", "w", 96, 0.3)],
   [N(700, "3 HRS", "y", 200), T(920, "VISIT · MEASURE · WRITE UP", "grey", 56, 0.4)],
   [N(700, "12 HRS", "r", 200), T(920, "A MONTH. FOR NOTHING.", "w", 76, 0.4)],
   [N(700, "~150", "r", 240), T(940, "HOURS A YEAR", "w", 90, 0.3)],
   REAL("SOME WERE", "NEVER BUYING."),
   [T(700, "THEY CAN'T", "w", 100), T(850, "PICTURE IT.", "y", 110, 0.4)],
   [T(700, "SILENCE IS EASIER", "w", 84), T(850, "THAN SAYING NO.", "r", 90, 0.5)],
   [T(600, "SHOW THEM", "w", 96), T(750, "THEIR ROOM,", "y", 110, 0.3), T(900, "FINISHED.", "y", 120, 0.5)],
   OWN_S, CTA_S],
  caption="Ghosted after the estimate? Count what it cost you.\n10 estimates, 4 go quiet, 3 hours each = 12 hours a month for nothing. Most go quiet because they can't picture it.\nFirst tour free, link in bio."),
 dict(id="d018", date="2026-11-13", angle="pain 2", slug="door_sample", topic="samples vs finished room, cheaper bid",
  hook_card=[("NOBODY CAN", "dark"), ("PICTURE A KITCHEN", "dark"), ("FROM A", "dark"), ("DOOR SAMPLE.", "w")],
  lines=["Nobody can picture a kitchen from a door sample.",
   "You hand them a white shaker door and a tile chip.",
   "Your bid is forty-two thousand.",
   "The other guy says thirty-six.",
   "They can't see a difference, so they see the price.",
   "Six thousand dollars, and you lose the job.",
   "Real talk, sometimes cheaper really is the better fit.",
   "But usually they just can't imagine yours.",
   "Samples show parts. People buy the finished room.",
   "Show them their own kitchen, done, on their phone.", OWN, CTA],
  scenes=[None,
   [T(700, "A SHAKER DOOR.", "w", 96), T(850, "A TILE CHIP.", "w", 96, 0.6)],
   [T(560, "YOUR BID", "grey", 64), N(760, "$42,000", "w", 190, 0.2)],
   [T(560, "THEIR BID", "grey", 64), N(760, "$36,000", "y", 190, 0.2)],
   [T(700, "NO DIFFERENCE?", "w", 96), T(850, "THEY SEE PRICE.", "r", 96, 0.5)],
   [N(700, "$6,000", "r", 210), T(930, "AND YOU LOSE IT.", "w", 84, 0.4)],
   REAL("SOMETIMES CHEAPER", "IS THE BETTER FIT."),
   [T(700, "THEY CAN'T", "w", 100), T(850, "IMAGINE YOURS.", "y", 100, 0.4)],
   [T(700, "SAMPLES = PARTS.", "w", 92), T(850, "THEY BUY THE ROOM.", "y", 88, 0.6)],
   [T(600, "THEIR KITCHEN,", "w", 100), T(750, "DONE,", "y", 120, 0.3), T(900, "ON THEIR PHONE.", "y", 96, 0.5)],
   OWN_S, CTA_S],
  caption="Nobody can picture a kitchen from a door sample.\n$42k vs $36k, and all they've seen is a door and a tile chip. So they compare price.\nFirst tour free, link in bio."),
 dict(id="d019", date="2026-11-14", angle="pain 1", slug="referrals_vs_ads", topic="referrals close, ad leads don't",
  hook_card=[("WHY REFERRALS", "dark"), ("CLOSE AND", "dark"), ("YOUR AD LEADS", "dark"), ("DON'T.", "w")],
  lines=["Why your referrals close and your ad leads don't.",
   "A referral already saw a kitchen you finished.",
   "At their friend's house. In real life.",
   "An ad lead saw nothing. Just your logo.",
   "Say referrals close seven in ten.",
   "And ad leads close two in ten.",
   "The gap isn't your price. It's what they've seen.",
   "Real talk, you can't make every lead a referral.",
   "But you can show them a finished room first.",
   "Their own room, finished, before they decide.", OWN, CTA],
  scenes=[None,
   [T(560, "REFERRAL", "y", 80), T(720, "ALREADY SAW", "w", 96, 0.2), T(870, "YOUR WORK.", "w", 96, 0.4)],
   [T(700, "AT A FRIEND'S HOUSE.", "w", 80), T(850, "IN REAL LIFE.", "y", 96, 0.5)],
   [T(560, "AD LEAD", "grey", 80), T(720, "SAW NOTHING.", "r", 100, 0.2), T(870, "JUST A LOGO.", "w", 90, 0.6)],
   [T(560, "REFERRALS", "grey", 64), N(780, "7 / 10", "g", 220, 0.2)],
   [T(560, "AD LEADS", "grey", 64), N(780, "2 / 10", "r", 220, 0.2)],
   [T(700, "NOT YOUR PRICE.", "w", 96), T(850, "WHAT THEY'VE SEEN.", "y", 88, 0.6)],
   REAL("NOT EVERY LEAD", "IS A REFERRAL."),
   [T(700, "SHOW A FINISHED", "w", 92), T(850, "ROOM FIRST.", "y", 110, 0.4)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "FINISHED,", "y", 120, 0.3), T(900, "BEFORE THEY DECIDE.", "w", 80, 0.6)],
   OWN_S, CTA_S],
  caption="Why your referrals close and your ad leads don't.\nA referral already saw a kitchen you finished. An ad lead saw your logo. That's the gap, not your price.\nFirst tour free, link in bio."),
 dict(id="d020", date="2026-11-15", angle="pain 5", slug="second_walkthrough", topic="second walkthrough hours",
  hook_card=[("DRIVING BACK", "dark"), ("FOR A SECOND", "dark"), ("WALKTHROUGH?", "dark"), ("DO THIS MATH.", "w")],
  lines=["Driving back for a second walkthrough? Do this math.",
   "Say five clients a month want you to come back.",
   "To go over it again before they decide.",
   "That's two hours each, with the drive.",
   "Ten hours a month. And two of them still say no.",
   "They're not asking for you. They're asking to see it.",
   "Real talk, some jobs do need a second visit.",
   "But most second visits just mean help me picture it.",
   "Answer that on the first visit.",
   "Send them their own room, finished, before you leave.", OWN, CTA],
  scenes=[None,
   [N(700, "5", "w", 280), T(940, "CLIENTS WANT YOU BACK", "w", 74, 0.3)],
   [T(700, "\"LET'S GO OVER", "w", 92), T(850, "IT AGAIN.\"", "y", 100, 0.4)],
   [N(700, "2 HRS", "y", 210), T(920, "EACH, WITH THE DRIVE", "grey", 64, 0.4)],
   [N(700, "10 HRS", "r", 200), T(920, "AND 2 STILL SAY NO.", "w", 80, 0.8)],
   [T(700, "THEY WANT", "w", 100), T(850, "TO SEE IT.", "y", 120, 0.6)],
   REAL("SOME JOBS NEED", "A SECOND VISIT."),
   [T(700, "\"HELP ME", "w", 100), T(850, "PICTURE IT.\"", "y", 110, 0.4)],
   [T(700, "ANSWER IT ON", "w", 96), T(850, "THE FIRST VISIT.", "y", 96, 0.3)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "FINISHED,", "y", 120, 0.3), T(900, "BEFORE YOU LEAVE.", "w", 84, 0.6)],
   OWN_S, CTA_S],
  caption="Driving back for a second walkthrough? Do this math.\n5 clients a month, 2 hours each = 10 hours. Most of them just mean \"help me picture it.\"\nFirst tour free, link in bio."),
 dict(id="d021", date="2026-11-16", angle="pain 4", slug="render_week", topic="renders arrive after the decision",
  hook_card=[("YOUR RENDERS", "dark"), ("TAKE A WEEK.", "dark"), ("THEY DECIDE", "dark"), ("IN TWO DAYS.", "w")],
  lines=["Your renders take a week. They decide in two days.",
   "Say you send the drawings out after the walkthrough.",
   "The designer needs five to seven days.",
   "Meanwhile, two other contractors already sent prices.",
   "By the time your render lands, they've picked one.",
   "You paid three hundred dollars to show up late.",
   "Real talk, detailed drawings still matter for the build.",
   "But the decision happens in the first few days.",
   "That's when they need to see it.",
   "Their own room, finished, the same day.", OWN, CTA],
  scenes=[None,
   [T(700, "DRAWINGS GO OUT", "w", 92), T(850, "AFTER THE VISIT.", "grey", 84, 0.4)],
   [N(700, "5–7", "y", 240), T(940, "DAYS", "w", 96, 0.3)],
   [N(700, "2", "r", 280), T(940, "OTHER PRICES ALREADY IN", "w", 70, 0.4)],
   [T(700, "RENDER LANDS.", "w", 96), T(850, "THEY PICKED ONE.", "r", 96, 0.6)],
   [N(700, "$300", "r", 220), T(930, "TO SHOW UP LATE", "w", 84, 0.4)],
   REAL("DRAWINGS STILL", "MATTER FOR THE BUILD."),
   [T(700, "THEY DECIDE IN", "w", 96), T(850, "THE FIRST DAYS.", "y", 100, 0.4)],
   [T(700, "THAT'S WHEN", "w", 100), T(850, "THEY NEED TO SEE IT.", "y", 84, 0.3)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "FINISHED,", "y", 120, 0.3), T(900, "THE SAME DAY.", "w", 96, 0.5)],
   OWN_S, CTA_S],
  caption="Your renders take a week. They decide in two days.\nBy the time the $300 render lands, two other prices are already in.\nFirst tour free, link in bio."),
 dict(id="d022", date="2026-11-17", angle="pain 3", slug="driveway", topic="excitement fades after the visit",
  hook_card=[("THE BEST TIME", "dark"), ("TO CLOSE IS", "dark"), ("BEFORE YOU LEAVE", "dark"), ("THE DRIVEWAY.", "w")],
  lines=["The best time to close is before you leave the driveway.",
   "At the walkthrough, they're excited. They're picturing it.",
   "A week later, they're comparing three PDFs.",
   "Say you leave ten homes a month with I'll send a quote.",
   "If three would have said yes that night...",
   "That's three jobs you let cool down.",
   "Real talk, nobody should be pushed into a kitchen.",
   "But excitement fades faster than you think.",
   "Give them something to keep the picture alive.",
   "Their own room, finished, on their phone tonight.", OWN, CTA],
  scenes=[None,
   [T(700, "AT THE WALKTHROUGH:", "w", 84), T(850, "EXCITED.", "g", 120, 0.6)],
   [T(560, "A WEEK LATER:", "grey", 70), N(800, "3 PDFs", "r", 200, 0.3)],
   [N(700, "10", "w", 260), T(930, "\"I'LL SEND A QUOTE.\"", "w", 80, 0.5)],
   [N(700, "3", "y", 280), T(940, "WOULD HAVE SAID YES", "w", 76, 0.3)],
   [T(700, "3 JOBS YOU LET", "w", 96), T(850, "COOL DOWN.", "r", 110, 0.4)],
   REAL("NOBODY SHOULD", "BE PUSHED."),
   [T(700, "EXCITEMENT", "w", 104), T(850, "FADES FAST.", "r", 110, 0.4)],
   [T(700, "KEEP THE PICTURE", "w", 92), T(850, "ALIVE.", "y", 130, 0.4)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "FINISHED,", "y", 120, 0.3), T(900, "ON THEIR PHONE.", "w", 90, 0.5)],
   OWN_S, CTA_S],
  caption="The best time to close is before you leave the driveway.\nAt the walkthrough they're excited. A week later they're comparing 3 PDFs.\nFirst tour free, link in bio."),
 dict(id="d023", date="2026-11-18", angle="pain 1", slug="price_vs_close", topic="raise prices vs close one more",
  hook_card=[("RAISE PRICES 10%", "dark"), ("OR CLOSE", "dark"), ("ONE MORE", "dark"), ("JOB?", "w")],
  lines=["Raise your prices ten percent, or close one more job?",
   "Say your average job is thirty thousand.",
   "You close three out of ten estimates a month.",
   "That's ninety thousand a month.",
   "Raise prices ten percent. Ninety-nine thousand.",
   "Close just one more. A hundred twenty thousand.",
   "One extra yes beats the price hike by twenty-one grand.",
   "Real talk, if you're underpriced, raise it anyway.",
   "But the bigger lever is your close rate.",
   "Show them their own room, finished, before they decide.", OWN, CTA],
  scenes=[None,
   [T(560, "AVERAGE JOB", "grey", 64), N(780, "$30,000", "w", 200, 0.2)],
   [T(560, "YOU CLOSE", "grey", 64), N(780, "3 / 10", "w", 220, 0.2)],
   [N(700, "$90K", "w", 240), T(930, "A MONTH", "grey", 80, 0.3)],
   [C(520, "+10% PRICE", "w", "dark", 54), N(760, "$99K", "y", 240, 0.4)],
   [C(520, "+1 JOB", "y", "dark", 54), N(760, "$120K", "g", 240, 0.4)],
   [N(700, "+$21K", "g", 230), T(930, "FROM ONE MORE YES", "w", 80, 0.5)],
   REAL("UNDERPRICED?", "RAISE IT ANYWAY."),
   [T(700, "THE BIGGER LEVER:", "w", 88), T(850, "CLOSE RATE.", "y", 110, 0.4)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "FINISHED,", "y", 120, 0.3), T(900, "BEFORE THEY DECIDE.", "w", 80, 0.6)],
   OWN_S, CTA_S],
  caption="Raise your prices 10%, or close one more job?\n$30k jobs, 3 in 10: $90k. +10% price: $99k. One more yes: $120k.\nFirst tour free, link in bio."),
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
    week = {"note": "R360 TikTok week 2026-11-12..11-18", "posts": []}
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
    json.dump(week, open(os.path.join(HERE, "week_2026-11-12.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
