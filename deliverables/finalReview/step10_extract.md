# Step 10 — Chapter I extract
**Feeds:** § 1.5 (primary), § 1.6

## Digest

Population-based methods train or evaluate a set of agents instead of a single policy. When strategies beat each other in cycles, training only against the latest self can chase those cycles without progress [1]. Evolutionary game theory gives the idealised picture. Under the replicator dynamics every Nash equilibrium is a rest point, every stable rest point is a Nash equilibrium, and every evolutionarily stable strategy (ESS) is asymptotically stable. None of the converses holds, and in zero-sum rock–paper–scissors all interior orbits are closed cycles around the equilibrium [2]. The same dynamics describe multi-agent learning algorithms [3].

The structure of a zero-sum interaction can be measured. An antisymmetric payoff matrix decomposes orthogonally into a transitive component, the rating differences, and a cyclic component [4, 5]. Real games appear to have a "spinning-top" geometry. Cycles are most numerous at intermediate strength and thin out towards the extremes of strength. This explains why training needs populations and how their size relates to the game [6].

Convergence guarantees exist only in two-player zero-sum games with exact best responses. The double-oracle algorithm converges to a minimax equilibrium [7]. PSRO generalises it, together with fictitious play and independent RL, to approximate best responses learned by deep RL, and selects meta-strategies by empirical game-theoretic analysis [8]. Population-based training (PBT) copies better-performing models and perturbs their hyperparameters [9]. AlphaStar's league combines these ideas at scale. Main agents train by prioritised fictitious self-play against the league, main exploiters target the current main agents, and league exploiters target the whole league. Almost 900 players were created, and the final agents were rated above 99.8% of ranked human players. The league's robustness is shown only empirically, through exploiter win rates, relative population performance and a league Nash that puts little weight on old players [1].

Empirical game-theoretic analysis (EGTA) estimates a normal-form meta-game among a finite set of strategies from simulation and analyses it with equilibrium tools [10, 13]. An equilibrium of the estimated meta-game approximates one of the exact meta-game, with bounds on the samples needed [11]. α-Rank ranks agents by the stationary distribution of an evolutionary process. It runs in polynomial time and covers asymmetric and many-player games, subject to a ranking-intensity parameter [12]. All of these score agents relative to the population they are computed on. They bound worst-case exploitability in the full game only when that population contains the relevant best responses, as in double oracle (analysis).

## Key sources
1. O. Vinyals, I. Babuschkin, W. M. Czarnecki, M. Mathieu, A. Dudzik et al., "Grandmaster level in StarCraft II using multi-agent reinforcement learning," *Nature*, vol. 575, no. 7782, pp. 350–354, 2019. DOI 10.1038/s41586-019-1724-z. [verified: Crossref; full text of DeepMind's unformatted preprint (league types, PFSP, "almost 900 distinct players", 99.8%, FSP convergence sentence, "suggesting … does not cycle or regress")]
2. J. Hofbauer, K. Sigmund, "Evolutionary game dynamics," *Bull. Amer. Math. Soc.*, vol. 40, no. 4, pp. 479–519, 2003. DOI 10.1090/S0273-0979-03-00988-1. [verified: full text (§2.3 folk theorem, §2.6 ESS, Thm 2 RPS closed orbits)]
3. D. Bloembergen, K. Tuyls, D. Hennes, M. Kaisers, "Evolutionary dynamics of multi-agent learning: A survey," *J. Artif. Intell. Res.*, vol. 53, pp. 659–697, 2015. DOI 10.1613/jair.4818. [verified: Crossref metadata only]
4. D. Balduzzi, K. Tuyls, J. Pérolat, T. Graepel, "Re-evaluating evaluation," in *Proc. NeurIPS*, 2018. arXiv:1806.02643. [verified: arXiv PDF text (Hodge decomposition into transitive + cyclic; Elo "meaningless" in cyclic games; Nash averaging)]
5. D. Balduzzi, M. Garnelo, Y. Bachrach, W. M. Czarnecki, J. Pérolat, M. Jaderberg, T. Graepel, "Open-ended learning in symmetric zero-sum games," in *Proc. ICML*, PMLR 97, 2019, pp. 434–443. arXiv:1901.08106. [verified: arXiv abstract; pages per lit_evaluation.md]
6. W. M. Czarnecki, G. Gidel, B. Tracey, K. Tuyls, S. Omidshafiei, D. Balduzzi, M. Jaderberg, "Real world games look like spinning tops," in *Proc. NeurIPS*, 2020. arXiv:2004.09468. [verified: arXiv abstract; venue per lit_evaluation.md]
7. H. B. McMahan, G. J. Gordon, A. Blum, "Planning in the presence of cost functions controlled by an adversary," in *Proc. ICML*, 2003, pp. 536–543. [verified: PDF text (Theorem 1: double oracle converges to a minimax equilibrium); pages via proceedings listing]
8. M. Lanctot, V. Zambaldi, A. Gruslys, A. Lazaridou, K. Tuyls, J. Pérolat, D. Silver, T. Graepel, "A unified game-theoretic approach to multiagent reinforcement learning," in *Proc. NIPS*, 2017. arXiv:1711.00832. [verified: arXiv abstract]
9. M. Jaderberg, V. Dalibard, S. Osindero, W. M. Czarnecki et al., "Population based training of neural networks," arXiv:1711.09846, 2017. [verified: arXiv abstract]
10. M. P. Wellman, "Methods for empirical game-theoretic analysis," in *Proc. AAAI*, 2006, pp. 1552–1555. [verified: AAAI PDF (page folios 1552–1555)]
11. K. Tuyls, J. Pérolat, M. Lanctot, E. Hughes, R. Everett, J. Z. Leibo, C. Szepesvári, T. Graepel, "Bounds and dynamics for empirical game theoretic analysis," *Auton. Agents Multi-Agent Syst.*, vol. 34, no. 1, art. 7, 2020. DOI 10.1007/s10458-019-09432-y. [verified: Crossref; abstract of the AAMAS 2018 version, arXiv:1803.06376]
12. S. Omidshafiei, C. Papadimitriou, G. Piliouras, K. Tuyls, M. Rowland, J.-B. Lespiau, W. M. Czarnecki, M. Lanctot, J. Pérolat, R. Munos, "α-Rank: Multi-agent evaluation by evolution," *Sci. Rep.*, vol. 9, art. 9937, 2019. DOI 10.1038/s41598-019-45619-9. [verified: Crossref + arXiv abstract 1903.01373]
13. M. P. Wellman, K. Tuyls, A. Greenwald, "Empirical game theoretic analysis: A survey," *J. Artif. Intell. Res.*, vol. 82, pp. 1017–1076, 2025. DOI 10.1613/jair.1.16146. [verified in lit_evaluation.md; not rechecked]
14. J. Hofbauer, K. Sigmund, *Evolutionary Games and Population Dynamics*. Cambridge Univ. Press, 1998. [verified: bibliographic listing only; not read — cite [2] for the specific statements]
15. M. Lanctot et al., "OpenSpiel: A framework for reinforcement learning in games," arXiv:1908.09453, 2019 (NashConv = Σᵢ δᵢ; exploitability = NashConv/n). [verified in lit_evaluation.md]
16. M. Lanctot, J. Schultz, N. Burch, M. O. Smith, D. Hennes, T. Anthony, J. Pérolat, "Population-based evaluation in repeated rock-paper-scissors as a benchmark for multiagent reinforcement learning," *TMLR*, 2023. arXiv:2303.03196. [verified in lit_evaluation.md]
17. J. Ge, Y. Wang, W. Li, C. Jin, "Securing equal share: A principled approach for learning multiplayer symmetric games," in *Proc. ICML*, 2025, pp. 18989–19010. arXiv:2406.04201. [verified in lit_gaps.md]

## Gaps
- **G-a (C2): population training carries no loss guarantee outside two-player zero-sum games with exact best responses.**
  - Double oracle converges only with exact best responses in finite two-player zero-sum games [7]. PSRO generalises it [8], and it recovers that guarantee only in the exact-oracle limit (analysis).
  - The machinery that scales, the league with PFSP and exploiters [1] and PBT [9], has empirical robustness evidence only. None of them states a loss bound relative to a baseline, and none addresses more than two players or coalitions.
  - This is consistent with `lit_gaps.md` C2: the core is still open, but "no N-player safety notion" must not be claimed. Equal share and team-maxmin values exist, and self-play-style meta-algorithms are shown to fail to secure equal share [17].
  - Own evidence: a small league regresses late (below). AlphaStar reports no regression at its scale [1], so the claim must stay "no guarantee", not "leagues regress".
- **G-b (C3): population evaluation is relative, not worst-case.**
  - EGTA meta-Nash [10, 11], Nash averaging [4] and α-Rank [12] score agents against the evaluated population, and α-Rank's ranking depends on its intensity parameter [12]. This matches `lit_evaluation.md` failure modes 1 and 4.
  - Own evidence: a meta-Nash mixture was 2.6× more exploitable than the population's least exploitable agent, which it gave zero weight.
  - The only protocol that reports population return and within-population exploitability together is the repeated-RPS benchmark, for a single two-player game [16]. This is consistent with `lit_gaps.md` C3: narrowed; still open across games, including N-player ones.
- **G-c (C3, analysis; literature check needed): structure diagnostics depend on how the evaluation population is built.**
  - Hodge and spinning-top ratios are properties of a population [4, 6]. In this step the same game read as mostly cyclic (a best-response population) or mostly transitive (training snapshots).
  - Benchmarks fix their population by convention [16]. I found no source that shows this sensitivity explicitly, so it must not be claimed as a documented gap before a search.

## Own evidence
- **Same game, opposite structure.** On Leduc, the Hodge transitive ratio of the PSRO best-response meta-game is 0.457 (smoke, 8 rounds) and 0.411 (scale, 20 rounds, 27 three-cycles). The league's training-snapshot meta-game gives 0.981 / 0.937. Source: `implementation/step10/implementation/results/{smoke,scale}_results.json` (`spinning_top`, `league.league_metagame_transitive_ratio`); report_en §3. Caveat: one run per config; empirical payoff matrices of a toy game.
- **A population score is not a worst-case score.** At scale, the EGTA meta-Nash mixture over 56 agents has NashConv 3.418. The least exploitable agent (1.305, snapshot from epoch 29) gets zero weight. The mixture is *less* exploitable than each of its three components (3.558, 3.932, 4.262), so the gap comes from the meta-Nash objective, not from mixing. Source: `scale_results.json` → `league.egta`. Caveat: a single PBT run; tabular-extracted PPO policies on Leduc. Values are NashConv (sum over both seats = 2 × OpenSpiel exploitability [15]), not the chapter's "exploitability".
- **No monotone improvement, league or self-play.** The minimum NashConv of the main agents falls from 4.73 to ≈ 1.3–1.4 (epochs 20–40) and ends at 2.05 (epoch 119). The self-play baseline reaches 1.396 at epoch 100 and ends at 3.683. Source: `scale_results.json` → `league.trajectory`, `baselines.selfplay`. Caveat: one seed; 8 live agents and 48 snapshots, against AlphaStar's ≈ 900 players [1].

## Figure candidate
None by default.
- **Spinning top (fig. 57).** It is the natural §1.6 picture, but as printed it is English, has colliding labels, and puts whole games and populations on one top (F10-G04). Its source text also misattributes the concept (F10-S04). A redrawn schematic after Czarnecki et al. [6] would serve better.
- **EGTA pipeline (fig. 62).** If §1.6 needs a process diagram, it can be used after F10-G09. The caveat box must be rewritten, because the "mixing adds tells" claim is wrong (F10-C03).

## To verify
- **[1] "almost 900 distinct players" and the 99.8% figure** were read in DeepMind's unformatted preprint. Confirm them in the typeset Nature article.
- **FSP convergence.** "The mixture converges to a Nash equilibrium in two-player zero-sum games" is Vinyals et al.'s sentence citing their own ref. 20. Cite the original fictitious-play source only after checking it.
- **[11] scope of the bound.** Its abstract (AAMAS 2018 version) says an equilibrium of the meta-game is approximately one of "the true underlying game". Confirm in the JAAMAS text that this means the exact meta-game over the same strategies, not the full game, before paraphrasing.
- **[3]** was checked for metadata only. Read it before attributing the "replicator dynamics ↔ learning algorithms" link to specific algorithms.
- **Pages from `lit_evaluation.md`.** [10] prints pp. 1552–1555; `lit_evaluation.md` says 1552–1556, so use 1552–1555. [5]'s pages and [6]'s NeurIPS venue come from `lit_evaluation.md` and were not rechecked.
- **Claims not to carry into Chapter I:**
  - "PSRO keeps double-oracle convergence with exact oracles" is an inference, not a quoted theorem of [8].
  - Do not reuse the chapter's statements that rest points "are exactly" Nash, that the spinning top is Balduzzi 2019, that the AlphaStar league used "~600 agents", or that "mixing adds tells" (F10-C01, S04, S05, C03).
  - The step-10 numbers are NashConv; label them so.
- **G-c** needs a literature search before it is stated as a gap.
