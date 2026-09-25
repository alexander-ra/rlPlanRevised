# Chapter 15 — Implementation: feasibility pilots for the contributions

Phase 4 of step 15 (raw plan `planning/rawSteps/step_15_research_frontier_mapping.md`, Phase 4) is a
design phase; its documents are in `../design/`. This folder holds the pilots that were **run** to
test the design's feasibility, as the brief requires. Numbers come from `results/*.json`; the log
is `../EXECUTION_NOTES.md`. Chapter 14's engine is imported read-only through `boot.py`.

## Module map

| Module | Role | Design item |
|---|---|---|
| `boot.py`, `log15.py` | read-only access to Chapter 14 (and through it Chapter 7); logger | — |
| `gifts.py` | Ganzfried & Sandholm's gift accounting on the exact trees: the opponent's best response constrained to the observed actions (Alg. 6) or to some consistent card (§ 8.2.2) | Exp. 2.0 |
| `safe_agents.py` | `GiftSafe`: RWYWE, BEFEWP, BEFFE, best equilibrium, best response; G&S's frequency model or Chapter 7's continuous model; `floor_tiebreak` (LP ties toward the blueprint) | Exp. 2.0 |
| `run_gs_table.py` | P0: replication of G&S (2015) Table I on Kuhn | validation |
| `run_protocol2p.py` | P1: RWYWE and G&S's baselines under Chapter 14's joint protocol (Kuhn, Leduc), with match-level safety S | Exp. 2.0 |
| `maximin3p.py` | the team-maxmin value of each three-player Kuhn seat (constraint generation + exact coalition oracle) | Exp. 2.1 |
| `bounded3p.py` | `Probe3` (exact baseline-relative loss and coalition value), `BoundedMix3P` (capped sequence-form mixture), `KLAnchor3P` (KL-anchored soft response) | Exp. 2.1 |
| `mmsafe3p.py` | `CoalitionOracle` (unique pure plans of the smaller opponent, ≈ 5 ms per call), `MMSafe3P` (G&S's method with the maximin floor: MM-RWYWE, MM-BestEq), `OracleProbe` | Exp. 2.1 |
| `run_bounded3p.py` | P2: all three-player agents against independent, fixed-colluding and adaptively colluding pairs | Exp. 2.1 |
| `plot_pilots.py` | every data figure, from the JSON only → `deliverables/reports/step15/figures/` | — |

## How to run (from this folder, repo `.venv` active)

```bash
python run_gs_table.py                      # P0, ~39 min on 14 cores -> results/gs_replication.json
python run_gs_table.py --no-tiebreak        # P0 without the LP tie-break (~14 min) -> gs_replication_notb.json
python run_protocol2p.py --game kuhn        # P1, ~3 min  -> results/protocol2p_kuhn.json
python run_protocol2p.py --game leduc --tol 0.01 --agents Nash BestEq "RNR(0.5)" DirBR RWYWE RWYWE-rev BEFEWP
                                            # P1, ~25 min -> results/protocol2p_leduc.json
python maximin3p.py                         # P2a, 7 s    -> results/maximin3p.json
python run_bounded3p.py                     # P2b, ~32 min -> results/bounded3p.json (needs maximin3p.json)
python plot_pilots.py                       # figures from the JSON only
python ../exploration/lp_ties.py            # the LP tie check (20 s)
```

## Conventions

- Chapter 14's definitions throughout: **gain** = expected payoff minus the Nash blueprint's
  against the same opponent in the same seat; **exposure** = v*_seat − worst case of the policy
  in force; **h50/r50**, **teaching loss** as in Chapter 14.
- **Match-level safety S** (new): mean over the match of (EV_t − reference), the reference being
  v*_seat for two players and the seat's team-maxmin value v_mm for three. Ganzfried & Sandholm's
  safety is E[S] ≥ 0.
- **Baseline-relative loss L(σ)**: max over the other two players' joint (coordinated) strategies
  of u_i(blueprint) − u_i(σ). Exact by enumeration in three-player Kuhn.
- **Coalition value**: min over the other two players' joint strategies of u_i(σ).
- Seeds: two-player decks = Chapter 14's (10,000 + seed, common across agents); three-player decks
  = Chapter 14's (20,000 + seed); action seeds from crc32 of the match description.

## Validation targets and outcomes

| Target | Outcome |
|---|---|
| RWYWE reproduces G&S Table I (ordering and magnitudes) | safety and orderings reproduced; safe levels 0.001–0.033 below G&S's; the best-response row not reproduced (0.328 vs 0.470; open) |
| Exposure of the policy in force ≤ k_t every hand (RWYWE family) | 0 violations in every match of P0 and P1 (`gift_diagnostics.exposure_above_k`) |
| Capped mixture: L(σ) ≤ ε for every policy in force | yes (max 0.010 / 0.029 / 0.095 / 0.285 for ε = 0.01 / 0.03 / 0.1 / 0.3) |
| Maximin-floor agents: S ≥ 0 in every match; coalition value ≥ floor | yes in all 135 matches per agent; floor undershoot ≤ 5e-7 |
| Chapter 14's BestEq / RNR(0.5) / DirBR gains reproduced in this harness | Kuhn: +0.020 / +0.210 / +0.273, identical to Chapter 14 |
| Fast coalition oracle equals Chapter 14's enumeration | equal to 1e-9 on 12 random strategies (`EXECUTION_NOTES`) |
| Maximin constraint generation converges | 14–23 cuts per seat, LP bound = oracle value |

## Likely to break

- LP ties: without `floor_tiebreak` HiGHS returns an arbitrary optimal vertex (see
  `../exploration/lp_ties.py`).
- The maximin-floor LP at k = 0 sits on a degenerate face; the oracle acceptance tolerance
  (`ACCEPT_TOL = 2e-6`) is needed or constraint generation never terminates.
- Everything three-player is exact only because one opponent has 6,561–10,000 unique pure plans;
  three-player Leduc needs a learned coalition exploiter (Experiment 2.1, scaling arm).

## Key takeaways for the final summary

See `../EXECUTION_NOTES.md` § Results and the chapter summary; the numbers are not repeated here.
