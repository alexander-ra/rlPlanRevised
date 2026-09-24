# Step 04 — Chapter I extract
**Feeds:** § 1.2 (primary)

## Digest

Equilibrium solvers scale with the number of information sets, and real games exceed them by many orders of magnitude. Heads-up limit Texas hold'em has 3.19 × 10¹⁴ decision points [2]. The no-limit variant of the Annual Computer Poker Competition has 6.37 × 10¹⁶¹ information sets [1]. The standard response is abstraction: solve a smaller game whose strategies map back to the original, then measure the loss in the original game. Information abstraction merges information sets; action abstraction restricts the actions considered.

Lossless abstraction merges only strategically isomorphic situations. It made possible an exact solution of Rhode Island Hold'em, a game of 3.1 billion nodes [3]. Lossy abstraction can carry a bound on the resulting exploitability in which each merge's error is weighted by its reach probability. Finding the bound-minimizing abstraction is NP-complete even for one player, but a single level reduces to clustering [4, 5]. Practical abstractions cluster hands with k-means under the earth mover's distance between hand-strength distributions, with imperfect recall. In Texas hold'em these outperform expectation-based and perfect-recall abstractions of equal size [6, 8]. They carry no guarantee. Refining an abstraction can make the resulting strategy more exploitable [9]. An abstract equilibrium is also not the least exploitable strategy the abstraction can represent: CFR-BR finds strategies up to three times less exploitable [6, 7].

Opponent actions outside the abstraction must be translated. The pseudo-harmonic mapping, derived from the equilibrium of a simplified game, is markedly less exploitable than earlier heuristics [10]. Since 2017, strong agents have paired an abstract blueprint with real-time subgame solving [13]. Safe subgame solving never makes the blueprint more exploitable in two-player zero-sum games [11, 12]. Solving a new subgame for each off-tree action was about ten times less exploitable than pseudo-harmonic translation in a no-limit test game [12]. DeepStack [14] and Deep CFR [15] replace precomputed abstraction with learned approximation.

Sampling-based solvers, together with abstraction and real-time refinement, therefore make equilibrium computation feasible at the scale of poker. It remains an approximation whose quality has to be measured in the full game. The safety guarantee of subgame solving is stated for two players only.

## Key sources
1. M. Johanson, "Measuring the size of large no-limit poker games," Univ. of Alberta, technical report, 2013; arXiv:1302.7008. [verified: arXiv PDF, Table 6: 6.37 × 10¹⁶¹ information sets, 6.31 × 10¹⁶⁴ states]
2. M. Bowling, N. Burch, M. Johanson, O. Tammelin, "Heads-up limit hold'em poker is solved," *Science*, vol. 347, no. 6218, pp. 145–149, 2015. DOI 10.1126/science.1259433. [verified: Crossref + PDF text: 3.16 × 10¹⁷ states, 3.19 × 10¹⁴ decision points]
3. A. Gilpin, T. Sandholm, "Lossless abstraction of imperfect information games," *J. ACM*, vol. 54, no. 5, art. 25, 2007. DOI 10.1145/1284320.1284324. [verified: Crossref + PDF: 3.1 billion nodes, signal tree 6,632,705, "over four orders of magnitude"]
4. C. Kroer, T. Sandholm, "Extensive-form game abstraction with bounds," in *Proc. ACM EC*, 2014, pp. 621–638. DOI 10.1145/2600057.2602905. [verified: Crossref metadata only]
5. C. Kroer, T. Sandholm, "Imperfect-recall abstractions with bounds in games," in *Proc. ACM EC*, 2016, pp. 459–476. DOI 10.1145/2940716.2940736; arXiv:1409.3302. [verified: Crossref + arXiv PDF: Thm. 3 NP-complete for a single player and tree height two; single-level reduction to clustering, 2-approximation in the metric case; leaf error weighted by reach probability]
6. M. Johanson, N. Burch, R. Valenzano, M. Bowling, "Evaluating state-space abstractions in extensive-form games," in *Proc. AAMAS*, 2013, pp. 271–278. [verified: PDF + Crossref: EMD over hand-strength histograms; distribution-aware "clear advantage once the abstract game is large enough"; imperfect > perfect recall; CFR-BR "as little as 1/3"; 2,428,287,420 canonical river combinations]
7. M. Johanson, N. Bard, N. Burch, M. Bowling, "Finding optimal abstract strategies in extensive-form games," in *Proc. AAAI*, vol. 26, no. 1, 2012, pp. 1371–1379. DOI 10.1609/aaai.v26i1.8269. [verified: Crossref + PDF abstract/introduction]
8. S. Ganzfried, T. Sandholm, "Potential-aware imperfect-recall abstraction with earth mover's distance in imperfect-information games," in *Proc. AAAI*, vol. 28, no. 1, 2014. DOI 10.1609/aaai.v28i1.8816. [verified: Crossref + PDF abstract]
9. K. Waugh, D. Schnizlein, M. Bowling, D. Szafron, "Abstraction pathologies in extensive games," in *Proc. AAMAS*, 2009, pp. 781–788. [verified: PDF abstract ("Refining an abstraction can actually lead to a weaker strategy") + Crossref pages]
10. S. Ganzfried, T. Sandholm, "Action translation in extensive-form games with large action spaces: Axioms, paradoxes, and the pseudo-harmonic mapping," in *Proc. IJCAI*, 2013, pp. 120–127. [verified: IJCAI PDF text: formula, conclusions, Tartanian1 exploitation]
11. N. Burch, M. Johanson, M. Bowling, "Solving imperfect information games using decomposition," in *Proc. AAAI*, vol. 28, no. 1, 2014. DOI 10.1609/aaai.v28i1.8810. [verified: Crossref metadata only]
12. N. Brown, T. Sandholm, "Safe and nested subgame solving for imperfect-information games," in *Proc. NIPS*, 2017; arXiv:1705.02955. [verified: arXiv v3 PDF: two-player zero-sum scope; safe = "no higher than" the blueprint; Table 4: 1,465 vs 119–150 mbb/h in no-limit flop hold'em]
13. N. Brown, T. Sandholm, "Superhuman AI for heads-up no-limit poker: Libratus beats top professionals," *Science*, vol. 359, no. 6374, pp. 418–424, 2018. DOI 10.1126/science.aao1733. [verified: Crossref]
14. M. Moravčík et al., "DeepStack: Expert-level artificial intelligence in heads-up no-limit poker," *Science*, vol. 356, no. 6337, pp. 508–513, 2017. DOI 10.1126/science.aam6960. [verified: Crossref + PDF text ("does not compute and store a complete strategy prior to play")]
15. N. Brown, A. Lerer, S. Gross, T. Sandholm, "Deep counterfactual regret minimization," in *Proc. ICML*, 2019; arXiv:1811.00164. [verified: arXiv abstract ("obviates the need for abstraction")]
16. N. Brown, T. Sandholm, "Superhuman AI for multiplayer poker," *Science*, vol. 365, no. 6456, pp. 885–890, 2019. DOI 10.1126/science.aay2400. [verified: Crossref metadata only]
17. Y. Rubner, C. Tomasi, L. J. Guibas, "The Earth Mover's Distance as a metric for image retrieval," *Int. J. Comput. Vis.*, vol. 40, no. 2, pp. 99–121, 2000. DOI 10.1023/A:1026543900054. [verified: Crossref; optional]

## Gaps
- **G-a (C3): abstraction quality can be measured exactly only in small or limit games, and the measures disagree.**
  - Full-game exploitability, or CFR-BR, is computable only where a best response can be traversed [6, 7]. Larger no-limit and multiplayer agents are judged by head-to-head play.
  - [6] reports that earlier work found exploitability "does not correlate well with one-on-one performance". The quality of an abstraction therefore depends on which metric is chosen.
  - This supports C3's framing ("existing evaluation breaks here"). It is consistent with `lit_gaps.md` C3 (narrowed): the open part is reporting representation size, worst-case robustness and performance against a population *together*, across games. No separate gap is claimed.
- **G-b (C2): the safety of real-time refinement is a two-player result.**
  - Safe subgame solving guarantees no increase in exploitability only in two-player zero-sum games [12].
  - The six-player Pluribus uses the same blueprint-plus-search architecture [16]. No equivalent guarantee was found for it; this has to be checked before it is stated (To verify).
  - This matches `lit_gaps.md` C2, "safety theory stops at two players", and adds that the *refinement* step of the standard pipeline has the same boundary.
- *Not claimed:* "abstraction destroys the information an opponent model needs". Opponent models built over abstracted games exist (step-07 source [5], Ganzfried & Sandholm 2011), and no search was made for work on abstraction granularity and opponent inference. See To verify.

## Own evidence
- **Lossless compression buys iterations.**
  - Result: suit isomorphism reduces fixed-limit Leduc from 936 to 288 information sets. Under the same 180-s CFR+ budget it reaches 3.13 × 10⁻⁶ exploitability against 4.44 × 10⁻⁵ for the full game (14,185 vs 2,655 iterations). On Extended Leduc (4 ranks) it goes from 10,304 to 2,968 information sets, and exploitability from 0.0272 to 0.00126.
  - Source: `implementation/step04/phase4/.day07_cfrplus_results.csv`, report_en §3.
  - Caveat: three runs of deterministic CFR+ are not independent; one machine; toy games. The gain is iterations per second, not abstraction quality.
- **Lossy card buckets set a floor.**
  - Result: perfect-recall k = 2 / k = 3 bucketings stay at 0.571 / 0.382 after more than 11,000 iterations, four orders of magnitude above the full game.
  - Source: same file.
  - Caveat: Leduc's hand-strength distributions collapse to three shapes (k = 5 gives the same result as k = 3).
- **Do not cite:**
  - The action-abstraction numbers (0.673 Mini-NL; 4.696 / 4.734 Extended). The harness plays every abstract small bet as the large bet, and the three translators return identical values (review F04-C01).
  - Imperfect-recall results: the chapter's own runs contradict the literature claim (F04-C02).
  - The Pareto figure, which plots a 200-iteration smoke test (F04-G04).

## Figure candidate
None. § 1.2 has about one page for four chapters. The only candidate would be a regenerated size-vs-exploitability plot from the 180-s CFR+ data (F04-G04 fix), without the action-abstraction points until F04-C01 is resolved. It illustrates a textbook trade-off and does not support a gap.

## To verify
- [4] Kroer & Sandholm 2014: whether the bounds cover n-player or general-sum games. Not read; only the metadata was checked.
- [16] Pluribus: whether its real-time search carries any safety or exploitability guarantee. `lit_gaps.md` records only that it "plays a fixed strategy".
- The "about ten times" figure in [12] comes from one experiment (no-limit flop hold'em, one translator). Do not generalise it to HUNL.
- Gilpin & Sandholm (AAAI 2008), "expectation-based stronger in small abstractions", is known only through [6]'s summary. Read it before citing it directly.
- Modicum (Brown, Sandholm & Amos, 2018) is named in the chapter but was not checked.
- The Tishby et al. information-bottleneck reference was verified on arXiv only (physics/0004057). The Allerton 1999 venue is unverified. Use it only if Chapter I keeps the IB analogy, which is the candidate's own framing.
- Page range of [10]: the IJCAI PDF prints 120–127, while [12] cites 120–128. Check against the proceedings index.
- Whether any work quantifies how abstraction granularity limits opponent inference. It was not searched; only then could it become a C1 gap.
- The chapter's action-abstraction experiment must be rerun after the code fix in F04-C01 before any number from it appears in Chapter I.
