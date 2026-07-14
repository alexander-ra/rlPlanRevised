# Step 08 — Safe Exploitation (Theory, Algorithms, Real-Time Search)

**Source spec:** [`planning/rawSteps/step_08_safe_exploitation.md`](../../planning/rawSteps/step_08_safe_exploitation.md)
**Tier / duration:** Tier 1, 21 days · **Plan phase:** D (Opponent Modeling + Exploitation)
**Depends on:** Step 02 (Game Theory + CFR), Step 03 (Leduc + best response), Step 06
(End-to-End Game AI), and **Step 07 (Opponent Modeling)** — the *sensor* this step turns
into an *actuator*.
**PhD connection:** the SECOND HALF of Contribution #1 (Behavioral Adaptation Framework)
and the launch point for Contribution #2 (Multi-Agent Safe Exploitation). Step 07 built the
model that infers *how* an opponent plays; Step 08 exploits that model **without becoming
exploitable** — and pins down exactly where the 2-player zero-sum assumption enters the
safety proofs (the thesis attack point).

> **In one line:** exploitation = *constrained optimization* — maximize value against your
> opponent model, subject to a **safety** constraint that caps how much a clever adversary
> can punish you. Every algorithm in this step (RNR → Ganzfried → Prime-Safe → SES →
> Adaptation-Safety) is the *same* objective with a *different* safety constraint.

---

## How this folder is built

This step follows the per-phase contract in [`../workflow.md`](../workflow.md). In short:

- **Code is written here but NOT executed.** The human runs, debugs, validates, and refines
  it in separate sessions.
- **No fabricated results.** Every number in the docs is a *prediction / target to verify*,
  sourced from the raw step (Validation, L558–564) or theory — never a claimed measurement.
- **`consolidation/` is deliberately absent** — it is written by hand after the code has
  been run and the results checked.
- Foundations are **imported, not copied** (see below).

---

## Phase folders

| Folder | Phase | Contains |
|--------|-------|----------|
| [`intuition/`](intuition/) | 1 — Intuition | `intuition.md`: the exploitation-safety tradeoff in plain terms, the leveling-war analogy, the menu of methods, and the dated RNR→ABD lineage. |
| [`exploration/`](exploration/) | 2 — Exploration | Small, seeded, runnable Kuhn/Leduc scripts (the exploitation-safety playground, the Pareto curve, the danger of naive best response, an RNR p-sweep, a one-subgame peek) + a README on how to play with them and read the output. |
| [`targetedReading/`](targetedReading/) | 3 — Targeted Reading | `summary.md`: condensed VIP-only notes on the six papers (Johanson 2007 → Milec 2025) + the book sections, with cited key math, the three worked "Math Flags", and a synthesis. |
| [`implementation/`](implementation/) | 4 — Implementation | The full build: one sequence-form LP engine and the five safe-exploitation solvers built on it, a safety checker, the exploitation metrics, a Step-7→Step-8 pipeline, a teaching-attack stress test, a tournament + Pareto plots, and a validation harness — plus a README with the verification runbook. |
| `consolidation/` | 5 — Consolidation | Not produced by the agent. Written by the human afterward. |

---

## Imported foundations (never copied)

This step is **built on Step 07's validated modules** — it does not re-implement the game
engines, best response, Nash, or the opponent models. See
[`implementation/deps.py`](implementation/deps.py), which bootstraps them onto `sys.path`
under stable names:

- **Uniform game interface** (Kuhn + Leduc): [`../step07/implementation/engines.py`](../step07/implementation/engines.py)
- **Exact best response / exploitability** (the worst-case oracle every safety constraint
  calls): [`../step07/implementation/best_response.py`](../step07/implementation/best_response.py)
- **Nash baseline via CFR** (the safety anchor; early-stopped → an ε-equilibrium for the
  prime-safe test): [`../step07/implementation/nash.py`](../step07/implementation/nash.py)
- **Policy currency + blends**: [`../step07/implementation/policies.py`](../step07/implementation/policies.py)
- **Opponent type zoo** (the exploitees): [`../step07/implementation/opponent_types.py`](../step07/implementation/opponent_types.py)
- **Sequence form (treeplex)** reused directly for the LP: `SequenceForm` in
  [`../step07/implementation/consistent_model.py`](../step07/implementation/consistent_model.py)
- **Opponent models** (type-based / continuous) plugged into the pipeline:
  [`../step07/implementation/type_based_model.py`](../step07/implementation/type_based_model.py),
  [`continuous_model.py`](../step07/implementation/continuous_model.py)

Step 07 loads the Kuhn (step02) and Leduc (step03) engines via `importlib` to avoid a real
hazard: both ship a package named `cfr` that would merge into one namespace package and
silently cross-wire `cfr.info_set_node`. Step 08 reuses that same loader by importing
Step 07's `engines.py`. **Run implementation scripts from
`implementation/step08/implementation/`.**

---

## Build status

- [x] Scaffold (this README + the four phase folders)
- [x] `intuition/intuition.md`
- [x] `exploration/` (code + README) — written, not yet executed
- [x] `targetedReading/summary.md`
- [x] `implementation/` (code + README) — written, not yet executed
- [ ] `consolidation/` — left for the human, after runs
