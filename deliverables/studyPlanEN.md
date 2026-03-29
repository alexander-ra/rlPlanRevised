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

> *Superscript numerals (e.g. ¹⁵) refer to entries in the Glossary at the end of this document.*

## 1. Introduction

### 1.1 Research Context and Significance

Multi-agent systems operating under conditions of imperfect information<sup>5</sup> represent one of the most challenging and practically relevant areas of artificial intelligence research. In such systems, autonomous agents must make strategic decisions without complete knowledge of the environment state or the intentions of other participants — a setting that arises naturally in cybersecurity (adversarial network defense), financial markets (competing algorithmic traders), autonomous system coordination, and fraud detection.

The mathematical framework for reasoning about such interactions is provided by extensive-form games<sup>4</sup> with imperfect information, a branch of game theory that models sequential decision-making when players hold private information. Over the past decade, substantial progress has been achieved in computing equilibrium strategies<sup>7</sup> for large-scale imperfect-information games. Landmark systems include Libratus (Brown and Sandholm, 2017) and Pluribus (Brown and Sandholm, 2019), which defeated professional human players in two-player and six-player poker respectively, as well as more general architectures such as ReBeL (Brown et al., 2020) and Student of Games (Schmid et al., 2023), which unify game-solving approaches across perfect- and imperfect-information domains.

Despite these advances, a critical limitation persists: state-of-the-art systems compute fixed equilibrium strategies that do not adapt to the specific behavioral patterns exhibited by encountered opponents. In practice, real-world adversaries rarely play optimally, and the ability to detect and exploit systematic deviations from equilibrium — while maintaining guarantees against being exploited in return — constitutes a fundamental open problem. This problem, known as safe opponent exploitation<sup>3</sup>, has been investigated primarily in two-player zero-sum<sup>8</sup> settings. Its extension to multiplayer environments, where coalitions may form and dissolve dynamically, remains largely unexplored in the literature.

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

## 2. Phase A — Foundation (Steps 1–2) · mid-February – mid-March 2026

### 2.1 Phase Overview

This phase occupies the first position in the study plan because all subsequent algorithmic work presupposes a thorough command of both domains. Reinforcement learning<sup>13</sup> concepts — value estimation<sup>14</sup>, policy<sup>11</sup> optimization, and experience replay<sup>9</sup> — recur throughout the thesis in the context of opponent modeling (Contribution 1) and adaptive exploitation (Contribution 2). The game-theoretic foundations — extensive-form game representation<sup>4</sup>, Nash equilibrium<sup>7</sup> computation, and exploitability<sup>3</sup> measurement — provide the formal language and evaluation standards that underpin all three contributions.

### 2.2 Step 1 — Reinforcement Learning Basics

**Contribution Alignment.** Value networks<sup>14</sup> and policy gradient<sup>12</sup> methods constitute the learning backbone of the behavioral adaptation framework (Contribution 1). The experience replay<sup>9</sup> mechanism introduced in this step reappears in the design of opponent behavioral trace storage (Phase D). Hyperparameter sensitivity analysis undertaken here establishes a methodological foundation for the systematic evaluation framework developed in Contribution 3.

**Literature.**

1. Sutton, R.S. and Barto, A.G. (2018). *Reinforcement Learning: An Introduction*, 2nd edition. MIT Press.
2. Mnih, V., Kavukcuoglu, K., Silver, D. et al. (2015). "Human-level control through deep reinforcement learning." *Nature*, 518(7540), pp. 529–533.
3. Schulman, J., Wolski, F., Dhariwal, P., Radford, A. and Klimov, O. (2017). "Proximal Policy Optimization Algorithms." Preprint.

**Practical Tasks.**

- Implement a Deep Q-Network<sup>16</sup> (DQN) agent with experience replay<sup>9</sup> and target network; train on a discrete control task (CartPole-v1).
- Implement a Proximal Policy Optimization<sup>17</sup> (PPO) agent with generalized advantage estimation; train on a continuous control task (LunarLander-v3).
- Compare learning curves of both agents; analyze sensitivity to key hyperparameters (learning rate, batch size, discount factor).
- Validate both implementations against established reference results.

### 2.3 Step 2 — Game Theory and Counterfactual Regret Minimization

**Contribution Alignment.** The extensive-form game<sup>4</sup> representation introduced in this step constitutes the formal language employed throughout the thesis. Counterfactual Regret Minimization<sup>15</sup> (CFR) provides the baseline equilibrium<sup>7</sup> computation from which the safe exploitation framework (Contribution 1) measures and bounds deviations. Exploitability<sup>3</sup>, defined and implemented here, serves as the primary quantitative metric in the evaluation methodology (Contribution 3). Supplementary study of sequence-form linear programming introduces an alternative equilibrium computation approach relevant to the scaled exploitation algorithms developed in Phase D.

**Literature.**

1. Shoham, Y. and Leyton-Brown, K. (2008). *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations.* Cambridge University Press.
2. Neller, T.W. and Lanctot, M. (2013). "An Introduction to Counterfactual Regret Minimization." Technical report, Gettysburg College.
3. Zinkevich, M., Johanson, M., Bowling, M. and Piccione, C. (2007). "Regret Minimization in Games with Incomplete Information." *Advances in Neural Information Processing Systems 20 (NeurIPS).*

**Practical Tasks.**

- Construct a complete game engine for Kuhn Poker<sup>19</sup> (three-card deck, two players, one betting round), including game tree enumeration and terminal payoff computation.
- Implement vanilla CFR<sup>15</sup> with regret<sup>18</sup> accumulation and average strategy computation; verify convergence to the known analytical Nash equilibrium<sup>7</sup> of Kuhn Poker.
- Implement best response<sup>1</sup> computation and exploitability<sup>3</sup> measurement; verify $O(1/\sqrt{T})$ convergence rate on a log-log scale.
- Cross-validate the resulting strategy profile against the OpenSpiel reference implementation.

---

## 3. Phase B — Scaling the Toolbox (Steps 3–4) · beginning of April – mid-April 2026

### 3.1 Phase Overview

Phase A established a working CFR<sup>15</sup> solver on the minimal Kuhn Poker<sup>19</sup> benchmark. However, vanilla CFR requires a full traversal of the game tree on every iteration — an approach that becomes computationally infeasible as the game grows. This phase introduces two complementary scaling mechanisms: Monte Carlo sampling methods that reduce per-iteration cost by traversing only portions of the tree, and game abstraction techniques that reduce the tree itself by merging strategically equivalent or similar states. Together, these tools bridge the gap between toy benchmarks and the medium-scale games (Leduc Hold'em<sup>20</sup>, Extended Leduc) on which the thesis contributions will be developed and validated in subsequent phases.

### 3.2 Step 3 — CFR Variants and Monte Carlo Methods

**Contribution Alignment.** Monte Carlo CFR (MCCFR) provides the computationally tractable baseline equilibrium computation that underlies the behavioral adaptation framework (Contribution 1) — the blueprint Nash strategy against which opponent deviations are detected and exploited. The convergence acceleration offered by CFR+ enables equilibrium computation for the medium-scale games used in the empirical validation of multi-agent safe exploitation heuristics (Contribution 2). The variance characteristics of different sampling schemes directly inform the design of scalable opponent modeling architectures in Phase D.

**Literature.**

1. Lanctot, M., Waugh, K., Zinkevich, M. and Bowling, M. (2009). "Monte Carlo Sampling for Regret Minimization in Extensive Games." *Advances in Neural Information Processing Systems 22 (NeurIPS).*
2. Tammelin, O., Burch, N., Johanson, M. and Bowling, M. (2015). "Solving Heads-Up Limit Texas Hold'em." *Proceedings of the 24th International Joint Conference on Artificial Intelligence (IJCAI).*
3. Chen, B. and Ankenman, J. (2006). *The Mathematics of Poker.* ConJelCo. Chapters 1–8.

**Practical Tasks.**

- Construct a Leduc Hold'em<sup>20</sup> game engine (six-card deck, two rounds, one community card, ~936 information sets<sup>6</sup>).
- Implement external-sampling MCCFR on both Kuhn and Leduc; verify convergence to the same Nash equilibrium as vanilla CFR with lower wall-clock time.
- Implement CFR+ with regret flooring, alternating updates, and linear averaging; demonstrate approximately ten-fold convergence speedup over vanilla CFR on Kuhn Poker.
- Compare convergence profiles of all variants: exploitability<sup>3</sup> versus iterations and versus wall time.

### 3.3 Step 4 — Game Abstraction and Scaling Imperfect-Information Games

**Contribution Alignment.** Lossless abstraction<sup>21</sup> provides the guarantee that an equilibrium computed in the reduced game remains exact in the original — this is the baseline abstraction strategy against which lossy approaches are measured in the evaluation framework (Contribution 3). Lossy card bucketing determines the granularity of game representations used in opponent modeling (Contribution 1, Phase D): coarser abstractions improve computational tractability but may obscure behaviorally distinct opponent types. Action translation — the mechanism for mapping unobserved opponent actions to known abstract categories — directly parallels the opponent classification problem central to Contribution 1. Subgame solving<sup>22</sup> introduces the safety guarantee that a refined strategy cannot become more exploitable than the original blueprint, a principle that extends directly to the safe exploitation algorithms of Phase D.

**Literature.**

1. Gilpin, A. and Sandholm, T. (2007). "Lossless Abstraction of Imperfect Information Games." *Journal of the ACM*, 54(5).
2. Johanson, N., Burch, N., Valenzano, R. and Bowling, M. (2013). "Evaluating State-Space Abstractions in Extensive-Form Games." *Proceedings of the 12th International Conference on Autonomous Agents and Multi-Agent Systems (AAMAS).*
3. Kroer, C. and Sandholm, T. (2016). "Imperfect-Recall Abstractions with Bounds in Games." Preprint.
4. Brown, N. and Sandholm, T. (2017). "Safe and Nested Subgame Solving for Imperfect-Information Games." Preprint.

**Practical Tasks.**

- Implement lossless abstraction via suit isomorphism detection on Leduc Hold'em; verify that the resulting Nash equilibrium<sup>7</sup> is identical to the unabstracted solution.
- Implement lossy card bucketing with configurable granularity; measure exploitability degradation as the number of buckets decreases.
- Construct an Extended Leduc variant (four ranks, two suits, multiple bet sizes, ~5000+ information sets) as a scaling testbed.
- Build a combined abstraction pipeline composing card bucketing, action abstraction, and suit isomorphism; evaluate on a Pareto frontier of abstraction size versus exploitability gap.

---

## 4. Phase C — Neural Methods for Games (Steps 5–6) · mid-April – end of May 2026

### 4.1 Phase Overview

Phases A and B established tabular equilibrium solvers and abstraction techniques for medium-scale games. However, tabular methods store explicit strategy and regret values at every information set<sup>6</sup> — an approach whose memory requirements grow linearly with game size and become prohibitive for large-scale domains. This phase replaces tabular storage with neural network function approximation, enabling equilibrium computation without explicit game tree enumeration. Step 5 introduces the core approximation methods (Deep CFR<sup>25</sup>, NFSP<sup>27</sup>), while Step 6 studies the complete game-solving architectures (DeepStack, Libratus, Pluribus, ReBeL<sup>28</sup>, Student of Games) that integrate these components into competition-grade systems. Together, these steps complete the algorithmic toolbox from which the thesis contributions are developed: Contribution 1 builds on the public belief state<sup>29</sup> framework of ReBeL, Contribution 2 addresses the theoretical gap exposed by Pluribus's multiplayer success without formal safety guarantees, and Contribution 3 draws on the exploitability metrics applied uniformly across all five architectures.

### 4.2 Step 5 — Neural Equilibrium Approximation (Deep CFR, DREAM)

**Contribution Alignment.** Deep CFR<sup>25</sup> provides the mechanism for computing baseline Nash strategies in games too large for tabular solvers — a prerequisite for the behavioral adaptation framework (Contribution 1), which detects and exploits deviations from such baselines. The information state tensor encoding developed in this step becomes the standard input representation for the opponent modeling networks of Phase D. Neural Fictitious Self-Play (NFSP<sup>27</sup>) introduces the anticipatory parameter $\eta$, which continuously interpolates between equilibrium play and best-response exploitation — a mechanism that foreshadows the exploitation–safety tradeoff at the heart of Contribution 1.

**Literature.**

1. Brown, N., Lerer, A., Gross, S. and Sandholm, T. (2019). "Deep Counterfactual Regret Minimization." *Proceedings of the 36th International Conference on Machine Learning (ICML).*
2. Steinberger, E. (2019). "Single Deep Counterfactual Regret Minimization." *Proceedings of the 34th AAAI Conference on Artificial Intelligence (2020).*
3. Heinrich, J. and Silver, D. (2016). "Deep Reinforcement Learning from Self-Play in Imperfect-Information Games." Preprint.

**Practical Tasks.**

- Develop a reusable information state tensor encoding for Leduc Hold'em<sup>20</sup>, designed for compatibility with all subsequent neural implementations.
- Implement Deep CFR with advantage networks, reservoir sampling, and strategy network distillation; verify that predicted counterfactual values<sup>2</sup> match tabular baselines on Kuhn Poker<sup>19</sup>.
- Implement NFSP as a comparative baseline; evaluate the effect of the anticipatory parameter on the Nash–exploitation tradeoff.
- Compare convergence behavior (exploitability<sup>3</sup> versus wall time) of Deep CFR, tabular MCCFR<sup>23</sup>, and NFSP on Leduc Hold'em.

### 4.3 Step 6 — End-to-End Game AI Architectures

**Contribution Alignment.** This step surveys the five landmark game-solving systems that define the state of the art in imperfect-information game AI. ReBeL's public belief state<sup>29</sup> (PBS) framework serves as the architectural starting point for the belief-based opponent modeling developed in Contribution 1, extended from beliefs about game states to beliefs about opponent strategy types. Pluribus demonstrates empirical success in six-player poker without formal multiplayer safety guarantees — exposing the precise theoretical gap that Contribution 2 addresses through tractable exploitation heuristics. The depth-limited solving bounds established by Brown and Sandholm (2018) provide the mathematical foundation for bounding exploitation risk in the safe exploitation algorithms of Phase D. The exploitability<sup>3</sup> metric applied uniformly across all five architectures serves as the model for the domain-agnostic evaluation framework of Contribution 3.

**Literature.**

1. Moravcik, M., Schmid, M., Burch, N., Lisý, V., Morrill, D., Bard, N., Davis, T., Waugh, K., Johanson, M. and Bowling, M. (2017). "DeepStack: Expert-Level Artificial Intelligence in Heads-Up No-Limit Poker." *Science*, 356(6337), pp. 508–513.
2. Brown, N. and Sandholm, T. (2018). "Superhuman AI for Heads-Up No-Limit Poker: Libratus Beats Top Professionals." *Science*, 359(6374), pp. 418–424.
3. Brown, N. and Sandholm, T. (2019). "Superhuman AI for Multiplayer Poker." *Science*, 365(6456), pp. 885–890.
4. Brown, N., Bakhtin, A., Lerer, A. and Hu, Q. (2020). "Combining Deep Reinforcement Learning and Search for Imperfect-Information Games." *Advances in Neural Information Processing Systems (NeurIPS).*
5. Schmid, M., Moravcik, M., Burch, N. et al. (2023). "Student of Games: A Unified Learning Algorithm for Both Perfect and Imperfect Information Games." *Science Advances*, 9(46).
6. Brown, N. and Sandholm, T. (2018). "Depth-Limited Solving for Imperfect-Information Games." *Advances in Neural Information Processing Systems (NeurIPS).*

**Practical Tasks.**

- Implement a simplified ReBeL system ("ReBeL-Lite") for Leduc Hold'em: public belief state representation with Bayesian updates, local PBS-CFR solver, and a value network trained via self-play.
- Verify that training iterations produce monotonically decreasing exploitability on Leduc.
- Construct a comparative analysis of all five architectures (DeepStack, Libratus, Pluribus, ReBeL, Student of Games), mapping shared components (MCCFR<sup>23</sup>, subgame solving<sup>22</sup>, neural value estimation, depth-limited search) and identifying the evolutionary path from single-player to multiplayer to unified systems.

---

## 5. Phase D — Opponent Modeling and Exploitation (Steps 7–8) · end of May – beginning of July 2026

### 5.1 Phase Overview

This phase constitutes the thesis-critical core of the study plan. The preceding phases established the algorithmic toolbox — equilibrium solvers, abstraction techniques, and neural approximation methods — upon which the thesis contributions are built, but did not yet address the central research question of how an agent should adapt its play to a specific opponent. Phase D closes this gap by introducing, first, the inference mechanisms that convert observed action sequences into beliefs about opponent behavior (Step 7), and then the exploitation algorithms that translate those beliefs into profitable yet provably safe strategy adjustments (Step 8). Together these two steps produce the end-to-end pipeline — observe, model, exploit safely — that constitutes the prototype for Contribution 1 (Behavioral Adaptation Framework) and exposes the precise theoretical obstacles that Contribution 2 (Multi-Agent Safe Exploitation) seeks to address.

### 5.2 Step 7 — Opponent Modeling — Inference from Behavioral Traces

**Contribution Alignment.** Bayesian opponent modeling<sup>31</sup> provides the "sensor" component of the Behavioral Adaptation Framework (Contribution 1): the mechanism that infers opponent behavioral patterns from partial observations accumulated during play. Three modeling paradigms are studied — type-based models with Dirichlet-multinomial priors, continuous parametric models estimating per-information-set action distributions, and consistent convergent estimators based on the sequence-form projected gradient descent of Ganzfried (2025) — each offering a different tradeoff between structural assumptions, convergence speed, and robustness to unknown opponent types. The multiplayer extension of opponent modeling, which requires maintaining joint beliefs over all opponents simultaneously, lays the groundwork for Contribution 2 by exposing the computational challenges of scaling inference beyond the two-player case. Non-stationarity handling — detecting and responding to opponents who change strategies mid-game — addresses a key open problem for Contribution 3 (Evaluation Methodology), where standard metrics may understate exploitability when opponents are adaptive.

**Literature.**

1. Southey, F., Bowling, M., Larson, B., Piccione, C., Burch, N., Billings, D. and Rayner, C. (2005). "Bayes' Bluff: Opponent Modelling in Poker." *Proceedings of the 21st Conference on Uncertainty in Artificial Intelligence (UAI).*
2. Bard, N., Johanson, M., Burch, N. and Bowling, M. (2013). "Online Implicit Agent Modelling." *Proceedings of the 12th International Conference on Autonomous Agents and Multi-Agent Systems (AAMAS).*
3. Ganzfried, S. and Sun, Q. (2016). "Bayesian Opponent Exploitation in Imperfect-Information Games." Preprint.
4. Ganzfried, S., Wang, K.A. and Chiswick, M. (2022). "Opponent Modeling in Multiplayer Imperfect-Information Games." Preprint.
5. Ganzfried, S. (2025). "Consistent Opponent Modeling in Imperfect-Information Games." Preprint.
6. Shoham, Y. and Leyton-Brown, K. (2008). *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations.* Cambridge University Press. Chapter 7: Learning and Teaching.

**Practical Tasks.**

- Construct an opponent type library with five or more distinct strategies (tight-aggressive, loose-passive, Nash equilibrium, exploitative, random) for both Kuhn Poker<sup>19</sup> and Leduc Hold'em<sup>20</sup>.
- Implement an observation buffer handling partial observability (showdown versus non-showdown information extraction).
- Implement a type-based Bayesian opponent model<sup>31</sup> with Dirichlet-multinomial posterior inference and a continuous Bayesian model with per-information-set action distribution estimation.
- Implement a consistent opponent modeler following the Ganzfried (2025) sequence-form projected gradient descent approach.
- Build an adaptive exploitation pipeline integrating opponent modeling and best-response<sup>1</sup> computation.
- Conduct a head-to-head model comparison measuring convergence speed, final exploitation rate, and robustness to unknown opponent types.
- Execute non-stationarity tests demonstrating model behavior under opponent type switching.

### 5.3 Step 8 — Safe Exploitation — Theory, Algorithms, and Real-Time Search

**Contribution Alignment.** The exploitation–safety tradeoff<sup>33</sup> studied in this step constitutes the theoretical core of the thesis. The Restricted Nash Response (RNR<sup>32</sup>) provides the initial algorithmic tool for blending equilibrium play with exploitative best-response play, parameterized by a continuous safety coefficient. The Safety Theorem of Ganzfried and Sandholm (2015) establishes the formal guarantee that exploitation strategies anchored to a Nash equilibrium<sup>7</sup> baseline cannot lose more than the baseline itself — a two-player zero-sum result whose dependence on the minimax theorem exposes the precise failure point for N-player extension (Contribution 2). Prime-safe exploitation (Jeary and Turrini, 2023) extends safety guarantees to $\varepsilon$-equilibrium baselines, connecting Step 4 abstraction quality to Step 8 exploitation budgets. Subgame exploitation methods (SES, OX-Search) enable real-time safe exploitation during play without full-game recomputation — the scalability mechanism required for practical deployment of Contribution 1. Teaching attack<sup>34</sup> resilience testing, in which a deceptive opponent deliberately plays suboptimally to manipulate the modeler before switching to an exploitative strategy, provides the prototype adversarial evaluation methodology for Contribution 3. The adaptation safety<sup>35</sup> notion of Ge et al. (2024) — requiring that the exploitation strategy be no more exploitable than the blueprint baseline — offers the practical safety definition adopted by the thesis for settings where strict Nash safety is not achievable.

**Literature.**

1. Johanson, M., Bowling, M. and Zinkevich, M. (2007). "Computing Robust Counter-Strategies." *Advances in Neural Information Processing Systems (NeurIPS).*
2. Ganzfried, S. and Sandholm, T. (2015). "Safe Opponent Exploitation." *ACM Transactions on Economics and Computation*, 3(2).
3. Liu, W., Wang, H., Guo, T. and Xing, J. (2022). "Safe Opponent-Exploitation Subgame Refinement." *Advances in Neural Information Processing Systems (NeurIPS).*
4. Jeary, J. and Turrini, P. (2023). "Safe Opponent Exploitation For Epsilon Equilibrium Strategies." Preprint.
5. Ge, C., Zhu, Y. et al. (2024). "Safe and Robust Subgame Exploitation in Imperfect Information Games." *Proceedings of the 41st International Conference on Machine Learning (ICML).*
6. Milec, D., Kovařík, V. and Lisý, V. (2025). "Adapting Beyond the Depth Limit: Counter Strategies in Large Imperfect Information Games." Preprint.
7. Shoham, Y. and Leyton-Brown, K. (2008). *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations.* Cambridge University Press. Sections 3.4 and 4.6.

**Practical Tasks.**

- Implement a safety checker module computing worst-case exploitability<sup>3</sup> and verifying safety constraints against the blueprint strategy.
- Implement an exploitation metrics module measuring exploitation value and safety violations.
- Build a Restricted Nash Response (RNR<sup>32</sup>) solver with configurable safety parameter $p \in [0,1]$.
- Implement the Ganzfried safe exploitation solver enforcing the Safety Theorem guarantee.
- Implement a prime-safe exploitation extension handling $\varepsilon$-equilibrium baselines (connecting abstraction quality from Step 4).
- Build an SES-style subgame exploitation solver with gadget construction for real-time safe exploitation.
- Implement an adaptation safety<sup>35</sup> checker following the Ge et al. (2024) safety notion.
- Generate exploitation–safety Pareto frontier plots for all methods across multiple opponent types.
- Integrate the full pipeline: Step 7 opponent models<sup>30</sup> feeding Step 8 exploitation engine, evaluated end-to-end.
- Conduct a teaching attack<sup>34</sup> stress test with deceptive opponent switching behavior mid-game and robustness analysis.

---

<!-- Phases E through G will be added in subsequent iterations. -->

---

## Glossary

### Game Theory

**[1] Best response.**
A strategy that maximizes a player's expected payoff given fixed strategies of all other players. Computing a best response against a candidate strategy is the standard method for measuring that strategy's exploitability.

**[2] Counterfactual value.**
The expected payoff a player would receive at a given decision point, computed under the assumption that the player acts to reach that point while all other players follow their current strategies. The central quantity in the CFR algorithm.

**[3] Exploitability.**
A quantitative measure of how far a strategy profile deviates from Nash equilibrium, defined as the sum of the payoff gains achievable by best-response opponents. An exploitability of zero indicates an exact Nash equilibrium.

**[4] Extensive-form game.**
A representation of a sequential game as a tree structure, specifying players, available actions, information sets, chance events, and terminal payoffs. The standard formal model for imperfect-information games.

**[5] Imperfect information.**
A property of games in which players do not observe all actions previously taken by other players or by nature. Not to be confused with incomplete information, which refers to uncertainty about the game's rules or other players' preferences.

**[6] Information set.**
A set of game states that are indistinguishable to the acting player due to hidden information. A strategy must prescribe the same action distribution across all states within a single information set.

**[7] Nash equilibrium.**
A strategy profile in which no player can unilaterally increase their expected payoff by changing their own strategy. In two-player zero-sum games, Nash equilibrium strategies are unexploitable by definition.

**[8] Zero-sum game.**
A game in which the payoffs of all players sum to zero at every terminal state. The strictly competitive setting in which regret-minimization algorithms such as CFR are guaranteed to converge to Nash equilibrium.

### Reinforcement Learning

**[9] Experience replay.**
A technique in which past transitions (state, action, reward, next state) are stored in a buffer and sampled in mini-batches for training, reducing temporal correlation and improving learning stability.

**[10] Markov decision process (MDP).**
A mathematical model for sequential decision-making in which the transition to the next state depends only on the current state and action. The standard formalism for single-agent reinforcement learning problems.

**[11] Policy.**
A mapping from observations to a probability distribution over actions. Policies may be deterministic (selecting a single action) or stochastic (assigning probabilities to multiple actions).

**[12] Policy gradient.**
A family of reinforcement learning methods that directly optimize a parameterized policy by estimating the gradient of expected cumulative reward with respect to the policy parameters.

**[13] Reinforcement learning (RL).**
A branch of machine learning in which an agent learns to select actions within an environment so as to maximize cumulative reward over time, through a process of trial, error, and delayed feedback.

**[14] Value function.**
A function estimating the expected cumulative reward from a given state (state-value function, $V$) or state–action pair (action-value function, $Q$) under a given policy.

### Algorithms

**[15] Counterfactual Regret Minimization (CFR).**
An iterative algorithm for approximating Nash equilibrium strategies in two-player zero-sum extensive-form games. Each iteration traverses the game tree, computes counterfactual values, accumulates regrets per action, and updates the strategy via regret matching. The average strategy converges to equilibrium at a rate of $O(1/\sqrt{T})$.

**[16] Deep Q-Network (DQN).**
A reinforcement learning algorithm that approximates the optimal action-value function using a deep neural network, stabilized by experience replay and a periodically updated target network.

**[17] Proximal Policy Optimization (PPO).**
A policy gradient algorithm that stabilizes training by constraining each update step via a clipped surrogate objective function, preventing excessively large policy changes.

**[18] Regret matching.**
A decision rule in which each action is selected with probability proportional to its accumulated positive regret. When applied iteratively within the CFR framework, the resulting average strategy profile converges to Nash equilibrium.

### Benchmark Games

**[19] Kuhn Poker.**
A simplified poker variant with a three-card deck (Jack, Queen, King), two players, and a single betting round. Kuhn Poker has a known analytical Nash equilibrium (game value $\approx -1/18$ for the first player) and serves as the standard minimal testbed for imperfect-information game algorithms.

**[20] Leduc Hold'em.**
A two-round poker variant with a six-card deck (three ranks, two suits) and one community card, producing approximately 936 information sets. Used as an intermediate benchmark between Kuhn Poker and full-scale poker games.

**[21] Game abstraction (lossless / lossy).**
A technique for reducing the size of a game by merging states that are strategically equivalent (lossless) or approximately similar (lossy). Lossless abstractions preserve the exact equilibrium of the original game; lossy abstractions trade solution quality for computational tractability, quantified by the exploitability gap between the abstracted and original solutions.

**[22] Subgame solving.**
A real-time refinement technique that re-solves a portion of the game tree at a finer granularity than the pre-computed blueprint strategy. Safe subgame solving guarantees that the refined strategy is no more exploitable than the original blueprint.

**[23] Monte Carlo CFR (MCCFR).**
A family of CFR variants that sample portions of the game tree rather than traversing it in full on each iteration. Reduces per-iteration cost at the expense of introducing sampling variance. Common instantiations include external sampling (samples opponent and chance actions) and outcome sampling (samples a single trajectory).

**[24] CFR+.**
An accelerated variant of CFR that applies three modifications: flooring negative regrets to zero, alternating which player's strategy is updated, and weighting later iterations more heavily. Empirically achieves $O(1/T)$ convergence — substantially faster than the $O(1/\sqrt{T})$ rate of vanilla CFR.

**[25] Deep CFR.**
A neural variant of CFR that replaces tabular regret and strategy storage with deep neural networks (advantage networks and a strategy network). Training data is generated via external-sampling MCCFR traversals and maintained using reservoir sampling, enabling equilibrium approximation in games too large for tabular methods.

**[26] DREAM (Deep Regret minimization with Advantage baselines and Model-free learning).**
An outcome-sampling variant of Deep CFR that uses baseline subtraction to reduce sampling variance. Achieves comparable solution quality with a single-network architecture.

**[27] Neural Fictitious Self-Play (NFSP).**
An equilibrium-finding algorithm that combines a deep Q-network for best-response computation with a supervised-learning network for average strategy approximation. An anticipatory parameter $\eta$ interpolates between Nash equilibrium play and exploitative best-response play.

**[28] ReBeL (Recursive Belief-based Learning).**
A game-solving framework that combines self-play reinforcement learning with search over public belief states. Enables AlphaZero-style learning and planning for imperfect-information games without requiring pre-computed blueprint strategies or explicit game abstraction.

**[29] Public belief state (PBS).**
A probability distribution over all possible private information assignments, maintained and updated via Bayes' rule as public actions are observed. The PBS serves as a sufficient statistic for decision-making in imperfect-information games and is the central representation in the ReBeL architecture.

### Opponent Modeling and Exploitation

**[30] Opponent modeling.**
The process of inferring an opponent's strategy, intentions, or type from observed behavioral traces during play. Opponent models may be explicit (maintaining a belief distribution over opponent strategies) or implicit (adapting one's own strategy directly from observations without constructing an explicit belief).

**[31] Bayesian opponent modeling.**
An opponent modeling approach that maintains a prior distribution over possible opponent types or action frequencies and updates it via Bayes' rule as new observations are collected. Type-based variants use Dirichlet-multinomial conjugacy for closed-form posterior updates; continuous variants estimate per-information-set action distributions.

**[32] Restricted Nash Response (RNR).**
A safe exploitation algorithm that constructs a strategy blending Nash equilibrium play with best-response exploitation. A safety parameter $p \in [0,1]$ controls the tradeoff: at $p = 0$ the strategy is a pure best response, and at $p = 1$ it is the Nash equilibrium itself. Formulated as a linear program.

**[33] Safe exploitation.**
The problem of adapting one's strategy to exploit a modeled opponent's weaknesses while maintaining provable guarantees against worst-case loss. In two-player zero-sum games, the Safety Theorem (Ganzfried and Sandholm, 2015) ensures that an exploitation strategy anchored to a Nash equilibrium baseline cannot lose more than the baseline against any opponent.

**[34] Teaching attack.**
An adversarial strategy in which an opponent deliberately plays suboptimally to manipulate an adaptive agent's opponent model, then switches to an exploitative strategy once the agent has been misled. Resilience to teaching attacks is a key robustness criterion for opponent modeling systems.

**[35] Adaptation safety.**
A safety notion (Ge et al., 2024) requiring that an exploitation strategy be no more exploitable than the blueprint baseline strategy from which it was derived. A weaker but more practically achievable guarantee than strict Nash safety, applicable to settings where the baseline is an approximate rather than exact equilibrium.
