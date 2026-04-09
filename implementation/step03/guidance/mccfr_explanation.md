# MCCFR: Monte Carlo Counterfactual Regret Minimization

## Overview

MCCFR extends classical Counterfactual Regret Minimization (CFR) by sampling game histories instead of traversing the complete game tree. This reduces computational complexity while maintaining convergence guarantees.

**Core Insight:** Only sample visited histories, ignore tree branches with low probability.

## Standard CFR vs MCCFR

| Aspect | Standard CFR | MCCFR |
|--------|-------------|-------|
| **Traversal** | Full tree every iteration | Sample one history |
| **Complexity** | O(\|T\|) per iteration | O(depth) per iteration |
| **Variance** | Zero (deterministic) | Non-zero (stochastic) |
| **Convergence** | O(1/√T) | O(1/√T) (guaranteed) |
| **Memory** | High (full tree stored) | Low (sampled histories only) |

## The Two Sampling Types

### 1. External Sampling

**What it samples:** Outcomes of external (chance) nodes only

**How it works:**
```
While traversing tree at decision node:
  IF node is chance node:
    Sample outcome from chance distribution
  ELSE (player node):
    Use best response or current policy
```

**Properties:**
- ✓ Lower variance on regret updates
- ✓ Doesn't re-sample agent decisions
- ✗ Bias if policy changes dramatically
- ✗ Slower to explore new policies
- **Use case:** When you want stable updates from chance-driven games

**Mathematical note:**
- Regret bounds hold with unbiased sampling of chance outcomes
- Requires care with reach probabilities for weighting

### 2. Outcome Sampling

**What it samples:** Outcomes of BOTH chance nodes AND agent decisions

**How it works:**
```
While traversing tree at any node:
  IF node is chance node:
    Sample outcome from chance distribution
  ELSE (agent node):
    Sample action from current policy σ(a | info_set)
```

**Properties:**
- ✓ Higher variance but more direct policy updates
- ✓ Faster exploration of policy space
- ✓ Adapts quickly to strategy changes
- ✗ Higher noise in regret signals
- **Use case:** When fast convergence and online learning matter

**Mathematical note:**
- Requires importance weighting: w = 1 / (product of sampled probabilities)
- Variance scales with policy entropy; tends to decrease during training

## Convergence Analysis

Both types converge at rate O(1/√T):
$$\text{exploitability}(T) = O\left(\frac{1}{\sqrt{T}}\right)$$

**In practice:**
- **External Sampling:** Smoother convergence curve, lower variance early
- **Outcome Sampling:** More volatile initially, but often reaches low exploitability faster

**Log-log plot property:** Both should have slope ≈ -0.5 when plotting log(exploitability) vs log(iterations)

## Kuhn Poker Context

In Kuhn Poker (3-card game):
- 12 decision nodes per player
- Simple chance structure (2 possible card deals per player)
- Nash value for P1: -1/18 ≈ -0.0556
- Optimal strategies well-known analytically

**Equilibrium:**
```
P1 with Jack (J):   Bet with prob ≈ 1/3 (bluff occasionally)
P1 with Queen (Q):  Check with prob ≈ 1.0 (fold to bet)
P1 with King (K):   Bet with prob ≈ 1.0 (always capitalize)
```

## Practical Considerations

### When to use External Sampling:
1. Deterministic games (no chance nodes act as bottleneck)
2. When memory is critical
3. Game structure heavily skewed toward player actions

### When to use Outcome Sampling:
1. Large policy space with high entropy
2. Online learning where fast adaptation needed
3. Games with symmetries (MCCFR exploits fewer samples)

### Hybrid Approaches:
- **Chance sampling only:** External sampling on chance, outcome sampling on agent actions
- **Adaptive switching:** Start with outcome sampling, switch to external when stable
- **Weighted average:** Combine both solvers as ensemble

## Implementation Checklist (for step03)

- [ ] Load Kuhn Poker from OpenSpiel
- [ ] Initialize ExternalSamplingSolver
- [ ] Initialize OutcomeSamplingSolver  
- [ ] Run both for 10k+ iterations
- [ ] Log exploitability at regular intervals
- [ ] Compare final strategies
- [ ] Analyze convergence speed
- [ ] Document differences observed

## References

- **Lanctot et al. (2009)** – "Monte Carlo sampling for regret minimization in extensive games"
- **Burch et al. (2014)** – "Efficient monte carlo counterfactual regret minimization in games with public information"
- **Neller & Lanctot (2013)** – "An Introduction to Counterfactual Regret Minimization" (foundational CFR paper)
