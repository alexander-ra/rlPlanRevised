# Chapter 15 — Exploration: mapping, and one solver check

The plan's exploration phase (raw step 15, Phase 2) is a mapping exercise, not an implementation:
build the three-column frontier map and try to *disprove* each gap.

## Activity 1 — the frontier map

Done as `../design/frontier_map.md` (nine sections, plus § 10: what the April 2026 map got
wrong). Every "what exists" entry carries its source; every feasibility claim names a result file.

## Activity 2 — gap validation log

The full validation was done on 2026-09-24 (`deliverables/finalReview/lit_gaps.md`: arXiv,
NeurIPS/ICML/ICLR/AAAI/IJCAI/AAMAS proceedings, forward searches from OX-Search, equal share and
VasE; verdicts C1 narrowed, C2 open at the core, C3 narrowed). This chapter adds one finding from
reading Ganzfried & Sandholm (2015) in full:

| Gap | New evidence | Effect |
|---|---|---|
| C2 | G&S § 2.3: the method "applies straightforwardly" to multiplayer games with the maximin value in place of the minimax value | not a counter-example (stated, not evaluated; no coalition-aware floor, no test against colluders), but prior art for the maximin-floor construction: C2 must cite it and claim only the implementation with a coordinated-pair floor, the exact checks and the collusion tests |

Limitations are those of lit_gaps.md (OpenReview behind a bot check; no Scholar crawl; 2026 items
are preprints unless a venue is stated). Verdicts read "no counter-example found".

## One runnable check — `lp_ties.py`

| Script | What it does | Runtime |
|---|---|---|
| `lp_ties.py` | shows which equilibrium the best-equilibrium LP returns when the model makes all equilibria equally good, and what that choice costs against G&S's "sophisticated" opponents | ≈ 20 s |

**How to play with it.** Change the opponent class in `opponent_profile(ctx, "sophisticated", i)`
to `"random"`: ties matter much less against far-from-equilibrium opponents, because the model
then breaks them itself.

**What to watch out for.** The LP is not wrong — every returned strategy is an equilibrium; the
issue is *which* one. A degenerate equilibrium (never bluff, never bet the best hand) is optimal
against an equilibrium model and poor against a slightly different real opponent.

**How to read the result** (observed, 2026-09-25): HiGHS returns the equilibrium that never
bluffs the Jack and checks the King (P(bet) = 0 at "0" and "2"); the tie-broken solution is the
blueprint itself. Against 300 sophisticated opponents: blueprint −0.019, HiGHS vertex −0.034,
best equilibrium with the true model −0.011 (numbers from the check in `EXECUTION_NOTES.md`).

## Key takeaways for the final summary

- The September gap check stands; G&S § 2.3 is added to C2's prior art.
- LP tie-breaking decides which equilibrium a "best equilibrium" agent plays when the model is
  uninformative; break ties toward the blueprint.
