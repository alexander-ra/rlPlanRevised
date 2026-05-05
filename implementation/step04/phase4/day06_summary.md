# Phase 4 — Implementation summary

This file is the bridge between the implementation directory and the
deliverable's §7 / §8 / §9 sections. It records what was built, what
each day produced, and what numbers go into the deliverable when step 13
runs.

## Modules added

| Module | Day | Role |
|---|---|---|
| `leduc_full_engine.py` | 1 | step03 shim |
| `leduc_rank_engine.py` | 1 | rank-canonical Leduc (suit-iso baked in) |
| `day01_suit_isomorphism.py` | 1 | sanity probe for Definition 3.2 |
| `cfr_trainer.py` | 1 | generic vanilla CFR over any Leduc-shaped engine |
| `exploitability.py` | 1 | scores any node-map against the full game |
| `day01_train.py` | 1 | trains full + rank-canonical engines, reports numbers |
| `day02_hand_strength.py` | 2 | HSD features per Leduc info set |
| `day02_emd.py` | 2 | EMD via L1-of-CDFs + LP-form reference |
| `day02_kmeans_emd.py` | 2 | k-means with EMD distance |
| `day02_card_bucketing.py` | 2 | bucket builder + key translator |
| `day02_train.py` | 2 | sweeps `k × recall`, scores in full game |
| `mini_nl_leduc.py` | 3 | promoted variable-bet engine |
| `day03_translators.py` | 3 | nearest / probability-split / pseudo-harmonic |
| `day03_train.py` | 3 | full + abstracted training, translator BR |
| `extended_leduc.py` | 4 | new 4-rank, 2-suit Leduc variant |
| `day04_combined.py` | 4 | suit + bucket + action composition |
| `day04_train.py` | 4 | external-sampling MCCFR on triple-abstracted |
| `day05_exploitability_gap.py` | 5 | abstract / CFR-BR / decomposition |
| `day05_emd_evaluator.py` | 5 | direct EMD-proxy scalar per config |
| `day05_pareto.py` | 5 | aggregates per-day JSONs into a CSV |
| `day05_plots.py` | 5 | renders the Pareto figure |
| `day05_train.py` | 5 | dispatches `pareto.py` → EMD merge → `plots.py` |
| `day06_openspiel_compare.py` | 6 | cross-validation against OpenSpiel CFR |

## How to reproduce (smoke-test budget)

```
cd implementation/step04/phase4

python day01_train.py   --iterations 200
python day02_train.py   --iterations 200
python day03_train.py   --iterations 100
python day04_train.py   --iterations 20000
python day05_train.py
python day06_openspiel_compare.py --iterations 200
```

Each entry-point writes a `.dayXX_results.json` (or comparable) into the
phase4 directory; day 5 reads them back and emits the aggregate table
plus the matplotlib figure.

## Mapping to deliverable sections

- §7.0 Exploration — pre-existing in `implementation/step04/exploration/`,
  not touched by phase 4.
- §7.1 Lossless abstraction → day 1 outputs.
- §7.2 Lossy card bucketing → day 2 outputs.
- §7.3 Action abstraction + translation → day 3 outputs.
- §7.4 Extended Leduc + combined → day 4 outputs.
- §7.5 Quality evaluation → day 5 outputs.
- §7.6 Cross-validation → day 6 outputs.
- §8 Pareto frontier → `phase4/figures/day05_pareto.png`.
- §9 Reproduction → the command list above.
- §10 Exit checklist → satisfied per the table at the top of this file.

## What remains limited at this stage

- Verification is at the smoke-test budget, not a convergence study or
  multi-seed benchmark.
- Multi-seed averaging on MCCFR — single seed at the smoke-test budget.
- Pseudo-harmonic translation inside subgame solving — deferred to step 6.
- Imperfect-recall *with bucket-trail forgetting in CFR* — implemented
  via the key translator at evaluation time, but the rank engine itself
  retains the ranks. A fully imperfect-recall *engine* (where the round-1
  bucket id literally replaces the round-0 trail in the game state) is
  flagged for review feedback before committing.

## Open questions for tomorrow's review

1. **Day 2 — `_BucketedRankState` in `day02_train.py`.** Is the
   inflate-rank-to-card-id approach inside the translator wrapping
   acceptable? The cleaner alternative is to introduce a
   "rank-flavoured" translator that operates on rank ids directly,
   avoiding the round trip through `2 * rank + 0`.

2. **Day 3 — `_strategy_with_translation`.** The translator currently
   redistributes the abstract small-bet mass over `{small, large}`
   when the opponent's actual action is `BET_LARGE`. This is one of
   several reasonable interpretations — see the function docstring.
   In the current two-bet mini-NL game all three translators collapse
   to the same endpoint behaviour, so the equal Day 3 numbers are
   expected rather than a plotting failure. A richer full action set
   with an off-tree bet strictly between two abstract bets would be
   needed to separate them empirically.

3. **Day 4 — MCCFR seed budget.** Single seed, 20 000 iterations is
   enough to populate the bucketed node-map but probably not enough
   to converge. Day 5 won't have a meaningful exploitability number
   for the triple-abstracted config until this is bumped.

4. **Day 5 — `cfr_br_loop`.** The reference implementation in
   `day05_exploitability_gap.py` is structurally correct but has not
   been wired into a runnable trainer; the day 5 entry point currently
   reports only abstract-strategy exploitability, not the abstract /
   CFR-BR decomposition. Plumbing the loop into `day05_train.py` is
   the obvious next increment.

5. **Day 6 — OpenSpiel comparison semantics.** Key alignment is now
   implemented and all 936 Leduc info sets compare. The remaining
   interpretation issue is that phase-4 CFR and OpenSpiel CFR do not
   have identical update conventions, so the L1 strategy diff is a
   sanity check, not a proof of trajectory equivalence.

These are all increments — not blockers — for the deliverable's step 13
integration.
