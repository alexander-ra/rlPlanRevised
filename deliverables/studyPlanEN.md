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

Throughout the study plan, Kuhn Poker<sup>19</sup> and Leduc Hold'em<sup>20</sup> serve as the primary implementation testbeds. These games are chosen deliberately as pedagogical vehicles: their small state spaces (12 and approximately 936 information sets, respectively) and known analytical equilibria permit exact verification of every algorithm, while their imperfect-information structure retains the strategic complexity that the thesis demands. By working within well-understood domains, each step concentrates on algorithmic concepts rather than domain-specific engineering, maximizing the volume of theoretical material covered within the allotted timeframe. In later phases, the study plan validates generality beyond poker by applying the developed methods to matrix games, Goofspiel, So Long Sucker<sup>45</sup>, and anonymized real-world behavioral data.

The thesis contributions themselves are formulated in domain-agnostic terms — no contribution is specific to poker or to any other single game. The Behavioral Adaptation Framework (Contribution 1) addresses arbitrary imperfect-information games; the Multi-Agent Safe Exploitation heuristics (Contribution 2) are defined over general N-player extensive-form structures; and the Evaluation Methodology (Contribution 3) is designed for cross-domain applicability.

The study plan is aligned with the milestones of the university individual plan. Upon completion of each thematic phase, the corresponding material will be incorporated into Chapter I of the dissertation — covering the state-of-the-art analysis and the formulation of relevance, objectives, tasks, and thesis statements — which is due in November 2026. In this way, the literature review and foundational exposition accumulate incrementally rather than being composed retrospectively. Step 15 produces a detailed Chapter I outline and publication pipeline as its final deliverable.

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

**Contribution Alignment.** The extensive-form game<sup>4</sup> representation introduced in this step constitutes the formal language employed throughout the thesis. Counterfactual Regret Minimization<sup>15</sup> (CFR) provides the baseline equilibrium<sup>7</sup> computation from which the behavioral adaptation framework (Contribution 1) detects opponent deviations and the safe exploitation methods (Contribution 2) bound exploitation risk. Exploitability<sup>3</sup>, defined and implemented here, serves as the primary quantitative metric in the evaluation methodology (Contribution 3). Supplementary study of sequence-form linear programming introduces an alternative equilibrium computation approach relevant to the scaled exploitation algorithms developed in Phase D.

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

## 6. Phase E — Multi-Agent Dynamics (Steps 9–11) · beginning of July – mid-August 2026

### 6.1 Phase Overview

The preceding phases developed techniques for two-player imperfect-information games — equilibrium computation, neural approximation, opponent modeling, and safe exploitation. Phase E transitions the thesis from two-player settings to the multi-agent world, where fundamental new challenges arise: non-stationarity<sup>36</sup> induced by simultaneously learning agents, credit assignment in joint-reward environments, and the emergence of coalitions<sup>41</sup> that no two-player framework can capture. Three steps address these challenges in sequence. Step 9 introduces the core algorithmic paradigms for multi-agent reinforcement learning — centralized training with decentralized execution (CTDE<sup>37</sup>) and Policy Space Response Oracles (PSRO<sup>38</sup>). Step 10 scales these methods to population-based training<sup>39</sup> systems and connects population dynamics to evolutionary game theory. Step 11 applies the resulting toolkit to dynamic coalition formation in free-for-all games, crystallizing the central theoretical gap of Contribution 2 and prototyping the multi-agent evaluation methodology of Contribution 3.

### 6.2 Step 9 — Multi-Agent RL — Coordination, Competition, and Communication

**Contribution Alignment.** This step provides the algorithmic vocabulary for extending the thesis from two-player to multi-agent settings. The CTDE<sup>37</sup> paradigm (MADDPG, QMIX, MAPPO) introduces the architectural pattern — centralized information during training, decentralized execution at deployment — that is adopted throughout the remainder of the thesis. PSRO<sup>38</sup> unifies fictitious play, self-play, and the double oracle method within a single population-based meta-Nash framework, providing the starting point for defining safety in multi-agent populations (Contribution 2). Learning with Opponent-Learning Awareness (LOLA<sup>40</sup>) contributes the insight that modeling an opponent's learning dynamics — rather than their current strategy alone — enables superior adaptation; this principle extends the Bayesian opponent modeling<sup>31</sup> of Step 7 from static inference to dynamic anticipation within the Behavioral Adaptation Framework (Contribution 1). The meta-Nash analysis produced by PSRO generalizes two-player exploitability<sup>3</sup> to the population setting, providing an evaluation tool for Contribution 3.

**Literature.**

1. Lowe, R., Wu, Y., Tamar, A., Harb, J., Abbeel, P. and Mordatch, I. (2017). "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments." *Advances in Neural Information Processing Systems (NeurIPS).*
2. Rashid, T., Samvelyan, M., de Witt, C.S., Farquhar, G., Foerster, J. and Whiteson, S. (2018). "QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning." *Proceedings of the International Conference on Machine Learning (ICML).*
3. Yu, C., Velu, A., Vinitsky, E., Gao, J., Wang, Y., Baez, A. and Fishi, S. (2022). "The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games." *Advances in Neural Information Processing Systems (NeurIPS).*
4. Foerster, J., Chen, R.Y., Al-Shedivat, M., Whiteson, S., Abbeel, P. and Mordatch, I. (2018). "Learning with Opponent-Learning Awareness." *Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS).*
5. Lanctot, M., Zambaldi, V., Gruslys, A., Lazaridou, A., Tuyls, K., Pérolat, J., Silver, D. and Graepel, T. (2017). "A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning." *Advances in Neural Information Processing Systems (NeurIPS).*
6. Sukhbaatar, S., Szlam, A. and Fergus, R. (2016). "Learning Multiagent Communication with Backpropagation." *Advances in Neural Information Processing Systems (NeurIPS).*

**Practical Tasks.**

- Construct a matrix game testbed (Prisoner's Dilemma, Matching Pennies, Stag Hunt, Battle of the Sexes) with verified Nash equilibria.
- Implement independent PPO learners as a baseline demonstrating non-stationarity<sup>36</sup> failures in multi-agent settings.
- Implement MADDPG (centralized critic, decentralized actors) and MAPPO (PPO with centralized value function) as CTDE<sup>37</sup> representatives.
- Implement PSRO<sup>38</sup> with population-based meta-Nash computation and RL best-response oracle; verify convergence to Nash equilibrium on Kuhn Poker<sup>19</sup> and Leduc Hold'em<sup>20</sup>.
- Integrate a CommNet differentiable communication channel with MADDPG; evaluate the benefit of emergent communication on cooperative tasks.
- Produce a comparative evaluation table: independent learning versus CTDE versus PSRO across all test environments and Goofspiel.

### 6.3 Step 10 — Population-Based Training and Evolutionary Game Theory

**Contribution Alignment.** Population-Based Training<sup>39</sup> (PBT) provides a meta-optimization framework in which a population of agents co-evolves weights and hyperparameters simultaneously, replacing sequential hyperparameter search with population-level selection. The AlphaStar league architecture — with its three-role design of main agents, main exploiters, and league exploiters — constitutes automated opponent modeling at population scale, complementing the explicit Bayesian modeling<sup>31</sup> of Step 7 with implicit population-level adaptation (Contribution 1). For Contribution 2, the AlphaStar league provides heuristic safety through exploiter pressure but lacks formal guarantees; formalizing what "safe exploitation in a population" means mathematically is a key thesis objective. The spinning top decomposition<sup>42</sup> (Balduzzi et al., 2019) separates any payoff matrix into a transitive (genuine skill ranking) and a cyclic (non-transitive, rock-paper-scissors) component, providing a diagnostic that distinguishes real improvement from illusory cycling — a tool adopted directly into the evaluation methodology of Contribution 3. Empirical Game-Theoretic Analysis<sup>43</sup> (EGTA) generalizes exploitability to the population setting via meta-Nash computation over sampled strategy sets.

**Literature.**

1. Jaderberg, M., Dalibard, V., Osindero, S., Czarnecki, W.M. et al. (2017). "Population Based Training of Neural Networks." Preprint.
2. Jaderberg, M., Czarnecki, W.M., Dunning, I. et al. (2019). "Human-Level Performance in First-Person Multiplayer Games with Population-Based Deep Reinforcement Learning." *Science*, 364(6443), pp. 859–865.
3. Vinyals, O., Babuschkin, I., Czarnecki, W.M. et al. (2019). "Grandmaster Level in StarCraft II Using Multi-Agent Reinforcement Learning." *Nature*, 575(7782), pp. 350–354.
4. Balduzzi, D., Garnelo, M., Bachrach, Y., Czarnecki, W.M., Pérolat, J., Jaderberg, M. and Graepel, T. (2019). "Open-Ended Learning in Symmetric Zero-Sum Games." *Proceedings of the International Conference on Learning Representations (ICLR).*
5. Tuyls, K., Pérolat, J., Lanctot, M. et al. (2018). "A Generalised Method for Empirical Game Theoretic Analysis." *Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS).*
6. Hofbauer, J. and Sigmund, K. (2003). "Evolutionary Game Dynamics." *Bulletin of the American Mathematical Society*, 40(4), pp. 479–519.

**Practical Tasks.**

- Implement a replicator dynamics simulator on matrix games; verify convergence to Nash equilibrium and evolutionary stable strategies on Prisoner's Dilemma, Hawk-Dove, and Stag Hunt, and verify cycling on Rock-Paper-Scissors. Generate phase portraits.
- Implement the spinning top decomposition<sup>42</sup> (Balduzzi et al., 2019); apply to PSRO<sup>38</sup> meta-game payoff matrices from Step 9 and to the league meta-game from this step. Compute the transitive ratio as a diagnostic metric.
- Build a PBT league for Leduc Hold'em<sup>20</sup> with three agent roles (main agents, main exploiters, league exploiters), prioritized matchmaking, periodic agent freezing, and PBT explore-exploit population updates.
- Conduct EGTA<sup>43</sup> analysis: construct the empirical normal-form game over the league population and compute meta-Nash equilibrium; verify that the meta-Nash mixture exploitability does not exceed that of the best individual agent.
- Produce a comparative evaluation: league versus PSRO (Step 9) versus single self-play agent versus MCCFR<sup>23</sup> Nash strategy (Step 3), measuring exploitability, Elo rating, effective population diversity, and strategy clustering.

### 6.4 Step 11 — Dynamic Coalition Formation in Competitive Free-For-All Games

**Contribution Alignment.** This step crystallizes the central theoretical gap of the thesis. In two-player games, safe exploitation<sup>33</sup> employs Nash equilibrium as the safety baseline (Step 8). In N-player free-for-all games, Nash equilibrium is both computationally intractable and strategically insufficient — it ignores the coalition structures that dominate actual play. The piKL regularization approach of Bakhtin et al. (2022) suggests replacing equilibrium-based safety with behavioral-prior-based safety, a shift that Contribution 2 seeks to formalize for competitive settings. The coalition detection module developed here extends the opponent modeling methodology of Step 7 from inferring individual player types to inferring multi-agent social structure — the multi-agent generalization of behavioral adaptation (Contribution 1). Shapley-value<sup>44</sup> credit decomposition, combined with EGTA<sup>43</sup> meta-game analysis over agent populations, provides an alternative evaluation framework for N-player settings where standard exploitability<sup>3</sup> is undefined; this becomes the prototype for the domain-agnostic evaluation methodology of Contribution 3. The So Long Sucker<sup>45</sup> (SLS) game — a four-player coalition formation benchmark designed by Nash, Shapley, Shubik, and Hausner — serves as the primary experimental testbed.

**Literature.**

1. Sharan, M. and Adak, C. (2024). "Reinforcing Competitive Multi-Agents for Playing 'So Long Sucker'." Preprint.
2. De Carufel, J.-L. and Jerade, M.R. (2024). "So Long Sucker: Endgame Analysis." Preprint.
3. Bakhtin, A., Wu, D.J., Lerer, A., Gray, J., Jacob, A.P., Farina, G., Miller, A.H. and Brown, N. (2022). "Mastering the Game of No-Press Diplomacy via Human-Regularized Reinforcement Learning and Planning." Preprint.
4. Chalkiadakis, G., Elkind, E. and Wooldridge, M. (2011). *Computational Aspects of Cooperative Game Theory.* Morgan and Claypool.
5. Wang, J., Zhang, Y., Kim, T.-K. and Gu, Y. (2020). "Shapley Q-value: A Local Reward Approach to Solve Global Reward Games." *Proceedings of the 34th AAAI Conference on Artificial Intelligence.*

**Practical Tasks.**

- Build a verified So Long Sucker<sup>45</sup> environment with coalition tracking, rich state representation, and correctness validation against the endgame analysis of De Carufel and Jerade (2024).
- Implement a coalition detection module that infers implicit alliances from observed chip-placement behavior using help/harm matrices, extending the opponent modeling methodology of Step 7 to multi-agent alliance inference.
- Adapt Shapley Q-value<sup>44</sup> decomposition to the competitive free-for-all setting, distributing each action's credit among all players according to marginal coalition contributions.
- Train four-player MAPPO agents with Shapley-decomposed rewards via self-play; compare against a sparse-reward baseline replicating Sharan and Adak (2024).
- Apply EGTA<sup>43</sup> (Step 10) to construct the four-player payoff tensor and compute meta-Nash over the agent population; apply the spinning top decomposition<sup>42</sup> to quantify the non-transitive structure of coalition dynamics.
- Produce a comparative evaluation: coalition-aware agents versus sparse-reward agents versus random baselines, measuring win rate, coalition formation frequency, Shapley variation, and game length.

---

## 7. Phase F — Data-Driven Approaches (Steps 12–13) · mid-August – beginning of September 2026

### 7.1 Phase Overview

The preceding phases developed game-solving algorithms and multi-agent training systems entirely within synthetic, self-play environments. Phase F bridges the gap between theoretical methods and real-world behavioral data. Step 12 introduces sequence models — Decision Transformers<sup>46</sup> and their adversarially robust variants — that reformulate offline reinforcement learning as conditional sequence generation, alongside an assessment of large language model agents in strategic settings. Step 13 applies the resulting data pipeline to anonymized real-world poker hand histories, constructing player embeddings<sup>48</sup>, behavioral classification systems, and a collusion detection<sup>50</sup> module. Together, these steps transform the Behavioral Adaptation Framework (Contribution 1) from a theoretical construct into a working system demonstrated on industry data, provide the empirical base for quantifying exploitation opportunities (Contribution 2), and prototype the evaluation methodology (Contribution 3) on data where ground truth is unavailable and standard metrics must be validated against practical outcomes.

### 7.2 Step 12 — Sequence Models and LLM Agents in Strategic Settings

**Contribution Alignment.** The Decision Transformer<sup>46</sup> architecture reformulates offline reinforcement learning as return-conditioned sequence prediction, enabling strategy learning from pre-collected game trajectories without temporal-difference learning or Bellman backups. The Adversarially Robust Decision Transformer (ARDT<sup>47</sup>) extends this approach by conditioning on minimax returns via expectile regression, recovering near-Nash strategies from offline data — an alternative path for Contribution 2 that bypasses the intractable equilibrium computation in N-player settings identified in Step 11. The critical stochasticity limitation demonstrated by Paster et al. (2022) — that return conditioning conflates lucky outcomes with skilled decisions in stochastic environments such as poker — directly constrains the design of the real-world data pipeline in Step 13. The poker state tensor encoding developed in this step (cards, position, pot size, stack sizes, betting history) constitutes the foundational input representation for the Behavioral Adaptation Framework (Contribution 1). The multi-paradigm comparison table produced here — spanning CFR, Decision Transformer, ARDT, behavioral cloning, and LLM agents on a single benchmark with standardized metrics — serves as the prototype for the comprehensive evaluation framework of Contribution 3.

**Literature.**

1. Chen, L., Lu, K., Rajeswaran, A., Lee, K., Grover, A., Laskin, M., Abbeel, P., Srinivas, A. and Mordatch, I. (2021). "Decision Transformer: Reinforcement Learning via Sequence Modeling." *Advances in Neural Information Processing Systems (NeurIPS).*
2. Paster, K., McIlraith, S. and Ba, J. (2022). "You Can't Count on Luck: Why Decision Transformers and RvS Fail in Stochastic Environments." Preprint.
3. Tang, X., Marques, A., Kamalaruban, P. and Bogunovic, I. (2024). "Adversarially Robust Decision Transformer." *Advances in Neural Information Processing Systems (NeurIPS).*
4. Janner, M., Li, Q. and Levine, S. (2021). "Offline Reinforcement Learning as One Big Sequence Modeling Problem." *Advances in Neural Information Processing Systems (NeurIPS).*
5. Guertler, L., Cheng, B., Yu, S., Liu, B., Choshen, L. and Tan, C. (2025). "TextArena." Preprint.
6. Meta AI (2022). "Human-Level Play in the Game of Diplomacy by Combining Language Models with Strategic Reasoning." *Science*, 378(6624), pp. 1067–1074.

**Practical Tasks.**

- Generate a poker trajectory dataset (50,000+ Kuhn Poker<sup>19</sup> hands) using CFR agents from Step 3; design the poker state tensor encoding that will transfer to the real-world data pipeline in Step 13.
- Adapt and train a Decision Transformer<sup>46</sup> for poker state and action spaces; validate return-to-go conditioning and demonstrate the stochasticity limitation (Paster et al., 2022) whereby the model conflates lucky card deals with skilled play.
- Implement ARDT<sup>47</sup> with minimax expectile regression; train on mixed-quality opponent data and verify recovery of near-Nash strategies on Kuhn Poker (measured by exploitability<sup>3</sup> against the known analytical equilibrium from Step 2).
- Deploy LLM agents on TextArena strategic games to assess capabilities in negotiation, deception, and theory-of-mind reasoning.
- Evaluate LLM agents on Kuhn Poker with standardized metrics: exploitability, bluff frequency, value bet frequency, illegal move rate, and opponent adaptation.
- Produce a unified multi-paradigm comparison table (CFR, Decision Transformer, ARDT, behavioral cloning, LLM agents) on Kuhn Poker with standardized metrics.

### 7.3 Step 13 — Behavioral Analysis Pipelines and Real-World Data

**Contribution Alignment.** This step transforms the Behavioral Adaptation Framework (Contribution 1) from a theoretical construct into a working system demonstrated on industry data. The complete pipeline — parsing anonymized Playtech hand histories into structured records, encoding game states as tensors, computing player statistics, training player embeddings<sup>48</sup> via a Transformer encoder with masked action prediction, and classifying player styles via clustering — constitutes the practical instantiation of the behavioral adaptation methodology developed across Steps 7, 8, and 12. The behavioral deviation from Nash or GTO play measured on real player data quantifies the exploitation opportunity that the safe exploitation theory of Step 8 addresses (Contribution 2). The collusion detection<sup>50</sup> module — combining co-occurrence anomaly detection, chip dumping scores, and soft play scores into a composite framework — represents a direct methodological contribution (Contribution 3), transferring the coalition detection principles of Step 11 from abstract game environments to a practical fraud detection application. Few published solutions exist for poker collusion detection, positioning this work as a candidate for publication.

**Literature.**

1. Wang et al. (2024). "player2vec: A Language Modeling Approach to Understand Player Behavior in Games." Preprint.
2. Kumar, A., Hong, J., Singh, A. and Levine, S. (2022). "When Should We Prefer Offline Reinforcement Learning Over Behavioral Cloning?" *Proceedings of the International Conference on Learning Representations (ICLR).*
3. DeLong and Bhatt (2020). "Towards Collusion Detection in Poker."
4. Yan and Browne (2016). "Collusion Detection in Online Poker."
5. Southey, F., Bowling, M., Larson, B., Piccione, C., Burch, N., Billings, D. and Rayner, C. (2005). "Bayes' Bluff: Opponent Modelling in Poker." *Proceedings of the 21st Conference on Uncertainty in Artificial Intelligence (UAI).*

**Practical Tasks.**

- Build a data pipeline from anonymized Playtech hand histories (~50,000–100,000 hands, cash game six-max tables) to structured game records and state tensors; validate for impossible states (duplicate cards, negative stacks, pot mismatches).
- Extend Step 12's poker state tensor encoding from Kuhn and Leduc to full Hold'em (52-dimensional one-hot card encoding, position, pot/stack ratios, betting history, street indicator, active player count).
- Compute standard behavioral statistics per player: VPIP<sup>49</sup>, PFR, Aggression Factor, WTSD, W\$SD, 3-bet percentage, and continuation bet percentage.
- Train player embeddings<sup>48</sup> (player2vec approach) by treating poker actions as tokens and training a Transformer encoder with masked action prediction; extract per-player embedding vectors.
- Apply k-means clustering (four classic archetypes: tight-aggressive, loose-aggressive, tight-passive, loose-passive) and DBSCAN on the embedding space; validate against manual VPIP×PFR classification and test temporal stability.
- Implement a collusion detection<sup>50</sup> module with three signals — co-occurrence anomaly, chip dumping score, and soft play score — combined via weighted composite scoring; validate by injecting synthetic collusion patterns and measuring detection recall (target >90%) and false positive rate (target <5%).
- Apply the Decision Transformer<sup>46</sup> from Step 12 to Playtech data; compare return-conditioned versus EV-conditioned training per the Paster et al. stochasticity warning.

---

## 8. Phase G — Integration (Steps 14–15) · beginning of September – beginning of October 2026

### 8.1 Phase Overview

The preceding six phases progressively developed the theoretical foundations, algorithmic toolbox, and data pipelines required by the thesis. Phase G synthesizes this body of work into two integrative deliverables. Step 14 constructs a unified, three-layer evaluation framework — combining exploitability<sup>3</sup> computation, population-level ranking, and statistical confidence quantification — that is validated across all game types encountered in the study plan (two-player, N-player, and real-world data). This framework constitutes the core of Contribution 3 (Evaluation Methodology). Step 15 maps the research frontier across all three contribution areas, designs the experimental programme for the subsequent research phase, produces a detailed outline for the first dissertation chapter (due November 2026), and establishes the publication pipeline through to defense. Together, these steps complete the transition from the learning phase (Steps 1–14) to the research phase of the doctoral programme.

### 8.2 Step 14 — Evaluation Frameworks and Exploitability Metrics

**Contribution Alignment.** This step constitutes Contribution 3 (Evaluation Methodology) directly. The three-layer evaluation framework integrates: (1) an exploitability layer providing exact computation for small games and approximate computation via RL-based best response<sup>51</sup> for large games, supplemented by the adaptation safety<sup>35</sup> metric of Ge et al. (2024); (2) a population ranking layer comparing Elo, $\alpha$-Rank<sup>52</sup> (evolutionary dynamics via Markov-Conley chains), VasE<sup>53</sup> (social choice theory via maximal lotteries), and meta-Nash equilibrium from EGTA<sup>43</sup>, with the spinning top decomposition<sup>42</sup> as a diagnostic for intransitive competitive structure; and (3) a statistical confidence layer applying AIVAT<sup>54</sup> variance reduction for imperfect-information game evaluation and bootstrapped confidence intervals with sample complexity bounds. The framework is validated across Kuhn Poker<sup>19</sup>, Leduc Hold'em<sup>20</sup>, So Long Sucker<sup>45</sup>, and Playtech real-world data. For Contribution 1, the framework measures whether behavioral adaptation produces measurable improvements in exploitability and population ranking. For Contribution 2, marginal exploitability<sup>55</sup> — the N-player extension of standard exploitability — tests whether two-player safe exploitation guarantees generalize to multi-agent settings.

**Literature.**

1. Timbers, F., Bard, N., Lockhart, E., Lanctot, M., Schmid, M., Burch, N., Schrittwieser, J., Hubert, T. and Bowling, M. (2022). "Approximate Exploitability: Learning a Best Response in Large Games." Preprint.
2. Lanctot, M., Larson, K., Bachrach, Y., Marris, L., Li, Z., Bhoopchand, A., Anthony, T., Tanner, B. and Koop, A. (2025). "Evaluating Agents using Social Choice Theory." Preprint.
3. Rowland, M., Omidshafiei, S., Tuyls, K., Perolat, J., Valko, M., Piliouras, G. and Munos, R. (2019). "Multiagent Evaluation under Incomplete Information." Preprint.
4. Burch, N., Johanson, M. and Bowling, M. (2019). "AIVAT: A New Variance Reduction Technique for Agent Evaluation in Imperfect Information Games." *Proceedings of the 33rd AAAI Conference on Artificial Intelligence.*
5. Omidshafiei, S., Papadimitriou, C., Piliouras, G., Tuyls, K. et al. (2019). "$\alpha$-Rank: Multi-Agent Evaluation by Evolution." *Nature Scientific Reports.*

**Practical Tasks.**

- Audit and unify all evaluation code from prior steps (exploitability from Steps 3 and 8, EGTA<sup>43</sup> and spinning top decomposition<sup>42</sup> from Step 10, SLS metrics from Step 11, behavioral metrics from Step 13) into a three-layer evaluation API.
- Construct a bot zoo of reference agents for Kuhn and Leduc covering four tiers: trivial (random, always-call, always-fold), heuristic (tight-aggressive, loose-aggressive, tight-passive), computed (Nash/CFR, DQN), and advanced (PSRO<sup>38</sup>, Decision Transformer<sup>46</sup>).
- Implement $\alpha$-Rank<sup>52</sup> with Fermi selection function; compute stationary distributions via eigenvalue decomposition and analyze sensitivity to the selection pressure parameter.
- Implement VasE<sup>53</sup> with tournament matrix construction from pairwise comparisons across games; compute maximal lotteries via linear programming and intransitive cycle detection.
- Implement AIVAT<sup>54</sup> variance reduction using a CFR-derived control variate with counterfactual adjustment per chance node; verify variance reduction of at least five-fold on Kuhn and ten-fold on Leduc relative to raw evaluation.
- Conduct cross-game validation: full three-layer evaluation on Kuhn, Leduc, So Long Sucker<sup>45</sup> (marginal exploitability<sup>55</sup>), and Playtech data (AIVAT-adjusted confidence intervals for style classification and collusion detection<sup>50</sup>).
- Produce a disagreement analysis comparing Elo, $\alpha$-Rank, and VasE rankings, with the spinning top decomposition explaining cases of divergence between transitive and cyclic competitive structures.

### 8.3 Step 15 — Research Frontier Mapping and Contribution Design

**Contribution Alignment.** This step completes the learning phase and designs the research phase. The deliverables directly become the structural components of the doctoral work: the research frontier map identifies the specific gaps addressed by each contribution against the most recent literature; the contribution design documents formalize the three research proposals (Behavioral Adaptation Framework, Multi-Agent Safe Exploitation, Evaluation Methodology) with precise problem statements, proposed methods, experimental protocols, and risk assessments; the experiment specifications define four controlled studies validating the contributions across Kuhn Poker, Leduc Hold'em, three-player Kuhn, and So Long Sucker; the Chapter I outline structures the first dissertation chapter (25–30 pages, due November 2026) covering foundations, opponent modeling, safe exploitation, and evaluation; and the publication pipeline maps six target publications across four dissertation chapters through to defense in April 2029.

**Literature.**

1. Southey, F., Bowling, M., Larson, B., Piccione, C., Burch, N., Billings, D. and Rayner, C. (2005). "Bayes' Bluff: Opponent Modelling in Poker." *Proceedings of the 21st Conference on Uncertainty in Artificial Intelligence (UAI).*
2. Ganzfried, S. and Sandholm, T. (2015). "Safe Opponent Exploitation." *ACM Transactions on Economics and Computation*, 3(2).
3. Ge, C., Zhu, Y. et al. (2024). "Safe and Robust Subgame Exploitation in Imperfect Information Games." *Proceedings of the 41st International Conference on Machine Learning (ICML).*
4. Ge, C., Wang, Y., Li, W. and Jin, C. (2024). "Securing Equal Share: A Principled Approach for Learning Multiplayer Symmetric Games." Preprint.
5. Milec, D., Kovařík, V. and Lisý, V. (2025). "Adapting Beyond the Depth Limit: Counter Strategies in Large Imperfect Information Games." Preprint.
6. Omidshafiei, S., Papadimitriou, C., Piliouras, G., Tuyls, K. et al. (2019). "$\alpha$-Rank: Multi-Agent Evaluation by Evolution." *Nature Scientific Reports.*

**Practical Tasks.**

- Produce a research frontier map documenting, for each of the three contributions, the current state of the art, the identified gap, supporting evidence from the study plan, and a feasibility assessment.
- Validate each identified gap against recent publications (2024–2026), conference proceedings, and existing dissertations; record findings in a gap validation log.
- Write contribution design documents (three documents, two to three pages each) specifying the problem statement, prior art, gap, proposed method, experimental protocol, target publications, timeline, and risk analysis.
- Specify four experiments: (1) behavioral adaptation on Kuhn Poker (player embedding<sup>48</sup> classification accuracy within 50 hands), (2) N-player safe exploitation on three-player Kuhn (piKL-regularized exploitation versus equal-share baseline), (3) coalition-aware safe exploitation on So Long Sucker<sup>45</sup>, and (4) cross-game evaluation framework validation across Kuhn, Leduc, and SLS.
- Produce a Chapter I outline (seven sections, 25–30 pages) covering introduction, foundations, opponent modeling and behavioral adaptation, safe exploitation, evaluation of multi-agent game AI, proposed contributions, and research plan — aligned with the November 2026 deadline.
- Establish the publication pipeline: six target publications mapped to four dissertation chapters with venue selections and submission deadlines through April 2029.

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

### Multi-Agent Dynamics

**[36] Non-stationarity (multi-agent).**
The fundamental challenge that arises when multiple agents learn simultaneously: each agent's environment — which includes the other agents — changes as those agents update their policies, violating the stationarity assumption of single-agent reinforcement learning.

**[37] Centralized Training with Decentralized Execution (CTDE).**
A multi-agent reinforcement learning paradigm in which agents have access to global information (other agents' observations and actions) during training but execute using only local observations at deployment. Representative algorithms include MADDPG (centralized critic, decentralized actors), QMIX (monotonic value decomposition), and MAPPO (PPO with centralized value function).

**[38] Policy Space Response Oracles (PSRO).**
A population-based framework that maintains a growing set of policies and iteratively computes meta-Nash equilibria over the current population, then trains new best-response policies via reinforcement learning. Unifies fictitious play, self-play, and the double oracle method as special cases.

**[39] Population-Based Training (PBT).**
A meta-optimization framework in which a population of agents trains in parallel, periodically copying weights from high-performing agents (exploit) and mutating hyperparameters (explore). The AlphaStar league is the landmark application, with three agent roles — main agents, main exploiters, and league exploiters — maintaining population diversity and robustness.

**[40] Learning with Opponent-Learning Awareness (LOLA).**
A multi-agent learning algorithm in which each agent differentiates through the anticipated parameter update of its opponent, enabling anticipatory adaptation rather than reactive best-response. Achieves cooperation in settings where naive independent learners converge to suboptimal outcomes.

**[41] Coalition.**
A subset of players in an N-player game who coordinate their strategies for mutual benefit. In free-for-all settings, coalitions may form and dissolve dynamically during play, creating a social structure that cannot be captured by two-player game-theoretic frameworks.

**[42] Spinning top decomposition.**
A decomposition (Balduzzi et al., 2019) of any antisymmetric payoff matrix into a transitive component (representing genuine skill ranking) and a cyclic component (representing non-transitive, rock-paper-scissors structure). The transitive ratio serves as a diagnostic distinguishing real improvement from illusory cycling in population-based training.

**[43] Empirical Game-Theoretic Analysis (EGTA).**
A framework for analyzing multi-agent systems by constructing finite empirical games over sampled strategy sets and computing Nash equilibria of the resulting meta-game. Generalizes two-player exploitability to the population setting and provides approximation bounds for empirical Nash convergence.

**[44] Shapley value.**
A solution concept from cooperative game theory that assigns each player a payoff equal to their average marginal contribution across all possible coalition orderings. Applied in multi-agent reinforcement learning as a credit assignment mechanism (Shapley Q-value) that decomposes joint rewards into per-agent attributions.

**[45] So Long Sucker (SLS).**
A four-player coalition formation game designed by Nash, Shapley, Shubik, and Hausner (1950) in which players must form temporary alliances to eliminate opponents but only one player can win. Serves as a benchmark for studying dynamic coalition formation, betrayal, and negotiation in competitive multi-agent settings.

### Data-Driven Approaches

**[46] Decision Transformer (DT).**
A sequence model architecture that reformulates offline reinforcement learning as return-conditioned sequence prediction. A GPT-2 backbone predicts actions from (return-to-go, state, action) token sequences, matching or exceeding value-based offline RL methods without temporal-difference learning or Bellman backups. Subject to a critical limitation in stochastic environments, where return conditioning conflates lucky outcomes with skilled decisions.

**[47] Adversarially Robust Decision Transformer (ARDT).**
An extension of the Decision Transformer that conditions on minimax returns-to-go via expectile regression rather than empirical returns ­— recovering near-Nash equilibrium strategies from offline data in sequential games with sufficient data coverage. Addresses the standard Decision Transformer's vulnerability in adversarial settings.

**[48] Player embedding (player2vec).**
A vector representation of a player's behavioral patterns, obtained by treating in-game actions as tokens and training a Transformer encoder with masked action prediction on sequences of a player's hands. Produces representations that cluster by behavioral style without requiring manual labels.

**[49] VPIP (Voluntarily Put In Pot).**
A standard poker behavioral statistic measuring the percentage of hands in which a player voluntarily contributes chips to the pot before the flop. Combined with PFR (Pre-Flop Raise percentage), VPIP forms the primary axis for classifying player archetypes (tight versus loose, passive versus aggressive).

**[50] Collusion detection.**
The problem of identifying coordinated play among ostensibly independent players in multiplayer games. Detection signals include co-occurrence anomaly (pairs appearing together more often than expected), chip dumping (directional monetary transfer between colluding players), and soft play (reduced aggression against specific opponents). Extends the coalition detection methodology of Step 11 to a practical fraud detection application.

### Evaluation and Integration

**[51] Approximate exploitability.**
A method for estimating exploitability in games too large for exact best-response computation, by training an RL-based best-response agent against the strategy under evaluation. The trained agent's payoff provides a lower bound on the true exploitability.

**[52] $\alpha$-Rank.**
A multi-agent evaluation method based on evolutionary dynamics. Constructs a Markov chain over the strategy population using a Fermi selection function; the stationary distribution assigns each strategy a ranking that captures both transitive dominance and cyclic competitive structure. Unlike Elo, $\alpha$-Rank is sensitive to intransitive (rock-paper-scissors) relationships.

**[53] VasE (Voting as Stochastic Estimation).**
An evaluation method grounded in social choice theory. Constructs a tournament matrix from pairwise agent comparisons across games and computes maximal lotteries via linear programming. Detects intransitive cycles that Elo-based rankings cannot capture and provides a principled aggregation of performance across heterogeneous evaluation domains.

**[54] AIVAT.**
A variance reduction technique for evaluating agents in imperfect-information games (Burch, Johanson, and Bowling, 2019). Uses a control variate derived from the CFR value function to make counterfactual adjustments at each chance node, reducing evaluation variance by an order of magnitude while maintaining an unbiased estimator.

**[55] Marginal exploitability.**
An extension of standard exploitability to N-player settings. Measures each player's incentive to deviate unilaterally from the current strategy profile, accounting for the fact that in multiplayer games the concept of a unique best response is complicated by coalition structures and non-unique equilibria.
