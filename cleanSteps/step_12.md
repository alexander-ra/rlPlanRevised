# Step 12 — Sequence Models + LLM Agents in Strategic Settings

**Duration:** 10 days (Tier 3)  
**Dependencies:** Step 5 (Neural Equilibrium Approximation), Step 7 (Opponent Modeling)  
**Phase:** F — Data-Driven Approaches  

---

## Objectives

1. Study the Decision Transformer architecture and understand how reinforcement learning can be reformulated as conditional sequence generation, where the transformer predicts actions conditioned on desired future returns and state history.
2. Analyze the fundamental limitations of return-conditioned sequence models in stochastic environments (the luck-vs-skill problem), which directly impacts applicability to card games and real-world poker data.
3. Implement and evaluate the Adversarially Robust Decision Transformer (ARDT), which recovers minimax (Nash Equilibrium) strategies from offline game data by conditioning on worst-case returns-to-go via expectile regression.
4. Survey the emerging field of LLM agents in strategic game settings, covering natural-language-based game playing, theory-of-mind reasoning, and multi-agent interaction through platforms such as TextArena.
5. Evaluate LLM strategic reasoning capabilities on Kuhn Poker against known Nash equilibrium baselines, measuring exploitability, bluff frequency, and opponent adaptation.
6. Build the poker state tensor encoding that will serve as the foundation for the Playtech behavioral analysis pipeline in Step 13, prototyping on synthetic Kuhn/Leduc data.
7. Produce a comparative evaluation of multiple paradigms — equilibrium-based (CFR), sequence-model-based (DT, ARDT), supervised (behavioral cloning), and language-model-based — on the same benchmark game with standardized metrics.

---

## Key Topics

- Decision Transformer: reformulating offline RL as return-conditioned sequence prediction using GPT-2 architecture over (return-to-go, state, action) token sequences
- Trajectory Transformer: offline RL as full-sequence modeling with beam search planning (Janner et al., 2021)
- Stochasticity limitations: why return conditioning conflates luck with skill in stochastic environments (Paster, McIlraith & Ba, 2022)
- Adversarially Robust Decision Transformer (ARDT): minimax expectile regression for worst-case return conditioning, recovering Nash Equilibrium from offline data (Tang et al., 2024)
- Conservative Q-Learning (CQL): value-based offline RL baseline using pessimistic Q-function estimation (Kumar et al., 2020)
- LLM agents in strategic games: natural-language game playing, in-context strategic reasoning, theory-of-mind inference
- TextArena: benchmark platform with 57+ competitive text-based games for LLM agent evaluation (Guertler et al., 2025)
- LLM-game integration architectures: CICERO's language model + strategic planner combination (Meta AI, 2022), SpinGPT's LLM + CFR hybrid (Maugin & Cazenave, 2025)
- Poker state tensor encoding: fixed-dimensional representation of game state (cards, position, pot, stacks, betting history) for sequence model input

---

## Literature

### Core References

1. **Chen, L., Lu, K., Rajeswaran, A., Lee, K., Grover, A., Laskin, M., Abbeel, P., Srinivas, A. & Mordatch, I.** (2021). *Decision Transformer: Reinforcement Learning via Sequence Modeling.* In Proc. NeurIPS 2021. arXiv:2106.01345.  
   — Reformulates offline RL as conditional sequence generation. A GPT-2 backbone predicts actions from (return-to-go, state, action) token sequences. Matches or exceeds value-based offline RL on Atari and MuJoCo benchmarks without temporal-difference learning or Bellman backups. Foundation for applying sequence models to game trajectory data.

2. **Paster, K., McIlraith, S. & Ba, J.** (2022). *You Can't Count on Luck: Why Decision Transformers and RvS Fail in Stochastic Environments.* arXiv:2205.15967.  
   — Proves that return-conditioned policies are suboptimal in stochastic environments: conditioning on high returns selects for lucky trajectories rather than skilled decisions. Provides formal bounds on suboptimality (Theorem 2.1). Critical limitation for applying Decision Transformers to poker and card game data, where outcome variance is dominated by card deals rather than strategic quality.

3. **Tang, X., Marques, A., Kamalaruban, P. & Bogunovic, I.** (2024). *Adversarially Robust Decision Transformer.* In Proc. NeurIPS 2024. arXiv:2407.18414.  
   — Addresses DT's vulnerability in adversarial settings by conditioning on minimax returns-to-go via expectile regression. In sequential games with full data coverage, ARDT recovers Nash Equilibrium strategies. Demonstrates superior worst-case robustness compared to standard DT methods in large-scale games and continuous adversarial RL environments.

4. **Janner, M., Li, Q. & Levine, S.** (2021). *Offline Reinforcement Learning as One Big Sequence Modeling Problem.* In Proc. NeurIPS 2021. arXiv:2106.02039.  
   — Trajectory Transformer: models states, actions, and rewards jointly as a single token sequence, using beam search at inference for planning. Complements Decision Transformer by adding explicit planning capability via sequence-level search, conceptually analogous to Monte Carlo Tree Search.

5. **Guertler, L., Cheng, B., Yu, S., Liu, B., Choshen, L. & Tan, C.** (2025). *TextArena.* arXiv:2504.11442.  
   — Open-source collection of 57+ competitive text-based games for LLM agent evaluation, spanning negotiation, deception, theory of mind, and strategic reasoning. Uses TrueSkill scoring for real-time leaderboard comparison across models. Addresses the evaluation gap for dynamic social intelligence capabilities that classical game-theoretic benchmarks do not capture.

### Supplementary References

6. **Kumar, A., Zhou, A., Tucker, G. & Levine, S.** (2020). *Conservative Q-Learning for Offline Reinforcement Learning.* In Proc. NeurIPS 2020. arXiv:2006.04779.  
   — Value-based offline RL using pessimistic Q-function estimation. Penalizes Q-values for out-of-distribution actions. Handles stochasticity more gracefully than return-conditioned methods. Serves as the primary value-based baseline for comparison with sequence model approaches.

7. **Zhang, X., Zheng, H., Lv, A., Liu, Y., Song, Z., Chen, X., Yan, R. & Sung, F.** (2025). *Divide-Fuse-Conquer: Eliciting "Aha Moments" in Multi-Scenario Games.* arXiv:2505.16401.  
   — RL fine-tuning of LLMs across 18 TextArena games using a divide-train-fuse strategy. Qwen2.5-32B trained with this approach reaches performance comparable to Claude 3.5. State-of-the-art methodology for training LLM game agents.

8. **Guo, J. et al.** (2023). *Suspicion-Agent: Playing Imperfect Information Games with Theory of Mind Aware GPT-4.* arXiv:2309.17277.  
   — GPT-4 agent with explicit theory-of-mind planning for deception-heavy games (Werewolf, Avalon). Demonstrates that LLM strategic reasoning improves when augmented with structured belief modeling of other players' mental states. Connects LLM agents to the explicit opponent modeling methodology of Step 7.

9. **Meta AI** (2022). *Human-Level Play in the Game of Diplomacy by Combining Language Models with Strategic Reasoning* (CICERO). Science, 378(6624), 1067–1074.  
   — Integrates a language model for natural-language negotiation with a game-theoretic planner for strategic move selection in 7-player Diplomacy. The most complete demonstration of combining LLM capabilities with formal game-solving methods. Architecture reference for hybrid LLM-game AI systems.

10. **Lee, K.-H., Nachum, O., Yang, M., Lee, L., Freeman, D., Xu, W., Guadarrama, S., Fischer, I., Jang, E., Michalewski, H. & Mordatch, I.** (2022). *Multi-Game Decision Transformers.* In Proc. NeurIPS 2022. arXiv:2205.15241.  
    — Single Decision Transformer trained across 46 Atari games, demonstrating generalist agent capability. Proof of concept for multi-domain sequence model competence. Relevant for understanding scalability of the DT paradigm beyond single-task settings.

---

## Methodology

Following the 5-phase learning cycle (Tier 3, 10-day allocation):

| Phase | Duration | Focus |
|-------|----------|-------|
| Intuition | 1 day | Two paradigms: sequence models for offline RL, LLM agents in strategic games |
| Exploration | 1 day | Run Decision Transformer on game data, test LLM agent on TextArena and Kuhn Poker |
| Targeted Reading | 2 days | Core papers: Decision Transformer → stochasticity limits → ARDT → TextArena → Trajectory Transformer |
| Implementation | 4 days | Poker DT data pipeline, DT training, ARDT implementation, LLM evaluation, comparison analysis |
| Consolidation | 2 days | Survey integration, PhD mapping, learning log, one-pager |

### Implementation Plan

1. **Poker trajectory dataset:** Generate 50K+ Kuhn Poker trajectories using CFR agents from Step 3. Design the poker state tensor encoding (cards, position, pot, stacks, betting history) that will carry to the Playtech data pipeline in Step 13.
2. **Decision Transformer training:** Adapt HuggingFace Decision Transformer for poker state/action spaces. Validate return-to-go conditioning (high return → better play). Demonstrate the stochasticity limitation from Paster et al. (2022): DT conflates lucky cards with skilled play.
3. **ARDT implementation:** Implement minimax expectile regression for adversarially robust return conditioning. Train on mixed-quality opponent data and verify that ARDT recovers near-Nash strategies on Kuhn Poker (measured by exploitability against the known Nash equilibrium from Step 2).
4. **TextArena LLM evaluation:** Deploy LLM agents on TextArena strategic games to assess capabilities in negotiation, deception, and theory of mind — the social intelligence dimensions that formal game-theoretic methods do not capture.
5. **Kuhn Poker LLM evaluation:** Test LLM agents on Kuhn Poker with standardized metrics: exploitability (computed against known Nash), bluff frequency, value bet frequency, illegal move rate, and opponent adaptation. Compare against the known Nash equilibrium.
6. **Comparative analysis:** Produce a unified comparison table spanning all paradigms (CFR, DT, ARDT, behavioral cloning, LLM) on Kuhn Poker with standardized metrics, establishing the evaluation methodology prototype for Step 14.

---

## PhD Alignment

**Contribution #1 — Behavioral Adaptation Framework:** The poker state tensor encoding (cards, position, pot size, stack sizes, betting history) designed in this step is the foundational representation for the behavioral adaptation framework. The same encoding transfers directly to the Playtech data pipeline (Step 13), determining what behavioral patterns can be detected and modeled. This step prototypes the encoding on synthetic small-game data.

**Contribution #2 — Multi-Agent Safe Exploitation:** ARDT demonstrates that minimax (safe) strategies can emerge from offline data without explicit game-theoretic computation such as CFR iteration. This opens an alternative path for Contribution #2: learning safe exploitation strategies directly from behavioral data rather than computing Nash equilibria (which is intractable in N-player settings, as established in Step 11). The minimax return conditioning is the offline analog of the online safe exploitation theory from Step 8.

**Contribution #3 — Evaluation Methodology:** The comparison table (CFR vs DT vs ARDT vs behavioral cloning vs LLM agents, all on Kuhn Poker with standardized metrics) is a microcosm of the evaluation framework proposed in Contribution #3. Multiple agent architectures, same game, standardized metrics (exploitability, behavioral statistics). This prototype methodology scales to the comprehensive evaluation framework in Step 14.

**Bridge to Step 13:** The trajectory dataset format, state tensor encoding, and DT training pipeline all transfer directly to Playtech's anonymized hand history data. Step 12 builds the prototype on synthetic data; Step 13 applies it to real-world poker data. The stochasticity warning from Paster et al. (2022) directly constrains Step 13's design: condition on decision expected value, not raw outcomes.

**Bridge to Step 14:** The multi-paradigm comparison methodology prototyped here (formal vs learned vs language-based agents) feeds into the comprehensive evaluation framework design of Step 14.

---

## Expected Outputs

1. Poker trajectory dataset (50K+ Kuhn Poker hands) with thesis-relevant state tensor encoding
2. Decision Transformer trained on Kuhn Poker with validated return-to-go conditioning
3. Stochasticity experiment demonstrating the luck-vs-skill limitation on poker data
4. ARDT implementation with minimax expectile regression, producing near-Nash play on Kuhn Poker
5. TextArena LLM agent evaluation on at least one strategic game
6. Kuhn Poker LLM evaluation with standardized metrics (exploitability, bluff frequency, opponent adaptation)
7. Multi-paradigm comparison table: CFR vs DT vs ARDT vs behavioral cloning vs LLM on Kuhn Poker
8. Documented poker state tensor encoding specification for reuse in Step 13
9. One-page summary document
10. Updated learning log with cross-step connections and open research questions
