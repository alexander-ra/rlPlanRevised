<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->

# Chapter 02 — Game Theory & CFR Basics: Implementation Report

**Environment:** April 2026  
**Game:** Kuhn Poker (3-card, 2-player)  
**Algorithm:** Counterfactual Regret Minimization (CFR) with chance sampling  
**Targets:** Nash strategies to 4 decimal places, game value ≈ −1/18, exploitability O(1/√T)  
**Status:** Game-value and convergence-rate targets met; mixed frequencies within 0.005–0.038 of the closed form (4-decimal accuracy reached only for the King's and the Jack's pure decisions)

---

## 1. What was developed

Chapter 02 implements a modular version of Counterfactual Regret Minimization (CFR) with chance sampling, applied to Kuhn Poker, written from scratch in Python. It proves that the framework successfully discovers Nash equilibrium strategies in a multi-agent, imperfect-information environment.

**Key Components Built:**
- **Game Engine:** `kuhn_poker.py` handles terminal payoffs, betting actions, and info-set representations.
- **CFR Core Algorithm:** Recursive tree traversal with Chance Sampling and Regret Matching (`cfr_trainer.py`, `info_set_node.py`).
- **Exploitability & Best Response Evaluator:** Brute-force pure strategy aggregation to calculate exact exploitability (`evaluate/best_response.py`, `evaluate/exploitability.py`).
- **Convergence Logger & Visualizations:** Utilities to plot exploitability and strategy convergence metrics over iterations (`utils/plotting.py`, `evaluate/convergence.py`).
- **OpenSpiel Cross-Verification:** Check against standard open-source libraries (`compare_openspiel.py`).

## 2. Key Results and Visualizations

- **Minimax Optimal Convergence:** The algorithm converged to within 0.038 of the analytical Nash equilibrium family (parameterized by α); the exploitability of the average strategy after 100,000 iterations is 0.006.
- **Exploitability Decay Rate:** The log-log slope for exploitability over iterations is −0.52 ± 0.02 (5 seeds, 100–100,000 iterations), consistent with the theoretical O(1/√T) bound.
- **Game Value Accuracy:** After 100,000 iterations, the exact value of the average strategy (−0.0555) matches the theoretical value −1/18 (−0.0556) to within 8·10⁻⁵; the running mean of the sampled payoffs is −0.0613.

### Game Value Convergence
![Game Value Convergence](figures/game_value_convergence.png)

### Exploitability Convergence
![Exploitability Convergence](figures/exploitability_convergence.png)

### Strategy Analysis
![Strategy Analysis](figures/strategy_analysis.png)
