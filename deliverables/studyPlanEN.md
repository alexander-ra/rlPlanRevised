---
title: "Individual Study Plan"
subtitle: "Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments"
author: "Alexander Andreev"
date: "March 2026"
lang: en
---

# Individual Study Plan

## Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments

|                          |                                                                 |
|--------------------------|-----------------------------------------------------------------|
| **Doctoral Student**     | Alexander Andreev                                               |
| **University**           | University of Ruse "Angel Kanchev"                              |
| **Scientific Area**      | 4.6 Informatics                                                 |
| **Scientific Supervisor**| Prof. Dr. Tsvetomir Vasilev                                     |
| **Scientific Consultant**| Assoc. Prof. Dr. Rumen Rusev                                    |
| **Date of Enrollment**   | 18 February 2026                                                |
| **Phase 1 Deadline**     | November 2026                                                   |
| **Planned Defense**      | April 2029                                                      |

&nbsp;

**Approved by:**

Scientific Supervisor: &emsp; \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; (Prof. Dr. Ts. Vasilev)

Scientific Consultant: &emsp; \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; (Assoc. Prof. Dr. R. Rusev)

Date: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## 1. Introduction

### 1.1 Research Context and Significance

Multi-agent systems operating under conditions of imperfect information<sup>[G5]</sup> represent one of the most challenging and practically relevant areas of artificial intelligence research. In such systems, autonomous agents must make strategic decisions without complete knowledge of the environment state or the intentions of other participants — a setting that arises naturally in cybersecurity (adversarial network defense), financial markets (competing algorithmic traders), autonomous system coordination, and fraud detection.

The mathematical framework for reasoning about such interactions is provided by extensive-form games<sup>[G4]</sup> with imperfect information, a branch of game theory that models sequential decision-making when players hold private information. Over the past decade, substantial progress has been achieved in computing equilibrium strategies<sup>[G7]</sup> for large-scale imperfect-information games. Landmark systems include Libratus (Brown and Sandholm, 2017) and Pluribus (Brown and Sandholm, 2019), which defeated professional human players in two-player and six-player poker respectively, as well as more general architectures such as ReBeL (Brown et al., 2020) and Student of Games (Schmid et al., 2023), which unify game-solving approaches across perfect- and imperfect-information domains.

Despite these advances, a critical limitation persists: state-of-the-art systems compute fixed equilibrium strategies that do not adapt to the specific behavioral patterns exhibited by encountered opponents. In practice, real-world adversaries rarely play optimally, and the ability to detect and exploit systematic deviations from equilibrium — while maintaining guarantees against being exploited in return — constitutes a fundamental open problem. This problem, known as safe opponent exploitation<sup>[G3]</sup>, has been investigated primarily in two-player zero-sum<sup>[G8]</sup> settings. Its extension to multiplayer environments, where coalitions may form and dissolve dynamically, remains largely unexplored in the literature.

The present study plan is organized as a progressive program of fifteen study steps, grouped into seven thematic phases:

- **Phase A — Foundation** (Steps 1–2): Reinforcement learning and game-theoretic fundamentals required by all subsequent work.
- **Phase B — Scaling the Toolbox** (Steps 3–4): Monte Carlo CFR variants and game abstraction techniques for handling larger game instances.
- **Phase C — Neural Methods for Games** (Steps 5–6): Neural network approximations of equilibrium strategies and end-to-end game AI architectures.
- **Phase D — Opponent Modeling and Exploitation** (Steps 7–8): Inference from behavioral traces and safe exploitation algorithms — the thesis-critical core.
- **Phase E — Multi-Agent Dynamics** (Steps 9–11): Multi-agent reinforcement learning, population-based training, and coalition dynamics in competitive settings.
- **Phase F — Data-Driven Approaches** (Steps 12–13): Sequence models and behavioral analysis pipelines connecting theory to real-world data.
- **Phase G — Integration** (Steps 14–15): Evaluation framework construction and research frontier mapping.

### 1.2 Research Objective and Expected Contributions

The primary objective of this doctoral research is to develop methods for adaptive strategy learning in multi-agent environments with imperfect information. The research program is structured around three planned contributions:

**Contribution 1 — Behavioral Adaptation Framework.** A general method for inferring and adapting to opponent strategies from observed action sequences in real time, applicable to arbitrary imperfect-information games. This contribution addresses the gap between static equilibrium computation and dynamic, opponent-aware play.

**Contribution 2 — Multi-Agent Safe Exploitation.** Tractable heuristic approaches — including KL-regularized exploitation and equal-share baselines — for safe exploitation in small N-player games (three-player Kuhn and Leduc poker variants), extending existing results from the two-player zero-sum case. This contribution is scoped to the empirical validation of practical heuristics rather than a general safety theorem for arbitrary N-player settings.

**Contribution 3 — Evaluation Methodology.** A domain-agnostic framework for measuring agent adaptability and robustness across different game environments and opponent populations, with emphasis on identifying failure modes of existing evaluation approaches and demonstrating where standard metrics provide misleading assessments.

---

## 2. Phase A — Foundation (Steps 1–2)

### 2.1 Phase Overview

This phase occupies the first position in the study plan because all subsequent algorithmic work presupposes a thorough command of both domains. Reinforcement learning<sup>[G13]</sup> concepts — value estimation<sup>[G14]</sup>, policy<sup>[G11]</sup> optimization, and experience replay<sup>[G9]</sup> — recur throughout the thesis in the context of opponent modeling (Contribution 1) and adaptive exploitation (Contribution 2). The game-theoretic foundations — extensive-form game representation<sup>[G4]</sup>, Nash equilibrium<sup>[G7]</sup> computation, and exploitability<sup>[G3]</sup> measurement — provide the formal language and evaluation standards that underpin all three contributions.

### 2.2 Step 1 — Reinforcement Learning Basics

**Contribution Alignment.** Value networks<sup>[G14]</sup> and policy gradient<sup>[G12]</sup> methods constitute the learning backbone of the behavioral adaptation framework (Contribution 1). The experience replay<sup>[G9]</sup> mechanism introduced in this step reappears in the design of opponent behavioral trace storage (Phase D). Hyperparameter sensitivity analysis undertaken here establishes a methodological foundation for the systematic evaluation framework developed in Contribution 3.

**Literature.**

1. Sutton, R.S. and Barto, A.G. (2018). *Reinforcement Learning: An Introduction*, 2nd edition. MIT Press.
2. Mnih, V., Kavukcuoglu, K., Silver, D. et al. (2015). "Human-level control through deep reinforcement learning." *Nature*, 518(7540), pp. 529–533.
3. Schulman, J., Wolski, F., Dhariwal, P., Radford, A. and Klimov, O. (2017). "Proximal Policy Optimization Algorithms." Preprint.

**Practical Tasks.**

- Implement a Deep Q-Network<sup>[G16]</sup> (DQN) agent with experience replay<sup>[G9]</sup> and target network; train on a discrete control task (CartPole-v1).
- Implement a Proximal Policy Optimization<sup>[G17]</sup> (PPO) agent with generalized advantage estimation; train on a continuous control task (LunarLander-v3).
- Compare learning curves of both agents; analyze sensitivity to key hyperparameters (learning rate, batch size, discount factor).
- Validate both implementations against established reference results.

### 2.3 Step 2 — Game Theory and Counterfactual Regret Minimization

**Contribution Alignment.** The extensive-form game<sup>[G4]</sup> representation introduced in this step constitutes the formal language employed throughout the thesis. Counterfactual Regret Minimization<sup>[G15]</sup> (CFR) provides the baseline equilibrium<sup>[G7]</sup> computation from which the safe exploitation framework (Contribution 1) measures and bounds deviations. Exploitability<sup>[G3]</sup>, defined and implemented here, serves as the primary quantitative metric in the evaluation methodology (Contribution 3). Supplementary study of sequence-form linear programming introduces an alternative equilibrium computation approach relevant to the scaled exploitation algorithms developed in Phase D.

**Literature.**

1. Shoham, Y. and Leyton-Brown, K. (2008). *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations.* Cambridge University Press.
2. Neller, T.W. and Lanctot, M. (2013). "An Introduction to Counterfactual Regret Minimization." Technical report, Gettysburg College.
3. Zinkevich, M., Johanson, M., Bowling, M. and Piccione, C. (2007). "Regret Minimization in Games with Incomplete Information." *Advances in Neural Information Processing Systems 20 (NeurIPS).*

**Practical Tasks.**

- Construct a complete game engine for Kuhn Poker<sup>[G19]</sup> (three-card deck, two players, one betting round), including game tree enumeration and terminal payoff computation.
- Implement vanilla CFR<sup>[G15]</sup> with regret<sup>[G18]</sup> accumulation and average strategy computation; verify convergence to the known analytical Nash equilibrium<sup>[G7]</sup> of Kuhn Poker.
- Implement best response<sup>[G1]</sup> computation and exploitability<sup>[G3]</sup> measurement; verify $O(1/\sqrt{T})$ convergence rate on a log-log scale.
- Cross-validate the resulting strategy profile against the OpenSpiel reference implementation.

### 2.4 Phase Timeline

Phase A was completed during the period February–March 2026, immediately following enrollment.

| Step | Duration | Dates |
|------|----------|-------|
| Step 1 — Reinforcement Learning Basics | 14 days | 18 February – 3 March 2026 |
| Step 2 — Game Theory and CFR Basics     | 14 days | 4 March – 17 March 2026    |

---

<!-- Phases B through G will be added in subsequent iterations. -->

---

## Glossary

### Game Theory

**[G1] Best response.**
A strategy that maximizes a player's expected payoff given fixed strategies of all other players. Computing a best response against a candidate strategy is the standard method for measuring that strategy's exploitability.

**[G2] Counterfactual value.**
The expected payoff a player would receive at a given decision point, computed under the assumption that the player acts to reach that point while all other players follow their current strategies. The central quantity in the CFR algorithm.

**[G3] Exploitability.**
A quantitative measure of how far a strategy profile deviates from Nash equilibrium, defined as the sum of the payoff gains achievable by best-response opponents. An exploitability of zero indicates an exact Nash equilibrium.

**[G4] Extensive-form game.**
A representation of a sequential game as a tree structure, specifying players, available actions, information sets, chance events, and terminal payoffs. The standard formal model for imperfect-information games.

**[G5] Imperfect information.**
A property of games in which players do not observe all actions previously taken by other players or by nature. Not to be confused with incomplete information, which refers to uncertainty about the game's rules or other players' preferences.

**[G6] Information set.**
A set of game states that are indistinguishable to the acting player due to hidden information. A strategy must prescribe the same action distribution across all states within a single information set.

**[G7] Nash equilibrium.**
A strategy profile in which no player can unilaterally increase their expected payoff by changing their own strategy. In two-player zero-sum games, Nash equilibrium strategies are unexploitable by definition.

**[G8] Zero-sum game.**
A game in which the payoffs of all players sum to zero at every terminal state. The strictly competitive setting in which regret-minimization algorithms such as CFR are guaranteed to converge to Nash equilibrium.

### Reinforcement Learning

**[G9] Experience replay.**
A technique in which past transitions (state, action, reward, next state) are stored in a buffer and sampled in mini-batches for training, reducing temporal correlation and improving learning stability.

**[G10] Markov decision process (MDP).**
A mathematical model for sequential decision-making in which the transition to the next state depends only on the current state and action. The standard formalism for single-agent reinforcement learning problems.

**[G11] Policy.**
A mapping from observations to a probability distribution over actions. Policies may be deterministic (selecting a single action) or stochastic (assigning probabilities to multiple actions).

**[G12] Policy gradient.**
A family of reinforcement learning methods that directly optimize a parameterized policy by estimating the gradient of expected cumulative reward with respect to the policy parameters.

**[G13] Reinforcement learning (RL).**
A branch of machine learning in which an agent learns to select actions within an environment so as to maximize cumulative reward over time, through a process of trial, error, and delayed feedback.

**[G14] Value function.**
A function estimating the expected cumulative reward from a given state (state-value function, $V$) or state–action pair (action-value function, $Q$) under a given policy.

### Algorithms

**[G15] Counterfactual Regret Minimization (CFR).**
An iterative algorithm for approximating Nash equilibrium strategies in two-player zero-sum extensive-form games. Each iteration traverses the game tree, computes counterfactual values, accumulates regrets per action, and updates the strategy via regret matching. The average strategy converges to equilibrium at a rate of $O(1/\sqrt{T})$.

**[G16] Deep Q-Network (DQN).**
A reinforcement learning algorithm that approximates the optimal action-value function using a deep neural network, stabilized by experience replay and a periodically updated target network.

**[G17] Proximal Policy Optimization (PPO).**
A policy gradient algorithm that stabilizes training by constraining each update step via a clipped surrogate objective function, preventing excessively large policy changes.

**[G18] Regret matching.**
A decision rule in which each action is selected with probability proportional to its accumulated positive regret. When applied iteratively within the CFR framework, the resulting average strategy profile converges to Nash equilibrium.

### Benchmark Games

**[G19] Kuhn Poker.**
A simplified poker variant with a three-card deck (Jack, Queen, King), two players, and a single betting round. Kuhn Poker has a known analytical Nash equilibrium (game value $\approx -1/18$ for the first player) and serves as the standard minimal testbed for imperfect-information game algorithms.

**[G20] Leduc Hold'em.**
A two-round poker variant with a six-card deck (three ranks, two suits) and one community card, producing approximately 936 information sets. Used as an intermediate benchmark between Kuhn Poker and full-scale poker games.
