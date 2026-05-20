# Step 05 — Exploration Phase

Scripts for Phase 2 of [step_05_neural_equilibrium.md](../../../planning/rawSteps/step_05_neural_equilibrium.md).

## Goal

Get hands-on with the two main neural equilibrium families before reading the papers:

- **Deep CFR** (Brown et al., 2019) — neural advantage networks replace the tabular regret table; trained via external-sampling MCCFR traversals.
- **NFSP** (Heinrich & Silver, 2016) — RL-side approach: DQN learns a best response, supervised learning distils the average policy.

Both are run from OpenSpiel's PyTorch implementations on Leduc Hold'em (and Kuhn for NFSP), with our own from-scratch tabular MCCFR from [step03](../../step03/) as the conceptual baseline.

## Files

| File | What it does |
|------|---|
| [day01_deep_cfr.py](day01_deep_cfr.py) | Trains OpenSpiel Deep CFR on Leduc, sweeps three network sizes, and overlays a tabular MCCFR convergence curve. Outputs `figures/day01_*.png` and `logs/day01_*.json`. |
| [day02_nfsp.py](day02_nfsp.py) | Trains NFSP on Kuhn and Leduc, and inspects Deep CFR's learned action probabilities against the OpenSpiel tabular-CFR ground truth at specific Leduc info states. Outputs `figures/day02_*.png` and `logs/day02_*.json`. |
| [findings.md](findings.md) | Observations and answers to the Phase 2 questions, filled in after running. |

## Running

```bash
source .venv/bin/activate

# Day 1: ~5–15 min on CPU at default settings
python implementation/step05/exploration/day01_deep_cfr.py

# Day 2: ~5–15 min on CPU at default settings
python implementation/step05/exploration/day02_nfsp.py
```

Both scripts expose `--quick` (smoke-test) and individual iteration/episode flags. See `--help`.

## Why OpenSpiel for the MCCFR baseline?

The rawSteps brief says "compare against your tabular MCCFR from Step 3." Step 3 has a from-scratch external-sampling MCCFR, but on a custom Leduc engine — its info-set keys and utility scale don't line up with OpenSpiel's `leduc_poker`. Mixing them would compare exploitability values in two different games.

For these exploration scripts I use OpenSpiel's own `external_sampling_mccfr` as the tabular baseline so all three methods (Deep CFR, NFSP, tabular MCCFR) are scored by the same `exploitability.exploitability` function on the same game. The step03 implementation remains the "from-scratch understanding" reference; the actual head-to-head is left to Phase 4 where we re-implement Deep CFR ourselves and can choose either engine.

## Phase 2 question prompts

The raw plan asks four questions to answer by end of Day 2. They're answered in [findings.md](findings.md) and reproduced here so the scripts have something to verify:

1. What are the three components of Deep CFR? (advantage networks, strategy network, reservoir sampling)
2. How does NFSP differ architecturally from Deep CFR?
3. What role does reservoir sampling play? Why not just use all the data?
4. On Leduc, which method converges faster? Which reaches lower exploitability?
