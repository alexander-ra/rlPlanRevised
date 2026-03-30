## 2. Phase A — Foundation (Steps 1–2)

### 2.1 Phase Overview

This phase covers the foundational material required for all subsequent work: reinforcement learning basics (value estimation, policy optimization, experience replay) and game-theoretic fundamentals (extensive-form games, Nash equilibrium computation, and exploitability measurement). A solid command of both domains is essential before proceeding to the more specialized topics of later phases.

### 2.2 Step 1 — Reinforcement Learning Basics

**Contribution Alignment.** The reinforcement learning methods studied in this step — value estimation, policy gradients, and experience replay — will recur throughout the thesis, particularly in the opponent modeling and adaptive exploitation components of the planned contributions.

**Literature.**

1. Sutton, R.S. and Barto, A.G. (2018). *Reinforcement Learning: An Introduction*, 2nd edition. MIT Press.
2. Mnih, V., Kavukcuoglu, K., Silver, D. et al. (2015). "Human-level control through deep reinforcement learning." *Nature*, 518(7540), pp. 529–533.
3. Schulman, J., Wolski, F., Dhariwal, P., Radford, A. and Klimov, O. (2017). "Proximal Policy Optimization Algorithms." Preprint.

**Practical Tasks.**

- Implement a Deep Q-Network^16^ (DQN) agent with experience replay^9^ and target network; train on a discrete control task (CartPole-v1).
- Implement a Proximal Policy Optimization^17^ (PPO) agent with generalized advantage estimation; train on a continuous control task (LunarLander-v3).
- Compare learning curves of both agents; analyze sensitivity to key hyperparameters (learning rate, batch size, discount factor).
- Validate both implementations against established reference results.

### 2.3 Step 2 — Game Theory and Counterfactual Regret Minimization

**Contribution Alignment.** The extensive-form game representation and CFR algorithm introduced here will provide the formal framework and baseline equilibrium computation used throughout the thesis. Exploitability^3^, defined and implemented in this step, will serve as the primary quantitative metric across all three contributions.

**Literature.**

1. Shoham, Y. and Leyton-Brown, K. (2008). *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations.* Cambridge University Press.
2. Neller, T.W. and Lanctot, M. (2013). "An Introduction to Counterfactual Regret Minimization." Technical report, Gettysburg College.
3. Zinkevich, M., Johanson, M., Bowling, M. and Piccione, C. (2007). "Regret Minimization in Games with Incomplete Information." *Advances in Neural Information Processing Systems 20 (NeurIPS).*

**Practical Tasks.**

- Construct a complete game engine for Kuhn Poker^19^ (three-card deck, two players, one betting round), including game tree enumeration and terminal payoff computation.
- Implement vanilla CFR^15^ with regret^18^ accumulation and average strategy computation; verify convergence to the known analytical Nash equilibrium^7^ of Kuhn Poker.
- Implement best response^1^ computation and exploitability^3^ measurement; verify $O(1/\sqrt{T})$ convergence rate on a log-log scale.
- Cross-validate the resulting strategy profile against the OpenSpiel reference implementation.

