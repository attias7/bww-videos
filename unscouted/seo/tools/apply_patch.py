#!/usr/bin/env python3
"""Apply a page-upgrade patch to a built Unscouted page and resolve it into
plain find/replace ops that can be applied to the LIVE WordPress content.

Usage: python3 tools/apply_patch.py <slug>
Reads:  pages/<slug>.patch.json, build/<slug>.html
Writes: build/<slug>.v2.html (preview), pages/<slug>.ops.json (resolved ops)

Patch format:
{
  "slug": "...", "keyword": "...",
  "title": "new SEO title or null", "meta": "new meta description or null",
  "ops": [
    {"type": "insert_before" | "insert_after" | "replace",
     "anchor": "exact substring of build/<slug>.html, must occur exactly once",
     "html": "new html"}
  ],
  "faq_add": [{"q": "...", "a": "plain text answer, no html"}]
}
"""
import json, re, sys, html as H

slug = sys.argv[1]
base = __file__.rsplit('/tools/', 1)[0]
src = open(f'{base}/build/{slug}.html').read()
patch = json.load(open(f'{base}/pages/{slug}.patch.json'))
errors, resolved = [], []

def once(s, anchor):
    n = s.count(anchor)
    if n != 1:
        errors.append(f'anchor found {n}x: {anchor[:80]!r}')
        return False
    return True

out = src
for op in patch.get('ops', []):
    a, h, t = op['anchor'], op['html'], op['type']
    if not once(src, a) or not once(out, a):
        continue
    new = {'insert_before': h + a, 'insert_after': a + h, 'replace': h}[t]
    out = out.replace(a, new)
    resolved.append({'find': a, 'replace': new})

faq = patch.get('faq_add') or []
if faq:
    dets = re.findall(r'<details><summary>.*?</details>', out, re.S)
    if not dets:
        errors.append('no FAQ <details> found')
    else:
        last = dets[-1]
        add = ''.join(f'\n    <details><summary>{H.escape(f["q"], quote=False)}</summary><p>{H.escape(f["a"], quote=False)}</p></details>' for f in faq)
        if once(out, last):
            out = out.replace(last, last + add)
            resolved.append({'find': last, 'replace': last + add})
    m = re.search(r'(<script type="application/ld\+json">)(\{"@context":"https://schema.org","@type":"FAQPage".*?)(</script>)', out, re.S)
    if not m:
        errors.append('no FAQPage JSON-LD found')
    else:
        old = m.group(2)
        data = json.loads(old)
        for f in faq:
            data['mainEntity'].append({'@type': 'Question', 'name': f['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}})
        new = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        if once(out, old):
            out = out.replace(old, new)
            resolved.append({'find': old, 'replace': new})

for bad in ['&&']:
    if bad in out:
        errors.append(f'forbidden {bad!r} in output')
for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', out, re.S):
    try:
        json.loads(s)
    except Exception as e:
        errors.append(f'JSON-LD invalid: {e}')

open(f'{base}/build/{slug}.v2.html', 'w').write(out)
json.dump({'slug': slug, 'title': patch.get('title'), 'meta': patch.get('meta'), 'ops': resolved},
          open(f'{base}/pages/{slug}.ops.json', 'w'), ensure_ascii=False, indent=1)
wc = lambda s: len(re.sub(r'<script.*?</script>|<[^>]+>', ' ', s, flags=re.S).split())
print(f'{slug}: words {wc(src)} -> {wc(out)}, ops {len(resolved)}, faq +{len(faq)}')
if patch.get('title'): print('  title', len(patch['title']), patch['title'])
if patch.get('meta'): print('  meta', len(patch['meta']), patch['meta'])
if errors:
    print('ERRORS:'); [print('  -', e) for e in errors]; sys.exit(1)
print('OK')
