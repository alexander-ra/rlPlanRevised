## 7. Phase F — Data-Driven Approaches (Steps 12–13)

### 7.1 Phase Overview

The preceding phases developed methods entirely within synthetic, self-play environments. Phase F will bridge the gap between theoretical methods and real-world behavioral data. Step 12 introduces sequence models (Decision Transformers^46^) and assesses large language model agents in strategic settings. Step 13 applies the resulting pipeline to anonymized real-world poker hand histories, constructing player embeddings^48^, behavioral classification systems, and a collusion detection^50^ module.

### 7.2 Step 12 — Sequence Models and LLM Agents in Strategic Settings

**Contribution Alignment.** This step will study the Decision Transformer^46^ architecture and its adversarially robust variant (ARDT^47^), which recovers near-Nash strategies from offline data — a potential alternative path for Contribution 2 that bypasses intractable equilibrium computation in N-player settings. A critical limitation of return conditioning in stochastic environments will constrain the design of the real-world data pipeline in Step 13. The multi-paradigm comparison table produced here will serve as a prototype for the evaluation framework of Contribution 3.

**Literature.**

1. Chen, L., Lu, K., Rajeswaran, A., Lee, K., Grover, A., Laskin, M., Abbeel, P., Srinivas, A. and Mordatch, I. (2021). "Decision Transformer: Reinforcement Learning via Sequence Modeling." *Advances in Neural Information Processing Systems (NeurIPS).*
2. Paster, K., McIlraith, S. and Ba, J. (2022). "You Can't Count on Luck: Why Decision Transformers and RvS Fail in Stochastic Environments." Preprint.
3. Tang, X., Marques, A., Kamalaruban, P. and Bogunovic, I. (2024). "Adversarially Robust Decision Transformer." *Advances in Neural Information Processing Systems (NeurIPS).*
4. Janner, M., Li, Q. and Levine, S. (2021). "Offline Reinforcement Learning as One Big Sequence Modeling Problem." *Advances in Neural Information Processing Systems (NeurIPS).*
5. Guertler, L., Cheng, B., Yu, S., Liu, B., Choshen, L. and Tan, C. (2025). "TextArena." Preprint.
6. Meta AI (2022). "Human-Level Play in the Game of Diplomacy by Combining Language Models with Strategic Reasoning." *Science*, 378(6624), pp. 1067–1074.

**Practical Tasks.**

- Generate a poker trajectory dataset (50,000+ Kuhn Poker^19^ hands) using CFR agents from Step 3; design the poker state tensor encoding that will transfer to the real-world data pipeline in Step 13.
- Adapt and train a Decision Transformer^46^ for poker state and action spaces; validate return-to-go conditioning and demonstrate the stochasticity limitation (Paster et al., 2022) whereby the model conflates lucky card deals with skilled play.
- Implement ARDT^47^ with minimax expectile regression; train on mixed-quality opponent data and verify recovery of near-Nash strategies on Kuhn Poker (measured by exploitability^3^ against the known analytical equilibrium from Step 2).
- Deploy LLM agents on TextArena strategic games to assess capabilities in negotiation, deception, and theory-of-mind reasoning.
- Evaluate LLM agents on Kuhn Poker with standardized metrics: exploitability, bluff frequency, value bet frequency, illegal move rate, and opponent adaptation.
- Produce a unified multi-paradigm comparison table (CFR, Decision Transformer, ARDT, behavioral cloning, LLM agents) on Kuhn Poker with standardized metrics.

### 7.3 Step 13 — Behavioral Analysis Pipelines and Real-World Data

**Contribution Alignment.** This step will apply the behavioral adaptation methodology from Steps 7, 8, and 12 to anonymized industry data, providing practical validation for Contribution 1. The behavioral deviation from equilibrium play measured on real player data will quantify exploitation opportunities relevant to Contribution 2. The collusion detection^50^ module — transferring coalition detection principles from Step 11 to a practical fraud detection application — will represent a direct contribution to the evaluation methodology (Contribution 3).

**Literature.**

1. Wang et al. (2024). "player2vec: A Language Modeling Approach to Understand Player Behavior in Games." Preprint.
2. Kumar, A., Hong, J., Singh, A. and Levine, S. (2022). "When Should We Prefer Offline Reinforcement Learning Over Behavioral Cloning?" *Proceedings of the International Conference on Learning Representations (ICLR).*
3. DeLong and Bhatt (2020). "Towards Collusion Detection in Poker."
4. Yan and Browne (2016). "Collusion Detection in Online Poker."
5. Southey, F., Bowling, M., Larson, B., Piccione, C., Burch, N., Billings, D. and Rayner, C. (2005). "Bayes' Bluff: Opponent Modelling in Poker." *Proceedings of the 21st Conference on Uncertainty in Artificial Intelligence (UAI).*

**Practical Tasks.**

- Build a data pipeline from anonymized Playtech hand histories (~50,000–100,000 hands, cash game six-max tables) to structured game records and state tensors; validate for impossible states (duplicate cards, negative stacks, pot mismatches).
- Extend Step 12's poker state tensor encoding from Kuhn and Leduc to full Hold'em (52-dimensional one-hot card encoding, position, pot/stack ratios, betting history, street indicator, active player count).
- Compute standard behavioral statistics per player: VPIP^49^, PFR, Aggression Factor, WTSD, W\$SD, 3-bet percentage, and continuation bet percentage.
- Train player embeddings^48^ (player2vec approach) by treating poker actions as tokens and training a Transformer encoder with masked action prediction; extract per-player embedding vectors.
- Apply k-means clustering (four classic archetypes: tight-aggressive, loose-aggressive, tight-passive, loose-passive) and DBSCAN on the embedding space; validate against manual VPIP×PFR classification and test temporal stability.
- Implement a collusion detection^50^ module with three signals — co-occurrence anomaly, chip dumping score, and soft play score — combined via weighted composite scoring; validate by injecting synthetic collusion patterns and measuring detection recall (target >90%) and false positive rate (target <5%).
- Apply the Decision Transformer^46^ from Step 12 to Playtech data; compare return-conditioned versus EV-conditioned training per the Paster et al. stochasticity warning.

