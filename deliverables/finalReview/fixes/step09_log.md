# Step 09 — fixes applied
Applied: 72 (3 of them in part) · Skipped: 0 whole findings, 3 parts · Central: 11 (T01–T11) + 4 other items

Counted per finding id (83 in the review: G 12 · B 35 · T 11 · C 12 · S 8 · X 5). Every G, B, C, S
and X finding was applied; the 11 T findings are glossary-file changes, so they are central, and
their occurrences in this chapter were fixed through the B findings. Quotes were applied by exact
search and replace with a one-match assertion per quote (summaryEn 46, summaryBg 143 + 10 captions,
onePager 6, onePagerBg 18, report_en 30). All quotes matched. `report_bg.md` had no findings of its
own but carried every glossary defect of the summary, so it was rewritten paragraph by paragraph
against `report_en.md` (same structure, same numbers).

No R-item for this step. Nothing was rerun: every number comes from the saved JSON, whose sha256 was
checked before and after every plotting run (all seven files unchanged).

**Content fixes (as the review verified them).**
- C04/S02: "the CTDE variance-reduction claim, confirmed" → "the centralized critic fits its value
  target far more precisely; that alone does not mean lower policy-gradient variance — with converged
  critics a centralized critic can even increase it (Lyu et al., 2021)". Applied in the summary
  (§ 9.5, reconciliation, § 9.9 (4), takeaways), both one-pagers (the bullet head too: "fits its
  value target almost exactly"), the report (§ 6 heading "critic residual", results, conclusion,
  § 9.4, § 11.2, § 12) and the fig. 50 panel title ("lower = better fit", not "less variance").
- C05: the "MADDPG" is labelled a discrete-action variant with a COMA-style counterfactual baseline
  (Foerster et al., 2018) in the summary reconciliation, report § 6/§ 9.4/§ 11.2 and both one-pagers.
- C02: the orbit reconciliation now says the closed orbit is right for infinitesimal steps (Singh et
  al., 2000) and the outward spiral comes from the fixed step 0.1 — summary, fig. 48 caption, report
  § 3 and § 9.1; takeaway 1 and § 9.9 (1) scoped to "last iterate / at a fixed step".
- C01, C03 (+ S08 Abou Risk & Szafron), C06, C07, C08, C09, C10, C11, C12 as proposed, EN and BG.

**Glossary ✅ rows applied beyond the review's list** (grep for the "Now" forms, incl. report_bg):
1.1 двуигров, 1.7 Нашев/Нашов/наш, 1.18 предсказвач → оракул, 1.27 съгласуване → съпоставка,
1.29 хвърляне на монета → „съвпадение на монети“ (Matching Pennies), 1.30 дефект → предателство,
2.1 политика → стратегия, 2.2 on-policy, 2.4 самостоятелно → независимо обучение, 2.6 сходява,
2.10 разминаване (trajectory) → отдалечаване, 2.13 средно по времето, 2.16 изчислителна мощност →
изчислителни разходи/бюджет, 2.34 плъзгаща средна → текуща средна, 2.35 smoke/scale → бърза
проверка / пълен мащаб, 2.38 семена → начални числа, 2.39 проектиран градиент, 2.48 игрови мащаб →
мащаб на опростен модел, 3.13 четене → преценка за противника, 0.2 English values (Kuhn's Theorem,
Machine Zero, LOLA learners, Iterated Prisoner's Dilemma, jSON artifacts), "Глава 07" → "Глава 7".
Rows 1.10, 2.3 and 2.5 were not touched (see Skipped).

**Deviations from the review's proposals (on purpose).**
- B08/G01/G07: "пробна / пълна конфигурация" → glossary row 2.35 wording ("конфигурация за бърза
  проверка (smoke)", "конфигурация в пълен мащаб (scale)", "бърза проверка").
- "котва" (anchor) is "опора" throughout (B25/B33 use "опора" in two places; the other four
  occurrences said "котва", so the chapter now uses one word).
- S05: besides the footnote, "often the strongest baseline" is softened to "a strong baseline, often
  competitive with or better than more elaborate methods" — what the verified page supports.
- X03: QMIX gets its own table row (with the `rashid2018` citation in the timeline), and the
  sentence says "MADDPG, MAPPO and QMIX are three variants of CTDE".
- X01 applied to the EN summary too ("§4" → "Section 9.4").
- EN one-pager "(kept predictions, §9)" → "§9 of the report", as in the BG.
- New footnotes (EN+BG): abourisk2010, lyu2021, claus1998, matignon2012, foerster2018coma,
  rashid2018, kuhn1953; foerster2018 completed; lowe2017 (MAPPO title/venue), albrecht2024
  (Ch. 5 and 9), lanctot2017 (Tuyls) corrected.

## Skipped (id — reason)
- B03 (part) — self-play is glossary row 2.3, still open. "самообучение" is left as is, including in
  the new text (fig. 53 caption and title: "Самообучение в Кун…" instead of the review's "Игра
  срещу себе си…"). The one meaning error — § 9.9 "самостоятелното обучение се сближава в средното"
  (self-play rendered as independent learning) — was changed to "самообучението", so the later
  row-2.3 pass will catch it. "двоен предсказвач" was fixed (oracle, row 1.18).
- S02 (part) — Kraemer & Banerjee (2016) not added: the reviewer did not read it ("To verify"); the
  definition keeps Lowe et al. (2017), and the variance claim now rests on Lyu et al. (verified).
- S08 (optional part) — Robinson (1951) not added.

## Central (id — what is needed)
- T01–T11 — `glossary_settled.md` / `terminology_EN_BG.md`: converge (сходява), Kuhn's Theorem /
  Machine Zero / Iterated Prisoner's Dilemma / LOLA learners / JSON artifacts / EGTA Meta-Game,
  defect, thesis hooks, greedy team reward / greedy reward, two-player, matching pennies, oracle
  family (also the curated file), self-play (row 2.3, open) and independent learning, time-average /
  divergence, reconciliation, climbing game / value loss / referential task / learner entries /
  hard-exploration coordination.
- Figure labels — merge `fixes/labels_step09.json` (76 keys). New generic keys that other chapters
  would inherit: "Kuhn", "Leduc", "central", "independent", "optimum", "safe", "start" (старт →
  начало), "none" (→ без централизация), "Prisoner's Dilemma", "Stag Hunt", "Battle of the Sexes",
  "average iterate". **"solve" is shared with step 10**: the overlay changes "реши" → "решаване"
  (the imperative was wrong there too — please confirm for step 10). Now-unused step-09 keys can be
  pruned: the old one-line EN strings of the four diagrams (e.g. "Centralized critic  $Q(s,\,a_1,a_2)$
  \n(low-variance target)", "local obs $o_1$", "LOLA\nmodels opponent as a LEARNER", "…Step 07)",
  "PSRO = Step 2's …"), "Climbing game: CTDE escapes the safe trap", "Critic residual (lower = less
  variance)", "Matching Pennies: independent learners orbit, never converge", "naive (agent 1)",
  "LOLA (agent 1)", "P(col = Heads)"-style keys are kept.
- Renderer / script list — the exploration scripts no longer contain `savefig`: their plotting moved
  to the new `implementation/step09/exploration/plot_results.py`, which only reads `figures/*.json`
  (the two matrix-game figures recompute their deterministic exact-gradient trajectory, which the
  JSON does not store — < 1 s, nothing written but PNGs). So the renderer now runs plot_results.py
  instead of the experiment scripts, which rewrote their JSON when run. `selfplay_vs_nash.py` in
  `extract_labels.SKIP` is now redundant but harmless; if `check_coverage.py` lists step-09 figures
  as English-only by decision, those entries can go (all six data figures have BG twins).
- `plotting.py` default is now `--config scale` (the chapter's numbers); `render_bg_figures.py`
  therefore plots the scale results.
- Typography § 5.1–5.2 not applied (dashes, decimal comma in text). New text follows the
  surrounding style.

## Numbers changed (old → new, where)
No measured value changed (JSON untouched). Wording/ranges corrected against the JSON:
- Goofspiel K=4: "oscillates 1.4 ↔ 2.0" → "1.24 ↔ 2.0 (8 rounds)"; "~1.4 and ~2.0" → "~1.2 and 2.0"
  — summary EN/BG table + reconciliation 2, report EN/BG § 5 table/results and § 9.3; report final
  value gets its round index "(7)".
- Goofspiel K=3 (1.33 → 0) marked as the smoke config — summary tables, reconciliation 2, report § 5
  (table + Data line: from `smoke_results.json`, scale ran K=4 only), § 9.3.
- Leduc PSRO: "clear, roughly monotone decline" / "declines steadily" → "oscillates over the first
  eight rounds (3.73–6.83; round 1 is the maximum), then declines to 2.16" — summary, fig. 52 caption
  (EN/BG), report § 5 results and § 9.2.
- LOLA exploration run: "~2.9" → "2.67 and 2.93 for the two agents (mean 2.80)" — summary EN/BG § 9.8,
  report EN/BG § 8 (was "~2.67–2.93"); fig. 54 now plots the mean of both agents.
- Fig. 52 caption: RPS removed (not plotted).

## Figures (file — what changed — printed size now)
Printed sizes from `renders_fix/step09/manifest.json` (BG summary, figs. 1–10 = bundle 45–54).
Type size = fs × printed width ÷ saved width.
- Fig. 1 `nonstationarity_dance(_bg)` — all text fs 10; agent boxes 3.8 wide; bottom box 11.0 × 1.05
  (two lines); notes re-placed so nothing collides; BG top line wrapped, no English, „…“ quotes,
  "(учи се)". 17.6 cm, 377 ppi, text ≈ 8.8 pt.
- Fig. 2 `methods_spectrum(_bg)` — all fs 10.5; boxes no longer overlap; IL spans the whole
  horizontal axis; level labels ("без централизация / оценител при обучение / пълно решаване…") in
  one column; vertical axis label rotated; LOLA/PSRO/CommNet boxes enlarged; title two lines.
  17.6 cm, 414 ppi, ≈ 8.4 pt.
- Fig. 3 `matrix_games_playground(_bg)` — display names, BG axis labels, one figure-level legend,
  7 × 6.2 in at 300 dpi, fs 10; the Matching Pennies panel is a separate off-centre run (0.7, 0.3),
  titled so (the table's centre run stays as reported). 17.5 cm, 300 ppi, 10 pt.
- Fig. 4 `nonstationarity_demo(_bg)` — title "spiral outward, never converge", legend below the axes
  (equilibrium star visible), 300 dpi, fs 10. 13.4 cm, 300 ppi, ≈ 10 pt.
- Fig. 5 `ctde_architecture(_bg)` — all fs 11; label boxes 1.2 high, critic 1.6; the two notes are
  two-line and inside their panels (no collision); "цел с ниска дисперсия". 17.6 cm, 431 ppi, ≈ 8.4 pt.
- Fig. 6 `impl_coop_ctde_comm(_bg)` — title "no method reaches the optimum"; critic panel on a log
  axis (the 3.2e-11 bar is now visible); static legends; ticks via set_xticklabels (translated);
  2 × 2 layout (critic | communication / climbing game across) because a 1 × 3 row at print width
  collided in BG; caption reordered (Горе вляво / Горе вдясно / Долу). 17.3 cm, 300 ppi, 10 pt.
- Fig. 7 `psro_loop(_bg)` — "Chapter 2"/"Chapter 7", all fs 10.5, boxes widened, arrow labels above
  the row, bottom box 9.0 × 1.2 (two lines); no imperatives or "предсказвач". 17.6 cm, 363 ppi, ≈ 9.6 pt.
- Fig. 8 `impl_psro_exploitability(_bg)` — display names, integer rounds, 300 dpi, fs 10.
  17.0 cm, 300 ppi, 10 pt.
- Fig. 9 `selfplay_vs_nash(_bg)` — first BG twin (via plot_results.py), legend clear of the curves,
  title wrapped, 300 dpi, fs 10. 16.7 cm, 300 ppi, 10 pt.
- Fig. 10 `lola_ipd_playground(_bg)` — mean of both agents, legend fs 10, 300 dpi. 16.8 cm, 300 ppi,
  10 pt.
- All ten BG captions are Bulgarian; `summaryBg.md` links every `_bg` twin; EN and BG PNGs copied to
  `summary/` and `figures/`; `figures/README.md` status set to generated.

## Remaining overflow / legibility warnings
- `render_bg_figures.py --only step09 --labels-overlay …`: 7 scripts ok, 11 BG figures, **no
  overflow warnings**.
- Fig. 3 BG: the Matching Pennies panel title is wider than its panel (it stays inside the figure and
  touches nothing).
- Fig. 6 is now ~14 cm tall; if page breaks get tight after the typography pass, it can be scaled.

## Verification (build ok? check_headings / check_captions output for this step)
- `python scripts/build_reports.py --step step09 --type all`: all six PDFs built. Summaries EN 21 pp,
  BG 24 pp; reports EN 11 pp, BG 13 pp; one-pagers EN 1 page (10 pt / 1.5 cm), **BG 1 page
  (8.5 pt / 1.2 cm)**.
- `check_headings.py`: 44 PDFs, 9 missing headings — all in step 08 (report_bg, summaries); step 09
  clean.
- `check_captions.py`: 24 PDFs, 2 with unaccounted figures — both step 08; step 09 EN/BG clean.
- `render_printed.py --pdf deliverables/summaries/step09_bg.pdf --out
  deliverables/finalReview/renders_fix/step09`: 10 crops, 300–431 ppi, all read; no overlaps, no
  English in the BG figures.
- Text scan of the three BG PDFs: no "⟦", "дефект", "сходява", "предсказвач", "хвърляне на
  монета", "самостоятелно", "двуигров", "Нашев/Нашов", "политик", "съгласуване", "опонент",
  "Stag/Hare", "Kuhn's Theorem", "Machine Zero", "Step/Стъпка", "Глава 0…".
