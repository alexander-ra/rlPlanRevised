# Step 13 — Behavioural Analysis Pipelines + Real-World Data

Deliverable chapter: **Chapter 13** (`deliverables/reports/step13/`). Executed end to end on
2026-09-24/25; see `EXECUTION_NOTES.md` for the full run log.

**Data substitute.** The plan assumes Playtech hand histories, which are not yet available. This
step uses public data instead: 2,032,655 no-limit hold'em hands played on the iPoker Network
(Playtech's own network in 2009) at $0.50/$1 blinds in July 2009, player IDs obfuscated, from the
MIT-licensed PHH dataset; and the 10,000 released hands of Pluribus against professionals as
ground truth for bot detection. It is 2009 data, not Playtech's current data; the Playtech dataset
remains the future validation.

| Folder | Phase | Content |
|---|---|---|
| `intuition/` | 1 | `intuition.md` — why real logs are different, approaches compared, pitfalls |
| `exploration/` | 2 | `explore_hands.py` + README — look at raw hands and their replay |
| `targetedReading/` | 3 | `summary.md` — verified sources, plan corrections, worked Bayesian math flag |
| `implementation/` | 4 | parser, validators, statistics, cloning, player2vec, clustering, collusion, bot detection; `results/`, `logs/`, `plots/` |
| `EXECUTION_NOTES.md` | — | every run, seed, runtime, result file, surprise and fix |

`consolidation/` is not produced (phase 5 is the candidate's).
