# Page upgrade round (Oct 13): beat the current top 3 on Google

You upgrade EXISTING, already-published Unscouted pages (unscoutedfootball.com, football/soccer self-coaching for players 15–21 not in an academy). Goal: for each page's target keyword, our page must be clearly more useful, complete and quotable than the current top 3 organic results.

Read first: `ARTICLE_SPEC.md` (hard rules, voice, products, URLs), the page's section in `RESEARCH.md`, any `pages/<slug>-serp.md`, `pages/<slug>.json` (current title/meta), and the current page `build/<slug>.html`. The tracker `build/pages-tracker.csv` gives each page's target keyword.

## Steps per page
1. **SERP check.** WebSearch the target keyword (and 1–2 close variants). Pick the top 3 ORGANIC results that are real articles (skip unscoutedfootball.com, Reddit/Quora threads, YouTube, spam/scraped copies, pure shop pages). WebFetch each one fully. Note: title, H1, H2 outline, approx words, what they cover, unique facts/data, tables, FAQs, visuals, freshness.
2. **Gap analysis vs our page.** List concretely: subtopics/questions any of the 3 cover that we don't (or cover thinly); search intents we miss (e.g. "what does X mean", "how many", "best age", "drills"); People-Also-Ask style questions; anything AI answers (Google AI Overviews / ChatGPT) would want that we lack: a crisp 40–60 word definition answer, a comparison table, numbered steps, a stat with a source.
3. **Upgrade with targeted additions** (NOT a rewrite; the page is new and already decent). Typical: 1–3 new sections or table/list additions, sharper answer-first paragraphs under question H2s, 2–4 new FAQ questions, a better title/meta if ours is weaker than what the top results show for this intent. Every addition must add real value for a player training alone. Keep total length sensible (no padding; aim for the most useful page, not the longest).
4. **Write `pages/<slug>.patch.json`** (format below) and run `python3 tools/apply_patch.py <slug>` until it prints OK. Then read the relevant parts of `build/<slug>.v2.html` to check the new HTML sits correctly and reads well.
5. **Write `pages/<slug>-upgrade.md`**: the 3 competitor URLs with a one-line verdict each, the gap list, and what you changed (bullets).

## Patch rules
- `ops` anchors must be EXACT substrings of `build/<slug>.html` that occur exactly once. Use short-ish anchors at clean boundaries, e.g. a whole `<h2 id="s7">…</h2>` line, or a closing `</p>` of a specific paragraph including some of its text. Prefer `insert_before` an existing `<h2 id=...>` to add a new section, and `replace` for improving one specific paragraph or table.
- NEVER anchor on or change: the FAQ JSON-LD (use `faq_add` instead, the script updates both the visible FAQ and the schema), the `<h2 id="faq">` line, CTA boxes (`us-cta`), anything inside `<script>` or any interactive tool markup (free test / scanning test pages: only add article content around the tool, never touch the tool).
- New HTML must use only the classes/patterns already used in that page (look at it: tables, `us-box`, lists, etc.). Give new H2s an id like `s10`, `s11` (unique on the page). No new images. No JavaScript.
- `faq_add`: plain-text answers 25–60 words, answer-first, no HTML.
- `title` (50–60 chars, keyword near the start) and `meta` (140–158 chars) only if you are improving them; otherwise null.
- Hard rules from ARTICLE_SPEC apply: never the owner's name, no invented stories/stats/testimonials/quotes, competitor facts only verified with a cited source, no `&&` anywhere, `&amp;` for a literal ampersand, plain English for a 16-year-old, no AI-tell phrasing, no em dashes.
- Do NOT publish anything, do not use a browser, do not git commit. Only write the files above.

## Final reply (keep it short)
For each page: the 3 competitors (domain + why they rank), the top 3 gaps you closed, words before→after, and the apply_patch OK line.
