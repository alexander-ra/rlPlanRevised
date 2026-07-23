# Step 09 — Execution Notes (dev log)

**What this is.** Step 09's code was authored but never run ("every number is a prediction to
verify"). This file records the actual execution: measured-vs-predicted, bugs + minimal fixes,
and observations. **Consolidation (Phase 5) is deliberately left to another agent** — this is raw
dev observation, not the write-up.

Run env: repo `.venv` (Python 3.12.10); numpy 2.4.6, torch 2.11.0+cu128, scipy 1.18.0,
matplotlib 3.11.0, OpenSpiel (`pyspiel`) present. **PettingZoo installed this session** (see
below). Scripts run from their own phase folder per the sys.path-shim contract. Date: 2026-07-23.

Status: **Phase 2 (Exploration) executed. Paused for review before Phase 4 (Implementation).**

---

## Environment / dependency install (this session)

- Installed **`pettingzoo` 1.26.1** + **`supersuit` 3.11.0**. Confirmed the MPE risk the plan
  flagged: **PettingZoo 1.26 no longer ships MPE** (the `mpe` extra doesn't exist; env families
  are atari/butterfly/classic/magent/sisl). MPE moved to the separate Farama package **`mpe2`**,
  which I installed (**`mpe2` 1.1.0**) to get `simple_spread`/`simple_adversary`.
- **Action item for Phase 4:** `compare_pettingzoo.py` imports `from pettingzoo.mpe import
  simple_spread_v3` (the old path). That import will fail on 1.26; it needs `from mpe2 import
  simple_spread_v3`. Minor, but the guarded cross-check won't run until that line is updated.

---

## Phase 2 — Exploration: 5 authored scripts (all pass; predictions hold)

| script | measured | vs prediction |
|---|---|---|
| `matrix_games_playground` | PD→P(C)=0.003 (defect, payoff 1.0); Matching Pennies→**not converged** (orbit); Stag Hunt→(Hare,Hare) risk-dominant (payoff 3.0); BoS→(Football,Football) (0.996/1.991) | ✅ matches (Stag Hunt/BoS reach *a* pure NE per init) |
| `nonstationarity_demo` | MP window-distance from Nash 0.301→0.476; PD distance→0.003 | ✅ MP non-converging, PD converges. **Nuance:** the MP radius slightly **grows** (spirals out) rather than staying exactly constant — discrete Euler updates on the saddle are not perfectly energy-preserving. Still non-convergent (the point). |
| `selfplay_vs_nash` (Kuhn, reuses Step 07) | avg-iterate NashConv 0.24→**0.031** over 200 iters; last-iterate stays **0.33–0.83** oscillating | ✅ exactly the averaging lesson |
| `psro_peek` (RPS) | population→{R,P,S}; mixture→(0.335,0.336,0.329); exploitability 2.0→**0.017** | ✅ →(⅓,⅓,⅓), exploitability→~0 |
| `lola_ipd_playground` | naive (1.07, 1.06); LOLA **(2.67, 2.93)** *(after fix)* | ✅ after fix (see below); before fix it missed |

Artifacts written: `exploration/figures/` — 5 JSON + 5 PNG (`matrix_games_playground`,
`nonstationarity_demo`, `selfplay_vs_nash`, `psro_peek`, `lola_ipd_playground`).

### Bug/fix — `lola_ipd_playground.py`: default look-ahead too small
At the authored default `lr_opp=1.0`, LOLA-vs-LOLA settled into an **asymmetric partial-
cooperation** fixed point — measured **(1.18, 2.40)**, not the predicted ~3-each mutual
cooperation (and the asymmetry direction flips by seed). **This is not a code bug:** the
`lr_opp=0`→naive guardrail reproduces the naive gradient exactly (1.066/1.062 both ways), and the
memory-1 IPD value + finite-difference look-ahead are structurally correct. The look-ahead step
was simply too small relative to this IPD's value scale to cross into the cooperative basin.
Probe (steps stable at 2000, so it's a fixed point not slow convergence):

```
lr_opp   0.3 → (1.02,1.02) defect   1.0 → (1.2,2.5) asym   3.0 → (2.6,3.0)   5.0 → (2.5-2.9 robust)   10 → (3.0,2.9)
```

**Minimal fix:** `CONFIG["lr_opp"] 1.0 → 5.0` (with an explanatory comment). At 5.0 both agents
land in **[2.44, 2.93] across 6 seeds** — near-symmetric, unambiguously cooperative vs naive ~1.0,
and `lr_opp=0` still degenerates to naive. Note the finite-difference demo plateaus at ~2.5–2.9,
i.e. *near*-cooperation, not exactly 3.0 (residual defection probability); the cleaner analytic
LOLA is `implementation/lola.py` (Phase 4).

---

## Phase 2 — Interactive familiarization (raw spec Day 1–2, scripted, no training)

Ran random rollouts to observe API/structure (the MAPPO-vs-IL and non-stationarity *results* are
covered by the authored scripts / Phase 4, so no heavy MARL-framework training here):

- **mpe2 `simple_spread`** (parallel API): 3 agents, obs `(18,)`, `Discrete(5)`; random rollout
  return **−16.6 each** — cooperation is terrible with random policies (the shared distance
  reward), the visceral motivation for CTDE.
- **mpe2 `simple_adversary`**: agents `[adversary_0, agent_0, agent_1]` — the mixed
  cooperative-competitive split.
- **PettingZoo classic `connect_four` / `tictactoe`** (AEC agent-cycle API): obs is a dict of
  `observation` + `action_mask`; turn-based, perfect-info — the contrast with the simultaneous
  MPE envs.
- **OpenSpiel `goofspiel(4)`**: 2 players, simultaneous-move nodes, provides info-state strings;
  random playthrough returns `[1.0, −1.0]` — the simultaneous joint-action "complexity explosion"
  the raw step points at.

(EPyMARL/MARLlib MAPPO-vs-IL training deliberately skipped — heavy external frameworks; that
comparison is done properly in the authored Phase-4 `tournament.py`.)

---

## Open items / carried to Phase 4
- Update `compare_pettingzoo.py` MPE import path (`pettingzoo.mpe` → `mpe2`) before that guarded
  cross-check can run.
- Everything else in Phase 4 is unrun; per the plan we **paused here for review** before the
  neural implementation phase (self-tests → `validate.py` → tournament smoke → scale).
- `consolidation/` intentionally not authored (left to another agent).
