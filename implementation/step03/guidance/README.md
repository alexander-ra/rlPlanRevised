# Step 03 — MCCFR Variants: CFR Sampling Strategies

**PhD Context:** This step is part of the official research program:
- **EN:** Research on the possibilities for applying Artificial Intelligence in computer games
- **BG:** Изследване на възможностите за приложение на изкуствения интелект в компютърни игри

Monte Carlo Counterfactual Regret Minimization (MCCFR) exploring two sampling paradigms: External Sampling vs Outcome Sampling on Kuhn Poker.

> **Environment setup:** See the [project-level README](../../README.md#python-environment-setup).
> The project uses a single `.venv` at the repository root shared across all steps.

## Overview

**Standard CFR** traverses the full game tree every iteration: O(|T|) complexity, zero variance.  
**MCCFR** samples game histories stochastically, exploiting tree sparsity: O(depth) complexity, non-zero variance but same O(1/√T) convergence rate.

This step compares two MCCFR variants empirically:

1. **External Sampling MCCFR** – samples chance outcomes only; agent nodes are traversed deterministically
2. **Outcome Sampling MCCFR** – samples both chance AND agent decisions from current policy

### Key Trade-offs

| Dimension | External | Outcome |
|-----------|----------|---------|
| **Sampling** | Chance nodes | All nodes |
| **Variance** | Lower (regret updates more stable) | Higher (samples policy stochastically) |
| **Exploration** | Slower (deterministic agent play) | Faster (samples policy diversity) |
| **Practical convergence** | Often smoother; reaches Nash quicker | More volatile; noisy signals |
| **Memory** | O(|IS| × |A|) | O(|IS| × |A|) + policy density |

## Repository Structure

```
step03/
├── playground.py              # 🟡 AI-ASSISTED: Main comparison script
├── analyze_mccfr.py           # 🟡 AI-ASSISTED: Variance & cost analysis
├── mccfr_explanation.md       # 🟢 AI-GENERATED: Detailed algorithm explanation
├── config.py                  # Configuration & hyperparameters
├── README.md                  # This file
├── mccfr_comparison_results.json   # Output: convergence records
├── mccfr_detailed_analysis.json    # Output: variance/cost analysis
├── logs/                      # Training logs (if extended)
└── models/                    # Saved policies (if extended)
```

## What You'll See

### Step 1: Main Comparison (`playground.py`)

Runs both solvers for 10,000 iterations each on Kuhn Poker:

```bash
python implementation/step03/playground.py
```

**Output:**
```
External Sampling:
  • Exploitability after 10k: ~0.011 (near-equilibrium)
  • Time: ~2.4 seconds
  • Convergence: Steady improvement

Outcome Sampling:
  • Exploitability after 10k: ~0.091 (higher variance)
  • Time: ~2.4 seconds
  • Convergence: More volatile but explores faster
```

**Insights:**
- External Sampling achieves lower exploitability (closer to equilibrium)
- Both solve in similar wall-clock time (sampling dominates, not computation)
- External Sampling's deterministic agent traversal = more stable regrets
- Outcome Sampling's policy sampling = more exploration, less immediate accuracy

### Step 2: Detailed Analysis (`analyze_mccfr.py`)

```bash
python implementation/step03/analyze_mccfr.py
```

Runs 5 independent trials to measure variance ("stability") of each sampler:

**Output:**
- Coefficient of Variation (CV) for each method
- Which sampler is more stable across runs
- Wall-clock time per iteration
- Raw convergence statistics

## Technical Details

### External Sampling Algorithm

```
For each iteration:
  1. Sample card deal (resolve chance node)
  2. For each player i:
       Walk game tree deterministically using best response
       Update counterfactual regrets at all i-relative positions
  3. Update average strategy (regret matching)
```

**Why lower variance?**
- Chance outcomes sampled → but no policy variance injected
- Regrets are deterministic (same tree walk each time)
- Policy only changes through regret matching, not sampling noise

### Outcome Sampling Algorithm

```
For each iteration:
  1. Sample card deal
  2. For each player i:
       Sample actions from current mixed strategy σ
       Walk stochastic tree (importance-weighted by sampling probs)
       Update counterfactual regrets
  3. Update average strategy
```

**Why higher variance?**
- Both chance AND agent actions are sampled
- Regrets include path-dependent importance weights
- High policy entropy → high variance early training

**Why faster exploration?**
- Direct samples from current policy
- Quickly adapts to policy changes
- Better handles large action spaces

## Theoretical Convergence

Both converge at rate:
$$\text{exploitability}(T) = O\left(\sqrt{\frac{\ln T}{T}}\right)$$

(More precisely: $O(1/\sqrt{T})$ asymptotically)

In Kuhn Poker:
- Nash exploitability = 0 (both reach it eventually)
- P1 equilibrium value = -1/18 ≈ -0.0556

## References

**Foundational Papers:**
- Zinkevich, Bowling, Burch, Billings (2007) — "Regret Minimization in Games with Incomplete Information"
- Neller & Lanctot (2013) — "An Introduction to Counterfactual Regret Minimization"

**MCCFR Extensions:**
- Lanctot et al. (2009) — "Monte Carlo sampling for regret minimization in extensive games"
- Burch et al. (2014) — "Efficient monte carlo counterfactual regret minimization in games with public information"

## Extensions & Future Work

**For deeper exploration:**

1. **Adagrad Updates:** Use adaptive learning rates (seen in DeepStack, OpenSpiel)
2. **Chance Sampling:** Compare with multiple chance sampling strategies
3. **Game Scaling:** Test on larger games (Leduc Hold'em, Dou Dizi)
4. **Hybrid:** Start with outcome sampling, switch to external when stable
5. **Dual Perspectives:** Run both from P1 and P2 viewpoints simultaneously
6. **Visualization:** Plot strategy convergence (bet probabilities over time)

## Quick Commands

```bash
# Run main comparison (both samplers, 10k iterations each)
python implementation/step03/playground.py

# Run variance analysis (5 independent trials)
python implementation/step03/analyze_mccfr.py

# View results
cat implementation/step03/mccfr_comparison_results.json
cat implementation/step03/mccfr_detailed_analysis.json
```

## Learning Outcomes

After this step, you should understand:

✓ Why MCCFR scales better than full CFR for large games  
✓ The bias-variance tradeoff between External and Outcome sampling  
✓ How chance dominance affects convergence speed  
✓ When to use each variant (problem-dependent)  
✓ How to empirically compare RL algorithms (convergence curves, variance)

