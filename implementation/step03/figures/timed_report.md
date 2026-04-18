# Leduc Poker — Timed CFR Variant Comparison

Each algorithm was trained for **180 seconds** of wall-clock training time. Exploitability was snapshotted at geometrically spaced iteration counts.

## Final Results

| Algorithm | Iterations | Train Time (s) | Final Exploitability | Info Sets |
|-----------|-----------:|---------------:|---------------------:|----------:|
| Vanilla CFR | 3,713 | 180.0 | 0.0044 | 936 |
| CFR+ | 3,706 | 180.0 | 0.0000 | 936 |
| MCCFR External | 3,504,665 | 180.0 | 0.0548 | 936 |
| MCCFR Outcome | 8,262,137 | 180.0 | 0.1030 | 936 |

## Exploitability vs Iterations (log-log)

![Iterations](exploitability_vs_iterations.png)

Dotted vertical lines mark each algorithm's final iteration count — sampling-based variants run many more iterations per second, so their curves extend farther right before the 3-minute budget is exhausted. Full-traversal variants (Vanilla CFR, CFR+) cut off much earlier on the iteration axis but move far more per step.

## Exploitability vs Wall-Clock (log-y)

![Wall-Clock](exploitability_vs_wallclock.png)

This view normalises the comparison to compute time. CFR+ usually dominates in wall-clock convergence thanks to regret flooring and linear strategy averaging; Vanilla CFR follows a slower O(1/√T) trajectory; sampling variants reduce per-iteration cost but require many more iterations to catch up.
