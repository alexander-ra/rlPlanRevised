# Step 8 — Safe Exploitation — Theory, Algorithms, and Real-Time Search

**Duration:** 21 days (Tier 1)  
**Dependencies:** Step 6 (End-to-End Game AI Architectures), Step 7 (Opponent Modeling)  
**Phase:** D — Opponent Modeling + Exploitation

---

## Objectives

Develop the theory and practice of safe exploitation — computing strategies that maximally exploit detected opponent weaknesses while maintaining provable safety guarantees:

1. Understand the exploitation-safety tradeoff: naive best-response exploitation is maximally profitable against the modeled opponent but catastrophically vulnerable to model error
2. Study the progression of safety notions from Restricted Nash Response (bounded deviation) to strict Nash safety (Ganzfried 2015) to $\varepsilon$-safety for approximate baselines (Jeary 2023) to adaptation safety (Ge 2024)
3. Learn subgame-based exploitation (SES, OX-Search) as the mechanism enabling real-time safe exploitation without full-game recomputation
4. Understand depth-limited exploitation (ABD) and why opponent model information beyond the search horizon requires fundamentally different techniques
5. Implement the complete safe exploitation pipeline — integrating Step 7 opponent models with multiple exploitation algorithms — and identify the precise failure point for extension to $N$-player games

---

## Literature

### Papers

1. **Johanson, M., Bowling, M. & Zinkevich, M. (2007).** "Computing Robust Counter-Strategies." *Advances in Neural Information Processing Systems (NIPS).* Also: AAMAS 2009 extended version.  
   Available: https://poker.cs.ualberta.ca/publications/AAMAS09-johanson.pdf  
   *Introduces the Restricted Nash Response (RNR) — the first principled safe exploitation framework. Formulates exploitation as a linear program: maximize expected value against the opponent model subject to an exploitability bound. The parameter $p \in [0,1]$ controls the Nash-to-best-response interpolation. Establishes the template that all subsequent safe exploitation algorithms refine.*

2. **Ganzfried, S. & Sandholm, T. (2015).** "Safe Opponent Exploitation." *ACM Transactions on Economics and Computation (TEAC), 3(2).*  
   Available: https://www.sganzfried.com/safe-exploitation.pdf  
   *Proves the foundational Safety Theorem: if the baseline $\sigma^*$ is a Nash equilibrium in a 2-player zero-sum game, then the safe exploitation strategy $\sigma_{SE}$ satisfies $v(\sigma_{SE}, \sigma') \geq v(\sigma^*, \sigma')$ for all opponent strategies $\sigma'$. The proof relies on the minimax theorem. Identifies the theoretical guarantee that the thesis must extend to $N$-player settings.*

3. **Liu, W., Wang, H., Guo, T. & Xing, J. (2022).** "Safe Opponent-Exploitation Subgame Refinement." *Advances in Neural Information Processing Systems (NeurIPS).*  
   *Introduces the SES algorithm: at each subgame root, construct a "gadget" game that converts the global safety constraint (Ganzfried 2015) into a local constraint solvable with standard CFR/LP methods. The gadget adds virtual "fall back to Nash" actions, ensuring that the subgame exploitation never violates global safety. Bridges the theoretical framework to real-time exploitation.*

4. **Jeary, J. & Turrini, P. (2023).** "Safe Opponent Exploitation For Epsilon Equilibrium Strategies."  
   arXiv: https://arxiv.org/abs/2307.12338  
   *Identifies a critical flaw in Ganzfried (2015): when the baseline is an $\varepsilon$-equilibrium (as all practical implementations are, due to abstraction), the safety guarantee breaks. Develops "prime-safe" exploitation that redefines the safety floor as the worst-case value of the $\varepsilon$-equilibrium. The realistic safety notion for any system using game abstraction (Step 4).*

5. **Ge, C., Zhu, Y. et al. (2024).** "Safe and Robust Subgame Exploitation in Imperfect Information Games." *Proceedings of the 41st International Conference on Machine Learning (ICML).*  
   *Introduces Adaptation Safety: an exploitation strategy is "safe" if it is no more exploitable than the blueprint ($\text{exploitability}(\sigma_{exploit}) \leq \text{exploitability}(\sigma_{blueprint})$). The OX-Search algorithm provides per-information-set exploitation bounds and neutralizes the "teaching attack" where an adversary intentionally plays suboptimally to manipulate the opponent model. Represents the state of the art in 2-player safe exploitation.*

6. **Milec, D., Kovařík, V. & Lisý, V. (2025).** "Adapting Beyond the Depth Limit: Counter Strategies in Large Imperfect Information Games."  
   arXiv: https://arxiv.org/abs/2501.10464  
   *Proposes the ABD algorithm using a strategy-portfolio approach with matrix-valued states for depth-limited exploitation. The first method to fully utilize opponent model information beyond the depth limit — prior methods assume rational play beyond search depth. Demonstrates $>$2× utility improvement when opponents make mistakes beyond the depth limit.*

### Textbook

7. **Shoham, Y. & Leyton-Brown, K. (2008).** *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations.* Cambridge University Press.  
   Sections 3.4 (Computing Nash Equilibria) and 4.6 (Computing Best Responses).  
   Available: http://www.masfoundations.org/download.html  
   *Revisit equilibrium computation with exploitation in mind: best response is the exploitation algorithm; Nash equilibrium is the safety baseline. The LP machinery from these sections powers the safety constraints.*

### Supplementary References

8. **Milec, D., Kovařík, V. & Lisý, V. (2021).** "Continual Depth-limited Responses for Computing Counter-strategies."  
   arXiv: https://arxiv.org/abs/2112.12594  
   *Precursor to ABD. Depth-limited response method that motivates the strategy-portfolio extension.*

9. **Farina, G. & Sandholm, T. (2021).** "Model-Free Online Learning in Unknown Sequential Decision Making Problems and Games." *AAAI Conference on Artificial Intelligence.*  
   arXiv: https://arxiv.org/abs/2103.04539  
   *Contrasting approach: model-free regret minimization that adapts without an opponent model. Avoids model misspecification risk at the cost of slower adaptation and no exploitation guarantee.*

---

## Methodology

### Phase 1: Conceptual Foundation (2 days)

Survey of the safe exploitation problem: why naive best-response exploitation is dangerous (the "teaching attack" — an adversary plays suboptimally to manipulate your model, then switches to exploit your adapted strategy), what "safety" means formally (expected value never drops below the Nash baseline), and how real-time subgame search changes the exploitation paradigm. Establish understanding of the exploitation-safety Pareto frontier and the progression of safety notions across the literature.

### Phase 2: Empirical Familiarization (2 days)

Hands-on experimentation building intuition for the exploitation-safety tradeoff:
- Construction of the exploitation-safety Pareto curve: sweep Nash-to-best-response blend parameter, measure exploitation profit (X-axis) vs. worst-case exploitability (Y-axis) for each blend
- Demonstration of naive exploitation vulnerability: compute the full best response to a weak opponent, then measure exploitability of that best response against a Nash-playing adversary
- Implementation of a simple Restricted Nash Response: vary the deviation parameter $p$ and observe the exploitation-vs-safety tradeoff across opponent types
- Prototype subgame exploitation: at a specific Leduc decision point, solve the sub-tree assuming the modeled opponent, compare with the blueprint action
- Identification of key questions: formal definition of safety, why Nash-BR blending is insufficient, and how subgame solving enables local exploitation

### Phase 3: Literature Study (4 days)

Structured reading of six primary sources in logical progression:

1. **Johanson et al. (2007):** Restricted Nash Response — the LP formulation ($\max c^T x$ subject to exploitability $\leq$ bound), the safety parameter $p$, and experiments showing the exploitation-safety tradeoff on Kuhn and Leduc. Focus on the LP structure, which recurs in all subsequent papers.

2. **Ganzfried & Sandholm (2015):** The Safety Theorem — proof sketch using the minimax theorem, the constrained optimization formulation (maximize EV against opponent model subject to worst-case EV $\geq$ Nash value), and identification of where the proof assumes perfect Nash and 2-player zero-sum.

3. **Liu et al. (2022):** SES algorithm — the gadget construction that converts global safety into a local subgame constraint, enabling real-time exploitation with standard solvers. Focus on how the gadget adds "fall back to Nash" virtual actions.

4. **Jeary & Turrini (2023):** The $\varepsilon$-equilibrium gap — why Ganzfried's guarantee breaks for approximate baselines, the prime-safe redefinition of the safety floor, and implications for any system using game abstraction.

5. **Ge et al. (2024):** Adaptation Safety — the modern safety definition (exploitation strategy no more exploitable than the blueprint), OX-Search with per-information-set bounds, and the teaching attack neutralization.

6. **Milec et al. (2025):** ABD algorithm — matrix-valued states at the depth limit, strategy-portfolio approach, and the first principled method for utilizing opponent model information beyond the search horizon.

Mathematical content requiring derivation:
- Safety Theorem proof sketch (Ganzfried 2015, Theorem 1): reproduce with pen and paper, identify the minimax theorem step, and locate the 2-player zero-sum assumption that prevents $N$-player extension
- Adaptation Safety definition (Ge 2024, Definition 2): formal comparison with Ganzfried's safety — understand why the weaker condition enables tractable exploitation with imperfect baselines
- RNR LP formulation (Johanson 2007, Eq. 3–4): understand the linear program structure that serves as the computational backbone across all methods

### Phase 4: Implementation (10 days)

From-scratch implementation in Python (NumPy + SciPy for LP), building on Step 7 opponent models, Steps 2–3 Nash strategies, and Step 6 game tree infrastructure:

| Implementation | Games | Validation Criterion |
|----------------|-------|---------------------|
| Safety checker (worst-case exploitability computation) | Kuhn + Leduc | Matches OpenSpiel exploitability to within 0.001 (Kuhn) / 0.01 (Leduc) |
| Restricted Nash Response (RNR) LP solver | Kuhn + Leduc | At $p=0$: exploitability matches Nash; at $p=1$: exploitation matches full BR |
| Ganzfried safe exploitation solver | Kuhn + Leduc | Worst-case EV $\geq$ Nash value within 0.001 tolerance |
| Prime-safe extension for $\varepsilon$-equilibrium baselines | Leduc (abstracted) | Safety floor correctly adjusted by $\varepsilon$ of abstract strategy |
| SES-style subgame exploitation with gadget construction | Leduc | Subgame solution exploits more than blueprint; gadget safety maintained |
| Adaptation safety checker (Ge 2024 notion) | Kuhn + Leduc | $\text{exploitability}(\sigma_{exploit}) \leq \text{exploitability}(\sigma_{blueprint})$ |
| Full pipeline integration (Step 7 models → Step 8 exploitation) | Kuhn + Leduc | Cumulative profit positive against exploitable opponents; zero safety violations |

Implementation is sub-structured as: 2 days architecture + scaffolding → 6 days core algorithms (RNR, Ganzfried, prime-safe, SES, adaptation safety) → 2 days validation + benchmarking.

**Validation approach:** Cross-validation against OpenSpiel exploitability and best-response modules. Head-to-head comparison of all methods across all Step 7 opponent types. Teaching attack stress test (opponent switches from exploitable to Nash mid-game). Exploitation-safety Pareto frontier plots for each method.

### Phase 5: Synthesis (3 days)

Consolidation of theoretical and practical knowledge:
- Complete mapping of the safe exploitation trajectory: RNR → Ganzfried → Jeary → SES → OX-Search → ABD, with each paper's contribution and limitation
- Precise identification of where the 2-player zero-sum assumption enters each safety proof — the thesis extension point for Contribution #2
- Analysis of the Ganzfried Safety Theorem proof step that uses the minimax theorem: this step fails for $N > 2$ players, defining the thesis attack vector
- Integration assessment: Step 7 (sensor: opponent model) + Step 8 (actuator: safe exploitation) = complete Behavioral Adaptation Framework prototype for 2-player games
- Forward connection: extending safe exploitation guarantees to $N$-player games requires either a weaker safety notion or structural assumptions (coalition structure, Step 11)
- Documentation of open questions: $N$-player safety definitions, baseline quality requirements for adaptation safety, model latency interaction with safety guarantees

---

## Deliverables

1. **Safety checker module** computing worst-case exploitability and verifying safety constraints
2. **Exploitation metrics module** measuring exploitation value and safety violations
3. **Restricted Nash Response (RNR) solver** with configurable safety parameter
4. **Ganzfried safe exploitation solver** implementing the Safety Theorem guarantee
5. **Prime-safe exploitation extension** handling $\varepsilon$-equilibrium baselines
6. **SES-style subgame exploitation solver** with gadget construction
7. **Adaptation safety checker** implementing the Ge (2024) safety notion
8. **Exploitation-safety Pareto frontier** plots for all methods
9. **Full pipeline integration** — Step 7 opponent models feeding Step 8 exploitation engine
10. **Head-to-head comparison** — all exploitation methods × all opponent types, with safety and profit metrics
11. **Teaching attack stress test** — deceptive opponent switching behavior mid-game
12. **Step summary** documenting the safe exploitation progression and thesis contribution gap

---

## PhD Contribution Alignment

| Concept | Downstream Application |
|---------|----------------------|
| Safety Theorem (Ganzfried 2015) | Foundation for Contribution #1 (Behavioral Adaptation Framework) — the formal guarantee that exploitation doesn't sacrifice safety |
| Minimax theorem dependency | The precise failure point for $N$-player extension — Contribution #2 must find an alternative guarantee when minimax doesn't hold |
| Adaptation Safety (Ge 2024) | The practical safety definition the thesis should adopt — achievable where strict Nash safety is not |
| Prime-safe exploitation (Jeary 2023) | Required for any implementation using game abstraction — connects Step 4 abstraction quality to Step 8 exploitation budget |
| Subgame exploitation (SES/OX-Search) | Real-time exploitation mechanism for Contribution #1 — enables safe exploitation during play without full-game recomputation |
| Depth-limited exploitation (ABD) | Scalability mechanism — matrix-valued states may extend to multi-agent settings (Contribution #2) |
| Teaching attack resilience | Prototype evaluation methodology for Contribution #3 (Evaluation Framework) — adversarial robustness testing |
| Full exploitation pipeline | End-to-end prototype for Contribution #1: observe → model (Step 7) → exploit safely (Step 8), validated on 2-player games and ready for $N$-player extension |

> **[P3] Contribution #2 scope narrowing:** Reframe “PhD Contribution Alignment”: Contribution #2 is **tractable heuristics + empirical validation on small N-player games**, not a general N-player safety theorem. Targets: piKL-regularized exploitation, equal share baseline (payoff ≥ C/n), adaptation safety extended to 3-player Kuhn/Leduc. Explicitly state the non-claim: general N-player minimax analog.

> **[P6] Sequence-form LP understanding:** Ensure LP formulations (RNR, Ganzfried constrained response) are understood as **sequence-form programs**, not black-box solvers. Connect to the sequence-form representation from Shoham & Leyton-Brown Ch. 4 (referenced in Step 2 note).

---

## Exit Criteria

- [ ] All five exploitation methods implemented and working on both Kuhn and Leduc
- [ ] RNR Pareto curve generated showing exploitation vs. exploitability tradeoff
- [ ] Ganzfried Safety Theorem verified: exploitation strategies meet Nash value guarantee
- [ ] Prime-safe extension working with $\varepsilon$-equilibrium baselines from Step 4 abstractions
- [ ] SES subgame exploitation with gadget construction functioning on Leduc subgames
- [ ] Adaptation safety correctly computed and compared with Ganzfried safety
- [ ] Ability to explain the safe exploitation progression from memory: RNR → Ganzfried → Jeary → SES → OX-Search → ABD
- [ ] Ability to identify WHERE the 2-player zero-sum assumption enters the safety proofs
- [ ] Ability to explain the difference between Ganzfried safety and adaptation safety
- [ ] Full pipeline integration: Step 7 model → Step 8 exploitation → measured safety + profit
- [ ] Teaching attack stress test completed with results documented
- [ ] Exploitation-safety Pareto frontier generated for all methods
- [ ] Cross-validated against OpenSpiel exploitability and best-response modules
- [ ] Step summary completed and committed to repository
- [ ] Connections to Steps 2–7 and forward to Steps 9–11 identified and documented
- [ ] Thesis contribution gap documented: $N$-player extension as Contribution #2 target

---

**Short Title:** Step 8 — Safe Exploitation

---

**Short Title:** Step 8 — Safe Exploitation
