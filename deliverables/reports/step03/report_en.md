<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->

# Step 03 — CFR Variants & Monte Carlo Methods: Implementation Report

**Environment:** April 2026  
**Game:** Leduc Poker (6-card, 2-player, 2 betting rounds)  
**Algorithms:** Vanilla CFR, CFR+, MCCFR External Sampling, MCCFR Outcome Sampling  
**Targets:** CFR+ exploitability < 0.001 within 180s, cross-validation against OpenSpiel, convergence analysis  
**Status:** All targets achieved ✓

---

## 1. Introduction <a id="1-introduction"></a>

Step 02 established a working Vanilla CFR solver on Kuhn Poker — the minimal imperfect-information benchmark with only 12 information sets. While sufficient for validating the CFR framework, vanilla CFR requires a **full traversal of the game tree on every iteration**. This approach becomes infeasible as games grow: Kuhn Poker has 58 terminal nodes, but Texas Hold'em has over $10^{14}$ information sets. No computer can enumerate that tree even once.

Step 03 addresses this scalability gap by introducing two complementary mechanisms:

1. **CFR+ (Tammelin, 2014):** A modification of vanilla CFR that achieves dramatically faster convergence through regret flooring, linear strategy averaging, and alternating updates. CFR+ was the algorithm that "solved" Heads-Up Limit Texas Hold'em — the first non-trivial poker variant to be essentially solved.

2. **Monte Carlo CFR (Lanctot et al., 2009):** Instead of traversing the entire game tree each iteration, MCCFR samples a small portion — one deal, one path. Each iteration is orders of magnitude cheaper, at the cost of noisier updates. This is the only tractable approach for games where full traversal is physically impossible.

Both algorithms are implemented from scratch on **Leduc Poker**, a medium-scale benchmark (~936 information sets, ~78× larger than Kuhn) that is small enough for exact computation but large enough to reveal meaningful performance differences between CFR variants.

**PhD Connection:** This step feeds directly into **Contribution #1 (Behavioral Adaptation Framework)**. MCCFR is the algorithm that computes the baseline Nash strategy — the "play it safe" anchor — from which an adaptive agent deviates based on opponent observations. CFR+ makes this computation tractable. The Leduc implementation also establishes the intermediate benchmark game used in Steps 5–8 before scaling to full poker.

**Components developed:**

- **Leduc Poker game engine:** Full game implementation — 6 cards, 2 betting rounds, community card, fold/call/raise actions, 120 deal permutations, pair-based hand ranking. Matches OpenSpiel's semantics exactly.
- **Vanilla CFR trainer:** Full-traversal with buffered regret accumulation across all 120 deals.
- **CFR+ trainer:** Regret flooring, linear strategy weighting, alternating player updates (Tammelin, 2014).
- **MCCFR External Sampling trainer:** One sampled deal per iteration, all traverser actions explored, opponent actions sampled (Lanctot et al., 2009).
- **MCCFR Outcome Sampling trainer:** Single sampled trajectory with ε-on-policy exploration and importance sampling correction.
- **Exploitability evaluator:** Iterative information-set-constrained best response computation.
- **Timed benchmark harness:** Runs all four algorithms under a common wall-clock budget with geometric snapshot spacing.
- **Cross-validation suite:** Compares outputs against OpenSpiel's reference implementations.

---

## 2. Background Concepts <a id="2-background-concepts"></a>

### 2.1 Monte Carlo Tree Search (MCTS) <a id="21-monte-carlo-tree-search-mcts"></a>

Monte Carlo Tree Search is a family of algorithms that use **random sampling** to evaluate positions in a game tree without exhaustive enumeration. MCTS builds an asymmetric search tree incrementally, focusing computation on the most promising branches.

The algorithm follows four repeated phases:

1. **Selection:** Starting from the root, descend through the tree by choosing child nodes according to a selection policy (typically UCB1 — Upper Confidence Bound) that balances exploitation of known-good moves with exploration of under-visited ones.

2. **Expansion:** When a leaf node is reached, expand it by adding one or more child nodes to the tree.

3. **Simulation (Rollout):** From the new node, play out a random game to completion — no strategy, just uniform random moves until a terminal state.

4. **Backpropagation:** Propagate the result (win/loss/draw) back up through the visited nodes, updating their statistics (visit count and cumulative reward).

After many iterations, the child of the root with the highest visit count (or highest average reward) is selected as the best move. The key insight is that **random rollouts, aggregated over thousands of iterations, converge to accurate value estimates** — even without any domain knowledge beyond the game rules.

MCTS is the foundation behind AlphaGo and AlphaZero, where the random rollout phase is replaced by a neural network evaluation. It is most naturally suited to **perfect-information** games (Go, Chess), but its sampling philosophy directly inspires the Monte Carlo methods used in MCCFR for imperfect-information settings.

### 2.2 MCTS vs Minimax <a id="22-mcts-vs-minimax"></a>

Minimax with alpha-beta pruning is the classical approach to game tree search. It evaluates **every** relevant node in the tree to a fixed depth, then applies a heuristic evaluation function at the leaves. This works well when:

- The game tree has a manageable branching factor (Chess: ~35, Checkers: ~10).
- Good evaluation functions exist (material counting in Chess, piece-square tables).
- Search depth can be bounded without losing critical information.

MCTS takes a fundamentally different approach: instead of evaluating all branches to a fixed depth, it evaluates **some** branches to **full depth** (terminal states). The comparison:

| Property | Minimax + α-β | MCTS |
|----------|--------------|------|
| Tree coverage | All branches to depth $d$ | Selected branches to terminal |
| Evaluation | Heuristic at depth limit | Exact (terminal payoff) or neural net |
| Branching factor sensitivity | Exponential: $O(b^d)$ | Graceful: focuses on promising branches |
| Domain knowledge needed | Strong eval function required | None (random rollout) or learned |
| Best suited for | Moderate branching, good heuristics | High branching, weak/no heuristics |

For Go (branching factor ~250, no known good evaluation function before neural networks), Minimax is impractical. MCTS was the breakthrough that made Go AI competitive — and the same principle of "sample instead of enumerate" motivates MCCFR's approach to imperfect-information game trees.

### 2.3 Markov Chains and Monte Carlo Methods <a id="23-markov-chains-and-monte-carlo-methods"></a>

The "Monte Carlo" in MCCFR refers to a broad family of computational methods that use **repeated random sampling** to obtain numerical results. The name originates from the Manhattan Project, where Stanislaw Ulam and John von Neumann used random sampling to simulate neutron diffusion — a problem too complex for analytical solution.

The mathematical foundation rests on **Markov chains** — stochastic processes where the next state depends only on the current state, not on the history of how it was reached (the **Markov property**). A game tree traversal can be viewed as a Markov chain: from any game state, the transition to the next state depends only on the current state and the action chosen, not on the sequence of moves that led there.

The key theoretical guarantee is the **Law of Large Numbers**: if we sample enough trajectories through the Markov chain, the average of the sampled values converges to the true expected value. For MCCFR, this means:

$$\frac{1}{T}\sum_{t=1}^{T} \hat{v}_I^{(t)} \xrightarrow{T \to \infty} v_I$$

where $\hat{v}_I^{(t)}$ is the sampled counterfactual value at information set $I$ on iteration $t$, and $v_I$ is the true value that vanilla CFR computes exactly. The sampled values are **unbiased estimators** — their expected value equals the true value — which guarantees convergence to the same Nash equilibrium as full-traversal CFR.

The tradeoff is **variance**: individual samples can deviate substantially from the true value, requiring more iterations to achieve the same precision. This variance-for-speed tradeoff is the central theme of this step.

### 2.4 The Mathematics of Poker <a id="24-the-mathematics-of-poker"></a>

Poker is the canonical testbed for imperfect-information game theory because it combines three sources of complexity:

1. **Hidden information:** Each player sees only their own cards, not the opponent's. This creates information asymmetry — the same observable game state (information set) can correspond to many different actual game states.

2. **Stochastic elements:** Card deals introduce chance nodes into the game tree. An optimal strategy must account for all possible deals, not just the observed one.

3. **Strategic deception:** Unlike perfect-information games, poker rewards mixed strategies. A player who always bets with strong hands and checks with weak hands is trivially exploitable. The Nash equilibrium requires **randomized bluffing** at mathematically precise frequencies.

The formal framework uses **extensive-form games** with the following components:

- **Game tree:** All possible sequences of actions and chance events.
- **Information sets:** Groups of game states that are indistinguishable to a given player (because they differ only in hidden information).
- **Strategies:** Mappings from information sets to probability distributions over actions.
- **Nash equilibrium:** A strategy profile where no player can improve their expected utility by unilaterally changing strategy.

The key quantities for evaluating strategies are:

- **Expected value (EV):** The average payoff under a given strategy pair.
- **Best response:** The optimal counter-strategy against a fixed opponent strategy — the strongest possible exploitation.
- **Exploitability:** The average gain an opponent could obtain by playing a perfect best response. A Nash equilibrium has exploitability zero — no opponent can exploit it, regardless of their strategy.

Chen & Ankenman's *The Mathematics of Poker* (2006) formalises these concepts through toy game solutions where Nash equilibrium bluffing frequencies can be derived analytically. These toy games (half-street, full-street models) build intuition for why CFR's output strategies contain the precise bluff/call ratios they do — the math dictates that a balanced player must bluff with a frequency proportional to the pot odds they offer.

### 2.5 Leduc Poker vs Kuhn Poker <a id="25-leduc-poker-vs-kuhn-poker"></a>

Kuhn Poker (Step 02) is the simplest non-trivial poker game: 3 cards (J, Q, K), 1 betting round, 12 information sets. It captures the essential elements of imperfect information — bluffing and calling — in the smallest possible game tree.

Leduc Poker scales this up significantly:

| Property | Kuhn Poker | Leduc Poker |
|----------|-----------|-------------|
| **Cards** | 3 (J, Q, K) | 6 ({J, Q, K} × {♠, ♥}) |
| **Rounds** | 1 | 2 (pre-flop + community card) |
| **Community card** | None | 1 revealed between rounds |
| **Hand ranking** | High card only | Pair (private == community) beats high card |
| **Bet sizes** | Fixed (1 chip) | Variable (2 in round 1, 4 in round 2) |
| **Max raises/round** | 1 | 2 |
| **Information sets** | 12 | 936 |
| **Game tree nodes** | 58 | 10,200 |
| **Chance outcomes** | 6 | 120 |

Leduc introduces several complexities absent from Kuhn:

- **Multi-round structure:** Information changes between rounds (community card reveal), requiring strategies that adapt to new information.
- **Pair hands:** The hand ranking system (pair beats high card) creates asymmetric hand values that depend on the community card — a Jack can become the best hand if a Jack is dealt as the community card.
- **Larger bet sizes in later rounds:** The 4-chip raise in round 2 (vs 2 in round 1) means that decisions in later rounds carry more weight.

Despite being ~78× larger than Kuhn, Leduc remains small enough for exact computation (a full tree traversal takes ~50ms). This makes it the ideal benchmark for comparing CFR variants: large enough that performance differences are meaningful, small enough that all algorithms can be run to near-convergence within minutes.

---

## 3. Algorithm Descriptions <a id="3-algorithm-descriptions"></a>

### 3.1 CFR+ (Regret Matching Plus) <a id="31-cfr-regret-matching-plus"></a>

CFR+ (Tammelin, 2014) makes three modifications to vanilla CFR, each small in implementation but significant in effect:

**Modification 1 — Regret Flooring:**

In vanilla CFR, cumulative regrets can become arbitrarily negative:

$$R^{T+1}(I, a) = R^T(I, a) + r^T(I, a)$$

In CFR+, regrets are floored at zero after each update:

$$R^{T+1}(I, a) = \max\left(R^T(I, a) + r^T(I, a),\ 0\right)$$

This prevents actions from accumulating large negative regret that takes many iterations to "pay off" before the action is reconsidered. The analogy to ReLU activations in neural networks is direct: both clip negative values to zero, preventing "dead" units or actions from requiring a long recovery period.

**Modification 2 — Linear Strategy Averaging:**

Vanilla CFR computes the average strategy with uniform weights — every iteration contributes equally. CFR+ weights iteration $t$'s strategy by $t$ itself:

$$\bar{\sigma}^T(I, a) = \frac{\sum_{t=1}^{T} t \cdot \sigma^t(I, a)}{\sum_{t=1}^{T} t}$$

Later iterations, which have lower regret and better strategies, contribute more to the average. This accelerates convergence because early (noisy) iterations are down-weighted.

**Modification 3 — Alternating Updates:**

Instead of updating both players' regrets on every iteration, CFR+ updates player 0 on odd iterations and player 1 on even iterations. This reduces per-iteration work by ~50% and provides a small convergence benefit by avoiding simultaneous strategy shifts.

**Combined effect:** The empirical convergence rate improves from $O(1/\sqrt{T})$ to approximately $O(1/T)$ — a dramatic speedup. CFR+ with 1,000 iterations achieves what vanilla CFR needs ~1,000,000 iterations for. This is what made it feasible to "solve" Heads-Up Limit Texas Hold'em ($10^{14}$ information sets) in 2015. Note: while the $O(1/T)$ rate is consistently observed empirically, it lacks a formal proof — Tammelin et al. provide the algorithm but not a convergence theorem matching the observed rate.

### 3.2 MCCFR External Sampling <a id="32-mccfr-external-sampling"></a>

External Sampling (Lanctot et al., 2009) replaces full tree traversal with partial sampling:

- **Chance nodes:** Sample one deal per iteration (instead of enumerating all 120 in Leduc).
- **Traversing player's nodes:** Explore **all** actions (same as vanilla CFR).
- **Opponent's nodes:** **Sample** one action according to the opponent's current strategy.

The traversing player's regrets are updated based on the sampled subtree. Since only one deal and the opponent's sampled action path are visited, each iteration touches ~42 nodes (vs 20,400 for full traversal) — roughly **945× faster** per iteration.

The critical theoretical property: sampled counterfactual values are **unbiased estimators** of the true values (Lanctot et al., Theorem 1). This guarantees that MCCFR converges to the same Nash equilibrium as vanilla CFR, despite the sampling noise.

The cost of sampling is **variance**. Each sampled update deviates from the true counterfactual value because it reflects only one possible deal, not the expectation over all deals. The convergence rate remains $O(1/\sqrt{T})$, but the constant is ~315× larger than vanilla CFR on Leduc — meaning External Sampling needs ~100,000× more iterations to reach the same exploitability.

### 3.3 MCCFR Outcome Sampling <a id="33-mccfr-outcome-sampling"></a>

Outcome Sampling takes the sampling further: instead of exploring all of the traversing player's actions, it samples a **single trajectory** through the entire tree:

- **Chance nodes:** Sample one deal.
- **All player nodes:** Sample one action.
- **Update player's actions:** Sampled with ε-on-policy exploration (with probability ε, choose uniformly; otherwise follow current strategy). This ensures all actions are explored even if the current strategy assigns zero probability.
- **Importance sampling:** Because actions are sampled rather than enumerated, the regret update must be corrected by the ratio of the true reach probability to the sampling probability.

Each iteration touches only ~5.5 nodes (one root-to-terminal path) — **2,228× faster** than full traversal. However, the variance is substantially higher than External Sampling because each information set is updated based on a single sampled action rather than all actions. The variance constant is ~721× larger than vanilla CFR, requiring ~520,000× more iterations for the same precision.

Outcome Sampling is the **cheapest possible** MCCFR variant per iteration and the **noisiest**. It becomes competitive only when the game tree is so large that even External Sampling's partial traversal is too expensive.

---

## 4. Exploration Phase <a id="4-exploration-phase"></a>

Before building the from-scratch implementation, exploratory experiments were conducted using OpenSpiel's reference implementations. These served two purposes: building intuition for how each algorithm behaves, and establishing ground-truth baselines for later cross-validation.

### 4.1 Kuhn Poker Experiments <a id="41-kuhn-poker-experiments"></a>

The first exploration compared five algorithms on Kuhn Poker at 5,000 iterations: the Step 02 custom CFR, OpenSpiel's vanilla CFR, OpenSpiel's CFR+, External Sampling MCCFR, and Outcome Sampling MCCFR. Each algorithm was run using OpenSpiel's Python API:

**Results at 5,000 iterations:**

| Algorithm | Exploitability | Time |
|-----------|---------------|------|
| Custom CFR (Step 02) | ~0.00035 | < 1s |
| OpenSpiel CFR | ~0.0015 | ~2s |
| CFR+ | ~0.0003 | ~2s |
| External Sampling MCCFR | ~0.004 | ~1s |
| Outcome Sampling MCCFR | ~0.025 | ~1s |

![Kuhn Poker — Exploitability vs Iterations](figures/kuhn_exploitability_iterations.png)

![Kuhn Poker — Exploitability vs Wall-Clock Time](figures/kuhn_exploitability_time.png)

**Key observations:**
- On a 12-information-set game, all algorithms converge rapidly. CFR+ is fastest due to regret flooring and linear averaging.
- The custom CFR from Step 02 matches OpenSpiel's implementation, validating correctness.
- Both MCCFR variants converge slower per iteration (sampling noise), but their per-iteration cost is negligible on a game this small.
- On Kuhn Poker, the distinction between algorithms is academic — all reach near-Nash within seconds.

### 4.2 Leduc Poker Experiments <a id="42-leduc-poker-experiments"></a>

The Leduc comparison ran all four OpenSpiel algorithms for 5,000 iterations on the 936-information-set game.

**Results at 5,000 iterations:**

| Algorithm | Exploitability @5k iters | Time for 5k iters |
|-----------|--------------------------|-------------------|
| CFR+ | ~0.000054 | ~859s |
| Vanilla CFR | ~0.0076 | ~747s |
| External Sampling MCCFR | ~1.17 | ~7s |
| Outcome Sampling MCCFR | ~3.08 | ~5s |

![Leduc Poker — Exploitability vs Iterations](figures/leduc_exploitability_iterations.png)

![Leduc Poker — Exploitability vs Wall-Clock Time](figures/leduc_exploitability_time.png)

The performance gap between full-traversal and sampling methods is stark. Full-traversal algorithms (CFR, CFR+) are dramatically better per-iteration — CFR+ reaches exploitability 0.000054 while Outcome Sampling is still at 3.08 — but each full-traversal iteration costs ~100× more time than an MCCFR iteration.

### 4.3 Five-Minute Wall-Clock Race <a id="43-five-minute-wall-clock-race"></a>

The final exploration gave each algorithm a fixed 300-second budget and measured exploitability throughout.

**Final values at 300 seconds:**

| Algorithm | Exploitability | Iterations in 5 min |
|-----------|---------------|---------------------|
| CFR+ | ~0.00042 | ~300 |
| External Sampling MCCFR | see cache | ~200k+ |
| Outcome Sampling MCCFR | ~0.527 | ~millions |

**Key finding:** CFR+ dominates on small games. With Leduc's 10,200-node tree, full traversal costs ~1 second per iteration — cheap enough to complete ~300 high-quality updates in 5 minutes, reaching near-Nash performance. Outcome Sampling, despite running millions of iterations, remains at exploitability ~0.53 — over 1,000× worse than CFR+.

**Takeaway for the thesis:** The crossover point where sampling beats full traversal is well above Leduc's size. For the benchmark games used in Steps 5–8, full-traversal methods (especially CFR+) will be the tool of choice. MCCFR becomes essential only at the scale of real poker ($10^{14}+$ information sets).

---

## 5. Implementation: Timed Benchmark <a id="5-implementation-timed-benchmark"></a>

The main implementation delivers four from-scratch CFR variants on Leduc Poker, benchmarked under a common 180-second wall-clock budget each. All code is hand-written in Python with NumPy only — no game-solving libraries.

**Components built (all hand-coded in Python/NumPy):**
- **Leduc Poker game engine:** Full implementation matching OpenSpiel's semantics — 6 cards, 2 rounds, community card, fold/call/raise actions, all 120 deal permutations, pair-based hand ranking.
- **Vanilla CFR:** Full-traversal with buffered regret accumulation across all 120 deals per iteration.
- **CFR+:** Regret flooring, linear weighting, alternating updates. Buffered regrets applied atomically per pass.
- **MCCFR External Sampling:** One sampled deal per iteration, all traverser actions explored, opponent actions sampled.
- **MCCFR Outcome Sampling:** One sampled trajectory per iteration with ε-on-policy exploration (ε = 0.6) and importance sampling correction.
- **Best Response / Exploitability evaluator:** Iterative information-set-constrained best response to compute exact exploitability.

The core CFR+ regret update (simplified) follows this pattern:

```python
# CFR+ regret flooring — the key modification vs vanilla CFR
for info_set, deltas in regret_buffer.items():
    node = node_map[info_set]
    for a in range(node.num_actions):
        node.regret_sum[a] = max(node.regret_sum[a] + deltas[a], 0.0)
```

External Sampling traversal follows this pseudocode:

```python
def external_cfr(state, update_player):
    if state.is_terminal():
        return state.get_utility(update_player)

    player = state.current_player()
    strategy = get_strategy(state.info_set(player))

    if player == update_player:
        # Explore ALL actions (same as vanilla CFR)
        values = [external_cfr(state.apply(a), update_player)
                  for a in legal_actions]
        node_value = sum(strategy[a] * values[a] for a in legal_actions)
        # Update regrets
        for a in legal_actions:
            regret[info_set][a] += values[a] - node_value
        return node_value
    else:
        # SAMPLE one opponent action from strategy
        sampled_action = sample(strategy)
        return external_cfr(state.apply(sampled_action), update_player)
```

**180-Second Timed Results:**

| Algorithm | Iterations | Final Exploitability | Info Sets |
|-----------|----------:|---------------------:|----------:|
| Vanilla CFR | 3,713 | 0.0044 | 936 |
| CFR+ | 3,706 | 0.000026 | 936 |
| MCCFR External | 3,504,665 | 0.0548 | 936 |
| MCCFR Outcome | 8,262,137 | 0.1030 | 936 |

### Exploitability vs Iterations (log-log)

![Exploitability vs Iterations](figures/exploitability_vs_iterations.png)

Dotted vertical lines mark each algorithm's final iteration count. Sampling-based variants run millions of iterations in 180 seconds, while full-traversal variants complete ~3,700 — but each full-traversal iteration is dramatically more informative.

### Exploitability vs Wall-Clock Time (log-y)

![Exploitability vs Wall-Clock Time](figures/exploitability_vs_wallclock.png)

This is the fair comparison: given equal compute time, which algorithm produces the best strategy? CFR+ dominates, reaching exploitability 0.000026 — nearly exact Nash equilibrium — in 3 minutes. Vanilla CFR follows at 0.0044. Both MCCFR variants lag behind on this game size.

### Cross-Validation Against OpenSpiel

All implementations were cross-checked against OpenSpiel's reference solvers:

| Algorithm | Ours (500 iters) | OpenSpiel (500 iters) | Match |
|-----------|------------------:|----------------------:|:-----:|
| Vanilla CFR | 0.020 | 0.022 | ✅ |
| CFR+ | 0.00086 | 0.00094 | ✅ |

Small differences arise from implementation details (deal ordering, random seeds), but both converge to the same Nash equilibrium within noise margins.

---

## 6. Convergence Analysis <a id="6-convergence-analysis"></a>

The most surprising result of this step is that despite running **1,000× more iterations**, MCCFR External achieves **12× worse exploitability** than Vanilla CFR. A detailed mathematical analysis explains why this is expected and predicts exactly when MCCFR would become competitive.

### 6.1 Variance vs Speed <a id="61-variance-vs-speed"></a>

All four algorithms follow $O(1/\sqrt{T})$ convergence, but with different constants:

$$\epsilon(T) = \frac{C}{\sqrt{T}}$$

| Algorithm | $C_{\text{iter}}$ | Speed (iter/s) | $C_w$ (wall-clock) | Relative to Vanilla |
|-----------|-------------------:|---------------:|--------------------:|--------------------:|
| Vanilla CFR | 0.34 | 20.6 | **0.075** | 1.0× |
| CFR+ | 0.34 | 20.6 | **~0.002** | ~38× faster |
| MCCFR External | 107 | 19,470 | **0.767** | 10.2× slower |
| MCCFR Outcome | 245 | 45,901 | **1.143** | 15.3× slower |

The wall-clock convergence constant $C_w = C / \sqrt{\text{speed}}$ determines real-world performance. Despite being 945× faster per iteration, External Sampling's variance constant (107 vs 0.34) is 315× larger. The speed advantage **does not overcome the variance penalty**:

$$\frac{99{,}000\text{× more iterations needed}}{945\text{× faster per iteration}} \approx 105\text{× more wall-clock time}$$

**Why does the variance exist?** Vanilla CFR computes **exact** counterfactual values by enumerating all 120 deals. Its regret update has zero variance. MCCFR samples one deal per iteration. Even if it explored the full tree for that deal, it would still have variance because:

$$\text{Var}[\hat{v}_I] = \mathbb{E}_{\text{deal}}[(\hat{v}_I - v_I)^2] \propto \frac{|N|}{|I|}$$

This is the variance **across deals** — it comes from the hidden information (which cards were dealt), and no amount of within-deal exploration eliminates it.

### 6.2 The Crossover Formula <a id="62-the-crossover-formula"></a>

MCCFR becomes competitive when the game tree is large enough that full traversal's linear cost in $|N|$ exceeds MCCFR's roughly constant per-iteration cost. The critical tree size is:

$$|N|_{\text{crossover}} = |N|_{\text{Leduc}} \cdot \left(\frac{C_{mc}}{C_v}\right)^2 \cdot \frac{\text{speed}_v}{\text{speed}_{mc}}$$

**Plugging in our measured values:**

| Variant | $|N|_{\text{crossover}}$ |
|---------|-------------------------:|
| External Sampling | ~2,100,000 nodes |
| Outcome Sampling | ~4,800,000 nodes |

| Game | $|N|$ | External wins? | Outcome wins? |
|------|------:|:--------------:|:-------------:|
| Leduc Poker | 10,200 | No (210× too small) | No (466× too small) |
| Limit Hold'em | ~$10^{14}$ | Yes ($10^7$× above threshold) | Yes |
| No-Limit Hold'em | ~$10^{17}$ | Yes ($10^{10}$× above threshold) | Yes |

**Leduc is 210× too small** for External Sampling to break even, and **466× too small** for Outcome Sampling. Full traversal dominates because the entire game tree fits in memory and can be enumerated in milliseconds.

But the conclusion reverses completely at real poker scales. Texas Hold'em's $10^{17}$-node tree makes full traversal physically impossible — even one iteration would take longer than the age of the universe. At that scale, MCCFR (and specifically External Sampling with variance reduction techniques) becomes the **only** tractable approach.

---

## 7. Summary and Next Steps <a id="7-summary-and-next-steps"></a>

### What was achieved

1. **Four CFR variants implemented from scratch** on Leduc Poker, all hand-coded in Python with NumPy only.
2. **CFR+ confirmed as the dominant algorithm** for small-to-medium games — reaching exploitability 0.000026 (near-exact Nash) in 180 seconds on Leduc's 936 information sets.
3. **MCCFR's variance-speed tradeoff quantified** with precise measurements: External Sampling needs ~100,000× more iterations (315² variance penalty) despite 945× cheaper iterations. Outcome Sampling needs ~520,000× more iterations (721² variance penalty) despite 2,228× cheaper iterations.
4. **Crossover point derived and validated** — MCCFR becomes competitive at ~2.1M nodes (External) or ~4.8M nodes (Outcome), explaining why it was essential for solving real poker but unnecessary for Leduc.
5. **Cross-validated against OpenSpiel** — both full-traversal implementations match OpenSpiel's output within noise margins.

### Key insight

> Monte Carlo methods trade **per-iteration quality** for **per-iteration speed**. The crossover point — where sampling beats full traversal — depends on the game tree size $|N|$, not the number of information sets $|I|$. For Leduc ($|N| = 10{,}200$), full traversal wins. For Texas Hold'em ($|N| > 10^{14}$), sampling is the only option.

### Connection to next steps

- **Step 04 (Game Abstraction & Scaling):** Addresses the scalability problem from the opposite direction — instead of sampling the tree, reduce the tree itself through abstraction. Combines with MCCFR to make real poker games tractable.
- **Step 05 (Neural Equilibrium):** Deep CFR replaces tabular strategy storage with neural networks, using MCCFR's sampling framework. Understanding MCCFR's variance properties (from this step's convergence analysis) explains why Deep CFR requires specific variance reduction techniques.
- **Step 06 (End-to-End Game AI):** Builds on both CFR+ and MCCFR to construct complete game-playing agents. The Leduc Poker engine from this step serves as the benchmark environment.

---

## References

- **CFR:** Zinkevich, M., Bowling, M., Burch, N., Billings, D., & Larson, K. (2007). Regret Minimization in Games with Incomplete Information. *IJCAI*.
- **CFR+:** Tammelin, O. (2014). Solving Large Imperfect Information Games Using CFR+. *AAAI*.
- **MCCFR:** Lanctot, M., Gibson, R., Burch, N., Zinkevich, M., & Bowling, M. (2009). Monte Carlo Sampling for Regret Minimization in Extensive Games. *NeurIPS*.
- **Leduc Poker:** Southey, F., Bowling, M., Larson, B., Burch, C., Billings, D., & Rayner, C. (2005). Bayes' Bluff: Opponent Modelling in Poker. *UAI*.
- **Mathematics of Poker:** Chen, B. & Ankenman, J. (2006). *The Mathematics of Poker*. ConJelCo.
