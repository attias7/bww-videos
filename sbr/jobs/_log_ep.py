"""Log one scheduled episode: append episodes.csv row + mark hook ✅ in HOOKS.md. Usage: python3 _log_ep.py N "status" """
import csv, sys, datetime, re, json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
M = {
22: ("2026-10-18","pain","Every side hustle ends with: now get on a call.","why every side hustle (agency/freelancing/closing) ends in a call + flip it: customer finds you, contractor pays on close (months; leads don't always close)","ICP: night-time pain (sales dread) | hook type: pain"),
23: ("2026-10-19","fear-tech","If you've never built a website, start here.","start with one service + one town, search it first, site = 3 things, AI helps; ranking takes months and might not happen","ICP: fear (stuck on the tech) | hook type: callout"),
24: ("2026-10-20","suspicion","Month one, nothing happens. Here's why that's normal.","honest timeline: new site is a stranger to Google, month one is quiet, make page useful; first lead ~1-3 months; some sites never rank","ICP: suspicion (income screenshots skip the boring part) + fear (months and it never works) | hook type: time/honest"),
25: ("2026-10-21","education","Why contractors say yes to: pay only if it closes.","pay-on-close from the contractor's side vs ads/lead sellers; risk on you; some say no, trust needed","ICP: goal (a skill that compounds: offer design) | hook type: mechanism"),
26: ("2026-10-22","fear-owners","Find a contractor without picking up the phone.","3 written ways to reach contractors (FB group - the 27 comments, contact form, email from Google listing) + short message; comments aren't customers","ICP: fear (looking stupid talking to a business owner) | hook type: effort reduction"),
27: ("2026-10-23","build-in-public","How I built a business around being an introvert.","22 + introvert -> 3 design rules (customers find me, writing not calls, pay-on-close); not zero talking; first lead ~1-3 months","ICP: night-time pain (dreads selling) + goal (proof they can do it) | hook type: how-I"),
28: ("2026-10-24","enemy+soft-product","Learn sales first is terrible advice for introverts.","'learn sales first' advice vs changing the model + soft $37 Starter Kit mention (no calls, no upsell)","ICP: enemy ('you have to be good at sales' advice) | hook type: contrarian"),
}
n = int(sys.argv[1]); status = sys.argv[2]
d, pillar, hook, topic, notes = M[n]
out = json.load(open(f'jobs/ep{n}.json'))['out']
fname = 'sbr_' + os.path.basename(out)
rows = list(csv.reader(open('episodes.csv')))
rows = [r for r in rows if r[0] != str(n)]
rows.append([str(n), d, pillar, hook, topic, fname, status, datetime.date.today().isoformat(), notes + f'; jobs/ep{n}.json; custom hook cover; voice Arthur eleven_v4'])
csv.writer(open('episodes.csv','w',newline='')).writerows(rows)
h = open('HOOKS.md').read()
base = hook.rstrip('.')
pat = re.compile(r'^- (?!✅)(' + re.escape(base) + r'\.?)\s*$', re.M)
if pat.search(h): h = pat.sub(lambda m: f'- ✅ Ep {n} — {m.group(1)}', h, count=1)
elif f'Ep {n} —' not in h: h = h.replace('## 3. Hook bank (✅ = used, with the episode)\n', f'## 3. Hook bank (✅ = used, with the episode)\n- ✅ Ep {n} — {hook}\n', 1)
open('HOOKS.md','w').write(h)
print('logged', n)
