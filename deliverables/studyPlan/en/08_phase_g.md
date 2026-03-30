## 8. Phase G — Integration (Steps 14–15)

### 8.1 Phase Overview

Phase G will synthesize the preceding work into two integrative deliverables. Step 14 constructs a unified evaluation framework validated across all game types encountered in the study plan — constituting the core of Contribution 3 (Evaluation Methodology). Step 15 maps the research frontier, designs the experimental program, produces a Chapter I outline for the dissertation (due November 2026), and establishes the publication pipeline.

### 8.2 Step 14 — Evaluation Frameworks and Exploitability Metrics

**Contribution Alignment.** This step will constitute the core of Contribution 3 directly. The planned three-layer evaluation framework will integrate exploitability computation, population-level ranking (Elo, $\alpha$-Rank^52^, VasE^53^), and statistical confidence quantification (AIVAT^54^ variance reduction). It will be validated across Kuhn Poker^19^, Leduc Hold'em^20^, So Long Sucker^45^, and real-world data. For Contribution 1, the framework will measure whether behavioral adaptation produces measurable improvements. For Contribution 2, marginal exploitability^55^ will test whether two-player safe exploitation guarantees generalize to multi-agent settings.

**Literature.**

1. Timbers, F., Bard, N., Lockhart, E., Lanctot, M., Schmid, M., Burch, N., Schrittwieser, J., Hubert, T. and Bowling, M. (2022). "Approximate Exploitability: Learning a Best Response in Large Games." Preprint.
2. Lanctot, M., Larson, K., Bachrach, Y., Marris, L., Li, Z., Bhoopchand, A., Anthony, T., Tanner, B. and Koop, A. (2025). "Evaluating Agents using Social Choice Theory." Preprint.
3. Rowland, M., Omidshafiei, S., Tuyls, K., Perolat, J., Valko, M., Piliouras, G. and Munos, R. (2019). "Multiagent Evaluation under Incomplete Information." Preprint.
4. Burch, N., Johanson, M. and Bowling, M. (2019). "AIVAT: A New Variance Reduction Technique for Agent Evaluation in Imperfect Information Games." *Proceedings of the 33rd AAAI Conference on Artificial Intelligence.*
5. Omidshafiei, S., Papadimitriou, C., Piliouras, G., Tuyls, K. et al. (2019). "$\alpha$-Rank: Multi-Agent Evaluation by Evolution." *Nature Scientific Reports.*

**Practical Tasks.**

- Audit and unify all evaluation code from prior steps (exploitability from Steps 3 and 8, EGTA^43^ and spinning top decomposition^42^ from Step 10, SLS metrics from Step 11, behavioral metrics from Step 13) into a three-layer evaluation API.
- Construct a bot zoo of reference agents for Kuhn and Leduc covering four tiers: trivial (random, always-call, always-fold), heuristic (tight-aggressive, loose-aggressive, tight-passive), computed (Nash/CFR, DQN), and advanced (PSRO^38^, Decision Transformer^46^).
- Implement $\alpha$-Rank^52^ with Fermi selection function; compute stationary distributions via eigenvalue decomposition and analyze sensitivity to the selection pressure parameter.
- Implement VasE^53^ with tournament matrix construction from pairwise comparisons across games; compute maximal lotteries via linear programming and intransitive cycle detection.
- Implement AIVAT^54^ variance reduction using a CFR-derived control variate with counterfactual adjustment per chance node; verify variance reduction of at least five-fold on Kuhn and ten-fold on Leduc relative to raw evaluation.
- Conduct cross-game validation: full three-layer evaluation on Kuhn, Leduc, So Long Sucker^45^ (marginal exploitability^55^), and Playtech data (AIVAT-adjusted confidence intervals for style classification and collusion detection^50^).
- Produce a disagreement analysis comparing Elo, $\alpha$-Rank, and VasE rankings, with the spinning top decomposition explaining cases of divergence between transitive and cyclic competitive structures.

### 8.3 Step 15 — Research Frontier Mapping and Contribution Design

**Contribution Alignment.** This step will complete the learning phase and design the research phase. The deliverables will include a research frontier map for each contribution, formal contribution design documents, experimental specifications, a Chapter I outline (25–30 pages, due November 2026), and a publication pipeline through to defense.

**Literature.**

1. Southey, F., Bowling, M., Larson, B., Piccione, C., Burch, N., Billings, D. and Rayner, C. (2005). "Bayes' Bluff: Opponent Modelling in Poker." *Proceedings of the 21st Conference on Uncertainty in Artificial Intelligence (UAI).*
2. Ganzfried, S. and Sandholm, T. (2015). "Safe Opponent Exploitation." *ACM Transactions on Economics and Computation*, 3(2).
3. Ge, C., Zhu, Y. et al. (2024). "Safe and Robust Subgame Exploitation in Imperfect Information Games." *Proceedings of the 41st International Conference on Machine Learning (ICML).*
4. Ge, C., Wang, Y., Li, W. and Jin, C. (2024). "Securing Equal Share: A Principled Approach for Learning Multiplayer Symmetric Games." Preprint.
5. Milec, D., Kovařík, V. and Lisý, V. (2025). "Adapting Beyond the Depth Limit: Counter Strategies in Large Imperfect Information Games." Preprint.
6. Omidshafiei, S., Papadimitriou, C., Piliouras, G., Tuyls, K. et al. (2019). "$\alpha$-Rank: Multi-Agent Evaluation by Evolution." *Nature Scientific Reports.*

**Practical Tasks.**

- Produce a research frontier map documenting, for each of the three contributions, the current state of the art, the identified gap, supporting evidence from the study plan, and a feasibility assessment.
- Validate each identified gap against recent publications (2024–2026), conference proceedings, and existing dissertations; record findings in a gap validation log.
- Write contribution design documents (three documents, two to three pages each) specifying the problem statement, prior art, gap, proposed method, experimental protocol, target publications, timeline, and risk analysis.
- Specify four experiments: (1) behavioral adaptation on Kuhn Poker (player embedding^48^ classification accuracy within 50 hands), (2) N-player safe exploitation on three-player Kuhn (piKL-regularized exploitation versus equal-share baseline), (3) coalition-aware safe exploitation on So Long Sucker^45^, and (4) cross-game evaluation framework validation across Kuhn, Leduc, and SLS.
- Produce a Chapter I outline (seven sections, 25–30 pages) covering introduction, foundations, opponent modeling and behavioral adaptation, safe exploitation, evaluation of multi-agent game AI, proposed contributions, and research plan — aligned with the November 2026 deadline.
- Establish the publication pipeline: six target publications mapped to four dissertation chapters with venue selections and submission deadlines through April 2029.

