# Step 12 — Sequence Models + LLM Agents in Strategic Settings

**Duration:** 10 days (Tier 3)  
**Dependencies:** Step 5 (Neural Equilibrium Approximation), Step 7 (Opponent Modeling)  
**Phase:** F — Data-Driven Approaches  
**Freshness Note:**  
- ArXiv search: "Decision Transformer offline reinforcement learning game" sorted by date (Jun 2026) — 9 results. Key finds:  
  - Tang, Marques, Kamalaruban & Bogunovic (Jul 2024, NeurIPS 2024) "Adversarially Robust Decision Transformer" (arXiv:2407.18414) — **directly relevant.** Proposes ARDT: worst-case-aware offline RL via minimax expectile regression on returns-to-go. In sequential games with full data coverage, ARDT recovers Nash Equilibrium strategies. *Core — the first DT variant explicitly designed for adversarial/game settings. Bridges Decision Transformer to game-theoretic equilibrium.*  
  - Tatematsu & Wachi (Mar 2025) "Target Return Optimizer for Multi-Game Decision Transformer" (arXiv:2503.02311) — target return optimization for generalist agents across diverse games. *Supplementary — multi-game DT relevant for generalization.*  
  - Paster, McIlraith & Ba (May 2022) "You Can't Count on Luck: Why Decision Transformers and RvS Fail in Stochastic Environments" (arXiv:2205.15967) — *Critical warning paper.* Shows DT struggles in stochastic environments because conditioning on high returns selects for lucky trajectories, not skilled ones. Poker/card games are stochastic by nature. *Core — must understand this limitation before applying DT to poker.*  
  - Lee et al. (May 2022, NeurIPS 2022) "Multi-Game Decision Transformers" (arXiv:2205.15241) — trains single DT across 46 Atari games. *Supplementary — proof of concept for generalist agents.*  
  - Batth et al. (Apr 2025) "Do We Need Transformers to Play FPS Video Games?" (arXiv:2504.17891) — compares DT architectures for FPS games. *Tangential — note for awareness.*  
- ArXiv search: "TextArena language game" (Jun 2026) — 3 results:  
  - Guertler, Cheng, Yu, Liu, Choshen & Tan (Apr 2025) "TextArena" (arXiv:2504.11442) — **the benchmark.** 57+ competitive text-based games for LLM agent evaluation: negotiation, deception, theory of mind. TrueSkill scoring. *Core — this is the plan's designated LLM game testbed.*  
  - Zhang et al. (May 2025) "Divide-Fuse-Conquer: Eliciting 'Aha Moments' in Multi-Scenario Games" (arXiv:2505.16401) — RL fine-tuning of LLMs across 18 TextArena games. Qwen2.5-32B reaches Claude 3.5-level via divide-train-fuse strategy. *Supplementary — state-of-the-art on LLM game training as of 2025.*  
  - Lou et al. (Feb 2026) "AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness" (arXiv:2603.03329) — synthesizes code harnesses for LLM agents in game environments. *Supplementary — practical tool for LLM agent development.*  
- Known foundational papers (not found via keyword search):  
  - Chen et al. (Jun 2021, NeurIPS 2021) "Decision Transformer: Reinforcement Learning via Sequence Modeling" (arXiv:2106.01345) — the seminal DT paper. *Core.*  
  - Janner, Li & Levine (Jun 2021, NeurIPS 2021) "Offline Reinforcement Learning as One Big Sequence Modeling Problem" (arXiv:2106.02039) — Trajectory Transformer. *Core.*  
  - Kumar, Zhou, Tucker & Levine (Jun 2020, NeurIPS 2020) "Conservative Q-Learning for Offline Reinforcement Learning" (arXiv:2006.04779) — CQL baseline. *Supplementary — the value-based alternative to sequence modeling.*  
  - Meta AI (Nov 2022) "Human-Level Play in the Game of Diplomacy by Combining Language Models with Strategic Reasoning" (CICERO). Science, 378(6624). — LLM + strategic planning. *Already covered in Step 11; reference for continuity.*  
  - Maugin & Cazenave (Sep 2025, ACG 2025) "SpinGPT: A Large-Language-Model Approach to Playing Poker Correctly" — LLM + CFR hybrid for poker. *Logged from Step 5 freshness scan. Supplementary.*  
  - Guo et al. (Sep 2023) "Suspicion-Agent: Playing Imperfect Information Games with Theory of Mind Aware GPT-4" (arXiv:2309.17277) — GPT-4 with theory-of-mind planning for Werewolf and Avalon. *Supplementary.*  
- Cross-reference from Step 11: CICERO, Welfare Diplomacy (Mukobi et al., 2023) as LLM+strategy prior art. Step 11 freshness note flagged SpinGPT for this step.  
- Cross-reference from Step 5: SpinGPT was logged in Step 5's freshness scan as "reserve for Step 12."  
- Field assessment: **Sequence models for strategic decision-making = established (DT, 2021) but with known stochasticity gaps (Paster et al., 2022). LLM agents in games = extremely young field (TextArena Apr 2025, Divide-Fuse-Conquer May 2025). The plan architecture correctly assessed Tier 3: survey-dominant, the field is too young for more than a focused implementation exercise + literature mapping.**

---

## Phase 1: Intuition (1 day)

The goal: understand TWO distinct but converging paradigms:

**Paradigm A — Sequence Modeling for Offline RL (Decision Transformer):** Instead of learning a value function like Q-learning, what if you reformulate RL as a SEQUENCE prediction problem? Given a history of (state, action, reward) triples, predict the next action — conditioned on the DESIRED future return. The transformer architecture handles this naturally: it's already designed to predict the next token given a sequence. The breakthrough insight: you can train on a static dataset of past games (no environment interaction needed), and at test time, you simply condition on "I want high reward" and the model produces good actions.

**Paradigm B — LLM Agents in Strategic Games:** What if you give a powerful language model (GPT-4, Claude, etc.) the rules of a game in natural language and let it PLAY? No RL training, no game tree search — just prompt engineering, in-context learning, and reasoning. This is radically different from everything in Steps 1–11. It works shockingly well in some settings (Diplomacy via CICERO) and fails embarrassingly in others (simple logical games). The key question: WHERE does LLM strategic reasoning work, where does it fail, and can it be COMBINED with game-theoretic methods?

End of day: you should be able to explain to a non-expert: "There are two ways to use modern AI for game playing beyond classical RL. First, you can treat game histories as text sequences and train a transformer to predict good moves — this is the Decision Transformer approach. Second, you can just ask a large language model like GPT-4 to play a game by giving it the rules in plain English — and sometimes it plays surprisingly well, especially in games involving negotiation and deception. Both approaches have serious limitations: the sequence model struggles with luck-based games, and the LLM sometimes makes illegal moves or terrible strategic blunders. The frontier research question is how to combine these approaches with the game-theoretic methods we've already studied."

### Videos

- **Lilian Weng — "Decision Transformer / Offline RL as Sequence Modeling"**  
  https://www.youtube.com/watch?v=w4Bw8WYL8Ps  
  Duration: ~30m  
  *Clear walkthrough of the Decision Transformer architecture. Watch for: how return-to-go conditioning works, how the positional encoding captures time, and the comparison with traditional RL.*

- **Noam Brown — "CICERO: An AI agent that negotiates, persuades, and cooperates with people"**  
  https://www.youtube.com/watch?v=u5_BHosc7bE  
  Duration: ~20m | Speaker: Noam Brown (Meta AI)  
  *Already watched in Step 11 for coalition dynamics. RE-WATCH with a different lens: this time focus on the LANGUAGE MODEL component. How does CICERO use a language model for negotiation? How is the LM output constrained by the strategic planner? This is the most successful LLM+game integration to date.*

- **Yannic Kilcher (or similar) — "Decision Transformer" paper review**  
  Search YouTube: "Decision Transformer Yannic Kilcher" or "Decision Transformer explained"  
  Duration: ~20m  
  *Deeper dive into the technical details: tokenization of (return, state, action) triples, how GPT-2 architecture is adapted, key ablations.*

### Blog Posts / Accessible Reads

- **Lilian Weng — "The Prompt Report: A Systematic Survey of Prompting Techniques" (blog)**  
  https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/  
  *Background on prompt engineering techniques that LLM game agents rely on: chain-of-thought, in-context learning, role prompting. You'll need this to understand how TextArena agents are constructed.*

- **TextArena documentation & leaderboard**  
  https://www.textarena.ai/  
  https://github.com/LeonGuertler/TextArena  
  *Browse the games list: 57+ environments spanning negotiation, deception, strategy. Check the TrueSkill leaderboard: which LLMs dominate? Which game types are hardest? This gives you the landscape.*

- **Hugging Face Blog — "Decision Transformer" tutorial**  
  https://huggingface.co/blog/decision-transformers  
  *Hands-on tutorial with code. Good for getting a quick implementation running before diving into the papers.*

---

## Phase 2: Exploration (1 day)

### Morning: Decision Transformer on a Game Task

1. **Run the HuggingFace Decision Transformer example:**
   ```bash
   pip install transformers datasets torch
   ```
   - Use the `edbeeching/decision_transformer_gym_replay` dataset on HuggingFace
   - Train a DT on Atari or MuJoCo if compute allows; otherwise use the pre-trained checkpoint
   - **Key experiment:** Vary the return-to-go conditioning:
     - Condition on low return → observe: DT should produce poor play
     - Condition on medium return → observe: DT should produce average play
     - Condition on high return → observe: DT should produce good play
     - **Condition on IMPOSSIBLE return** (higher than ever seen in data) → observe: what happens? Does DT extrapolate or collapse? This is the critical limitation (see Paster et al., 2022)

2. **Hands-on with stochasticity:**
   - If possible, run DT on a stochastic environment (e.g., a simple card game if available, or add noise to a deterministic environment)
   - Observe: does conditioning on high return produce genuinely skilled play, or does it just reproduce lucky trajectories? This is the fundamental problem flagged by Paster et al.

### Afternoon: LLM Agent on TextArena

3. **Set up TextArena:**
   ```bash
   pip install textarena
   ```
   - Browse available games: `textarena.list_games()`
   - Pick a simple strategic game (e.g., a negotiation or deduction game)
   - Play a game manually (human vs LLM) to understand the interface
   - **Key experiment:** Run GPT-4 (or Claude, or an open model) against a random baseline:
     - Does the LLM understand the rules? (Check for illegal move attempts)
     - Does the LLM reason strategically? (Look for evidence of planning, bluffing, theory of mind)
     - Does the LLM adapt to opponent behavior? (Play multiple rounds — does it exploit patterns?)
   - **Connection to Step 7:** Compare the LLM's implicit opponent modeling (in-context) with the explicit Bayesian opponent model from Step 7. Which is more systematic? Which is more flexible?

4. **Quick sanity check — LLM on Kuhn Poker:**
   - Write a simple Kuhn Poker text interface (you have the environment from Step 2)
   - Prompt an LLM to play Kuhn Poker. Does it discover that bluffing with a Jack is sometimes optimal? Does it understand the information asymmetry?
   - This connects ALL of Steps 2–8 to the LLM paradigm: you know the Nash equilibrium for Kuhn Poker. Can an LLM find it through REASONING alone, without training?

---

## Phase 3: Targeted Reading (2 days)

### Paper 1: Chen, Lu, Rajeswaran, Lee, Grover, Laskin, Abbeel, Srinivas & Mordatch — "Decision Transformer: Reinforcement Learning via Sequence Modeling" (2021)
**Link:** https://arxiv.org/abs/2106.01345

- **READ:** Sections 1–3 (Introduction, Preliminaries, Decision Transformer)
  - KEY INSIGHT: RL reformulated as conditional sequence generation. The return-to-go token replaces the reward-maximization objective.
  - Architecture: GPT-2 backbone, input = (R̂₁, s₁, a₁, R̂₂, s₂, a₂, ...). Each modality (return, state, action) gets its own embedding + learned positional encoding.
  - Training: standard cross-entropy / MSE loss on action prediction, conditioned on return-to-go and state history.
- **READ:** Section 4 (Experiments) — Table 1 especially
  - DT matches or exceeds CQL and behavior cloning on offline Atari and MuJoCo tasks
  - KEY OBSERVATION: DT is competitive without any temporal difference learning, Bellman backup, or value function. Pure supervised learning on (state, action, return) sequences.
- **SKIM:** Section 5 (Discussion)
- **SKIP:** Appendix details on specific environments (unless you're replicating)
- **PhD Connection:** The state representation (cards, position, pot, stacks, betting history) from the original docPlan maps directly to the DT input tokenization. Hand histories become sequences. Return-to-go = desired winrate. This is the *architecture* for Step 13's Playtech behavioral cloning.

### Paper 2: Paster, McIlraith & Ba — "You Can't Count on Luck" (2022)
**Link:** https://arxiv.org/abs/2205.15967

- **READ:** Sections 1–3 (Introduction, Problem formulation, Theoretical results)
  - KEY INSIGHT: In stochastic environments, high-return trajectories often OVERREPRESENT lucky outcomes rather than skilled decisions. Conditioning DT on high return-to-go amplifies luck, not skill.
  - Theorem 2.1: formal bound on suboptimality of return-conditioned policies in stochastic MDPs.
- **READ:** Section 4 (Experiments)
  - Coin-flip MDP experiment: DT learns to predict "heads" (lucky), not the optimal strategy
  - Stochastic offline RL environments: DT significantly underperforms CQL when stochasticity is high
- **SKIM:** Section 5 (Related work)
- **MATH:** 🔢 Work through Theorem 2.1 with pen and paper. This is the formal reason why DT on poker (a stochastic game) requires careful modifications.
- **PhD Connection:** CRITICAL. Poker hand histories are highly stochastic (card deals). A naive DT trained on Playtech data will associate "good outcomes" with "lucky cards," not "good strategy." The fix: condition on STRATEGIC quality metrics (e.g., EV of decisions) rather than raw win/loss. This insight shapes the Step 13 data pipeline design.

### Paper 3: Tang, Marques, Kamalaruban & Bogunovic — "Adversarially Robust Decision Transformer" (2024, NeurIPS 2024)
**Link:** https://arxiv.org/abs/2407.18414

- **READ:** Sections 1–3 (Introduction, Preliminaries, ARDT method)
  - KEY INSIGHT: In adversarial games, the return-to-go is not just a function of your policy — it depends on the OPPONENT's strategy. ARDT conditions on MINIMAX returns-to-go: the best return achievable against the WORST-CASE opponent.
  - Minimax expectile regression: learns both "what is the best I can do" and "what is the worst my opponent can do" from offline data.
- **READ:** Section 4 (Experiments)
  - Sequential games with full data coverage: ARDT produces Nash Equilibrium strategies!
  - Continuous adversarial RL + large games with partial coverage: ARDT achieves highest worst-case returns
- **SKIM:** Proofs / detailed math (only work through if time permits)
- **PhD Connection:** ARDT connects Step 5 (equilibrium computation) to the sequence model paradigm. If Nash can emerge from offline sequence modeling with the right conditioning, this may provide an alternative path to equilibrium strategies that doesn't require CFR at all. Direct bridge: Step 5's Deep CFR vs Step 12's ARDT — two roads to the same destination?

### Paper 4: Guertler, Cheng, Yu, Liu, Choshen & Tan — "TextArena" (2025)
**Link:** https://arxiv.org/abs/2504.11442

- **READ:** Entire paper (5 pages — short)
  - 57+ competitive text-based game environments  
  - TrueSkill scoring system for LLM evaluation
  - Game categories: negotiation, deception, theory of mind, strategy
  - Which LLMs perform best? On which game types?
- **KEY OBSERVATION:** TextArena tests *social* intelligence (negotiation, deception) — the exact capabilities that game-theoretic methods DON'T capture. This is the complement to your CFR/MARL toolkit: formal methods handle exploitability and equilibrium, LLMs handle negotiation and persuasion.
- **PhD Connection:** TextArena games map to "soft" strategic settings where behavioral signals matter more than equilibrium computation. This connects to Step 7's opponent modeling: can an LLM's in-context "model" of the opponent complement or replace explicit Bayesian inference?

### Paper 5: Janner, Li & Levine — "Offline Reinforcement Learning as One Big Sequence Modeling Problem" (2021)
**Link:** https://arxiv.org/abs/2106.02039

- **READ:** Sections 1–3 (Introduction, discretization, Trajectory Transformer architecture)
  - KEY DIFFERENCE from DT: Trajectory Transformer (TT) models EVERYTHING as tokens — states, actions, AND rewards — and uses beam search at inference time instead of simple conditioning.
  - TT can do PLANNING (via beam search over future trajectories), while DT does only generation.
- **SKIM:** Experiments on MuJoCo benchmarks
- **SKIP:** Detailed ablations
- **PhD Connection:** Beam search over game trajectories is conceptually similar to Monte Carlo Tree Search (Steps 3–4). The sequence model world is converging with the game AI world. TT's planning via beam search connects to ReBeL's search (Step 6) — both search over future sequences to find good actions.

### Supplementary Reading (skim as time permits):

- **Kumar et al. (2020) — "Conservative Q-Learning"** (arXiv:2006.04779): The value-based offline RL baseline. SKIM Section 3 (CQL penalties) to understand the alternative to sequence modeling. You need to know when CQL > DT and vice versa.

- **Zhang et al. (2025) — "Divide-Fuse-Conquer"** (arXiv:2505.16401): State-of-the-art LLM game training on TextArena. SKIM for: how they partition games by difficulty, how model merging works, what performance level Qwen2.5-32B achieves vs Claude 3.5.

- **Guo et al. (2023) — "Suspicion-Agent"** (arXiv:2309.17277): GPT-4 with theory-of-mind planning for Werewolf and Avalon. SKIM for: the planning module architecture — it explicitly models other players' beliefs, connecting to Step 7's opponent modeling.

### Math Flags:

🔢 **Paster et al. Theorem 2.1** — Work through with pen and paper. Understand the formal bound on return-conditioned policy suboptimality in stochastic MDPs. This is the mathematical reason why naive DT on poker data will fail.  
**WHY this can't be substituted by algorithmic understanding:** The theorem directly constrains what information you can extract from poker hand history data — it tells you the gap between "best outcome" (lucky) and "best strategy" (skilled). Without this, you'll misinterpret DT results on Playtech data.

🔢 **ARDT minimax expectile regression** — Understand how expectile regression at different quantiles captures best-case and worst-case returns from the same offline dataset. This is a specific statistical technique (not standard ML) that you need to understand for the implementation.  
**WHY this can't be substituted by algorithmic understanding:** This is a specific loss function modification — you need to implement it correctly, and understanding the math ensures you get the quantile semantics right.

---

## Phase 4: Implementation (4 days)

### Project: Decision Transformer for Kuhn/Leduc Poker + LLM Agent Evaluation on TextArena

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| Kuhn Poker DT data pipeline (state encoding) | 🔴 HAND-CODE | The state representation is thesis-critical — same tensor design carries to Playtech data. Must deeply understand each feature. |
| Decision Transformer training loop | 🟡 AI-ASSISTED | Use HuggingFace DT implementation as base, adapt for poker state/action spaces. Understand the architecture but don't rewrite the transformer from scratch. |
| ARDT minimax return conditioning | 🔴 HAND-CODE | The minimax expectile regression is the novel component — must implement the loss function yourself to understand the adversarial conditioning. |
| TextArena LLM agent wrapper | 🟢 AI-GENERATED | Boilerplate API integration code — no deep understanding needed for wrapper/prompt formatting. |
| LLM strategic reasoning evaluation | 🔴 HAND-CODE | Designing evaluation metrics for LLM game play (illegal moves, strategic quality, opponent adaptation) requires domain expertise from Steps 2–7. |
| Comparison analysis + visualizations | 🟡 AI-ASSISTED | Analysis code with manual interpretation of results. |

**Day 1 — Kuhn/Leduc Decision Transformer: Data Pipeline**

- 🔴 Build the data pipeline for offline RL on poker:
  ```python
  class PokerTrajectoryDataset:
      """Convert poker game histories into Decision Transformer input format.
      
      Each trajectory = one complete hand (deal → betting rounds → showdown).
      Tokenization: (return-to-go, state, action) triples per decision point.
      
      State representation (will carry to Playtech in Step 13):
        - cards: one-hot encoding of hole cards (2 for Kuhn, 2 for Leduc)
        - board: one-hot encoding of community cards (0 for Kuhn, 1 for Leduc)
        - position: binary indicator (dealer/non-dealer)
        - pot: normalized pot size (pot / starting_stack)
        - stack: normalized remaining stack
        - betting_history: sequence of actions encoded as integers
                           (fold=0, check=1, call=2, bet=3, raise=4)
        - round_flag: current betting round (preflop/postflop)
      """
      
      def __init__(self, game_type='kuhn', n_trajectories=50000):
          self.game_type = game_type
          self.trajectories = []
          self.generate_data(n_trajectories)
      
      def generate_data(self, n):
          """Generate trajectories by running trained CFR agents (from Step 3)
          against each other. This gives near-Nash data — the quality of data
          matters for DT training."""
          # Use your CFR solver from Step 3 to generate strategy profiles
          # Play games using those profiles, record full trajectories
          for _ in range(n):
              trajectory = self.play_one_hand()
              self.trajectories.append(trajectory)
      
      def encode_state(self, game_state):
          """Encode game state as a fixed-dim tensor.
          THIS IS THE CRITICAL FUNCTION — same encoding will be reused 
          on Playtech data in Step 13."""
          cards_enc = self.encode_cards(game_state.hole_cards)
          board_enc = self.encode_cards(game_state.board_cards)
          position = [1.0 if game_state.is_dealer else 0.0]
          pot = [game_state.pot / game_state.starting_stack]
          stack = [game_state.stack / game_state.starting_stack]
          history = self.encode_history(game_state.action_sequence)
          round_flag = self.encode_round(game_state.current_round)
          return np.concatenate([cards_enc, board_enc, position, 
                                  pot, stack, history, round_flag])
      
      def compute_return_to_go(self, trajectory, timestep):
          """Return-to-go = sum of future rewards from this point.
          For poker: reward = final payoff (positive or negative chips won).
          WARNING (Paster et al.): this conflates skill with luck.
          Future work (Step 13): replace with EV-based returns."""
          return sum(r for _, _, r in trajectory[timestep:])
  ```
- Generate 50K+ Kuhn Poker trajectories using your CFR agent from Step 3
- Generate 50K+ Leduc Poker trajectories if time permits
- Verify data quality: distribution of returns should match known game values

**Day 2 — Decision Transformer Training on Poker**

- 🟡 Adapt the HuggingFace Decision Transformer for poker:
  ```python
  from transformers import DecisionTransformerConfig, DecisionTransformerModel
  
  config = DecisionTransformerConfig(
      state_dim=STATE_DIM,        # Your state encoding dimension
      act_dim=ACTION_DIM,         # Number of poker actions
      max_length=20,              # Max timesteps per hand (poker hands are short)
      max_ep_len=20,
      hidden_size=128,            # Smaller than default — poker is a small game
      n_layer=3,
      n_head=4,
      activation_function='relu',
  )
  model = DecisionTransformerModel(config)
  ```
- Train the DT on your Kuhn Poker data
- **Key experiments:**
  1. **Return conditioning test:** Generate actions at different return-to-go levels
     - High return-to-go: does DT play closer to Nash?
     - Low return-to-go: does DT play worse? (It should — this validates conditioning works)
  2. **Stochasticity test (Paster et al.'s warning):**
     - Train on mixed data: near-Nash play + random play
     - Condition on high return → does DT learn Nash strategy or lucky card selection?
     - Measure: action prediction accuracy BY CARD — if DT's "good play" depends on the card rather than the situation, it's learning luck, not skill
  3. **Comparison with behavioral cloning:**
     - Simple BC: predict action from state (no return conditioning)
     - DT: predict action from (return-to-go, state history)
     - Are they different on Kuhn Poker? (Expected: minimal difference on small games, larger difference on Leduc)

**Day 3 — ARDT Implementation for Adversarial Poker**

- 🔴 Implement the minimax return-to-go conditioning from ARDT:
  ```python
  class AdversariallyRobustDT:
      """Decision Transformer with minimax return conditioning.
      
      Standard DT: condition on τ (target return) → generate actions that 
      historically achieved return τ.
      
      ARDT: condition on τ_minimax = max_π min_opponent E[return | π, opponent]
      → generate actions that achieve high return EVEN AGAINST the worst opponent.
      
      Implementation: expectile regression on returns-to-go at different quantiles
      to estimate worst-case and best-case returns from the offline data.
      """
      
      def __init__(self, dt_model, tau=0.9):
          self.dt = dt_model
          self.tau = tau  # Expectile parameter: 0.5 = symmetric, 0.9 = pessimistic
          
      def expectile_loss(self, pred, target):
          """Asymmetric loss: penalize underestimates more than overestimates.
          This gives us a PESSIMISTIC estimate of return — the worst-case
          return-to-go under adversarial opponent behavior."""
          diff = target - pred
          weight = torch.where(diff > 0, self.tau, 1 - self.tau)
          return (weight * diff.pow(2)).mean()
      
      def compute_minimax_return(self, states, returns):
          """Estimate the minimax return-to-go for each state.
          This replaces the raw return-to-go with an adversarially robust estimate.
          The key idea: among all trajectories passing through this state,
          what return do you achieve against the WORST opponent?"""
          # Train an expectile regression model on (state → return-to-go)
          # with high tau (e.g., tau=0.9) to get pessimistic estimates
          return self.expectile_model(states)
      
      def train_step(self, batch):
          """Modified DT training: use minimax returns instead of raw returns."""
          states, actions, raw_returns = batch
          minimax_returns = self.compute_minimax_return(states, raw_returns)
          # Feed minimax returns as the return-to-go conditioning
          predicted_actions = self.dt(minimax_returns, states)
          action_loss = F.cross_entropy(predicted_actions, actions)
          return action_loss
  ```
- **Experiment:** Train ARDT on Kuhn Poker data generated from MIXED opponents:
  - 50% near-Nash opponents (produced by your CFR solver)
  - 50% exploitable opponents (loose-passive, tight-aggressive from Step 7)
  - Compare: standard DT vs ARDT when TESTED against a Nash opponent (worst case)
  - Expected: ARDT should produce near-Nash play even when trained on mixed data, while standard DT may learn to exploit the weak opponents and fail against Nash
- **Validation:** Compare ARDT's extracted strategy with the known Nash equilibrium for Kuhn Poker (from Step 2). Use exploitability metric from Step 2 to quantify gap.

**Day 4 — LLM Agent Evaluation on TextArena + Kuhn Poker**

- 🟢 Set up TextArena LLM agent:
  ```python
  import textarena as ta
  
  # Pick a strategic game — e.g., negotiation or deduction
  env = ta.make("SpyFall-v0")  # or another deception/deduction game
  
  # Create LLM agent (use whatever API you have access to)
  agent = ta.agents.OpenRouterAgent(
      model="anthropic/claude-3.5-sonnet",
      system_prompt="You are a strategic game player. Think step by step."
  )
  
  # Run evaluation: LLM vs LLM, LLM vs random
  results = ta.evaluate(env, [agent, ta.agents.RandomAgent()], n_games=50)
  ```
- 🔴 Build Kuhn Poker LLM evaluation:
  ```python
  class KuhnPokerLLMAgent:
      """Wrapper to test LLM play on Kuhn Poker.
      Uses the Kuhn environment from Step 2."""
      
      def __init__(self, llm_client, system_prompt=None):
          self.llm = llm_client
          self.system_prompt = system_prompt or self.default_prompt()
      
      def default_prompt(self):
          return """You are playing Kuhn Poker. Rules:
          - 3-card deck: Jack, Queen, King (King > Queen > Jack)
          - Each player gets 1 card, sees only their own
          - Betting: check/bet → check/call/fold
          - Higher card wins at showdown
          Think about: what card does your opponent likely have? 
          Should you bluff? What's the optimal strategy?"""
      
      def get_action(self, game_state):
          prompt = f"""Current state:
          Your card: {game_state.my_card}
          Pot: {game_state.pot}
          Betting history: {game_state.action_history}
          Legal actions: {game_state.legal_actions}
          
          Choose your action and explain your reasoning."""
          response = self.llm.complete(self.system_prompt, prompt)
          action = self.parse_action(response, game_state.legal_actions)
          return action
  ```
- **Key evaluation metrics (🔴 hand-design these):**
  1. **Illegal move rate:** How often does the LLM attempt an illegal action?
  2. **Exploitability:** Extract the LLM's empirical strategy profile (over many hands) and compute exploitability using the exact game solver from Step 2
  3. **Bluff frequency:** Does the LLM bluff with Jack? (Nash says ~1/3 of the time.) Does it value bet with King? (Nash says always.)
  4. **Opponent adaptation:** If you change the opponent from Nash to always-call, does the LLM stop bluffing? (A good exploitative agent would — see Step 8)
  5. **Reasoning quality:** Read the LLM's explanations. Does it demonstrate theory of mind? Information-theoretic reasoning? Or is it just pattern-matching?
- **Comparison table (the step's key output):**
  | Agent | Exploitability (mbb/h) | Bluff Freq (J) | Value Bet Freq (K) | Illegal Move % | Adapts to Opp? |
  |-------|----------------------|-----------------|--------------------|----|---|
  | Nash CFR (Step 2) | 0 | 1/3 | 1.0 | 0 | No |
  | DT (high return) | ? | ? | ? | 0 | No |
  | ARDT (minimax) | ? | ? | ? | 0 | No |
  | Behavioral cloning | ? | ? | ? | 0 | No |
  | LLM (no prompting) | ? | ? | ? | ? | ? |
  | LLM (CoT prompting) | ? | ? | ? | ? | ? |
  | LLM (game theory prompt) | ? | ? | ? | ? | ? |
  - The game theory prompt: tell the LLM about Nash equilibrium for Kuhn Poker and ask it to approximate it. Does it? How close?

### Deliverables:
- [ ] Poker trajectory dataset (50K+ Kuhn hands) with state encoding matching thesis tensor design
- [ ] Decision Transformer trained on Kuhn Poker; return conditioning validated
- [ ] Stochasticity experiment demonstrating the Paster et al. (2022) luck-vs-skill issue
- [ ] ARDT implementation with minimax expectile regression, tested on Kuhn Poker
- [ ] ARDT strategy compared to known Nash equilibrium (exploitability measurement)
- [ ] TextArena LLM agent running on at least one strategic game
- [ ] Kuhn Poker LLM evaluation: exploitability, bluff frequency, illegal moves, opponent adaptation
- [ ] Comparison table: Nash CFR vs DT vs ARDT vs BC vs LLM on Kuhn Poker

### Validation:
- **DT return conditioning:** Low return-to-go produces worse play than high return-to-go (measured by exploitability).
- **Stochasticity test:** DT's action prediction accuracy varies by card dealt — confirming it partially learns luck, not just skill.
- **ARDT vs DT:** ARDT should produce lower exploitability when tested against Nash opponents, especially when trained on mixed (Nash + exploitable) opponent data.
- **ARDT vs known Nash:** On Kuhn Poker, ARDT's extracted strategy should be within 50 mbb/h of Nash exploitability. (If it's zero, that's remarkable and matches the paper's claims for full-coverage settings.)
- **LLM exploitability:** An honest comparison — the LLM will likely have HIGHER exploitability than any trained model. The interesting finding is WHERE it fails (e.g., suboptimal bluffing frequency, failure to adapt).

---

## Phase 5: Consolidation (2 days)

### Day 1 — Survey Skim + Cross-References

- **Reference skim:** Kumar et al. (2020) — CQL Sections 1–3  
  *Understand the value-based offline RL alternative: CQL penalizes Q-values for unseen actions (pessimism principle). Compare with DT's sequence modeling approach. When is CQL better than DT? (Answer from Paster et al.: CQL handles stochasticity better because it doesn't condition on return.)*

- **Supplementary skim:** Zhang et al. (2025) — "Divide-Fuse-Conquer"  
  https://arxiv.org/abs/2505.16401  
  *Skim Section 3: the divide-fuse-conquer pipeline for LLM game training. Note: they use TextArena as testbed. How does their Qwen2.5-32B compare to the Claude/GPT models on the leaderboard?*

- **Supplementary skim:** Guo et al. (2023) — "Suspicion-Agent"  
  https://arxiv.org/abs/2309.17277  
  *Skim the planning module: how GPT-4 simulates other players' intentions. Connect to Step 7: explicit theory of mind via LLM vs explicit Bayesian opponent model — two implementations of the same concept.*

- **Supplementary skim:** Maugin & Cazenave (2025) — "SpinGPT"  
  *Skim for: how they combine LLM reasoning with CFR-based strategy. This is the most direct bridge between the formal game-solving track (Steps 2–6) and the LLM track (this step).*

- **Forward scan:** Check arXiv for any new papers on Decision Transformer + games, or LLM agents + strategic reasoning, since the freshness scan at the start of this step.

### Day 2 — PhD Mapping + One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 2] Kuhn Poker Nash equilibrium → [Step 12] used as ground truth to evaluate DT, ARDT, and LLM agents. The exact Nash solution is the benchmark that all other methods are measured against.
    - [Step 3] CFR agent → [Step 12] used as DATA GENERATOR. The quality of DT training data depends on the quality of the generating agent. Near-Nash CFR data = high-quality offline data. Random data = low-quality.
    - [Step 5] Deep CFR (neural equilibrium) → [Step 12] ARDT offers an ALTERNATIVE path to equilibrium strategies: instead of iterating CFR with neural networks, just do supervised learning on an offline game dataset with adversarially robust conditioning. Same destination, different road.
    - [Step 7] Bayesian opponent model → [Step 12] LLM agents do implicit opponent modeling via in-context reasoning. Same function (infer opponent's state from behavior), radically different implementation (statistics vs language).
    - [Step 8] Safe exploitation → [Step 12] ARDT's minimax conditioning is the offline RL analog of safe exploitation: play well against the WORST-CASE opponent. The safety guarantee transfers from online (Step 8) to offline (Step 12) settings.
    - [Step 11] CICERO/Welfare Diplomacy → [Step 12] CICERO is the most complete LLM+game AI system. Step 11 analyzed the strategic planning component; Step 12 analyzes the language model component. Together, they give the full picture.
    - [Step 12] Poker state tensor encoding → prediction: [Step 13] Same encoding applied to Playtech data. The DT pipeline is the PROTOTYPE for Step 13's real-world behavioral analysis pipeline.
    - [Step 12] Paster et al. stochasticity warning → prediction: [Step 13] Must condition on decision EV, not outcome, when building the Playtech pipeline. Return-to-go conflates luck with skill in poker.
  - **Confusions:**
    - [Step 12] DT conditions on return-to-go, but in poker the return depends heavily on card deal (luck). Paster et al. say this means DT will fail. ARDT's fix (minimax conditioning) helps, but does it fully solve the problem? In Kuhn Poker (3 cards, tiny game), we can verify. In full poker (10^160 information sets), unclear. → PARTIALLY ADDRESSED (ARDT helps; full solution may need EV-based conditioning, deferred to Step 13)
    - [Step 12] LLM agents understand game rules through language, but their strategic reasoning is inconsistent (sometimes optimal, sometimes terrible). Can we QUANTIFY when LLM reasoning is reliable? What game properties predict LLM success? → OPEN (TextArena evaluation may give partial answers)
    - [Step 12] ARDT recovers Nash in full-coverage settings (Tang et al.'s claim). But offline poker data has PARTIAL coverage (not all states visited). How does ARDT degrade with partial coverage? → OPEN (tested on Kuhn, but Kuhn is too small to stress this)
    - [Step 7→12] Bayesian opponent model (Step 7) is precise but requires explicit state representation and prior specification. LLM opponent model (Step 12) is flexible but imprecise and uncontrollable. Is there a principled way to COMBINE them? (e.g., LLM generates hypotheses, Bayesian model evaluates them) → OPEN (potentially novel contribution)
    - [Step 5→12] Deep CFR iterates to equilibrium via self-play. ARDT reaches equilibrium from offline data without self-play. When would you prefer one over the other? → PARTIALLY ADDRESSED (ARDT needs offline data, Deep CFR needs a simulator. For real-world domains like Playtech where you HAVE data but NOT a perfect simulator, ARDT may be preferred.)

### PhD Connection

This step bridges the thesis's FORMAL tools (Steps 2–8: CFR, equilibrium, exploitation) to the DATA-DRIVEN paradigm:

- **Contribution #1 (Behavioral Adaptation):** The state tensor encoding (cards, position, pot, stacks, betting history) designed here carries directly to the Playtech behavioral analysis pipeline (Step 13). The encoding IS the foundation of the behavioral adaptation framework — how you represent game state determines what behavioral patterns you can detect. This step prototypes the encoding on small games; Step 13 scales it to real data.

- **Contribution #2 (Multi-Agent Safe Exploitation):** ARDT demonstrates that safe (minimax) strategies can emerge from offline data without explicit game-theoretic computation. This opens a path for Contribution #2: instead of computing Nash equilibria for N-player games (intractable, as shown in Step 11), learn safe strategies directly from behavioral data. The minimax conditioning on return-to-go is the offline analog of safe exploitation.

- **Contribution #3 (Evaluation Methodology):** The comparison table (CFR vs DT vs ARDT vs BC vs LLM on Kuhn Poker) is a microcosm of the evaluation framework: multiple agent architectures, same game, standardized metrics (exploitability, behavioral statistics). This prototype scales to the full evaluation framework in Step 14.

- **Bridge to Step 13:** Everything in this step's implementation — the state tensor encoding, the trajectory dataset format, the DT training pipeline — transfers to Playtech's anonymized hand history data. Step 12 builds the prototype on synthetic Kuhn/Leduc data; Step 13 applies it to real poker data.

- **LLM angle for job market:** 3/10 target job postings mention LLM skills. This step demonstrates fluency with the LLM paradigm, positioning you for both the AI researcher path (combining formal methods with LLMs) and the fraud/risk path (LLM-based anomaly description and reasoning).

---

## Exit Checklist

- [ ] Decision Transformer trained on Kuhn Poker offline data with return conditioning validated
- [ ] Stochasticity experiment completed: DT's luck-vs-skill confusion quantified
- [ ] ARDT minimax conditioning implemented and tested (🔴 hand-coded loss function)
- [ ] ARDT produces near-Nash play on Kuhn Poker (within 50 mbb/h exploitability)
- [ ] TextArena LLM agent tested on at least one strategic game
- [ ] LLM evaluation on Kuhn Poker: exploitability, bluff frequency, illegal moves, adaptation metrics computed
- [ ] Comparison table completed: Nash CFR vs DT vs ARDT vs BC vs LLM
- [ ] Poker state tensor encoding documented and verified (same encoding to be reused in Step 13)
- [ ] Can explain from memory: Decision Transformer architecture (return-to-go conditioning, GPT-2 backbone)
- [ ] Can explain from memory: why DT fails in stochastic environments (Paster et al. Theorem 2.1)
- [ ] Can explain from memory: ARDT's minimax expectile regression and why it recovers Nash
- [ ] Can explain from memory: strengths and limitations of LLM agents in strategic games
- [ ] All 🔴 components hand-coded (state encoding, ARDT loss function, LLM evaluation metrics)
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Steps 2–11 + new confusions + PhD bridge notes)
- [ ] PhD connection documented (state encoding → Step 13, ARDT → Contribution #2 offline path, comparison table → Contribution #3 prototype)
- [ ] Step notes committed to repo
