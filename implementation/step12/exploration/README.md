# Step 12 — Exploration (Phase 2)

Small, seeded, deliberately scrappy probes that build intuition for the two hazards this step is
really about: **return conditioning** and the **luck-vs-skill trap**, plus a look at an **LLM
actually playing Kuhn**. Per [`../../WORKFLOW.md`](../../WORKFLOW.md) these are **written but not
executed** — every number below is a **prediction to verify** in the run session.

All three scripts share [`_bootstrap.py`](_bootstrap.py), which puts the Step 12
`implementation/` folder on `sys.path` (which in turn chains step02/step07/step09). Run from this
folder, e.g. `python dt_return_conditioning.py`.

---

## Scripts

### 1. `dt_return_conditioning.py`  (torch)
**What:** trains a tiny DT on near-Nash Kuhn self-play, then extracts its strategy while
conditioning on a sweep of target returns — the real `{-2,-1,+1,+2}` plus an **impossible +3**
— and reports the exact Step 02 exploitability at each.
**Knobs:** `n_trajectories`, `cfr_iters`, DT size/epochs (all inline, tiny), the target sweep.
**Watch out:** the +3 point is **out-of-distribution** (no Kuhn hand pays +3); do not read a
lower number there as "better play" — it is extrapolation.
**How to read:** exploitability should **fall** as the target return rises across the real
range; the impossible +3 should **saturate or worsen**.
**Predicted runtime:** seconds to ~1 min on CPU.

### 2. `luck_vs_skill_coinflip.py`  (numpy, no torch)
**What:** the Paster luck trap in a one-step bandit. Action A is the EV-optimal safe choice
(0.5); action B is risky (1.0 w.p. 0.4 → EV 0.4). Conditioning on the highest return (1.0)
recovers **only** B-trajectories, so return-conditioned cloning learns the **worse** action.
**Knobs:** `p_win_B`, sample size, the conditioning target.
**Watch out:** this is the cleanest statement of *why ARDT exists* — keep it in mind reading the
ARDT section.
**How to read:** `P(action=B | return=1.0) ≈ 1.0` while the EV-optimal action is A.
**Predicted runtime:** < 1 s.

### 3. `llm_kuhn_repl.py`  (offline stub by default)
**What:** plays a few hands of *LLM vs near-Nash CFR* on the real Step 02 engine, printing the
card, betting, the model's reasoning, and the parsed action.
**Knobs:** `SPEC` (swap the stub for a `config.py` local-model preset), `N_HANDS`,
`PROMPT_STYLE`.
**Watch out:** the stub is deterministic and legal by construction (illegal rate 0%); a **real**
model is where you expect mis-set bluff frequency and the occasional illegal action.
**How to read:** sanity of King/Jack play is easy; the interesting signal is **bluff frequency**
and **illegal moves**.
**Predicted runtime:** seconds with the stub; model-bound with a real backend.

---

## Predictions (to verify — not measured)

- **Return conditioning works, then breaks OOD.** Exploitability decreases with higher in-range
  target return; the impossible +3 gives no further gain (saturates/degrades).
- **High return ≠ skill under stochasticity.** The coin-flip probe shows high-return conditioning
  selecting the EV-*worse* action — the entire motivation for ARDT.
- **The LLM is honestly imperfect.** Sensible extremes (K/J) but off-Nash bluffing and a nonzero
  illegal-move rate with a real model; the offline stub is a clean, legal baseline.

*Interpretation with PASS/FAIL lives in [`../implementation/validate.py`](../implementation/validate.py).*
