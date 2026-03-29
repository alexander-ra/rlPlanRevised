# Step 11 — Dynamic Coalition Formation in Competitive FFA Games

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 7 (Opponent Modeling), Step 9 (Multi-Agent RL), Step 10 (PBT + Evolutionary Game Theory)  
**Phase:** E — Multi-Agent Dynamics  
**Freshness Note:**  
- ArXiv search: "coalition formation reinforcement learning game" sorted by date (Mar 2026) — 5 results. Relevant:  
  - Sharan & Adak (Nov 2024, v2 Oct 2025) "Reinforcing Competitive Multi-Agents for Playing 'So Long Sucker'" (arXiv:2411.11057) — **the primary benchmark.** First computational framework for SLS with DQN/DDQN/Dueling DQN. Agents achieve ~50% of max reward, outperform random baselines, but need ~2000 games and still commit occasional illegal moves. *This confirms the plan's choice — SLS is the right testbed and nearly untouched by RL.*  
  - De Carufel & Jerade (Mar 2024, v2 Oct 2025) "So Long Sucker: Endgame Analysis" (arXiv:2403.17302) — 51-page combinatorial analysis of the 2-player SLS endgame. Characterizes Blue's winning scenarios. *Important for understanding endgame theory and verifying implementation.*  
  - Remaining 3 results: telecom/IoT coalition papers — NOT relevant.  
- ArXiv search: '"So Long Sucker" game' — 2 results: same two papers above. Confirms the field is extremely sparse.  
- ArXiv search: "Shapley value credit assignment multi agent reinforcement learning" — 7 results. Key:  
  - Wang, Li, Kaski, Lawry (Jun 2025) "Shapley Machine: A Game-Theoretic Framework for N-Agent Ad Hoc Teamwork" (arXiv:2506.11285) — Shapley-based framework for ad hoc teamwork in N-agent settings. *Supplementary — interesting connection: ad hoc teamwork IS implicit coalition formation.*  
  - Li et al. (Jun 2021, KDD 2021) "Shapley Counterfactual Credits for Multi-Agent Reinforcement Learning" (arXiv:2106.00285) — Shapley-based credit assignment in CTDE cooperative MARL. *Core — the Shapley credit mechanism adapted for MARL.*  
  - Wang, Zhang, Kim, Gu (Jul 2019, AAAI 2020) "Shapley Q-value: A Local Reward Approach to Solve Global Reward Games" (arXiv:1907.05707) — Decomposes team reward into individual Shapley values. *Core — the foundational Shapley-Q paper.*  
  - Ding et al. (Nov 2025) "A Historical Interaction-Enhanced Shapley Policy Gradient Algorithm for Multi-Agent Credit Assignment" (arXiv:2511.07778) — builds on Shapley PG with historical interaction graph. *Supplementary.*  
- ArXiv search: "diplomacy game AI human level" — 1 result:  
  - Bakhtin, Wu, Lerer, Gray, Jacob, Farina, Miller, Brown (Oct 2022) "Mastering the Game of No-Press Diplomacy via Human-Regularized Reinforcement Learning and Planning" (arXiv:2210.05492) — Meta AI's no-press Diplomacy agent. 7-player game with implicit coalition dynamics. *Core — the closest large-scale FFA+coalition work to SLS.*  
- Additional known work not found in search (published in Science, not indexed by keyword):  
  - Meta AI CICERO (Science, Nov 2022) — full-press Diplomacy with language model + planning. Created human-level Diplomacy play. *Supplementary — instructive but far too large to replicate. Read for architecture insights.*  
  - Mukobi et al. (2023) "Welfare Diplomacy: Benchmarking Language Model Cooperation" — LLM agents playing Diplomacy variants. *Supplementary — Step 12 bridge.*  
- Cross-reference from Step 10: Balduzzi (2019) spinning top decomposition predicted that FFA coalition games will have large cyclic component. Step 10's EGTA framework carries forward as evaluation tool.  
- Field assessment: **Dynamic coalition formation in competitive FFA settings is nearly unstudied.** Only 2 papers exist on SLS, and the RL paper (Sharan & Adak) uses basic DQN without any coalition-aware mechanisms. This confirms the plan architecture's assessment: Step 11 covers a frontier topic and a direct PhD differentiator.

---

## Phase 1: Intuition (1 day)

The goal: understand WHY coalition formation is hard (and interesting). Key insight: in all previous steps, you've worked with 2-player games. The moment you add a third player, something fundamentally changes: **players can form temporary alliances.** In a 2-player game, there's nothing to negotiate — you either cooperate or not. In a 3+ player game, you can say "Let's gang up on Player C" — and then betray your ally later. This dynamic — form coalitions, exploit them, dissolve them, form new ones — is the heart of FFA games and is essentially unstudied in the RL/game AI literature.

End of day: you should be able to explain to a non-expert: "In a poker game with 6 players, two players might secretly work together — sharing information about their hands, or one folding to let the other win a big pot. This is a COALITION. But coalitions in competitive games are unstable — eventually, one member will betray the other when it's profitable. Learning WHEN to form, MAINTAIN, and BREAK coalitions is an unsolved problem in AI. Traditional game theory (Nash equilibrium) can't tell you much about this because Nash treats each player independently. Cooperative game theory (Shapley value, the core) provides tools to analyze WHO should be in a coalition and HOW to divide the gains — but it assumes coalitions are stable. The real challenge is when coalitions are DYNAMIC."

- **Noam Brown — "CICERO: An AI agent that negotiates, persuades, and cooperates with people" (Meta AI, 2022)**  
  https://www.youtube.com/watch?v=u5_BHosc7bE  
  Duration: ~20m | Speaker: Noam Brown (Meta AI)  
  *THE state-of-the-art in multi-player game AI with coalition dynamics. Diplomacy is a 7-player game where players form alliances, negotiate, and betray. CICERO combines a language model (for negotiation) with strategic planning (for moves). Watch for: how does the system decide WHOM to ally with? When does it betray? How does it balance short-term alliance utility vs long-term strategic independence? You won't implement CICERO's language component, but the STRATEGIC component (planning under temporary alliances) is directly relevant.*

- **Tim Roughgarden — "Algorithmic Game Theory" (Stanford, Lecture on Cooperative Games)**  
  https://www.youtube.com/watch?v=aImpLOhtPBc  
  Duration: ~75m | Speaker: Tim Roughgarden (Stanford/Columbia)  
  *THE accessible introduction to cooperative game theory: the Shapley value, the core, the nucleolus. These concepts tell you how to fairly divide gains from cooperation — and when a coalition is stable (no subgroup has incentive to leave). Critical for understanding WHEN coalitions should form and WHY they break.*

- **Grant Sanderson (3Blue1Brown-style) — "The Shapley Value" (short explainer)**  
  Search YouTube for "Shapley value explained" — pick a 10-15m video.  
  *Quick visual intuition for the Shapley value: each player's marginal contribution to every possible coalition, averaged. This is the "fair" way to distribute coalition gains. You'll use it for credit assignment in multi-agent SLS.*

### Blog Posts / Accessible Reads

- **Meta AI Blog — "CICERO: An AI agent that negotiates, persuades, and cooperates with people"**  
  https://ai.meta.com/research/cicero/  
  *Read for the system architecture: how planning and language are combined for Diplomacy.*

- **Wikipedia — "Cooperative Game Theory"**  
  https://en.wikipedia.org/wiki/Cooperative_game_theory  
  *Quick primer on the core, Shapley value, and stability concepts. Read the "Solution concepts" section.*

- **Wikipedia — "So Long Sucker"**  
  https://en.wikipedia.org/wiki/So_Long_Sucker  
  *Read the rules of the game. SLS (created by Nash, Shapley, Shubik, and Hausner in 1950!) is specifically designed to study coalition dynamics: 4 players, chip-passing creates implicit alliances, and one player must be "killed" to win. The game FORCES coalition formation and betrayal.*

- **John Nash, Lloyd Shapley, Martin Shubik & Melvin Hausner — Original SLS design context**  
  The game was created by four of the greatest game theorists of the 20th century. Nash and Shapley (both Nobel laureates) designed it to study the tension between cooperation and competition. The fact that the first RL paper on SLS appeared in 2024 shows how under-explored this area is.

---

## Phase 2: Exploration (2 days)

### Day 1: Play So Long Sucker + Understand Coalition Dynamics

1. **Get the SLS codebase from Sharan & Adak:**
   - Their paper (arXiv:2411.11057) includes a GUI + benchmarking framework
   - Clone and run the code. Play several games manually (or against their random baseline)
   - **Understand the rules viscerally:**
     - 4 players, each starts with 7 chips of their color
     - On your turn: place a chip on any pile (starts or extends a pile)
     - A pile is "captured" when the top two chips are the same color — that player takes all chips below
     - You can place OTHER players' chips (that you captured) — this creates implicit alliances (you're helping them)
     - A player is eliminated when they have no chips in hand AND no chips on any pile
     - Last player standing wins
   - **Key observation:** Placing another player's chip = implicit alliance signal. Taking it back or refusing to play it = betrayal signal. The ENTIRE coalition dynamic is encoded in chip-placement decisions.

2. **Observe the DQN agents from Sharan & Adak:**
   - Run their trained DQN/DDQN/Dueling DQN agents
   - Do the agents show any coalition-like behavior? (Do they consistently help one player over others?)
   - Answer: likely no — basic DQN treats each decision independently without a coalition concept

3. **Manual coalition experiments:**
   - Play a 4-player game with 2 hand-coded coalition strategies:
     - "Always ally with Player 1": consistently place Player 1's chips, never capture Player 1's piles
     - "Betray at endgame": ally with Player 1 for the first half, then switch targets
   - Observe: does the fixed-ally strategy dominate the random baseline? Does the betrayal strategy dominate the fixed-ally?

### Day 2: Cooperative Game Theory on Simple Games

1. **Compute Shapley values on toy coalition games:**
   ```python
   import itertools
   import numpy as np
   
   def shapley_value(n_players, value_function):
       """Compute Shapley value for each player.
       value_function(coalition) → value of the coalition (set of player indices)."""
       shapley = np.zeros(n_players)
       for i in range(n_players):
           for perm in itertools.permutations(range(n_players)):
               # Find i's position in the permutation
               pos = list(perm).index(i)
               # Coalition before i joins
               before = set(perm[:pos])
               # Coalition after i joins
               after = before | {i}
               # Marginal contribution of i
               shapley[i] += value_function(after) - value_function(before)
           shapley[i] /= np.math.factorial(n_players)
       return shapley
   ```
   
   - Test on the classic "glove game": Players {1,2,3}, player 1 has a left glove, players 2 and 3 each have a right glove. A pair is worth $1. Shapley values: player 1 = $2/3, players 2,3 = $1/6 each. (Player 1 is more valuable because they're scarce.)
   
   - Test on a 3-player majority game: any 2+ players can win together. v({1})=v({2})=v({3})=0, v({1,2})=v({1,3})=v({2,3})=v({1,2,3})=1. Shapley values: each player gets 1/3. (Symmetric → equal split.)

2. **Compute the core of these games:**
   ```python
   # The core: set of payoff allocations where no coalition can do better
   # For the glove game: core = {(1, 0, 0)} - player 1 gets everything!
   # (Because any coalition without player 1 gets 0, so player 1 has all leverage)
   # 
   # Contrast: Shapley value says (2/3, 1/6, 1/6)
   # Core says (1, 0, 0)
   # Key insight: the core is about STABILITY (no group can deviate profitably)
   # Shapley is about FAIRNESS (average marginal contribution)
   # These can differ dramatically!
   ```

3. **Connect to SLS:**
   - In SLS, the "value" of a coalition = probability of its members winning
   - But the coalition structure changes EVERY TURN (dynamic, not static)
   - Shapley value can be computed at each timestep to estimate "who is helping whom the most"
   - The challenge: computing Shapley exactly requires 2^N subsets. For N=4, that's 16 — feasible. For N=6 (poker), that's 64 — still feasible. For large N, you'd need approximations.

---

## Phase 3: Targeted Reading (3 days)

### Paper 1: Sharan & Adak — "Reinforcing Competitive Multi-Agents for Playing 'So Long Sucker'" (2024)

**Link:** https://arxiv.org/abs/2411.11057

```
├── READ:  Section 2 (SLS game formalization — state representation, action space,
│          reward function. CRITICAL for your implementation. How do they encode
│          the game state for neural networks? What actions are available? How is
│          the reward structured for a game where 3 out of 4 players LOSE?),
│          Section 3 (RL approach — self-play training, DQN/DDQN/Dueling DQN. 
│          What's the training setup? How many games? What's the training horizon?),
│          Section 4 (Results — ~50% of max reward, outperforms random. What 
│          strategies emerge? Are there any coalition-like patterns?)
├── SKIM:  Abstract, Section 1 (Introduction — motivation for SLS as benchmark),
│          Section 5 (Conclusion — identified gaps and future work)
├── SKIP:  Related work on standard MARL benchmarks (you covered in Step 9)
├── MATH:  → "No complex math. Read the state representation carefully — this is 
│             your starting point for implementation. Their reward function is key:
│             how do you reward an agent in a game where only 1 out of 4 wins?"
└── KEY INSIGHT: "The first RL paper on SLS uses basic DQN with NO coalition-aware 
    mechanisms. Agents learn to play legally but don't form or exploit coalitions.
    This is the gap your step fills: adding coalition detection (Step 7's opponent 
    model applied to alliance behavior) and coalition-aware training (Shapley 
    credit assignment) to SLS."
```

### Paper 2: De Carufel & Jerade — "So Long Sucker: Endgame Analysis" (2024)

**Link:** https://arxiv.org/abs/2403.17302

```
├── READ:  Section 2 (Formal game rules — the definitive mathematical formalization
│          of SLS. Use this to verify your implementation's correctness),
│          Section 3 (Endgame characterization — when only 2 players remain, 
│          who wins? This gives you the endgame ground truth for evaluation)
├── SKIM:  Abstract, Section 1 (Introduction),
│          Sections 4–5 (deeper combinatorial analysis — skim for structure)
├── SKIP:  Detailed proofs (51 pages — read statements of results only)
├── MATH:  → "Theorems 1–3 characterize winning conditions in 2-player endgame.
│             READ STATEMENTS, skip proofs. These give you ground truth: when your
│             agents reach 2-player endgame, is the winner playing optimally?"
└── KEY INSIGHT: "The 2-player endgame has a complete analytical solution! This means 
    you can evaluate your agents' endgame play perfectly. The interesting/unsolved 
    part is the 4-player mid-game — where coalition dynamics dominate."
```

### Paper 3: Bakhtin et al. — "Mastering the Game of No-Press Diplomacy" (2022)

**Link:** https://arxiv.org/abs/2210.05492

```
├── READ:  Section 2 (How to handle N>2 players in an imperfect-information game:
│          Diplomacy has 7 players, simultaneous moves, and implicit alliances.
│          The key technique: "piKL" — regularized policy search that keeps the 
│          agent's policy close to a human-regularized prior. This prevents the
│          agent from deviating too far into "AI-optimal but human-incomprehensible"
│          play, which matters because coalition dynamics require being 
│          INTERPRETABLE to potential allies),
│          Section 3 (Search — how to do real-time planning in a 7-player game.
│          They use sampled rollouts + evaluation. Connection to your Step 6 
│          subgame solving — but in the N-player setting, you can't just solve 
│          the subgame because there's no clear "opponent" — everyone is both
│          potential ally and potential enemy),
│          Section 4 (Results — achieves human-level no-press Diplomacy. What
│          coalition patterns emerge? Does the agent learn to ally and betray?)
├── SKIM:  Abstract, Section 1, Section 5 (Discussion — what makes N-player 
│          games fundamentally harder than 2-player)
├── SKIP:  Training infrastructure details (Meta-scale compute)
├── MATH:  → "The piKL regularization (Section 2.2) — read the formula. 
│             piKL = argmin KL(pi, pi_human) + lambda * expected_loss.
│             This is the N-player analog of safe exploitation from Step 8: 
│             instead of a Nash baseline, the agent uses a HUMAN PRIOR as its 
│             safety baseline. Why? Because in N-player games, Nash is 
│             computationally intractable AND strategically unhelpful (Nash in 
│             Diplomacy is 'do nothing' — not a useful baseline)."
└── KEY INSIGHT: "In N-player games, the 'safe' baseline is no longer Nash (too 
    hard to compute, not strategically meaningful). Instead, it's a HUMAN PRIOR 
    — play like humans do, deviate only when you can prove it's profitable. This 
    is a profound shift from Steps 2–8 (where Nash was always the baseline). 
    For your thesis Contribution #2: safe exploitation in N-player FFA games 
    may require a human-behavioral (or population-behavioral) baseline instead 
    of a Nash baseline."
```

### Paper 4: Chalkiadakis, Elkind & Wooldridge — "Computational Aspects of Cooperative Game Theory" (2011)

**Link:** (Morgan & Claypool Synthesis Lectures — available via university library or https://www.morganclaypool.com/)

This is a slim textbook (~160 pages), not a paper. You need Chapters 2–4.

- **Chapters 1:** What cooperative game theory is and how it differs from non-cooperative GT. *Prior context: you've studied non-cooperative GT extensively (Steps 2–8). Cooperative GT is the other half: it asks "which coalitions will form and how will they divide the payoff?" instead of "what strategies will each individual player choose?"*
- **Chapters 2–3 (READ):** The core solution concepts: Shapley value, core, nucleolus, bargaining set. These are the mathematical tools for analyzing coalition stability and fair payoff division. For each concept understand: (a) what it means informally, (b) the formula, (c) when it exists (some games have an empty core!), (d) computational complexity.
- **Chapter 4 (READ):** Coalition structure generation — how to find the OPTIMAL partition of players into coalitions. N-player games have 2^N possible coalitions and B_N possible coalition structures (Bell number — grows super-exponentially). This chapter covers algorithms for searching this space.
- **Chapters 5+ (SKIM titles only):** Extensions (games with externalities, overlapping coalitions, dynamic settings). *Context for what's beyond the scope — you'll revisit in thesis work.*

```
├── READ:  Chapters 2–4 (Shapley value, core, nucleolus definitions + algorithms,
│          coalition structure generation)
├── SKIM:  Chapter 1 (basics — much you already know from non-cooperative GT),
│          Chapter 5+ (titles and first paragraphs — extensions, dynamic settings)
├── MATH:  → "The Shapley value formula — MUST know. The core constraints (linear 
│             program) — MUST know. Coalition structure generation algorithms 
│             (Chapter 4) — understand the search space, skim algorithm details."
└── KEY INSIGHT: "Cooperative GT gives you the TOOLS to analyze coalitions: who 
    should cooperate, how to divide gains, when a coalition is stable. But 
    classical cooperative GT assumes STATIC coalitions decided before the game.
    Your thesis challenge (Step 11) is the DYNAMIC case: coalitions form, evolve,
    and dissolve DURING the game. No classical solution concept handles this."
```

### Paper 5: Wang, Zhang, Kim & Gu — "Shapley Q-value: A Local Reward Approach to Solve Global Reward Games" (AAAI 2020)

**Link:** https://arxiv.org/abs/1907.05707

```
├── READ:  Section 3 (Shapley Q-value — decomposes the team's joint Q-value into
│          per-agent Shapley values. Each agent's "credit" for the team's success
│          is its Shapley value: the average marginal contribution across all 
│          possible coalition orderings. This gives each agent a LOCAL reward 
│          derived from the GLOBAL reward),
│          Section 4 (Algorithm — how to compute/approximate Shapley Q-values 
│          in practice. Exact computation: sum over all 2^N subsets. 
│          Approximation: Monte Carlo sampling of coalition orderings)
├── SKIM:  Abstract, Section 1 (Introduction — credit assignment problem in MARL),
│          Section 5 (Experiments — cooperative games)
├── SKIP:  Detailed experimental tables (check headline results only)
├── MATH:  → "The Shapley Q-value decomposition formula (Eq. 3-5). MUST understand.
│             Q_shapley_i(s,a) = E_π[Σ_S⊆N\{i} (|S|!(n-|S|-1)!/n!) * 
│             (Q(s, a_S∪{i}) - Q(s, a_S))]. This is Shapley's formula applied to 
│             Q-values instead of coalition values. The key approximation: sample 
│             random permutations instead of summing over all subsets."
└── KEY INSIGHT: "Shapley Q-value solves the credit assignment problem in 
    cooperative MARL. For your SLS implementation: instead of giving all credit to 
    the winner (sparse reward), decompose each state's value into per-agent Shapley 
    contributions. This lets agents learn WHO they're really helping with each action, 
    which is exactly the signal needed for coalition-aware learning."
```

### Supplementary References

- **Li, Kuang, Wang, Liu, Chen, Wu & Xiao (2021, KDD) — "Shapley Counterfactual Credits for Multi-Agent Reinforcement Learning"**  
  https://arxiv.org/abs/2106.00285  
  *Combines Shapley values with counterfactual baselines (reminiscent of CFR's counterfactual regret). SKIM Section 3 for the counterfactual Shapley mechanism. Connection: your CFR expertise (Steps 2–4) meets cooperative GT here.*

- **Wang, Li, Kaski & Lawry (2025) — "Shapley Machine: A Game-Theoretic Framework for N-Agent Ad Hoc Teamwork"**  
  https://arxiv.org/abs/2506.11285  
  *N-agent ad hoc teamwork = implicit coalition formation with unknown teammates. SKIM for the connection between Shapley values and ad hoc team formation.*

- **Meta AI — "Human-Level Play in the Game of Diplomacy by Combining Language Models with Strategic Reasoning" (CICERO, Science 2022)**  
  https://www.science.org/doi/10.1126/science.ade9097  
  *The full-press Diplomacy system — combines language model for negotiation with game-theoretic planning. SKIM for architecture insights only. You will NOT implement language-based negotiation, but the planning component (Section 2) shows how to integrate coalition reasoning into search.*

- **Mukobi et al. (2023) — "Welfare Diplomacy: Benchmarking Language Model Cooperation"**  
  https://arxiv.org/abs/2310.08901  
  *LLM agents playing Diplomacy variants. Relevant for Step 12 bridge (LLM agents in strategic settings). SKIM abstract only.*

### Math Flags

🔢 **Shapley value formula** — Must understand and implement.  
**WHY:** The Shapley value φ_i(v) = Σ_{S⊆N\{i}} (|S|!(n-|S|-1)!/n!) * [v(S∪{i}) - v(S)] is the central computational tool for this step. It tells you each player's "fair share" of coalition value. In SLS: it tells you how much each chip-placement action helped or hurt each potential coalition. For your thesis (Contribution #2): Shapley values in FFA settings are the replacement for exploitability in the 2-player setting — they measure "how much does coalition membership benefit each agent?"

🔢 **The core (linear programming characterization)** — Must understand the definition.  
**WHY:** The core of a cooperative game is the set of payoff allocations where no coalition can profitably deviate. If the core is empty, NO coalition structure is stable — every arrangement of players can be "broken" by some subgroup deviating. For SLS: the game almost certainly has an empty core (because the game is zero-sum among 4 players: only 1 wins). This means coalitions are INHERENTLY UNSTABLE — they will always be betrayed eventually. Understanding this instability is key to modeling coalition dynamics.

🔢 **piKL regularization (Bakhtin et al., Section 2.2)** — Read the formula.  
**WHY:** This is the N-player replacement for Nash-based safety from Step 8. Instead of π_safe = Nash, use π_safe = human_prior. The regularized policy search minimizes KL(π, π_human) subject to performance constraints. For your thesis (Contribution #2): this suggests that safe exploitation in N-player FFA games uses a BEHAVIORAL baseline (from population or from human data) instead of an equilibrium baseline.

---

## Phase 4: Implementation (6 days)

### Project: Coalition-Aware Multi-Agent Training for So Long Sucker

**Language + Framework:** Python 3.10+ / PyTorch / Custom SLS environment (building on Sharan & Adak's framework)

Starting point: Sharan & Adak's SLS implementation + your Step 9 MARL infrastructure (MADDPG, MAPPO) + your Step 10 EGTA analysis

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| SLS environment (extended from Sharan & Adak) | 🟡 AI-ASSISTED | Start from their codebase, extend with coalition tracking and richer state representation. AI helps with GUI integration, you write the game logic extensions. |
| Coalition detection from action history | 🔴 HAND-CODE | This IS the thesis-relevant mechanism: inferring implicit coalitions from observed actions (who is placing whose chips, who captures whose piles). Directly extends Step 7's opponent modeling to alliance modeling. |
| Shapley value credit assignment for SLS | 🔴 HAND-CODE | Adapting Shapley Q-value to the FFA setting. Must understand the decomposition deeply: in a 4-player game, each action's credit is distributed among all possible coalitions. |
| MARL training with coalition-aware rewards | 🔴 HAND-CODE | The core training loop: agents train with Shapley-decomposed rewards instead of sparse winner-takes-all reward. This is the novel training signal that should produce coalition-aware agents. |
| Spinning top decomposition on SLS meta-game | 🔴 HAND-CODE | Apply Step 10's analytical tool to SLS: how much of the 4-player dynamics are transitive (skill) vs cyclic (coalition rock-paper-scissors)? |
| EGTA evaluation of SLS agent populations | 🔴 HAND-CODE | Apply Step 10's EGTA framework to SLS: compute meta-Nash of the SLS agent population. This is the multi-agent evaluation prototype for Contribution #3. |
| Baseline agents (random, heuristic, DQN from paper) | 🟡 AI-ASSISTED | Standard baselines for comparison. AI drafts, you verify. |
| Visualization (coalition graphs, Shapley attribution plots) | 🟢 AI-GENERATED | Standard plotting infrastructure. |

### Sub-phase Breakdown (6 days):

**Day 1 — SLS Environment Setup + Verification:**
- 🟡 Get the SLS environment working:
  ```python
  # Either use Sharan & Adak's code or implement from rules
  class SLSGame:
      def __init__(self, n_players=4, chips_per_player=7):
          self.n_players = n_players
          self.hands = {i: [i] * chips_per_player for i in range(n_players)}
          self.piles = []  # List of lists (each pile = sequence of chip colors)
          self.eliminated = set()
          self.current_player = 0
      
      def get_legal_actions(self):
          """Actions: place chip X on pile Y (or start new pile)."""
          actions = []
          for chip_color in set(self.hands[self.current_player]):
              for pile_idx in range(len(self.piles)):
                  actions.append(('place', chip_color, pile_idx))
              actions.append(('place', chip_color, 'new'))
          return actions
      
      def step(self, action):
          """Execute action, check for captures, check for eliminations."""
          # Place chip → check if pile captured → check if player eliminated
          ...
  ```
- Verify rules against De Carufel & Jerade's formalization
- Run random games to completion, verify game termination and winner selection
- **Key verification:** In the 2-player endgame, does the analytical winner (from De Carufel & Jerade) match the simulation? This is your implementation correctness check.

**Day 2 — Coalition Detection Module:**
- 🔴 Implement coalition inference from action history:
  ```python
  class CoalitionDetector:
      """Detect implicit coalitions from observed chip-placement behavior."""
      def __init__(self, n_players):
          self.n_players = n_players
          # Help matrix: help[i][j] = how many times player i placed player j's chips
          self.help_matrix = np.zeros((n_players, n_players))
          # Harm matrix: harm[i][j] = how many times player i captured player j's chips
          self.harm_matrix = np.zeros((n_players, n_players))
      
      def update(self, player, action, game_state):
          """Update coalition signals after an action."""
          if action[0] == 'place':
              chip_color = action[1]
              if chip_color != player:
                  # Player is playing someone else's chip — HELP signal
                  self.help_matrix[player][chip_color] += 1
          # Also track captures that hurt specific players
          ...
      
      def get_coalition_scores(self):
          """Compute pairwise coalition strength.
          coalition_score[i][j] = net help from i to j."""
          net_help = self.help_matrix - self.harm_matrix
          # Symmetrize: coalition between i and j = help[i][j] + help[j][i]
          coalition_strength = net_help + net_help.T
          return coalition_strength
      
      def detect_coalitions(self, threshold=2.0):
          """Identify active coalitions (pairs/triples with high mutual help)."""
          scores = self.get_coalition_scores()
          coalitions = []
          for i in range(self.n_players):
              for j in range(i+1, self.n_players):
                  if scores[i][j] > threshold:
                      coalitions.append((i, j, scores[i][j]))
          return coalitions
  ```
- **Connection to Step 7:** This is your opponent model adapted for alliance detection. Step 7 inferred opponent's HAND from behavior. Step 11 infers opponent's ALLIANCES from behavior. Same Bayesian inference principle, different observation space.
- Test on hand-crafted game histories: create a game log where players 0 and 1 clearly cooperate (always place each other's chips). Does the detector identify it?

**Day 3 — Shapley Credit Assignment for SLS:**
- 🔴 Implement Shapley Q-value decomposition for SLS:
  ```python
  def shapley_credit_assignment(game_state, action, agent_values, n_players=4):
      """Decompose the value of an action into per-agent Shapley credits.
      
      For a 4-player game, the action affects all players differently.
      The Shapley credit for player i = average marginal contribution of i
      across all possible "coalition orderings."
      
      In SLS context: when player 0 places player 1's chip on a pile,
      the Shapley credit distributes: how much did this help player 1?
      How much did it hurt players 2, 3? How much did player 0 benefit?
      """
      credits = np.zeros(n_players)
      # For each permutation of players, compute marginal contributions
      for perm in itertools.permutations(range(n_players)):
          for idx, player in enumerate(perm):
              # Coalition = players before this one in the permutation
              coalition_before = set(perm[:idx])
              coalition_after = coalition_before | {player}
              # Marginal contribution: value(S+{i}) - value(S)
              val_before = estimate_coalition_value(game_state, coalition_before, agent_values)
              val_after = estimate_coalition_value(game_state, coalition_after, agent_values)
              credits[player] += (val_after - val_before)
      credits /= np.math.factorial(n_players)
      return credits
  
  def estimate_coalition_value(game_state, coalition, agent_values):
      """Estimate value of a coalition in the current game state.
      Approximation: expected future reward if coalition members share resources."""
      if not coalition:
          return 0.0
      # Sum of individual value estimates for coalition members
      # with bonus for coalition synergy (shared chip placement)
      return sum(agent_values[i] for i in coalition) * (1 + 0.1 * len(coalition))
  ```
- **Key challenge:** In a competitive game, "coalition value" is ambiguous — there's no shared reward to divide. The adaptation: define coalition value as the INCREASE in winning probability when players cooperate. This requires estimating counterfactuals: "what would my winning probability be WITHOUT this ally?"
- Test on simple game states where coalition value is obvious (e.g., 2 players with many chips vs 2 players nearly eliminated)

**Day 4 — Coalition-Aware MARL Training:**
- 🔴 Extend your MADDPG or MAPPO from Step 9 with coalition-aware rewards:
  ```python
  class CoalitionAwareMAPPO:
      def __init__(self, n_players, state_dim, action_dim):
          # Each agent has its own policy + value network
          self.agents = [PPOAgent(state_dim, action_dim) for _ in range(n_players)]
          self.coalition_detector = CoalitionDetector(n_players)
          
      def compute_rewards(self, game_state, actions, winner):
          """Replace sparse winner-takes-all reward with Shapley-decomposed reward."""
          # Original: reward = +1 for winner, -1 for losers
          # Coalition-aware: reward = Shapley credit for this action
          
          shapley_credits = shapley_credit_assignment(
              game_state, actions, 
              [a.estimate_value(game_state) for a in self.agents]
          )
          
          # Blend: alpha * sparse_reward + (1-alpha) * shapley_reward  
          # This gives learning signal throughout the game, not just at end
          alpha = 0.3
          sparse = np.zeros(self.n_players)
          sparse[winner] = 1.0
          sparse[np.arange(self.n_players) != winner] = -1.0 / (self.n_players - 1)
          
          return alpha * sparse + (1 - alpha) * shapley_credits
  ```
- Train a population of 4 agents via self-play for 5000+ games
- Compare:
  - Sparse reward (winner-takes-all) — baseline from Sharan & Adak
  - Shapley-decomposed reward (this step's contribution)
- Metrics: average game length, win rate vs random, presence of coalition behavior (measured by coalition detector)

**Day 5 — Population Analysis + Meta-Game Construction:**
- 🔴 Build the SLS meta-game using Step 10's EGTA framework:
  ```python
  def build_sls_meta_game(agent_pool, n_games=500):
      """Construct empirical payoff tensor for 4-player SLS.
      
      Unlike 2-player games (payoff MATRIX), 4-player games have a 
      payoff TENSOR: payoff[i,j,k,l] = expected reward for agent i 
      when agents j,k,l are opponents.
      
      Simplification: compute average reward for each agent type against
      each combination of opponent types.
      """
      n_agents = len(agent_pool)
      # For 4-player: we need to evaluate all 4-tuples of agents
      payoffs = {}
      for combo in itertools.combinations_with_replacement(range(n_agents), 4):
          total_rewards = np.zeros(4)
          for _ in range(n_games):
              agents = [agent_pool[i] for i in combo]
              rewards = play_sls_game(agents)
              total_rewards += rewards
          payoffs[combo] = total_rewards / n_games
      return payoffs
  ```
- 🔴 Apply spinning top decomposition:
  - **Challenge:** Balduzzi's decomposition assumes 2-player (antisymmetric payoff matrix). For 4-player SLS, the payoff structure is a TENSOR, not a matrix. 
  - **Adaptation:** Project the 4-player payoff tensor into pairwise matchups — for each pair of agent types, compute their head-to-head performance when matched in random 4-player games. This gives you a 2D payoff matrix you can decompose.
  - Compute transitive ratio: expect SLS to have LARGE cyclic component (coalition dynamics = non-transitive: A+B beats C+D, B+C beats A+D, etc.)

**Day 6 — Comparison + Analysis:**
- Run the full comparison:
  | Method | Win Rate vs Random | Avg Game Length | Coalition Score | Shapley Variation |
  |--------|-------------------|-----------------|-----------------|-------------------|
  | Random baseline | 25% | X games | ~0 | ~0 |
  | DQN (Sharan & Adak) | ~40%? | Y games | low | low |
  | MAPPO (sparse reward) | ? | ? | ? | ? |
  | MAPPO + Shapley (this step) | ? | ? | higher? | higher? |

- 🟢 Create visualizations:
  - Coalition detection over time: at each turn, which pairs have positive coalition scores?
  - Shapley attribution plot: for the winning agent, how did each turn's Shapley credit accumulate?
  - Coalition formation/dissolution timeline: when do alliances form and when do they break?
  - Spinning top transitive ratio for SLS meta-game

### Deliverables:
- [ ] Working SLS environment, verified against De Carufel & Jerade's rules
- [ ] Coalition detection module (help/harm matrices → alliance inference)
- [ ] Shapley credit assignment for SLS adapted to competitive setting
- [ ] Coalition-aware MAPPO training producing agents that form implicit coalitions
- [ ] EGTA meta-game analysis for 4-player SLS agent population
- [ ] Spinning top decomposition adapted for the N-player meta-game
- [ ] Comparison: sparse reward vs Shapley reward training on SLS
- [ ] Coalition dynamics visualizations (formation/dissolution over game turns)

### Validation:
- **SLS environment:** 2-player endgame outcomes match De Carufel & Jerade's analytical results.
- **Coalition detection:** On hand-crafted cooperative logs, detector correctly identifies the cooperating pair.
- **Shapley values:** On symmetric game states, all players get equal Shapley credit. On asymmetric states (one player clearly helping another), the helper-helpee pair gets high mutual credit.
- **Coalition-aware agents:** Agents trained with Shapley rewards should show HIGHER coalition scores (via the detector) than agents trained with sparse rewards. Whether they WIN more is secondary — the primary validation is that they FORM COALITIONS.
- **Spinning top on SLS:** Expect significant cyclic component (>50%), confirming that FFA coalition dynamics are non-transitive.

---

## Phase 5: Consolidation (2 days)

### Day 1 — Survey Skim + Cross-References

- **Reference skim:** Chalkiadakis, Elkind & Wooldridge (2011) — Chapters 5–6  
  *Dynamic coalition formation and games with externalities. Skim for: does any classical theory address the DYNAMIC coalition case? (Answer: very little — most theory is static, which is exactly your PhD gap.)*

- **Supplementary skim:** Li et al. (2021, KDD) — "Shapley Counterfactual Credits for MARL"  
  https://arxiv.org/abs/2106.00285  
  *Read Section 3: counterfactual Shapley — combines counterfactual baselines (from your CFR expertise, Steps 2–4) with Shapley decomposition. Could this improve your SLS credit assignment?*

- **Supplementary skim:** Wang et al. (2025) — "Shapley Machine: N-Agent Ad Hoc Teamwork"  
  https://arxiv.org/abs/2506.11285  
  *Read abstract + method overview. Ad hoc teamwork = joining a team of unknown agents without pre-coordination. This is exactly what happens when a new coalition forms in SLS — you don't know if your "ally" will cooperate or betray.*

- **Forward scan:** Skim arXiv for any new SLS or FFA coalition papers since the freshness scan. Search: "So Long Sucker", "coalition formation competitive", "multi-player free-for-all".

### Day 2 — PhD Mapping + One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 2] Nash equilibrium → [Step 11] Nash is nearly useless in FFA games. In a 4-player zero-sum game, Nash tells each player to minimize their maximum loss — but this ignores coalitions entirely. The "safe" strategy according to Nash might be terrible if other players coordinate. This is the fundamental limitation that motivates Contribution #2.
    - [Step 7] Opponent model (hand inference from actions) → [Step 11] Coalition detector (alliance inference from actions). Same Bayesian principle: observe behavior → update beliefs. In Step 7, you infer what cards the opponent HOLDS. In Step 11, you infer which players are ALIGNED. The state space changes; the methodology doesn't.
    - [Step 8] Safe exploitation (bounded deviation from Nash) → [Step 11] In FFA games, the "safe baseline" shifts from Nash to BEHAVIORAL PRIOR (piKL from Bakhtin et al.). This is the most important theoretical insight of Phase E: as games become multi-player, EQUILIBRIUM-BASED safety becomes intractable and is replaced by EMPIRICAL/BEHAVIORAL safety.
    - [Step 9] MADDPG/MAPPO → [Step 11] MARL training extended to 4 players. Centralized critic now sees ALL agents' observations — the critic can learn coalition structure implicitly.
    - [Step 10] Spinning top decomposition → [Step 11] CONFIRMED: SLS meta-game has large cyclic component (coalition dynamics ARE non-transitive). This validates Step 10's prediction.
    - [Step 10] EGTA → [Step 11] EGTA on the 4-player payoff tensor is the evaluation mechanism. But the tensor dimensionality explosion (payoff_matrix → payoff_tensor) is a challenge.
    - [Step 11] Shapley credit in FFA → prediction: [Step 13] Playtech's multi-table poker data may contain implicit coalitions (chip dumping, soft-play). The coalition detector from Step 11 could be adapted for collusion detection in real poker data. This directly connects to Contribution #3.
    - [Step 11] Dynamic coalition instability → prediction: [Step 14] The evaluation framework must handle non-stationary opponent populations where coalition structures shift mid-evaluation. Standard exploitability (fixed opponent assumption) breaks down.
  - **Confusions:**
    - [Step 11] The Shapley value assumes the grand coalition is optimal and asks "how to divide the gains fairly." But in SLS, the grand coalition makes no sense (only 1 player wins). How should the Shapley decomposition be adapted for purely competitive settings where coalition help is TEMPORARY? → PARTIALLY ADDRESSED (use Shapley for credit, not for payoff division)
    - [Step 11] Coalition detection from action history is noisy — a player might place another's chip for strategic reasons (not alliance). Can the detector distinguish "genuine alliance" from "strategic manipulation"? → OPEN (relates to deception detection, potentially Step 13)
    - [Step 11] In 4-player SLS, there are only 3 possible pairwise coalitions ({01,23}, {02,13}, {03,12}) plus 4 possible 3-vs-1 coalitions. For larger N (e.g., 6-player poker), the coalition space explodes. How to scale? → OPEN (for thesis scaling work)
    - [Step 8→11] Step 8 proved: safe exploitation is optimal in 2-player zero-sum games (deviate from Nash only against exploitable opponents). In 4-player SLS: (a) Nash is intractable, (b) game is not zero-sum pairwise (coalitions create positive-sum subgames between allies). What IS the "safe" strategy? → OPEN (THIS IS THE CORE OF CONTRIBUTION #2)
    - [Step 10→11] The spinning top decomposition on the projected 2D payoff matrix may lose information about 3-player and 4-player coalition effects. Is there a proper multi-player spinning top decomposition? → OPEN (potentially novel contribution)

### PhD Connection

This step is the THESIS FRONTIER. Everything from Steps 2–10 was building existing tools. Step 11 enters unstudied territory:

- **Contribution #1 (Behavioral Adaptation):** The coalition detector extends opponent modeling from "what kind of player is this?" to "who is allied with whom?" This is the multi-agent generalization of behavioral adaptation: instead of adapting to one opponent's style, you adapt to the SOCIAL STRUCTURE of the game.
- **Contribution #2 (Multi-Agent Safe Exploitation):** The central thesis gap crystallizes here:
  - In 2-player games: safe exploitation = bounded deviation from Nash. Well-studied.
  - In N-player FFA games: Nash is intractable AND strategically useless (ignores coalitions). The "safe baseline" must be something else — Bakhtin et al.'s piKL suggests a BEHAVIORAL prior, Step 10's population mechanisms suggest a POPULATION-LEVEL baseline. Your thesis contribution: define and prove safety guarantees for N-player FFA settings, likely using a behavioral or population-based safety notion instead of an equilibrium one.
  - SLS is the TESTBED for this contribution. It's small enough to analyze exhaustively (4 players, finite state space) but rich enough to exhibit real coalition dynamics.
- **Contribution #3 (Evaluation Methodology):** Standard exploitability doesn't work in N-player games (no clear "best response" against a coalition). The EGTA meta-game over agent populations + Shapley credit decomposition provides the alternative evaluation framework. SLS is where you prototype and validate this framework.

---

## Exit Checklist

- [ ] SLS environment working and verified against formal rules + endgame analysis
- [ ] Coalition detection module tested on hand-crafted and learned game histories
- [ ] Shapley credit assignment implemented and verified on symmetric/asymmetric game states
- [ ] Coalition-aware MAPPO agents trained and showing coalition behavior (measured by detector)
- [ ] Can explain from memory: Shapley value formula and what it means in FFA settings
- [ ] Can explain from memory: the core of a cooperative game and why SLS likely has an empty core
- [ ] Can explain from memory: why Nash equilibrium fails as a safety baseline in N-player FFA games
- [ ] Can explain from memory: piKL regularization and why behavioral priors replace Nash in N-player settings
- [ ] EGTA meta-game constructed for SLS agent population (payoff tensor, not matrix)
- [ ] Spinning top decomposition applied — cyclic component quantified for SLS
- [ ] Comparison table: sparse reward vs Shapley reward agents on SLS
- [ ] All 🔴 components hand-coded (coalition detector, Shapley credit, coalition-aware training, meta-game analysis, spinning top adaptation)
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Steps 2–10 + new confusions + thesis gap crystallization)
- [ ] PhD connection documented (N-player safety gap = Contribution #2 core, coalition detector = Contribution #1 extension, EGTA on SLS = Contribution #3 prototype)
- [ ] Step notes committed to repo
