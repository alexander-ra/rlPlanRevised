# Step 4 — Game Abstraction + Scaling Imperfect-Information Games

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 2 (Game Theory + CFR Basics), Step 3 (CFR Variants + Monte Carlo Methods)  
**Phase:** B — Scaling the Toolbox

---

## Objectives

Develop the theory and practice of game abstraction — the essential scaling mechanism that enables CFR-family algorithms to handle large imperfect-information games:

1. Understand the distinction between lossless and lossy abstraction, and when each is appropriate
2. Learn information abstraction (card bucketing) and action abstraction (bet-size restriction) as the two primary compression dimensions
3. Study subgame solving as the mechanism for correcting abstraction errors in real time
4. Implement an end-to-end abstraction pipeline and quantify the abstraction quality–computational cost tradeoff

---

## Literature

### Papers

1. **Gilpin, A. & Sandholm, T. (2007).** "Lossless Abstraction of Imperfect Information Games." *Journal of the ACM, 54(5).*  
   Available: https://www.cs.cmu.edu/~sandholm/lossless.jacm.pdf  
   *Introduces the concept of ordered game isomorphisms — the formal criterion for determining when two information sets can be merged without any strategic loss. Provides the GameShrink algorithm for automatically finding all lossless abstractions.*

2. **Johanson, N., Burch, N., Valenzano, R. & Bowling, M. (2013).** "Evaluating State-Space Abstractions in Extensive-Form Games." *Proceedings of the 12th International Conference on Autonomous Agents and Multi-Agent Systems (AAMAS).*  
   Available: https://poker.cs.ualberta.ca/publications/AAMAS13-abstraction.pdf  
   *Proposes Earth Mover's Distance (EMD) as a quantitative metric for evaluating lossy abstraction quality. Establishes the relationship between abstraction granularity and resulting strategy quality.*

3. **Kroer, C. & Sandholm, T. (2016).** "Imperfect-Recall Abstractions with Bounds in Games."  
   arXiv: https://arxiv.org/abs/1409.3302  
   *Provides error bounds for imperfect-recall abstractions, bridging the gap between lossless abstraction theory and practical lossy approaches. Demonstrates that deliberately forgetting information can reduce game sizes exponentially while maintaining provable guarantees.*

4. **Brown, N. & Sandholm, T. (2017).** "Safe and Nested Subgame Solving for Imperfect-Information Games."  
   arXiv: https://arxiv.org/abs/1705.02955  
   *Introduces subgame solving with safety guarantees — the real-time refinement mechanism that corrects abstraction errors at specific game states. The resolved strategy provably cannot be more exploitable than the original blueprint. Foundational technique used in all competitive poker AIs since Libratus.*

### Supplementary References

5. **Li, W. et al. (2024).** "RL-CFR: A New RL Framework for Action Abstraction in Imperfect Information Extensive-Form Games."  
   arXiv: https://arxiv.org/abs/2403.14114  
   *Uses reinforcement learning to learn action abstractions rather than hand-crafting them. Bridges RL methods (Step 1) to the abstraction problem.*

6. **Fu, H. et al. (2025).** "No-Regret Strategy Optimization with KrwEmd Metric for Imperfect-Recall Abstraction." *Accepted at AAAI 2026.*  
   arXiv: https://arxiv.org/abs/2411.16111  
   *Frontier work proposing a new earth-mover-distance-based abstraction metric for imperfect-recall games.*

---

## Methodology

### Phase 1: Conceptual Foundation (1 day)

Survey of the game abstraction problem: why real-world games exceed computational tractability ($10^{161}$ states in Texas Hold'em), how grouping similar states and restricting action sets reduces game size, and why poor abstractions can produce arbitrarily bad strategies. Establish understanding of the lossless–lossy spectrum and the role of subgame solving in managing abstraction errors.

### Phase 2: Empirical Familiarization (2 days)

Hands-on experimentation using the Leduc Hold'em engine from Step 3:
- Application of suit isomorphism as a lossless abstraction on Leduc (~936 → ~468 info sets)
- Construction of lossy card bucketing at multiple granularities ($k = 2, 3, 5$, full)
- Extension of Leduc with variable bet sizes to create an action abstraction testbed
- Measurement of exploitability gaps between abstracted and exact Nash strategies
- Introduction of action translation: mapping out-of-abstraction actions to abstract actions

### Phase 3: Literature Study (3 days)

Structured reading of four sources:

1. **Gilpin & Sandholm (2007):** Ordered game isomorphisms (the formal criterion for lossless abstraction) and the GameShrink algorithm for automatic lossless abstraction detection. Focus on the definition and its implications for abstraction design.

2. **Johanson et al. (2013):** Earth Mover's Distance (EMD) as a quantitative metric for lossy abstraction quality. Establishes the relationship between abstraction granularity and resulting strategy exploitability.

3. **Kroer & Sandholm (2016):** Error bounds for imperfect-recall abstractions. Demonstrates that deliberately forgetting past information can reduce game size exponentially while maintaining provable quality guarantees.

4. **Brown & Sandholm (2017):** Safe and nested subgame solving. The real-time refinement mechanism that corrects abstract blueprint errors with a safety guarantee (resolved strategy cannot be more exploitable than the blueprint). Foundational to all modern poker AI architectures studied in Step 6.

### Phase 4: Implementation (6 days)

From-scratch implementation in Python (NumPy only), building on the Step 3 Leduc engine and MCCFR solver:

| Implementation | Games | Validation Criterion |
|----------------|-------|---------------------|
| Lossless abstraction (suit isomorphism detection + merge) | Leduc | Nash equilibrium identical to unabstracted game; info set count halved |
| Lossy card bucketing (hand-strength clustering, configurable $k$) | Leduc | Exploitability monotonically decreasing as $k$ increases |
| Action abstraction + translation | Extended Leduc | Positive exploitability gap, bounded, playable strategy |
| Extended Leduc variant (4 ranks, 2 suits, multiple bet sizes) | — | Correct game tree with ~5000+ information sets |
| Combined abstraction pipeline | Extended Leduc | Successfully composes all three abstraction types |
| Abstraction quality evaluation | All variants | Pareto frontier: abstraction size vs. exploitability gap |

**Validation approach:** Cross-validation against OpenSpiel; exploitability computation in the full (unabstracted) game for all abstract strategies; Pareto frontier analysis showing the tradeoff between computational cost and strategy quality.

### Phase 5: Synthesis (2 days)

Consolidation of theoretical and practical knowledge:
- Architecture preview: identify abstraction and subgame solving components in the Pluribus pipeline (preparation for Step 6)
- Connection mapping: hand-crafted abstraction (Step 4) → neural approximation (Step 5, Deep CFR) → full architecture integration (Step 6)
- Forward connection: abstraction granularity → opponent distinguishability in modeling (Step 7)
- Documentation of step summary and learning log updates

---

## Deliverables

1. **Lossless abstraction module** applying suit isomorphism to Leduc Hold'em
2. **Lossy card bucketing module** with configurable number of buckets
3. **Action abstraction module** with action translation for unmapped bet sizes
4. **Extended Leduc Hold'em variant** (4 ranks, 2 suits, ~5000+ information sets)
5. **Combined abstraction pipeline** composing all three abstraction types
6. **Abstraction quality evaluation** — Pareto frontier plot: info set count vs. exploitability gap
7. **Step summary** connecting game abstraction to the broader algorithmic progression

---

## PhD Contribution Alignment

| Concept | Downstream Application |
|---------|----------------------|
| Lossless abstraction | Guarantees no strategic loss — baseline abstraction strategy for Contribution #1 |
| Lossy abstraction + quality metrics | Determines game representation granularity for opponent modeling (Contribution #1, Step 7) |
| Action translation | Maps unseen opponent behavior to known abstract types — parallels the opponent classification problem (Contribution #1) |
| Exploitability gap measurement | Standard evaluation metric for Contribution #3 (Evaluation Methodology) |
| Pareto frontier framework | Template for evaluating tradeoffs in the thesis evaluation chapter (Contribution #3) |
| Subgame solving | Safety mechanism for real-time strategy refinement — extends to safe exploitation (Step 8, Contribution #1) |

---

## Exit Criteria

- [ ] Lossless abstraction produces identical Nash equilibrium on Leduc
- [ ] Lossy card bucketing demonstrates measurable quality degradation as $k$ decreases
- [ ] Action abstraction + translation pipeline functioning end-to-end
- [ ] Combined abstraction pipeline tested on Extended Leduc
- [ ] Pareto frontier plot produced: abstraction size vs. exploitability gap
- [ ] Ability to explain lossless vs. lossy abstraction and subgame solving from memory
- [ ] Understanding of action translation problem and its practical solutions
- [ ] Step summary completed and committed to repository
- [ ] Connections to Steps 1–3 and forward to Steps 5–6 identified and documented
