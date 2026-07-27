# Step 12 — Execution Notes (measured-vs-predicted dev log)

This is the running dev log for **executing** the Step 12 phases that were authored (unexecuted) in
the `step12 initial` commit. It follows WORKFLOW §0.1: predictions written during authoring are kept
in place; here we record **what actually happened on a real run**, suspect bugs before blaming a
prediction, and keep honest FAILs red.

## Run environment

- **Date:** 2026-07-25
- **Machine / interpreter:** Windows 11, repo venv `.venv/Scripts/python.exe`
- **Python:** 3.12.10
- **Packages:** numpy 2.4.6 · matplotlib 3.11.0 · torch 2.11.0+cu128
- **GPU:** NVIDIA GeForce RTX 5090, `torch.cuda.is_available() = True` → the neural probes ran on
  **cuda**. Because torch is present, **nothing SKIPs**.
- **LLM serving:** no local server was installed at the start of this session (LM Studio and Ollama
  both absent; ports 1234 / 11434 closed). Setting one up is part of this session — see
  *Phase 2 — real-model wiring* below.

---

## Phase 2 — Exploration

Ran all three scripts from `implementation/step12/exploration/`. Stdout-only (no artifacts written).

### Measured vs predicted

| Script | Prediction | Measured | Verdict |
|---|---|---|---|
| `luck_vs_skill_coinflip` | `P(action=B \| R=1.0) ≈ 1.00` while A is EV-optimal | `E[A]=0.500`, `E[B]=0.400`; `P(B\|R=1.0)=1.00` (n=39,985); `P(A\|R=0.5)=1.00` | ✅ **exact** |
| `dt_return_conditioning` — monotone trend | exploitability **falls** as target return rises across `{-2,-1,+1,+2}` | `-2: 0.6717`, `-1: **1.9269**`, `+1: 0.6801`, `+2: 0.6841` chips — **flat**, with a large spike at `-1`; and `expl(+2) > expl(-2)` | ❌ **prediction wrong** (real effect — see reconciliation) |
| `dt_return_conditioning` — OOD probe | the impossible `+3` **saturates or degrades** | `+3: 0.6834` vs `+2: 0.6841` → indistinguishable, no further gain | ✅ **saturates**, as predicted |
| `llm_kuhn_repl` (offline stub) | K value-bets, J folds to a bet / occasionally bluffs, Q checks; 0% illegal | exactly that (hand 3 K→BET, hand 6 J→bluff-BET called for −2, Q checks); **0% illegal over 9 calls** | ✅ **exact** |

### §0.1 reconciliation — why return conditioning did not steer

The headline prediction ("higher target return → lower exploitability") failed. Per §0.1 I suspected a
bug first and ran a targeted diagnostic (full 12-info-set strategy per target, a fine RTG grid, and the
data's own return distribution) before accepting the result.

**It is not a bug — the DT responds to the conditioned return, sharply:**

- **The metric is sane.** Near-Nash CFR (3,000 iters) on the same exact ruler scores **0.0372 chips**,
  i.e. ≈ 0. The DT's ~0.65 is genuinely far from Nash, not a broken measurement.
- **The model is not ignoring RTG.** A fine sweep of `P(bet)` at info set `3` (root, King):

  | R | −3.0 | −2.0 | −1.5 | **−1.0** | −0.5 | 0.0 | +1.0 | +2.0 | +3.0 |
  |---|---|---|---|---|---|---|---|---|---|
  | P(bet) | 0.747 | 0.681 | 0.505 | **0.020** | 0.436 | 0.655 | 0.744 | 0.769 | 0.781 |

  Outside the notch it is smooth and monotone increasing; **at exactly R = −1 it collapses to PASS**.
- **What the notch is.** `R = −1` is the *modal* return in the data (**41.7%** of all steps; vs +1 32.6%,
  −2 14.3%, +2 11.4%), and it is the payoff of **folding** (or losing the ante-only pot). Conditioning
  on it selects the folding line: at R = −1 the DT passes at 11 of 12 info sets (≈0.00–0.02), which is
  maximally exploitable → **1.98 chips**.

**The real lesson (a sharper version of Paster's point).** In Kuhn the *magnitude* of the return encodes
**which betting line was played** (|R| = 2 ⇒ someone bet and was called; |R| = 1 ⇒ a fold or check-check),
while the *sign* encodes **who held the better card** — pure luck. So return-to-go conditions the DT on
*the shape of the hand*, not on how well it was played, and the sign it does carry is exactly the part
the hero does not control. That is why `expl(+2) ≈ expl(−2)`: both select "the betting line", and the
DT cannot use the sign for anything. The takeaway the step is built on ("return-to-go conflates luck
with skill") **survives and is strengthened** — but the *mechanism* is not the predicted monotone
degradation, it is a line-selector with a sharp mode at the fold payoff.

**Consequence for Phase 4:** validation **target #1** (`expl(high RTG) < expl(low RTG)`, with
high = +2 and low = −2) is expected to **FAIL** on this evidence. It is a genuine finding, not a
threshold to tune.

*(The diagnostic was a separate training run; its per-target numbers — `−2: 0.5328`, `−1: 1.9771`,
`+1: 0.6532`, `+2: 0.6498`, `+3: 0.6473` — differ slightly from the probe's because of RNG-init
ordering, but reproduce the same structure: flat elsewhere, spike at −1, `expl(+2) > expl(−2)`.)*

### Findings to carry into Phase 4 (implementation)

1. **Target #1 is predicted red** (above). Do not tune `TARGET_RETURNS` to make it pass.
2. **Target #2 should pass comfortably.** The per-card strategies at high conditioning are strongly
   card-dependent (root `P(bet)` = 1.00 / 0.05 / 0.77 for J / Q / K), far above the 0.10 spread threshold —
   though note the *direction* is odd (the Jack bets more than the Queen), itself worth a look.
3. **Extraction/training timestep mismatch (caveat, not yet a fix).** `extract_dt_strategy` queries every
   info set with a length-1 sequence at `timestep = 0`, including second-ply sets (`1pb`, `2pb`, `3pb`
   and all P1 sets) that occurred at `t ≥ 1` during training. The encoder carries the betting history so
   the info set is still identified, but the timestep embedding is mismatched. This is the
   implementation README's own "single-step conditioning in extraction" risk; flagging it as a possible
   contributor to the DT's distance from Nash.
4. **Data-quality gate needs a per-seat split.** The pooled episode return is `+0.0000` (correct for a
   zero-sum game, both seats in one dataset), so the predicted `−1/18` seat-0 asymmetry cannot be read
   off the pooled mean — check it per seat in Phase 4.

### Run-driven fix

- **`train_dt.py:64`** emitted `UserWarning: Converting a tensor with requires_grad=True to a scalar` on
  every epoch (`float(loss)` inside the logging accumulator). Cosmetic but noisy across every training
  call; fixed with `float(loss.detach())`. No effect on training or results. (Same one-line fix applied
  to `ardt.py` ×2 and `behavioral_cloning.py`.)

---

## Phase 2b — Real-model wiring (gpt-oss-20b)

LM Studio **0.4.20** installed via winget (`ElementLabs.LMStudio`). Note: the GUI must be launched
**once by hand** before `lms bootstrap` works ("Cannot find LM Studio installation"), and a GUI app
cannot be started from a non-interactive session — so this step needs a human click, and that is
where the session stalled until the owner opened it. Server: `lms server start` on port 1234.

**Served id ≠ preset id.** `GET /v1/models` reports **`openai/gpt-oss-20b`**, publisher-qualified;
the authored preset guessed the bare `"gpt-oss-20b"`. Presets corrected, and the client now raises a
helpful error listing what *is* served instead of a bare 404.

### Two authored predictions about reasoning models — one wrong, one still open

| Prediction (authored) | Measured on gpt-oss-20b | Verdict |
|---|---|---|
| Reasoning arrives mixed into `content`; `max_tokens=256` truncates before the `Action:` line ⇒ inflated illegal rate | LM Studio returns a **separate `reasoning` field**; `content` holds just the answer (`**Action: BET**`). 99 completion tokens (30 reasoning), `finish_reason=stop`, **0 truncations** at 256 | ❌ **prediction wrong for gpt-oss** — the split channel makes the small budget safe |
| Long CoT inflates latency | ~2.4–3.0 s/call warm | ⚠️ modest here; still expected to bite on OpenThinker3 (inline `<think>`) |

The `<think>`-stripping and `max_tokens` knobs were kept anyway — they are needed for the *inline*
reasoning style (OpenThinker3), just not for gpt-oss. `max_tokens` is now per-preset (512 for
gpt-oss/Qwen, 4096 for OpenThinker3) and truncations are counted rather than silently mis-scored.

### The bug only a real model could expose — every seat-1 prompt was mis-narrated

`_describe_history` labelled action index 0 as **"You"** unconditionally, i.e. it assumed the agent
always sits in seat 0. But the agent is queried at **all 12** Kuhn info sets, **six of which belong
to seat 1**. History `"b"` therefore rendered as:

```
Your private card: King.
Betting so far: You bet.        <- WRONG: that was the OPPONENT's bet
You are facing a bet.           <- ...so the prompt contradicts itself
```

**Measured consequence (gpt-oss-20b, temperature 0): it FOLDED THE KING to a bet** — a strictly
dominated play. After the fix (`who = "You" iff i % 2 == len(history) % 2`) it calls. The offline
stub is blind to this (it reads only the card and a "facing a bet" flag), so **no amount of
stub-based testing could have caught it** — and it would have silently corrupted half of every LLM
row. Any seat-1 LLM number taken before this fix is invalid.

**Post-fix gpt-oss-20b strategy (temp 0, all 12 info sets, 0% illegal, 0 truncated):**

| Card | root | facing bet | after opp. check | check-then-bet |
|---|---|---|---|---|
| J | PASS | PASS | PASS | PASS |
| Q | **BET** | BET | PASS | BET |
| K | BET | BET | BET | BET |

Coherent, and honestly non-Nash in two specific ways: it **over-bets the Queen at the root** (Kuhn
Nash never bets Q first) and **never bluffs the Jack** (Nash bluffs J with probability α > 0). That
is the "LLMs fail informatively" result the step is after — a *named* deviation, not a leaderboard
number.

### Methodology finding: you cannot measure an LLM's mixed strategy at temperature 0

The SMOKE profile sets `llm_temperature = 0.0` — a sensible default when the backend is the
deterministic offline stub, and **the wrong setting for a real model**. Three runs of *the same*
config against gpt-oss-20b produced:

| run | samples | expl plain | expl CoT | expl game-theory | bluff(J) game-theory | adapt |
|---|---|---|---|---|---|---|
| 1 | 4 | 0.4583 | 0.3750 | 0.3333 | **0.75** | +0.00 |
| 2 | 4 | 0.5833 | 0.2917 | 0.3333 | **0.25** | +1.00 |
| 3 | **24** | 0.3333 | 0.4931 | 0.4931 | **1.00** | +0.04 |

Raising the sample count from 4 to 24 did **not** stabilise it, which rules out simple Bernoulli
noise and identifies the real mechanism: **at temperature 0 the model plays a PURE strategy.** Every
one of the N samples at an info set returns the same action, so the estimated frequency degenerates
to exactly 0.0 or 1.0 and `bluff(J)` can only ever read 0 or 1 — never Nash's 0.23. Exploitability
then becomes a *lottery over which pure strategy the model happened to land on* that run (MoE
routing under batched serving is not bit-reproducible, so it does not even land on the same one).

**Consequence: every LLM frequency in the SMOKE-default table is an artifact of temperature, not a
property of the model.** Measuring a mixed strategy requires `temperature > 0` (SCALE already uses
0.7). Added `STEP12_LLM_TEMP` and `STEP12_LLM_SAMPLES` overrides; the headline LLM measurement is
re-run at temperature 0.7 with 24 samples. This is a *measurement-protocol* result and it applies
to the whole LLM-vs-Nash comparison, so it carries directly into Step 14's evaluation framework:
**a single greedy-decode run cannot characterise an LLM's strategy in a game that requires mixing.**

**Confirmed by the re-run (gpt-oss-20b, temperature 0.7, 24 samples):** every frequency is now
genuinely intermediate rather than 0/1 — `bluff(J)` = 0.00 / 0.08 / **0.46**, `adapt` = +0.67 /
+0.79 / +0.25 — so the mixed strategy is measurable exactly as the diagnosis predicted. **And the
illegal-move rate became nonzero (1%)**, which retires an open prediction: the authored README
expected "a nonzero illegal-move rate with a real model", and at temperature 0 we measured a flat
0%. The prediction was right, but it only manifests *under sampling* — greedy decoding hides it.

### OpenThinker3-7B: the reasoning-tuned model is a different animal

This is the model the `<think>`/`max_tokens` guards were written for, and unlike gpt-oss it does
put its trace **inline** in `content` (field `reasoning_content` exists but is empty — note the name
differs from gpt-oss's `reasoning`; the client now checks both).

**Measured cost per single Kuhn decision** (temperature 0.7):

| | gpt-oss-20b | OpenThinker3-7B | ratio |
|---|---|---|---|
| completion tokens | 99 | **~6,500** | **66×** |
| latency | ~2.8 s | **34–43 s** | ~13× |

**At the authored `max_tokens=4096` it never finishes thinking.** Three probes all returned
`finish_reason=length`, ~18,000 characters of open `<think>` with **no `</think>` and no action
committed**. It needs ~6,500 completion tokens, and the request only fits if the model is *loaded*
with a bigger context (`lms load openthinker3-7b --context-length 32768`; the 8192 default leaves
no room). Preset raised to `max_tokens=16000`, with the load requirement documented next to it.

**A measurement-honesty bug in my own earlier fix.** The first version of the `<think>` handling
fell back to scanning the *whole* string when `</think>` was missing, so it scraped a poker verb out
of the unfinished monologue and returned a confident `BET` — reporting `parsed_ok=True` and
`illegal=0%` for a model that had **not answered at all**. That is precisely the "invent a
plausible-looking result" failure §0 warns about, introduced while fixing something else. Now an
unclosed `<think>` returns `None` and is counted as unparseable, which is the honest reading.

Two smaller real deviations: OpenThinker3 writes **`Action/PASS`** rather than the requested
`Action: PASS` (the separator class now accepts `/` and `=`, since punctuation drift is not an
illegal *move*), and it sometimes ends with prose only ("...by passing!") with no directive at all —
which correctly counts as unparseable. On the King-first-to-act probe it concluded **PASS**, i.e. it
checks the best hand.

**Scope decision (owner-approved).** A full 3-style × 24-sample pass is 864 calls ≈ **9 hours** for
this model. Measured instead on the **CoT row only at n=12** (~288 calls, ~1.5 h), which preserves
the scientifically interesting comparison — OpenThinker3-7B is a reasoning-SFT of the *same*
Qwen2.5-7B base, so CoT-vs-CoT isolates the effect of reasoning tuning. The `plain` and
`gametheory` rows are left **unmeasured and reported as absent**, not defaulted. Added
`STEP12_LLM_STYLES` for this.

### Operational: exactly ONE loaded instance per model, and never rely on JIT

Three separate failure modes, one underlying lesson.

1. **JIT auto-load is unreliable.** Two runs died on
   `HTTP 400: Failed to load model … Engine protocol startup was aborted`, while an explicit
   `lms load` of the *same* model succeeded in **3.6 s**. Requests arriving while another model is
   loading or serving trigger it.
2. **Killing a run mid-request poisons the server; only a server restart clears it.** Batch runs hung
   indefinitely — **~2 CPU-seconds consumed over 24–33 minutes**, GPU pinned at 0%, model `IDLE`,
   and the client's 180 s timeout never fired (the socket stayed open, so there was nothing to time
   out on). CPU time matched "CFR finished, then blocked on the very first HTTP request."
   Ad-hoc single requests still succeeded throughout, which is what made it look like a client bug.
   *Wrong first diagnosis:* I blamed duplicate instances (`lms load X` does add a second `X:2`
   rather than reusing X, and tidying that up did coincide with the one successful run). Removing
   the duplicate did **not** fix it — the next run wedged identically with exactly one instance
   loaded. The actual cause is stale server-side state from the runs I had killed mid-request: with
   `PARALLEL 4`, the orphaned connections hold every slot and new requests queue forever.
   **`lms server stop && lms server start` fixed it immediately** — a validation run then completed
   end-to-end in under a minute.
   **Protocol: after any killed/crashed run, restart the server, `lms unload --all`, `lms load
   <model> --ttl <n>`, confirm `lms ps` shows exactly one row, then run.**
3. **Buffered output hides all of this.** Under `Tee-Object` the hung run produced a **0-byte log**
   for 33 minutes — indistinguishable from "still starting up". Running `python -u` with a direct
   `>` redirect made the header appear immediately, which is how the second hang was caught in
   minutes instead of half an hour.

None of this is a defect in the step's own code, but all of it is required to get a trustworthy
real-model measurement, so it belongs in the runbook for Step 13's larger sweeps.

### Real-model results — the roster measured (temperature 0.7)

Protocol: `STEP12_PROFILE=SMOKE`, temperature **0.7** (mandatory — see the temperature finding
above), exactly one model instance loaded, server restarted between models. Files:
`results/comparison_SMOKE_<model>.json`, one bar figure per backend.

| Backend | style | expl (chips) | bluff J | value-bet K | illegal | adapt |
|---|---|---|---|---|---|---|
| **Nash-CFR** (reference) | — | **0.0162** | 0.23 | 0.68 | — | — |
| **BC** (best learned) | — | **0.020–0.065** | 0.20–0.24 | 0.65–0.71 | — | — |
| gpt-oss-20b (n=24) | plain | 0.2760 | 0.00 | 1.00 | 0% | +0.67 |
| gpt-oss-20b (n=24) | **CoT** | **0.2500** | 0.08 | 1.00 | 1% | +0.79 |
| gpt-oss-20b (n=24) | game-theory | 0.3316 | 0.46 | 1.00 | 1% | +0.25 |
| Qwen2.5-7B (n=24) | plain | 0.3125 | 0.00 | 1.00 | 0% | +0.00 |
| Qwen2.5-7B (n=24) | CoT | 0.3183 | 0.58 | 1.00 | 0% | +0.42 |
| Qwen2.5-7B (n=24) | game-theory | 0.3032 | 0.50 | 1.00 | 0% | +0.21 |
| OpenThinker3-7B (n=12) | CoT | 0.2882 | **0.33** | 1.00 | **16%** | **+0.92** |
| ARDT | — | 0.42–0.52 | 0.34–0.40 | 0.39–0.43 | — | — |
| DT | — | 0.62–0.85 | 1.00 | 0.61–0.75 | — | — |

**1. Scale buys nothing here.** Qwen2.5-**7B** (0.303–0.318) matches gpt-oss-**20B** (0.250–0.332)
despite being ~3× smaller. Kuhn does not reward knowledge or scale; it rewards *mixing at the right
frequency*, which none of them do.

**2. Every LLM beats both trained sequence models, and all lose badly to BC.** The ordering is
**Nash (0.016) < BC (0.02–0.07) ≪ LLM (0.25–0.33) < ARDT (0.42–0.52) < DT (0.62–0.85)**. A zero-shot
LLM with no training and no search is less exploitable than the Decision Transformer this step is
built around — while plain behavioral cloning, the dumbest baseline present, is ~15× better than any
LLM and lands within 0.004 chips of Nash on its best run.

**3. Two failures are universal across models and prompts.** Every backend value-bets the King at
**1.00** where Nash mixes at 0.68, and **no model bluffs the Jack at all under the plain prompt**
(0.00 for both gpt-oss and Qwen). LLMs play the *ranking* of hands correctly and the *frequencies*
wrongly — they cannot mix.

**4. Reasoning tuning: a real but expensive improvement (the base-vs-SFT pair).** OpenThinker3-7B is
a reasoning-SFT of the *same* Qwen2.5-7B base, so the CoT rows isolate the effect:

| CoT row | expl | bluff J (Nash 0.23) | illegal | adapt | tokens/decision |
|---|---|---|---|---|---|
| Qwen2.5-7B (base) | 0.3183 | 0.58 | 0% | +0.42 | ~100 |
| OpenThinker3-7B (reasoning-SFT) | **0.2882** | **0.33** | **16%** | **+0.92** | ~6,500 |

Reasoning tuning **improved every strategic metric** — lower exploitability, bluff frequency far
closer to Nash (0.58 → 0.33 vs 0.23), strongest opponent adaptation of any run (+0.92) — and paid
for it with a **16% illegal-move rate** and **65× the tokens**. *Caveat: n=12 and a single style, so
this is one clean observation, not a tight interval; the other two styles were not run (~9 h).*

**5. The illegal-move prediction is confirmed, and only by the honest parser.** The authored README
predicted "a nonzero illegal-move rate with a real model". Measured: 0% (Qwen), 1% (gpt-oss), **16%
(OpenThinker3)**. The 16% is real unparseable output — replies whose `<think>` never closed, plus
prose-only endings with no action directive — and it would have read as a **false 0%** under the
first version of my `<think>` fix, which scraped a verb out of unfinished reasoning.

---

## Phase 4b — Deeper LLM investigation (experiments A1, A2, B4, B5, B6, C10)

Six follow-on experiments, run 2026-07-26/27 on Qwen2.5-7B and gpt-oss-20b. Motivated by a
structural limit of everything above: `strategy_extraction` queries each info set *independently*
with a length-1 sequence, so every LLM number so far describes a **static, memoryless policy**, and
"adaptation" was measured by *describing* an opponent in the prompt rather than letting the model
observe one.

### A1 — exact mixed strategies from logprobs (and where it is NOT valid)

Prefill the assistant turn with `"Action:"`, request `top_logprobs`, and read the action
distribution directly: **one call per info set, zero sampling variance**. Mass must be summed over
surface forms (`' BET'`, `'BET'`, `' Bet'`, `' PAS'`), otherwise the top token alone reports a
*pure* strategy.

`validate_logprob.py` compared it against N=24 sampling on the same prompts (qwen2.5-7b, temp 0.7):

| style | mean \|P(bet) gap\| | binomial SE | verdict |
|---|---|---|---|
| **plain** | **0.027** | 0.102 | ✅ CONSISTENT (3.8× inside the noise floor) |
| cot | 0.237 | 0.102 | ❌ DISCREPANT (2.3× outside) |

Cost on the plain run: **12 calls / 26 s vs 288 calls / 614 s — 24× fewer calls.**

**The CoT failure is not a bug, it is a boundary.** The CoT prompt says "think step by step, THEN
answer"; the prefill forces the answer at token 1, so we measure an out-of-distribution
"gut reaction" rather than the model's CoT policy (0.832 vs 0.350 chips for the same prompt sampled
properly). Added `reasoned_logprob_policy`: sample k reasonings, read the logprob distribution after
each, average. That is Rao-Blackwellisation, not a free lunch — a CoT policy mixes through *two*
channels (which reasoning it produces, and the action given that reasoning); logprobs integrate out
the second exactly, the first still needs sampling. Cost 2k calls instead of 1, but far lower
variance per unit budget than k coin flips. **All exact-extraction experiments below therefore use
the `plain` style, where A1 is validated.**

### A2 — where the leak actually is (and why the headline was misleading)

`exploitability_decomposition.py` patches one info set at a time to Nash and re-measures with the
exact metric. Self-test: on a strategy that is Nash everywhere except it folds the King to a bet, it
attributes **99.4%** of the leak to exactly that node. Qwen2.5-7B (plain, 0.3571 chips baseline):

| info set | P(bet) | Nash | deviation | % of leak |
|---|---|---|---|---|
| `2p` (Q, opponent checked) | 1.000 | 0.000 | 1.000 | **41.4%** |
| `2b` (Q, facing a bet) | 0.253 | 0.347 | 0.094 | 13.1% |
| `1` (J, root) | 0.006 | 0.183 | 0.177 | 8.3% |
| `2` (Q, root) | 1.000 | 0.001 | 0.999 | 5.1% |
| `3` (K, root) | 1.000 | 0.561 | **0.439** | **0.1%** |

**This corrects an earlier headline in these notes.** Phase 4 reported "every LLM value-bets the
King at 1.00 where Nash mixes at 0.68" as a signature failure. A2 shows that error is **almost
free** (0.1% of the leak) — over-betting a hand that is never behind costs almost nothing. The
damage is concentrated in the **Queen** nodes, above all `2p`: always betting the Queen after the
opponent checks is **41% of the total loss**, and fixing that single decision would take the model
from 0.357 to 0.209 chips. **Deviation magnitude and cost are nearly uncorrelated**, which is
exactly what a single aggregate number hides. Top-3 nodes = 63% of the leak.

### B4 — the models play BETTER than they can explain (the strongest result here)

Asked, at the same 12 info sets with byte-identical situation text, "what percentage of the time
should you BET here?", then scored a strategy built from their own answers:

| | MAE vs Nash (stated) | MAE vs Nash (executed) | expl if it played what it says | expl actually played |
|---|---|---|---|---|
| Qwen2.5-7B | 0.353 | **0.246** | 0.921 chips | **0.357** (2.6× better) |
| gpt-oss-20b | 0.434 | **0.328** | 1.576 chips | **0.392** (4.0× better) |

**Both models' stated strategies are substantially WORSE than their played strategies**, on both
metrics, on every comparison. This **refutes the hypothesis I went in with** (that models know the
right frequency but cannot sample it). It is not an execution gap — it is that verbalised strategy
is *less* informative than behaviour.

The two failure modes differ, which strengthens the result rather than weakening it:
- **Qwen answers "50%" at 11 of 12 info sets** — including with the King (Nash 1.000) and the Jack
  facing a bet (Nash 0.000). A generic hedge whenever asked to name a frequency.
- **gpt-oss answers near-zero at 8 of 12** ("bet ~1% of the time"), including all three King nodes
  where Nash bets 100%. It also failed to produce a parseable number **8/36** times.

**Implication for the thesis:** any method that extracts a strategy from an LLM by *asking* it will
get something worse than the model's own play. Behavioural probing is not merely more convenient
than introspection here — it is more accurate.

### B5 — no in-context opponent modelling (after fixing a broken measurement)

**First run reported "evidence of in-context learning, mean gap closed +1.59" — that was an
artefact and is retracted.** `gap_closed > 1` means beating the *exact best response*, which is
impossible. Against AlwaysBet it showed the hero at +0.617 chips/hand when the theoretical ceiling
is **+0.333** (K→+2, Q→0, J→−1 over three equally likely cards) — a figure I checked by hand, which
matched the computed BR of +0.3387 and so identified the *hero* number as the artefact.

**Cause:** a 60-hand session was compared against baselines sampled over their *own, different*
deals. Kuhn's per-hand std is ~1.2, giving SE ≈ 0.155 on 60 hands — comparable to the entire
Nash→BR span — so unpaired deal luck dominated. **Fix:** baselines are now computed **exactly**
(full tree expectation, no sampling) on the **hero's own realised deal sequence**, halves get their
own paired baselines, hero SE is reported, and an `exceeds_ceiling` guard flags impossible results.

Corrected (qwen2.5-7b, CoT, 120 hands, history of the last 20 hands in context):

| opponent | Nash | BR ceiling | hero ± SE | gap closed ± SE | learning (2nd − 1st half) |
|---|---|---|---|---|---|
| AlwaysPass | +0.229 | +0.981 | +0.850 ± 0.056 | **+0.83 ± 0.07** | +0.00 |
| AlwaysBet | +0.319 | +0.530 | +0.383 ± 0.169 | +0.31 ± 0.80 | −0.52 |
| TightPassive | +0.088 | +0.316 | +0.092 ± 0.122 | +0.02 ± 0.53 | −0.15 |

**Conclusion reverses: exploitative but NOT learning** (mean learning **−0.22**). Against the one
well-powered cell (AlwaysPass, ±0.07) it captures 83% of the available exploitation *from the first
half onward* and never improves. That is a **fixed loose-aggressive prior**, not opponent modelling
— exactly what B6 independently shows. Honest caveat: the AlwaysBet and TightPassive cells have SEs
of ±0.80 and ±0.53 (their Nash→BR spans are narrow), so only AlwaysPass is conclusive; tightening
the others needs ~30× more hands (~4.5 h of calls).

### B6 — the safe-exploitation trade-off, measured

Extract the static policy once (12 calls), then simulate 4,000 hands per opponent call-free:

| agent | expl | AlwaysPass | AlwaysBet | TightPassive | LooseAggr | Thresholdish | Random | **mean** |
|---|---|---|---|---|---|---|---|---|
| Nash-CFR | 0.0061 | 0.168 | 0.129 | −0.006 | 0.162 | 0.087 | 0.119 | **0.110** |
| Qwen (plain) | 0.3571 | **0.374** | 0.191 | **−0.047** | 0.198 | 0.079 | **0.267** | **0.177** |

The LLM **exploits 61% harder than Nash while being 59× more exploitable** — but the gain is
entirely against *passive/random* opponents (AlwaysPass 0.374 vs 0.168; Random 0.267 vs 0.119).
Against the two most competent archetypes it is **worse than Nash** (TightPassive −0.047 vs −0.006;
Thresholdish 0.079 vs 0.087). Loose aggression prints against weak opposition and leaks against
real players — the exploitation/exploitability frontier of thesis contribution #2, on one plot.

### C10 — head-to-head, and exploitability predicts it

4 entrants × 20,000 hands/pair, seats alternated, all from cached static strategies (call-free).
Sanity checks pass: Nash vs Nash = 0.0000 exactly, and Nash loses to nobody.

| row player | vs Nash | vs gpt-oss | vs OpenThinker3 | vs Qwen | **mean** | expl |
|---|---|---|---|---|---|---|
| Nash-CFR | 0.0000 | +0.1061 | +0.1245 | +0.0806 | **+0.104** | 0.0061 |
| Qwen2.5-7B | −0.0806 | **+0.1618** | +0.1817 | 0.0000 | **+0.088** | 0.3571 |
| gpt-oss-20b | −0.1061 | 0.0000 | +0.1535 | −0.1618 | −0.038 | 0.3917 |
| OpenThinker3-7B | −0.1245 | −0.1535 | 0.0000 | −0.1817 | −0.153 | 0.8940 |

1. **The 7B beats the 20B head-to-head** (+0.162 chips/hand), reinforcing that Kuhn rewards mixing,
   not scale.
2. **The ordering is strictly transitive and matches the exploitability ordering exactly**
   (Qwen 0.357 < gpt-oss 0.392 < OpenThinker3 0.894). In this population exploitability *predicts*
   head-to-head results — not guaranteed in general (cf. the spinning-top/non-transitivity
   literature and Step 11's own cyclic findings), but it holds cleanly here.
3. **OpenThinker3 has no usable immediate-action distribution: 34% unmapped mass** at the action
   token under a plain prompt (vs 0.02% for Qwen, 0.17% for gpt-oss) — it wants to emit `<think>`.
   Its 0.894 chips here is therefore **not comparable** to its 0.288 under CoT: the plain row
   measures a model being asked to do something it structurally cannot. The honest headline for it
   is the 34% figure, not the exploitability.

### What these six add up to

The static-policy picture from Phase 4 survives, but the *explanation* changes. LLMs are not
"uniformly sloppy": they are near-optimal on hand ranking, nearly free-of-charge wrong on the
King, catastrophically wrong on one Queen node, incapable of stating what they do, and
exploitative-by-default rather than adaptive. **Every one of those is invisible in a single
exploitability number**, which is the methodological argument for Step 14's evaluation framework.

---

## Phase 4c — Leduc Stage 0: is the Kuhn return-conditioning result a toy-game artefact?

Narrow by design: encoder + dataset + DT training + a return-conditioning sweep scored by **actual
performance** (chips/hand vs a near-Nash opponent). No exact exploitability (that needs step03,
whose `cfr` package collides with step02's), no LLM, no ARDT.

### Porting: every flagged Leduc blocker cleared, and one was a real bug

| Blocker (flagged earlier) | Outcome |
|---|---|
| `make_cfr_policy` raises for non-Kuhn | Fixed — routes to step07 `solve_nash_cached`. Note its 2nd return value differs by game (step02 `node_map` for Kuhn, CFR `table` for Leduc); documented at the call site. |
| `PokerStateEncoder` on 2 streets + board | Works unchanged, `state_dim=35` (Kuhn 17) |
| `PokerTrajectoryDataset` | Works unchanged; 15 distinct return values, ≤4 decisions/player/hand |
| **Unmasked illegal actions** | **A REAL BUG, now fixed.** Leduc states have 2 *or* 3 legal actions and `action_probs` softmaxes over all of `act_dim`. At smoke size the DT put **1.4–3.5%** of its probability mass on illegal actions; well-trained it drops to ~0.02–0.6%, but never to zero. In Kuhn all actions are always legal, so this was structurally unobservable. Masking + renormalisation added, with the illegal mass reported as a diagnostic. |

Data sanity: seat-0 mean return **−0.115 ± 0.025** (Leduc's first-mover disadvantage), and the
payoff alphabet is **15 values** {−13…+13} vs Kuhn's 4, with **−1 still modal but at 20.1%** rather
than Kuhn's 41.7%.

### Result (40k trajectories, 20k CFR iters, 40 epochs, 4,000 hands per target)

| target R | chips/hand vs near-Nash | ± SE | data share |
|---|---|---|---|
| −13 | −0.277 | 0.104 | 0.5% |
| −5 | **−0.878** | 0.059 | 8.5% |
| −1 (modal) | −0.454 | 0.025 | 20.1% |
| 0 | −0.801 | 0.070 | 17.4% |
| +7 | −0.286 | 0.097 | 3.3% |
| +13 | −0.369 | 0.098 | 0.5% |
| **+15 (impossible)** | −0.366 | 0.097 | 0% |

- **The Kuhn notch does NOT reproduce.** At the modal return the DT is **0.2 SE** from the mean of
  the other targets — no collapse, nothing like Kuhn's jump to 1.93 chips exploitability where it
  passed at 11 of 12 info sets.
- **But conditioning still does not steer.** Pearson **r = +0.062**, Spearman **ρ = −0.054**, slope
  **+0.0014** chips per unit of target return. Higher targets do not produce better play.
- **Conditioning is not inert, though**: the spread across targets is **0.60 chips/hand**, many
  times the per-point SE, so the target materially changes the policy — just not in an order
  related to how good the target is. Worst at R=−5 and R=0, best at R=−13 and R=+7.
- **The impossible +15 saturates** (−0.366, indistinguishable from the high real targets) —
  the one Kuhn prediction that reproduces cleanly.
- The DT **loses to near-Nash at every target** (−0.28 to −0.88 chips/hand), consistent with Kuhn.

### §0.1 reconciliation — this refines the Phase 2 mechanism, and partly refutes it

The Phase 2 notes explained the Kuhn behaviour as: *the return's magnitude encodes which betting
line was played (|R|=2 ⇔ a bet was called, |R|=1 ⇔ a fold), its sign is card luck, and R=−1 — the
modal fold payoff — therefore selects "the folding line"*. That explanation predicted the effect
should **weaken or vanish on a richer payoff alphabet.** Half of that prediction is confirmed and
half is refuted:

- ✅ **The notch vanished**, exactly as the mechanism predicts, when the alphabet went 4 → 15 values
  and the modal share 41.7% → 20.1%.
- ❌ **Steering did not appear.** If the notch were the only thing suppressing return conditioning,
  removing it should have let "higher target → better play" emerge. It did not (r ≈ 0.06).

**So the payoff-alphabet story explains the Kuhn *notch*, but it is NOT why return conditioning
fails.** The failure is more fundamental and survives a 15-value ladder, two betting streets and a
board card. The likeliest remaining explanation — consistent with Paster et al. and now with two
games — is that in a zero-sum imperfect-information game the realised return is dominated by
factors the hero does not control (the opponent's private card and their actions), so conditioning
on it cannot systematically select better play no matter how finely the payoffs are graded. That is
a stronger and more transferable claim than the Kuhn-only version, and it is the one that should
carry into Step 13: **on fixed poker logs, return-conditioned DT is the wrong instrument; the
value of ARDT-style relabeling is precisely that it replaces an uncontrollable target with a
controllable one.**

### Honest note on the smoke run

A 2,000-trajectory / 200-hand-per-target smoke pass showed an apparent **monotone rise** from −0.36
at R=−13 to +0.33 at R=+13, which looked like "conditioning works on Leduc". At that size the
per-point SE was **±0.20–0.37** — comparable to the entire apparent effect. At 4,000 hands
(SE ±0.02–0.10) it is flat (r = +0.06). **The trend was noise.** Recorded because it is the third
time this session a small-sample pattern looked like a discovery (see also the seat-0 scare in
Phase 2 and the retracted B5 "in-context learning" result); the standing lesson is that no
performance claim in this step is safe below ~10³ hands.

---

## Phase 4d — Leduc LLM scouting (Stage 1-lite)

Deliberately cheap, per the owner's framing that LLM play is *scouting the field*, not a thesis
contribution. Two choices kept it so:

- **No exact exploitability.** Scored by chips/hand vs near-Nash — the same yardstick
  `leduc_stage0.py` used for the DT, so LLM and DT are directly comparable — which sidesteps the
  step02/step03 `cfr` collision entirely.
- **No 936-info-set enumeration.** The policy queries lazily and caches by info-set string, so
  reach probability does the subsetting for free.

### Two porting complications (both real, both fixed)

**1. Leduc card ids are 0–5, not ranks 0–2.** `rank = card // 2` (0,1=J; 2,3=Q; 4,5=K), matching
`state_encoding.py:167`. The first deal is `(0,1,2)`, which *looks* like ranks, so the prompt code
worked until a King (id 4/5) appeared and raised `KeyError: 5`. The subtler half: the "does your
card pair the board" check compared card **ids**, so it would have told the model a Jack never
pairs the other Jack. Fixed; verified over all 120 deals × 6 lines (0 failures, pair message
correctly shown 72×). **The encoder already used `// 2`, so Stage 0's DT results are unaffected.**

**2. Tokenizer-split action words INVERTED the measured policy.** qwen2.5-7b tokenises
`RAISE → ' RA'` and `FOLD → ' F'` while `CALL`/`CHECK` stay whole. Exact whole-word matching
discarded **70% of the probability mass** and read a model that wanted to raise at **p=0.953** as
calling ~97% of the time. The first Leduc run therefore produced a confident, plausible, and
**entirely wrong** result (−0.83 chips/hand, losing to every zoo archetype) — discarded.

Fixed with prefix-aware matching (`map_token`), which attributes a partial token **only when it
prefixes exactly one action**. Critical safety property, verified: in Kuhn `'c'` could begin `call`
(BET) or `check` (PASS), so it must stay unmapped rather than be guessed — it does. The Kuhn A1
self-test is byte-identical, so **all earlier Kuhn results stand** (their unmapped mass was already
0.02%). Kuhn never exposed this because `' BET'`/`' PASS'` happen to be single tokens.

### Result (qwen2.5-7b, plain, temp 0.7, 600 hands vs near-Nash, seats alternated)

| | chips/hand vs near-Nash |
|---|---|
| **LLM (qwen2.5-7b)** | **−0.463 ± 0.132** |
| DT (return-conditioned, modal target) | −0.454 |
| Nash vs Nash | 0 by construction |

| opponent | LLM | ± SE | Nash |
|---|---|---|---|
| CallingStation | +0.310 | 0.140 | +0.669 |
| LoosePassive | +0.223 | 0.160 | +0.589 |
| Rock | −0.060 | 0.173 | +0.340 |
| Random | −0.200 | 0.188 | +0.735 |
| Maniac | −0.628 | 0.270 | +0.575 |
| **MEAN** | **−0.071** | | **+0.582** |

**1. The LLM's Kuhn advantage evaporates.** On Kuhn a zero-shot LLM clearly beat the trained DT
(0.25–0.33 vs 0.62–0.85 exploitability). On Leduc the two are **statistically indistinguishable**
(−0.463 ± 0.132 vs −0.454), both bleeding ~0.46 chips/hand to near-Nash.

**2. Its exploitation collapses.** On Kuhn the LLM *out-exploited* Nash against the zoo (0.177 vs
0.110 chips/hand). On Leduc it manages **−0.071 vs Nash's +0.582** — it cannot beat weak opponents
at all, losing even to **Random** (−0.200) and to Maniac (−0.628). Kuhn's "loose aggression prints
against passive opponents" does not survive two streets and a board card.

**3. Only a third to a half of the info sets are ever needed.** 293 distinct info sets (**31.3%**
of 936) covered 600 hands vs near-Nash; 507 (**54.2%**) covered every match including the zoo.
Reach probability does the subsetting automatically, so full enumeration is unnecessary —
confirming the owner's instinct and making Leduc LLM measurement affordable.

**4. Substantial illegal-action intent (~25% of probability mass).** After the tokenizer fix the
residual unmapped mass is **not** a decoding artefact — it is the model wanting to take actions
that are not legal. It is dominated by **folding when folding is illegal**: at `'2:5|rc/'`, where
nothing is due and checking is free, it puts **p=0.983 on FOLD**. Folding a free check is strictly
dominated, and this is the Leduc analogue of Kuhn's illegal-move rate — a direct measure of rules
comprehension, and far worse here than Kuhn's 0–1%.

### Illegal-action taxonomy — ONE misconception, not diffuse confusion

Reach-sampled 220 Leduc info sets, reading the raw 3-action mass *without* masking:

| category | mean mass | applies to | mean where it applies |
|---|---|---|---|
| **FOLD_WHEN_FREE** | **0.2340** | 112 sets | **0.4596** |
| RAISE_AT_CAP | 0.0000 | 36 sets | 0.0001 |
| NON_ACTION (format failure) | 0.0001 | 220 sets | 0.0001 |

**FOLD_WHEN_FREE is 100% of the illegal mass.** Rules comprehension is otherwise essentially
perfect: the model **never** tries to raise past the 2-raise cap (0.0000 over 36 applicable sets)
and effectively always emits a valid action token (0.0001 non-action). By situation:

| situation | mean illegal mass | info sets |
|---|---|---|
| round 1 / facing a bet | 0.0002 | 23 |
| round 1 / nothing due | 0.0086 | 12 |
| round 2 / facing a bet | 0.0000 | 85 |
| **round 2 / nothing due** | **0.5138** | 100 |

Sharply localised: **in the second betting round with nothing due it wants to fold ~51% of the
time**, rising to **0.99** at the worst info sets — every one of which is a weak unpaired hand
against a high board (`2:5|cc/` Queen vs King board, `3:4|cc/` Queen vs King, `0:4|cc/` Jack vs
King). It conflates *"my hand is weak"* with *"I should fold"*, forgetting that checking is free;
folding a free check is strictly dominated. The near-zero rate in round 1 (0.86%) shows this is
**board-texture-triggered, not a rules gap** — there is no board to look weak against before the
flop. A one-line prompt fix ("you may check for free") would likely remove most of it, which makes
this a *prompting* finding rather than a capability ceiling.

**Net scouting read:** LLM poker competence degrades sharply from Kuhn to Leduc. On the toy game
LLMs looked competitive with trained sequence models and better than Nash at punishing weak
opponents; one street and one board card later they are no better than the DT, cannot exploit
anybody, and want to make illegal folds a quarter of the time. Any optimism from the Kuhn table
should be read as a property of Kuhn.

### Transient 400s ⇒ the client now retries

A full comparison pass is 150+ sequential requests. The first gpt-oss run died at ~90 calls with
`HTTP 400`; the identical request succeeded seconds later — LM Studio JIT-unloads an idle model and
a request arriving mid-reload is rejected. Not a defect in our code, but fatal to a multi-minute
batch. `OpenAICompatClient` now retries transient HTTP/transport failures 3× with exponential
backoff, surfaces the **response body** in the error (the original handler only did so for 404, which
is why the first failure was opaque), and counts `transient_errors`. The model is also pinned with
`lms load --ttl 7200` so it cannot unload mid-run.

---

## Phase 4 — Implementation (SMOKE)

Ran the [implementation README](implementation/README.md) runbook from
`implementation/step12/implementation/`, profile **SMOKE**, device **cuda**, LLM = offline stub.
Artifacts: `results/{comparison,dt_experiments,tau_sweep}_SMOKE.json`, 4 PNGs, `logs/*.log`.

### Module self-tests — all exit 0

`deps`, `state_encoding` (kuhn dim 17 / leduc 35, 0 validity failures), `trajectory_dataset`,
`strategy_extraction` (12/12 info sets), `evaluation` (Nash-CFR 0.0284 chips ≈ 0), `llm_agent`
(0% illegal, parse-robustness OK), `decision_transformer` (shapes OK, 26,594 params),
`ardt`, `behavioral_cloning`, `plotting`.

### Two real bugs found by running (neither is a prediction miss)

**1. `config` module hijack — broke `comparison_table.py` and `validate.py` outright.**
Both died with `ImportError: cannot import name 'active_config' from 'config'
(.../step02/config.py)`. `deps.py` deliberately *appends* prior steps so Step 12's own modules win —
but that is not sufficient: `step02/evaluate/best_response.py:23` and
`step02/evaluate/exploitability.py:20` each run `sys.path.insert(0, <step02 dir>)` at **module**
level (their own standalone-script bootstrap). Step 12 imports those two **lazily**, inside
`evaluation.py`'s functions, so the insert fires *in the middle of a run* and pushes step02 ahead of
this folder. A `sys.path` trace confirmed it — step02 ends up at positions 0 **and** 1:

```
[sys.path append]    .../implementation/step02          <- deps.py, by design
[sys.path insert@0]  .../implementation/step02          <- step02/evaluate/*, mid-run
[sys.path insert@0]  .../implementation/step02
final sys.path[0:3] = [step02, step02, step12/implementation]
```

`config.py` is the only name Step 12 shares with the step02 root, so it is the only casualty.
**Fix:** `deps.py` now pins Step 12's own `config` into `sys.modules` by explicit file path at
bootstrap, so every later `from config import …` hits the cache and is immune to path *order*.
Verified: with step02 still sitting at `sys.path[0]`, `config` resolves to Step 12's.
This is the same class of trap as the documented `cfr` collision — worth carrying into Step 13.

**2. Prompt contamination faked an LLM result.** The first comparison table showed
`LLM-gametheory` at **1.667 chips vs 0.833** for plain/CoT — which reads as "the game-theory prompt
makes it worse." It was an artifact: `ScriptedReasonerClient._extract_card` scanned the **whole**
prompt for the first card name, and the game-theory instruction text itself names every card
("with the King bet/call for value; with the Jack you must sometimes BLUFF…"), so the stub played
**every hand as a Jack** under that style. Fixed by anchoring on the explicit
`"Your private card: X."` line. After the fix all three styles score identically (0.8333) — correct,
since the stub is not a real reasoner and ignores style. **A real model is where style should
matter; this row can only become meaningful with a real backend.**

### Data-quality gate — a false alarm, now instrumented

`trajectory_dataset`'s self-test prints seat-0 mean return **−0.1280** against the target −1/18
(−0.0556), which looks alarming. Suspecting a bug first, I computed the CFR policy's **exact** game
value by enumerating all 6 deals × all action sequences (no Monte Carlo):

| cfr_iters | exact value P0 | gap vs −1/18 | exploitability |
|---|---|---|---|
| 500 | −0.06145 | −0.00590 | 0.0673 |
| 3,000 | −0.05587 | −0.00032 | 0.0372 |
| 20,000 | −0.05548 | +0.00007 | 0.0085 |
| 200,000 | −0.05555 | +0.00000 | 0.0026 |

The engine and generator are **correct** — the value converges to −1/18 to five decimals and
exploitability decreases monotonically. The −0.1280 was pure sampling noise: n=1000, std=1.33 ⇒
**SE 0.042**, so the reading is **1.7 SE** from the true value. The self-test invited the false alarm
by printing a sample mean with no error bar, so `return_stats()` now reports `se` and the self-test
prints the distance in SE with an OK / INVESTIGATE verdict.

### `validate.py --config SMOKE` — 3/5 PASS, 0 SKIP

| # | Check | Result | Verdict |
|---|---|---|---|
| 1 | DT high-RTG < low-RTG exploitability | high(+2)=0.6981 vs low(−2)=0.6928 chips | **FAIL** |
| 2 | DT action varies by card (luck) | root P(bet) J/Q/K = 1.00/0.03/0.70, **spread 0.97** ≫ 0.10 | **PASS** |
| 3 | ARDT < standard DT (same mixed data) | **ARDT 0.5034 vs DT 0.7212** chips | **PASS** |
| 4 | ARDT within ~50 mbb/h of Nash | ARDT 0.5034 vs tol 0.05 chips (gap 0.4872) | **FAIL** |
| 5 | LLM honestly more exploitable than Nash | LLM 0.8333 > Nash 0.0162; bluff(J)=1.00, illegal 0% | **PASS** |

**Target #1's FAIL was predicted in Phase 2 and is a genuine finding**, not a threshold to tune: the
DT keys on the *magnitude* of the conditioned return (which betting line was played), and the sign
— who won — carries almost no strategy signal in Kuhn. Both ±2 select "the betting line", so they
score within 0.005 chips of each other. **Target #4 stays red**: at 0.50 chips ARDT is 10× outside
the aspirational 0.05 tolerance. That is not close enough to blame on SMOKE size alone — see the
τ-sweep reconciliation below.

### Comparison table (`results/comparison_SMOKE.json`)

| Method | expl (chips) | expl (mbb/h) | bluff J | value-bet K | illegal | adapt |
|---|---|---|---|---|---|---|
| Nash-CFR | **0.0162** | 16.2 | 0.23 | 0.68 | — | — |
| BC | **0.0546** | 54.6 | 0.22 | 0.74 | — | — |
| ARDT | 0.4585 | 458.5 | 0.40 | 0.43 | — | — |
| DT | 0.6709 | 670.9 | 1.00 | 0.69 | — | — |
| LLM-plain / CoT / game-theory | 0.8333 | 833.3 | 1.00 | 1.00 | 0% | +0.00 |

**The headline surprise: plain behavioral cloning is the best learned method by an order of
magnitude** (0.055 chips, within 0.04 of Nash), while the return-conditioned DT is 12× worse
(0.671). On near-Nash self-play data BC simply copies a near-Nash policy, whereas the DT must route
that same policy through a return-conditioning channel that — per the Phase 2 finding — carries
mostly luck. **Return conditioning actively destroys information here.** ARDT recovers part of it
(0.459 < 0.671) but nowhere near BC. That ordering (BC ≪ ARDT < DT < LLM) is the honest story of
this step, and it is *not* the one the raw step anticipated.

> **§0.1 note added during the deliverables pass (2026-07-27) — the table above is superseded by a
> later re-run, and the gap is training variance.** The numbers above come from the FIRST stub run,
> taken before results were tagged per backend. The committed artifact
> `results/comparison_SMOKE_stub.json` (timestamp `2026-07-26T07:02:06`) is a later re-run of the
> **same config**, and it is what the deliverables cite:
>
> | Method | this table (1st run) | committed JSON (re-run) |
> |---|---|---|
> | Nash-CFR | 0.0162 | 0.0162 (identical — CFR is seeded) |
> | BC | 0.0546 | **0.0550** |
> | ARDT | 0.4585 | **0.4691** |
> | DT | 0.6709 | **0.7992** |
> | LLM (stub) | 0.8333 | 0.8333 (identical — the stub is deterministic) |
>
> The two deterministic rows reproduce **exactly**, which localises the difference: the dataset and
> CFR are seeded, but each `comparison_table.py` invocation **retrains** the neural models, and the
> torch RNG state differs between invocations. So DT exploitability moves **0.671 → 0.799** across
> re-runs of an identical configuration — a ~19% swing, larger than several effects discussed
> elsewhere in this file. **Consequence: single-run DT/BC/ARDT numbers carry meaningful training
> variance and should not be compared at 3 decimal places across runs.** The qualitative ordering
> (BC ≪ ARDT < DT < LLM) is unaffected — BC still beats the DT by 14×. Neither table is wrong; the
> original is kept per §0.1 and the committed JSON is authoritative because it is the artifact on
> disk.

### MATH FLAG B — RESOLVED, and the two halves disagree

**Definition (settled, twice).** ARDT **Eq. (6)** `L^α_ER(u) = E[|α − 1(u>0)|·u²]` with **Eq. (7)**
`lim_{α→0} g_α = min`, `lim_{α→1} g_α = max`. So **low τ is the pessimistic side** — the raw step's
"τ=0.9 = pessimistic" is inverted, exactly as the flag claimed. Independently confirmed by
`ardt.py`'s own self-test, which recovers the *analytic* expectiles of a skewed sample
(τ=0.1 → −1.951, τ=0.9 → 0.000; both exact for 90%×(−2) + 10%×(+2)). The paper runs **α = 0.01**
(Algorithm 1, line 1), 10× more aggressive than our default.

**Behaviour (`tau_sweep.py`, 3 paired seeds, `results/tau_sweep_SMOKE.json`).**

| τ | expl (chips) ± SE | mean relabel target |
|---|---|---|
| 0.01 (paper) | 0.5023 ± 0.0255 | −0.626 |
| 0.10 (our default) | 0.5038 ± 0.0294 | −0.351 |
| 0.50 (mean) | 0.4905 ± 0.0272 | +0.193 |
| **0.90 (optimistic)** | **0.3864 ± 0.0313** | +0.854 |
| vanilla DT | 0.7310 ± 0.0029 | (baseline) |
| Nash | 0.0173 ± 0.0032 | (anchor) |

The relabel target moves **monotonically** with τ (−0.626 → +0.854), so the mechanism is wired
correctly and the convention is confirmed a third time. **But exploitability is LOWEST at τ=0.9 —
the optimistic side — the opposite of what ARDT theory predicts** (≈2.7 SE below our default; every
τ still beats the DT baseline, so target #3 passes at all τ).

**§0.1 reconciliation.** I do not think this refutes ARDT; I think it exposes what our proxy drops.
Reading the paper closely (Algorithm 1, line 7) the relabel target is **`R̃_t = Q̃_ν(s_t, a_t)` — a
state-ACTION value** produced by two *coupled* networks (Eq. 8/9, nested min-max per Eq. 10/11).
Our `MinimaxReturnEstimator` is **state → scalar**, so it relabels with `V(s)` and cannot separate
"this state is bad" from "*this action* in this state is bad" — which is precisely the
discrimination that makes ARDT pick the robust action. With a state-only target, pushing τ toward 0
just hands the DT a uniformly negative number, and — by the Phase 2 finding — conditioning a Kuhn DT
on a strongly negative return selects **the folding line** (the R=−1 collapse, P(bet)≈0 at 11 of 12
info sets). So low τ recreates the pessimistic *fold*, not the robust *strategy*. The τ=0.9 win is
that artifact in reverse, not evidence that optimism is right.

**Decision:** `EXPECTILE_TAU` stays at **0.1**. It is the theoretically correct side per Eq. (7),
and switching to 0.9 to buy a better number would be rigging the result (WORKFLOW §0.1: report,
don't rig). The honest headline is *"our single-sided, state-only proxy does not reproduce ARDT's
advantage; the state-action formulation is the missing piece"* — a concrete, well-evidenced hand-off
to Step 13.

### Figures — the fabricated-figure hazard, closed

`plotting.py` shipped with **only** a `_selftest()` that plotted hard-coded numbers
(`{"DT": 0.20, "ARDT": 0.05}`) into `results/`. It was the sole PNG-producing path in the step, so
following the runbook literally would have committed a **fabricated figure** — a direct §0
violation. (It did: the first runbook pass wrote `results/exploitability_bars.png` from those fake
numbers; that file was deleted and regenerated from real data.) Replaced with a `main()` that renders
only from `results/*.json`, and `train_dt.py` now persists its two experiments so there is something
real to render. Four figures, all traceable to committed JSON: `return_conditioning.png`,
`bet_prob_by_card.png`, `exploitability_bars.png`, `tau_sweep.png`.

### Still outstanding

- **Real-model LLM rows.** All LLM numbers above come from the offline stub, which is legal by
  construction (0% illegal) and style-insensitive — so targets around bluff frequency, illegal
  moves and prompt style are only *mechanically* exercised, not answered. LM Studio 0.4.20 was
  installed this session and `openai/gpt-oss-20b`, `Qwen2.5-7B-Instruct` and `OpenThinker3-7B` are
  downloading; the GUI needed a manual first launch (it cannot be started from a non-interactive
  session), which is why this is deferred.
- **SCALE profile** not yet run.
