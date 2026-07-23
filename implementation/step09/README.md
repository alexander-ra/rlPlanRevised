# Step 09 — Multi-Agent RL: Coordination, Competition, and Communication

**Source spec:** [`planning/rawSteps/step_09_multi_agent_rl.md`](../../planning/rawSteps/step_09_multi_agent_rl.md)
**Tier / duration:** Tier 2, 14 days · **Plan phase:** E (Multi-Agent Dynamics)
**Depends on:** Step 01 (RL Basics — PPO), Step 02 (Game Theory + CFR — Kuhn, Nash),
Step 03 (Leduc + best response / MCCFR), Step 06 (End-to-End Game AI), and the Step 07
`Game`/best-response/CFR toolchain this step reuses wholesale.
**PhD connection:** the pivot from **2-player zero-sum** (Steps 2–8) to the **multi-agent**
world. Three thesis hooks: LOLA as *dynamic* opponent modeling (Contribution #1), PSRO as
the framework for **safe exploitation in a population** where there is no minimax theorem
(Contribution #2), and PSRO's meta-game as a **multi-agent evaluation methodology**
(Contribution #3).

> **In one line:** in single-agent RL the agent learns against a *fixed* world; in
> multi-agent RL every agent **is** the world for every other agent, so the world is
> **non-stationary**. This step builds and compares the four responses to that fact —
> Independent Learning (the baseline that breaks), CTDE (MADDPG/MAPPO — centralize the
> critic), PSRO (bring game theory to bear on a *population* of policies), and LOLA
> (differentiate through the opponent's learning step) — plus emergent communication.

---

## How this folder is built

This step follows the per-phase contract in [`../WORKFLOW.md`](../WORKFLOW.md). In short:

- **Code is written here but NOT executed.** The human runs, debugs, validates, and refines
  it in separate sessions.
- **No fabricated results.** Every number in the docs is a *prediction / target to verify*,
  sourced from the raw step (Deliverables L438–448, Validation L450–456) or theory — never a
  claimed measurement.
- **`consolidation/` is deliberately absent** — it is written by hand after the code has
  been run and the results checked.
- Foundations are **imported, not copied** (see below).

---

## Phase folders

| Folder | Phase | Contains |
|--------|-------|----------|
| [`intuition/`](intuition/) | 1 — Intuition | `intuition.md`: why MARL differs from single-agent RL and from equilibrium computation, the dance-partner analogy, non-stationarity, the menu of methods (IL / CTDE / PSRO / LOLA / communication), the dated lineage, misconceptions, the **[P9] Markov-games bridge**, and a self-check. |
| [`exploration/`](exploration/) | 2 — Exploration | Small, seeded, runnable scripts: the four matrix games under independent learners, the non-stationarity/cycling demo, PG self-play vs the Step 2 Nash, a tiny PSRO peek, and LOLA-vs-naive on the Prisoner's Dilemma — plus a README on how to play with them and read the output. |
| [`targetedReading/`](targetedReading/) | 3 — Targeted Reading | `summary.md`: condensed VIP-only notes on the six papers (MADDPG, QMIX, MAPPO, LOLA, PSRO, CommNet) + supplementary + consolidation surveys, with cited key math, the four worked "Math Flags", and a synthesis. |
| [`implementation/`](implementation/) | 4 — Implementation | The full build: matrix games + native Goofspiel + a cooperative env + a normal-form meta-solver; Independent Learners, MADDPG, MAPPO, PSRO, CommNet, and LOLA; a tournament + plots + a validation harness — plus a README with the verification runbook. Guarded OpenSpiel / PettingZoo bridges. |
| `consolidation/` | 5 — Consolidation | **Absent — written by the human after the runs.** |

---

## Imported foundations (never copied)

This step is **built on Step 07's validated modules** (which themselves wrap the Step 02
Kuhn engine and the Step 03 Leduc engine). See
[`implementation/deps.py`](implementation/deps.py), which bootstraps them onto `sys.path`:

- **Uniform game interface** (Kuhn + Leduc): [`../step07/implementation/engines.py`](../step07/implementation/engines.py)
- **Exact best response / exploitability / NashConv** (the PSRO best-response oracle *and*
  the validation ground truth): [`../step07/implementation/best_response.py`](../step07/implementation/best_response.py)
- **Nash baseline via CFR** (the PSRO-vs-CFR comparison + the self-play convergence target):
  [`../step07/implementation/nash.py`](../step07/implementation/nash.py)
- **Policy currency + simulation** (`tabular_policy`, `uniform_policy`, `play_hand`,
  `blend_policies`): [`../step07/implementation/policies.py`](../step07/implementation/policies.py)

> **The `cfr` namespace trap (inherited safely).** step02 and step03 both ship a package
> named `cfr`; putting both on `sys.path` merges them and silently cross-wires
> `cfr.info_set_node`. Step 07's `engines.py` sidesteps this by loading each engine file
> directly via `importlib` under a unique name. By importing Step 07's `engines.py` we
> inherit that safe loader for free. **Run implementation scripts from
> `implementation/step09/implementation/`.**

The PPO learner used by MAPPO / the PSRO RL oracle is a **compact, self-contained discrete
PPO** (mirrors Step 01's clipped-surrogate objective, but rewritten for the small
matrix/coop/EFG settings rather than Gym rollout loops) — see
[`implementation/learners.py`](implementation/learners.py).

---

## Scope notes (per WORKFLOW.md + the confirmed plan)

- **Self-contained core, guarded optional bridges.** Matrix games, Goofspiel, and the
  cooperative env run on `numpy` (+ `torch` for the neural methods) alone. PettingZoo-MPE
  (`compare_pettingzoo.py`) and OpenSpiel (`compare_openspiel.py`) are optional
  cross-checks that print `SKIP` and exit cleanly when the library is absent — `requirements.txt`
  intentionally excludes both.
- **LOLA is included** (raw-step reading paper + mandatory Math Flag + thesis Contribution
  #1) as a compact exact implementation on the Iterated Prisoner's Dilemma, beyond the
  strict Phase-4 deliverables list.
- **QMIX** is covered as *reading* (Phase 3) + the monotonicity Math Flag; an optional small
  monotonic-mixing illustration lives in the implementation phase but is not a required
  deliverable.

---

## Build status

- [x] Scaffold (this README + the four phase folders + `deps.py`)
- [x] `intuition/intuition.md`
- [x] `exploration/` (code + README) — written, not yet executed
- [x] `targetedReading/summary.md`
- [x] `implementation/` (code + README + validation harness) — written, **not executed**
- [ ] `consolidation/` — deferred to the human, after running and refining the code
- [ ] `deliverables/reports/step09/` — deferred (Phase 6, from verified results only)
