# Step 01 — fixes applied
Applied: 57 · Skipped: 2 · Central: 6

Applied = G01–G03, B01–B29, T01–T04 + T06–T12 (occurrences in this chapter), C01–C08,
S01–S05, X01. 189 exact search-and-replace edits across summaryEn/Bg, onePager/Bg and
report_en/bg; every quote in the review matched. A few items were superseded or adapted:

- **C01: option B, as instructed.** The text now describes the SB3 DQN run that the figure
  and the committed `sb3_results_cache.json` contain: the run of 6 Apr 2026 (commit de7456b),
  with the RL Zoo's tuned CartPole settings and 100K steps. It reaches 1,255 episodes, a best
  rolling-100 of 222.4 at episode 695 (≈51K steps) and a final 134.3. All of these were
  recomputed from the cache. The Zoo settings were verified against `hyperparams/dqn.yml`
  on GitHub (n_timesteps 5e4), and the citation `[^rlzoo2020]` against the Zoo README's
  BibTeX. The three-cause list ("fixed 1000-step interval", step-based ε, early stopping)
  was dropped, because it does not describe this run. The report EN/BG keeps a
  "Superseded run" note on the 750K run of 3 Apr (293.9, commit 4a173d2).
- **C02: adapted to run (ii).** train_freq=4 does not apply to this run. The untested
  update-count difference is stated instead: 128 gradient steps per 256 env steps against
  our 1 per step. So is the exploration difference in the plotted training episodes:
  final ε 0.04 against ours ≈0.006 at episode 1011. "Decisive factors … advantage
  normalization" (§ 1.8 and report § 5.2) was softened to "used throughout / not measured".
- **Superseded by the C01 rewrite** (the sentence no longer exists): B01 item 3 ("като
  Atari Games"), B05 ("почти случайна мода"), B09 items 1–3, B22 items 4 and 6 ("5 епизода
  са…", "Настройките по подразбиране…").
- **B03:** "Итерация на политиката" was changed to "Итерация по стратегии", following
  GLOSSARY_DECISIONS 2.1, not the review's "Итерация на стратегията".
- **B10 (partial):** row 2.5 is open, so "самоподкрепяне" is kept (3× in summaryBg). The
  bias/tradeoff fixes were applied ("отместване (bias)", "компромис"). The same term is
  kept in the B03 triad item.
- **B23:** the bold was also dropped in the EN paragraph (parity). The EN C04 text has no
  bold, matching the BG.
- **B28:** K/M → "хил."/"млн." in summaryBg/onePagerBg prose only. The report keeps "K",
  as the review says for the report.
- **Report consistency** (not listed in the review, same claims): the glossary rows (2.29
  PPO gloss, 2.30 GAE — English left, 2.31 "персонализиран" 4×, 2.14, 2.25 "недообучена",
  0.4 "сходи/сходял", T09 "q-мрежа/reLU", T12 buffer) were applied to report_bg. So were
  "Run 1–3" → "Изпълнение 1–3", "Adam optimizer", "Mini-batch SGD", "дипломна работа" →
  "дисертационната работа", and "300K стъпки са едва достатъчни" (meaning inverted) →
  "се оказаха малко недостатъчни". The BG report figure captions were translated.

## Skipped (id — reason)
- T05 — row 2.5 (bootstrapping) is not yet decided; "самоподкрепяне" (summaryBg ×3) and the
  misspelled "буутстрапинга" (report_bg § PPO architecture) are left for the later pass.
- S06 — spot-check only; nothing to change.
- G02(a), seed part — adding `seed` to dqn/train.py and ppo/train.py and re-training is
  not plotting code, and a re-run is not allowed. Needs the candidate (see Figures).

## Central (id — what is needed)
1. T01–T04, T06–T10, T12 — the glossary files themselves (`glossary_settled.md`, curated
   `terminology_EN_BG.md`, incl. "контрафактуалн…" → "контрафактичн…"). Only this
   chapter's occurrences were fixed.
2. S02 — the same corrected `[^shoham2008]` text is needed in steps 02, 07 and 08 (or fix
   F07-X01). `[^suttonbarto2018]` (Ch. 13 and §11.3 added) is shared with step 03.
3. `scripts/figures/out/figure_labels.json` — merge `fixes/labels_step01.json`. Drop the
   stale runtime key 'Custom\nstopped\n(ep 0)', and replace the 'Персонализиран …' values
   of 'Custom DQN' / 'Custom PPO'. The overlay's number keys ("477.5" → "477,5" …) serve
   the bar values of final_metrics.
4. Row 2.5 (bootstrapping) — see T05.
5. T11 — the corpus-wide "сходява" grep. Step 01's occurrences are fixed (B08, report_bg).
6. GLOSSARY 2.20 ("critic → критик") conflicts with the curated "Оценител / актьор-оценител".
   The chapter keeps "оценител"; somebody has to pick one. Row 2.34 ("плъзгаща средна" →
   "текуща средна") was deliberately not applied: here it is a rolling (windowed) average,
   for which "плъзгаща се средна" is correct.

## Numbers changed (old → new, where)
- SB3 DQN best rolling-100: 293.9 → 222.4 (onePager EN/BG, report EN/BG § 4.1, § 4.3 table,
  § 5.3; summary EN/BG § 1.9.1).
- SB3 DQN run: 750K steps / 17,176 episodes → 100K / 1,255 (same places). "Rolling average
  stays around 30" → "peaks at 222.4 at episode 695 (≈51K steps), ends at 134.3" (summary).
- SB3 DQN target sync: "fixed 1000 steps" → every 10 steps (Zoo). Budgets: "matched (DQN
  750K, PPO 500K)" → "PPO 500K matched; DQN 100K with the Zoo settings".
- final_metrics.png, custom PPO bar: 180.3 (the earlier [64,64] run) → 203.6 (final run).
  This now agrees with the report table.
- Fig. 2, custom PPO curve: 730-episode run → 547-episode final run (restored render; see
  below).
- No other result number changed. 477.5, 202.2, 203.6, 543, 264,192 and 131.2 are as
  before. 543 cannot be re-checked without the logs, but it is consistent with the
  restored figure, where training stops at episode 547.

## Figures (file — what changed — printed size now)
The TensorBoard logs of our DQN/PPO runs were never committed (gitignored) and exist
nowhere on disk (C:/ and D:/ searched). Without re-training, `compare_sb3.py` cannot re-draw
the learning curves. What was done instead:
- `figures/ppo_comparison.png`: restored from commit 049b4c4 (3 Apr). That render plots
  the final PPO run (547 episodes, early stop) against the same SB3 PPO data as today's
  cache (1,224 episodes, footnote and 131.2 match). The 6 Apr render had plotted Run 1
  (730 episodes, best 180.3) — F01-G03.
- `summary/make_comparison_panels.py` (new, stop-gap): crops the rolling-average panel
  (G02c) out of the saved two-panel renders. It redraws the axis labels and an opaque
  legend exactly over the old one (a coverage check is built in), so render_bg_figures
  produces the BG twin from the overlay. Curves and tick numbers are the saved pixels,
  unchanged. It checks its input layout and writes nothing once compare_sb3.py produces
  single-panel figures again.
  - `dqn_rolling.png` / `_bg` (summary/ and figures/) — prints at 15.0 cm. Tick numbers
    9.9 pt, labels 10 pt, legend 9.9 pt (was 5.9 / 5.9 / 4.3–7.5 pt). The raster content
    is 167 ppi; the PNG is 300 dpi.
  - `ppo_rolling.png` / `_bg` — same sizes. Its window is still 50 episodes, as in the
    saved render; the captions and the report say so.
- `figures/final_metrics.png` / `_bg`: regenerated by compare_sb3.py in plot-only mode.
  Custom bars use `RECORDED_CUSTOM_BEST` = {477.5, 203.6} (read from the logs on 3 Apr;
  049b4c4 render). SB3 bars are computed from the cache. 7.0×3.4 in, 300 dpi; prints at
  16.6 cm in the report ≈ 10 pt. The suptitle was dropped.
- `implementation/step01/compare_sb3.py` (plotting code only): G02a–d and G03 for the
  next real render. It selects the run explicitly (DQN_RUN/PPO_RUN, or the only event
  file; it refuses to guess), writes a `custom_results_cache.json` on the first read,
  uses a single panel at 7.0×3.4 in with window 100 for both, adds an axvline legend
  entry "Custom stopped", drops the note and footnote, uses fonts 10.5/11 and 300 dpi,
  and trains SB3 only with `--train-sb3` when there is no cache. Without logs it leaves
  the saved comparison PNGs untouched; before, it would have drawn SB3-only curves.
- Summary and report EN/BG now point at `*_rolling(_bg).png` and `final_metrics(_bg).png`.
  `summary/dqn_comparison.png` and `ppo_comparison.png` are unused. They were kept,
  because `summaryBg_old.md` still references them.
- **For the candidate:** a seeded re-run of dqn/train.py (~1,000 episodes) and
  ppo/train.py (~264K steps), with seeds added to both configs, would let compare_sb3.py
  redraw both figures properly with window 100. The panels script is then obsolete, and
  the summary should point back at `dqn_comparison(_bg).png` / `ppo_comparison(_bg).png`.

## Remaining overflow / legibility warnings
- The renderer reported no overflowing labels. The final_metrics BG y-label is wrapped
  onto two lines through the overlay.
- X01, partly: § 1.9's heading fits on one line now. Fig. 1 (15 cm × ~10 cm with caption)
  still does not fit under the § 1.9 intro, so PDF p. 10 of the chapter has about a
  quarter page blank (was half).
- The raster content of Figs. 1–2 is 167 ppi (the saved 150-dpi render at 0.9 scale):
  sharp enough, but softer than a fresh 300-dpi render.

## Verification (build ok? check_headings / check_captions output for this step)
- `build_reports.py --step step01 --type all`: all 6 PDFs built. The BG one-pager is 1 page
  at 9 pt / 1.3 cm, the same type size as the previous build. Summary PDFs: EN 11 pp,
  BG 13 pp.
- `check_headings.py`: "44 PDF(s) checked, 0 missing heading(s)."
- `check_captions.py`: "24 PDF(s) checked, 0 with unaccounted figures."
- `render_printed.py` crops in `renders_fix/step01/ch01/` (p011_f1, p012_f1) were read:
  Bulgarian labels, legible, and the captions match the figures. Footnotes: every
  reference has a definition and none is unused (EN and BG). The new labels
  (kaelbling1998, vanhasselt2016, williams1992, gae2016, ouyang2022, raffin2021,
  rlzoo2020) are unique in the corpus.
