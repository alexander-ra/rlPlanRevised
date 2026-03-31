# Step 3 — CFR Variants + Monte Carlo Methods

**Duration:** 10 days (Tier 2 — compressed)  
**Dependencies:** Step 2 (Game Theory + CFR Basics)  
**Phase:** B — Scaling the Toolbox

> **Know-How First compression:** Implementation phase cut from 6d to 3d. Build one MC-CFR variant (External Sampling) to working correctness on Kuhn and Leduc. Defer polished multi-variant comparison (Outcome Sampling, Robust Sampling) to implementation phase post-November. All reading and intuition phases unchanged.
> Phase allocation: Intuition 1d | Exploration 1d | Reading 3d | Implementation **3d** | Consolidation 2d  
**Freshness Note:**  
- ArXiv search: "counterfactual regret minimization" sorted by date (Mar 2026) — 99 results total  
- ArXiv search: "monte carlo sampling regret extensive games" (Mar 2026)  
- Core resources unchanged: Lanctot et al. (2009) MCCFR, Tammelin et al. (2015) CFR+ remain the standard references  
- Notable recent papers logged but belong to later steps: Xu et al. "Deep Predictive Discounted CFR" (AAAI 2026, → Step 5), Zhang et al. "Faster Game Solving via Hyperparameter Schedules" (AAAI 2026, → Step 5/6), Li et al. "RL-CFR" (Mar 2024, → Step 4 action abstraction)  
- VR-MCCFR (Schmid et al., 2018) added as supplementary — variance reduction for MCCFR, bridges to Deep CFR in Step 5  
- No superseded content for Step 3 scope

---

> **Phase Overview:** Phase A established a working CFR solver on the minimal Kuhn Poker benchmark, but vanilla CFR requires a full traversal of the game tree on every iteration — an approach that becomes infeasible as games grow. This phase will introduce two complementary scaling mechanisms: Monte Carlo sampling methods that reduce per-iteration cost, and game abstraction techniques that reduce the game tree itself. These tools are needed to bridge the gap between toy benchmarks and the medium-scale games on which later thesis work will be developed.
>
> **Contribution Alignment:** Monte Carlo CFR variants will provide the computationally tractable equilibrium computation needed for medium-scale games, which will underpin the empirical work in later contributions. CFR+ accelerates convergence, enabling equilibrium computation for games beyond the reach of vanilla CFR.


## Table of Contents
- [Phase 1: Intuition (1 day)](#phase-1-intuition-1-day)
  - [Videos](#videos)
  - [Blog Posts](#blog-posts)
- [Phase 2: Exploration (2 days)](#phase-2-exploration-2-days)
  - [Day 1: MCCFR in OpenSpiel — Different Sampling Schemes](#day-1-mccfr-in-openspiel-different-sampling-schemes)
  - [Day 2: CFR+ and Convergence Comparison](#day-2-cfr-and-convergence-comparison)
- [Phase 3: Targeted Reading (3 days)](#phase-3-targeted-reading-3-days)
  - [Paper 1: Lanctot et al. — "Monte Carlo Sampling for Regret Minimization in Extensive Games" (2009)](#paper-1-lanctot-et-al-monte-carlo-sampling-for-regret-minimization-in-extensive-games-2009)
  - [Paper 2: Tammelin et al. — "Solving Heads-Up Limit Texas Hold'em" (2015)](#paper-2-tammelin-et-al-solving-heads-up-limit-texas-holdem-2015)
  - [Paper 3: Zinkevich et al. (2007) — Revisit Section 5](#paper-3-zinkevich-et-al-2007-revisit-section-5)
  - [Book: Chen & Ankenman — "The Mathematics of Poker" (2006)](#book-chen-ankenman-the-mathematics-of-poker-2006)
  - [Optional Supplementary](#optional-supplementary)
  - [Math Flags](#math-flags)
- [Phase 4: Implementation (6 days)](#phase-4-implementation-6-days)
  - [Project: MCCFR for Leduc Hold'em + CFR+ for Kuhn/Leduc — From Scratch](#project-mccfr-for-leduc-holdem-cfr-for-kuhnleduc-from-scratch)
  - [Sub-phase Breakdown (6 days):](#sub-phase-breakdown-6-days)
  - [Deliverables:](#deliverables)
  - [Validation:](#validation)
- [Phase 5: Consolidation (2 days)](#phase-5-consolidation-2-days)
  - [Day 1 — Reference Skim + Gap Fill](#day-1-reference-skim-gap-fill)
  - [Day 2 — One-Pager + Learning Log](#day-2-one-pager-learning-log)
  - [PhD Connection](#phd-connection)
- [Exit Checklist](#exit-checklist)

## Phase 1: Intuition (1 day)

The goal: understand WHY vanilla CFR is too slow for large games, what Monte Carlo sampling does about it, and how CFR+ improved convergence. End of day: you should be able to explain to a non-expert: "Instead of walking every branch of the game tree every iteration, we sample a few branches — it's noisier, but we only need to update the sampled branches, which makes each iteration 1000x cheaper."

### Videos

- **Noam Brown — "Superhuman AI for Multiplayer Poker" (NeurIPS 2019)**  
  https://www.youtube.com/watch?v=p_n5fF8apiE  
  Duration: ~25m | Speaker: Noam Brown  
  *You bookmarked this in Step 2. NOW watch the section about blueprint computation (~5:00–12:00) — Brown explains why vanilla CFR can't handle Texas Hold'em and how MCCFR + abstraction solved Libratus/Pluribus.*

- **Marc Lanctot — "OpenSpiel: A Framework for Reinforcement Learning in Games"**  
  https://www.youtube.com/watch?v=b7bStIQovcY  
  Duration: ~45m | Speaker: Marc Lanctot (DeepMind/Google)  
  *Lanctot literally wrote the MCCFR paper. This talk covers the framework that implements all the CFR variants you'll study. Focus on the first 20 minutes for algorithm overview.*

- **Dustin Morrill — "CFR and its Variants" (AAAI 2020 Tutorial)**  
  https://www.youtube.com/watch?v=7L2sUGcOgh0  
  Duration: ~1h 30m | Speaker: Dustin Morrill (UAlberta/DeepMind)  
  *Detailed walkthrough of CFR, MCCFR (external/outcome/chance sampling), CFR+, Discounted CFR, Linear CFR. Watch at 1.25x. This is the best single video for this step.*

### Blog Posts

- **Martin Schmid — "Variance Reduction in MCCFR"**  
  https://arxiv.org/abs/1809.03057 (read abstract and introduction only — paper is for Phase 3)  
  *Quick context on why variance matters in MCCFR — motivates why you'll experiment with different sampling schemes.*

---

## Phase 2: Exploration (2 days)

### 🎮 Interactive Exploration
- **[Slumbot (CFR Poker AI)](https://www.slumbot.com/)** — Play Heads-Up Texas Hold'em against a top CFR-based bot to see its behavior and baseline performance.


### Day 1: MCCFR in OpenSpiel — Different Sampling Schemes

1. **Run MCCFR variants on Kuhn Poker via OpenSpiel:**
   ```python
   import pyspiel
   from open_spiel.python.algorithms import mccfr
   from open_spiel.python.algorithms import exploitability as expl
   
   game = pyspiel.load_game("kuhn_poker")
   
   # External sampling MCCFR
   es_solver = mccfr.ExternalSamplingSolver(game)
   for i in range(10000):
       es_solver.iteration()
   es_exploit = expl.exploitability(game, es_solver.average_policy())
   print(f"External sampling exploitability after 10k: {es_exploit:.6f}")
   
   # Outcome sampling MCCFR
   os_solver = mccfr.OutcomeSamplingSolver(game)
   for i in range(10000):
       os_solver.iteration()
   os_exploit = expl.exploitability(game, os_solver.average_policy())
   print(f"Outcome sampling exploitability after 10k: {os_exploit:.6f}")
   ```

2. **Compare convergence speed** — Run all three (vanilla CFR from Step 2, external sampling, outcome sampling) for [100, 500, 1000, 5000, 10000, 50000] iterations. Plot exploitability vs iterations AND exploitability vs wall-clock time.
   - *Key insight to observe: per-iteration, vanilla CFR converges faster (lower variance). Per second, MCCFR wins big because iterations are cheaper.*

3. **Explore Leduc Hold'em in OpenSpiel:**
   ```python
   game = pyspiel.load_game("leduc_poker")
   print(f"Game type: {game.get_type()}")
   print(f"Num distinct info sets: {game.num_distinct_action_histories()}")
   
   state = game.new_initial_state()
   print(state)
   # Explore the game tree — Leduc has ~936 information sets vs Kuhn's ~12
   ```
   *Observe: Leduc is ~80x larger than Kuhn. Vanilla CFR is already noticeably slower here. This motivates MCCFR.*

### Day 2: CFR+ and Convergence Comparison

1. **Run CFR+ on Kuhn and Leduc via OpenSpiel:**
   ```python
   from open_spiel.python.algorithms import cfr
   
   game = pyspiel.load_game("leduc_poker")
   
   # CFR+ solver
   cfr_plus_solver = cfr.CFRPlusSolver(game)
   for i in range(1000):
       cfr_plus_solver.evaluate_and_update_policy()
   exploit = expl.exploitability(game, cfr_plus_solver.average_policy())
   print(f"CFR+ exploitability after 1k: {exploit:.6f}")
   ```

2. **Head-to-head convergence comparison on Leduc:**
   - Run vanilla CFR, CFR+, external-sampling MCCFR all on Leduc for 5000 iterations
   - Plot exploitability vs iterations (log-log) for all three
   - *Expected result: CFR+ converges roughly as O(1/T) vs vanilla CFR's O(1/√T) — a dramatic improvement*

3. **Questions to answer by end of Day 2:**
   - What's the difference between external sampling, outcome sampling, and chance sampling?
   - Why is outcome sampling highest variance but cheapest per iteration?
   - What modification does CFR+ make to regret accumulation, and why does it help?
   - On Leduc, which algorithm reaches exploitability < 0.01 fastest (by wall time)?

---

## Phase 3: Targeted Reading (3 days)

### Paper 1: Lanctot et al. — "Monte Carlo Sampling for Regret Minimization in Extensive Games" (2009)

**Link:** https://papers.nips.cc/paper/2009/hash/00411460f7c92d2124a67ea0f4cb5f85-Abstract.html  
http://mlanctot.info/files/papers/nips09mccfr.pdf

```
├── READ:  Section 3 (MCCFR framework — the unifying theory for all sampling variants),
│          Section 4 (External sampling, outcome sampling, chance sampling — the
│          three concrete instantiations),
│          Section 5 (Experiments — convergence plots on poker variants)
├── SKIM:  Abstract, Section 1 (Introduction — framing the problem),
│          Section 2 (Background — you know this from Step 2)
├── SKIP:  Proofs in the appendix (unless you want deeper theory)
├── MATH:  → "Theorem 1 (Unbiased counterfactual value estimation under sampling) —
│             Read the STATEMENT. Key is: sampled counterfactual values are UNBIASED
│             estimates of the full-traversal counterfactual values. This is why
│             MCCFR converges to the same answer as vanilla CFR despite sampling.
│             Skim the proof structure only."
│          → "Corollary 1 (Convergence rate of external sampling) — note that the
│             bound is the same O(1/√T) as vanilla CFR but with a different constant.
│             The constant involves the number of actions |A| — bigger action spaces
│             mean more variance."
└── KEY INSIGHT: "MCCFR is not a different algorithm — it's the SAME algorithm
    (CFR) applied to SAMPLED game tree blocks. External sampling visits all of
    the traversing player's actions but samples the opponent's; outcome sampling
    samples everything but requires importance-weighting. The tradeoff is
    variance vs cost-per-iteration."
```

### Paper 2: Tammelin et al. — "Solving Heads-Up Limit Texas Hold'em" (2015)

https://arxiv.org/abs/1407.5042 (originally appeared in AAAI 2015 / Science 2015)

```
├── READ:  Section 2 (CFR+ algorithm — the three modifications: floor regrets at 0
│          instead of tracking negative, weight later iterations more, alternating
│          updates by player),
│          Section 3 (Experiments — how they "solved" HULHE)
├── SKIM:  Abstract, Section 1 (Introduction — the significance of solving a real poker variant),
│          Section 4 (Discussion)
├── SKIP:  Supplementary material on the computation cluster setup
├── MATH:  → "The regret floor modification (Eq. 2 vs Eq. 1) — this is the core of
│             CFR+: instead of R(I,a) ← R(I,a) + r, it uses R(I,a) ← max(0, R(I,a) + r).
│             This is trivial to implement but has profound convergence effects.
│             No proof needed — understand it algorithmically."
└── KEY INSIGHT: "CFR+ makes three small changes to vanilla CFR, and the combined
    effect is O(1/T) convergence instead of O(1/√T). That's the difference between
    needing 10^12 iterations and needing 10^6. This is what made it feasible to
    'solve' Heads-Up Limit Hold'em with 10^14 information sets."
```

### Paper 3: Zinkevich et al. (2007) — Revisit Section 5

https://arxiv.org/abs/0709.2092  
*You read this in Step 2. Now revisit Section 5 (the Kuhn/Rhode Island experiments) with fresh eyes — you've now seen MCCFR and CFR+ convergence in Phase 2. Compare the convergence plots.*

### Book: Chen & Ankenman — "The Mathematics of Poker" (2006)

**Link:** No free version available. Purchase: https://www.amazon.com/Mathematics-Poker-Bill-Chen/dp/1886070253  
**Assigned chapters:** 1–8  
**Context — what comes before:** Nothing — Chapter 1 is the start.  
**Context — what comes after (Ch 9–end):** Ch 9–14 cover toy game solutions, multistreet play, tournament theory. *Relevant for poker intuition but not for CFR implementation. Can revisit during Step 13 (behavioral analysis pipelines) if working with poker data.*  
**Reading focus:**
- **Ch 1–3 (skim, ~1 hr):** EV basics, pot odds, fundamental theorem of poker. You know most of this from playing. Skim for formal vocabulary.
- **Ch 4–5 (read, ~2 hrs):** Game-theoretic optimal play, exploitation, the balance between GTO and exploitative strategy. *This is the vocabulary that connects to Steps 7–8 (opponent modeling + safe exploitation).*
- **Ch 6–8 (read key sections, ~2 hrs):** Half-street and full-street toy game solutions. These are the simplest games where you can see Nash equilibrium bluffing frequencies derived analytically. *Builds intuition for why the CFR output "looks the way it does" — the math explains the bluff/call frequencies.*

**Note:** If you can't get this book, the poker-specific math can be substituted by reading Neller & Lanctot's worked examples more carefully and playing with Leduc. The book adds color and domain intuition but isn't algorithmically critical.

### Optional Supplementary

- **Schmid et al. (2018) — "Variance Reduction in Monte Carlo Counterfactual Regret Minimization"**  
  https://arxiv.org/abs/1809.03057  
  *VR-MCCFR adds baseline subtraction to reduce sampling variance. SKIM Sections 1–3 only. This technique reappears in Step 5 (Deep CFR relies on variance reduction).*

- **Farina et al. (2020) — "Stochastic Regret Minimization in Extensive-Form Games"**  
  https://arxiv.org/abs/2002.08493  
  *Unifies sampling-based regret minimization. SKIM abstract only — good for bibliography mining.*

### Math Flags

🔢 **MCCFR unbiased estimation theorem (Lanctot et al., Theorem 1)** — Read statement only.  
**WHY this can't be substituted:** Understanding that sampled updates are UNBIASED is crucial. If they were biased, MCCFR would converge to the wrong answer. The unbiasedness guarantee is what lets you trust the output of a noisy sampling process.

🔢 **CFR+ regret floor (Tammelin et al.)** — Algorithmic understanding only, no proof.  
**WHY:** The improvement from O(1/√T) to O(1/T) is empirically observed and conjectured, not formally proven (Tammelin et al. don't provide a full convergence proof for CFR+). Know the mechanism, not the proof.

---

## Phase 4: Implementation (6 days)

### Project: MCCFR for Leduc Hold'em + CFR+ for Kuhn/Leduc — From Scratch

**Language + Framework:** Python 3.10+ / NumPy only (same constraint as Step 2)

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| Leduc Hold'em game engine (6-card deck, 2 rounds, community card) | 🔴 HAND-CODE | Leduc is significantly more complex than Kuhn (card dealing, 2 rounds, raise/call/fold logic, pot management). Building it teaches you the structure of a real poker variant. |
| External-sampling MCCFR (sample opponent actions, traverse all of own) | 🔴 HAND-CODE | Core contribution #1 of this step. The key difference from vanilla CFR is in how reach probabilities are handled under sampling. THE code to hand-write. |
| Outcome-sampling MCCFR (sample full trajectory, importance weight) | 🟡 AI-ASSISTED | Once you've built external sampling, outcome sampling follows the same structure with importance weighting added. AI drafts it, you review and understand the weighting. |
| CFR+ modifications (regret floor, alternating updates, linear weighting) | 🔴 HAND-CODE | Three small changes to your Step 2 vanilla CFR. Each is ~5 lines, but understanding WHY each helps is the point. Apply to both Kuhn and Leduc. |
| Exploitability computation for Leduc | 🟡 AI-ASSISTED | Same best-response algorithm as Step 2, but extended to a larger game tree. AI drafts the Leduc-specific traversal, you verify. |
| Convergence comparison framework (run all variants, collect metrics, plot) | 🟢 AI-GENERATED | Experiment scaffolding — run N variants × M iteration counts, store results, generate comparison plots. |
| Plotting (convergence curves, strategy tables) | 🟢 AI-GENERATED | Matplotlib comparisons. |

### Sub-phase Breakdown (6 days):

**Day 1 — Leduc Hold'em Game Engine:**
- 🔴 Implement: `leduc_holdem.py`
  - Card representation: 6 cards = {J♠, J♥, Q♠, Q♥, K♠, K♥}
  - Two rounds: pre-flop (2 hole cards dealt) → flop (1 community card)
  - Actions: fold, call, raise (with bet sizes: 2 chips pre-flop, 4 chips on flop)
  - Information sets: (player_hand, community_card_if_revealed, action_history)
  - Terminal payoffs: pair > high card, ties split pot
- Test: verify game tree has ~936 distinct info sets (or enumerate and count them)

**Days 2–3 — External-Sampling MCCFR:**
- 🔴 Implement external sampling for both Kuhn and Leduc:
  - When it's the traversing player's turn: try ALL actions (same as vanilla CFR)
  - When it's the opponent's turn: SAMPLE one action according to the opponent's current strategy
  - When it's a chance node: SAMPLE one outcome
  - Regret updates only along the sampled path for opponent/chance
- Run on Kuhn first (validate against Step 2 vanilla CFR — should converge to same Nash)
- Run on Leduc — compare wall-clock time vs vanilla CFR to reach same exploitability

**Day 4 — CFR+ Implementation:**
- 🔴 Modify your vanilla CFR from Step 2:
  1. **Regret floor:** `cumulative_regret[a] = max(0, cumulative_regret[a] + instant_regret[a])` (instead of allowing negative accumulation)
  2. **Alternating updates:** Update Player 1's regrets on odd iterations, Player 2's on even (instead of both every iteration)
  3. **Linear averaging:** Weight iteration t's strategy by t (instead of uniform weighting)
- Run on Kuhn: verify faster convergence than vanilla CFR
- Run on Leduc: compare convergence vs vanilla CFR and MCCFR

**Day 5 — Outcome Sampling + Full Comparison:**
- 🟡 AI-ASSISTED: Outcome-sampling MCCFR — sample an entire trajectory (all players + chance), importance-weight the regret update
- Compare all four algorithms on Leduc:
  | Algorithm | Exploitability @ 10k iter | Wall time to reach exploit < 0.01 |
  |-----------|---------------------------|----------------------------------|
  | Vanilla CFR | ? | ? |
  | External Sampling MCCFR | ? | ? |
  | Outcome Sampling MCCFR | ? | ? |
  | CFR+ | ? | ? |

**Day 6 — Validation + Documentation:**
- Compare your MCCFR Leduc output against OpenSpiel's MCCFR on Leduc
- Compare your CFR+ output against OpenSpiel's CFR+
- Generate all comparison plots
- Document: which variant is best for Kuhn (small game) vs Leduc (medium game)? What would you choose for a truly large game?

### Deliverables:
- [ ] Leduc Hold'em game engine (fully tested, all 6 cards × 2 rounds × raise/call/fold logic)
- [ ] External-sampling MCCFR solver converging on both Kuhn and Leduc
- [ ] Outcome-sampling MCCFR solver converging on Leduc
- [ ] CFR+ solver converging on both Kuhn and Leduc (faster than vanilla CFR)
- [ ] 4-way convergence comparison plot: vanilla CFR vs external MCCFR vs outcome MCCFR vs CFR+
- [ ] Exploitability comparison table (exploitability @ fixed iterations + wall time to threshold)
- [ ] All code committed with clear README

### Validation:
- **MCCFR on Kuhn:** Should converge to the same Nash equilibrium as your Step 2 vanilla CFR (within noise). Compare strategies — they should agree to ~2 decimal places at 50k iterations.
- **CFR+ on Kuhn:** Should reach exploitability < 0.001 in ~1000 iterations (vs ~10000 for vanilla CFR). Verify ~10x speedup.
- **Leduc:** Cross-validate exploitability values against OpenSpiel at [1k, 5k, 10k] iterations. Should agree within 15% (sampling variance).
- **Convergence rates:** On log-log plot, CFR+ should show slope ≈ -1.0 (vs vanilla CFR's ≈ -0.5). MCCFR should show similar slope to vanilla CFR but reach same exploitability in less wall time.

---

## Phase 5: Consolidation (2 days)

### Day 1 — Reference Skim + Gap Fill

- **Reference skim (book):** Chen & Ankenman Ch 4–5 if not already read — the game-theoretic optimal play vocabulary connects directly to the CFR output you've been computing.
- **Reference skim (paper):** VR-MCCFR (Schmid et al., 2018) abstract + Section 2 — understand the idea of variance reduction baselines. *This bridges to Step 5: Deep CFR uses neural networks as function approximators, and understanding variance reduction here makes Deep CFR's design choices make sense.*
- **Forward preview:** Skim the abstract of Brown et al. "Deep CFR" (2019) — you'll read it fully in Step 5, but see how it builds on MCCFR.
- Review: any components of your implementation you don't fully understand?

### Day 2 — One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 1] Monte Carlo methods (S&B Ch 5) sample trajectories instead of sweeping all states → [Step 3] MCCFR samples game tree paths instead of traversing the full tree. Same principle: trading bias-free estimation for variance in exchange for computational savings.
    - [Step 2] Vanilla CFR traverses full tree O(|tree|) per iteration → [Step 3] MCCFR traverses O(|tree|/branching_factor) per iteration. Same convergence rate, dramatically cheaper per-iteration cost.
    - [Step 2] Cumulative regrets can go negative → [Step 3] CFR+ floors regrets at zero. Parallels [Step 1] ReLU in neural networks — clipping negative activations/regrets both prevent "dead" units/actions.
    - [Step 3] Outcome sampling uses importance weighting → prediction: [Step 5] Deep CFR will need similar variance-control techniques when using neural network approximations.
  - **Confusions:**
    - [Step 3] External sampling converges faster per iteration than outcome sampling, but outcome sampling is cheaper per iteration. When does the crossover happen where outcome sampling wins on wall time? → OPEN (likely depends on game size)
    - [Step 3] CFR+ has O(1/T) convergence empirically but no formal proof. Is this a problem for the thesis? → OPEN (check if proofs exist by Step 6)
    - [Step 2→3] My Step 2 confusion about "average vs current strategy" — I now see current strategy in MCCFR is used for SAMPLING (opponents play it), while average strategy is the output. The current strategy is the exploration mechanism. → RESOLVED by Step 3

### PhD Connection

This step feeds **Contribution #1 (Behavioral Adaptation Framework)** directly: MCCFR is the algorithm that will compute the baseline Nash strategy (the "play it safe" anchor) from which the adaptive agent will deviate based on opponent observations. CFR+ is the tool that makes this computation tractable for real-sized games. The Leduc implementation also establishes the intermediate benchmark game used in Steps 5–8 before scaling to full poker.

---

## Exit Checklist

- [ ] Leduc Hold'em game engine working and tested
- [ ] External-sampling MCCFR converging on both Kuhn and Leduc
- [ ] Outcome-sampling MCCFR converging on Leduc
- [ ] CFR+ converging on both Kuhn and Leduc, demonstrably faster than vanilla CFR
- [ ] Can explain from memory: external vs outcome sampling tradeoffs (variance vs cost)
- [ ] Can explain from memory: the three CFR+ modifications and why each helps
- [ ] Can explain from memory: why MCCFR converges to the same answer as vanilla CFR (unbiased estimation)
- [ ] 4-way convergence comparison with clear winner analysis
- [ ] Cross-validated against OpenSpiel implementations
- [ ] All 🔴 components hand-coded
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Steps 1–2 + new confusions + resolved confusions)
- [ ] Step notes committed to repo

