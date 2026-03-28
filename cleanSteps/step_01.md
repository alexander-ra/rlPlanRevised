# Step 1 — Reinforcement Learning Basics

**Duration:** 14 days (Tier 2)  
**Dependencies:** None (entry point)  
**Phase:** A — Foundation

---

## Objectives

Establish foundational competence in reinforcement learning theory and practice:

1. Master the mathematical framework of Markov Decision Processes (MDPs)
2. Understand the progression from tabular methods (dynamic programming, Monte Carlo, temporal-difference learning) to deep reinforcement learning
3. Implement two foundational deep RL algorithms — Deep Q-Network (DQN) and Proximal Policy Optimization (PPO)
4. Develop practical experience with standard RL environments and benchmarking methodology

---

## Literature

### Textbook

**Sutton, R.S. & Barto, A.G. (2018).** *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.  
Available: http://incompleteideas.net/book/the-book-2nd.html

| Chapters | Topic | Focus |
|----------|-------|-------|
| 1–2 | Introduction & Multi-Armed Bandits | Problem framing, notation |
| 3 | Finite Markov Decision Processes | MDP formulation, Bellman equations |
| 4 | Dynamic Programming | Policy evaluation, policy iteration, value iteration |
| 5 | Monte Carlo Methods | Model-free estimation, first-visit MC |
| 6 | Temporal-Difference Learning | TD(0), SARSA, Q-learning |
| 13 | Policy Gradient Methods | REINFORCE algorithm, baseline methods |

### Papers

1. **Mnih, V., Kavukcuoglu, K., Silver, D. et al. (2015).** "Human-level control through deep reinforcement learning." *Nature*, 518(7540), 529–533.  
   arXiv: https://arxiv.org/abs/1509.06461  
   *Introduces Deep Q-Networks (DQN) combining Q-learning with deep neural networks, experience replay, and target networks for stable learning in high-dimensional state spaces.*

2. **Schulman, J., Wolski, F., Dhariwal, P., Radford, A. & Klimov, O. (2017).** "Proximal Policy Optimization Algorithms."  
   arXiv: https://arxiv.org/abs/1707.06347  
   *Introduces the clipped surrogate objective for stable policy gradient updates, achieving trust-region-like stability with first-order optimization.*

### Supplementary References

3. **Santana, P. (2025).** "An Introduction to Deep Reinforcement and Imitation Learning."  
   arXiv: https://arxiv.org/abs/2512.08052  
   *Recent self-contained treatment covering MDPs through PPO and imitation learning methods.*

4. **OpenAI.** "Spinning Up in Deep RL."  
   https://spinningup.openai.com/  
   *Structured primer on key RL concepts and policy optimization.*

---

## Methodology

### Phase 1: Conceptual Foundation (1 day)

Survey of core RL concepts through structured introductory material: agent-environment interaction, reward hypothesis, policy and value functions, exploration-exploitation trade-off. Establish the conceptual vocabulary needed for the subsequent phases.

### Phase 2: Empirical Familiarization (2 days)

Hands-on experimentation with existing RL implementations using the Gymnasium library and Stable-Baselines3 framework. Systematic observation of:
- Training dynamics for value-based (DQN) and policy-based (PPO) methods
- Hyperparameter sensitivity on CartPole-v1 and LunarLander-v3 environments
- Comparative behavior of on-policy vs off-policy algorithms

### Phase 3: Literature Study (3 days)

Structured reading of Sutton & Barto Chapters 1–6 and 13, covering the theoretical progression from tabular dynamic programming to temporal-difference methods to policy gradient optimization. Focused study of the DQN paper (Mnih et al., 2015) and PPO paper (Schulman et al., 2017) with emphasis on:
- Algorithmic descriptions and design motivations
- Experimental methodology and key results
- The role of experience replay and target networks (DQN)
- The clipped surrogate objective and its relationship to trust region methods (PPO)

### Phase 4: Implementation (6 days)

From-scratch implementation of both algorithms in Python (PyTorch / Gymnasium):

| Implementation | Environment | Success Criterion |
|----------------|-------------|-------------------|
| DQN (Q-network, experience replay, target network, ε-greedy) | CartPole-v1 | Mean reward ≥ 475/500 over 100 episodes |
| PPO (actor-critic, GAE, clipped surrogate loss) | LunarLander-v3 | Mean reward ≥ 200 over 100 episodes |

**Validation approach:** Comparison of learning curves against Stable-Baselines3 reference implementations under identical hyperparameter configurations. Reward convergence within ±10% of reference.

### Phase 5: Synthesis (2 days)

Consolidation of theoretical and practical knowledge:
- Gap analysis against textbook material (targeted review of Sutton & Barto Ch 7, 9 for forward context)
- Preparation of step summary document
- Identification of cross-step connections and open questions for subsequent steps
- Documentation of methodological insights for the learning log

---

## Deliverables

1. **DQN agent** solving CartPole-v1, validated against Stable-Baselines3 reference
2. **PPO agent** solving LunarLander-v3, validated against Stable-Baselines3 reference
3. **Comparative analysis** — learning curves and hyperparameter sensitivity report
4. **Step summary** connecting RL foundations to the broader research progression

---

## PhD Contribution Alignment

This step provides the foundational RL vocabulary, agent architecture patterns, and implementation methodology required by all subsequent steps. The core concepts introduced here serve the research program as follows:

| Concept | Downstream Application |
|---------|----------------------|
| Value networks (DQN) | Opponent value estimation in behavioral adaptation (Contribution #1) |
| Policy gradient methods (PPO) | Adaptive policy learning against non-stationary opponents (Contribution #1) |
| Experience replay | Behavioral trace storage for opponent modeling (Contribution #1, Step 7) |
| Hyperparameter sensitivity analysis | Evaluation methodology for agent robustness (Contribution #3, Step 14) |

---

## Exit Criteria

- [ ] Both agents achieve target performance metrics, validated against reference implementations
- [ ] Ability to explain DQN and PPO algorithms from memory without reference material
- [ ] Understanding of key design choices: target networks (DQN), clipped objective (PPO)
- [ ] Step summary completed and committed to repository
- [ ] Connections to subsequent steps (2–6) identified and documented
