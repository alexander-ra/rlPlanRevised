# Why MCCFR Converges Slower Than Full-Traversal CFR on Leduc Poker

## 1. Setup: The Four Algorithms on One Small Game

We implemented four CFR variants on Leduc Poker (6 cards, 2 players, 936 info sets) and trained each for 180 seconds. The results:

| Algorithm | Final Exploitability | Iterations |
|-----------|--------------------:|----------:|
| CFR+      | 0.000026           | 3,706     |
| Vanilla CFR | 0.0044           | 3,713     |
| MCCFR External | 0.0548        | 3,504,665 |
| MCCFR Outcome  | 0.1030        | 8,262,137 |

Despite running **1,000x more iterations**, MCCFR External achieved 12x worse exploitability than Vanilla CFR. This document explains why this is mathematically expected, derives when MCCFR *would* win, and verifies the prediction against our data.

## 2. Defining the Variables

| Symbol | Meaning | Leduc Value |
|--------|---------|-------------|
| $\|N\|$ | Total game tree nodes (across all chance outcomes) | 10,200 |
| $\|I\|$ | Information sets (what players observe) | 936 |
| $\|A\|$ | Max actions per info set | 3 |
| $\Delta$ | Utility range (max − min payoff) | 13 |
| $D$ | Number of chance outcomes (deals) | 120 |
| $L$ | Average path length (root to terminal) | 5.47 |

**Key ratio:** $|N|/|I| = 10.9$. In Leduc, the physical tree is only ~11x larger than the player's information perspective — there is relatively little hidden information for the tree size.

## 3. Convergence Rate: Iterations to Reach Exploitability $\epsilon$

### Vanilla CFR

The standard CFR regret bound (Zinkevich et al., 2007) gives:

$$\epsilon(T) \leq \frac{\Delta \sqrt{|A|}}{D} \cdot \frac{\sum_{I} 1}{\sqrt{T}} = \frac{C_v}{\sqrt{T}}$$

where $C_v$ absorbs the game-specific constants. From our experiments:

$$C_v \approx 0.34 \quad \text{(measured: exploit} \times \sqrt{T} \text{ is stable at } 0.27\text{–}0.45 \text{)}$$

So to reach exploitability $\epsilon$:

$$T_v = \frac{C_v^2}{\epsilon^2} = \frac{0.34^2}{\epsilon^2} = \frac{0.116}{\epsilon^2}$$

### MCCFR (External or Outcome Sampling)

MCCFR follows the **same** $O(1/\sqrt{T})$ bound, but with a larger constant due to sampling variance:

$$\epsilon(T) \leq \frac{C_{mc}}{\sqrt{T}}$$

The constant $C_{mc}$ includes a **variance penalty** $\sigma^2$ that depends on the sampling scheme:

$$C_{mc} = C_v \cdot \sigma$$

From our experiments:

| Variant | $C_{mc}$ | Variance factor $\sigma = C_{mc}/C_v$ |
|---------|-------:|-------:|
| External | 107 | 315x |
| Outcome  | 245 | 721x |

To reach the same $\epsilon$:

$$T_{mc} = \frac{C_{mc}^2}{\epsilon^2} = \sigma^2 \cdot T_v$$

External needs $315^2 \approx 99{,}000\text{x}$ more iterations. Outcome needs $721^2 \approx 520{,}000\text{x}$ more.

## 4. Time per Iteration

Here is where the MC advantage lives — each iteration is much cheaper:

| Algorithm | Nodes visited per iteration | Time per iteration | Iterations/sec |
|-----------|---:|---:|---:|
| Vanilla CFR | $2 \cdot |N| = 20{,}400$ | 48.5 ms | 20.6 |
| External | ~42 (1 deal, partial tree) | 0.051 ms | 19,470 |
| Outcome  | ~5.5 (1 deal, 1 path) | 0.022 ms | 45,901 |

Speed advantage: External is **945x faster per iteration**, Outcome is **2,228x faster**.

## 5. Total Wall-Clock Time

Wall-clock time to reach exploitability $\epsilon$ is:

$$W = \frac{T}{\text{speed}} = \frac{C^2}{\epsilon^2 \cdot \text{speed}}$$

We can define a **wall-clock convergence constant** $C_w$ such that:

$$\epsilon(t_{\text{sec}}) = \frac{C_w}{\sqrt{t_{\text{sec}}}} \quad \text{where} \quad C_w = \frac{C}{\sqrt{\text{speed}}}$$

| Algorithm | $C_{\text{iter}}$ | Speed (iter/s) | $C_w$ | Relative to Vanilla |
|-----------|-----:|-------:|-------:|---:|
| Vanilla   | 0.34 | 20.6   | **0.075** | 1.0x |
| External  | 107  | 19,470 | **0.767** | 10.2x slower |
| Outcome   | 245  | 45,901 | **1.143** | 15.3x slower |

**The speed advantage does not overcome the variance penalty.** External is 945x faster per iteration but needs 99,000x more iterations. Net: $99{,}000 / 945 \approx 105\text{x}$ more wall-clock time.

### Concrete prediction vs. observed

To match Vanilla's final exploitability of 0.0044 (reached in 180s):

| Variant | Iterations needed | Wall-clock needed |
|---------|------------------:|------------------:|
| External | 582 million | ~500 minutes |
| Outcome | 3.1 billion | ~1,100 minutes |

## 6. Why the Sample Size Does Not Cancel

The original proof claims that sample size $s$ cancels:
- More samples per iteration → slower iterations (cost $\propto s$)
- More samples per iteration → less variance (savings $\propto 1/s$)
- Therefore $s$ cancels out of wall-clock time

**This cancellation is approximately correct**, but it conceals the real question. The issue is not *how many* nodes you sample, but *what information those samples provide about the full game*.

### The real variance source

Vanilla CFR computes **exact** counterfactual values by enumerating all $D = 120$ deals. Its regret update has **zero variance** — every update is the true expected value.

MCCFR samples one deal per iteration. Even if it explored the full tree for that deal, it would still have variance because:

$$\text{Var}[\text{regret update}] \propto \text{Var}_{\text{deal}}[\text{counterfactual value}]$$

This is the variance **across deals**, not across nodes within a deal. It comes from the hidden information (which cards were dealt), and no amount of within-deal exploration eliminates it.

For External Sampling, the sampled counterfactual value $\hat{v}_I$ for one deal is an unbiased estimator of the true $v_I$, but with variance:

$$\text{Var}[\hat{v}_I] = \mathbb{E}_{\text{deal}}[(\hat{v}_I - v_I)^2] \approx \frac{|N|}{|I|}$$

This is why $|N|/|I|$ matters: more hidden structure (more nodes mapping to each info set) means more variance per sample.

## 7. The Crossover Formula (Corrected)

MCCFR beats Vanilla when its speed advantage overcomes its variance penalty:

$$C_w^{mc} < C_w^{v} \iff \frac{C_{mc}}{\sqrt{\text{speed}_{mc}}} < \frac{C_v}{\sqrt{\text{speed}_v}}$$

As the game grows (more deals, deeper tree), Vanilla slows down linearly with $|N|$:

$$\text{speed}_v(|N|) = \frac{\text{speed}_v^{\text{Leduc}} \cdot |N|_{\text{Leduc}}}{|N|}$$

while MC speed stays roughly constant (always one sampled deal per iteration). Substituting:

$$\frac{C_{mc}}{\sqrt{\text{speed}_{mc}}} < \frac{C_v \cdot \sqrt{|N|}}{\sqrt{\text{speed}_v^{\text{Leduc}} \cdot |N|_{\text{Leduc}}}}$$

Solving for $|N|$:

$$|N| > |N|_{\text{Leduc}} \cdot \frac{C_{mc}^2 \cdot \text{speed}_v^{\text{Leduc}}}{C_v^2 \cdot \text{speed}_{mc}}$$

This gives us the critical tree size:

$$|N|_{\text{crossover}} = |N|_{\text{Leduc}} \cdot \left(\frac{C_{mc}}{C_v}\right)^2 \cdot \frac{\text{speed}_v}{\text{speed}_{mc}}$$

### Plugging in our numbers

**External Sampling:**

$$|N|_{\text{cross}} = 10{,}200 \times \left(\frac{107}{0.34}\right)^2 \times \frac{20.6}{19{,}470} \approx 2{,}100{,}000 \text{ nodes}$$

**Outcome Sampling:**

$$|N|_{\text{cross}} = 10{,}200 \times \left(\frac{245}{0.34}\right)^2 \times \frac{20.6}{45{,}901} \approx 4{,}800{,}000 \text{ nodes}$$

### Interpretation

| Game | $\|N\|$ | External wins? | Outcome wins? |
|------|--------:|:-:|:-:|
| Leduc Poker | 10,200 | No (210x too small) | No (466x too small) |
| Limit Hold'em | ~$10^{14}$ | Yes ($10^7$x above threshold) | Yes |
| No-Limit Hold'em | ~$10^{17}$ | Yes ($10^{10}$x above threshold) | Yes |

**Leduc is 210x too small for External Sampling to break even, and 466x too small for Outcome Sampling.** Full traversal dominates because the entire game tree fits comfortably in memory and can be enumerated in milliseconds.

## 8. Summary: Two Key Insights

### Insight 1: Variance, not speed, determines the winner

The speed advantage of MCCFR (945–2,228x fewer nodes per iteration) is overwhelmed by the variance penalty (99,000–520,000x more iterations needed). For small games like Leduc, exact computation beats sampling.

### Insight 2: The crossover depends on $|N|$, not $|I|$

As the game grows, Vanilla CFR slows linearly with $|N|$ (must enumerate more nodes), while MCCFR's cost per iteration stays roughly constant (always one sampled path/deal). The variance penalty grows slower than $|N|$ because the $|N|/|I|$ ratio that drives variance grows sublinearly. Once $|N|$ crosses the threshold (~2M nodes for External), MCCFR begins to dominate.

This is why MCCFR was essential for solving real poker games ($|N| > 10^{14}$) despite being provably worse on toy games like Leduc ($|N| = 10{,}200$).

## Appendix: Empirical Verification

The table below confirms that $C = \epsilon \times \sqrt{T}$ is stable for all algorithms, validating $O(1/\sqrt{T})$ convergence:

**External Sampling** ($C \approx 107$, stable within ±20%):
| T | Exploitability | $C = \epsilon\sqrt{T}$ |
|--:|---------------:|---:|
| 120,000 | 0.290 | 100 |
| 500,000 | 0.177 | 125 |
| 1,400,000 | 0.072 | 85 |
| 2,700,000 | 0.060 | 100 |
| 3,500,000 | 0.055 | 103 |

**Outcome Sampling** ($C \approx 245$, noisier as expected):
| T | Exploitability | $C = \epsilon\sqrt{T}$ |
|--:|---------------:|---:|
| 300,000 | 0.337 | 183 |
| 900,000 | 0.254 | 241 |
| 2,700,000 | 0.114 | 189 |
| 5,400,000 | 0.137 | 317 |
| 8,300,000 | 0.103 | 296 |

**Vanilla CFR** ($C \approx 0.34$, slowly decreasing — converges *faster* than $O(1/\sqrt{T})$):
| T | Exploitability | $C = \epsilon\sqrt{T}$ |
|--:|---------------:|---:|
| 100 | 0.090 | 0.90 |
| 500 | 0.020 | 0.45 |
| 1,400 | 0.009 | 0.33 |
| 2,700 | 0.005 | 0.28 |
| 3,700 | 0.004 | 0.27 |

Vanilla's $C$ decreasing over time indicates it benefits from structural properties (alternating updates, full information) that accelerate convergence beyond the worst-case $O(1/\sqrt{T})$ bound.
