# NLHE Status Analysis — 2026-07-07

Analysis of the live `status.txt` snapshot: the DeepCFR NLHE pilot results and the
MCCFR 6-max blueprint progress, the learning mechanics behind them, coverage
dynamics, comparison to published work (Pluribus et al.), and strategic
recommendations for the path to an NN-bootstrapped agent.

Scope note: the real-money / opponent-modeling data discussion is intentionally
**not** included here (that work is weeks out). This doc covers the base
(MCCFR blueprint + DeepCFR pilot) only.

---

## TL;DR

- Both agents show the **same qualitative signature**: crush the calling station,
  ~break even vs random, get **destroyed by TAG** (MCCFR ≈ −466 bb/100, DeepCFR
  ≈ −897 bb/100). A common cause, not two separate algorithm bugs.
- The TAG loss is **real, not a harness bug** (sign/seat logic verified). Its root
  cause is a **coarse, under-converged, aggression-skewed policy that defaults to
  uniform-random (incl. 25% all-in) on the majority of postflop nodes**, stress-tested
  by a baseline whose chips only go in with strong hands.
- The **deployed metric uses the *average* strategy** (`stratsum`), which retains the
  early uniform junk far longer than the current (regret-matched) strategy does.
  Pluribus explicitly avoids this — it plays the **current/last-iterate strategy**
  postflop for exactly this reason.
- **Coverage is plateauing** (river `strat_nz` fill rate already decayed 0.39 → 0.25
  pts/B iters). **80% river coverage is effectively unreachable** and is the wrong
  target; depth-on-support is healthy and growing.
- **1000h on this box ≈ Pluribus blueprint compute** (~500 core-days). Time is not the
  main gap; **action-abstraction richness and (later) real-time search are.**
- Highest-leverage next steps: **(5.1) eval the current strategy, not the average;
  (5.2) purify + fix the uniform default policy;** then a **modest action-abstraction
  enrichment** (add 0.5× pot, re-enable preflop open) before pouring in more hours.

---

## 1. Evaluation results

### 1.1 MCCFR blueprint — run `20260703_6max_200_v1`

6-max, 200bb, SB 1 / BB 2. At snapshot: iteration ≈ 38.1B, 149,738 iters/s, 12
workers, 214,143,408 infosets, 15.6 GB table, ~73h elapsed, pruning on.

Most recent evals (bb/100, `pilot_decks`≈2000):

| vs | result | 95% CI |
|---|---|---|
| random | ≈ +44 | ±52 |
| calling_station | ≈ +293 | ±49 |
| tag | ≈ **−466** | ±42 |

Trajectory over the run:
- **calling_station improved** ~+120 → ~+293 (learning to value-bet/jam harder).
- **tag stuck** in the −350…−650 band the entire run — **no downward trend** across 38B iters.
- random drifted from slightly negative to slightly positive (~+44).

### 1.2 DeepCFR pilot — run `20260706-1034_deepcfr-pilot_s7`

`state=DONE_MAXHOURS` (ran to the 11h cap). `cfr_iter=2578`, `nodes_total≈684.6M`,
advantage & strategy reservoirs both **saturated at 8M**, `device=cuda`,
`k_traversals=3000`, `hidden=[256,256]`, seed 7, ~1.4 GB VRAM.

Final eval (iter 2578, 4000 decks, `policy=final_advantage_net`):

| vs | result | 95% CI |
|---|---|---|
| random | +332 | ±137 |
| calling_station | +2010 | ±128 |
| tag | **−897** | ±105 |

Trajectory (iter 98 → 2578): **flat / non-learning.** `adv_loss` pinned at ~6200–6400
throughout; tag stuck −780…−944; calling_station actually **drifted down** 2602 → 2010;
random noisy +73…+358.

Read: a **successful infrastructure pilot** (GPU path works, buffers fill, evals run,
~30k nodes/s) but a **model-quality non-event** — converged to a crude policy almost
immediately, then nothing. Two contributing factors:
- Tiny net + 11h + saturated buffers → essentially no useful learning signal.
- **Evaluated on `final_advantage_net`** = the last-iterate regret-matching policy, *not*
  an average-strategy net. In CFR only the *average* converges toward equilibrium, so this
  scores a peakier, higher-variance policy. Confirmed by the CIs: **±105–137 on 4000 decks**
  vs MCCFR's **±42–52 on ~2000 decks** → ~an order of magnitude more per-deck variance
  (a jam-happy, stack-off-prone policy).

Caveat: the pilot's *trainer* code is not in this repo (config path points at a separate
`rlPlanRevised-dev` checkout); DeepCFR-specific claims are inferred from status/metrics +
the shared eval harness.

### 1.3 The shared pattern and its cause

Two very different algorithms (214M-entry table vs a neural net) land on the identical
shape → the cause is **shared**: the game/abstraction + the policy character, not the
learner.

Magnitude sanity check: −466 / −897 bb/100 is **losing 4.7–9 bb per hand** to a mechanical
rule bot. Folding every hand only costs ~0.25–1.5 bb/hand (blinds). To bleed 4.7–9 bb/hand
you must be **putting stacks in and losing them** repeatedly.

**Why TAG specifically punishes them (and the station rewards them):**
- TAG only commits chips with strong hands, and when strong it **shoves** (the all-in is
  emitted last among raise actions and TAG picks the largest — see `src/engine_nb.py`
  ~199–207 and `src/evalmatch.py` ~117–134). Threshold: raise if bucket-equity ≥ 0.65,
  call if ≥ 0.5, else fold/check.
- Against a **calling station**, big pots are uncorrelated with the opponent's strength →
  any aggression prints (+293 / +2010).
- Against **TAG**, every big pot is one TAG has → any stack-off leak is maximally punished.
  Same policy, opposite outcome, purely from *who the money goes in against*.

**Where the leak comes from (high confidence for MCCFR):** the blueprint plays **uniform
random** (fold/call/pot/all-in at 25% each) whenever an infoset is unseen *or* has zero
accumulated average-strategy mass (`src/evalmatch.py` ~39–53). The uniform default puts
**25% on all-in and 25% on fold everywhere it fires** — free money to a station, a wash vs
random, and a stack-donation machine vs a tight range.

Sign/seat logic verified (`src/evalmatch.py` ~258–267): station-positive confirms the sign,
so the negative TAG number genuinely means the blueprint loses chips. **Not a harness bug.**

---

## 2. How MCCFR learns (mechanics)

### 2.1 Infoset identity and the abstraction tie

Infoset = `hash(public betting state) ⊗ card bucket` (`src/mccfr.py` ~166–169). Regret and
strategy rows live **per (betting-state × bucket)**, not per exact hand. Every hand k-means
placed in the same bucket at the same betting node **shares one regret row and one strategy
row** — they are forced to play identically. That is the entire abstraction coupling.

The update at the traverser's own node walks all 4 actions, gets each action's counterfactual
value from the **actual sampled cards** (real showdown payoffs at the leaves), then updates
regret with CFR+ flooring (`src/mccfr.py` ~196–202):

```python
if cfr_plus == 1:
    r = regret[slot, a] + (util[a] - node)
    regret[slot, a] = r if r > 0.0 else 0.0
else:
    regret[slot, a] += util[a] - node
```

Because values come from the *actual* cards but regret is stored *per bucket*, a bucket's
regret becomes the (discounted) **sum over all real hands that landed in it** of
`(action value − node value)`. The learned strategy is the regret-matching compromise for the
bucket's *mixture* of hands. Buckets that lump strategically-divergent hands → muddy,
exploitable strategies (abstraction coarseness → strategy quality).

### 2.2 Current vs average strategy — the key distinction

- **Current strategy** = regret matching over `regret[slot]`. After the *first* traverser
  visit it is non-uniform; bad actions accumulate negative regret and (with CFR+) are pinned
  near 0. Converges fast per node (O(1/√T), diminishing marginal impact per visit).
- **Average strategy** = `stratsum`, accumulated **only at opponent nodes**
  (`src/mccfr.py` ~203–206), and it is **what eval/deploy uses**. It is a running sum of
  current strategies, so it is **anchored to the early uniform/noisy iterations** and lags
  badly. `discount()` (Linear-CFR-style, `src/mccfr.py` ~253–261) exists to shrink old mass
  and fight this anchoring.

**Consequence:** even after the current strategy sharpens, the deployed average still carries
residual mass on the bad actions (the 25% shove) on under-visited nodes. **Pluribus reached
the same conclusion** and plays the current/snapshot strategy postflop instead of the raw
average (see §4).

### 2.3 What `strat>1 / >10 / >100` mean

At each opponent visit `stratsum += strat`, and `strat` is a probability distribution summing
to **exactly 1** → each visit adds **+1.0 total** to the infoset's strategy mass (before
discounting). Therefore **mass ≈ discounted visit count**, and the coverage-scan thresholds
(`scripts/measure_reach.py` ~124–135) are **visit-depth buckets**:

- `strat_nz` = visited at all (has any average-strategy mass)
- `strat>1` = visited more than ~1×
- `strat>10` = visited more than ~10×
- `strat>100` = visited more than ~100×

### 2.4 Do repeat visits have diminishing returns?

Yes. Current strategy: O(1/√T) — visit 100 barely moves a normalized strategy that already
sums 99 prior updates. Average strategy: converges even slower and needs many visits before it
even *reflects* a good strategy, because of the uniform anchoring above.

**How fast does the 25%/25% drop?**
- In the **current** strategy: almost immediately (1–few visits), but noisily (single-sample
  counterfactual values are high-variance).
- In the **deployed average**: decays only like `(early-uniform mass) / (total visits)` — an
  infoset visited 10× with 2 early uniform visits still carries ≈5% random all-in; at 100
  visits ≈0.5%. So **tens-to-hundreds of visits** are needed for the tail to vanish.

The user's instinct ("initial values too offset to align to proper values") is essentially
correct — but the mechanism is the **average-strategy anchoring**, not the regret init (CFR
requires zero-init → uniform; don't hack that). Fixes are: deploy current/snapshot strategy,
purify/threshold, and replace the uniform default with a poker-sane one.

---

## 3. Coverage dynamics and the plateau

### 3.1 Three different metrics (don't conflate)

- **`reach_flop_pct` ≈ 65%, flat** — NOT coverage. It's the fraction of hands the current
  strategy plays past preflop (i.e., it folds ~35% preflop = healthy poker). Its flatness is
  not stalling.
- **`strat_nz` (breadth)** — real table coverage; growing but decelerating.
- **`avg_mass` (depth on touched nodes)** — growing ~linearly; common lines are getting
  genuinely deep.

### 3.2 Latest coverage scan (iter ≈ 37.66B)

| street | strat_nz | strat>1 | strat>10 | strat>100 |
|---|---|---|---|---|
| preflop | 67.5% | 59.6% | 44.5% | 25.8% |
| flop | 54.3% | 44.5% | 24.6% | 10.6% |
| turn | 46.4% | 37.5% | 21.0% | 9.6% |
| river | 39.3% | 32.6% | 19.4% | **9.2%** |

River reading: only ~9% of infosets visited >100×; ~80% ≤10×; ~61% never (→ uniform default).
That one row is the whole postflop-weakness story.

### 3.3 Depth vs breadth

- River `avg_mass` (touched nodes): 5,134 (11.2B) → 12,667 (37.66B), ~+280 per B iters →
  **depth-on-support is healthy and growing linearly.**
- River `strat_nz` fill rate is **decelerating**:

| iter | river strat_nz | rate since prev |
|---|---|---|
| 25.3B | 35.7% | — |
| 27.0B | 36.3% | 0.39 pts/B |
| 28.7B | 36.9% | 0.35 pts/B |
| 30.3B | 37.5% | 0.32 pts/B |
| 37.7B | 39.3% | **0.25 pts/B** |

### 3.4 Interpretation

- The **plateau is already visible** in the run's own scans. Extrapolating the decay, river
  breadth asymptotes somewhere in the **mid-40s–~50s %, not 80%.**
- **80% river coverage is effectively unreachable and is the wrong target.** The never-filled
  infosets are overwhelmingly near-zero-probability equilibrium lines; on flop/turn, low
  breadth is *partly by design* (negative-regret pruning deliberately starves bad actions,
  which "effectively increases the card abstraction" — Pluribus's phrasing).
- The infosets that stay thin **and matter** are off-support lines a tight/real opponent forces
  you into — and **more hours will never fill those, because self-play doesn't go there.**
  That is a **structural** limit, not a time limit → the fix is NN generalization + a sane
  default + (later) real-time search, not brute-force hours.

### 3.5 Compute calibration

- Pluribus blueprint: 64 cores × 8 days ≈ **512 core-days**.
- This box: 12 workers × 1000h ≈ **500 core-days**.

So **1000h here is roughly Pluribus-blueprint scale.** Time is not the primary gap; abstraction
richness and (later) search are. The lowest-ROI compute is the ~250h→400h+ stretch on the
current coarse abstraction (marginal depth on support, targets a coarse equilibrium).

---

## 4. Comparison to published work

Best comparable: **Pluribus (Brown & Sandholm 2019 supplement)** — it uses the *identical*
200-buckets-per-postflop-round abstraction, so differences are informative.

- **Action abstraction is richer than ours, even in the blueprint.** Turn/river use at least
  `{0.5× pot, 1× pot, all-in}` for the first raise (≤2 for remaining); preflop is
  fine-grained. Ours is `{1× pot, all-in}` only with preflop-open sizing disabled — pot-or-shove
  forces an all-in-heavy tree. **This is a real gap and the biggest lever on the TAG leak.**
- **They do NOT deploy the average strategy postflop.** Quote: *"Since CFR's average strategy
  is not guaranteed to converge to a Nash equilibrium in six-player poker, there is no
  theoretical benefit to using the average strategy... For situations after the first betting
  round, a snapshot of the current strategy was taken every 200 minutes... averaged together."*
  And at play time they *"[play] according to the strategy on the final iteration rather than
  the weighted average... [to] avoid poor actions that are not completely eliminated in CFR's
  weighted average strategy."* → **directly validates §2.2.**
- **Pruning matches ours exactly:** skip actions with regret < −300M in 95% of iters, never on
  the last round or leading to terminals. We copied the right thing.
- Linear-CFR discounting only for the first ~400 min, then stopped.
- Compute: 64-core node, <0.5 TB RAM, **no GPU**; real-time on a 28-core/128GB node.
- Continuation strategies for search bias the blueprint toward fold/call/raise (×5 then
  renormalize) — evidence they actively reshape away from the raw blueprint.

Other references: **ozzi7/Poker-MCCFRM** (2-player, same 200bb/1-2 blinds, richer `1/2/3× pot`
sizes, 169-1000-1000-1000 buckets, OCHS+EMD); **krukah/robopoker** (Rust, EMD via Sinkhorn,
hierarchical k-means, external sampling, targets Pluribus parity); Deep-CFR literature (HUNL
<1 mbb/hand in ~10k iters; reservoir 1M–10M — too small → catastrophic forgetting, too large →
stale data dominates).

**Extractable lessons:** (a) enrich the postflop action set (≥ add 0.5× pot); (b) stop relying
on the raw average strategy postflop.

---

## 5. Extending the action abstraction (migration)

**Mechanically doable as a warm-start, not a free lunch.** Adding `0.5× pot` (+ re-enabling
the preflop open) means:

- `MAXA` 4 → 5 (fold/call/½pot/pot/allin); the `(capacity, MAXA)` regret/stratsum arrays gain a
  column.
- New raise size → **new committed/current-bet values → all downstream betting states are new
  hashes with no data.** Upstream states keep their hash but need the widened row.
- **Migration path:** rebuild the betting tree with the new rules → re-populate → for every old
  hash that survives, copy its 4 columns into the new row (pot→pot, allin→allin) and zero-init
  the ½pot column → continue training. Preserves the deep, valuable preflop/early training
  (preflop >100-visit mass ≈26%). ~1–2 days of scripting since hashing is deterministic and
  `build_table` exists.

**The catch is memory.** 200 buckets was chosen for the ~15.6 GB fit. Richer actions inflate the
betting tree substantially (more raise sequences) → possibly 2–3× the infosets/table size. On
this RAM budget you likely must **trade buckets for actions** (e.g., 200 → 150). Pluribus had
512 GB; we don't. This memory wall is *the* reason the plan moves to an NN (the net escapes it).

**Strategic point often missed:** the action set is a **ceiling on the final model too**, not
just the seed. Self-play only refines *within* its action set — a pot-or-shove agent can never
*discover* a half-pot bet and will always leak to half-pot bettors, no matter how long it
trains (unless the action set is expanded at the NN stage, which carries the same warm-start
cost in NN-land).

**Recommendation:** do a **modest enrichment now** (add 0.5× pot postflop + re-enable the
2.25bb preflop open, dropping buckets if RAM forces it) rather than grinding the coarse set to
400h first. Every hour on the coarse-set equilibrium optimizes a target you will abandon;
warm-starting recovers most of the sunk preflop compute.

---

## 6. Strategic outlook — can NN + self-play beat Pluribus?

Separate three meanings:

1. **Static NN policy, no search, head-to-head vs real Pluribus → very unlikely.** Pluribus's
   strength came primarily from **real-time depth-limited search**, not the blueprint; the
   blueprint alone was substantially weaker. A distilled static net *is* a blueprint, so it tops
   out at "strong blueprint" — a rung or two below Pluribus-with-search — on ~1/5 the wall-clock
   parallelism and a coarser abstraction.
2. **Pluribus-*competitive*, if "self-train later" includes test-time search (ReBeL-style
   value+policy net → depth-limited solving) → a long shot but not crazy** for a multi-year PhD.
   Open-source efforts target "functional parity." Understand it's reproducing 2019–2020 SOTA on
   a hobbyist budget, and search is a substantial second system.
3. **Winning *more than* Pluribus vs exploitable/real opponents via adaptive exploitation →
   genuinely plausible, and it's literally the thesis.** Pluribus plays fixed, non-adaptive,
   GTO-ish poker and deliberately does not maximally exploit. An adaptive exploiter can out-earn
   it against leaky opposition **without ever out-GTO-ing it head-to-head.** This is the framing
   to anchor on.

**Gut feeling:** don't frame the goal as "beat Pluribus at its own game" (low-probability,
dominated by search + compute we don't have). Frame it as **"a strong-blueprint NN + adaptive
exploitation that beats exploitable opposition by more than a GTO baseline does"** — achievable
*and* the actual contribution. Prerequisites line up: a clean seed (current/purified, not
raw-average), an adequate action set (≥ ½pot), and NN generalization — not brute-force table
coverage — covering the sparse nodes.

---

## 7. Recommendations / next actions

Ordered by leverage:

1. **(5.1) Evaluate the *current* (regret-matched) strategy, not the raw average.** Re-run
   `evalmatch` reading `regret` instead of `stratsum`. Cheap; directly tests how much of the
   −466 vs TAG is average-strategy junk vs real weakness. (Pluribus's exact conclusion for 6-max.)
2. **(5.2) Purify + fix the default policy.** On deploy, drop actions below ~5% and renormalize
   (or argmax on thin nodes); change the uniform fallback in `_blueprint_strategy`
   (`src/evalmatch.py` ~39–53) to a poker-sane default (check/call, fold-when-facing-a-bet)
   instead of 25%-shove. Targets the leak mechanically.
3. **Modest action-abstraction enrichment** (§5): add 0.5× pot postflop + re-enable the preflop
   open, warm-start-migrating the current table; drop buckets if RAM requires. Do this **before**
   investing more hours.
4. **Redefine "workable" as depth-on-support, not coverage %.** Cut over to NN distillation
   earlier (~150–250h), not 400h; the coarse-set tail is the most wasteable compute.
5. **Distillation guidance for the NN seed:** distill the **current/snapshot** strategy (not raw
   average), **weight the loss by visit mass (`ssum`)**, and lean on NN generalization for thin
   nodes rather than memorizing them. Do **not** let a raw-average table (with 25% shove tails on
   ~80% of postflop nodes) become the distill target.
6. **Verify the DeepCFR eval policy** — confirm whether future runs score the average-strategy
   net vs the advantage net; the pilot scored `final_advantage_net`, which inflates variance and
   understates a properly-averaged policy.

### Open question to resolve with data
Run 5.1 / 5.2 and report the numbers. If current-strategy/purified eval closes a large chunk of
the TAG gap, the base is healthier than −466 suggests, and we plan the abstraction migration +
distillation on real evidence.
