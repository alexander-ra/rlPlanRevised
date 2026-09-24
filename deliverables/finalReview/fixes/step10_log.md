# Step 10 — fixes applied
Applied: 62 · Skipped: 0 · Central: 11

Counted per finding id (73 in the review: G 11 · B 32 · T 10 · C 10 · S 8 · X 2). All G, B, C
and S findings and X01 were applied. T01–T10 are glossary-file changes, so they are central;
their occurrences in this chapter were fixed through the B findings and the glossary pass. X02
is corpus-wide. Every quote matched exactly: 108 replacements in `summaryBg.md`, 44 in
`summaryEn.md`, 31 in `onePagerBg.md`, 6 in `onePager.md` and 28 in `report_en.md`. Each script
asserted one match per quote. `report_bg.md` had no line-level findings, so 85 of its lines were
rewritten for the same content fixes and the glossary rows (see below).

**R7 (text fix), as decided in TRIAGE § B.** Nothing was rerun. All numbers were read from
`implementation/step10/implementation/results/{smoke,scale}_results.json`.
- **C01.** "Rest points are exactly Nash; stable rest points are ESS" is gone from the summary,
  report § 2 and fig. 55. The text now says every Nash equilibrium is a rest point, stable rest
  points are Nash, and every ESS is asymptotically stable. It cites Hofbauer & Sigmund 2003 (new
  footnote).
- **C02.** The meta-Nash mixture (3.418) is better than self-play's final agent (3.683), not
  "the weakest". Tables and text were reordered and rewritten in the summary, report § 7 and
  fig. 63.
- **C03.** The "tells" explanation is gone. The mixture is *less* exploitable than each of its
  three components (3.558, 3.932, 4.262; weights 0.322, 0.645, 0.032). The least exploitable
  agent (`main_2#e29`, 1.305) got zero weight. "Its best member" now reads "the population's best
  member" in the summary, one-pagers, report § 6/§ 8.1/§ 10/§ 11 and fig. 62.
- **C04.** Best-of-run is now compared like for like. Self-play's best iterate is 1.396 at
  epoch 100, and the text says "one run each". Self-play also regresses after epoch 100 without
  exploiters, so the exploiter-pressure explanation is hedged.
- **C07 (NashConv).** Every value is labelled NashConv at its first use, in summary § 10.5 and
  report § 4, with the OpenSpiel halving stated there. The comparison tables and figs. 60 and 63
  also say NashConv.
- **Spinning top (S04).** The decomposition is credited to Balduzzi et al. 2018 (new footnote) and
  2019. The spinning-top geometry is credited to Czarnecki et al. 2020 (new footnote). This was
  applied in the summary text, the reconciliation, the history line, the footnotes, both reports'
  § 8.2 and the figure-script docstring.

**Glossary ✅ rows applied beyond the review's list:**
- 1.18 "предсказвач" → "оракул". This includes places where the review's own proposals said
  "предсказвач": B24, the C04 one-pager and table 39.
- 1.27 "Съгласуване" → "Съпоставка", instead of the review's "Съпоставяне".
- 2.16 → "изчислителни разходи" (the review's B14 had "ресурси").
- 1.6, 1.7, 1.25, 1.26, 1.30, 2.1, 2.35, 2.38, 2.43, 2.48, 0.4 and row 4 (AlphaStar) in
  `report_bg.md`.
- Rows 1.10, 2.3 and 2.5 were not touched. "самообучение" stays everywhere, including in new
  text and figure labels.

**Extras (same kind of defect):**
- Comparison tables (summary EN/BG, report EN/BG) have a new "self-play – best iterate" row, so the
  table matches fig. 63.
- Report EN/BG § 2: "at a steady radius" is now the Euler-spiral wording (C10).
- Report EN/BG: "raw step" → "original plan" in the rewritten sentences.
- "Chapter 07" → "Chapter 7" in the EN summary and one-pager.
- The one-pager BG title and heading now use "Обучение на базата на популации" (B30 rule).
- All `report_bg` captions are now Bulgarian and link the `_bg` twins.

## Skipped (id — reason)
- None. Deviations, all intentional:
  - **B32.** PFSP is expanded where the review put it (§ 10.5 "сдвояването по PFSP"). The table in
    § 10.2 and "PFSP самообучение" earlier in § 10.5 mention it first, unexpanded.
  - **G10.** Fig. 63 is now a horizontal bar chart sorted by value, not the review's vertical order.
    The labels would not fit under six vertical bars in BG.
  - **Overlay keys.** Figure-label keys follow the new EN strings, not the review's proposed keys.
    For example, titles are two-line "Prisoner's Dilemma\nshare of Cooperate".

## Central (id — what is needed)
- **T01–T10.** Glossary files:
  - defect → предателство
  - wheel of counters → кръг от контрастратегии
  - self-play is open (row 2.3)
  - exploiter → експлоататор
  - churn → непрекъсната смяна
  - non-words (отговорчик etc.)
  - spinning-top attribution in `terminology_EN_BG.md` l. 92 (row 1.31)
  - smoke/scale → бърза проверка / пълен мащаб
  - rest point → точка на покой
  - policy → стратегия
- **X02.** The BG subtitle in the YAML of all summaries/one-pagers differs from the official
  title. Fix it corpus-wide.
- **Footnotes (§ 5.3).** `lanctot2017`, `balduzzi2019` and `vinyals2019` are also defined in other
  chapters. New in ch. 10: `hofbauer2003`, `balduzzi2018`, `czarnecki2020`, `jaderberg2017`,
  `wellman2006`, `tuyls2020`.
- **Shared label keys changed by `labels_step10.json`:**
  - 'solve' → 'решаване'. Shared with step 09; the imperative "реши" is wrong there too.
  - 'weakest' → 'най-слабите'.
  - 'meta-Nash exploitability', 'league epoch', 'exploitability (NashConv, exact)',
    'pure skill (transitive)' and 'pure cycling (RPS)' were corrected.
  - Now-unused step-10 keys can be pruned: the old one-line box labels, "…(this step)",
    "PREDICT: …" titles, 'min main-agent exploitability', 'population diversity (…)',
    'Naive PBT: …', the old CAVEAT and "measured: …" notes, 'Spinning-top: …', 'Leduc
    exploitability (lower = closer to Nash)', 'Comparison on Leduc …'.
- **Renderer.** `render_bg_figures.py --only step10` also runs `exploration/game_landscape.py`.
  That script re-runs 8 PSRO rounds on Leduc (minutes) and rewrites `game_landscape.json`. Its
  figure is not cited anywhere, so I ran the renderer per script (`--only step10/summary`,
  `…/implementation/plotting`, `…/exploration/mini_pbt`, `…/exploration/replicator_playground`).
  A central run should skip `game_landscape.py`.
  - `mini_pbt.py` and `replicator_playground.py` rewrite their JSON on every run. They are seeded
    and deterministic; the checksums were unchanged.
- **Not edited** (outside this step's plotting/deliverable scope, or not a finding):
  - `report_en/bg` § intro "AlphaStar league … whose guarantee is missing" was not softened (S01
    was scoped to the summary).
  - `figures/README.md` still gives the old `plotting.py --config` usage.

## Numbers changed (old → new, where)
- **Minimum timing.** "Minimum near epoch 60 / 60-65 / ep ~64" → "steep fall within ~15 epochs,
  lowest around epochs 20–40 (meta-Nash 1.32 at ep 21; best snapshot ep 29); single min-main low
  1.21 at ep **66**". Changed in summary EN/BG § 10.5, fig. 60 caption, report EN/BG § 5 and § 8.3.
- **Self-play.** Best iterate **1.396 (ep 100)** added next to its final agent 3.683 in the summary
  tables, one-pagers, takeaways, report § 7/§ 9/§ 11 and fig. 63. Smoke best iterate: 3.111.
- **Mixture components.** 3.558 / 3.932 / 4.262 and weights 0.322 / 0.645 / 0.032 added (C03).
- **C06.** A note says 2.96 is the start-of-epoch-119 meta-Nash, while 3.418 is the final
  56-agent EGTA.
- **AlphaStar.** "~600 agents" → "almost 900 distinct players" (S05; summary EN/BG, report EN/BG
  § 10).
- **History line.** "spinning top 2019" → decomposition 2018–2019, spinning top 2020.
  AlphaStar "beat human pros" → Grandmaster, above 99.8% of ranked players.
- **SVD rank-1 (C09).** The reason now given: the method caps at 0.707 for any game (it also gives
  0.707 on a skill ladder).

## Figures (file — what changed — printed size now)
All nine BG figures now print in Bulgarian. `summaryBg.md` links nine `_bg` files, and
`report_bg.md` links five `figures/*_bg.png`. Every canvas is ~7 in wide, so fonts print at
about their set size. Crops are in `renders_fix/step10`.

- **Fig. 1 `replicator_selection(_bg)`** (`make_replicator_figure.py`):
  - Redrawn at 7 × 5.5 in, all text fs 10. Boxes are 6.3 × 1.7 and nothing is bold.
  - The rest box now reads "Stable rest points = ESS" (C01); the title says "this chapter".
  - BG labels are pre-wrapped, so no hyphen breaks.
  - 17.6 cm, ≈ 9.9 pt, 331 ppi.
- **Fig. 2 `replicator_playground(_bg)`** (`exploration/replicator_playground.py`):
  - 2×2 at 7 × 5.6 in, dpi 300.
  - Display titles replace the code names; legend is $x_0$; fs 10 (legend 9.5).
  - The BG twin is new. 17.6 cm, ≈ 9.9 pt, 303 ppi.
- **Fig. 3 `spinning_top(_bg)`** (`make_spinning_top_figure.py`):
  - Wider markers with two-line labels. The T/C sub-labels sit on a white patch below the
    markers, and the cyclic note moved out of the RPS marker.
  - The bottom note is split into 3 lines, so the canvas no longer inflates. fs 10.
  - The BG twin is new. 17.4 cm, ≈ 9.9 pt, 330 ppi.
- **Fig. 4 `impl_transitive_ratios(_bg)`** (`plotting.py`):
  - Display tick labels via `set_xticklabels`, so the BG render translates them.
  - Value labels use a locale decimal comma. No title; ylabel "transitive ratio"; dpi 300.
  - The BG twin is new. 17.6 cm, ≈ 9.9 pt, 303 ppi.
- **Fig. 5 `league_architecture(_bg)`** (`make_league_figure.py`):
  - 7 × 4.8 in, fs 10.
  - The PFSP note moved above the panel, clear of its title. The "measured: …" note was deleted
    (C04).
  - The exploiter arrow now dips below the boxes; "->" became "→".
  - 16.8 cm, ≈ 10 pt, 330 ppi.
- **Fig. 6 `impl_league_exploitability(_bg)`** (`plotting.py`):
  - No PREDICT title, no markers.
  - The self-play trajectory is added as a dashed grey line (optional part of G07; it supports
    C04).
  - y-label NashConv; dpi 300. The BG twin is new. 17.6 cm, ≈ 9.9 pt, 303 ppi.
- **Fig. 7 `mini_pbt(_bg)`** (`exploration/mini_pbt.py`):
  - Display legend names, no title, new y-label, dpi 300.
  - The BG twin is new. 17.6 cm, ≈ 9.9 pt, 303 ppi.
- **Fig. 8 `egta_pipeline(_bg)`** (`make_egta_figure.py`):
  - 7 × 4.3 in, fs 10.
  - The caveat is now a full-width box with the corrected content (C03). "Step 07" → "Chapter 7".
  - BG decimal commas in the caveat. 17.6 cm, ≈ 9.9 pt, 331 ppi.
- **Fig. 9 `impl_comparison_exploitability(_bg)`** (`plotting.py`):
  - Horizontal bars sorted by value, six rows including the league's best individual and
    self-play's best iterate (G10, C04).
  - Locale value labels; x-label says NashConv. The BG twin is new. 17.6 cm, ≈ 9.9 pt, 303 ppi.
- **Report only.** `impl_replicator_portraits(_bg)` (`plotting.py`) got the same 2×2 treatment
  as fig. 2. `plotting.py` now defaults to `--config scale` and uses `parse_known_args`.

## Remaining overflow / legibility warnings
- The renderer (save-time fitting, fs 9.5 floor) reported **no overflowing labels** for any step-10
  script.
- The BG figures print at ≥ 9.4 pt (legends) and ≈ 9.9 pt elsewhere.

## Verification (build ok? check_headings / check_captions output for this step)
- `build_reports.py --step step10 --type all`: all 6 PDFs built.
  - Summaries: EN 16 pp., BG 19 pp.
  - Reports: EN 15 pp., BG 18 pp.
  - One-pagers: EN 1 page (10 pt / 1.8 cm), BG 1 page (9 pt / 1.3 cm).
- `check_headings.py`: step 10 is clean. The only misses reported are in step 08, whose agent is
  still working.
- `check_captions.py`: step 10 is clean (captions 1–9 in EN and BG). The only flag is step 08.
- `render_printed.py`: 9 crops, all read and legible.
- Result files were checksummed before and after every plotting run and are unchanged:
  - `scale_results.json` 835bd28e…
  - `smoke_results.json` fdca6ae4…
  - `mini_pbt.json` b386b1c0…
  - `replicator_playground.json` e91c8a59…
  - `game_landscape.json` 66d11057… (not run)
