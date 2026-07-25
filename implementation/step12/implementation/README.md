# Step 12 — Implementation (Phase 4)

The full build for Step 12: a self-contained **Decision Transformer** + **ARDT** + a
model-agnostic **LLM agent**, all scored on the **exact Step 02 Kuhn exploitability** in one
comparison table. Grounded in
[`../../../planning/rawSteps/step_12_sequence_models_llm_agents.md`](../../../planning/rawSteps/step_12_sequence_models_llm_agents.md)
and governed by [`../../WORKFLOW.md`](../../WORKFLOW.md).

> **Status: written, NOT executed** (WORKFLOW section 0). Every number in this file is a
> **prediction / target**. Measured results go in `EXECUTION_NOTES.md` and `consolidation/`
> **next session**.

---

## Module map (→ raw-step line ranges, with tags)

`[CORE]` thesis-critical · `[SUP]` support · `[INF]` infrastructure

| Module | Tag | Raw | What it does |
|---|---|---|---|
| [`deps.py`](deps.py) | INF | — | Bootstraps step02/step07/step09 onto `sys.path` (append-only so Step 12 wins); torch guard with local fallback. Avoids the step02/03 `cfr` collision by adding **only** step02. |
| [`state_encoding.py`](state_encoding.py) | CORE | L234-282 | `PokerStateEncoder`: fixed-dim tensor (card/board one-hot, position, normalized pot/stack, per-ply betting-history one-hot, round flag). **The artifact carried into Step 13.** |
| [`trajectory_dataset.py`](trajectory_dataset.py) | CORE | L236-293 | `PokerTrajectoryDataset`: `(return-to-go, state, action)` triples from CFR self-play (`self_play_nash`) or mixed opponents (`mixed_opponents`, step07 zoo + exact best response). Return-stats data-quality check vs ±1/18. |
| [`decision_transformer.py`](decision_transformer.py) | SUP | L297-312 | Self-contained GPT-2-style discrete-action DT (mirrors HF `DecisionTransformerConfig` fields). Torch-guarded. |
| [`behavioral_cloning.py`](behavioral_cloning.py) | SUP | L322-325 | MLP state→action BC baseline (no return conditioning). |
| [`train_dt.py`](train_dt.py) | SUP | L295-325 | DT training + return-conditioning experiment + luck-vs-skill (bet-by-card) experiment. |
| [`ardt.py`](ardt.py) | CORE | L327-379 | `expectile_loss`, `MinimaxReturnEstimator`, `relabel_returns`, `AdversariallyRobustDT`. **Contains MATH FLAG B** (τ direction). |
| [`llm_agent.py`](llm_agent.py) | CORE/INF | L381-446 | Model-agnostic `LLMClient` (offline stub / OpenAI-compat HTTP / optional HF) + `KuhnPokerLLMAgent` (plain/CoT/game-theory) + robust parsing / illegal handling + `llm_policy`. |
| [`textarena_agent.py`](textarena_agent.py) | INF | L383-398 | Optional, guarded TextArena bridge for the same client. |
| [`strategy_extraction.py`](strategy_extraction.py) | CORE | L430-446 | Any agent (DT/ARDT/BC/LLM/policy) → a 12-info-set Kuhn `node_map` in Step 02's exact-metric format. |
| [`evaluation.py`](evaluation.py) | CORE | L430-463 | Exact exploitability (reuse step02) + chips↔mbb/h + bluff(J)/value-bet(K) + illegal rate + opponent adaptation. |
| [`comparison_table.py`](comparison_table.py) | SUP | L436-446 | The headline Nash/DT/ARDT/BC/LLM×prompts table → `results/comparison_<profile>.json`. |
| [`config.py`](config.py) | INF | — | SMOKE/SCALE profiles + LLM roster presets + `RUNTIME_NOTES` (5090 serving). |
| [`plotting.py`](plotting.py) | INF | — | Guarded matplotlib: return-conditioning curve, bet-by-card, exploitability bars. |
| [`validate.py`](validate.py) | CORE/INF | L458-463 | PASS/FAIL harness for the five validation targets. |

---

## Data flow

```
CFR (step02) ─┐                                     ┌─> strategy_extraction ─> evaluation ─┐
step07 zoo ───┼─> trajectory_dataset ─> DT / BC / ARDT ┘        (exact step02 expl +       ├─> comparison_table (JSON)
state_encoding┘                                                  bluff/value/illegal/adapt) └─> validate.py (PASS/FAIL)
LLM client (stub / local model) ─> llm_agent ─> llm_policy ─> strategy_extraction ─────────┘
```

---

## Runbook (for the verification session — do not run now)

From this folder (`implementation/`). SMOKE is the default; nothing needs a GPU or an LLM key.

```bash
# 0. Sanity: reused engines import cleanly
python deps.py

# 1. Torch-free building blocks (each has a self-test)
python state_encoding.py
python trajectory_dataset.py
python strategy_extraction.py
python evaluation.py
python llm_agent.py

# 2. Neural pieces (need torch; auto-skip / clear error if absent)
python decision_transformer.py
python ardt.py                 # includes the expectile τ-direction sanity check
python train_dt.py             # return-conditioning + luck-vs-skill experiments

# 3. Headline table + validation
python comparison_table.py     # writes results/comparison_SMOKE.json
python validate.py             # PASS/FAIL on the five targets

# 4. Scale up on the RTX 5090 with a real local model (PowerShell)
$env:STEP12_PROFILE = "SCALE"; $env:STEP12_LLM = "gpt_oss_20b"; python comparison_table.py
$env:STEP12_LLM = "qwen2.5_7b";       python comparison_table.py
$env:STEP12_LLM = "openthinker3_7b";  python comparison_table.py
```

See `RUNTIME_NOTES` in [`config.py`](config.py) for serving models (LM Studio / Ollama / vLLM)
and Blackwell/CUDA notes.

---

## How to verify — thresholds (raw L458-463)

Exploitability is reported in **chips** and **mbb/h**. Conversion: 1-chip ante = big blind ⇒
`mbb/h = chips × 1000`; the raw "within 50 mbb/h" target ⇒ **≤ 0.05 chips**.

| # | Target | Check in `validate.py` |
|---|---|---|
| 1 | DT: high return-to-go → **lower** exploitability than low | `expl(high R) < expl(low R)` |
| 2 | Stochasticity: DT action **varies by card** (learns luck) | root `P(bet)` spread across J/Q/K ≥ 0.10 |
| 3 | ARDT **<** standard DT (same mixed data, vs Nash) | `expl(ARDT) < expl(DT_mixed)` |
| 4 | ARDT **within ~50 mbb/h** of Nash | `expl(ARDT) ≤ 0.05 chips` *(aspirational; may need SCALE)* |
| 5 | LLM **honestly more exploitable** than Nash; capture failure | `expl(LLM) > expl(Nash)`, plus bluff(J) & illegal% |

---

## Expected outcomes (PREDICTIONS — to be measured)

- **Data quality:** near-Nash self-play → seat-0 mean return ≈ **−1/18 (−0.056)**, seat-1 ≈ **+1/18**
  (Kuhn first-mover disadvantage). Deviation ⇒ CFR under-trained or a utility-sign bug.
- **Nash-CFR row:** exploitability ≈ **0** (a few thousandths of a chip); bluff(J) and value-bet(K)
  near the known Kuhn Nash frequencies.
- **DT:** exploitability **decreases** with higher in-range target return; the **impossible +3**
  saturates/degrades (OOD). Bet-frequency **shifts with the card** under high conditioning — the
  Paster luck signature (target #2).
- **ARDT:** **below** the same-data vanilla DT vs Nash (target #3), trending toward Nash as data
  coverage grows; target #4 (≤0.05 chips) likely needs SCALE and the τ resolved (MATH FLAG B).
- **BC:** roughly recovers the (near-Nash) data policy on self-play data — a sensible middle.
- **LLM:** honestly **more exploitable** than Nash; the interesting output is **where** — off-Nash
  bluff frequency and a nonzero **illegal-move rate** with a real model (0% for the offline stub).
  CoT ≥ plain; game-theory prompt may narrow the bluff gap. OpenThinker3's long CoT costs latency.

---

## Likely-to-break (called out up front)

- **`cfr` package name collision** (step02 vs step03): mitigated — `deps.py` adds **only** step02;
  Leduc is reached via step07's importlib-loaded `make_game("leduc")`, never the `cfr` package.
- **Exploitability units** (chips vs mbb/h): the ARDT-vs-Nash threshold is the easy place to
  misread; `evaluation.py` reports both and states the 1-chip-BB convention.
- **ARDT τ direction (MATH FLAG B):** the raw sketch's `τ=0.9`-as-"pessimistic" is likely inverted;
  code defaults to the low-τ (pessimistic) side and flags it. **Resolve against arXiv:2407.18414
  §4 before trusting targets #3-4.**
- **Torch/Blackwell:** DT/ARDT are torch-guarded; SMOKE is CPU-tiny. On the 5090 you may need a
  cu128 PyTorch wheel or it silently falls back to CPU.
- **LLM parsing / illegal handling:** real models emit "raise/all-in/fold" and stray prose;
  `parse_action` maps poker verbs leniently and counts only truly unmappable replies as illegal.
  The offline stub makes this path testable with no model.
- **OpenThinker3 always-on long CoT:** inflates latency and parse cost vs Qwen2.5-7B (timeout
  already raised; documented).
- **Single-step conditioning in extraction:** strategy is read per info set with a length-1
  sequence (the info set already encodes history). Fine for Kuhn; revisit for multi-street games.

---

## Static self-review (WORKFLOW section 8 — read, not run)

- **Imports, not copies:** engines/metrics/opponents/torch-guard all come through `deps.py`; no
  step02/03/07/09 code is duplicated here.
- **Torch is optional at import:** only the neural modules do `require_torch()` at import;
  `strategy_extraction`, `evaluation`, `comparison_table`, `validate` import torch **lazily** so
  the CFR + LLM-stub path runs with no torch installed.
- **Determinism:** dataset/CFR seeded; the offline LLM stub is deterministic ⇒ the SMOKE table and
  validation are reproducible without a GPU or network.
- **Exact metric reused verbatim:** exploitability is Step 02's `compute_exploitability` on a
  12-info-set `node_map`; every agent is coerced into that one format by `strategy_extraction`.
- **Honesty about the math:** the two derived results (Paster gap; ARDT expectile/τ) are labelled
  "agent derivation, TO VERIFY" in `targetedReading/summary.md` and echoed as MATH FLAG B in
  `ardt.py`. Nothing asserts a paper result I have not re-derived or cited.
- **Scope discipline:** Kuhn is fully wired and validated; Leduc is a documented SCALE extension
  (encoder ready + `make_game("leduc")`), not silently half-built.
- **Open risks to watch on first run:** (a) τ direction flips target #3-4; (b) target #4 needs
  SCALE-size data coverage; (c) `max_ep_len`/`max_length` are generous for Kuhn — trim for speed
  if needed.

---

## Key takeaways

- **One exact ruler, five methods.** DT, ARDT, BC, and LLM×prompts are all coerced into Step 02's
  exact Kuhn exploitability — an honest, ground-truthed comparison rather than anecdotes.
- **ARDT is a second, offline road to Nash.** Minimax return conditioning (expectile-relabeled)
  is the robustness fix for the luck/adversary trap that plain DT falls into — and the technique
  that carries to Step 13's fixed Playtech logs.
- **The state encoder is the reusable asset.** `PokerStateEncoder` is the concrete artifact Step
  13 inherits; getting its features right here pays off downstream.
- **LLMs fail informatively.** The value is in *where* they leave Nash (bluff frequency, illegal
  moves, (non-)adaptation), all measured — not a leaderboard number.
