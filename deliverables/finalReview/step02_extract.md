# Step 02 — Chapter I extract
**Feeds:** § 1.2 (primary), § 1.6 (exploitability)

## Digest

In finite two-player zero-sum games the minimax theorem [1] gives each player a value it can secure against any opponent. A Nash equilibrium, which exists in every finite game [2], then coincides with a minimax profile, so equilibrium play is safe. The guarantee does not extend further. With three players an equilibrium profile can let one player shift utility between the other two [3]. Computing a Nash equilibrium is PPAD-complete, already for two-player general-sum games [4, 5].

Card games are modelled in extensive form. Histories a player cannot tell apart form an information set, and a strategy must act identically across it [6]. Regret matching [7, 8] plays each action in proportion to its positive cumulative regret. Average regret then vanishes at rate O(1/√T), and in two-player zero-sum self-play the average strategies converge to an equilibrium. Counterfactual regret minimization (CFR) [9] bounds a player's overall regret by the sum of immediate counterfactual regrets at its information sets, weighted by the probability that the opponent and chance reach them, and minimizes each with regret matching. The average profile, not the current one, is then an ε-equilibrium with ε = O(Δ|𝓘|√|A|/√T), linear in the number of information sets. Sampling chance outcomes, used in the original poker experiments, belongs to the Monte Carlo CFR family, whose bounds hold with high probability [10]. With the CFR+ variant, heads-up limit hold'em has been essentially weakly solved [11]. Kuhn poker [12] is the standard correctness test [13]: twelve information sets, a one-parameter equilibrium family for the first player, and value −1/18.

Solution quality is measured by exploitability, the sum of both players' best-response values against a profile, zero exactly at equilibrium. The same sum is called NashConv; some libraries report half of it as exploitability [14]. A best response must commit to one action per information set. Matching the game value is not enough: a strategy can earn the full value against an equilibrium opponent yet remain exploitable. Exploitability is a two-player, worst-case notion. It gives no credit for gains against weak opponents, and with more than two players it no longer bounds anyone's loss (§ 1.6).

## Key sources
1. J. von Neumann, "Zur Theorie der Gesellschaftsspiele," *Math. Ann.*, vol. 100, no. 1, pp. 295–320, 1928. DOI 10.1007/BF01448847. [verified: Crossref]
2. J. F. Nash, "Equilibrium points in n-person games," *PNAS*, vol. 36, no. 1, pp. 48–49, 1950. DOI 10.1073/pnas.36.1.48. [verified: Crossref]
3. D. Szafron, R. Gibson, N. Sturtevant, "A parameterized family of equilibrium profiles for three-player Kuhn poker," in *Proc. AAMAS*, 2013, pp. 247–254. [verified: Crossref pages + PDF abstract (utility transfer within the equilibrium family)]
4. C. Daskalakis, P. W. Goldberg, C. H. Papadimitriou, "The complexity of computing a Nash equilibrium," *SIAM J. Comput.*, vol. 39, no. 1, pp. 195–259, 2009. DOI 10.1137/070699652. [verified: Crossref metadata only]
5. X. Chen, X. Deng, S.-H. Teng, "Settling the complexity of computing two-player Nash equilibria," *J. ACM*, vol. 56, no. 3, pp. 1–57, 2009. DOI 10.1145/1516512.1516516. [verified: Crossref metadata only]
6. Y. Shoham, K. Leyton-Brown, *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations*. Cambridge Univ. Press, 2008, §§ 3.3, 3.4.1, 4.1, 5.2, 7.5. [verified: official TOC at masfoundations.org]
7. D. Blackwell, "An analog of the minimax theorem for vector payoffs," *Pacific J. Math.*, vol. 6, no. 1, pp. 1–8, 1956. DOI 10.2140/pjm.1956.6.1. [verified: Crossref]
8. S. Hart, A. Mas-Colell, "A simple adaptive procedure leading to correlated equilibrium," *Econometrica*, vol. 68, no. 5, pp. 1127–1150, 2000. DOI 10.1111/1468-0262.00153. [verified: Crossref]
9. M. Zinkevich, M. Johanson, M. Bowling, C. Piccione, "Regret minimization in games with incomplete information," in *Advances in NIPS 20*, 2007, pp. 1729–1736. [verified: proceedings PDF; Theorems 2–4 and the chance-sampling paragraph read]
10. M. Lanctot, K. Waugh, M. Zinkevich, M. Bowling, "Monte Carlo sampling for regret minimization in extensive games," in *Advances in NIPS 22*, 2009, pp. 1078–1086. [verified: NeurIPS proceedings page (authors, abstract); pages from ACM DL listing]
11. M. Bowling, N. Burch, M. Johanson, O. Tammelin, "Heads-up limit hold'em poker is solved," *Science*, vol. 347, no. 6218, pp. 145–149, 2015. DOI 10.1126/science.1259433. [verified: Crossref; abstract wording via search snippet]
12. H. W. Kuhn, "A simplified two-person poker," in *Contributions to the Theory of Games I* (Annals of Mathematics Studies 24), Princeton Univ. Press, 1950, pp. 97–103. DOI 10.1515/9781400881727-010. [verified: De Gruyter chapter listing via search; equilibrium values cross-checked by exact computation]
13. T. W. Neller, M. Lanctot, "An introduction to counterfactual regret minimization," tutorial (version of 9 July 2013). [verified: PDF read, §§ 2–3, "chance-sampled CFR"; venue (EAAI Model AI Assignments) unverified]
14. M. Lanctot et al., "OpenSpiel: A framework for reinforcement learning in games," arXiv:1908.09453, 2019. [verified: `exploitability.py` source docstring "equivalent to NashConv / num_players"; paper metadata per lit_evaluation.md]
15. N. Brown, T. Sandholm, "Superhuman AI for multiplayer poker," *Science*, vol. 365, no. 6456, pp. 885–890, 2019. DOI 10.1126/science.aay2400. [verified: Crossref; content statements per lit_evaluation.md]

## Gaps
Step 02 is foundational. It establishes the two-player baseline and does not by itself show a gap in the literature. It supplies the premises of two gaps.
- **G-a (C2): the equilibrium safety guarantee is a two-player zero-sum property.**
  - Minimax safety [1, 2] does not survive beyond two players. With three players an equilibrium profile guarantees nothing to an individual player and allows utility transfer between players [3]. Computing an equilibrium is PPAD-complete [4, 5]. Pluribus is evaluated empirically [15].
  - Consistent with `lit_gaps.md` (C2): N-player safety *notions* do exist (equal share, team-maxmin, baseline-relative regret). The open part is exploitation with a stated, empirically tested loss bound in N-player imperfect-information games. Do not write "there is no N-player safety theory".
- **G-b (C3): exploitability, the field's standard quality measure [9, 14], is two-player and worst-case.**
  - It cannot credit gains against weak opponents, and for N > 2 NashConv measures distance from *an* equilibrium, not a guarantee (`lit_evaluation.md`, failure modes 1–2).
  - The converse failure, where game value misses exploitability, is shown by the step's own example (Own evidence 4).
  - An evaluation protocol for adaptive agents has to report both axes.

## Own evidence
1. **CFR recovers the analytical equilibrium family on Kuhn.**
   - *Numbers:* α = 0.1941; P(bet | K) = 0.5825 vs 3α = 0.5822. The second player's Queen calls at 0.335 vs 1/3. Mixed frequencies lie within 0.002–0.011 of the closed form; pure decisions reach ≥ 0.9999.
   - *Source:* `implementation/step02/models/cfr_results.json` (chance-sampled CFR, 10⁵ iterations).
   - *Caveat:* toy game, one unseeded run.
2. **Quality of that profile.**
   - *Numbers:* exact value for the first player −0.05549 (vs −1/18 = −0.05556); NashConv 0.0043.
   - *Source:* computed during this review from `cfr_results.json` by exact traversal of the 6 deals; not yet in any repository file.
   - *Caveat:* the chapter's "−0.0602" is a running mean of sampled payoffs, not this value (review F02-C06).
3. **Convergence rate.**
   - *Numbers:* log–log slope of exploitability −0.489 (`evaluate/convergence.py`). A 5-seed re-run in this review gave −0.53 ± 0.04 (range −0.50 to −0.60).
   - *Caveat:* 6 checkpoints, each an independent run, up to 5·10⁴ iterations. Consistent with, not a confirmation of, the O(1/√T) bound.
4. **Game value is not a validity check.**
   - *Numbers:* if the second player always bluffs the Jack while the first player plays the equilibrium, the game value stays exactly −1/18, yet the first player's best response earns +1/6 per hand (0.22 above the value).
   - *Source:* computed in this review from the closed-form equilibrium.
   - *Caveat:* Kuhn only. Not in any repository file; the chapter states it only qualitatively.

## Figure candidate
None. Chapter I does not need the Kuhn plots. The step's figures are all English, and fig. 5 is illegible in print (review F02-G02–G04). If § 1.2 needs a picture, a newly drawn CFR schematic serves better than fig. 4, which is a generic log–log plot. The schematic would show regret matching at each information set, reach weighting and averaging.

## To verify
- Own evidence 2–4 were computed during the review. Reproduce them with repository code (`evaluate/exploitability.py` plus an exact-value print; the seeded `convergence.py` of F02-G03) before Chapter I cites any of them.
- [4]: only metadata was checked. Read the abstract before saying which number of players the result covers. The PPAD statement in the digest relies on [5] for the two-player case.
- [8]: the paper's procedure concerns conditional regrets and correlated equilibrium. The O(1/√T) rate of unconditional regret matching follows from Blackwell approachability [7] and is stated with a constant in [9], Theorem 4. Cite [9] for the constant.
- [10]: only the abstract was read ("a new tighter bound" for CFR). Read the bound before stating its form. Do not quote the √|𝓘| form the chapter prints (review F02-C03).
- [11]: "essentially weakly solved" and "played competitively by humans" come from a search snippet of the abstract. No computing-cost figures were checked.
- [13]: confirm the venue (EAAI 2013 Model AI Assignments) before listing it as a publication.
- [15] and [14]: content statements are taken from `lit_evaluation.md`.
- Chen & Ankenman, *The Mathematics of Poker* (2006): the half-street / full-street claims in the chapter were not checked. Do not cite without reading.
