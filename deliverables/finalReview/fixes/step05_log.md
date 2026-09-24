# Step 05 — fixes applied
Applied: 64 · Skipped: 1 (partial: part of B11) · Central: 16

Counted per finding id (74 in the review: G 9 · B 27 · T 10 · C 13 · S 11 · X 4). All 64 non-T
findings were applied. B11 was applied only in part, so it is counted in both "Applied" and
"Skipped". The 10 T findings are glossary-file changes, so they are central; their occurrences in
this chapter were fixed through the B findings. Every quote matched exactly: 71 replacements in
`summaryEn.md`, 123 in `summaryBg.md`, 9 in `onePager.md`, 18 + 3 in `onePagerBg.md`. The scripts
asserted one match per quote.

**R5 (caveat), as decided in TRIAGE § B.** Nothing was rerun.
- The advantage losses are now reported as rising (C01).
- ~1.69 is reported as the frozen value, with a uniform random policy at 2.37 (C02).
- The patched 64×64 run (1.700–1.706 at every checkpoint, the same as the unpatched solver) is
  **dropped** from the text and from both result figures. One caveat sentence explains why, in
  § 5.2.5 and § 5.2.4 and in the one-pager's bug bullet.
- The one-pager's total-variation probe also comes from a 64×64 run at 1.70, so it is now marked
  provisional.

**Post-2020 work (S09 / C07).**
- One paragraph in § 5.4.4 replaces the out-of-date "no pressure toward unexploitability" claim.
  It covers NeuRD, R-NaD/DeepNash, MMD and Rudolph et al. (ICLR 2026, scoped to five two-player
  zero-sum games).
- One sentence on ESCHER follows DREAM in § 5.3.2.
- Only citations the review verified are used.

**Glossary ✅ rows applied beyond the review's list:**
- 2.34: "плъзгаща средна/оценка/статистики" → "текуща …".
- 2.8: "безпристрастна" → "неизместена".
- 2.2: "извън политиката" → "извън текущата стратегия (off-policy)".
- 2.10: "разминава/разминаването" → "отдалечават се / разходимост".
- 2.6: "сходяват / сходи / се сближава към" → "клонят към / достигне сходимост".
- 1.24: PBS.
- 2.16: "изчислителна мощност".
- 2.31: "персонализиран двигател".
- 2.1: "политика" in the one-pager.
- 1.2: "n-играчен".
- 3.13: "четене".
- Rows 1.10, 2.3 ("самообучение" left as is, including in new text) and 2.5 were not touched.

**Extras (not in the review, same kind of defect):**
- EN "the previous chapter's *hidden state*" → "the previous step's" (left over from the step→chapter
  rename).
- One-pagers: "the step's" → "the chapter's" (2× EN and 2× BG).
- BG § 5.2.2 heading: "многослоен перцептрон" → "MLP".
- BG § 5.2.1 heading: capital letter after the colon.
- BG AlphaStar sentence: gerund grammar rewritten while adding its citation.
- The second "ръка карти" → "картите в ръката".
- The BG stub comment "Step 1/3/4/6" → "Chapter".

## Skipped (id — reason)
- **B11 (partial)** — the three "bootstrap" items ("**целевите стойности по метода „bootstrap“**"
  2×, "целта с бутстрапиране") are left alone because glossary row 2.5 (bootstrapping) is still
  open. The "attention" item was applied.

## Central (id — what is needed)
- **T01** — glossary: permutation-equivariant → "еквивариантен спрямо пермутации";
  permutation-invariant → "инвариантен спрямо пермутации" (row 2.27).
- **T02** — time-average → "средно по времето" (row 2.13).
- **T03** — self-play is row 2.3, which the candidate has not decided. Because of that, this chapter
  still prints "самообучение" (§ 5.4.4 heading, Table 8, § 5.3.1, § 5.1.3, § 5.3.3 and the new
  C07 text).
- **T04** — convolution → "конволюция" (row 2.26).
- **T05** — anticipatory parameter → "антиципиращ параметър". This row is not in
  GLOSSARY_DECISIONS; the text uses it already.
- **T06** — overfitting/underfitting (row 2.25).
- **T07** — grid → "решетка" (row 2.28).
- **T08** — bootstrapping is row 2.5 (open); the counterfactual pair is row 1.11; off-policy is
  row 2.2.
- **T09** — bias vector (row 2.9).
- **T10** — sample efficiency (row 2.14) and wall-clock (row 2.15).
- **Shared label keys changed by `labels_step05.json`.** These affect other chapters' figures when
  merged:
  - 'MLP' → 'MLP' (removes the glossary expansion "многослоен перцептрон"; rule: abbreviations
    stay Latin).
  - 'Exploitability' → 'Експлоатируемост' (capitalised axis label).
  - 'Tabular MCCFR' → 'Табличен MCCFR'.
  - Now-unused step-05 keys can be pruned from `figure_labels.json`: "(64,64) baseline",
    "Convergence in …", "Wall-clock seconds", "Exploitability (log)", "Outer iterations (log)",
    "Tabular MCCFR (iterations)", "Leduc Hold'em …", the old long titles of `make_arch_figure.py`,
    "Hourglass (bottleneck)", "Funnel (tapering)" and "General pattern …/Example …" with "->".
- **Renderer (`render_bg_figures.py`).**
  - `fit_label` measures the box when `box()` is called. A script that calls `tight_layout()`
    afterwards gets narrower fit-time boxes than it prints, so the renderer reports false
    overflows and shrinks labels. This chapter fixes its axes position up front. Other chapters'
    diagrams may have the same problem.
  - Printing a warning with "×" crashes on a cp1251 console. Run it with `PYTHONIOENCODING=utf-8`.
- **Plotting-script list.**
  - `implementation/step05/exploration/day01_deep_cfr.py` no longer contains `savefig`: its plot
    functions moved to the new `plot_from_logs.py`, which it imports. `plotting_scripts()` now
    picks up `plot_from_logs.py`, which only reads the logs, instead of the training script, which
    would retrain for 5–15 min and overwrite `logs/day01_results.json` during a central BG
    render.
  - `day02_nfsp.py` stays in `SKIP`; its Leduc figure is now drawn by `plot_from_logs.py`.
  - `check_coverage.py`'s `BY_DECISION` can drop `day02_nfsp_leduc.png`, which now has a BG twin.
    `deepcfr.png` stays English because it is reproduced from a paper.
- **Float policy.** X04's fallback ("let fig. 17 float") is impossible: `float_layout.tex` pins
  all figures to `H`. It was solved by size instead (see Figures).
- **`SOURCE_GAPS.md`, step 05.** Rows 1–5 are now cited or softened (S01–S05). Row 6 is gone
  with the stubs (S06).
- **`implementation/step05/exploration/findings.md`.** This is not a deliverable and not
  plotting code, so it was not edited, but it still:
  - says "the original paper … uses 400+ iterations";
  - lists "file a fix upstream" (fixed upstream in OpenSpiel 1.6.13, C13);
  - holds the only record of the CFR+ run (0.00123 / 92 s), which the one-pager now cites
    (C12.3).
- **Typography § 5.1–5.2.** Not applied: dashes, decimal comma, "50,000", "×" in text. New text
  follows the surrounding style.

## Numbers changed (old → new, where)
- **Summary § "Why Neural Networks" (EN/BG):** Deep CFR "reached only 1.70" → "stayed above 1.1 at
  every network size tried".
- **§ 5.1.2:**
  - Leduc tensor "about thirty numbers (card, history, pot)" → "30 numbers (player to act,
    private card, public card, betting history)".
  - The capacity explanation (overfitting) → a hypothesis (C04).
- **§ 5.2.3:** "the pot a single scalar … used in Chapters 3–4" → "OpenSpiel's 30-dim vector; the
  pot is not a separate input".
- **§ 5.2.4:**
  - "lower than networks two and four times wider" → "1.14 vs 1.49 (128×128×128)".
  - 64×64 (1.70) excluded pending a rerun.
  - "the ranking would reverse" → "would likely reverse".
- **§ 5.2.5:**
  - "frozen at the random-strategy level" → "frozen near 1.69 (uniform random 2.37)".
  - New sentence: the patched 64×64 run still sits at 1.70.
  - "a loss that falls steadily" → "a loss that keeps moving".
- **§ 5.3.2:**
  - "advantage losses fell" → "moved (and grew, iteration-weighted targets)".
  - "near 1.70" → "above 1.1 at every size (1.14 at best)".
  - "several times more iterations" → "a far larger sampling budget (40 vs 1,500 traversals per
    iteration)".
- **§ 5.3.3:** NFSP "around 2.5" + "near the uniform-random level of 2.37".
- **One-pager (EN/BG):**
  - Deep CFR **1.49–1.70** (~95 s) → **1.14–1.49** at (32,32) and (128,128,128) (87–101 s).
  - CFR+ **~1,400×** → **~900×** better than the best Deep CFR run (1.1441 / 0.00123 = 930).
  - "(64,64) **1.7002**" removed from the network-size bullet.
  - "random-strategy level (~1.69)" → "~1.69 (uniform random 2.37)".
  - "paper uses 400+" → "only 40 traversals per iteration (Steinberger 2019: 1,500)".
  - Added the upstream fix (OpenSpiel 1.6.13, Mar 2026).
  - TV-distance probe marked provisional (64×64 at 1.70).
  - CFR+ source given as `findings.md`.
  - "day0{1.2}" → "day0{1,2}".
- **Figures:** the 64×64 curve is removed from the network-size and vs-MCCFR plots. The vs-MCCFR
  plot now shows 32×32 and 128×128×128, plus a uniform-random line.

## Figures (file — what changed — printed size now)
Numbers are per-chapter PDF numbers; the bundle numbers are 17–23. Printed type sizes are measured
from `renders_fix/step05/manifest.json`.

- **Fig. 1 `arch_comparison(_bg).png`** — `make_arch_figure.py`:
  - figsize (11, 8.2) → (6.9, 5.0), ylim trimmed, dpi 300.
  - Titles 10.5 → 10, notes and t-labels 8.5 → 10.
  - Shorter EN/BG titles; BG "Конволюция" (not "Сгъвка").
  - Text: the colour-legend sentence now matches the figure (G02).
  - Width 66% → 90%, so it fits under its paragraph without leaving half a page blank (X04).
  - Prints at 15.8 cm, text ≈ 9.5 pt, 315 ppi.
- **Fig. 2 `arch_hybrid(_bg).png`** — `make_hybrid_figure.py`:
  - Rewritten at print size (6.9 × 5.4 in, dpi 300), text 9 → 10.
  - Boxes widened; boxes now go through a new `summary/_diagram_utils.py` so the BG renderer
    re-wraps them.
  - Axes fixed before drawing, so the fitter sees the printed geometry.
  - "->" → "→"; shorter titles; all English removed from the BG version; one name per component
    (глава / ствол / ядро).
  - Width 58% → 94%.
  - Prints at 16.5 cm, text ≈ 9.2 pt (≥ 8.3 pt for any re-fitted label), 324 ppi.
- **Fig. 3 `day01_network_sizes(_bg).png`** — new `implementation/step05/exploration/plot_from_logs.py`,
  which reads the logs and does not retrain:
  - Linear axis, legend "32×32"/"128×128×128", no title, 4.3 × 2.9 in, fs 10, dpi 300.
  - 64×64 dropped (R5). The BG twin is new; `summaryBg.md` now links `_bg`.
  - Prints at 10.9 cm, 10 pt, 300 ppi.
- **Fig. 4 `arch_shapes(_bg).png`** — `make_shapes_figure.py`:
  - figsize (12.5, 3) → (6.9, 1.9), dpi 300.
  - Titles 10; "Hourglass\n(bottleneck)"; BG "Равномерна / Фуния / Пясъчен часовник (стеснение) /
    Яка".
  - Width 82% → 100%.
  - Prints at 17.6 cm, ≈ 10.2 pt, 295 ppi.
- **Fig. 5 `../deepcfr.png`** — the soft screenshot of both panels is replaced by panel (a) only,
  rendered from the vector arXiv PDF (1901.07621v4, p. 6) at 450 dpi:
  - Width 88% → 50%.
  - Caption corrected: Leduc, mA/g, reproduced from Steinberger 2019 Fig. 1a. `[^sdcfr]` is cited
    in the paragraph above, not inside the caption, because LaTeX drops footnotes in captions.
  - Prints at 8.8 cm, ≈ 12 pt, 332 ppi.
  - Its axis text stays English (third-party figure).
- **Fig. 6 `day01_deep_cfr_vs_mccfr(_bg).png`** — `plot_from_logs.py`:
  - Single wall-clock panel (the mixed-unit iterations panel is dropped), linear axis.
  - Deep CFR 32×32 and 128×128×128, plus the uniform-random line (labelled in place); legend below
    the axes.
  - The BG twin is new; linked `_bg`.
  - Prints at 10.9 cm, 10 pt, 300 ppi.
- **Fig. 7 `day02_nfsp_leduc(_bg).png`** — `plot_from_logs.py`:
  - Linear axis; x in thousands of episodes; uniform-random reference line 2.374.
  - No code identifier in the title.
  - The BG twin is new; linked `_bg`.
  - Prints at 10.9 cm, 10 pt, 300 ppi.
- **All seven BG captions** replaced with Bulgarian (G01). Figs. 3, 5, 6 and 7 were reworded for
  R5 and G06–G08.

## Remaining overflow / legibility warnings
- `render_bg_figures.py --only step05` with the overlay reports **no overflowing labels**.
- **Fig. 5 (SD-CFR)** keeps English axis labels ("Exploitability in mA/g", "Algorithm Iterations",
  "SD-CFR (ours)") because it is reproduced from the paper. The caption explains it. Before any
  reuse in Chapter I, check the arXiv licence (extract, "To verify").
- **Layout.** BG pp. 10 and 15 end about 30% short: the pinned `H` figures are 3 and 6, and they
  just miss the page. EN has no gap larger than 12%. The central typography pass will move these
  breaks again.

## Verification (build ok? check_headings / check_captions output for this step)
- `python scripts/build_reports.py --step step05 --type all`: all PDFs built.
  - `summaries/step05_en.pdf` 17 pp.; `step05_bg.pdf` 20 pp. There is no report for step 05.
  - One-pagers: EN 1 page (10 pt / 1.5 cm); **BG 1 page** (8 pt / 1.1 cm, the tightest setting). It
    first came out at 2 pages, so I shortened my own added BG wording without changing content.
- `python scripts/check_headings.py`: 44 PDFs, 0 missing headings. Step 05 is clean. The five "Част
  N" headings and the 13 stub headings are gone from the TOC.
- `python scripts/check_captions.py`: 24 PDFs, 0 with unaccounted figures. Step 05 EN and BG each
  have captions 1–7.
- `python scripts/figures/render_printed.py --pdf deliverables/summaries/step05_bg.pdf --out
  deliverables/finalReview/renders_fix/step05`: 7 crops, all read and legible.
- The logs were checksummed before and after every plotting run and are unchanged:
  `day01_results.json` 8abaef14…, `day02_results.json` 3b676394….
