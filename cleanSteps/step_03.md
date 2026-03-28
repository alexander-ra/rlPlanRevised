# Step 3 — CFR Variants + Monte Carlo Methods

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 2 (Game Theory + CFR Basics)  
**Phase:** B — Scaling the Toolbox

---

## Objectives

Extend the foundational CFR knowledge from Step 2 to scalable variants suitable for larger games:

1. Understand Monte Carlo Counterfactual Regret Minimization (MCCFR) and its sampling schemes (external, outcome, chance)
2. Learn CFR+ and the modifications that achieve faster empirical convergence
3. Implement MCCFR and CFR+ from scratch on a larger benchmark game (Leduc Hold'em)
4. Develop quantitative understanding of the convergence-speed vs. variance tradeoff across CFR variants

---

## Literature

### Papers

1. **Lanctot, M., Waugh, K., Zinkevich, M. & Bowling, M. (2009).** "Monte Carlo Sampling for Regret Minimization in Extensive Games." *Advances in Neural Information Processing Systems 22 (NeurIPS).*  
   Available: http://mlanctot.info/files/papers/nips09mccfr.pdf  
   *Introduces the MCCFR framework unifying external sampling, outcome sampling, and chance sampling as instantiations of a single sampling scheme with convergence guarantees.*

2. **Tammelin, O., Burch, N., Johanson, M. & Bowling, M. (2015).** "Solving Heads-Up Limit Texas Hold'em." *Proceedings of the 24th International Joint Conference on Artificial Intelligence (IJCAI).*  
   arXiv: https://arxiv.org/abs/1407.5042  
   *Introduces CFR+ — three modifications to vanilla CFR (regret floor, alternating updates, linear averaging) that yield empirically $O(1/T)$ convergence, enabling the first essentially complete solution of Heads-Up Limit Hold'em.*

### Textbook

3. **Chen, B. & Ankenman, J. (2006).** *The Mathematics of Poker.* ConJelCo.  
   Chapters 1–8: Expected value, pot odds, game-theoretic optimal play, exploitation theory.  
   *Provides domain-specific mathematical vocabulary connecting CFR outputs to poker strategic concepts.*

### Supplementary References

4. **Schmid, M., Burch, N., Lanctot, M., Moravcik, M., Kadlec, R. & Bowling, M. (2018).** "Variance Reduction in Monte Carlo Counterfactual Regret Minimization (VR-MCCFR) for Extensive Form Games using Baselines."  
   arXiv: https://arxiv.org/abs/1809.03057  
   *Baseline subtraction techniques for reducing MCCFR sampling variance. Bridges to neural function approximation in Step 5.*

---

## Methodology

### Phase 1: Conceptual Foundation (1 day)

Survey of the motivation for scalable CFR variants: computational bottleneck of full tree traversal in vanilla CFR, the sampling principle in MCCFR, and the convergence acceleration in CFR+. Establish understanding of the core tradeoff between per-iteration cost and convergence variance.

### Phase 2: Empirical Familiarization (2 days)

Hands-on experimentation using OpenSpiel's MCCFR and CFR+ implementations:
- Comparative convergence analysis on Kuhn Poker: vanilla CFR vs. external-sampling MCCFR vs. CFR+
- Introduction to Leduc Hold'em as a larger benchmark (~936 information sets vs. Kuhn's ~12)
- Measurement of both iteration-count efficiency and wall-clock efficiency across variants
- Exploration of different sampling schemes and their convergence behaviors

### Phase 3: Literature Study (3 days)

Structured reading of three sources:

1. **Lanctot et al. (2009):** MCCFR framework — the unifying sampling formulation, external vs. outcome sampling tradeoffs, convergence guarantees under sampling. Focus on the unbiased estimation theorem (sampled counterfactual values are unbiased estimates of full-traversal values).

2. **Tammelin et al. (2015):** CFR+ — the three modifications (regret floor at zero, alternating player updates, linear iteration weighting) and their combined effect on convergence speed. Focus on the algorithmic description and the HULHE results.

3. **Chen & Ankenman (2006), Chapters 1–8:** Game-theoretic optimal play and exploitation theory in poker. Provides the domain vocabulary connecting equilibrium computation to strategic concepts.

### Phase 4: Implementation (6 days)

From-scratch implementation in Python (NumPy only):

**Leduc Hold'em** (6-card deck, 2 rounds, 1 community card) serves as the step-up benchmark — large enough that vanilla CFR becomes noticeably slow, motivating the need for MCCFR and CFR+.

| Implementation | Games | Validation Criterion |
|----------------|-------|---------------------|
| Leduc Hold'em game engine | — | Correct game tree with ~936 information sets |
| External-sampling MCCFR | Kuhn + Leduc | Convergence to same Nash as vanilla CFR; lower wall time for equivalent exploitability |
| Outcome-sampling MCCFR | Leduc | Convergence with importance weighting; higher variance than external sampling |
| CFR+ | Kuhn + Leduc | ~10x faster convergence than vanilla CFR on Kuhn; $O(1/T)$ rate on log-log plot |

**Validation approach:** Four-way convergence comparison across variants (exploitability vs. iterations and vs. wall time). Cross-validation against OpenSpiel reference implementations at multiple iteration checkpoints.

### Phase 5: Synthesis (2 days)

Consolidation of theoretical and practical knowledge:
- Connection mapping: MCCFR's sampling principle ↔ Step 1's Monte Carlo methods (S&B Ch 5)
- Forward connection: variance reduction in MCCFR ↔ Deep CFR's neural approximation (Step 5)
- Analysis of which variant is optimal for which game sizes
- Documentation of step summary and learning log updates

---

## Deliverables

1. **Leduc Hold'em game engine** with complete game tree handling
2. **External-sampling MCCFR solver** converging on both Kuhn and Leduc
3. **Outcome-sampling MCCFR solver** converging on Leduc
4. **CFR+ solver** converging on Kuhn and Leduc with demonstrably faster convergence
5. **Four-way convergence comparison** — exploitability vs. iterations and wall time for all variants
6. **Step summary** connecting CFR variants to the broader algorithmic progression

---

## PhD Contribution Alignment

| Concept | Downstream Application |
|---------|----------------------|
| MCCFR | Blueprint computation for the baseline Nash strategy in the behavioral adaptation framework (Contribution #1) |
| CFR+ convergence acceleration | Tractable equilibrium computation for real-sized games (Contributions #1, #2) |
| Sampling scheme tradeoffs | Informs design choices for scalable opponent modeling (Contribution #1, Step 7) |
| Leduc Hold'em benchmark | Intermediate evaluation environment used in Steps 5–8 before scaling to full poker |

---

## Exit Criteria

- [ ] All four CFR variants produce convergent strategies on Leduc, cross-validated against OpenSpiel
- [ ] CFR+ demonstrates faster convergence than vanilla CFR (empirical $O(1/T)$ vs. $O(1/\sqrt{T})$)
- [ ] Ability to explain MCCFR sampling schemes and CFR+ modifications from memory
- [ ] Understanding of convergence-variance tradeoff across sampling strategies
- [ ] Step summary completed and committed to repository
- [ ] Connections to Steps 1–2 and forward to Steps 5–6 identified and documented
