# Step 2 — Game Theory + CFR Basics

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 1 (RL Basics)  
**Phase:** A — Foundation  

### PhD Connection

This step feeds **all three thesis contributions** at the foundational level:
- **Contribution #1 (Behavioral Adaptation Framework):** CFR's information-set decomposition is the basis for computing counter-strategies against observed behavior.
- **Contribution #2 (Multi-Agent Safe Exploitation):** Safe exploitation (Step 8) is defined as deviation from Nash equilibrium — you must first understand Nash computation via CFR to understand what you're deviating FROM.
- **Contribution #3 (Evaluation Methodology):** Exploitability (computed via best response) is the primary evaluation metric for your thesis. You implemented it from scratch in this step.

> **[P6] Sequence-form reading pointer:** When reviewing Step 2 material during Step 8, revisit Shoham & Leyton-Brown Chapter 4 on sequence-form representation. The sequence-form is the mathematical backbone of all LP-based equilibrium and exploitation computation used in Step 8.

---

## Table of Contents
- [Phase 1: Intuition (1 day)](#phase-1-intuition-1-day)
  - [Videos](#videos)
  - [Blog Posts](#blog-posts)
- [Phase 2: Exploration (2 days)](#phase-2-exploration-2-days)
  - [Day 1: Play Games + Understand Game Trees](#day-1-play-games-understand-game-trees)
  - [Day 2: CFR Convergence + Regret Matching](#day-2-cfr-convergence-regret-matching)
- [Phase 3: Targeted Reading (3 days)](#phase-3-targeted-reading-3-days)
  - [Core Reading: Neller & Lanctot — "An Introduction to Counterfactual Regret Minimization" (2013)](#core-reading-neller-lanctot-an-introduction-to-counterfactual-regret-minimization-2013)
  - [Book Chapters: Shoham & Leyton-Brown — "Multiagent Systems" (2008)](#book-chapters-shoham-leyton-brown-multiagent-systems-2008)
  - [Paper 1: Zinkevich et al. — "Regret Minimization in Games with Incomplete Information" (2007)](#paper-1-zinkevich-et-al-regret-minimization-in-games-with-incomplete-information-2007)
  - [Math Flags](#math-flags)
- [Phase 4: Implementation (6 days)](#phase-4-implementation-6-days)
  - [Project: Vanilla CFR for Kuhn Poker — From Scratch](#project-vanilla-cfr-for-kuhn-poker-from-scratch)
  - [Sub-phase Breakdown (6 days):](#sub-phase-breakdown-6-days)
  - [Deliverables:](#deliverables)
  - [Validation:](#validation)
- [Phase 5: Consolidation (2 days)](#phase-5-consolidation-2-days)
  - [Day 1 — Reference Skim + Gap Fill](#day-1-reference-skim-gap-fill)
  - [Day 2 — One-Pager + Learning Log](#day-2-one-pager-learning-log)
- [Exit Checklist](#exit-checklist)

## Phase 1: Intuition (1 day)

The goal: understand what game theory IS, why Nash equilibrium matters, what an extensive-form game looks like, and why CFR was invented. NO math, NO code — just build the mental model.

### Videos

- [**Game Theory 101 (#1): Introduction**](https://www.youtube.com/watch?v=NSVmOC_5zrE)
  *Clean primer on normal-form games, dominant strategies, Nash equilibrium. Perfect starting point if game theory is new.*

- [**The Prisoner's Dilemma**](https://www.youtube.com/watch?v=t9Lo2fgxWHw)
  *The classic game theory example. Builds intuition for why rational agents can end up at suboptimal outcomes — and why equilibrium concepts matter.*

- [**Stanford CS221 — Lecture 10: Games I (Autumn 2025)**](https://www.youtube.com/watch?v=SMOD_GiRzb8)
  *University lecture covering game trees, minimax, alpha-beta pruning, and evaluation functions. The formal framework for two-player games that CFR operates on.*

- [**Poker AI: Libratus and an Introduction to Counterfactual Regret Minimization**](https://www.youtube.com/watch?v=htRtfyab-Ns)
  *Concise intro to CFR with a Rock-Paper-Scissors worked example. Explains regret matching, convergence to Nash equilibrium, and how Libratus used CFR to beat top poker pros.*

- [**Noam Brown — AI for Imperfect-Information Games: Poker and Beyond**](https://www.youtube.com/watch?v=cn8Sld4xQjg)
  *Comprehensive talk covering the journey from game theory basics to superhuman poker AI. Covers CFR, abstraction, subgame solving, and why imperfect information is fundamentally harder than chess/Go.*

### Blog Posts

- **LessWrong / Arbital — "Nash Equilibrium"**  
  https://arbital.com/p/nash_equilibrium/  
  *Accessible explanation of Nash equilibrium without heavy notation.*

- **Tim Roughgarden — "Algorithmic Game Theory" (Stanford lecture notes overview)**  
  http://timroughgarden.org/f13/f13.html  
  *Lecture notes index — skim the titles for a roadmap of the field. Don't read the PDFs yet.*

---

## Phase 2: Exploration (2 days)

### 🎮 Interactive Exploration
- **[The Evolution of Trust](https://ncase.me/trust/)** — An interactive guide to the game theory of trust, iterated prisoner's dilemmas, and equilibria.
- **[Game Theory Explorer](http://gametheoryexplorer.org/)** — Build normal-form and extensive-form games and computationally solve for their Nash Equilibria in your browser.


No reading yet. Run existing CFR solvers, play games, see convergence happen.

### Day 1: Play Games + Understand Game Trees

1. **Play Kuhn Poker by hand (15 min):**
   - Rules: 3 cards (J, Q, K), 2 players, 1 round. Deal one card each. Player 1: bet or check. If check → Player 2: bet or check. If bet → opponent: call or fold.
   - Play 20 hands against yourself on paper. Track your intuitive strategy. Note: with only 3 cards, you should start sensing the optimal strategy (bet K, sometimes bluff J, check-call Q).
   - *This creates the intuition for what the CFR algorithm will compute formally.*

2. **Visualize the Kuhn Poker game tree:**
   - Draw the full game tree by hand. It has ~30 terminal nodes. Label each node with: player, information set, actions.
   - Resources for verification: Neller & Lanctot Figure 1 (you'll read this paper in Phase 3, but peek at the figure now).

3. **Install OpenSpiel and run their CFR on Kuhn:**
   ```bash
   pip install open_spiel
   ```
   ```python
   import pyspiel
   from open_spiel.python.algorithms import cfr
   
   game = pyspiel.load_game("kuhn_poker")
   cfr_solver = cfr.CFRSolver(game)
   
   for i in range(10000):
       cfr_solver.evaluate_and_update_policy()
   
   # Get the average policy (Nash equilibrium approximation)
   average_policy = cfr_solver.average_policy()
   
   # Print strategy at each information set
   from open_spiel.python.algorithms import expected_game_score
   print("Nash equilibrium strategies:")
   for state in average_policy.states_per_player[0]:
       print(f"  Info set: {state}, policy: {average_policy.policy_for_key(state)}")
   ```
   *Observe: after ~1000 iterations, the strategy stabilizes. Compare against the known Nash equilibrium for Kuhn (Player 1 bets K always, bluffs J with probability 1/3, checks Q always).*

4. **Explore OpenSpiel's game catalog:**
   ```python
   # List all available games
   print(pyspiel.registered_names())
   
   # Try a normal-form game
   game = pyspiel.load_game_as_turn_based("matrix_rps")  # Rock-Paper-Scissors
   state = game.new_initial_state()
   print(state)
   ```

### Day 2: CFR Convergence + Regret Matching

1. **Run CFR on Kuhn with different iteration counts, observe convergence:**
   ```python
   import matplotlib.pyplot as plt
   
   game = pyspiel.load_game("kuhn_poker")
   exploitabilities = []
   iterations = [10, 50, 100, 500, 1000, 5000, 10000]
   
   for n_iter in iterations:
       solver = cfr.CFRSolver(game)
       for _ in range(n_iter):
           solver.evaluate_and_update_policy()
       
       from open_spiel.python.algorithms import exploitability as expl
       avg_policy = solver.average_policy()
       exploit = expl.exploitability(game, avg_policy)
       exploitabilities.append(exploit)
       print(f"Iterations: {n_iter}, Exploitability: {exploit:.6f}")
   
   plt.plot(iterations, exploitabilities, 'bo-')
   plt.xscale('log')
   plt.yscale('log')
   plt.xlabel('CFR Iterations')
   plt.ylabel('Exploitability')
   plt.title('CFR Convergence on Kuhn Poker')
   plt.savefig('cfr_convergence.png')
   plt.show()
   ```
   *Key observation: exploitability decreases as O(1/√T). This convergence rate is fundamental to the theory.*

2. **Implement regret matching for Rock-Paper-Scissors (simple standalone):**
   ```python
   import numpy as np
   
   # Regret matching for RPS — the building block of CFR
   cumulative_regret = np.zeros(3)  # [Rock, Paper, Scissors]
   strategy_sum = np.zeros(3)
   
   def get_strategy(regret):
       positive = np.maximum(regret, 0)
       total = positive.sum()
       if total > 0:
           return positive / total
       return np.ones(3) / 3  # uniform if no positive regret
   
   # Self-play: 10000 rounds
   for _ in range(10000):
       strategy = get_strategy(cumulative_regret)
       strategy_sum += strategy
       # Opponent plays uniform
       opp_strategy = np.array([1/3, 1/3, 1/3])
       # ... compute action utilities and regret updates
   ```
   *This is not a complete implementation — you'll build the full thing in Phase 4. The point is to see regret matching converge to 1/3, 1/3, 1/3 (the Nash equilibrium of RPS).*

3. **Questions to answer by end of Day 2:**
   - What is an information set, and why is it different from a game state?
   - What does "exploitability" measure, and why is it the right metric?
   - Why does CFR converge for 2-player zero-sum games?
   - How does the OpenSpiel CFR output compare to the known Kuhn Nash equilibrium?

---

## Phase 3: Targeted Reading (3 days)

### Core Reading: Neller & Lanctot — "An Introduction to Counterfactual Regret Minimization" (2013)

http://modelai.gettysburg.edu/2013/cfr/cfr.pdf  
**Length:** ~30 pages  
**This is the single most important reading for Step 2.** Read it front-to-back — it's a tutorial, not a research paper. It's specifically designed to teach CFR from scratch.

```
├── READ:  The ENTIRE document. It's only 30 pages and every page matters.
│          - Section 1: Rock-Paper-Scissors example (regret matching)
│          - Section 2: Regret matching convergence
│          - Section 3: Extensive-form games (notation you'll use for the rest of the PhD)
│          - Section 4: Kuhn Poker CFR walkthrough (the algorithm step-by-step)
│          - Section 5: Implementation details
├── SKIM:  Nothing — read it all
├── SKIP:  Nothing
├── MATH:  → "Theorem 1 (regret matching convergence) — read the statement and
│             understand what it guarantees: average strategy converges to a
│             correlated equilibrium. The PROOF can be skimmed — understand the
│             bound O(√T) on average regret, not the full derivation."
│          → "Theorem 4 (CFR convergence for extensive-form games) — read the
│             statement: average strategy converges to Nash equilibrium in 2-player
│             zero-sum games. WHY this matters: this is the guarantee your
│             implementations rely on. Skim the proof for intuition only."
└── KEY INSIGHT: "CFR decomposes a game-wide learning problem into per-information-set
    regret matching. Each information set independently minimizes its own regret,
    and the magic of the decomposition theorem guarantees that the overall strategy
    converges to Nash equilibrium. That decomposition is what makes CFR tractable."
```

### Book Chapters: Shoham & Leyton-Brown — "Multiagent Systems" (2008)

**Link:** https://www.masfoundations.org/download.html (free PDF available)  
**Assigned chapters:** 3, 4, 6  
**Context — what comes before (Ch 1–2):** Introduction to multi-agent systems and distributed AI. Sets up the framing of agents interacting in shared environments. *Skim Ch 1 if you want context (~15 min), skip Ch 2.*  
**Context — what comes after (Ch 7+):** Ch 7 covers learning in games (connects to MARL in Step 9). Ch 8+ covers mechanism design, auctions, social choice — not relevant for this PhD track.  
**Reading focus:**
- **Ch 3 (read carefully, ~2 hrs):** Introduction to game theory. Normal-form games, strategy profiles, best responses. This is the vocabulary.
- **Ch 4 (read 4.1–4.3 carefully, skim rest, ~2 hrs):** Solution concepts. Nash equilibrium definition, mixed strategies, existence theorem. *The Nash existence proof (Theorem 4.1.3) is important to know EXISTS but you don't need to reproduce it — treat it as: "Nash proved that every finite game has at least one mixed-strategy equilibrium."*
- **Ch 6 (read carefully, ~3 hrs):** Extensive-form games. This is the critical chapter: game trees, information sets, perfect vs imperfect information, subgame perfect equilibrium, behavioural strategies. *This notation directly transfers to CFR and every paper you'll read in Steps 3–8.*

### Paper 1: Zinkevich et al. — "Regret Minimization in Games with Incomplete Information" (2007)

https://arxiv.org/abs/0709.2092  
*The original CFR paper. You DON'T need to read this front-to-back — Neller & Lanctot covers the same material more accessibly. Use this paper as a reference.*

```
├── READ:  Section 3 (Counterfactual Regret — the formal definition),
│          Section 4 (the main theorem and algorithm)
├── SKIM:  Abstract, Section 1 (motivation), Section 5 (Kuhn poker experiments)
├── SKIP:  Section 2 (standard game theory background — you have this from S&LB),
│          Section 6 (Rhode Island Hold'em — a game you won't use)
├── MATH:  → "Theorem 3 (CFR convergence bound) — this is the formal version of
│             what Neller & Lanctot present informally. Read the STATEMENT to
│             understand the bound: average overall regret after T iterations is
│             O(Δ√(|I|/T)) where |I| is the number of information sets and Δ is
│             the range of utilities. Skim the proof for structure only."
└── KEY INSIGHT: "The key insight is 'counterfactual' — CFR computes the regret at
    each information set by imagining 'what if I had played differently, but
    everything else stayed the same?' This counterfactual value decomposition is
    what makes per-info-set regret minimization equivalent to game-wide convergence."
```

### Math Flags

🔢 **Regret Matching convergence (Neller & Lanctot, Theorem 1)** — Read the statement and understand the O(√T) bound on average regret.  
**WHY this can't be substituted by algorithmic understanding:** You need to know that CFR's convergence rate is O(1/√T) because in Step 3 you'll learn CFR+ which achieves O(1/T) — understanding the baseline bound is necessary to appreciate the improvement.

🔢 **Nash Equilibrium existence (Shoham & Leyton-Brown, Theorem 4.1.3)** — Read the statement only.  
**WHY:** You need to know that Nash equilibria always exist in finite games (it's a foundational fact your thesis will cite), but the fixed-point proof itself won't reappear in your work.

🔢 **Counterfactual value decomposition (Zinkevich et al., Theorem 3)** — Read the statement and the bound.  
**WHY:** This bound reappears in every CFR variant paper. Knowing the structure of the bound (what depends on |I|, what depends on T) will help you read CFR+ and MCCFR papers much faster.

---

## Phase 4: Implementation (6 days)

### Project: Vanilla CFR for Kuhn Poker — From Scratch

**Language + Framework:** Python 3.10+ / NumPy only (no PyTorch, no game libraries)  
**Why no libraries:** This is the most educational implementation in the entire plan. Building the game tree traversal, information set mapping, and regret accumulation from scratch is how you internalize the algorithm.

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| Kuhn Poker game engine (card dealing, action legality, payoff computation) | 🔴 HAND-CODE | The game tree structure IS the algorithm's input. You must understand every branch. Small enough to code by hand (~100 lines). |
| CFR recursive tree traversal (walk the game tree, compute counterfactual values) | 🔴 HAND-CODE | This IS the thesis algorithm. The recursive computation of counterfactual values at each information set, the reach probability factoring — this is the core of CFR. Every bug you fix teaches you the algorithm. |
| Regret matching (convert cumulative regrets to strategy) | 🔴 HAND-CODE | ~15 lines but critical. Must understand: clip negative regrets, normalize, fallback to uniform. |
| Strategy accumulation (accumulate weighted strategies for average) | 🔴 HAND-CODE | The AVERAGE strategy converges to Nash, not the current strategy. Getting this wrong is a common bug — hand-coding forces you to understand the distinction. |
| Exploitability computation (best response calculation) | 🔴 HAND-CODE | This is your validation metric. Computing a best response against a fixed strategy teaches you exactly what exploitability measures. |
| Convergence plotting + visualization | 🟢 AI-GENERATED | Matplotlib code to plot exploitability vs iterations, strategy evolution over time. |
| Nash equilibrium verification (compare with known analytical solution) | 🟡 AI-ASSISTED | The analytical Nash for Kuhn is known — AI can help set up the comparison, you verify correctness. |

### Sub-phase Breakdown (6 days):

**Day 1 — Architecture + Game Engine:**
- Design the code structure: `kuhn_poker.py` (game engine), `cfr.py` (algorithm), `evaluate.py` (exploitability), `main.py` (training loop + plots)
- 🔴 Implement Kuhn Poker game engine:
  - Card representation: J=0, Q=1, K=2
  - Game state: (player_card, opponent_card, history_string)
  - Information set: (player_card, history_string) — note: opponent card is HIDDEN
  - Terminal state payoff computation
  - Test: enumerate all 12 possible deals × all action sequences = verify correct game tree structure

**Days 2–3 — CFR Core Algorithm:**
- 🔴 Implement the CFR recursive traversal:
  ```
  function cfr(state, reach_probabilities):
      if terminal(state): return payoff
      info_set = get_info_set(state)
      strategy = regret_match(cumulative_regrets[info_set])
      action_values = {}
      for each action:
          next_state = apply(state, action)
          action_values[action] = -cfr(next_state, updated_reaches)  # note the negation for zero-sum
      node_value = sum(strategy[a] * action_values[a] for a in actions)
      for each action:
          regret = action_values[action] - node_value
          cumulative_regrets[info_set][action] += opponent_reach * regret
      strategy_sum[info_set] += player_reach * strategy
      return node_value
  ```
- 🔴 Implement regret matching: `positive_regret / sum(positive_regret)`, fallback to uniform
- 🔴 Implement strategy accumulation: weight by reach probability for the current player
- Train for 10,000 iterations. Print strategies at each information set.
- Verify against known Kuhn Nash equilibrium:
  - Player 1 with J: bet 1/3 (bluff), check-fold 2/3
  - Player 1 with Q: always check, call if bet
  - Player 1 with K: always bet
  - (Player 2 has corresponding optimal response)

**Days 4–5 — Exploitability + Best Response:**
- 🔴 Implement best response computation:
  - Given a fixed opponent strategy, compute the best response for each information set
  - Best response = pure strategy that maximizes expected value at each info set
  - This involves its own tree traversal (similar to CFR but choosing max instead of weighted average)
- 🔴 Implement exploitability:
  - exploitability(σ) = BR₁(σ₂) + BR₂(σ₁) — sum of both players' best response values
  - At Nash equilibrium, exploitability = 0
- Plot exploitability vs CFR iterations (log-log scale). Verify O(1/√T) convergence rate.
- Run CFR for [100, 500, 1000, 5000, 10000, 50000] iterations, plot the curve.

**Day 6 — Validation + Comparison:**
- Compare your strategy outputs with OpenSpiel's CFR outputs for Kuhn (from Phase 2)
- Verify numerical match within floating-point tolerance (strategies should agree to ~4 decimal places at 50k iterations)
- Compare exploitability curves: your implementation vs OpenSpiel
- 🟡 AI-ASSISTED: Generate a table comparing your Nash strategies vs the known analytical solution for every information set
- Document: common bugs encountered (off-by-one in reach probability, forgetting to negate payoffs for player 2, strategy sum vs current strategy confusion)

### Deliverables:
- [ ] Kuhn Poker game engine (fully tested, handles all card deals and action sequences)
- [ ] Vanilla CFR solver converging to Nash equilibrium on Kuhn Poker
- [ ] Best response + exploitability calculation
- [ ] Convergence plot: exploitability vs iterations (log-log), demonstrating O(1/√T) rate
- [ ] Strategy comparison: your CFR output vs known analytical Nash equilibrium
- [ ] Strategy comparison: your CFR output vs OpenSpiel's CFR output
- [ ] All code committed with clear README

### Validation:
- **Correctness:** Strategies at 50k iterations should match the known Kuhn Nash equilibrium to ~4 decimal places. Specifically: P1 bet frequency with J ≈ 0.333, P1 bet frequency with K ≈ 1.0, P1 bet frequency with Q ≈ 0.0.
- **Convergence rate:** On log-log plot, exploitability vs iterations should show a slope of approximately -0.5 (confirming O(1/√T)).
- **Cross-validation:** Your exploitability values at [100, 1000, 10000] iterations should be within 10% of OpenSpiel's values.
- **Sanity check:** Game value (expected payoff for Player 1 at Nash) should be approximately -1/18 ≈ -0.0556.

---

## Phase 5: Consolidation (2 days)

### Day 1 — Reference Skim + Gap Fill

- **Reference skim:** Shoham & Leyton-Brown Ch 7 (Learning in games) — NOT to learn deeply, but to see how regret-based learning fits into the broader landscape of learning algorithms for games. This connects to Steps 9 (MARL) and 10 (population-based training).
- **Optional skim:** Zinkevich et al. (2007) Sections 5–6 for the Rhode Island Hold'em experiments — this gives a preview of what larger games look like before you scale to Leduc in Step 3.
- Review your Phase 4 code: can you trace through the CFR recursion by hand for a 2-card, 1-action subtree? If not, do it now.

### Day 2 — One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 1] Q-learning updates at each state → [Step 2] CFR updates at each information set. Same idea: local regret minimization → global convergence.
    - [Step 1] Experience replay (DQN) stores transitions → [Step 2] Strategy sum accumulates weighted strategies over time. Both are "memory" mechanisms that stabilize learning.
    - [Step 2] Vanilla CFR traverses the full game tree → [Step 3] MCCFR samples paths (Monte Carlo). Same relationship as: dynamic programming (full sweep) → Monte Carlo methods (sampling).
  - **Confusions:** Common open questions for Step 2:
    - "Why does the AVERAGE strategy converge to Nash, but the CURRENT strategy doesn't?"
    - "CFR is proven for 2-player zero-sum — what happens in N-player or general-sum games?" → Flag for Step 9/11
    - "How does CFR handle games much larger than Kuhn where you can't traverse the full tree?" → This is exactly Step 3 (MCCFR)

## Exit Checklist

- [ ] Vanilla CFR solving Kuhn Poker — strategies match known Nash equilibrium (P1 J-bet ≈ 0.333, K-bet ≈ 1.0, Q-bet ≈ 0.0)
- [ ] Exploitability converges at O(1/√T) — verified on log-log plot
- [ ] Game value ≈ -1/18 for Player 1
- [ ] Cross-validated against OpenSpiel's CFR implementation
- [ ] Can explain from memory: What is an information set? How does CFR decompose the game? Why does the average strategy converge?
- [ ] Can trace CFR recursion by hand on a small game tree (whiteboard test)
- [ ] Can explain: What is exploitability? How is best response computed?
- [ ] Can explain WHY CFR works for 2-player zero-sum but not directly for N-player games
- [ ] All 🔴 components hand-coded — no AI-generated game engine or CFR algorithm code
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Step 1 + new confusions)
- [ ] Step notes committed to repo
