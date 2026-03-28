# Step 5 — Neural Equilibrium Approximation (Deep CFR, DREAM)

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 1 (RL Basics), Step 3 (CFR Variants + MC Methods), Step 4 (Game Abstraction + Scaling)  
**Phase:** C — Neural Methods for Games  
**Freshness Note:**  
- ArXiv search: "deep counterfactual regret minimization" sorted by date (Mar 2026) — 19 results total  
- ArXiv search: "neural fictitious self play imperfect information" (Mar 2026) — 4 results total  
- Notable recent papers:  
  - Xu et al. (Nov 2025) "Deep (Predictive) Discounted Counterfactual Regret Minimization" — accepted AAAI 2026. Combines discounted regret weights with predictive neural networks for faster convergence. *Add as supplementary — directly extends Deep CFR.*  
  - Rudolph et al. (Feb 2025) "Reevaluating Policy Gradient Methods for Imperfect-Information Games" — challenges the assumption that naive self-play DRL fails in adversarial IIGs. *Add as supplementary — bridges Step 1 RL to Step 5 game solving, important perspective.*  
  - SpinGPT (Maugin & Cazenave, Sep 2025) "A Large-Language-Model Approach to Playing Poker Correctly" — LLM + CFR hybrid, ACG 2025. *Log for Step 12 (LLM agents).*  
  - Chen et al. (May 2023, updated Nov 2025) "Hierarchical Deep Counterfactual Regret Minimization" — hierarchical state abstraction for Deep CFR. *Log as optional supplementary.*  
- Core resources unchanged: Brown et al. (2019) Deep CFR, Steinberger (2019) Single Deep CFR / DREAM, Heinrich & Silver (2016) NFSP remain the canonical references.  
- No superseded content for Step 5 scope.

---

## Phase 1: Intuition (1 day)

The goal: understand WHY we need neural networks in CFR (tabular CFR can't handle full-scale games even WITH abstraction), what Deep CFR does differently (replaces the regret table with neural networks that generalize across similar states), and where NFSP fits (a completely different approach — RL-based instead of CFR-based). End of day: you should be able to explain to a non-expert: "Instead of memorizing the best strategy for every possible poker situation — which would take more memory than exists on Earth — we train a neural network to PREDICT what the best response would be. It's like learning a general rule instead of memorizing every answer."

### Videos

- **Noam Brown — "Deep Counterfactual Regret Minimization" (ICML 2019)**  
  https://www.youtube.com/watch?v=jIAZGz7wN3I  
  Duration: ~15m | Speaker: Noam Brown  
  *Brown's own presentation of Deep CFR at ICML 2019. Concise explanation of: why tabular CFR can't scale to NLHE, how advantage networks approximate counterfactual regret, how reservoir sampling creates training data, and the key experiments on poker.*

- **Eric Steinberger — "Single Deep CFR / DREAM"**  
  https://www.youtube.com/watch?v=YJO3-bMKvnI  
  Duration: ~20m | Speaker: Eric Steinberger  
  *Steinberger explains how DREAM simplifies Deep CFR: single network instead of separate advantage + strategy networks, lower variance through tighter sampling. More practical to implement.*

- **Johannes Heinrich — "Deep RL from Self-Play in Imperfect-Information Games" (NIPS 2016 workshop)**  
  https://www.youtube.com/watch?v=qndXrHcV1sM  
  Duration: ~25m | Speaker: Johannes Heinrich  
  *Heinrich introduces NFSP — Neural Fictitious Self-Play. The key insight: instead of using CFR at all, use two neural networks (best-response + average strategy) that play against each other, converging to Nash via fictitious play. Totally different architecture from Deep CFR.*

### Blog Posts

- **Noam Brown's website — Deep CFR summary**  
  https://noambrown.github.io/  
  *Links to all of Brown's major papers with brief descriptions. Scan the Deep CFR entry for a one-paragraph overview.*

- **Papers With Code — "Deep Counterfactual Regret Minimization"**  
  https://paperswithcode.com/paper/deep-counterfactual-regret-minimization  
  *Check for reference implementations and benchmarks. Note: the official implementation is in the Facebook Research repo.*

---

## Phase 2: Exploration (2 days)

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

### Paper 1: Brown, Lerer, Gross & Sandholm — "Deep Counterfactual Regret Minimization" (2019)

**Link:** https://arxiv.org/abs/1811.00164 (ICML 2019)

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

**Link:** https://arxiv.org/abs/1901.07621  
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

**Link:** https://arxiv.org/abs/1603.01121

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

### PhD Connection

This step feeds **Contribution #1 (Behavioral Adaptation Framework)** directly: Deep CFR's advantage networks are the technical mechanism for computing baseline strategies in games too large for tabular CFR. The information state encoding designed here (tensor representation of game state) becomes the foundation for the opponent modeling input in Step 7. NFSP's anticipatory parameter η foreshadows the exploitation-safety tradeoff central to Step 8 and the thesis.

---

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
