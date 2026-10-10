# Unscouted article pages: writing + HTML spec

You are writing ONE OR TWO SEO pages for Unscouted (football/soccer self-coaching for players 15–21 who are NOT in an academy). Research with the keyword plan is in `/home/claude/bww-videos/unscouted/seo/RESEARCH.md` — read the section for your page(s) and follow its plan (title, meta, H1, H2 outline, angle, FAQ, internal links, verified competitor facts). Before writing, run a few WebSearch / WebFetch checks of your own on the keyword to confirm what the top pages cover, and make yours clearly better: more specific, more useful to a player training alone, real worked examples, honest.

## Hard rules
- Never mention the owner's name. Brand voice is "Unscouted" / "we" sparingly, mostly direct "you". Do NOT invent personal stories, experiences, testimonials, results, stats or quotes. No "go pro" or results promises.
- Facts about competitors: ONLY the verified ones in RESEARCH.md section 4 (with their source links) or ones you verify yourself on the official site (cite). Say "prices checked October 2026". Fair, not bashing.
- Studies: only cite if you have read the source; word it carefully.
- Plain English a 16-year-old reads easily. Short paragraphs. No fluff intros, no "In today's fast-paced world". Avoid AI tells (delve, unlock, elevate, game-changer, "it's not just X, it's Y", em-dash overuse — use commas/colons).
- Length: 1,300–2,200 words of real content. Not padded.
- JavaScript: none, except the FAQ JSON-LD block. NEVER write `&&` anywhere. Use `&amp;` for a literal ampersand in text.
- Use "football" or "soccer" as the page plan says (US pages "soccer", UK pages "football"); mention the other term once naturally.

## Products and URLs (for internal links — use these relative URLs)
- Free test (8 situations, free, no sign-up): `/soccer-iq-test/`
- Pause & Decide: 100 Situations ($27, interactive, 20 per position): `/shop/#pause-and-decide`
- The Basics Kit ($47; 10 guides on analysing a player, a game, a team and yourself, training system, 12-week plan, worksheets, mental side): `/shop/#basics-kit` — check: if unsure of anchor use `/shop/`
- Position packs ($17 each): `/shop/#striker`, `/shop/#winger`, `/shop/#number-10`, `/shop/#defender-pack`
- Game Library ($27, 84 pro games to watch and analyse with notes to compare): `/shop/#game-library`
- Everything Bundle ($99): `/shop/`
- Other articles (link where natural): `/soccer-iq-training/`, `/football-decision-making-training/`, `/get-scouted-without-an-academy/`, `/analyse-a-football-match-as-a-player/`, `/soccer-intelligym-alternative/`, `/vr-soccer-training-alternative/`

## Boards (tactics-board images)
If your page needs worked situations (the decision-making page does; others optional, max 3), write them in the engine format as a JS file `/home/claude/bww-videos/unscouted/seo/pages/<slug>-boards.js` containing `QS2.mid=[ {...}, ... ];` — same format as `/home/claude/bww-videos/unscouted/web/more_mid.js` (read it and `/home/claude/bww-videos/unscouted/web/SCENARIO_BRIEF.md` for the coordinate system and accuracy rules). Options stay in the order you write them (A, B, C). Then render:
`cd /home/claude/bww-videos/unscouted/web/tools && python3 render_boards.py ../../seo/pages/<slug>-boards.js /home/claude/bww-videos/unscouted/seo/pages/img/<slug> --reveal`
It writes `<slug>-1.png` (question) and `<slug>-1-answer.png` (pro arrow shown, letter = A/B/C in your order). LOOK at every PNG with the Read tool and fix until accurate. In the HTML reference them as `IMG/<slug>-1.png` (I replace IMG with the real upload path). Never use `&&` in that JS either.

## HTML structure (write to `/home/claude/bww-videos/unscouted/seo/pages/<slug>.html`) — a fragment, no <html>/<head>/<body>, no <style>; classes come from the site's stylesheet:
```html
<div class="us-art">
<header class="us-art-hero"><div class="in">
  <p class="us-art-kick">GUIDE · DECISION MAKING</p>
  <h1>…exact H1 from plan…</h1>
  <p class="lead">1–2 sentence promise of what this page gives the reader.</p>
  <a class="us-btn" href="/soccer-iq-test/">Take the free test →</a>
  <p class="us-art-meta">By Unscouted · Updated October 2026 · 8 min read</p>
</div></header>
<div class="us-art-body">
  <div class="us-quick"><p><strong>Quick answer:</strong> …2–4 sentences that directly answer the search…</p></div>
  <nav class="us-toc"><p>ON THIS PAGE</p><ol><li><a href="#s1">…</a></li>…</ol></nav>
  <h2 id="s1">…</h2> <p>…</p>
  <!-- optional elements: -->
  <div class="us-note"><p>…tip / honest caveat…</p></div>
  <figure class="us-board"><img src="IMG/<slug>-1.png" alt="descriptive alt text" width="1066" height="520" loading="lazy"><figcaption>…what to look at…</figcaption></figure>
  <ul class="us-opts"><li><b>A</b> …</li><li class="pro"><b>B</b> … (pro pick)</li><li><b>C</b> …</li></ul>
  <div class="us-tablewrap"><table class="us-table"><thead><tr><th>…</th></tr></thead><tbody><tr><td>…</td></tr></tbody></table></div>
  <!-- mid-page CTA once, end CTA once: -->
  <div class="us-cta"><h2>…</h2><p>…</p><div class="row"><a class="us-btn" href="…">…</a><a class="us-btn ghost" href="…">…</a></div></div>
  <h2 id="faq">FAQ</h2>
  <div class="us-faq"><details><summary>Question?</summary><p>Answer.</p></details>…</div>
  <p class="us-src">Sources: <a href="…" rel="nofollow noopener" target="_blank">…</a> · …</p>
</div>
</div>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"…","acceptedAnswer":{"@type":"Answer","text":"…"}}]}</script>
```
Image width/height: use the real PNG pixel size (check with python PIL).
The CTA links should go to the most relevant product. Keep CTAs honest ("Try 8 situations free", "Get 100 situations, $27").

Also write `/home/claude/bww-videos/unscouted/seo/pages/<slug>.json`: {"slug":"…","title":"…seo title ≤60…","h1":"…","meta":"…≤155…","focus":"main keyword","kicker":"…"}.

Final reply: file paths, word count, the title/meta, sources used, and anything you were unsure about. Short.
