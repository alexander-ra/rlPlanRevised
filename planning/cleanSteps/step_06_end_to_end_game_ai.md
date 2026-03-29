# Step 6 — End-to-End Game AI Architectures

**Duration:** 21 days  
**Prerequisites:** Step 3 (CFR Variants & Monte Carlo Methods), Step 4 (Game Abstraction & Scaling), Step 5 (Neural Equilibrium Approximation)  
**Phase:** C — Neural Methods for Games

---

## Formal Objectives

1. Study the architectural evolution of superhuman game-playing AI systems, from modular pipeline designs (DeepStack, Libratus) through multi-player extensions (Pluribus) to unified learning-and-search frameworks (ReBeL, Student of Games).
2. Understand Public Belief States (PBS) as the foundational state representation enabling search in imperfect-information games, including their formal definition, Bayesian update mechanics, and role in convergence guarantees.
3. Analyse depth-limited solving as the unifying theoretical concept across all five architectures, with emphasis on error propagation bounds and their implications for strategy safety.
4. Implement a simplified ReBeL system (ReBeL-Lite) for Leduc Hold'em, integrating PBS representation, local CFR solving, and neural value estimation into a self-play training loop.
5. Construct a comparative analysis framework mapping architectural innovations across all five systems, identifying component reuse from Steps 3–5 and open research gaps relevant to the thesis.

---

## Literature

### Core References

1. **Moravcik, M., Schmid, M., Burch, N., Lisý, V., Morrill, D., Bard, N., Davis, T., Waugh, K., Johanson, M. & Bowling, M.** (2017). DeepStack: Expert-Level Artificial Intelligence in Heads-Up No-Limit Poker. *Science*, 356(6337), 508–513. https://arxiv.org/abs/1701.01724  
   *Introduces continual re-solving with deep counterfactual value networks — online game solving without pre-computed blueprints.*

2. **Brown, N. & Sandholm, T.** (2018). Superhuman AI for Heads-Up No-Limit Poker: Libratus Beats Top Professionals. *Science*, 359(6374), 418–424.  
   *Three-module architecture: abstracted MCCFR blueprint + real-time subgame solving + self-improvement. First AI to defeat top professionals in HUNL.*

3. **Brown, N. & Sandholm, T.** (2019). Superhuman AI for Multiplayer Poker. *Science*, 365(6456), 885–890. https://arxiv.org/abs/1911.07559  
   *Extends game-solving to six-player no-limit Hold'em. MCCFR blueprint with depth-limited real-time search. Demonstrates empirical effectiveness of Nash-based approaches in multiplayer settings lacking theoretical equilibrium guarantees.*

4. **Brown, N., Bakhtin, A., Lerer, A. & Hu, Q.** (2020). Combining Deep Reinforcement Learning and Search for Imperfect-Information Games. In *Advances in Neural Information Processing Systems (NeurIPS)*. https://arxiv.org/abs/2007.13544  
   *Introduces ReBeL — the Public Belief State (PBS) framework enabling AlphaZero-style self-play and search for imperfect-information games. Eliminates the need for abstraction or pre-computed blueprints.*

5. **Schmid, M., Moravcik, M., Burch, N., Kadlec, R., Davidson, J., Waugh, K., Bard, N., Timbers, F., Lanctot, M., Holland, G.Z., Davoodi, E., Christianson, A. & Bowling, M.** (2023). Student of Games: A Unified Learning Algorithm for Both Perfect and Imperfect Information Games. *Science Advances*, 9(46). https://arxiv.org/abs/2112.03178  
   *Proposes Growing-Tree CFR (GT-CFR) — a unified algorithm handling both perfect-information (Go, chess) and imperfect-information (poker) games within a single framework. Combines value and policy networks with incremental tree growth.*

6. **Brown, N. & Sandholm, T.** (2018). Depth-Limited Solving for Imperfect-Information Games. In *Advances in Neural Information Processing Systems (NeurIPS)*. https://arxiv.org/abs/1805.08195  
   *Establishes the theoretical foundation for depth-limited search in imperfect-information games, including exploitability bounds for value estimation errors at the depth limit. Fundamental to all five architectures studied.*

### Supplementary References

7. **Milec, D., Kovařík, V. & Lisý, V.** (2025). Adapting Beyond the Depth Limit: Counter Strategies in Large Imperfect Information Games. https://arxiv.org/abs/2501.10464  
   *Studies opponent adaptation beyond the depth limit in large IIGs — directly relevant to the thesis's safe exploitation contribution and the bridge from architecture to adaptation.*

8. **Kubíček, J. & Lisý, V.** (2023/2025). Look-ahead Search on Top of Policy Networks in Imperfect Information Games. https://arxiv.org/abs/2312.15220  
   *Explores test-time search augmentation of policy networks in imperfect-information settings.*

9. **Zhang, Z., Zheng, S., Guo, W. & Li, K.** (2026). Faster Game Solving via Hyperparameter Schedules. In *Proceedings of the AAAI Conference on Artificial Intelligence*.  
   *Optimization of the solving process through adaptive hyperparameter scheduling.*

---

## Methodology

### Phase 1 — Orientation (Days 1–2)
Survey the five core architectures through author-presented talks and accessible publications. Construct architecture diagrams for each system identifying offline vs. online components, the role of neural networks, search mechanisms, and the relationship to prior step content (MCCFR from Step 3, abstraction from Step 4, neural estimation from Step 5).

### Phase 2 — Exploration (Days 3–4)
Map component-level similarities and differences across architectures through structured comparison. Run available open-source implementations (OpenSpiel) on Leduc and Liar's Dice to observe training dynamics and computational requirements. Identify the Public Belief State (PBS) as the key representational innovation distinguishing ReBeL/SoG from earlier systems.

### Phase 3 — Literature Study (Days 5–8)
Close reading of all six core papers with emphasis on:
- **Moravcik et al.** — continual re-solving, deep counterfactual value networks (Sections 2–3)
- **Brown & Sandholm (Libratus)** — modular architecture: blueprint + subgame solving + self-improvement
- **Brown & Sandholm (Pluribus)** — multiplayer adaptation: depth-limited search, modified RBP, empirical treatment of multiplayer equilibrium
- **Brown et al. (ReBeL)** — Public Belief State definition, soundness theorem for PBS search, self-play training loop
- **Schmid et al. (SoG)** — Growing-Tree CFR algorithm, convergence guarantee, unification of perfect and imperfect information
- **Brown & Sandholm (Depth-Limited Solving)** — exploitability bound for depth-limited strategies, error propagation from value estimates

Critical mathematical content: PBS formal definition (ReBeL, Definition 1), depth-limited exploitability bound (Brown & Sandholm 2018, Theorem 1), GT-CFR convergence (Schmid et al., Theorem 1).

### Phase 4 — Implementation (Days 9–18)
Implement a simplified ReBeL system (ReBeL-Lite) for Leduc Hold'em:
1. **PBS representation** — probability distributions over private information assignments with Bayesian update on observed actions
2. **PBS-CFR** — local CFR solver operating on arbitrary belief states (adapting Step 3 CFR to work within depth-limited search)
3. **PBS value network** — MLP predicting expected value from PBS tensor, trained on CFR solutions
4. **ReBeL training loop** — self-play generating PBS-CFR solutions → value network training → improved search → iteration

Construct architecture comparison framework: feature comparison table, evolutionary diagram, and component reuse analysis mapping Steps 3–5 building blocks across all five systems.

### Phase 5 — Consolidation (Days 19–21)
Synthesise findings into an architecture evolution essay tracing the progression from abstraction-based offline computation to neural-approximation-based learning-and-search. Map each architecture to thesis contributions:
- **Contribution 1 (Behavioral Adaptation):** ReBeL's PBS as starting point for belief-based opponent modelling; extension to include beliefs about opponent strategy types.
- **Contribution 2 (Multi-Agent Safe Exploitation):** Pluribus's empirical success without multiplayer safety guarantees identifies the theoretical gap this thesis addresses.
- **Contribution 3 (Evaluation Methodology):** Exploitability as universal evaluation metric across all architectures.

Update learning log with cross-step connections and newly identified research questions.

---

## Expected Outputs

- Working ReBeL-Lite implementation for Leduc Hold'em demonstrating decreasing exploitability across training iterations
- PBS representation module with verified Bayesian update logic
- Architecture comparison table and evolutionary analysis covering all five systems
- One-page summary document (per Section 4.7 of the plan architecture)
- Updated learning log with connections to Steps 1–5 and thesis contribution mapping

---

## PhD Alignment

This step establishes the architectural foundation for the entire thesis. The five systems studied represent the state of the art in game-solving AI, and each thesis contribution directly extends one of the open problems identified:

- **Contribution 1** extends ReBeL's PBS framework to incorporate strategic beliefs about opponent types — creating a richer state representation for adaptive play.
- **Contribution 2** addresses Pluribus's demonstrated gap: Nash-based approaches work empirically for N-player games but lack formal safety guarantees. The depth-limited solving bounds from Brown & Sandholm (2018) and the opponent adaptation analysis from Milec et al. (2025) provide the theoretical starting point.
- **Contribution 3** builds on the exploitability metric used universally across all five architectures, extending it into a comprehensive evaluation methodology for adaptive agents in multi-player settings.

