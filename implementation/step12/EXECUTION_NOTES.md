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
