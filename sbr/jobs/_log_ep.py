"""Log one scheduled episode: append episodes.csv row + mark hook ✅ in HOOKS.md. Usage: python3 _log_ep.py N "status" """
import csv, sys, datetime, re, json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
M = {
15: ("2026-10-11","pain","Introverts: get contractors to pay you, no sales calls.","why every make-money-online path ends in a sales call + rank & rent where the customer finds you (months; leads don't always close)","ICP: night-time pain (sales dread) | hook type: hybrid (callout+result+objection removal)"),
16: ("2026-10-12","fear-tech","Never built a site? Build one without code.","how small one lead site is (one service, one town, 3 parts; AI-assisted) + ranking is the hard part","ICP: fear (stuck on the tech) | hook type: hybrid (callout+ease)"),
17: ("2026-10-13","suspicion","Sick of income screenshots? Here's the honest version.","what rank & rent actually takes: months, some sites never rank, leads that don't close","ICP: suspicion (income screenshots / courses) | hook type: callout/contrarian"),
18: ("2026-10-14","education","Never heard of SEO? Here it is in thirty seconds.","SEO in plain words: answer the search, be useful, get mentioned; slow but a skill that stacks","ICP: goal (a skill that compounds) | hook type: callout"),
19: ("2026-10-15","fear-owners","Scared to message a business owner? Same.","reaching contractors in writing: 27-comment group post + pay-on-close offer message (some won't reply)","ICP: fear (looking stupid talking to a business owner) | hook type: pain"),
20: ("2026-10-16","build-in-public","If you feel behind, start with one small thing.","22 + introvert -> one service, one town, one site; first lead took ~1-3 months","ICP: night-time pain (feeling behind) + goal (proof to self/family) | hook type: callout/pain"),
21: ("2026-10-17","enemy+soft-product","A two thousand dollar course won't make you less shy.","guru courses still end in calls; build around introversion + soft $37 Starter Kit mention (no calls, no upsell)","ICP: enemy ($2,000 courses with upsells/calls) | hook type: contrarian"),
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
