# Step 6 — End-to-End Game AI Architectures (Pluribus → ReBeL → Student of Games)

**Duration:** 21 days (Tier 1)  
**Dependencies:** Step 3 (CFR Variants + MC Methods), Step 4 (Game Abstraction + Scaling), Step 5 (Neural Equilibrium Approximation)  
**Phase:** C — Neural Methods for Games  
**Freshness Note:**  
- ArXiv search: "deep counterfactual regret minimization" sorted by date (Mar 2026) — cross-referenced with Step 5 scan  
- ArXiv search: "depth-limited search imperfect information" (Mar 2026) — 5 results  
- ArXiv search: "student of games imperfect information" (Mar 2026) — 1 result (original paper only)  
- Notable recent papers:  
  - Milec, Kovařík & Lisý (Jan 2025) "Adapting Beyond the Depth Limit: Counter Strategies in Large Imperfect Information Games" — studies opponent adaptation beyond the depth limit in large IIGs. *Directly relevant to Step 6's depth-limited solving + bridge to Step 8 (safe exploitation).*  
  - Kubíček & Lisý (Dec 2023, updated Jan 2025) "Look-ahead Search on Top of Policy Networks in Imperfect Information Games" — learned-model search that partially replaces hand-crafted search. *Relevant to the search component of architectures.*  
  - Zhang et al. "Faster Game Solving via Hyperparameter Schedules" — accepted AAAI 2026. *Optimization of the solving process. Add as supplementary.*  
  - Xu et al. (Nov 2025) "Deep Predictive Discounted CFR" — AAAI 2026. *Carried from Step 5 scan, relevant to neural CFR component of architectures.*  
  - Kubíček & Lisý (Oct 2025) "Look-ahead Reasoning with Learned Model for IIG" — *flagged in Step 4. Add as supplementary.*  
- Core references unchanged: DeepStack (2017), Libratus (2017), Pluribus (2019), ReBeL (2020), Student of Games (2021/2023) remain the canonical architecture progression.  
- Brown & Sandholm (2018) "Depth-Limited Solving for Imperfect-Information Games" confirmed as essential theoretical foundation.  
- No superseded content for Step 6 scope — these architectures form a clear historical progression.

---

> **Contribution Alignment:** This step will survey five landmark game-solving systems that define the current state of the art. ReBeL's public belief state framework is of particular relevance to the planned belief-based opponent modeling (Contribution 1). Pluribus demonstrates empirical success in multiplayer poker without formal safety guarantees — highlighting the theoretical gap that Contribution 2 will seek to address.


## Phase 1: Intuition (2 days)

The goal: understand the EVOLUTION of game-solving architectures and WHY each system exists. This isn't about memorizing papers — it's about understanding a 7-year design progression:
- **DeepStack (2017):** "What if we use neural networks to estimate values at the bottom of a search tree, like AlphaGo but for poker?"
- **Libratus (2017):** "What if we compute a coarse blueprint strategy offline, then refine it in real-time for specific situations?"
- **Pluribus (2019):** "What if we extend this to 6 players, where Nash equilibrium doesn't even technically apply?"
- **ReBeL (2020):** "What if we unify search and learning into a single framework, like AlphaZero but for imperfect info?"
- **Student of Games (2023):** "What if we unify PERFECT and IMPERFECT information games in ONE algorithm?"

End of phase: you should be able to draw the architecture diagram of each system and explain how component A of system N became component B of system N+1.

### Day 1: The Poker AI Progression (DeepStack → Libratus → Pluribus)

- **Noam Brown — "Superhuman AI for Multiplayer Poker" (NeurIPS 2019)**  
  https://www.youtube.com/watch?v=7L2sUGcOgh0  
  Duration: ~25m | Speaker: Noam Brown  
  *Fourth and final time watching this talk. NOW you have the full context (CFR, MCCFR, abstraction, Deep CFR) to understand every component Brown describes. Follow the full pipeline: blueprint → depth-limited solving → real-time search.*

- **Matej Moravcik — "DeepStack: Expert-Level Artificial Intelligence in Heads-Up No-Limit Poker"**  
  https://www.youtube.com/watch?v=2dX0lwaQRX0  
  Duration: ~20m | Speaker: Matej Moravcik (DeepMind/UAlberta)  
  *DeepStack's creator explains: continual re-solving + deep counterfactual value networks. Key difference from Libratus: DeepStack uses neural value estimation AT EVERY decision point, not just at the blueprint level.*

- **Tuomas Sandholm — "Superhuman AI for Strategic Reasoning: Libratus"**  
  https://www.youtube.com/watch?v=b7bStIQovcY  
  Duration: ~1h | Speaker: Tuomas Sandholm (CMU)  
  *Sandholm walks through the full Libratus architecture: (1) blueprint via abstracted MCCFR, (2) subgame solving for off-tree actions, (3) self-improvement module. Watch 15:00–45:00.*

### Day 2: The Unification Progression (ReBeL → Student of Games)

- **Noam Brown — "Combining Deep Reinforcement Learning and Search for Imperfect-Information Games" (NeurIPS 2020)**  
  https://www.youtube.com/watch?v=kRGJIn8mh5Q  
  Duration: ~25m | Speaker: Noam Brown  
  *Brown presents ReBeL — the first algorithm that treats imperfect-info game solving like AlphaZero treats perfect-info: alternate between (1) self-play to generate data and (2) training a value/policy network. The key innovation: the game state for imperfect info is a PUBLIC BELIEF STATE (probability distribution over all possible private information).*

- **Martin Schmid — "Student of Games: A Unified Learning Algorithm" (Science Advances 2023)**  
  https://www.youtube.com/watch?v=HZGCoVF3YvM  
  Duration: ~30m | Speaker: Martin Schmid (DeepMind/Modelbased)  
  *Schmid presents the student of games framework: Growing-Tree CFR (GT-CFR) + search + value networks. Works on BOTH perfect-info (Go, chess) AND imperfect-info (poker) games. This is the generalization proof your professors want.*

- **David Silver — "AlphaZero: Shedding New Light on Chess, Shogi, and Go" (optional)**  
  https://www.youtube.com/watch?v=p_n5fF8apiE  
  Duration: ~50m | Speaker: David Silver (DeepMind)  
  *Watch 10:00–25:00 for the AlphaZero architecture. This is the PERFECT-information template that ReBeL and Student of Games extend to imperfect information. Knowing AlphaZero helps you see exactly what ReBeL changed.*

### Blog Posts / Accessible Reads

- **Science Magazine — "Superhuman AI for multiplayer poker" (Brown & Sandholm, 2019)**  
  https://www.science.org/doi/10.1126/science.aay2400  
  *Pluribus paper in Science. Read first 3 pages for the accessible overview of the 6-player architecture.*

- **Science Advances — "Student of Games" (Schmid et al., 2023)**  
  https://www.science.org/doi/10.1126/sciadv.adg3256  
  *The Student of Games Science Advances publication. Read the introduction for the unification argument.*

- **Meta AI Blog — "ReBeL: Combining deep reinforcement learning and search" (2020)**  
  https://ai.meta.com/blog/rebel-a-general-game-playing-ai-bot-that-excels-at-poker-and-more/  
  *Accessible explanation of ReBeL with diagrams.*

---

## Phase 2: Exploration (2 days)

### Day 1: Architecture Mapping — Draw Before You Code

This step has MORE reading and LESS coding than previous steps. The value is in understanding system DESIGN, not algorithm implementation. Day 1 is a design exercise.

1. **Draw the architecture diagram for each system (pen and paper or digital):**
   
   For each system, draw a box diagram showing:
   - Offline components (computed before play)
   - Online components (computed during play)
   - The flow between them
   - Where neural networks appear
   - Where CFR/MCCFR appears
   - Where search appears
   
   **DeepStack:**
   ```
   [Training phase: Generate random poker situations → Solve with CFR → 
    Train value network to predict solution values] →
   [Play phase: At each decision → Build local subgame → Use value network 
    at depth limit → Solve subgame with CFR → Act]
   ```
   
   **Libratus:**
   ```
   [Offline: Abstract NLHE → Solve with MCCFR → Blueprint strategy] →
   [Play phase: Follow blueprint UNLESS at key decision → 
    Subgame solve (real-time CFR with safety guarantee) → Act] →
   [Post-session: Self-improvement — fix blueprint weaknesses found during play]
   ```
   
   **Pluribus:**
   ```
   [Offline: Abstract 6-max NLHE → Solve with MCCFR → Blueprint] →
   [Play phase: Follow blueprint OR depth-limited search with 
    modified RBP (Real-time Blueprint Pruning) → Act]
   ```
   
   **ReBeL:**
   ```
   [Training loop (like AlphaZero): 
    Self-play using public belief states (PBS) → 
    Generate (PBS, value) training pairs →
    Train value network on PBS → Repeat] →
   [Play phase: Search over PBS tree using trained value network]
   ```
   
   **Student of Games:**
   ```
   [Training: Growing-Tree CFR (GT-CFR) — grow game tree incrementally →
    Train value + policy networks on GT-CFR data →
    Use networks to guide further GT-CFR tree growth → Repeat] →
   [Play phase: Search using trained networks (works for perfect AND imperfect info)]
   ```

2. **Create a comparison table (fill in from videos + papers):**
   | Feature | DeepStack | Libratus | Pluribus | ReBeL | Student of Games |
   |---------|-----------|----------|----------|-------|-----------------|
   | Year | 2017 | 2017 | 2019 | 2020 | 2023 |
   | Players | 2 | 2 | 6 | 2+ | 2+ |
   | Game type | HUNL | HUNL | 6-max NL | Any IIG | Any game |
   | Blueprint | No (online) | Yes (offline) | Yes (offline) | No (learned) | No (learned) |
   | Neural component | Value net | None | None | Value net | Value + policy |
   | Search component | CFR re-solve | Subgame solve | Depth-limited | PBS search | GT-CFR search |
   | Abstraction | No | Yes | Yes | No | No |
   | Perfect info too? | No | No | No | No | **Yes** |

### Day 2: Run Existing Implementations

1. **OpenSpiel: Explore available architectures:**
   ```python
   import pyspiel
   
   # Check what IIG algorithms are available
   print([g for g in dir(pyspiel) if 'game' in g.lower()])
   
   # Run CFR variants you know on different game sizes
   # Compare solve time: Kuhn vs Leduc vs Liar's Dice
   for game_name in ["kuhn_poker", "leduc_poker", "liars_dice"]:
       game = pyspiel.load_game(game_name)
       print(f"{game_name}: {game.num_distinct_actions()} actions, "
             f"info state shape: {game.information_state_tensor_shape()}")
   ```

2. **If a ReBeL or Student of Games implementation is available in OpenSpiel or GitHub:**
   - Run it on a small game
   - Observe the training loop structure — how does it alternate between self-play and network training?
   - *Note: Full implementations may not be publicly available. If so, read the released code (e.g., Facebook's ReBeL release: https://github.com/facebookresearch/rebel) and trace the architecture.*

3. **Explore Liar's Dice as a new testbed:**
   ```python
   game = pyspiel.load_game("liars_dice")
   # Liar's Dice is larger than Leduc, has bluffing dynamics, 
   # and was used to evaluate DeepStack and Student of Games
   ```
   - Run your Step 3 MCCFR on Liar's Dice — observe convergence
   - *This game is large enough to feel the limitations of tabular methods, motivating the architectures you're studying*

4. **Questions to answer by end of Day 2:**
   - What's the key architectural difference between DeepStack and Libratus? (online re-solving vs. offline blueprint)
   - What problem does Pluribus solve that Libratus doesn't? (multi-player equilibrium)
   - How does ReBeL avoid the need for abstraction or blueprints? (public belief states + learned values)
   - What does Student of Games do that ReBeL doesn't? (unified framework for perfect AND imperfect info)

---

## Phase 3: Targeted Reading (4 days)

### Paper 1: Moravcik et al. — "DeepStack: Expert-Level Artificial Intelligence in Heads-Up No-Limit Poker" (2017)

https://arxiv.org/abs/1701.01724https://arxiv.org/abs/2102.04360

```
├── READ:  Section 2 (Continual Re-Solving — how DeepStack operates without a 
│          pre-computed blueprint by re-solving the game from scratch at each 
│          decision point using a depth-limited lookahead),
│          Section 3 (Deep Counterfactual Value Networks — the neural networks 
│          that estimate values at the depth limit of the search tree, trained 
│          offline on random poker subgames),
│          Section 4 (Experiments — results against professional poker players)
├── SKIM:  Abstract, Section 1 (Introduction — the "intuition + computation" framing),
│          Section 5 (Discussion)
├── SKIP:  Supplementary material on hand histories (unless you want poker strategy analysis)
├── MATH:  → "Equation 2 (Continual re-solving with value network) — understand 
│             how the value network at depth d replaces a full subtree traversal.
│             This is the KEY architectural innovation: instead of computing Nash
│             for the ENTIRE game (impossible for NLHE), DeepStack computes Nash
│             for a SMALL subtree and uses the network for the 'rest of the game.'
│             Same idea as AlphaGo's value network, but adapted for imperfect info."
└── KEY INSIGHT: "DeepStack treats poker like a sequence of small, solvable games
    stitched together by a value network. At each decision, it asks: 'If I solve
    this local situation perfectly and use the network for everything beyond, 
    what's my best action?' No blueprint, no abstraction — just local solving
    + learned evaluation."
```

### Paper 2: Brown & Sandholm — "Superhuman AI for Heads-Up No-Limit Poker: Libratus Beats Top Professionals" (2018)

**Link:** https://www.science.org/doi/10.1126/science.aao1733  
http://www.cs.cmu.edu/~noamb/papers/17-IJCAI-Libratus.pdfhttps://arxiv.org/abs/2006.04635

```
├── READ:  Section: "Blueprint computation" (how Libratus uses abstracted MCCFR 
│          to compute a coarse strategy for the entire game),
│          Section: "Subgame solving" (how Libratus improves the blueprint in 
│          real-time at specific decision points — this uses the safe subgame 
│          solving from Step 4's Brown & Sandholm 2017 paper),
│          Section: "Self-improvement" (the third module — post-session refinement
│          where Libratus identifies situations it handled poorly and re-solves them)
├── SKIM:  Introduction, Results section
├── SKIP:  Extended match details (human-interest reporting, not technical)
├── MATH:  → "No new math beyond what you've seen in Steps 2–5. The innovation is 
│             ARCHITECTURAL — how the three components (blueprint + subgame solve + 
│             self-improve) compose into a system. Understand the data flow."
└── KEY INSIGHT: "Libratus is a 3-module system where each module compensates for
    the others' weaknesses: (1) blueprint handles the average case with abstraction,
    (2) subgame solving fixes abstraction errors at specific decision points,
    (3) self-improvement patches systematic weaknesses found during play. This
    modular design principle recurs across all subsequent systems."
```

### Paper 3: Brown & Sandholm — "Superhuman AI for Multiplayer Poker" (Pluribus, 2019)

**Link:** https://www.science.org/doi/10.1126/science.aay2400  
**Alt link:** https://arxiv.org/abs/1911.07559https://arxiv.org/abs/2004.04136 (extended version)

```
├── READ:  Section 2 (Methods — the full 6-player architecture: MCCFR blueprint
│          with Linear CFR + depth-limited search with modified RBP),
│          Section 2.1 (Blueprint strategy — how MCCFR is adapted for 6 players:
│          use "everyone vs. everyone" training, not just player-vs-player),
│          Section 2.2 (Real-time search — how depth-limited search works when 
│          Nash equilibrium is ILL-DEFINED for 6 players: Pluribus uses a 
│          modified search that assumes opponents stick to the blueprint 
│          beyond a certain depth)
├── SKIM:  Abstract, Section 1 (Introduction),
│          Section 3 (Results — 10,000 hands against professionals),
│          Section 4 (Discussion)
├── SKIP:  Supplementary hand analysis
├── MATH:  → "Section 2.2 (Modified search for multiplayer) — understand the key
│             dilemma: in 2-player zero-sum, Nash equilibrium guarantees you can't
│             lose. In 6-player, there IS no single Nash equilibrium — opponents
│             can collude against you. Pluribus handles this pragmatically, not
│             theoretically: search assuming opponents follow blueprint, then
│             adapting. NOT proven safe — empirically effective."
└── KEY INSIGHT: "Pluribus proves that Nash-equilibrium-based approaches work 
    empirically for multiplayer games even though they LACK theoretical 
    guarantees beyond 2-player zero-sum. This is important for your thesis:
    extending safety guarantees to N-player settings (Contribution #2) is 
    an OPEN PROBLEM that Pluribus deliberately sidesteps."
```

### Paper 4: Brown, Bakhtin, Lerer & Hu — "Combining Deep Reinforcement Learning and Search for Imperfect-Information Games" (ReBeL, 2020)

https://arxiv.org/abs/2007.13544https://arxiv.org/abs/1707.06203 (NeurIPS 2020)

```
├── READ:  Section 3 (Public Belief States — THE key theoretical innovation: 
│          representing the game state as a probability distribution over all 
│          possible private information, conditioned on publicly observed actions.
│          This is what makes search in IIGs tractable without abstraction),
│          Section 4 (The ReBeL algorithm — the full training loop: generate 
│          PBS values via CFR at leaf nodes, train a value network on (PBS, value)
│          pairs, use the trained network for deeper search. Exactly like AlphaZero
│          but with PBS instead of board states),
│          Section 5 (Experiments — Liar's Dice and HUNL results)
├── SKIM:  Abstract, Section 1 (Introduction — the AlphaZero parallel),
│          Section 2 (Background),
│          Section 6 (Discussion)
├── SKIP:  Appendix proofs (read theorem statements only)
├── MATH:  → "Definition 1 (Public Belief State) — MUST understand. A PBS is a 
│             vector of probabilities: for each possible private information 
│             assignment (e.g., each possible hand), what's the probability of
│             that assignment given the publicly observed action history? This
│             is the state representation that makes imperfect-info search work.
│             It's the imperfect-info analog of a board position in chess."
│          → "Theorem 1 (Sound PBS-based search) — read the STATEMENT. This 
│             guarantees that searching over PBS space converges to a Nash 
│             equilibrium. This is the theoretical foundation for ReBeL."
└── KEY INSIGHT: "ReBeL solves the holy grail problem: how to do AlphaZero-style
    search in imperfect-information games. The answer is Public Belief States — 
    instead of searching over game positions (which are hidden in IIGs), search 
    over PROBABILITY DISTRIBUTIONS of what position you might be in. Combined 
    with CFR at leaf nodes and a learned value network, this enables search 
    without abstraction or blueprints."
```

### Paper 5: Schmid et al. — "Student of Games: A Unified Learning Algorithm for Both Perfect and Imperfect Information Games" (2023)

https://arxiv.org/abs/2112.03178https://arxiv.org/abs/1611.02779 (Science Advances 2023)

```
├── READ:  Section 2 (Growing-Tree CFR — GT-CFR: the algorithm that incrementally
│          builds a game tree guided by policy networks, instead of requiring the
│          full tree. This is what enables combined perfect + imperfect info),
│          Section 3 (The Student of Games framework — how GT-CFR + value networks
│          + policy networks compose into a unified algorithm),
│          Section 4.2 (Imperfect-info experiments — poker and Scotland Yard results),
│          Section 4.3 (Perfect-info experiments — Go results)
├── SKIM:  Abstract, Section 1 (Introduction — the unification argument),
│          Section 4.1 (Setup),
│          Section 5 (Discussion)
├── SKIP:  Appendix details on Go training (not relevant to your thesis domain)
├── MATH:  → "Algorithm 1 (GT-CFR) — trace the algorithm carefully. The key
│             difference from vanilla CFR: instead of traversing the ENTIRE tree,
│             GT-CFR grows the tree incrementally, guided by the policy network.
│             Where the tree hasn't been expanded, it uses value network estimates.
│             This is how it handles games too large for full traversal."
│          → "Theorem 1 (Convergence of GT-CFR) — read statement only. Guarantees
│             that GT-CFR converges to Nash as the tree grows."
└── KEY INSIGHT: "Student of Games unifies perfect-info (AlphaZero approach) and
    imperfect-info (CFR approach) into ONE algorithm. For perfect-info subtrees,
    it reduces to MCTS-like search. For imperfect-info, it reduces to CFR-like
    iteration. The policy network decides WHERE to expand the tree, making it
    efficient for both types. THIS is the generalization proof your professors want:
    a single algorithm framework that subsumes both chess/Go AI and poker AI."
```

### Paper 6: Brown & Sandholm — "Depth-Limited Solving for Imperfect-Information Games" (2018)

https://arxiv.org/abs/1805.08195https://arxiv.org/abs/2009.04416 (NeurIPS 2018)

```
├── READ:  Section 3 (Depth-limited solving — the theoretical framework for 
│          cutting off search at a fixed depth and using estimated leaf values.
│          Fundamental to ALL architectures above: DeepStack, Libratus, Pluribus,
│          ReBeL all use some form of depth-limited solving),
│          Section 4 (Using learned values at the depth limit — the connection
│          between this theoretical framework and neural value estimation)
├── SKIM:  Abstract, Sections 1–2, Section 5 (Experiments)
├── SKIP:  Convergence proofs (read statements)
├── MATH:  → "Theorem 1 (Exploitability bound for depth-limited solving) — read
│             the STATEMENT. This bound is what tells you: 'if your value network
│             estimates are off by ε, the full strategy's exploitability increases
│             by at most f(ε).' This is the error propagation guarantee that makes
│             depth-limited search trustworthy. Critical for Step 8 (safe exploitation)."
└── KEY INSIGHT: "Depth-limited solving is the UNIFYING theoretical concept across
    all five architectures. Every system cuts off the game tree at some depth and 
    uses an estimate for 'everything beyond.' DeepStack uses a trained value 
    network. Libratus uses the blueprint. Pluribus uses the blueprint with 
    rollouts. ReBeL uses a learned PBS value. The theory in this paper is what 
    guarantees they all work."
```

### Supplementary References

- **Milec, Kovařík & Lisý (2025) — "Adapting Beyond the Depth Limit"**  
  https://arxiv.org/abs/2501.10464https://arxiv.org/abs/1507.01228  
  *Studies opponent adaptation beyond the search depth. SKIM abstract + Section 3. Bridges Step 6 → Step 8 (safe exploitation). Key question: can depth-limited search-based systems adapt to sub-rational opponents while maintaining robustness?*

- **Kubíček & Lisý (2023/2025) — "Look-ahead Search on Top of Policy Networks in IIGs"**  
  https://arxiv.org/abs/2312.15220https://arxiv.org/abs/2103.04026  
  *Explores adding test-time search on top of policy networks trained via RL/CFR. SKIM abstract + Section 2. Relevant to the search-vs-learning tradeoff.*

- **Zarick et al. (2020) — "Unlocking the Potential of Deep Counterfactual Value Networks"**  
  https://arxiv.org/abs/2007.10442https://arxiv.org/abs/1912.06680  
  *Improvements to DeepStack-style value network training. SKIM for practical insights if implementing value networks.*

### Math Flags

🔢 **Public Belief State definition (Brown et al., ReBeL, Def. 1)** — Must understand fully.  
**WHY this can't be substituted:** PBS is the core state representation for imperfect-info search. Your thesis (opponent modeling in Step 7) will likely need to track beliefs about opponent strategies — essentially, you're building a more nuanced PBS. If you don't understand the standard PBS definition, you can't extend it.

🔢 **Depth-limited solving exploitability bound (Brown & Sandholm 2018, Theorem 1)** — Must understand the statement and what it depends on.  
**WHY:** This bound quantifies how value network errors propagate to exploitability. For your thesis's safe exploitation component (Contribution #1), you need to know: if your opponent model is wrong by ε, how much can you lose? This theorem provides the template for that analysis.

🔢 **GT-CFR convergence (Schmid et al., Theorem 1)** — Read statement.  
**WHY:** Student of Games is the most general framework in this step. Understanding its convergence guarantee tells you what conditions your thesis framework needs to satisfy.

---

## Phase 4: Implementation (10 days)

### Project: ReBeL-Lite for Leduc Hold'em + Architecture Comparison Framework

This step's implementation is different from Steps 3–5. The primary output is UNDERSTANDING OF SYSTEM DESIGN, not just algorithmic implementation. The implementation focuses on ReBeL (the most general and instructive architecture) as a concrete case study, while the other architectures are studied through paper analysis and diagram construction.

**Language + Framework:** Python 3.10+ / PyTorch

Starting point: Your Leduc engine (Step 3) + Deep CFR (Step 5) + abstraction pipeline (Step 4).

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| Public Belief State (PBS) representation + update logic | 🔴 HAND-CODE | PBS is the core theoretical concept. You must understand: how to initialize a belief (uniform over possible hands), how to update it given observed actions (Bayesian update using action probabilities), and how to represent it as a tensor. This is YOUR thesis's belief representation foundation. |
| PBS-based CFR at leaf nodes (mini-CFR solver within search) | 🔴 HAND-CODE | ReBeL uses CFR to solve local subgames at search leaves. This connects Step 3's CFR to the search framework. You must hand-code this to understand how CFR operates WITHIN a search tree, not just on a complete game. |
| PBS value network (predicts expected value given a public belief state) | 🔴 HAND-CODE | The network that estimates game value from a PBS. This is analogous to AlphaZero's value head but for imperfect info. Input: PBS tensor. Output: expected payoff. Training data comes from PBS-CFR solutions. Core to both ReBeL and DeepStack architectures. |
| ReBeL training loop (self-play → PBS-CFR → value network training → repeat) | 🔴 HAND-CODE | The training loop IS ReBeL. Understanding how search data feeds network training which feeds better search is the key intellectual content. |
| Architecture comparison framework (tables, diagrams, written analysis) | 🟡 AI-ASSISTED | Comparison tables and written analysis. AI helps structure, you fill in the analysis from your paper readings. |
| Search tree expansion logic | 🟡 AI-ASSISTED | Tree data structures and traversal. AI drafts template, you implement the PBS-specific logic. |
| Hyperparameter tuning, logging, experiment management | 🟢 AI-GENERATED | Standard training infrastructure. |
| Plotting (training curves, PBS visualizations, architecture diagrams) | 🟢 AI-GENERATED | Visualizations. |

### Sub-phase Breakdown (10 days):

**Days 1–2 — Architecture + PBS Representation:**
- 🔴 Design the Public Belief State representation for Leduc:
  - PBS = vector of probabilities over all possible private information assignments
  - In Leduc: each player can hold one of 6 cards. PBS for player 1 = 6-dim probability vector (one per possible hand)
  - Two-player PBS: a probability matrix over (hand_p1, hand_p2) — constrained by dealt cards
  - Update rule: given observed action a at info set I, update PBS using Bayes' rule:
    ```
    P(hand | action_history + a) ∝ P(a | hand, info_set) × P(hand | action_history)
    ```
  - Implement: `PBS.update(action, acting_player)` — the Bayesian update
  - Test: verify belief updates are correct on Kuhn (simple enough to verify by hand)
- Design the overall ReBeL-Lite architecture:
  - Training: Iterate (self-play PBS episodes → solve PBS positions with CFR → train value net on solutions → repeat)
  - Search: Given PBS → build local game tree of depth d → CFR at leaves → estimate leaf PBS values with network

**Days 3–4 — PBS-CFR (Local Solver):**
- 🔴 Implement CFR that operates on PUBLIC BELIEF STATES rather than information sets:
  - Input: a PBS (probability distribution over hands)
  - Operation: run CFR iterations over the local game tree, starting from the given PBS
  - Output: strategy at each info set + expected value for the given PBS
  - This is your Step 3 CFR adapted to work within a search tree depth window
- Difference from Step 3 CFR: instead of starting from the root (where all hands are equally likely), you start from an ARBITRARY belief state (because the search may reach this PBS from different paths)
- Test on Kuhn: solve the full game using PBS-CFR starting from the initial PBS. Should match your Step 2/3 Nash solution.

**Days 5–6 — PBS Value Network + Training Data:**
- 🔴 Implement the PBS value network:
  - Input: PBS tensor (the probability distribution over possible private information)
  - Architecture: MLP (PBS_dim → 128 → 128 → 1) predicting expected value for the acting player
  - Training data: (PBS, value_from_CFR_solution) pairs generated by PBS-CFR
- 🔴 Generate training data:
  - Sample random PBS positions in Leduc (random action histories → compute resulting PBS)
  - Solve each PBS with PBS-CFR (your standalone solver)
  - Collect (PBS, expected_value) pairs
  - Train value network via supervised learning (MSE loss)
- Validate: check that trained network's value predictions correlate with CFR solutions (R² > 0.9)

**Days 7–8 — ReBeL Training Loop:**
- 🔴 Implement the full ReBeL-Lite training loop:
  1. Initialize random value network
  2. For each training iteration:
     a. Play self-play games using current value network for depth-limited search
     b. At depth limit: query value network for PBS value estimate
     c. Above depth limit: run K iterations of CFR using value network at leaves
     d. Collect (PBS, CFR_value) training pairs from the search
     e. Train value network on collected pairs
  3. After N iterations, evaluate: compute exploitability of the policy implied by the value network
- Run for 100+ outer iterations on Leduc
- Plot: exploitability vs training iterations (should steadily decrease)
- Compare against: (a) Deep CFR from Step 5, (b) tabular MCCFR from Step 3

**Days 9–10 — Architecture Comparison + Documentation:**
- 🟡 AI-ASSISTED: Create the comprehensive architecture comparison:
  
  1. **Comparison table** (filled in from your paper readings + implementation experience):
     | Feature | DeepStack | Libratus | Pluribus | ReBeL | SoG |
     |---------|-----------|----------|----------|-------|-----|
     | Offline compute | Value net training | Blueprint MCCFR | Blueprint MCCFR | Self-play + net training | GT-CFR + net training |
     | Online compute | Continual re-solve | Subgame solve | Depth-limited search | PBS search + CFR | GT-CFR search |
     | Uses abstraction? | No | Yes | Yes | No | No |
     | Uses neural nets? | Yes (value) | No | No | Yes (value) | Yes (value + policy) |
     | Players | 2 | 2 | 6 | 2+ | 2+ |
     | Perfect info too? | No | No | No | No | Yes |
     | Key innovation | Online re-solving | Modular system | Multi-player | PBS framework | Unified perfect/imperfect |
  
  2. **Evolution diagram**: Draw how each system builds on the previous
  3. **Component reuse analysis**: Which Step 3–5 components appear in which architecture?
     - MCCFR → appears in Libratus (blueprint), Pluribus (blueprint)
     - Deep CFR value networks → DeepStack, ReBeL, SoG all use similar value nets
     - Abstraction → Libratus, Pluribus. NOT in DeepStack, ReBeL, SoG (replaced by neural approximation)
     - PBS → ReBeL, SoG

- Cross-validate ReBeL-Lite against published results:
  - Exploitability on Leduc should comparable to Deep CFR
  - Training should show clear improvement over untrained random play

- Document the architecture comparison as a structured analysis

### Deliverables:
- [ ] PBS representation module (init, Bayesian update, tensor encoding) — working on Kuhn and Leduc
- [ ] PBS-CFR local solver operating on arbitrary belief states
- [ ] PBS value network trained on Leduc, predictions correlating with CFR solutions
- [ ] ReBeL-Lite training loop — self-play → PBS-CFR → value network → repeat
- [ ] Architecture comparison table (all 5 systems) with analysis
- [ ] Architecture evolution diagram
- [ ] Component reuse analysis (which Steps 3–5 building blocks appear where)
- [ ] All code committed with README

### Validation:
- **PBS updates:** Beliefs must sum to 1, must correctly zero out impossible hands (e.g., if a card is on the board, no player holds it). Verify on Kuhn by hand.
- **PBS-CFR on Kuhn:** Should reproduce full-game Nash equilibrium when starting from initial uniform PBS.
- **PBS-CFR on Leduc:** Exploitability should match Step 3's CFR within 10%.
- **PBS value network:** R² > 0.9 between predicted values and CFR-solved values on held-out test PBS positions.
- **ReBeL-Lite:** Exploitability should decrease monotonically across training iterations. After 100+ iterations, should be within 2x of Deep CFR's exploitability on Leduc.

---

## Phase 5: Consolidation (3 days)

### Day 1 — Book Chapter Skim + Supplementary Papers

- **Reference skim:** Brown & Sandholm (2018) "Depth-Limited Solving" — if not fully absorbed during Phase 3, revisit Section 3 and the exploitability bound. This paper is the theoretical glue across all architectures.

- **Supplementary skim:** Milec et al. (2025) "Adapting Beyond the Depth Limit" — read abstract + Section 3. *Key connection to Step 8: what happens when your depth-limited search encounters an opponent who deviates from expectations beyond the depth limit? This is the bridge to safe exploitation.*

- **Supplementary skim:** Kubíček & Lisý (2025) "Look-ahead Search on Policy Networks in IIGs" — read abstract. *Notes for Step 15: is learned search replacing hand-coded search?*

- Review: which architecture components do you NOT yet understand well enough for the whiteboard test?

### Day 2 — Architecture Synthesis + PhD Mapping

- **Write the architecture evolution essay (1–2 pages, committed to repo):**
  - The evolution from "solve everything offline" (Libratus) → "solve nothing offline, learn instead" (ReBeL/SoG)
  - The evolution from "abstraction-based" (Libratus/Pluribus) → "neural-approximation-based" (DeepStack/ReBeL/SoG)
  - The convergence toward AlphaZero-style "self-play + search + network" for imperfect info
  - Where the OPEN problems remain:
    - Multi-player safety guarantees (Pluribus sidesteps this)
    - Opponent adaptation beyond the depth limit (Milec et al. 2025)
    - Real-time compute budget constraints

- **Map each architecture to your thesis contributions:**
  - Contribution #1 (Behavioral Adaptation): ReBeL's PBS is the natural starting point for belief-based opponent modeling. Your innovation: extending PBS to include BELIEFS ABOUT THE OPPONENT'S STRATEGY TYPE, not just their hand.
  - Contribution #2 (Multi-Agent Safe Exploitation): Pluribus's lack of multiplayer safety guarantees IS the gap. Your thesis fills it.
  - Contribution #3 (Evaluation Methodology): The exploitability metric used across all 5 systems becomes your evaluation backbone.

### Day 3 — One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 3] MCCFR → [Step 6] appears as the blueprint computation engine in Libratus and Pluribus. Same algorithm, different scale.
    - [Step 4] Abstraction → [Step 6] required by Libratus/Pluribus but ABSENT in DeepStack/ReBeL/SoG. Neural approximation replaced hand-crafted abstraction. The progression: manual (Step 4) → learned (Step 5) → integrated into architecture (Step 6).
    - [Step 4] Subgame solving (Brown & Sandholm 2017) → [Step 6] the online refinement mechanism in Libratus. Same algorithm, now embedded in a system.
    - [Step 5] Deep CFR advantage networks → [Step 6] DeepStack's value networks and ReBeL's PBS value network are conceptually identical — neural networks predicting game values at specific states. Deep CFR trains on info states, ReBeL trains on public belief states.
    - [Step 5] NFSP's anticipatory parameter → [Step 6] Pluribus's "search assuming opponents follow blueprint" is a similar pragmatic tradeoff between Nash play and adaptation.
    - [Step 1] AlphaGo/AlphaZero (Silver et al.) → [Step 6] ReBeL IS AlphaZero for imperfect info. Self-play + search + value network. The PBS is what makes this possible for hidden information.
    - [Step 6] PBS-based search → prediction: [Step 7] Opponent modeling will extend PBS by adding a BELIEF ABOUT OPPONENT STRATEGY TYPE on top of the belief about hands.
    - [Step 6] Depth-limited solving error bounds → prediction: [Step 8] Safe exploitation will need similar bounds: "if my opponent model is wrong by ε, how much can I lose?"
  - **Confusions:**
    - [Step 6] ReBeL works on 2-player. The paper says it can extend to multiplayer. But how? In multiplayer, the PBS becomes exponentially larger (belief over all opponents' hands). → OPEN (check Step 9 MARL literature, or Step 15 frontier mapping)
    - [Step 6] Student of Games promises to work for BOTH perfect and imperfect info. But is GT-CFR actually competitive with MCTS for Go? The paper shows it works but doesn't match AlphaZero. Is the unified framework too general to be optimal for either? → OPEN (philosophical question for Step 15)
    - [Step 5→6] My Step 5 confusion about why Deep CFR trains from scratch each iteration: ReBeL also alternates training and data collection but FINE-TUNES the network. What's different? → PARTIALLY RESOLVED (hypothesis: ReBeL's PBS-based data is more stable because it conditions on public history, while Deep CFR's info-state data shifts as the strategy changes)
    - [Step 3→6] Pluribus uses Linear CFR for the blueprint. This was Xu et al.'s starting point for Predictive Discounted CFR (AAAI 2026). Is LCFR provably better than DCFR for blueprints? → OPEN (minor, check if papers address this)

### PhD Connection

This step is the **architectural foundation** for the entire thesis. Every subsequent step (7–15) builds on the systems studied here:
- **Contribution #1 (Behavioral Adaptation Framework):** ReBeL's PBS representation provides the starting point. Your thesis extends PBS to include beliefs about opponent strategy types, creating a richer state representation for adaptive play. DeepStack's continual re-solving provides the template for real-time strategy adjustment.
- **Contribution #2 (Multi-Agent Safe Exploitation):** Pluribus demonstrates that Nash-based approaches work empirically for N-player games but provides NO safety guarantee. This gap is your thesis contribution. The theoretical tools from Steps 4 (subgame solving safety) and 6 (depth-limited solving bounds) provide the starting point for developing N-player guarantees.
- **Contribution #3 (Evaluation Methodology):** The exploitability metric used across ALL five systems is the evaluation backbone. Student of Games' unified framework for perfect + imperfect info provides the template for a domain-agnostic evaluation framework.

---

## Exit Checklist

- [ ] Can draw architecture diagrams for all 5 systems from memory (DeepStack, Libratus, Pluribus, ReBeL, Student of Games)
- [ ] Can explain the evolution: why each system exists and what problem it addresses that previous systems didn't
- [ ] PBS representation module working with correct Bayesian updates
- [ ] PBS-CFR local solver working on Kuhn and Leduc
- [ ] PBS value network trained and correlating with CFR solutions (R² > 0.9)
- [ ] ReBeL-Lite training loop converging on Leduc (exploitability decreasing)
- [ ] Architecture comparison table completed with written analysis
- [ ] Architecture evolution diagram created
- [ ] Can explain from memory: Public Belief States and why they enable search in IIGs
- [ ] Can explain from memory: depth-limited solving and the error propagation bound
- [ ] Component reuse analysis showing which Steps 3–5 building blocks appear in which architecture
- [ ] All 🔴 components hand-coded
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Steps 1–5 + new confusions + resolved confusions)
- [ ] Step notes committed to repo

