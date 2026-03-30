## Glossary

```{=latex}
\small
```

### Game Theory

**[1] Best response.** A strategy that maximizes a player's expected payoff given fixed strategies of all other players. Computing a best response against a candidate strategy is the standard method for measuring that strategy's exploitability.

**[2] Counterfactual value.** The expected payoff a player would receive at a given decision point, computed under the assumption that the player acts to reach that point while all other players follow their current strategies. The central quantity in the CFR algorithm.

**[3] Exploitability.** A quantitative measure of how far a strategy profile deviates from Nash equilibrium, defined as the sum of the payoff gains achievable by best-response opponents. An exploitability of zero indicates an exact Nash equilibrium.

**[4] Extensive-form game.** A representation of a sequential game as a tree structure, specifying players, available actions, information sets, chance events, and terminal payoffs. The standard formal model for imperfect-information games.

**[5] Imperfect information.** A property of games in which players do not observe all actions previously taken by other players or by nature. Not to be confused with incomplete information, which refers to uncertainty about the game's rules or other players' preferences.

**[6] Information set.** A set of game states that are indistinguishable to the acting player due to hidden information. A strategy must prescribe the same action distribution across all states within a single information set.

**[7] Nash equilibrium.** A strategy profile in which no player can unilaterally increase their expected payoff by changing their own strategy. In two-player zero-sum games, Nash equilibrium strategies are unexploitable by definition.

**[8] Zero-sum game.** A game in which the payoffs of all players sum to zero at every terminal state. The strictly competitive setting in which regret-minimization algorithms such as CFR are guaranteed to converge to Nash equilibrium.

### Reinforcement Learning

**[9] Experience replay.** A technique in which past transitions (state, action, reward, next state) are stored in a buffer and sampled in mini-batches for training, reducing temporal correlation and improving learning stability.

**[10] Markov decision process (MDP).** A mathematical model for sequential decision-making in which the transition to the next state depends only on the current state and action. The standard formalism for single-agent reinforcement learning problems.

**[11] Policy.** A mapping from observations to a probability distribution over actions. Policies may be deterministic (selecting a single action) or stochastic (assigning probabilities to multiple actions).

**[12] Policy gradient.** A family of reinforcement learning methods that directly optimize a parameterized policy by estimating the gradient of expected cumulative reward with respect to the policy parameters.

**[13] Reinforcement learning (RL).** A branch of machine learning in which an agent learns to select actions within an environment so as to maximize cumulative reward over time, through a process of trial, error, and delayed feedback.

**[14] Value function.** A function estimating the expected cumulative reward from a given state (state-value function, $V$) or state–action pair (action-value function, $Q$) under a given policy.

### Algorithms

**[15] Counterfactual Regret Minimization (CFR).** An iterative algorithm for approximating Nash equilibrium strategies in two-player zero-sum extensive-form games. Each iteration traverses the game tree, computes counterfactual values, accumulates regrets per action, and updates the strategy via regret matching. The average strategy converges to equilibrium at a rate of $O(1/\sqrt{T})$.

**[16] Deep Q-Network (DQN).** A reinforcement learning algorithm that approximates the optimal action-value function using a deep neural network, stabilized by experience replay and a periodically updated target network.

**[17] Proximal Policy Optimization (PPO).** A policy gradient algorithm that stabilizes training by constraining each update step via a clipped surrogate objective function, preventing excessively large policy changes.

**[18] Regret matching.** A decision rule in which each action is selected with probability proportional to its accumulated positive regret. When applied iteratively within the CFR framework, the resulting average strategy profile converges to Nash equilibrium.

**[19] Kuhn Poker.** A simplified poker variant with a three-card deck (Jack, Queen, King), two players, and a single betting round. Kuhn Poker has a known analytical Nash equilibrium (game value $\approx -1/18$ for the first player) and serves as the standard minimal testbed for imperfect-information game algorithms.

**[20] Leduc Hold'em.** A two-round poker variant with a six-card deck (three ranks, two suits) and one community card, producing approximately 936 information sets. Used as an intermediate benchmark between Kuhn Poker and full-scale poker games.

**[21] Game abstraction (lossless / lossy).** A technique for reducing the size of a game by merging states that are strategically equivalent (lossless) or approximately similar (lossy). Lossless abstractions preserve the exact equilibrium of the original game; lossy abstractions trade solution quality for computational tractability, quantified by the exploitability gap between the abstracted and original solutions.

**[22] Subgame solving.** A real-time refinement technique that re-solves a portion of the game tree at a finer granularity than the pre-computed blueprint strategy. Safe subgame solving guarantees that the refined strategy is no more exploitable than the original blueprint.

**[23] Monte Carlo CFR (MCCFR).** A family of CFR variants that sample portions of the game tree rather than traversing it in full on each iteration. Reduces per-iteration cost at the expense of introducing sampling variance. Common instantiations include external sampling (samples opponent and chance actions) and outcome sampling (samples a single trajectory).

**[24] CFR+.** An accelerated variant of CFR that applies three modifications: flooring negative regrets to zero, alternating which player's strategy is updated, and weighting later iterations more heavily. Empirically achieves $O(1/T)$ convergence — substantially faster than the $O(1/\sqrt{T})$ rate of vanilla CFR.

**[25] Deep CFR.** A neural variant of CFR that replaces tabular regret and strategy storage with deep neural networks (advantage networks and a strategy network). Training data is generated via external-sampling MCCFR traversals and maintained using reservoir sampling, enabling equilibrium approximation in games too large for tabular methods.

**[26] DREAM (Deep Regret minimization with Advantage baselines and Model-free learning).** An outcome-sampling variant of Deep CFR that uses baseline subtraction to reduce sampling variance. Achieves comparable solution quality with a single-network architecture.

**[27] Neural Fictitious Self-Play (NFSP).** An equilibrium-finding algorithm that combines a deep Q-network for best-response computation with a supervised-learning network for average strategy approximation. An anticipatory parameter $\eta$ interpolates between Nash equilibrium play and exploitative best-response play.

**[28] ReBeL (Recursive Belief-based Learning).** A game-solving framework that combines self-play reinforcement learning with search over public belief states. Enables AlphaZero-style learning and planning for imperfect-information games without requiring pre-computed blueprint strategies or explicit game abstraction.

**[29] Public belief state (PBS).** A probability distribution over all possible private information assignments, maintained and updated via Bayes' rule as public actions are observed. The PBS serves as a sufficient statistic for decision-making in imperfect-information games and is the central representation in the ReBeL architecture.

### Opponent Modeling and Exploitation

**[30] Opponent modeling.** The process of inferring an opponent's strategy, intentions, or type from observed behavioral traces during play. Opponent models may be explicit (maintaining a belief distribution over opponent strategies) or implicit (adapting one's own strategy directly from observations without constructing an explicit belief).

**[31] Bayesian opponent modeling.** An opponent modeling approach that maintains a prior distribution over possible opponent types or action frequencies and updates it via Bayes' rule as new observations are collected. Type-based variants use Dirichlet-multinomial conjugacy for closed-form posterior updates; continuous variants estimate per-information-set action distributions.

**[32] Restricted Nash Response (RNR).** A safe exploitation algorithm that constructs a strategy blending Nash equilibrium play with best-response exploitation. A safety parameter $p \in [0,1]$ controls the tradeoff: at $p = 0$ the strategy is a pure best response, and at $p = 1$ it is the Nash equilibrium itself. Formulated as a linear program.

**[33] Safe exploitation.** The problem of adapting one's strategy to exploit a modeled opponent's weaknesses while maintaining provable guarantees against worst-case loss. In two-player zero-sum games, the Safety Theorem (Ganzfried and Sandholm, 2015) ensures that an exploitation strategy anchored to a Nash equilibrium baseline cannot lose more than the baseline against any opponent.

**[34] Teaching attack.** An adversarial strategy in which an opponent deliberately plays suboptimally to manipulate an adaptive agent's opponent model, then switches to an exploitative strategy once the agent has been misled. Resilience to teaching attacks is a key robustness criterion for opponent modeling systems.

**[35] Adaptation safety.** A safety notion (Ge et al., 2024) requiring that an exploitation strategy be no more exploitable than the blueprint baseline strategy from which it was derived. A weaker but more practically achievable guarantee than strict Nash safety, applicable to settings where the baseline is an approximate rather than exact equilibrium.

### Multi-Agent Dynamics

**[36] Non-stationarity (multi-agent).** The fundamental challenge that arises when multiple agents learn simultaneously: each agent's environment — which includes the other agents — changes as those agents update their policies, violating the stationarity assumption of single-agent reinforcement learning.

**[37] Centralized Training with Decentralized Execution (CTDE).** A multi-agent reinforcement learning paradigm in which agents have access to global information (other agents' observations and actions) during training but execute using only local observations at deployment. Representative algorithms include MADDPG (centralized critic, decentralized actors), QMIX (monotonic value decomposition), and MAPPO (PPO with centralized value function).

**[38] Policy Space Response Oracles (PSRO).** A population-based framework that maintains a growing set of policies and iteratively computes meta-Nash equilibria over the current population, then trains new best-response policies via reinforcement learning. Unifies fictitious play, self-play, and the double oracle method as special cases.

**[39] Population-Based Training (PBT).** A meta-optimization framework in which a population of agents trains in parallel, periodically copying weights from high-performing agents (exploit) and mutating hyperparameters (explore). The AlphaStar league is the landmark application, with three agent roles — main agents, main exploiters, and league exploiters — maintaining population diversity and robustness.

**[40] Learning with Opponent-Learning Awareness (LOLA).** A multi-agent learning algorithm in which each agent differentiates through the anticipated parameter update of its opponent, enabling anticipatory adaptation rather than reactive best-response. Achieves cooperation in settings where naive independent learners converge to suboptimal outcomes.

**[41] Coalition.** A subset of players in an N-player game who coordinate their strategies for mutual benefit. In free-for-all settings, coalitions may form and dissolve dynamically during play, creating a social structure that cannot be captured by two-player game-theoretic frameworks.

**[42] Spinning top decomposition.** A decomposition (Balduzzi et al., 2019) of any antisymmetric payoff matrix into a transitive component (representing genuine skill ranking) and a cyclic component (representing non-transitive, rock-paper-scissors structure). The transitive ratio serves as a diagnostic distinguishing real improvement from illusory cycling in population-based training.

**[43] Empirical Game-Theoretic Analysis (EGTA).** A framework for analyzing multi-agent systems by constructing finite empirical games over sampled strategy sets and computing Nash equilibria of the resulting meta-game. Generalizes two-player exploitability to the population setting and provides approximation bounds for empirical Nash convergence.

**[44] Shapley value.** A solution concept from cooperative game theory that assigns each player a payoff equal to their average marginal contribution across all possible coalition orderings. Applied in multi-agent reinforcement learning as a credit assignment mechanism (Shapley Q-value) that decomposes joint rewards into per-agent attributions.

**[45] So Long Sucker (SLS).** A four-player coalition formation game designed by Nash, Shapley, Shubik, and Hausner (1950) in which players must form temporary alliances to eliminate opponents but only one player can win. Serves as a benchmark for studying dynamic coalition formation, betrayal, and negotiation in competitive multi-agent settings.

### Data-Driven Approaches

**[46] Decision Transformer (DT).** A sequence model architecture that reformulates offline reinforcement learning as return-conditioned sequence prediction. A GPT-2 backbone predicts actions from (return-to-go, state, action) token sequences, matching or exceeding value-based offline RL methods without temporal-difference learning or Bellman backups. Subject to a critical limitation in stochastic environments, where return conditioning conflates lucky outcomes with skilled decisions.

**[47] Adversarially Robust Decision Transformer (ARDT).** An extension of the Decision Transformer that conditions on minimax returns-to-go via expectile regression rather than empirical returns — recovering near-Nash equilibrium strategies from offline data in sequential games with sufficient data coverage. Addresses the standard Decision Transformer's vulnerability in adversarial settings.

**[48] Player embedding (player2vec).** A vector representation of a player's behavioral patterns, obtained by treating in-game actions as tokens and training a Transformer encoder with masked action prediction on sequences of a player's hands. Produces representations that cluster by behavioral style without requiring manual labels.

**[49] VPIP (Voluntarily Put In Pot).** A standard poker behavioral statistic measuring the percentage of hands in which a player voluntarily contributes chips to the pot before the flop. Combined with PFR (Pre-Flop Raise percentage), VPIP forms the primary axis for classifying player archetypes (tight versus loose, passive versus aggressive).

**[50] Collusion detection.** The problem of identifying coordinated play among ostensibly independent players in multiplayer games. Detection signals include co-occurrence anomaly (pairs appearing together more often than expected), chip dumping (directional monetary transfer between colluding players), and soft play (reduced aggression against specific opponents). Extends the coalition detection methodology of Step 11 to a practical fraud detection application.

### Evaluation and Integration

**[51] Approximate exploitability.** A method for estimating exploitability in games too large for exact best-response computation, by training an RL-based best-response agent against the strategy under evaluation. The trained agent's payoff provides a lower bound on the true exploitability.

**[52] $\alpha$-Rank.** A multi-agent evaluation method based on evolutionary dynamics. Constructs a Markov chain over the strategy population using a Fermi selection function; the stationary distribution assigns each strategy a ranking that captures both transitive dominance and cyclic competitive structure. Unlike Elo, $\alpha$-Rank is sensitive to intransitive (rock-paper-scissors) relationships.

**[53] VasE (Voting as Stochastic Estimation).** An evaluation method grounded in social choice theory. Constructs a tournament matrix from pairwise agent comparisons across games and computes maximal lotteries via linear programming. Detects intransitive cycles that Elo-based rankings cannot capture and provides a principled aggregation of performance across heterogeneous evaluation domains.

**[54] AIVAT.** A variance reduction technique for evaluating agents in imperfect-information games (Burch, Johanson, and Bowling, 2019). Uses a control variate derived from the CFR value function to make counterfactual adjustments at each chance node, reducing evaluation variance by an order of magnitude while maintaining an unbiased estimator.

**[55] Marginal exploitability.** An extension of standard exploitability to N-player settings. Measures each player's incentive to deviate unilaterally from the current strategy profile, accounting for the fact that in multiplayer games the concept of a unique best response is complicated by coalition structures and non-unique equilibria.

```{=latex}
\normalsize
```
