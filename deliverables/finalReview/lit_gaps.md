# Gap validation (checked 2026-09)

*Checked on 2026-09-24. For each contribution I took the gap as the repository currently
states it and tried to disprove it. The claims come from `PLAN.md` §2,
`CHAPTER1_SKELETON.md`, the frontier map in `planning/rawSteps/step_15…`, and the May progress
report `deliverables/reports/ruseMay/report.md`. The search covered arXiv, the
NeurIPS/ICML/ICLR/AAAI/IJCAI/AAMAS proceedings, PMLR and AAAI OJS, using targeted queries per
contribution and forward searches from the key papers (OX-Search, equal share, VasE).*

*Limitations. OpenReview pages were behind a bot check, so ICLR 2026 submissions could not be
read. No Google Scholar citation-chain crawl was possible. Papers from 2026 are unrefereed
arXiv preprints unless a venue is stated. Each verdict therefore reads "no counter-example
found", not "none exists". Keys match `lit_evaluation.md`.*

---

## C1 — Behavioral Adaptation Framework (real-time opponent inference)

### Claimed gap

- The skeleton, §1.4, says there is "no unified detect → adapt → evaluate loop". §1.3 ends with
  "every landmark system plays a fixed approximate equilibrium — nobody adapts".
- The step-15 frontier map lists three gaps. "No unified framework for detect → adapt (papers
  do one, not both)". "Static detection only — no temporal adaptation". "Not cross-game;
  poker-specific".
- The May report says opponent-modelling methods "can infer behavior but lack integration with
  the equilibrium-finding pipeline and do not account for the risk of model misspecification".

### Closest recent work

**Detect → adapt with a conservative fallback, including non-stationary opponents**

- **[Fu 2022]** H. Fu, Y. Tian, H. Yu, W. Liu, S. Wu, J. Xiong, Y. Wen, K. Li, J. Xing, Q. Fu, W. Yang, "Greedy when sure and conservative when uncertain about the opponents" (GSCU), *ICML*, PMLR 162, 6829–6848, 2022.
  - *What it does.* It keeps an online posterior over an opponent-policy embedding and plays a
    single best response conditioned on that embedding. An adversarial bandit switches between
    this greedy policy and a fixed conservative one, with a regret guarantee. It was tested on
    **Kuhn poker** and a four-player Predator-Prey game, against opponent sequences that were
    seen, unseen, mixed, or *adapting*.
  - *What it does not do.* The conservative policy is a fallback, not a bound on
    exploitability. It has no N-player imperfect-information testbed.
  - [verified: PMLR abstract; the environments come from a search summary of the paper and
    GitHub repo]
- **[Ma 2024]** L. Ma, Y. Wang, F. Zhong, S.-C. Zhu, Y. Wang, "Fast peer adaptation with context-aware exploration" (PACE), *ICML*, 2024; arXiv:2402.02468.
  - *What it does.* A peer-identification reward makes the agent explore when it is unsure of
    the peer's strategy and exploit when it is confident. It is tested on **Kuhn poker**,
    PO-Overcooked and Predator-Prey-W.
  - *What it does not do.* It offers no safety criterion.
  - [verified: arXiv metadata]

**In-context and sequence-model opponent modelling**

- **[Jing 2024a]** Y. Jing, K. Li, B. Liu, Y. Zang, H. Fu, Q. Fu, J. Xing, J. Cheng, "Towards offline opponent modeling with in-context learning" (TAO), *ICLR*, 2024.
  - *What it does.* It learns from offline data a transformer that recognises opponents in
    context. The authors show this is equivalent to Bayesian posterior sampling and that it
    adapts quickly to unseen *fixed* opponents.
  - [verified: ICLR proceedings]
- **[Jing 2024b]** Y. Jing, B. Liu, K. Li, Y. Zang, H. Fu, Q. Fu, J. Xing, J. Cheng, "Opponent modeling with in-context search" (OMIS), *NeurIPS*, 2024.
  - *What it does.* It combines an in-context actor, opponent imitator and critic with
    decision-time search. The opponents are unknown and switch policy *between episodes*.
    Experiments use Predator-Prey, Level-Based Foraging and Overcooked.
  - *What it does not do.* It has no imperfect-information card games.
  - [verified: NeurIPS PDF text]
- **[Jing 2025]** Y. Jing et al., "An open-ended learning framework for opponent modeling" (OEOM), *AAAI*, 39(22), 23222–23230, 2025, doi:10.1609/aaai.v39i22.34488.
  - *What it does.* It generates a diverse opponent population so that the modeller
    generalises to unseen opponents.
  - [verified: AAAI OJS + Crossref]
- **[Caen 2026]** A. Caen, M. H. M. Winands, D. J. N. J. Soemers, "StratFormer: Adaptive opponent modeling and exploitation in imperfect-information games," *Computers and Games 2026* (accepted); arXiv:2604.25796.
  - *What it does.* This is the closest single paper to C1. It works on **Leduc**, heads-up. A
    transformer models the opponent from action histories while the agent plays GTO, then
    shifts toward a best response. How far it shifts is set by a regularisation schedule tied
    to the opponent's exploitability. It reports NashConv and a loss of −0.050 BB/hand against
    GTO.
  - *What it does not do.* The authors list non-stationary opponents and human opponents as
    future work. It is not N-player.
  - [verified: arXiv abstract + HTML]
- **[Murgoci 2026]** V. Murgoci, M. Spaan, Y. Oren, "AlphaExploitem: Going beyond the Nash equilibrium in poker by learning to exploit suboptimal play," arXiv:2605.09150, 2026.
  - *What it does.* It works on **Kuhn and Leduc**, heads-up. A hierarchical transformer reads
    all previously played hands against the current opponent, and the agent is trained against
    a pool of exploitable opponents. It exploits both in- and out-of-distribution opponents and
    stays close to equilibrium value against a Nash opponent.
  - *What it does not do.* It gives no formal safety guarantee and is two-player only.
  - [verified: arXiv abstract + HTML]

**Opponent models inside equilibrium search in large games**

- **[Milec 2024]** D. Milec, O. Kubíček, V. Lisý, "Continual depth-limited responses for computing counter-strategies in sequential games," *AAMAS* (extended abstract), 2024, pp. 2393–2395; arXiv:2112.12594.
  - [verified: Crossref + arXiv]
- **[Milec 2025]** D. Milec, V. Kovařík, V. Lisý, "Adapting beyond the depth limit: Counter strategies in large imperfect information games" (ABD), *AAMAS* (extended abstract), 2025, pp. 2675–2677; arXiv:2501.10464.
  - *What both do.* They give a robust response to an opponent model inside depth-limited
    search, tested on poker and battleship.
  - *What they do not do.* The model is **given**, not learned online, and both are two-player.
  - [verified: Crossref + IFAAMAS PDF listing]
- **[Ganzfried 2025]** S. Ganzfried, "Consistent opponent modeling in imperfect-information games," arXiv:2508.17671, v8 July 2026.
  - *What it does.* It proves convergence to the true strategy of a *static* opponent.
  - [verified: arXiv]

**N-player imperfect-information games**

- **[Ganzfried 2024]** S. Ganzfried, K. A. Wang, M. Chiswick, "Opponent modeling in multiplayer imperfect-information games," in *Proc. 6th Int. Conf. Distributed Artificial Intelligence (DAI '24)*, 2024, pp. 39–45, doi:10.1145/3719545.3721108; arXiv:2212.06027.
  - *What it does.* In **three-player Kuhn poker**, opponent modelling significantly
    outperforms all agents it plays, including exact Nash equilibrium strategies.
  - *What it does not do.* It has no safety notion.
  - [verified: Crossref + arXiv]
- **[Shi 2025]** D. Shi, X. Guo, Y. Liu, W. Fan, "Adaptive multi-player poker policy learning based on opponent style modeling," *Neural Computing and Applications*, 37(19), 13525–13546, 2025, doi:10.1007/s00521-025-11262-x.
  - *What it does.* It predicts opponent-style features in multi-player Texas Hold'em and
    feeds them to an actor-critic policy.
  - *What it does not do.* It has no safety notion.
  - [verified: Crossref + abstract listing]
- **[Cross 2025]** L. Cross, V. Xiang, A. Bhatia, D. L. K. Yamins, N. Haber, "Hypothetical Minds: Scaffolding theory of mind for multi-agent tasks with large language models," *ICLR*, 2025; arXiv:2407.07086.
  - *What it does.* An LLM agent generates natural-language hypotheses about other agents'
    strategies and refines them from their observed behaviour. It is tested in Melting Pot,
    including N-player population substrates.
  - [verified: ICLR proceedings + arXiv]

**LLM agents in imperfect-information card games**

- **[Guo 2023]** J. Guo, B. Yang, P. Yoo, B. Y. Lin, Y. Iwasawa, Y. Matsuo, "Suspicion-Agent: Playing imperfect information games with theory of mind aware GPT-4," arXiv:2309.17277, 2023.
  - *What it does.* It is a prompted GPT-4 agent that adapts its play to the opponent. Leduc
    Hold'em is the quantitative testbed.
  - [verified: arXiv]
- **[Zhang 2024]** W. Zhang, K. Tang, H. Wu, M. Wang, Y. Shen, G. Hou, et al., "Agent-Pro: Learning to evolve via policy-level reflection and optimization," *ACL*, 2024, pp. 5348–5375, doi:10.18653/v1/2024.acl-long.292.
  - *What it does.* It refines an LLM's beliefs at the policy level through reflection. It is
    tested on Blackjack and Limit Texas Hold'em.
  - [verified: ACL Anthology + Crossref]
- **[Lin 2026]** H.-T. Lin, T.-Y. Hou, "Readable Minds: Emergent theory-of-mind-like behavior in LLM poker agents," arXiv:2604.04157, 2026 (submitted to PNAS).
  - *What it does.* Poker agents with memory deviate from GTO to exploit specific opponents.
  - [verified: arXiv]
- **[Xu 2025b]** S. Xu, S. Cui, Y. Wang, B. Xu, Q. Wang, "Strategy-augmented planning for large language models via opponent exploitation," *IJCNN*, 2025; arXiv:2505.08459.
  - *What it does.* It recognises the opponent's strategy and greedily best-responds to it.
    The testbed is MicroRTS, not imperfect-information cards.
  - [verified: arXiv comments]

**Surveys to anchor §1.4**

- [Nashed & Zilberstein 2022] S. Nashed, S. Zilberstein, *JAIR* 73, 277–327, doi:10.1613/jair.1.12889.
- [Albrecht & Stone 2018] S. V. Albrecht, P. Stone, *Artificial Intelligence* 258, 66–95, doi:10.1016/j.artint.2018.01.002.
- [Hernandez-Leal 2017] P. Hernandez-Leal, M. Kaisers, T. Baarslag, E. Munoz de Cote, "A survey of learning in multiagent environments: Dealing with non-stationarity," arXiv:1707.09183.
- [verified: JAIR/Crossref, Crossref, arXiv respectively]

### Verdict: **narrowed (substantially)**

Three of the stated sub-gaps are no longer true as general statements.

- **"Papers do one, not both."** GSCU (2022) and PACE (2024) detect and adapt online, and both
  do so in Kuhn poker as well as non-poker games.
- **"No temporal adaptation."** GSCU is evaluated explicitly against switching and *adapting*
  opponents, with a conservative fallback.
- **"Poker-specific."** The 2024 in-context methods are cross-domain.
- **No integrated model-and-exploit agent.** StratFormer and AlphaExploitem (2026) model and
  exploit opponents in small poker games while staying anchored to equilibrium.
- **No link to equilibrium search.** ABD links opponent models to equilibrium search in large
  imperfect-information games.

Four parts remain open; no counter-example was found for any of them.

1. **N-player adaptation with safety.** Online inference and adaptation in N-player
   imperfect-information games that is paired with an explicit, measured safety criterion.
   Every N-player work found has none [Ganzfried 2024; Shi 2025].
2. **Shifts within a match.** Opponents that change strategy *within* a match in
   imperfect-information games, with the cost of detection and recovery reported. GSCU and
   OMIS switch opponents between episodes, and StratFormer lists this as future work.
3. **A learned model coupled to the safe pipeline.** An opponent model that is *learned*
   online, rather than given as in ABD, and coupled to a blueprint-plus-safe-response pipeline.
   This is done only in small two-player games (StratFormer, AlphaExploitem).
4. **One protocol across games.** The same inference mechanism evaluated under one common
   protocol across structurally different imperfect-information games. This overlaps with C3.

### How Chapter I should phrase the gap

> Real-time opponent modelling is an active field. Online Bayesian or in-context inference is
> combined with a conservative fallback against switching opponents [Fu 2022; Jing 2024b].
> Recent transformer agents model and exploit opponents in small poker games while staying
> close to equilibrium [Caen 2026; Murgoci 2026]. Opponent models have been integrated into
> depth-limited equilibrium search in large games [Milec 2025]. These methods are two-player,
> however. Each is evaluated on its own opponent set, and none offers a loss bound in games
> with more than two players. Opponent modelling in three-player poker exists [Ganzfried 2024],
> but without any safety criterion. C1 therefore does not claim the detect–adapt loop itself.
> It claims the loop's extension to N-player imperfect-information games with within-match
> strategy shifts, coupled to an explicit safety criterion (C2) and measured under a common
> protocol (C3).

Avoid "no unified detect → adapt framework exists", "opponent modelling is static only" and
"nobody adapts". In §1.3, write instead "none of the landmark superhuman systems adapts to
its opponents". Pluribus's own paper states that it "plays a fixed strategy that does not
adapt" [Brown 2019].

---

## C2 — Multi-Agent Safe Exploitation (small N-player games)

### Claimed gap

- The skeleton, §1.5, says "safety theory stops at two players; coalitions/collusion break it".
  The scope is stated as "no general N-player safety theorem is claimed".
- The step-15 map lists four gaps. "ALL safe exploit is 2-player zero-sum". "Minimax theorem
  fails N>2". "'Equal share' is NEW, no exploitation on top of it". "Coalition dynamics
  unstudied".
- `PLAN.md` §2 names the planned method: piKL-regularised exploitation with an equal-share
  baseline on three-player Kuhn and Leduc.
- The May report says "no existing work systematically studies the exploitation–safety
  tradeoff in multiplayer settings". It also describes equal share as "each player's guaranteed
  minimum payoff".

### Closest recent work

**Two-player safe exploitation is still advancing and still two-player**

This group confirms where the two-player boundary lies.

- **[Ge 2024]** Z. Ge, Z. Xu, T. Ding, L. Meng, B. An, W. Li, Y. Gao, "Safe and robust subgame exploitation in imperfect information games," *ICML*, PMLR 235, 15255–15270, 2024.
  - *What it does.* It defines adaptation safety (be no more exploitable than the blueprint)
    and implements it in OX-Search.
  - *What it does not do.* It is two-player zero-sum only.
  - [verified: PMLR]
- **[Li & Huang 2026]** B. Li, L. Huang, "Agents that certify their own exploits: Confidence-scheduled restricted responses for safe opponent exploitation," arXiv:2607.28520, 2026.
  - *What it does.* It issues a per-deployment safety certificate, built from confidence
    sequences, for restricted-response exploitation. Tested on Leduc and Liar's Dice.
  - *What it does not do.* It is **two-player zero-sum only**.
  - [verified: arXiv abstract]
- **[Guo 2026]** J. Guo, "Safe observation capacity for opponent exploitation under showdown censoring," arXiv:2608.09954, 2026.
  - *What it does.* It handles the fact that folded hands are never shown, which biases the
    data used to model the opponent. Two-player.
  - [verified: arXiv]
- **[Kubíček 2026]** O. Kubíček, V. Lisý, T. Sandholm, "Test-time reinforcement learning in imperfect information games," arXiv:2608.30635, 2026.
  - *What it does.* It proves that regularised test-time policy gradient keeps strategy
    degradation bounded.
  - *What it does not do.* It is two-player zero-sum, with no opponent model.
  - [verified: arXiv]
- **[Müller 2025]** A. Müller, J. Schneider, S. Skoulakis, L. Viano, V. Cevher, "Best of both worlds: Regret minimization versus minimax play," *ICML*, 2025; arXiv:2502.11673.
  - *What it does.* With bandit feedback it achieves O(1) regret against a *given comparator
    strategy* and Õ(√T) regret against any fixed strategy. Applied to two-player zero-sum
    games, the agent risks only O(1) loss while gaining Ω(T) from exploitable opponents.
  - *Relevance to C2 (analysis).* Safety is defined relative to a baseline's realised payoff
    and does not itself need the minimax theorem. In an N-player game it would mean "never much
    worse than the baseline would have done against the same opponents". That is a candidate
    safety notion for C2, but it is not a worst-case guarantee.
  - [verified: arXiv + ML Anthology ICML 2025]

**Safety notions for N-player games and coalitions already exist**

- **[Ge 2025]** J. Ge, Y. Wang, W. Li, C. Jin, "Securing equal share: A principled approach for learning multiplayer symmetric games," *ICML*, 2025, pp. 18989–19010; arXiv:2406.04201.
  - *What it does.* Equal share is an expected payoff of C/n in an n-player symmetric
    constant-sum game with total payoff C. It is achievable with no-regret learning (Hedge)
    **only if all opponents play the same strategy and do not adapt arbitrarily fast**.
  - *What it proves impossible.* Equal share **cannot be secured** against opponents that play
    *different* fixed strategies (Prop. 4.1), or against arbitrarily adapting ones (Prop. 4.2).
  - *Experiments.* Three-player Majority Vote and a 30-player Switch Dominance game. There,
    self-play meta-algorithms like those in prior multiplayer systems fail to secure equal
    share.
  - *What it does not do.* It does no exploitation and uses no imperfect-information testbed.
  - [verified: arXiv HTML, Props. 4.1–4.2]
- **Adversarial team games** give a worst-case value against a coordinated coalition, under
  three communication regimes:
  - [Celli & Gatti 2018] *AAAI*, doi:10.1609/aaai.v32i1.11462.
  - [Zhang 2021] Y. Zhang, B. An, J. Černý, *AAAI* 35(6), 5813–5821, doi:10.1609/aaai.v35i6.16728. It names poker and bridge teams as the use case.
  - [Zhang 2023] B. H. Zhang, G. Farina, T. Sandholm, *ICML*, PMLR 202.
  - [verified: Crossref/PMLR]
- **[Babyak 2024]** J. Babyak, K. Buck, L. Dichter, D. Jiang, K. Zumbrun, "Synchronous vs. asynchronous coalitions in multiplayer games, with applications to guts poker," arXiv:2412.19855, 2024.
  - *What it does.* It compares three values: symmetric Nash, asynchronous-coalition optimum and
    synchronous-coalition optimum. The asynchronous optimum is a nonconvex problem. Tested on
    three-player rock-paper-scissors and discretised Guts poker.
  - [verified: arXiv metadata; note the arXiv title misspells "Sychronous"]
- **[Szafron 2013]** It shows that in three-player Kuhn poker a player can transfer utility
  between the other two while staying inside an equilibrium family.
  - [verified: IFAAMAS listing]

**N-player exploitation without any safety notion**

- [Ganzfried 2024] and [Shi 2025], see C1.
- [Brown 2019]: Pluribus is a fixed strategy.

**KL-anchored policies are behavioural anchors, not safety guarantees**

- **[Jacob 2022]** A. P. Jacob, D. J. Wu, G. Farina, A. Lerer, H. Hu, A. Bakhtin, J. Andreas, N. Brown, "Modeling strong and human-like gameplay with KL-regularized search" (piKL), *ICML*, 2022; arXiv:2112.07544.
  - *What it does.* It regularises search toward an **imitation-learned human policy**, in
    chess and Go, with a Hanabi extension.
  - [verified: arXiv metadata + PMLR PDF link]
- **[Bakhtin 2023]** A. Bakhtin, D. J. Wu, A. Lerer, J. Gray, A. P. Jacob, G. Farina, A. H. Miller, N. Brown, "Mastering the game of no-press Diplomacy via human-regularized reinforcement learning and planning" (DiL-piKL), *ICLR*, 2023; arXiv:2210.05492.
  - *What it does.* It applies the same human-regularised approach to seven-player no-press
    Diplomacy. It is evaluated by score and Elo against humans.
  - *What it does not do.* It gives no exploitability or loss bound.
  - [verified: arXiv + ICLR listing]
- **[FAIR 2022]** Meta Fundamental AI Research Diplomacy Team (FAIR), A. Bakhtin, N. Brown, E. Dinan, et al., "Human-level play in the game of Diplomacy by combining language models with strategic reasoning" (CICERO), *Science* 378(6624), 1067–1074, 2022, doi:10.1126/science.ade9097.
  - [verified: Crossref + ADS]
- **[Sokota 2023]** S. Sokota, R. D'Orazio, J. Z. Kolter, N. Loizou, M. Lanctot, I. Mitliagkas, N. Brown, C. Kroer, "A unified approach to reinforcement learning, quantal response equilibria, and two-player zero-sum games" (magnetic mirror descent), *ICLR*, 2023.
  - *What it does.* It regularises toward an anchor ("magnet") policy. Two-player zero-sum.
  - [verified: arXiv + author page]
- **[Shen & How 2022]** M. Shen, J. P. How, "Safe adaptation in multiagent competition," arXiv:2203.07562.
  - *What it does.* It regularises the opponent model so that adaptation stays hard to
    exploit. Two-player MuJoCo.
  - [verified: arXiv]
- [Caen 2026] also regularises toward GTO, but in a two-player game.

**Collusion detection**

- [Mazrooei 2013] uses collusion tables in poker (*AAAI*).
- [Bonjour 2022] measures mutual information between agents' actions, in iterated RPS and
  Leduc (*UAI*).
- **[Greige 2022]** L. Greige, F. De Mesentier Silva, M. Trotter, C. Lawrence, P. Chin, D. Varadarajan, "Collusion detection in team-based multiplayer games," arXiv:2203.05121.
  - *What it does.* It combines social-graph features with Isolation Forest on more than
    170,000 players.
  - [verified: arXiv]
- **[Xu 2025]** Y. E. Xu, Z. Feng, F. Fang, "Deviate or not: Learning coalition structures with multiple-bit observations in games," *AAAI* 39(13), 14184–14192, 2025, doi:10.1609/aaai.v39i13.33553.
  - *What it does.* It learns a hidden coalition structure by presenting agents with designed
    games.
  - [verified: arXiv + Crossref]
- None of these links detection to what the agent does next.

### Verdict: **open at the core, narrowed around it. Two sub-claims must be corrected.**

**Still open.** No counter-example was found in the September 2026 search for an
opponent-exploitation method in **N-player imperfect-information games** that meets all three
of these conditions:

- it has a stated safety criterion, such as bounded loss relative to a baseline;
- that criterion is checked empirically;
- it is tested against heterogeneous and colluding opponents.

Every *safe* exploitation paper found (2022–2026) is two-player zero-sum. Every N-player
*exploitation* paper found has no safety notion.

**Narrowed.** Four earlier claims no longer hold:

- **Safety notions.** N-player safety notions *do* exist: equal share, with sharp
  impossibility results [Ge 2025]; team-maxmin values against coalitions [Celli & Gatti 2018;
  Zhang 2021]; and baseline-relative regret [Müller 2025].
- **Coalition dynamics.** They are *not* unstudied [Babyak 2024; the adversarial team games
  literature].
- **KL anchoring.** KL-anchored play *has* been deployed in a seven-player game [Bakhtin 2023],
  but as human-compatibility regularisation, not as exploitation safety.
- **The "tradeoff never studied" line.** The May report's "no existing work systematically
  studies the exploitation–safety tradeoff in multiplayer settings" is borderline. Ganzfried
  et al. [2024] study exploitation in three-player Kuhn, and Ge et al. [2025] study what a
  multiplayer learner can guarantee. Reword it as "no work combines both".

**Correction 1 — equal share.** The May report calls equal share "each player's guaranteed
minimum payoff". That is wrong. Equal share is the fair-share *target* C/n, and it is
*provably not securable* when opponents play different strategies [Ge 2025, Prop. 4.1]. A
table with heterogeneous players, let alone a colluding pair, is exactly that case. So C2
cannot promise to "exploit while guaranteeing at least equal share" in general. It can claim
this only under Ge et al.'s conditions (identical, slowly adapting opponents), or it can use
equal share as an *empirical* reference line.

**Correction 2 — piKL.** Step 15 says piKL keeps the policy "within a KL-divergence ball of
the Nash policy". In the sources the anchor is a **human imitation policy**, and the
regularisation provides no worst-case guarantee [Jacob 2022; Bakhtin 2023]. KL-anchoring an
exploiting policy to a blueprint is the *thesis's own proposal*. Its two-player relatives are
restricted Nash response (a mixture), magnetic mirror descent, and StratFormer's schedule.
Present it that way, not as an established technique.

### How Chapter I should phrase the gap

> Safe opponent exploitation has a mature two-player zero-sum theory. It runs from the
> original safety theorem and restricted Nash responses to adaptation safety [Ge 2024] and,
> most recently, certified per-deployment guarantees [Li & Huang 2026]. Every one of these
> results relies on the two-player minimax value. With three or more players the notions
> that exist are either very conservative (team-maxmin values against a coordinated
> coalition [Celli & Gatti 2018; Zhang 2021]) or provably unattainable against heterogeneous
> opponents (equal share [Ge 2025]). Opponent exploitation in multiplayer poker has been
> demonstrated [Ganzfried 2024], but without any loss bound. KL-regularised play in
> seven-player Diplomacy [Bakhtin 2023] anchors to human behaviour for compatibility, not for
> safety. No counter-example was found to the following statement: no method exploits
> sub-optimal opponents in N-player imperfect-information games while bounding its loss
> relative to a baseline, and none tests that bound against colluding opponents. C2 targets
> this gap empirically, in small games. It uses baseline-relative criteria in the spirit of
> [Müller 2025] and equal share [Ge 2025] as reference lines, not as guarantees.

---

## C3 — Evaluation Methodology (adaptability and robustness, cross-game)

### Claimed gap

- The skeleton, §1.6, says there is "no cross-game framework for adaptability/robustness", to
  be framed as "existing evaluation breaks here, ours catches it".
- The step-15 map lists four gaps. "No framework combines exploitability + ranking +
  confidence". "No cross-game validation". "N-player eval needs coalition-aware metrics".
  "Scaling: O(n²) full payoff matrix".
- The May report says "existing metrics each capture only a single dimension".

### Closest recent work

Full references are in `lit_evaluation.md`.

- **[Lanctot 2023b] Repeated RPS benchmark** (*TMLR*).
  - *What it does.* It has 43 bots, some deliberately weak, and fixed 1000-throw matches. It
    reports population return and within-population exploitability, combined into one
    aggregate score. RL, online-learning and LLM agents are all evaluated.
  - *What it does not do.* It covers one simultaneous-move two-player game, with no hidden
    private information beyond the opponent's strategy. It is the **nearest existing
    instance** of joint adaptability-and-robustness evaluation.
- **[Leibo 2021; Agapiou 2022; Trivedi 2024; Smith 2025] Melting Pot family and Concordia.**
  - *What they do.* They measure cross-substrate, N-player generalisation to held-out
    co-players and are cross-game by design.
  - *What they do not do.* They report focal per-capita return only: no exploitability, no
    safety, no competitive imperfect-information card games.
- **Ratings of fixed agents across tasks, including N-player and general-sum ones:**
  [Lanctot 2023a] (VasE), [Lanctot 2025] (SCO), [Lanctot 2026] (active evaluation),
  [Marris 2022], [Marris 2025], [Liu 2025].
  - *What they do not do.* They do not model adaptation within a match.
- **[Timbers 2022] Approximate exploitability.** It works across games, but only in the worst
  case and for two-player games.
- **Confidence under variance:** [Burch 2018], [Li 2026] (anytime-valid AIVAT), [Kim & Sandholm
  2026] (AIVAT pathologies), [Rowland 2019].
- **Opponent-modelling papers' own protocols:** [Fu 2022] (seen, unseen, mixed and adaptive
  opponent sequences), [Jing 2024b], [Ma 2024] (three games), [Caen 2026] (NashConv plus
  gain). Useful templates, but mutually incomparable.
- **[Hu 2025]** S. Hu, M. A. Hady, J. Qiao, J. Cao, M. Pratama, R. Kowalczyk, "Toward adaptable multi-agent reinforcement learning: An assumption-aware review," arXiv:2507.10142, v2 July 2026.
  - *What it does.* It proposes an *adaptability* taxonomy (learning, policy and
    scenario-driven adaptability).
  - *What it does not do.* It is conceptual, with no competitive-game metric.
  - [verified: arXiv]
- **LLM arenas:** [Wang 2026] (Mindgames: "leaderboard validity differs sharply across
  environments"), [Huang 2025], [Duan 2024], [Kelly 2026], [Provost 2026].
  - *What they do not do.* They rank fixed agents and do not measure adaptation.

### Verdict: **narrowed**

**Weak as stated.**

- **"No framework combines exploitability + ranking + confidence."** RRPS already combines an
  exploitation return with exploitability in one score, and the rating papers report
  confidence. Assembling known tools will not be accepted as novel.
- **"No cross-game validation."** False for generalisation and rating: Melting Pot, VasE,
  SCO and approximate exploitability all work across games.
- **"O(n²) scaling."** Partly addressed by adaptive sampling [Rowland 2019] and active
  evaluation [Lanctot 2026]. Drop it as a gap.

**Still open (no counter-example found).** A protocol that measures, together:

- **adaptability:** gain against a sub-optimal population, and the speed of adaptation and of
  recovery after an opponent switches strategy;
- **robustness:** worst-case exploitability, or a coalition-aware substitute in N-player games;
- **confidence:** bounds on both, from variance reduction.

It must also be applied unchanged across several imperfect-information games, including
N-player ones. Coalition-aware robustness metrics for *agent evaluation* were not found at all.
The strongest framing is the one the skeleton already chose: list the concrete failure modes
of existing evaluation for adaptive, exploiting and N-player agents (the nine points in
`lit_evaluation.md`) and show that the proposed protocol detects them.

### How Chapter I should phrase the gap

> Evaluation methodology for game-playing agents is well developed along separate axes. These
> are: worst-case exploitability and its approximations [Johanson 2011; Lisý & Bowling 2017;
> Timbers 2022]; variance-reduced head-to-head estimation [Burch 2018]; population ratings
> that handle intransitivity and redundancy [Balduzzi 2018; Omidshafiei 2019; Lanctot 2023a;
> Marris 2025]; and generalisation to held-out co-players [Leibo 2021]. Only one benchmark
> scores adaptation to a population and robustness together, and it is limited to repeated
> rock–paper–scissors [Lanctot 2023b]. For adaptive agents the axes pull against each other:
> exploitability can only penalise adaptation, population ratings over-credit or ignore
> exploitation of weak opponents, and none of these measures is defined for coalitions in
> games with more than two players. C3 proposes a protocol that reports exploitation gain,
> adaptation speed and a worst-case (or coalition-aware) robustness measure with confidence
> bounds, applied unchanged across several imperfect-information games including N-player ones.

---

## Newly found works Chapter I should cite

These are the works not in the step 01–12 corpus, in priority order. The full evaluation-side
list is in `lit_evaluation.md`.

**Must cite (they change or frame a gap claim)**

1. [Ge 2025] Equal share (*ICML 2025*): the N-player safety notion and its impossibility
   results (§1.5, C2).
2. [Fu 2022] GSCU (*ICML 2022*): detect, adapt and fall back, against non-stationary opponents,
   in Kuhn poker (§1.4, C1).
3. [Caen 2026] StratFormer and [Murgoci 2026] AlphaExploitem: the current state of
   model-and-exploit agents in small poker games (§1.4).
4. [Ganzfried 2024] Opponent modelling in three-player Kuhn poker (*DAI '24*): the N-player
   baseline for C1 and C2 (§1.4–1.5).
5. [Lanctot 2023b] RRPS population benchmark (*TMLR*): the nearest C3 precedent (§1.6).
6. [Jacob 2022] piKL (*ICML 2022*) and [Bakhtin 2023] DiL-piKL (*ICLR 2023*): the correct
   sources for "piKL" (§1.5).
7. [Müller 2025] Best of both worlds (*ICML 2025*): baseline-relative safety (§1.5).
8. [Li & Huang 2026] CS-RNR: the current state of two-player safe exploitation (§1.5).

**Should cite**

- **§1.4:** [Jing 2024b] OMIS and [Jing 2024a] TAO; [Ma 2024] PACE; [Milec 2025] ABD (it is
  already in the corpus, but now with its AAMAS 2025 venue); [Cross 2025] Hypothetical Minds;
  [Nashed & Zilberstein 2022] survey.
- **§1.5:** [Celli & Gatti 2018] / [Zhang 2021] team-maxmin; [Babyak 2024] coalitions;
  [Szafron 2013] three-player Kuhn utility transfer; [Bonjour 2022] and [Xu 2025] collusion and
  coalition detection.
- **§1.6:** the evaluation sources for the failure modes: [Czarnecki 2020], [Davis 2014],
  [Wang 2023], [Kim & Sandholm 2026], [Marris 2025], [Liu 2025].

**Optional, for LLM context in §1.1 or §1.4:** [Guo 2023], [Zhang 2024], [Lin 2026], [Wang 2026].

### Could not verify

- **GOE-LLM**, "Generalizable opponent exploitation in LLM agents …". It is an anonymous
  OpenReview submission, probably to ICLR 2026, and the page was behind a bot check.
  [unverified: authors, venue and acceptance unknown.] Do not cite.
- **VasE [Lanctot 2023a] and deviation ratings [Marris 2025].** Neither has a venue listed.
  Cite them as arXiv.
- **GSCU's environments** (Kuhn poker and Predator-Prey) were confirmed through a search
  summary and the project repository, not the PDF body.
- **Kaggle Game Arena poker protocol.** See `lit_evaluation.md`.

### Citation corrections for the existing corpus and plans

These were found while checking. I edited none of these files.

- **`deliverables/reports/ruseMay/report.md` ref. [7].** It merges two papers. It gives the
  title and authors of the *ICLR 2023* DiL-piKL paper [Bakhtin 2023], but under a slightly
  altered title ("Human-Level Play in the Game of No-Press Diplomacy via…"), together with the
  *Science* 378(6624):1067–1074 details, which belong to CICERO [FAIR 2022]. Split it into the
  two correct entries. Add [Jacob 2022] as the origin of piKL.
- **`deliverables/reports/step08/summary/summaryEn.md` footnotes.**
  - Jeary & Turrini's first author is **Linus** Jeary ("Jeary, L.", not "Jeary, J.").
  - Liu et al. 2022 is **Mingyang** Liu ("Liu, M.", not "Liu, W."). Its authors are M. Liu,
    C. Wu, Q. Liu, Y. Jing, J. Yang, P. Tang, C. Zhang, *NeurIPS* 2022.
  - Milec et al. 2025 appeared at **AAMAS 2025** as an extended abstract, pp. 2675–2677.
- **`planning/rawSteps/step_15…`.**
  - OX-Search is by **Ge, Xu, Ding, Meng, An, Li & Gao**, not "Ge, Kovařík & Lisý". Kovařík
    and Lisý are Milec's co-authors on ABD. The arXiv link placeholder "2405.XXXXX / 2405.15999"
    was not confirmed; cite PMLR v235 instead.
  - The Diplomacy paper labelled "Human-Level Performance in No-Press Diplomacy (Bakhtin et al.,
    2022)" is actually Gray, Lerer, Bakhtin & Brown, *ICLR 2021* ("Human-level performance in
    no-press Diplomacy via equilibrium search", arXiv:2010.02923). The piKL sources are
    [Jacob 2022] and [Bakhtin 2023]. [verified: ICLR 2021 virtual-site listing + arXiv]
- **Equal share.** Wherever a file says the equal-share bound is guaranteed (the May report;
  step-15's "guarantees at least equal share"), qualify it with Ge et al.'s conditions
  (Props. 4.1–4.2).
