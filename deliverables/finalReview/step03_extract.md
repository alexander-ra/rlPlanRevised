# Step 03 — Chapter I extract
**Feeds:** § 1.2 (primary), § 1.6

## Digest

Counterfactual regret minimization (CFR) approximates a Nash equilibrium of a two-player zero-sum extensive-form game by minimizing regret separately at each information set. After T iterations, the exploitability of the average strategy is bounded by O(1/√T) [1]. Vanilla CFR traverses the whole tree on every iteration, so its cost per iteration grows with the size of the game.

Two families of refinements address this. CFR+ [2] resets negative cumulative regrets to zero, weights later iterations more heavily in the average strategy, and updates the players alternately. It keeps the O(1/√T) worst-case bound [3, 4], but in practice converges much faster. With full traversals it essentially solved heads-up limit Texas hold'em, a game with 3.19×10¹⁴ information sets [5]. A discounted CFR variant has since outperformed CFR+ in every game tested [6]. Monte Carlo CFR (MCCFR) [7] instead samples part of the tree on each iteration: chance and opponent actions in external sampling, and a single trajectory with importance weighting in outcome sampling. The sampled counterfactual values are unbiased, so the same regret bound holds with high probability. An external-sampling iteration costs O(√|H|) rather than O(|H|) in balanced games [7]. The price is variance, which control-variate baselines reduce substantially [8].

Which family is faster depends on game size and implementation. Neither removes the need for abstraction where no full traversal is possible, as in no-limit hold'em with up to 6.3×10¹⁶⁴ states [9]. Equilibrium is computable at scale only by combining sampling with abstraction.

For evaluation (§ 1.6), the standard measure is exploitability, the gain of a best response. NashConv sums that gain over the players [10]. Both can be computed exactly only in small benchmark games such as Kuhn and Leduc poker [11, 12]. Reported values must state the convention, since in two-player games the two differ by a factor of two.

## Key sources
1. M. Zinkevich, M. Johanson, M. Bowling, C. Piccione, "Regret Minimization in Games with Incomplete Information," in *Advances in Neural Information Processing Systems 20 (NIPS)*, 2007. [verified: NeurIPS proceedings listing + PDF link; bound read as quoted in [7] ("[1, Theorem 4]"); pages not checked]
2. O. Tammelin, "Solving Large Imperfect Information Games Using CFR+," arXiv:1407.5042, 2014. [verified: arXiv abstract, single author, no convergence theorem]
3. O. Tammelin, N. Burch, M. Johanson, M. Bowling, "Solving Heads-Up Limit Texas Hold'em," in *Proc. IJCAI*, 2015, pp. 645–652. [verified: IJCAI abstract page: "prove the theoretical soundness of CFR+ and its component algorithm, regret-matching+"; start page 645 checked, end page not]
4. N. Burch, M. Moravčík, M. Schmid, "Revisiting CFR+ and Alternating Updates," *J. Artif. Intell. Res.*, vol. 64, pp. 429–443, 2019. DOI 10.1613/jair.1.11370. [verified: Crossref + JAIR abstract (error in the original proof, bound recovered)]
5. M. Bowling, N. Burch, M. Johanson, O. Tammelin, "Heads-up limit hold'em poker is solved," *Science*, vol. 347, no. 6218, pp. 145–149, 2015. DOI 10.1126/science.1259433. [verified: Crossref + full-text PDF: 3.16×10¹⁷ states, 3.19×10¹⁴ infosets, "exhaustive iterations over the entire game tree", 1,579 iterations, 900 core-years, CFR+ "considerably less computation … than state-of-the-art sampling CFR"]
6. N. Brown, T. Sandholm, "Solving Imperfect-Information Games via Discounted Regret Minimization," in *Proc. AAAI*, vol. 33, no. 1, pp. 1829–1836, 2019. DOI 10.1609/aaai.v33i01.33011829; arXiv:1809.04040. [verified: Crossref + arXiv abstract ("outperforms CFR+ … in every game tested")]
7. M. Lanctot, K. Waugh, M. Zinkevich, M. Bowling, "Monte Carlo Sampling for Regret Minimization in Extensive Games," in *Advances in Neural Information Processing Systems 22 (NIPS)*, 2009, pp. 1078–1086. [verified: NeurIPS page + PDF text (Lemma 1 unbiasedness; Thms. 4–5 probabilistic bounds; external-sampling iteration cost O(√|H|); ε = 0.6); pages not checked]
8. M. Schmid, N. Burch, M. Lanctot, M. Moravčík, R. Kadlec, M. Bowling, "Variance Reduction in Monte Carlo Counterfactual Regret Minimization (VR-MCCFR) for Extensive Form Games Using Baselines," in *Proc. AAAI*, vol. 33, no. 1, pp. 2157–2164, 2019. DOI 10.1609/aaai.v33i01.33012157; arXiv:1809.03057. [verified: Crossref + arXiv abstract ("order of magnitude speedup", empirical variance down three orders of magnitude)]
9. M. Johanson, "Measuring the Size of Large No-Limit Poker Games," arXiv:1302.7008, 2013. [verified: arXiv PDF text (ACPC 2009–13 no-limit: 6.31×10¹⁶⁴ states, 6.37×10¹⁶¹ infosets; smallest ACPC no-limit format 1.38×10⁵¹ states)]
10. M. Lanctot et al., "OpenSpiel: A Framework for Reinforcement Learning in Games," arXiv:1908.09453, 2019. [verified: as recorded in `lit_evaluation.md` (PDF text: NashConv = Σᵢ δᵢ, exploitability = NashConv/n); also checked in the installed package, where `exploitability()` = NashConv/2 for Leduc]
11. F. Southey, M. Bowling, B. Larson, C. Piccione, N. Burch, D. Billings, C. Rayner, "Bayes' Bluff: Opponent Modelling in Poker," in *Proc. UAI*, 2005. arXiv:1207.1411. [verified: in the step-07 extract (arXiv abstract; introduces Leduc hold'em)]
12. H. W. Kuhn, "A Simplified Two-Person Poker," in *Contributions to the Theory of Games I*, Annals of Mathematics Studies 24, 1950, pp. 97–103. [unverified: bibliographic details from memory]
13. C. Browne et al., "A Survey of Monte Carlo Tree Search Methods," *IEEE Trans. Comput. Intell. AI Games*, vol. 4, no. 1, pp. 1–43, 2012. DOI 10.1109/TCIAIG.2012.2186810. [verified: Crossref; background for the "sample instead of enumerate" lineage, optional]

## Gaps
This chapter feeds the foundations section. Its gaps are mostly boundary conditions that §§ 1.4–1.6 build on, not gaps of their own.
- **G-a (C2): the equilibrium guarantee of the whole CFR family is a two-player zero-sum guarantee.** The average-strategy-to-Nash link and all the bounds above [1, 3, 4, 7] assume two-player zero-sum games. Multiplayer poker agents run the same machinery without that guarantee: Pluribus "plays a fixed strategy", and with three or more players equilibrium play guarantees nothing (`lit_evaluation.md`, [Brown 2019]). The "safe baseline" that C2 exploits from therefore has no worst-case meaning at N > 2. This is consistent with `lit_gaps.md`, where C2 is open at the core.
- **G-b (C1/C2, bridge, not a gap): solvers deliver a static anchor.** Every method here produces one fixed approximate equilibrium offline [5, 6]. Adaptation must be layered on top (§§ 1.4–1.5). Following `lit_gaps.md`, do not write "nobody adapts". Write that the solver literature optimizes convergence to equilibrium, not performance against a specific opponent.
- **G-c (C3, supporting illustration only): solver rankings do not transfer across game sizes.** MCCFR beats vanilla CFR by large margins on games of 10⁷–10⁸ histories [7]. Full-traversal CFR+ beat sampling CFR on limit hold'em [5]. On Leduc (≈10⁴ nodes) full traversal leads by 12–4,000× (Own evidence). This illustrates § 1.6's point that conclusions drawn in one game with one cost measure need a common protocol. `lit_gaps.md` shows cross-game *agent rating* already exists, so do not present it as a new gap.

## Own evidence
- **Leduc, equal 180-s budget, pure-Python implementations:**
  - CFR+ 2.6×10⁻⁵ (3,706 iterations)
  - vanilla CFR 4.4×10⁻³ (3,713)
  - external-sampling MCCFR 5.5×10⁻² (3.5 M)
  - outcome-sampling MCCFR 1.0×10⁻¹ (8.3 M)

  Exploitability = (BR₀+BR₁)/2. Source: `implementation/step03/models/timed_all_snapshots.json`; report_en § 5. Caveat: one run per algorithm (sampling seed 42), one machine, Python constants; toy game.
- **Measured convergence slopes (log-log):** external −0.50 and outcome −0.53 (T ≈ 10⁵–3.5×10⁶); vanilla CFR −0.84 (T = 97–3,713); CFR+ −1.74. Only MCCFR follows the O(1/√T) bound; the full-traversal methods beat it. Same source. Caveat: single runs, fitted over the ranges given.
- **Cross-validation:** at 500 iterations the custom solvers match OpenSpiel: vanilla 0.020 vs 0.022, CFR+ 8.6×10⁻⁴ vs 9.4×10⁻⁴. Source: report_en § 6. Caveat: one run.
- **Crossover estimate (use only as an illustration, if at all):** with the chapter's own model, sampling overtakes vanilla CFR at ≈ 1.1 M (external) / 2.4 M (outcome) nodes, 105× / 233× above Leduc. The summary's 2.1 M / 4.8 M and 210× / 466× are arithmetic errors (F03-C01). Caveat: the estimate assumes scale-free constants, a 1/√T vanilla rate and constant MCCFR cost per iteration. With O(√|H|) cost the same data give ≈ 10⁸ nodes (F03-C09).

## Figure candidate
None recommended. Chapter I's 1–3 figures are better spent on the problem statement (§§ 1.4–1.5). If § 1.2 needs one solver figure, use fig. 11 (Leduc exploitability vs wall-clock, 180 s; `implementation/step03/cfr/train_all_timed.py`, `plot_wallclock_chart`) after the fixes in F03-G05: legible type, no "0.0000" legend, BG labels.

## To verify
- Page ranges of [1] and [7], and the end page of [3]. The details of [12] (Kuhn 1950) are from memory.
- "CFR+ converges much faster in practice": do not write "O(1/T)" in Chapter I without a source that measures it. The digest avoids the rate.
- That Pluribus's blueprint used a Monte Carlo CFR variant: check in Brown & Sandholm, *Science* 2019, before naming MCCFR in G-a. The "fixed strategy" quote is verified in `lit_evaluation.md`.
- Leduc sizes: 936 information sets and 9,457 tree nodes, counted with OpenSpiel's `leduc_poker`. The chapter's "10,200" is its engine's per-traversal count (120 deals × 85). Cite 936 and, if needed, 9,457.
- Bowling et al. [5] used the *current* CFR+ strategy, not the average, as the HULHE solution. Do not say "CFR variants always output the average strategy".
- Metropolis (1987, *Los Alamos Science* 15) was located but not read. Needed only if Chapter I mentions the origin of "Monte Carlo"; otherwise drop it.
