# Step 07 — Opponent Modeling (Inference from Behavioral Traces)

**Source spec:** [`planning/rawSteps/step_07_opponent_modeling.md`](../../planning/rawSteps/step_07_opponent_modeling.md)
**Tier / duration:** Tier 1, 21 days · **Plan phase:** D (Opponent Modeling + Exploitation)
**Depends on:** Step 02 (Game Theory + CFR) and Step 06 (End-to-End Game AI).
**PhD connection:** First half of Contribution #1 (Behavioral Adaptation Framework) — the
opponent model is the *sensor* that turns observed actions into an estimate of the
opponent's strategy, which Step 08 then exploits safely.

> **In one line:** Nash play ignores who it's playing. This step builds models that infer
> *how a specific opponent plays* from their behavior, so the agent can deviate from Nash
> to exploit them — without becoming exploitable itself.

---

## How this folder is built

This step follows the per-phase contract in [`../WORKFLOW.md`](../WORKFLOW.md). In short:

- **Code is written here but NOT executed.** The human runs, debugs, validates, and
  refines it in separate sessions.
- **No fabricated results.** Every number in the docs is a *prediction / target to
  verify*, sourced from the raw step or theory — never a claimed measurement.
- **`consolidation/` is deliberately absent** — it is written by hand after the code has
  been run and the results checked.
- Engines are **imported, not copied** (see below).

---

## Phase folders

| Folder | Phase | Contains |
|--------|-------|----------|
| [`intuition/`](intuition/) | 1 — Intuition | `intuition.md`: the idea in plain terms, the menu of modeling approaches, and how the field developed over time. |
| [`exploration/`](exploration/) | 2 — Exploration | Small, seeded, runnable scripts (opponent "type zoo", behavioral fingerprints, exploitation gap, a naive Bayesian type detector) + a README on how to play with them and read the output. |
| [`targetedReading/`](targetedReading/) | 3 — Targeted Reading | `summary.md`: condensed VIP-only notes on the step's papers (Southey 2005 → Ganzfried 2025) + the book chapter, with cited key math and a synthesis. |
| [`implementation/`](implementation/) | 4 — Implementation | The full build: observation buffer, type-based / continuous / consistent Bayesian models, best response vs. an inferred model, the adaptive-exploitation pipeline, a tournament + non-stationarity harness, and plotting — plus a README with the verification runbook. |
| `consolidation/` | 5 — Consolidation | Not produced by the agent. Written by the human afterward. |

---

## Imported foundations (never copied)

- **Kuhn Poker engine:** [`../step02/cfr/kuhn_poker.py`](../step02/cfr/kuhn_poker.py)
- **Leduc Hold'em engine:** [`../step03/cfr/leduc_poker.py`](../step03/cfr/leduc_poker.py)
- **Best response / exploitability:** [`../step03/evaluate/`](../step03/evaluate/)

The **exploration** scripts add a small `sys.path` bootstrap to import the Step 02 engine.
The **implementation** loads *both* engines directly from their files via `importlib`
(`implementation/engines.py`) — this avoids a real hazard: step02 and step03 both ship a
package named `cfr`, which would merge into one namespace package and silently cross-wire
`cfr.info_set_node` if both were on `sys.path`. Run implementation scripts from
`implementation/step07/implementation/`.

---

## Build status

- [x] Scaffold (this README + the four phase folders)
- [x] `intuition/intuition.md`
- [x] `exploration/` (code + README)
- [x] `targetedReading/summary.md`
- [x] `implementation/` (code + README) — written, not yet executed
- [ ] `consolidation/` — left for the human, after runs
