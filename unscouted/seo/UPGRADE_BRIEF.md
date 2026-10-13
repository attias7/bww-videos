# Competitor-beating upgrade brief (one page at a time)

Goal: for each assigned page, make our page clearly better than the top 3 pages currently ranking for its main keyword — for Google AND AI answers (ChatGPT, Perplexity, Google AI Overviews).

Files: /home/claude/bww-videos/unscouted/seo/pages/<slug>.html (+ <slug>.json). Rules: ARTICLE_SPEC.md (incl. "LLM / AI-search rules" and Boards section) in the same folder — follow it. Never write `&&`. No owner name. No invented stats, quotes, testimonials, results, personal stories. Facts about competitors/leagues/products only if verified (cite). Keep every product link and CTA that already exists (prices: Basics Kit $47, packs $17, Game Library $27, Pause & Decide $27, Bundle $99, free test /soccer-iq-test/, scanning test /football-scanning-test/).

## Step 1 — Find the 3 competitors
- Main keyword = the "focus" in <slug>.json. Run WebSearch for it (and 1 close variant). Pick the top 3 ORGANIC pages that target the same intent (skip our own site, skip pure video/forum/social results, skip shop listings unless the SERP is all shops). Note: WebSearch approximates Google — say so in the teardown.
- WebFetch each of the 3. If one can't be fetched, take the next result.

## Step 2 — Teardown (save to pages/<slug>-serp.md; append a new dated section "## Upgrade teardown 2026-10-13" if the file exists)
For each competitor: URL, title, H1, approx word count, H2 outline, what it covers (subtopics, questions answered), media/tables/tools, schema if visible, freshness/date, E-E-A-T signals, and its weaknesses.
Then: our current page the same way. Then a GAP TABLE: subtopic/question/element | comp1 | comp2 | comp3 | ours (before) | ours (after).

## Step 3 — Upgrade our page
- Cover EVERY subtopic/question that 2+ competitors cover (if relevant to a player 15–21), plus the unique things only we can do (worked tactics-board situations, solo training plan, decision rules, free tools).
- Title (≤60 chars, keyword at the start where natural) and meta (≤155, includes keyword + a reason to click) in the .json — must beat competitors' titles for click-through. H1 includes the keyword.
- Quick answer box first (2–4 sentences, names Unscouted once), Key takeaways, question-style H2s each opening with a 40–60 word standalone answer, tables for comparisons/steps, FAQ 6–8 real questions (People-Also-Ask style variants of the keyword) with FAQPage JSON-LD matching the visible FAQ exactly, Article JSON-LD (datePublished keep original if present, dateModified "2026-10-13"; author/publisher Organization "Unscouted" url https://unscoutedfootball.com). Add HowTo JSON-LD only for real step-by-step sections.
- Depth: aim to be the most complete AND the easiest to scan. Length should end up at or above the longest competitor's useful content, but no padding (typically 1,800–3,000 words).
- Internal links: 4–8 contextual links to relevant pages from this list (only these exist): /soccer-iq-test/, /football-scanning-test/, /soccer-iq-training/, /football-decision-making-training/, /get-scouted-without-an-academy/, /analyse-a-football-match-as-a-player/, /soccer-intelligym-alternative/, /vr-soccer-training-alternative/, /soccer-intelligym-vs-be-your-best/, /train-effective-alternative/, /best-soccer-iq-apps/, /how-to-become-a-professional-soccer-player/, /pro-soccer-tryouts/, /best-online-soccer-training-programs/, /soccer-iq-book/, /soccer-training-plan/, /how-to-scan-in-soccer/, /soccer-striker/, /winger-soccer/, /number-10-soccer/, /center-back-soccer/, /shop/.
- Images: every <img> needs descriptive alt text with the topic; width/height set. New boards are welcome where a worked situation helps (render + LOOK at them per spec).
- Keep the existing HTML class system (us-art etc.). Keep any existing boards (IMG/... references) working.
- Update "Updated October 2026" meta line and add "Checked October 2026" next to anything time-sensitive.

## Step 4 — Self-check before finishing
- JSON-LD parses; FAQ text matches; no `&&`; all internal links are from the list; title/meta lengths OK; word count; no claims you didn't verify.

Final reply per page (short): slug; the 3 competitor URLs; 3 bullets on why ours now beats them; new title/meta; word count before→after; anything uncertain.
