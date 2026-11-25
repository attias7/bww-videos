#!/usr/bin/env python3
"""R360 TikTok week 2026-11-26..12-02 (d031..d037). Writes jobs/dNNN.json + week_2026-11-26.json."""
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
 dict(id="d031", date="2026-11-26", angle="pain 1", slug="slow_january", topic="slow January, fix the close rate now",
  hook_card=[("DREADING A", "dark"), ("SLOW JANUARY?", "dark"), ("FIX THIS", "dark"), ("NUMBER NOW.", "w")],
  lines=["Dreading a slow January? Fix this number now.",
   "Say you give ten estimates between now and Christmas.",
   "Average job, twenty-five thousand.",
   "You close three. Seventy-five thousand on the calendar.",
   "Close five instead, and it's a hundred twenty-five.",
   "That's two more jobs to start in January.",
   "Real talk, winter is slower for most remodelers.",
   "But you don't need more leads to fill it.",
   "You need more of these ten to say yes.",
   "Show them their own room, finished, before you leave.", OWN, CTA],
  scenes=[None,
   [N(700, "10", "w", 260), T(920, "ESTIMATES BEFORE CHRISTMAS", "w", 62, 0.3)],
   [T(560, "AVERAGE JOB", "grey", 64), N(780, "$25,000", "w", 190, 0.2)],
   [T(560, "YOU CLOSE 3", "grey", 64), N(780, "$75K", "w", 240, 0.2)],
   [T(560, "CLOSE 5", "grey", 64), N(780, "$125K", "g", 240, 0.2)],
   [C(520, "JANUARY", "y", "dark", 54), N(760, "+2 JOBS", "g", 210, 0.4)],
   REAL("WINTER IS SLOWER", "FOR MOST OF US."),
   [T(700, "YOU DON'T NEED", "w", 100), T(850, "MORE LEADS.", "r", 110, 0.4)],
   [T(700, "MORE OF THESE 10", "w", 92), T(850, "TO SAY YES.", "y", 110, 0.4)],
   [T(600, "SHOW THEM", "w", 96), T(750, "THEIR ROOM,", "y", 110, 0.3), T(900, "FINISHED.", "y", 120, 0.5)],
   OWN_S, CTA_S],
  caption="Dreading a slow January? Fix this number now.\n10 estimates at $25k before Christmas. Close 3 = $75k. Close 5 = $125k, two more jobs for January.\nFirst tour free, link in bio."),
 dict(id="d032", date="2026-11-27", angle="pain 2", slug="more_than_expected", topic="\"that's more than we expected\"",
  hook_card=[("\"THAT'S MORE", "dark"), ("THAN WE", "dark"), ("EXPECTED.\"", "dark"), ("HERE'S WHAT IT MEANS.", "w")],
  lines=["\"That's more than we expected.\" Here's what they mean.",
   "Your bathroom bid is thirty-two thousand.",
   "They had twenty-five in their head.",
   "Seven thousand dollars they can't explain to themselves.",
   "So they go looking for the twenty-five thousand guy.",
   "And you lose a job you priced right.",
   "Real talk, sometimes the budget really is the budget.",
   "But most people stretch for something they can see.",
   "Nobody stretches for a line on a PDF.",
   "Show them their own bathroom, finished, before they see the number.", OWN, CTA],
  scenes=[None,
   [T(560, "YOUR BID", "grey", 64), N(780, "$32,000", "w", 190, 0.2)],
   [T(560, "IN THEIR HEAD", "grey", 64), N(780, "$25,000", "y", 190, 0.2)],
   [N(700, "$7,000", "r", 210), T(930, "THEY CAN'T EXPLAIN", "w", 80, 0.4)],
   [T(700, "THEY LOOK FOR", "w", 100), T(850, "THE $25K GUY.", "r", 100, 0.4)],
   [T(700, "YOU LOSE A JOB", "w", 96), T(850, "YOU PRICED RIGHT.", "y", 90, 0.4)],
   REAL("SOMETIMES THE BUDGET", "IS THE BUDGET."),
   [T(700, "PEOPLE STRETCH", "w", 100), T(850, "FOR WHAT THEY SEE.", "y", 90, 0.4)],
   [T(700, "NOT FOR A LINE", "w", 100), T(850, "ON A PDF.", "r", 110, 0.4)],
   [T(600, "THEIR BATHROOM,", "w", 96), T(750, "FINISHED,", "y", 120, 0.3), T(900, "BEFORE THE NUMBER.", "w", 80, 0.6)],
   OWN_S, CTA_S],
  caption="\"That's more than we expected.\" Here's what they mean.\n$32k bid, $25k in their head. $7k they can't explain to themselves, so they go find the $25k guy.\nFirst tour free, link in bio."),
 dict(id="d033", date="2026-11-28", angle="pain 3", slug="excitement_expires", topic="bid valid 30 days, excitement lasts 3",
  hook_card=[("YOUR BID IS GOOD", "dark"), ("FOR 30 DAYS.", "dark"), ("THEIR EXCITEMENT", "dark"), ("LASTS 3.", "w")],
  lines=["Your bid is good for thirty days. Their excitement lasts three.",
   "Day one, they loved everything you said.",
   "Day three, they're back to scrolling kitchens online.",
   "Day ten, \"we're still thinking about it.\"",
   "Say you send eight bids a month.",
   "Five of them cool off like this. Five jobs on ice.",
   "Real talk, big decisions take time. That's fair.",
   "But excitement fades fastest when there's nothing to look at.",
   "A bid gives them a number, not a picture.",
   "Give them their own room, finished, to look at on day three.", OWN, CTA],
  scenes=[None,
   [C(520, "DAY 1", "y", "dark", 54), T(760, "THEY LOVED IT.", "g", 110, 0.3)],
   [C(520, "DAY 3", "y", "dark", 54), T(760, "SCROLLING ONLINE.", "w", 96, 0.3)],
   [C(520, "DAY 10", "y", "dark", 54), T(760, "\"STILL THINKING.\"", "r", 100, 0.3)],
   [N(700, "8", "w", 280), T(940, "BIDS A MONTH", "w", 90, 0.3)],
   [N(700, "5", "r", 280), T(940, "JOBS ON ICE", "w", 90, 0.3)],
   REAL("BIG DECISIONS", "TAKE TIME."),
   [T(700, "NOTHING TO", "w", 100), T(850, "LOOK AT.", "r", 120, 0.4)],
   [T(700, "A NUMBER,", "w", 100), T(850, "NOT A PICTURE.", "y", 104, 0.4)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "FINISHED,", "y", 120, 0.3), T(900, "ON DAY THREE.", "w", 90, 0.6)],
   OWN_S, CTA_S],
  caption="Your bid is good for 30 days. Their excitement lasts 3.\nDay 1 they love it, day 10 they're \"still thinking.\" 8 bids a month, 5 go cold.\nFirst tour free, link in bio."),
 dict(id="d034", date="2026-11-29", angle="pain 4", slug="finish_selection", topic="hours picking finishes before they sign",
  hook_card=[("6 HOURS", "dark"), ("PICKING FINISHES.", "dark"), ("THEN THEY", "dark"), ("DIDN'T SIGN.", "w")],
  lines=["Six hours picking finishes. Then they didn't sign.",
   "Tile samples. Cabinet doors. Two trips to the showroom.",
   "That's six hours before there's even a contract.",
   "Say you do this with four clients a month.",
   "Twenty-four hours of free design help.",
   "Two of them take your choices to a cheaper guy.",
   "Real talk, helping clients choose is part of good service.",
   "But they keep picking because they can't see the result.",
   "Every sample is a guess.",
   "Show them their own room, finished, with those finishes in it.", OWN, CTA],
  scenes=[None,
   [T(600, "TILE SAMPLES.", "w", 96), T(740, "CABINET DOORS.", "w", 96, 0.3), T(880, "2 SHOWROOM TRIPS.", "y", 90, 0.6)],
   [N(700, "6 HRS", "r", 200), T(920, "BEFORE A CONTRACT", "w", 80, 0.4)],
   [N(700, "4", "w", 280), T(940, "CLIENTS A MONTH", "w", 86, 0.3)],
   [N(700, "24 HRS", "r", 200), T(920, "FREE DESIGN HELP", "w", 80, 0.4)],
   [N(700, "2", "r", 280), T(940, "GO TO A CHEAPER GUY", "w", 72, 0.3)],
   REAL("HELPING THEM CHOOSE", "IS GOOD SERVICE."),
   [T(700, "THEY CAN'T SEE", "w", 100), T(850, "THE RESULT.", "y", 110, 0.4)],
   [T(700, "EVERY SAMPLE", "w", 100), T(850, "IS A GUESS.", "r", 110, 0.4)],
   [T(600, "THEIR ROOM,", "w", 100), T(750, "FINISHED,", "y", 120, 0.3), T(900, "WITH THOSE FINISHES.", "w", 76, 0.6)],
   OWN_S, CTA_S],
  caption="Six hours picking finishes. Then they didn't sign.\n4 clients a month = 24 hours of free design help, and 2 take your choices to a cheaper guy.\nFirst tour free, link in bio."),
 dict(id="d035", date="2026-11-30", angle="pain 5", slug="explaining_calls", topic="phone calls explaining one estimate",
  hook_card=[("COUNT THE CALLS", "dark"), ("IT TAKES TO", "dark"), ("EXPLAIN ONE", "dark"), ("ESTIMATE.", "w")],
  lines=["Count the calls it takes to explain one estimate.",
   "\"What does the vanity look like?\"",
   "\"Where does the shower door go?\"",
   "Say it's three calls, twenty minutes each, per estimate.",
   "Ten estimates a month, that's ten hours on the phone.",
   "Most of it at night, after the crew goes home.",
   "Real talk, good communication wins jobs.",
   "But every one of those calls is the same question.",
   "\"What will it look like?\"",
   "Show them their own room, finished, and most of those calls stop.", OWN, CTA],
  scenes=[None,
   [T(700, "\"WHAT DOES THE", "w", 96), T(850, "VANITY LOOK LIKE?\"", "y", 90, 0.4)],
   [T(700, "\"WHERE DOES THE", "w", 96), T(850, "SHOWER DOOR GO?\"", "y", 90, 0.4)],
   [N(700, "3 × 20 MIN", "w", 170), T(920, "PER ESTIMATE", "grey", 70, 0.4)],
   [N(700, "10 HRS", "r", 200), T(920, "ON THE PHONE", "w", 86, 0.4)],
   [T(700, "MOST OF IT", "w", 100), T(850, "AT NIGHT.", "r", 120, 0.4)],
   REAL("GOOD COMMUNICATION", "WINS JOBS."),
   [T(700, "EVERY CALL,", "w", 100), T(850, "SAME QUESTION.", "y", 104, 0.4)],
   [T(760, "\"WHAT WILL IT", "w", 104), T(900, "LOOK LIKE?\"", "y", 120, 0.3)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "FINISHED.", "y", 120, 0.3), T(900, "FEWER CALLS.", "w", 90, 0.6)],
   OWN_S, CTA_S],
  caption="Count the calls it takes to explain one estimate.\n3 calls, 20 minutes each, 10 estimates a month = 10 hours on the phone, mostly at night.\nFirst tour free, link in bio."),
 dict(id="d036", date="2026-12-01", angle="pain 2", slug="skipped_upgrades", topic="clients skip upgrades they can't picture",
  hook_card=[("CLIENTS SKIP", "dark"), ("UPGRADES THEY", "dark"), ("CAN'T PICTURE.", "dark"), ("COUNT IT.", "w")],
  lines=["Clients skip upgrades they can't picture. Count it.",
   "You offer quartz, tile to the ceiling, better lighting.",
   "They say, \"let's keep it simple.\"",
   "Say that's four thousand dollars of upgrades, gone.",
   "On three jobs a month, that's twelve thousand.",
   "A year, about a hundred forty thousand left on the table.",
   "Real talk, some people really do want simple.",
   "But a lot of them just couldn't see the difference.",
   "To them, it just sounds like extra cost.",
   "Show them their own room, finished, with the upgrade and without.", OWN, CTA],
  scenes=[None,
   [T(600, "QUARTZ.", "w", 100), T(740, "TILE TO THE CEILING.", "w", 86, 0.3), T(880, "BETTER LIGHTING.", "y", 92, 0.6)],
   [T(760, "\"LET'S KEEP IT", "w", 104), T(900, "SIMPLE.\"", "r", 120, 0.3)],
   [T(560, "UPGRADES GONE", "grey", 64), N(780, "$4,000", "r", 210, 0.2)],
   [T(560, "3 JOBS A MONTH", "grey", 64), N(780, "$12,000", "r", 190, 0.2)],
   [T(560, "A YEAR", "grey", 64), N(780, "~$140K", "r", 220, 0.2)],
   REAL("SOME PEOPLE REALLY", "DO WANT SIMPLE."),
   [T(700, "THEY COULDN'T SEE", "w", 88), T(850, "THE DIFFERENCE.", "y", 100, 0.4)],
   [T(760, "IT SOUNDS LIKE", "w", 100), T(900, "EXTRA COST.", "r", 120, 0.3)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "WITH THE UPGRADE", "y", 96, 0.3), T(900, "AND WITHOUT.", "w", 96, 0.6)],
   OWN_S, CTA_S],
  caption="Clients skip upgrades they can't picture. Count it.\n$4k of upgrades on 3 jobs a month = $12k. About $140k a year left on the table.\nFirst tour free, link in bio."),
 dict(id="d037", date="2026-12-02", angle="pain 1", slug="yearly_math", topic="one more yes a month, yearly math",
  hook_card=[("ONE MORE YES", "dark"), ("A MONTH.", "dark"), ("DO THE", "dark"), ("YEARLY MATH.", "w")],
  lines=["One more yes a month. Do the yearly math.",
   "Say your average kitchen is thirty thousand.",
   "One more signed job a month.",
   "That's three hundred sixty thousand more in a year.",
   "Same leads. Same ad spend. Same crew size to start.",
   "Most contractors plan next year around more leads.",
   "Real talk, growth usually needs both.",
   "But the cheapest yes is from someone already in front of you.",
   "They just need to see it before they sign.",
   "Show them their own room, finished, at the first visit.", OWN, CTA],
  scenes=[None,
   [T(560, "AVERAGE KITCHEN", "grey", 64), N(780, "$30,000", "w", 190, 0.2)],
   [C(520, "+1 JOB", "y", "dark", 54), T(760, "EVERY MONTH", "w", 110, 0.3)],
   [N(700, "+$360K", "g", 220), T(930, "IN A YEAR", "w", 90, 0.4)],
   [T(650, "SAME LEADS.", "w", 96), T(790, "SAME AD SPEND.", "w", 96, 0.3), T(930, "SAME CREW.", "y", 96, 0.6)],
   [T(700, "NEXT YEAR'S PLAN:", "w", 96), T(850, "\"MORE LEADS.\"", "r", 110, 0.4)],
   REAL("GROWTH USUALLY", "NEEDS BOTH."),
   [T(700, "THE CHEAPEST YES", "w", 92), T(850, "IS ALREADY HERE.", "y", 96, 0.4)],
   [T(700, "THEY NEED TO SEE IT", "w", 84), T(850, "BEFORE THEY SIGN.", "y", 90, 0.4)],
   [T(600, "THEIR OWN ROOM,", "w", 96), T(750, "FINISHED,", "y", 120, 0.3), T(900, "AT THE FIRST VISIT.", "w", 80, 0.6)],
   OWN_S, CTA_S],
  caption="One more yes a month. Do the yearly math.\n$30k kitchen, one more signed job a month = $360k more in a year. Same leads, same ad spend.\nFirst tour free, link in bio."),
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
    week = {"note": "R360 TikTok week 2026-11-26..12-02", "posts": []}
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
    json.dump(week, open(os.path.join(HERE, "week_2026-11-26.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
