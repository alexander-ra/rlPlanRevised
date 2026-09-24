# Chapter 14 — Implementation: a joint evaluation protocol for adaptive agents

Phase 4 of step 14 (raw plan `planning/rawSteps/step_14_evaluation_frameworks.md`, Phase 4,
L318–781). **Everything here was run**; numbers come from the files in `results/` and the log in
`../EXECUTION_NOTES.md`. The plan's three-layer framework (exploitability, population ranking,
statistical confidence) is built and validated first; on top of it sits the part this chapter
adds for the C3 gap (`deliverables/finalReview/lit_gaps.md`): a protocol that reports, together
and with confidence, the **gain** against a sub-optimal population, the **speed** of adaptation
and **recovery** after an opponent switch, and the **exposure** (two-player worst case; N-player
coalition value), unchanged across Kuhn, Leduc and three-player Kuhn.

## Module map

| Module | Role | Plan |
|---|---|---|
| `deps.py` | read-only access to Chapters 7, 8, 10, 11, 12 (appended to `sys.path`; clashing names loaded by path) | §6 workflow |
| `trees.py` | one exact array representation of an OpenSpiel game (any number of players): info sets, sequences, exact values, best responses, NashConv, node values, sampling | Day 1 exploitability module |
| `solvers.py` | CFR / CFR+ / MCCFR blueprints (OpenSpiel C++); the one-shot sequence-form dual LP for maxmin, RNR(p) and floor (best equilibrium) | L336–400 |
| `bridge07.py` | maps our trees to Chapter 7's engines, policies and hands (verified to 1e-14) | Day 2 zoo |
| `agents.py` | stationary, switching, teaching-attack, Chapter 7×8 adaptive agents, black-box MC learner | Day 2 zoo |
| `zoo.py` | the Kuhn (16) and Leduc (12) zoos, incl. Chapter 12's LLM-extracted Kuhn strategies | Day 2 zoo |
| `simulate.py` | two-player match runner: fixed seats, duplicate cards, four per-hand estimators | Day 5 |
| `aivat.py` | AIVAT (Burch et al. 2018) tabulated per terminal: exact mean/variance | Day 4 |
| `population.py` | Elo (ML fit), Nash averaging (max-entropy), meta-Nash, α-Rank (single + multi-population), maximal lotteries / IML (VasE), Hodge spinning top (Chapter 10) | Days 2–3 |
| `nplayer.py` | three-player types, batched best response, exact coalition value, the adaptive DirBR3P agent, coalition teacher | Day 6 |
| `tasks.py` | one match as a picklable task (multiprocessing) | — |
| `run_validation.py` | E0: every component vs its reference (OpenSpiel, Chapters 3/7/8/10) | Validation L776–781 |
| `run_population.py` | E1: round-robins, rankings, clone test, horizon, bootstrap | Day 5 |
| `run_adaptation.py` | E2: the joint protocol (gain, speed, recovery, exposure, teaching attack, estimator comparison) | [P4*] |
| `run_approx_br.py` | E3: learned best response vs exact; black-box learner vs white-box attack | Paper 1 |
| `run_nplayer.py` | E4: three-player Kuhn equilibria, tensor, protocol, colluders | Day 6 |
| `run_sls.py` | E5: Layer 2 + coalition probe on Chapter 11's So Long Sucker | Day 6 |
| `run_bridge13.py` | E6 (optional): confidence on Chapter 13's parsed Pluribus hands | Day 5 bridge |
| `run_crossgame.py` | E7: cross-game table and failure-mode summary (derived only) | Day 6 table |
| `plot_figures.py` | all data figures, from the JSON only → `deliverables/reports/step14/figures/` | — |

## How to run (from this folder, repo `.venv` active)

```bash
python run_validation.py                                   # 14 s  -> results/validation.json
python run_population.py --games kuhn leduc --seeds 10     # ~4 min -> results/population_*.json
python run_adaptation.py --games kuhn leduc --seeds 10     # ~3 min -> results/adaptation_*.json
python run_approx_br.py --seeds 3 --max-hands 100000       # ~1 min -> results/approx_br_*.json
python run_nplayer.py --seeds 5 --pop-seeds 3              # ~1.5 min -> results/nplayer_kuhn3.json
python run_sls.py --games 2000 --seeds 3                   # 35 s  -> results/sls.json
python run_bridge13.py                                     # needs D:/datasets/step13_cache
python run_crossgame.py                                    # derived -> results/crossgame.json
python plot_figures.py                                     # figures from the JSON only
```

Needs numpy, scipy, OpenSpiel, cvxpy + ecos (Nash averaging; OpenSpiel's cross-checks),
matplotlib. 14 worker processes by default (`--workers`). No GPU is used.

## Conventions

- **NashConv** = Σ_p (best-response value − value); **exploitability** = NashConv / n
  (OpenSpiel). For one two-player agent (σ₀, σ₁) its exploitability equals the mean over seats
  of how far a best responder pushes it below the game value.
- **Exposure** of the policy in force for seat s: v*_s − min_y u_s(σ, y) ≥ 0 (chips/hand).
- **Gain**: policy-exact expected payoff minus the Nash blueprint's exact payoff against the same
  opponent in the same seat. **Capture**: gain ÷ (best-response value − blueprint value).
- **h50 / r50**: first hand at which the capture is ≥ 0.5 *and* its mean over the next 100 hands
  is ≥ 0.5 (after the switch hand for r50). Resolution = the refit period (50 hands).
- **Estimators**: raw chips; AIVAT with chance + the tested agent known and blueprint self-play
  values as the value function; policy-exact EV (both policies known — simulation only).

## Validation targets (plan L776–781) — outcome

| Target | Outcome |
|---|---|
| Kuhn exploitability matches Chapters 3/8 to 4 d.p. | matches Chapter 3 (Leduc) and Chapters 7/8 (Kuhn) to ≥ 6 d.p.; OpenSpiel exactly |
| Leduc approximate within 10 % of exact | only at 10⁵ hands and for 4 of 6 targets (Rock 71 %, Maniac 84 %) |
| α-Rank: RPS uniform, transitive concentrated, matches OpenSpiel | yes; max |diff| 5e-14 |
| VasE: RPS uniform, transitive concentrated | yes; matches OpenSpiel's maximal lotteries |
| AIVAT ≥ 5× Kuhn, ≥ 10× Leduc, unbiased | unbiased exactly; Kuhn 18/20 pairs ≥ 5×; Leduc 7/12 pairs ≥ 10× (median 12.2) |
| Report < 5 min Kuhn, < 30 min Leduc | Kuhn ~1.5 min, Leduc ~6 min (14 processes) |

## Likely to break

- `nash_average` on near-tied agents: see EXECUTION_NOTES (fixed tolerance + support LPs).
- `run_bridge13.py` depends on another chapter's cache outside the repo; it skips cleanly.
- The coalition value enumerates 2¹⁶ pure strategies — exact for three-player Kuhn only.

## Key takeaways for the final summary

- One exact engine reproduces OpenSpiel's NashConv, Chapter 3's exploitability and Chapter 7/8's
  best responses; the sequence-form dual LP solves full-Leduc safe exploitation in 0.02–0.04 s
  where Chapter 8's constraint-generation loop did not converge within its caps.
- The joint protocol separates agents that every single ranking conflates: on Leduc RNR(0.5)
  gains +0.80 chips/hand at exposure 0.26, DirBR +0.99 at exposure 2.46, BestEq +0.05 at 0.
- Existing evaluation breaks where predicted: exploitability ranks the zero-gain BestEq first,
  Elo and the RRPS score rank DirBR near the top, Nash averaging gives exploiters zero mass, and
  α-Rank's winner changes three times as α goes from 0.01 to 100.
- With three players, equilibrium components lose 0.06–0.17 chips/hand more to a coordinated pair
  than they earn in equilibrium; the adaptive DirBR3P that tops population return, Elo and Nash averaging loses 0.47 chips/hand to a
  coalition teaching attack.
