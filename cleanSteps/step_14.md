# Step 14 — Evaluation Frameworks + Exploitability Metrics

**Duration:** 14 days · **Phase G:** Integration · **Depends on:** Steps 8 (Safe Exploitation), 11 (Coalition Formation), 13 (Behavioral Analysis)

---

## Objective

Design and implement a unified three-layer evaluation framework for game-playing agents: (1) single-agent exploitability, (2) population-level ranking, and (3) statistical confidence with variance reduction. Validate the framework across multiple game types (2-player poker, N-player coalition games, real-world behavioral data) to produce domain-agnostic evaluation methodology.

**Core questions:**
1. How can we measure agent quality beyond simple win rates, accounting for intransitive competitive dynamics?
2. When do game-theoretic ranking methods (α-Rank, VasE) produce different rankings than Elo, and what does this reveal about the game's structure?
3. How many evaluation games are needed for confident agent rankings in imperfect-information settings?

---

## Literature

### Core

1. **Timbers, Bard, Lockhart, Lanctot, Schmid, Burch, Schrittwieser, Hubert & Bowling** (2022). "Approximate Exploitability: Learning a Best Response in Large Games." *arXiv:2004.09677*.
   - Introduces ISMCTS-BR for scalable exploitability approximation via learned best responses.
   - **Relevance:** Bridge from exact exploitability (Steps 3, 8) to approximate evaluation on larger games.

2. **Lanctot, Larson, Bachrach, Marris, Li, Bhoopchand, Anthony, Tanner & Koop** (2023/2025). "Evaluating Agents using Social Choice Theory." *arXiv:2312.03121*.
   - VasE framework: frames evaluation as voting, identifies maximal lotteries as axiomatically grounded ranking. More robust than Elo and Nash averaging.
   - **Relevance:** Freshest principled approach to multi-agent evaluation. Candidate backbone for Contribution #3.

3. **Rowland, Omidshafiei, Tuyls, Perolat, Valko, Piliouras & Munos** (2019). "Multiagent Evaluation under Incomplete Information." *arXiv:1909.09849*.
   - Derives sample complexity for confident agent ranking under noisy game outcomes. Adaptive evaluation algorithms.
   - **Relevance:** Provides the statistical confidence layer — essential for evaluation with stochastic games.

4. **Burch, Johanson & Bowling** (2019). "AIVAT: A New Variance Reduction Technique for Agent Evaluation in Imperfect Information Games." *AAAI*.
   - Unbiased, low-variance estimator using counterfactual value functions as control variates.
   - **Relevance:** Essential for poker evaluation; reduces required evaluation hands by 10–100×.

5. **Omidshafiei, Papadimitriou, Piliouras, Tuyls et al.** (2019). "α-Rank: Multi-Agent Evaluation by Evolution." *Nature Scientific Reports*.
   - Uses Markov-Conley chains from evolutionary dynamics for tractable game-theoretic ranking beyond Elo.
   - **Relevance:** Established standard for multi-agent evaluation; handles intransitivity.

### Supplementary

6. **Balduzzi, Tuyls et al.** (2019). "Re-evaluating Evaluation." *NeurIPS*.
   - Spinning top decomposition: payoff matrix = transitive + cyclic components. Studied in Step 10.
   - **Relevance:** Diagnostic tool for evaluation — transitive ratio indicates when Elo suffices vs. when game-theoretic methods are needed.

7. **Tuyls, Pérolat, Lanctot et al.** (2018). "A Generalised Method for Empirical Game Theoretic Analysis." *AAMAS*.
   - EGTA framework for analyzing multi-agent systems as meta-games. Studied in Step 10.
   - **Relevance:** Provides meta-Nash computation as a population-level evaluation metric.

8. **Martin & Sandholm** (2023/2024). "ApproxED: Approximate Exploitability Descent via Learned Best Responses." *AAMAS 2025*. arXiv:2301.08830.
   - Learned best-response functions for exploitability minimization in continuous-action games.
   - **Relevance:** Adversarial training approach to exploitability — potential extension for approximate evaluation.

9. **Ge, Liu, Zhang, Li, Chen, An & Wang** (2024). "Safe and Robust Subgame Exploitation in Imperfect Information Games." *ICML*.
   - Adaptation Safety: exploitation strategy is safe if no more exploitable than baseline. Already studied in Step 8.
   - **Relevance:** Adaptation safety as an exploitability-based evaluation criterion.

---

## Methodology

### 1. Evaluation Framework Design (Days 1–2)

- **Audit:** Inventory all evaluation code from prior steps (exploitability from Steps 3/8, EGTA + spinning top from Step 10, Elo tracking, SLS metrics from Step 11, behavioral metrics from Step 13).
- **Three-layer API:**
  - **Layer 1 — Exploitability:** Exact computation for small games via game tree traversal; approximate computation for large games via RL-based best response. Adaptation safety (Ge et al.) as a secondary metric.
  - **Layer 2 — Population ranking:** Elo (baseline), α-Rank (evolutionary dynamics), VasE/maximal lotteries (social choice theory), meta-Nash (EGTA). Spinning top decomposition as diagnostic.
  - **Layer 3 — Statistical confidence:** AIVAT variance reduction for imperfect-information games; bootstrapped confidence intervals; sample complexity bounds (Rowland et al.).
- **Bot zoo:** Construct reference agent collections for Kuhn and Leduc covering four tiers: trivial (random, always-call, always-fold), heuristic (tight-aggressive, loose-aggressive, tight-passive), computed (Nash/CFR, DQN), advanced (PSRO, Decision Transformer).

### 2. Metric Implementation (Days 2–4)

- **α-Rank:** Markov chain construction with Fermi selection function; stationary distribution via eigenvalue decomposition; sensitivity analysis across selection pressure α.
- **VasE:** Tournament matrix from pairwise comparisons across games; maximal lottery via LP solving; intransitive cycle detection.
- **AIVAT:** Control variate from CFR value function; counterfactual adjustment per chance node; variance reduction measurement.

### 3. Cross-Game Validation (Days 5–6)

- **Kuhn poker:** Full evaluation (all layers, all bot zoo agents). Gold standard — exact exploitability available.
- **Leduc poker:** Full evaluation. Approximate exploitability compared with exact.
- **So Long Sucker (Step 11):** N-player extension using marginal exploitability. α-Rank and VasE on SLS meta-game.
- **Playtech data (Step 13):** AIVAT applied to behavioral analysis. Confidence intervals for style classification and collusion detection.
- **Comparison:** Elo vs α-Rank vs VasE disagreement analysis. Spinning top diagnostic to explain disagreements.

---

## Expected Outcomes

1. Unified evaluation framework API covering exploitability, population ranking, and statistical confidence.
2. Empirical comparison of ranking methods: cases where Elo, α-Rank, and VasE produce different orderings, explained by competitive structure (transitive vs cyclic).
3. AIVAT variance reduction of ≥5× on Kuhn and ≥10× on Leduc relative to raw evaluation.
4. Cross-game evaluation table demonstrating framework generality across 2-player, N-player, and real-world data settings.
5. N-player exploitability extension (marginal exploitability) applied to SLS coalition dynamics.

---

## Connections

- **From Step 3:** CFR exploitability tracking generalizes into Layer 1; CFR value function enables AIVAT.
- **From Step 8:** Exploitability computation and adaptation safety integrate into the framework; exploitation-safety Pareto frontier becomes an evaluation artifact.
- **From Step 10:** EGTA meta-Nash, spinning top decomposition, and Elo tracking integrate as Layer 2 modules.
- **From Step 11:** SLS provides the N-player test case; help/harm matrices provide ground truth for coalition-aware evaluation.
- **From Step 13:** Playtech behavioral data provides real-world validation; AIVAT essential for noisy poker evaluation.
- **To Step 15:** The evaluation framework determines what can be rigorously evaluated and therefore claimed as thesis contributions.

---

## PhD Mapping

- **Contribution 3 (Evaluation Methodology):** This step IS Contribution #3 — a three-layer evaluation framework (exploitability + population ranking + statistical confidence) validated across multiple game types. The axiomatic grounding from VasE (social choice theory) and the variance reduction from AIVAT provide principled justification for evaluation choices.
- **Contribution 1 (Behavioral Adaptation):** The framework measures whether behavioral adaptation (Steps 7–8) works: does the adapting agent's exploitability decrease? Does its population ranking improve? With what confidence?
- **Contribution 2 (Multi-Agent Safe Exploitation):** The N-player extension tests whether 2-player safe exploitation generalizes. Marginal exploitability and coalition-aware metrics detect gaps between theory and multi-agent reality.
- **Publication integration:** Combined with Step 13's Playtech data, the evaluation framework strengthens the first publication: methodology (three-layer evaluation) + application (poker behavioral data) + validation (cross-game generality).
