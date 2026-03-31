# Step 9 — Multi-Agent RL — Coordination, Competition, and Communication

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 1 (RL Basics), Step 6 (End-to-End Game AI Architectures)  
**Phase:** E — Multi-Agent Dynamics  
**Freshness Note:**  
- ArXiv search: "multi agent reinforcement learning communication cooperation" sorted by date (Mar 2026) — 351 results total, scanned top 50. Dominated by telecom/UAV/robotics applications. Relevant MARL-theory papers:  
  - Wittner (Jan 2026) "Communication Methods in Multi-Agent Reinforcement Learning" (arXiv:2601.12886) — 12-page survey of MARL communication methods. *Useful reference for Phase 3.*  
  - HCPO: Liu et al. (Nov 2025) "Hierarchical Conductor-Based Policy Optimization in MARL" (AAAI 2026). *New cooperative MARL architecture.*  
  - Samvelyan (Dec 2025) "Robust Agents in Open-Ended Worlds" (arXiv:2512.08139) — PhD thesis on open-ended MARL. *Survey reference for Phase 5.*  
  - Hill et al. (Aug 2025) "Communicating Plans, Not Percepts: Scalable Multi-Agent Coordination with Embodied World Models" — NeurIPS 2025 workshop. *Interesting communication approach.*  
- ArXiv search: "PSRO policy space response oracle multi agent" sorted by date (Mar 2026) — 9 results:  
  - Hennes, Li, Schultz & Lanctot (Mar 2026) "Code-Space Response Oracles: Generating Interpretable Multi-Agent Policies with LLMs" (AAMAS 2026) — LLM-generated PSRO policies. *Supplementary, interesting for Step 12 bridge.*  
  - Li, Schultz, Hennes & Lanctot (Feb 2026) "Discovering Multiagent Learning Algorithms with Large Language Models" (arXiv:2602.16928) — meta-discovery of MARL algorithms via LLMs. *Supplementary.*  
  - Bighashdel, Simão & Oliehoek (Feb 2026) "Sample-Efficient PSRO with Joint Experience Best Response" (AAMAS 2026) — improves PSRO sample efficiency. *Relevant supplementary.*  
  - GEMS: Sharma et al. (Sep 2025, TMLR 2026) "Generative Evolutionary Meta-Solver" — scalable surrogate-free MARL. *Relevant to Step 10.*  
- ArXiv search: "QMIX MAPPO cooperative multi agent reinforcement learning" (Mar 2026) — 8 results:  
  - Zhong et al. (Apr 2023, Dec 2023) "Heterogeneous-Agent Reinforcement Learning (HARL)" (arXiv:2304.09870) — unified framework for heterogeneous cooperative MARL. *Important foundational recent work.*  
  - Amato (May 2024, updated May 2025) "An Initial Introduction to Cooperative MARL" (arXiv:2405.06161) — pedagogical survey. *Good Phase 1/3 reference.*  
- Core references unchanged: Lowe et al. (2017 MADDPG), Rashid et al. (2018 QMIX), Yu et al. (2022 MAPPO), Foerster et al. (2016 CommNet / 2018 LOLA), Sukhbaatar et al. (2016 CommNet), Lanctot et al. (2017 PSRO).  
- No superseded content for Step 9 scope — the CTDE paradigm and foundational MARL algorithms remain canonical.

---

> **Phase Overview:** The preceding phases focused on two-player imperfect-information games. Phase E will transition the study to multi-agent settings, where new challenges arise: non-stationarity from simultaneously learning agents, credit assignment in joint-reward environments, and the emergence of coalitions. Step 9 introduces multi-agent RL paradigms (CTDE, PSRO), Step 10 scales to population-based training and evolutionary game theory, and Step 11 applies these tools to coalition formation in free-for-all games.
>
> **Contribution Alignment:** This step will provide the algorithmic vocabulary for extending the thesis from two-player to multi-agent settings. The CTDE paradigm introduces the architectural pattern — centralized training, decentralized execution — used throughout the remainder of the thesis. PSRO provides a population-based framework relevant to defining safety in multi-agent populations.


## Phase 1: Intuition (1 day)

The goal: understand WHY multi-agent RL is fundamentally different from single-agent RL and from the game-theoretic approach you've used so far. In Steps 2–8 you computed or approximated Nash equilibria — strategies against a RATIONAL opponent. In MARL, agents LEARN simultaneously in a SHARED environment, so the environment is NON-STATIONARY from each agent's perspective (the other agents are also changing). This creates two new challenges: (1) coordination — how do cooperating agents learn to work together without explicit programming? (2) credit assignment — when the team wins, which agent's actions were responsible?

End of day: you should be able to explain to a non-expert: "In single-agent RL, the agent learns by trial and error in a fixed world. In multi-agent RL, every agent IS the 'world' for every other agent — so the 'world' keeps changing as agents learn. It's like learning to dance with a partner who is also learning to dance — you keep stepping on each other's toes until you accidentally synchronize."

- **Jakob Foerster — "Multi-Agent Reinforcement Learning" (AAAI 2024 Tutorial)**  
  https://www.youtube.com/watch?v=2GwBez0D20A  
  Duration: ~2h | Speaker: Jakob Foerster (Oxford)  
  *THE definitive MARL tutorial. Foerster covers: (1) why single-agent RL fails in multi-agent settings (non-stationarity), (2) the CTDE (Centralized Training, Decentralized Execution) paradigm, (3) cooperative MARL (QMIX, MAPPO), (4) competitive MARL (self-play, PSRO), (5) communication. Watch 0:00–1:00 for the conceptual framework, skim the rest for specific algorithms you'll read about in Phase 3.*

- **Shimon Whiteson — "Cooperative Multi-Agent Learning" (invited talk)**  
  https://www.youtube.com/watch?v=nIgIv4IfJ6s  
  Duration: ~50m | Speaker: Shimon Whiteson (Waymo / Oxford)  
  *Whiteson's group created QMIX and many cooperative MARL methods. This talk gives the intuition for the CENTRAL-THEN-DECENTRAL design: train with global info, execute with local info. Watch 10:00–30:00 for the design rationale.*

- **Natasha Jaques — "Social Influence as Intrinsic Motivation for MARL"**  
  https://www.youtube.com/watch?v=NSVmOC_5zrE  
  Duration: ~25m | Speaker: Natasha Jaques (Google Brain → UC Berkeley)  
  *A different angle: agents learn to INFLUENCE each other's behavior as an intrinsic reward. This bridges to your thesis's opponent modeling (Step 7): instead of modeling an opponent to exploit them, you model them to COORDINATE with them.*

### Blog Posts / Accessible Reads

- **Lowe et al. — "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments" (OpenAI Blog, 2017)**  
  https://openai.com/index/learning-to-cooperate-compete-and-communicate/  
  *Accessible intro to MADDPG. The original mixed cooperative-competitive MARL paper. Short read.*

- **PettingZoo documentation — Multi-Agent RL environments**  
  https://pettingzoo.farama.org/  
  *The standard multi-agent environment library (successor to OpenAI's multiagent-particle-envs). Browse the environment list to see the variety of MARL settings: cooperative, competitive, mixed.*

- **Amato (2024/2025) — "An Initial Introduction to Cooperative MARL"**  
  https://arxiv.org/abs/2405.06161https://arxiv.org/abs/1705.01820  
  *Pedagogical survey — read Sections 1–3 for a gentle conceptual intro if the video tutorials feel too fast.*

---

## Phase 2: Exploration (2 days)

### Day 1: PettingZoo + Simple Multi-Agent Environments

1. **Install PettingZoo + Gymnasium:**
   ```bash
   pip install pettingzoo gymnasium supersuit
   ```

2. **Run the classic multi-agent environments:**
   ```python
   from pettingzoo.mpe import simple_spread_v3, simple_adversary_v3
   from pettingzoo.classic import connect_four_v3, tictactoe_v3
   
   # Cooperative: simple_spread — 3 agents must cover 3 landmarks
   env = simple_spread_v3.parallel_env(N=3)
   observations, infos = env.reset()
   # Run random agents and observe: cooperation is terrible with random policies
   
   # Competitive: simple_adversary — 1 adversary vs N cooperating agents
   env = simple_adversary_v3.parallel_env(N=2)
   # Observe the mixed cooperative-competitive dynamics
   
   # Classic games (your familiar territory): connect_four, tictactoe
   # These are turn-based, perfect-info — contrast with the simultaneous-action MPE envs
   ```

3. **Observe the non-stationarity problem:**
   - Train a single PPO agent in simple_spread (treating other agents as environment)
   - Watch it fail: the "environment" is non-stationary because other agents are also learning
   - This is the motivation for CTDE

4. **Explore OpenSpiel's multi-agent support:**
   ```python
   import pyspiel
   # Run a multi-player game you haven't used yet
   game = pyspiel.load_game("goofspiel", {"num_cards": 4})
   # Goofspiel: simultaneous-action card game, N-player
   # Try running your MCCFR on it — observe the multiplayer complexity explosion
   ```

### Day 2: CTDE in Practice + Self-Play

1. **Run an existing MAPPO or QMIX implementation:**
   - Use EPyMARL (https://github.com/uoe-agents/epymarl) or MARLlib
   - Train MAPPO on simple_spread
   - Compare learning curves: MAPPO (CTDE) vs independent PPO (no coordination)
   - **Expected result:** MAPPO converges faster and achieves better cooperative performance

2. **Self-play for competitive games:**
   ```python
   # Use OpenSpiel's self-play infrastructure
   # Run PPO self-play on Kuhn or Leduc
   # Compare the self-play strategy with your Nash solution from Step 2
   # Key question: does self-play converge to Nash? (Spoiler: not always)
   ```

3. **Questions to answer by end of Day 2:**
   - What's the difference between independent learning and centralized training?
   - Why does QMIX restrict the mixing network to be monotone?
   - In self-play, when does the learned strategy converge to Nash and when does it cycle?
   - How does PettingZoo's API differ from Gymnasium? (agent-agentenv-cycle vs parallel)

---

## Phase 3: Targeted Reading (3 days)

### Paper 1: Lowe et al. — "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments" (MADDPG, 2017)

https://arxiv.org/abs/1706.02275https://arxiv.org/abs/1505.00533

```
├── READ:  Section 3 (MADDPG algorithm — multi-agent version of DDPG where each 
│          agent's CRITIC sees all agents' observations and actions during training,
│          but each agent's ACTOR only sees its own observation during execution.
│          This is the original CTDE algorithm for continuous action spaces),
│          Section 4 (Experiments — the Multi-agent Particle Environment (MPE) results)
├── SKIM:  Abstract, Section 1 (Introduction — the non-stationarity argument),
│          Section 2 (Background — DDPG review, skip if comfortable from Step 1)
├── SKIP:  Section 5 (Discussion — short, skim)
├── MATH:  → "Equation 5 (MADDPG policy gradient) — understand how the gradient
│             for agent i uses the centralized critic Q(x, a1, ..., aN) that sees
│             ALL agents' actions, while the policy πi(oi) only uses agent i's
│             observation. This asymmetry between training (centralized) and
│             execution (decentralized) is the core CTDE idea."
└── KEY INSIGHT: "MADDPG solves the non-stationarity problem by giving each agent's
    critic access to all agents' policies during training. From the critic's 
    perspective, the environment IS stationary (because it can see what everyone 
    is doing). The actor remains decentralized. This is the template for all
    CTDE methods."
```

### Paper 2: Rashid et al. — "QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning" (2018)

https://arxiv.org/abs/1803.11485https://arxiv.org/abs/1603.01121 (ICML 2018)

```
├── READ:  Section 3 (QMIX architecture — how individual agent Q-values are 
│          combined via a MONOTONIC mixing network to produce the joint Q-value.
│          Key constraint: ∂Qtot/∂Qi ≥ 0 for all i. This ensures that 
│          argmax of Qtot decomposes into argmax of individual Qi's),
│          Section 4 (Experiments on StarCraft micromanagement — SMAC benchmark)
├── SKIM:  Abstract, Section 1 (Introduction),
│          Section 2 (Background — Dec-POMDP formulation)
├── SKIP:  Appendix details
├── MATH:  → "The monotonicity constraint (Section 3.1) — understand WHY it's 
│             needed. If the mixing function were arbitrary, you couldn't decompose
│             the joint action into individual agent decisions at execution time.
│             The monotonicity guarantees that each agent can independently maximize
│             its own Qi and the result maximizes Qtot. This is the key structural
│             assumption that makes decentralized execution work."
└── KEY INSIGHT: "QMIX's genius is the monotonicity constraint: it limits 
    expressiveness (can't represent all joint Q-functions) but gains 
    DECOMPOSABILITY (each agent can act independently). This is the 
    cooperation-through-structure approach — different from MADDPG's 
    cooperation-through-centralized-critics."
```

### Paper 3: Yu et al. — "The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games" (MAPPO, 2022)

https://arxiv.org/abs/2103.01955https://arxiv.org/abs/1906.02701 (NeurIPS 2022)

```
├── READ:  Section 3 (MAPPO — multi-agent PPO with shared parameters and centralized
│          value function. The simplest CTDE method: just PPO with extra state in 
│          the value function),
│          Section 4 (Experiments — comparison with QMIX, MADDPG on SMAC, MPE, Hanabi)
├── SKIM:  Abstract, Section 1 (Introduction — "PPO is surprisingly competitive"),
│          Section 5 (Ablations — which implementation tricks matter most)
├── SKIP:  Detailed hyperparameter tables unless debugging your implementation
├── MATH:  → "No new math. MAPPO is PPO with a centralized value function V(s)
│             where s is the global state. If you understood PPO from Step 1,
│             you understand MAPPO."
└── KEY INSIGHT: "MAPPO demonstrates that a SIMPLE method (PPO + centralized value 
    + shared parameters) outperforms or matches more complex methods (QMIX, MADDPG)
    across a wide range of cooperative tasks. The implication: in cooperative MARL,
    implementation quality and hyperparameter tuning matter more than algorithmic
    novelty. A cautionary tale for over-engineering."
```

### Paper 4: Foerster et al. — "Learning with Opponent-Learning Awareness" (LOLA, 2018)

https://arxiv.org/abs/1709.04326https://arxiv.org/abs/2208.11326 (AAMAS 2018)

```
├── READ:  Section 3 (LOLA algorithm — instead of just optimizing your own reward,
│          DIFFERENTIATE THROUGH the other agent's learning update. You model how
│          your OWN action changes what the OTHER agent will learn, and optimize 
│          for that second-order effect),
│          Section 4 (Experiments — Iterated Prisoner's Dilemma and Matching Pennies)
├── SKIM:  Abstract, Section 1–2
├── SKIP:  Proofs in appendix (read theorem statements)
├── MATH:  → "Equation 4 (LOLA gradient) — MUST understand. The standard policy
│             gradient optimizes E[R1(π1, π2)]. LOLA optimizes E[R1(π1, π2 + Δπ2)]
│             where Δπ2 = α∇_{π2}R2(π1, π2) — the update agent 2 WILL MAKE given
│             π1. So agent 1 is optimizing for a FUTURE world where agent 2 has 
│             already adapted. This is LOOK-AHEAD learning. Connection to your 
│             thesis: opponent modeling (Step 7) is about inferring what the opponent
│             IS doing; LOLA is about anticipating what they WILL do."
└── KEY INSIGHT: "LOLA achieves cooperation in the Prisoner's Dilemma (where naive 
    learners converge to mutual defection) by having each agent model the other's 
    LEARNING PROCESS. This is a fundamentally different paradigm from opponent 
    modeling (Step 7) or equilibrium computation (Steps 2–6): agents don't model 
    static strategies, they model dynamic learning trajectories. This distinction 
    matters for your thesis."
```

### Paper 5: Lanctot et al. — "A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning" (PSRO, 2017)

https://arxiv.org/abs/1711.00832https://arxiv.org/abs/2301.02345 (NeurIPS 2017)

```
├── READ:  Section 3 (PSRO framework — the double oracle approach: maintain a 
│          population of policies, compute best responses to the population's 
│          meta-Nash equilibrium, add new policies to the population, repeat.
│          This is the multi-agent analog of iterative best response from Step 2),
│          Section 4 (Connection to existing algorithms — PSRO unifies fictitious 
│          play, DO, and self-play as special cases)
├── SKIM:  Abstract, Section 1 (Introduction),
│          Section 2 (Background — normal-form game theory),
│          Section 5 (Experiments — Kuhn, Leduc, Liar's Dice)
├── SKIP:  Proofs (read statements)
├── MATH:  → "Algorithm 1 (PSRO) — trace carefully. The key loop: (1) compute 
│             meta-Nash over existing policy population (Nash over the GAME BETWEEN
│             POLICIES, not the original game), (2) train a new best-response policy
│             against the meta-Nash mixture, (3) add it to the population, (4) repeat.
│             When using RL for the best-response oracle, this connects game theory
│             to RL in a principled way."
└── KEY INSIGHT: "PSRO is the BRIDGE between game theory (Steps 2–8) and MARL 
    (Steps 9–11). It uses game-theoretic reasoning (meta-Nash) to GUIDE the RL 
    training process (best-response oracle). Instead of hoping that self-play 
    converges to something good, PSRO uses the structure of game theory to ensure 
    convergence to a Nash equilibrium of the POLICY SPACE. This is directly 
    relevant to your Step 10 (population-based training) and Step 11 (coalitions)."
```

### Paper 6: Sukhbaatar et al. — "Learning Multiagent Communication with Backpropagation" (CommNet, 2016)

https://arxiv.org/abs/1605.07736https://arxiv.org/abs/2102.04360 (NeurIPS 2016)

```
├── READ:  Section 2 (CommNet architecture — agents share a continuous communication
│          channel that is DIFFERENTIABLE. Each agent sends a message, receives the 
│          mean of other agents' messages, and uses that as additional input to its policy),
│          Section 4 (Experiments — traffic junction, bAbI tasks)
├── SKIM:  Abstract, Section 1 (Introduction), Section 3 (Related work)
├── SKIP:  bAbI experiment details (NLP-focused, less relevant)
├── MATH:  → "Equation 3 (communication update) — understand the mean-field 
│             communication: agent i receives c_i = mean(h_j for j ≠ i). Simple 
│             but powerful. The key is that this is all DIFFERENTIABLE, so the 
│             communication protocol is LEARNED through backprop, not designed."
└── KEY INSIGHT: "CommNet shows that useful communication can EMERGE from end-to-end 
    training — no one designs the protocol, the agents learn what to say. This is
    relevant to your thesis's multi-agent setting: in N-player poker, players 
    communicate through their ACTIONS (bets, raises, folds). CommNet shows the 
    principle of emergent communication; your thesis applies it to strategic settings."
```

### Supplementary References

- **Zhong et al. (2023) — "Heterogeneous-Agent Reinforcement Learning (HARL)"**  
  https://arxiv.org/abs/2304.09870https://arxiv.org/abs/2004.04136  
  *Unified framework for cooperative MARL with heterogeneous agents. SKIM abstract + Section 3 architecture. Addresses the "homogeneous agent assumption" that QMIX/MAPPO make.*

- **Bighashdel et al. (2026) — "Sample-Efficient PSRO with Joint Experience Best Response"**  
  https://arxiv.org/abs/2602.06599https://arxiv.org/abs/1707.06203  
  *AAMAS 2026. Improves PSRO sample efficiency. SKIM abstract. Relevant for understanding latest PSRO advances.*

- **Wittner (2026) — "Communication Methods in Multi-Agent Reinforcement Learning"**  
  https://arxiv.org/abs/2601.12886https://arxiv.org/abs/1611.02779  
  *12-page survey of MARL communication. SKIM for reference map of communication approaches.*

### Math Flags

🔢 **MADDPG centralized critic gradient (Lowe et al., Equation 5)** — Must understand.  
**WHY:** This is the prototype CTDE gradient. The centralized critic sees (s, a1, ..., aN) but the policy gradient updates only πi(oi). Understanding this asymmetry is essential for all cooperative MARL methods.

🔢 **QMIX monotonicity constraint (Rashid et al., Section 3.1)** — Must understand the constraint and WHY it enables decomposition.  
**WHY:** The monotonicity constraint is a structural assumption that trades expressiveness for tractability. Your thesis will face similar tradeoffs: in N-player exploitation (Contribution #2), you'll need structural assumptions about agent interactions to make the problem tractable.

🔢 **LOLA gradient (Foerster et al., Equation 4)** — Must understand.  
**WHY:** LOLA differentiates through the opponent's learning step. This "look-ahead" gradient is conceptually related to your Step 7 opponent modeling but operates at a different level — modeling the learning DYNAMICS, not the static strategy. Understanding the difference is important for positioning your thesis contribution.

🔢 **PSRO meta-Nash + best-response oracle (Lanctot et al., Algorithm 1)** — Must trace the full algorithm.  
**WHY:** PSRO is the bridge between game theory (Steps 2–8) and MARL (Steps 9–11). The meta-Nash computation is a game over POLICIES, not information states. This abstraction layer is what Step 10 (population-based training) builds on.

---

## Phase 4: Implementation (6 days)

### Project: Multi-Agent Learning Benchmark on Matrix Games + Goofspiel

This step's implementation focuses on COMPARING different MARL paradigms on controlled testbeds, rather than building one system from scratch. The goal is to understand WHEN each approach works and fails.

**Language + Framework:** Python 3.10+ / PyTorch / PettingZoo / OpenSpiel

Starting point: Your PPO from Step 1, your Nash solver from Step 2, your MCCFR from Step 3.

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| Independent Learners (IL) baseline — each agent runs PPO ignoring others | 🔴 HAND-CODE | Must understand WHY independent learning fails: non-stationarity. Building it yourself makes the failure modes visceral. Use your Step 1 PPO, extend to multi-agent. |
| MADDPG — centralized critic with decentralized actors | 🔴 HAND-CODE | The core CTDE algorithm. Hand-code the centralized critic that takes all agents' observations + actions. The actor remains your standard policy network. Key learning: the asymmetry between training and execution. |
| MAPPO — PPO with centralized value function | 🟡 AI-ASSISTED | After hand-coding MADDPG, you understand CTDE. MAPPO is simpler (just PPO + global state in value function). AI-draft, review the centralized value function integration. |
| PSRO loop — population + meta-Nash + best-response oracle | 🔴 HAND-CODE | PSRO is the game-theory↔MARL bridge. You must hand-code the double-oracle loop: compute meta-Nash over policy population, train best-response via RL, add to population. This is thesis-critical for Step 10. |
| Matrix game experiments (Prisoner's Dilemma, Matching Pennies, Stag Hunt) | 🔴 HAND-CODE | Small enough to verify analytically. Build the matrix game environment and run all methods on it. You should predict the results before running. |
| Goofspiel environment wrapper | 🟡 AI-ASSISTED | Use OpenSpiel's Goofspiel. Write a PettingZoo-compatible wrapper if needed, AI-assisted. |
| Communication channel (CommNet-style) | 🟡 AI-ASSISTED | Implement a simple mean-field communication channel between agents. AI drafts the communication layer, you integrate with MADDPG. |
| Tournament + evaluation framework | 🟢 AI-GENERATED | Standard comparison infrastructure. Plotting, metrics, logging. |

### Sub-phase Breakdown (6 days):

**Day 1 — Matrix Game Testbed + Independent Learners:**
- 🔴 Build the matrix game environment (Prisoner's Dilemma, Matching Pennies, Stag Hunt, Battle of the Sexes):
  ```python
  class MatrixGame:
      """2-player simultaneous-action matrix game."""
      def __init__(self, payoff_matrix_1, payoff_matrix_2):
          # payoff_matrix_i[a1][a2] = reward for player i
          ...
      def step(self, action_1, action_2):
          return reward_1, reward_2
  ```
- 🔴 Run independent PPO learners on each game:
  - Prisoner's Dilemma: expect mutual defection (Nash)
  - Matching Pennies: expect cycling (mixed Nash is unstable for learners)
  - Stag Hunt: expect coordination failure (agents learn the safe payoff-dominant equilibrium?)
  - Battle of the Sexes: expect one of two pure Nash, or cycling
- Document: WHAT converges, what cycles, what fails. This establishes the baseline.

**Days 2–3 — MADDPG + MAPPO:**
- 🔴 Implement MADDPG:
  - **Centralized critic:** Q(s, a1, a2) — input is concatenation of all observations + all actions
  - **Decentralized actors:** πi(oi) — each actor only sees own observation
  - Training: critic trained on centralized data, actor trained with centralized critic gradients
  - Execution: only actors used, no communication between agents
- Run on matrix games — compare with independent learners
- 🟡 Implement MAPPO (AI-assisted):
  - Simpler than MADDPG: just PPO with V(global_state) instead of V(local_obs)
  - Run on matrix games and MPE simple_spread
- Compare: IL vs MADDPG vs MAPPO on all matrix games
  - Expected: MADDPG/MAPPO converge to cooperative outcomes more reliably than IL

**Days 4–5 — PSRO:**
- 🔴 Implement the PSRO loop:
  ```python
  class PSRO:
      def __init__(self, game, br_oracle):
          self.population = {i: [random_policy()] for i in range(num_players)}
          self.meta_game = {}  # payoff matrix between policies
      
      def compute_meta_nash(self):
          # Solve the normal-form game where actions = policies in population
          # Returns: mixture weights over population for each player
          ...
      
      def train_best_response(self, player, opponent_mixture):
          # Train a new policy via RL against opponent_mixture
          # This is the "oracle" — can be PPO, DQN, or exact best-response
          ...
      
      def iterate(self, num_rounds):
          for _ in range(num_rounds):
              meta_nash = self.compute_meta_nash()
              for player in range(self.num_players):
                  br = self.train_best_response(player, meta_nash)
                  self.population[player].append(br)
                  self.update_meta_game(br, player)
  ```
- Run PSRO on Kuhn Poker (using your Step 2 exact best-response as the oracle):
  - Verify: the meta-Nash should converge to the game's Nash equilibrium
  - Compare convergence speed: PSRO vs vanilla CFR from Step 2
- Run PSRO on Leduc (using PPO as the approximate best-response oracle):
  - Observe: how well does approximate BR affect PSRO convergence?
  - Compare exploitability of PSRO's meta-Nash strategy vs your MCCFR strategy from Step 3

**Day 6 — Communication + Goofspiel:**
- 🟡 Implement CommNet-style communication:
  - Add a communication channel to MADDPG: each agent broadcasts a learned message vector
  - Other agents receive the mean of all messages as additional input
  - Run on simple_spread: compare MADDPG vs MADDPG+CommNet
  - Expected: communication helps in cooperative tasks
- 🟡 Run experiments on Goofspiel (OpenSpiel):
  - Goofspiel is a simultaneous-action card game — good for testing MARL on a GAME (vs the particle envs)
  - Run PSRO on Goofspiel(4 cards) — does the meta-Nash converge?
  - Compare with MCCFR on Goofspiel — which approach is more sample-efficient?
- Collect all results into comparison tables

### Deliverables:
- [ ] Matrix game testbed (PD, Matching Pennies, Stag Hunt, Battle of the Sexes)
- [ ] Independent learners baseline with documented failure modes
- [ ] MADDPG implementation with centralized critic
- [ ] MAPPO implementation with centralized value function
- [ ] PSRO loop with meta-Nash + best-response oracle
- [ ] PSRO verified on Kuhn (convergence to Nash)
- [ ] PSRO vs MCCFR comparison on Leduc
- [ ] Communication channel (CommNet-style) integrated with MADDPG
- [ ] Goofspiel experiments
- [ ] Comparison table: IL vs MADDPG vs MAPPO vs PSRO across all games

### Validation:
- **Matrix games:** Verify learning outcomes match known Nash equilibria. PD → mutual defection, Matching Pennies → 50/50 mixed, Stag Hunt → depends on initialization (risk-dominant vs payoff-dominant).
- **MADDPG critics:** Centralized critic should have lower variance than independent critics (measure loss curves).
- **PSRO on Kuhn:** Meta-Nash exploitability should converge to ≈0 (matching CFR).
- **PSRO on Leduc:** Meta-Nash exploitability should decrease below 0.5 bb/hand within 20 PSRO iterations.
- **Communication:** Agents with CommNet should achieve higher reward on simple_spread than agents without.

---

## Phase 5: Consolidation (2 days)

### Day 1 — Survey Skim + Supplementary Papers

- **Reference skim:** Shoham & Leyton-Brown (2009) — "Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations"  
  https://www.masfoundations.org/  
  *Chapters 6–7 (learning in games). Skip Chapters 1–5 (game theory basics — you know this from Steps 2–3). Skip Chapters 8+ (mechanism design, social choice — relevant to a different thesis). Focus: how does the textbook characterize the convergence difficulties in multi-agent learning?*

- **Survey skim:** Zhang, Yang & Basar (2021) — "Multi-Agent Reinforcement Learning: A Selective Overview of Theories and Algorithms"  
  https://arxiv.org/abs/1911.10635https://arxiv.org/abs/2009.04416  
  *The canonical MARL survey. SKIM Sections 3 (cooperative MARL), 4 (competitive MARL), and 6 (emergent communication). Cross-reference with what you just implemented — map each algorithm you built to its section in this survey.*

- **Supplementary read:** Samvelyan (2025) — "Robust Agents in Open-Ended Worlds" PhD thesis  
  https://arxiv.org/abs/2512.08139https://arxiv.org/abs/1507.01228  
  *SKIM Chapter 2 (background on open-ended learning + auto-curricula). This connects to Step 10 (population-based training + evolution) and Step 11 (emergent complexity in competitive FFA).*

### Day 2 — PhD Mapping + One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 1] PPO → [Step 9] MAPPO is literally PPO with a centralized value function. Your Step 1 implementation is the building block.
    - [Step 2] Nash equilibrium → [Step 9] PSRO converges to Nash in the POLICY SPACE. The meta-game solved by PSRO is a normal-form game over policies — exactly what you learned in Step 2 but one level up.
    - [Step 3] MCCFR → [Step 9] PSRO with CFR as the best-response oracle is an alternative to PSRO with RL. For perfect-recall games, CFR oracle is more efficient than RL oracle.
    - [Step 6] ReBeL/Pluribus self-play → [Step 9] Self-play is a SPECIAL CASE of PSRO (population size 1, no meta-Nash computation). PSRO generalizes self-play by maintaining a diverse population and solving a meta-game.
    - [Step 7] Opponent model (static) → [Step 9] LOLA models the opponent's LEARNING DYNAMICS, not their current strategy. LOLA is a dynamic extension of opponent modeling. For your thesis: worth investigating whether combining Step 7's static model with LOLA's dynamic anticipation gives better exploitation.
    - [Step 8] Safe exploitation assumes a FIXED or slowly-changing opponent → [Step 9] In MARL, opponents are constantly learning. Do Step 8's safety guarantees hold when the opponent is a LEARNER (non-stationary)? → OPEN question for Step 10/11.
    - [Step 9] PSRO population → [Step 10] Population-based training is the evolutionary generalization. PSRO uses meta-Nash to select policies; PBT can use other evolutionary pressures.
  - **Confusions:**
    - [Step 9] QMIX's monotonicity constraint prevents it from representing all joint value functions. Specifically, it can't handle games where individual agent value DECREASES when the joint outcome improves (e.g., one agent sacrifices for the team). How problematic is this in practice? → OPEN (WQMIX, QPLEX address this, check if relevant)
    - [Step 9] PSRO with an APPROXIMATE best-response oracle: the convergence guarantee assumes EXACT best responses. With PPO as the oracle, the best response is approximate. Does PSRO still converge? How does the approximation error compound? → OPEN (Bighashdel et al. 2026 may address this)
    - [Step 9] CommNet uses MEAN aggregation of messages. This throws away information about WHO sent what message. In competitive settings, knowing the source matters (you treat an opponent's message differently from an ally's). Is there a principal-agent communication framework? → OPEN (check TarMAC, IC3Net for targeted communication)
    - [Step 7→9] Step 7's Bayesian opponent model assumes the opponent's strategy is drawn from a fixed prior. LOLA assumes the opponent is a learner with a known learning rule. In reality, opponents are somewhere in between. How to model an opponent whose learning rule is UNKNOWN? → OPEN (relevant to Contribution #1)

### PhD Connection

This step transitions the thesis from 2-player zero-sum game theory (Steps 2–8) to the multi-agent world. The key thesis-relevant insights:

- **Contribution #1 (Behavioral Adaptation):** LOLA's "learning-aware" gradient provides a new angle on opponent modeling. Your Step 7 model detects WHAT the opponent is doing; LOLA anticipates what they WILL do. Combining both — a belief model that predicts both current and future strategies — is a potential thesis contribution.
- **Contribution #2 (Multi-Agent Safe Exploitation):** The fundamental gap: Step 8's safety guarantees assume 2-player zero-sum. In the multi-agent world, there's no minimax theorem. PSRO provides the framework: can you define "safe exploitation in a population" where the safety guarantee is against the meta-Nash of the POPULATION? This is the bridge to Steps 10 and 11.
- **Contribution #3 (Evaluation Methodology):** PSRO's meta-game analysis provides an evaluation framework for multi-agent systems. Instead of just measuring exploitability (which is 2-player), you can measure the meta-Nash distance — how far is the learned policy population from the meta-Nash equilibrium?

---

## Exit Checklist

- [ ] Matrix game testbed working with correct Nash equilibria verified
- [ ] Independent learners showing documented failure modes (non-stationarity, coordination failure)
- [ ] MADDPG working on matrix games + MPE
- [ ] MAPPO working on matrix games + MPE
- [ ] PSRO loop working: meta-Nash convergence verified on Kuhn
- [ ] Can explain CTDE from memory: why centralized training, why decentralized execution
- [ ] Can explain PSRO from memory: the double-oracle loop (population → meta-Nash → best response → add to population)
- [ ] Can explain LOLA's gradient: how differentiating through the opponent's learning step achieves cooperation
- [ ] Can explain the difference between Independent Learning, CTDE, and PSRO approaches
- [ ] Communication channel showing measurable benefit on cooperative tasks
- [ ] Comparison table populated across all methods and all games
- [ ] All 🔴 components hand-coded (IL, MADDPG, PSRO, matrix games)
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Steps 1–8 + new confusions + resolved confusions)
- [ ] PhD connection documented (CTDE paradigm, PSRO as bridge to population training, LOLA as dynamic opponent modeling)
- [ ] Markov-games bridge notation exercise completed (P9)
- [ ] Step notes committed to repo

> **[P9] Markov-Games Bridge:** Add a short formal bridge on Markov games (stochastic games) to Phase 1 (Orientation), before jumping into CTDE/PSRO/LOLA. ~Half-page of notation connecting EFG-style reasoning (game trees, information sets, counterfactual values) to MARL-style reasoning (joint policies, centralized critics, decentralized execution). Explains what is preserved (sequential decisions, partial observability) and what is lost (exact game tree structure, regret-based convergence guarantees). ~0.5d absorbed within 14d allocation.

