# Step 5 — Neural Equilibrium Approximation (Deep CFR, DREAM)

**Duration:** 11 days (Tier 2 — compressed)  
**Dependencies:** Step 1 (RL Basics), Step 3 (CFR Variants + MC Methods), Step 4 (Game Abstraction + Scaling)  
**Phase:** C — Neural Methods for Games

> **Know-How First compression:** Implementation phase cut from 6d to 3d. Get Deep CFR running on Leduc with correct exploitability convergence. Understand DREAM conceptually (reading + exploration). Defer full DREAM implementation and head-to-head Deep CFR vs. DREAM benchmark to implementation phase post-November. All reading and intuition phases unchanged.
> Phase allocation: Intuition 1d | Exploration 2d | Reading 3d | Implementation **3d** | Consolidation 2d  

### PhD Connection

This step feeds **Contribution #1 (Behavioral Adaptation Framework)** directly: Deep CFR's advantage networks are the technical mechanism for computing baseline strategies in games too large for tabular CFR. The information state encoding designed here (tensor representation of game state) becomes the foundation for the opponent modeling input in Step 7. NFSP's anticipatory parameter η foreshadows the exploitation-safety tradeoff central to Step 8 and the thesis.

---

> **Phase Overview:** Phases A and B established tabular equilibrium solvers and abstraction techniques for medium-scale games. However, tabular methods store explicit strategy and regret values at every information set — an approach whose memory requirements grow linearly with game size and become prohibitive for large-scale domains. This phase replaces tabular storage with neural network function approximation, enabling equilibrium computation without explicit game tree enumeration.


## Table of Contents
- [Phase 1: Intuition (1 day)](#phase-1-intuition-1-day)
  - [Bridge: Neural Network Foundations for RL](#bridge-neural-network-foundations-for-rl)
  - [Videos](#videos)
  - [Blog Posts](#blog-posts)
- [Phase 2: Exploration (2 days)](#phase-2-exploration-2-days)
  - [Day 1: Deep CFR in OpenSpiel](#day-1-deep-cfr-in-openspiel)
  - [Day 2: NFSP in OpenSpiel + Advantage Network Internals](#day-2-nfsp-in-openspiel-advantage-network-internals)
- [Phase 3: Targeted Reading (3 days)](#phase-3-targeted-reading-3-days)
  - [Preliminary Reading: Function Approximation Theory](#preliminary-reading-function-approximation-theory)
  - [Paper 1: Brown, Lerer, Gross & Sandholm — "Deep Counterfactual Regret Minimization" (2019)](#paper-1-brown-lerer-gross-sandholm-deep-counterfactual-regret-minimization-2019)
  - [Paper 2: Steinberger — "Single Deep Counterfactual Regret Minimization" (2019)](#paper-2-steinberger-single-deep-counterfactual-regret-minimization-2019)
  - [Paper 3: Heinrich & Silver — "Deep Reinforcement Learning from Self-Play in Imperfect-Information Games" (2016)](#paper-3-heinrich-silver-deep-reinforcement-learning-from-self-play-in-imperfect-information-games-2016)
  - [Supplementary References](#supplementary-references)
  - [Math Flags](#math-flags)
- [Phase 4: Implementation (6 days)](#phase-4-implementation-6-days)
  - [Project: Deep CFR for Leduc Hold'em — From Scratch in PyTorch](#project-deep-cfr-for-leduc-holdem-from-scratch-in-pytorch)
  - [Sub-phase Breakdown (6 days):](#sub-phase-breakdown-6-days)
  - [Deliverables:](#deliverables)
  - [Validation:](#validation)
- [Phase 5: Consolidation (2 days)](#phase-5-consolidation-2-days)
  - [Day 1 — Reference Skim + Gap Fill](#day-1-reference-skim-gap-fill)
  - [Day 2 — One-Pager + Learning Log](#day-2-one-pager-learning-log)
- [Exit Checklist](#exit-checklist)

## Phase 1: Intuition (1 day)

The goal: understand WHY we need neural networks in CFR (tabular CFR can't handle full-scale games even WITH abstraction), what Deep CFR does differently (replaces the regret table with neural networks that generalize across similar states), and where NFSP fits (a completely different approach — RL-based instead of CFR-based). End of day: you should be able to explain to a non-expert: "Instead of memorizing the best strategy for every possible poker situation — which would take more memory than exists on Earth — we train a neural network to PREDICT what the best response would be. It's like learning a general rule instead of memorizing every answer."

### Bridge: Neural Network Foundations for RL

> **Why this section exists:** In Step 1, you implemented DQN and PPO — but the focus was on the RL algorithm, not on WHY neural networks work as function approximators. Before diving into Deep CFR (which replaces tabular regret with neural networks), you need a solid understanding of what a neural network actually computes, how gradient descent trains it, and what happens when you combine function approximation with bootstrapping (the "deadly triad"). This bridge fills the gap between tabular RL (Sutton & Barto Ch 1–6) and the neural methods in Phase C.

**Neural Network Mechanics (~1.5 hours):**

- **3Blue1Brown — "But what is a Neural Network?" (Chapter 1)**
  https://www.3blue1brown.com/lessons/neural-networks
  https://www.youtube.com/watch?v=aircAruvnKk
  Duration: ~19m | Creator: Grant Sanderson
  *Start here. What neurons, weights, biases, and activations actually ARE — introduced through handwritten digit recognition. This grounds the abstract "neural network" concept you've seen in DQN/PPO code (q_network.py's Linear layers, ReLU activations) in concrete visual intuition.*

- **3Blue1Brown — "Gradient descent, how neural networks learn" (Chapter 2)**
  https://www.3blue1brown.com/lessons/gradient-descent
  https://www.youtube.com/watch?v=IHZwWFHWa-w
  Duration: ~21m | Creator: Grant Sanderson
  *How the cost function works and why gradient descent finds good weights. After watching: you'll understand what loss.backward() and optimizer.step() in your DQN train_step actually do — they compute the gradient of the loss and nudge all 33,000+ weights downhill.*

- **3Blue1Brown — "What is backpropagation really doing?" (Chapter 4)**
  https://www.3blue1brown.com/lessons/backpropagation
  https://www.youtube.com/watch?v=Ilg3gGewQ5U
  Duration: ~14m | Creator: Grant Sanderson
  *The intuition behind backpropagation — how each training example "wants" to nudge the weights, and how averaging these desires across a mini-batch gives the gradient. This is exactly what happens inside your DQN's train_step when PyTorch calls .backward().*

- **3Blue1Brown — "Backpropagation calculus" (Chapter 5)**
  https://www.3blue1brown.com/lessons/backpropagation-calculus
  https://www.youtube.com/watch?v=tIeHLnjs5U8
  Duration: ~10m | Creator: Grant Sanderson
  *Optional but recommended: the chain rule math behind backpropagation. If the previous video gave you the intuition, this one gives you the equations. Skip if you're comfortable with the conceptual version.*

**Function Approximation in RL (~1.5 hours):**

- **David Silver — Lecture 6: Value Function Approximation**
  https://www.youtube.com/watch?v=2pWv7GOvuf0&list=PLqYmG7hTraZDM-OYHWgPebj2MfCFzFObQ (Lecture 6 in playlist)
  Slides: https://davidstarsilver.wordpress.com/wp-content/uploads/2025/04/lecture-6-value-function-approximation-.pdf
  Duration: ~1h20m | Instructor: David Silver (DeepMind / UCL)
  *THE bridge lecture. Covers: why tables fail in large state spaces, linear function approximation, neural network approximation, convergence guarantees (and when they break), the deadly triad (function approximation + bootstrapping + off-policy = instability). After watching: you'll understand WHY DQN needs target networks and experience replay — they're engineering patches for the deadly triad. This directly explains the design decisions in your Step 1 implementation.*

**🔗 Connection to Step 1:** After watching these, revisit your DQN code mentally:
- `q_network.py` → the MLP architecture (3Blue1Brown Ch 1)
- `loss.backward()` in `train_step` → backpropagation (3Blue1Brown Ch 4-5)
- `optimizer.step()` → gradient descent (3Blue1Brown Ch 2)
- Target network + replay buffer → deadly triad mitigation (David Silver L6)
- The 33,000+ parameters in your [128,128] network → the weight matrices 3Blue1Brown visualizes

### Videos

- **Stanford CS234 — Lecture 4: Q-learning and Function Approximation (Spring 2024)**  
  https://www.youtube.com/watch?v=b_wvosA70f8  
  Duration: ~1h19m | Instructor: Emma Brunskill (Stanford)  
  *The bridge from tabular to neural: Q-learning, SARSA, and why function approximation is needed when state spaces are too large for tables. The foundational concept that Deep CFR builds on.*

- **Stanford CS224R — Lecture 6: Q-Learning (Spring 2025)**  
  https://www.youtube.com/watch?v=-7kv6jf0isQ  
  Duration: ~1h2m | Instructor: Chelsea Finn (Stanford)  
  *DQN, target networks, experience replay buffers — the practical deep RL building blocks. Covers how to stabilize Q-learning in practice with neural networks.*

- **ReBeL — Combining Deep RL and Search for Imperfect-Information Games (Explained)**  
  https://www.youtube.com/watch?v=BhUWvQmLzSk  
  Duration: ~1h12m | Channel: Yannic Kilcher  
  *Detailed paper explanation covering how neural networks replace tabular CFR: from counterfactual values to learned value functions, public belief states, and the transition from tabular to neural game solving.*

- **Player of Games: All the games, one algorithm! (w/ author Martin Schmid)**  
  https://www.youtube.com/watch?v=U0mxx7AoNz0  
  Duration: ~54m | Channel: Yannic Kilcher  
  *Interview with the author covering how Student of Games unifies Deep CFR-style neural methods for both perfect and imperfect information games (chess, Go, poker, Scotland Yard).*

### Blog Posts

- **Noam Brown's website — Deep CFR summary**  
  https://noambrown.github.io/  
  *Links to all of Brown's major papers with brief descriptions. Scan the Deep CFR entry for a one-paragraph overview.*

- **Papers With Code — "Deep Counterfactual Regret Minimization"**  
  https://paperswithcode.com/paper/deep-counterfactual-regret-minimization  
  *Check for reference implementations and benchmarks. Note: the official implementation is in the Facebook Research repo.*

---

## Phase 2: Exploration (2 days)

### 🎮 Interactive Exploration
- **[TensorFlow Playground](https://playground.tensorflow.org/)** — Tinker with a Neural Network architecture right in your browser to build intuition for continuous approximations.


### Day 1: Deep CFR in OpenSpiel

1. **Run OpenSpiel's Deep CFR on Leduc Hold'em:**
   ```python
   import pyspiel
   from open_spiel.python.algorithms import deep_cfr
   from open_spiel.python.algorithms import exploitability as expl
   import tensorflow as tf  # or torch, depending on OpenSpiel version
   
   game = pyspiel.load_game("leduc_poker")
   
   deep_cfr_solver = deep_cfr.DeepCFRSolver(
       game,
       policy_network_layers=(64, 64),
       advantage_network_layers=(64, 64),
       num_iterations=100,
       num_traversals=100,
       learning_rate=1e-3,
       batch_size_advantage=128,
       batch_size_strategy=1024,
       memory_capacity=int(1e6),
   )
   
   # Train
   _, advantage_losses, policy_loss = deep_cfr_solver.solve()
   
   # Get policy and compute exploitability
   conv = expl.exploitability(game, deep_cfr_solver.policy_network())
   print(f"Deep CFR exploitability: {conv:.6f}")
   ```

2. **Compare against your tabular MCCFR from Step 3:**
   - Run your Step 3 MCCFR for 50k iterations → record exploitability
   - Run OpenSpiel Deep CFR for 100 iterations → record exploitability
   - *Key observation: Deep CFR reaches comparable exploitability with FAR fewer "iterations" but each iteration is more expensive (forward/backward passes). The tradeoff is iterations vs. per-iteration cost.*

3. **Experiment with network sizes:**
   - Try (32, 32), (64, 64), (128, 128, 128) hidden layers
   - How does network capacity affect convergence speed and final exploitability?
   - *Observe: too small → underfitting (can't represent the strategy); too large → slower training, possible overfitting*

### Day 2: NFSP in OpenSpiel + Advantage Network Internals

1. **Run NFSP on Kuhn and Leduc:**
   ```python
   from open_spiel.python.algorithms import nfsp
   
   game = pyspiel.load_game("leduc_poker")
   
   agents = [
       nfsp.NFSP(
           game, player_id=i,
           state_representation_size=game.information_state_tensor_shape()[0],
           num_actions=game.num_distinct_actions(),
           hidden_layers_sizes=[128, 128],
           reservoir_buffer_capacity=int(2e5),
           anticipatory_param=0.1,  # η: mix between best response and average
       )
       for i in range(game.num_players())
   ]
   ```
   - Train for 10k episodes, measure exploitability every 1k
   - *Key observation: NFSP is simpler conceptually (just RL self-play) but converges slower and less precisely than Deep CFR for this game size.*

2. **Inspect advantage network predictions:**
   - After training Deep CFR, feed in specific Leduc info states you know the Nash strategy for
   - Compare the network's predicted advantages against your Step 3 tabular counterfactual values
   - *This grounds the neural approximation — you can SEE what the network learned (or failed to learn)*

3. **Questions to answer by end of Day 2:**
   - What are the three components of Deep CFR? (advantage networks, strategy network, reservoir sampling)
   - How does NFSP differ architecturally from Deep CFR?
   - What role does reservoir sampling play? Why not just use all the data?
   - On Leduc, which method converges faster? Which reaches lower exploitability?

---

## Phase 3: Targeted Reading (3 days)

### Preliminary Reading: Function Approximation Theory

> **Before the papers:** The Deep CFR and NFSP papers assume familiarity with function approximation in RL. These textbook chapters provide the theoretical foundation — read them on Day 1 of this phase before starting the papers.

**Sutton & Barto — Chapter 9: On-policy Prediction with Approximation**
http://incompleteideas.net/book/the-book-2nd.html (free PDF/HTML)
```
├── READ:  9.1 (Value-function Approximation — the general framework),
│          9.2 (The Prediction Objective — what "best approximation" means when
│               you can't represent every state exactly),
│          9.3 (Stochastic Gradient and Semi-Gradient Methods — the core algorithms;
│               this is what DQN's train_step implements),
│          9.5.4 (Nonlinear Function Approximation: ANNs — neural networks as
│                  value approximators, connecting to your Step 1 implementation)
├── SKIM:  9.4 (Linear Methods — useful as contrast to understand what neural
│               networks add beyond linear approximation),
│          9.5 (Feature Construction — how different representations affect
│               learning; relevant for your Leduc state encoding in this step)
├── SKIP:  9.6–9.8 (memory-based methods, kernel-based, interest/emphasis —
│               not needed for Deep CFR)
└── KEY INSIGHT: "Semi-gradient methods (Section 9.3) are what almost all deep RL
    uses in practice. They follow the gradient of the loss with respect to the
    weights, but IGNORE the effect of changing weights on the target. This is
    exactly what DQN does — and it's exactly what Deep CFR's advantage networks do.
    Understanding this 'semi' part explains why target networks are needed."
```

**Sutton & Barto — Chapter 11.1–11.3: The Deadly Triad**
```
├── READ:  11.1 (Off-policy Learning — why learning from old experiences is harder
│               than it sounds; directly relevant to replay buffers),
│          11.2 (Examples of Instability — concrete cases where function
│               approximation + bootstrapping + off-policy diverges),
│          11.3 (The Deadly Triad — the combination of three individually-useful
│               features that together cause instability)
└── KEY INSIGHT: "The deadly triad: (1) function approximation (neural networks),
    (2) bootstrapping (using your own estimates as targets — TD learning),
    (3) off-policy learning (learning from past experiences, i.e., replay buffer).
    DQN has ALL THREE. Deep CFR has (1) and a form of (2). Understanding WHY
    these combine dangerously explains every stabilization trick in deep RL:
    target networks, experience replay, gradient clipping, etc."
```

### Paper 1: Brown, Lerer, Gross & Sandholm — "Deep Counterfactual Regret Minimization" (2019)

https://arxiv.org/abs/1811.00164 (ICML 2019)

```
├── READ:  Section 3 (Deep CFR algorithm — the full specification: how advantage 
│          networks replace tabular regret storage, the training loop with external
│          sampling MCCFR, reservoir sampling for experience replay, and the 
│          strategy network that distills the average policy),
│          Section 4 (Experiments — convergence on Leduc and single-card poker,
│          comparison with tabular CFR and NFSP, scaling results on abstracted HUNL)
├── SKIM:  Abstract, Section 1 (Introduction — motivation for neuralizing CFR),
│          Section 2 (Background — you know CFR/MCCFR from Steps 2–3),
│          Section 5 (Related Work)
├── SKIP:  Nothing — this paper is concise and densely informative
├── MATH:  → "Equation 3 (Advantage network loss function) — understand this. 
│             The advantage network predicts counterfactual values, and the loss
│             is MSE between the network's prediction and the sampled CF values
│             from the traversal. This is where tabular CFR becomes Deep CFR —
│             the rest is architectural scaffolding."
│          → "Section 3.3 (Reservoir Sampling) — understand why uniform-at-random
│             sampling from the buffer approximates the average strategy. This
│             is NOT just 'random replay' — it has theoretical justification."
└── KEY INSIGHT: "Deep CFR is MCCFR where the regret table is replaced by neural
    networks. Each iteration, external-sampling MCCFR generates (info_state, 
    counterfactual_values) training pairs. Advantage networks learn to predict 
    CF values → used for next MCCFR iteration. Strategy network learns the 
    average of all advantage networks → the output Nash approximation. It's 
    'tabular MCCFR with function approximation' — same convergence goal, 
    neural implementation."
```

### Paper 2: Steinberger — "Single Deep Counterfactual Regret Minimization" (2019)

https://arxiv.org/abs/1901.07621  
*(Later published as DREAM framework at AAAI 2020)*

```
├── READ:  Section 3 (Single Deep CFR — how to collapse the separate advantage 
│          networks into one network that handles both players, reducing memory
│          and computation),
│          Section 4 (DREAM extension — outcome sampling instead of external 
│          sampling, with variance reduction techniques),
│          Section 5 (Experiments — convergence comparison on Leduc and HUNL)
├── SKIM:  Abstract, Section 1 (Introduction),
│          Section 2 (Background),
│          Section 6 (Related Work)
├── SKIP:  Proofs in appendix
├── MATH:  → "Algorithm 1 (Single Deep CFR) vs Algorithm 2 (DREAM) — trace both
│             algorithms step by step. The key difference is sampling: Single 
│             Deep CFR uses external sampling (same as Deep CFR), while DREAM 
│             uses outcome sampling + baselines for variance reduction. DREAM 
│             is more practical because outcome sampling is cheaper."
└── KEY INSIGHT: "DREAM is the practitioner's Deep CFR. Single network, outcome 
    sampling, baseline subtraction for variance reduction. If Deep CFR is the 
    'theory paper,' DREAM is the 'engineering paper.' For your thesis 
    implementation, DREAM is likely the better starting point."
```

### Paper 3: Heinrich & Silver — "Deep Reinforcement Learning from Self-Play in Imperfect-Information Games" (2016)

https://arxiv.org/abs/1603.01121

```
├── READ:  Section 3 (Neural Fictitious Self-Play — the two-network architecture:
│          best-response network trained via DQN + average-policy network trained
│          via supervised learning on the replay buffer),
│          Section 4 (Experiments — convergence on Leduc poker)
├── SKIM:  Abstract, Section 1 (Introduction),
│          Section 2 (Background — fictitious play, extensive-form games),
│          Section 5 (Discussion)
├── SKIP:  Section 2.1 if you're comfortable with fictitious play from Step 2
├── MATH:  → "Equation 1 (Anticipatory parameter η) — understand this. η controls 
│             the mixing between best-response play and average-strategy play.
│             η = 0 → pure average strategy (converges to Nash but slowly).
│             η = 1 → pure best response (doesn't converge to Nash, just exploits).
│             η = 0.1 is typically used — mostly average with occasional best-response."
└── KEY INSIGHT: "NFSP approaches equilibrium from the RL side, not the CFR side.
    It doesn't compute regrets at all — it uses DQN for best response and 
    supervised learning for the average strategy. This is elegant but less 
    precise than Deep CFR for equilibrium computation. Its value is as a 
    BRIDGE between RL (Step 1) and game theory (Steps 2–4) — showing that 
    RL can also find Nash equilibria, just differently."
```

### Supplementary References

- **Xu et al. (2025) — "Deep (Predictive) Discounted Counterfactual Regret Minimization" (AAAI 2026)**  
  https://arxiv.org/abs/2511.08174  
  *Combines discounted regret weights (from DCFR) with predictive networks. Claims faster convergence than vanilla Deep CFR. SKIM abstract + Section 3. Log insights for implementation comparison.*

- **Rudolph et al. (2025) — "Reevaluating Policy Gradient Methods for Imperfect-Information Games"**  
  https://arxiv.org/abs/2502.08938  
  *Important perspective: challenges the assumption that naive self-play DRL fails in adversarial IIGs. Shows that with proper hyperparameter tuning, standard policy gradient can perform surprisingly well. SKIM Section 3 (experiments) and Table 1 (comparisons). This reframes the Deep CFR vs RL question.*

- **Zarick et al. (2020) — "Unlocking the Potential of Deep Counterfactual Value Networks"**  
  https://arxiv.org/abs/2007.10442  
  *Practical improvements to Deep CFR's value network training. SKIM abstract + Section 3.*

### Math Flags

🔢 **Deep CFR advantage network loss (Brown et al., Eq. 3)** — Understand the loss function.  
**WHY this can't be substituted:** This equation is the ONLY thing that makes Deep CFR different from tabular MCCFR. The loss defines what the network learns to predict (counterfactual values), and getting it wrong means the network doesn't converge to Nash. When you implement from scratch, this equation IS the core of your training loop.

🔢 **NFSP anticipatory parameter η (Heinrich & Silver, Eq. 1)** — Understand the mixing dynamics.  
**WHY:** η controls the convergence-exploitation tradeoff. For your thesis (opponent exploitation in Step 8), understanding this parameter is key — it's the same tradeoff between playing safe (Nash) and exploiting (best-response). NFSP makes this tradeoff explicit as a single scalar.

---

## Phase 4: Implementation (6 days)

### Project: Deep CFR for Leduc Hold'em — From Scratch in PyTorch

**Language + Framework:** Python 3.10+ / PyTorch (first step using GPU)

Starting point: Your Leduc Hold'em engine from Step 3. Your MCCFR from Step 3 provides the comparison baseline.

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| Information state tensor encoding (Leduc state → fixed-size vector) | 🔴 HAND-CODE | The state representation design is critical for all downstream neural methods. You must decide what features to include (hand, board, action history, pot), how to normalize them, and what dimensionality works. This representation carries through to Steps 6–8. |
| Advantage network architecture (MLP predicting CF values per action) | 🔴 HAND-CODE | The network IS Deep CFR. Understanding the input/output shapes, the loss function (MSE on sampled CF values), and the iterative training loop is the core intellectual content. |
| External-sampling MCCFR traversal → training data generation | 🔴 HAND-CODE | This connects your Step 3 MCCFR to the neural training pipeline. You must understand: each traversal produces (info_state, CF_values) pairs that become training data. The MCCFR logic is identical to Step 3, but now the strategy comes from the neural network instead of a table. |
| Reservoir sampling memory buffer | 🟡 AI-ASSISTED | Reservoir sampling is a well-known algorithm (Vitter 1985). AI drafts it, you verify correctness — that each element has equal probability of being in the buffer. |
| Strategy network (average policy distillation) | 🟡 AI-ASSISTED | Second network that learns the average of all advantage network predictions. Follows the same pattern as the advantage network but with different training data (strategies instead of advantages). |
| NFSP implementation for comparison | 🟡 AI-ASSISTED | You already understand the architecture from the paper. AI drafts the DQN + supervised learning pipeline, you review and verify convergence. The value is in comparing against Deep CFR, not in rebuilding DQN from scratch (done in Step 1). |
| Training loop, hyperparameter search, logging | 🟢 AI-GENERATED | Standard PyTorch training plumbing. |
| Comparison plots (Deep CFR vs MCCFR vs NFSP) | 🟢 AI-GENERATED | Matplotlib visualizations. |

### Sub-phase Breakdown (6 days):

**Day 1 — State Encoding + Advantage Network:**
- 🔴 Design the Leduc information state tensor:
  - Hand card: one-hot (3 values for J/Q/K, or 6 if tracking suits)
  - Community card: one-hot (3 values + "not yet revealed")
  - Action history: fixed-length encoding (sequence of actions, padded)
  - Pot size: normalized float
  - Total: ~20-30 dimensional input vector
- 🔴 Build the advantage network:
  - Input: info state tensor (dim ~25)
  - Hidden: 2 layers of 64 units, ReLU activation
  - Output: CF value per action (dim = num_actions, typically 3: fold/call/raise)
  - Loss: MSE between predicted CF values and sampled CF values from MCCFR traversal
  - One network per player (2 total)

**Days 2–3 — MCCFR Traversal → Neural Training Loop:**
- 🔴 Implement the Deep CFR training loop:
  1. For each iteration t = 1, ..., T:
     a. For player p = 1, 2:
        - Run external-sampling MCCFR traversal using current advantage network's predictions as the strategy
        - Collect (info_state, sampled_CF_values) pairs
        - Store pairs in player p's reservoir buffer
     b. Train each player's advantage network on its reservoir buffer for E epochs
  2. After all T iterations, train the strategy network on the collected average strategies
- 🟡 AI-ASSISTED: Reservoir sampling buffer (ensure uniform-at-random retention)
- Run on Kuhn first (should converge quickly — small game validates the pipeline)
- Run on Leduc — compare exploitability against tabular MCCFR at [100, 500, 1000, 5000] MCCFR iterations vs [10, 50, 100, 200] Deep CFR iterations

**Day 4 — Strategy Network + NFSP:**
- 🟡 AI-ASSISTED: Strategy network — a separate MLP trained on (info_state, average_strategy) pairs. This is the OUTPUT of Deep CFR: the Nash approximation.
- 🟡 AI-ASSISTED: NFSP implementation for Leduc:
  - Best-response network: DQN (from Step 1 knowledge) trained via self-play
  - Average-policy network: supervised learning on replay buffer
  - Anticipatory parameter η = 0.1
- Run NFSP for 100k episodes, measure exploitability every 10k

**Day 5 — Comparison + GPU Profiling:**
- Run full comparison on Leduc:
  | Method | Exploitability | Training Time | Memory |
  |--------|---------------|---------------|--------|
  | Tabular MCCFR (Step 3, 50k iter) | baseline | ? | ? |
  | Deep CFR (100 outer iter) | ? | ? | ? |
  | NFSP (100k episodes) | ? | ? | ? |
  
- Generate convergence plots: exploitability vs training iterations, exploitability vs wall time
- GPU profiling: this is the first step using GPU. Monitor:
  - GPU utilization during training
  - Memory usage per network
  - Training throughput (samples/second)
  - *Log these numbers — they inform compute budget planning for Steps 6+*
- If available: try extending to a larger game (e.g., Extended Leduc from Step 4) and observe how Deep CFR handles it without explicit abstraction

**Day 6 — Validation + Documentation:**
- Cross-validate against OpenSpiel's Deep CFR:
  - Run OpenSpiel Deep CFR on Leduc with matching hyperparameters
  - Compare exploitability and strategy probabilities at specific info states
  - Should agree within ~20% (neural methods have inherent variance)
- Run ablation: what happens if you remove reservoir sampling and just use all data? (Answer: the strategy network overfits to later iterations)
- Document: which method would you choose for Leduc-scale games? For NLHE-scale?

### Deliverables:
- [ ] Information state tensor encoding for Leduc (reusable in Steps 6–8)
- [ ] Deep CFR implementation: advantage networks (2) + strategy network + reservoir sampling + MCCFR traversal
- [ ] NFSP implementation for comparison
- [ ] Convergence comparison: Deep CFR vs tabular MCCFR vs NFSP (exploitability + wall time)
- [ ] GPU profiling report (utilization, memory, throughput)
- [ ] All code committed with README

### Validation:
- **Deep CFR on Kuhn:** Should reach exploitability < 0.01 within 50 iterations. Strategy should match Step 2/3 Nash closely.
- **Deep CFR on Leduc:** Should reach exploitability < 0.1 within 100 iterations. Better than NFSP at equivalent training time.
- **NFSP on Leduc:** Should converge to exploitability < 0.2 within 100k episodes. Slower but less precise than Deep CFR.
- **Cross-validation:** OpenSpiel Deep CFR and your implementation should produce strategies with exploitability within 50% of each other on Leduc (neural stochasticity makes exact matching impossible, but order-of-magnitude should match).

---

## Phase 5: Consolidation (2 days)

### Day 1 — Reference Skim + Gap Fill

- **Reference skim (paper):** Rudolph et al. (2025) "Reevaluating Policy Gradient Methods for IIGs" — read abstract + Section 3 (experiments) + Table 1. *Critical perspective: if naive policy gradient CAN work in IIGs (which this paper argues), what's the TRUE value of Deep CFR over simpler RL approaches? This shapes your thesis methodology decisions.*

- **Reference skim (paper):** Xu et al. (2025) "Deep Predictive Discounted CFR" — read abstract + Section 3. Note: uses discounted regret (from DCFR/LCFR) combined with predictive targets. Could provide a minor implementation improvement. *Forward preview for Step 6.*

- **Forward preview:** Skim Brown et al. (2020) "Combining Deep RL and Search for Imperfect-Information Games" (ReBeL) abstract. *You'll read this fully in Step 6, but see how it builds on value networks similar to Deep CFR.*

- **Forward preview:** Skim Schmid et al. (2023) "Student of Games" abstract. *See how Growing-Tree CFR (GT-CFR) extends the Deep CFR paradigm to both perfect and imperfect info games.*

### Day 2 — One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Update the Learning Log** (`learningLog.md`):
  - **Connections:**
    - [Step 1] DQN (S&B Ch 9 + Mnih 2015) → [Step 5] NFSP uses DQN as its best-response learner. The same replay buffer + target network architecture from Atari now computes best responses in poker.
    - [Step 1] Neural network function approximation → [Step 5] Deep CFR replaces tabular regret storage with MLP advantage networks. Same principle: when the state space is too large for a table, learn a function instead.
    - [Step 3] External-sampling MCCFR → [Step 5] Deep CFR's traversal is IDENTICAL to external-sampling MCCFR, except the strategy at each info state comes from the advantage network instead of a regret table. Same sampling, different lookup mechanism.
    - [Step 3] VR-MCCFR baseline subtraction → [Step 5] DREAM uses similar baseline subtraction for variance reduction. Step 3's optional paper is now directly relevant.
    - [Step 4] Hand-crafted abstraction → [Step 5] Deep CFR's neural approximation REPLACES explicit abstraction. Instead of grouping states by hand, the network learns which states are similar by training on CF values. This is the progression: manual compression (Step 4) → learned compression (Step 5).
    - [Step 5] Advantage networks predict counterfactual values at each info state → prediction: [Step 6] DeepStack's value network does the SAME thing but at the depth-limit boundary of a search tree.
  - **Confusions:**
    - [Step 5] Deep CFR trains advantage networks iteratively — network from iteration t uses strategy from iteration t-1. But each network is trained from scratch on the reservoir buffer, not fine-tuned. Why? Wouldn't fine-tuning be faster? → OPEN (hypothesis: fresh training prevents catastrophic forgetting of early iteration data)
    - [Step 5] NFSP's anticipatory parameter η = 0.1 works for Leduc. Would the same η work for larger games? How to tune it? → OPEN (check in Step 6 when analyzing Pluribus/ReBeL)
    - [Step 3→5] Deep CFR uses external sampling (traverse all own actions, sample opponent). DREAM uses outcome sampling. My Step 3 confusion about external vs outcome sampling tradeoffs now has a concrete answer: in the NEURAL setting, outcome sampling is better because the network generalizes across unvisited states. → PARTIALLY RESOLVED by Step 5

## Exit Checklist

- [ ] Deep CFR implementation working and producing convergent strategies on Leduc
- [ ] NFSP implementation working and producing convergent strategies on Leduc
- [ ] Convergence comparison completed: Deep CFR vs tabular MCCFR vs NFSP
- [ ] Can explain from memory: how advantage networks replace tabular regret (the loss function, the training loop)
- [ ] Can explain from memory: difference between Deep CFR and NFSP architectures
- [ ] Can explain from memory: role of reservoir sampling in Deep CFR
- [ ] GPU profiling completed (know the compute cost of neural methods)
- [ ] Information state encoding designed and documented (reusable for Steps 6–8)
- [ ] Cross-validated against OpenSpiel's Deep CFR
- [ ] All 🔴 components hand-coded
- [ ] One-pager written and committed
- [ ] Learning Log updated (connections from Steps 1–4 + new confusions + resolved confusions)
- [ ] Step notes committed to repo
