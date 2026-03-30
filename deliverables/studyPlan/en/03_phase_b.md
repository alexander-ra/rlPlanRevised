## 3. Phase B — Scaling the Toolbox (Steps 3–4)

### 3.1 Phase Overview

Phase A established a working CFR^15^ solver on the minimal Kuhn Poker^19^ benchmark, but vanilla CFR requires a full traversal of the game tree on every iteration — an approach that becomes infeasible as games grow. This phase will introduce two complementary scaling mechanisms: Monte Carlo sampling methods that reduce per-iteration cost, and game abstraction techniques that reduce the game tree itself. These tools are needed to bridge the gap between toy benchmarks and the medium-scale games on which later thesis work will be developed.

### 3.2 Step 3 — CFR Variants and Monte Carlo Methods

**Contribution Alignment.** Monte Carlo CFR variants will provide the computationally tractable equilibrium computation needed for medium-scale games, which will underpin the empirical work in later contributions. CFR+ accelerates convergence, enabling equilibrium computation for games beyond the reach of vanilla CFR. Understanding the variance characteristics of different sampling schemes will inform later design decisions in opponent modeling.

**Literature.**

1. Lanctot, M., Waugh, K., Zinkevich, M. and Bowling, M. (2009). "Monte Carlo Sampling for Regret Minimization in Extensive Games." *Advances in Neural Information Processing Systems 22 (NeurIPS).*
2. Tammelin, O., Burch, N., Johanson, M. and Bowling, M. (2015). "Solving Heads-Up Limit Texas Hold'em." *Proceedings of the 24th International Joint Conference on Artificial Intelligence (IJCAI).*
3. Chen, B. and Ankenman, J. (2006). *The Mathematics of Poker.* ConJelCo. Chapters 1–8.

**Practical Tasks.**

- Construct a Leduc Hold'em^20^ game engine (six-card deck, two rounds, one community card, ~936 information sets^6^).
- Implement external-sampling MCCFR on both Kuhn and Leduc; verify convergence to the same Nash equilibrium as vanilla CFR with lower wall-clock time.
- Implement CFR+ with regret flooring, alternating updates, and linear averaging; demonstrate approximately ten-fold convergence speedup over vanilla CFR on Kuhn Poker.
- Compare convergence profiles of all variants: exploitability^3^ versus iterations and versus wall time.

### 3.3 Step 4 — Game Abstraction and Scaling Imperfect-Information Games

**Contribution Alignment.** This step will study how game abstraction — both lossless and lossy — affects the quality of computed equilibria, and how subgame solving^22^ can refine strategies during play. These techniques are directly relevant to later work on safe exploitation (where abstraction quality bounds exploitation risk) and opponent modeling (where abstraction granularity determines the ability to distinguish opponent types).

**Literature.**

1. Gilpin, A. and Sandholm, T. (2007). "Lossless Abstraction of Imperfect Information Games." *Journal of the ACM*, 54(5).
2. Johanson, N., Burch, N., Valenzano, R. and Bowling, M. (2013). "Evaluating State-Space Abstractions in Extensive-Form Games." *Proceedings of the 12th International Conference on Autonomous Agents and Multi-Agent Systems (AAMAS).*
3. Kroer, C. and Sandholm, T. (2016). "Imperfect-Recall Abstractions with Bounds in Games." Preprint.
4. Brown, N. and Sandholm, T. (2017). "Safe and Nested Subgame Solving for Imperfect-Information Games." Preprint.

**Practical Tasks.**

- Implement lossless abstraction via suit isomorphism detection on Leduc Hold'em; verify that the resulting Nash equilibrium^7^ is identical to the unabstracted solution.
- Implement lossy card bucketing with configurable granularity; measure exploitability degradation as the number of buckets decreases.
- Construct an Extended Leduc variant (four ranks, two suits, multiple bet sizes, ~5000+ information sets) as a scaling testbed.
- Build a combined abstraction pipeline composing card bucketing, action abstraction, and suit isomorphism; evaluate on a Pareto frontier of abstraction size versus exploitability gap.

