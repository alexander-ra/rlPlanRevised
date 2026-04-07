# Step 7 — Opponent Modeling — Inference from Behavioral Traces

**Duration:** 21 days (Tier 1)  
**Dependencies:** Step 2 (Game Theory + CFR Basics), Step 6 (End-to-End Game AI Architectures)  
**Phase:** D — Opponent Modeling + Exploitation  

### PhD Connection

This step is the FIRST HALF of Contribution #1 (Behavioral Adaptation Framework). The opponent model is the "sensor" that takes raw behavioral data (observed actions, revealed hands at showdown) and produces a structured estimate of the opponent's strategy. Without this sensor, the agent cannot adapt — it can only play Nash (safe but unexploitative).

**What this step provides for the thesis:**
- Three concrete opponent modeling approaches with empirical comparisons
- Understanding of when each approach is appropriate
- A clear open question: handling non-stationarity (the thesis's novel contribution opportunity)
- Demonstration that opponent modeling WORKS on toy games — now must scale (via Steps 8 + 11)

---

> **Phase Overview:** This phase addresses the central research question: how should an agent adapt its play to a specific opponent? The preceding phases built the algorithmic toolbox — equilibrium solvers, abstraction, and neural approximation — but did not yet tackle opponent-aware play. Step 7 will introduce inference mechanisms that convert observed action sequences into beliefs about opponent behavior. Step 8 will cover algorithms that translate those beliefs into profitable yet safe strategy adjustments.


## Table of Contents
- [Phase 1: Intuition (2 days)](#phase-1-intuition-2-days)
  - [Day 1: The Problem & Classical Approaches](#day-1-the-problem-classical-approaches)
  - [Day 2: Modern Approaches & the Exploitation Tradeoff](#day-2-modern-approaches-the-exploitation-tradeoff)
  - [Blog Posts / Accessible Reads](#blog-posts-accessible-reads)
- [Phase 2: Exploration (2 days)](#phase-2-exploration-2-days)
  - [Day 1: Observing Opponent Types in OpenSpiel](#day-1-observing-opponent-types-in-openspiel)
  - [Day 2: Bayesian Type Inference — Hands-On](#day-2-bayesian-type-inference-hands-on)
- [Phase 3: Targeted Reading (4 days)](#phase-3-targeted-reading-4-days)
  - [Paper 1: Southey et al. — "Bayes' Bluff: Opponent Modelling in Poker" (2005)](#paper-1-southey-et-al-bayes-bluff-opponent-modelling-in-poker-2005)
  - [Paper 2: Bard et al. — "Online Implicit Agent Modelling" (2013)](#paper-2-bard-et-al-online-implicit-agent-modelling-2013)
  - [Paper 3: Ganzfried & Sun — "Bayesian Opponent Exploitation in Imperfect-Information Games" (2016/2018)](#paper-3-ganzfried-sun-bayesian-opponent-exploitation-in-imperfect-information-games-20162018)
  - [Paper 4: Ganzfried, Wang & Chiswick — "Opponent Modeling in Multiplayer Imperfect-Information Games" (2022/2024)](#paper-4-ganzfried-wang-chiswick-opponent-modeling-in-multiplayer-imperfect-information-games-20222024)
  - [Paper 5: Ganzfried — "Consistent Opponent Modeling in Imperfect-Information Games" (2025/2026)](#paper-5-ganzfried-consistent-opponent-modeling-in-imperfect-information-games-20252026)
  - [Book Chapters (Supplementary)](#book-chapters-supplementary)
  - [Math Flags](#math-flags)
- [Phase 4: Implementation (10 days)](#phase-4-implementation-10-days)
  - [Project: Bayesian Opponent Modeler + Adaptive Exploiter for Kuhn & Leduc — From Scratch](#project-bayesian-opponent-modeler-adaptive-exploiter-for-kuhn-leduc-from-scratch)
  - [Sub-phase Breakdown (10 days):](#sub-phase-breakdown-10-days)
  - [Deliverables:](#deliverables)
  - [Validation:](#validation)
- [Phase 5: Consolidation (3 days)](#phase-5-consolidation-3-days)
  - [Day 1 — Reference Skim + Gap Fill](#day-1-reference-skim-gap-fill)
  - [Day 2 — Deep Comparison + Thesis Connection](#day-2-deep-comparison-thesis-connection)
  - [Day 3 — One-Pager + Learning Log](#day-3-one-pager-learning-log)
- [Exit Checklist](#exit-checklist)

## Phase 1: Intuition (2 days)

The goal: understand WHY opponent modeling matters (Nash equilibrium ignores opponent weaknesses), what KIND of information you can extract from behavioral traces (action frequencies, timing patterns, deviations from equilibrium), and WHEN it's worth deviating from Nash to exploit a weak opponent. End of days: you should be able to explain to a non-expert: "If your opponent always folds to big bets, a Nash equilibrium strategy doesn't know that — it plays the same regardless. An opponent model DETECTS that pattern and lets you bluff more against that specific player. The hard part is doing this without becoming exploitable yourself."

### Day 1: The Problem & Classical Approaches

- **Bayes theorem, the geometry of changing beliefs**  
  https://www.youtube.com/watch?v=HZGCoVF3YvM  
  Duration: ~15m | Channel: 3Blue1Brown  
  *Essential refresher on Bayesian inference — the mathematical backbone of all opponent modeling. Prior beliefs updated by evidence to form posterior beliefs.*

- **Stanford CS224R — Lecture 2: Imitation Learning (Spring 2025)**  
  https://www.youtube.com/watch?v=WxRDyObrm_M  
  Duration: ~1h7m | Instructor: Chelsea Finn (Stanford)  
  *Learning from observing others' behavior: behavioral cloning, DAgger, and expressive policy distributions. The same paradigm used for inferring opponent strategies from their actions.*

### Day 2: Modern Approaches & the Exploitation Tradeoff

- **AI for Imperfect-Information Games: Beating Top Humans in No-Limit Poker**  
  https://www.youtube.com/watch?v=McV4a6umbAY  
  Duration: ~1h | Speaker: Noam Brown | Channel: Microsoft Research  
  *Covers Libratus's self-improvement module: how the system detects opponent patterns during play and patches its own weaknesses overnight. The practical side of opponent adaptation.*

### Blog Posts / Accessible Reads

- **Sam Ganzfried — "Opponent Modeling and Exploitation in Poker and Beyond" (personal blog / research summary)**  
  https://www.sganzfried.com/research  
  *Overview of Ganzfried's line of research. Read the opponent modeling section for a non-technical summary of the progression.*

- **AI and Poker — "The Evolution from GTO to Exploitative Play"**  
  Search for poker AI blogs covering the GTO-vs-exploitative spectrum. Any poker strategy site explaining "GTO vs exploitative" gives intuition for why opponent modeling matters.  
  *The poker community has been debating this for decades. The academic formalization is exactly what this step covers.*

---

## Phase 2: Exploration (2 days)

### 🎮 Interactive Exploration
- **[Rock Paper Scissors Pattern Modeler](https://www.afiniti.com/corporate/rock-paper-scissors)** — Play against an AI that actively models your behavioral tendencies using Markov Chains. Try to be unpredictable!


### Day 1: Observing Opponent Types in OpenSpiel

1. **Create a simple opponent type zoo in your Kuhn/Leduc engine:**
   ```python
   import pyspiel
   import numpy as np
   
   # Define 4 opponent types for Kuhn Poker:
   # Type 1: "Always Call" — never folds, never raises
   # Type 2: "Tight-Passive" — only bets with K, folds J to any bet
   # Type 3: "Loose-Aggressive" — always raises regardless of hand
   # Type 4: "Nash" — plays the known Nash equilibrium strategy
   
   # For each type, define a fixed strategy (action probabilities per info set)
   # Run 1000 hands of each type against a Nash player
   # Log: action frequencies at each info set
   ```

2. **Visualize opponent behavioral signatures:**
   - For each opponent type, compute: bet frequency, fold frequency, call frequency per info set
   - Plot a "behavioral fingerprint" — a bar chart showing action distributions across info sets
   - *Key insight to observe: different opponent types produce DISTINCT behavioral signatures. The tight-passive opponent's fingerprint looks nothing like the loose-aggressive one. This is what an opponent model tries to infer.*

3. **Measure exploitation opportunity:**
   - Compute the best response to each opponent type using OpenSpiel's `exploitability` module
   - Compare: Nash expected value vs best-response expected value against each type
   - *Expected result: against the Nash opponent, best response ≈ Nash value (0). Against fixed exploitable types, best response >> 0. The gap IS the exploitation opportunity.*

### Day 2: Bayesian Type Inference — Hands-On

1. **Implement a naive Bayesian type detector:**
   ```python
   # Prior: uniform over 4 opponent types [0.25, 0.25, 0.25, 0.25]
   # After each observed action:
   #   likelihood = P(action | type, info_set)  — from type's known strategy
   #   posterior ∝ prior × likelihood
   #   normalize posterior
   
   # Run against hidden Type 2 (tight-passive) for 50 hands
   # Plot: posterior probability of each type over time
   ```
   - *Expected result: after ~10-20 hands, the posterior concentrates on the correct type. The speed of convergence depends on how distinctive the opponent's actions are — if they fold with J, that's highly informative.*

2. **Test the limits of type-based modeling:**
   - What happens when the opponent is Type 5 (a mixture of Type 1 and Type 3)?
   - The Bayesian detector should spread probability between the two closest types
   - *Observe: type-based models fail when the opponent doesn't fit any predefined type. This motivates the continuous/parametric models in Phase 3.*

3. **Play with OpenSpiel's policy-based tools:**
   ```python
   from open_spiel.python.algorithms import best_response
   from open_spiel.python import policy as policy_lib
   
   game = pyspiel.load_game("kuhn_poker")
   
   # Create a tabular policy for your opponent model (initially uniform)
   opponent_policy = policy_lib.TabularPolicy(game)
   
   # Compute best response to this policy
   br = best_response.BestResponsePolicy(game, player_id=0, policy=opponent_policy)
   ```
   - *This is the exploitation side — once you HAVE a model, computing the best response against it is straightforward. The hard part is getting the model right.*

4. **Questions to answer by end of Day 2:**
   - How many observations do you need before the Bayesian detector is confident?
   - What happens when the opponent switches types mid-game?
   - Why can't you just compute the best response to the observed frequencies directly? (Answer: overfitting to small samples → catastrophic exploitation if the opponent adapts.)
   - What's the difference between "implicit" modeling (infer from behavior) and "explicit" modeling (assume a type)?

---

## Phase 3: Targeted Reading (4 days)

### Paper 1: Southey et al. — "Bayes' Bluff: Opponent Modelling in Poker" (2005)

https://poker.cs.ualberta.ca/publications/UAI05.pdf

```
├── READ:  Section 3 (Bayesian opponent model — the generative model of opponent 
│          play: prior over strategy parameters, likelihood of observed actions,
│          posterior inference via Bayes' rule),
│          Section 4 (Experiments — Bayesian model on simplified poker)
├── SKIM:  Abstract, Section 1 (Introduction — history of opponent modeling),
│          Section 2 (Background — poker rules, game formalism)
├── SKIP:  Section 5 (Discussion — general commentary)
├── MATH:  → "The Bayesian update equation (Eq. 3-4) — work through a small example
│             by hand. Start with a uniform prior over 3 opponent types, observe
│             one action, compute the posterior. This is the foundation of ALL 
│             Bayesian opponent modeling that follows."
│          → "The Dirichlet prior (Section 3.2) — understand why Dirichlet is the
│             natural conjugate prior for multinomial action distributions. This
│             is NOT optional — it's the standard prior used in all subsequent
│             papers. If you know Beta distributions, Dirichlet is just the 
│             multivariate version."
└── KEY INSIGHT: "Opponent modeling IS Bayesian inference: you have a prior belief
    about how the opponent plays, you update it as you observe their actions,
    and you compute a posterior. The GAME STRUCTURE constrains what information
    is available — you only see actions, not the opponent's private hand. This
    partial observability is what makes opponent modeling in games HARD."
```

### Paper 2: Bard et al. — "Online Implicit Agent Modelling" (2013)

https://poker.cs.ualberta.ca/publications/AAMAS13-bard.pdf

```
├── READ:  Section 3 (Implicit agent modelling — instead of maintaining an explicit
│          belief over types, the opponent model is IMPLICIT in the strategy's
│          response to observed actions),
│          Section 4 (Online algorithm — how to update the model after each game,
│          the incremental update procedure),
│          Section 5 (Experiments — implicit vs explicit modeling on poker)
├── SKIM:  Abstract, Section 1–2 (Background),
│          Section 6 (Related work), Section 7 (Conclusion)
├── SKIP:  None — paper is concise (~8 pages)
├── MATH:  → "The implicit model update (Algorithm 1) — trace the algorithm 
│             step-by-step. The key distinction from explicit Bayesian modeling 
│             is that you never maintain a probability distribution over types.
│             Instead, the strategy itself evolves to be a soft best-response 
│             to the observed action frequencies."
└── KEY INSIGHT: "There are TWO paradigms for opponent modeling: EXPLICIT (maintain
    a belief distribution, compute best response to the posterior) and IMPLICIT
    (let the strategy adapt directly without maintaining beliefs). Explicit gives 
    you interpretability (you know what you think the opponent is doing). Implicit
    is simpler to implement and scales better. Your thesis needs to understand
    both — the Behavioral Adaptation Framework (Contribution #1) likely uses
    explicit modeling for interpretability."
```

### Paper 3: Ganzfried & Sun — "Bayesian Opponent Exploitation in Imperfect-Information Games" (2016/2018)

https://arxiv.org/abs/1603.03491

```
├── READ:  Section 3 (The Bayesian exploitation framework — prior over opponent
│          strategies, posterior update from observed hand histories, best-response
│          computation to the posterior),
│          Section 4 (Experiments on Kuhn Poker and Leduc Hold'em — convergence
│          of exploitation profit over time)
├── SKIM:  Abstract, Section 1 (Introduction — the exploitation-exploration tradeoff),
│          Section 2 (Background — Nash equilibrium, best response),
│          Section 5 (Conclusion + open questions)
├── SKIP:  Proofs in appendix (unless pursuing theoretical depth)
├── MATH:  → "Theorem 1 (Convergence of Bayesian exploitation) — read the STATEMENT.
│             This guarantees that as observations increase, the exploitation 
│             strategy converges to the true best response. Know the assumptions:
│             the opponent plays a FIXED (stationary) strategy, and the prior
│             has support on the opponent's true strategy."
│          → "WHY this can't be substituted by algorithmic understanding: the 
│             convergence guarantee is what separates principled Bayesian 
│             exploitation from ad-hoc heuristics. Your thesis must state
│             WHEN the guarantee holds and WHEN it breaks (non-stationary 
│             opponents, misspecified priors). The theorem tells you both."
└── KEY INSIGHT: "This paper CONNECTS opponent modeling (Step 7) to exploitation 
    (Step 8). The model is the input; the best response to the model is the 
    output. The question is: how do you exploit WITHOUT losing safety? That's 
    Step 8's problem. But first you need the model to be GOOD — that's THIS 
    step's problem."
```

### Paper 4: Ganzfried, Wang & Chiswick — "Opponent Modeling in Multiplayer Imperfect-Information Games" (2022/2024)

https://arxiv.org/abs/2212.06027

```
├── READ:  Section 3 (Extension of opponent modeling to N-player games — the 
│          key complication: with N opponents, you need N separate models,
│          and the optimal response depends on ALL of them jointly),
│          Section 4 (Experiments on 3-player Kuhn Poker — how the modeling
│          algorithm performs against heterogeneous opponent populations)
├── SKIM:  Abstract, Section 1–2 (Background),
│          Section 5 (Conclusion)
├── SKIP:  None — paper is relatively short
├── MATH:  → "The joint opponent model (Section 3.1) — understand how the 
│             single-opponent Bayesian framework extends to multiple opponents.
│             The posterior is now over TUPLES of strategies (one per opponent).
│             Skim the algebra; focus on the conceptual extension."
└── KEY INSIGHT: "Multiplayer opponent modeling is NOT just 'do 2-player modeling 
    N times.' The optimal exploitation strategy against opponents A and B 
    jointly differs from the combination of individual best responses. This 
    is the core complication that feeds into your thesis Contribution #2 
    (Multi-Agent Safe Exploitation)."
```

### Paper 5: Ganzfried — "Consistent Opponent Modeling in Imperfect-Information Games" (2025/2026)

https://arxiv.org/abs/2508.17671

```
├── READ:  Section 3 (The consistency property — what existing algorithms FAIL
│          to guarantee: convergence to the opponent's true strategy even in
│          the limit of infinite observations),
│          Section 4 (New algorithm — sequence-form projected gradient descent
│          for consistent opponent modeling),
│          Section 5 (Experiments — comparison against prior methods)
├── SKIM:  Abstract, Section 1–2 (Motivation and background),
│          Section 6 (Conclusion)
├── SKIP:  Full convergence proof details (read statement + sketch only)
├── MATH:  → "The convex optimization formulation (Section 4) — understand why 
│             the sequence-form representation makes opponent modeling a CONVEX
│             problem. This is important because convexity guarantees a unique 
│             solution and efficient algorithms (projected gradient descent)."
│          → "WHY this can't be substituted: the paper shows existing methods
│             FAIL a basic consistency test. Understanding the convex formulation
│             tells you why the fix works and why it's computationally tractable."
└── KEY INSIGHT: "Existing opponent modeling algorithms (including Papers 1-4 above)
    don't guarantee convergence to the TRUE opponent strategy even with infinite
    data. This paper fixes that with a convex optimization approach. It's the 
    most recent work in the field and directly relevant to your thesis — your
    Behavioral Adaptation Framework should incorporate or extend this guarantee."
```

### Book Chapters (Supplementary)

**Book:** Shoham, Y. & Leyton-Brown, K. — *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations* (2008)  
**Link:** http://www.masfoundations.org/download.html (free PDF)  
**Assigned chapters:** 7 (Learning and Teaching)  
**Context — what comes before (Ch 1–6):** Game theory foundations (normal form, extensive form, Nash equilibrium, computing equilibria). *You know all of this from Steps 2–4.*  
**Context — what comes after (Ch 8–end):** Coalitional game theory, social choice, mechanism design. *Relevant for Step 11 (coalition formation) — skip for now.*  
**Reading focus:** Section 7.1–7.3 specifically covers opponent modeling as a learning problem in games. Provides the formal framework connecting your papers.

### Math Flags

🔢 **Bayesian posterior update for opponent models (Southey et al., Eq. 3-4)** — Must work through by hand on a small example.  
**WHY this can't be substituted:** The posterior update is the CORE computation of the entire step. If you can't do it on paper for 3 types × 3 info sets, you can't debug your implementation or extend it for your thesis.

🔢 **Dirichlet-multinomial conjugacy (Southey et al., Section 3.2)** — Must understand why Dirichlet is the natural prior.  
**WHY:** Every Bayesian opponent modeling paper uses this. It's the reason posterior updates are CLOSED-FORM (no MCMC needed). Your implementation relies on this efficiency.

🔢 **Sequence-form convex formulation (Ganzfried 2025, Section 4)** — Must understand the formulation, not the full proof.  
**WHY:** This is the cutting edge. Your thesis likely extends or applies this. Know it well enough to explain to your committee.

---

## Phase 4: Implementation (10 days)

### Project: Bayesian Opponent Modeler + Adaptive Exploiter for Kuhn & Leduc — From Scratch

**Language + Framework:** Python 3.10+ / NumPy (core algorithm), PyTorch optional for neural extensions

Starting point: Your Kuhn Poker engine (Step 2), Leduc Hold'em engine (Step 3), Nash equilibrium strategies from CFR/MCCFR (Steps 2–3), and game tree infrastructure from Step 6.

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| Opponent type library (4+ fixed strategies for Kuhn/Leduc) | 🟡 AI-ASSISTED | Strategy definitions are straightforward; AI drafts type table, you verify strategic correctness. |
| Bayesian type-based opponent model (Dirichlet-multinomial) | 🔴 HAND-CODE | This IS the step. The posterior update, the likelihood computation from partial observations, the handling of unobserved private information. Must own every line. |
| Continuous Bayesian model (per-info-set action distribution estimation) | 🔴 HAND-CODE | The extension from discrete types to continuous strategy estimation. This is the parametric model that will matter for the thesis. |
| Consistent opponent modeler (Ganzfried 2025 — convex optimization approach) | 🔴 HAND-CODE | The cutting-edge algorithm. Implement the sequence-form projected gradient descent. This is thesis-critical — understanding requires building it. |
| Best-response computation against inferred opponent model | 🟡 AI-ASSISTED | You've built best-response trees before (Steps 2–4). The new part is feeding the opponent model's posterior into the BR computation. AI drafts the integration, you review. |
| Adaptive exploitation pipeline (observe → update model → compute BR → act) | 🔴 HAND-CODE | The full pipeline that ties everything together. This is the prototype for Contribution #1 (Behavioral Adaptation Framework). |
| Tournament framework (run modeler against various opponents, measure performance) | 🟢 AI-GENERATED | Tournament infrastructure: run 10000 hands, switch opponents, log results. |
| Plotting + visualization (posterior evolution, exploitation profit curves) | 🟢 AI-GENERATED | Matplotlib visualizations for analysis. |

### Sub-phase Breakdown (10 days):

**Days 1–2 — Architecture + Scaffolding:**

*Day 1 — Opponent Type Library + Observation Infrastructure:*
- 🟡 AI-ASSISTED: Create `opponent_types.py`:
  - Kuhn Poker types: AlwaysCall, TightPassive, LooseAggressive, Nash, TightAggressive (5 types)
  - Leduc Hold'em types: same behavioral archetypes but adapted for 2-round structure
  - Each type is a callable policy: `type.action_probabilities(info_set) → dict[action → prob]`
- 🔴 HAND-CODE: Create `observation_buffer.py`:
  - Stores game history: (info_set_observed, action_taken, outcome)
  - Handles partial observability: you see the opponent's ACTIONS but not their private hand (unless showdown)
  - At showdown: record revealed hands → this is the most informative observation
  - Non-showdown: record action sequence only → less informative but more common

*Day 2 — Bayesian Framework Setup:*
- 🔴 HAND-CODE: Create `bayesian_model.py` skeleton:
  - Prior: Dirichlet distribution over action probabilities at each info set
  - Likelihood function: P(observed_action | info_set, model_params)
  - Posterior update: closed-form Dirichlet update when observation is available
  - Handle partial observability: when opponent's hand is unknown, marginalize over possible hands
  - Interface: `model.update(observation)`, `model.predict(info_set) → action_probs`

**Days 3–8 — Core Algorithm Implementation:**

*Day 3 — Discrete Type-Based Bayesian Model:*
- 🔴 HAND-CODE: `type_based_model.py`:
  - Prior: uniform over K opponent types
  - Observation: (info_set, action) pair
  - Likelihood: `P(action | type_k, info_set)` = type_k's strategy probability
  - Posterior: `P(type_k | observations) ∝ prior(type_k) × ∏ P(action_i | type_k, info_set_i)`
  - Predicted strategy: `E[strategy | observations] = Σ_k P(type_k | observations) × strategy_k`
- Test on Kuhn: run against hidden TightPassive, verify posterior concentrates correctly

*Day 4 — Handling Partial Observability:*
- 🔴 HAND-CODE: The hard version of the likelihood:
  - When you DON'T see the opponent's hand (most situations), the likelihood becomes:
    `P(action | info_set_visible) = Σ_hand P(hand) × P(action | info_set_full(hand), type_k)`
  - This marginalization is the computational bottleneck in larger games
  - Implement for Kuhn (trivial — 3 possible hands) and Leduc (6 possible hands)
- Test: compare posterior convergence speed with/without showdown information
  - *Expected: showdown hands are ~3x more informative per observation*

*Day 5 — Continuous Bayesian Model:*
- 🔴 HAND-CODE: `continuous_model.py`:
  - Instead of K fixed types, estimate action probabilities DIRECTLY at each info set
  - Prior: Dirichlet(α₀) at each info set (α₀ = 1 for uniform, or α₀ tuned to taste)
  - Update: after observing action a at info set I: `α_I[a] += 1`
  - Posterior mean: `P(a | I) = α_I[a] / Σ_a' α_I[a']`
  - This is a maximum a posteriori (MAP) estimate with Laplace smoothing
- Compare against type-based model:
  - Against known types: type-based should converge faster (uses structural knowledge)
  - Against unknown types (mixtures, novel strategies): continuous should be more robust

*Day 6 — Consistent Opponent Modeler (Ganzfried 2025):*
- 🔴 HAND-CODE: `consistent_model.py`:
  - Represent opponent strategy in sequence form (realization plan)
  - After N observations, form the empirical frequency vector
  - Solve: minimize distance between model and empirical frequencies, subject to sequence-form constraints
  - Use projected gradient descent onto the sequence-form polytope
  - *The sequence-form constraint is what makes this "consistent" — it forces the model to be a valid strategy, not just arbitrary action frequencies*
- Test on Kuhn: verify convergence to true opponent strategy as N → ∞

*Day 7 — Best Response Against Inferred Model:*
- 🟡 AI-ASSISTED: Adapt your Step 2–4 best-response computation:
  - Input: the opponent model's predicted strategy (from any of the three models above)
  - Output: the strategy that maximizes EV against that predicted strategy
  - For type-based model: compute BR against the posterior-weighted mixture of types
  - For continuous model: compute BR against the estimated action probabilities
  - For consistent model: compute BR against the sequence-form model output
- 🔴 Verify that BR against Nash ≈ Nash value (0 for Kuhn), and BR against exploitable types >> 0

*Day 8 — Adaptive Exploitation Pipeline:*
- 🔴 HAND-CODE: `adaptive_exploiter.py`:
  - Full pipeline: observe → update model → compute best response → play best response → repeat
  - Run against each opponent type for 10000 hands
  - Measure: cumulative exploitation profit over time for each model (type-based, continuous, consistent)
  - Plot: profit curves for all three models against all opponent types
  - *This is the prototype of Contribution #1*

**Days 9–10 — Validation + Benchmarking:**

*Day 9 — Head-to-Head Model Comparison:*
- Run all three models against all 5 opponent types on both Kuhn and Leduc
- Measure:
  | Model | Opponent | Convergence Speed | Final Exploitation Rate | Robustness to Type Switch |
  |-------|----------|-------------------|------------------------|--------------------------|
  | Type-Based | TightPassive | ? | ? | ? |
  | Continuous | TightPassive | ? | ? | ? |
  | Consistent | TightPassive | ? | ? | ? |
  | ... | ... | ... | ... | ... |

- Test non-stationarity: opponent switches type after 5000 hands
  - Type-based model with exponential decay on prior should adapt
  - Continuous model with exponential moving average of counts should adapt
  - Consistent model: does it handle non-stationarity? (Likely not without modification — log as open question)

*Day 10 — Cross-Validation + Documentation:*
- Cross-validate against OpenSpiel's best-response and exploitability tools:
  - Compute your model's predicted opponent strategy
  - Have OpenSpiel compute the best response to that strategy
  - Compare OpenSpiel's BR value against your BR value → should match within numerical precision
- Run exploitability computation:
  - Your adaptive exploiter, when playing its BR, should achieve exploitation close to the KNOWN exploitation ceiling (the true best response to the true opponent strategy)
  - Gap between achieved exploitation and ceiling = modeling error
- Document all results
- Clean code, write README

### Deliverables:
- [ ] Opponent type library (5+ types for Kuhn, 5+ for Leduc)
- [ ] Observation buffer with partial observability handling
- [ ] Type-based Bayesian opponent model with Dirichlet-multinomial inference
- [ ] Continuous Bayesian opponent model with per-info-set Dirichlet estimation
- [ ] Consistent opponent modeler (Ganzfried 2025 sequence-form approach)
- [ ] Best-response computation against inferred models
- [ ] Adaptive exploitation pipeline (observe → model → exploit → repeat)
- [ ] Head-to-head model comparison table + exploitation profit curves
- [ ] Non-stationarity test results (type-switching opponent)
- [ ] Cross-validation against OpenSpiel

### Validation:
- **Type-based model on Kuhn:** Posterior should concentrate on true type within 20 hands (~90% posterior probability). Compare with analytical Bayes update computed by hand.
- **Continuous model on Kuhn:** Action probability estimates should converge to true opponent strategy within 5% after 500 observations. Compare with true frequencies from 100k-hand simulation.
- **Consistent model on Kuhn:** Should converge to true strategy in sequence form. Verify that the resulting strategy satisfies sequence-form constraints (realization plan sums correctly).
- **Exploitation pipeline:** Against a fixed exploitable opponent, cumulative profit should be strictly positive and growing faster than the Nash baseline (which earns 0 in expectation against any strategy in a 2-player zero-sum game).
- **Cross-validation:** Best-response values must match OpenSpiel's computation to within 0.001 on Kuhn, 0.01 on Leduc.

---

## Phase 5: Consolidation (3 days)

### Day 1 — Reference Skim + Gap Fill

- **Reference skim (book):** Shoham & Leyton-Brown, Chapter 7 (Learning and Teaching). Focus on Sections 7.1–7.3 for the formal learning framework in games. Note how opponent modeling is formalized as a learning problem with partial feedback.
  *Link:* http://www.masfoundations.org/download.html

- **Reference skim (paper):** Milec, Kovařík & Lisý (2025) "Adapting Beyond the Depth Limit" — read abstract + Section 3. Note how they handle the depth-limited setting where you can't inspect the whole game tree. *This bridges directly to Step 8.*
  https://arxiv.org/abs/2501.10464

- **Reference skim (paper):** Zhou et al. (2022/2024) "DecisionHoldem" — skim abstract + method overview. Note the diverse opponent handling approach.
  https://arxiv.org/abs/2201.11580

- **Forward preview:** Read the abstract of Ganzfried & Sandholm (2015) "Safe Opponent Exploitation" — this is the core paper for Step 8. Note how it takes the opponent MODEL (what you built in this step) and derives the SAFETY constraint (what Step 8 formalizes).

- **Review:** Any components of your implementation you don't fully understand? Any posterior updates that gave unexpected results?

### Day 2 — Deep Comparison + Thesis Connection

- **Compare your three models analytically:**
  - Type-based: strongest when the true opponent IS one of the types. Fails gracefully if types are close to the true opponent. Fails catastrophically if the type library is poor.
  - Continuous: most robust to unknown opponents. Slowest convergence because it estimates independently at each info set (no structural sharing).
  - Consistent: best theoretical guarantees (convergence to true strategy). Requires solving an optimization problem per update — more computational cost but most principled.
  - *Which one should the thesis use?* Log this as a research question. Answer likely: "a hybrid that uses structural priors (like types) when data is sparse and converges to the consistent model as data grows."

- **PhD Connection deep dive:**
  - Contribution #1 (Behavioral Adaptation Framework): this step built the "sensor" — the component that infers opponent behavior from observations. Step 8 builds the "actuator" — the component that translates the model into safe exploitation.
  - The key open question: how do you handle NON-STATIONARY opponents? Your non-stationarity test from Day 9 likely showed that fixed models degrade. The thesis contribution should address this — either windowed estimation, change-point detection, or online learning with forgetting.
  - Log for Step 11: in multi-player games, you need MULTIPLE opponent models running simultaneously. How does computational cost scale? Can you share information across models (e.g., "all opponents are fish" as a joint prior)?

### Day 3 — One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 2] Nash equilibrium = the strategy that ignores opponent identity → [Step 7] Opponent model = the mechanism that USES opponent identity to deviate from Nash. Steps 2 and 7 are the two endpoints of the safety-exploitation spectrum.
    - [Step 3] MCCFR samples opponent actions according to the CURRENT strategy → [Step 7] Opponent model samples opponent actions according to the INFERRED model. Same sampling mechanism, different source of the distribution.
    - [Step 4] Abstraction groups similar game states → [Step 7] Type-based modeling groups similar opponent strategies. Same idea (clustering for tractability), different domain (game states vs. strategy space).
    - [Step 4] Action translation maps unseen bets to known abstractions → [Step 7] Opponent model maps unseen behavior to known types. Same "nearest neighbor in reduced space" logic.
    - [Step 6] Blueprint strategy (from Pluribus/ReBeL) = the Nash baseline → [Step 7] Deviation from blueprint = exploitation. The model determines HOW MUCH to deviate and in WHAT DIRECTION.
  - **Confusions:**
    - [Step 7] The consistent model (Ganzfried 2025) requires solving a convex optimization per update. In a real-time game, is this fast enough? → OPEN (check computational complexity; may be addressed in Step 8 via subgame solving approximation)
    - [Step 7] Non-stationary opponents: all three models assume stationarity for convergence guarantees. How badly do they degrade when the opponent adapts? → PARTIALLY ADDRESSED (exponential decay helps empirically) → Need theoretical treatment (possibly Step 14 evaluation framework)
    - [Step 7] In Leduc, partial observability significantly slows convergence. In NLHE (10^161 states), how many hands would you need? → OPEN (this is why abstraction from Step 4 matters — model in the abstract space, not the full space)
    - [Step 4→7] Prediction confirmed: opponent model DOES need "map unseen behavior to known types" logic, exactly like action translation. The parallels are deep.

## Exit Checklist

- [ ] All three opponent models working and validated on Kuhn and Leduc
- [ ] Type-based model converges to correct type within 20 hands (Kuhn)
- [ ] Continuous model action estimates within 5% of true strategy after 500 hands
- [ ] Consistent model converges to true sequence-form strategy
- [ ] Can explain Bayesian opponent modeling from memory (prior → likelihood → posterior → best response)
- [ ] Can explain the difference between explicit and implicit modeling
- [ ] Can explain WHY the consistent model fixes a flaw in prior approaches
- [ ] Adaptive exploitation pipeline running end-to-end with measurable profit
- [ ] Head-to-head model comparison complete with clear conclusions
- [ ] Non-stationarity test completed and results documented
- [ ] Cross-validated against OpenSpiel
- [ ] All 🔴 components hand-coded (type-based model, continuous model, consistent model, exploitation pipeline)
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Steps 2–6 + new confusions + resolved confusions)
- [ ] PhD connection documented (Contribution #1: sensor component)
- [ ] Open questions logged: non-stationarity handling, computational cost of consistent model, scaling to large games
- [ ] Level-k opponent type implemented and tested (P5)
- [ ] Bayesian online changepoint detection integrated into non-stationarity experiment (P8)
- [ ] Step notes committed to repo

> **[P5] Level-k / Cognitive Hierarchy merge:** Add one paper on Level-k/cognitive hierarchy models (e.g., Wright & Leyton-Brown 2014 or Camerer, Ho & Chong 2004) to Phase 3 reading. Add a Level-k opponent type to the opponent type library in Phase 4. Models human suboptimality — critical for Playtech data validation in Step 13. ~1.5d absorbed within 21d allocation.

> **[P8] Bayesian Online Changepoint Detection merge:** Add Adams & MacKay (2007) changepoint detection to the non-stationarity experiment in Phase 4. Instead of ad-hoc “observe what happens when opponent switches type,” detect the switch point statistically, then trigger re-modeling. ~0.5d absorbed within 21d allocation.

> **[P11*] Meta-Learning Baseline (optional):** If Step 7 completes ahead of schedule, run one off-the-shelf meta-learning method (e.g., MAML or contextual bandit) as a comparison baseline against the Bayesian opponent model. No tuning. Preempts reviewer question “why not just meta-learn?”
