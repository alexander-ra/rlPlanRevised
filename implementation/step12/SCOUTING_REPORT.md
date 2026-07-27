# Step 12 — Scouting Report: LLM & sequence-model play beyond the headline table

**Scope.** This covers the *follow-on* work done after the main Step 12 build and its comparison
table: six deeper LLM experiments on Kuhn, a narrow Leduc port, and a Leduc LLM scouting pass.
Measured 2026-07-26/27 on an RTX 5090 with local models via LM Studio 0.4.20.

**Status of this document.** A summary of *measured* results. It is **not** the Phase 5
`consolidation/` one-pager or the EN/BG deliverable reports — per
[`../WORKFLOW.md`](../WORKFLOW.md) §4.5 those are written by hand. Full run-by-run detail,
including every reconciliation, lives in [`EXECUTION_NOTES.md`](EXECUTION_NOTES.md).

**Framing.** LLM play is *scouting the field* for this thesis, not a core contribution. Scope was
kept deliberately cheap where that was defensible, and the shortcuts are named in *Limitations*.

---

## 1. Method advances (reusable beyond this step)

| # | What | Why it matters |
|---|---|---|
| **A1** | Exact mixed-strategy extraction from **token logprobs** — prefill `"Action:"`, read `top_logprobs`, sum mass over surface forms | **24× cheaper** than sampling (12 calls / 26 s vs 288 calls / 614 s) with **zero sampling variance**. Makes Leduc-scale LLM measurement affordable at all. |
| **A2** | Per-info-set **exploitability decomposition** — patch one info set to Nash, re-measure | Turns one aggregate number into a ranked diagnosis. Self-test recovers a planted flaw at **99.4%**. |
| — | **Exact paired baselines** — full-tree expectation on the hero's own realised deals | Removes deal luck *and* opponent randomness from small-sample comparisons. |

**A1 has a validated boundary.** Against N=24 sampling on identical prompts:

| prompt style | mean \|P(bet) gap\| | binomial SE | verdict |
|---|---|---|---|
| `plain` | **0.027** | 0.102 | ✅ consistent (3.8× inside noise) |
| `cot` | 0.237 | 0.102 | ❌ discrepant |

The CoT failure is a boundary, not a bug: the prefill forces an answer at token 1 while the prompt
says "reason first". A Rao-Blackwellised variant (`reasoned_logprob_policy`) handles CoT at 2k calls.

---

## 2. Findings

### 2.1 Where the loss actually is — and it isn't where the headline said

Qwen2.5-7B, plain, 0.357 chips baseline:

| info set | P(bet) | Nash | deviation | **% of leak** |
|---|---|---|---|---|
| `2p` (Queen, opponent checked) | 1.000 | 0.000 | 1.000 | **41.4%** |
| `2b` (Queen, facing a bet) | 0.253 | 0.347 | 0.094 | 13.1% |
| `3` (King, root) | 1.000 | 0.561 | **0.439** | **0.1%** |

**This corrected an earlier headline of ours.** "Every LLM value-bets the King at 1.00 where Nash
mixes at 0.68" was reported as a signature failure; it costs **0.1%** of the leak. Over-betting a
hand that is never behind is nearly free. The damage is concentrated in the **Queen** nodes.
**Deviation magnitude and cost are nearly uncorrelated** — which is precisely what a single
exploitability number hides, and the core methodological argument for Step 14.

### 2.2 Models play *better than they can explain*

Asked, at identical info sets, what percentage of the time they should bet:

| | MAE vs Nash (stated) | MAE vs Nash (executed) | expl. if it played what it says | expl. actually played |
|---|---|---|---|---|
| Qwen2.5-7B | 0.353 | **0.246** | 0.921 chips | **0.357** (2.6× better) |
| gpt-oss-20b | 0.434 | **0.328** | 1.576 chips | **0.392** (4.0× better) |

Both models' **stated** strategies are substantially worse than their **played** ones. This
**refutes the hypothesis we went in with** (knows-the-frequency-but-cannot-sample). Different
failure modes — Qwen answers "50%" at 11/12 info sets; gpt-oss answers ~0% at 8/12 including all
three King nodes — which strengthens the shared conclusion:

> **Extracting a strategy from an LLM by *asking* it yields something worse than probing its
> behaviour.** Verbalised strategy is less informative than behaviour.

### 2.3 Exploitative by default, not adaptive

In-context opponent modelling over 120-hand sessions with observed history (exact paired baselines):

| opponent | Nash | BR ceiling | hero ± SE | gap closed | learning (2nd − 1st half) |
|---|---|---|---|---|---|
| AlwaysPass | +0.229 | +0.981 | +0.850 ± 0.056 | **+0.83 ± 0.07** | +0.00 |
| AlwaysBet | +0.319 | +0.530 | +0.383 ± 0.169 | +0.31 ± 0.80 | −0.52 |
| TightPassive | +0.088 | +0.316 | +0.092 ± 0.122 | +0.02 ± 0.53 | −0.15 |

Mean learning **−0.22**. Against the one well-powered cell it captures 83% of available exploitation
**from the first half onward and never improves** — a fixed loose-aggressive prior, not opponent
modelling. Corroborated independently by the exploitation/exploitability frontier: the LLM exploits
**61% harder than Nash while being 59× more exploitable**, but *only* against passive/random
opponents — against the two most competent archetypes it is **worse** than Nash.

### 2.4 Scale doesn't help; the ordering is transitive

4-way head-to-head, 20,000 hands/pair (Nash vs Nash = 0.0000 exactly; Nash loses to nobody):

| row player | mean chips/hand | exploitability |
|---|---|---|
| Nash-CFR | +0.104 | 0.0061 |
| **Qwen2.5-7B** | **+0.088** | 0.3571 |
| gpt-oss-20b | −0.038 | 0.3917 |
| OpenThinker3-7B | −0.153 | 0.8940 |

The **7B beats the 20B** (+0.162 chips/hand). The ordering is strictly transitive and matches the
exploitability ordering exactly — in this population, exploitability predicts head-to-head results.

### 2.5 Return conditioning fails on *both* games — for different reasons

| | Kuhn | Leduc |
|---|---|---|
| payoff alphabet | 4 values | **15 values** |
| notch at the modal return | **yes** (collapse to 1.93 chips) | **no** (0.2 SE) |
| monotone steering | no | **no** (Pearson r = **+0.062**) |
| impossible target | saturates | saturates |

This **partly refutes our own Phase 2 mechanism**. That explanation (magnitude encodes the betting
line, sign is luck, so the modal fold payoff selects "the folding line") predicted the effect should
weaken on a richer alphabet. The notch vanished exactly as predicted — **but steering did not appear
in its place.** So the payoff-alphabet story explains the Kuhn *notch* and is **not** why return
conditioning fails. The failure survives 15 payoff values, two streets and a board card, pointing at
something more fundamental: in a zero-sum imperfect-information game the realised return is
dominated by what the hero does not control.

### 2.6 LLM competence degrades sharply from Kuhn to Leduc

| | Kuhn | Leduc |
|---|---|---|
| LLM vs trained DT | LLM clearly **better** | **indistinguishable** (−0.463 ± 0.132 vs −0.454) |
| LLM vs Nash at exploiting the zoo | LLM **better** (0.177 vs 0.110) | LLM **−0.071** vs Nash **+0.582** |
| illegal-action intent | 0–1% | **23.4% of probability mass** |

On Leduc the LLM loses to **Random** (−0.200) and Maniac (−0.628), beating only the two most passive
archetypes. **Any optimism from the Kuhn table should be read as a property of Kuhn.**

### 2.7 The illegal-action failure is *one* misconception, not confusion

Reach-sampled over 220 Leduc info sets:

| category | mean mass | applies to | mean where it applies |
|---|---|---|---|
| **FOLD_WHEN_FREE** | **0.2340** | 112 sets | **0.4596** |
| RAISE_AT_CAP | 0.0000 | 36 sets | 0.0001 |
| NON_ACTION (format failure) | 0.0001 | 220 sets | 0.0001 |

**FOLD_WHEN_FREE is 100% of all illegal mass.** By situation:

| situation | mean illegal mass |
|---|---|
| round 1 / facing a bet | 0.0002 |
| round 1 / nothing due | 0.0086 |
| round 2 / facing a bet | 0.0000 |
| **round 2 / nothing due** | **0.5138** |

The model's rules comprehension is otherwise **essentially perfect** — it never tries to raise past
the 2-raise cap (0.0000) and effectively always emits a valid action token (0.0001 non-action). It
has exactly **one** systematic error, and it is sharply localised: **in the second betting round
with nothing due, it wants to fold ~51% of the time** — up to **0.99** at the worst info sets, all
of which are weak unpaired hands against a high board (`2:5|cc/` = Queen vs King board, `0:4|cc/` =
Jack vs King board).

**Interpretation:** it conflates *"my hand is weak"* with *"I should fold"*, forgetting that
checking is free. Folding a free check is strictly dominated. The error is invisible in round 1
(0.86%) because there is no board to look weak against — so this is a board-texture-triggered
impulse, not a rules gap.

---

## 3. Measurement failures caught (and what stopped them)

Four results looked like discoveries and were artefacts. Recording them because the *detection
mechanism* is the transferable part.

| # | Apparent result | Reality | Caught by |
|---|---|---|---|
| 1 | Seat-0 return −0.128 vs −1/18 → "engine bias" | 1.7 SE of sampling noise | Computing the **exact** game value (converges to −0.05555) |
| 2 | B5 "in-context learning, gap closed +1.59" | Impossible: >1 means beating the exact best response | **Hand-checking the ceiling** (+0.333 vs AlwaysBet) |
| 3 | Leduc smoke: monotone trend −0.36 → +0.33 | Noise; SE ±0.20–0.37 ≈ the whole effect | Re-running at 20× the hands (r → +0.06) |
| 4 | Leduc LLM −0.83, "loses to everything" | Decoder discarded **70% of probability mass** and *inverted* the policy | The **unmapped-mass diagnostic** |

Cause of #4: the tokenizer splits `RAISE → " RA"` and `FOLD → " F"` while `CALL`/`CHECK` stay whole,
so whole-word matching read a model raising at p=0.953 as calling ~97% of the time. Fixed with
prefix-aware matching that attributes a partial token **only when it prefixes exactly one action**
(Kuhn's `'c'` — `call`=BET vs `check`=PASS — correctly stays ambiguous).

**Standing rules this produced:** report unmapped/illegal mass rather than renormalising it away;
pair baselines on the hero's own deals; guard for physically impossible values; and treat no
performance claim below ~10³ hands as safe.

---

## 4. Limitations

- **Leduc rests on one model, one prompt style, 600 hands (SE ±0.13).** Enough to say the Kuhn
  advantage does not transfer; **not** enough to rank models on Leduc. A second model was scoped
  out. This is the single largest caveat in this report.
- **No exact Leduc exploitability.** Blocked on the step02/step03 `cfr` package collision;
  chips/hand vs near-Nash was used instead (the same yardstick as the Leduc DT, so they compare).
- **A1 is validated for `plain` prompts only**; CoT numbers come from sampling or the RB variant.
- **B5's AlwaysBet/TightPassive cells are underpowered** (±0.80, ±0.53). Only AlwaysPass is
  conclusive; tightening the others needs ~30× more hands.
- **OpenThinker3** was measured on the CoT row only (n=12); a full pass is ~9 h.
- All Kuhn LLM numbers are **SMOKE-profile**; no SCALE run.

---

## 5. What carries into Steps 13–14

1. **Return-conditioned DT is the wrong instrument on fixed logs** — now falsified on two games.
   ARDT's relabeling matters precisely because it swaps an uncontrollable conditioning target for a
   controllable one.
2. **ARDT's `Q(s,a)` vs our `V(s)`** — the paper relabels with a state-**action** value via two
   coupled networks (Alg. 1 line 7; Eqs. 8–11). Our state-only proxy cannot distinguish "this state
   is bad" from "*this action* is bad", the top candidate fix for Step 13.
3. **A single exploitability number hides the diagnosis** (§2.1) — the concrete argument for Step
   14's evaluation framework.
4. **Probe behaviour, don't ask** (§2.2) — relevant to any LLM-based opponent-modelling component.
5. **Logprob extraction + reach-weighted sampling** make LLM measurement affordable at scale: only
   **31–54%** of Leduc's 936 info sets were ever reached.

---

## 6. Artifact index

| Script | Produces |
|---|---|
| `logprob_policy.py`, `validate_logprob.py` | A1 extraction + its validation |
| `exploitability_decomposition.py` | A2 per-info-set leak attribution |
| `frequency_elicitation.py` | B4 stated vs executed |
| `opponent_modeling.py` | B5 in-context adaptation |
| `exploitation_vs_zoo.py` | B6 exploitation/exploitability frontier |
| `llm_head_to_head.py` | C10 tournament |
| `leduc_stage0.py` | Leduc DT return-conditioning sweep |
| `leduc_llm.py` | Leduc LLM scouting |
| `leduc_illegal_taxonomy.py` | §2.7 illegal-action breakdown |

Results in `implementation/results/*.json`, raw stdout in `implementation/logs/*.log`.
