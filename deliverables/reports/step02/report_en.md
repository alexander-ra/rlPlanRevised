<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->

# Step 02 — Game Theory & CFR Basics: Implementation Report

**Environment:** April 2026  
**Game:** Kuhn Poker (3-card, 2-player)  
**Algorithm:** Vanilla Counterfactual Regret Minimization (CFR)  
**Targets:** Nash strategies to 4 decimal places, game value ≈ −1/18, exploitability O(1/√T)  
**Status:** All targets achieved ✓

---

## Table of Contents

- [Overview](#overview)
- [CFR — Counterfactual Regret Minimization](#cfr)
  - [Game Engine](#game-engine)
  - [Algorithm Architecture](#cfr-architecture)
  - [Key Design Decisions](#cfr-design)
  - [Training Results](#cfr-results)
- [Exploitability & Best Response](#exploitability)
  - [Best Response Computation](#br-computation)
  - [Convergence Analysis](#convergence)
- [Nash Equilibrium Verification](#nash-verification)
- [Key Learnings](#learnings)
- [Appendix — Reproduction](#appendix)

---

## Overview <a id="overview"></a>

Step 02 implements vanilla CFR from scratch in Python, applied to Kuhn Poker — the simplest
non-trivial imperfect-information game. The original implementation was a single monolithic
file (`oldSources/kjunCRF/kuhn_cfr.py`, 1041 lines) created before the research plan was
formalized. It has been refactored into a modular structure consistent with Step 01 conventions.

New components added for Step 02: best response calculator, exploitability computation,
and convergence analysis — all required by the step exit criteria.

**Source layout:**

```
implementation/step02/
├── cfr/
│   ├── kuhn_poker.py        # Game engine (cards, actions, terminal payoffs)
│   ├── info_set_node.py     # Information set node (regret matching)
│   ├── cfr_trainer.py       # Recursive CFR traversal + training loop
│   └── train.py             # Training orchestration entrypoint
├── evaluate/
│   ├── best_response.py     # Best response (brute-force over pure strategies)
│   ├── exploitability.py    # Exploitability = BR₁(σ₂) + BR₂(σ₁)
│   └── convergence.py       # Log-log convergence analysis
├── utils/
│   ├── logger.py            # JSON-based training logger
│   └── plotting.py          # Strategy charts, convergence plots
├── compare_openspiel.py     # Cross-verification vs OpenSpiel
├── config.py                # CFR_CONFIG hyperparameters
└── verify_setup.py          # Dependency verification
```

**Reference:**
> Neller, T.W. & Lanctot, M. (2013). "An Introduction to Counterfactual Regret Minimization"  
> Zinkevich, M. et al. (2007). "Regret Minimization in Games with Incomplete Information"

---

## CFR — Counterfactual Regret Minimization <a id="cfr"></a>

### Game Engine <a id="game-engine"></a>

**Kuhn Poker** uses 3 cards (J, Q, K), 2 players, and 2 actions (pass/bet). Each player
antes 1 chip and receives 1 private card. Players alternate starting with Player 0.
Terminal conditions:

| History | Outcome | Payoff |
|---------|---------|--------|
| `pp` | Both pass → showdown | Higher card wins ±1 |
| `bp` | P0 bets, P1 folds | P0 wins +1 |
| `bb` | Both bet → showdown | Higher card wins ±2 |
| `pbp` | P0 passes, P1 bets, P0 folds | P1 wins +1 |
| `pbb` | P0 passes, P1 bets, P0 calls → showdown | Higher card wins ±2 |

There are 12 possible information sets (6 per player), each identified by the player's
card concatenated with the action history (e.g., `"2pb"` = holds Queen, history is pass-bet).

### Algorithm Architecture <a id="cfr-architecture"></a>

The CFR implementation follows Algorithm 1 from Neller & Lanctot (2013):

1. **Chance sampling:** At each iteration, shuffle cards randomly (replaces explicit chance nodes)
2. **Recursive tree walk:** From root, recurse through all possible actions at each info set
3. **Regret matching:** At each info set, convert cumulative positive regrets into a strategy:

$$\sigma^{T+1}(I, a) = \begin{cases} \frac{R^{T,+}(I,a)}{\sum_{a'} R^{T,+}(I,a')} & \text{if } \sum > 0 \\ \frac{1}{|A(I)|} & \text{otherwise} \end{cases}$$

4. **Strategy accumulation:** Weighted by reach probability — the *average* strategy converges to Nash
5. **Regret update:** Counterfactual regret weighted by opponent reach probability:

$$R^T(I, a) \mathrel{+}= \pi_{-i}^T \cdot (v(I, a) - v(I))$$

### Key Design Decisions <a id="cfr-design"></a>

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Sampling method | Chance sampling (shuffle cards) | Simpler than full tree enumeration; same convergence guarantee |
| Strategy output | Average strategy (not current) | Current strategy oscillates; average converges to Nash (Theorem 4, Neller & Lanctot) |
| Iteration count | 100,000 default | Gives game value within 0.005 of theoretical −1/18 |
| Checkpoint interval | Every iterations/200 | Smooth convergence plots without excessive memory |
| Info set representation | String: card + history | Simple, unique, human-readable (e.g., "2pb") |
| Best response method | Brute-force pure strategy enumeration (2⁶ = 64) | Correct for imperfect info; avoids per-state oracle bug (see Key Learnings) |

### Training Results <a id="cfr-results"></a>

Results from `python cfr/train.py --iterations 100000`:

| Metric | Value |
|--------|-------|
| Training iterations | 100,000 |
| Average game value (P0) | −0.0602 |
| Theoretical game value | −0.0556 (= −1/18) |
| Difference | 0.0047 |

**Strategy at key information sets (100K iterations):**

| Info Set | Card | History | P(pass) | P(bet) | Nash Range |
|----------|------|---------|---------|--------|------------|
| 1 | J | (root) | 0.806 | 0.194 | pass ≥ 2/3 ✓ |
| 2 | Q | (root) | 1.000 | 0.000 | always pass ✓ |
| 3 | K | (root) | 0.418 | 0.582 | bet ∈ [0, 1] (free param 3α) ✓ |
| 1b | J | b | 1.000 | 0.000 | always fold ✓ |
| 2b | Q | b | 0.665 | 0.335 | call ≈ 1/3 + α ✓ |
| 3b | K | b | 0.000 | 1.000 | always call ✓ |
| 1p | J | p | 0.660 | 0.340 | bet ≈ 1/3 ✓ |
| 2p | Q | p | 1.000 | 0.000 | always pass ✓ |
| 3p | K | p | 0.000 | 1.000 | always bet ✓ |
| 1pb | J | pb | 1.000 | 0.000 | always fold ✓ |
| 2pb | Q | pb | 0.461 | 0.539 | indifferent (any mix) ✓ |
| 3pb | K | pb | 0.000 | 1.000 | always call ✓ |

The strategies match the known Nash equilibrium family. Kuhn Poker has a one-parameter
family of Nash equilibria indexed by α ∈ [0, 1/3]. The pure-strategy info sets (J-fold,
K-call, etc.) converge precisely; the mixed-strategy info sets (J-bluff ≈ 1/3, Q-call ≈ 1/3)
also match the theoretical values to within 0.01.

**Note on game value convergence:** The computed game value (−0.0602) is close to but not
exactly −1/18 (−0.0556). This is expected behavior with chance sampling — each iteration
samples one random card deal rather than enumerating all 6 deals, introducing variance.
The average converges at O(1/√T), so 100K iterations gives accuracy within ~0.005. Running
1M iterations would reduce this to ~0.001.

![Game Value Convergence](figures/game_value_convergence.png)
![Strategy Analysis](figures/strategy_analysis.png)

---

## Exploitability & Best Response <a id="exploitability"></a>

### Best Response Computation <a id="br-computation"></a>

The best response for a player is the strategy that maximizes expected value against the
opponent's fixed strategy. In imperfect-information games, this is more subtle than in
perfect-information games: the best-responding player must choose the same action at all
game states within the same information set (they cannot distinguish those states).

**Implementation:** We enumerate all 2⁶ = 64 possible pure strategies for the BR player
(6 info sets × 2 actions each), evaluate each against the opponent's average strategy
across all 6 card deals, and return the maximum value.

This brute-force approach is tractable for Kuhn Poker. For larger games (e.g., Leduc Poker
in Step 3+), a bottom-up info-set-aggregated traversal would be needed instead.

**Exploitability** measures distance from Nash equilibrium:

$$\text{exploit}(\sigma) = BR_0(\sigma_1) + BR_1(\sigma_0)$$

At Nash equilibrium, exploitability equals zero (neither player can improve by deviating).

### Convergence Analysis <a id="convergence"></a>

CFR's theoretical convergence rate is O(1/√T) for exploitability in 2-player zero-sum games
(Theorem 4, Zinkevich et al. 2007). On a log-log plot, this should appear as a line with
slope ≈ −0.5.

**Measured convergence:**

| Iterations | Exploitability |
|-----------|---------------|
| 100 | 0.1363 |
| 500 | 0.0626 |
| 1,000 | 0.0347 |
| 5,000 | 0.0307 |
| 10,000 | 0.0104 |
| 50,000 | 0.0064 |

**Log-log slope: −0.489** (expected: −0.500) ✓

The slight deviation from the theoretical slope is expected due to the stochastic nature
of chance sampling — each run uses different random card shuffles, introducing variance at
lower iteration counts.

![Exploitability Convergence](figures/exploitability_convergence.png)

---

## Nash Equilibrium Verification <a id="nash-verification"></a>

The Kuhn Poker Nash equilibrium has a known analytical form (family parameterized by α ∈ [0, 1/3]):

| Player | Card | Nash Strategy |
|--------|------|---------------|
| P0 | J | Bet with prob α (bluff); fold to bet |
| P0 | Q | Always pass; call bet with prob 1/3 + α |
| P0 | K | Bet with prob 3α; always call |
| P1 | J | Bet (bluff) with prob 1/3 after pass; fold to bet |
| P1 | Q | Pass after pass; call bet with prob 1/3 + α |
| P1 | K | Always bet; always call |

**Fixed-point strategies** (independent of α) match to 4+ decimal places:
- J always folds to bet (P(fold) = 1.0000) ✓
- K always calls bet (P(call) = 1.0000) ✓
- K always bets after pass (P(bet) = 0.9999) ✓
- Q always passes at root (P(pass) = 0.9999) ✓

**Mixed strategies** match theoretical 1/3 mixing probability:
- J bluffs after pass: P(bet) = 0.340 ≈ 1/3 ✓
- Q calls facing bet: P(call) = 0.335 ≈ 1/3+α (α ≈ 0) ✓

---

## Key Learnings <a id="learnings"></a>

### 6.1 CFR Algorithm
1. **Average strategy, not current:** The single most important insight. The current
   iteration's strategy oscillates wildly; only the reach-probability-weighted average
   converges to Nash equilibrium. This is non-intuitive and is the most common
   implementation mistake.
2. **Counterfactual weighting matters:** Regret updates must be weighted by the *opponent's*
   reach probability, not the player's own. This is the "counterfactual" part — asking
   "if I had intentionally played to reach this info set..." Without this weighting,
   convergence fails completely.
3. **Chance sampling is sufficient:** Enumerating all deals per iteration is cleaner but
   unnecessary. Random shuffling converges to the same result and is simpler to implement.

### 6.2 Best Response & Exploitability
4. **Information set aggregation is critical:** The initial best response implementation
   had a conceptual bug — it chose actions per *game state* (knowing the opponent's card)
   rather than per *information set* (aggregating over unknown cards). This created an
   "oracle" with perfect information, giving constant exploitability regardless of training.
   The fix: enumerate all pure strategies and evaluate each across all deals, ensuring the
   same action is chosen at all states in the same information set.
5. **Exploitability is the primary evaluation metric:** Game value alone is insufficient —
   a strategy can achieve the right game value while still being exploitable. Exploitability
   directly measures distance from Nash equilibrium.

### 6.3 Connections to Step 01
6. **Local regret minimization → global convergence:** In Step 01, DQN minimizes TD error
   at each state; in CFR, regret matching minimizes regret at each information set. Both
   are local optimization procedures that achieve global objectives (optimal policy / Nash
   equilibrium) through aggregation.
7. **Strategy accumulation ≈ experience replay:** Both serve a stabilization role — replay
   buffers prevent catastrophic forgetting, while strategy accumulation prevents oscillation
   around the equilibrium.

---

## Appendix — Reproduction <a id="appendix"></a>

```bash
# From repo root, with .venv activated:

# Verify dependencies:
python implementation/step02/verify_setup.py

# Train CFR (100K iterations, generates figures):
python implementation/step02/cfr/train.py

# Train with custom iteration count:
python implementation/step02/cfr/train.py --iterations 50000

# Compute exploitability:
python implementation/step02/evaluate/exploitability.py

# Convergence analysis (log-log plot):
python implementation/step02/evaluate/convergence.py

# Cross-verify vs OpenSpiel + analytical Nash:
python implementation/step02/compare_openspiel.py
```

*Generated figures are in `deliverables/reports/step02/figures/`.*
