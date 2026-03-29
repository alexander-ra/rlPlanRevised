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

Multi-agent systems operating under conditions of imperfect information represent one of the most challenging and practically relevant areas of artificial intelligence research. In such systems, autonomous agents must make strategic decisions without complete knowledge of the environment state or the intentions of other participants — a setting that arises naturally in cybersecurity (adversarial network defense), financial markets (competing algorithmic traders), autonomous system coordination, and fraud detection.

The mathematical framework for reasoning about such interactions is provided by extensive-form games with imperfect information, a branch of game theory that models sequential decision-making when players hold private information. Over the past decade, substantial progress has been achieved in computing equilibrium strategies for large-scale imperfect-information games. Landmark systems include Libratus (Brown and Sandholm, 2017) and Pluribus (Brown and Sandholm, 2019), which defeated professional human players in two-player and six-player poker respectively, as well as more general architectures such as ReBeL (Brown et al., 2020) and Student of Games (Schmid et al., 2023), which unify game-solving approaches across perfect- and imperfect-information domains.

Despite these advances, a critical limitation persists: state-of-the-art systems compute fixed equilibrium strategies that do not adapt to the specific behavioral patterns exhibited by encountered opponents. In practice, real-world adversaries rarely play optimally, and the ability to detect and exploit systematic deviations from equilibrium — while maintaining guarantees against being exploited in return — constitutes a fundamental open problem. This problem, known as safe opponent exploitation, has been investigated primarily in two-player zero-sum settings. Its extension to multiplayer environments, where coalitions may form and dissolve dynamically, remains largely unexplored in the literature.

### 1.2 Research Objective and Expected Contributions

The primary objective of this doctoral research is to develop methods for adaptive strategy learning in multi-agent environments with imperfect information. The research program is structured around three planned contributions:

**Contribution 1 — Behavioral Adaptation Framework.** A general method for inferring and adapting to opponent strategies from observed action sequences in real time, applicable to arbitrary imperfect-information games. This contribution addresses the gap between static equilibrium computation and dynamic, opponent-aware play.

**Contribution 2 — Multi-Agent Safe Exploitation.** Tractable heuristic approaches — including KL-regularized exploitation and equal-share baselines — for safe exploitation in small N-player games (three-player Kuhn and Leduc poker variants), extending existing results from the two-player zero-sum case. This contribution is scoped to the empirical validation of practical heuristics rather than a general safety theorem for arbitrary N-player settings.

**Contribution 3 — Evaluation Methodology.** A domain-agnostic framework for measuring agent adaptability and robustness across different game environments and opponent populations, with emphasis on identifying failure modes of existing evaluation approaches and demonstrating where standard metrics provide misleading assessments.

### 1.3 Study Plan Structure and Methodology

The present study plan is organized as a progressive program of fifteen study steps, grouped into seven thematic phases (A through G). Each step follows a structured five-phase learning cycle:

1. **Intuition** — building conceptual understanding through accessible materials (lectures, talks, expository articles);
2. **Exploration** — hands-on experimentation with existing implementations and software tools;
3. **Targeted reading** — focused engagement with primary literature, emphasizing algorithmic content over boilerplate;
4. **Implementation** — construction of core algorithms, with explicit ownership rules distinguishing hand-coded components from AI-assisted scaffolding;
5. **Consolidation** — gap-filling, synthesis, and explicit connection to thesis contributions.

Steps are assigned to one of three duration tiers based on their complexity and relevance to the thesis:

| Tier | Duration | Criteria |
|------|----------|----------|
| Tier 1 — Deep Dive   | 3 weeks  | Thesis-critical material requiring extensive implementation |
| Tier 2 — Standard    | 2 weeks  | Well-scoped steps with clear deliverables              |
| Tier 3 — Focused     | 10 days  | Survey-oriented steps with lighter implementation      |

The seven phases and their constituent steps are as follows:

| Phase | Title | Steps | Duration |
|-------|-------|-------|----------|
| **A** | Foundation | Steps 1–2 | ~4 weeks |
| **B** | Scaling the Toolbox | Steps 3–4 | ~3 weeks |
| **C** | Neural Methods for Games | Steps 5–6 | ~5 weeks |
| **D** | Opponent Modeling and Exploitation | Steps 7–8 | ~6 weeks |
| **E** | Multi-Agent Dynamics | Steps 9–11 | ~6 weeks |
| **F** | Data-Driven Approaches | Steps 12–13 | ~3.5 weeks |
| **G** | Integration | Steps 14–15 | ~3.5 weeks |

The total study period spans approximately twenty-six weeks (April–October 2026), with an additional buffer of approximately four weeks before the Phase 1 milestone in November 2026, at which point the first dissertation chapter and an initial publication draft are to be completed.

---

## 2. Phase A — Foundation (Steps 1–2)

### 2.1 Phase Overview

The foundation phase establishes the two methodological pillars upon which the entire research program is constructed: reinforcement learning, which provides the mechanisms for learning and adaptation from experience, and game theory with counterfactual regret minimization, which supplies the strategic framework for reasoning about imperfect-information interactions.

This phase occupies the first position in the study plan because all subsequent algorithmic work presupposes a thorough command of both domains. Reinforcement learning concepts — value estimation, policy optimization, and experience replay — recur throughout the thesis in the context of opponent modeling (Contribution 1) and adaptive exploitation (Contribution 2). The game-theoretic foundations — extensive-form game representation, Nash equilibrium computation, and exploitability measurement — provide the formal language and evaluation standards that underpin all three contributions.

The concepts selected for study are not intended as a broad survey of either field but are chosen for their direct relevance to the doctoral work. Deep Q-Networks are studied because value network architectures reappear in opponent value estimation; Proximal Policy Optimization is included because clipped policy gradient methods form the basis of stable policy updates in exploitation algorithms. Counterfactual Regret Minimization is studied not only as a solver but as the mechanism whose internal structure — counterfactual values, regret accumulation, strategy averaging — is extended and modified in subsequent phases.

### 2.2 Step 1 — Reinforcement Learning Basics

**Contribution Alignment.** Value networks and policy gradient methods constitute the learning backbone of the behavioral adaptation framework (Contribution 1). The experience replay mechanism introduced in this step reappears in the design of opponent behavioral trace storage (Phase D). Hyperparameter sensitivity analysis undertaken here establishes a methodological foundation for the systematic evaluation framework developed in Contribution 3.

**Literature.**

1. Sutton, R.S. and Barto, A.G. (2018). *Reinforcement Learning: An Introduction*, 2nd edition. MIT Press.
2. Mnih, V., Kavukcuoglu, K., Silver, D. et al. (2015). "Human-level control through deep reinforcement learning." *Nature*, 518(7540), pp. 529–533.
3. Schulman, J., Wolski, F., Dhariwal, P., Radford, A. and Klimov, O. (2017). "Proximal Policy Optimization Algorithms." Preprint.

**Practical Tasks.**

- Implement a Deep Q-Network (DQN) agent with experience replay and target network; train on a discrete control task (CartPole-v1).
- Implement a Proximal Policy Optimization (PPO) agent with generalized advantage estimation; train on a continuous control task (LunarLander-v3).
- Compare learning curves of both agents; analyze sensitivity to key hyperparameters (learning rate, batch size, discount factor).
- Validate both implementations against established reference results.

### 2.3 Step 2 — Game Theory and Counterfactual Regret Minimization

**Contribution Alignment.** The extensive-form game representation introduced in this step constitutes the formal language employed throughout the thesis. Counterfactual Regret Minimization (CFR) provides the baseline equilibrium computation from which the safe exploitation framework (Contribution 1) measures and bounds deviations. Exploitability, defined and implemented here, serves as the primary quantitative metric in the evaluation methodology (Contribution 3). Supplementary study of sequence-form linear programming introduces an alternative equilibrium computation approach relevant to the scaled exploitation algorithms developed in Phase D.

**Literature.**

1. Shoham, Y. and Leyton-Brown, K. (2008). *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations.* Cambridge University Press.
2. Neller, T.W. and Lanctot, M. (2013). "An Introduction to Counterfactual Regret Minimization." Technical report, Gettysburg College.
3. Zinkevich, M., Johanson, M., Bowling, M. and Piccione, C. (2007). "Regret Minimization in Games with Incomplete Information." *Advances in Neural Information Processing Systems 20 (NeurIPS).*

**Practical Tasks.**

- Construct a complete game engine for Kuhn Poker (three-card deck, two players, one betting round), including game tree enumeration and terminal payoff computation.
- Implement vanilla CFR with regret accumulation and average strategy computation; verify convergence to the known analytical Nash equilibrium of Kuhn Poker.
- Implement best response computation and exploitability measurement; verify $O(1/\sqrt{T})$ convergence rate on a log-log scale.
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

**Best response.**
A strategy that maximizes a player's expected payoff given fixed strategies of all other players. Computing a best response against a candidate strategy is the standard method for measuring that strategy's exploitability.

**Counterfactual value.**
The expected payoff a player would receive at a given decision point, computed under the assumption that the player acts to reach that point while all other players follow their current strategies. The central quantity in the CFR algorithm.

**Exploitability.**
A quantitative measure of how far a strategy profile deviates from Nash equilibrium, defined as the sum of the payoff gains achievable by best-response opponents. An exploitability of zero indicates an exact Nash equilibrium.

**Extensive-form game.**
A representation of a sequential game as a tree structure, specifying players, available actions, information sets, chance events, and terminal payoffs. The standard formal model for imperfect-information games.

**Imperfect information.**
A property of games in which players do not observe all actions previously taken by other players or by nature. Not to be confused with incomplete information, which refers to uncertainty about the game's rules or other players' preferences.

**Information set.**
A set of game states that are indistinguishable to the acting player due to hidden information. A strategy must prescribe the same action distribution across all states within a single information set.

**Nash equilibrium.**
A strategy profile in which no player can unilaterally increase their expected payoff by changing their own strategy. In two-player zero-sum games, Nash equilibrium strategies are unexploitable by definition.

**Zero-sum game.**
A game in which the payoffs of all players sum to zero at every terminal state. The strictly competitive setting in which regret-minimization algorithms such as CFR are guaranteed to converge to Nash equilibrium.

### Reinforcement Learning

**Experience replay.**
A technique in which past transitions (state, action, reward, next state) are stored in a buffer and sampled in mini-batches for training, reducing temporal correlation and improving learning stability.

**Markov decision process (MDP).**
A mathematical model for sequential decision-making in which the transition to the next state depends only on the current state and action. The standard formalism for single-agent reinforcement learning problems.

**Policy.**
A mapping from observations to a probability distribution over actions. Policies may be deterministic (selecting a single action) or stochastic (assigning probabilities to multiple actions).

**Policy gradient.**
A family of reinforcement learning methods that directly optimize a parameterized policy by estimating the gradient of expected cumulative reward with respect to the policy parameters.

**Value function.**
A function estimating the expected cumulative reward from a given state (state-value function, $V$) or state–action pair (action-value function, $Q$) under a given policy.

### Algorithms

**Counterfactual Regret Minimization (CFR).**
An iterative algorithm for approximating Nash equilibrium strategies in two-player zero-sum extensive-form games. Each iteration traverses the game tree, computes counterfactual values, accumulates regrets per action, and updates the strategy via regret matching. The average strategy converges to equilibrium at a rate of $O(1/\sqrt{T})$.

**Deep Q-Network (DQN).**
A reinforcement learning algorithm that approximates the optimal action-value function using a deep neural network, stabilized by experience replay and a periodically updated target network.

**Proximal Policy Optimization (PPO).**
A policy gradient algorithm that stabilizes training by constraining each update step via a clipped surrogate objective function, preventing excessively large policy changes.

**Regret matching.**
A decision rule in which each action is selected with probability proportional to its accumulated positive regret. When applied iteratively within the CFR framework, the resulting average strategy profile converges to Nash equilibrium.

### Benchmark Games

**Kuhn Poker.**
A simplified poker variant with a three-card deck (Jack, Queen, King), two players, and a single betting round. Kuhn Poker has a known analytical Nash equilibrium (game value $\approx -1/18$ for the first player) and serves as the standard minimal testbed for imperfect-information game algorithms.

**Leduc Hold'em.**
A two-round poker variant with a six-card deck (three ranks, two suits) and one community card, producing approximately 936 information sets. Used as an intermediate benchmark between Kuhn Poker and full-scale poker games.
