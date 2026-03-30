## 5. Phase D — Opponent Modeling and Exploitation (Steps 7–8)

### 5.1 Phase Overview

This phase addresses the central research question: how should an agent adapt its play to a specific opponent? The preceding phases built the algorithmic toolbox — equilibrium solvers, abstraction, and neural approximation — but did not yet tackle opponent-aware play. Step 7 will introduce inference mechanisms that convert observed action sequences into beliefs about opponent behavior. Step 8 will cover algorithms that translate those beliefs into profitable yet safe strategy adjustments. Together, these steps will form the foundation for Contribution 1 (Behavioral Adaptation) and expose the theoretical limitations that Contribution 2 (Multi-Agent Safe Exploitation) will need to address.

### 5.2 Step 7 — Opponent Modeling — Inference from Behavioral Traces

**Contribution Alignment.** Bayesian opponent modeling^31^ will serve as the inference component of the planned Behavioral Adaptation Framework (Contribution 1). Three modeling paradigms will be studied — type-based models, continuous parametric models, and consistent convergent estimators — each offering different tradeoffs between assumptions, convergence speed, and robustness. The multiplayer extension, which requires joint beliefs over all opponents, will expose computational challenges relevant to Contribution 2. Non-stationarity handling will address an open problem relevant to the evaluation methodology (Contribution 3).

**Literature.**

1. Southey, F., Bowling, M., Larson, B., Piccione, C., Burch, N., Billings, D. and Rayner, C. (2005). "Bayes' Bluff: Opponent Modelling in Poker." *Proceedings of the 21st Conference on Uncertainty in Artificial Intelligence (UAI).*
2. Bard, N., Johanson, M., Burch, N. and Bowling, M. (2013). "Online Implicit Agent Modelling." *Proceedings of the 12th International Conference on Autonomous Agents and Multi-Agent Systems (AAMAS).*
3. Ganzfried, S. and Sun, Q. (2016). "Bayesian Opponent Exploitation in Imperfect-Information Games." Preprint.
4. Ganzfried, S., Wang, K.A. and Chiswick, M. (2022). "Opponent Modeling in Multiplayer Imperfect-Information Games." Preprint.
5. Ganzfried, S. (2025). "Consistent Opponent Modeling in Imperfect-Information Games." Preprint.
6. Shoham, Y. and Leyton-Brown, K. (2008). *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations.* Cambridge University Press. Chapter 7: Learning and Teaching.

**Practical Tasks.**

- Construct an opponent type library with five or more distinct strategies (tight-aggressive, loose-passive, Nash equilibrium, exploitative, random) for both Kuhn Poker^19^ and Leduc Hold'em^20^.
- Implement an observation buffer handling partial observability (showdown versus non-showdown information extraction).
- Implement a type-based Bayesian opponent model^31^ with Dirichlet-multinomial posterior inference and a continuous Bayesian model with per-information-set action distribution estimation.
- Implement a consistent opponent modeler following the Ganzfried (2025) sequence-form projected gradient descent approach.
- Build an adaptive exploitation pipeline integrating opponent modeling and best-response^1^ computation.
- Conduct a head-to-head model comparison measuring convergence speed, final exploitation rate, and robustness to unknown opponent types.
- Execute non-stationarity tests demonstrating model behavior under opponent type switching.

### 5.3 Step 8 — Safe Exploitation — Theory, Algorithms, and Real-Time Search

**Contribution Alignment.** This step covers the exploitation–safety tradeoff^33^, which is the theoretical core of the thesis. Key topics include the Restricted Nash Response (RNR^32^), the Safety Theorem of Ganzfried and Sandholm (2015) — which provides formal guarantees in two-player zero-sum settings but fails in N-player games, exposing the gap that Contribution 2 will address — subgame exploitation methods for real-time safe play (relevant to Contribution 1), and teaching attack^34^ resilience testing as a prototype for the adversarial evaluation methodology of Contribution 3.

**Literature.**

1. Johanson, M., Bowling, M. and Zinkevich, M. (2007). "Computing Robust Counter-Strategies." *Advances in Neural Information Processing Systems (NeurIPS).*
2. Ganzfried, S. and Sandholm, T. (2015). "Safe Opponent Exploitation." *ACM Transactions on Economics and Computation*, 3(2).
3. Liu, W., Wang, H., Guo, T. and Xing, J. (2022). "Safe Opponent-Exploitation Subgame Refinement." *Advances in Neural Information Processing Systems (NeurIPS).*
4. Jeary, J. and Turrini, P. (2023). "Safe Opponent Exploitation For Epsilon Equilibrium Strategies." Preprint.
5. Ge, C., Zhu, Y. et al. (2024). "Safe and Robust Subgame Exploitation in Imperfect Information Games." *Proceedings of the 41st International Conference on Machine Learning (ICML).*
6. Milec, D., Kovařík, V. and Lisý, V. (2025). "Adapting Beyond the Depth Limit: Counter Strategies in Large Imperfect Information Games." Preprint.
7. Shoham, Y. and Leyton-Brown, K. (2008). *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations.* Cambridge University Press. Sections 3.4 and 4.6.

**Practical Tasks.**

- Implement a safety checker module computing worst-case exploitability^3^ and verifying safety constraints against the blueprint strategy.
- Implement an exploitation metrics module measuring exploitation value and safety violations.
- Build a Restricted Nash Response (RNR^32^) solver with configurable safety parameter $p \in [0,1]$.
- Implement the Ganzfried safe exploitation solver enforcing the Safety Theorem guarantee.
- Implement a prime-safe exploitation extension handling $\varepsilon$-equilibrium baselines (connecting abstraction quality from Step 4).
- Build an SES-style subgame exploitation solver with gadget construction for real-time safe exploitation.
- Implement an adaptation safety^35^ checker following the Ge et al. (2024) safety notion.
- Generate exploitation–safety Pareto frontier plots for all methods across multiple opponent types.
- Integrate the full pipeline: Step 7 opponent models^30^ feeding Step 8 exploitation engine, evaluated end-to-end.
- Conduct a teaching attack^34^ stress test with deceptive opponent switching behavior mid-game and robustness analysis.

