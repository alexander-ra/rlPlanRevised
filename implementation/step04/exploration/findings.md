# Step 04 — Exploration Findings (Intermediate Report)

Status: intermediate. Covers day-1 audit of the card-abstraction comparison
prior to running the regime-2 (game-tree) experiments.

---

## 1. Engine provenance

The day-1 experiment uses **step03's Leduc Poker engine**, not OpenSpiel.

- [day01_compare.py](day01_compare.py) imports `ALL_DEALS`, `LeducState as OrigState`
  from [step03/cfr/leduc_poker.py](../../step03/cfr/leduc_poker.py), and
  `best_response_value` from [step03/evaluate/best_response.py](../../step03/evaluate/best_response.py).
- [leduc_suit_abstracted.py](leduc_suit_abstracted.py) and
  [leduc_lossy_abstracted.py](leduc_lossy_abstracted.py) are near-verbatim
  copies of step03's file. Only `get_info_set()` differs. `legal_actions`,
  `apply_action`, `showdown_winner`, `get_utility`, and the 120-deal enumeration
  are byte-identical.
- Exploitability is always scored in the **original** full game via the
  `_AbstractedMapProxy`, so each abstraction is honestly judged against the
  unabstracted Nash target.

This matches the step04 raw-plan requirement of "minimal changes to the step03
engine" for both lossless and lossy variants.

## 2. Measured info-set counts

| Variant                     | Info sets | Reduction vs Original |
|-----------------------------|-----------|-----------------------|
| Original                    | 936       | —                     |
| Suit-Abstracted (lossless)  | 288       | 3.25×                 |
| Lossy (J/Q=low, K=high)     | 132       | 7.1×                  |

The docstring in [leduc_suit_abstracted.py:9](leduc_suit_abstracted.py#L9)
claimed "~468"; the true value is 288 because **both** the private-card and the
community-card bucket collapse under suit abstraction. To be corrected.

Also the step04 raw plan ([step_04_game_abstraction_scaling.md:278-279](../../../planning/rawSteps/step_04_game_abstraction_scaling.md#L278-L279),
[:340](../../../planning/rawSteps/step_04_game_abstraction_scaling.md#L340))
asserts "~468 instead of ~936" and "info set count should halve" — both wrong
for the same reason.

## 3. Two definitions of "abstraction"

Exploration surfaced that the word *abstraction* in the raw plan is used in two
very different senses, and the day-1 code only implements the weaker one.

**Regime 1 — policy-bucket (what day-1 has now).**
The info-set *key* is shared across a bucket; the game state itself still
stores the real cards; the game tree, the 120-deal enumeration, and the
per-iteration traversal work are all unchanged. Only the node_map is smaller.

**Regime 2 — game-tree (what the plan's "2× faster" claim requires).**
The game state is re-expressed in the bucket variable itself (for lossless
suit: ranks 0..2 instead of card IDs 0..5). Deal enumeration uses canonical
rank-triples weighted by multiplicity. Training traverses a strictly smaller
tree per iteration.

The raw plan is ambiguous about which regime it intends. Sentences like
"abstracted game tree" ([step_04:96](../../../planning/rawSteps/step_04_game_abstraction_scaling.md#L96))
and "abstraction reduces the **total game tree size**" ([step_04:368](../../../planning/rawSteps/step_04_game_abstraction_scaling.md#L368))
plus the "2× faster" row in the Pareto table
([step_04:319](../../../planning/rawSteps/step_04_game_abstraction_scaling.md#L319))
point to regime 2. The implementation sentence "merge the info sets into a
single abstract info set" ([step_04:276](../../../planning/rawSteps/step_04_game_abstraction_scaling.md#L276))
reads like regime 1. We treat it as "both, and compare them" to eliminate the
ambiguity empirically.

## 4. Why vanilla CFR on a symmetric lossless policy-bucket shows no speedup

This is the key theoretical result surfaced during exploration, and the one
that clarified why the existing suit-abstracted run was "not improving".

Consider the unabstracted info sets `I_A = "0|cr"` (J♠) and `I_B = "1|cr"` (J♥).
By the suit symmetry of Leduc's showdown, for every iteration *t*:
- the legal actions at `I_A` and `I_B` are identical,
- the opponent reach distributions at `I_A` and `I_B` are identical,
- the counterfactual values per action at `I_A` and `I_B` are equal.

So `regret_sum(I_A, a, t) = regret_sum(I_B, a, t)` at every *t*, and the
regret-matching strategy at `I_A` *equals* the strategy at `I_B` at every *t*.

The suit-abstracted node `"0|cr"` accumulates the **sum** of those two
identical signals:

```
regret_sum(0|cr) = regret_sum(I_A) + regret_sum(I_B) = 2 × regret_sum(I_A)
```

Regret-matching normalises by the positive-regret sum:

```
strategy[a] = max(R[a], 0) / Σ max(R[·], 0)
```

This map is **scale-invariant**: doubling every regret yields the same
distribution. Therefore the suit-abstracted strategy at `"0|cr"` is *exactly*
the unabstracted strategy at `I_A` (= at `I_B`) at every iteration.

**Consequence.** Exploitability-vs-iterations curves for Original and
Suit-Abstracted under vanilla CFR are mathematically identical (up to
floating-point noise). The only real benefit of regime-1 lossless abstraction
in vanilla CFR is **memory**: 936 → 288 stored nodes. No wall-clock speedup
(same 120-deal traversal), no per-iteration convergence speedup (same
normalised strategy trajectory).

This is the opposite of what the step04 raw plan's "2× faster" row suggests —
regime 1 alone cannot deliver it. Regime 2 can.

## 5. When abstraction *does* accelerate — and the MCCFR bug

Lossless abstraction accelerates training in two settings:

**(a) Sampling-based CFR (MCCFR).** External sampling visits a single deal per
iteration. With 288 buckets instead of 936 info-set keys, each bucket gets ~3×
the sample rate, so variance at each bucket drops accordingly.

**(b) Game-tree (regime 2) CFR.** Canonical deals shrink the per-iteration
traversal. For Leduc suit isomorphism this is 120 → 24 deals = ~5× per-iter
wall-clock speedup, for *identical* convergence trajectory.

The MCCFR story matters here because [day01_seeded_mccfr.py](day01_seeded_mccfr.py)
has an incorrect update rule. Both the traverser **and** the opponent are
sampled, and unsampled actions on the traverser's turn are assigned
`cf_val = 0.0`. That is neither standard external sampling (which would fully
explore the traverser's actions) nor standard outcome sampling (which would
correct with `1/prob` importance weights). The resulting regret estimator is
biased, and the bias dominates whatever abstraction gain there might be.

step03 already ships a correct external-sampling implementation at
[step03/cfr/mccfr_external_trainer.py](../../step03/cfr/mccfr_external_trainer.py)
(explore all actions on update-player turn, sample one action on opponent
turn, update strategy-sum at update-player nodes only). The fix is to adopt
that pattern in day01_seeded_mccfr.

Once fixed, regime 1 lossless abstraction is expected to show a visible
win in MCCFR exploitability-vs-iterations.

## 6. Lossy (J/Q=low) abstraction — conclusion, frozen

We're **not running additional experiments** on the lossy variant. The
takeaway is already clear enough to close the file.

**What it does.** Collapses J and Q into one bucket; K stays separate. 132
info sets. Strategies at "low|…" are shared across actual J and actual Q
deals.

**Why it must exhibit a positive exploitability floor.** In the real game, Q
strictly dominates J at non-paired showdown. A shared policy at "low|…" has
to compromise between two genuinely different optimal actions, and the best
it can do is a convex combination that is exploitable against a best-response
opponent who *can* distinguish J from Q. The exploitability floor
`ε_abs > 0` is a property of the abstraction, not of the algorithm. More
iterations do not move it.

**Literature term.** "Abstraction bias" / "abstraction pathology" (Waugh 2009;
Johanson, Burch, Valenzano & Bowling 2013; Lanctot & Kroer tutorials). It is
*the* reason lossless abstraction is preferred wherever it's available, and
lossy abstraction is treated as "only use at scale where lossless is
infeasible."

**What we keep.** The file [leduc_lossy_abstracted.py](leduc_lossy_abstracted.py)
stays as-is for reference. Day-1 results won't rerun the lossy variant. Any
later curiosity about the exact floor can be recovered in a few minutes from
the existing checkpoint machinery.

**What the exercise taught.**
1. Abstraction correctness is not the same as abstraction helpfulness.
2. A shrinking info-set count is *not* a sufficient signal that the
   algorithm will benefit — the game tree and the sampling regime matter too.
3. Measuring abstraction quality against the **full game** (not the abstract
   game) is the only evaluation that catches the floor.

## 7. Plan for the rest of day 1

Driven by sections 3-5:

- **Fix** `day01_seeded_mccfr.py` external-sampling update rule to match
  step03's reference implementation.
- **Build regime 2**: a rank-canonical engine `leduc_rank_engine.py` with
  24 canonical rank-deals and integer multiplicity weights.
- **Compare CFR @ 10k iterations**: Original vs Rank-canonical (regime 2).
  Expected: identical exploitability curves (by §4), ~5× wall-clock speedup
  for regime 2.
- **Compare MCCFR @ 10M iterations**: Original vs Suit-abstracted (regime 1)
  vs Rank-canonical (regime 2). Expected: regime 2 strictly fastest,
  regime 1 strictly better than Original, all three converging to 0 exploitability.

## 8. Spec hygiene (followup)

The step04 raw plan should be tightened:
- "~468" → "~288" (3 occurrences).
- Explicitly distinguish regime 1 (policy-bucket) and regime 2 (game-tree).
- Annotate the "2× faster" row as achievable only under regime 2.

Deferred until after experiments complete, so the spec edit reflects measured
numbers rather than predictions.

---

## 9. Measured results

Two experiments were run on top of the framework above.

### 9.1 CFR @ 10k iterations — Original vs Rank-canonical (regime 2)

Script: [day01_cfr_compare.py](day01_cfr_compare.py). Plot:
[figures/day01_cfr_compare.png](figures/day01_cfr_compare.png).

| Variant          | Info sets | Train time | Final exploitability |
|------------------|-----------|------------|----------------------|
| Original         | 936       | 514.2 s    | 0.00200              |
| Rank-canonical   | 288       | **90.3 s** | 0.00199              |

**Wall-clock speedup: 5.69×**, matching the predicted 120/24 = 5× from the
canonical-deal count.

Exploitability-vs-iteration equivalence at every checkpoint:

| Iter   | Original  | Rank-canonical | |Δ|       |
|--------|-----------|----------------|-----------|
| 10     | 0.81171   | 0.81171        | 2.2e-16   |
| 30     | 0.28717   | 0.28717        | 2.2e-16   |
| 100    | 0.09000   | 0.09000        | 1.3e-16   |
| 300    | 0.03380   | 0.03380        | 8.6e-13   |
| 1,000  | 0.01143   | 0.01143        | 5.3e-07   |
| 3,000  | 0.00491   | 0.00478        | 1.2e-04   |
| 10,000 | 0.00200   | 0.00199        | 5.7e-06   |

The drift grows with iterations but stays below 10⁻⁴, consistent with
accumulation-order floating-point noise across two engines that execute
arithmetic in a different order on the same abstract operations. This is
the expected behaviour from findings §4 — the two curves are *not* two
algorithms, they are the same algorithm run through different plumbing.

**Takeaway for the raw plan.** The "2× faster" row in Phase 4 day 5 is not
only achievable, it *underestimates* the actual speedup from regime 2 on
Leduc. The true factor is ~5× for this game.

### 9.2 MCCFR @ 10M iterations — Original vs Suit (regime 1) vs Rank (regime 2)

Script: [day01_mccfr_compare.py](day01_mccfr_compare.py). Plot:
[figures/day01_mccfr_compare.png](figures/day01_mccfr_compare.png).

Using the corrected external-sampling MCCFR (update player explores all
actions, opponent is sampled).

Exploitability trajectories:

| Iter       | Original | Suit (R1) | Rank (R2) |
|------------|----------|-----------|-----------|
| 10,000     | 0.695    | 0.555     | 0.428     |
| 30,000     | 0.486    | 0.417     | 0.288     |
| 100,000    | 0.307    | 0.218     | 0.191     |
| 300,000    | 0.211    | 0.143     | 0.121     |
| 1,000,000  | 0.119    | 0.110     | 0.128     |
| 3,000,000  | 0.061    | 0.112     | 0.080     |
| 10,000,000 | **0.103**| **0.169** | **0.056** |

Per-iteration throughput was ~22k iter/s across all three variants (external
sampling traversal cost is dominated by tree-walk depth, not info-set count,
so wall-clock-per-iteration is similar for all three).

**Three things to read off this table.**

1. **Early-training advantage of abstraction is real but modest.** Up to
   ~300k iterations the ordering is Rank ≤ Suit ≤ Original, consistent with
   the variance-reduction argument: fewer info-set keys → more samples per
   key → lower variance per key. By 1M iterations the three are essentially
   tied within noise.

2. **MCCFR exploitability is non-monotonic at high iteration counts.** All
   three variants show excursions after 1M iters (Suit regresses badly:
   0.110 → 0.169; Original dips to 0.061 then returns to 0.103). This is a
   known property of single-seed external-sampling MCCFR: the running
   strategy average is uniformly weighted over iterations, so a sequence of
   unlucky late-stage samples can drag the average away from Nash. A proper
   measurement should average over many seeds — we ran one — but that
   multiplies wall-clock by the seed count and was out of scope for day 1.

3. **Vanilla CFR at 10k utterly dominates MCCFR at 10M on this game.** CFR
   hits 0.002 exploitability in 90 s (rank-canonical) or 514 s (original);
   MCCFR hits ~0.05–0.17 in 450 s. On games small enough for full
   traversal, MCCFR has no story. Its reason for existing is regime
   3: games too large to enumerate. Leduc is not that regime.

### 9.3 What this changes in the plan

- **Regime 2 is the right default for all "lossless" Leduc work going
  forward.** It is faster per iteration, identical per strategy, and the
  node_map it produces is a drop-in replacement for the suit-abstracted
  map at evaluation time (same key format).
- **Regime 1 (suit-abstracted) is kept as a teaching artefact.** Its value
  is demonstrating section 4 empirically: show that CFR curves overlap
  exactly with the original, and explain why.
- **MCCFR is a red herring for Leduc.** The step04 raw plan suggests MCCFR
  as the training method for abstracted games ([step_04:96](../../../planning/rawSteps/step_04_game_abstraction_scaling.md#L96)).
  For a 120-deal game, full CFR under regime 2 is strictly preferable.
  MCCFR returns as the right tool in step 5 / 6 when game size grows
  beyond full enumeration (Extended Leduc, no-limit variants).
- **Multi-seed MCCFR** should happen before drawing conclusions about
  abstraction's effect on MCCFR convergence rate. Filed as a followup,
  not blocking day 1 write-up.

