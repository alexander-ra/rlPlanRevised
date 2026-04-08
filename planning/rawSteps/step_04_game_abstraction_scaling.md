# Step 4 — Game Abstraction + Scaling Imperfect-Information Games

**Duration:** 10 days (Tier 2 — compressed)  
**Dependencies:** Step 2 (Game Theory + CFR Basics), Step 3 (CFR Variants + MC Methods)  
**Phase:** B — Scaling the Toolbox

> **Know-How First compression:** Implementation phase cut from 6d to 3d. Build one working abstraction example (card bucketing on Extended Leduc). Defer full abstraction pipeline (action abstraction, information abstraction comparison) to implementation phase post-November. All reading and intuition phases unchanged.
> Phase allocation: Intuition 1d | Exploration 1d | Reading 3d | Implementation **3d** | Consolidation 2d  

### PhD Connection

This step feeds **Contribution #1 (Behavioral Adaptation Framework)**: the abstraction pipeline determines the game representation that the adaptive agent will operate on. Poor abstraction limits how finely the agent can distinguish between opponent types. Also feeds **Contribution #3 (Evaluation Methodology)**: the exploitability-gap metric from this step becomes a standard evaluation measure. The Pareto frontier framework (abstraction size vs strategy quality) provides a template for evaluating tradeoffs in the thesis evaluation chapter.

---

## Table of Contents
- [Phase 1: Intuition (1 day)](#phase-1-intuition-1-day)
  - [Videos](#videos)
  - [Blog Posts / Accessible Reads](#blog-posts-accessible-reads)
- [Phase 2: Exploration (2 days)](#phase-2-exploration-2-days)
  - [Day 1: Information Abstraction — Card Bucketing in OpenSpiel](#day-1-information-abstraction-card-bucketing-in-openspiel)
  - [Day 2: Action Abstraction — Restricting Bet Sizes](#day-2-action-abstraction-restricting-bet-sizes)
- [Phase 3: Targeted Reading (3 days)](#phase-3-targeted-reading-3-days)
  - [Paper 1: Gilpin & Sandholm — "Lossless Abstraction of Imperfect Information Games" (2007)](#paper-1-gilpin-sandholm-lossless-abstraction-of-imperfect-information-games-2007)
  - [Paper 2: Johanson, Burch, Valenzano & Bowling — "Evaluating State-Space Abstractions in Extensive-Form Games" (2013)](#paper-2-johanson-burch-valenzano-bowling-evaluating-state-space-abstractions-in-extensive-form-games-2013)
  - [Paper 3: Kroer & Sandholm — "Imperfect-Recall Abstractions with Bounds in Games" (2016)](#paper-3-kroer-sandholm-imperfect-recall-abstractions-with-bounds-in-games-2016)
  - [Paper 4: Brown & Sandholm — "Safe and Nested Subgame Solving for Imperfect-Information Games" (2017)](#paper-4-brown-sandholm-safe-and-nested-subgame-solving-for-imperfect-information-games-2017)
  - [Supplementary References](#supplementary-references)
  - [Math Flags](#math-flags)
- [Phase 4: Implementation (6 days)](#phase-4-implementation-6-days)
  - [Project: Abstraction Pipeline for Leduc & Extended Leduc — From Scratch](#project-abstraction-pipeline-for-leduc-extended-leduc-from-scratch)
  - [Sub-phase Breakdown (6 days):](#sub-phase-breakdown-6-days)
  - [Deliverables:](#deliverables)
  - [Validation:](#validation)
- [Phase 5: Consolidation (2 days)](#phase-5-consolidation-2-days)
  - [Day 1 — Reference Skim + Architecture Preview](#day-1-reference-skim-architecture-preview)
  - [Day 2 — One-Pager + Learning Log](#day-2-one-pager-learning-log)
- [Exit Checklist](#exit-checklist)

## Phase 1: Intuition (1 day)

The goal: understand WHY abstraction is needed (games are too large to represent in memory), what the two types of abstraction ARE (information abstraction = grouping similar game states; action abstraction = reducing the set of available moves), and what the danger IS (bad abstraction → bad strategies). End of day: you should be able to explain to a non-expert: "Texas Hold'em has 10^161 game states. We can't store them all, so we group similar ones together — like calling a king-high flush the same whether it's spades or hearts. The trick is choosing groups that don't throw away strategic differences."

### Videos

- [**Stanford CS221 — Lecture 10: Games I (Autumn 2025)**](https://www.youtube.com/watch?v=SMOD_GiRzb8)
  *Why search explodes: game trees, minimax, evaluation functions, alpha-beta pruning. The motivation for why abstraction is needed — games are too large to solve exactly.*

- [**Monte Carlo Tree Search — Computerphile**](https://www.youtube.com/watch?v=BEFY7IHs0HM)
  *Why brute-force fails and how sampling-based search (MCTS) provides an alternative to full enumeration. The conceptual bridge from "traverse everything" to "sample intelligently."*

- [**NIPS 2017 Best Paper — Safe & Nested Subgame Solving for Imperfect-Information Games**](https://www.youtube.com/watch?v=tRiaGahlyy4)
  *Accessible walkthrough of how subgame solving fixes abstraction errors in real-time during play. The key idea: solve a coarse abstract game first, then refine specific subgames.*

- [**AI for Imperfect-Information Games: Beating Top Humans in No-Limit Poker**](https://www.youtube.com/watch?v=McV4a6umbAY)
  *Full deep-dive into the Libratus architecture: how card abstraction groups similar hands, how action abstraction restricts bet sizes, how strategies are translated back, and how subgame solving patches errors.*

- [**Stanford CS234 — Lecture 15: Value Alignment (Spring 2024)**](https://www.youtube.com/watch?v=FOlPpjNbHjE)
  *Covers MCTS and AlphaZero — the search methods used inside modern game AI when doing depth-limited solving at the game tree's frontier, exactly where abstraction matters most.*

### Blog Posts / Accessible Reads

- **Science Magazine — "Superhuman AI for heads-up no-limit poker: Libratus beats top professionals" (2017)**  
  https://www.science.org/doi/10.1126/science.aao1733  
  *The Libratus paper in Science format — read the first 3 pages for a clear, non-technical description of how abstraction + solving works in practice.*

- **Papers With Code — "Game Abstraction" task page**  
  https://paperswithcode.com/task/game-abstraction  
  *Quick overview of what's been done + links to implementations. Check if any new benchmarks have appeared.*

---

## Phase 2: Exploration (2 days)

### 🎮 Interactive Exploration
- **[Visualizing K-Means Clustering](https://www.naftaliharris.com/blog/visualizing-k-means-clustering/)** — Abstraction connects deeply with clustering. Play with this K-Means interactive to build intuition on grouping similar game states.


### Day 1: Information Abstraction — Card Bucketing in OpenSpiel

1. **Explore Leduc Hold'em information sets from Step 3:**
   - From your Step 3 Leduc engine, enumerate all 936 information sets
   - Group them manually by "strategic similarity":
     - Pre-flop with J vs Q vs K (3 groups)
     - Post-flop with pair (J+J, Q+Q, K+K → 3 groups) vs non-pair (J+Q, J+K, Q+K, etc. → 6 groups)
   - *Observe: Leduc has natural abstraction because suits don't matter. If you had J♠ and J♥ as separate info sets, collapsing them is a LOSSLESS abstraction — no strategic information is lost.*

2. **Run MCCFR on Leduc with suit isomorphism explicitly applied:**
   - Modify your Step 3 Leduc engine to collapse suit-isomorphic states
   - Run MCCFR on the abstracted game tree
   - *Expected result: identical Nash equilibrium strategies, fewer info sets to store, faster convergence*

3. **Experiment with a LOSSY information abstraction:**
   - Collapse J and Q into one "low card" bucket, keep K separate
   - Run MCCFR on this 2-bucket abstraction
   - Compare the resulting strategy against the exact Nash equilibrium
   - *Observe: the abstract strategy will be WRONG. The differences between J and Q matter strategically. This is the danger of lossy abstraction.*

### Day 2: Action Abstraction — Restricting Bet Sizes

1. **Create a "Mini NLHE" variant in your engine:**
   - Take Leduc Hold'em and allow variable bet sizes: {0.5×pot, 1×pot, 2×pot, all-in}
   - *This creates a much larger game tree (each decision point now has 4+ choices instead of 2)*
   - Count info sets → should be ~10k+ depending on implementation

2. **Apply action abstraction:**
   - Abstract: allow only {fold, call, pot-size bet}
   - Run MCCFR on abstracted version
   - Translate strategies back to the full game using nearest-action mapping
   - *Observe: the translated strategy won't be Nash for the full game, but will be "close." How close?*

3. **Measure abstraction quality:**
   - Compute exploitability of the abstract strategy when deployed in the full game
   - Compare: full-game Nash exploitability (the target) vs abstracted strategy's exploitability
   - *This gap is the "price of abstraction" — the central quantity this step teaches you to manage.*

4. **Questions to answer by end of Day 2:**
   - What's the difference between information abstraction and action abstraction?
   - When is abstraction lossless vs lossy? What makes it lossless?
   - What happens when an opponent plays an action that isn't in your abstraction? (action translation problem)
   - Why can't you just pick the finest-grained abstraction possible? (memory + computation tradeoff)

---

## Phase 3: Targeted Reading (3 days)

### Paper 1: Gilpin & Sandholm — "Lossless Abstraction of Imperfect Information Games" (2007)

https://dl.acm.org/doi/10.5555/1625275.1625300  
https://www.cs.cmu.edu/~sandholm/lossless.jacm.pdf

```
├── READ:  Section 2 (Game-theoretic background — skim if comfortable from Step 2),
│          Section 3 (Ordered Game Isomorphisms — THE key concept: what makes an
│          abstraction information-preserving/lossless),
│          Section 4 (Algorithm for finding lossless abstractions — GameShrink 
│          algorithm)
├── SKIM:  Abstract, Section 1 (Introduction — framing),
│          Section 5 (Experiments — reduction sizes on poker variants),
│          Section 6 (Related work)
├── SKIP:  Proofs in Section 3 (unless you want to verify the isomorphism guarantees)
├── MATH:  → "Definition 3 (Ordered Game Isomorphism) — read and understand the 
│             formal definition. This is NOT optional math — it's the criterion you 
│             use to decide whether a proposed abstraction is lossless. If you get 
│             this wrong, your abstracted strategy could be arbitrarily bad."
│          → "Theorem 1 (GameShrink finds all ordered game isomorphisms) — read 
│             the statement. This tells you the algorithm is COMPLETE — it won't
│             miss any lossless abstractions of this type."
└── KEY INSIGHT: "Not all abstractions are equal. Lossless abstraction GUARANTEES
    the Nash equilibrium of the abstract game IS a Nash equilibrium of the original
    game. Lossy abstraction introduces error with no upper bound unless you work
    to bound it. Always prefer lossless when possible; use lossy only at scale."
```

### Paper 2: Johanson, Burch, Valenzano & Bowling — "Evaluating State-Space Abstractions in Extensive-Form Games" (2013)

https://poker.cs.ualberta.ca/publications/AAMAS13-abstraction.pdf

```
├── READ:  Section 3 (Earth Mover's Distance for evaluating abstraction quality —
│          THE quantitative measure of how much information a lossy abstraction 
│          throws away),
│          Section 4 (Experiments — how abstraction granularity maps to strategy
│          quality on poker variants)
├── SKIM:  Abstract, Section 1–2 (Background — you know this),
│          Section 5 (Related work),
│          Section 6 (Conclusions)
├── SKIP:  None — this paper is concise
├── MATH:  → "Definition 1 (EMD between abstract and real game distributions) —
│             understand the formula. It's the metric you'll use to evaluate YOUR
│             abstractions in Phase 4."
└── KEY INSIGHT: "Abstraction quality isn't binary — it's a spectrum measurable 
    by Earth Mover's Distance. This gives you a principled way to CHOOSE between 
    abstraction granularities: finer = better strategy but more memory/compute, 
    coarser = faster but worse strategy. The optimal point depends on your 
    computational budget."
```

### Paper 3: Kroer & Sandholm — "Imperfect-Recall Abstractions with Bounds in Games" (2016)

https://arxiv.org/abs/1409.3302

```
├── READ:  Section 3 (Bounded imperfect-recall abstractions — how to deliberately 
│          forget information while maintaining error guarantees),
│          Section 4 (The A-EFCE solution concept and its properties)
├── SKIM:  Abstract, Section 1–2 (Background),
│          Section 5 (Experiments),
│          Section 6 (Conclusion)
├── SKIP:  Full proofs in Section 3 (read theorem statements only)
├── MATH:  → "Theorem 1 (Error bound for imperfect-recall abstraction) — read the 
│             STATEMENT. This is the first result showing that lossy abstraction 
│             can have provable error guarantees. Know that the bound exists and 
│             what it depends on (abstraction granularity + game structure)."
└── KEY INSIGHT: "Imperfect recall (deliberately forgetting past information) is a 
    powerful abstraction technique — it can reduce game size exponentially. 
    Kroer & Sandholm show it doesn't have to be blind loss: you can compute 
    error bounds. This is the theoretical basis for practical card bucketing in 
    large poker games."
```

### Paper 4: Brown & Sandholm — "Safe and Nested Subgame Solving for Imperfect-Information Games" (2017)

https://arxiv.org/abs/1705.02955

```
├── READ:  Section 3 (Subgame solving — how Libratus/Pluribus refines the abstract 
│          blueprint strategy in real time for specific game subtrees),
│          Section 4 (Nested subgame solving — recursive refinement)
├── SKIM:  Abstract, Section 1–2 (Motivation and Unsafe subgame solving),
│          Section 5 (Experiments — results on poker variants)
├── SKIP:  Proofs (read for understanding, not derivation)
├── MATH:  → "Theorem 1 (Safety guarantee of subgame solving) — read the 
│             STATEMENT. This guarantee is what makes subgame solving 'safe':
│             the resolved strategy cannot be more exploitable than the original 
│             blueprint. Critical for understanding how abstraction errors get 
│             fixed in practice."
└── KEY INSIGHT: "Abstraction creates errors. Subgame solving FIXES those errors 
    in real-time at specific game states. Together, 'abstract blueprint + 
    real-time subgame solving' is the architecture behind EVERY competitive 
    poker AI since 2017. Step 6 studies the full architectures that use this."
```

### Supplementary References

- **Li, W. et al. (2024) — "RL-CFR: A New RL Framework for Action Abstraction in Imperfect Information Extensive-Form Games"**  
  https://arxiv.org/abs/2403.14114  
  *Uses RL to learn action abstractions instead of hand-crafting them. Bridges Step 1 (RL) → Step 4 (abstraction). SKIM abstract + Section 3 (RL-CFR method). Log as potential enrichment for Steps 5–6.*

- **Fu, H. et al. (2025) — "No-Regret Strategy Optimization with KrwEmd Metric for Imperfect-Recall Abstraction" (AAAI 2026)**  
  https://arxiv.org/abs/2411.16111  
  *Frontier work on abstraction metrics. SKIM abstract only. Log for Step 15 (frontier mapping).*

### Math Flags

🔢 **Ordered Game Isomorphism (Gilpin & Sandholm, Definition 3)** — Must understand the formal definition.  
**WHY this can't be substituted:** This definition IS the criterion for lossless abstraction. If you can check whether a proposed grouping satisfies this definition, you know the abstraction preserves Nash equilibria. Without it, you're guessing.

🔢 **Earth Mover's Distance for abstraction quality (Johanson et al., Definition 1)** — Must understand the metric.  
**WHY:** EMD gives you a NUMBER for how much information your abstraction throws away. It's the quantitative tool for comparing abstractions, and you'll use it in your implementation (Phase 4).

🔢 **Subgame solving safety guarantee (Brown & Sandholm, Theorem 1)** — Read statement.  
**WHY:** This theorem is the bridge between "abstraction introduces errors" and "those errors don't kill you in practice." It's the safety net that makes the entire abstract-then-resolve pipeline trustworthy. Feeds directly into Step 8 (Safe Exploitation).

---

## Phase 4: Implementation (6 days)

### Project: Abstraction Pipeline for Leduc & Extended Leduc — From Scratch

**Language + Framework:** Python 3.10+ / NumPy only (same constraint as Steps 2–3)

Starting point: Your Leduc Hold'em engine + MCCFR solver from Step 3.

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| Lossless abstraction module (suit isomorphism detection + GameShrink-style merger) | 🔴 HAND-CODE | This is the core contribution of this step. You must be able to identify when two info sets are strategically equivalent and merge them correctly. The merge logic must preserve the game structure. |
| Lossy card bucketing module (k-means on hand features → card buckets) | 🔴 HAND-CODE | You need to understand how card bucketing works — choosing features (hand strength, potential, board interaction), the clustering step, and mapping info sets to bucket IDs. This is what every poker AI uses. |
| Action abstraction module (restrict bet sizes to a fixed set + action translation) | 🔴 HAND-CODE | Action translation is the tricky part: when an opponent plays a bet that's not in your abstraction, how do you map it to the nearest abstract action? This mapping introduces systematic error that you must understand. |
| Extended Leduc variant (4 ranks, 2 suits → 8 cards, allowing multiple bet sizes) | 🟡 AI-ASSISTED | Extension of your Step 3 Leduc engine. The game logic follows the same pattern, just larger. AI drafts the extension, you verify the game tree is correct. |
| Abstraction quality evaluation (exploitability of abstract strategy in full game) | 🔴 HAND-CODE | Computing exploitability in the full game after translating back from the abstract game is the key diagnostic. You must own this computation — it's the metric that judges your abstraction. |
| Convergence + comparison framework | 🟢 AI-GENERATED | Run configurations, store results, generate plots. |
| Plotting (abstraction size vs strategy quality, convergence curves) | 🟢 AI-GENERATED | Matplotlib visualizations. |

### Sub-phase Breakdown (6 days):

**Day 1 — Lossless Abstraction on Leduc:**
- 🔴 Implement suit isomorphism detection:
  - For each info set, check: can swapping suits produce an identical strategic situation?
  - If yes, merge the info sets into a single abstract info set
  - Example: In Leduc, J♠ vs community Q♠ is strategically identical to J♥ vs community Q♥ → merge
- Run MCCFR on the abstracted game
- Verify: same Nash equilibrium, fewer info sets (~468 instead of ~936)
- *This is the "freebie" — lossless abstraction costs nothing strategically but halves memory*

**Day 2 — Lossy Card Bucketing:**
- 🔴 Implement hand-strength-based card bucketing:
  - Feature: hand strength = probability of winning against a random opponent hand given the current board
  - Compute hand strength for every possible (hand, board) combination in Leduc
  - Cluster into k buckets using k-means (try k = 2, 3, 5, "full")
  - Map each info set to its bucket
- Run MCCFR on each abstraction granularity
- Compare: exploitability of abstract-then-translate strategy vs exact Nash
- Expected: k=5 ≈ near-exact; k=2 = noticeably exploitable

**Day 3 — Action Abstraction + Action Translation:**
- 🔴 Extend Leduc with variable bet sizing (half-pot, pot, 2×pot, all-in)
- 🔴 Implement action abstraction: restrict to {fold, call, pot-bet}
- 🔴 Implement action translation for unmapped bets:
  - When opponent bets 0.5×pot but your abstraction only has "pot": allocate probability to nearest abstract actions proportionally
  - Test two strategies: (a) map to nearest abstract action, (b) split probability between two nearest
  - Compare exploitability of both translation methods
- *This is the hardest/most subtle part — action translation errors are where practical poker AIs lose the most equity*

**Day 4 — Extended Leduc + Combined Abstraction:**
- 🟡 AI-ASSISTED: Build Extended Leduc (4 ranks: J, Q, K, A; 2 suits each → 8 cards, but still 2 rounds)
  - This creates ~5000+ info sets — large enough that unabstracted MCCFR is slow
- 🔴 Apply both card bucketing (k=3 buckets) + suit isomorphism simultaneously
- 🔴 Apply action abstraction on top
- Run MCCFR on the triple-abstracted game
- Measure: total info set reduction ratio and strategy quality degradation

**Day 5 — Abstraction Quality Evaluation:**
- 🔴 Implement abstraction quality metrics:
  - Exploitability gap: `exploit(abstract_strategy, full_game) - exploit(Nash, full_game)`
  - If you implemented EMD from the Johanson et al. paper: measure EMD between abstract and full-game distributions
  - Create a graph: **abstraction size (number of info sets) vs strategy quality (exploitability)**
  - *This is the key deliverable — the Pareto frontier of abstraction*
- Compare all abstraction configurations:
  | Config | Info Sets | Exploitability | Solve Time |
  |--------|-----------|---------------|------------|
  | No abstraction | ~5000+ | baseline (Nash) | slow |
  | Suit isomorphism only | ~2500 | = Nash (lossless) | 2x faster |
  | 5 card buckets + suits | ~500 | slight degradation | 10x faster |
  | 3 card buckets + action abstract | ~200 | moderate degradation | 25x faster |
  | 2 card buckets + action abstract | ~100 | significant degradation | 50x faster |

**Day 6 — Cross-Validation + Documentation:**
- Cross-validate your Leduc abstractions against OpenSpiel (run OpenSpiel's CFR on the same abstract games, compare strategies)
- Optionally: skim the Libratus Science paper (Brown & Sandholm 2017) architecture diagram — identify where abstraction and subgame solving fit. *Don't go deep — that's Step 6. Just identify the components.*
- Document the tradeoff results
- Write all deliverables

### Deliverables:
- [ ] Lossless abstraction module (suit isomorphism) working on Leduc
- [ ] Lossy card bucketing module with configurable k
- [ ] Action abstraction module with action translation
- [ ] Extended Leduc Hold'em variant (4 ranks, 2 suits)
- [ ] Combined abstraction pipeline (card bucketing + suit isomorphism + action abstraction)
- [ ] Abstraction quality evaluation: exploitability gap per configuration
- [ ] Pareto frontier plot: abstraction size vs strategy quality
- [ ] All code committed with README

### Validation:
- **Lossless abstraction on Leduc:** Nash equilibrium must be IDENTICAL to unabstracted Leduc (zero exploitability gap). Info set count should halve.
- **Lossy card bucketing:** Exploitability should monotonically decrease as k increases (finer buckets → better strategy). At k = "full" (no bucketing), exploitability should match exact Nash.
- **Action abstraction:** Exploitability gap should be positive (abstraction always hurts at least a little for lossy) but bounded. Both translation methods should produce playable strategies.
- **Cross-validation:** Your abstracted-game Nash strategies should agree with OpenSpiel's to within 5% on strategy probabilities at matched info sets.

---

## Phase 5: Consolidation (2 days)

### Day 1 — Reference Skim + Architecture Preview

- **Reference skim (paper):** Brown & Sandholm "Superhuman AI for Multiplayer Poker" (Pluribus, Science 2019) — read Section 2 (Methods) only. Identify: where does card abstraction happen? Where does action abstraction happen? How does subgame solving interact with the abstract blueprint?  
  *This is a PREVIEW for Step 6 — don't go deep. Just map the architecture components to what you've built in this step.*

- **Reference skim (supplementary):** Li et al. (2024) "RL-CFR" — read abstract + Section 3. Note the idea of using RL to learn abstractions rather than hand-crafting them.  
  *Forward connection: In your thesis, could the opponent modeling framework (Step 7) inform adaptive abstraction? Log this as a PhD open question.*

- **Reference skim (supplementary):** Fu et al. (2025) "KrwEmd" — read abstract only. Note the new abstraction metric.  
  *Frontier logging: Could this replace EMD as the standard abstraction quality metric? Log for Step 15.*

- Review: any components of your implementation you don't fully understand?

### Day 2 — One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 2] Vanilla CFR computes Nash on the full game tree → [Step 4] Abstraction shrinks that tree so CFR/MCCFR can handle larger games. Abstraction is the SCALING mechanism that makes Steps 2–3 algorithms practical.
    - [Step 3] MCCFR reduces per-iteration cost via sampling → [Step 4] Abstraction reduces the total game tree size. These are ORTHOGONAL scaling techniques that compose: abstract game + MCCFR = both dimensions compressed.
    - [Step 1] Policy improvement (Sutton & Barto Ch 4) iterates between evaluation and improvement → [Step 4] Subgame solving iterates between blueprint (abstract) and refinement (real-time). Same iterate-and-refine pattern.
    - [Step 4] Action translation = mapping unseen actions to known abstractions → prediction: [Step 7] Opponent modeling will need similar "map unseen behavior to known types" logic.
    - [Step 4] Abstraction quality → Step 5 replaces hand-crafted abstraction with neural approximation (Deep CFR). The progression: hand-craft (Step 4) → learn (Step 5) → integrate (Step 6).
  - **Confusions:**
    - [Step 4] Action translation: nearest-action vs probability-split mapping — which is theoretically better? The papers don't give a clear answer. → OPEN (may be addressed in Brown & Sandholm 2017 subgame solving paper)
    - [Step 4] Imperfect-recall abstraction requires forgetting past information. How do you decide WHAT to forget? Kroer & Sandholm give bounds, but the design space is huge. → OPEN (possibly resolved in Step 6 or Step 15 frontier)
    - [Step 3→4] MCCFR on an abstracted game: does sampling interact badly with abstraction? (Variance from sampling + error from abstraction — do they compound?) → OPEN (check during Step 5)

## Exit Checklist

- [ ] Lossless abstraction (suit isomorphism) produces identical Nash on Leduc
- [ ] Lossy card bucketing produces strategies with measurable quality degradation as k decreases
- [ ] Action abstraction + action translation pipeline working end-to-end
- [ ] Extended Leduc variant working with ~5000+ info sets
- [ ] Combined abstraction pipeline tested on Extended Leduc
- [ ] Pareto frontier plot: abstraction size vs exploitability gap
- [ ] Can explain from memory: lossless vs lossy abstraction and when each is appropriate
- [ ] Can explain from memory: action translation problem and its solutions
- [ ] Can explain from memory: subgame solving's role in fixing abstraction errors (Brown & Sandholm)
- [ ] Cross-validated against OpenSpiel implementations
- [ ] All 🔴 components hand-coded
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Steps 1–3 + new confusions + resolved confusions)
- [ ] Step notes committed to repo
