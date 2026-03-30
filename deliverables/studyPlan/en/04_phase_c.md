## 4. Phase C — Neural Methods for Games (Steps 5–6)

### 4.1 Phase Overview

Phases A and B established tabular equilibrium solvers and abstraction techniques for medium-scale games. However, tabular methods store explicit strategy and regret values at every information set^6^ — an approach whose memory requirements grow linearly with game size and become prohibitive for large-scale domains. This phase replaces tabular storage with neural network function approximation, enabling equilibrium computation without explicit game tree enumeration. Step 5 introduces the core approximation methods (Deep CFR^25^, NFSP^27^), while Step 6 studies the complete game-solving architectures (DeepStack, Libratus, Pluribus, ReBeL^28^, Student of Games) that integrate these components into competition-grade systems. Together, these steps complete the algorithmic toolbox from which the thesis contributions are developed: Contribution 1 builds on the public belief state^29^ framework of ReBeL, Contribution 2 addresses the theoretical gap exposed by Pluribus's multiplayer success without formal safety guarantees, and Contribution 3 draws on the exploitability metrics applied uniformly across all five architectures.

### 4.2 Step 5 — Neural Equilibrium Approximation (Deep CFR, DREAM)

**Contribution Alignment.** Deep CFR^25^ and NFSP^27^ will be studied as methods for computing equilibrium strategies in games too large for tabular solvers — a capability needed for the planned behavioral adaptation work. NFSP’s anticipatory parameter, which interpolates between equilibrium and exploitative play, foreshadows the exploitation–safety tradeoff central to the thesis. The information state tensor encoding developed here will serve as the standard input representation for later neural architectures.

**Literature.**

1. Brown, N., Lerer, A., Gross, S. and Sandholm, T. (2019). "Deep Counterfactual Regret Minimization." *Proceedings of the 36th International Conference on Machine Learning (ICML).*
2. Steinberger, E. (2019). "Single Deep Counterfactual Regret Minimization." *Proceedings of the 34th AAAI Conference on Artificial Intelligence (2020).*
3. Heinrich, J. and Silver, D. (2016). "Deep Reinforcement Learning from Self-Play in Imperfect-Information Games." Preprint.

**Practical Tasks.**

- Develop a reusable information state tensor encoding for Leduc Hold'em^20^, designed for compatibility with all subsequent neural implementations.
- Implement Deep CFR with advantage networks, reservoir sampling, and strategy network distillation; verify that predicted counterfactual values^2^ match tabular baselines on Kuhn Poker^19^.
- Implement NFSP as a comparative baseline; evaluate the effect of the anticipatory parameter on the Nash–exploitation tradeoff.
- Compare convergence behavior (exploitability^3^ versus wall time) of Deep CFR, tabular MCCFR^23^, and NFSP on Leduc Hold'em.

### 4.3 Step 6 — End-to-End Game AI Architectures

**Contribution Alignment.** This step will survey five landmark game-solving systems that define the current state of the art. ReBeL’s public belief state^29^ framework is of particular relevance to the planned belief-based opponent modeling (Contribution 1). Pluribus demonstrates empirical success in multiplayer poker without formal safety guarantees — highlighting the theoretical gap that Contribution 2 will seek to address. The exploitability metric applied uniformly across all architectures will inform the evaluation methodology design (Contribution 3).

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
- Construct a comparative analysis of all five architectures (DeepStack, Libratus, Pluribus, ReBeL, Student of Games), mapping shared components (MCCFR^23^, subgame solving^22^, neural value estimation, depth-limited search) and identifying the evolutionary path from single-player to multiplayer to unified systems.

