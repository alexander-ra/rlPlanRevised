# Step 04 — fixes applied
Applied: 58 · Skipped: 1 · Central: 4

Counted per finding of `step04_review.md` (61 = G 5 · B 27 · T 9 · C 11 · S 6 · X 3).
Applied = G01–G05, B01–B27 (B17 in part, see below), the T occurrences of T01–T04 and
T07–T09 (T05 needed no text change), C01–C11 (C01 as the R3 caveat), S01–S06 (S06 in
part), X02, X03. 281 exact replacements, all quotes matched; applied with a script, then
proofread in the built PDF.

Beyond the review, the ✅ rows of `GLOSSARY_DECISIONS.md` found in these files were applied:
1.7 (Нашево/Нашово/Неш → равновесие на Наш), 2.1 (политики → стратегии), 2.15 (wall-clock
"реално време"/"време на часовника" → време за изпълнение), 2.16 (изчислителна мощност →
изчислителни разходи/време), 2.23 (модели на последователности), 2.28 (мрежа → решетка for
the bet grid), 2.31 (персонализирана → собствена), 2.33, 2.34, 2.38 (семена → начални числа),
2.40 (кошчета/припомняне → клъстери/памет), 0.4/2.6 (не се е сходил → клони към),
1.15 (в очакване → средно), 3.1 (fold/raise → отказ/вдигане; "пас/залог/повишаване" →
"отказ/плащане/вдигане"), 3.4 (кръг → рунд for betting rounds), 3.11 (хедс-ъп …, покер без
лимит → безлимитен … за двама играчи), and "Ледюк с фиксиран лимит" → "Ледюк с лимит",
"Extended Ледюк" → "разширен Ледюк" throughout, incl. `report_bg.md`.

Where applying the intent differed from the review's literal text:
- B21: review wrote "пас/плащане/повишаване"; glossary 3.1 gives "отказ/плащане/вдигане" — used the glossary.
- B27: review wrote "за същото реално време"; glossary 2.15 gives "време за изпълнение" — used the glossary.
- S01: "(по аналогия с метода на информационното стеснение)" right after "…информационното стеснение" repeats itself → "(по аналогия с едноименния метод[^tishby1999])".
- C02: "фиг. 13" is the bundle number and wrong in the standalone PDF → "вж. фигурата за Ледюк с лимит в „Практическо валидиране“" (EN likewise).
- C03: "CFR се сходи към него" → "CFR клони към него" (glossary 0.4).
- C10: the review's "0.46–0.70" are gaps from the 200-iteration smoke test; with the Pareto figure now on the CFR+ benchmark, the text quotes the CFR+ exploitability of the same k = 3/k = 5 abstractions, 0.38–0.57 (EN and BG).
- S01/C06 new notes: reused the corpus-wide keys instead of new ones — `[^deepcfr]` (step 05) for brown2019deep, `[^deepstack]` and `[^pluribus]` (step 06) for moravcik2017 and brown2019, with identical bodies, so the bundle's de-duplication keeps one note per work. New keys: tishby1999, rubner2000, waugh2009, ganzfried2013, ganzfried2014; bowling2015 copied from step 03 (body already glossary-clean).
- Footnote markers placed after the full stop, as everywhere else in this chapter.
- Report (not in the review): duplicated heading "## 1. Какво беше разработено" in `report_bg.md` → "**Структура на изходния код:**" (EN has "Source layout"); "CFR toolkit" → "набора от инструменти за CFR"; BG table rows/config names translated to the figure labels; pseudo-harmonic row corrected as in S02 (EN and BG); reproduction block gains `python day05_plots.py`.

R3 (F04-C01, caveat): caveat text applied to summary § 4.12 (EN/BG), the one-pagers
(headline qualified "as deployed here", "translation error dominates" → mapping error under
the current deployment rule, limitations bullet names the rule and the identical translator
results, open question adds "survives a corrected action mapping"), report § 3.2, and the
related § 3.3, § 4 table and § 6 item 3 so no document states "translation error dominates"
as a finding. Figures mark the action-abstraction runs with hollow markers and say why in the
caption. Harness not touched, nothing rerun.

## Skipped (id — reason)
- T06 / B17 blueprint items — glossary row 1.10 is open: "(blueprint)" first-mention gloss, "план-стойности" (2×), "план-печалби" (2×) and "Мостът към глава 6 е архитектурният план." left for the 1.10 pass. B17's non-blueprint parts applied (Reach, "Така строгата гаранция отпада", "под-игра-скеле", "резюме" → "главата").

## Central (id — what is needed)
- F04-X01 — per-chapter footnote labels: `brown2017` marker still points into chapter 3 in the bundle.
- F04-T01–T09 — the settled/curated glossary entries themselves (T05: curated "Изоморфизъм на цветовете" → "Изоморфизъм на боите").
- Shared footnote bodies — S06 metadata for `brown2017` (and `libratus`) not changed: shared with steps 03/06. `bowling2015` bodies currently differ between steps 02 and 03 (other agents are editing them); the bundle keeps one.
- `labels_step04.json` changes existing shared keys: 'Final exploitability (log scale)' → 'Крайна експлоатируемост' (shortened: the full form was clipped on the axis; "log scale" is in the caption), 'Final exploitability after 180s (log scale)', 'CFR+ abstraction comparison: 3 seeds x 3 minutes each', 'Mean +/- SD exploitability', 'Exploitability (full game)' / '(own game)', 'info-set count', 'exploitability gap Δ_abs (full game)', 'Hand strength (P(win) + 0.5·P(tie))  — jittered' (decimal comma, "с разсейване"), and 'Action abstraction' (runtime-observed key, lower-case in the shared file; capitalised here). Also adds global keys 'Jack'/'Queen'/'King', 'Full game', '0.17'/'0.50'/'0.83'.
- Not editable here: `implementation/step04/EXPERIMENT_RESULTS.md` l. 76 still reads "the restricted action set and deployment translator dominate" — needs the same caveat.
- `render_bg_figures.py`: `Axes.legend` wrapper translates arg 1 (the handles), not the labels, so `legend(handles, labels)` stays English — worked around in `day05_plots.py` with labelled proxy lines.

## Numbers changed (old → new, where)
- § 4.1 (EN/BG): "~10¹⁷ hand-vs-board situations" → "≈ 2.8 × 10⁹ hole/board combinations; 3.16 × 10¹⁷ HULHE states" (+bowling2015).
- § 4.6.3: "~10⁹ canonical river boards" → "≈ 2.4 × 10⁹ canonical private/public combinations on the last round".
- § 4.10.3: "10–100× lower than every prior translator on HUNL" → "≈ 10× lower than pseudo-harmonic translation, 119–150 vs 1465 mbb/g, no-limit flop hold'em".
- § 4.7.2: added "EMD proxy 0 for k = 3/5, exploitability 0.38–0.57"; § 4.9.2: added "108 vs 132 info sets, 0.574 vs 0.571".
- Pareto figure: smoke-test values (e.g. k2 perfect gap 0.958) → 180-s CFR+ means (k2 perfect 0.571), matching text and panels.
- One-pager and report tables: no numbers changed.

## Figures (file — what changed — printed size now)
All print at 17.6 cm, 342 ppi, scale 0.877 → fs 10 = 8.8 pt, fs 11 = 9.6 pt.
- `summary/leduc_hsd{,_bg}.png` — NEW (G02, preferred option): replaces the k-means scatter in § 4.9.2. Pre-flop HSDs of J/Q/K and the 3×3 post-flop strengths coloured by the k-means-EMD bucket, computed by `phase4/day02_hand_strength.py` / `day02_card_bucketing.py` (no training; asserts k = 3 and k = 5 give the same partition). Script `deliverables/reports/step04/summary/make_leduc_hsd.py`. 17.6 × 7.8 cm.
- `day07_cfrplus_fixed_leduc` (G03) — (16,7)/150 dpi → (8,5)/300; title and legend removed; info-set count above each group; translatable tick labels; hollow markers for action abstraction. 17.6 × 10.9 cm (was 4.4 pt, now 8.8 pt).
- `day07_cfrplus_mini_nl_leduc`, `…extended_leduc` (G03) — (12,7) → (8,3.3). 17.6 × 7.1 cm each (was 5.8 pt).
- `day05_pareto` (G04) — `day05_plots.py` rewritten to read `.day07_cfrplus_results.json`: mean of 3 runs per config vs info sets, one colour per game, step line through each game's non-dominated points, config labels at fs 10, legend below; old smoke-test plot kept behind `--smoke-test` (→ `day05_pareto_smoke.png`, not used). (11,7)/150 → (8,5.8)/300. 17.6 × 12.6 cm (was 4.4 pt).
- X02: Extended panel moved next to the Mini-NL panel (EN and BG); pages 17–20 now full — no half-empty pages.
- `day07_cfrplus_panels.py` `main()` re-saved `.day07_cfrplus_results.{json,csv}` on every run even when nothing was trained; now saves only after a new run. Hashes of both files unchanged before/after all plotting runs.
- BG twins rendered with `--only step04/phase4` and `--only step04/summary` (not `--only step04`): the exploration scripts `day01_cfr_compare/compare/mccfr_compare` and `day02_nl_compare` retrain CFR when run. `day01_infoset_clustering.py` not rerun (its figure left the chapter).
- Report `figures/` and `summary/` now hold the new EN + `_bg` PNGs; `report_bg.md` and `summaryBg.md` point at the `_bg` twins. Now unreferenced, left in place: `summary/day01_infosets_{kmeans,manual}{,_bg}.png`, `figures/day01_infosets_kmeans{,_bg}.png`.

## Remaining overflow / legibility warnings
- Renderer: no overflow warnings. Crops (`renders_fix/step04/ch04/`) read clean; figure text ≈ 80 % of caption size.
- Mini-NL/Extended BG y-label "Крайна експлоатируемост" fills the axis height exactly (fits, no clipping).

## Verification (build ok? check_headings / check_captions output for this step)
- `build_reports.py --step step04 --type all`: all six PDFs built. BG one-pager fits one page (9pt/1.3cm), EN one page (10pt/1.5cm). Summary BG 21 pp, EN 17 pp.
- `check_headings.py`: 44 PDFs, 0 missing headings. `check_captions.py`: 24 PDFs, 0 with unaccounted figures.
- Cyrillic inside `\text{}` (formula § 4.2) renders correctly; no U+FFFD in the BG PDFs; ↔ ∈ × Δ „“ ѝ present.
