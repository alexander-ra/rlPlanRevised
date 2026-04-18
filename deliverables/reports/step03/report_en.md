<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->

# Step 03 — CFR Variants & Monte Carlo Methods: Implementation Report

## 1. Introduction
This report documents the exploration of Monte Carlo Tree Search (MCTS) and Advanced Counterfactual Regret Minimization (CFR) variants applied to Leduc Poker.

## 2. Background Concepts
- **MCTS**: Heuristic search algorithm for some kinds of decision processes, most notably employed in game play.
- **MCTS vs Minimax**: MCTS builds an asymmetric tree focusing on promising branches, while Minimax explores all branches up to a depth limit.
- **Markov Chains**: Stochastic models describing a sequence of possible events.
- **Poker Math**: Exploiting probabilities, combinatorics, and expected value.
- **Leduc vs Kuhn**: Leduc has a 6-card deck with community cards, making it vastly larger than Kuhn.

## 3. Algorithm Descriptions
- **CFR+**: Regret Matching Plus, introduces alternating updates and floor operations.
- **MCCFR External**: Samples opponent chance and action nodes, traverses all player actions.
- **MCCFR Outcome**: Traverses only a single sampled trajectory per iteration.

## 4. Exploration Phase
We implemented `implDayOne1_test.py` to compare Vanilla and CFR+ exploitability.

## 5. Timed Run Results
Results demonstrate CFR+ reaches the required target exploitability within constraints.

## 6. Convergence Analysis (vs OpenSpiel)
The empirical data accurately matches baseline expectations defined by OpenSpiel.

## 7. Conclusion and Next Steps
Moving ahead to Step 04 for game abstraction.
