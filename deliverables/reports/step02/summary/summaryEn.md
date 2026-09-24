---
title: "Chapter 2 Summary — Game Theory & CFR Basics"
subtitle: "Research on the possibilities for applying Artificial Intelligence in computer games"
author: "Alexander Andreev"
date: "April 2026"
lang: en
vars:
  research_focus: "Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments"
---

# Chapter 2 — Game Theory & CFR Basics

---

## From Single-Agent RL to Multi-Agent Strategic Interaction

Chapter 1 treated environments as passive — the cart-pole doesn't fight back, the lander doesn't try to crash you. The agent optimized against fixed dynamics. Chapter 2 introduces a fundamentally different problem: the environment includes another *strategic* decision-maker whose actions depend on yours.

This shift breaks the MDP framework. In a single-agent setting, the optimal policy is fixed — there exists a single best way to act regardless of what strategy you considered before. In a multi-agent setting, the "best" strategy depends on what the opponent does, and the opponent's best strategy depends on what you do. This circularity is the core challenge of game theory.

The formalization begins with **normal-form games** (simultaneous moves, like Rock-Paper-Scissors) and extends to **extensive-form games** (sequential moves with a tree structure, like poker). In both cases, the solution concept shifts from "optimal policy" to **Nash equilibrium** — a strategy profile where no player can improve by unilaterally changing their own strategy.[^shoham2008]

---

## Extensive-Form Games and Information Sets

An **extensive-form game** represents strategic interaction as a tree. Each node is a decision point for one player (or "chance" for random events like card deals). Edges represent actions, and leaves carry payoffs for each player.

The critical distinction is between **perfect** and **imperfect** information:

- **Perfect information** (chess, Go): every player sees the full game state. The game tree has no grouped nodes — each node is its own information set. Minimax and alpha-beta pruning solve these games.
- **Imperfect information** (poker, many real-world problems): players cannot observe some aspects of the state. In poker, you see your own cards but not your opponent's. This means multiple game states are *indistinguishable* to the acting player.

An **information set** groups all game states that a player cannot tell apart. At an information set, the player must choose the same strategy for all states in the group (since they cannot distinguish them). This constraint is what makes imperfect-information games fundamentally harder than perfect-information ones — you cannot simply pick the best action for each state; you must pick one action that works well *on average* across all states in the information set.

In Kuhn Poker, the information set `"2pb"` contains two game states: "I hold Queen, opponent holds Jack, history is pass-bet" and "I hold Queen, opponent holds King, history is pass-bet." The player holding Queen cannot distinguish these and must use the same strategy (call probability) for both.[^shoham2008]

---

## Minimax Theorem

The Minimax Theorem, established by John von Neumann in 1928,[^vonneumann1928] provides a foundational solution concept for two-player zero-sum games. It states that for every finite, two-player, zero-sum game, there exists a strategy for both players where the maximum expected loss is minimized. In other words, each player can guarantee a specific expected payoff, known as the "value of the game," regardless of the opponent's strategy. This creates a scenario where one player's optimal strategy is to maximize their minimum reward (maximin), while the opponent seeks to minimize the first player's maximum reward (minimax). The theorem states that, with mixed strategies, these two values are always equal; their common value is the value of the game. The theorem relates directly to Nash equilibrium: in the specific case of two-player zero-sum games, a Minimax strategy profile is equivalent to a Nash equilibrium. Discovering this Minimax solution guarantees safety against any exploitative strategy the opponent might employ.

---

## Nash Equilibrium

A **Nash equilibrium** is a strategy profile where each player's strategy is a best response to every other player's strategy. Formally, for each player $i$:

$$u_i(\sigma_i^*, \sigma_{-i}^*) \geq u_i(\sigma_i, \sigma_{-i}^*) \quad \forall \sigma_i$$

No player can improve their expected payoff by unilaterally deviating. This does not mean everyone is happy with the outcome (Prisoner's Dilemma), just that no one can do better by changing only their own strategy.

In games extended to more than two players (N-player games) or general-sum games, the properties of Nash equilibrium become significantly more complex. In these settings, computing a Nash equilibrium is PPAD-complete, even for two-player general-sum games, and is therefore believed to be intractable.[^daskalakis2009][^chen2009] Furthermore, the equilibria lose their safety guarantee: playing a Nash strategy in a 3-player game does not protect against two opponents who might deviate from equilibrium, potentially forming temporary coalitions that exploit the third player.[^szafron2013] This dynamic necessitates entirely different evaluation and training frameworks (such as those discussed in Chapters 9 and 11) since the direct equivalence between Nash and minimax optimality no longer holds.

**Key properties:**

- **Existence:** Nash (1950)[^nash1950] proved that every finite game has at least one Nash equilibrium (possibly in mixed strategies). This is a foundational theorem but does not help with computation.
- **Uniqueness:** Games may have multiple equilibria. Kuhn Poker has a one-parameter *family* of Nash equilibria indexed by $\alpha \in [0, 1/3]$.
- **Mixed strategies:** In many games, the equilibrium requires randomization. In Kuhn Poker, the Nash equilibrium has Player 1 (the second to act) bluffing with Jack exactly 1/3 of the time — any other frequency is exploitable.

For 2-player zero-sum games (where one player's gain is the other's loss), Nash equilibria have a special property: they are **minimax optimal**. Playing your Nash strategy guarantees you at least the game value, regardless of what the opponent does. This is the safety guarantee that makes Nash equilibrium the baseline for poker AI.[^nash1950]

---

## Regret Matching — The Building Block

Before CFR can minimize regret across a game tree, we need a mechanism to minimize regret at a single decision point. **Regret matching** is that mechanism.

The idea: after many rounds of play, for each action $a$, compute the **cumulative regret** — how much better you would have done if you had always played $a$ instead of your actual mixed strategy. Then set your next strategy proportional to the *positive* regrets:

$$\sigma^{T+1}(a) = \begin{cases} \frac{R^{T,+}(a)}{\sum_{a'} R^{T,+}(a')} & \text{if } \sum > 0 \\ \frac{1}{|A|} & \text{otherwise} \end{cases}$$

**Convergence guarantee:** Blackwell (1956)[^blackwell1956] and Hart & Mas-Colell (2000)[^hartmascolell2000] proved that regret matching ensures average regret converges to zero at rate $O(1/\sqrt{T})$ (cumulative regret grows no faster than $O(\sqrt{T})$). In a two-player zero-sum game, if both players use regret matching at their respective decision points, the average strategy profile converges to a Nash equilibrium.

A simple example is Rock-Paper-Scissors. If you play regret matching against a fixed opponent who always plays Rock, your cumulative regret for Paper will grow (Paper beats Rock), while regret for Scissors turns negative and has no effect on the strategy. The strategy quickly moves to Paper, the correct best response.[^neller2013]

---

## Counterfactual Regret Minimization (CFR)

CFR (Zinkevich et al., 2007)[^zinkevich2007] extends regret matching to extensive-form games. The key insight: decompose the total regret of a game strategy into **local regrets** at each information set, then minimize each local regret independently using regret matching. If each information set's average regret converges to zero, the overall *average* strategy converges to a Nash equilibrium.

**The "counterfactual" part** is crucial. At each information set $I$, the regret for action $a$ is not simply "how much better $a$ would have been." It is the *counterfactual* regret — the improvement assuming the player had intentionally played to reach $I$ (reach probability = 1 for the player) but everything else (opponent strategy, chance events) stayed the same. Formally:

$$R^T(I, a) = \sum_{t=1}^{T} \pi_{-i}^t \cdot \left(v^t(I, a) - v^t(I)\right)$$

where $\pi_{-i}^t$ is the opponent's reach probability and $v^t(I, a)$ is the counterfactual value of action $a$ at $I$ on iteration $t$.

**Why opponent reach probability?** The regret at an information set matters more when the opponent is likely to have played such that we reach that information set. Weighting by $\pi_{-i}$ ensures that regret is proportional to the frequency with which the information set is "relevant" to the game outcome.

**Algorithm (CFR with chance sampling, as in Neller & Lanctot, 2013[^neller2013]):**

1. Initialize all cumulative regrets and strategy sums to zero
2. For $T$ iterations:
   a. Sample a random card deal (chance sampling)
   b. Recursively traverse the game tree from root
   c. At each info set, compute strategy via regret matching
   d. For each action, recurse into the subtree (negating utility for zero-sum)
   e. Update cumulative regrets weighted by opponent reach probability
   f. Accumulate strategy weighted by player's own reach probability
3. Output the **average** strategy (not the final iteration's strategy)

**Convergence:** The average strategy profile converges to Nash equilibrium at rate $O(1/\sqrt{T})$ for exploitability, where $T$ is the number of iterations (Theorem 4, Zinkevich et al. 2007). The convergence bound is:

$$\text{exploit}(\bar{\sigma}^T) \leq \frac{\Delta\,|\mathcal{I}|\,\sqrt{|A|}}{\sqrt{T}}$$

where $\Delta$ is the range of payoffs, $|\mathcal{I}|$ the number of information sets of both players and $|A|$ the largest number of actions at an information set.[^zinkevich2007] The bound is linear in $|\mathcal{I}|$; a tighter bound was proved later.[^lanctot2009]

---

## The Mathematics of Poker

Poker is the canonical testbed for imperfect-information game theory because it combines three sources of complexity that rarely co-occur:

1. **Hidden information** — each player sees only their own cards. The same observable game state (information set) can correspond to many different underlying game states.
2. **Stochastic elements** — card deals introduce chance nodes into the game tree. An optimal strategy must account for all possible deals, not just the observed one.
3. **Strategic deception** — unlike perfect-information games, poker rewards mixed strategies. A player who always bets with strong hands and checks with weak ones is trivially exploitable. Nash equilibrium requires **randomized bluffing at mathematically precise frequencies**.

Chen & Ankenman formalise these concepts through toy-game solutions where Nash bluffing frequencies can be derived analytically. Their half-street and full-street models build intuition for why CFR's output strategies contain the precise bluff/call ratios they do — a balanced player must bluff with a frequency proportional to the pot odds they offer.[^chen2006]

---

## Kuhn Poker — The Simplest Testbed

Kuhn Poker (Kuhn, 1950) is the standard minimal example for imperfect-information game algorithms. With only 3 cards, 2 players, and 12 information sets, it is small enough to solve analytically yet rich enough to exhibit the key phenomena: bluffing, information asymmetry, mixed equilibria.

**Rules:** 3 cards {J, Q, K}, each player antes 1 chip, each receives 1 private card. Player 0 acts first: pass or bet. Player 1 responds: pass or bet. If Player 0 passed and Player 1 bet, Player 0 gets to respond again. Showdown with higher card winning.

**Nash equilibrium (parameterized by $\alpha \in [0, 1/3]$):**

- **Player 0 with J:** Bet (bluff) with probability $\alpha$. If facing bet after passing, always fold.
- **Player 0 with Q:** Always pass. If facing bet after passing, call with probability $1/3 + \alpha$.
- **Player 0 with K:** Bet with probability $3\alpha$. If facing bet after passing, always call.
- **Player 1 with J:** After pass, bet (bluff) with probability 1/3. After bet, always fold.
- **Player 1 with Q:** After pass, always pass. After bet, call with probability 1/3.
- **Player 1 with K:** Always bet, always call.

(Player 1's strategy is the same in every equilibrium; only Player 0's depends on $\alpha$. The strategy CFR reaches is shown in the last figure under "Empirical Visualizations".)

**Game value:** Player 0's expected payoff at Nash is $-1/18 \approx -0.0556$. Player 0 has a structural disadvantage from acting first. The first figure under "Empirical Visualizations" shows how training approaches this value.

**Why Kuhn matters:** Every key concept in imperfect-information game solving appears here in miniature — bluffing (J bets despite being worst card), information asymmetry (Player 1 sees Player 0's action but not their card), mixed strategies (exact 1/3 bluff frequency), indifference (Q is indifferent between call and fold at certain info sets). If your algorithm cannot solve Kuhn correctly, it cannot solve anything.[^kuhn1950]

---

## Exploitability — Measuring Distance from Nash

**Exploitability** is the primary evaluation metric for strategies in imperfect-information games. It measures how much a strategy can be exploited by a worst-case opponent:

$$\text{exploit}(\sigma) = BR_0(\sigma_1) + BR_1(\sigma_0)$$

where $BR_i(\sigma_{-i})$ is the expected payoff of player $i$'s best response to the opponent's strategy. In a two-player zero-sum game this sum is also called NashConv; OpenSpiel reports half of it as "exploitability", so the two conventions differ by a factor of 2.

At Nash equilibrium, exploitability is exactly zero — neither player can improve by deviating. For approximate Nash equilibria, exploitability quantifies the approximation quality.

**Best response computation** in imperfect-information games is subtle. The best-responding player must choose the same action at all states within an information set (they cannot distinguish them). A naive approach that picks the best action per game state (using knowledge of the opponent's private card) computes an "oracle" value, not a true best response. For Kuhn Poker, a brute-force approach that enumerates all 2⁶ = 64 pure strategies suffices; larger games need a single bottom-up traversal that aggregates over information sets.

**Convergence rate:** In theory, the exploitability of CFR's average strategy decreases as $O(1/\sqrt{T})$[^zinkevich2007] (see the second figure under "Empirical Visualizations"). On a log-log plot, this appears as a line with slope $\approx -0.5$. Over five seeds, with checkpoints from 100 to 100,000 iterations, the measured slope is $-0.52 \pm 0.02$, consistent with the $O(1/\sqrt{T})$ bound, which is an upper limit rather than a prediction of the exact rate.

**Why not just game value?** A strategy can achieve the correct game value while still being exploitable. Consider a Kuhn strategy where Player 1 always bluffs with J (instead of 1/3 of the time). The average game value might be close to $-1/18$, but the strategy is highly exploitable — Player 0 can always call with Q and profit. Exploitability catches this; game value alone does not.

> **This metric recurs throughout the thesis.** Chapters 7–8 (opponent modeling, safe exploitation) use exploitability as the primary measure. It is also the starting point of the thesis's evaluation methodology (Contribution #3).

---

## Connections to Chapter 1 and Forward Pointers

**Local optimization → global convergence.** In Chapter 1, Q-learning reduces the TD error one state at a time, yet in the tabular case the Q-function provably converges to the optimum; DQN keeps the update rule but, with a neural network, loses the guarantee. In Chapter 2, CFR minimizes regret at each information set independently, yet the overall *average* strategy converges to Nash. Both demonstrate the same principle: local updates, when properly structured, achieve global objectives.

**Strategy accumulation ≈ experience replay.** CFR outputs the *average* strategy, not the last iteration's strategy. This averaging stabilizes convergence, just as experience replay in DQN stabilizes learning by preventing the agent from over-fitting to recent transitions. Both are memory mechanisms that smooth out noise.

**Forward:** The implementation here samples one card deal per iteration (chance sampling) but traverses every action sequence of that deal, so each iteration still touches a large part of the tree. For larger games even this is too expensive.[^bowling2015] Chapter 3 introduces Monte Carlo CFR (MCCFR), which samples parts of the tree, trading exactness for scalability. Chapter 4 adds game abstraction, reducing the game size. Chapter 5 replaces tabular strategies with neural networks.

---

## Empirical Visualizations

To validate the theoretical guarantees of CFR and its application to Kuhn Poker, several metrics were tracked during the training process:

![The running mean of Player 0's payoff over the sampled deals, averaged from the start of training, fluctuates around the theoretical value $-1/18$ within sampling noise. The exact value of the average strategy after 100,000 iterations is $-0.0555$.](game_value_convergence.png)

![Exploitability of the average strategy against the number of iterations, log-log scale, mean over five seeds; the shaded band is their range. The measured points roughly follow the $O(1/\sqrt{T})$ reference slope (dashed line), consistent with the theoretical bound.](exploitability_convergence.png)

![The average strategy CFR finds for Kuhn poker after 100,000 iterations: action probabilities at each information set. The Jack's bluffing and the Queen's calling frequencies are close to the Nash equilibrium family ($\alpha \approx 0.18$).](strategy_analysis.png)

<!-- Source footnotes. Definitions may sit anywhere at top level; keeping them
     together here keeps the prose readable and the EN/BG pair easy to compare. -->

[^vonneumann1928]: von Neumann, J. (1928). "Zur Theorie der Gesellschaftsspiele." *Mathematische Annalen*, 100(1), 295-320. English translation: "On the Theory of Games of Strategy," in *Contributions to the Theory of Games*, Vol. 4 (1959), 13-42.

[^nash1950]: Nash, J.F. (1950). "Equilibrium Points in N-Person Games." *Proceedings of the National Academy of Sciences*, 36(1), 48-49.

[^blackwell1956]: Blackwell, D. (1956). "An Analog of the Minimax Theorem for Vector Payoffs." *Pacific Journal of Mathematics*, 6(1), 1-8.

[^hartmascolell2000]: Hart, S. & Mas-Colell, A. (2000). "A Simple Adaptive Procedure Leading to Correlated Equilibrium." *Econometrica*, 68(5), 1127-1150.

[^zinkevich2007]: Zinkevich, M., Johanson, M., Bowling, M. & Piccione, C. (2007). "Regret Minimization in Games with Incomplete Information." *Advances in Neural Information Processing Systems 20*, 1729-1736.

[^shoham2008]: Shoham, Y. & Leyton-Brown, K. (2008). *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations*. Ch. 3 (games in normal form; §3.3 best response and Nash equilibrium, §3.4.1 maxmin and minmax strategies); §4.1 (computing Nash equilibria of two-player zero-sum games); Ch. 5 (extensive-form games; §5.2 imperfect information and information sets, §5.2.3 the sequence form); §7.5 "No-regret learning and universal consistency". Free: <http://www.masfoundations.org/download.html>

[^neller2013]: Neller, T.W. & Lanctot, M. (2013). "An Introduction to Counterfactual Regret Minimization," §2–3 (version of 9 July 2013).

[^chen2006]: Chen, B. & Ankenman, J. (2006). *The Mathematics of Poker*. ConJelCo — analytical Nash derivations for toy poker games.

[^kuhn1950]: Kuhn, H.W. (1950). "Simplified Two-Person Poker." *Contributions to the Theory of Games*, Vol. 1, Annals of Mathematics Studies 24, Princeton University Press, 97–103.

[^bowling2015]: Bowling, M., Burch, N., Johanson, M. & Tammelin, O. (2015). "Heads-up limit hold'em poker is solved." *Science*, 347(6218), 145–149. Used CFR+ to solve heads-up limit Texas Hold'em — the first non-trivial imperfect-information game played competitively by humans to be (essentially weakly) solved.

[^lanctot2009]: Lanctot, M., Waugh, K., Zinkevich, M. & Bowling, M. (2009). "Monte Carlo Sampling for Regret Minimization in Extensive Games." *Advances in Neural Information Processing Systems 22*, 1078–1086.

[^daskalakis2009]: Daskalakis, C., Goldberg, P. W. & Papadimitriou, C. H. (2009). "The Complexity of Computing a Nash Equilibrium." *SIAM Journal on Computing*, 39(1), 195–259.

[^chen2009]: Chen, X., Deng, X. & Teng, S.-H. (2009). "Settling the Complexity of Computing Two-Player Nash Equilibria." *Journal of the ACM*, 56(3), 1–57.

[^szafron2013]: Szafron, D., Gibson, R. & Sturtevant, N. (2013). "A Parameterized Family of Equilibrium Profiles for Three-Player Kuhn Poker." *Proc. AAMAS 2013*, 247–254. In three-player Kuhn poker one player can transfer utility from one opponent to the other while staying within the equilibrium family.
