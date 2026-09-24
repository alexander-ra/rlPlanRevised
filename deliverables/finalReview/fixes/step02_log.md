# Step 02 — fixes applied
Applied: 39 · Skipped: 0 · Central: 4 (+ 6 central sub-items below)

Applied = G01–G04, B01–B13, C01–C14, S01–S06, X01, X02 (the T01–T04 *occurrences* in the
step-02 files are covered by B01/B02/B04/B07/C05/C11/S03). R6 (fix) done: seeded rerun,
curve data saved, plot-only mode, EN + BG figures regenerated, numbers updated.

Quotes applied by exact replacement (every one matched once), except where noted:
- **G01 captions adapted to the rerun.** Fig. 3: "се приближава към" → "се колебае около …
  в рамките на шума от извадката" + the exact value −0.0555 (the seeded running mean ends at
  −0.0613, below −1/18, so "approaches" no longer describes the curve). Fig. 4: adds "средно
  за пет начални числа; оцветената ивица показва обхвата". Fig. 5: α ≈ 0.19 → 0.18,
  "съответстват на" → "са близки до", "с вале/дама" → "с Вале/Дама" (chapter's capitals),
  "100 000" → "100,000" (surrounding style; typography is central). EN mirrored.
- **X02 figure references** written descriptively ("първата / втората / последната фигура в
  раздела „Емпирични визуализации“"), not "фиг. N": the standalone summary numbers them 1–3,
  the bundle 3–5 (see Central).
- **B09 "предсказвач за най-добър отговор"** → "оракул за най-добър отговор" (glossary 1.18
  overrides the review's wording).
- **C09 / C10 / G02 numbers** replaced with the seeded-rerun values (table below), not the
  review's −0.489 / 0.002–0.011 / 0.011.
- **One-pager bullet 1 claim rewritten** (EN + BG): "CFR lands *inside* the family, not merely
  near it … holds to 2.6e-4" → "lands *close to* the family … holds to within 0.038; even so
  the profile's exploitability is only 0.006". The seed-0 run does not support the old claim.
- Extra, same intent: report_bg "сходи" → "се доближава" (glossary 0.4), "информационни
  набори" → "информационните множества", "вероятностна извадка" → "извадка на случайните
  събития" (B07); report_en/bg header and § 1 "Vanilla CFR" → CFR with chance sampling (C05/T02).
- Fig. 3 caption no longer says the curve *converges*; C06's quantity split (running mean vs
  exact value of the average strategy) is now in the one-pager, reports and caption.

## Skipped (id — reason)
- none. (X01's optional build guard is a `scripts/**` change → Central.)

## Central (id — what is needed)
- F02-T01 — glossary_settled: two-player → "за двама играчи"; n-/N-player → "с N играчи";
  delete "N-игрова среда", "N-играторска граница"; fix the Latin "e" in "n-играчeн".
- F02-T02 — glossary_settled: single-agent RL, TD error ("TD грешка"), PPAD-complete
  ("PPAD-пълен"), vanilla CFR long form, n-player EGTA framework.
- F02-T03 — glossary_settled: fold → "отказ / се отказва" (call → "плащане", GLOSSARY 3.1).
- F02-T04 — curated terminology_EN_BG.md: "контрафактуален" → "контрафактичен" (GLOSSARY 1.11).
- F02-B07 / B10 — settled entries "chance sampling → вероятностна извадка" and "half-street
  models → модели на наполовина улица" need replacing (text already fixed here).
- F02-G03 labels — `labels_step02.json` redefines two keys shared with step03:
  'CFR Iterations' → 'Итерации на CFR', 'Exploitability' → 'Експлоатируемост' (capitalised);
  also 'Training Iterations' → 'Итерации на обучението' and a new BG for
  '$O(1/\sqrt{T})$ reference' ('еталонен наклон …'). Merge into figure_labels.json.
- F02-X02 — stable "фиг. 2.1–2.3" needs `\counterwithin{figure}{section}` in the build header.
- F02-X01 — optional build guard (list after a non-blank line) in `scripts/`.
- F07-X01 / GLOSSARY 5.3 — shared footnote labels (shoham2008; new lanctot2009 may also exist
  in step03). GLOSSARY 0.5 — extra bold in BG (83 vs 49 spans) left for the mechanical pass.
- GLOSSARY 5.1–5.2 typography (dashes, decimal comma, "100,000") left for the central pass.

## Numbers changed (old → new, where)
Rerun: `cfr/train.py` seed 0 (100,000 iterations, 1.2 s) and `evaluate/convergence.py` seeds
0–4 × checkpoints 100…100,000 (3.2 s). Old values from the unseeded run in git HEAD's
`models/cfr_results.json`; "exact value" and exploitability computed with the new
`evaluate/exploitability.py:average_strategy_value` / `compute_exploitability`.

| Quantity | Old | New | Where |
|---|---|---|---|
| α = P(bet \| J, root) | 0.1941 | 0.1792 | onePager EN/BG; fig. 5 caption (α ≈ 0.19 → 0.18) EN/BG |
| P(bet \| K, root) vs 3α | 0.58247 vs 0.58221 (2.6e-4) | 0.5758 vs 0.5377 (0.038) | onePager EN/BG |
| King bets / calls (3p, 3b, 3pb) | ≥ 0.9999 | ≥ 0.9999 (0.999985 / 0.999985 / 0.999982) | onePager (unchanged) |
| Jack folds to a bet (min of 1b, 1pb) | 0.99998 | 0.99996 | onePager EN/BG |
| Queen passes at the root | 0.99993 | 0.9995 | onePager EN/BG |
| Mixed frequencies off closed form | 0.002–0.011 | 0.005–0.038 (1p 0.005, 2b 0.012, 2pb 0.018, K-vs-3α 0.038) | onePager EN/BG; report_en/bg status |
| Jack bluff after pass (1p) | 0.3403 | 0.3387 | onePager EN/BG |
| Queen call after pass–bet (2pb) vs 1/3 + α | 0.5387 vs 0.5274 | 0.5307 vs 0.5126 | onePager EN/BG |
| Player 1 Queen call vs bet (2b) | 0.3353 | 0.3454 | fig. 5 only (0.34 → 0.35) |
| Running mean of sampled payoffs | −0.0602 | −0.0613 | onePager EN/BG; report_en/bg; fig. 3 |
| Exact value of the average strategy | −0.05549 (reviewer) | −0.05548 → printed −0.0555 | onePager, reports, fig. 3 caption (new) |
| Exploitability BR0+BR1 of the 100k average strategy | 0.0043 (reviewer) | 0.0060 | onePager EN/BG; report_en/bg (new) |
| Log-log slope | −0.489 (6 unseeded single runs, 100–50k) | −0.52 ± 0.02 (5 seeds, 7 checkpoints 100–100k; per seed −0.553, −0.539, −0.511, −0.505, −0.501; slope of mean −0.520) | summary EN/BG § 2.9; onePager EN/BG; report_en/bg |
| Last exploitability checkpoint | 50,000 | 100,000 | fig. 4 |
| Report status | "All targets achieved ✓" | game-value + rate met; mixed 0.005–0.038; 4-decimal only for the King's and Jack's pure decisions (Queen's are 5e-4 / 1.7e-4 off) | report_en/bg |

Note: the seed-0 curve in `convergence.json` ends at 0.0035, not 0.0060: `KuhnTrainer.train`
restarts its card list on every call, so the incremental run deals a different sequence than
`train.py`'s single call (same process, different numbers; documented in `convergence.py`).
The old "inside the family to 2.6e-4" was one unseeded run; other seeds were not examined.

Implementation (R6): `config.py` (checkpoints `[100, 300, 1k, 3k, 10k, 30k, 100k]`, `seed`,
`convergence_seeds`); `cfr/train.py` (`--seed`, default 0; saves `iteration_history`,
`game_value_history`, `avg_strategy_value`, `exploitability`); `evaluate/convergence.py`
(5 seeds, one incremental trainer each, saves `models/convergence.json`);
`evaluate/exploitability.py` (`average_strategy_value`, checked: −1/18 and 0 exploitability
on the analytic α = 0.2 profile; 1/3 + α at "2b" gives 0.033, confirming F02-C01);
`utils/plotting.py` (plot-only `__main__` reading both JSONs; writes summary/ and figures/).
No change to `cfr_trainer.py`, `info_set_node.py`, `kuhn_poker.py`, `best_response.py`.

## Figures (file — what changed — printed size now)
Printed at 17.6 cm (render_printed manifest); EN and `_bg` twins in `summary/` and `figures/`.
- game_value_convergence(_bg).png — 8×4 in @300 dpi (was 10×5 @150); title dropped; legend
  lower right, off the curve; "Running mean of sampled payoffs"; y "Payoff to Player 0
  (running mean)"; 200 points from saved JSON. Scale 0.96 → all text 9.6 pt; 313 ppi.
- exploitability_convergence(_bg).png — 8×4.6 @300 (was 10×6 @150); title dropped; mean of 5
  seeds + min–max band; checkpoints to 100k; O(1/√T) line fitted to all points (was anchored
  to the first). Scale 0.99 → 9.9 pt; 304 ppi.
- strategy_analysis(_bg).png — 8×6.6 @300 (was 14×12 @150); suptitle dropped; Player 0/1;
  J/Q/K; compact two-column legends (BG "Плащане (залог)" had overhung the panel); bar values
  use the locale decimal comma in BG. Scale 0.885 → values/legend 8.5 pt, axes/ticks 8.9 pt,
  titles 9.3 pt (was 4.8–6.5 pt); 339 ppi.
- summaryBg.md → `*_bg.png`; report_bg.md → `figures/*_bg.png`.

## Remaining overflow / legibility warnings
- Renderer: none (no diagram boxes in this step). All printed text ≥ 8.5 pt.
- Layout: in the standalone BG summary the heading "Емпирични визуализации" and its one intro
  line sit at the foot of p. 9, the three figures on pp. 10–12 (float placement). Recheck
  after the central typography pass changes the text length.

## Verification (build ok? check_headings / check_captions output for this step)
- `build_reports.py --step step02 --type all`: all 6 PDFs built. BG one-pager fits on one
  page at 9pt / 0.90 / 1.3cm (rung 5 of 7); EN at 10pt / 1.8cm.
- Cyrillic `\text{ако}` / `\text{в противен случай}` render; the а)–е) sub-list and the
  "Ключови свойства" list print as lists; new footnotes print.
- `check_headings.py`: no missing heading in step 02 (44 PDFs, 5 missing — all in
  step03_bg, not this step).
- `check_captions.py`: 24 PDFs checked, 0 with unaccounted figures.
- Crops: `deliverables/finalReview/renders_fix/step02/ch02/p010–p012_f1.png`, read and checked.
