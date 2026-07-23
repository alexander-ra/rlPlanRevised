# Step 09 — Execution Notes (dev log)

**What this is.** Step 09's code was authored but never run ("every number is a prediction to
verify"). This file records the actual execution: measured-vs-predicted, bugs + minimal fixes,
and observations. **Consolidation (Phase 5) is deliberately left to another agent** — this is raw
dev observation, not the write-up.

Run env: repo `.venv` (Python 3.12.10); numpy 2.4.6, torch 2.11.0+cu128, scipy 1.18.0,
matplotlib 3.11.0, OpenSpiel (`pyspiel`) present. **PettingZoo installed this session** (see
below). Scripts run from their own phase folder per the sys.path-shim contract. Date: 2026-07-23.

Status: **Phase 2 (Exploration) and Phase 4 (Implementation) executed.** `validate.py` = 8 PASS /
1 FAIL (the one red is a deliberately-preserved negative finding — see Phase 4).

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

## Open items / carried to Phase 4  (all actioned — see Phase 4 below)
- `consolidation/` intentionally not authored (left to another agent).

---

# Phase 4 — Implementation

Executed after the exploration checkpoint. `validate.py` ends **8 PASS / 1 FAIL**, where the one
red is a *deliberately preserved* negative finding (owner decision). All fixes are Step 09 code
only; Step 07 untouched.

## Module self-tests (all 7 exit 0)
`matrix_games` (all NEs, NashConv 0), `meta_nash` (RPS uniform, NashConv 0), `goofspiel`
(symmetric value 0; BR beats uniform 0.667/0.75), `coop_env` (CoopSignal reward + ceilings;
Climbing optimal 11/safe 5), `qmix` (monotone mixer → IGM True, non-monotone → False), `psro`
(Kuhn exploitability 0.92→0.14 in 6 rounds). `lola` self-test: guardrail `lr_opp=0`==naive matches
exactly; LOLA return **1.78** at the module's own default (a soft under-cooperation, same cause as
the exploration script — see below; the check only requires LOLA>naive, which holds).

## `validate.py` — 8 PASS / 1 FAIL

| check | result |
|---|---|
| matrix outcomes vs analytic Nash | PASS (PD→Defect; **MP time-avg NashConv 0.008** after the lr fix; Stag Hunt/BoS reach a pure NE all seeds) |
| PSRO Kuhn exploitability → 0 | PASS (→0.000 in 15 rounds) |
| PSRO Leduc decreases substantially | PASS *(reframed)* — 4.75→2.16 in 20 rounds (< 0.5·start) |
| PSRO Goofspiel decreases | PASS (1.33→0.00) |
| MADDPG central critic lower variance | PASS (0.0897 < 0.0927) |
| communication helps (CommNet ON vs OFF) | PASS *(after budget fix)* — **ON 1.000 vs OFF 0.269** |
| CTDE beats IL on climbing | **FAIL (kept red on purpose)** — MADDPG 5.00 vs IL 5.00; see finding |
| LOLA induces cooperation | PASS (guardrail ok; naive 1.06 vs LOLA 1.79 > naive) |
| OpenSpiel NashConv cross-check | PASS — **exact** (kuhn 0.916667, leduc 4.747222, \|Δ\| 0.000000) |

## Bugs/fixes (Phase 4)

1. **`validate.py` communication check — training budget too small.** The batch REINFORCE loop
   does *one* update per `batch_episodes`, so the authored `episodes=6000, batch_episodes=256`
   gave only **~24 gradient updates** → the channel never learned (comm ON stuck at the no-comm
   1/K ceiling 0.244 == OFF). Not a wiring bug (the listener does receive the speaker's g-dependent
   message; verified). **Fix:** `40000/32` (~1250 updates) → **ON 1.000 vs OFF 0.269**. Probe:
   ~24 upd→0.244, ~312→0.734, ~1250→1.000. Same fix applied to `config.py` `scale.coop`
   (`20000/32`).
2. **`validate.py` Matching-Pennies time-average — lr too large.** Under discrete gradient
   updates the MP orbit around (½,½) slowly spirals *outward* (energy-preserving only in
   continuous time), biasing the second-half time-average off-centre → NashConv 0.115 (> 0.1) at
   lr=0.1. **Fix:** MP sub-check lr `0.1 → 0.02` → NashConv **0.008** (x=[0.5,0.5]). The other
   games keep lr=0.1 (they converge fine); the last iterate still cycles (the lesson).
3. **`lola` under-cooperation (exploration + config).** Same look-ahead-magnitude issue found in
   Phase 2: `lr_opp=1.0` settles below full cooperation. Bumped `config.py` `lola.lr_opp 1.0→5.0`
   (both smoke/scale) for a clean tournament demonstration. (The `lola.py` module's own default
   still shows ~1.78 in its self-test; the validate check passes on LOLA>naive, so left as-is.)
4. **`compare_pettingzoo.py` MPE import.** PettingZoo 1.26 removed MPE (moved to `mpe2`). Added a
   fallback: try `pettingzoo.mpe` then `mpe2`. The reachability check now runs (simple_spread: 3
   agents, obs (18,), 5 actions, steppable).

## Two failures reframed/kept per owner decision (genuine limitations, not bugs)

- **PSRO on Leduc — `<0.5 in 20 iters` is unreachable → reframed to the true claim.** Exact
  double-oracle on the full Leduc tree converges *slowly and non-monotonically*: 4.75 → 2.16 @20
  rounds, and only ~1.0–1.3 by round 40 (trajectory bounces: 2.2→1.3→1.6→1.4→1.2→0.9→1.3). PSRO
  **Kuhn** by contrast hits 0.000 in 15, so the machinery is sound — Leduc is just big (many pure
  BRs), the same "exact methods are slow on Leduc" wall as Step 08. The check now asserts a
  **substantial decrease (< 0.5·start)**, which holds and matches the Goofspiel/`psro_peek`
  trend framing.
- **MADDPG on the climbing game — kept FAILING as an honest negative result.** The raw step
  predicts MADDPG→optimum 11 while IL stays trapped at 5. Empirically vanilla COMA/MADDPG **never
  reaches 11** (caps at 5–6 across entropy∈{0.02,0.1,0.3} and seeds 0–3) and even *underperforms*
  IL (which reaches 7) — the classic **relative-overgeneralization** trap that a centralized
  critic alone does not solve (the literature uses lenient/hysteretic learning). The CTDE wins
  this repo *does* demonstrate are the **lower critic variance** (passes) and the **communication
  channel** (passes). Left red rather than reframed, with an explanatory comment in `validate.py`.

## Optional cross-checks / plots
- `compare_openspiel.py`: NashConv(uniform) matches OpenSpiel **exactly** (kuhn/leduc |Δ|=0.000000).
- `compare_pettingzoo.py`: MPE `simple_spread` reachable & steppable (after the `mpe2` fix).
- `plotting.py --config smoke`: wrote `plots/psro_exploitability.png`, `plots/coop_ctde_comm.png`.

## Tournament
- **smoke** (`results/smoke_results.json`): PSRO Kuhn/matrix/goofspiel →0; LOLA cooperates>naive;
  critic variance central<indep. Communication/climbing degenerate at the fast smoke budget
  (expected — that's what the budget fixes above are for at scale).
- **scale** (`results/scale_results.json`): with the bumped coop budget + `lr_opp=5.0`, the
  effects now show clearly:
  - **communication: comm ON 0.795 vs OFF 0.204** (1/K=0.2) → helps ✔
  - **critic variance: central 0.000 vs indep 0.077** → central lower ✔
  - **LOLA: naive 1.042 vs LOLA 2.816** (lr_opp=5.0) → cooperates ✔
  - **climbing: IL 7.0, MAPPO 7.0, MADDPG 5.0** → MADDPG *underperforms* (the documented trap) ✔finding
  - PSRO: Kuhn/matrix→0; **Leduc 20 rounds →2.16** (bouncing 2.8/3.1/2.2/2.4/2.5/2.16 — slow, as noted); Goofspiel K=4 stays ~1.7 over 8 rounds (bigger game, non-monotone — K=3 in validate →0).
- Plots: `plots/psro_exploitability.png`, `plots/coop_ctde_comm.png` (regenerated for scale).

## Files touched (Phase 4)
`validate.py` (comm budget, MP lr, PSRO-Leduc reframe, climbing annotation), `config.py`
(`scale.coop` budget, `lola.lr_opp` both configs), `compare_pettingzoo.py` (mpe2 fallback).
New generated artifacts: `implementation/results/` (+ scale), `implementation/plots/`.
`consolidation/` intentionally not authored (left to another agent).
