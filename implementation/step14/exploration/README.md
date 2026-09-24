# Chapter 14 — Exploration (Phase 2)

Three small scripts, all run on 2026-09-25 (outputs in `figures/`). Run from this folder with the
repo `.venv` active; each takes seconds.

| Script | What it does | Output |
|---|---|---|
| `audit_prior_eval.py` | Day 1 audit: runs the evaluators of Chapters 3, 7, 8 and 10 on a common input and compares with this chapter's engine | `figures/audit.json` |
| `zoo_sanity.py` | Day 2: the plan's zoo sanity checks, exactly (no sampling) | `figures/zoo_sanity.json` |
| `toy_rankings.py` | intuition for failure mode 4: Elo, population return, Nash averaging, α-Rank and maximal lotteries on RPS, a ladder and an "exploiter" toy | `figures/toy_rankings.json` |

## Day 1 — audit of the evaluation code written so far

| Chapter | Evaluator | Status after the audit |
|---|---|---|
| 3 | `evaluate/exploitability.py` — NashConv/2 of a Leduc CFR node map | agrees with this chapter's engine (0.422144 both, 20 CFR iterations) |
| 7 | `best_response.nash_gap` — NashConv of a profile on Chapter 7's engines | agrees (Kuhn TightPassive self-play 0.483958 both) |
| 8 | `safety_checker.worst_case_value` | agrees (Kuhn seat-0 LooseAggressive −0.333333 both); its constraint-generation solvers are replaced by a one-shot dual LP (see implementation) |
| 10 | `spinning_top.transitive_ratio` (Hodge) and `elo.ratings_from_score_matrix` (online updates) | Hodge ratio reused unchanged; Elo re-implemented as a maximum-likelihood fit (the online version depends on update order; the A–C gap differs by 0.05 Elo points on a ladder) |
| 11 | help/harm matrices, win rates, EGTA pairwise projection | game-specific; the projection is re-stated in `run_sls.py` |
| 12 | LLM-extracted Kuhn strategies (`results/strategy_*_plain.json`) | used as zoo members |

**The common interface** the audit points to: every metric consumes either a behaviour profile
(exact metrics) or a record of hands with the policies in force (estimators). That is the split
between `trees.py` and `simulate.py`.

## Day 2 — zoo sanity checks (exact)

Prediction from the plan: *"Nash should be approximately unexploitable, random should lose to
everyone, always-fold should lose even more."*

What happened: the Nash blueprint's exploitability is 9.6e-6 (Kuhn) and 8.5e-5 (Leduc) — as
predicted. In Leduc, Random loses to every stationary agent. **In Kuhn it does not:** Random
beats AlwaysPass (the always-check/fold bot), whose population return (−0.517) is the lowest of
the zoo. Not a bug — AlwaysPass never bets and folds to every bet, so even uniform play takes its
antes. The lesson survives: the weakest agents are the most exploitable, but "random is the
floor" is not a law.

## How to read `toy_rankings.py`

On the **exploiter** toy (N ties with the strong and beats the weak slightly; E loses 0.05 to N
but beats the weak bots by 1.0), Elo puts E first (1700 vs 1588), Nash averaging and the maximal
lottery put all mass on N and give E a skill of −0.05, and α-Rank splits (0.48/0.49) at α = 0.1
but puts everything on N at α = 100. The bot zoo reproduces exactly this pattern at scale.

## Key takeaways for the final summary

- The prior chapters' evaluators all agree with one engine; the only real re-implementation is
  Chapter 8's safe-exploitation solver (dual LP) and Chapter 10's Elo (ML fit).
- "Random loses to everyone" is false in Kuhn (it beats AlwaysPass); the plan's sanity check is
  kept as a prediction with this correction.
- A four-agent toy already shows the ranking conflict the chapter measures on the full zoo.
