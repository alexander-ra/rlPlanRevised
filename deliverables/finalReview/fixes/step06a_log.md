# Step 06a — fixes applied (Introduction, DeepStack, Libratus, Pluribus; one-pager)

Applied: 101 · Skipped: 1 · Central: 18
(G 5 · B 62 · C 12 · S 18 · X 4 applied; B63 skipped; T01–T18 central — their occurrences in this half are applied through the B items)

Files: `summaryEn.md` / `summaryBg.md` (up to "## ReBeL (2020)", plus the shared footnote block at the end), `onePager.md`, `onePagerBg.md`, `make_{deepstack,libratus,pluribus}_figure.py`, `_diagram_utils.py`, the six `*_arch[_bg].png`, `fixes/labels_step06.json`. Scripts used: scratchpad `s06a/apply_text.py`, `apply_onepager.py` (exact-match replacement with count checks; every pattern matched).

**For the 06b agent (same files, after me):**
- Footnote definitions already added to the shared block (both languages): `brown2018dls`, `brown2020rebel`, `cicero2022` (06b's labels and metadata), plus `ganzfried2016reflections`, `libratusijcai`, `nunez2024`, `pluribussm`, `sandholm2021`. Do not define them again. `brown2017`, `burch2014`, `lbr` got the S18 metadata.
- `_diagram_utils.py`: `note()` default fs 7.6 → 10 (F06a-G05); `panel_bg(..., label_ha="left")` added (default unchanged).
- `render_bg_figures.py --only step06` also re-renders figs. 24–26: always pass `--labels-overlay deliverables/finalReview/fixes/labels_step06.json`, or they revert to the stale central mapping. Add your keys to that file; don't remove mine.
- Chapter-wide consistency I could not reach from this half: "Невронна компонента" row label kept in all tables; "Затворената празнина" / "The gap it closed" heading in ReBeL/SoG → "Пропускът, който запълни" (X02); the row "Също и пълна информация?" → "Също и с пълна информация?", "Изчислителна мощност" headings in ReBeL/SoG (X02/B39); `|--|------|` separators (X03); 10 × "deepStack" remain in ReBeL/SoG/Synthesis.

## Deviations from the review's exact proposals (intent kept)
- **Glossary rows win over the review where they differ:** fold → "отказ" not "пас" (3.1/3.2; B48, C09, figures); opponent-blind(ness) → „сляп“/„слепота“ за противника (1.17), not "независимост от противника" (B61) — also applied to "**независима от противника**" in the intro and one-pager; mbb/g gloss → "хилядни от големия блайнд на раздаване" (3.10; B40, DeepStack/Pluribus openings).
- Blueprint (row 1.10) untouched: figure labels keep "План-стратегия" (G03/G04 proposed "План"); "таблична схема" (T13) left as is.
- B02: table row label kept "Невронна компонента" in all three tables (the ReBeL/SoG tables use it too); only the English cell was translated.
- B31/3.6 applied beyond the listed quotes wherever hand = cards held/deal played was mixed (Libratus key-innovation paragraph, "възможно само в няколко хиляди раздавания", "Така всяко раздаване се играе поотделно").
- C05: the EN/BG strengths sentence on Pluribus (not in the proposal) rewritten to the same intent: the identity remark now says it rules out collusion between copies.
- S15: label `ganzfried2016reflections`, because `ganzfried2016` is step 07's label for a different paper (Ganzfried & Sun).
- S05/S14: `brown2020rebel` (06b's label) instead of `rebel2020`; the Libratus-legacy and Pluribus-legacy test-time-compute claims rephrased to match the source ("20 seconds of search ≈ 100,000× scaling") and cited `[^nunez2024]`; "(voiced by Noam Brown)" deleted.
- S08: kept the operational sentence and cited `[^sandholm2021]`; course title/lecture verified on the CMU 15-888 F21 page (WebFetch).
- X01: "(Фигура 6.N)" → "(вж. фигурата по-долу)", EN "(see the figure below)".
- X03 applied to the EN tables too.
- Adjacent fixes: "и малкия, но преносим трик" → "малкият" (nominative next to the rewritten B57 item); "евтин план, решаващ в реално време" → "модул за решаване в реално време" (adjective without noun, as B54); "решаващите програми" → "програми за решаване" (as B44); "оскъдни залози" → "разреден набор от залози" (DeepStack table, 2.19-type error); "три пристрастни копия" → "изместени" (2.9); "Ледюк" → "Ледюк Холдем" (3.14).
- New BG numbers written like the surrounding text ("20,000", "100,000") so the central typography pass converts them together.

## Skipped (id — reason)
- F06a-B63 (S3, optional) — chapter title "…от край до край" → "Цялостни архитектури…": steps 03, 04 (BG) and the BG study plan refer to chapter 6 by the old title; changing it here alone desyncs those cross-references. Candidate's call; do it corpus-wide or not at all.

## Central (id — what is needed)
- F06a-T01…T18 — glossary entries (`llmPipeline/glossary_settled.md`, `terminology_EN_BG.md`): turn/river, hand clusters, player-count adjectives, opponent-blindness, win rate, continuation strategy, leaf value, sound, offline/online, inference/test-time, decision points/endgame/lookup table, counterfactual, (blueprint = row 1.10, open), value-network entries, self-improver, HUNL family, LBR probe/no-regret/frontier, public belief state.
- `figure_labels.json` — merge `fixes/labels_step06.json` (all keys of figs. 24–26 changed with the relayout; old keys for these three scripts are now unused).
- GLOSSARY 0.5 extra bold spans; § 5.1–5.2 dashes, decimal points, "120,000"-style separators (≈ 209 + 17 in this half) — left for the central pass.
- § 5.3 shared footnote labels: `brown2017`, `burch2014`, `libratus` also exist in steps 03/04; after S18 the ch. 6 note text for `brown2017`/`burch2014` differs from theirs.
- Page layout: figs. 25–26 now print ≈ 20 cm tall (the price of ≥ 8.2 pt Bulgarian text in 3–4 dense boxes per row); the candidate may prefer to trim figure text.

## Numbers changed (old → new, where)
- Pluribus professionals: "rotating cast of thirteen elite pros" → "fifteen (13 in 5H+1AI, Ferguson and Elias in 1H+5AI)"; "tens of thousands of hands" → "20,000 hands"; "thirteen strong humans" → "fifteen" (EN/BG: opening, Strengths ×2) — C02.
- Libratus compute (Pluribus § Compute): "~15 million core-hours to build its blueprint, ~100-CPU cluster" → "~25 million core-hours in total (~6 million for the blueprint), 100 CPUs to play" — C04.
- Baby Tartanian8: "raw blueprint lost by 8 mbb/g … won by 63" → "did not beat it (−8 ± 15 mbb/g, 95% CI) … 63 ± 28 mbb/g" (summary EN/BG; one-pager "**did not beat** (−8 ± 15 mbb/g)") — C06/S07.
- Modicum single-continuation ablation: "lost to both bots (10 and 1)… won (6 and 11)" → "−10 ± 8 vs Baby Tartanian8, −1 ± 15 vs Slumbot; +6 ± 5 and +11 ± 9" — C07.
- DeepStack re-solve size: "10¹⁶⁰ → about 10⁷" → "at most 10¹⁷ from the depth limit, about 10⁷ with the sparse action set" — C10.
- One-pager: "over 1,100 Elo below Go specialists" → "2 of 400 Go games against AlphaZero" (C01); "several times the win rate" → "four times what folding every hand would lose" (C09).
- "Chapters 7–15" → "7–12" (intro ×2, EN/BG) — C08.
- Noam Brown claim → "20 s of search per hand ≈ scaling the model 100,000-fold" (Libratus and Pluribus legacy) — S14.
- Deleted: Loeliger "later rematch" sentence (C03); one-pager "drafted but not yet signed off" (C12).

## Figures (file — what changed — printed size now)
All three: text fs 10, panel titles fs 11, `shrink` 2.0, 330 dpi; boxes sized from measured Bulgarian extents (renderer margin 0.9) so no label is re-wrapped or shrunk; panel titles left-aligned so arrows enter on the right; BG twins from the overlay; Bulgarian captions (G01). Printed at 16.7 cm (95 %) = 0.84 × saved size → **labels 8.4 pt, titles 9.2 pt**, 393 ppi.
- `deepstack_arch[_bg].png` (fig. 24) — side-by-side → two stacked panels (G02); net above the re-solve box with a straight dashed "leaf values" arrow; "loops back" note dropped (the arrows say it); turn → "търн", zero-sum → "изход с нулева сума", leaf → "листата", "с нея", "ОФЛАЙН"; width 92 % → 95 % (at 92 % fs 10 prints 8.1 pt); EN caption "(left)/(right)" → "(top)/(bottom)". Prints 16.7 × 13.4 cm.
- `libratus_arch[_bg].png` (fig. 25) — three stacked panels re-laid out (G03): abstraction box full width, gadget "Приспособление" under the solve step, dashed value-estimate arrow down the m3/m4 gap with its note in the white gap, off-tree note in the panel, feedback note one line in the gap; "Достигане на кръг 3", "РАЗШИРЕНАТА" (one term), no imperative/1st person, "55 млн.→2,5 млн.", "самоусъвършенстване". Loop arrow now Act → gadget (a new augmented subgame), m3–gadget an undirected connector. Prints 16.7 × 20.1 cm.
- `pluribus_arch[_bg].png` (fig. 26) — two panels (G04): blueprint strategy box under the solver, dashed arrow down the q2/q3 gap into the leaf box, online loop drawn as a cycle (state → finer subgame → solve → leaf evaluation → act → next decision), off-tree note inside the panel; "подробна" (fine), no Latin "a", "корен на под-играта", "ЛИСТО", "изместен към отказ / плащане / повишаване", "Действие по последната итерация", "MCCFR с външна извадка"; online title on two lines so it ends left of the dashed arrow. Prints 16.7 × 19.8 cm.
- `_diagram_utils.py` — note() default fs 10; panel_bg label_ha (G05).

## Remaining overflow / legibility warnings
- `render_bg_figures.py` reports no overflow for figs. 24–26; no renderer re-wraps (checked in the images).
- By design: the dashed blueprint arrow crosses the short m3→m4 (fig. 25) and q2→q3 (fig. 26) arrows in the inter-box gap (as in the review's own layout); nothing crosses a box or a label.
- Figs. 27–30 (ReBeL/SoG/evolution/reuse) are 06b's and still the old renders.

## Verification
- `python scripts/build_reports.py --step step06 --type all`: all built — summaries EN 46 pp / BG 55 pp; one-pagers EN 1 page (10pt/1.8cm), **BG 1 page (9pt/1.3cm)**.
- `check_headings.py`: step06 EN/BG — no missing headings (the 3 misses listed are step07_bg ×2, step08_en).
- `check_captions.py`: step06 OK (only step08_en flagged).
- BG PDF: Cyrillic `\text{експлоатируемост}` / `\text{без съжаление}` / `σ_усъв` typeset (pp. 8, 17, 26); all 15 footnotes print with text (no literal `[^…]`); `render_printed.py` crops in `deliverables/finalReview/renders_fix/step06/ch06/p006, p014, p024` checked.
