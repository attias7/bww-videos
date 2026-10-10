# Brief: write 12 new "Pause & Decide" situations for one position

Product: Unscouted, a football self-coaching brand for players 15–21 outside the academy system. These situations go into a paid interactive quiz ("Pause & Decide: 100 Situations"). Each situation is a tactics-board picture plus 3 options; the player picks one, then sees the pro pick and why.

## Read first
- `/home/claude/bww-videos/unscouted/web/scenarios.js` — the existing 40 situations (8 per position) and the exact data format. Match it precisely. Do NOT duplicate or lightly reword any of the existing 8 situations for your position; yours must be new situations.
- Coordinate system (metres, real pitch): x 0 = left touchline … 68 = right touchline. y 0 = goal line at the TOP of the board. Halfway line at y = 52.5. Penalty box: x 13.84–54.16, y 0–16.5. Six-yard box: x 24.84–43.16, y 0–5.5. Penalty spot (34, 11). Goal x 30.34–37.66. Attacking questions: top = THEIR goal (their GK near (34,2)). Defending questions: add `g:'your goal'` and top = YOUR goal (your GK near (34,2)); attackers move UP the board towards it.
- Each player entry: `[kind, side, x, y, label]` — kind is `'me' | 'us' | 'them' | 'gk'`; side is `0` except for gk where it is `'them'` or `'us'`; label is a short role (`'CB','FB','CM','DM','10','W','ST','GK'`, or `'FREE'`) — the `me` label is always `''`.
- `ball:[x,y]` (place the ball 1–1.5 m from whoever has it) and/or `pass:[x1,y1,x2,y2]` (white dashed arrow of a pass already on its way; the ball is drawn at its start), `run:[x1,y1,x2,y2]` (lime dashed arrow: a teammate's run already happening). Each option: `[text, points, [x1,y1,x2,y2 arrow], explanation]`. `pro` = index (0,1,2) of the best option. The view auto-crops to the players, so you don't set a view.

## Rules (these matter most)
1. **Realistic and accurate.** Positions must make football sense at real scale: back lines roughly level, sensible distances (players 5–15 m apart, not stacked), offside lines respected, keepers where keepers stand. Show 6–10 players: everyone relevant to the decision plus the nearest others. Think like a UEFA-licensed coach drawing on a tactics board.
2. **Hard, not obvious.** All 3 options must be real choices a decent player might make. No joke/silly options (no "complain to the ref", "stop and watch"). The best option must depend on a DETAIL VISIBLE IN THE PICTURE (where a defender stands, an open lane, a free man, how deep their line is, the keeper's position, the score/minute chip). The question text gives only the facts you'd know without looking (role is separate; give the situation in ≤ 2 short sentences) — NEVER put the answer's cue in the text (no "you're faster", "nobody behind you", "he isn't closing you"). Mix up whether the bold/attacking or the safe option is correct — roughly half the time the patient/safe option should be right. Vary `pro` across 0/1/2 evenly.
3. **Points:** the pro option = 2, the second-best = 1, the weakest = 0 (scoring only rewards the pro pick, but keep this pattern).
4. **Explanations:** 1–3 short sentences, plain English a 16-year-old reads easily, direct "you" voice. The pro explanation must point at the visual cue ("Look where their full-back is…"). Wrong-option explanations say honestly why it's worse here (it's fine to say when it WOULD be right). No invented statistics. No promises.
5. **"From my notes":** only for striker / winger / ten — and only if the lesson genuinely appears in the notes library listed for you (quote the idea, don't invent). Max 3 situations in your set may use it. Otherwise speak as a coach.
6. **Variety across your 12:** cover different phases (build-up, between the lines, final third, transition, set piece, game state/score & clock, defending/recovery for attackers too), different areas of the pitch, both sides, different scores/minutes. Each needs a `cat` key; reuse existing keys from `CATS` in scenarios.js where they fit, or add new ones and list them (with a short label) at the top of your file in a comment like `// NEW CATS: key:'Label'`.
7. JavaScript constraints: the file is pasted into a WordPress page, so **never use `&&`** anywhere. Escape apostrophes inside single-quoted strings with `\'`. No template literals.

## Output
Write the file `/home/claude/bww-videos/unscouted/web/more_<POS>.js` containing exactly:
```js
QS2.<POS>=[ {...}, {...}, ... 12 items ... ];
```
Then CHECK your work visually — this step is required:
```
cd /home/claude/bww-videos/unscouted/web/tools && python3 render_set.py ../more_<POS>.js <POS> /tmp/claude-0/sc/check_<POS>.png
```
Open the PNG with the Read tool and look at every board: arrows point where the option says, nobody overlaps badly, distances look real, the visual cue for the pro pick is clearly visible. Fix and re-render until all 12 look right (option A's arrow and the pro arrow are drawn). Also run `grep -c '&&' ../more_<POS>.js` → must print 0.

Final reply to me: the file path, the 12 situations in one line each (role · minute/score · situation · pro option letter-index), any new cat keys, and anything you're unsure about. Keep it short.
