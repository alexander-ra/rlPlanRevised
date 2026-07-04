# Improvement Proposals — NLHE 6-max Trainer

Status snapshot (from the current run + `convo.txt`):

- External-sampling MCCFR, one shared tabular table (`regret`/`stratsum`), one
  rotating traverser per game, button fixed at seat 0. CPU/Numba (`prange`).
- ~146k iters/s, 5.26B iters in ~10h. Preflop (**~7M infosets**) converged and
  sensible (AA never folds, AKs raises 93%, 72o folds 100%). Postflop
  (**~207M infosets**, 200 buckets/street) is **~87% never-visited** → plays
  **near-random postflop**. Eval too noisy (2k decks, CI ±155–184 bb/100).

## The actual goal (this reframes everything)

The tabular base is **NOT the final product**. It is a **seed** to warm-start
**self-play (RL)**, so self-play doesn't begin from a random strategy. After
self-play, the model is a neural net that is refined further.

Consequences for what "good" means:

- The seed must be **sensible everywhere + low-variance**, not deep/precise
  anywhere. Self-play grows skill; the seed just prevents flailing on basics.
- **"Random postflop" is the enemy** — it's exactly the cold start we're paying
  to avoid, on 87% of the state space.
- **Pure 400h of MCCFR is inefficient for this goal**: most hours re-confirm the
  already-converged preflop trunk (the starvation), while starving the postflop
  we actually need. MCCFR only becomes a good seed *with* the quick wins below.
- The long-term architecture is an **asymmetric spiral** (ReBeL / DeepStack /
  expert-iteration style): tabular does local exact solving; the NN generalizes
  + improves via self-play beyond the abstraction; feed back into finer targeted
  tabular subgame solves; re-distill. (A symmetric tabular↔NN ping-pong on the
  same abstraction is NOT useful — CFR's fixed point doesn't move and distillation
  error accumulates.)
- GPU (RTX 5090) idle during CFR is **expected** — CFR is a CPU workload. The GPU
  lights up for distillation + self-play + NN-value subgame solving.

---

## Legend

- **Effort**: rough engineering size (S/M/L).
- **Risk**: chance of correctness/variance problems (Low/Med/High).
- **Lever**: which sub-problem it attacks — *Symptom* (unvisited=random),
  *Throughput* (postflop visits/s), *Learning/visit*, *Scale*, *Measure*.

---

## Bucket A — Fix the symptom cheaply (unvisited != random)  ← QUICK WINS

These don't speed learning; they stop untouched postflop from playing randomly.
For a **self-play seed**, these are first-class: they define what the seed (and
later the distilled NN) does on the cold 87%.

### A1. Heuristic default policy for unvisited/thin infosets  ★ TOP QUICK WIN
- **Lever:** Symptom · **Effort:** S · **Risk:** Low
- Replace the uniform fallback (when `stratsum≈0`) with a pot-odds / bucket-equity
  rule: call if bucket-equity > required pot odds, bet strong buckets, else
  fold/check. Applied only where the table is untrained; trained nodes untouched.
- **Why now:** single highest value-per-effort change for the seed goal. Turns
  "random postflop" into "reasonable postflop" everywhere, immediately.

### A2. Nearest-bucket generalization fallback  ★ QUICK WIN
- **Lever:** Symptom · **Effort:** S · **Risk:** Low
- Buckets are equity-ordered; an unvisited bucket borrows the strategy of the
  closest *visited* bucket on that street. Converts 16% → ~100% "reasonable".
- Complements A1 (A1 = principled default; A2 = interpolate from learned data).

### A3. Heuristic warm-start of the table
- **Lever:** Symptom · **Effort:** S · **Risk:** Low
- Seed initial `stratsum` mass with A1's heuristic so early play is sane and CFR
  refines from a sensible prior instead of uniform.

---

## Bucket B — Increase postflop visits (sampling / curriculum)

The `convo.txt` direction. Attacks the "most iterations die preflop" waste.

### B1. Flop-start via rejection sampling  ★ QUICK-ISH WIN (root-cause)
- **Lever:** Throughput · **Effort:** M · **Risk:** Low
- Sample preflop with current strategy (no updates), discard hands that fold out,
  run the learning traversal from the flop. Bias-free given the current trunk;
  correct ranges/pots/multiway. Preflop sampling is ~microseconds, so discarding
  folded deals is nearly free.
- Pairs with **B3 soft-freeze** so the preflop trunk keeps adapting.

### B2. Tempered / flattened sampling (the "flatten the differences" idea)
- **Lever:** Throughput · **Effort:** M · **Risk:** Med
- Sample situations with `q ∝ p^α` (start α≈0.5), with `p/q` importance
  correction on utilities. Reallocates toward worst-case competence over
  EV-optimality — a legitimate objective change for a base, not a hack.

### B3. Soft-freeze iteration mix (~25% full-game / ~75% postflop-focused)
- **Lever:** Throughput · **Effort:** S (given B1) · **Risk:** Low
- Keep some full-game iters so preflop keeps adapting as postflop tightens.
  Hard-freezing preflop now would lock in distortions (it converged vs random
  postflop). Hard freeze becomes safe later once preflop stops moving.

### B4. Stratified dealing by bucket coverage
- **Lever:** Throughput · **Effort:** M · **Risk:** Med
- Track per-bucket visit counts; bias the deal toward under-visited buckets (with
  importance correction). Directly targets the 87% cold region.

### B5. Prioritized subgame replay
- **Lever:** Throughput · **Effort:** L · **Risk:** Med
- Queue under-visited public states; start a fraction of games there with ranges
  reconstructed from the trunk (prioritized sweeping).

---

## Bucket C — More learning per visit (algorithmic)

### C1. Vector / public-chance-sampling CFR
- **Lever:** Learning/visit · **Effort:** L · **Risk:** Med
- Update the whole range/bucket vector at each public state (matmul showdown
  utilities). Coverage per game scales with bucket count, not ×1. Also the only
  variant with a GPU-shaped inner loop — but 200-wide vectors are small; needs
  heavy batching across subgames to saturate a 5090.

### C2. Simultaneous multi-traverser updates
- **Lever:** Learning/visit · **Effort:** M · **Risk:** Low
- Update all seats per game (~6× tree work, ~6× signal). Sometimes a net coverage
  win vs rotating one traverser.

### C3. CFR+ / DCFR tweaks
- **Lever:** Learning/visit · **Effort:** S · **Risk:** Low
- Regret flooring + alternating updates; faster convergence per visit than
  vanilla regret-matching. Cheap swap, low risk.

### C4. Deep CFR / DREAM (NN function approximator)
- **Lever:** Learning/visit + Scale + Symptom · **Effort:** L · **Risk:** High
- Replace the tabular table with a net that **generalizes** across infosets →
  unvisited buckets get sensible values by interpolation (dissolves coverage),
  output IS the NN seed (no distill step), and it **uses the 5090**.
- **Risk is real:** finicky (reservoir buffers, capacity, noisy advantage
  targets); "MAY be a lot better or a lot worse". **Decide empirically** — run a
  short prototype and bake-off vs the MCCFR blueprint with the existing eval
  (`evalmatch.py` / `run_eval.py`) before committing 400h.

---

## Bucket D — Reduce the scale (abstraction)

### D1. Coarser postflop card buckets (50–100)
- **Lever:** Scale · **Effort:** S · **Risk:** Low · **Rejected by owner** —
  wastes preflop work, lowers ceiling.

### D2. Coarser postflop action abstraction  ← preferred scale knob
- **Lever:** Scale · **Effort:** M · **Risk:** Low
- Fewer bet sizes postflop shrinks the 207M count multiplicatively without
  touching card resolution. Different knob than card buckets.

### D3. Depth-limited solving + leaf value estimate
- **Lever:** Scale · **Effort:** L · **Risk:** Med
- Cap the tree (e.g. at turn), use a value net/rollout at the leaf. Standard in
  modern solvers; feeds the spiral's subgame phase.

### D4. Decoupled / offline subgame solving (nested)
- **Lever:** Scale · **Effort:** L · **Risk:** Med
- Freeze trunk, solve postflop subgames on demand with reconstructed ranges +
  NN leaf values (Libratus-style). This is the tabular half of the spiral.

---

## Bucket E — Instrumentation (decide from numbers)

### E1. Run `measure_reach.py`  ★ QUICK WIN (already written)
- **Lever:** Measure · **Effort:** S · **Risk:** Low
- Flop-reach rate + per-street coverage. This is where the last session stalled.
  Requires a checkpoint (not in this fresh clone).

### E2. Per-bucket visit histograms
- **Lever:** Measure · **Effort:** S · **Risk:** Low
- Targeting data for B4/B5.

### E3. Readable eval (decks 2k → ~25k)  ★ QUICK WIN
- **Lever:** Measure · **Effort:** S · **Risk:** Low
- CI ~3.5× tighter (±~50 bb/100) so changes are actually measurable. Isolated
  subprocess — doesn't slow training.

---

## Recommended order (given: base = self-play seed)

1. **Now, no-risk:** A1 + A2 (sane everywhere) · E3 (readable eval) · E1 (numbers).
2. **Root-cause throughput:** B1 (+B3 soft-freeze); then B2/B4 once E2 gives data.
3. **Cheap algorithmic:** C3 (CFR+/DCFR).
4. **The empirical fork:** short **C4 Deep CFR** prototype, bake-off vs blueprint
   with existing eval. Winner gets the big compute.
5. **Scale relief if needed:** D2/D3 (keep card resolution).
6. **Spiral (long-term):** blueprint → distill → self-play → nested subgame
   re-solve (D3/D4 + NN leaf values) → re-distill. Rule: every round-trip must
   add an operator the other representation couldn't produce (self-play gain or
   finer subgame resolution) — never a symmetric same-abstraction ping-pong.

## Compose notes

- A-bucket is orthogonal to everything and helps *both* MCCFR and Deep CFR seeds.
- Better postflop sampling (B) is what makes finer buckets (avoiding D1) affordable.
- C4 subsumes A/scale concerns *if* it trains stably — hence the bake-off gate.
