# Abstract {.unnumbered}

\begingroup
\footnotesize
\leftskip=2em
\rightskip=2em
\noindent Autonomous AI agents increasingly operate in competitive environments where trading systems react to hidden market positions, security tools face adaptive attackers, and online platforms confront coordinated bots or colluding participants. These settings require agents to reason under hidden information, infer behavioral patterns from limited observations, and adapt without unacceptable risk. Imperfect-information extensive-form games provide the mathematical framework for studying this problem. Over the past decade, Counterfactual Regret Minimization (CFR) and related neural methods have enabled superhuman performance in large-scale games such as two-player and six-player poker. However, these systems largely compute fixed equilibrium strategies that do not adapt to specific opponents, and the safety guarantees that support exploitation in two-player settings fail in multiplayer environments. This paper surveys equilibrium computation, opponent modeling, and safe exploitation for imperfect-information games; identifies the gap at the intersection of adaptive play and multiplayer safety; and proposes three doctoral contributions: a Behavioral Adaptation Framework for real-time opponent inference, Multi-Agent Safe Exploitation heuristics grounded in regularization-based safety, and a domain-agnostic Evaluation Methodology for measuring adaptability and robustness across heterogeneous game environments.
\par
\endgroup

# Introduction

Autonomous AI agents are increasingly deployed in open environments where success depends not only on prediction or control, but on strategic interaction: trading systems react to hidden market positions, security tools face adaptive attackers, platform moderators confront coordinated bots, and multi-agent services negotiate with unfamiliar human or artificial participants. In such settings, each decision is made under partial information about other actors' goals, private knowledge, and future behavior. This makes isolated single-agent training insufficient. The central research problem is how an agent can infer behavioral patterns from limited observations, adapt its strategy in real time, and do so without exposing itself to unacceptable risk.

This challenge is, at its mathematical foundation, a problem in imperfect-information extensive-form games. These games model sequential interaction among multiple players who hold private information, face stochastic outcomes, and act without full knowledge of either the environment state or the strategies of others. They are useful not merely as academic benchmarks, but as compact abstractions of the same strategic structure found in real-world multi-agent systems. Poker became the canonical testbed because it combines hidden information, sequential actions, stochastic outcomes, and self-interested players while still providing an unambiguous win criterion. Landmark systems --- Counterfactual Regret Minimization (CFR) [1], Libratus [2], Pluribus [3], and ReBeL [4] --- were validated mainly on poker variants, but the underlying methods are domain-agnostic and have since informed work on broader strategic domains such as Diplomacy [7] and Stratego [8].

The past decade has seen remarkable progress in equilibrium-finding algorithms for progressively larger games. CFR was scaled via Monte Carlo sampling, neural function approximation, and real-time subgame solving, culminating in superhuman performance in both two-player [2] and six-player poker [3]. However, these systems share a fundamental limitation: they compute *fixed* equilibrium strategies that play identically against every opponent. Against sub-optimal adversaries --- which includes virtually all real-world opponents, human or artificial --- an equilibrium strategy is safe but blind, systematically failing to exploit detectable weaknesses. Furthermore, as games scale to many players, even the notion of "safe" becomes problematic: Nash equilibrium loses its minimax guarantee, and the research paradigm must shift from computing perfect solutions in controlled settings to enabling rapid adaptation in environments too complex for any single equilibrium to suffice.

This situation exposes three interrelated open problems. First, *adaptation*: how can an agent infer an opponent's behavioral tendencies from observed actions and adjust its own strategy in real time, when the opponent's private information and intentions remain hidden? Second, *safety under adaptation*: how can an agent exploit detected weaknesses while bounding worst-case losses --- particularly in $N$-player settings where formal safety guarantees from two-player theory provably fail? Third, *evaluation*: how do we reliably measure whether an agent adapts well, across different games, opponent populations, and environmental conditions, when existing metrics each capture only a single dimension of performance?

The present doctoral research addresses these three open problems through three contributions: a Behavioral Adaptation Framework for real-time opponent inference, Multi-Agent Safe Exploitation heuristics for bounded-risk adaptation, and a domain-agnostic Evaluation Methodology for measuring adaptability and robustness across heterogeneous game environments. Each contribution is grounded in working implementations and evaluated against analytical solutions or reference frameworks, so that the research program remains experimental rather than purely synthetic.


# Review of Existing Solutions

The algorithmic foundation for computing strategies in imperfect-information games was established by Counterfactual Regret Minimization (CFR) [1], which decomposes the problem of finding a Nash equilibrium into independent local subproblems at each decision point and guarantees convergence of the average strategy at a rate of $O(1/\sqrt{T})$. CFR made computational game theory practical, but required scaling work to handle large games: Monte Carlo sampling reduced per-iteration cost, while neural function approximation replaced tabular storage with deep networks. The practical payoff of these advances was demonstrated by Libratus [2], which defeated top professionals in two-player no-limit poker, and Pluribus [3], which extended this to six-player poker. ReBeL [4] subsequently unified reinforcement learning and search under the *public belief state* framework --- a probability distribution over hidden information, updated via Bayesian inference as play unfolds --- bringing AlphaZero-style methods to imperfect-information games. Collectively, these systems represent a decade of progress in computing equilibrium strategies for progressively larger and more complex games.

However, these systems retain the limitation introduced above: they compute *fixed* strategies and play identically against every opponent. The question of adapting to a specific opponent was addressed by Southey et al. [5], who developed a Bayesian framework for opponent modeling that maintains a prior over opponent strategy types and updates it from observed actions. Even rough opponent models were shown to yield significant exploitation gains over equilibrium play. The formal treatment of *safety* during exploitation was provided by Ganzfried and Sandholm [6], who proved the Safety Theorem: in a two-player zero-sum game, any exploitation strategy anchored to a Nash equilibrium baseline cannot lose more than that baseline against any opponent, regardless of model accuracy. A safety parameter $p \in [0,1]$ controls the tradeoff between exploitation potential and worst-case protection. This is a foundational result --- but the Safety Theorem relies on the minimax property of Nash equilibrium, which holds only in two-player zero-sum games. In $N$-player or general-sum settings, Nash equilibrium does not protect against coalitions or correlated deviations, and the paper itself identifies the multiplayer extension as an open problem.

Two recent systems suggest a direction forward. Bakhtin et al. [7] achieved human-level play in Diplomacy --- a seven-player game with coalition formation and betrayal --- using $\pi$KL regularization, which anchors the agent not to a Nash equilibrium (computationally intractable and strategically meaningless in this setting) but to a *human behavioral prior* learned from data, with a KL-divergence penalty preventing excessive deviation. Independently, Perolat et al. [8] solved Stratego using Regularized Nash Dynamics (R-NaD), a model-free approach that uses regularization to converge to Nash equilibrium rather than cycling. Both systems demonstrate that regularization-based methods can tame learning dynamics at enormous scale --- but neither adapts to specific opponents, and no existing work systematically studies the exploitation--safety tradeoff in multiplayer settings or provides a framework for evaluating adaptive behavior across different game environments.

Notably, the game-theoretic solvers currently in operational or near-operational use --- security-patrol randomization systems, simulated air-combat research agents, and auction-design engines underlying multi-billion-dollar spectrum allocations --- all rely on *fixed* equilibrium or equilibrium-adjacent strategies. They inherit, by design, exactly the three limitations this thesis targets: no runtime adaptation to specific opponents, no formal safety guarantees once the setting extends beyond two players, and no standardized methodology for evaluating adaptive behavior across heterogeneous strategic environments. The research gap identified in the literature is therefore not merely academic; it is the gap that separates today's deployed systems from the next generation of operationally adaptive, safety-aware multi-agent AI.


# Proposed Solution

The review reveals the central gap in the current state of the art: we have formal safety guarantees for two-player exploitation and practical regularization for large multi-agent games, but no framework that connects them --- providing safety-aware adaptive exploitation in multiplayer settings with systematic evaluation. The three contributions below address this gap from complementary angles: inference (how to model opponents), action (how to exploit safely), and measurement (how to evaluate the result).

## Contribution 1: Behavioral Adaptation Framework

Existing game AI systems compute equilibrium strategies that are blind to opponent-specific behavioral patterns. Opponent modeling methods [5] can infer behavior but lack integration with the equilibrium-finding pipeline and do not account for the risk of model misspecification. The first contribution targets a general method for inferring opponent strategies from observed action sequences in real time and integrating those inferences into the agent's decision-making process. Candidate architectures include augmenting the public belief state representation [4] with behavioral beliefs about opponent tendencies --- extending the belief state from "what private information might the opponent hold?" to "what type of player is the opponent?" --- as well as consistent opponent modeling techniques that guarantee convergence to the opponent's true strategy given sufficient observations.

A critical design constraint is graceful degradation: when insufficient observations have been collected, the agent should default to equilibrium play rather than acting on unreliable inferences. The framework will be validated on structurally diverse games --- card games with hidden hands (Kuhn Poker, Leduc Hold'em), sequential bidding games with hidden valuations (Goofspiel), and multi-agent environments with partial observability (pursuit-evasion on grid worlds, simplified Diplomacy variants) --- to demonstrate domain-agnostic applicability. A natural byproduct of this work is the ability to detect and classify anomalous behavior, with direct applications in fraud detection, bot identification, and collusion detection on multiplayer platforms.

## Contribution 2: Multi-Agent Safe Exploitation

The Safety Theorem [6] provides formal guarantees for exploitation in two-player zero-sum games, but these guarantees provably fail in $N$-player settings where coalition dynamics invalidate the minimax foundation. Pluribus [3] demonstrated empirical success in six-player poker without any safety framework, but offers no theoretical grounding for when or why such success generalizes. The second contribution targets tractable approaches for safe exploitation in $N$-player imperfect-information games, investigating several candidate directions.

The most promising direction adapts the $\pi$KL regularization paradigm from Diplomacy [7], constraining the exploitative policy to remain close to a safe reference strategy via a KL-divergence penalty. The reference strategy need not be a Nash equilibrium --- it can be a population average, a learned behavioral prior, or an approximate equilibrium --- making the approach applicable when exact equilibrium computation is intractable. An alternative direction explores equal-share baselines, using each player's guaranteed minimum payoff as a safety anchor that bypasses equilibrium computation entirely. Validation is planned across $N$-player game variants including three-player card games, the four-player coalition formation game So Long Sucker, and multi-agent grid environments with partial observability.

## Contribution 3: Evaluation Methodology

There is currently no standardized framework for evaluating adaptive agents across different game environments and opponent populations. Exploitability measures worst-case vulnerability but ignores adaptation quality; Elo rating measures relative strength but cannot detect cyclic dominance; and variance in imperfect-information games makes raw win rates statistically unreliable. The third contribution targets a domain-agnostic evaluation framework combining individual safety metrics (exploitability and its $N$-player extension), population-level ranking methods sensitive to non-transitive dynamics ($\alpha$-Rank [9]), and variance reduction techniques (AIVAT [10]) for statistically reliable evaluation under the high variance inherent to imperfect-information games. The framework will be validated across heterogeneous game types to ensure that evaluations are comparable across structurally different strategic interactions.

## Expected Outcomes

The scope of each contribution depends on algorithmic choices made during the study program, which continues through October 2026, and on the available resources. The progressions below distinguish the grounded starting point from the realistic thesis target; further depth is kept as a direction, not promised as an outcome.

Work on **Contribution 1** begins by showing that the adaptation framework outperforms static equilibrium play on the primary testbeds (Kuhn Poker, Leduc Hold'em). The realistic target is to extend this validation to structurally different game families --- card games, bidding games, and grid-based environments --- so that adaptation gains hold beyond card games. Convergence guarantees for opponent-type inference remain an open direction, depending on how the later study steps unfold.

**Contribution 2** begins with empirical validation of existing heuristics --- $\pi$KL regularization and equal-share baselines --- on small $N$-player games, with failure modes characterized so that the exploitation--safety tradeoff is mapped rather than asserted. The realistic target is a method that combines these heuristics with opponent-aware or population-based dynamics in ways the literature has not yet covered. A theoretical extension of the Safety Theorem beyond two-player zero-sum games remains in view, but the thesis does not depend on reaching it.

**Contribution 3** begins by ensuring that the evaluation framework reproduces known agent orderings and detects known non-transitive structures across benchmark games. The realistic target is to extend the framework to real-world behavioral data, such as anonymized game logs, so that it produces actionable insights beyond synthetic benchmarks. Specific findings cannot be pre-specified honestly; the value of the framework lies in what it reveals when applied.

Together, these grounded outcomes --- a validated adaptation method, empirically characterized safety heuristics, and a working evaluation framework --- already constitute a coherent thesis. Further depth from later study steps would build on this foundation rather than replace it.


# Conclusion

The foundational phase of this doctoral research is complete. The literature review shows that the state of the art can compute equilibrium strategies at superhuman levels and exploit specific opponents safely in two-player settings, but no existing framework provides safety-aware adaptive exploitation in multi-agent environments with systematic evaluation. The three proposed contributions --- Behavioral Adaptation, Multi-Agent Safe Exploitation, and Evaluation Methodology --- address this gap from complementary angles, with expectations calibrated to the available resources and timeline.

The methods under development are not specific to any single game or domain. They address adaptive strategic decision-making under uncertainty with multiple adversaries --- a setting that arises wherever autonomous agents interact under hidden information. As such agents become more common in real-world systems, ensuring that they adapt safely and can be reliably evaluated becomes a practical necessity.


\newpage

# References {.unnumbered}

\footnotesize

[1] Zinkevich, M., Johanson, M., Bowling, M. and Piccione, C. (2007). "Regret Minimization in Games with Incomplete Information." *Advances in Neural Information Processing Systems 20 (NeurIPS).*

[2] Brown, N. and Sandholm, T. (2018). "Superhuman AI for Heads-Up No-Limit Poker: Libratus Beats Top Professionals." *Science*, 359(6374), pp. 418--424.

[3] Brown, N. and Sandholm, T. (2019). "Superhuman AI for Multiplayer Poker." *Science*, 365(6456), pp. 885--890.

[4] Brown, N., Bakhtin, A., Lerer, A. and Hu, Q. (2020). "Combining Deep Reinforcement Learning and Search for Imperfect-Information Games." *Advances in Neural Information Processing Systems (NeurIPS).*

[5] Southey, F., Bowling, M., Larson, B., Piccione, C., Burch, N., Billings, D. and Rayner, C. (2005). "Bayes' Bluff: Opponent Modelling in Poker." *Proceedings of the 21st Conference on Uncertainty in Artificial Intelligence (UAI).*

[6] Ganzfried, S. and Sandholm, T. (2015). "Safe Opponent Exploitation." *ACM Transactions on Economics and Computation*, 3(2).

[7] Bakhtin, A., Wu, D.J., Lerer, A., Gray, J., Jacob, A.P., Farina, G., Miller, A.H. and Brown, N. (2022). "Human-Level Play in the Game of No-Press Diplomacy via Human-Regularized Reinforcement Learning and Planning." *Science*, 378(6624), pp. 1067--1074.

[8] Perolat, J., De Vylder, B., Hennes, D. et al. (2022). "Mastering the Game of Stratego with Model-Free Multiagent Reinforcement Learning." *Science*, 378(6623), pp. 990--996.

[9] Omidshafiei, S., Papadimitriou, C., Piliouras, G., Tuyls, K. et al. (2019). "$\alpha$-Rank: Multi-Agent Evaluation by Evolution." *Nature Scientific Reports.*

[10] Burch, N., Johanson, M. and Bowling, M. (2019). "AIVAT: A New Variance Reduction Technique for Agent Evaluation in Imperfect Information Games." *Proceedings of the 33rd AAAI Conference on Artificial Intelligence.*

\normalsize
