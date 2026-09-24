# Step 11 — Chapter I extract
**Feeds:** § 1.5 (primary), § 1.6, § 1.1

## Digest

With three or more players, the guarantees that anchor two-player zero-sum play disappear. Computing a Nash equilibrium is PPAD-complete already for three-player games [1]. Zero-sum games with three or more players are no easier, because a dummy player turns any two-player game into a three-player zero-sum one [2]. If players select equilibria independently, the resulting profile need not be an equilibrium; the authors of the first superhuman six-player poker agent call the right goal in such games an open question [2]. Nash equilibrium also guards only against unilateral deviations. Joint deviations by coalitions require stronger concepts such as coalition-proof equilibrium [3]. In three-player Kuhn poker, one player can shift utility between the other two while all remain within a family of equilibria [4].

Cooperative game theory supplies the vocabulary for coalitions. The Shapley value [5] is the unique allocation satisfying efficiency, symmetry, null-player and additivity axioms. The core is the set of allocations that no coalition can improve upon, and it may be empty [6]. Every essential constant-sum game has an empty core [7]. A winner-takes-all game in which no player can guarantee a win alone is such a game (analysis), so no division of the spoils is stable and alliances are temporary by construction. Shapley-based credit assignment splits a team reward among agents in cooperative multi-agent reinforcement learning [8].

For competitive play against coalitions, worst-case notions exist only in restricted forms:
- team-maxmin equilibria against a coordinated team [9, 10];
- an equal-share objective that is provably unattainable against heterogeneous opponents [11];
- comparisons of synchronous and asynchronous coalitions [12].

KL-regularized search towards an imitation-learned human policy produced strong play in seven-player Diplomacy [13, 14]. The anchor serves human compatibility; it is not a loss bound.

Collusion detection is studied as a separate task. Methods include collusion tables built from poker hand histories [15], mutual information between agents' actions [16], social-graph features in team-based online games [17], and designed probe games that reveal hidden coalition structure [18]. None of them couples detection to the detecting agent's own play.

So Long Sucker is a four-player bargaining game whose outcome rests on unenforceable agreements [19]. It has been proposed as a multi-agent RL benchmark. There, DQN-family agents reach about half of the maximum reward, and coalition-aware strategies are named as future work [20]. Its two-player endgame is fully characterized [21].

At population level, empirical game-theoretic analysis estimates a meta-game from simulated matches [22]. Zero-sum functional-form games decompose into transitive and cyclic components [23], and many real-world games show a "spinning top" geometry [24]. These decompositions are pairwise tools. Applying them to an N-player payoff tensor requires a projection, which can discard coalition effects (analysis).

## Key sources
1. C. Daskalakis, P. W. Goldberg, C. H. Papadimitriou, "The complexity of computing a Nash equilibrium," *SIAM J. Comput.*, vol. 39, no. 1, pp. 195–259, 2009. DOI 10.1137/070699652. [verified: Crossref incl. abstract ("three-player games … PPAD-complete")]
2. N. Brown, T. Sandholm, "Superhuman AI for multiplayer poker," *Science*, vol. 365, no. 6456, pp. 885–890, 2019. DOI 10.1126/science.aay2400. [verified: full-text PDF; quotes on dummy-player hardness, "not clear that playing such an equilibrium strategy would be wise", "what the right goal should even be"]
3. B. D. Bernheim, B. Peleg, M. D. Whinston, "Coalition-proof Nash equilibria I. Concepts," *J. Econ. Theory*, vol. 42, no. 1, pp. 1–12, 1987. DOI 10.1016/0022-0531(87)90099-8. [verified: Crossref metadata only]
4. D. Szafron, R. Gibson, N. Sturtevant, "A parameterized family of equilibrium profiles for three-player Kuhn poker," in *Proc. AAMAS*, 2013, pp. 247–254. [verified in lit_evaluation.md (IFAAMAS listing + abstract); not re-checked]
5. L. S. Shapley, "A value for n-person games," in *Contributions to the Theory of Games II* (Ann. Math. Stud. 28). Princeton Univ. Press, 1953, pp. 307–318. DOI 10.1515/9781400881970-018. [verified: Crossref]
6. G. Chalkiadakis, E. Elkind, M. Wooldridge, *Computational Aspects of Cooperative Game Theory*, Synthesis Lectures on AI and ML. Morgan & Claypool, 2011. DOI 10.2200/S00355ED1V01Y201107AIM016. [verified: Crossref (resolves to the Springer reissue 10.1007/978-3-031-01558-8, listed 2012); contents not read]
7. T. S. Ferguson, *Game Theory*, Part IV "Games in Coalitional Form," §2.3, Thm. 1 ("The core of an essential n-person constant-sum game is empty"), class notes, UCLA Math 167, 2000. [verified: PDF text; lecture notes, so replace with a textbook (Owen) before citing]
8. J. Wang, Y. Zhang, T.-K. Kim, Y. Gu, "Shapley Q-value: A local reward approach to solve global reward games," in *Proc. AAAI*, vol. 34, no. 5, pp. 7285–7292, 2020. DOI 10.1609/aaai.v34i05.6220. [verified: Crossref]
9. A. Celli, N. Gatti, "Computational results for extensive-form adversarial team games," in *Proc. AAAI*, vol. 32, no. 1, 2018. DOI 10.1609/aaai.v32i1.11462. [verified in lit_evaluation.md; not re-checked]
10. Y. Zhang, B. An, J. Černý, "Computing ex ante coordinated team-maxmin equilibria in zero-sum multiplayer extensive-form games," in *Proc. AAAI*, vol. 35, no. 6, pp. 5813–5821, 2021. DOI 10.1609/aaai.v35i6.16728. [verified in lit_evaluation.md; not re-checked]
11. J. Ge, Y. Wang, W. Li, C. Jin, "Securing equal share: A principled approach for learning multiplayer symmetric games," in *Proc. ICML*, 2025, pp. 18989–19010. arXiv:2406.04201. [verified in lit_gaps.md (Props. 4.1–4.2); not re-checked]
12. J. Babyak, K. Buck, L. Dichter, D. Jiang, K. Zumbrun, "Synchronous vs. asynchronous coalitions in multiplayer games, with applications to guts poker," arXiv:2412.19855, 2024. [verified in lit_gaps.md (arXiv metadata); not re-checked]
13. A. P. Jacob, D. J. Wu, G. Farina, A. Lerer, H. Hu, A. Bakhtin, J. Andreas, N. Brown, "Modeling strong and human-like gameplay with KL-regularized search," in *Proc. ICML*, 2022. arXiv:2112.07544. [verified in lit_gaps.md; not re-checked]
14. A. Bakhtin, D. J. Wu, A. Lerer, J. Gray, A. P. Jacob, G. Farina, A. H. Miller, N. Brown, "Mastering the game of no-press Diplomacy via human-regularized reinforcement learning and planning," in *Proc. ICLR*, 2023. arXiv:2210.05492. [verified in lit_gaps.md; not re-checked]
15. P. Mazrooei, C. Archibald, M. Bowling, "Automating collusion detection in sequential games," in *Proc. AAAI*, vol. 27, no. 1, pp. 675–682, 2013. DOI 10.1609/aaai.v27i1.8674. [verified in lit_evaluation.md; not re-checked]
16. T. Bonjour, V. Aggarwal, B. Bhargava, "Information theoretic approach to detect collusion in multi-agent games," in *Proc. UAI*, PMLR 180, 2022. [verified in lit_evaluation.md; not re-checked]
17. L. Greige, F. De Mesentier Silva, M. Trotter, C. Lawrence, P. Chin, D. Varadarajan, "Collusion detection in team-based multiplayer games," arXiv:2203.05121, 2022. [verified in lit_gaps.md; not re-checked]
18. Y. E. Xu, Z. Feng, F. Fang, "Deviate or not: Learning coalition structures with multiple-bit observations in games," in *Proc. AAAI*, vol. 39, no. 13, pp. 14184–14192, 2025. DOI 10.1609/aaai.v39i13.33553. [verified in lit_gaps.md; not re-checked]
19. M. Hausner, J. Nash, L. Shapley, M. Shubik, "So Long Sucker — A four-person game," in M. Shubik (ed.), *Game Theory and Related Approaches to Social Behavior*. New York: Wiley, 1964, pp. 359–361. [verified: the book exists (OUP *Social Forces* review listing, Internet Archive record); chapter title and pages from Wikipedia and secondary citations; the chapter itself was not seen]
20. M. Sharan, C. Adak, "Reinforcing competitive multi-agents for playing 'So Long Sucker'," arXiv:2411.11057, 2024 (v2 2025). [verified: arXiv abstract]
21. J.-L. De Carufel, M. R. Jerade, "So Long Sucker: Endgame analysis," arXiv:2403.17302, 2024 (v2 2025). [verified: arXiv abstract + HTML v2 introduction]
22. M. P. Wellman, "Methods for empirical game-theoretic analysis," in *Proc. AAAI*, 2006, pp. 1552–1556. [verified in lit_evaluation.md; not re-checked]
23. D. Balduzzi, M. Garnelo, Y. Bachrach, W. M. Czarnecki, J. Pérolat, M. Jaderberg, T. Graepel, "Open-ended learning in symmetric zero-sum games," in *Proc. ICML*, PMLR 97, 2019, pp. 434–443. arXiv:1901.08106. [verified in lit_evaluation.md; not re-checked]
24. W. M. Czarnecki, G. Gidel, B. Tracey, K. Tuyls, S. Omidshafiei, D. Balduzzi, M. Jaderberg, "Real world games look like spinning tops," in *Proc. NeurIPS*, 2020. arXiv:2004.09468. [verified in lit_evaluation.md; not re-checked]

## Gaps
- **G-a (C2): No N-player exploitation method comes with a checked safety criterion or is tested against colluding opponents.** Safety notions for N players exist, but they are either very conservative (team-maxmin [9, 10]) or unattainable against heterogeneous opponents (equal share [11]). KL anchoring [13, 14] is behavioural regularization, not a loss bound. This matches `lit_gaps.md`: C2 is open at the core. Do not claim that "coalition dynamics are unstudied" [12, team-game literature], and do not claim that "safety theory ignores N players" [11].
- **G-b (C2 → C1, fair play): collusion detection is not coupled to play.** Detectors [15–18] are scored offline as classification tasks on logs or probe games. No work found lets an agent detect a coalition forming against itself during a match and then adjust its response within a safety bound (`lit_gaps.md`: "None of these links detection to what the agent does next").
- **G-c (C3): no coalition-aware robustness metric for agent evaluation.** Population tools [22–24] and exploitability-style metrics are pairwise or equilibrium-distance measures. An N-player tensor must be projected before these tools apply. `lit_evaluation.md` failure mode 8 found no metric that asks how an agent fares when some opponents coordinate. (Whether a tensor-native transitive/cyclic decomposition exists was not searched; see To verify.)
- **G-d (C1/C2, testbed): the one RL treatment of So Long Sucker is coalition-blind** and lists coalition-aware strategies as future work [20]. The two-player endgame is solved [21], which gives an exact anchor inside a small N-player game. This is a testbed opportunity, not a field-level gap.

## Own evidence
- **A planted alliance is readable from moves.** A help/harm detector recovers a scripted pair {0,1} exactly (pair score 10.0; every other entry 0 or −1). Source: `implementation/step11/implementation/results/smoke_results.json` (`detector`). Caveat: one overt scripted pair, no false-positive test. The engine omits negotiation, so alliances show up *only* on the board, which is the easy case compared with poker collusion.
- **One engine rule can dominate N-player evaluation.** In the simplified SLS engine, about 99.5 % of random games end in deadlock. A lowest-index tie-break then gave seat 0 roughly twice its fair share of wins (94 of 200 random-game wins instead of about 50). It also inflated a trained agent's win rate from about 0.41 to about 0.87. An unbiased tie-break reduced the symmetric-position credit spread from 0.54 to 0.013. Source: `implementation/step11/EXECUTION_NOTES.md` (Phase 4 refinement); `smoke_results.json`. Caveat: specific to this engine's simplified rules. Usable in § 1.6 only as an illustration that "a symmetric position is not a symmetric outcome".
- **Do not cite as evidence of coalition learning.** At α ≈ 0 (win reward removed), the detector score rises by +0.0376 ± 0.0103 over sparse-reward agents (5 seeds, `results/sweep_scale.json`), while the win rate falls to 0.29. The "Shapley credit" as implemented carries no coalition information: it reduces to each agent's own win-probability share, or to its own critic value minus the table mean. The score also counts hostile interactions (review F11-C02).
- **Population composition decides the structure.** The cyclic ratio is 0.25 for a skill-ladder pool (`smoke_results.json`, `egta`) and about 0.57–0.69 for a coalition pool, where the transitive part is still slightly larger. Caveat: 4–5 hand-coded strategies with a pairwise projection. The coalition-pool values exist only in `EXECUTION_NOTES.md`, with no results file.

## Figure candidate
None. The chapter's figures show the project's own pipeline and need heavy repair (review G02–G09). Fig. 64 (detector diagram, `summary/make_sls_coalition_figure.py`) could illustrate on-board coalition signals in § 1.5, but only after its "no negotiation" note is corrected (F11-C03). For a state-of-the-art chapter it adds little that one sentence cannot say.

## To verify
- **The year 1950.** It has no primary source: Wikipedia cites only the 1964 chapter, De Carufel & Jerade write "In 1964 … was developed", and Burnett says "late-1950s". Cite the 1964 publication and do not state 1950. The chapter pages (359–361) were not seen in the book.
- **The empty-core theorem.** Replace Ferguson's lecture notes [7] with a textbook source (Owen's *Game Theory* is the usual attribution; edition and theorem number unchecked). "SLS is essential constant-sum" is my analysis and needs one sentence of justification: a single player cannot guarantee a win.
- **Sharan & Adak v2 (Oct 2025).** Only the abstract was read. Check that v2 adds no coalition mechanism before calling their agents "coalition-blind".
- **References [3] and [6].** Only metadata was verified. Read before attributing specific definitions to them.
- **References [4], [9]–[18], [22]–[24].** Verified by the literature-gap pass, not re-checked here.
- **Tensor-native decompositions for N-player meta-games** (beyond α-Rank and N-player ratings) were not searched. Do not claim their absence.
- **The coalition-pool cyclic ratios (0.57–0.69)** have no results file. Rerun `validate.py` with the output saved before quoting them.
