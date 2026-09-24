# Brief — executing a new step end to end (steps 13, 14, 15)

Steps 13–15 were planned but never executed. You execute **one step** completely: the
study phases, the implementation, **real experiments**, and the English chapter
deliverables, at the same standard and length as chapters 1–12 *after* the September 2026
final review. The candidate is asleep and has given full rights: you implement and run
everything yourself (the old 🔴 HAND-CODE tags and the "agent never runs anything" rule in
`implementation/WORKFLOW.md` are retired — ignore them). Work autonomously; when a choice is
genuinely open, pick the defensible option and record why.

## Read first

1. `planning/rawSteps/step_NN_*.md` — what to learn and build (source of truth for topics,
   papers, day structure, deliverables, validation targets). Its plan may contain errors the
   September review found; the files below win where they disagree.
2. `deliverables/finalReview/lit_gaps.md` and `lit_evaluation.md` — the verified state of the
   literature (Sept 2026). The gap wording in your chapter must match them.
3. `deliverables/finalReview/CHAPTER1_OUTLINE.md` — how the chapters feed Chapter I.
4. `deliverables/finalReview/TRIAGE.md` and one or two `stepNN_review.md` files — what the
   review found wrong in earlier chapters. **Do not repeat those mistakes** (list below).
5. Two finished chapters as models of structure and voice:
   `deliverables/reports/step11/summary/summaryEn.md`, `…/step08/summary/summaryEn.md`, and
   their `report_en.md` and `onePager.md`. Reuse their front matter (the HTML comment with the
   official title + YAML block), heading pattern, "Honest notes, limitations, and where this
   hands off" and "Key takeaways for the thesis synthesis" sections, footnote style.
6. `implementation/WORKFLOW.md` §3–§5 for the implementation folder layout (ignore its
   "don't run" rules).

## What you produce

**Implementation** — `implementation/stepNN/`:
`README.md`, `intuition/`, `exploration/`, `targetedReading/`, `implementation/` (code +
README + `results/` JSON + `logs/`), and `EXECUTION_NOTES.md` — a running log of every run
(command, seed, runtime, result file, what it showed, anything that surprised you and how it
was resolved). Update `EXECUTION_NOTES.md` as you go: if you are interrupted, the next agent
continues from it.

**Deliverables** — `deliverables/reports/stepNN/`:
- `summary/summaryEn.md` — the chapter, **4,000–5,500 words**, 6–10 figures.
- `report_en.md` — the experimental report, **2,500–4,500 words**.
- `summary/onePager.md` — ~600 words; must build to one page.
- `figures/` (report figures) and `summary/*.png` + `summary/make_*.py` (chapter figures;
  diagrams via a copy of `deliverables/reports/step11/summary/_diagram_utils.py`).

No Bulgarian yet — that is a later pass. Build the English PDFs:
`PYTHONIOENCODING=utf-8 python scripts/build_reports.py --step stepNN --lang en --type all`,
then `python scripts/check_headings.py` and `python scripts/check_captions.py`.

## Standards (from the September review — each was a real defect elsewhere)

- **Numbers:** every number in the text comes from a results file you name; seeds fixed and
  recorded; ≥ 3 seeds (report mean ± SE) for any claim about a difference; say "one run"
  when it is one run. Never let a plotting script retrain or overwrite results — plot from
  saved JSON.
- **Claims:** no "first", "proves", "state of the art", "always", "statistically
  indistinguishable" unless the evidence carries it. Toy-game results are toy-game results.
  When a result contradicts the plan's prediction, keep the prediction and add what happened
  and why (WORKFLOW §0.1) — suspect a bug first.
- **Sources:** cite only what you verified (WebSearch/WebFetch; say how in a comment or the
  log). Footnotes in the chapters' style: `[^key]: Author, A. (Year). "Title." *Venue*.`.
  Prefer primary papers. Use the verified entries in `lit_gaps.md`/`lit_evaluation.md` and the
  `stepNN_extract.md` files. Known corrections: OX-Search is Ge, Xu, Ding, Meng, An, Li & Gao
  (ICML 2024); equal share (Ge, Wang, Li & Jin, ICML 2025) is a target, provably not
  securable against heterogeneous opponents; piKL anchors to a human-imitation policy
  (Jacob et al. 2022; Bakhtin et al. 2023), not to Nash; spinning top = Czarnecki et al.
  2020, the decomposition = Balduzzi et al.; AIVAT = Burch, Schmid, Moravčík, Morrill &
  Bowling, AAAI 2018.
- **Figures:** text in figures must print at ≥ 8.2 pt: printed pt = fontsize × (printed
  width ÷ saved width in inches); at the usual 17.6 cm print width use fs ≥ 10; dpi ≥ 200;
  no overlapping labels; legends outside the data; label every axis; the caption says what
  the figure shows and nothing it doesn't. Keep labels short (they will be translated to
  Bulgarian, ~15 % longer). Look at every figure you make (Read the PNG) and at the printed
  PDF page (`python scripts/figures/render_printed.py --pdf deliverables/summaries/stepNN_en.pdf --out deliverables/finalReview/renders_new/stepNN`).
- **Naming:** chapters are "Chapter N" (never "Step N" in the deliverables). Chapters 1–15 all
  exist now. Metric names exact: say NashConv vs exploitability (OpenSpiel's exploitability =
  NashConv / n).
- **Gaps:** consistent with `lit_gaps.md` — C1 is narrowed (two-player real-time opponent
  modelling exists: GSCU, StratFormer, AlphaExploitem); C2 open at the core (no N-player
  exploitation with a checked loss bound); C3 narrowed (the repeated-RPS benchmark already
  scores return + exploitability for one game). Never "nobody adapts".

## Boundaries

- Edit only `implementation/stepNN/**`, `deliverables/reports/stepNN/**`, and your own
  scratch folder `…/scratchpad/stepNN/` (never the scratchpad root — other agents share it).
- Import prior steps' engines and utilities read-only; if one needs a fix, copy the module into
  your step and note it.
- Shared files (`scripts/**`, glossaries, `requirements.txt`, other steps) are not yours: list
  needed changes in `EXECUTION_NOTES.md` under "Central".
- You may `pip install` packages into `.venv`; list them under "Central" so they reach
  `requirements.txt`.
- Large data goes **outside the repo** (`D:/datasets/…`); never commit data. Do not commit at all.
- Keep any single experiment under ~60 minutes; the RTX 5090 (CUDA) is available.

## Final message

≤ 12 lines: what was built and run, the three most important results (with numbers and
their source files), what did not work, and anything the candidate should look at first.
