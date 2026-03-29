# Step 9 — Multi-Agent RL — Coordination, Competition, and Communication

**Duration:** 14 days  
**Prerequisites:** Step 1 (RL Basics), Step 6 (End-to-End Game AI Architectures)  
**Phase:** E — Multi-Agent Dynamics

---

## Formal Objectives

1. Understand the fundamental challenges of multi-agent reinforcement learning — non-stationarity, credit assignment, and the coordination problem — that distinguish MARL from both single-agent RL and equilibrium computation.
2. Study the Centralized Training with Decentralized Execution (CTDE) paradigm as the dominant approach to cooperative MARL, through its principal instantiations: MADDPG (centralized critic), QMIX (value decomposition), and MAPPO (centralized value function).
3. Study Policy Space Response Oracles (PSRO) as the game-theoretic framework that bridges equilibrium computation (Steps 2–8) with multi-agent learning, unifying fictitious play, self-play, and double oracle as special cases.
4. Examine learning-aware opponent modeling (LOLA) as a distinct paradigm from the static inference approach studied in Step 7, where agents model the opponent's learning dynamics rather than current strategy.
5. Implement and compare independent learning, CTDE methods, and PSRO on matrix games and Goofspiel, establishing empirical understanding of when each approach succeeds or fails.

---

## Literature

### Core References

1. **Lowe, R., Wu, Y., Tamar, A., Harb, J., Abbeel, P. & Mordatch, I.** (2017). Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments. In *Advances in Neural Information Processing Systems (NeurIPS)*. https://arxiv.org/abs/1706.02275  
   *Introduces MADDPG — the original CTDE algorithm for continuous action spaces. Centralized critics observe all agents' actions during training; decentralized actors execute with local observations only.*

2. **Rashid, T., Samvelyan, M., de Witt, C.S., Farquhar, G., Foerster, J. & Whiteson, S.** (2018). QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning. In *Proceedings of the International Conference on Machine Learning (ICML)*. https://arxiv.org/abs/1803.11485  
   *Proposes value decomposition via monotonic mixing networks. The monotonicity constraint enables decentralized argmax execution while training on the joint Q-function.*

3. **Yu, C., Velu, A., Vinitsky, E., Gao, J., Wang, Y., Baez, A. & Fishi, S.** (2022). The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games. In *Advances in Neural Information Processing Systems (NeurIPS)*. https://arxiv.org/abs/2103.01955  
   *Demonstrates that simple PPO with centralized value function (MAPPO) matches or outperforms more complex cooperative MARL methods across diverse benchmarks.*

4. **Foerster, J., Chen, R.Y., Al-Shedivat, M., Whiteson, S., Abbeel, P. & Mordatch, I.** (2018). Learning with Opponent-Learning Awareness. In *Proceedings of the International Conference on Autonomous Agents and Multiagent Systems (AAMAS)*. https://arxiv.org/abs/1709.04326  
   *Introduces LOLA — agents that differentiate through the opponent's learning update, achieving cooperation in settings where naive learners converge to suboptimal outcomes.*

5. **Lanctot, M., Zambaldi, V., Gruslys, A., Lazaridou, A., Tuyls, K., Pérolat, J., Silver, D. & Graepel, T.** (2017). A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning. In *Advances in Neural Information Processing Systems (NeurIPS)*. https://arxiv.org/abs/1711.00832  
   *Proposes Policy Space Response Oracles (PSRO) — the double-oracle framework that maintains a policy population, computes meta-Nash equilibria, and trains best-response policies via RL. Unifies fictitious play, self-play, and double oracle as special cases.*

6. **Sukhbaatar, S., Szlam, A. & Fergus, R.** (2016). Learning Multiagent Communication with Backpropagation. In *Advances in Neural Information Processing Systems (NeurIPS)*. https://arxiv.org/abs/1605.07736  
   *Introduces CommNet — differentiable inter-agent communication via mean-field message aggregation. Demonstrates that useful communication protocols can emerge from end-to-end training.*

### Supplementary References

7. **Zhong, Y., Kuba, J.G., Feng, X., Hu, S., Ji, J. & Yang, Y.** (2023). Heterogeneous-Agent Reinforcement Learning. https://arxiv.org/abs/2304.09870  
   *Unified framework for cooperative MARL with heterogeneous agents, addressing the homogeneity assumption in standard CTDE methods.*

8. **Bighashdel, A., Simão, T.D. & Oliehoek, F.A.** (2026). Sample-Efficient Policy Space Response Oracles with Joint Experience Best Response. In *Proceedings of AAMAS 2026*. https://arxiv.org/abs/2602.06599  
   *Improves PSRO sample efficiency through joint experience sharing across best-response training.*

9. **Amato, C.** (2024/2025). An Initial Introduction to Cooperative Multi-Agent Reinforcement Learning. https://arxiv.org/abs/2405.06161  
   *Pedagogical survey of cooperative MARL concepts and algorithms.*

---

## Methodology

### Phase 1 — Orientation (Day 1)
Survey the multi-agent RL landscape through tutorial talks (Foerster AAAI 2024, Whiteson cooperative MARL) and accessible introductions. Establish the conceptual distinctions between independent learning, centralized training with decentralized execution (CTDE), game-theoretic MARL (PSRO), and learning-aware optimization (LOLA).

### Phase 2 — Exploration (Days 2–3)
Hands-on experimentation with PettingZoo multi-agent environments (simple_spread, simple_adversary) and OpenSpiel multi-player games (Goofspiel). Run random and independent PPO agents to observe coordination failures. Explore existing MAPPO/QMIX implementations to see CTDE in action. Test self-play on familiar games (Kuhn, Leduc) and compare with equilibrium solutions.

### Phase 3 — Literature Study (Days 4–6)
Close reading of six core papers with emphasis on:
- **Lowe et al. (MADDPG)** — centralized critic gradient as CTDE template (Section 3, Equation 5)
- **Rashid et al. (QMIX)** — monotonicity constraint for value decomposition (Section 3)
- **Yu et al. (MAPPO)** — simplicity-effectiveness tradeoff in cooperative MARL (Sections 3–4)
- **Foerster et al. (LOLA)** — learning-aware gradient that differentiates through opponent's update (Section 3, Equation 4)
- **Lanctot et al. (PSRO)** — double-oracle framework bridging game theory and MARL (Section 3, Algorithm 1)
- **Sukhbaatar et al. (CommNet)** — differentiable emergent communication (Section 2)

Critical mathematical content: MADDPG centralized gradient, QMIX monotonicity condition, LOLA look-ahead gradient, PSRO meta-Nash computation.

### Phase 4 — Implementation (Days 7–12)
Build and compare MARL paradigms on controlled testbeds:
1. **Matrix game testbed** — Prisoner's Dilemma, Matching Pennies, Stag Hunt, Battle of the Sexes
2. **Independent learners** — PPO agents ignoring other agents (baseline for non-stationarity failures)
3. **MADDPG** — centralized critic with decentralized actors
4. **MAPPO** — PPO with centralized value function
5. **PSRO** — population-based meta-Nash + RL best-response oracle, verified on Kuhn and Leduc
6. **CommNet communication** — mean-field message channel integrated with MADDPG

Evaluate on Goofspiel (OpenSpiel) as a multi-player strategic game beyond the particle environments.

### Phase 5 — Consolidation (Days 13–14)
Survey skim of Shoham & Leyton-Brown (Chapters 6–7) and Zhang et al. (2021) MARL survey. Map each implemented algorithm to its position in the MARL taxonomy. Synthesise findings connecting PSRO to thesis Contribution #2 (meta-Nash as safety framework for multi-agent exploitation) and LOLA to Contribution #1 (dynamic opponent modeling extending Step 7's static model).

---

## Expected Outputs

- Matrix game testbed with verified Nash equilibria
- Working implementations of independent learning, MADDPG, MAPPO, and PSRO
- PSRO convergence to Nash verified on Kuhn Poker
- CommNet communication channel showing measurable benefit on cooperative tasks
- Comparison table: independent learning vs CTDE vs PSRO across all test environments
- One-page summary and updated learning log

---

## PhD Alignment

This step transitions the thesis from two-player zero-sum settings (Steps 2–8) to the multi-agent world, providing the algorithmic vocabulary for the remaining thesis contributions:

- **Contribution 1** extends opponent modeling (Step 7) with LOLA's insight that modelling learning dynamics, not just current strategy, enables better adaptation. The thesis combines static Bayesian inference with dynamic anticipation.
- **Contribution 2** identifies the fundamental gap: Step 8's safety guarantees rely on the minimax theorem (2-player zero-sum). PSRO's meta-Nash framework provides the starting point for defining safety in multi-agent populations. Steps 10 and 11 will develop this further.
- **Contribution 3** gains PSRO's meta-game analysis as a multi-agent evaluation tool — measuring distance to meta-Nash equilibrium rather than two-player exploitability alone.

> **[P9] Markov-Games Bridge:** Add a short formal bridge on Markov games (stochastic games) to Phase 1 (Orientation), before jumping into CTDE/PSRO/LOLA. ~Half-page of notation connecting EFG-style reasoning (game trees, information sets, counterfactual values) to MARL-style reasoning (joint policies, centralized critics, decentralized execution). Explains what is preserved (sequential decisions, partial observability) and what is lost (exact game tree structure, regret-based convergence guarantees). ~0.5d absorbed within 14d allocation.

