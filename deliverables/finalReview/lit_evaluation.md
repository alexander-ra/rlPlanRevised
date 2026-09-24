# Evaluation of multi-agent game AI — literature extract (§1.6)

*Compiled 2026-09-24 for §1.6, the one section of Chapter I that has no study chapter behind it
(steps 14–15 were never executed). Every source below was checked online; the Key sources list
records how. Citation keys are author–year, so they can be renumbered into the chapter's
single `[n]` sequence at drafting time. Items dated 2026 are arXiv preprints unless a venue is
given. They are recent enough to cite as "recent work", but not as settled results.*

## Digest

**Two questions, two families of metrics.** Evaluating a game-playing agent means answering
one of two questions: *how badly can it be beaten in the worst case*, or *how well does it do
against the opponents it will actually meet*. In two-player zero-sum games the first question
is answered by exploitability, the gain a best-responding opponent obtains over the game
value. Exploitability can be computed exactly in small games. Accelerated best-response
traversal made it computable for heads-up limit hold'em [Johanson 2011], and refining an
abstraction does not even guarantee lower exploitability [Waugh 2009]. Larger games admit only
lower bounds. Local best response (LBR) is a cheap, poker-specific probe [Lisý & Bowling 2017];
ISMCTS-BR is a learned approximate best response that works across games [Timbers 2022].
With N players the usual generalisation, NashConv, sums each player's incentive to deviate
[Lanctot 2019]. It measures distance from an equilibrium, not what any player is guaranteed.

The two families disagree. Two competition bots were statistically indistinguishable
head-to-head yet about 1300 mbb/g apart in LBR exploitability [Moravčík 2017]. Conversely, a
less exploitable strategy can do worse one-on-one against a range of opponents [Davis 2014].
The Annual Computer Poker Competition used two winner rules for this reason. Total bankroll
rewards exploiting the field; bankroll instant-runoff rewards not losing and favours
equilibrium-based agents [Bard 2013].

**Head-to-head estimation and variance.** In poker the luck of the deal dominates small
samples. Two remedies make matches of feasible length significant. The first is duplicate
play, which replays the same cards with seats swapped [Bard 2013]. The second is a family of
unbiased low-variance estimators: DIVAT [Billings & Kan 2006], the optimal unbiased estimators
of [Zinkevich 2006], and AIVAT, which builds control variates for chance events and for the
actions of agents with known strategies [Burch 2018]. DeepStack reported an 85% reduction in
standard deviation with AIVAT [Moravčík 2017]. Pluribus won 48 ± 25 mbb/game over 10,000
six-player hands. AIVAT cannot be applied to human players, and no individual human's result
reached significance [Brown 2019]. Recent work warns that AIVAT's heuristic value function must
be fixed before the evaluation data are seen. Tuning it afterwards can push the variance, or
the test statistic, almost anywhere [Kim & Sandholm 2026]. Other recent work adds
anytime-valid stopping rules [Li 2026]. [Rowland 2019] gives sample-complexity bounds and
adaptive match allocation for ranking under noisy payoffs.

**Population ranking.** Elo [Elo 1978] and TrueSkill [Herbrich 2006] assume a latent transitive
skill. Elo has no predictive power in cyclic games, and adding copies of an agent that a player
beats inflates that player's rating [Balduzzi 2018]. Elo even fails on some purely transitive
games [Bertrand 2023]. Nash averaging scores agents against the maximum-entropy Nash
equilibrium of the meta-game, which makes the ranking invariant to redundant agents and tasks
[Balduzzi 2018]. α-Rank ranks agents by the stationary distribution of an evolutionary Markov
chain. It covers many-player and asymmetric games and depends on a selection-pressure
parameter [Omidshafiei 2019]. Voting-as-Evaluation (VasE) treats tasks as voters and
recommends maximal lotteries [Lanctot 2023a]. Soft Condorcet Optimization [Lanctot 2025] and
active task selection [Lanctot 2026] followed. For N-player general-sum data there are
equilibrium-based ratings [Marris 2022], clone-invariant "deviation ratings" built on coarse
correlated equilibria [Marris 2025], and an equilibrium rating of LLMs cast as a three-player
game [Liu 2025].

**Empirical game-theoretic analysis (EGTA).** EGTA estimates a normal-form meta-game from
simulated matches between a finite set of strategies, then analyses it with equilibrium and
dynamics tools [Wellman 2006; Tuyls 2020; Wellman 2025]. Work on the geometry of such games
adds three findings. Zero-sum functional-form games decompose into transitive and cyclic
components [Balduzzi 2019]. Real-world games look like "spinning tops": strongly cyclic at
intermediate strength and more transitive near the top [Czarnecki 2020]. Response-graph
measures place many games in one "landscape" [Omidshafiei 2020].

**Generalisation to novel co-players.** Melting Pot evaluates a focal population against
held-out background populations in more than 80 scenarios. It reports focal per-capita return
in "resident" and "visitor" modes [Leibo 2021; Agapiou 2022; Trivedi 2024]. Concordia extends
the idea to LLM agents [Smith 2025]. The repeated Rock–Paper–Scissors benchmark is the closest
competitive analogue [Lanctot 2023b]. It uses 43 bots, some deliberately weak, and two metrics:
average return against the population, which measures exploitation, and within-population
exploitability, which measures robustness. Adversarial-policy studies show that agents rated
superhuman can still be beaten systematically by trained exploiters
[Wang 2023; Haluska & Schmid 2024].

**LLM game arenas (2024–2026).** The main arenas are GTBench [Duan 2024], the N-player
GAMA-Bench [Huang 2025], SPIN-Bench [Yao 2025], TextArena with TrueSkill [Guertler 2025],
Mindgames [Wang 2026], Game Reasoning Arena on OpenSpiel [Cipolina-Kun 2025], Kaggle Game Arena
(chess, heads-up no-limit poker, Werewolf) [Kelly 2026] and PokerBench [Zhuang 2025].
Mindgames is the largest, with 944 agents, and found that leaderboard validity varies sharply
from game to game. The GTO Wizard Benchmark scores poker agents against a single near-equilibrium
opponent with AIVAT [Provost 2026]. All of these rank fixed agents by win rate or rating. None
reports exploitability or how quickly an agent adapts.

## Where existing evaluation breaks

These are concrete failure modes when the agent under test is *adaptive* (it changes play in
response to opponents), *exploiting* (it deliberately departs from equilibrium), or plays in an
*N-player* game. Together they are the C3 gap. Items marked *(analysis)* are inferences drawn
from the cited definitions, not claims a source makes itself.

1. **Exploitability can only punish adaptation.** Any departure from equilibrium raises
   exploitability. An agent that exploits weak opponents safely therefore scores strictly worse
   than the equilibrium it started from, however much it gains. The exploitation–safety
   trade-off has two dimensions (the restricted-Nash frontier [Johanson 2007]), and neither
   scalar captures it. Worst-case and head-to-head numbers disagree in both directions
   [Moravčík 2017; Davis 2014]. The ACPC needed two winner rules for this reason [Bard 2013].
   Only one published protocol reports both axes on one population and combines them
   (aggregate score = population return − within-population exploitability) [Lanctot 2023b],
   and it covers a single two-player game.
2. **Exploitability does not carry over to N players.** NashConv measures distance from *an*
   equilibrium [Lanctot 2019], but with three or more players equilibrium play guarantees
   nothing. Pluribus's authors state the question of what the goal should even be is open, and
   they evaluate empirically instead [Brown 2019]. In three-player Kuhn poker, one player can
   transfer utility to a second at the third's expense while every player still plays an
   equilibrium profile [Szafron 2013]. Even the weaker "equal share" objective is provably
   unattainable against opponents that play different fixed strategies [Ge 2025]. The only
   worst-case notion that covers coalitions is the team-maxmin value against a coordinated
   coalition [Celli & Gatti 2018; Zhang 2021; Zhang 2023]. It is a solution concept, not an
   evaluation protocol, and it is very conservative *(analysis)*.
3. **Approximate best responses give lower bounds only.** When LBR or a learned best response
   finds no exploit, that does not show the agent is safe [Lisý & Bowling 2017; Timbers 2022].
   The adversarial-policy results show real leaks that head-to-head and population ratings had
   missed [Wang 2023; Haluska & Schmid 2024]. A C3 framework must report the exploiter's
   budget and strength, not just the number it produced.
4. **Population rankings reward or ignore exploitation for the wrong reasons.** Elo is inflated
   by adding copies of beaten agents [Balduzzi 2018], so an exploiter of a zoo full of weak bots
   is over-credited. Nash averaging does the opposite by design: agents outside the
   max-entropy Nash support get zero weight, so gains against weak opponents count for nothing
   *(analysis of [Balduzzi 2018])*. α-Rank rankings can change with the selection-pressure
   parameter [Omidshafiei 2019]. All of these methods treat each agent as a fixed strategy in a
   meta-game. An adaptive agent's payoff depends on match length and history, so its meta-game
   entry is only defined once the horizon and the opponent schedule are fixed *(analysis)*.
   Existing protocols fix them by convention; the RRPS benchmark, for instance, fixes every
   match at 1000 throws [Lanctot 2023b].
5. **Variance compounds with adaptation.** Final win rate already needs thousands of hands with
   variance reduction [Moravčík 2017; Brown 2019]. Measuring *adaptation* needs per-segment
   estimates along a match, which needs still more data *(analysis)*. Humans cannot be
   variance-reduced by AIVAT [Brown 2019]. AIVAT itself can be manipulated if its heuristic is
   chosen after the data [Kim & Sandholm 2026]. Ranking confidence depends on payoff gaps
   [Rowland 2019].
6. **Generalisation suites do not measure competitive robustness.** Melting Pot measures focal
   per-capita return in mixed-motive substrates. Its authors did not train prosocial variants
   on zero-sum substrates, because there per-capita return is zero by definition [Leibo 2021].
   It has no exploitability and no safety measure. Opponent-modelling papers each use a bespoke
   protocol, so their results cannot be compared: seen / unseen / mixed / adaptive opponent
   sequences [Fu 2022], seen:unseen ratios [Jing 2024b], three unrelated games [Ma 2024],
   NashConv plus gain on Leduc [Caen 2026].
7. **Non-stationary and deceptive opponents are mostly untested.** Evaluation against fixed bots
   cannot reveal the "being taught and then exploited" failure that motivates adaptation safety
   [Ge 2024]. Recent exploiting agents list non-stationary opponents as future work
   [Caen 2026].
8. **Collusion is evaluated separately from play.** Collusion detection is scored as a detection
   task, using collusion tables [Mazrooei 2013] or mutual information between agents' actions
   [Bonjour 2022]. No agent-evaluation metric asks how an agent fares when some opponents
   coordinate *(analysis; no counter-example found)*.
9. **LLM arenas inherit all of the above.** They report TrueSkill, Elo or big blinds per 100
   hands against a changing field [Guertler 2025; Kelly 2026]. Leaderboard validity differs by
   environment [Wang 2026]. The one poker benchmark with variance reduction measures play
   against an equilibrium opponent only, not exploitation [Provost 2026].

**What this implies for C3.** Existing tools cover the pieces separately: worst-case
exploitability (two-player), variance-reduced head-to-head results, population ratings of fixed
agents, and generalisation to held-out co-players. No protocol found reports all of the
following together, across several imperfect-information games including N-player ones:
(a) gain against a sub-optimal population, (b) worst-case loss or its N-player substitute,
(c) speed of adaptation and recovery after an opponent switch, and (d) coalition-aware
robustness, each with confidence bounds.

## Key sources

- [Johanson 2011] M. Johanson, K. Waugh, M. Bowling, M. Zinkevich, "Accelerating best response calculation in large extensive games," in *Proc. IJCAI*, 2011, pp. 258–265. — [verified: IJCAI 2011 proceedings PDF, paper 054; abstract checked]
- [Waugh 2009] K. Waugh, D. Schnizlein, M. Bowling, D. Szafron, "Abstraction pathologies in extensive games," in *Proc. AAMAS*, 2009, pp. 781–788. — [verified: Bowling publication page and PDF]
- [Lisý & Bowling 2017] V. Lisý, M. Bowling, "Equilibrium approximation quality of current no-limit poker bots," AAAI-17 Workshop on Computer Poker and Imperfect Information Games, arXiv:1612.07547, 2017. — [verified: arXiv abstract + U. Alberta PDF]
- [Timbers 2022] F. Timbers, N. Bard, E. Lockhart, M. Lanctot, M. Schmid, N. Burch, J. Schrittwieser, T. Hubert, M. Bowling, "Approximate exploitability: Learning a best response," in *Proc. IJCAI*, 2022, paper 484; arXiv:2004.09677. — [verified: IJCAI proceedings page + arXiv metadata]
- [Lanctot 2019] M. Lanctot et al., "OpenSpiel: A framework for reinforcement learning in games," arXiv:1908.09453, 2019. — [verified: PDF text; NashConv = Σᵢ δᵢ(π), exploitability = NashConv/n]
- [Moravčík 2017] M. Moravčík et al., "DeepStack: Expert-level artificial intelligence in heads-up no-limit poker," *Science*, 356(6337), 508–513, 2017, doi:10.1126/science.aam6960; arXiv:1701.01724. — [verified: arXiv PDF text: AIVAT 85% SD reduction; Act1 vs Slumbot ≈1300 mbb/g LBR gap]
- [Davis 2014] T. Davis, N. Burch, M. Bowling, "Using response functions to measure strategy strength," in *Proc. AAAI*, 28(1), 2014, doi:10.1609/aaai.v28i1.8830. — [verified: AAAI OJS + Crossref]
- [Bard 2013] N. Bard, J. Hawkin, J. Rubin, M. Zinkevich, "The Annual Computer Poker Competition," *AI Magazine*, 34(2), 112–114, 2013, doi:10.1609/aimag.v34i2.2474. — [verified: read full article PDF (total bankroll vs instant-runoff; duplicate poker)]
- [Billings & Kan 2006] D. Billings, M. Kan, "A tool for the direct assessment of poker decisions," *ICGA Journal*, 29(3), 119–142, 2006, doi:10.3233/ICG-2006-29302. — [verified: SAGE/IOS listing + Crossref]
- [Zinkevich 2006] M. Zinkevich, M. Bowling, N. Bard, M. Kan, D. Billings, "Optimal unbiased estimators for evaluating agent performance," in *Proc. AAAI*, 2006, pp. 573–578. — [verified: AAAI library + Bowling page]
- [Burch 2018] N. Burch, M. Schmid, M. Moravčík, D. Morrill, M. Bowling, "AIVAT: A new variance reduction technique for agent evaluation in imperfect information games," in *Proc. AAAI*, 32(1), 2018, doi:10.1609/aaai.v32i1.11481; arXiv:1612.06915. — [verified: AAAI OJS + Crossref]
- [Brown 2019] N. Brown, T. Sandholm, "Superhuman AI for multiplayer poker," *Science*, 365(6456), 885–890, 2019, doi:10.1126/science.aay2400. — [verified: full-text PDF: 48±25 mbb/g, 10,000 hands, AIVAT not applicable to humans, "Pluribus plays a fixed strategy"]
- [Kim & Sandholm 2026] J. Kim, T. Sandholm, "Heuristic pathologies and further variance reduction via uncertainty propagation in the AIVAT family of techniques," arXiv:2605.14261, 2026. — [verified: arXiv abstract]
- [Li 2026] B. Li, Y. Chen, L. Huang, "AV-AIVAT: 74× cheaper agent evaluation with certified anytime-valid stopping in imperfect-information games," arXiv:2608.06362, 2026. — [verified: arXiv HTML abstract; 74× = median raw-vs-AIVAT hands to stop at ±1 BB, 95%]
- [Rowland 2019] M. Rowland, S. Omidshafiei, K. Tuyls, J. Pérolat, M. Valko, G. Piliouras, R. Munos, "Multiagent evaluation under incomplete information," in *Proc. NeurIPS*, 2019; arXiv:1909.09849. — [verified: NeurIPS proceedings + arXiv]
- [Elo 1978] A. E. Elo, *The Rating of Chessplayers, Past and Present*. New York: Arco, 1978. — [verified: Open Library / Internet Archive record]
- [Herbrich 2006] R. Herbrich, T. Minka, T. Graepel, "TrueSkill™: A Bayesian skill rating system," in *Proc. NIPS*, 2006, pp. 569–576. — [verified: NeurIPS proceedings + DBLP]
- [Balduzzi 2018] D. Balduzzi, K. Tuyls, J. Pérolat, T. Graepel, "Re-evaluating evaluation," in *Proc. NeurIPS*, 2018; arXiv:1806.02643. — [verified: arXiv PDF text (Elo "meaningless in cyclic games", inflation by copies; Nash averaging; Hodge/Schur decomposition, mElo)]
- [Bertrand 2023] Q. Bertrand, W. M. Czarnecki, G. Gidel, "On the limitations of the Elo, real-world games are transitive, not additive," in *Proc. AISTATS*, PMLR 206, 2023, pp. 2905–2921; arXiv:2206.12301. — [verified: PMLR page + arXiv metadata]
- [Omidshafiei 2019] S. Omidshafiei, C. Papadimitriou, G. Piliouras, K. Tuyls, M. Rowland, J.-B. Lespiau, W. M. Czarnecki, M. Lanctot, J. Pérolat, R. Munos, "α-Rank: Multi-agent evaluation by evolution," *Scientific Reports*, 9, 9937, 2019, doi:10.1038/s41598-019-45619-9. — [verified: Nature + PubMed]
- [Lanctot 2023a] M. Lanctot, K. Larson, Y. Bachrach, L. Marris, Z. Li, A. Bhoopchand, T. Anthony, B. Tanner, A. Koop, "Evaluating agents using social choice theory," arXiv:2312.03121, v4 2025. — [verified: arXiv (no journal-ref); venue unknown, cite as arXiv]
- [Lanctot 2025] M. Lanctot, K. Larson, M. Kaisers, Q. Berthet, I. Gemp, M. Diaz, R.-R. Maura-Rivero, Y. Bachrach, A. Koop, D. Precup, "Soft Condorcet optimization for ranking of general agents," in *Proc. AAMAS*, 2025; arXiv:2411.00119. — [verified: arXiv comments + ACM DL]
- [Lanctot 2026] M. Lanctot, K. Larson, I. Gemp, M. Kaisers, "Active evaluation of general agents: Problem definition and comparison of baseline algorithms," in *Proc. AAMAS*, 2026; arXiv:2601.07651. — [verified: arXiv comments]
- [Marris 2022] L. Marris, M. Lanctot, I. Gemp, S. Omidshafiei, S. McAleer, J. Connor, K. Tuyls, T. Graepel, "Game theoretic rating in N-player general-sum games with equilibria," arXiv:2210.02205, 2022. — [verified: arXiv]
- [Marris 2025] L. Marris, S. Liu, I. Gemp, G. Piliouras, M. Lanctot, "Deviation ratings: A general, clone-invariant rating method," arXiv:2502.11645, 2025. — [verified: arXiv; no venue listed]
- [Liu 2025] S. Liu, I. Gemp, L. Marris, G. Piliouras, N. Heess, M. Lanctot, "Re-evaluating open-ended evaluation of large language models," in *Proc. ICLR*, 2025; arXiv:2502.20170. — [verified: arXiv comments "Published at ICLR 2025"]
- [Wellman 2006] M. P. Wellman, "Methods for empirical game-theoretic analysis," in *Proc. AAAI*, 2006, pp. 1552–1556. — [verified: AAAI PDF + ACM DL]
- [Tuyls 2020] K. Tuyls, J. Pérolat, M. Lanctot, E. Hughes, R. Everett, J. Z. Leibo, C. Szepesvári, T. Graepel, "Bounds and dynamics for empirical game theoretic analysis," *Autonomous Agents and Multi-Agent Systems*, 34(1), art. 7, 2020, doi:10.1007/s10458-019-09432-y. — [verified: Crossref]
- [Wellman 2025] M. P. Wellman, K. Tuyls, A. Greenwald, "Empirical game theoretic analysis: A survey," *JAIR*, 82, 1017–1076, 2025, doi:10.1613/jair.1.16146; arXiv:2403.04018. — [verified: JAIR + Crossref]
- [Balduzzi 2019] D. Balduzzi, M. Garnelo, Y. Bachrach, W. M. Czarnecki, J. Pérolat, M. Jaderberg, T. Graepel, "Open-ended learning in symmetric zero-sum games," in *Proc. ICML*, PMLR 97, 2019, pp. 434–443; arXiv:1901.08106. — [verified: PDF text (Theorem 1: transitive + cyclic decomposition of FFGs; "gamescapes")]
- [Czarnecki 2020] W. M. Czarnecki, G. Gidel, B. Tracey, K. Tuyls, S. Omidshafiei, D. Balduzzi, M. Jaderberg, "Real world games look like spinning tops," in *Proc. NeurIPS*, 2020; arXiv:2004.09468. — [verified: NeurIPS proceedings + arXiv]
- [Omidshafiei 2020] S. Omidshafiei, K. Tuyls, W. M. Czarnecki, F. C. Santos, M. Rowland, J. Connor, D. Hennes, P. Muller, J. Pérolat, B. De Vylder, A. Gruslys, R. Munos, "Navigating the landscape of multiplayer games," *Nature Communications*, 11, 5603, 2020, doi:10.1038/s41467-020-19244-4. — [verified: Nature + Crossref]
- [Leibo 2021] J. Z. Leibo, E. Duéñez-Guzmán, A. S. Vezhnevets, J. P. Agapiou, P. Sunehag, R. Koster, J. Matyas, C. Beattie, I. Mordatch, T. Graepel, "Scalable evaluation of multi-agent reinforcement learning with Melting Pot," in *Proc. ICML*, PMLR 139, 2021, pp. 6187–6199; arXiv:2107.06857. — [verified: PMLR PDF text (focal/background, resident/visitor, per-capita return, zero-sum note)]
- [Agapiou 2022] J. P. Agapiou et al. (17 authors), "Melting Pot 2.0," arXiv:2211.13746, 2022. — [verified: arXiv metadata]
- [Trivedi 2024] R. S. Trivedi et al., "Melting Pot contest: Charting the future of generalized cooperative intelligence," in *NeurIPS Datasets & Benchmarks*, 2024. — [verified: NeurIPS proceedings abstract page]
- [Smith 2025] C. Smith et al., "Evaluating generalization capabilities of LLM-based agents in mixed-motive scenarios using Concordia," in *NeurIPS Datasets & Benchmarks*, 2025; arXiv:2512.03318. — [verified: arXiv comments]
- [Lanctot 2023b] M. Lanctot, J. Schultz, N. Burch, M. O. Smith, D. Hennes, T. Anthony, J. Pérolat, "Population-based evaluation in repeated rock-paper-scissors as a benchmark for multiagent reinforcement learning," *TMLR*, 2023; arXiv:2303.03196. — [verified: arXiv journal-ref + PDF text (K = 1000; aggregate score; within-population exploitability ≈ 75% of an externally learned exploiter's)]
- [Wang 2023] T. T. Wang, A. Gleave, T. Tseng, K. Pelrine, N. Belrose, J. Miller, M. D. Dennis, Y. Duan, V. Pogrebniak, S. Levine, S. Russell, "Adversarial policies beat superhuman Go AIs," in *Proc. ICML*, PMLR 202, 2023, pp. 35655–35739; arXiv:2211.00241. — [verified: PMLR]
- [Haluska & Schmid 2024] R. Haluska, M. Schmid, "Learning to beat ByteRL: Exploitability of collectible card game agents," arXiv:2404.16689, 2024. — [verified: arXiv]
- [Duan 2024] J. Duan, R. Zhang, J. Diffenderfer, B. Kailkhura, L. Sun, E. Stengel-Eskin, M. Bansal, T. Chen, K. Xu, "GTBench: Uncovering the strategic reasoning limitations of LLMs via game-theoretic evaluations," in *Proc. NeurIPS*, 2024; arXiv:2402.12348. — [verified: NeurIPS proceedings + arXiv]
- [Huang 2025] J. Huang, E. J. Li, M. H. Lam, T. Liang, W. Wang, Y. Yuan, W. Jiao, X. Wang, Z. Tu, M. R. Lyu, "How far are we on the decision-making of LLMs? Evaluating LLMs' gaming ability in multi-agent environments" (GAMA-Bench), in *Proc. ICLR*, 2025; arXiv:2403.11807. — [verified: ICLR proceedings (listed as "Competing large language models in multi-agent gaming environments") + arXiv metadata]
- [Yao 2025] J. Yao, K. Wang, R. Hsieh, H. Zhou, T. Zou, Z. Cheng, Z. Wang, P. Viswanath, "SPIN-Bench: How well do LLMs plan strategically and reason socially?," in *Proc. COLM*, 2025; arXiv:2503.12349. — [verified: arXiv metadata + COLM header]
- [Guertler 2025] L. Guertler, B. Cheng, S. Yu, B. Liu, L. Choshen, C. Tan, "TextArena," arXiv:2504.11442, 2025. — [verified: arXiv abstract (TrueSkill)]
- [Wang 2026] K. Wang, A. Thöni, B. Kempinski, B. Cheng, J. Yao, B. Finch, L. Guertler, V. Nadkarni, et al., "MINDGAMES: A live arena for evaluating social and strategic reasoning in multi-agent LLMs," arXiv:2605.29512, 2026. — [verified: arXiv abstract]
- [Cipolina-Kun 2025] L. Cipolina-Kun, M. Nezhurina, J. Jitsev, "Game Reasoning Arena: A framework and benchmark for assessing reasoning capabilities of large language models via game play," arXiv:2508.03368, 2025. — [verified: arXiv]
- [Kelly 2026] O. Kelly (Google DeepMind), "Game Arena: Poker and Werewolf, and Gemini 3 tops chess," Google blog, 2 Feb 2026 (Kaggle Game Arena launched Aug 2025). — [verified: blog post; the poker methodology itself is on the Kaggle blog, which could not be read, see below]
- [Zhuang 2025] R. Zhuang, A. Gupta, R. Yang, A. Rahane, Z. Li, G. Anumanchipalli, "PokerBench: Training large language models to become professional poker players," in *Proc. AAAI*, 39(24), 26175–26182, 2025, doi:10.1609/aaai.v39i24.34814. — [verified: AAAI OJS + Crossref]
- [Provost 2026] M.-A. Provost, N. Ilenic, C. Solinas, P. Beardsell, "GTO Wizard Benchmark," arXiv:2603.23660, 2026. — [verified: arXiv abstract]
- [Johanson 2007] M. Johanson, M. Zinkevich, M. Bowling, "Computing robust counter-strategies," in *Proc. NIPS*, 2007. — [already cited in corpus step 08; not re-checked]
- [Szafron 2013] D. Szafron, R. Gibson, N. Sturtevant, "A parameterized family of equilibrium profiles for three-player Kuhn poker," in *Proc. AAMAS*, 2013, pp. 247–254. — [verified: IFAAMAS proceedings PDF listing + abstract]
- [Ge 2025] J. Ge, Y. Wang, W. Li, C. Jin, "Securing equal share: A principled approach for learning multiplayer symmetric games," in *Proc. ICML*, 2025, pp. 18989–19010; arXiv:2406.04201. — [verified: arXiv HTML (Props. 4.1–4.2) + ICML listing]
- [Celli & Gatti 2018] A. Celli, N. Gatti, "Computational results for extensive-form adversarial team games," in *Proc. AAAI*, 32(1), 2018, doi:10.1609/aaai.v32i1.11462. — [verified: AAAI OJS + Crossref]
- [Zhang 2021] Y. Zhang, B. An, J. Černý, "Computing ex ante coordinated team-maxmin equilibria in zero-sum multiplayer extensive-form games," in *Proc. AAAI*, 35(6), 5813–5821, 2021, doi:10.1609/aaai.v35i6.16728. — [verified: arXiv comments + Crossref]
- [Zhang 2023] B. H. Zhang, G. Farina, T. Sandholm, "Team belief DAG: Generalizing the sequence form to team games for fast computation of correlated team max-min equilibria via regret minimization," in *Proc. ICML*, PMLR 202, 2023, pp. 40996–41018. — [verified: PMLR + DBLP]
- [Ge 2024] Z. Ge, Z. Xu, T. Ding, L. Meng, B. An, W. Li, Y. Gao, "Safe and robust subgame exploitation in imperfect information games," in *Proc. ICML*, PMLR 235, 2024, pp. 15255–15270. — [verified: PMLR]
- [Fu 2022], [Jing 2024b], [Ma 2024], [Caen 2026] — opponent-modelling protocols, full entries in `lit_gaps.md` (C1).
- [Mazrooei 2013] P. Mazrooei, C. Archibald, M. Bowling, "Automating collusion detection in sequential games," in *Proc. AAAI*, 27(1), 675–682, 2013, doi:10.1609/aaai.v27i1.8674. — [verified: AAAI OJS + Crossref]
- [Bonjour 2022] T. Bonjour, V. Aggarwal, B. Bhargava, "Information theoretic approach to detect collusion in multi-agent games," in *Proc. UAI*, PMLR 180, 2022. — [verified: PMLR page]

## Open questions / to verify

- **Kaggle Game Arena poker protocol.** A search snippet of the Kaggle blog reports 900,000
  duplicate hands, with each model pair playing 20,000 hands ranked by BB/100. The blog page
  itself could not be machine-read, and the Google and dev.to posts give no protocol details.
  [unverified: numbers from snippet only.] The Werewolf leaderboard image is labelled
  "Equilibrium Rating", which is consistent with [Liu 2025] / [Marris 2025], but the method was
  not confirmed.
- **VasE venue.** arXiv v4 (June 2025) lists no journal reference, and an OpenReview entry
  exists but was not accessible. Cite as arXiv unless the venue is confirmed.
  **Deviation ratings** [Marris 2025] likewise have no venue listed.
- **Elo Uncovered** (Boubdir et al.). Verified as a GEM 2023 workshop paper (ACL Anthology).
  Crossref also lists a NeurIPS 2024 version with the same title, which was not checked. Use
  only if §1.6 needs an LLM-specific Elo critique; [Balduzzi 2018] and [Bertrand 2023] already
  cover the point.
- **Johanson 2011 numbers.** No specific exploitability values are quoted from it. The
  "head-to-head vs exploitability indiscernible in limit hold'em" statement is attributed to it
  by [Moravčík 2017]. If Chapter I wants a number, read §6 of the IJCAI paper.
- **"ABR" terminology.** The literature says "approximate best response" or
  "learned best response" (ISMCTS-BR) [Timbers 2022]. No separate method named "ABR" was found.
  Use the descriptive term.
- **Corrections for the existing corpus / plans** (found while checking; these files were not
  edited):
  - `planning/rawSteps/step_14…`: AIVAT is Burch, Schmid, Moravčík, Morrill & Bowling, AAAI
    **2018**, not "Burch, Johanson & Bowling (2019)". "Re-evaluating evaluation" is NeurIPS
    **2018**, not 2019.
  - `deliverables/reports/step10`, `step11`: the "spinning top" footnote cites Balduzzi et al.
    2019 (ICML). That paper gives the transitive/cyclic decomposition. The spinning-top
    geometry is [Czarnecki 2020]. Cite both.
