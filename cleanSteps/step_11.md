# Step 11 — Dynamic Coalition Formation in Competitive Free-For-All Games

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 7 (Opponent Modeling), Step 9 (Multi-Agent Reinforcement Learning), Step 10 (PBT + Evolutionary Game Theory)  
**Phase:** E — Multi-Agent Dynamics  

---

## Objectives

1. Study the So Long Sucker (SLS) game as a benchmark for coalition formation in competitive multi-agent settings, and implement a verified computational environment for the game.
2. Develop coalition detection mechanisms that infer implicit alliances from observed agent behavior, extending the opponent modeling methodology from Step 7 to the multi-agent alliance setting.
3. Implement Shapley-value-based credit assignment for competitive free-for-all games, adapting cooperative game theory tools to environments where coalitions are temporary and unstable.
4. Train coalition-aware multi-agent reinforcement learning agents using Shapley-decomposed rewards and evaluate whether coalition-aware training produces qualitatively different strategic behavior compared to standard sparse-reward training.
5. Apply empirical game-theoretic analysis (EGTA) and the spinning top decomposition from Step 10 to analyze the non-transitive structure of coalition dynamics.
6. Connect findings to the thesis: formalize the gap between 2-player safe exploitation (Step 8) and N-player FFA safety (Contribution #2), and prototype EGTA-based evaluation for N-player games (Contribution #3).

---

## Key Topics

- So Long Sucker: 4-player coalition formation game designed by Nash, Shapley, Shubik, and Hausner (1950)
- Cooperative game theory: Shapley value, the core, and coalition stability concepts
- Coalition detection: inferring implicit alliances from behavioral observation sequences
- Shapley Q-value: decomposition of global reward into per-agent contributions via marginal coalition analysis
- N-player game-theoretic planning: piKL regularization and behavioral priors as replacements for Nash baselines in multiplayer settings
- Non-transitivity in free-for-all dynamics: spinning top decomposition adapted for N-player payoff tensors

---

## Literature

### Core References

1. **Sharan, M. & Adak, C.** (2024). *Reinforcing Competitive Multi-Agents for Playing 'So Long Sucker'.* arXiv:2411.11057.  
   — First computational framework and RL benchmark for SLS. Trains DQN/DDQN/Dueling DQN agents via self-play; agents achieve approximately 50% of maximum reward and outperform random baselines. Establishes SLS as a negotiation-aware benchmark for multi-agent reinforcement learning.

2. **De Carufel, J.-L. & Jerade, M. R.** (2024). *So Long Sucker: Endgame Analysis.* arXiv:2403.17302.  
   — Complete combinatorial characterization of winning strategies in the 2-player SLS endgame. Provides ground truth for verifying implementation correctness and evaluating agent endgame optimality.

3. **Bakhtin, A., Wu, D. J., Lerer, A., Gray, J., Jacob, A. P., Farina, G., Miller, A. H. & Brown, N.** (2022). *Mastering the Game of No-Press Diplomacy via Human-Regularized Reinforcement Learning and Planning.* arXiv:2210.05492.  
   — Achieves human-level play in 7-player no-press Diplomacy. Introduces piKL regularization: policy search constrained to remain close to a human behavioral prior, replacing intractable Nash-based safety with empirical behavioral baselines. Demonstrates implicit coalition formation in large-scale multiplayer games.

4. **Chalkiadakis, G., Elkind, E. & Wooldridge, M.** (2011). *Computational Aspects of Cooperative Game Theory.* Morgan & Claypool.  
   — Textbook treatment of cooperative game theory solution concepts (Shapley value, core, nucleolus, bargaining set) and coalition structure generation algorithms. Chapters 2–4 provide the mathematical foundations for coalition analysis.

5. **Wang, J., Zhang, Y., Kim, T.-K. & Gu, Y.** (2020). *Shapley Q-value: A Local Reward Approach to Solve Global Reward Games.* In Proc. AAAI 2020. arXiv:1907.05707.  
   — Decomposes joint Q-values into per-agent Shapley values for credit assignment in cooperative MARL. Provides both exact and Monte Carlo approximation algorithms. Foundation for adapting Shapley credit assignment to competitive FFA settings.

### Supplementary References

6. **Li, J., Kuang, K., Wang, B., Liu, F., Chen, L., Wu, F. & Xiao, J.** (2021). *Shapley Counterfactual Credits for Multi-Agent Reinforcement Learning.* In Proc. KDD 2021. arXiv:2106.00285.  
   — Combines Shapley value decomposition with counterfactual baselines for MARL credit assignment. Connects cooperative game theory credit assignment with counterfactual reasoning methods from regret minimization (Steps 2–4).

7. **Wang, J., Li, Y., Kaski, S. & Lawry, J.** (2025). *Shapley Machine: A Game-Theoretic Framework for N-Agent Ad Hoc Teamwork.* arXiv:2506.11285.  
   — Shapley-based framework for ad hoc teamwork in N-agent settings. Addresses implicit coalition formation with unknown teammates, directly relevant to the dynamic alliance setting in SLS.

8. **Meta AI** (2022). *Human-Level Play in the Game of Diplomacy by Combining Language Models with Strategic Reasoning* (CICERO). Science, 378(6624), 1067–1074.  
   — Full-press Diplomacy system combining language model negotiation with game-theoretic planning. Demonstrates multi-player coalition reasoning at the state-of-the-art level. Architecture reference for integrating coalition reasoning into strategic planning.

9. **Mukobi, S., Erlebach, H., Lauffer, N., Hammond, L., Chan, A. & Clifton, J.** (2023). *Welfare Diplomacy: Benchmarking Language Model Cooperation.* arXiv:2310.08901.  
   — LLM agents playing Diplomacy variants. Evaluates cooperation and coalition formation in language-model-driven multi-agent settings. Bridge to Step 12 (LLM agents in strategic settings).

---

## Methodology

Following the 5-phase learning cycle (Tier 2, 14-day allocation):

| Phase | Duration | Focus |
|-------|----------|-------|
| Intuition | 1 day | Coalition dynamics motivation, SLS rules, cooperative game theory fundamentals |
| Exploration | 2 days | Play SLS manually + with baseline agents, compute Shapley values on toy coalition games |
| Targeted Reading | 3 days | Core papers: SLS benchmark → SLS endgame → no-press Diplomacy → cooperative GT textbook → Shapley Q-value |
| Implementation | 6 days | SLS environment, coalition detection, Shapley credit assignment, coalition-aware MARL training, EGTA analysis |
| Consolidation | 2 days | Survey integration, PhD mapping, learning log, one-pager |

### Implementation Plan

1. **SLS environment:** Build or extend a verified SLS implementation with coalition tracking and rich state representation. Verify correctness against the formal rules and endgame analysis from De Carufel & Jerade (2024).
2. **Coalition detection module:** Infer implicit alliances from observed chip-placement behavior using help/harm matrices. Extends Step 7's opponent modeling methodology to multi-agent alliance inference.
3. **Shapley credit assignment:** Adapt Shapley Q-value decomposition to the competitive FFA setting: each action's credit distributed among all players according to marginal coalition contributions. Replaces sparse winner-takes-all rewards with dense, attribution-aware learning signals.
4. **Coalition-aware MARL training:** Train 4-player MAPPO agents with Shapley-decomposed rewards via self-play. Compare against sparse-reward baseline (replicating Sharan & Adak) to evaluate whether coalition-aware training produces qualitatively different strategic behavior.
5. **Meta-game analysis:** Apply EGTA (Step 10) to construct the 4-player payoff tensor and compute meta-Nash over the agent population. Apply spinning top decomposition (projected to pairwise matchups) to quantify the non-transitive structure of coalition dynamics.
6. **Comparative evaluation:** Coalition-aware agents vs sparse-reward agents vs random baselines. Metrics: win rate, coalition formation frequency, Shapley variation, game length, spinning top transitive ratio.

---

## PhD Alignment

**Contribution #1 — Behavioral Adaptation Framework:** The coalition detection module extends opponent modeling from inferring individual player types to inferring multi-agent social structure. This is the multi-agent generalization of behavioral adaptation: adapting to the alliance structure of the game rather than to individual opponents alone.

**Contribution #2 — Multi-Agent Safe Exploitation:** This step crystallizes the central thesis gap. In 2-player games, safe exploitation uses Nash equilibrium as the safety baseline (Step 8). In N-player FFA games, Nash is both computationally intractable and strategically unhelpful (it ignores coalitions). The piKL approach from Bakhtin et al. (2022) suggests replacing equilibrium-based safety with behavioral-prior-based safety. Formalizing this shift — defining and proving safety guarantees for N-player FFA settings using behavioral or population-based baselines — is the core thesis contribution.

**Contribution #3 — Evaluation Methodology:** Standard exploitability is undefined in N-player games because there is no clear "best response" against a coalition structure. EGTA meta-game analysis over agent populations, combined with Shapley-based credit decomposition, provides an alternative evaluation framework. SLS serves as the prototype environment for developing and validating this methodology.

**Bridge to Step 13:** The coalition detection mechanisms developed here directly transfer to collusion detection in real-world multiplayer poker data (Playtech), connecting theoretical coalition analysis to practical fraud detection (Contribution #3).

**Bridge to Step 14:** The N-player EGTA evaluation framework prototyped here extends into the formal evaluation methodology of Step 14, addressing the challenge of evaluating agents in non-stationary, multi-player environments.

---

## Expected Outputs

1. Verified SLS environment with correct game mechanics and endgame analysis validation
2. Coalition detection module inferring implicit alliances from behavioral observation sequences
3. Shapley credit assignment implementation adapted for competitive FFA games
4. Coalition-aware MAPPO agents trained via self-play with Shapley-decomposed rewards
5. EGTA meta-game analysis (4-player payoff tensor, meta-Nash computation)
6. Spinning top decomposition measuring non-transitive structure of SLS coalition dynamics
7. Comparative analysis: coalition-aware vs sparse-reward agents on SLS
8. Coalition dynamics visualizations (formation/dissolution timelines, Shapley attribution plots)
9. One-page summary document
10. Updated learning log with cross-step connections, thesis gap crystallization, and open research questions
