# Step 7 — Opponent Modeling — Inference from Behavioral Traces

**Duration:** 21 days (Tier 1)  
**Dependencies:** Step 2 (Game Theory + CFR Basics), Step 6 (End-to-End Game AI Architectures)  
**Phase:** D — Opponent Modeling + Exploitation

---

## Objectives

Develop the theory and practice of inferring opponent strategies from observed behavioral data in imperfect-information games:

1. Understand Bayesian opponent modeling as inference under partial observability — prior beliefs over opponent strategies, likelihood of observed actions, posterior estimation via Bayes' rule
2. Study the progression from discrete type-based models to continuous parametric models to consistent convergent estimators
3. Understand the distinction between explicit modeling (maintain a belief distribution) and implicit modeling (adapt strategy directly from observations)
4. Implement three opponent modeling approaches with comparative analysis on standard benchmarks
5. Build a complete adaptive exploitation pipeline as a prototype for the thesis Behavioral Adaptation Framework

---

## Literature

### Papers

1. **Southey, F., Bowling, M., Larson, B., Piccione, C., Burch, N., Billings, D. & Rayner, C. (2005).** "Bayes' Bluff: Opponent Modelling in Poker." *Proceedings of the 21st Conference on Uncertainty in Artificial Intelligence (UAI).*  
   Available: https://poker.cs.ualberta.ca/publications/UAI05.pdf  
   *Introduces Bayesian opponent modeling for poker: a generative model with Dirichlet-multinomial priors over opponent action probabilities at each information set. The foundational framework upon which all subsequent Bayesian opponent modeling builds.*

2. **Bard, N., Johanson, M., Burch, N. & Bowling, M. (2013).** "Online Implicit Agent Modelling." *Proceedings of the 12th International Conference on Autonomous Agents and Multi-Agent Systems (AAMAS).*  
   Available: https://poker.cs.ualberta.ca/publications/AAMAS13-bard.pdf  
   *Introduces implicit agent modeling — an alternative paradigm where the modeling agent's strategy evolves to respond to observed behavior without maintaining an explicit belief distribution. Demonstrates faster adaptation in certain settings with reduced computational overhead.*

3. **Ganzfried, S. & Sun, Q. (2016).** "Bayesian Opponent Exploitation in Imperfect-Information Games."  
   arXiv: https://arxiv.org/abs/1603.03491  
   *Develops the formal framework connecting Bayesian opponent modeling to exploitation. Proves convergence of the exploitation strategy to the true best response as observations increase, under stationarity and prior support assumptions. Bridges opponent modeling (this step) to safe exploitation (Step 8).*

4. **Ganzfried, S., Wang, K. A. & Chiswick, M. (2022).** "Opponent Modeling in Multiplayer Imperfect-Information Games."  
   arXiv: https://arxiv.org/abs/2212.06027  
   *Extends opponent modeling from 2-player to N-player settings. Demonstrates that multiplayer opponent modeling requires joint modeling of all opponents simultaneously, and that the optimal exploitation strategy against multiple opponents differs from the combination of individual best responses. Experiments on 3-player Kuhn Poker.*

5. **Ganzfried, S. (2025).** "Consistent Opponent Modeling in Imperfect-Information Games."  
   arXiv: https://arxiv.org/abs/2508.17671  
   *Identifies a fundamental limitation of existing opponent modeling approaches: they do not guarantee convergence to the opponent's true strategy even in the limit. Develops a new algorithm based on sequence-form projected gradient descent that achieves consistency — guaranteed convergence to the true opponent strategy under standard identifiability assumptions.*

### Textbook

6. **Shoham, Y. & Leyton-Brown, K. (2008).** *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations.* Cambridge University Press.  
   Chapter 7: Learning and Teaching.  
   Available: http://www.masfoundations.org/download.html  
   *Formal framework for opponent modeling as a learning problem in multi-agent systems. Sections 7.1–7.3 cover the learning dynamics relevant to this step.*

### Supplementary References

7. **Milec, D., Kovařík, V. & Lisý, V. (2025).** "Adapting Beyond the Depth Limit: Counter Strategies in Large Imperfect Information Games."  
   arXiv: https://arxiv.org/abs/2501.10464  
   *Extends exploitation methods to depth-limited settings using strategy portfolios. Bridges opponent modeling to practical large-game exploitation. Primarily studied in Step 8.*

8. **Zhou, Q., Bai, D., Zhang, J., Duan, F. & Huang, K. (2022).** "DecisionHoldem: Safe Depth-Limited Solving With Diverse Opponents for Imperfect-Information Games."  
   arXiv: https://arxiv.org/abs/2201.11580  
   *Practical depth-limited solver handling diverse opponent populations in Texas Hold'em.*

---

## Methodology

### Phase 1: Conceptual Foundation (2 days)

Survey of the opponent modeling problem: why Nash equilibrium strategies ignore opponent weaknesses, what information can be extracted from behavioral traces under partial observability, and when the exploitation opportunity justifies the risk of model misspecification. Establish understanding of the two paradigms (explicit Bayesian modeling vs. implicit strategy adaptation) and their respective strengths.

### Phase 2: Empirical Familiarization (2 days)

Hands-on experimentation building intuition for opponent modeling dynamics:
- Construction of an opponent type library (5+ distinct strategies for Kuhn and Leduc Poker)
- Visualization of behavioral signatures — action frequency distributions that distinguish opponent types
- Measurement of exploitation opportunity: best-response value minus Nash value for each opponent type
- Prototype Bayesian type detector: posterior concentration over observed opponent types
- Exploration of failure modes: what happens when the opponent doesn't match any predefined type

### Phase 3: Literature Study (4 days)

Structured reading of five primary sources:

1. **Southey et al. (2005):** Bayesian opponent modeling framework — Dirichlet-multinomial prior, likelihood computation from observed actions, posterior update under partial observability (action visible, private hand often not). Focus on the posterior update equation and why Dirichlet conjugacy enables closed-form updates.

2. **Bard et al. (2013):** Implicit agent modeling — the strategy itself adapts to observations without maintaining explicit beliefs. Focus on the algorithmic distinction from Bayesian models and the tradeoff: explicit models provide interpretability and convergence guarantees; implicit models provide computational simplicity.

3. **Ganzfried & Sun (2016):** Bayesian exploitation framework — convergence guarantee for exploitation profit under stationarity and prior support assumptions. Focus on Theorem 1 (convergence of exploitation to true best response) and its assumptions. Bridges this step to Step 8.

4. **Ganzfried, Wang & Chiswick (2022):** Multiplayer opponent modeling — joint modeling of N opponents, the complication that optimal joint exploitation differs from individual best responses. Focus on the extension from 2-player to N-player and experimental results on 3-player Kuhn Poker.

5. **Ganzfried (2025):** Consistent opponent modeling — sequence-form projected gradient descent approach that guarantees convergence to the true opponent strategy. Focus on the consistency property that prior methods lack and the convex optimization formulation.

Mathematical content requiring derivation:
- Bayesian posterior update for opponent models (Southey et al.): small-example manual computation to build intuition for the update mechanics
- Dirichlet-multinomial conjugacy: understanding why this prior family enables efficient closed-form updates
- Sequence-form convex formulation (Ganzfried 2025): understanding the optimization landscape that makes consistent modeling tractable

### Phase 4: Implementation (10 days)

From-scratch implementation in Python (NumPy only for core algorithms):

Building on the Kuhn Poker engine (Step 2), Leduc Hold'em engine (Step 3), and Nash equilibrium strategies (Steps 2–3).

| Implementation | Games | Validation Criterion |
|----------------|-------|---------------------|
| Opponent type library (5+ strategies per game) | Kuhn + Leduc | Distinct behavioral signatures; correct best-response values |
| Observation buffer with partial observability | Kuhn + Leduc | Correct handling of showdown vs. non-showdown information |
| Type-based Bayesian opponent model (Dirichlet-multinomial) | Kuhn + Leduc | Posterior concentrates on correct type within 20 hands (Kuhn) |
| Continuous Bayesian model (per-info-set Dirichlet estimation) | Kuhn + Leduc | Action estimates within 5% of true strategy after 500 observations |
| Consistent opponent modeler (sequence-form projected gradient descent) | Kuhn + Leduc | Converges to true sequence-form strategy |
| Adaptive exploitation pipeline (observe → model → exploit → repeat) | Kuhn + Leduc | Cumulative profit strictly positive against exploitable opponents |

Implementation is sub-structured as: 2 days architecture + scaffolding → 6 days core algorithm → 2 days validation + benchmarking.

**Validation approach:** Cross-validation against OpenSpiel best-response and exploitability modules. Head-to-head comparison of all three models across all opponent types. Non-stationarity test (opponent switches type mid-game) to evaluate robustness.

### Phase 5: Synthesis (3 days)

Consolidation of theoretical and practical knowledge:
- Analytical comparison of three modeling approaches: type-based (strong structural priors, fast convergence, fragile to unknown types) vs. continuous (robust to unknown types, slow convergence) vs. consistent (best theoretical guarantees, highest computational cost)
- Connection mapping: opponent model as "sensor" feeds exploitation engine as "actuator" (Step 8)
- Forward connection: multiplayer opponent modeling requires simultaneous models of all opponents (Steps 9–11)
- Identification of thesis Contribution #1 prototype: the adaptive exploitation pipeline
- Documentation of open questions: non-stationarity handling, computational scaling, multi-model information sharing

---

## Deliverables

1. **Opponent type library** with 5+ distinct strategies for Kuhn and Leduc Poker
2. **Observation buffer** handling partial observability (showdown vs. non-showdown information)
3. **Type-based Bayesian opponent model** with Dirichlet-multinomial posterior inference
4. **Continuous Bayesian opponent model** with per-information-set action distribution estimation
5. **Consistent opponent modeler** implementing Ganzfried (2025) sequence-form approach
6. **Adaptive exploitation pipeline** integrating modeling and best-response computation
7. **Head-to-head model comparison** — convergence speed, final exploitation rate, robustness
8. **Non-stationarity test results** demonstrating model behavior under opponent type switching
9. **Step summary** connecting opponent modeling to the Behavioral Adaptation Framework

---

## PhD Contribution Alignment

| Concept | Downstream Application |
|---------|----------------------|
| Bayesian opponent modeling | Core component of Contribution #1 (Behavioral Adaptation Framework) — the "sensor" that infers opponent behavior from observations |
| Consistent opponent modeling | Potential basis for the thesis's theoretical contribution — extending consistency guarantees to non-stationary and multi-agent settings |
| Partial observability handling | Directly applicable to real-world adversarial settings (fraud detection, cybersecurity) where the adversary's full strategy is never visible |
| Multiplayer modeling extension | Foundation for Contribution #2 (Multi-Agent Safe Exploitation) — modeling N opponents jointly for coalition detection (Step 11) |
| Non-stationarity challenge | Key open problem for the thesis — how to maintain model quality when opponents adapt in response to exploitation |
| Adaptive exploitation pipeline | End-to-end prototype for Contribution #1, validated on toy games in this step and scaled in Steps 8–11 |

> **[P5] Level-k / Cognitive Hierarchy merge:** Add one paper on Level-k/cognitive hierarchy models (e.g., Wright & Leyton-Brown 2014 or Camerer, Ho & Chong 2004) to Phase 3 reading. Add a Level-k opponent type to the opponent type library in Phase 4. Models human suboptimality — critical for Playtech data validation in Step 13. ~1.5d absorbed within 21d allocation.

> **[P8] Bayesian Online Changepoint Detection merge:** Add Adams & MacKay (2007) changepoint detection to the non-stationarity experiment in Phase 4. Instead of ad-hoc “observe what happens when opponent switches type,” detect the switch point statistically, then trigger re-modeling. ~0.5d absorbed within 21d allocation.

> **[P11*] Meta-Learning Baseline (optional):** If Step 7 completes ahead of schedule, run one off-the-shelf meta-learning method (e.g., MAML or contextual bandit) as a comparison baseline against the Bayesian opponent model. No tuning. Preempts reviewer question “why not just meta-learn?”

---

## Exit Criteria

- [ ] All three opponent models produce convergent estimates on Kuhn and Leduc
- [ ] Type-based model demonstrates correct type identification within 20 hands on Kuhn
- [ ] Continuous model achieves action probability estimates within 5% of true strategy after 500 observations
- [ ] Consistent model converges to true sequence-form strategy, verified against ground truth
- [ ] Adaptive exploitation pipeline demonstrates measurable profit against exploitable opponents
- [ ] Ability to explain Bayesian opponent modeling from memory: prior → likelihood → posterior → best response
- [ ] Ability to explain explicit vs. implicit modeling distinction and when each is appropriate
- [ ] Head-to-head model comparison completed with clear conclusions per opponent type
- [ ] Non-stationarity test completed with robustness analysis
- [ ] Cross-validated against OpenSpiel best-response and exploitability modules
- [ ] Step summary completed and committed to repository
- [ ] Connections to Steps 2–6 and forward to Steps 8–11 identified and documented
- [ ] Open questions documented: non-stationarity handling, computational scaling, multiplayer extension

---

**Short Title:** Step 7 — Opponent Modeling

---

**Short Title:** Step 7 — Opponent Modeling
