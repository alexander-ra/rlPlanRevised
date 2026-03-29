# Step 10 — Population-Based Training and Evolutionary Game Theory

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 7 (Opponent Modeling), Step 8 (Safe Exploitation), Step 9 (Multi-Agent Reinforcement Learning)  
**Phase:** E — Multi-Agent Dynamics  

---

## Objectives

1. Study Population-Based Training (PBT) as a meta-optimization framework for multi-agent systems, including the AlphaStar league architecture and its three-role population design.
2. Develop working knowledge of evolutionary game theory (replicator dynamics, evolutionary stable strategies) and its connection to multi-agent learning dynamics.
3. Implement and apply the spinning top decomposition (Balduzzi et al., 2019) to analyze the transitive and non-transitive structure of multi-agent competition.
4. Build an empirical game-theoretic analysis (EGTA) framework for evaluating population-based training systems.
5. Connect population-level training dynamics to the thesis contributions: automated opponent modeling (Contribution #1), population-level safety guarantees (Contribution #2), and meta-game evaluation methodology (Contribution #3).

---

## Key Topics

- Population-Based Training: co-evolution of weights and hyperparameters across parallel agent populations
- AlphaStar League: three-role architecture (main agents, main exploiters, league exploiters) and prioritized matchmaking
- Replicator dynamics: continuous-time selection dynamics over strategy populations
- Evolutionary stable strategies (ESS): refinement of Nash equilibrium under evolutionary perturbation
- Spinning top decomposition: separation of payoff structure into transitive (skill) and cyclic (non-transitive) components
- Empirical Game-Theoretic Analysis (EGTA): finite-strategy approximation of large-scale games via population sampling

---

## Literature

### Core References

1. **Jaderberg, M., Dalibard, V., Osindero, S., Czarnecki, W. M., Donahue, J., Razavi, A., Vinyals, O., Green, T., Dunning, I., Simonyan, K., Fernando, C. & Kavukcuoglu, K.** (2017). *Population Based Training of Neural Networks.* arXiv:1711.09846.  
   — Foundational PBT framework: parallel population of models with exploit (copy best weights) and explore (mutate hyperparameters) operations. Replaces sequential hyperparameter search with population-level co-evolution.

2. **Jaderberg, M., Czarnecki, W. M., Dunning, I., Marris, L., Lever, G., Castañeda, A. G., Beattie, C., Rabinowitz, N. C., Morcos, A. S., Ruderman, A., Sonnerat, N., Green, T., Deason, L., Leibo, J. Z., Silver, D., Hassabis, D., Kavukcuoglu, K. & Graepel, T.** (2019). *Human-Level Performance in First-Person Multiplayer Games with Population-Based Deep Reinforcement Learning.* Science, 364(6443), 859–865.  
   — First application of PBT to multiplayer games (Capture-the-Flag). Demonstrates emergent cooperation and competition within population dynamics, with implicit curriculum creation through population self-organization.

3. **Vinyals, O., Babuschkin, I., Czarnecki, W. M., Mathieu, M., Dudzik, A., Chung, J., Choi, D. H., Powell, R., Ewalds, T., Georgiev, P., ... & Silver, D.** (2019). *Grandmaster Level in StarCraft II Using Multi-Agent Reinforcement Learning.* Nature, 575(7782), 350–354.  
   — The AlphaStar league: gold standard for population-based training in games. Three agent roles (main agents, main exploiters, league exploiters) maintain population diversity and robustness. Meta-Nash computation over the league defines training matchups.

4. **Balduzzi, D., Garnelo, M., Bachrach, Y., Czarnecki, W. M., Pérolat, J., Jaderberg, M. & Graepel, T.** (2019). *Open-Ended Learning in Symmetric Zero-Sum Games.* In Proc. ICLR 2019. arXiv:1901.01753.  
   — Introduces the spinning top decomposition: every antisymmetric payoff matrix decomposes into a transitive (skill ranking) and cyclic (non-transitive, rock-paper-scissors) component. Proposes rectified PSRO to handle the cyclic component. Critical diagnostic for evaluating whether population-based improvement is genuine or illusory.

5. **Tuyls, K., Pérolat, J., Lanctot, M., Ostrovski, G., Savani, R., Leibo, J. Z., Ord, T., Graepel, T. & Legg, S.** (2018). *A Generalised Method for Empirical Game Theoretic Analysis.* In Proc. AAMAS 2018. arXiv:1803.06376.  
   — Framework for analyzing multi-agent systems by constructing finite empirical games over sampled strategy sets. Provides approximation bounds for empirical Nash convergence. Theoretical foundation for PSRO convergence analysis and population-level evaluation.

### Supplementary References

6. **Hofbauer, J. & Sigmund, K.** (2003). *Evolutionary Game Dynamics.* Bulletin of the American Mathematical Society, 40(4), 479–519.  
   — Foundational treatment of replicator dynamics, evolutionary stable strategies, and their relationship to Nash equilibria. Provides the mathematical framework connecting evolutionary dynamics to game-theoretic solution concepts.

7. **Hill, E.** (2025). *Co-Evolving Complexity: An Adversarial Framework for Automatic MARL Curricula.* In NeurIPS 2025 Workshop. arXiv:2509.03771.  
   — Co-evolutionary curriculum design for multi-agent training. Automatic difficulty progression through adversarial population dynamics. Relevant to auto-curriculum mechanisms in population-based training.

8. **Xu, G., Liu, Z., Deng, Y., Xu, H., Zhong, F. & Li, B.** (2025). *Heterogeneous Adversarial Play in Interactive Environments.* In Proc. NeurIPS 2025. arXiv:2510.18407.  
   — Population diversity through heterogeneous adversarial self-play mechanisms. Relevant to maintaining strategy diversity in population-based training systems.

9. **De La Fuente, Y., Ley, R. & Ortega, J.** (2024). *Game Theory and Multi-Agent Reinforcement Learning: From Nash Equilibria to Evolutionary Dynamics.* arXiv:2412.20523.  
   — Survey connecting classical game theory with evolutionary approaches to multi-agent reinforcement learning. Provides conceptual overview of the integration between equilibrium computation and population dynamics.

---

## Methodology

Following the 5-phase learning cycle (Tier 2, 14-day allocation):

| Phase | Duration | Focus |
|-------|----------|-------|
| Intuition | 1 day | PBT motivation, AlphaStar population design, evolutionary game theory fundamentals |
| Exploration | 2 days | PSRO population analysis, replicator dynamics on matrix games, PBT hyperparameter experiment |
| Targeted Reading | 3 days | Core papers: PBT → FTW → AlphaStar → spinning top decomposition → EGTA |
| Implementation | 6 days | Replicator dynamics simulator, spinning top decomposition, PBT league for Leduc, EGTA analysis, diversity metrics |
| Consolidation | 2 days | Survey integration, PhD mapping, learning log, one-pager |

### Implementation Plan

1. **Replicator dynamics simulator:** Implement continuous-time replicator dynamics on matrix games. Verify convergence to Nash/ESS on Prisoner's Dilemma, Hawk-Dove, Stag Hunt; verify cycling on Rock-Paper-Scissors. Generate phase portraits.
2. **Spinning top decomposition:** Implement the transitive-cyclic decomposition (Balduzzi et al., 2019, Theorem 1). Apply to PSRO meta-game payoff matrices from Step 9 and to the league meta-game from this step. Compute transitive ratio as a diagnostic metric.
3. **PBT league for Leduc poker:** Three agent roles inspired by AlphaStar: main agents (trained against full league for robustness), main exploiters (trained against main agents to find weaknesses), league exploiters (trained against entire league). Includes prioritized matchmaking, periodic agent freezing, and PBT explore-exploit population updates.
4. **EGTA analysis:** Construct the empirical normal-form game over the league population. Compute meta-Nash equilibrium. Verify: meta-Nash mixture exploitability ≤ best individual agent exploitability.
5. **Comparative evaluation:** League vs PSRO (Step 9) vs single self-play agent vs MCCFR Nash strategy (Step 3). Metrics: exploitability, Elo rating, effective population diversity, strategy clustering.

---

## PhD Alignment

**Contribution #1 — Behavioral Adaptation Framework:** PBT's exploiter mechanism constitutes automated opponent modeling at population scale. Main exploiters identify weaknesses in main agents analogously to the explicit Bayesian modeling of Step 7, but embedded within the training loop. The thesis integrates explicit modeling (Step 7) with implicit population-level modeling (Step 10).

**Contribution #2 — Multi-Agent Safe Exploitation:** The AlphaStar league provides heuristic safety through exploiter pressure but lacks formal guarantees. Formalizing population-level safety — defining what "safe exploitation in a population" means mathematically — is a key thesis contribution. The spinning top decomposition suggests a decomposition of safety: guarantee non-exploitability in the transitive component while accepting cycling in the cyclic component.

**Contribution #3 — Evaluation Methodology:** EGTA provides the multi-agent evaluation framework: meta-Nash of the agent population generalizes exploitability to the population setting. The spinning top decomposition provides a diagnostic distinguishing genuine skill improvement from non-transitive cycling. These tools form the prototype for the thesis evaluation methodology.

**Bridge to Step 11:** The population of diverse agents and evolutionary analysis from this step directly feeds into Step 11's coalition formation in free-for-all games. Population dynamics create the diverse agent pool needed for coalition emergence, and the spinning top decomposition predicts that FFA coalition dynamics will exhibit significant non-transitive structure.

---

## Expected Outputs

1. Replicator dynamics simulator with verified convergence/cycling behaviour on matrix games
2. Phase portraits for Prisoner's Dilemma, Hawk-Dove, Rock-Paper-Scissors, and Stag Hunt
3. Spinning top decomposition implementation with transitive ratio metric applied to PSRO and league meta-games
4. PBT league for Leduc poker with three agent roles, matchmaking, and population evolution
5. EGTA analysis computing meta-Nash of the league population
6. Elo rating system tracking skill progression across training epochs
7. Comparative analysis: league vs PSRO vs self-play vs Nash (MCCFR) on Leduc
8. One-page summary document
9. Updated learning log with cross-step connections and open research questions

