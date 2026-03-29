# Step 5 — Neural Equilibrium Approximation (Deep CFR, DREAM)

**Duration:** 11 days (Tier 2 — compressed)  
**Dependencies:** Step 1 (RL Basics), Step 3 (CFR Variants + MC Methods), Step 4 (Game Abstraction + Scaling)  
**Phase:** C — Neural Methods for Games

> **Know-How First compression:** Implementation phase cut from 6d to 3d. Get Deep CFR running on Leduc with correct exploitability convergence. Understand DREAM conceptually. Defer full DREAM implementation and head-to-head benchmark to implementation phase post-November. All reading and intuition phases unchanged.

---

## Objectives

Replace tabular CFR with neural function approximation to enable equilibrium computation in games too large for explicit state enumeration:

1. Understand Deep CFR's architecture: advantage networks approximating counterfactual values, strategy networks distilling the average policy, and reservoir sampling for experience management
2. Understand Neural Fictitious Self-Play (NFSP) as an alternative paradigm connecting deep reinforcement learning to Nash equilibrium computation
3. Implement Deep CFR from scratch in PyTorch on Leduc Hold'em and compare against tabular MCCFR from Step 3
4. Establish the first GPU-accelerated training pipeline and information state encoding reusable in subsequent steps

---

## Literature

### Papers

1. **Brown, N., Lerer, A., Gross, S. & Sandholm, T. (2019).** "Deep Counterfactual Regret Minimization." *Proceedings of the 36th International Conference on Machine Learning (ICML).*  
   arXiv: https://arxiv.org/abs/1811.00164  
   *Replaces tabular regret storage with neural advantage networks trained via external-sampling MCCFR traversals. Uses reservoir sampling for experience replay and a separate strategy network for average policy distillation. First demonstration of neural CFR scaling beyond explicit game representations.*

2. **Steinberger, E. (2019).** "Single Deep Counterfactual Regret Minimization." *Proceedings of the 34th AAAI Conference on Artificial Intelligence (2020).*  
   arXiv: https://arxiv.org/abs/1901.07621  
   *Simplifies Deep CFR with a single network handling both players, introduces DREAM (Deep Regret minimization with Advantage baselines and Model-free learning) — an outcome-sampling variant with variance reduction. More practical to implement than original Deep CFR.*

3. **Heinrich, J. & Silver, D. (2016).** "Deep Reinforcement Learning from Self-Play in Imperfect-Information Games."  
   arXiv: https://arxiv.org/abs/1603.01121  
   *Introduces Neural Fictitious Self-Play (NFSP) — a completely different approach to equilibrium computation using DQN for best-response learning and supervised learning for average strategy approximation. Bridges deep RL and game-theoretic equilibrium, providing an alternative paradigm to CFR-based methods.*

### Supplementary References

4. **Xu, H. et al. (2025).** "Deep (Predictive) Discounted Counterfactual Regret Minimization." *Accepted at AAAI 2026.*  
   arXiv: https://arxiv.org/abs/2511.08174  
   *Combines discounted regret weights with predictive neural networks for faster convergence. Extends the Deep CFR framework with modern optimization techniques.*

5. **Rudolph, M. et al. (2025).** "Reevaluating Policy Gradient Methods for Imperfect-Information Games."  
   arXiv: https://arxiv.org/abs/2502.08938  
   *Challenges the assumption that naive self-play deep RL fails in adversarial imperfect-information games, showing competitive performance with proper hyperparameter tuning. Provides important context for the relative merits of CFR-based vs. RL-based equilibrium methods.*

---

## Methodology

### Phase 1: Conceptual Foundation (1 day)

Survey of the neural equilibrium problem: why tabular CFR cannot scale to full-sized games even with abstraction (e.g., Texas Hold'em has $10^{161}$ states), and how neural function approximation enables generalization across similar game states. Establish understanding of two paradigms — CFR-based (Deep CFR, DREAM) and RL-based (NFSP) — and their respective tradeoffs.

### Phase 2: Empirical Familiarization (2 days)

Hands-on experimentation using OpenSpiel implementations:
- Deep CFR on Leduc Hold'em: convergence analysis, network size sensitivity
- NFSP on Kuhn and Leduc: convergence comparison against Deep CFR and tabular MCCFR
- Inspection of advantage network predictions against known tabular counterfactual values from Step 3
- Identification of the iteration cost vs. convergence speed tradeoff between neural and tabular methods

### Phase 3: Literature Study (3 days)

Structured reading of three sources:

1. **Brown et al. (2019):** Deep CFR architecture — advantage network loss function (MSE on sampled counterfactual values), the external-sampling MCCFR traversal for data generation, reservoir sampling for experience management, and the strategy network for average policy output. Focus on understanding the advantage network loss as the core mechanism replacing tabular regret.

2. **Steinberger (2019):** Single Deep CFR and DREAM — single-network simplification, outcome sampling with baseline subtraction for variance reduction. Practical considerations for implementation efficiency.

3. **Heinrich & Silver (2016):** NFSP — the two-network architecture (DQN best-response + supervised average-policy), anticipatory parameter $\eta$ controlling the Nash-exploitation tradeoff. Understanding of NFSP as the RL-based alternative to CFR-based equilibrium methods.

### Phase 4: Implementation (6 days)

From-scratch implementation in PyTorch, building on the Step 3 Leduc engine:

| Implementation | Validation Criterion |
|----------------|---------------------|
| Information state tensor encoding | Consistent representation reusable in Steps 6–8 |
| Advantage networks (2 per player, MLP) | Predicted CF values match tabular values on Kuhn within 10% |
| External-sampling MCCFR → training data pipeline | Generates valid (info_state, CF_values) training pairs |
| Reservoir sampling memory buffer | Uniform retention probability verified |
| Strategy network (average policy distillation) | Exploitability < 0.1 on Leduc within 100 iterations |
| NFSP implementation for comparison | Exploitability < 0.2 on Leduc within 100k episodes |

**Validation approach:** Three-way convergence comparison (Deep CFR vs. tabular MCCFR vs. NFSP) on both exploitability and wall-clock time. Cross-validation against OpenSpiel's Deep CFR implementation. GPU profiling to establish compute baselines for subsequent steps.

### Phase 5: Synthesis (2 days)

Consolidation of theoretical and practical knowledge:
- Connection mapping: tabular MCCFR (Step 3) → neural MCCFR (Step 5) → search-based architectures (Step 6)
- Connection mapping: hand-crafted abstraction (Step 4) → learned compression via neural approximation (Step 5)
- Forward connection: advantage networks ↔ value networks in DeepStack/ReBeL (Step 6)
- Assessment of Rudolph et al. (2025) perspective on RL vs. CFR for equilibrium computation
- Documentation of step summary and learning log updates

---

## Deliverables

1. **Information state tensor encoding** for Leduc Hold'em (reusable in Steps 6–8)
2. **Deep CFR implementation** with advantage networks, strategy network, reservoir sampling, and MCCFR traversal
3. **NFSP implementation** for comparative analysis
4. **Three-way convergence comparison** — Deep CFR vs. tabular MCCFR vs. NFSP (exploitability and wall time)
5. **GPU profiling report** documenting compute requirements for neural equilibrium methods
6. **Step summary** connecting neural equilibrium methods to the broader algorithmic progression

---

## PhD Contribution Alignment

| Concept | Downstream Application |
|---------|----------------------|
| Deep CFR advantage networks | Technical mechanism for computing baseline strategies in large games (Contribution #1) |
| Information state encoding | Foundation for opponent modeling input representation (Contribution #1, Step 7) |
| Neural function approximation | Enables scalable strategy computation without explicit abstraction (Contributions #1, #2) |
| NFSP's anticipatory parameter η | Foreshadows the exploitation-safety tradeoff central to safe exploitation (Step 8, Contribution #1) |
| GPU training pipeline | Infrastructure for all subsequent neural implementations |

---

## Exit Criteria

- [ ] Deep CFR producing convergent strategies on Leduc, cross-validated against OpenSpiel
- [ ] NFSP producing convergent strategies on Leduc
- [ ] Three-way convergence comparison completed with clear analysis
- [ ] Ability to explain Deep CFR architecture and advantage network loss from memory
- [ ] Ability to explain the difference between Deep CFR and NFSP paradigms
- [ ] GPU profiling completed with documented compute baselines
- [ ] Information state encoding designed and documented for reuse
- [ ] Step summary completed and committed to repository
- [ ] Connections to Steps 1–4 and forward to Steps 6–8 identified and documented

