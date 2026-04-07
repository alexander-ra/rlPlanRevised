# Step 10 — Population-Based Training + Evolutionary Game Theory

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 7 (Opponent Modeling), Step 8 (Safe Exploitation), Step 9 (Multi-Agent RL)  
**Phase:** E — Multi-Agent Dynamics  

### PhD Connection

This step provides the EVOLUTIONARY MACHINERY for the thesis. The connection to each contribution:

- **Contribution #1 (Behavioral Adaptation):** PBT's exploiter mechanism is automated opponent modeling at scale. The main exploiter finds weaknesses in the main agent — exactly what your Step 7 opponent model does, but embedded in the training loop. Your thesis combines EXPLICIT modeling (Step 7's Bayesian model) with IMPLICIT modeling (Step 10's exploiter agents).
- **Contribution #2 (Multi-Agent Safe Exploitation):** The key gap: AlphaStar's league provides HEURISTIC safety (exploiters keep main agents honest) but NO FORMAL SAFETY GUARANTEE. Your thesis contribution is to formalize this: what does "safe exploitation in a population" MEAN mathematically? The spinning top decomposition tells you that the cyclic component is where safety is hardest (because improvement is illusory). Can you define safety as "never losing to the transitive component" while accepting cycling in the cyclic component? This is a concrete thesis hypothesis.
- **Contribution #3 (Evaluation Methodology):** EGTA provides the evaluation framework: measure the meta-Nash of the agent population as the multi-agent generalization of exploitability. The spinning top decomposition provides a diagnostic: how much of the competitive structure is "real skill" vs "rock-paper-scissors dynamics"?

---

## Table of Contents
- [Phase 1: Intuition (1 day)](#phase-1-intuition-1-day)
  - [Blog Posts / Accessible Reads](#blog-posts-accessible-reads)
- [Phase 2: Exploration (2 days)](#phase-2-exploration-2-days)
  - [Day 1: PSRO as Population-Based Training](#day-1-psro-as-population-based-training)
  - [Day 2: Evolutionary Dynamics on Matrix Games](#day-2-evolutionary-dynamics-on-matrix-games)
- [Phase 3: Targeted Reading (3 days)](#phase-3-targeted-reading-3-days)
  - [Paper 1: Jaderberg et al. — "Population Based Training of Neural Networks" (2017)](#paper-1-jaderberg-et-al-population-based-training-of-neural-networks-2017)
  - [Paper 2: Jaderberg et al. — "Human-Level Performance in First-Person Multiplayer Games with Population-Based DRL" (FTW, 2019)](#paper-2-jaderberg-et-al-human-level-performance-in-first-person-multiplayer-games-with-population-based-drl-ftw-2019)
  - [Paper 3: Vinyals et al. — "Grandmaster Level in StarCraft II Using Multi-Agent Reinforcement Learning" (AlphaStar, 2019)](#paper-3-vinyals-et-al-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning-alphastar-2019)
  - [Paper 4: Balduzzi et al. — "Open-Ended Learning in Symmetric Zero-Sum Games" (2019)](#paper-4-balduzzi-et-al-open-ended-learning-in-symmetric-zero-sum-games-2019)
  - [Paper 5: Tuyls, Pérolat, Lanctot et al. — "A Generalised Method for Empirical Game Theoretic Analysis" (2018)](#paper-5-tuyls-pérolat-lanctot-et-al-a-generalised-method-for-empirical-game-theoretic-analysis-2018)
  - [Supplementary References](#supplementary-references)
  - [Math Flags](#math-flags)
- [Phase 4: Implementation (6 days)](#phase-4-implementation-6-days)
  - [Project: PBT League for Leduc + Evolutionary Analysis](#project-pbt-league-for-leduc-evolutionary-analysis)
  - [Sub-phase Breakdown (6 days):](#sub-phase-breakdown-6-days)
  - [Deliverables:](#deliverables)
  - [Validation:](#validation)
- [Phase 5: Consolidation (2 days)](#phase-5-consolidation-2-days)
  - [Day 1 — Survey Skim + Supplementary Papers](#day-1-survey-skim-supplementary-papers)
  - [Day 2 — PhD Mapping + One-Pager + Learning Log](#day-2-phd-mapping-one-pager-learning-log)
- [Exit Checklist](#exit-checklist)

## Phase 1: Intuition (1 day)

The goal: understand WHY population-based training exists (self-play against ONE opponent is brittle — you need a POPULATION for robustness) and HOW evolutionary game theory provides the mathematical lens to analyze populations of strategies competing and evolving. Key insight: in Steps 2–8, you computed a SINGLE strategy (Nash equilibrium). In Steps 9–10, you maintain a POPULATION of strategies that evolve over time. Evolutionary game theory tells you what happens to these populations in the long run.

End of day: you should be able to explain to a non-expert: "Instead of training one AI against itself (self-play), we train a POPULATION of different AIs against each other. The strong ones survive, the weak ones get replaced. This is like evolution — but instead of biological organisms, we're evolving AI strategies. The result is more robust AIs because they've been tested against many different opponents, not just one. Evolutionary game theory is the math that tells us what this population converges to."

- **Evolution of aggression and sharing: the replicator dynamics with the Hawk Dove Game**  
  https://www.youtube.com/watch?v=tDTVRvfaaQo  
  Duration: ~11m | Channel: Vincent Knight  
  *Visual walkthrough of evolutionary game theory: the Hawk-Dove game, replicator dynamics differential equations, and how populations reach mixed equilibrium. The mathematical foundation for understanding population evolution.*

- **Human-level in first-person multiplayer games with population-based deep RL**  
  https://www.youtube.com/watch?v=dltN4MxV1RI  
  Duration: ~8m | Channel: Max Jaderberg (DeepMind)  
  *Supplementary video showing PBT applied to Capture the Flag. Agents learn to cooperate with teammates and compete against opponents through population-based training.*

- **Game highlights of AlphaStar versus Team Liquid's TLO and MaNa**  
  https://www.youtube.com/watch?v=6EQAsrfUIyo  
  Duration: ~13m | Channel: DeepMind  
  *Commentary and analysis of AlphaStar matches with Artosis, RotterdaM, Oriol Vinyals and David Silver. Shows the result of population-based league training — diverse strategies emerging from the AlphaStar League.*

- **Stanford CS234 — Lecture 15: Value Alignment (Spring 2024)**  
  https://www.youtube.com/watch?v=FOlPpjNbHjE  
  Duration: ~1h14m | Instructor: Emma Brunskill + Dan Webber (Stanford)  
  *Covers MCTS, AlphaZero, DPO, and RLHF. The AlphaZero section is relevant for understanding how self-play within a population produces superhuman performance.*

- **Self-Play**  
  https://www.youtube.com/watch?v=EY9iHSe82Hc  
  Duration: ~56m | Speaker: Noam Brown | Cooperative AI Summer School 2024  
  *Covers population-based methods in depth, including the relationship between PSRO, evolutionary dynamics, and the AlphaStar league design.*

### Blog Posts / Accessible Reads

- **DeepMind Blog — "AlphaStar: Mastering the Real-Time Strategy Game StarCraft II"**  
  https://deepmind.google/discover/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/  
  *The accessible overview of AlphaStar's population-based training. Read for the league architecture diagrams.*

- **DeepMind Blog — "Capture the Flag: the emergence of complex cooperative agents"**  
  https://deepmind.google/discover/blog/capture-the-flag-the-emergence-of-complex-cooperative-agents/  
  *The CTF blog post. Short, with clear diagrams of the PBT pipeline.*

- **Wikipedia — "Evolutionary Game Theory"**  
  https://en.wikipedia.org/wiki/Evolutionary_game_theory  
  *A quick primer on replicator dynamics, evolutionary stable strategies (ESS), and the Hawk-Dove game. Context for the formal paper reading.*

---

## Phase 2: Exploration (2 days)

### 🎮 Interactive Exploration
- **[Simulating the World](https://ncase.me/simulating/)** — Play with evolutionary and population dynamics models in the browser.


### Day 1: PSRO as Population-Based Training

1. **Re-use your Step 9 PSRO implementation as the starting point:**
   - Your PSRO loop IS a form of population-based training: maintain a population of policies, evolve the population by adding best responses
   - Run PSRO on Leduc for many iterations (50+) and observe how the population grows
   - Visualize the meta-game payoff matrix: what does it look like? Is it transitive (one policy dominates all others) or cyclic (rock-paper-scissors dynamics)?

2. **Experiment with population diversity:**
   ```python
   # After running PSRO, analyze the population:
   # - How many policies in the population are "active" (have non-zero weight in meta-Nash)?
   # - How many are dominated (never played)?
   # - What's the effective diversity of the population?
   
   meta_nash = psro.compute_meta_nash()
   active_policies = [i for i, w in enumerate(meta_nash) if w > 0.01]
   print(f"Active policies: {len(active_policies)} / {len(psro.population)}")
   ```
   - **Diversity problem:** Often, most of the population weight concentrates on a few policies. The rest are "dead weight." AlphaStar's league design specifically addresses this.

3. **Visualize the game landscape:**
   ```python
   # Compute the payoff matrix between all policies in the population
   # Use PCA or t-SNE to visualize strategies in 2D
   # Plot arrows showing best-response dynamics
   # Do you see cycles (non-transitivity) or a clear hierarchy (transitivity)?
   ```

### Day 2: Evolutionary Dynamics on Matrix Games

1. **Implement replicator dynamics on your matrix games:**
   ```python
   def replicator_dynamics(payoff_matrix, population, dt=0.01):
       """One step of continuous replicator dynamics.
       population[i] = proportion of population playing strategy i."""
       fitness = payoff_matrix @ population
       avg_fitness = population @ fitness
       # Replicator equation: dx_i/dt = x_i * (f_i - avg_f)
       dpop = population * (fitness - avg_fitness)
       return population + dpop * dt
   ```
   - Run on Prisoner's Dilemma: defection dominates (evolutionary stable)
   - Run on Hawk-Dove: converges to mixed ESS
   - Run on Rock-Paper-Scissors: cycles forever (no ESS)
   - **Key observation:** The replicator dynamics on RPS NEVER converge. This is analogous to the cycling you see in PSRO/self-play for non-transitive games. The spinning-top decomposition from Balduzzi explains why.

2. **Compare replicator dynamics with your Step 2 Nash solutions:**
   - For each matrix game: what does the replicator dynamics converge to? Does it match Nash?
   - Answer: for some games (PD, Hawk-Dove), replicator dynamics converge to Nash. For others (RPS), they cycle AROUND Nash without converging. This is the fundamental difficulty of evolutionary approaches to equilibrium computation.

3. **Run a simple PBT experiment:**
   - Create a population of 10 PPO agents with DIFFERENT hyperparameters (learning rate, entropy bonus)
   - Train them via round-robin against each other (each agent plays N games vs each other agent)
   - Periodically: replace the bottom 20% with mutated copies of the top 20%
   - Observe: does the population converge to a single dominant strategy or maintain diversity?

---

## Phase 3: Targeted Reading (3 days)

### Paper 1: Jaderberg et al. — "Population Based Training of Neural Networks" (2017)

https://arxiv.org/abs/1711.09846 (Original PBT paper)

```
├── READ:  Section 2 (PBT algorithm — the explore-exploit mechanism: a population
│          of models train in parallel, periodically the worst performers COPY 
│          the weights of the best performers (exploit) and then MUTATE their 
│          hyperparameters (explore). This is evolution applied to neural network
│          training),
│          Section 3 (Experiments — showing PBT finds better hyperparameters than
│          grid search or random search, with less compute)
├── SKIM:  Abstract, Section 1 (Introduction),
│          Section 4 (Discussion)
├── SKIP:  Detailed tables (look at summary results only)
├── MATH:  → "No complex math. PBT is an algorithm, not a theorem. Understand the 
│             EXPLOIT (copy best weights) and EXPLORE (perturb hyperparameters)
│             operations. The key insight: this is a simple evolutionary algorithm
│             applied to the meta-optimization problem (choosing hyperparameters)."
└── KEY INSIGHT: "PBT replaces the sequential 'train → evaluate → tune hyperparams → 
    retrain' cycle with a PARALLEL population that co-evolves training and 
    hyperparameters simultaneously. For MARL, this means the population also 
    serves as a diverse set of opponents, solving two problems at once."
```

### Paper 2: Jaderberg et al. — "Human-Level Performance in First-Person Multiplayer Games with Population-Based DRL" (FTW, 2019)

https://arxiv.org/abs/1807.01281 (Science 2019)

```
├── READ:  Section 2 (The FTW architecture — how PBT is applied to a 
│          multiplayer game: agents in the population are matched against each
│          other, creating a natural curriculum. The internal reward structure 
│          and population dynamics are co-evolved),
│          Section 3 (Results — emergence of cooperative and competitive 
│          strategies, including map control, teammate coordination, distraction)
├── SKIM:  Abstract, Section 1 (Introduction — the Capture-the-Flag setting),
│          Section 4 (Analysis — strategy emergence)
├── SKIP:  Network architecture details (Section 2.3) unless implementing
├── MATH:  → "The Elo rating system used to evaluate agents (Section 2.4). 
│             Understand: Elo is a relative skill measure. In a population,
│             Elo ratings tell you WHO is strong against WHOM. This is the 
│             empirical game theory lens: the Elo matrix IS the meta-game."
└── KEY INSIGHT: "FTW shows that population-based training creates an implicit 
    CURRICULUM: weak agents face weak opponents and gradually improve, strong 
    agents face strong opponents and keep being challenged. No hand-designed 
    curriculum needed — the population self-organizes into a difficulty ladder."
```

### Paper 3: Vinyals et al. — "Grandmaster Level in StarCraft II Using Multi-Agent Reinforcement Learning" (AlphaStar, 2019)

**Link:** https://www.nature.com/articles/s41586-019-1724-z  
**Alt link:** https://arxiv.org/abs/1911.12254 (extended version)

```
├── READ:  Section 2.3 ("AlphaStar League" — THE gold standard for PBT in games.
│          Three agent types in the population:
│          - Main agents: trained against the full league
│          - Main exploiters: trained to exploit ONLY the main agents' weaknesses
│          - League exploiters: trained to exploit the full league
│          This three-tier design solves the diversity problem: exploiters prevent
│          the main agents from becoming overfit to one strategy.
│          Also read: the priority mechanism for opponent selection — how agents 
│          are matched to create the optimal curriculum),
│          Section 3 (Results — Grandmaster performance, strategy diversity)
├── SKIM:  Abstract, Section 1 (Introduction),
│          Section 2.1–2.2 (Architecture — transformer-based agent, not critical 
│          for understanding the PBT design),
│          Section 4 (Analysis)
├── SKIP:  Architecture details, training infrastructure specifics (Google-scale)
├── MATH:  → "The Nash clustering and rectification mechanism (Methods, extended).
│             AlphaStar uses an approximation of the Nash equilibrium of the 
│             meta-game (the game between policies in the league) to determine 
│             training matchups. This connects directly to your Step 9 PSRO: 
│             AlphaStar's league IS a large-scale PSRO. The difference: AlphaStar
│             uses neural network agents as 'oracles' and trains continuously
│             instead of iteratively."
└── KEY INSIGHT: "AlphaStar's league solves the diversity problem in PBT: without 
    exploiters, the population converges to a single dominant strategy. Exploiters
    force the main agents to be robust to DIVERSE attack vectors. This is 
    ARTIFICIAL SELECTION — the exploiters create selection pressure that maintains
    population diversity. For your thesis: this is the multi-agent analog of the 
    exploitation-safety tradeoff from Step 8."
```

### Paper 4: Balduzzi et al. — "Open-Ended Learning in Symmetric Zero-Sum Games" (2019)

https://arxiv.org/abs/1901.01753 (ICLR 2019)

```
├── READ:  Section 3 (Spinning top decomposition — the payoff matrix between 
│          strategies can be decomposed into:
│          - A TRANSITIVE component (pure skill — strategy A > B > C)
│          - A CYCLIC component (non-transitive: A > B > C > A, like RPS)
│          This decomposition tells you: is your game's skill structure 
│          hierarchical or cyclic? If cyclic, self-play and naive PBT will 
│          fail because improvements are illusory (beating strategy B doesn't 
│          mean getting better; it means shifting in the cycle).),
│          Section 4 (Rectification — how to modify PSRO to handle the cyclic 
│          component by ensuring only genuinely improving policies are added)
├── SKIM:  Abstract, Sections 1–2 (Introduction and background),
│          Section 5 (Experiments — Blotto, random games)
├── SKIP:  Proofs (read statements only)
├── MATH:  → "Theorem 1 (Spinning top decomposition) — read the STATEMENT.
│             Every antisymmetric payoff matrix A = T + C where T is transitive
│             (has a total skill ordering) and C is cyclic (pure rock-paper-scissors
│             dynamics). This is the key diagnostic for multi-agent training: 
│             if your game has a large cyclic component, simple self-play CANNOT 
│             converge to a good strategy."
│          → "Section 3.2 (Game-theoretic strength) — understand the definition.
│             The transitive component T defines a 'true skill' ranking. The 
│             cyclic component C is noise in the ranking. Use this to evaluate 
│             whether your population's improvement is real or illusory."
└── KEY INSIGHT: "Balduzzi shows that many games have significant non-transitive 
    structure (like rock-paper-scissors). In these games, beating strategy A 
    doesn't mean you're 'better' — it might mean you've just shifted to 
    strategy B that happens to beat A but loses to C. Self-play and naive PBT 
    can cycle forever in these games. Rectified PSRO addresses this. For your 
    thesis: this is critical for understanding WHY population diversity matters 
    in FFA games (Step 11)."
```

### Paper 5: Tuyls, Pérolat, Lanctot et al. — "A Generalised Method for Empirical Game Theoretic Analysis" (2018)

https://arxiv.org/abs/1803.06376 (AAMAS 2018)

```
├── READ:  Section 3 (EGTA framework — how to analyze a multi-agent system as 
│          a game over a FINITE set of strategies. Instead of analyzing the 
│          original game (which may be enormous), you sample a finite set of 
│          strategies and construct an EMPIRICAL GAME among them. Nash of the 
│          empirical game approximates Nash of the real game),
│          Section 4 (Theoretical bounds — how well does the empirical Nash 
│          approximate the true Nash? This depends on the number of samples 
│          and the structure of the strategy space)
├── SKIM:  Abstract, Sections 1–2,
│          Section 5 (Experiments)
├── SKIP:  Extended proofs
├── MATH:  → "Theorem 1 (Approximation bound) — read the STATEMENT. The empirical
│             Nash converges to the true Nash as the strategy sample grows. The 
│             rate depends on the game's structure. This is the theoretical 
│             foundation for PSRO's convergence (PSRO IS empirical game theory 
│             with an expanding strategy sample)."
└── KEY INSIGHT: "EGTA provides the EVALUATION FRAMEWORK for population-based 
    training: instead of asking 'how good is my agent?', you ask 'how good is 
    the Nash equilibrium of the empirical game defined by my population?' This 
    is the multi-agent evaluation tool for your thesis's Contribution #3."
```

### Supplementary References

- **Hofbauer, J. & Sigmund, K. (1998/2003) — "Evolutionary Game Dynamics"**  
  http://www.ams.org/journals/bull/2003-40-04/S0273-0979-03-00988-1/  
  *The foundational reference on replicator dynamics and evolutionary stability. Read Section 2 for the replicator equation and Section 3 for evolutionary stable strategies (ESS). This is the mathematical backbone connecting evolutionary dynamics to multi-agent learning.*

- **Hill (2025) — "Co-Evolving Complexity: An Adversarial Framework for Automatic MARL Curricula"**  
  https://arxiv.org/abs/2509.03771  
  *NeurIPS 2025 workshop paper on co-evolutionary curriculum design. SKIM abstract + Section 3. Relevant to the auto-curriculum mechanism in PBT and Step 11's emergent complexity.*

- **Xu et al. (2025) — "Heterogeneous Adversarial Play in Interactive Environments"**  
  https://arxiv.org/abs/2510.18407  
  *NeurIPS 2025. Diversity through heterogeneous adversarial self-play. SKIM for population diversity mechanisms.*

- **De La Fuente et al. (2024) — "Game Theory and MARL: From Nash Equilibria to Evolutionary Dynamics"**  
  https://arxiv.org/abs/2412.20523  
  *22-page survey connecting game theory with evolutionary MARL. SKIM for conceptual overview.*

- **Yao et al. (2023) — "Policy Space Diversity for Non-Transitive Games"**  
  https://arxiv.org/abs/2306.16884  
  *Addresses PSRO diversity collapse in non-transitive games via diversity regularization. SKIM Section 3 for the diversity mechanism.*

### Math Flags

🔢 **Replicator dynamics equation (Hofbauer & Sigmund)** — Must understand.  
**WHY:** The replicator equation dx_i/dt = x_i(f_i(x) - f̄(x)) is the mathematical formalization of population evolution. It connects to Nash equilibria (fixed points are equilibria), evolutionary stability (ESS is an attractor), and the cycling problem in non-transitive games (orbits around the fixed point). For your thesis: understanding when replicator dynamics CONVERGE vs CYCLE tells you when population-based methods will work.

🔢 **Spinning top decomposition (Balduzzi et al., Theorem 1)** — Must understand the statement.  
**WHY:** This decomposition (A = T + C, transitive + cyclic) is the diagnostic tool for evaluating whether your multi-agent training is actually improving or just cycling. For your thesis: FFA games (Step 11) likely have significant non-transitive structure (coalition dynamics create RPS-like cycles). Understanding the decomposition helps you design evaluation metrics (Contribution #3) that distinguish real improvement from cyclical shift.

🔢 **EGTA approximation bound (Tuyls et al., Theorem 1)** — Read statement.  
**WHY:** This bound tells you how many policies you need in your population for the empirical Nash to approximate the true Nash. For your thesis evaluation (Contribution #3), this determines sample complexity for multi-agent evaluation.

---

## Phase 4: Implementation (6 days)

### Project: PBT League for Leduc + Evolutionary Analysis

**Language + Framework:** Python 3.10+ / PyTorch / OpenSpiel

Starting point: Your PSRO from Step 9 + your Nash solver from Step 2 + your Deep CFR/PPO from Steps 5/1.

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| Replicator dynamics simulator on matrix games | 🔴 HAND-CODE | Evolutionary game theory is a thesis foundation. Must understand the dynamics: code the replicator equation, verify ESS, observe cycling on RPS. |
| Spinning top decomposition (transitive + cyclic) | 🔴 HAND-CODE | The T+C decomposition is the key analytical tool for evaluating population-based training. Hand-code the SVD-based decomposition and apply it to your meta-game payoff matrices. |
| PBT League for Leduc (inspired by AlphaStar's league) | 🔴 HAND-CODE | The population training loop IS the thesis-relevant mechanism. Three agent roles: main agents, main exploiters, league exploiters. Implement the matchmaking, the exploitation-safety cycle, and the population evolution. |
| Elo rating system for the league | 🟡 AI-ASSISTED | Standard Elo computation. AI generates, you verify the update formula. |
| EGTA analysis of population | 🔴 HAND-CODE | Empirical game-theoretic analysis: construct the meta-game from league results, compute Nash of the meta-game, use it as evaluation metric. This is Contribution #3's prototype. |
| Diversity metrics (effective diversity, strategy clustering) | 🟡 AI-ASSISTED | Metrics for population diversity. AI drafts, you review the definitions. |
| Experiment logging + visualization | 🟢 AI-GENERATED | Standard infrastructure. Plotting evolution trajectories, Elo curves, payoff heatmaps. |

### Sub-phase Breakdown (6 days):

**Day 1 — Evolutionary Dynamics on Matrix Games:**
- 🔴 Implement replicator dynamics:
  ```python
  def simulate_replicator(payoff_A, payoff_B, x0, y0, T=1000, dt=0.01):
      """Simulate 2-population replicator dynamics.
      x = row player strategy distribution, y = column player distribution."""
      xs, ys = [x0], [y0]
      for _ in range(T):
          # Fitness for each strategy
          fx = payoff_A @ ys[-1]  # fitness of each row strategy
          fy = payoff_B.T @ xs[-1]  # fitness of each column strategy
          # Average fitness
          avg_fx = xs[-1] @ fx
          avg_fy = ys[-1] @ fy
          # Replicator update
          x_new = xs[-1] + xs[-1] * (fx - avg_fx) * dt
          y_new = ys[-1] + ys[-1] * (fy - avg_fy) * dt
          # Normalize (numerical stability)
          xs.append(x_new / x_new.sum())
          ys.append(y_new / y_new.sum())
      return xs, ys
  ```
- Run on all matrix games from Step 9. Verify:
  - PD: cooperate goes to 0, defect to 1 (defection dominates)
  - Hawk-Dove: converges to mixed ESS (matching Nash)
  - RPS: orbits around (1/3, 1/3, 1/3) without converging
  - Stag Hunt: depends on initial conditions (two basins of attraction)
- Plot phase portraits (2D: strategy probability vs time, or in simplex for 3-strategy games)

**Day 2 — Spinning Top Decomposition:**
- 🔴 Implement the transitive-cyclic decomposition from Balduzzi et al.:
  ```python
  def spinning_top_decomposition(payoff_matrix):
      """Decompose antisymmetric payoff matrix A into T (transitive) + C (cyclic).
      A must be zero-sum: A[i,j] = -A[j,i]."""
      n = payoff_matrix.shape[0]
      # Make antisymmetric: A_anti = (A - A.T) / 2
      A_anti = (payoff_matrix - payoff_matrix.T) / 2
      # SVD decomposition
      U, S, Vt = np.linalg.svd(A_anti)
      # Transitive component: rank-1 approximation
      # T = s1 * u1 * v1^T (the strongest skill dimension)
      T = S[0] * np.outer(U[:, 0], Vt[0, :])
      # Cyclic component: everything else
      C = A_anti - T
      return T, C
  ```
- Apply to:
  - Your PSRO meta-game from Step 9 (Leduc population)
  - Analytically: RPS (pure cyclic), "skill game" like a clear ranking (pure transitive)
- Measure: transitive_ratio = ||T|| / ||A|| — how much of the game is "real skill" vs "cycling"?
- **Thesis insight:** If Leduc has high transitive ratio → self-play works well. If low → population diversity is essential.

**Days 3–4 — PBT League for Leduc:**
- 🔴 Implement the mini-AlphaStar league for Leduc:
  ```python
  class LeducLeague:
      def __init__(self, num_main=3, num_main_exploiters=2, num_league_exploiters=2):
          # Three agent types (inspired by AlphaStar):
          # Main agents: trained against the whole league (goal: be robust)
          # Main exploiters: trained against main agents only (goal: find weaknesses)
          # League exploiters: trained against entire league (goal: exploit anyone)
          self.main_agents = [create_agent() for _ in range(num_main)]
          self.main_exploiters = [create_agent() for _ in range(num_main_exploiters)]
          self.league_exploiters = [create_agent() for _ in range(num_league_exploiters)]
          self.frozen_agents = []  # Historical snapshots
      
      def train_epoch(self):
          # 1. Match each agent type against appropriate opponents
          # Main: play vs entire league (uniform or prioritized sampling)
          # Main exploiters: play vs main agents only (find their weaknesses)
          # League exploiters: play vs all (find anyone's weakness)
          
          # 2. Each agent trains using PPO/DQN against its matched opponents
          
          # 3. Periodically freeze main agents (save snapshot to league history)
          
          # 4. PBT: replace underperforming agents with mutated copies of top agents
  ```
- Key design decisions:
  - Use your Step 1 PPO or Step 5 Deep CFR for agent training
  - Matchmaking: prioritize opponents that are challenging (high loss rate)
  - Population size: small (7 agents) is enough for Leduc — it's a small game
  - Frozen agents: snapshot main agents every K epochs to build a historical population
- Run for 100+ training epochs
- Track: Elo of all agents over time, exploitability of main agents over time

**Day 5 — EGTA Analysis:**
- 🔴 Apply Empirical Game-Theoretic Analysis to your league:
  ```python
  def build_empirical_game(league):
      """Construct the normal-form meta-game from league match results."""
      n = len(league.all_agents)
      payoff_matrix = np.zeros((n, n))
      for i in range(n):
          for j in range(n):
              # Average payoff of agent i vs agent j over N games
              payoff_matrix[i, j] = evaluate(league.all_agents[i], league.all_agents[j], N=1000)
      return payoff_matrix
  
  def compute_meta_nash(payoff_matrix):
      """Nash equilibrium of the empirical meta-game."""
      # Use your Step 2 Nash solver (support enumeration or LP)
      ...
  ```
- Compute the meta-Nash of the league's empirical game
- Compare: meta-Nash exploitability vs individual agent exploitability
  - The meta-Nash mixture should be LESS exploitable than any individual agent
- Apply spinning-top decomposition to the league payoff matrix:
  - How much of the league's game is transitive (skill) vs cyclic (style)?
  - Do exploiters create more cycling or more transitive structure?

**Day 6 — Diversity Analysis + Comparison:**
- 🟡 Compute diversity metrics:
  - Effective population size: how many agents have >1% weight in meta-Nash?
  - Strategy clustering: cluster agents by their behavior (action distributions on sample hands)
  - Exploit coverage: for each agent, is there an exploiter that beats it significantly?
- Compare final league results with:
  - Vanilla PSRO from Step 9
  - Single self-play agent (no population)
  - Your MCCFR Nash strategy from Step 3
- Create summary table: method → exploitability, Elo, diversity metrics

### Deliverables:
- [ ] Replicator dynamics simulator with verified behavior on matrix games
- [ ] Phase portraits for all matrix games showing convergence/cycling
- [ ] Spinning top decomposition implementation with transitive ratio metric
- [ ] PBT League for Leduc (main agents + exploiters + historical snapshots)
- [ ] EGTA analysis computing meta-Nash of the league
- [ ] Elo rating tracking across training epochs
- [ ] Diversity metrics (effective population size, strategy clustering)
- [ ] Comparison: league vs PSRO vs self-play vs Nash (MCCFR)

### Validation:
- **Replicator dynamics:** Verify against known analytical results for PD (defection dominates), Hawk-Dove (mixed ESS), RPS (cycling).
- **Spinning top on RPS:** Should be 100% cyclic (zero transitive component).
- **PBT League:** Main agents' exploitability should decrease over training epochs. Main exploiters should find weaknesses that push main agents to improve.
- **EGTA meta-Nash:** Exploitability of the meta-Nash mixture should be ≤ exploitability of best individual agent.
- **League vs PSRO:** On Leduc, the league's meta-Nash exploitability should be comparable to PSRO's (both are population-based).

---

## Phase 5: Consolidation (2 days)

### Day 1 — Survey Skim + Supplementary Papers

- **Reference skim:** Bloembergen, Tuyls et al. (2015) — "Evolutionary Dynamics of Multi-Agent Learning: A Survey"  
  https://jair.org/index.php/jair/article/view/10952  
  *The canonical survey connecting evolutionary game theory to multi-agent learning. SKIM Sections 4–6 for the connection between replicator dynamics and learning algorithms. Key result: many multi-agent learning algorithms can be INTERPRETED as replicator dynamics — the learning rate maps to selection pressure, the exploration rate maps to mutation.*

- **Supplementary skim:** Hill (2025) "Co-Evolving Complexity"  
  https://arxiv.org/abs/2509.03771  
  *Read abstract + Section 3 (co-evolutionary curriculum). Connection to Step 11: FFA games need auto-curricula because the opponent population evolves.*

- **Supplementary skim:** Yao et al. (2023) "Policy Space Diversity for Non-Transitive Games"  
  https://arxiv.org/abs/2306.16884  
  *Read abstract + diversity regularization (Section 3). For Step 11: preventing diversity collapse in the coalition formation game.*

### Day 2 — PhD Mapping + One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 2] Nash equilibrium → [Step 10] Nash of the meta-game. Your Step 2 solver is now used at a higher level: computing equilibria over POPULATIONS of strategies, not just actions in a game.
    - [Step 7] Opponent model → [Step 10] Main exploiters are "automated opponent modelers" — they find weaknesses in the main agents. AlphaStar's exploiters are the population-level analog of your Step 7 Bayesian model.
    - [Step 8] Safe exploitation → [Step 10] The AlphaStar league's three-agent-type design IS a safe exploitation mechanism: main agents balance SAFETY (robustness to exploiters) and SKILL (beating the league). Exploiters provide the "selection pressure" that keeps main agents honest.
    - [Step 9] PSRO → [Step 10] AlphaStar's league is a scaled-up, asynchronous PSRO with neural network oracles instead of exact best responses. The meta-Nash computation from Step 9 becomes the EGTA analysis from Step 10.
    - [Step 10] Spinning top decomposition → prediction: [Step 11] FFA coalition games likely have LARGE cyclic component (coalition dynamics are inherently non-transitive: A+B beats C, B+C beats A, C+A beats B). This means naive self-play/PBT will cycle, requiring the diversity mechanisms studied here.
    - [Step 10] EGTA → prediction: [Step 14] The empirical game-theoretic analysis becomes a core evaluation tool for Contribution #3. Meta-Nash of the agent population is the multi-agent generalization of exploitability.
  - **Confusions:**
    - [Step 10] AlphaStar uses ~600 agents in the league, trained with massive compute (TPU pods). For Leduc, we use 7 agents. Does the league design still make sense at small scale? Is the three-agent-type structure overhead that doesn't help for small games? → PARTIALLY ANSWERED (the exploiter mechanism still helps even at small scale, but the diversity benefits are less dramatic)
    - [Step 10] Replicator dynamics assume a fixed payoff matrix (a fixed game). But in PBT/league training, the agents are LEARNING — the "game" changes as agents improve. How does this non-stationarity affect the replicator analysis? → OPEN (link to Step 9's learning dynamics question)
    - [Step 10] The spinning top decomposition requires computing the FULL payoff matrix between all agents. For large populations, this is O(n²) games. Is there an efficient approximation? → OPEN (relevant for Step 14 scaling)
    - [Step 8→10] Step 8 proved safe exploitation for 2-player. The AlphaStar exploiter mechanism provides safety pressure in a POPULATION. But is there a formal guarantee? AlphaStar exploiters are heuristic — there's no theorem saying "main agents can't become exploitable." → OPEN (this IS the Contribution #2 gap: formalizing population-level safety)

## Exit Checklist

- [ ] Replicator dynamics working on all matrix games with verified convergence/cycling
- [ ] Phase portraits plotted for PD, Hawk-Dove, RPS, Stag Hunt
- [ ] Spinning top decomposition implemented and applied to PSRO meta-game + league meta-game
- [ ] Can explain from memory: replicator equation and what its fixed points correspond to (Nash / ESS)
- [ ] Can explain from memory: transitive vs cyclic components and why the cyclic component prevents naive PBT convergence
- [ ] PBT League for Leduc with three agent types (main, main exploiter, league exploiter) training and improving
- [ ] EGTA analysis: meta-Nash of league is less exploitable than any individual agent
- [ ] Elo tracking showing meaningful skill progression in the league
- [ ] Diversity metrics computed (effective population size, strategy clustering)
- [ ] Comparison table: league vs PSRO vs self-play vs MCCFR Nash on Leduc
- [ ] Can explain AlphaStar's league design from memory (three agent types, matchmaking, freezing)
- [ ] All 🔴 components hand-coded (replicator dynamics, spinning top decomposition, PBT league loop, EGTA analysis)
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Steps 2–9 + new confusions + resolved confusions)
- [ ] PhD connection documented (PBT as automated opponent modeling, population safety gap, EGTA as evaluation framework)
- [ ] Step notes committed to repo
