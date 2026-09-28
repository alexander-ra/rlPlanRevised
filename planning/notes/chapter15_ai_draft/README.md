# Chapter 15 — AI-written draft (reading notes only)

**Status: not authored by me, not reviewed. Read it, but do not cite, quote or build on it.**

This is the chapter 15 draft ("Research Frontier Mapping and Contribution Design") as it stood on
28 September 2026, written by AI assistants. I have not verified its reasoning, numbers or sources.
Chapter 15 will be written by hand after reconciliation with my supervisors. Until then this
folder is only something to think with.

The files keep the original "Alexander Andreev" byline in their front matter. That byline is
wrong for this draft.

## What was done when it was demoted

- Moved here from `deliverables/reports/step15/`. It is no longer built into any bundle.
- The chapter 8 and 14 passages that relied on it were removed, in every format and both
  languages. Chapter 8 again calls RWYWE future work. Chapter 14 dropped the BestEq tie-break
  note, which came from this draft's `lp_ties.py`.
- The study-plan preface still describes what chapter 15 is meant to be ("Integration",
  "a detailed Chapter I outline and publication pipeline"). That is the plan, not this draft.

## Contents

| Path | What it is |
|---|---|
| `report_en.md`, `report_bg.md` (+ `.pdf`) | the step report |
| `summary/summaryEn.md`, `summary/summaryBg.md` (+ `summary_{en,bg}.pdf`) | the full chapter summary |
| `summary/summaryShort{En,Bg}.md` | the condensed summary |
| `summary/onePager{,Bg}.md` (+ `onePager_{en,bg}.pdf`) | the one-pager |
| `figures/`, `summary/*.png`, `summary/make_*_figure.py` | figures and the scripts that drew them |

The experiments behind the draft (RWYWE pilots, the bounded three-player agent, `lp_ties.py`,
the C2/C3 design notes) are in `implementation/step15/`. They are also AI-written and just as
unverified.

## Other places that still lean on it

- `deliverables/finalReview/CHAPTER1_OUTLINE.md` cites `step15` results and
  `implementation/step15/design/publications.md`.
- `deliverables/finalReview/lit_gaps.md` corrects a claim in step 15 (piKL).
- `deliverables/finalReview/fixes/labels_step15.json` and `scripts/figures/out/figure_labels.json`
  point to the old `deliverables/reports/step15/` figure paths.
