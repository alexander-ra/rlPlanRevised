# Step 14 — Evaluation frameworks and exploitability metrics (Chapter 14)

Executed end to end on 2026-09-24/25 under `deliverables/finalReview/NEW_CHAPTER_BRIEF.md`.
Plan: `planning/rawSteps/step_14_evaluation_frameworks.md`. Gap wording: C3 in
`deliverables/finalReview/lit_gaps.md`; failure modes 1–9 in `lit_evaluation.md`.

**Aim.** Build the plan's three-layer framework (worst case, population ranking, confidence),
validate every component, and use it to test the open part of C3: a protocol that reports gain
against a sub-optimal population, speed of adaptation and recovery after a switch, and a worst
case (coalition-aware for N > 2), with confidence, unchanged across games — and to show where
existing evaluation breaks on adaptive, exploiting and N-player agents.

| Folder | Content |
|---|---|
| [`intuition/`](intuition/intuition.md) | the problem, approaches compared, timeline, misconceptions |
| [`exploration/`](exploration/README.md) | audit of prior evaluators, zoo sanity checks, toy rankings (run) |
| [`targetedReading/`](targetedReading/summary.md) | the five plan papers + RRPS, Nash averaging, spinning top; worked Math Flags |
| [`implementation/`](implementation/README.md) | the framework, the zoo, all experiments, results JSON, logs, figures script |
| [`EXECUTION_NOTES.md`](EXECUTION_NOTES.md) | running log: every run, seed, runtime, surprise |

Deliverables: `deliverables/reports/step14/` (`report_en.md`, `summary/summaryEn.md`,
`summary/onePager.md`, `figures/`, `summary/*.png` + `make_*.py`).

`consolidation/` is not produced (human-written phase).
