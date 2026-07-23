# Step 10 — Population-Based Training + Evolutionary Game Theory

**Source spec:** [`planning/rawSteps/step_10_population_training_evo_gt.md`](../../planning/rawSteps/step_10_population_training_evo_gt.md)
**Tier / duration:** Tier 2, 14 days · **Plan phase:** E (Multi-Agent Dynamics)
**Depends on:** Step 01 (PPO), Step 02 (CFR / Kuhn / Nash), Step 03 (Leduc + best response),
Step 07 (the `Game` / exact-best-response / CFR-Nash / policy toolchain), and **Step 09**
(PSRO, meta-Nash, the matrix-game testbed) — this step reuses both wholesale.
**PhD connection:** the population-level generalization of Steps 7–9. Three thesis hooks:
AlphaStar exploiters as **automated opponent modeling** (Contribution #1), the league's
*heuristic-only* safety as the gap **formal safe population training** must close
(Contribution #2), and the **meta-Nash of the empirical game** as a multi-agent evaluation
methodology / the generalization of exploitability (Contribution #3).

> **In one line:** stop training one agent against itself and instead **evolve a whole
> population** — AlphaStar's league (main agents, main-exploiters, league-exploiters, frozen
> history, PBT) — while using **evolutionary game theory** (replicator dynamics + the
> spinning-top transitive/cyclic decomposition + EGTA) to *predict and evaluate* what such a
> population converges to.

---

## How this folder is built

This step follows the per-phase contract in [`../WORKFLOW.md`](../WORKFLOW.md), with one scope
decision for this session:

- **Phases 1–4 are authored; Phases 5–6 are deferred.** This session wrote the *intuition*,
  *exploration*, *targeted reading*, and the full *implementation* (code + harness). **Nothing
  has been executed here** (WORKFLOW §0: write everything, run nothing). The
  measured-vs-predicted reconciliation (`consolidation/`) and the EN report
  (`deliverables/reports/step10/`) require verified run results and are left for the post-run
  session.
- **No fabricated results.** Every number in these docs is a **prediction / target to verify**
  (raw step Deliverables L475–484, Validation L486–492).
- **The PBT League uses neural PPO agents** on a Leduc info-state encoding (smoke = CPU, scale =
  5090), trained by self-play but **evaluated exactly** by extracting each net into a tabular
  policy and reusing Step 07's exact engine.
- Foundations are **imported, not copied** (see below).

---

## Phase folders

| Folder | Phase | Contains |
|--------|-------|----------|
| [`intuition/`](intuition/) | 1 — Intuition | `intuition.md`: population vs point, the dojo/league analogy, non-transitivity and why self-play cycles, the menu of methods (self-play / PSRO / PBT / AlphaStar league / replicator / EGTA), a dated lineage (1978→2019), misconceptions, and a self-check. |
| [`exploration/`](exploration/) | 2 — Exploration | Small, seeded, runnable scripts: replicator dynamics on the four games, a PSRO population peek on Leduc, a game-landscape (skill vs cycles) visualizer, and a fast PBT proxy showing diversity collapse — plus a README on how to play with them (all numbers as predictions). |
| [`targetedReading/`](targetedReading/) | 3 — Targeted Reading | `summary.md`: VIP-only notes on the five core papers (PBT, FTW, AlphaStar, spinning top, EGTA) + supplementary, with cited sections/theorems, four worked **Math Flags** (replicator, spinning-top, EGTA bound, Elo), a synthesis, and a verify-list. |
| [`implementation/`](implementation/) | 4 — Implementation | The full build: `evo_games` + `replicator` + `spinning_top` (exact numpy); `leduc_rl` + `ppo_agent` + `league` + `elo` + `egta` + `diversity` (the neural league, exactly evaluated); `config`/`evaluation`/`tournament`/`plotting`/`validate` — plus a README with the verification runbook, predictions, and a static self-review. |

*(Phase 5 `consolidation/` and Phase 6 `deliverables/reports/step10/` are intentionally absent
this session — they depend on verified run results.)*

---

## Imported foundations (never copied)

See [`implementation/deps.py`](implementation/deps.py), which bootstraps **Step 09** and **Step
07** onto `sys.path`:

- **Step 09** — [`../step09/implementation/psro.py`](../step09/implementation/psro.py) (`PSRO`,
  `mixture_behavioral_policy`), [`../step09/implementation/meta_nash.py`](../step09/implementation/meta_nash.py)
  (`solve_meta_nash`), [`../step09/implementation/matrix_games.py`](../step09/implementation/matrix_games.py)
  (PD + Stag Hunt, reused by `evo_games`), [`../step09/implementation/learners.py`](../step09/implementation/learners.py)
  (the lazy torch guard).
- **Step 07** — [`../step07/implementation/engines.py`](../step07/implementation/engines.py)
  (`make_game`, exact Leduc engine), [`../step07/implementation/best_response.py`](../step07/implementation/best_response.py)
  (`exact_value`, `nash_gap`), [`../step07/implementation/nash.py`](../step07/implementation/nash.py)
  (CFR Nash reference), [`../step07/implementation/policies.py`](../step07/implementation/policies.py)
  (`tabular_policy`, `materialize`, `sample_action` — the net→tabular bridge).

> **The `deps.py` shadowing dance (inherited safely).** Step 09's `psro.py` does `import deps`;
> since Step 10's folder is `sys.path[0]`, that resolves to **Step 10's** `deps.py`, which
> appends both prior steps — so `psro` finds `meta_nash` (Step 09) and `best_response`/`policies`
> (Step 07). **Run implementation scripts from `implementation/step10/implementation/`** and
> exploration scripts from `implementation/step10/exploration/`.

The neural agent is a **compact masked discrete PPO** ([`implementation/ppo_agent.py`](implementation/ppo_agent.py))
mirroring Step 01's / Step 09's clipped-surrogate objective, rewritten for Leduc's
variable-length imperfect-info episodes with action masking + per-agent PBT hyperparameters.

---

## Scope notes (per WORKFLOW.md + the confirmed plan)

- **Neural league, exact evaluation.** Agents train by rollouts; all reported metrics
  (exploitability, EGTA meta-Nash, Elo, spinning-top) are computed exactly via tabular
  extraction + Step 07's engine. Validity rests on Leduc perfect recall.
- **Self-contained exact core, guarded neural half.** Replicator / spinning-top / EGTA / PSRO /
  CFR run on `numpy` (+ `scipy` for the LP, with a fictitious-play fallback). The PBT league and
  self-play baseline need `torch` and SKIP cleanly if it's absent.
- **Spinning-top uses the Hodge (ratings-difference) decomposition**, not the raw step's rank-1
  SVD sketch — only Hodge yields "RPS = 100% cyclic" (see the module NOTE). This is flagged as a
  Math Flag to verify against Balduzzi's Theorem 1.

---

## Build status

- [x] Scaffold (this README + the four phase folders + `deps.py`)
- [x] `intuition/intuition.md`
- [x] `exploration/` (code + README) — **written, not executed**
- [x] `targetedReading/summary.md`
- [x] `implementation/` (code + README + validation harness) — **written, not executed**
- [ ] `consolidation/` — deferred to the post-run session (needs verified results)
- [ ] `deliverables/reports/step10/` — deferred to the post-run session (needs verified results)
