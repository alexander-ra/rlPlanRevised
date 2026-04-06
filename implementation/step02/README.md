# Step 02 — Game Theory & CFR Basics: Implementation

**PhD Context:** This step is part of the official research program:
- **EN:** Research on the possibilities for applying Artificial Intelligence in computer games
- **BG:** Изследване на възможностите за приложение на изкуствения интелект в компютърни игри

Vanilla Counterfactual Regret Minimization (CFR) for Kuhn Poker — Nash equilibrium solver, best response, exploitability analysis.

> **Environment setup:** See the [project-level README](../../README.md#python-environment-setup).
> The project uses a single `.venv` at the repository root shared across all steps.

## Structure

```
step02/
├── cfr/
│   ├── kuhn_poker.py        # 🔴 HAND-CODE: Game engine (cards, actions, terminal payoffs)
│   ├── info_set_node.py     # 🔴 HAND-CODE: Information set node (regret matching)
│   ├── cfr_trainer.py       # 🔴 HAND-CODE: Recursive CFR traversal + training loop
│   └── train.py             # Training orchestration for CFR on Kuhn Poker
├── evaluate/
│   ├── best_response.py     # 🔴 HAND-CODE: Best response calculator (tree traversal)
│   ├── exploitability.py    # 🔴 HAND-CODE: Exploitability = BR₁(σ₂) + BR₂(σ₁)
│   └── convergence.py       # Convergence analysis (exploitability vs iterations)
├── utils/
│   ├── logger.py            # 🟢 AI-GENERATED: JSON-based training logger
│   └── plotting.py          # 🟢 AI-GENERATED: Strategy charts, convergence plots
├── config.py                # CFR hyperparameters
├── compare_openspiel.py     # Cross-verification vs OpenSpiel + analytical Nash
└── verify_setup.py          # Dependency verification
```

## Reference

Based on pseudocode from:
> Neller, T.W. & Lanctot, M. (2013). "An Introduction to Counterfactual Regret Minimization"

Original paper:
> Zinkevich, M. et al. (2007). "Regret Minimization in Games with Incomplete Information"

## Targets

- **Nash strategies:** Match known equilibrium to 4 decimal places after 50k iterations
  - P1 with J: bet ≈ 1/3 (bluff threshold)
  - P1 with K: bet ≈ 1.0 (always bet)
  - P1 with Q: bet ≈ 0.0 (always check)
- **Game value:** Player 1 expected payoff ≈ -1/18 ≈ -0.0556
- **Exploitability:** Decreases at O(1/√T) rate (log-log slope ≈ -0.5)

## Quick Start

```bash
# From implementation/step02/
python verify_setup.py                       # check dependencies
python cfr/train.py                          # train CFR (100k iterations)
python cfr/train.py --iterations 50000       # custom iteration count
python evaluate/exploitability.py            # compute exploitability
python evaluate/convergence.py               # convergence analysis + plot
python compare_openspiel.py                  # compare vs OpenSpiel & analytical Nash
```

## Implementation Plan (6 days)

### Day 1 — Architecture + Game Engine
- Design module interfaces (information set node, trainer, evaluator)
- Implement Kuhn Poker game engine: card representation, info sets, terminal payoffs
- Test: verify all 12 deals × action sequences produce correct game tree

### Days 2–3 — CFR Core Algorithm
- Implement recursive CFR traversal + regret matching
- Implement strategy accumulation weighted by reach probability
- Train for 10,000+ iterations, verify strategy output matches known Nash

### Days 4–5 — Exploitability + Best Response
- Implement best response: given opponent strategy, compute optimal counter
- Implement exploitability metric: exploit(σ) = BR₁(σ₂) + BR₂(σ₁)
- Generate convergence plot (log-log): exploitability vs iterations
- Verify O(1/√T) convergence rate (slope ≈ -0.5)

### Day 6 — Validation + Cross-Verification
- Compare Nash strategies vs analytical solution (4 decimal places)
- Compare output vs OpenSpiel's CFR (if installed)
- Generate all figures for deliverables

## Debugging Tips

| Symptom | Likely Cause |
|---------|-------------|
| Game value far from -1/18 | Check terminal payoff signs and player alternation |
| Strategies all uniform | Regret update missing or using wrong reach probability |
| Exploitability not decreasing | Strategy accumulation not weighted by reach probability |
| P1 with K not betting ~100% | Not enough iterations, or regret matching fallback broken |
| OpenSpiel comparison: large delta | Check info set string mapping (card numbering differs) |
