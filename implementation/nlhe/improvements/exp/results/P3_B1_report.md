# Phase 3 report — B1+B3 flop-start (rejection sampling + soft-freeze)

**Date:** 2026-07-05 · **Gate G3.1:** PASS · **A/B verdict: FAIL (G3.2)** ·
**Recommendation: DO NOT adopt B1 on the live run (skip stop window #2).**
Nothing merged/flipped on LIVE; all work is in the DEV worktree.

## Setup
45-min small-game arms, back-to-back, seed 7, live daemon running throughout (consistent contention).
Control = stock full-game (`small50.json`). Mixed = B1+B3 flop-start, `full_game_fraction=0.25`
(`small50_mixed25.json`). Coverage from `measure_reach` (raw, uniform fallback); eval 25k paired decks, defaults off.

## Result

| | control (stock) | mixed (flop-start) | ratio / delta |
|---|---|---|---|
| final iterations | 159.8M | 376.9M | 2.36× |
| mean iters/s | 58,218 | 137,063 | 2.35× |
| **postflop `strat_nz`** (touched at all) | 3,832,853 | 3,573,247 | **0.93×** |
| **postflop `strat>1`** (plan metric) | 2,812,432 | 2,610,102 | **0.93×** |
| flop / turn / river `strat>1` ratio | — | — | 0.95 / 0.91 / 0.92 |
| eval vs random | −47.7 (±54) | −81.7 (±54) | −33.9 (within CI) |
| eval vs calling_station | +77.3 (±49) | +104.2 (±49) | +26.9 (within CI) |
| eval vs tag | −1186.4 (±43) | −1228.5 (±43) | −42.1 (within CI) |

**Gates:** G3.2 postflop ratio **0.93 (FAIL, needed ≥1.8)** · G3.3 tag/cs not-worse **PASS** (within CI) ·
G3.4 preflop drift 0.098 **PASS** (≤0.10) · G3.5 iters/s 2.35× **PASS**.

## Why flop-start *reduced* coverage (the key finding)

The premise — "60–80% of deals fold preflop, wasting iterations that could train postflop" — is
**weaker than it looks under external-sampling MCCFR**, because of how the traverser explores:

- **Stock full-game traverse** *branches every one of the traverser's preflop actions* (external
  sampling: traverser exhaustive, chance/opponents sampled). So a single deal reaches the flop through
  **many** preflop betting lines → many distinct flop betting-states × buckets touched per deal.
- **Flop-start `_advance_to_flop`** has **all seats sample one preflop line**, then traverses from the
  flop. So a deal reaches **one** flop betting-state. Rejection makes each iter cheap (2.35× more iters),
  but sampling concentrates on the *common* (converged) preflop lines and under-covers the rare ones.

Net: flop-start trades the traverser's exhaustive preflop **breadth** for a single sampled line. The
2.35× extra (cheap) iterations do **not** recover the lost breadth → 0.93× distinct coverage. `strat_nz`
(discount-insensitive) and `strat>1` agree, so this is a real coverage loss, not a schedule artifact.
(The earlier discount-desync worry was a false alarm: LCFR discounting is keyed to iteration count and
applied identically in iteration-space for both arms.)

**This will be *worse* on the live game, not better:** the live rules allow 2 raises/street (vs 1 here),
so the traverser's preflop branch factor is higher → stock already reaches even more diverse flop states,
and flop-start would give up even more relative breadth.

## Eval reading
Despite 2.36× more iterations, mixed's eval is statistically indistinguishable from control (all three
within combined CI) — i.e. flop-start bought no learning-quality gain either. Consistent with "same/worse
coverage, no benefit."

## Recommendation
- **Do not adopt B1+B3 on the live run.** It fails its core purpose (coverage) and would, if anything,
  slightly reduce live postflop coverage while adding sampling complexity and a resume-time code path.
- **B2 (tempered) / B4 (stratified) are premised on B1 helping** — deprioritize; the coverage lever isn't
  "reach the flop more often," it's "cover more distinct postflop states / more visits per state," which
  the traverser's branching already does. If postflop depth (visits/infoset) is the real target, that's a
  compute-budget/abstraction question, not a sampling-start question.
- The gated methodology worked exactly as intended: a plausible idea that would have mildly *hurt* the live
  run was caught in a 90-min offline A/B, with the live 300–400h run never touched.

## Addendum (final review, 2026-07-05) — quantitative tie-out + variant sweep

**Branch-multiplier tie-out.** Postflop visit volume (avg_mass × touched) is ≈ equal between arms
(1.07 × 0.93 ≈ 1.00). Solving 160M×B ≈ 94M×B + 141M×1 (141M = accepted flop-starts at ~50% reach)
gives **B ≈ 2.1**: each stock iteration was already worth ~2.1 flop entries via traverser preflop
branching, plus full preflop training. Flop-start's 2.36× iteration rate exactly cancels against losing
B — same volume, 0.93× diversity. Live rules (2 raises/street) make B larger → worse there.

**Root cause.** The motivating "60–80% of hands fold preflop" describes *sampled play*, not *training
work*: a traverser fold-branch costs one linear sampled rollout (~free), while the expensive branched
postflop subtree is identical per entry in both arms. B1 reclaimed a cost that didn't exist.

**Variant sweep (all no-go for the live run):** tuning `full_game_fraction` interpolates toward 1.0×,
never ≥1.8×; "branch-the-traverser flop-start" = stock; turn/river-start strictly worse; B2 tempered
trunk & ε-exploration at sampled nodes attack the *right* problem (entry/line diversity) but are
training-math changes with importance-weight variance and marginal seed value → Phase-6 memo only;
B4 stratified dealing warms tail states to ~tens of noisy visits (nonzero ≠ sensible). Structural
takeaway: **the 214M-infoset tail is unlearnable by visitation**; "sensible everywhere" comes from
A1/A2 defaults (built, parked for distill) + NN generalization (planned spiral), not sampling tricks.

**Steelman noted:** flop-start does buy +5–10% reach-weighted depth on common lines (arguably
imitation-relevant), but eval showed zero gain, and it costs 75% of preflop updates with drift already
at 0.098/0.10 in 45 min — unacceptable trunk risk over a 24h live soak.
