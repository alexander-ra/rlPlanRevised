# Academic Session Report — Structure Plan

**Event:** Ruse University Academic Session, May 2026
**Author:** Alexander Andreev
**Target length:** ~6 pages core content (excluding title page, abstract, references)
**Language:** English

---

## Working Title

**"Adaptive Strategy Learning in Multi-Agent Imperfect-Information Games: From Equilibrium Computation to Safe Opponent Exploitation"**

*Rationale:* The title signals three things: (1) the domain (multi-agent imperfect-info games), (2) the trajectory (from static equilibrium to adaptive play), and (3) the key differentiator (safe exploitation — not just exploitation). It avoids mentioning poker, keeping the framing domain-agnostic as the thesis intends.

---

## Section Plan

### 1. Introduction — Establishing Relevance (~1 page)

**Goal:** Justify *why* this research matters *now*. The introduction must answer three questions: Why this problem? Why now? Why games?

**Narrative arc:**

1. **The agentic AI inflection point (the "why now").** We are entering an era where autonomous AI agents operate alongside humans in open, adversarial environments — trading on financial markets, negotiating contracts, managing network security, interacting in online platforms. These agents encounter other strategic decision-makers (human or AI) whose intentions are hidden and whose behavior may be adversarial, cooperative, or deceptive. The core challenge is no longer training a single agent to perform well in isolation — it is enabling agents to reason about, adapt to, and safely interact with other agents under conditions of uncertainty and hidden information. This is, at its foundation, a game-theoretic problem — and it is rapidly moving from theoretical curiosity to practical necessity.

2. **Why imperfect-information extensive-form games are the right abstraction.** The real world is noisy, partially observable, and populated by strategic actors. Imperfect-information extensive-form games capture precisely these properties in a compact, mathematically tractable form: sequential decision-making, private information, stochastic outcomes, and multiple interacting agents. They are not merely benchmarks — they are *compressed simulacra* of the multi-agent dynamics that arise in cybersecurity (adversarial intrusion/defense), financial markets (competing algorithmic traders), fraud detection (identifying malicious actors hidden among legitimate ones), and autonomous system coordination. The field's landmark results — from CFR (Zinkevich et al., 2007) through Libratus (2018), Pluribus (2019), and ReBeL (2020) — were validated on poker, but the underlying algorithms are game-agnostic. Poker is the laboratory, not the subject.

3. **The field's trajectory: bigger but still sterile.** The past decade of game AI research has pursued a clear direction: apply equilibrium-finding algorithms to progressively larger games. CFR was scaled via Monte Carlo sampling, neural function approximation, and real-time subgame solving, culminating in superhuman performance in both two-player (Libratus) and six-player poker (Pluribus). These are landmark achievements — but they share a fundamental limitation. They compute *fixed* equilibrium strategies that do not adapt to the specific behavioral patterns of encountered opponents. Against sub-optimal opponents (which includes virtually all real-world adversaries, human or AI), a Nash strategy is safe but blind — it leaves exploitable value on the table. And as we move to N-player settings, even the notion of "safe" becomes problematic: Nash equilibrium loses its minimax guarantee, exact computation becomes intractable (PPAD-complete), and the paradigm must shift from "find the perfect solution" to "adapt quickly in environments too complex for any single equilibrium."

4. **The three open problems.** This creates a cluster of related open questions at the frontier:
   - *Adaptation:* How can an agent infer an opponent's behavioral tendencies from observed actions and adjust its strategy in real time, in environments where the opponent's private information and intentions are hidden?
   - *Safety under adaptation:* How can an agent exploit detected weaknesses while maintaining guarantees against worst-case loss — particularly in N-player settings where the two-player Safety Theorem (Ganzfried & Sandholm, 2015) provably fails?
   - *Evaluation:* How do we reliably measure whether an agent is actually adapting well — across different games, opponent populations, and environmental conditions — when existing metrics (exploitability, Elo) each capture only one dimension?

   A practical corollary deserves mention: an agent that can model and classify opponent behavior is also an agent that can *detect* anomalous or malicious behavior — unauthorized bots, colluding players, adversarial actors masquerading as legitimate participants. This surveillance capability flows directly from the adaptation methodology and has immediate applications in online platform integrity, fraud detection, and adversarial network defense.

5. **Our research program.** This doctoral research addresses these three open problems through a structured 15-step study plan. The foundational work is complete (reinforcement learning basics; game-theoretic equilibrium computation via CFR, validated on Kuhn Poker). The remainder of the program — scaling, neural methods, opponent modeling, safe exploitation, multi-agent dynamics, real-world data pipelines, and evaluation framework construction — targets three specific contributions: a Behavioral Adaptation Framework, Multi-Agent Safe Exploitation heuristics, and a domain-agnostic Evaluation Methodology. The methodology is validated on small-to-medium imperfect-information games (Kuhn Poker, Leduc Hold'em, and extensions); the design is intentionally domain-agnostic, aiming for transferability to more complex multi-agent environments.

**Tone note:** Lead with the world, not the field. The opening should make a non-specialist reader understand why this research matters *to them* — because AI agents are already operating in their world. Then narrow to the technical framing. The closing should be honest about scope: the methodology generalizes, the validation is on tractable benchmarks. Professors will respect the intellectual honesty more than overreach.

---

### 2. Review of Existing Solutions (~2.5 pages)

**Goal:** Survey 8 key papers that define the state of the art, organized as a narrative progression from foundations to the frontier. Each paper should be presented not just for what it *does*, but for what it *leaves open* — building toward the gap that the proposed solution addresses.

**Organization:** Thematic progression, not paper-by-paper list.

#### 2.1 Equilibrium Computation — The Algorithmic Foundation (~0.5 page)

**Paper 1: Zinkevich et al. (2007)** — "Regret Minimization in Games with Incomplete Information." *NeurIPS.*
- Introduced CFR — the first practical algorithm for computing Nash equilibria in imperfect-information extensive-form games.
- Key idea: decompose global regret into local per-information-set regrets; minimize each independently via regret matching.
- Convergence: average strategy approaches Nash equilibrium at O(1/sqrt(T)).
- **What it opened:** Made computational game theory practical for medium-scale games.
- **What it left open:** Vanilla CFR requires full game tree traversal — does not scale to large games. Monte Carlo variants (Lanctot et al., 2009) and neural approximations (Brown et al., 2019) were needed to bridge this gap.

#### 2.2 Superhuman Game AI — From Two-Player to Multiplayer (~0.75 page)

**Paper 2: Brown & Sandholm (2018)** — "Superhuman AI for Heads-Up No-Limit Poker: Libratus Beats Top Professionals." *Science.*
- First AI to defeat top professionals in heads-up no-limit Texas Hold'em.
- Architecture: blueprint computation via MCCFR + real-time subgame solving + self-improvement through opponent exploitation in subgames.
- **What it proved:** The CFR family of algorithms, combined with abstraction and subgame solving, can handle real-world-scale imperfect-information games.
- **What it left open:** Two-player only. The subgame solving safety guarantees rely on the zero-sum assumption.

**Paper 3: Brown & Sandholm (2019)** — "Superhuman AI for Multiplayer Poker." *Science.*
- Pluribus: first AI to defeat professionals in six-player no-limit Texas Hold'em.
- Key innovation: depth-limited search with a modified blueprint that uses an "average strategy" from MCCFR rather than opponent modeling.
- **Critical observation for our thesis:** Pluribus succeeds empirically in multiplayer poker *without any formal safety guarantees*. In two-player games, Nash equilibrium is the safe baseline; in six-player poker, no analogous baseline exists. Pluribus sidesteps this problem rather than solving it. This is the theoretical gap that Contribution 2 targets.

**Paper 4: Brown et al. (2020)** — "Combining Deep Reinforcement Learning and Search for Imperfect-Information Games." *NeurIPS.*
- ReBeL: unified framework that brings AlphaZero-style RL + search to imperfect-information games.
- Key abstraction: the *public belief state* (PBS) — a probability distribution over possible private information, updated via Bayes' rule as public actions are observed.
- **Why it matters for us:** The PBS framework provides the representational foundation for opponent modeling. If we can condition the belief state not just on Bayesian updates from game rules, but on inferred opponent behavioral patterns, we get a principled bridge from equilibrium play to adaptive play — this is the direction of Contribution 1.

#### 2.3 Opponent Modeling — Inferring Adversary Behavior (~0.5 page)

**Paper 5: Southey et al. (2005)** — "Bayes' Bluff: Opponent Modelling in Poker." *UAI.*
- Foundational work on Bayesian opponent modeling in imperfect-information games.
- Maintains a prior distribution over a parameterized space of opponent strategies; updates via Bayes' rule as hands are observed.
- Demonstrated that even rough opponent models can yield significant exploitation gains over Nash play.
- **What it left open:** The approach assumes a fixed, known parameterization of the opponent space. Real opponents may not fit any pre-defined type. The model does not address safety — exploiting a misidentified opponent type can lead to catastrophic losses. Also limited to two-player settings.

#### 2.4 Safe Exploitation — The Theoretical Core (~0.5 page)

**Paper 6: Ganzfried & Sandholm (2015)** — "Safe Opponent Exploitation." *ACM Transactions on Economics and Computation.*
- THE key paper for the thesis gap. Proves the Safety Theorem: in a two-player zero-sum game, any exploitation strategy that is anchored to a Nash equilibrium baseline (via the Restricted Nash Response formulation) cannot lose more than the Nash baseline against *any* opponent.
- Provides a formal framework for trading off exploitation potential vs. worst-case safety, parameterized by a safety coefficient p in [0,1].
- **What it left open (explicitly):** The Safety Theorem relies on the minimax property of Nash equilibrium in two-player zero-sum games. In N-player or general-sum games, Nash equilibrium does not guarantee safety against coalitions or correlated deviations. **The paper itself identifies the multiplayer extension as an open problem.** This is the exact gap that Contribution 2 targets.

#### 2.5 Scaling to Complex Domains — Regularization Approaches (~0.75 page)

**Paper 7: Bakhtin et al. (2022)** — "Human-Level Play in the Game of No-Press Diplomacy via Human-Regularized Reinforcement Learning and Planning." *Science.*
- Diplomacy: 7-player game with negotiation, coalition formation, and betrayal. No Nash equilibrium is computationally tractable, and even approximate equilibria are strategically meaningless (too many equilibria, none privileged).
- Key innovation: piKL regularization — instead of anchoring to Nash equilibrium (which doesn't exist meaningfully), anchor to a *human behavioral prior* learned from historical data. The KL-divergence penalty keeps the exploitation policy close to this prior, providing a practical safety substitute.
- **Why it matters for us:** piKL suggests a paradigm shift for Contribution 2 — replace equilibrium-based safety (which fails in N-player) with *behavioral-prior-based safety*. The prior can be a Nash strategy (recovering the two-player case), a population average, or a learned human model. This is the most promising direction for extending safe exploitation beyond two-player zero-sum.

**Paper 8: Perolat et al. (2022)** — "Mastering the Game of Stratego with Model-Free Multiagent Reinforcement Learning." *Science.*
- DeepNash: solved Stratego (10^535 game tree nodes — 10^175 times larger than Go) using Regularized Nash Dynamics (R-NaD).
- R-NaD directly modifies the learning dynamics to converge to Nash equilibrium rather than cycling, using a regularization term that discourages large deviations from the current policy iterate.
- **Why it matters for us:** R-NaD is conceptually aligned with piKL — both use regularization to tame the learning dynamics in large games. R-NaD demonstrates that regularization-based approaches scale to truly enormous imperfect-information games. For Contribution 2, this provides independent evidence that the regularization paradigm (rather than the equilibrium-anchoring paradigm) is the right foundation for safety in large-scale settings.

> **NEW PAPER — not currently in the study plan.** Perolat et al. (2022) is not listed in any step. It should be considered for inclusion in Step 6 (End-to-End Game AI Architectures) as a sixth landmark system alongside DeepStack, Libratus, Pluribus, ReBeL, and Student of Games. R-NaD provides an alternative equilibrium computation paradigm that complements the CFR-based approaches studied in Steps 3–5 and directly informs the regularization-based safety framework of Contribution 2.

#### Review Section Summary — The Gap

The eight papers above trace a clear arc:
- **CFR** (2007) made equilibrium computation practical.
- **Libratus** (2018) and **Pluribus** (2019) scaled it to superhuman performance.
- **ReBeL** (2020) unified RL and search under the public belief state framework.
- **Bayes' Bluff** (2005) showed that opponent modeling yields exploitation gains.
- **Ganzfried** (2015) formalized safe exploitation — but *only for two-player zero-sum games*.
- **Diplomacy** (2022) and **DeepNash** (2022) showed that regularization-based approaches work in large N-player and complex imperfect-info settings.

**The gap sits precisely between Ganzfried (2015) and the regularization papers (2022):** we have formal safety for two-player games and practical regularization for N-player games, but no framework that provides safety-aware adaptive exploitation in multi-agent settings with theoretical grounding.

---

### 3. Proposed Solution (~1.5 pages)

**Goal:** Present the three thesis contributions as a coherent response to the gap identified in the review. Frame each contribution around a specific limitation of the existing work and the proposed approach.

#### 3.1 Contribution 1 — Behavioral Adaptation Framework

**The limitation it addresses:** Existing game AI systems (Libratus, Pluribus, ReBeL) compute static equilibrium strategies that do not adapt to specific opponents. Opponent modeling methods (Bayes' Bluff) can infer opponent behavior but lack integration with the equilibrium-finding pipeline.

**The idea:** A general method for inferring opponent strategies from observed action sequences in real time and integrating those inferences into the agent's decision-making process. The framework operates over the public belief state representation (from ReBeL), augmenting Bayesian game-state beliefs with behavioral beliefs about opponent tendencies.

**Grounding in completed work:** Steps 1–2 established the RL and game-theoretic foundations. The CFR implementation on Kuhn Poker provides the equilibrium baseline against which adaptation is measured.

**Opportunistic applications:**
- Online gaming: detecting and adapting to bot behavior in real time
- Cybersecurity: inferring attacker strategies from network activity patterns
- Financial markets: adapting to adversarial trading strategies

**Honest scope:** The framework will be validated on a range of small-to-medium imperfect-information games chosen to stress different aspects of adaptation: card games with hidden hands (Kuhn Poker, Leduc Hold'em), sequential bidding games with hidden valuations (Goofspiel), and multi-agent environments with partial observability (pursuit-evasion on grid worlds, simplified Diplomacy variants without natural language). The methodology is designed to be domain-agnostic; validation spans multiple game types to demonstrate this, though scaling to truly large games remains an engineering challenge beyond the initial contribution.

#### 3.2 Contribution 2 — Multi-Agent Safe Exploitation

**The limitation it addresses:** The Safety Theorem (Ganzfried & Sandholm, 2015) guarantees that exploitation strategies cannot lose more than the Nash baseline in two-player zero-sum games. This guarantee provably fails in N-player settings, where coalition dynamics invalidate the minimax foundation. Pluribus demonstrated empirical success in 6-player poker without any safety framework. No existing work provides tractable safety heuristics for N-player exploitation.

**The idea:** Develop and empirically validate tractable heuristic approaches for safe exploitation in small N-player games — including 3-player card game variants, the coalition formation game So Long Sucker (4 players, designed by Nash and Shapley), and multi-agent grid environments where agents compete under partial observability. Two primary directions:
- **piKL-regularized exploitation:** Adapt the regularization paradigm from Diplomacy (Bakhtin et al., 2022), constraining the exploitative policy to remain close to a safe reference strategy via a KL-divergence penalty.
- **Equal-share baselines:** Use the equal-share value (each player's guaranteed minimum in a symmetric game) as an alternative safety anchor, bypassing the need for Nash equilibrium computation.

**What we are NOT claiming:** This is not a general N-player safety theorem. The contribution is empirical validation of practical heuristics on small games, identifying which approaches provide meaningful safety-exploitation tradeoffs and characterizing their failure modes.

**Opportunistic applications:**
- Fraud detection in multiplayer online platforms (directly maps to iGaming industry — multiple players, hidden information, potential collusion)
- Multi-party negotiation systems with safety constraints
- Adversarial network defense with multiple independent attackers

#### 3.3 Contribution 3 — Evaluation Methodology

**The limitation it addresses:** There is no standardized framework for evaluating adaptive game AI agents across different game environments and opponent populations. Existing metrics (exploitability, Elo rating) each capture only one dimension: exploitability measures worst-case vulnerability but ignores adaptation quality; Elo measures relative strength but cannot detect non-transitive (rock-paper-scissors) competitive structures.

**The idea:** A domain-agnostic three-layer evaluation framework:
- **Layer 1 — Individual safety:** Exploitability and marginal exploitability (N-player extension).
- **Layer 2 — Population ranking:** Alpha-Rank (evolutionary dynamics-based), VasE (social choice-based), and Elo, with disagreement analysis revealing when rankings diverge due to non-transitive structure.
- **Layer 3 — Statistical confidence:** AIVAT variance reduction for reliable evaluation under the high variance inherent to imperfect-information games.

The framework will be validated across heterogeneous game types (card games, bidding games, coalition games, grid-based multi-agent environments) to demonstrate domain-agnosticity — the evaluation methodology must work not just on one game family, but across structurally different strategic interactions.

**Opportunistic applications:**
- AI safety and alignment: standardized evaluation of autonomous decision-making systems across diverse adversarial conditions
- E-sports analytics: evaluating player strategies across different game environments
- Regulatory compliance: auditable evaluation of AI agents in high-stakes domains

---

### 4. Conclusion (~0.5–1 page)

**Goal:** Summarize the key findings from completed work, restate the identified gap and contributions, outline the research roadmap.

**Content:**
1. **Completed work summary:** Steps 1–2 established the RL and game-theoretic foundations. DQN and PPO were implemented from scratch and validated; Vanilla CFR was implemented for Kuhn Poker, verified against the analytical Nash equilibrium, and cross-validated against OpenSpiel.

2. **The gap (one-paragraph restatement):** The state of the art can compute equilibrium strategies for large imperfect-information games and can exploit specific opponents in two-player settings with safety guarantees. The open frontier is extending adaptive, safe exploitation to multi-agent environments — a problem with both theoretical depth and broad practical relevance.

3. **Future work — the research roadmap:**
   - Phases B–C (April–May 2026): Complete the algorithmic toolbox — Monte Carlo CFR, game abstraction, neural equilibrium approximation, survey of landmark game AI architectures.
   - Phase D (June–July 2026): The thesis-critical core — opponent modeling and safe exploitation algorithms.
   - Phases E–F (July–September 2026): Multi-agent dynamics, population training, coalition formation, real-world data pipelines.
   - Phase G (September–October 2026): Evaluation framework construction and research frontier mapping.
   - November 2026: Chapter I of the dissertation (state-of-the-art analysis, objectives, tasks, thesis statements).

4. **Closing sentence:** Something that ties back to the broader significance — the methods developed here are not specific to games but address the general problem of adaptive strategic decision-making under uncertainty with multiple adversaries, a setting that arises naturally across cybersecurity, financial markets, and autonomous systems.

---

## Additional Candidates for the Study Plan

Papers discovered during this planning that are NOT currently in the study plan and may strengthen the research program:

### Strong Candidate

**Perolat, J., De Vylder, B. et al. (2022).** "Mastering the Game of Stratego with Model-Free Multiagent Reinforcement Learning." *Science*, 378(6623), pp. 990–996.
- **Where it fits:** Step 6 (End-to-End Game AI Architectures) — as a sixth landmark system.
- **Why:** R-NaD provides an alternative equilibrium computation paradigm to CFR-based methods. The regularization approach directly informs Contribution 2 (piKL-regularized exploitation).
- **Impact on study plan:** Adds ~2 days to Step 6 for R-NaD study + comparison with ReBeL's approach.

### Worth Monitoring

**ODCFR (2025).** "On Deep CFR Integrated with Opponent Model in Imperfect Information Games." *Knowledge-Based Systems.*
- **Where it fits:** Between Steps 5 and 7 — bridges neural equilibrium approximation and opponent modeling.
- **Why:** Directly combines Deep CFR with online opponent modeling in a single framework. Very close to what Contribution 1 aims to generalize. Could serve as a baseline or inspiration.
- **Impact on study plan:** Read-only addition to Step 7 literature review (~1 day). No new implementation needed — our approach will differ in the safety-aware component.

---

## References (for the report itself)

1. Zinkevich, M., Johanson, M., Bowling, M. and Piccione, C. (2007). "Regret Minimization in Games with Incomplete Information." *NeurIPS.*
2. Brown, N. and Sandholm, T. (2018). "Superhuman AI for Heads-Up No-Limit Poker: Libratus Beats Top Professionals." *Science*, 359(6374).
3. Brown, N. and Sandholm, T. (2019). "Superhuman AI for Multiplayer Poker." *Science*, 365(6456).
4. Brown, N., Bakhtin, A., Lerer, A. and Hu, Q. (2020). "Combining Deep Reinforcement Learning and Search for Imperfect-Information Games." *NeurIPS.*
5. Southey, F., Bowling, M., Larson, B. et al. (2005). "Bayes' Bluff: Opponent Modelling in Poker." *UAI.*
6. Ganzfried, S. and Sandholm, T. (2015). "Safe Opponent Exploitation." *ACM Transactions on Economics and Computation*, 3(2).
7. Bakhtin, A., Wu, D.J., Lerer, A. et al. (2022). "Human-Level Play in the Game of No-Press Diplomacy via Human-Regularized Reinforcement Learning and Planning." *Science*, 378(6624).
8. Perolat, J., De Vylder, B. et al. (2022). "Mastering the Game of Stratego with Model-Free Multiagent Reinforcement Learning." *Science*, 378(6623).
