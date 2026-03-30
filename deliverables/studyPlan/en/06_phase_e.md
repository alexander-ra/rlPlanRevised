## 6. Phase E — Multi-Agent Dynamics (Steps 9–11)

### 6.1 Phase Overview

The preceding phases focused on two-player imperfect-information games. Phase E will transition the study to multi-agent settings, where new challenges arise: non-stationarity^36^ from simultaneously learning agents, credit assignment in joint-reward environments, and the emergence of coalitions^41^. Step 9 introduces multi-agent RL paradigms (CTDE^37^, PSRO^38^), Step 10 scales to population-based training^39^ and evolutionary game theory, and Step 11 applies these tools to coalition formation in free-for-all games — crystallizing the theoretical gap at the core of Contribution 2.

### 6.2 Step 9 — Multi-Agent RL — Coordination, Competition, and Communication

**Contribution Alignment.** This step will provide the algorithmic vocabulary for extending the thesis from two-player to multi-agent settings. The CTDE^37^ paradigm introduces the architectural pattern — centralized training, decentralized execution — used throughout the remainder of the thesis. PSRO^38^ provides a population-based framework relevant to defining safety in multi-agent populations (Contribution 2). LOLA^40^ contributes the insight of modeling an opponent's learning dynamics, extending the Bayesian modeling of Step 7 from static inference to dynamic anticipation (Contribution 1).

**Literature.**

1. Lowe, R., Wu, Y., Tamar, A., Harb, J., Abbeel, P. and Mordatch, I. (2017). "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments." *Advances in Neural Information Processing Systems (NeurIPS).*
2. Rashid, T., Samvelyan, M., de Witt, C.S., Farquhar, G., Foerster, J. and Whiteson, S. (2018). "QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning." *Proceedings of the International Conference on Machine Learning (ICML).*
3. Yu, C., Velu, A., Vinitsky, E., Gao, J., Wang, Y., Baez, A. and Fishi, S. (2022). "The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games." *Advances in Neural Information Processing Systems (NeurIPS).*
4. Foerster, J., Chen, R.Y., Al-Shedivat, M., Whiteson, S., Abbeel, P. and Mordatch, I. (2018). "Learning with Opponent-Learning Awareness." *Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS).*
5. Lanctot, M., Zambaldi, V., Gruslys, A., Lazaridou, A., Tuyls, K., Pérolat, J., Silver, D. and Graepel, T. (2017). "A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning." *Advances in Neural Information Processing Systems (NeurIPS).*
6. Sukhbaatar, S., Szlam, A. and Fergus, R. (2016). "Learning Multiagent Communication with Backpropagation." *Advances in Neural Information Processing Systems (NeurIPS).*

**Practical Tasks.**

- Construct a matrix game testbed (Prisoner's Dilemma, Matching Pennies, Stag Hunt, Battle of the Sexes) with verified Nash equilibria.
- Implement independent PPO learners as a baseline demonstrating non-stationarity^36^ failures in multi-agent settings.
- Implement MADDPG (centralized critic, decentralized actors) and MAPPO (PPO with centralized value function) as CTDE^37^ representatives.
- Implement PSRO^38^ with population-based meta-Nash computation and RL best-response oracle; verify convergence to Nash equilibrium on Kuhn Poker^19^ and Leduc Hold'em^20^.
- Integrate a CommNet differentiable communication channel with MADDPG; evaluate the benefit of emergent communication on cooperative tasks.
- Produce a comparative evaluation table: independent learning versus CTDE versus PSRO across all test environments and Goofspiel.

### 6.3 Step 10 — Population-Based Training and Evolutionary Game Theory

**Contribution Alignment.** Population-based training and the AlphaStar league architecture will be studied as examples of implicit opponent modeling at population scale, complementing the explicit Bayesian modeling of Step 7 (Contribution 1). The spinning top decomposition^42^ — distinguishing genuine skill improvement from non-transitive cycling — will be adopted into the evaluation methodology (Contribution 3). EGTA^43^ will provide meta-Nash analysis extending exploitability assessment to population settings.

**Literature.**

1. Jaderberg, M., Dalibard, V., Osindero, S., Czarnecki, W.M. et al. (2017). "Population Based Training of Neural Networks." Preprint.
2. Jaderberg, M., Czarnecki, W.M., Dunning, I. et al. (2019). "Human-Level Performance in First-Person Multiplayer Games with Population-Based Deep Reinforcement Learning." *Science*, 364(6443), pp. 859–865.
3. Vinyals, O., Babuschkin, I., Czarnecki, W.M. et al. (2019). "Grandmaster Level in StarCraft II Using Multi-Agent Reinforcement Learning." *Nature*, 575(7782), pp. 350–354.
4. Balduzzi, D., Garnelo, M., Bachrach, Y., Czarnecki, W.M., Pérolat, J., Jaderberg, M. and Graepel, T. (2019). "Open-Ended Learning in Symmetric Zero-Sum Games." *Proceedings of the International Conference on Learning Representations (ICLR).*
5. Tuyls, K., Pérolat, J., Lanctot, M. et al. (2018). "A Generalised Method for Empirical Game Theoretic Analysis." *Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS).*
6. Hofbauer, J. and Sigmund, K. (2003). "Evolutionary Game Dynamics." *Bulletin of the American Mathematical Society*, 40(4), pp. 479–519.

**Practical Tasks.**

- Implement a replicator dynamics simulator on matrix games; verify convergence to Nash equilibrium and evolutionary stable strategies on Prisoner's Dilemma, Hawk-Dove, and Stag Hunt, and verify cycling on Rock-Paper-Scissors. Generate phase portraits.
- Implement the spinning top decomposition^42^ (Balduzzi et al., 2019); apply to PSRO^38^ meta-game payoff matrices from Step 9 and to the league meta-game from this step. Compute the transitive ratio as a diagnostic metric.
- Build a PBT league for Leduc Hold'em^20^ with three agent roles (main agents, main exploiters, league exploiters), prioritized matchmaking, periodic agent freezing, and PBT explore-exploit population updates.
- Conduct EGTA^43^ analysis: construct the empirical normal-form game over the league population and compute meta-Nash equilibrium; verify that the meta-Nash mixture exploitability does not exceed that of the best individual agent.
- Produce a comparative evaluation: league versus PSRO (Step 9) versus single self-play agent versus MCCFR^23^ Nash strategy (Step 3), measuring exploitability, Elo rating, effective population diversity, and strategy clustering.

### 6.4 Step 11 — Dynamic Coalition Formation in Competitive Free-For-All Games

**Contribution Alignment.** This step crystallizes the central theoretical gap of the thesis. In two-player games, safe exploitation uses Nash equilibrium as the safety baseline (Step 8). In N-player free-for-all games, Nash equilibrium is both computationally intractable and strategically insufficient — it ignores coalition structures. The piKL regularization approach of Bakhtin et al. (2022) suggests replacing equilibrium-based safety with behavioral-prior-based safety, a shift that Contribution 2 will seek to formalize. Coalition detection will extend opponent modeling from individual player types to multi-agent social structure (Contribution 1). Shapley-value^44^ credit decomposition combined with EGTA^43^ will provide the basis for N-player evaluation methodology (Contribution 3).

**Literature.**

1. Sharan, M. and Adak, C. (2024). "Reinforcing Competitive Multi-Agents for Playing 'So Long Sucker'." Preprint.
2. De Carufel, J.-L. and Jerade, M.R. (2024). "So Long Sucker: Endgame Analysis." Preprint.
3. Bakhtin, A., Wu, D.J., Lerer, A., Gray, J., Jacob, A.P., Farina, G., Miller, A.H. and Brown, N. (2022). "Mastering the Game of No-Press Diplomacy via Human-Regularized Reinforcement Learning and Planning." Preprint.
4. Chalkiadakis, G., Elkind, E. and Wooldridge, M. (2011). *Computational Aspects of Cooperative Game Theory.* Morgan and Claypool.
5. Wang, J., Zhang, Y., Kim, T.-K. and Gu, Y. (2020). "Shapley Q-value: A Local Reward Approach to Solve Global Reward Games." *Proceedings of the 34th AAAI Conference on Artificial Intelligence.*

**Practical Tasks.**

- Build a verified So Long Sucker^45^ environment with coalition tracking, rich state representation, and correctness validation against the endgame analysis of De Carufel and Jerade (2024).
- Implement a coalition detection module that infers implicit alliances from observed chip-placement behavior using help/harm matrices, extending the opponent modeling methodology of Step 7 to multi-agent alliance inference.
- Adapt Shapley Q-value^44^ decomposition to the competitive free-for-all setting, distributing each action's credit among all players according to marginal coalition contributions.
- Train four-player MAPPO agents with Shapley-decomposed rewards via self-play; compare against a sparse-reward baseline replicating Sharan and Adak (2024).
- Apply EGTA^43^ (Step 10) to construct the four-player payoff tensor and compute meta-Nash over the agent population; apply the spinning top decomposition^42^ to quantify the non-transitive structure of coalition dynamics.
- Produce a comparative evaluation: coalition-aware agents versus sparse-reward agents versus random baselines, measuring win rate, coalition formation frequency, Shapley variation, and game length.

