# Step 14 — Evaluation Frameworks + Exploitability Metrics

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 8 (Safe Exploitation), Step 11 (Dynamic Coalition Formation), Step 13 (Behavioral Analysis Pipelines)  
**Phase:** G — Integration  
**Freshness Note:**  
- ArXiv search: '"approximate exploitability" game' (Mar 2026) — 2 results:  
  - Timbers, Bard, Lockhart, Lanctot, Schmid, Burch, Schrittwieser, Hubert & Bowling (2020/2022) "Approximate Exploitability: Learning a Best Response in Large Games" (arXiv:2004.09677) — **core reference.** Introduces ISMCTS-BR, a scalable search-based deep RL algorithm for learning approximate best responses, thereby approximating worst-case performance. Tested against AlphaZero-based agents in two-player zero-sum games. *The definitive paper on scaling exploitability computation beyond small games.*  
  - Martin & Sandholm (2023/2024, AAMAS 2025) "ApproxED: Approximate Exploitability Descent via Learned Best Responses" (arXiv:2301.08830) — proposes ApproxED: two methods for minimizing approximate exploitability in continuous-action games using learned best-response functions. A strategy profile and best-response network are trained simultaneously (adversarial). Evaluated on continuous games and GAN training. *Supplementary — relevant for the continuous-action formulation and the adversarial training approach to exploitability minimization.*  
- ArXiv search: "game theoretic evaluation agent Elo Nash ranking" (Mar 2026) — 3 results:  
  - **Lanctot, Larson, Bachrach, Marris, Li, Bhoopchand, Anthony, Tanner & Koop (2023, revised Jun 2025) "Evaluating Agents using Social Choice Theory" (arXiv:2312.03121)** — **critical new discovery.** Introduces VasE (Voting-as-Evaluation): frames multi-agent evaluation through social choice theory. Each task = a voter, agents = candidates. Uses ordinal rankings instead of cardinal scores. Identifies "maximal lotteries" as satisfying key consistency axioms. Shown to be MORE ROBUST than Elo and Nash averaging, discovers intransitive cycles, and predicts outcomes better than Elo in a 7-player game. Computationally efficient (polynomial). *Core — the freshest and most principled approach to multi-agent evaluation. Directly relevant to Contribution #3. The social choice framing is novel and the axioms provide justification the thesis needs.*  
  - Yan, Duan, Shi, Zhong, Marden & Bullo (2020) "Policy Evaluation and Seeking for Multi-Agent Reinforcement Learning via Best Response" (arXiv:2006.09585) — introduces cycle-based and memory-based metrics grounded on sink equilibrium for MARL evaluation. *Supplementary.*  
  - Rowland, Omidshafiei, Tuyls, Perolat, Valko, Piliouras & Munos (2019) "Multiagent Evaluation under Incomplete Information" (arXiv:1909.09849) — investigates evaluation with noisy game outcomes using α-Rank. Derives sample complexity for confident ranking. Adaptive algorithms with correctness guarantees. Tested on Kuhn poker. *Core — addresses exactly the noise problem: real evaluation data is noisy, α-Rank needs uncertainty quantification.*  
- ArXiv search: '"Nash averaging" evaluation agent game' (Mar 2026) — 1 result: same Lanctot VasE paper.  
- ArXiv search: '"alpha-rank" multi agent evaluation ranking' (Mar 2026) — 1 result: same Yan et al. (2020) paper.  
- ArXiv search: "OpenSpiel evaluation benchmark game" (Mar 2026) — 1 result:  
  - Cipolina-Kun, Nezhurina & Jitsev (Aug 2025) "Game Reasoning Arena: A Framework and Benchmark for Assessing Reasoning Capabilities of Large Language Models via Game Play" (arXiv:2508.03368) — *Supplementary — LLM evaluation through games, connects to Step 12's LLM agent assessment.*  
- ArXiv search: "AIVAT variance reduction poker" (Mar 2026) — rate-limited, no results extracted. Known reference: Burch, Johanson & Bowling (2019, AAAI) "AIVAT: A New Variance Reduction Technique for Agent Evaluation in Imperfect Information Games." *Will use from existing knowledge.*  
- ArXiv search: "exploitability imperfect information game evaluation" (Mar 2026) — failed to extract. Known core reference: Johanson et al. (2011) "Accelerating Best Response Calculation in Large Extensive Games."  
- **Known core references (not found via keyword search — well-established):**  
  - Omidshafiei, Papadimitriou, Piliouras, Tuyls et al. (2019, Nature Sci. Reports) "α-Rank: Multi-Agent Evaluation by Evolution" — original α-Rank paper. Uses Markov-Conley chains from evolutionary dynamics for game-theoretic ranking. *Core — the standard for multi-agent evaluation beyond Elo.*  
  - Balduzzi, Tuyls et al. (2019) "Re-evaluating Evaluation" (NeurIPS) — spinning top decomposition. Payoff matrix = transitive + cyclic components. *Already studied in Step 10. Core for evaluation diagnostics.*  
  - Burch, Johanson & Bowling (2019, AAAI) "AIVAT: A New Variance Reduction Technique for Agent Evaluation in Imperfect Information Games" — unbiased, low-variance estimator for agent performance in poker/imperfect-information games. *Core — essential for Step 13's Playtech data evaluation.*  
  - Johanson et al. (2011) "Accelerating Best Response Calculation in Large Extensive Games" — foundational for exploitability computation efficiency.  
  - Tuyls et al. (2018) "A Generalised Method for Empirical Game Theoretic Analysis" (AAMAS) — EGTA framework. *Already studied in Step 10. Core for population evaluation.*  
  - Lanctot et al. (2019) "OpenSpiel: A Framework for Reinforcement Learning in Games" — the standard library. *Already used throughout.*  
- **Cross-references from prior steps:**  
  - Step 8: Exploitability computation (exact) for Kuhn/Leduc, adaptation safety (Ge 2024), safety checker module, tournament framework prototype.  
  - Step 10: EGTA analysis of PBT league, spinning top decomposition, meta-Nash of population, Elo tracking, diversity metrics.  
  - Step 11: Coalition detector (help/harm matrices), SLS evaluation (win rates, coalition formation frequency, betrayal timing).  
  - Step 13: Playtech behavioral pipeline (player stats, BC accuracy, player2vec embeddings, style classification, collusion detection scores).  
- **Field assessment:** Multi-agent evaluation is an ACTIVE and well-studied field — far more developed than poker behavioral analysis (Step 13). The landscape has three layers: (1) **single-agent metrics** (exploitability, best-response value), (2) **population-level metrics** (Elo, α-Rank, Nash averaging, VasE), and (3) **variance-reduction methods** (AIVAT for noisy games). The freshest significant work is Lanctot et al.'s VasE (2023/2025), which argues that social choice theory provides axiomatically grounded evaluation — potentially displacing both Elo and α-Rank. The Timbers ISMCTS-BR paper (2020/2022) remains the standard for scaling exploitability computation. This step's thesis contribution value: INTEGRATING these layers into a unified framework applied across multiple game types (Kuhn, Leduc, SLS, Playtech data) — no existing paper combines all three layers on diverse game types.

---

## Phase 1: Intuition (1 day)

The goal: understand WHY evaluation in games is fundamentally harder than evaluation in single-agent settings (intransitivity: A beats B, B beats C, C beats A → who is "best"?), WHAT metrics exist (exploitability, Elo, α-Rank, Nash averaging, VasE), and WHY a unified framework matters for the thesis (Contribution #3 requires evaluation that works across 2-player, N-player, cooperative, and competitive games — no single existing metric does this).

End of day: you should be able to explain to a non-expert: "If I train an AI poker player and say it won 60% of games, that sounds good. But against WHOM? Against random players? Against other AIs? Against the best players? And what if it wins 90% against aggressive opponents but loses 80% against passive ones — is it 'good' or 'bad'? Evaluation in games requires answering: (1) how exploitable is this agent by a worst-case adversary? (exploitability), (2) how does it rank against a population of diverse opponents? (α-Rank, VasE), and (3) can we measure this accurately without playing millions of games? (AIVAT). Building a framework that answers ALL THREE questions across different game types is what this step delivers."

### Videos

- **Marc Lanctot — "OpenSpiel: A Framework for RL in Games" (2019/2020 talk)**  
  Search YouTube: "Marc Lanctot OpenSpiel" or "OpenSpiel reinforcement learning games"  
  Duration: ~30-40m  
  *Lanctot is co-author of both OpenSpiel and the VasE paper. Watch for: how the research community evaluates agents in practice, the problems with Elo in game AI, and why game-theoretic evaluation is needed.*

- **Karl Tuyls / DeepMind — "α-Rank: Multi-Agent Evaluation by Evolution" (talk)**  
  Search YouTube: "alpha-rank multi agent evaluation DeepMind"  
  Duration: ~30m  
  *The original α-Rank presentation. Key idea: instead of solving for Nash equilibrium of the meta-game (computationally expensive), use Markov-Conley chains from evolutionary dynamics (polynomial time). The ranking is the stationary distribution of a random walk on the strategy space. Watch for: how α-Rank differs from Elo, why it handles intransitivity, and its computational complexity.*

- **David Balduzzi — "Re-evaluating Evaluation" (NeurIPS 2019 talk or similar)**  
  Search YouTube: "Balduzzi re-evaluating evaluation spinning top"  
  Duration: ~20m  
  *Already watched in Step 10 — REWATCH with evaluation framework lens. The spinning top decomposition tells you WHAT FRACTION of the competitive structure is "real skill" (transitive) vs "rock-paper-scissors" (cyclic). This diagnostic should be part of any evaluation report for the thesis.*

### Blog Posts / Accessible Reads

- **DeepMind Blog — "AlphaRank: Multi-Agent Evaluation"**  
  Search: "deepmind alpha-rank" or "deepmind multiagent evaluation"  
  *The accessible blog version of the α-Rank paper. Clear diagrams of the Markov chain construction.*

- **Elo rating system — Wikipedia**  
  https://en.wikipedia.org/wiki/Elo_rating_system  
  *Quick refresher on Elo: originally for chess, assumes transitive skill. The key weakness for game AI: Elo CANNOT capture intransitivity. If your agents play rock-paper-scissors, Elo assigns roughly equal ratings — but α-Rank identifies the cycling structure.*

- **OpenSpiel documentation — Evaluation tools**  
  https://github.com/google-deepmind/open_spiel  
  *Browse the evaluation utilities in OpenSpiel: exploitability computation (for small games), best-response oracles, Elo tracking, AIVAT. These are the building blocks you'll use and extend.*

---

## Phase 2: Exploration (2 days)

### Day 1: Audit Existing Evaluation Code from Prior Steps

1. **Inventory all evaluation code you've written so far:**
   - 🔴 Systematic audit — this is the consolidation moment for the PhD:
     ```python
     # From Step 3: CFR exploitability tracking
     # → What: compute_exploitability(strategy, game) for Kuhn/Leduc
     # → Status: exact computation, works for small games, O(|game_tree|)
     
     # From Step 8: Safety checker + exploitation metrics
     # → What: exploitability_of(strategy), safety_violation(exploit_strategy, baseline)
     # → Status: works for Kuhn/Leduc, ties into RNR/Ganzfried/SES pipeline
     
     # From Step 10: EGTA analysis + spinning top
     # → What: build_empirical_game(league), compute_meta_nash(payoff_matrix),
     #   spinning_top_decomposition(payoff_matrix) → (transitive_ratio, cyclic_ratio)
     # → Status: works on Leduc league, 7-agent scale
     
     # From Step 10: Elo tracking
     # → What: update_elo(player_ratings, match_result)
     # → Status: basic implementation, tracks league training progress
     
     # From Step 11: SLS evaluation
     # → What: coalition_formation_frequency, betrayal_timing, help_harm matrices
     # → Status: SLS-specific metrics, not yet generalized
     
     # From Step 13: Playtech behavioral evaluation
     # → What: BC accuracy, style classification accuracy, collusion detection scores
     # → Status: domain-specific, not yet integrated with game-theoretic metrics
     ```
   - **Key question:** Can these be unified under a single evaluation API? What's the common interface?

2. **Design the evaluation framework API:**
   - 🔴 HAND-CODE the design — this IS Contribution #3:
     ```python
     class EvaluationFramework:
         """Unified evaluation framework for game-playing agents.
         
         Three evaluation layers:
         1. Agent-level: How exploitable is this single agent?
            → exploitability, best-response value, adaptation safety
         2. Population-level: How does this agent rank among diverse opponents?
            → Elo, α-Rank, VasE, Nash averaging, meta-Nash
         3. Statistical: How confident are we in these measurements?
            → AIVAT variance reduction, confidence intervals, sample complexity
         
         The framework should work across:
         - 2-player zero-sum (Kuhn, Leduc, Hold'em)
         - N-player competitive (SLS)
         - Real-world data (Playtech)
         """
         
         def __init__(self, game_type, agents):
             self.game_type = game_type
             self.agents = agents
             self.results = {}
         
         def evaluate_exploitability(self, agent):
             """Layer 1: Compute or approximate exploitability."""
             if self.game_type.is_small():
                 return exact_exploitability(agent, self.game_type)
             else:
                 return approximate_exploitability(agent, self.game_type)
         
         def evaluate_population(self, method='vase'):
             """Layer 2: Rank agents in a population context."""
             payoff_matrix = self.build_payoff_matrix()
             if method == 'elo':
                 return compute_elo_ratings(payoff_matrix)
             elif method == 'alpha_rank':
                 return compute_alpha_rank(payoff_matrix)
             elif method == 'vase':
                 return compute_vase(payoff_matrix)
             elif method == 'meta_nash':
                 return compute_meta_nash(payoff_matrix)
         
         def evaluate_with_confidence(self, agent1, agent2, n_games=10000):
             """Layer 3: Measure performance with confidence intervals."""
             if self.game_type.has_hidden_info():
                 # Use AIVAT for variance reduction
                 return aivat_evaluate(agent1, agent2, n_games)
             else:
                 # Standard evaluation with bootstrapped CIs
                 return standard_evaluate(agent1, agent2, n_games)
     ```

### Day 2: Build the Bot Zoo

3. **Construct the bot zoo:**
   - 🔴 This is the evaluation INFRASTRUCTURE — every comparison needs it:
     ```python
     class BotZoo:
         """Collection of reference agents for benchmarking.
         
         The zoo provides diverse opponents for evaluation:
         - Trivial agents (random, always-call, always-fold)
         - Heuristic agents (tight-aggressive, loose-aggressive)
         - Solved agents (Nash/CFR, from Step 3)
         - Learned agents (DQN from Step 5, PSRO from Step 9, DT from Step 12)
         - Exploitation agents (safe exploiter from Step 8)
         """
         
         def __init__(self, game_type):
             self.game_type = game_type
             self.agents = {}
             self._build_zoo()
         
         def _build_zoo(self):
             # Tier 1: Trivial baselines
             self.agents['random'] = RandomAgent(self.game_type)
             self.agents['always_call'] = AlwaysCallAgent(self.game_type)
             self.agents['always_fold'] = AlwaysFoldAgent(self.game_type)
             
             # Tier 2: Heuristic agents
             self.agents['tight_agg'] = TightAggressiveAgent(self.game_type)
             self.agents['loose_agg'] = LooseAggressiveAgent(self.game_type)
             self.agents['tight_passive'] = TightPassiveAgent(self.game_type)
             
             # Tier 3: Computed agents (from prior steps)
             self.agents['nash_cfr'] = load_cfr_agent(self.game_type)  # Step 3
             self.agents['dqn'] = load_dqn_agent(self.game_type)       # Step 5
             
             # Tier 4: Advanced agents (from later steps)
             if self.game_type.supports_psro():
                 self.agents['psro'] = load_psro_agent(self.game_type)   # Step 9
             if self.game_type.supports_dt():
                 self.agents['dt'] = load_dt_agent(self.game_type)       # Step 12
         
         def round_robin(self, n_games_per_pair=10000):
             """Run every pair of agents against each other.
             Returns the payoff matrix."""
             agents = list(self.agents.values())
             n = len(agents)
             payoff_matrix = np.zeros((n, n))
             for i in range(n):
                 for j in range(n):
                     if i != j:
                         payoff_matrix[i, j] = evaluate_pair(
                             agents[i], agents[j], n_games_per_pair
                         )
             return payoff_matrix
     ```
   - Build bot zoo for Kuhn poker (all tiers)
   - Build bot zoo for Leduc poker (all tiers)
   - Run round-robin tournament on both games
   - Sanity check: Nash agent should be approximately unexploitable, random should lose to everyone, always-fold should lose even more

---

## Phase 3: Targeted Reading (3 days)

### Paper 1: Timbers, Bard, Lockhart, Lanctot, Schmid, Burch, Schrittwieser, Hubert & Bowling — "Approximate Exploitability: Learning a Best Response in Large Games" (2022)
**Link:** https://arxiv.org/abs/2004.09677

- **READ:** Sections 1–4 (Introduction, Background, ISMCTS-BR Algorithm, Experiments)
  - KEY INSIGHT: Exploitability = value of best response - Nash value. In small games (Kuhn, Leduc), compute exactly. In large games (Go, StarCraft), you can't enumerate the game tree → train a NEURAL NETWORK to approximate the best response → use its value as an upper bound on exploitability. ISMCTS-BR combines Monte Carlo Tree Search with deep RL to learn this approximate best response.
  - Architecture: ISMCTS provides the search structure (handles imperfect info), deep RL trains the value/policy networks within the search, the resulting agent IS the approximate best response.
  - Evaluation: tested against AlphaZero agents in various games. The approximate exploitability tracks the true exploitability in games where truth is computable.
- **SKIM:** Sections 5–6 (additional experiments, related work)
- **PhD Connection:** This is the BRIDGE from your exact exploitability computation (Steps 3, 8 on Kuhn/Leduc) to evaluation on larger games (Hold'em, Playtech data). When the game is too large for exact computation, ISMCTS-BR provides the approximate metric. You won't implement ISMCTS-BR from scratch (it requires significant infrastructure), but you should understand the approach to design your evaluation framework's "approximate" mode.

### Paper 2: Lanctot, Larson, Bachrach, Marris, Li, Bhoopchand, Anthony, Tanner & Koop — "Evaluating Agents using Social Choice Theory" (2023/2025)
**Link:** https://arxiv.org/abs/2312.03121

- **READ:** Entire paper carefully — this is the FRESHEST significant work in multi-agent evaluation
  - KEY INSIGHT: Frame evaluation as a VOTING problem. Each task/game is a voter, each agent is a candidate. Use social choice axioms (anonymity, monotonicity, Condorcet consistency) to select the "best" evaluation function. The paper identifies "maximal lotteries" as the method satisfying the most desirable axioms.
  - Comparison with existing methods: Elo assumes transitivity (violated in games with RPS dynamics), Nash averaging is intractable for large games, α-Rank uses evolutionary dynamics but has parameter sensitivity. VasE (maximal lotteries) is polynomial, handles intransitivity, and discovers cyclic structures.
  - Practical demonstration: outperforms Elo at predicting outcomes in a 7-player game (Diplomacy or similar).
- **PhD Connection:** VasE could be the evaluation backbone for Contribution #3. Its axiomatic foundations provide JUSTIFICATION for the evaluation choices in the thesis. If your framework uses VasE, you can cite specific axioms to explain WHY the ranking is meaningful — much stronger than just "we used Elo."

### Paper 3: Rowland, Omidshafiei, Tuyls, Perolat, Valko, Piliouras & Munos — "Multiagent Evaluation under Incomplete Information" (2019)
**Link:** https://arxiv.org/abs/1909.09849

- **READ:** Sections 1–4 (Introduction, Background, Sample Complexity, Adaptive Algorithms)
  - KEY INSIGHT: Real evaluation data is NOISY — game outcomes have variance (especially in poker). α-Rank's stationary distribution depends on the payoff matrix, so noisy estimates of payoffs propagate to noisy rankings. This paper derives HOW MANY GAMES you need to play before the ranking is confident. It also provides adaptive evaluation algorithms that focus matches on "close" agents to resolve their relative ranking efficiently.
  - Sample complexity: depends on the gap between agents — closer agents need more games to distinguish. Provides theoretical bounds.
  - Connection to poker: Kuhn poker evaluation data is noisy (card dealing, imperfect info). This paper tells you how to handle that noise.
- **SKIM:** Section 5 (experiments on Bernoulli games, soccer, Kuhn poker)
- **PhD Connection:** Direct toolkit for Contribution #3. Your evaluation framework must report CONFIDENCE alongside rankings. This paper provides the theory. The adaptive evaluation algorithm could be integrated into your tournament framework to efficiently allocate evaluation compute.

### Paper 4: Burch, Johanson & Bowling — "AIVAT: A New Variance Reduction Technique for Agent Evaluation in Imperfect Information Games" (2019, AAAI)
**Source:** Search Google Scholar for "AIVAT Burch Johanson Bowling 2019"

- **READ:** Entire paper (likely short, AAAI format)
  - KEY INSIGHT: In poker, evaluation variance is HUGE because of card luck. A good player can still lose many hands in a row. AIVAT removes the luck component by using the game tree structure to compute what WOULD have happened with different cards (counterfactual reasoning). The resulting estimate is unbiased and has dramatically lower variance.
  - Mechanism: uses a value function over information states (computable from CFR equilibrium) to construct a control variate for variance reduction. Each hand's result is adjusted: actual_result + (counterfactual_value - expected_value) → the luck cancels out.
  - This is why professional poker evaluation uses millions of hands — AIVAT reduces the number needed by 10-100x.
- **PhD Connection:** ESSENTIAL for Step 13's Playtech data evaluation and for any evaluation involving poker. Without AIVAT, you'd need 1M+ hands to reliably rank two agents. With AIVAT, ~10K hands may suffice. Your evaluation framework MUST include AIVAT for any imperfect-information game evaluation.

### Paper 5: Omidshafiei, Papadimitriou, Piliouras, Tuyls et al. — "α-Rank: Multi-Agent Evaluation by Evolution" (2019, Nature Scientific Reports)
**Source:** Search Google Scholar / Nature for "α-Rank multi-agent evaluation evolution 2019"

- **READ:** Sections 1–4 (Introduction, α-Rank definition, Theoretical Properties, Experiments)
  - KEY INSIGHT: Traditional evaluation (Elo) assumes transitivity and fails on non-transitive games. Nash equilibrium of the meta-game is NP-hard to compute in general. α-Rank uses a Markov chain (transition probabilities derived from evolutionary dynamics) whose STATIONARY DISTRIBUTION is the ranking. This is polynomial to compute and uniquely defined (unlike Nash which can have multiple equilibria).
  - Connection to Step 10's evolutionary dynamics: the replicator dynamics from Step 10 are the CONTINUOUS analog; α-Rank's Markov chain is the DISCRETE analog. Same foundation, different computational representations.
  - Parameter: α (selection pressure). Higher α → stronger winner-take-all. The ranking can change with α → need sensitivity analysis.
- **SKIM:** Sections 5–6 (additional games, large-scale evaluation)
- **PhD Connection:** α-Rank is the ESTABLISHED standard for multi-agent evaluation. Your framework should implement it for comparison with VasE (Lanctot's newer work). The interesting research question: when do α-Rank and VasE disagree? What does that tell you about the game's competitive structure?

### Supplementary Reading (skim as time permits):

- **Balduzzi, Tuyls et al. (2019) — "Re-evaluating Evaluation"** (NeurIPS): Already studied in Step 10. RE-SKIM with the evaluation framework lens. The spinning top's transitive ratio IS an evaluation diagnostic: high transitive ratio → Elo is fine; high cyclic ratio → need α-Rank/VasE.

- **Martin & Sandholm (2023/2024) — "ApproxED"** (arXiv:2301.08830, AAMAS 2025): Skim for the adversarial training approach to exploitability descent. The learned best-response + strategy profile co-training could be adapted as an evaluation subroutine for continuous-action games.

### Math Flags:

🔢 **α-Rank Markov chain construction** — Must understand the transition matrix. Given a payoff matrix $M$, the transition probability from strategy profile $s$ to $s'$ depends on the fitness advantage $M(s', s) - M(s, s)$, scaled by selection pressure $\alpha$. Compute this for a 3×3 RPS example (should produce a chain that cycles uniformly).  
**WHY this can't be substituted by algorithmic understanding:** The selection pressure α controls how "sharp" the ranking is. You need to understand the math to choose α appropriately for your games and to interpret α-sensitivity plots.

🔢 **AIVAT control variate construction** — The variance reduction relies on a value function $V(h)$ at each information state $h$. The AIVAT estimator is: $\hat{u}_{AIVAT} = u_{actual} + \sum_{h} (V(h_{counterfactual}) - V(h_{actual}))$, where the sum is over chance nodes (card deals). The value function comes from the CFR equilibrium. Verify: this estimator is unbiased ($E[\hat{u}_{AIVAT}] = E[u_{actual}]$) and has lower variance ($Var[\hat{u}_{AIVAT}] \leq Var[u_{actual}]$).  
**WHY this can't be substituted by algorithmic understanding:** The variance reduction factor depends on how good the value function $V$ is. If $V$ perfectly predicts outcomes, variance → 0. If $V$ is random, no reduction. The quality of your CFR solution (Step 3) directly determines the quality of your AIVAT evaluation (Step 14).

🔢 **VasE maximal lotteries** — A maximal lottery is a probability distribution $p$ over candidates (agents) such that for every other candidate $c$, $\sum_{c'} p(c') \cdot margin(c', c) \geq 0$, where $margin(c', c)$ is the number of voters preferring $c'$ to $c$ minus those preferring $c$ to $c'$. This is a linear feasibility problem. Compute for a 3-agent example with 5 game-tasks.  
**WHY this can't be substituted by algorithmic understanding:** The maximal lottery is the game-theoretic solution of the "tournament" defined by pairwise comparisons. Understanding the LP formulation lets you extend it to weighted tasks (some games matter more than others for the PhD).

---

## Phase 4: Implementation (6 days)

### Project: Unified Evaluation Framework — From Single-Agent Exploitability to Multi-Agent Population Rankings with Variance Reduction

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| EvaluationFramework API design | 🔴 HAND-CODE | This IS Contribution #3. The API design encodes the thesis's conceptual framework. |
| Exact exploitability computation (from Step 3/8) | 🟡 AI-ASSISTED | Refactor existing Step 3/8 code into the framework API. Logic already hand-coded. |
| Bot zoo construction | 🟡 AI-ASSISTED | Collecting agents from prior steps. Heuristic agents are simple to code. |
| α-Rank implementation | 🔴 HAND-CODE | Must understand the Markov chain construction to implement correctly and extend. |
| VasE (maximal lotteries) implementation | 🔴 HAND-CODE | Newest method, directly relevant to Contribution #3. Must understand the LP. |
| AIVAT variance reduction | 🔴 HAND-CODE | Critical for poker evaluation. Must understand the control variate construction. |
| Round-robin tournament runner | 🟢 AI-GENERATED | Standard infrastructure — run games, collect results, build payoff matrix. |
| Spinning top integration (from Step 10) | 🟡 AI-ASSISTED | Refactor Step 10 code into the framework. |
| Visualization + reporting | 🟢 AI-GENERATED | Plots, tables, LaTeX-ready output. |

**Day 1 — Layer 1: Exploitability Module**

- 🔴 Formalize the exploitability computation into a reusable module:
  ```python
  class ExploitabilityModule:
      """Layer 1: Single-agent exploitability evaluation.
      
      Exploitability(σ) = BR_value(σ) - Nash_value
      where BR_value(σ) = max_{σ'} u(σ', σ)
      
      For small games: exact computation via game tree traversal.
      For large games: approximate via learned best response (ISMCTS-BR style).
      """
      
      def __init__(self, game):
          self.game = game
          self.game_size = estimate_game_size(game)
      
      def exact_exploitability(self, strategy):
          """Exact exploitability for small games (Kuhn, Leduc).
          
          Traverse full game tree, compute best response value at each 
          information set.
          
          From Step 3/8: already implemented. Refactor into this module.
          """
          br_value = compute_best_response_value(strategy, self.game)
          nash_value = self.game.nash_value  # 0 for symmetric zero-sum
          return br_value - nash_value
      
      def approximate_exploitability(self, strategy, n_episodes=10000):
          """Approximate exploitability for large games.
          
          Train a RL agent as approximate best response.
          The trained agent's value is an upper bound on exploitability.
          
          Simplified version of ISMCTS-BR (Timbers et al.):
          use DQN (from Step 5) as the approximate best-response learner.
          """
          br_agent = DQNAgent(self.game.state_dim, self.game.action_dim)
          # Train BR agent against the fixed strategy
          for episode in range(n_episodes):
              state = self.game.reset()
              while not state.is_terminal():
                  if state.current_player == 0:
                      action = br_agent.act(state)
                  else:
                      action = strategy.act(state)
                  state = self.game.step(action)
              br_agent.update(state.reward)
          
          # Evaluate the trained BR agent
          br_value = evaluate_pair(br_agent, strategy, n_games=10000)
          return br_value - self.game.nash_value
      
      def adaptation_safety(self, exploit_strategy, baseline_strategy):
          """Ge et al. (2024) adaptation safety check.
          
          exploit_strategy is adaptation-safe if:
          exploitability(exploit) ≤ exploitability(baseline)
          
          From Step 8: already implemented. Integrate here.
          """
          exploit_exp = self.exact_exploitability(exploit_strategy)
          baseline_exp = self.exact_exploitability(baseline_strategy)
          return exploit_exp <= baseline_exp, exploit_exp, baseline_exp
  ```
- **Validation:** Cross-check with Step 3's exploitability values on Kuhn. Step 3 tracked CFR convergence → exploitability should match to 4 decimal places.
- **Test:** Compute exploitability for all bot zoo agents on Kuhn and Leduc. Verify: random agent has high exploitability, Nash/CFR agent has near-zero exploitability.

**Day 2 — Layer 2a: α-Rank Implementation**

- 🔴 Implement α-Rank from scratch:
  ```python
  class AlphaRank:
      """α-Rank: Multi-Agent Evaluation by Evolution.
      
      Given a payoff matrix M (n×n for 2-player, or n1×...×nk for k-player),
      construct a Markov chain over strategy profiles.
      The stationary distribution IS the ranking.
      
      Transition logic: from profile s, consider mutating one player's strategy.
      Probability of mutation s→s' depends on:
      - Fitness advantage: M(s', s) - M(s, s) (how much better s' does against s's context)
      - Selection pressure α: higher α → winner-take-all
      
      The transition uses the Fermi function:
      P(s→s') ∝ 1 / (1 + exp(-α * (fitness(s') - fitness(s))))
      """
      
      def __init__(self, payoff_matrix, alpha=100):
          self.M = payoff_matrix
          self.alpha = alpha
          self.n = payoff_matrix.shape[0]
      
      def build_transition_matrix(self):
          """Construct the Markov chain transition matrix."""
          T = np.zeros((self.n, self.n))
          for i in range(self.n):
              for j in range(self.n):
                  if i != j:
                      fitness_diff = self.M[j, i] - self.M[i, i]
                      # Fermi selection: probability j invades population of i
                      T[i, j] = 1.0 / (1.0 + np.exp(-self.alpha * fitness_diff))
              # Self-transition: probability no mutation fixes
              T[i, i] = 0
              row_sum = T[i].sum()
              if row_sum > 0:
                  T[i] /= row_sum
              else:
                  T[i, i] = 1.0
          return T
      
      def compute_ranking(self):
          """Compute stationary distribution = α-Rank ranking."""
          T = self.build_transition_matrix()
          # Power iteration or eigenvalue decomposition
          eigenvalues, eigenvectors = np.linalg.eig(T.T)
          # Find eigenvector for eigenvalue closest to 1
          idx = np.argmin(np.abs(eigenvalues - 1))
          stationary = np.real(eigenvectors[:, idx])
          stationary = stationary / stationary.sum()
          return stationary
      
      def sensitivity_analysis(self, alphas=[1, 10, 100, 1000]):
          """How does the ranking change with α?"""
          results = {}
          for a in alphas:
              self.alpha = a
              results[a] = self.compute_ranking()
          return results
  ```
- **Validation:**
  - On RPS payoff matrix: ranking should be approximately uniform (1/3, 1/3, 1/3) for all α
  - On transitive game (A > B > C): ranking should concentrate on A as α increases
  - Compare with OpenSpiel's α-Rank implementation if available

**Day 3 — Layer 2b: VasE (Maximal Lotteries) Implementation**

- 🔴 Implement VasE from Lanctot et al.:
  ```python
  class VasE:
      """Voting-as-Evaluation using Maximal Lotteries.
      
      Input: a set of 'voters' (games/tasks) and 'candidates' (agents).
      Each voter provides a pairwise ordering of candidates.
      
      Output: a maximal lottery — a probability distribution over candidates
      such that no other candidate is preferred by a majority.
      
      This is computed as the Nash equilibrium of the zero-sum game
      defined by the tournament matrix T, where T[i,j] = margin of i over j.
      """
      
      def __init__(self, agents, games):
          self.agents = agents
          self.games = games
          self.n_agents = len(agents)
      
      def build_tournament_matrix(self, payoff_matrices):
          """Build the pairwise margin matrix across all games.
          
          For each pair (i, j) of agents:
          Count how many games prefer i over j (i.e., M_game[i,j] > M_game[j,i])
          margin[i,j] = #games_preferring_i - #games_preferring_j
          """
          T = np.zeros((self.n_agents, self.n_agents))
          for M in payoff_matrices:
              for i in range(self.n_agents):
                  for j in range(self.n_agents):
                      if M[i, j] > M[j, i]:
                          T[i, j] += 1
                      elif M[i, j] < M[j, i]:
                          T[i, j] -= 1
          return T
      
      def maximal_lottery(self, T):
          """Compute the maximal lottery as Nash equilibrium of tournament T.
          
          Solve: max p^T T q  for the row player (LP)
          This is the Nash equilibrium of the symmetric zero-sum game T.
          """
          from scipy.optimize import linprog
          n = T.shape[0]
          # Standard LP formulation for maximin strategy
          # Maximize v subject to: T @ p >= v, sum(p) = 1, p >= 0
          c = np.zeros(n + 1)
          c[-1] = -1  # maximize v → minimize -v
          A_ub = np.hstack([-T.T, np.ones((n, 1))])
          b_ub = np.zeros(n)
          A_eq = np.zeros((1, n + 1))
          A_eq[0, :n] = 1
          b_eq = np.array([1.0])
          bounds = [(0, None)] * n + [(None, None)]
          result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                          bounds=bounds, method='highs')
          return result.x[:n]
      
      def evaluate(self, payoff_matrices):
          """Full VasE evaluation pipeline."""
          T = self.build_tournament_matrix(payoff_matrices)
          lottery = self.maximal_lottery(T)
          return {
              'ranking': lottery,
              'tournament_matrix': T,
              'top_agent': self.agents[np.argmax(lottery)],
              'intransitive_cycles': self.detect_cycles(T)
          }
      
      def detect_cycles(self, T):
          """Find intransitive cycles in the tournament.
          A cycle exists if there are agents A, B, C where A>B, B>C, C>A."""
          cycles = []
          for i in range(self.n_agents):
              for j in range(self.n_agents):
                  for k in range(self.n_agents):
                      if T[i,j] > 0 and T[j,k] > 0 and T[k,i] > 0:
                          cycle = tuple(sorted([i,j,k]))
                          if cycle not in cycles:
                              cycles.append(cycle)
          return cycles
  ```
- **Validation:**
  - On the same bot zoo data used for α-Rank: do VasE and α-Rank agree on the top agent?
  - On a deliberately intransitive setup (agent A beats B, B beats C, C beats A): VasE should detect the cycle and assign roughly equal probabilities.
  - Compare VasE ranking with Elo ranking: where do they disagree? (Disagreement should occur in non-transitive matchups.)

**Day 4 — Layer 3: AIVAT Variance Reduction**

- 🔴 Implement AIVAT for imperfect-information game evaluation:
  ```python
  class AIVAT:
      """AIVAT: Variance Reduction for Imperfect Information Game Evaluation.
      
      In poker, game outcomes are dominated by card luck.
      AIVAT subtracts the expected luck component to isolate skill.
      
      Requires: a value function V(h) at each information state h.
      In practice, V(h) comes from the CFR equilibrium (Step 3).
      
      Estimator:
          AIVAT(hand) = actual_result 
                        + Σ_chance_nodes [ V(counterfactual) - V(actual) ]
      
      The counterfactual terms cancel out the card luck, leaving
      only the decision-making component.
      """
      
      def __init__(self, game, value_function):
          self.game = game
          self.V = value_function  # From CFR equilibrium
      
      def evaluate_hand(self, hand_record):
          """Compute AIVAT-adjusted result for one hand.
          
          For each chance node (card deal) in the hand:
          1. Compute V(actual cards dealt) using the value function
          2. Compute V(counterfactual: what if different cards?)
          3. The adjustment = V(counterfactual) - V(actual)
          
          AIVAT result = actual result + sum of adjustments
          """
          actual_result = hand_record.player_result
          adjustment = 0.0
          
          for chance_node in hand_record.chance_nodes:
              v_actual = self.V(chance_node.information_state,
                              chance_node.actual_action)
              # Expected value across all possible chance outcomes
              v_expected = sum(
                  prob * self.V(chance_node.information_state, action)
                  for action, prob in chance_node.action_distribution
              )
              adjustment += v_expected - v_actual
          
          return actual_result + adjustment
      
      def evaluate_match(self, agent1, agent2, n_hands):
          """Evaluate with AIVAT, returning mean and confidence interval."""
          aivat_results = []
          for _ in range(n_hands):
              hand = self.game.play_hand(agent1, agent2)
              aivat_result = self.evaluate_hand(hand)
              aivat_results.append(aivat_result)
          
          mean = np.mean(aivat_results)
          std = np.std(aivat_results)
          ci_95 = 1.96 * std / np.sqrt(n_hands)
          
          return {
              'mean_mbb_per_hand': mean * 1000,  # milli-big-blinds
              'ci_95': ci_95 * 1000,
              'n_hands': n_hands,
              'variance_reduction': np.var(aivat_results) / (np.var([h.actual_result for h in hand_records]) + 1e-10)
          }
  ```
- **Validation:**
  - On Kuhn poker (exact solution available):
    - AIVAT estimate should match the exact exploitability to high precision with far fewer hands than raw evaluation
    - Variance of AIVAT estimates should be < 20% of raw variance
  - On Leduc poker:
    - Compare: evaluate Nash-CFR agent vs random with and without AIVAT. Same mean, dramatically different confidence intervals.
    - Measure variance reduction factor: how many fewer games does AIVAT need for the same confidence?

**Day 5 — Integration + Cross-Game Evaluation**

- 🟡 Bring all three layers together:
  ```python
  class UnifiedEvaluationFramework:
      """The complete Contribution #3 prototype.
      
      Evaluates agents across three layers on any game:
      - Layer 1: Exploitability (single-agent worst-case)
      - Layer 2: Population ranking (multi-agent relative strength)
      - Layer 3: Statistical confidence (how sure are we?)
      
      Applied to: Kuhn, Leduc, SLS, Playtech data
      """
      
      def full_evaluation(self, game, agents, n_games=10000):
          """Complete evaluation report for a set of agents on a game."""
          report = {}
          
          # Layer 1: Exploitability
          report['exploitability'] = {}
          for name, agent in agents.items():
              if game.is_small():
                  report['exploitability'][name] = \
                      self.exploitability_module.exact(agent)
              else:
                  report['exploitability'][name] = \
                      self.exploitability_module.approximate(agent)
          
          # Layer 2: Population ranking
          payoff_matrix = self.run_round_robin(agents, game, n_games)
          report['elo'] = compute_elo(payoff_matrix)
          report['alpha_rank'] = AlphaRank(payoff_matrix).compute_ranking()
          report['vase'] = VasE(list(agents.keys()), [game]).evaluate([payoff_matrix])
          report['meta_nash'] = compute_meta_nash(payoff_matrix)
          report['spinning_top'] = spinning_top_decomposition(payoff_matrix)
          
          # Layer 3: Statistical confidence
          report['confidence'] = {}
          for i, (name_i, agent_i) in enumerate(agents.items()):
              for j, (name_j, agent_j) in enumerate(agents.items()):
                  if i < j:
                      if game.has_imperfect_info():
                          eval_result = self.aivat.evaluate_match(
                              agent_i, agent_j, n_games
                          )
                      else:
                          eval_result = self.standard_evaluate(
                              agent_i, agent_j, n_games
                          )
                      report['confidence'][(name_i, name_j)] = eval_result
          
          return report
  ```
- **Run full evaluation on Kuhn poker:**
  - All bot zoo agents evaluated across all three layers
  - Expected: Nash/CFR agent has lowest exploitability, highest ranking, tightest CIs
  - Expected: Random agent has highest exploitability, lowest ranking
  - Expected: Heuristic agents (tight-agg, loose-agg) fall in between
  - Expected: DQN agent (Step 5) positioned by its training quality
- **Run full evaluation on Leduc poker:**
  - Same analysis, larger game → approximate exploitability should still be meaningful
  - Compare Elo vs α-Rank vs VasE: any disagreements? If so, use spinning top to diagnose
- **Run evaluation bridge to Step 13:**
  - If Playtech data pipeline from Step 13 is available: apply evaluation framework to behavioral cloning agents
  - Measure: how does the BC model rank against bot zoo agents on Leduc?

**Day 6 — Multi-Agent Extension + Final Comparison**

- 🔴 Extend evaluation to N-player games:
  ```python
  class NPlayerEvaluation:
      """Extend the evaluation framework to N-player games.
      
      Challenge: in 2-player zero-sum, exploitability is well-defined
      (value of best response). In N-player, there's no single "best response"
      because the other N-1 players' strategies matter.
      
      Approaches:
      1. Marginal exploitability: fix all opponents at their strategies,
         compute best response for one player. Average across all players.
      2. Nash gap: distance from nearest Nash equilibrium.
      3. Population-based: use α-Rank/VasE on N-player empirical game.
      """
      
      def marginal_exploitability(self, agent, opponents, game):
          """How much can agent improve by unilateral deviation,
          given fixed opponents?"""
          current_value = evaluate_in_context(agent, opponents, game)
          br_value = compute_best_response_value_nplayer(
              agent_slot=0, opponents=opponents, game=game
          )
          return br_value - current_value
      
      def group_exploitability(self, agents, game):
          """Average marginal exploitability across all players.
          A profile is Nash iff group_exploitability = 0."""
          total = 0
          for i, agent in enumerate(agents):
              opponents = [a for j, a in enumerate(agents) if j != i]
              total += self.marginal_exploitability(agent, opponents, game)
          return total / len(agents)
  ```
- **Apply to SLS data from Step 11:**
  - Compute marginal exploitability for the SLS coalition agents
  - Run α-Rank and VasE on the SLS meta-game (from Step 11's EGTA analysis)
  - Apply spinning top: how much of SLS's competitive structure is transitive vs cyclic?
  - Compare with the help/harm matrix from Step 11: do the evaluation metrics correlate with known coalition dynamics?
- **Final comparison table:**
  | Metric | Kuhn (2P) | Leduc (2P) | SLS (N-P) | Playtech (data) | Notes |
  |--------|-----------|------------|-----------|-----------------|-------|
  | Exact exploitability | ✅ | ✅ | N/A (too large) | N/A (no game tree) | Gold standard for small games |
  | Approx. exploitability | ✅ (matches exact) | ✅ | partial | N/A | RL-based best response |
  | Elo | ✅ | ✅ | ✅ | ✅ | Fails on intransitive matchups |
  | α-Rank | ✅ | ✅ | ✅ | ✅ | Parameter sensitive (α) |
  | VasE | ✅ | ✅ | ✅ | ✅ | Axiomatically grounded |
  | Meta-Nash | ✅ | ✅ | ✅ | N/A | From EGTA |
  | Spinning top | ✅ | ✅ | ✅ | N/A | Diagnostic: transitive ratio |
  | AIVAT | ✅ | ✅ | N/A | ✅ | Variance reduction for poker |
  | Confidence intervals | ✅ | ✅ | ✅ | ✅ | From Rowland et al. |

### Deliverables:
- [ ] EvaluationFramework API with three-layer architecture
- [ ] Exploitability module (exact + approximate)
- [ ] Bot zoo for Kuhn and Leduc (trivial + heuristic + computed + advanced agents)
- [ ] Round-robin tournament runner producing payoff matrices
- [ ] α-Rank implementation with sensitivity analysis
- [ ] VasE (maximal lotteries) implementation
- [ ] AIVAT variance reduction for imperfect-information games
- [ ] Elo implementation (baseline comparison)
- [ ] Meta-Nash computation (from Step 10 EGTA, integrated)
- [ ] Spinning top decomposition (from Step 10, integrated)
- [ ] Full evaluation on Kuhn (all layers, all agents)
- [ ] Full evaluation on Leduc (all layers, all agents)
- [ ] N-player evaluation extension applied to SLS data
- [ ] Cross-game comparison table (Kuhn × Leduc × SLS × Playtech)
- [ ] Elo vs α-Rank vs VasE disagreement analysis

### Validation:
- **Exploitability:** On Kuhn, exact value matches Step 3/8 computations to 4 decimal places. On Leduc, approximate tracks exact within 10%.
- **α-Rank:** On RPS, uniform ranking. On transitive game, concentrated on best agent. Matches OpenSpiel's computation if available.
- **VasE:** On RPS, roughly uniform (detected cycle). On transitive game, concentrated on best agent. On mixed game, identifies cycles NOT found by Elo.
- **AIVAT:** Variance reduction ≥ 5× on Kuhn, ≥ 10× on Leduc (expected from literature). Unbiased: mean unchanged within statistical error.
- **Framework integration:** Full report generates in < 5 minutes for Kuhn, < 30 minutes for Leduc (including round-robin).

---

## Phase 5: Consolidation (2 days)

### Day 1 — Survey Skim + Cross-References

- **Reference skim:** Martin & Sandholm (2023/2024) — "ApproxED: Approximate Exploitability Descent"  
  https://arxiv.org/abs/2301.08830  
  *Skim for: the learned best-response training procedure. Compare with your approximate exploitability module: they learn a best-response FUNCTION (generalizes across strategy profiles), you learn a best-response POLICY (specific to one strategy). Their approach is more general but more expensive.*

- **Reference skim:** Cipolina-Kun et al. (2025) — "Game Reasoning Arena"  
  https://arxiv.org/abs/2508.03368  
  *Skim for: benchmark design for evaluating reasoning via game play. Connection to Step 12's LLM agent evaluation: could your framework evaluate LLM agents using the same games?*

- **Supplementary skim:** Yan et al. (2020) — "Policy Evaluation and Seeking for MARL via Best Response"  
  https://arxiv.org/abs/2006.09585  
  *Skim for: cycle-based and memory-based evaluation metrics grounded on sink equilibrium. Alternative to α-Rank for evaluating cycling dynamics.*

- **Forward scan:** Search for any recent papers on "evaluation in imperfect information games" or "multi-agent benchmark 2025." Note any developments since the Lanctot VasE paper.

### Day 2 — PhD Mapping + One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 2] Nash equilibrium → [Step 14] Exploitability is the DISTANCE from Nash. Your Step 2 Nash solutions ARE the zero-point on the exploitability scale. Every agent evaluated in Step 14 is measured by how far it is from this zero-point.
    - [Step 3] CFR convergence tracking → [Step 14] The exploitability curves from Step 3 (CFR iterations vs exploitability) are a special case of the evaluation framework: single-agent, single-metric, single-game. Step 14 generalizes to: multiple agents, multiple metrics, multiple games.
    - [Step 3] CFR equilibrium → [Step 14] AIVAT. The CFR solution provides the value function $V(h)$ needed for AIVAT variance reduction. The quality of Step 3's CFR directly determines the quality of Step 14's AIVAT evaluation. If CFR hasn't converged well, AIVAT's variance reduction is limited.
    - [Step 5] DQN agent → [Step 14] DQN is a bot zoo member AND the building block for approximate exploitability (RL-based best response). The same Step 5 infrastructure serves two roles.
    - [Step 8] Safe exploitation → [Step 14] The exploitation-safety Pareto frontier from Step 8 IS an evaluation artifact. Step 14 formalizes it: adaptation safety (Ge 2024) is an exploitability-based evaluation criterion.
    - [Step 8] Exploitability checker → [Step 14] Step 8's exploitability computation is refactored into Step 14's Layer 1 module. Same code, elevated to framework status.
    - [Step 9] PSRO meta-game → [Step 14] The PSRO meta-game payoff matrix is the INPUT to α-Rank/VasE. Step 9's population IS the evaluation population.
    - [Step 10] EGTA + spinning top → [Step 14] Direct integration. EGTA provides meta-Nash, spinning top provides the transitive/cyclic diagnostic. These are now evaluation modules in the unified framework.
    - [Step 10] Elo tracking → [Step 14] Elo is the BASELINE evaluation method. α-Rank and VasE are the game-theoretic improvements. Comparing all three reveals where Elo fails (intransitive matchups) and where it's sufficient (transitive games).
    - [Step 11] SLS evaluation → [Step 14] SLS provides the N-player test case. The evaluation framework must handle SLS's coalition dynamics where 2-player metrics (exploitability) don't directly apply. Marginal exploitability is the N-player extension.
    - [Step 11] Help/harm matrices → [Step 14] The help/harm matrices from Step 11 are a game-specific evaluation tool. Step 14 should connect them to the general framework: does the spinning top's cyclic component correlate with help/harm patterns?
    - [Step 13] Playtech data → [Step 14] AIVAT is essential for poker data evaluation. BC model accuracy and player2vec embedding quality need confidence intervals. The Playtech data provides the REAL-WORLD validation of the evaluation framework.
    - [Step 13] Collusion detection → [Step 14] Collusion detection is an EVALUATION task: evaluate whether player pairs are behaving "normally" or "abnormally." The confidence intervals from Step 14's Layer 3 apply directly.
  - **Confusions:**
    - [Step 14] VasE and α-Rank both claim to handle intransitivity, but they use different mathematical structures (social choice theory vs evolutionary dynamics). When do they disagree? Is one strictly better than the other? → OPEN (empirical comparison on Step 14 data should answer this)
    - [Step 14] AIVAT requires a value function from CFR. In large games (Hold'em), CFR uses abstraction → the value function is approximate → AIVAT's variance reduction is approximate. How sensitive is AIVAT to value function quality? → PARTIALLY ADDRESSED (measure correlation between CFR convergence and AIVAT effectiveness)
    - [Step 14] The approximate exploitability module trains a DQN as best response. But DQN has its own approximation errors. How do you distinguish "the agent is exploitable" from "the DQN didn't find the exploit"? → OPEN (upper bound interpretation: DQN gives a LOWER bound on true exploitability — the real exploitability is at least as high. If DQN finds high exploitability, it's real. If DQN finds low, the agent MIGHT still be exploitable.)
    - [Step 10→14] The spinning top decomposition requires the FULL payoff matrix. For large agent populations, this is O(n²) evaluations. Is there a sampling-based approximation? → OPEN (important for scaling to real-world deployment)
    - [Step 8→14] Adaptation safety is defined relative to a baseline. In Step 14's framework, which baseline? The Nash/CFR agent? The heuristic agent? The choice of baseline changes the evaluation outcome. → OPEN (thesis should propose a principled baseline selection method)
    - [Step 11→14] Marginal exploitability in N-player games depends on what the other N-1 players do. In SLS, the "opponents" are sometimes allies and sometimes enemies (coalition dynamics). Fixed-opponent exploitability doesn't capture this dynamic. → OPEN (potential Contribution #3 extension: coalition-aware exploitability)

### PhD Connection

This step IS Contribution #3. The mapping:

- **Contribution #3 (Evaluation Methodology):** The three-layer evaluation framework:
  - **Layer 1 (Exploitability):** How vulnerable is the agent to worst-case adversaries? Applicable to 2-player games directly, extended to N-player via marginal exploitability. Methods: exact (Step 3), approximate (Timbers et al.), adaptation safety (Ge et al.).
  - **Layer 2 (Population Ranking):** How does the agent perform relative to a diverse population? Methods: Elo (baseline), α-Rank (evolutionary dynamics), VasE (social choice theory), meta-Nash (EGTA). Diagnostic: spinning top decomposition reveals transitive vs cyclic structure.
  - **Layer 3 (Statistical Confidence):** How confident are these measurements? Methods: AIVAT (poker-specific variance reduction), confidence intervals (Rowland et al. sample complexity), bootstrapping.
  - **Cross-game validation:** Applied consistently to Kuhn, Leduc, SLS, and Playtech data → domain-agnostic evidence that the framework generalizes.

- **Contribution #1 (Behavioral Adaptation):** The evaluation framework MEASURES whether the behavioral adaptation from Steps 7–8 works. Does the adapting agent's exploitability decrease over time? Does its ranking in the population improve? Does the improvement hold up with statistical confidence?

- **Contribution #2 (Multi-Agent Safe Exploitation):** The N-player evaluation extension (marginal exploitability, coalition-aware metrics) tests whether safe exploitation generalizes from 2-player to N-player. If the Step 8 agent is "safe" in 2-player but not in N-player, the evaluation framework detects this — and the gap IS the thesis contribution.

- **Bridge to Step 15:** Step 15 maps the entire PhD research frontier. Step 14's evaluation framework determines what CAN be rigorously evaluated → what CAN be claimed as a thesis contribution. The evaluation framework is the basis for ALL experimental claims in the dissertation.

- **November publication strengthening:** If the evaluation framework is combined with Step 13's Playtech data paper, the result is: "Behavioral Analysis and Evaluation of Poker Agents: A Three-Layer Framework Applied to Real-World Data." This is a stronger paper than either step alone — it has both methodology (evaluation framework) and application (Playtech data).

---

## Exit Checklist

- [ ] Evaluation framework API working with three-layer architecture
- [ ] Exploitability module: exact on Kuhn/Leduc matches Step 3/8 values, approximate mode working
- [ ] Bot zoo: 7+ agents for Kuhn, 7+ agents for Leduc, covering trivial/heuristic/computed/advanced tiers
- [ ] Round-robin tournament successfully generates payoff matrices for both games
- [ ] α-Rank implemented and validated (RPS = uniform, transitive = concentrated)
- [ ] α-Rank sensitivity analysis completed (ranking vs α plots)
- [ ] VasE implemented and validated (detects cycles, agrees with α-Rank on transitive games)
- [ ] Elo vs α-Rank vs VasE disagreement identified and explained via spinning top
- [ ] AIVAT implemented: variance reduction ≥ 5× on Kuhn, ≥ 10× on Leduc
- [ ] AIVAT unbiasedness verified: mean within statistical error of raw evaluation
- [ ] Full evaluation report generated for Kuhn (all agents, all metrics)
- [ ] Full evaluation report generated for Leduc (all agents, all metrics)
- [ ] N-player evaluation (marginal exploitability) applied to SLS data from Step 11
- [ ] Cross-game comparison table (Kuhn × Leduc × SLS × Playtech) completed
- [ ] Can explain from memory: exploitability definition and computation (exact + approximate)
- [ ] Can explain from memory: α-Rank Markov chain construction and why it handles intransitivity
- [ ] Can explain from memory: VasE social choice framing and maximal lotteries LP
- [ ] Can explain from memory: AIVAT control variate and why it reduces variance
- [ ] Can explain from memory: when Elo fails and when α-Rank/VasE are needed
- [ ] Can explain from memory: the three-layer evaluation framework (the thesis Contribution #3)
- [ ] All 🔴 components hand-coded (exploitability module, α-Rank, VasE, AIVAT, N-player extension)
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Steps 2–13 + evaluation-specific confusions)
- [ ] PhD connection documented (framework = Contribution #3; measures Contributions #1 and #2)
- [ ] Step notes committed to repo

> **[P4*] Prove Evaluation Failure Modes (cautious):** Add explicit “evaluation failure mode” experiments to objectives: identify specific scenarios where Elo mis-ranks adaptive agents in non-transitive populations, or where single-metric evaluation misses safety violations. Frame as: “existing evaluation is broken in these N-player/adaptive settings, here’s what fixes it.” The spinning top decomposition (Step 10) already provides the diagnostic — reframe as a *finding*. Proceed cautiously — don’t over-engineer.

