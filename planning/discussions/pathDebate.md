# Path Debate: 15-Step PhD Preparation Roadmap

> **Purpose:** Establish consensus on two questions about a PhD preparation roadmap in *Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments*. This document is the starting position. Other LLM inputs will be appended until consensus is reached.
>
> **Debate Point 1:** Is this the correct PhD focus to pursue — given the candidate's profile, the academic landscape, and the career opportunities it unlocks?
>
> **Debate Point 2:** Given that (1) is settled, is the proposed 15-step path the best-suited preparation sequence for the timeframe (28 weeks, April–October 2026)?
>
> **Out of scope:** Learning methodology, day allocation, phase structure, AI-assistance rules. We are debating *what* to research and *what* to study — not *how* to study it.

---

## 1. Ultimate Goal

**By mid-October 2026, possess the complete technical foundation to:**

1. **Design and execute** three thesis contributions:
   - A Behavioral Adaptation Framework (detect → adapt → exploit from behavioral traces)
   - Multi-Agent Safe Exploitation (extend 2-player safety guarantees to N-player games)
   - A unified Evaluation Methodology (exploitability + population ranking + statistical confidence)

2. **Write Chapter I** (state of the art, ~30 pages) by November 2026 with no knowledge gaps.

3. **Draft the first publication** (evaluation framework on Kuhn + Leduc, targeting a workshop paper) by end of November 2026.

The PhD defense is April 2029. The learning phase ends October 2026. Everything after is research + writing + publishing. The path must therefore cover every technical prerequisite — algorithms, theory, implementation skill, and evaluation tools — so that the research phase can begin without backtracking.

---

## 2. Debate Point 1 — Is This the Right PhD Focus?

### 2.1 Candidate Profile

- **Alexander Andreev**, Ruse University "Angel Kanchev" — PhD in Informatics (4.6)
- 10 years of software engineering experience
- Current/recent industry: Playtech (iGaming) — direct access to real-world poker behavioral data
- Supervisors: Prof. Dr. Tsvetomir Vasilev, Assoc. Prof. Dr. Rumen Rusev
- Enrolled: 18.02.2026 | Phase 1 Deadline: 11.2026 | Defense: 04.2029
- Completed foundations: DQN, PPO, Gym (RL basics) + vanilla CFR on Kuhn Poker (game theory basics)

### 2.2 The Thesis Framing

**"Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments"**

Three planned contributions:
1. **Behavioral Adaptation Framework** — infer and adapt to opponent strategies from observed actions in real-time
2. **Multi-Agent Safe Exploitation** — extend safe exploitation guarantees from 2-player zero-sum to N-player settings
3. **Evaluation Methodology** — a unified framework for measuring agent adaptability and robustness across game types

### 2.3 Why This Focus Is Correct

**Academic alignment:**
- Game-theory themed (satisfies the university's informatics program expectations)
- Algorithms are generalized beyond poker — applicable to any multi-agent strategic interaction (satisfies supervisors' preference for generality)
- Multi-agent safe exploitation is explicitly flagged as an open frontier ("one of the most lucrative unsolved problems" per the OX-Search literature)
- Scope is tractable for 3 years — targets specific sub-problems (3-player Kuhn, piKL heuristic, equal share baseline) rather than a general N-player safety theorem

**Industrial alignment:**
- The word "poker" doesn't appear in any thesis contribution. Poker is merely one experimental domain.
- The same framework applies to: cybersecurity (adversarial network agents), market making (competing trading agents), autonomous driving (multi-agent navigation), fraud detection (modeling adversarial actors)
- This generality is what makes the PhD future-proof against AI automation — the candidate designs strategic architecture, not trains models

### 2.4 Career Paths This PhD Unlocks

Validated against 10 real job postings (Glassdoor, March 2026):

#### Path A — MARL / AI Solutions Architect (Primary)

| Role (Real Posting) | Salary | Steps That Hit | Key Skills Matched |
|---------------------|--------|----------------|--------------------|
| Serve Robotics — RL Lead | $160–300k | 5, 6, 9, 10 | Neural game architectures, MARL, population training |
| GM — Vehicle AI Staff Engineer | $189–290k | 5, 6, 9 | Multi-agent coordination, neural equilibrium |
| PARTech — AI Engineer | $200–215k | 5, 6, 7, 9 | Opponent modeling, MARL, neural methods |
| Zillow — Principal ML Engineer | $204–327k | 5, 7, 13 | Behavioral modeling, real-world data pipelines |
| Cloud Resources — AI Solutions Architect | Unlisted | 6, 9, 14 | System architectures, evaluation, multi-agent |

**PhD + 10 YOE SWE = rare combination.** Most MARL researchers lack production engineering depth; most engineers lack the game-theoretic foundation. The B2B consultancy route (Bulgaria-based, €140–220k) is uniquely enabled by this profile.

#### Path B — Fraud / Risk / Adversarial AI (Co-Primary)

| Role (Real Posting) | Salary | Steps That Hit | Key Skills Matched |
|---------------------|--------|----------------|--------------------|
| Whatnot — ML Scientist, Risk & Fraud | $245–345k | 7, 8, 12, 13 | Opponent modeling, safe exploitation, behavioral data |
| Adobe — Sr AI/ML Engineer, Fraud | $143–271k | 7, 8, 13 | Adversarial modeling, behavioral pipelines |
| PayPal — Staff ML Engineer, Fraud | $179–265k | 7, 8, 12, 13 | Exploitation detection, sequence models |
| Home Depot — Staff Engineer, Fraud | $140–220k | 7, 8, 13 | Adversarial detection, behavioral analysis |
| Intuit — Staff AI Engineer, Fraud | $202–278k | 7, 8, 13, 14 | Safe exploitation, evaluation, behavioral data |

**Natural Playtech bridge.** The PhD's opponent modeling + safe exploitation research maps 1:1 to adversarial detection and bot/fraud identification. The candidate has existing industry access.

#### Path C — iGaming/Fintech Consultancy

- PhD research directly produces a behavioral analysis + collusion detection pipeline (Step 13) on real Playtech data
- This is a publishable AND commercializable artifact
- Collusion detection in online poker is an unsolved industry problem with few academic solutions
- Publication title direction: "Behavioral Analysis and Collusion Detection in Online Poker via Transformer-Based Player Embeddings"

#### Path D — Web3/DeFi MEV Research (Opportunistic)

- Multi-agent adversarial strategy in competitive environments → MEV extraction / sandwich attack detection
- Pays well but crypto is volatile — keep as opportunistic, not primary

#### Path E — Indie Game AI (Lottery Ticket)

- MARL + opponent modeling → credible game AI that adapts to player skill
- Correctly identified as low-probability, high-upside

### 2.5 Coverage Analysis

**Steps 7–8 (Opponent Modeling + Safe Exploitation) hit 9/10 job postings** — they are the highest-value steps for career ROI.

**Dual-path safety:** The PhD is designed so the candidate has TWO high-probability career paths (MARL Architect + Fraud/Risk AI), not just one. If the MARL consulting market is slow, the fraud path is immediately accessible via Playtech connections.

**Identified gaps (for debate):**
- 5/10 jobs mention production/MLOps deployment skills — out of scope for the learning phase, flagged for post-PhD development
- 3/10 jobs mention LLM fluency — addressed in Step 12 (10-day survey)
- No jobs in the sample require mechanism design or auction theory — supporting the decision to exclude these

### 2.6 Could Re-Steering Unlock More Potential?

Three alternative PhD foci were considered and rejected:

| Alternative Focus | Upside | Why Rejected |
|-------------------|--------|--------------|
| **Pure LLM agents for games** | Hotter market (2025–26), more LLM job postings | Field is too young — no stable theoretical foundation to build a 3-year thesis on. Risk of being scooped by industry labs (Meta, Google). No clear contribution beyond prompt engineering. |
| **Pure MARL without game-theory grounding** | Broader applicability to robotics, autonomous systems | Loses the adversarial/exploitation angle that uniquely maps to fraud/risk roles and differentiates from the hundreds of MARL PhDs at top schools. Without game theory, the PhD is competing with DeepMind/FAIR alumni — unwinnable. |
| **Pure poker AI** | Clean benchmark, well-understood literature | Career ceiling. "Poker AI" on a CV is niche. The game-theoretic framing ("adaptive strategy in multi-agent imperfect-information environments") makes the same work applicable to cybersecurity, finance, autonomous systems, and fraud — without changing the research. |

**Verdict on re-steering:** The current framing is the sweet spot. It's specific enough to produce real contributions (safe exploitation in N-player games is genuinely unsolved) but general enough to map to multiple high-paying career paths. Re-steering toward LLMs adds trend-risk. Re-steering toward pure MARL loses the exploitation angle that makes the candidate distinctive.

### 2.7 Partnership Contingency (Oxford Coop Plan)

A potential partnership plan (B2B with an Oxford MBA candidate) was evaluated:
- **If partner is accepted:** B2B Fraud/AML Engine is the best joint target (€30–80k first contracts, scaling to €100–300k)
- **If partner is rejected:** The PhD career plan is fully self-sufficient — no dependency on the partnership
- **Critical design principle:** The PhD must work whether the partnership materializes or not. The current path satisfies this.

### 2.8 Open Questions on Focus (Debate Point 1)

1. **Is the adversarial/exploitation angle genuinely differentiating, or will the market commoditize it by 2029?** Frontier AI labs are working on this. Counter-argument: they're working on scale (full poker, Diplomacy), not on formal safety guarantees for N-player — which is the thesis niche.

2. **Should the PhD lean harder into the fraud/risk application to secure commercial value?** E.g., make Playtech collaboration a thesis chapter, not just a data source. Counter-argument: over-specializing to iGaming limits the generality claim.

3. **Is the "evaluation methodology" (Contribution #3) strong enough as a standalone thesis contribution, or is it supporting infrastructure?** Counter-argument: VasE + AIVAT + cross-game validation is genuinely novel as a unified framework — no one has done it.

4. **Does the candidate's Bulgarian university affiliation limit career opportunities compared to a top-10 CS school?** Counter-argument: the 10 YOE SWE + publications + real-world Playtech validation compensate. Reviewers care about the work, not the institution, for industry roles.

---

## 3. Debate Point 2 — Is the Path Best-Suited for the Timeframe?

### 3.1 Defense of the Current Path

#### Why this ordering is correct

The 15 steps follow a strict **dependency chain** dictated by the mathematics:

1. **You cannot do opponent modeling (Step 7) without knowing what an equilibrium is (Steps 2–4) and how it's computed at scale (Steps 5–6).** Modeling deviations from equilibrium requires understanding the equilibrium itself.

2. **You cannot do safe exploitation (Step 8) without opponent modeling (Step 7).** Safe exploitation is the constrained optimization: maximize profit from the opponent model subject to a safety floor. No model → nothing to exploit.

3. **You cannot extend to N-player (Steps 9–11) without the 2-player theory (Steps 7–8).** The thesis contribution is precisely identifying *where* the 2-player proofs break for N>2. You must know the proofs before you can break them.

4. **You cannot build evaluation frameworks (Step 14) without the agents and games to evaluate (Steps 3–13).** The evaluation framework is validated cross-game; the games and agents come from prior steps.

5. **You cannot map the research frontier (Step 15) without completing the full landscape survey (Steps 1–14).**

#### Why the scope is correct

- **Steps 1–2 (done):** RL + game theory foundations. Non-negotiable prerequisites.
- **Steps 3–4:** CFR scaling + game abstraction. Without these, you can't work on games larger than Kuhn Poker. Every subsequent step needs Leduc or larger.
- **Step 5:** Neural equilibrium methods. The bridge from tabular to scalable. Deep CFR and NFSP are the technical predecessors of every modern game AI system.
- **Step 6:** End-to-end architectures (DeepStack → Libratus → Pluribus → ReBeL → Student of Games). This is the state of the art. Skipping this means writing a literature review with blind spots.
- **Steps 7–8 (thesis core):** Opponent modeling + safe exploitation. These two steps *are* Contribution #1. They get maximum time (3 weeks each) because they define the PhD.
- **Steps 9–11:** Multi-agent extension. MARL fundamentals → population training → coalition formation. This is Contribution #2. The ordering goes from general (MARL algorithms) to specific (coalition dynamics in FFA).
- **Steps 12–13:** Data-driven bridge. Sequence models + LLM survey + Playtech pipeline. Connects theory to real-world data. Step 12 is lighter (10 days) because the LLM-in-games field is too young for deep study — a survey suffices.
- **Steps 14–15:** Integration. Evaluation framework (Contribution #3) + research plan. These are the capstone steps that turn the learning phase into a research plan.

#### Why nothing should be removed

Every step maps to at least one thesis contribution or is a prerequisite for one:

| Step | Maps to |
|------|---------|
| 1–2 | Universal prerequisite |
| 3–4 | Prerequisite for Steps 5–8 (can't work on large games without abstraction/scaling) |
| 5 | Prerequisite for Step 6 (neural methods used in all modern architectures) |
| 6 | Literature review completeness + ReBeL PBS framework used in Contribution #1 |
| 7 | Contribution #1 core (behavioral adaptation "sensor") |
| 8 | Contribution #1 core (safe exploitation "actuator") + Contribution #2 starting point |
| 9 | Prerequisite for Steps 10–11 (MARL vocabulary) |
| 10 | Contribution #2 (population-level safety) + Contribution #3 (EGTA evaluation) |
| 11 | Contribution #2 (N-player coalition dynamics, the frontier) |
| 12 | Contribution #1 (sequence model encoding for behavioral data) + literature coverage |
| 13 | Contribution #1 (real-world validation via Playtech) + Contribution #3 prototype |
| 14 | Contribution #3 core (evaluation framework) |
| 15 | Synthesis + research plan design |

#### Why nothing critical is missing

Potential objections addressed:

- **"Where is game theory beyond zero-sum?"** — Covered in Steps 9 (MARL general-sum), 10 (evolutionary GT), 11 (cooperative GT / Shapley value). The zero-sum focus in Steps 2–8 is deliberate: the thesis extends *from* zero-sum safety *to* N-player.
- **"Where are Dec-POMDPs / partial observability theory?"** — Implicitly covered through imperfect-information game formalism (Steps 2, 6, 7). Explicit Dec-POMDP theory is not needed because the thesis operates within the extensive-form game framework, not the POMDP framework.
- **"Where is mechanism design?"** — Out of scope. The thesis designs agents that play within given game rules, not the rules themselves.
- **"Where is large-scale engineering / MLOps?"** — Out of scope for the learning phase. Flagged as post-PhD skill development.

---

### 3.2 Condensed Technical Content per Step

### Step 1 — RL Basics ✅ (Done)
- Markov Decision Processes (MDPs), Bellman equations
- Tabular methods: dynamic programming, Monte Carlo, TD learning (TD(0), SARSA, Q-learning)
- Policy gradient: REINFORCE with baseline
- Deep Q-Network (DQN): experience replay, target networks, ε-greedy
- Proximal Policy Optimization (PPO): actor-critic, GAE, clipped surrogate objective
- Environments: CartPole, LunarLander (Gymnasium)

### Step 2 — Game Theory + CFR Basics ✅ (Done)
- Extensive-form games: game trees, information sets, strategies (behavioral vs. mixed)
- Solution concepts: Nash equilibrium, best response, exploitability
- Regret matching and regret minimization
- Counterfactual Regret Minimization (CFR): counterfactual values, recursive tree traversal, strategy accumulation
- Convergence: O(1/√T) average regret bound
- Implementation: Kuhn Poker engine, vanilla CFR solver, best-response calculator, exploitability evaluator

### Step 3 — CFR Variants + Monte Carlo Methods
- Monte Carlo CFR (MCCFR): external sampling, outcome sampling, chance sampling
- Unbiased estimation of counterfactual values via sampling
- Convergence-variance tradeoff across sampling schemes
- CFR+: regret floor, alternating updates, linear averaging → empirical O(1/T) convergence
- Variance reduction baselines (VR-MCCFR)
- Implementation: Leduc Hold'em engine (~936 info sets), all MCCFR variants, CFR+, four-way convergence comparison

### Step 4 — Game Abstraction + Scaling
- Lossless abstraction: ordered game isomorphisms (GameShrink algorithm)
- Lossy abstraction: card bucketing (hand-strength clustering), configurable granularity
- Earth Mover's Distance (EMD) as abstraction quality metric
- Action abstraction: bet-size restriction + action translation for out-of-abstraction actions
- Imperfect-recall abstractions with provable error bounds
- Subgame solving with safety guarantees (safe and nested)
- Abstraction quality–exploitability Pareto frontier analysis
- Implementation: lossless/lossy/action abstraction pipeline, Extended Leduc (~5000+ info sets)

### Step 5 — Neural Equilibrium Approximation
- Deep CFR: advantage networks (MLP), reservoir sampling, external-sampling MCCFR traversals, strategy network for average policy distillation
- Single Deep CFR / DREAM: single-network variant, outcome sampling with baseline variance reduction
- Neural Fictitious Self-Play (NFSP): DQN best-response + supervised average-policy, anticipatory parameter η
- Information state tensor encoding design (reusable in Steps 6–8)
- GPU training pipeline establishment
- Implementation: Deep CFR + NFSP on Leduc, three-way convergence comparison (Deep CFR vs tabular MCCFR vs NFSP)

### Step 6 — End-to-End Game AI Architectures
- DeepStack: continual re-solving, deep counterfactual value networks
- Libratus: modular architecture (MCCFR blueprint + real-time subgame solving + self-improvement)
- Pluribus: 6-player NLHE, depth-limited search, modified RBP, empirical multiplayer equilibrium
- ReBeL: Public Belief States (PBS), Bayesian update mechanics, PBS-CFR local solver, self-play training loop with neural value estimation
- Student of Games: Growing-Tree CFR (GT-CFR), unified perfect/imperfect-information framework
- Depth-limited solving theory: exploitability bounds for value estimation errors
- Implementation: ReBeL-Lite on Leduc (PBS representation + PBS-CFR + value network + self-play loop), architecture comparison framework

### Step 7 — Opponent Modeling
- Bayesian opponent modeling: Dirichlet-multinomial priors, likelihood from observed actions, posterior updates under partial observability
- Type-based models: discrete opponent types, posterior concentration
- Continuous parametric models: per-info-set action distribution estimation
- Implicit agent modeling: strategy adapts to observations without explicit beliefs
- Consistent opponent modeling: sequence-form projected gradient descent, guaranteed convergence to true strategy
- Multiplayer opponent modeling: joint modeling of N opponents, exploitation ≠ sum of individual best responses
- Non-stationarity: opponent type switching, model robustness
- Implementation: opponent type library, observation buffer, three opponent models (type-based, continuous, consistent), adaptive exploitation pipeline

### Step 8 — Safe Exploitation
- Exploitation-safety tradeoff: naive best-response vulnerability, teaching attacks
- Restricted Nash Response (RNR): LP formulation, safety parameter p interpolation
- Ganzfried Safety Theorem: worst-case EV ≥ Nash value, proof via minimax theorem, 2-player zero-sum requirement
- ε-safety (prime-safe exploitation): adjusted safety floor for approximate equilibrium baselines
- Adaptation Safety: exploitability(σ_exploit) ≤ exploitability(σ_blueprint)
- Subgame exploitation (SES): gadget construction converting global safety to local constraint
- OX-Search: per-info-set exploitation bounds, teaching attack neutralization
- Depth-limited exploitation (ABD): strategy-portfolio approach, matrix-valued states beyond depth limit
- **Critical identification:** exact failure point of safety proofs for N>2 (minimax theorem dependency)
- Implementation: safety checker, RNR solver, Ganzfried solver, prime-safe extension, SES-style solver, adaptation safety checker, full pipeline (Step 7 models → Step 8 exploitation), teaching attack stress test, Pareto frontier plots

### Step 9 — Multi-Agent RL
- MARL challenges: non-stationarity, credit assignment, coordination problem
- Centralized Training with Decentralized Execution (CTDE): MADDPG (centralized critic), QMIX (monotonic value decomposition), MAPPO (centralized value function)
- Policy Space Response Oracles (PSRO): double-oracle framework, meta-Nash, policy population
- Learning with Opponent-Learning Awareness (LOLA): differentiating through opponent's learning update
- Emergent communication (CommNet): differentiable inter-agent messaging
- Implementation: matrix game testbed (PD, Matching Pennies, Stag Hunt, BoS), independent learners, MADDPG, MAPPO, PSRO (verified on Kuhn), CommNet

### Step 10 — Population-Based Training + Evolutionary Game Theory
- Population-Based Training (PBT): parallel population co-evolution of weights + hyperparameters
- AlphaStar league: three-role architecture (main agents, main exploiters, league exploiters), prioritized matchmaking
- Replicator dynamics: continuous-time selection dynamics, phase portraits
- Evolutionary Stable Strategies (ESS): Nash refinement under evolutionary perturbation
- Spinning top decomposition: transitive (skill) vs cyclic (non-transitive) payoff structure separation
- Empirical Game-Theoretic Analysis (EGTA): finite-strategy meta-game, meta-Nash over population
- Implementation: replicator dynamics simulator, spinning top decomposition, PBT league for Leduc (3 roles), EGTA analysis, Elo tracking

### Step 11 — Coalition Formation in FFA Games
- So Long Sucker (SLS): 4-player coalition formation game (Nash/Shapley/Shubik benchmark)
- Cooperative game theory: Shapley value, the core, nucleolus, coalition stability
- Coalition detection: help/harm matrices from behavioral observations, implicit alliance inference
- Shapley Q-value: credit assignment via marginal coalition contributions in competitive FFA
- piKL regularization: behavioral-prior-based safety replacing intractable Nash in N-player games
- N-player EGTA: 4-player payoff tensor, meta-Nash, spinning top adapted for N-player
- Implementation: SLS environment (verified), coalition detection module, Shapley credit assignment, coalition-aware MAPPO training, meta-game analysis

### Step 12 — Sequence Models + LLM Agents
- Decision Transformer: offline RL as return-conditioned sequence prediction (GPT-2 backbone)
- Trajectory Transformer: full-sequence modeling with beam search planning
- Stochasticity limitation: return conditioning conflates luck and skill in card games
- Adversarially Robust Decision Transformer (ARDT): minimax expectile regression → recovers Nash from offline data
- Conservative Q-Learning (CQL): pessimistic offline RL baseline
- LLM agents in games: theory-of-mind reasoning, TextArena benchmark (57+ games), CICERO architecture
- Poker state tensor encoding: cards, position, pot, stacks, betting history → fixed-dimension vector
- Implementation: poker trajectory dataset (50K+ Kuhn hands), DT training, ARDT implementation, LLM evaluation on TextArena + Kuhn, multi-paradigm comparison (CFR vs DT vs ARDT vs BC vs LLM)

### Step 13 — Behavioral Analysis Pipelines + Real-World Data
- Playtech hand history parsing → structured records → state tensors
- Player statistics: VPIP, PFR, Aggression Factor, WTSD, W$SD, 3-bet%, C-bet%
- Behavioral cloning: neural action prediction from game state
- player2vec: Transformer encoder with masked action prediction → per-player behavioral embeddings
- Style classification: k-means (TAG, LAG, Nit, Fish archetypes) + DBSCAN on embedding space
- Collusion detection: co-occurrence anomaly, chip dumping score, soft play score, composite scoring
- Decision Transformer on real poker data: EV-conditioned vs outcome-conditioned training
- Implementation: end-to-end pipeline from Playtech data → embeddings → classification → collusion detection

### Step 14 — Evaluation Frameworks + Exploitability Metrics
- Layer 1 — Exploitability: exact (game tree traversal), approximate (RL-based best response / ISMCTS-BR), adaptation safety metric
- Layer 2 — Population ranking: Elo (baseline), α-Rank (evolutionary dynamics / Markov-Conley chains), VasE (social choice theory / maximal lotteries), meta-Nash (EGTA)
- Layer 3 — Statistical confidence: AIVAT variance reduction (counterfactual value control variates), bootstrapped confidence intervals, sample complexity bounds
- Spinning top decomposition as diagnostic (when does Elo suffice vs when are game-theoretic methods needed?)
- N-player exploitability extension: marginal exploitability
- Bot zoo construction: trivial / heuristic / computed / advanced agent tiers
- Implementation: three-layer API, α-Rank, VasE/LP, AIVAT, cross-game validation (Kuhn, Leduc, SLS, Playtech data)

### Step 15 — Research Frontier Mapping + Contribution Design
- Gap validation: confirm all three contribution gaps against recent literature (NeurIPS/ICML/ICLR 2025–26, AAAI 2026, recent dissertations)
- Contribution #1 design: detect → adapt → exploit closed-loop pipeline specification
- Contribution #2 design: N-player safety definitions (piKL, equal share baseline, adaptation safety extension), experimental protocol on 3-player Kuhn/Leduc + SLS
- Contribution #3 design: three-layer evaluation framework cross-game validation protocol
- Experimental programme: 4 experiments with falsifiable hypotheses
- Publication pipeline: 4–6 papers mapped to 4 dissertation chapters, venues, deadlines
- Chapter I outline: 7 sections, 25–30 pages
- First publication draft plan

---

### 3.3 Open Questions on Path (Debate Point 2)

The following are the aspects of the path most likely to benefit from challenge:

1. **Is Step 12 (Sequence Models + LLM Agents) worth 10 days, or should it be cut/merged?** The LLM-in-games field is immature. Counter-argument: ARDT directly enables learning safe strategies from offline data (alternative path for Contribution #2), and the poker state encoding feeds Step 13.

2. **Should Step 11 (Coalition Formation / SLS) be its own step or merged into Step 9/10?** It covers a frontier topic with very little prior work. Counter-argument: SLS is the only N-player competitive FFA benchmark, so it's essential for Contribution #2. Merging would reduce depth.

3. **Is there a faster path through Steps 3–6?** Four steps to reach the architecture survey feels methodical. Counter-argument: each step builds a specific capability needed later (MCCFR → abstraction → neural approx → full architecture). Skipping any creates gaps in the Chapter I story.

4. **Should mechanism design or auction theory appear anywhere?** The thesis claims domain-generality but doesn't cover mechanism design. Counter-argument: the thesis designs agents, not games. Mechanism design is a different problem class.

5. **Is the N-player extension (Contribution #2) realistic for a 3-year PhD?** The open problem is explicitly unsolved. Counter-argument: the plan targets tractable sub-problems (3-player Kuhn, piKL heuristic, equal share baseline) rather than a general N-player safety theorem.

6. **Should there be a dedicated step for Dec-POMDPs or partial observability theory?** The thesis works within imperfect-information extensive-form games. Counter-argument: Dec-POMDP theory is a different formalism; the thesis doesn't need it, but a reviewer might ask why.

---

---

## 4. Positions Log

### Position A, March 29 2026

**On Debate Point 1 (Is this the right focus?):**
Verdict: **Yes.** The framing is the best available for this candidate. The adversarial/exploitation niche is genuinely underserved (no competing PhD programs focus specifically on N-player safe exploitation with formal guarantees). The dual career path (MARL Architect + Fraud/Risk AI) provides safety. The general framing ("adaptive strategy in imperfect-information environments") avoids the poker-AI career ceiling while keeping poker as the testbed. Re-steering toward LLMs or pure MARL would sacrifice the differentiating angle.

**On Debate Point 2 (Is the path correct?):**
Verdict: **Yes, with minor concerns.** The dependency chain is mathematically dictated and correctly ordered. The three thesis contributions are traceable through the steps. The scope is aggressive but feasible for 28 weeks + 2.5-week buffer.

Minor concerns:
- Step 12's value is primarily as a bridge (state encoding → Step 13) and literature coverage (LLMs in games). If time pressure emerges, it's the most compressible step.
- Step 11's reliance on a single benchmark game (SLS) is a risk. If SLS proves too complex or uninteresting, the step has no fallback. Goofspiel or a custom N-player game could serve as backup.
- The path is maximally front-loaded with theory (Steps 3–8) and back-loaded with application (Steps 12–14). If motivation patterns favor variety, consider interleaving a lighter application task mid-path. However, this would break the dependency chain, so the current ordering is technically correct even if psychologically demanding.
- The career coverage is strongly concentrated on Steps 7–8 (9/10 postings). If those steps go poorly, the career value of subsequent steps diminishes. This is a feature (correctly prioritized) not a bug, but it does mean Steps 7–8 are the non-negotiable core.

### Position B, March 29 2026

**On Debate Point 1 (Is this the right focus?):**
Verdict: **Yes, heavily optimized for the candidate's unique advantages.** The transition from iGaming software engineering to MARL/Fraud AI is a highly credible narrative. By framing the research around "Adaptive Strategy," the candidate avoids being pigeonholed as a "poker researcher" while fully leveraging their domain expertise and data access. 
*A critical nuance:* Contribution #3 (Evaluation Methodology) must be carefully framed. To be a strong PhD contribution, it cannot merely be "a new benchmark tool"; it must demonstrate *why* existing evaluation metrics fail to capture the nuances of N-player safe exploitation and adaptability.

**On Debate Point 2 (Is the path correct?):**
Verdict: **Yes, but with a structural risk regarding data assumptions.** The mathematical dependency chain is undeniable. However, there is a practical risk in delaying the real-world data pipeline (Step 13) until the end of the theoretical progression.
*Key Challenges:*
- **The Data Reality Gap:** Steps 7 and 8 deal with formal opponent modeling and safe exploitation computationally. If Step 13 reveals that the real Playtech data lacks the necessary granularity or exhibits partial observability noise that breaks the assumptions of the models built in Step 7, significant backtracking will be required. A "data reality check" should arguably be front-loaded or run concurrently to ensure the theory aligns with the available data.
- **The LLM Distraction:** Step 12 (Sequence Models + LLM Agents) risks being a tangent. While sequence modeling (Decision Transformers) has relevance, surveying LLMs simply because they are the current trend might dilute the game-theoretic focus of the thesis. It is the most logical candidate for compression if time runs short.
- **The N-Player Leap:** Extending from 2-player zero-sum to N-player (Steps 9-11) is notoriously difficult. Relying heavily on purely empirical/heuristic methods (like piKL) for N-player, while practical, must be explicitly justified over restricted theoretical guarantees. 

*(Next position goes below this line)*

### Position C, March 29 2026

**On Debate Point 1 (Is this the right focus?):**
Verdict: **Yes, but only if the thesis is framed around defensible scientific claims rather than around the market narrative.** The focus is strong because it combines three elements that rarely appear together in one PhD: imperfect-information game theory, adaptive opponent exploitation, and access to real behavioral data. That combination is a legitimate niche. The differentiator is not "poker" and not generic MARL breadth; it is the ability to connect formal safety constraints with empirically observed strategic behavior.

The main caveat is framing discipline:
- **Contribution #1 is the strongest and most defensible contribution.** Opponent modeling plus adaptive exploitation is both technically coherent and commercially relevant.
- **Contribution #2 is viable only if stated narrowly.** It should be framed as tractable N-player safety criteria, heuristics, and experimentally validated approximations, not as a promise of a general N-player analogue of the 2-player safety theorem.
- **Contribution #3 is viable only if it proves evaluation failure modes in existing practice.** It must show that standard metrics can mis-rank adaptive agents in non-transitive or N-player settings, not merely bundle known tools into a benchmark package.

The right academic framing is therefore: **safe adaptive play under imperfect information**, with poker as the clean experimental substrate and fraud/risk as the strongest downstream application. That is more defensible than optimizing the thesis identity around career optionality, even if the career upside remains real.

**On Debate Point 2 (Is the path correct?):**
Verdict: **Mostly yes, but not in its current rigid form.** The mathematical dependency chain from Steps 3–11 is real, and the core sequence from CFR scaling through safe exploitation should stay intact. However, the plan currently assumes that the real-world data and the multiplayer benchmarks will cooperate with the theory. That is the main execution risk.

The path is therefore correct **with two guardrails**:
- **A minimal data audit should happen before Step 7 hardens the modeling assumptions.** This does not require a new full step, but it does require an early validation pass on Step 13 inputs: action granularity, missing observations, player identity consistency, and whether the available logs can support per-information-set inference.
- **Step 12 should be narrowed to sequence models for behavioral trajectories and offline strategy learning.** The LLM-in-games survey is acceptable as literature coverage, but it should not become a research center of gravity unless it directly improves Step 13 or Contribution #3.

The strongest part of the roadmap is that Steps 7, 8, and 14 form a coherent thesis spine: model opponents, exploit safely, then show that the evaluation protocol can actually detect robustness and adaptation. The weakest part is Step 11, not because coalition dynamics are unimportant, but because the benchmark ecosystem is thin. It should remain a dedicated step, but with an explicit fallback benchmark if SLS proves too narrow or brittle.

**Net Position:**
- Keep the focus.
- Keep the core ordering.
- Tighten the claim on Contribution #2.
- Treat the LLM component as optional bridge material, not as a pillar.
- Add an early data sanity check and a fallback plan for multiplayer benchmarking.

---

## User Comment — Alexander Andreev, March 29 2026

> I enrolled in the PhD more so to boost my career — I want to transition into RL anyway, but with a PhD it gives me structure and credibility. The scientific breakthrough is secondary but important to me also. I want to have unique skills to attach to my portfolio, but I am not looking for scientific praise among other CS academics.
>
> In short: career transition vehicle first, genuine skill acquisition second, academic recognition third. The thesis must be real and defensible, but I am optimizing for employable expertise, not citation count.

---

## Task for Debaters — Consensus Paragraph

**Assignment:** Given all three positions (A, B, C) and the user's stated priorities above, write a single paragraph answering: *What should be the focus of this PhD, how will it benefit the candidate, and what will the scientific novelty be?*

Each debater should then revise this paragraph once with the new context that the PhD is primarily a career transition vehicle with real but secondary scientific ambition.

### Draft Consensus Paragraph (pre-revision)

The PhD should focus on **adaptive strategy learning in multi-agent imperfect-information environments**, with opponent modeling and safe exploitation (Steps 7–8) as the non-negotiable core, multi-agent extension (Steps 9–11) as the differentiating frontier, and a unified evaluation framework (Step 14) as the methodological glue. **The benefit to the candidate** is a career-grade technical portfolio: the opponent modeling + safe exploitation skill set maps directly to both MARL Architect roles ($160–327k) and Fraud/Risk AI roles ($140–345k), validated against 10 real job postings where Steps 7–8 hit 9/10 positions. The PhD provides structured credibility for the RL career transition that the candidate would pursue regardless — the degree converts 10 years of SWE experience into a legible "AI researcher + engineer" profile that commands senior/staff-level compensation. **The scientific novelty** is the extension of safe exploitation guarantees from 2-player zero-sum to N-player settings — an explicitly unsolved problem in the literature — combined with a closed-loop behavioral adaptation pipeline (detect → model → exploit → evaluate) validated on both synthetic benchmarks and real-world Playtech data. The novelty is genuine but scoped to be achievable: tractable sub-problems (3-player Kuhn, piKL heuristics, equal share baselines) rather than a general N-player safety theorem, producing 4–6 publications that are real contributions without requiring a career spent chasing citations.

### Revision A

**Revised with user context:** The paragraph above already captures the correct balance. One adjustment: given that career transition is the primary driver, the path should be evaluated not just by thesis defensibility but by **portfolio demonstrability** — every step should produce an artifact (working code, a comparison plot, a pipeline) that can be shown in a job interview, not just referenced in a dissertation. This is already the case in the current plan (each step has concrete deliverables), but it reframes the *exit criteria*: the question isn't "can I pass a viva on this?" but "can I walk into a Whatnot or Serve Robotics interview and demonstrate this skill live?" The scientific novelty — N-player safe exploitation + unified evaluation — is real and publish-worthy, but its primary value to the candidate is as a differentiator on the CV, not as a bid for academic prestige. The thesis should be tight, defensible, and genuinely novel, but optimized for *portfolio depth* over *citation impact*.

*(Positions B and C: revise the consensus paragraph below with the user's stated priorities, then this section is complete.)*

---

## Position Updates After User Context

### Position A, Updated

**Does the user context change my positions?**

**On Debate Point 1:** No change to verdict. The career-transition framing actually *strengthens* the current focus choice. The adversarial/exploitation niche is the most employable angle — it maps to fraud/risk roles that are actively hiring and pay $140–345k. A "pure academic novelty" focus would have suggested a riskier Contribution #2 scope; the career-first framing correctly suggests keeping Contribution #2 narrow and practical (piKL heuristics, empirical validation) rather than chasing a general theorem.

**On Debate Point 2:** Minor adjustment. Given career-first priorities:
- **Steps 7–8 remain the non-negotiable core** — they are the career-value center (9/10 job postings).
- **Step 13 (Playtech pipeline) gains importance** — it's the most directly demonstrable portfolio artifact. Position C's suggestion of an early data sanity check is now more compelling: if the real-world pipeline is the interview showpiece, it shouldn't be left to month 5 to discover data problems.
- **Step 12 (LLM survey) becomes even more compressible** — the candidate isn't optimizing for conference breadth. Cut the TextArena evaluation and LLM-in-games survey down to ARDT + poker state encoding only. Save 3–4 days.
- **Step 11 (SLS/coalition formation) is still worth keeping** — coalition detection transfers directly to collusion detection in fraud roles, which is the co-primary career path.
- **Contribution #3 (evaluation framework) should be reframed as a portfolio tool**, not just a thesis chapter. A working three-layer evaluation API is something you can demo in an interview. This is more valuable as a career artifact than as a publication target.

**Net:** Keep the path. Compress Step 12. Front-load a data sanity check for Step 13. Reframe deliverables as portfolio artifacts alongside thesis outputs.

---

## User Comment #2 — Alexander Andreev, March 29 2026 (on Step 12 / LLMs)

> I don't want to dilute my specialty that much, but I expect in 3 years' time LLM/omni agents to have much more weight in the real world. The job listings query also showed it's a desirable skill asset (3/10 postings mention LLM fluency). So I want to touch on it just so I have the fundamentals — not to make it a thesis pillar, but to not be blind to it either.
>
> I don't have comments on the rest of the proposals. Feel free to discuss them.

---

## Position A, Response to User Comment #2

**On Step 12 / LLMs:** I retract my earlier suggestion to aggressively compress Step 12. The user's reasoning is sound: the goal isn't thesis depth on LLMs, it's **career insurance**. By 2029, interviewers will expect at minimum conversational fluency with LLM agent architectures. The 10-day Tier 3 allocation is already the lightest possible — it's a survey, not a deep dive. The right move is:

- **Keep the 10-day allocation as-is.** It's the minimum viable exposure.
- **Keep ARDT** (minimax offline strategy learning) — this directly feeds the thesis and is the strongest technical content in the step.
- **Keep the LLM evaluation on Kuhn Poker** — it takes 1 day and gives the candidate firsthand experience with LLM strategic reasoning limitations. This is the kind of thing that comes up in interviews ("have you actually tested LLMs on strategic tasks?").
- **The TextArena survey can remain light** — skim the benchmark, run one game, understand the landscape. No need to implement or publish.
- **Drop nothing.** The step is already 10 days. Compressing further would mean cutting content that provides career-relevant fundamentals.

The principle is: Step 12 isn't a thesis contribution step, it's a **career literacy step**. That's a valid reason to keep it at its current scope, especially given the user's 3-year time horizon to defense.

**On the rest of the proposals:** The three positions are converging. The remaining points of genuine disagreement are:

1. **Early data sanity check (Positions B and C want it, I'm now persuaded):** Add a lightweight data audit during Step 4 or 5 — just verify that Playtech hand histories exist, have the expected fields, and can be parsed. Not a full pipeline, just a reality check. This costs 1–2 days and prevents a nasty surprise in Step 13.

2. **Step 11 fallback benchmark (Position C wants it, I agree):** SLS is the right primary benchmark, but Goofspiel or a custom 3-player Leduc variant should be documented as fallbacks in the step spec. No schedule change needed — just an explicit Plan B.

3. **Contribution #2 scope (all three positions agree):** Frame it as tractable heuristics + empirical validation on small games, not a general N-player safety theorem. The user's career-first priority reinforces this: a narrow, defensible, published result is more valuable than an ambitious unpublished one.

4. **Contribution #3 framing (Position C's point, I agree):** It must demonstrate that existing evaluation metrics *fail* in specific N-player/non-transitive scenarios — not just bundle tools. This makes it a genuine contribution rather than an engineering exercise, while still producing a demo-ready portfolio artifact.

These four points feel close to consensus. No fundamental disagreements remain on the path ordering or the focus.

---

## User Comment #3 — Alexander Andreev, March 29 2026 (On General Sequence & Missing Topics)

> I didn't like the first round as it was nitpicking about terminology and what to focus on. I want to debate the *general structure of the plan's sequence*. 
>
> Try to identify 5-10 "steps" closely related to the domain but *not* included in current plan. Comment on why they should be put in the current plan or why they should remain excluded. Let's stress-test the sequence structurally.

---

## Position B, Response to User Comment #3

**Stress-Testing the Structure:** You are right to pull us out of the terminology weeds. If we look strictly at the macro-sequence (Foundations → Tabular GT → Neural GT → Adaptation/Exploitation → MARL → Real Data), we can identify several major adjacent fields that have been omitted. 

Here are 8 closely related topics/steps, heavily debated in literature, that are currently missing from your sequence. Here is why they are out, and whether they should be swapped in:

### 1. Inverse Reinforcement Learning (IRL) / Generative Adversarial Imitation Learning (GAIL)
- **What it is:** Learning the reward function or directly recovering a policy from expert demonstrations (instead of just predicting the next action like Behavioral Cloning).
- **Should it be included?** **Marginally as a sub-step.** You currently use Behavioral Cloning (Step 13) to build player embeddings. IRL/GAIL is technically superior for recovering robust strategic intent from data. However, adding it as a *full step* would derail the timeline. It should just be a bullet point in Step 13 as a method to explore if BC fails.

### 2. Formal Theory of Mind (ToM) / Cognitive Hierarchy (Level-k Reasoning)
- **What it is:** Explicitly recursive opponent modeling ("I think that you think that I think..."). Human data almost always conforms to Level-k bounds rather than Nash equilibriums.
- **Should it be included?** **Yes, merged into Step 7.** Currently, Step 7 focuses on mathematical Bayesian/Type-based modeling. It fundamentally lacks the human-centric "Level-k" reasoning which is critical for exploiting real human players (e.g., in Playtech data). Missing this means missing the most reliable way to model suboptimal human behavior.

### 3. Formal POMDPs and Dec-POMDPs (Decentralized Partially Observable MDPs)
- **What it is:** The classic RL framing of imperfect information. We are currently using the Extensive-Form Game (game tree) framing.
- **Should it be included?** **No. Keep excluded.** Swapping between the EFG paradigm (CFR, public states) and the POMDP paradigm causes massive conceptual whiplash. EFG is better suited for adversarial card games. Adding a step for Dec-POMDPs would just be an academic history lesson that clutters the technical execution.

### 4. Continuous Action / Continuous Time Environments
- **What it is:** MARL where action spaces aren't discrete (e.g., physics-based autonomous driving, or real-time strategy games like StarCraft macro-management).
- **Should it be included?** **No. Keep excluded.** Your thesis domain (Fraud, iGaming, Cybersecurity) is primarily discrete event-driven. Introducing continuous action spaces requires entirely different mathematical actor-critic architectures (like DDPG/SAC variants) which dilute your focus on extensive-form games. 

### 5. Adversarial Robustness / Policy Perturbation
- **What it is:** Evaluating how agents fail when the state space or observations are subtly perturbed (the RL equivalent of adversarial image noise).
- **Should it be included?** **No. Keep excluded.** Step 8 correctly focuses on *Strategic Safe Exploitation* (the opponent playing an exploit baseline), not *Pixel/Observation Attacks*. It's a completely different flavor of safety that leads toward deep-learning security, not game theory.

### 6. Distributed RL Infrastructure (Ray / RLlib / Kubernetes)
- **What it is:** The MLOps required to actually run AlphaStar/OpenAI Five on massive compute clusters.
- **Should it be included?** **No. Keep excluded.** Given your 10 YOE as a SWE, you already know systems architecture. Spending PhD thesis time analyzing `Ray` cluster setups offers zero scientific novelty. Keep the 28 weeks strictly focused on algorithms, not the plumbing.

### 7. Mean Field Games (MFG)
- **What it is:** Analyzing N-player games where N approaches infinity, reducing individual opponents to a "mass distribution" or fluid.
- **Should it be included?** **No. Keep excluded.** Your N-player challenge (Step 11) is for small, distinct colluding actors (4-6 players in poker/fraud rings). Moving to infinite-player approximations destroys the specific multi-agent cooperative dynamics you are trying to detect.

### 8. Mechanism Design / Contract Theory
- **What it is:** The inverse of game theory. Designing the rules of the game to ensure agents behave truthfully or cooperatively (e.g., auction design).
- **Should it be included?** **No. Keep excluded.** You are building an agent (or an anomaly detector) that operates *within* a fixed structure (a game of poker, a trading engine). Mechanism design is an entirely separate career track (often economics/operations research).

**Summary on Sequence Structure:**
The macro-structure holds up incredibly well against these alternatives. The only structural adjustment required is pulling **Level-k / Theory of Mind** reasoning explicitly into Step 7, and perhaps referencing **GAIL** in Step 13. Setting aside time for Dec-POMDPs, continuous math, or infrastructure would actively harm the focused momentum of your syllabus.

---

## Position C, Response to User Comment #3

**Stress-Testing the Sequence Structurally:** The current roadmap is strong on one axis: equilibrium computation and strategic adaptation in imperfect-information games. Where it is thinner is at the interfaces between theory and real behavior: human suboptimality, logged-data evaluation, online adaptation under drift, and the conceptual bridge from game-theoretic formalisms to general MARL. That means the plan is not missing a new major phase, but it is missing several adjacent topics that should either be merged into existing steps or explicitly kept out to avoid dilution.

Here are 9 closely related candidate steps that are currently absent, and whether they belong in the plan:

### 1. Sequence-Form / Linear Programming Methods for Extensive-Form Games
- **What it is:** The sequence-form representation of policies and LP-based equilibrium / best-response computation for imperfect-information games.
- **Should it be included?** **Yes, but only as a sub-step in Steps 2 and 8.**
- **Why:** Step 8 already depends on LP-flavored safe exploitation methods (RNR, constrained response, safety floors), and Step 7 mentions sequence-form projected methods. Right now that machinery appears in the plan mostly as a tool to be used, not as a concept to be understood. It does not deserve a full standalone step, but without at least a compact sequence-form bridge, safe exploitation can become procedural rather than principled.

### 2. Behavioral Game Theory (Quantal Response, Cognitive Hierarchy, Level-k)
- **What it is:** Models of bounded rationality and recursive reasoning that explain how real humans deviate from Nash play.
- **Should it be included?** **Yes, merged into Step 7.**
- **Why:** Your current Step 7 is mathematically strong but tilted toward idealized opponent estimation. Real Playtech users will not behave like equilibrium agents or even like stable type distributions all the time. If the thesis wants to exploit human behavior rather than only synthetic policies, Level-k / cognitive hierarchy is one of the most natural missing pieces.

### 3. Markov Games / Stochastic Games as the Bridge into MARL
- **What it is:** The standard formalism underlying multi-agent reinforcement learning in sequential environments.
- **Should it be included?** **Yes, but as a bridge inside Step 9, not a new step.**
- **Why:** The current plan jumps from extensive-form poker/game-theory machinery into CTDE, PSRO, and MAPPO. That jump is survivable, but structurally abrupt. A short formal bridge on Markov games would make the sequence cleaner and explain what is preserved and what is lost when moving from EFG-style reasoning to MARL-style function approximation.

### 4. Off-Policy Evaluation (OPE) for Logged Behavioral Data
- **What it is:** Importance sampling, weighted importance sampling, doubly robust estimators, and related tools for evaluating policies from historical logs.
- **Should it be included?** **Yes, merged into Steps 13 and 14.**
- **Why:** AIVAT is useful for variance reduction in game evaluation, but it does not substitute for a general logged-data evaluation toolkit. If Step 13 uses Playtech data and Step 14 claims a strong evaluation methodology, then OPE is a missing structural piece. It directly supports the real-data side of the thesis and makes the evaluation story more serious.

### 5. Meta-Learning / Fast Opponent Adaptation
- **What it is:** Learning policies or models that adapt quickly to a new opponent from a small amount of evidence.
- **Should it be included?** **Marginally, as a small comparison baseline in Step 7 or 10, not as a full step.**
- **Why:** It is highly relevant to the word "adaptive" in the thesis title. However, a full meta-RL step would open a second large literature and compete with the main game-theoretic throughline. The right structural role is a lightweight baseline: show one fast-adaptation method, compare it to the main opponent-modeling pipeline, and move on.

### 6. Change-Point Detection / Non-Stationarity Diagnostics
- **What it is:** Statistical methods for detecting regime shifts, opponent drift, and abrupt policy changes.
- **Should it be included?** **Yes, merged into Step 7 and reused in Step 13.**
- **Why:** Non-stationarity is mentioned in Step 7, but only at the problem-statement level. In practice, opponent type switching, bot updates, collusion onset, and market/fraud drift are all change-detection problems. This is one of the few adjacent topics that improves both the synthetic-game side and the real-data side without pulling the roadmap off course.

### 7. Imperfect-Information Search Baselines (ISMCTS / POMCP / Online Search)
- **What it is:** Search-based decision-making under hidden information, used as an alternative to equilibrium-style offline solving.
- **Should it be included?** **Yes, lightly, inside Step 6 or Step 14.**
- **Why:** The plan mentions approximate best response via ISMCTS-BR in Step 14, but search is not treated as a studied capability. That leaves a structural gap: the roadmap is very solver-heavy and under-represents online planning baselines. A lightweight inclusion would strengthen evaluation and help position CFR-style methods against planning-style agents.

### 8. Causal Inference on Behavioral Logs
- **What it is:** Distinguishing correlation from causal effect in observed behavior, interventions, and collusion signals.
- **Should it be included?** **No, keep excluded as a full step.**
- **Why:** It is adjacent to fraud analytics and would be useful if the thesis centered on intervention claims. But your roadmap is about strategic modeling and adaptation, not about estimating causal effects under observational confounding. Making causal inference a formal step would introduce a second methods stack that is too large for the value it adds during the preparation phase.

### 9. Formal Verification / Verified Safety for Learned Policies
- **What it is:** Proving or certifying that a learned policy respects constraints under defined conditions.
- **Should it be included?** **No, keep excluded.**
- **Why:** It sounds close to safe exploitation, but it is actually a different safety culture, closer to formal methods and control verification. Your notion of safety is strategic exploitability and worst-case value degradation, not reachability certificates or program proofs. Adding this would muddy the meaning of "safe" in the roadmap rather than clarify it.

**Structural Verdict:**
The sequence does **not** need a redesign. It needs a few better bridges. The most valuable additions are:
- **Merge behavioral game theory into Step 7** so real human deviation is modeled explicitly.
- **Merge sequence-form / LP intuition into Steps 2 and 8** so safe exploitation has a cleaner mathematical foundation.
- **Merge OPE into Steps 13–14** so logged-data evaluation is credible.
- **Merge change-point detection into Steps 7 and 13** so non-stationarity is operational, not just acknowledged.
- **Add a short Markov-games bridge at the start of Step 9** so the jump into MARL is conceptually smoother.

Everything else should stay excluded unless the scope expands. The current roadmap is already close to the correct macro-ordering; the main issue is not missing whole new pillars, but making the interfaces between the existing pillars more explicit.
