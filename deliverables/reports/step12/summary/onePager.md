# Step 12 — Consolidation (internal weave)

> Phase 5 of Step 12. Written **after** the code was executed, from **verified** run artifacts only
> (`implementation/results/*.json`, `implementation/logs/*.log`, and the measured-vs-predicted dev
> log [`../EXECUTION_NOTES.md`](../EXECUTION_NOTES.md)). This is the internal weave of the per-phase
> "Key takeaways"; the external write-up lives in `deliverables/reports/step12/`.
>
> **Artifact caveats (read once).**
> 1. **Two results were retracted mid-session and are superseded.** The first B5 run reported
>    "in-context learning, gap closed **+1.59**" — impossible, since >1 means beating the exact best
>    response; and the first Leduc LLM run reported **−0.83 chips/hand** from a decoder that
>    discarded 70% of the probability mass. Both were re-run after fixes; the committed JSONs hold
>    only the corrected values. The retracted numbers appear below **only as retractions**.
> 2. **The Nash reference differs by CFR budget.** `comparison_SMOKE_*.json` uses
>    `cfr_iters=5000` → **0.0162 chips**; the follow-on experiments (A2/B4/B6/C10) use 50,000 →
>    **0.0061 chips**. Both are ≈0; quote the one matching the experiment.
> 3. **OpenThinker3's `plain` row is not comparable to its `cot` row.** Under a plain prompt it puts
>    **34% of its mass on non-action tokens** (it wants to emit `<think>`), so its 0.8940 there
>    measures a model being asked to do something it structurally cannot; its honest number is the
>    CoT row (0.2882).
> 4. **All Leduc LLM conclusions rest on one model, one prompt style, 600 hands** (SE ±0.13).
> 5. **The neural rows carry training variance.** Datasets, CFR and the offline stub are seeded and
>    reproduce exactly, but each `comparison_table.py` invocation retrains DT/BC/ARDT. Across two
>    runs of an identical config, DT moved **0.671 → 0.799** (~19%) while the deterministic rows
>    (Nash 0.0162, stub 0.8333) reproduced to four decimals. Quote the committed JSON, and do not
>    compare these rows at three decimal places across runs.

---

## The one-sentence step

Take the two "post-classical" ways to play a game — **train a transformer to predict good moves from
past hands** (Decision Transformer, and its adversarially-robust variant ARDT) and **just ask an
LLM** — score both against the *exact* Kuhn Nash benchmark from Step 02, and discover that the
step's two nominal subjects finish **last**: plain behavioural cloning beats them all, a zero-shot
LLM beats the trained DT, return conditioning never steers (on Kuhn *or* Leduc), and the single
exploitability number that ranks them hides where the loss actually is.

---

## What each experiment actually showed (measured)

| Experiment | Prediction | Measured (verified artifact) | Verdict |
|---|---|---|---|
| Data quality — seat-0 mean return | ≈ −1/18 (−0.0556) | exact CFR value converges to **−0.05555** (200k iters); the alarming sample −0.128 was **1.7 SE** noise | confirmed (§R0) |
| Target #1 — DT high-RTG < low-RTG | high beats low | `high(+2)=0.6981` vs `low(−2)=0.6928` chips — tied, order wrong | **FAIL**, real (§R1) |
| Target #2 — DT action varies by card | spread ≥ 0.10 | J/Q/K root `P(bet)` = `1.00/0.03/0.70`, spread **0.97** | PASS |
| Target #3 — ARDT < DT on mixed data | ARDT lower | `ARDT 0.5034` vs `DT 0.7212` chips | PASS |
| Target #4 — ARDT within 50 mbb/h of Nash | ≤ 0.05 chips | `0.5034` chips — 10× outside | **FAIL**, real (§R2) |
| Target #5 — LLM more exploitable than Nash | yes | `0.8333` > `0.0162` (stub); real models `0.25–0.33` | PASS |
| Comparison table (SMOKE, stub) | DT/ARDT competitive | **BC 0.055 ≪ ARDT 0.469 < DT 0.799 < LLM 0.833**, Nash 0.016 | BC wins (§R3) |
| Real-model roster (temp 0.7, n=24) | CoT ≥ plain; nonzero illegal | gpt-oss `0.276/0.250/0.332`; Qwen `0.313/0.318/0.303`; OpenThinker3 CoT `0.288` | confirmed |
| Temperature protocol | — | at temp 0 every frequency degenerates to 0/1; `bluff(J)` read 0.75, 0.25, 1.00 across identical runs | protocol finding (§R7) |
| MATH FLAG B — τ direction | raw step's τ=0.9 "pessimistic" is inverted | ARDT Eq. 6/7: α→0 is the min; paper runs **α=0.01** (Alg. 1) | flag **correct** (§R2) |
| τ sweep (3 paired seeds) | low τ → lower exploitability | relabel target moves monotonically `−0.626 → +0.854`, but exploitability is **lowest at τ=0.9** (`0.3864` vs `0.5038`) | contradicts theory (§R2) |
| A1 — logprob vs sampling | equivalent, cheaper | `plain` gap **0.027** vs SE 0.102 (consistent), **24× cheaper**; `cot` gap 0.237 (discrepant) | validated with a boundary (§R8) |
| A2 — leak decomposition | — | `2p` = **41.4%** of the leak; `3` (King, deviation 0.439) = **0.1%**; top-3 = 63% | deviation ≠ cost (§R3) |
| B4 — stated vs executed | knows but cannot sample | stated is **worse**: Qwen `0.921` vs `0.357`; gpt-oss `1.576` vs `0.392` chips | **hypothesis refuted** (§R4) |
| B5 — in-context opponent modelling | learns from observed play | mean gap closed `+0.38`, mean **learning −0.22**; AlwaysPass `+0.83 ± 0.07`, flat across halves | no learning (§R5) |
| B6 — exploitation vs the zoo | — | LLM mean `0.177` vs Nash `0.110` chips/hand, while **59× more exploitable**; worse than Nash vs the 2 competent archetypes | trade-off measured (§R5) |
| C10 — head-to-head (20k hands/pair) | scale helps | **Qwen-7B beats gpt-oss-20B `+0.162`**; ordering strictly transitive and matches exploitability | scale irrelevant (§R6) |
| Leduc Stage 0 — return conditioning | notch is a 4-payoff artefact | notch **gone** (modal gap −0.2 SE) but steering **still absent** (Pearson `r = +0.062`) | half-refutes §R1's mechanism |
| Leduc LLM scouting | LLM advantage carries over | LLM `−0.463 ± 0.132` ≈ DT `−0.454`; vs zoo `−0.071` vs Nash `+0.582` | advantage lost (§R6) |
| Leduc illegal taxonomy | diffuse rule confusion | **FOLD_WHEN_FREE = 100%** of illegal mass; RAISE_AT_CAP `0.0000`; round 2/nothing due `0.5138` | one misconception |

Validation harness net: **`validate.py` (SMOKE) = 3 PASS / 2 FAIL / 0 SKIP**, both FAILs honestly
red and reconciled below.

---

## The reconciliations (kept predictions + what really happened)

Per WORKFLOW §0.1 the pre-run predictions are kept; what actually happened is appended.

### R0 — Three "findings" that were measurement artefacts, and one that was a fabricated figure
Four separate results looked like discoveries and were not: (a) a seat-0 return of `−0.128` vs
`−1/18`, which the **exact** game-value computation showed to be **1.7 SE** of sampling noise;
(b) B5's `+1.59` gap closed, impossible against an exact best-response ceiling that was verified by
hand (`K→+2, Q→0, J→−1 ⇒ +0.333`, matching the computed `+0.3387`); (c) a Leduc smoke-run monotone
trend that vanished at 20× the hands; (d) the pre-fix Leduc LLM `−0.83`, produced by a decoder that
discarded 70% of the probability mass. Separately, `plotting.py` shipped with **only** a `_selftest`
that wrote **hard-coded numbers** into `results/` — the sole PNG-producing path in the step, so
following the runbook literally committed a **fabricated figure**. Standing rules this produced:
report unmapped/illegal mass rather than renormalising it away; pair baselines on the hero's own
deals; guard for physically impossible values; render figures only from committed JSON; and treat no
performance claim below ~10³ hands as safe.

### R1 — Return conditioning never steers, and the proposed mechanism was only half right
Target #1 failed: `expl(+2)` and `expl(−2)` land within `0.005` chips. Diagnostics showed the DT
*does* respond to the conditioned return — a fine sweep of `P(bet)` at the King root runs
`0.747 → 0.020 → 0.781` — with a **sharp collapse at exactly R = −1**, the modal payoff (41.7% of
steps) and the payoff of *folding*: at R = −1 the DT passes at **11 of 12** info sets, scoring
**1.98 chips**. The mechanism proposed at the time: in Kuhn the return's *magnitude* encodes which
betting line was played (|R|=2 ⇔ a bet was called, |R|=1 ⇔ a fold), while its *sign* is card luck —
so conditioning selects the shape of the hand, not the quality of play. **Leduc tested that and
half-refuted it.** With 15 payoff values instead of 4 the notch **vanished** exactly as the
mechanism predicts (modal gap −0.2 SE) — **but steering did not appear in its place**
(`r = +0.062`, `ρ = −0.054`). Conditioning is not inert (spread across targets `0.60` chips/hand,
many times the per-point SE); it simply is not ordered by how good the target is. So the
payoff-alphabet story explains the Kuhn **notch** and is **not** why return conditioning fails. The
failure survives 15 payoff values, two streets and a board card — pointing at something more
fundamental: in a zero-sum imperfect-information game the realised return is dominated by what the
hero does not control (the opponent's card and actions).

### R2 — MATH FLAG B: the flag was right about τ, and understated the structural gap
The raw step (L347-360) writes `τ=0.9` and calls it "pessimistic"; the authored code flagged this as
inverted and defaulted to `0.1`. **The paper confirms the flag.** ARDT **Eq. (6)**
`L^α_ER(u) = E[|α − 1(u>0)|·u²]` with **Eq. (7)** `lim_{α→0} g_α = min`, `lim_{α→1} g_α = max`, and
Algorithm 1 line 1 runs **α = 0.01** — 10× more aggressive than our default. Independently confirmed
by `ardt.py`'s own self-test, which recovers the *analytic* expectiles of a skewed sample
(τ=0.1 → −1.951, τ=0.9 → 0.000). **But the empirical sweep contradicts the theory**: the relabel
target moves monotonically with τ (`−0.626 → +0.854`, so the mechanism is wired correctly), yet
exploitability is **lowest at τ = 0.9** — the optimistic side. Reading Algorithm 1 line 7 explains
why: ARDT relabels with **`R̃_t = Q̃_ν(s_t, a_t)`, a state-ACTION value** produced by two coupled
networks (Eqs. 8–11, nested min-max), whereas `MinimaxReturnEstimator` is `state → scalar` and
relabels with `V(s)`. A state-only target cannot distinguish "this state is bad" from "*this action*
is bad" — the exact discrimination ARDT needs — so pushing τ→0 just hands the DT a uniformly
negative number, which (by R1) selects the *folding* line rather than the *robust* one. **Decision:
`EXPECTILE_TAU` stays at 0.1** — the theoretically correct side; switching to 0.9 to buy a better
number would be rigging (§0.1: report, don't rig). Target #4 stays red at `0.5034` vs the `0.05`
tolerance, and the `Q(s,a)` formulation is the named fix for Step 13.

### R3 — Behavioural cloning wins, and deviation size does not predict cost
The step is built around DT and ARDT; **plain BC beats both by an order of magnitude** (`0.055`
chips, within `0.04` of Nash, vs DT `0.799`). On near-Nash self-play data BC simply copies a
near-Nash policy, while the DT must route that same policy through a return-conditioning channel
that (R1) carries mostly luck — **return conditioning actively destroys information here.** A2 then
overturned the step's own headline: "every LLM value-bets the King at 1.00 where Nash mixes at 0.68"
was reported as a signature failure, and it costs **0.1%** of the leak — over-betting a hand that is
never behind is nearly free. The damage is one Queen node: `2p` (always betting the Queen after a
check) is **41.4%** of total exploitability, and fixing that single decision alone would take the
model from `0.357` to `0.209` chips. **Deviation magnitude and cost are nearly uncorrelated.**

### R4 — The models play better than they can explain (the going-in hypothesis was wrong)
The hypothesis entering B4 was "the model knows the right frequency but cannot sample from it" — an
execution gap. **The data says the opposite.** Scored as a strategy, each model's *stated*
frequencies are substantially worse than its *played* ones: Qwen `0.921` vs `0.357` chips (2.6×),
gpt-oss `1.576` vs `0.392` (4.0×); MAE against Nash is worse for stated in both cases. The failure
modes differ — Qwen answers **"50%" at 11 of 12** info sets, gpt-oss answers **~0% at 8 of 12**
including all three King nodes where Nash bets 100% — which strengthens rather than weakens the
shared conclusion: **verbalised strategy is less informative than behaviour**, so extracting a
strategy from an LLM by *asking* it yields something worse than probing it.

### R5 — Exploitative by default, not adaptive
B5's corrected result: mean gap closed `+0.38` but mean **learning −0.22**. Against the one
well-powered cell (AlwaysPass, ±0.07) the model captures **83%** of available exploitation **from
the first half onward and never improves**. That is a fixed loose-aggressive prior, not opponent
modelling — corroborated independently by B6, where the LLM exploits **61% harder than Nash while
being 59× more exploitable**, but *only* against passive/random opponents (AlwaysPass `0.374` vs
`0.168`); against the two most competent archetypes it is **worse** than Nash. The earlier
"adaptation" metric in `evaluation.py` measured prompt-following (the opponent was *described*), not
opponent modelling; B5 is the first real test and it comes back negative.

### R6 — Scale is irrelevant, and the LLM advantage is a property of Kuhn
C10: **Qwen-7B beats gpt-oss-20B head-to-head (+0.162 chips/hand)**, and the 4-way ordering is
strictly transitive and matches the exploitability ordering exactly. Kuhn rewards *mixing at the
right frequency*, which neither model does — not knowledge or scale. On Leduc the LLM's Kuhn
advantage **evaporates**: statistically indistinguishable from the DT (`−0.463 ± 0.132` vs `−0.454`)
and unable to beat weak opponents at all (`−0.071` vs Nash's `+0.582`), losing even to **Random**.
Its residual **23.4% illegal-action intent** is a single misconception — `FOLD_WHEN_FREE` is
**100%** of it, concentrated in round 2 with nothing due (`0.5138`, up to `0.99`), on weak unpaired
hands against a high board. Rules comprehension is otherwise essentially perfect (`RAISE_AT_CAP`
`0.0000`; non-action `0.0001`), so this is **board-texture-triggered and a prompting finding**, not
a capability ceiling.

### R7 — You cannot measure an LLM's mixed strategy at temperature 0
SMOKE sets `llm_temperature = 0.0` — correct for the deterministic offline stub, **wrong for a real
model**. At temperature 0 the model plays a **pure** strategy, so all N samples at an info set
return the same action and every measured frequency degenerates to exactly 0.0 or 1.0: `bluff(J)`
read `0.75`, `0.25` and `1.00` across three runs of the *same* config, and raising N from 4 to 24
did not help (which is what ruled out Bernoulli noise). At temperature 0.7 the frequencies become
genuinely intermediate and the **illegal-move rate becomes nonzero (1%)** — retiring an open
prediction that greedy decoding had hidden. A measurement-protocol result that applies to the whole
LLM-vs-Nash comparison, and therefore to Step 14.

### R8 — Exact extraction is 24× cheaper, within a validated boundary
Reading the action distribution from **token logprobs** (prefill `"Action:"`, sum mass over surface
forms) replaces 288 sampled calls with **12**, with zero sampling variance — validated against
sampling at `plain` (mean gap `0.027` vs SE `0.102`). It is **not** valid with a CoT prompt: the
prefill contradicts "reason first", giving an out-of-distribution policy (`0.832` vs `0.350` chips).
Two decoding traps were found and fixed: probability mass **splits across surface forms**
(`' PASS'`/`'PASS'`/`' PAS'`), and on Leduc the tokenizer **splits action words** (`RAISE → ' RA'`,
`FOLD → ' F'`) so whole-word matching discarded 70% of the mass and *inverted* the policy. Prefix
matching attributes a partial token only when it prefixes exactly one action — Kuhn's `'c'`
(`call`=BET vs `check`=PASS) correctly stays ambiguous.

---

## Threads handed to the deliverables / next steps

- **The ARDT `Q(s,a)` fix is the highest-value follow-up (R2).** Replacing the state-only
  `MinimaxReturnEstimator` with the paper's coupled state-action estimators (Eqs. 8–11) is the named,
  evidence-backed reason our proxy underperforms, and it is what Step 13 needs on fixed logs. Add
  the Algorithm-1 warm-up (initialise both networks with the original returns-to-go) at the same time.
- **Return-conditioned DT is the wrong instrument on fixed poker logs (R1).** Falsified on two games
  now. The value of ARDT's relabeling is precisely that it swaps an *uncontrollable* conditioning
  target for a controllable one — that is the argument to carry into Step 13, not the DT itself.
- **A single exploitability number hides the diagnosis (R3).** Step 14's evaluation framework should
  report a per-decision decomposition, not a scalar; deviation magnitude is not a proxy for cost.
- **Probe behaviour, don't ask (R4).** Any LLM-based opponent-modelling component should read
  behaviour (logprobs/play), not self-reported strategy.
- **Config/measurement defaults, evidence-based, left as human design choices:** raise
  `llm_temperature` above 0 for any real-model measurement (R7); prefer `plain`-style logprob
  extraction where an exact strategy is needed (R8). `EXPECTILE_TAU` is deliberately **unchanged**
  at 0.1 despite τ=0.9 measuring better (§0.1).
- **The single largest caveat to carry forward:** every Leduc LLM conclusion rests on **one model,
  one prompt style, 600 hands**. It is enough to say the Kuhn advantage does not transfer; it is not
  enough to rank models on Leduc.
- **Cheap open item:** the Leduc `FOLD_WHEN_FREE` misconception (R6) is likely removable with one
  prompt line ("you may check for free") — worth testing before concluding anything about LLM
  capability at multi-street poker.
- **Thesis hooks confirmed on real runs:** Contribution #1 — behavioural adaptation is *absent*
  in-context (R5), so an explicit opponent model is required rather than assumed; Contribution #2 —
  the exploitation/exploitability frontier is now measured on one plot (R5), with the LLM buying
  61% more exploitation for 59× the exploitability, and only against weak opposition;
  Contribution #3 — the per-decision decomposition (R3) plus the temperature/extraction protocol
  (R7, R8) are concrete components of the Step 14 evaluation methodology.
