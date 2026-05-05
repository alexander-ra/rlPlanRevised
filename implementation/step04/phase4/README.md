# Phase 4 — Implementation directory

Phase 4 is the implementation pass for step 04 of the rlPlan. Six "days"
of work are committed here as self-contained increments:

| Day | Focus | Entry point |
|---|---|---|
| 1 | Lossless suit-isomorphic abstraction (rank-canonical engine) | `python day01_train.py` |
| 2 | Lossy card bucketing (HSD + EMD + k-means, recall sweep) | `python day02_train.py` |
| 3 | Action abstraction + translators (mini-NL Leduc) | `python day03_train.py` |
| 4 | Extended Leduc + combined abstraction (suits + buckets + actions) | `python day04_train.py` |
| 5 | Abstraction quality evaluation + Pareto frontier | `python day05_train.py` |
| 6 | OpenSpiel cross-validation + write-up | `python day06_openspiel_compare.py` |

## Conventions

- Each `dayXX_train.py` writes its results to `.dayXX_results.json` in
  this directory.
- Each `dayXX_*.py` module is keyed to one of §6.1–§6.4 (criterion /
  error budget / build-time pipeline / runtime patch) of the step-04
  deliverable. See `day06_summary.md` for the mapping.
- Foundation code (step03 algorithms, step04 exploration engines) is
  imported, never copied. The promoted modules are
  `leduc_full_engine.py` (a thin shim around step03), `leduc_rank_engine.py`,
  and `mini_nl_leduc.py` (rehomed from `exploration/`).
- All commands assume the repo root as the working directory and a
  Python 3.10+ environment with `numpy` and `matplotlib`.

## Where to look first

- `PHASE4_LOG.md` — day-by-day commit-style change log.
- `day06_summary.md` — the bridge into the deliverable §7 / §8 / §9.

## Status

All six days landed. The default smoke-test budgets have been executed,
result JSONs were generated, and the Pareto plot was rendered. Remaining
review notes are tabulated at the bottom of `day06_summary.md`.
