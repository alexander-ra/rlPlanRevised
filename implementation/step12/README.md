# Step 12 — Sequence Models + LLM Agents in Strategic Settings

**Source spec:** [`planning/rawSteps/step_12_sequence_models_llm_agents.md`](../../planning/rawSteps/step_12_sequence_models_llm_agents.md)
**Tier / duration:** Tier 3, 10 days · **Plan phase:** F (Data-Driven Approaches)
**Depends on:** Step 02 (Kuhn engine + exact exploitability + CFR), Step 03 (Leduc, SCALE-only),
Step 05 (neural equilibrium — conceptual sibling of ARDT), Step 07 (opponent modeling + the
exploitable opponent zoo used as ARDT's mixed-opponent data).

> **In one line:** two modern, post-classical ways to play games — **train a transformer to
> predict good moves from past game histories** (Decision Transformer, and its adversarially
> robust variant ARDT), and **just ask an LLM to play** — measured against the *exact* Kuhn
> Poker Nash benchmark from Step 02, in one comparison table.

---

## The two paradigms (read this first)

1. **Sequence modeling for offline RL (Decision Transformer).** Reframe RL as conditional
   sequence prediction: feed `(return-to-go, state, action)` triples to a GPT-style model and
   predict the next action *conditioned on the desired future return*. No value function, no
   Bellman backup — pure supervised learning on a static dataset of past hands. **ARDT** adds
   *minimax* return conditioning so the learned policy is robust to the worst-case opponent,
   not just tuned to exploit the opponents that happened to be in the data.
2. **LLM agents.** Give a language model the rules in plain English and let it play. No
   training, no tree search — prompt engineering + in-context reasoning. Works surprisingly
   well in some settings, embarrassingly badly in others (illegal moves, poor bluffing).

Kuhn Poker is the shared testbed because its Nash equilibrium and exploitability are
**exactly** computable (Step 02), so every method gets an honest, ground-truthed score.

---

## How this folder is built (scope for this session)

Per [`../WORKFLOW.md`](../WORKFLOW.md):

- **Phases 1-4 are authored; execution + Phase 5 are deferred.** This session wrote the
  *intuition*, *exploration*, *targeted reading*, and the full *implementation* (code +
  validation harness). **Nothing has been executed here** (WORKFLOW section 0: write
  everything, run nothing). The `consolidation/` one-pager + learning log, the
  `EXECUTION_NOTES.md` measured-vs-predicted dev log, and the EN/BG reports all require
  verified run results and are left for the post-run session.
- **No fabricated results.** Every number in these docs is a **prediction / target to
  verify** (raw Deliverables L448-456, Validation L458-463).
- **Foundations are imported, not copied** (see [`implementation/deps.py`](implementation/deps.py)).

---

## Phase folders

| Folder | Phase | Contains |
|--------|-------|----------|
| [`intuition/`](intuition/) | 1 — Intuition | `intuition.md`: the two paradigms in plain words, the menu of approaches (CQL vs DT vs Trajectory Transformer vs ARDT; LLM zero-shot vs CoT vs game-theory-prompted), a dated lineage (2021 DT/TT to 2025 TextArena/SpinGPT), misconceptions (return-to-go conflates luck with skill; LLM illegal moves), and a self-check. |
| [`exploration/`](exploration/) | 2 — Exploration | Small, seeded, runnable scripts: a toy DT return-conditioning sweep (incl. the "impossible return" test), the Paster coin-flip luck-vs-skill demo, and a Kuhn LLM REPL on the Step 02 engine — plus a README (all numbers as predictions). |
| [`targetedReading/`](targetedReading/) | 3 — Targeted Reading | `summary.md`: VIP-only notes on the five core papers (DT, Paster, ARDT, TextArena, Trajectory Transformer) + supplementary (CQL, Divide-Fuse-Conquer, Suspicion-Agent, SpinGPT), two worked **Math Flags** (Paster Theorem 2.1; ARDT minimax expectile regression), a synthesis and a verify-list. |
| [`implementation/`](implementation/) | 4 — Implementation | The full build: `state_encoding` + `trajectory_dataset` (thesis tensor + CFR/mixed-opponent data); the self-contained `decision_transformer` + `behavioral_cloning` + the core `ardt`; the `llm_agent` (offline stub + local-model client); `strategy_extraction` + `evaluation` + `comparison_table` on Step 02's exact exploitability; `config` / `plotting` / `validate` — plus a README with the verification runbook, predictions, and a static self-review. |

*(Phase 5 `consolidation/`, `EXECUTION_NOTES.md`, and `deliverables/reports/step12/` are
intentionally absent this session — they depend on verified run results.)*

---

## Imported foundations (never copied — WORKFLOW section 6)

See [`implementation/deps.py`](implementation/deps.py):

- **Step 02** — [`kuhn_poker.py`](../step02/cfr/kuhn_poker.py) (engine), `KuhnTrainer`
  ([`cfr_trainer.py`](../step02/cfr/cfr_trainer.py), our near-Nash data generator), and the
  exact metric [`exploitability.py`](../step02/evaluate/exploitability.py) /
  [`best_response.py`](../step02/evaluate/best_response.py).
- **Step 07** — [`engines.py`](../step07/implementation/engines.py) (`make_game`, the uniform
  `Game` interface + `KuhnState`), [`policies.py`](../step07/implementation/policies.py)
  (`play_hand`, `sample_action`, `tabular_policy`), and
  [`opponent_types.py`](../step07/implementation/opponent_types.py) (`make_type_zoo` — the
  exploitable archetypes that make up the ARDT mixed-opponent data).
- **Step 09** — [`learners.py`](../step09/implementation/learners.py)
  (`torch_available` / `require_torch`), with a local fallback in `deps.py`.

**Why the Decision Transformer is new code, not a HuggingFace import.** The raw step suggests
adapting HuggingFace's `DecisionTransformerModel`, but `transformers` is not a repo dependency
and the agent cannot smoke-test its version quirks. So [`implementation/decision_transformer.py`](implementation/decision_transformer.py)
is a compact, self-contained GPT-2-style DT in pure torch, with field names mirroring
`DecisionTransformerConfig` for parity — the same "write your own so it runs unchanged"
choice Step 11 made for its PPO.

---

## Scope notes (per WORKFLOW.md + the confirmed plan)

- **Kuhn is the primary, fully-validated testbed.** Its Nash/exploitability are exact
  (Step 02), so all five validation targets (raw L458-463) are checked on Kuhn. **Leduc is a
  documented SCALE-only extension**: the encoder supports it and `make_game("leduc")` works,
  but the default run is Kuhn.
- **LLM roster.** The default backend is an **offline scripted-reasoner stub** so the harness
  and comparison table run with **no GPU and no API keys**. A model-agnostic, OpenAI-chat-shaped
  client wires a **local model on the RTX 5090** (default target **gpt-oss 20B**; documented
  alternatives **Qwen2.5-7B-Instruct** and **OpenThinker3-7B**, a reasoning-SFT of the same
  Qwen2.5-7B base — a clean base-vs-reasoning-tuned comparison). Nemotron 3 Nano is deferred.
- **Units.** Step 02 exploitability is reported in **chips** (its `compute_exploitability`
  sums both players' best-response values). The raw step's "within 50 mbb/h" target is
  translated in [`implementation/README.md`](implementation/README.md) so the threshold is
  read correctly.

---

## Build status

- [x] Scaffold (this README + `implementation/deps.py` + the four phase folders)
- [x] `intuition/intuition.md`
- [x] `exploration/` (code + README) — **executed 2026-07-25**
- [x] `targetedReading/summary.md` — **MATH FLAG B resolved against the ARDT PDF**
- [x] `implementation/` (code + README + validation harness) — **executed at SMOKE 2026-07-25**
- [x] [`EXECUTION_NOTES.md`](EXECUTION_NOTES.md) — Phase 2 + Phase 4 (SMOKE) measured-vs-predicted
- [x] **Real-model LLM rows** — all 3 roster models measured (gpt-oss-20b, Qwen2.5-7B, OpenThinker3-7B)
- [x] **Deeper LLM investigation** — A1 logprob extraction (validated), A2 leak decomposition,
      B4 frequency elicitation, B5 opponent modelling, B6 exploitation-vs-zoo, C10 head-to-head
- [x] **Leduc Stage 0** — encoder/dataset/DT port + return-conditioning sweep (legal-action
      masking bug found and fixed); no exploitability/LLM on Leduc yet
- [ ] OpenThinker3 `plain` / `gametheory` rows — skipped (~9 h at ~38 s/decision); CoT row measured
- [ ] SCALE profile run
- [x] **Leduc LLM scouting** — chips/hand vs near-Nash + zoo, lazy cached logprob policy
      (only 31–54% of the 936 info sets are ever reached, so no full enumeration needed)
- [x] **[`SCOUTING_REPORT.md`](SCOUTING_REPORT.md)** — mini-report on all follow-on work
      (method advances, findings, the four measurement artefacts caught, limitations)
- [ ] Leduc Stage 1+ — exact exploitability (needs the step02/step03 `cfr` collision solved)
- [ ] `consolidation/` — deferred (human-written after runs)
- [ ] `deliverables/reports/step12/` — deferred

**Run status (SMOKE, 2026-07-25/26):** `validate.py` = **3 PASS / 2 FAIL / 0 SKIP**. Targets #1 and
#4 are honestly red — see [`EXECUTION_NOTES.md`](EXECUTION_NOTES.md) for the §0.1 reconciliations.

**Headline (exploitability in chips, lower = closer to Nash):**
**Nash-CFR 0.016 < BC 0.02–0.07 ≪ LLM 0.25–0.33 < ARDT 0.42–0.52 < DT 0.62–0.85.**
Plain behavioral cloning beats every method this step is about; a zero-shot LLM beats the Decision
Transformer. A 7B model matches a 20B one. Every LLM value-bets the King at 1.00 (Nash: 0.68) and
none bluffs the Jack under a plain prompt — they get hand *ranking* right and *frequencies* wrong.

> ⚠️ **Measurement protocol:** LLM rows **must** be run at `temperature > 0`. At temperature 0 a
> model plays a pure strategy, so every measured frequency collapses to 0.0 or 1.0 and
> exploitability becomes a lottery. Use `STEP12_LLM_TEMP=0.7` with `STEP12_LLM_SAMPLES≥24`.
