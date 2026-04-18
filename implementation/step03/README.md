# Step 03 — CFR Variants & Monte Carlo Methods: Implementation

**PhD Context:** This step is part of the official research program:
- **EN:** Research on the possibilities for applying Artificial Intelligence in computer games
- **BG:** Изследване на възможностите за приложение на изкуствения интелект в компютърни игри

Complete implementation and experimental comparison of four Counterfactual Regret Minimization (CFR) variants on Leduc Poker: Vanilla CFR, CFR+ (linear regret weighting), MCCFR External Sampling, and MCCFR Outcome Sampling. This step includes empirical convergence analysis with mathematical justification for why full-traversal methods dominate sampling-based approaches on small games.

> **Environment setup:** See the [project-level README](../../README.md#python-environment-setup).
> The project uses a single `.venv` at the repository root shared across all steps.

## Structure

```
step03/
├── cfr/
│   ├── leduc_poker.py           # 🔴 HAND-CODE: Leduc Poker game engine
│   ├── info_set_node.py         # 🔴 HAND-CODE: Regret-matching node (game-agnostic)
│   ├── cfr_trainer.py           # 🔴 HAND-CODE: Vanilla CFR full-traversal with buffered regrets
│   ├── cfrplus_trainer.py       # 🔴 HAND-CODE: CFR+ (Tammelin 2014) with linear regret weighting
│   ├── mccfr_external_trainer.py # 🔴 HAND-CODE: MCCFR External Sampling variant
│   ├── mccfr_outcome_trainer.py # 🔴 HAND-CODE: MCCFR Outcome Sampling variant
│   ├── train.py                 # Individual algorithm trainer (vanilla/external/outcome)
│   └── train_all_timed.py       # Comprehensive 4-algorithm benchmark with wall-clock timing
├── evaluate/
│   ├── best_response.py         # 🔴 HAND-CODE: Iterative info-set-constrained best response
│   ├── exploitability.py        # 🔴 HAND-CODE: Exploitability = (BR₀(σ₁) + BR₁(σ₀))/2
│   └── convergence.py           # Convergence diagnostics and export
├── utils/
│   ├── logger.py                # 🟢 AI-GENERATED: JSON-based training logger
│   └── plotting.py              # 🟢 AI-GENERATED: Convergence curves, strategy heatmaps
├── figures/                     # Generated convergence plots and comparison charts
├── models/                      # Saved strategy snapshots (JSON)
├── logs/                        # Training event logs (JSON)
├── tests/                       # Unit tests for game rules and CFR correctness
├── config.py                    # Hyperparameters and algorithm settings
├── compare_openspiel.py         # Cross-verification against OpenSpiel CFR and CFR+
├── verify_setup.py              # Dependency and environment verification
├── convergence_analysis.md      # Theoretical analysis: why MCCFR is slower on small games
├── exploration/                 # Exploratory experiments (variance analysis, MC simulation)
└── guidance/                    # Reference materials and tutorials
```

## Leduc Poker: Game Specification

| Property | Value |
|----------|-------|
| **Cards** | 6 (ranks {J, Q, K} × suits {♠, ♥}) |
| **Structure** | 2 players, 2 betting rounds, 1 community card revealed between rounds |
| **Antes** | 1 chip each |
| **Bet sizes** | Round 1: +2, Round 2: +4 |
| **Raises** | Up to 2 per round |
| **Hand ranking** | Pair (private == community) beats high card; higher rank wins |
| **Game tree** | 120 chance outcomes (deals), 10,200 nodes total, 936 information sets |
| **Depth** | Min 2, max 8, average 5.47 |
| **Nodes per info set** | Average 10.9 |

## Algorithms Implemented

### 1. **Vanilla CFR** (Zinkevich et al. 2007)
- **Method:** Full-traversal of entire game tree every iteration
- **Updates:** Buffered regret accumulation (atomic per 120-deal pass)
- **Convergence:** $O(1/\sqrt{T})$ with $C_v \approx 0.34$
- **Final exploitability (180s):** 0.0044 ± 0.0005

### 2. **CFR+** (Tammelin 2014)
- **Method:** Full-traversal with linear regret weighting
- **Updates:** Buffered regret accumulation with $\max(r + \Delta r, 0)$ flooring
- **Convergence:** $O(1/\sqrt{T})$ with $C_{cfr+} \approx 0.34$ (similar to vanilla in theory, but faster empirically)
- **Final exploitability (180s):** 0.000026 ± 0.000005

### 3. **MCCFR External Sampling** (Lanctot et al. 2009)
- **Method:** One sampled deal per iteration; opponent chance fixed, own chance sampled
- **Convergence:** $O(1/\sqrt{T})$ with $C_{ext} \approx 107$ (variance penalty for sampling)
- **Final exploitability (180s):** 0.0548 ± 0.0080
- **Iterations in 180s:** 3.5M (945x more than vanilla)

### 4. **MCCFR Outcome Sampling** (Lanctot et al. 2009)
- **Method:** One sampled deal and one sampled action path per iteration
- **Convergence:** $O(1/\sqrt{T})$ with $C_{out} \approx 245$ (highest variance among MCCFR variants)
- **Final exploitability (180s):** 0.1030 ± 0.0120
- **Iterations in 180s:** 8.3M (2,228x more than vanilla)

## Key Findings

1. **Full-traversal beats sampling on Leduc** — Despite running 1,000× more iterations, MCCFR External achieves 12× worse exploitability than Vanilla CFR.

2. **Why?** The variance penalty $\sigma^2 = (C_{mc}/C_v)^2$ dominates the speed advantage:
   - External: needs 315² ≈ 100,000× more iterations despite 945× faster per-iteration cost
   - Outcome: needs 721² ≈ 520,000× more iterations despite 2,228× faster per-iteration cost

3. **The crossover** — MCCFR becomes competitive (faster in wall-clock time) when the game tree exceeds ~2.1M nodes (External) or ~4.8M nodes (Outcome). Leduc is 210× too small for External, 466× too small for Outcome.

4. **Implication** — On real poker games (Texas Hold'em: $|N| \approx 10^{17}$), MCCFR is the only tractable approach. Full traversal's linear scaling with $|N|$ eventually loses to MC's constant per-iteration cost.

See [convergence_analysis.md](convergence_analysis.md) for detailed mathematical derivation and concrete predictions.

## Quick Start

```bash
# From implementation/step03/
python verify_setup.py                                # check dependencies

# Train individual algorithms
python cfr/train.py --iterations 1000                # Vanilla CFR
python cfr/train.py --algorithm cfrplus --iterations 1000  # CFR+
python cfr/train.py --algorithm mccfr_external       # MCCFR External
python cfr/train.py --algorithm mccfr_outcome        # MCCFR Outcome

# Comprehensive 180-second benchmark (all 4 algorithms with wall-clock timing)
python cfr/train_all_timed.py

# Generate convergence plots (requires ~30 min training)
python evaluate/convergence.py

# Cross-check against OpenSpiel
python compare_openspiel.py
```

## Convergence Analysis

The file [convergence_analysis.md](convergence_analysis.md) provides:

- **Section 1–5:** Experimental setup, definitions, per-iteration costs, wall-clock time analysis
- **Section 6:** Why the "sample size cancels" claim is incomplete (variance comes from deal sampling, not path sampling)
- **Section 7:** Derivation of the crossover formula and critical game tree size ($|N|_{crossover}$)
- **Section 8:** Summary with Texas Hold'em comparison
- **Appendix:** Empirical $C = \epsilon\sqrt{T}$ tables validating $O(1/\sqrt{T})$ convergence

## Validation

All implementations are cross-checked against OpenSpiel's reference implementations:

| Algorithm | Ours (500 iters) | OpenSpiel (500 iters) | Match |
|-----------|------:|------:|:-:|
| Vanilla CFR | 0.020 | 0.022 | ✅ |
| CFR+ | 0.00086 | 0.00094 | ✅ |

MCCFR variants are verified against OpenSpiel's structural design (regret accumulation, counterfactual values, empirical convergence rates).

## References

- **CFR:** Zinkevich, M., Bowling, M., Burch, N., Billings, D., & Larson, K. (2007). Regret Minimization in Games with Incomplete Information. IJCAI.
- **CFR+:** Tammelin, O. (2014). Solving Large Imperfect Information Games Using CFR+. AAAI.
- **MCCFR:** Lanctot, M., Gibson, R., Burch, N., Zinkevich, M., & Bowling, M. (2009). Monte Carlo Sampling for Regret Minimization in Extensive Games. NIPS.
- **Leduc Poker:** Southey, F., Bowling, M., Larson, B., Burch, C., Billings, D., & Rayner, C. (2005). Bayes' Bluff: Opponent Modelling in Poker. UAI.
