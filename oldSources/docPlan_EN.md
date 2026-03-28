# AI Poker Agent — Preparation Plan

**Goal:** Build foundational knowledge in Reinforcement Learning (RL), Game Theory, and Poker AI as preparation for a 36-month PhD focused on opponent playstyle detection and adaptive exploitation in 6-max No-Limit Hold’em, including detection of collusion/team play.

## Content
- [Introduction](#introduction)
- [Plan](#plan)
  - [Step 1 — Reinforcement Learning Basics](#step-1--reinforcement-learning-basics)
  - [Step 2 — Game Theory + CFR Basics](#step-2--game-theory--cfr-basics)
  - [Step 3 — CFR Variants + Poker Mathematics](#step-3--cfr-variants--poker-mathematics)
  - [Step 4 — Review of Existing Systems](#step-4--review-of-existing-systems)
  - [Step 5 — Deep CFR + Neural Approaches](#step-5--deep-cfr--neural-approaches)
  - [Step 6 — Opponent Modeling + Safe Exploitation](#step-6--opponent-modeling--safe-exploitation)
  - [Step 7 — Custom Data + Offline RL + Sequence Modeling](#step-7--custom-data--offline-rl--sequence-modeling)
  - [Step 8 — Integration, Evaluation Framework, Thesis Design](#step-8--integration-evaluation-framework-thesis-design)
- [Consolidated Reading List](#consolidated-reading-list)
- [Tools and Frameworks](#tools-and-frameworks)
- [36-Month Macro Plan](#36-month-macro-plan)
- [Appendix: Compute Requirements](#appendix-compute-requirements)
- [Glossary](#glossary)

---

## Introduction

This plan covers the **first ~3 months** of the 36-month PhD and acts as a targeted introduction to the specific Machine Learning (ML) areas directly required for the research — **Reinforcement Learning (RL)**, **Game Theory**, and **solvers for imperfect-information games (CFR and its variants)**. These fields form the theoretical and practical backbone of any modern poker AI system — from Libratus and DeepStack to Pluribus. Without a solid foundation here, work on the main thesis contributions (playstyle detection, adaptive exploitation, and collusion detection) cannot stand on solid ground.

A key principle of the plan is that **all practical projects will be conducted on simplified ("toy") poker variants** — Kuhn Poker (3 cards, 1 round) and Leduc Hold’em (6 cards, 2 rounds). These games preserve the structural properties of full No-Limit Hold’em — imperfect information, bluffing, multi-stage betting — but are small enough to be solved on a standard laptop in minutes instead of days on a cluster. This allows for rapid iteration, deep understanding of the algorithms, and reliable validation (solutions can be checked against known analytical results) before scaling to actual 6-max NLHE in later phases.

The plan is structured in **8 sequential steps**, each combining theoretical reading with a practical project. The progression is gradual: from RL and classic CFR basics (Steps 1–3), through examining modern systems and neural approaches (Steps 4–5), to opponent modeling, real data handling, and building an evaluation framework (Steps 6–8). By the end of these three months, the goal is to have: working implementations of key algorithms, a data pipeline, an agent evaluation framework, and a draft of the research questions — everything needed to transition into the infrastructure and research phase of the PhD.

---

## Plan

### Step 1 — Reinforcement Learning Basics

**Literature:**
| Material | Scope |
| :--- | :--- |
| **Sutton & Barto, Reinforcement Learning: An Introduction (2nd ed.)** | Chapters 1–6 (RL basics), Chapter 13 (policy gradient) |
| **OpenAI Spinning Up (spinningup.openai.com)** | "Key Concepts" + "Intro to Policy Optimization" |

**Practical Project 1: DQN + PPO in Gym environments**
- Install and get familiar with `stable-baselines3[extra]` and `gymnasium`.
- Train a DQN agent on CartPole, then a PPO agent on LunarLander.
- Experiment with hyperparameters: learning rate, network size, discount factor.
- Plot learning curves, observe the effects of reward shaping.
- **Result:** Training plots + notes on which hyperparameters matter most.

### Step 2 — Game Theory + CFR Basics

**Literature:**
| Material | Scope |
| :--- | :--- |
| **Neller & Lanctot, An Introduction to Counterfactual Regret Minimization (2013)** | The entire document (~30 pages) |
| **Shoham & Leyton-Brown, Multiagent Systems** | Chapters 3 (intro to game theory), 4 (solution concepts), 6 (extensive-form games) |

**Practical Project 2: Vanilla CFR for Kuhn Poker**
- Implement from scratch in Python (no libraries except numpy/matplotlib).
- Kuhn Poker: 3-card deck (J, Q, K), 2 players, 1 betting round.
- Implementation: game tree traversal, regret matching, strategy accumulation.
- Observe how the strategy converges to the Nash Equilibrium.
- Verify against the known existing analytical solution.
- Plot exploitability vs. iterations.
- **Result:** Working CFR solver + convergence plot + verified Nash strategies.

### Step 3 — CFR Variants + Poker Mathematics

**Literature:**
| Paper/Book | Year | Why |
| :--- | :--- | :--- |
| **Zinkevich et al., Regret Minimization in Games with Incomplete Information** | 2007 | The original CFR paper |
| **Lanctot et al., Monte Carlo Sampling for Regret Minimization in Extensive Games** | 2009 | Monte Carlo CFR (MCCFR) — makes CFR applicable to large games |
| **Tammelin et al., Solving Heads-Up Limit Texas Hold’em** | 2015 | CFR+ — the variant that "solved" limit hold’em |
| **Chen & Ankenman, The Mathematics of Poker** | 2006 | Chapters 1–8 (Expected Value (EV), pot odds, game theory framework) |

**Practical Project 3: MCCFR for Leduc Hold’em**
- Leduc: 6-card deck (two suits of J, Q, K), 2 players, pre-flop + flop (1 community card).
- Implement MCCFR (Monte Carlo Counterfactual Regret Minimization) from scratch.
- Compare and optimize convergence speed vs. vanilla CFR on Kuhn.
- Implement basic hand abstraction (grouping based on strength/suit isomorphism).
- Calculate and plot exploitability.
- **Result:** MCCFR solver for Leduc + exploitability comparison plot vs. vanilla CFR.

### Step 4 — Review of Existing Systems

**Literature:**
| Paper | Year | Key Ideas |
| :--- | :--- | :--- |
| **Moravcik et al., DeepStack** | 2017 | Value estimation via neural networks at leaf nodes, continuous re-solving |
| **Brown & Sandholm, Libratus** | 2018 | Blueprint strategy + endgame solving |
| **Brown & Sandholm, Pluribus** | 2019 | 6-player NLHE, blueprint via MCCFR, depth-limited search, why Nash equilibrium is ill-defined in 6-max |
| **Johanson et al., Finding Optimal Abstract Strategies...** | 2012 | Action and information abstraction — critical for scaling to NLHE |
| **Gilpin & Sandholm, Lossless Abstraction...** | 2007 | Theoretical foundations of card abstraction |

**Practical Work:**
- Draw an architectural diagram of Pluribus. Compare each component to the planned system for development.
- Install OpenSpiel (`pip install open_spiel`), run their CFR on Kuhn and Leduc, compare the output with your own implementations.

### Step 5 — Deep CFR + Neural Approaches

**Literature:**
| Paper | Year | Key Ideas |
| :--- | :--- | :--- |
| **Brown et al., Deep CFR** | 2019 | Replaces tabular CFR with neural networks — allows scaling without explicit abstraction |
| **Steinberger et al., DREAM** | 2020 | Improves Deep CFR with better variance reduction — more practical to implement |
| **Heinrich & Silver, NFSP** | 2016 | Uses deep RL to approximate Nash equilibria — a bridge between game theory and RL |

**Practical Project 4: Deep CFR for Leduc Hold’em**
- Implement in PyTorch from scratch.
- Train advantage networks (one per player) and a strategy network.
- Use reservoir sampling for memory buffers.
- Compare the resulting strategy with your tabular MCCFR from step 3.
- Monitor GPU load — this is the first real GPU workload.
- Validate against OpenSpiel’s Deep CFR implementation for Leduc.
- **Result:** Working Deep CFR pipeline + strategy comparison.

### Step 6 — Opponent Modeling + Safe Exploitation

**Literature:**
| Paper | Year | Why |
| :--- | :--- | :--- |
| **Southey et al., Bayes’ Bluff** | 2005 | Fundamental Bayesian approach to opponent modeling |
| **He et al., Opponent Modeling in Deep RL (DRON)** | 2016 | Deep RL approach to opponent modeling |
| **Foerster et al., LOLA** | 2018 | Agents that model the learning of opponents |
| **Bard et al., Online Implicit Agent Modelling** | 2020 | Implicit opponent modeling during play |
| **Johanson et al., Data-Biased Robust Counter Strategies** | 2009 | How to exploit opponents without becoming exploitable yourself |
| **Ganzfried & Sandholm, Safe Opponent Exploitation** | 2015 | Theoretical framework for constrained exploitation |
| **Lanctot et al., PSRO** | 2017 | Critical for population-based training |

**Practical Project 5: Opponent Modeling in Leduc**
- Using the Leduc implementation:
  - Implement a Bayesian opponent model (estimating hand range based on observed actions).
  - Implement a best-response calculation against a fixed (predictable) opponent.
  - Measure the winrate of the best-response vs. the Nash strategy against predictable opponents.
- **Result:** Quantified exploitation delta (how much you gain from modeling vs. playing GTO).

### Step 7 — Custom Data + Offline RL + Sequence Modeling

**Literature:**
| Paper | Year | Why |
| :--- | :--- | :--- |
| **Brown et al., ReBeL** | 2020 | Combines search + RL for imperfect-information games |
| **Chen et al., Decision Transformer** | 2021 | Sequence modeling for decision making — relevant for encoding hand histories |
| **Kumar et al., Conservative Q-Learning (CQL)** | 2020 | Core offline RL method — review for concepts |

**Practical Project 6: Behavioral Cloning on Custom Data**
- Take a subset of anonymized hand histories (~50–100k hands from **Playtech**).
- Design a **state representation tensor**:
  - Encode cards
  - Position
  - Pot size (normalized)
  - Stack sizes (normalized)
  - Betting history (sequence of actions with sizing)
  - Number of active players
- Train a supervised neural network (PyTorch) to predict the action taken by the human in the given state.
- Evaluate accuracy by round (preflop / flop / turn / river) and by position.
- **Result:** Working data pipeline + baseline action prediction accuracy + documented state representation.
  *(Note: This project is critical. The state representation runs through the entire thesis. The data pipeline will be reused for style classification and collusion detection.)*

### Step 8 — Integration, Evaluation Framework, Thesis Design

**Literature:**
| Material | Why |
| :--- | :--- |
| **DeLong & Bhatt, Towards Collusion Detection...** | Directly related to collusion detection |
| **Yan & Browne, Collusion Detection in Online Poker** | Statistical approaches to collusion detection |
| **Timbers et al., Approximate Exploitability (2022)** | Key metric for evaluating performance |
| **Reviews on Anomaly Detection in Graphs** | Methodology from related fields (community detection, suspicious coordination motifs) |

**Practical Project 7: Evaluation Framework + Bot Zoo**
- Build a **cross-play tournament framework**:
  - Any agent can play against any other agent for N hands.
  - Calculate mbb/hand (milli-big blinds per hand) with confidence intervals.
  - Support different table sizes (2–6 players).
- Create a small **bot zoo** for testing:
  - Random agent
  - Always-call agent
  - Tight-aggressive heuristic
  - Your Leduc Nash agent
- Run a round-robin tournament.
- **Result:** Reusable evaluation framework for the entire PhD.

**Thesis Design Work (in parallel):**
- 1–2 page draft of research questions.
- Planning each expected contribution.
- Identification of the first experiment for publication.

---

## Consolidated Reading List

1. Neller & Lanctot, *Intro to CFR* (2013)
2. Sutton & Barto, *RL: An Introduction*, ch 1–6, 13
3. Shoham & Leyton-Brown, *Multiagent Systems*, ch 3, 4, 6
4. Zinkevich et al., *Regret Minimization in Games* (2007)
5. **Brown & Sandholm, *Pluribus* (2019)**
6. Brown et al., *Deep CFR* (2019)
7. Johanson et al., *Data-Biased Robust Counter Strategies* (2009)
8. Moravcik et al., *DeepStack* (2017)
9. Brown & Sandholm, *Libratus* (2018)
10. Lanctot et al., *MCCFR* (2009)
11. Tammelin, *CFR+* (2015)
12. Heinrich & Silver, *NFSP* (2016)
13. Brown et al., *ReBeL* (2020)
14. Steinberger et al., *DREAM* (2020)
15. Southey et al., *Bayes’ Bluff* (2005)
16. Ganzfried & Sandholm, *Safe Exploitation* (2015)
17. Lanctot et al., *PSRO* (2017)
18. Chen et al., *Decision Transformer* (2021)

---

## Tools and Frameworks

| Tool | Purpose | When to use |
| :--- | :--- | :--- |
| **OpenSpiel (DeepMind)** | Reference implementations for CFR, Deep CFR, NFSP | Step 4+ as a baseline for validation |
| **PokerRL (Steinberger)** | Deep RL specifically for poker, includes NLHE env | Step 6+ for scaling to NLHE |
| **Stable-Baselines3** | Standard RL algorithms (PPO, DQN) | Step 1 for gym experiments |
| **Slumbot** | Free poker bot for benchmarking | Once you have a playing agent |
| **phevaluator / treys (Python)** | Fast poker hand evaluation | When building your NLHE environment |
| **OMPEval (C++)** | Very fast hand equity evaluator | When optimizing environment speed |
| **PyTorch** | Neural network training | Steps 5+ |
| **Weights & Biases / MLflow** | Experiment tracking | From step 5 onwards |

---

## 36-Month Macro Plan

| Months | Phase | Focus |
| :--- | :--- | :--- |
| **1 – 3** | Introduction | Reading + practical projects (this plan) |
| **4 – 5** | Infrastructure | Fast 6-max env (C++/Rust) + data pipeline + evaluation framework |
| **6 – 8** | Baseline | Deep CFR or MCCFR blueprint for 6-max NLHE |
| **9 – 14** | Contribution 1 | Opponent playstyle detection from action sequences (custom data) |
| **15 – 22** | Contribution 2 | Adaptive exploitation: GTO baseline + style-conditioned countermeasures |
| **23 – 28** | Contribution 3 | Detection of collusion/team play and robust play |
| **29 – 32** | Integration | Full system: detection → classification → adaptation → exploitation |
| **33 – 36** | Buffer | Thesis writing, defense |

---

## Appendix: Compute Requirements

Compute requirements for this project are modest by modern AI standards — comparable to training a mid-sized image classifier, rather than a Large Language Model (LLM). The vast majority of the research (opponent modeling, style detection, collusion analysis) trains in a matter of hours. The expensive part — computing a base poker strategy — is a one-time cost.

### Workload Profile

This project has two distinct workloads requiring different hardware:

- **Game Tree Search (CFR/MCCFR):** Requires many **CPU cores** and **large RAM**. Similar to Monte Carlo physics simulations — heavy combinatorial compute, no GPUs required. Runs for days continuously, but only a few times a year.
- **Neural Network Training (Deep CFR, opponent models):** Requires **GPU acceleration**. Similar to training ResNet on ImageNet — small to medium by deep learning standards. Individual runs take hours to days.

Both workloads are **bursty**: intensive for a few days, then idle for weeks during analysis and experiment design. Average utilization over the PhD is ~30–40%.

### Reference Scale

**Pluribus** trained its base strategy using approximately **12,000 CPU-core-hours** — equivalent to a 64-core server running for 8 days. This is a modest HPC (High-Performance Computing) allocation by any standard. The needs of this project are comparable or smaller, as the thesis focus is computationally cheaper than generating a base strategy.

### Three Hardware Tiers

| | Tier 1: Starter | Tier 2: Recommended | Tier 3: Ideal |
| :--- | :--- | :--- | :--- |
| **CPU Power** | 16 cores, 128 GB RAM | 32–64 cores, 256 GB RAM | 128–192 cores, 512+ GB RAM |
| **GPU Power** | 1 card, 24 GB VRAM | 2 cards, 32 GB VRAM each | 4 cards, 32–80 GB VRAM each |
| **Handles** | All toy experiments + opponent modeling. Full NLHE: slow (weeks/run). | All experiments. Full NLHE: days/run. Two parallel experiments. | Everything. Large population training. Exceeds what Pluribus used. |

A personal **Tier 1 workstation**, combined with **off-peak access to university HPC** (night/weekend batch jobs), is the most efficient path. Expected HPC usage during active training phases: ~500–2,000 CPU-core-hours and ~50–200 GPU-hours per month — a small allocation by cluster standards.

---

## Glossary

- **RL (Reinforcement Learning):** A field of machine learning where an agent learns to make decisions through trial and error.
- **CFR (Counterfactual Regret Minimization):** A core algorithm for finding strategies close to a Nash Equilibrium in imperfect-information games.
- **GTO (Game Theory Optimal):** In poker, refers to a strategy (an approximation of a Nash Equilibrium) that is mathematically unexploitable in the long run.
- **Nash Equilibrium:** A state in a game where no player can improve their outcome by unilaterally changing their strategy.
- **Blueprint Strategy:** A pre-computed, abstracted strategy for the entire game that serves as a basis for real-time decisions (used in systems like Libratus and Pluribus).
- **Information Abstraction:** Grouping similar game states (e.g., similar poker hands) together to reduce the size of the game tree to a computable level.
- **Action Abstraction:** Restricting the possible bet sizes (e.g., only half-pot, full-pot, and all-in) instead of the infinite possibilities in No-Limit.
- **Exploitability:** A measure of how much a given strategy deviates from a perfect Nash Equilibrium; measured by how much a perfect opponent could win against it maximally.
- **mbb/hand (milli-big-blinds per hand):** The standard unit for measuring winrate in poker research; one-thousandth of a big blind per hand.
- **Subgame Solving:** Re-computing the optimal strategy for the current situation in real-time during play, usually with finer granularity than the blueprint strategy.
- **Population-based training:** A methodology where multiple diverse agents are trained simultaneously by playing against each other, often to ensure diversity in playstyles.
- **Behavioral Cloning:** A method from supervised learning where a model is trained to imitate the actions of a human (or expert) based on collected data.