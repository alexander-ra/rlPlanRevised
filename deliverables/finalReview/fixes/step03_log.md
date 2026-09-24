# Step 03 — fixes applied
Applied: 59 of 59 findings (G 6 · B 20 · T 7 occurrences · C 17 · S 6 · X 3), 5 of them only in part (listed below) · Skipped: 0 whole findings, 5 optional or out-of-scope parts · Central: 6

R6 (fix) and R9 (text) are done. R6 involved **one seeded rerun** of the two OpenSpiel exploration scripts:
Kuhn took 6 s and Leduc 11 min 44 s, both under the 30-minute limit. The timed benchmark
(`cfr/train_all_timed.py`) was **not** rerun. It was already seeded (42) and its curves were already saved
in `models/timed_*_snapshots.json`, so it only gained a plot-only mode. Table 4, the constants, the
crossover inputs and the one-pager's 180 s numbers therefore stand.

### Deviations from the review's proposals (on purpose)
- **Metric (G01/G03/C07). The figures now plot what the text says; the labels were not changed to NashConv.**
  The rerun records exploitability = NashConv / 2, OpenSpiel's `exploitability`. This is the same quantity as
  figs. 10–11 and `evaluate/exploitability.py`. NashConv is stored beside it in the caches. Snapshots now
  end at 5,000 iterations (100·1.5ᵏ steps plus the final iteration), not 3,829. As a result:
  - the y-axis keeps "Exploitability" and the captions say "експлоатируемост", not "NashConv";
  - C07's "3,829 iterations / NashConv" rewrite became "5,000 iterations / exploitability" with the new numbers;
  - report § 4 "5,000 iterations" and "Exploitability @5k" are now simply true;
  - C07's defining sentence (exploitability = (BR₀+BR₁)/2, NashConv = sum) was added in § 3.5.
- **G02. PLOT_ONLY=1 (or `--plot-only`) loads the new seeded caches**, not the 1 Jul ones. The old caches are
  still in git at HEAD (commit 0957c86). The cache path is now script-relative, so the renderer no longer
  nests `exploration/exploration/`. The stray nested directory was deleted: 4 tracked files, now shown as
  " D" and not staged.
- **Time axis of figs. 1–4 (OpenSpiel).** The clock now stops while a snapshot is evaluated, as it already
  did in `train_all_timed.py`. The old times counted `nash_conv` evaluation, which made up most of MCCFR's
  "5–7 s". The axis label is now "Training time (seconds, log scale)".
- **G04.** The custom-CFR curve is now the real exploitability of chapter 2's average strategy, wrapped in a
  `TabularPolicy`. Its label is "Custom CFR (chance-sampled, Chapter 2)". The script's step02 import path
  was broken (`exploration/../step02`) and is fixed.
- **C04/S01 slopes.** My log-log fits of `models/timed_*_snapshots.json` give:
  - external −0.51 and outcome −0.39 (T ≥ 10⁵; −0.45 over 10⁵–3.6×10⁶), not −0.53;
  - vanilla −0.84;
  - CFR+ −1.77.

  The text therefore says "about −0.4 to −0.5" for MCCFR and "about −1.8" for CFR+.
- **Hold'em names.** GLOSSARY row 3.11 is used ("лимитен тексаски холдем за двама играчи", "безлимитен
  тексаски холдем"). The review's "Тексас холдем с/без лимит" is not.
- **Additional R9 edits** (limit hold'em claims that contradict Bowling et al. 2015):
  - § 3.1 "No computer can enumerate that tree even once" (EN and BG) now says one traversal took about an
    hour on 4,800 cores (see § 3.8);
  - one-pagers: "limit Hold'em (~1e14) is orders of magnitude past it" now reads "~3e17 states, past it by
    the model, yet solved by full-traversal CFR+".
- **Other edits outside the review's list:**
  - BG bullet "**Обща карта**" → "**Чифтове**" (the EN says "Pair hands"; the bullet also said "борд");
  - report § 3.5 and the source tree now give `(BR₀+BR₁)/2`. They said `BR₀+BR₁`, which is wrong for the code;
  - report § 4.2's conclusion sentence rewritten for the new numbers;
  - report reproduction block now points to `implDayOne1_test.py` and mentions `--plot-only`;
  - cross-references now use "Section 3.7 / 3.8" ("раздел 3.7 / 3.8");
  - the one-pager "anomaly" bullet was reworded per C04: the bound is not tight, and that is common.
- **Figures.** All six legends moved below the axes, because the Bulgarian names ran over a curve. Figs.
  10–11 were sized (8, 5) rather than (8, 4.4) to make room.

## Skipped (id — reason)
- C01 (part) — `implementation/step03/convergence_analysis.md` § 7 still says 2.1M / 4.8M. That file is
  outside the allowed files, so it is logged under Central.
- C11 (optional part) — the § 3.3 heading and the Markov-chain paragraph were kept. The lighter variant was
  applied instead: "trajectories drawn independently" and "at a fixed strategy profile".
- C15 (optional S3) — the Table 2 footnote on what "10,200" counts was not added.
- S05 (part) — no text was changed for the note that Bowling et al. used the *current* CFR+ strategy, which
  qualifies § 3.9's "Both still output the average strategy". The finding gave no proposal.
- S06 (optional) — the discounted-CFR sentence (`brown2019dcfr`) was not added. `schmid2019` is cited, per S02.

## Central (id — what is needed)
- G06 — merge `fixes/labels_step03.json` into `scripts/figures/out/figure_labels.json`. It has 19 keys,
  including "Vanilla CFR", which had no entry at all, the G06 corrections, and the new axis and legend keys.
- T01–T07 — the chapter's occurrences are fixed. Please confirm that the `glossary_settled.md` entries are
  updated: traverser, full-traversal cfr, ε-on-policy, MCCFR external/outcome, NLHE/HUNL, vanilla CFR,
  on-policy, the regret-flooring/averaging/variance compounds, Markov property, wall-clock.
- GLOSSARY row 3.14 ("Ледюк Холдем") was not applied. The chapter says "Ледюк покер" throughout, which
  matches the EN "Leduc Poker". Rows 1.10, 2.3 and 2.5 were left untouched, as the brief requires.
- Candidate — two files outside the allowed set still carry the old numbers:
  - `implementation/step03/convergence_analysis.md` § 7: crossover 2.1M / 4.8M → 1.1M / 2.4M, and
    210× / 466× → 105× / 233×;
  - `implementation/step03/exploration/README.md`: the Kuhn and Leduc tables still show old,
    unseeded values (Leduc as NashConv).
- Build — the report PDFs show double numbering ("1.3.5 3.5 …"). This is pre-existing and was not touched.
- Build — the dedupe filter reprints repeated footnotes as a back-reference; the chapter now cites
  `[^mccfr]` 5×, `[^bowling2015]` 2×, `[^tammelin2015]` 2× and `[^burch2019]` 2×. Six new footnotes were added:
  zinkevich2007, tammelin2015, burch2019, johanson2013, schmid2019, metropolis1987.

## Numbers changed (old → new, where)
- **§ 3.5 Leduc, OpenSpiel** (summaryEn/Bg) — CFR+ 5.4×10⁻⁵ → 1.8×10⁻⁵; vanilla ~7.6×10⁻³ → 3.6×10⁻³;
  ~140× → ~190×. The old values were NashConv at 3,829 from an unseeded run; the new ones are exploitability
  at 5,000, seed 42.
- **§ 3.6 Kuhn** (summaryEn/Bg) — "all four reach near-Nash" became measured values at 5,000:
  - CFR+ ≈ 3×10⁻⁵ and vanilla ≈ 2×10⁻⁴;
  - external sampling ≈ 0.013 and outcome sampling ≈ 0.04;
  - the chance-sampled chapter 2 CFR ≈ 0.006.
- **Report § 4.1 table (Kuhn)** — exploitability and time; times are now training time only:

  | Row | Exploitability | Time |
  |---|---|---|
  | Custom CFR | ~3.5×10⁻⁴ (not an exploitability) → 6.0×10⁻³ | <1 s → 0.03 s |
  | OpenSpiel CFR | ~1.5×10⁻³ → 1.8×10⁻⁴ | ~2 s → 2.1 s |
  | CFR+ | ~3.0×10⁻⁴ → 2.8×10⁻⁵ | ~2 s → 2.2 s |
  | External sampling | ~4×10⁻³ → 1.3×10⁻² | ~1 s → 0.4 s |
  | Outcome sampling | ~2.5×10⁻² → 4.1×10⁻² | ~1 s → 0.4 s |

- **Report § 4.2 table (Leduc)** — times are now training time only:

  | Row | Exploitability | Time |
  |---|---|---|
  | CFR+ | ~5.4×10⁻⁵ → 1.8×10⁻⁵ | ~859 s → 368 s |
  | Vanilla CFR | ~7.6×10⁻³ → 3.6×10⁻³ | ~747 s → 327 s |
  | External sampling | ~1.17 → 0.44 | ~7 s → 1.3 s |
  | Outcome sampling | ~3.08 → 1.65 | ~5 s → 0.7 s |

  The conclusion "4–5 orders" became "2–3 orders vs vanilla, 4–5 vs CFR+".
- **Crossover** (summary Tables 5–6 and text, both one-pagers) — 2.1M / 4.8M → 1.1M / 2.4M nodes;
  210× / 466× → 105× / 233×.
- **Table 4** —
  - external: "10.2× slower" → "10.2× (≈105× more time)";
  - outcome: "15.3× slower" → "15.3× (≈233× more time)";
  - CFR+ row: 0.34 / ~0.002 / ~38× faster → – / – / "not C/√T".

  One-pagers: "10.2x/15.3x slower" → "10.2x/15.3x less accurate at equal time, ~105x/~233x longer".
- **Table 6** —
  - limit hold'em: ~10¹⁴ and 10⁷× → ~3×10¹⁷ and ~10¹¹× ("yet solved by full-traversal CFR+");
  - no-limit: ~10¹⁷ and 10¹⁰× → up to ~6×10¹⁶⁴.
- **§ 3.5** — "1,000 vs ~1,000,000 iterations" → "2.0×10⁻⁴ after ~1,100; ~2M for vanilla (extrapolated)".
- **§ 3.7 / § 3.9 rates** — "all O(1/√T)" → slopes −0.4…−0.5 (MCCFR), −0.8 (vanilla), −1.8 (CFR+);
  ε√T 0.94 → 0.27.
- **§ 3.7, one-pagers, report § 5** — "multiple orders of magnitude" → "12–23× behind vanilla, 3–4 orders
  behind CFR+".
- **One-pagers** — "three localised changes" → "two"; limit hold'em ~1e14 → ~3e17 states.
- **§ 3.1** — "58 terminal nodes" → "58 nodes (30 terminal)"; BG "в пъти" → "стотици до хиляди пъти".

## Figures (file — what changed — printed size now)
All six figures print at 17.6 cm from 2110 px (7.03 in at 300 dpi), a scale of 0.985. Ticks and legend
(fs 10) print at ≈ 9.9 pt and axis labels (fs 11) at ≈ 10.8 pt; effective resolution ≈ 305 ppi. Before, the
figures printed at 4.9–6.4 pt. BG twins came from `render_bg_figures.py` with the overlay, and `summaryBg.md`
and `report_bg.md` now point at the `_bg` files.

| # | Figure | Script | What changed |
|---|---|---|---|
| 1 | `leduc_exploitability_iterations` | `exploration/leduc_comparison.py` | Seeded rerun; exploitability; ends at 5,000; figsize (14,7)/dpi 150 → (8,5)/300; title dropped; legend below |
| 2 | `leduc_exploitability_time` | same script | As fig. 1, plus the x axis is training time |
| 3–4 | `kuhn_exploitability_iterations`, `kuhn_exploitability_time` | `exploration/implDayOne1_test.py` | As figs. 1–2, plus the custom-CFR curve is now a real exploitability (G04) |
| 5–6 | `exploitability_vs_iterations`, `exploitability_vs_wallclock` | `cfr/train_all_timed.py --plot-only` | No rerun; (11,6)/150 → (8,5)/300; title dropped; legend is names only, below the axes; "final exploit 0.0000" is gone |

Printed crops are in `deliverables/finalReview/renders_fix/step03/ch03/`. All six were checked and are
legible, with no overlaps.

## Remaining overflow / legibility warnings
- None. The renderer reported no overflow (these are plots, with no boxes), and the tick labels are mathtext
  powers of ten, so there is no decimal point.
- The BG one-pager fits on one page at the 8.5pt/1.2cm rung, the second-tightest. The EN one-pager fits at
  10pt/1.5cm.
- Table 4 (BG) still wraps its first column to 2 lines, down from 3–4.

## Verification (build ok? check_headings / check_captions output for this step)
- `build_reports.py --step step03 --type all`: all 6 PDFs built. The summaries run to 15 pages (EN) and
  16 pages (BG); the one-pagers are 1 page each.
- `check_headings.py`: 44 PDFs checked, 0 missing headings (none for step 03).
- `check_captions.py`: 24 PDFs checked, 0 with unaccounted figures.
- Cyrillic inside `\text{}` (пресичане, Ледюк, скорост, раздаване, итер) renders correctly (B01 check).
- The seeded runs are reproducible: the OpenSpiel CFR and CFR+ values at 3,829 equal the 1 Jul caches
  (NashConv 5.35×10⁻⁵, 7.57×10⁻³, and on Kuhn 4.17×10⁻⁴, 6.09×10⁻⁵).
