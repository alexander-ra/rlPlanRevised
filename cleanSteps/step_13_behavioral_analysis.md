# Step 13 — Behavioral Analysis Pipelines + Real-World Data

**Duration:** 14 days · **Phase F:** Data-Driven Approaches · **Depends on:** Steps 7 (Opponent Modeling), 12 (Sequence Models + LLM Agents)

---

## Objective

Develop a complete pipeline for analyzing real-world poker behavioral data: parse Playtech hand histories into structured records, encode game states as tensors, compute player statistics, train behavioral cloning and embedding models, classify player styles via clustering, and prototype a collusion detection module.

**Core questions:**
1. What player archetypes emerge from real poker data, and how do they align with theoretical predictions?
2. Can Transformer-based player embeddings (player2vec approach) capture behavioral patterns that standard statistics miss?
3. What statistical signatures distinguish collusion from normal variance in multi-player poker?

---

## Literature

### Core

1. **Wang, Honari-Jahromi, Katsarou, Mikheeva, Panagiotakopoulos, Asadi & Smirnov** (2024). "player2vec: A Language Modeling Approach to Understand Player Behavior in Games." *arXiv:2404.04234*.
   - Transformer-based self-supervised learning on in-game behavior events. Produces player embeddings that cluster by behavioral patterns without labels.
   - **Relevance:** Directly validates the approach of treating poker actions as tokens and learning player representations from action sequences.

2. **Kumar, Hong, Singh & Levine** (2022). "When Should We Prefer Offline Reinforcement Learning Over Behavioral Cloning?" *International Conference on Learning Representations (ICLR)*.
   - Characterizes conditions under which offline RL outperforms behavioral cloning: sparse rewards, noisy/suboptimal data, long horizons.
   - **Relevance:** Poker data satisfies all three conditions. Provides theoretical grounding for pipeline design choices (BC as baseline, offline RL as upgrade path).

3. **DeLong & Bhatt** (2020). "Towards Collusion Detection in Poker."
   - Pattern-based collusion detection: information sharing, chip dumping, soft play.
   - **Relevance:** Foundational reference for the collusion detection module.

4. **Yan & Browne** (2016). "Collusion Detection in Online Poker."
   - Statistical approaches to identifying coordinated play.
   - **Relevance:** Provides statistical grounding and evaluation methodology for collusion detection.

5. **Southey, Bowling, Larson, Piccione, Burch, Billings & Rayner** (2005). "Bayes' Bluff: Opponent Modelling in Poker." *Conference on Uncertainty in Artificial Intelligence (UAI)*.
   - Bayesian player modeling from observed actions. Prior over player types, posterior refinement with data.
   - **Relevance:** Theoretical foundation for player modeling; player2vec automates what Bayesian inference does manually.

### Supplementary

6. **Kim, Park, Shin, Oh, Lim & Song** (2025). "A Framework for Mining Collectively-Behaving Bots in MMORPGs." *International Conference on Pattern Recognition (ICPR 2024)*. arXiv:2501.10461.
   - Trajectory representation learning + DBSCAN for detecting coordinated bot behavior.
   - **Relevance:** Methodological transfer — collective anomaly detection via embeddings + clustering applies directly to poker collusion.

7. **Garg, Chakraborty, Cundy, Song & Ermon** (2021). "IQ-Learn: Inverse soft-Q Learning for Imitation." *NeurIPS Spotlight*.
   - Inverse RL via soft Q-learning — learns reward functions from behavior data.
   - **Relevance:** Alternative to BC for learning from suboptimal poker data.

8. **Paster, McIlraith & Ba** (2022). "You Can't Count on Luck: Why Decision Transformers and Naive Return Conditioning Fail in Stochastic Environments."
   - Conditioning on outcomes in stochastic environments conflates luck and skill.
   - **Relevance:** Critical constraint for applying Decision Transformers to poker data (from Step 12 continuity).

---

## Methodology

### 1. Data Pipeline (Days 1–2)

- **Data source:** Anonymized Playtech hand histories (~50K–100K hands, cash game 6-max tables).
- **Parser:** Convert raw hand histories into structured records (hand ID, timestamp, players, actions by street, board cards, results).
- **Validation:** Check for impossible states (duplicate cards, negative stacks, pot mismatches).
- **State tensor encoding:** Extend Step 12's prototype from Kuhn/Leduc to full Hold'em — cards (one-hot 52-dim), position, pot/stack ratios, betting history, street indicator, active player count, stack-to-pot ratio.
- **Player statistics:** Compute standard behavioral metrics per player: VPIP, PFR, Aggression Factor, WTSD, W$SD, 3-bet %, C-bet %.

### 2. Behavioral Models (Days 3–4)

- **Behavioral cloning:** Train a neural network to predict human actions from game state. Evaluate accuracy by street, position, and player archetype.
- **player2vec embeddings:** Treat poker actions as tokens (position, street, action type, sizing bucket), concatenate hands per player, train a Transformer encoder with masked action prediction. Extract per-player embedding vectors.
- **Style classification:** Apply k-means (4 classic archetypes: TAG, LAG, Nit, Fish) and DBSCAN on embedding space. Validate against manual VPIP×PFR classification. Test temporal stability (same player, two time periods → same cluster?).

### 3. Collusion Detection (Day 5)

- **Detection signals:** Co-occurrence anomaly (pair frequency vs expected), chip dumping score (directional monetary transfer), soft play score (reduced aggression against specific opponents).
- **Composite scoring:** Weighted combination of three signals per player pair.
- **Validation:** Inject synthetic collusion patterns into data subset; measure detection recall and false positive rate.

### 4. Integration (Day 6)

- Apply Decision Transformer (from Step 12) to Playtech data. Compare return-conditioned (outcomes) vs EV-conditioned training per Paster et al. warning.
- Produce comparison table: player statistics vs behavioral cloning vs player2vec embeddings vs Decision Transformer across action prediction, style classification, and anomaly detection.

---

## Expected Outcomes

1. Working data pipeline from raw Playtech hand histories to structured game records and state tensors.
2. Behavioral cloning model with action prediction accuracy >55% (baseline: 14% random for 7 action types).
3. Player embedding space showing natural behavioral clusters matching known archetypes.
4. Collusion detection module achieving >90% recall on synthetic injected collusion with <5% false positive rate.
5. Empirical confirmation of Paster et al. stochasticity warning on real poker data.

---

## Connections

- **From Step 7:** Bayesian opponent model provides theoretical foundation; player2vec automates prior discovery.
- **From Step 8:** Safe exploitation theory quantifies the gap between real behavior and GTO play — the exploitation opportunity.
- **From Step 11:** Coalition detector (help/harm matrices in SLS) transfers to collusion detection (co-occurrence + chip dumping + soft play in poker).
- **From Step 12:** State tensor encoding prototype scales to full Hold'em. Paster et al. stochasticity warning constrains DT application.
- **To Step 14:** Evaluation metrics (action prediction accuracy, style classification, collusion precision/recall) feed into the formal evaluation framework.

---

## PhD Mapping

- **Contribution 1 (Behavioral Adaptation Framework):** The complete pipeline — state encoding, player embeddings, style classification, temporal tracking — IS the behavioral adaptation framework applied to real data. This step transforms the theoretical framework into a working system demonstrated on industry data.
- **Contribution 2 (Multi-Agent Safe Exploitation):** Real player data provides the empirical base for exploitation analysis. The behavioral deviation from Nash/GTO play (measured here) quantifies the exploitation opportunity that safe exploitation theory (Step 8) addresses.
- **Contribution 3 (Evaluation Methodology):** The collusion detection module is a direct methodological contribution. Few published solutions exist for poker collusion detection; this pipeline combines player embeddings, statistical signals, and coalition detection principles into a novel approach.
- **Publication candidate:** Pipeline + Playtech case study suitable for IEEE Transactions on Games, AAAI Workshop, or similar venue. Title direction: "Behavioral Analysis and Collusion Detection in Online Poker via Transformer-Based Player Embeddings."
> **[P8] Change-Point Detection for collusion:** Add Bayesian online changepoint detection (Adams & MacKay 2007) as a signal in the collusion detection composite score. Same algorithm from Step 7 applied to detect collusion onset / bot behavior changes in player timelines. ~0.5d absorbed within 14d allocation.

> **[P10] GAIL/IRL Fallback:** If behavioral cloning accuracy < 55% on action prediction, explore **IQ-Learn** (Garg et al., 2021) as an inverse RL alternative. IQ-Learn is already in supplementary references — this promotes it to documented Plan B.
