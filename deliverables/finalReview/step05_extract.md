# Step 05 — Chapter I extract
**Feeds:** § 1.3 (primary). The two-player scope of the guarantees also serves § 1.5 (C2), and the evaluation notes serve § 1.6 (C3).

## Digest

Tabular CFR stores a cumulative regret for every information set and action and updates it on every iteration [1]. Memory and per-iteration work therefore grow with the game, and large games were solved only after abstraction, with the abstract solution mapped back to the full game [2]. Neural function approximation removes this dependence. A network maps an encoding of the information state to regrets, values or action probabilities, generalizes to states it has never visited, and has a size fixed by its parameters rather than by the game. The price is costlier iterations, noisy training targets, and guarantees that hold only up to the network's approximation error.

Several lines of work followed.

- **Regret-based methods.** Deep CFR [2] samples traversals with external sampling, stores sampled advantages in reservoir memories, and retrains an advantage network per player each iteration with linear-CFR weighting. A second network learns the average strategy. Single Deep CFR [3] replaces that network with the stored per-iteration networks, which lowers approximation error. Both require a perfect simulator of the game. DREAM [4] removes that requirement through outcome sampling with a learned baseline against the resulting variance. ESCHER [5] eliminates importance sampling altogether and reports advantages over DREAM and NFSP that widen as games grow. The line remains active [6].
- **Methods from reinforcement learning,** which avoid tree traversal. NFSP [7] approximates fictitious self-play: a DQN learns a best response and a supervised network averages past best responses. PSRO [8] generalizes fictitious play and double oracle to a meta-game over a growing population of policies; population-based league training also produced AlphaStar [9].
- **Methods that change the learning dynamics** of model-free self-play so that it approaches equilibrium instead of cycling: NeuRD [10], R-NaD, which reached human-expert level in Stratego without search [11], and magnetic mirror descent [12].
- **Search plus learning.** ReBeL [13] and Student of Games [14] learn value functions over public belief states and run CFR in depth-limited subgames at play time. ReBeL is superhuman in heads-up no-limit hold'em.

The belief that generic self-play reinforcement learning fails in imperfect-information games is now contested. In an exploitability comparison over five games with millions of information states, NFSP, PSRO, ESCHER and R-NaD did not outperform generic policy-gradient methods such as PPO and MMD [15].

The trade-offs differ by family:

- Regret-based methods stay closest to CFR's guarantees but are sample-hungry, and without a simulator their targets have high variance.
- Population and policy-gradient methods are model-free and cope with long horizons, but they converge slowly or need regularization and large populations.
- Search-based methods play strongest but spend computation at every decision.

Two properties are shared by all of these families. First, the equilibrium guarantees are two-player zero-sum: in other games DREAM converges only to an extensive-form coarse correlated equilibrium [4]. Second, every family optimizes worst-case performance and returns a fixed strategy; none is designed to adapt to the particular opponent it faces.

## Key sources
1. M. Zinkevich, M. Johanson, M. Bowling, C. Piccione, "Regret Minimization in Games with Incomplete Information," in *Advances in Neural Information Processing Systems 20*, 2007, pp. 1729–1736. [verified: NeurIPS PDF; the storage sentence was read]
2. N. Brown, A. Lerer, S. Gross, T. Sandholm, "Deep Counterfactual Regret Minimization," in *Proc. ICML*, 2019; arXiv:1811.00164. [verified: arXiv abstract + full text (Algorithm 1, § 5.3 Linear CFR, § 6)]
3. E. Steinberger, "Single Deep Counterfactual Regret Minimization," arXiv:1901.07621, 2019. [verified: arXiv v4 full text (Fig. 1 Leduc, Fig. 2 5-FHP, App. A); preprint, no venue found]
4. E. Steinberger, A. Lerer, N. Brown, "DREAM: Deep Regret minimization with Advantage baselines and Model-free learning," arXiv:2006.10410, 2020. [verified: arXiv abstract + full text § 5; preprint, no venue found]
5. S. McAleer, G. Farina, M. Lanctot, T. Sandholm, "ESCHER: Eschewing Importance Sampling in Games by Computing a History Value Function to Estimate Regret," in *Proc. ICLR*, 2023; arXiv:2206.04122. [verified: arXiv abstract + ML Anthology ICLR 2023 listing]
6. H. Xu, K. Li, H. Fu, Q. Fu, J. Xing, J. Cheng, "Deep (Predictive) Discounted Counterfactual Regret Minimization," in *Proc. AAAI*, 2026; arXiv:2511.08174. [verified: arXiv metadata + abstract; the AAAI acceptance is stated only in the arXiv comment]
7. J. Heinrich, D. Silver, "Deep Reinforcement Learning from Self-Play in Imperfect-Information Games," arXiv:1603.01121, 2016. [verified: arXiv abstract + Algorithm 1]
8. M. Lanctot, V. Zambaldi, A. Gruslys, A. Lazaridou, K. Tuyls, J. Pérolat, D. Silver, T. Graepel, "A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning," in *Proc. NIPS*, 2017; arXiv:1711.00832. [verified: arXiv abstract; NIPS 2017 per the arXiv comment]
9. O. Vinyals et al., "Grandmaster level in StarCraft II using multi-agent reinforcement learning," *Nature*, vol. 575, pp. 350–354, 2019. DOI 10.1038/s41586-019-1724-z. [verified: Crossref; league and architecture via DeepMind's AlphaStar blog; the Nature full text was not accessible]
10. D. Hennes et al., "Neural Replicator Dynamics: Multiagent Learning via Hedging Policy Gradients," in *Proc. AAMAS*, 2020, pp. 492–501; arXiv:1906.00190. [verified: arXiv abstract + AAMAS proceedings listing]
11. J. Perolat et al., "Mastering the game of Stratego with model-free multiagent reinforcement learning," *Science*, vol. 378, no. 6623, pp. 990–996, 2022. DOI 10.1126/science.add4679. [verified: Crossref + arXiv:2206.15378 abstract]
12. S. Sokota, R. D'Orazio, J. Z. Kolter, N. Loizou, M. Lanctot, I. Mitliagkas, N. Brown, C. Kroer, "A Unified Approach to Reinforcement Learning, Quantal Response Equilibria, and Two-Player Zero-Sum Games," in *Proc. ICLR*, 2023; arXiv:2206.05825. [verified: arXiv; ICLR 2023 header in the PDF]
13. N. Brown, A. Bakhtin, A. Lerer, Q. Gong, "Combining Deep Reinforcement Learning and Search for Imperfect-Information Games," in *Proc. NeurIPS*, 2020; arXiv:2007.13544. [verified: arXiv abstract + NeurIPS 2020 proceedings page]
14. M. Schmid et al., "Student of Games: A unified learning algorithm for both perfect and imperfect information games," *Science Advances*, vol. 9, no. 46, eadg3256, 2023. DOI 10.1126/sciadv.adg3256. [verified: Crossref + arXiv:2112.03178]
15. M. Rudolph, N. Lichtlé, S. Mohammadpour, A. Bayen, J. Z. Kolter, A. Zhang, G. Farina, E. Vinitsky, S. Sokota, "Reevaluating Policy Gradient Methods for Imperfect-Information Games," in *Proc. ICLR*, 2026; arXiv:2502.08938. [verified: arXiv v4 full text (abstract, § 1, conclusion)]
16. R. S. Sutton, A. G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018, § 11.3 "The Deadly Triad". [verified: author PDF, § 11.3 read]
17. M. Schmid, N. Burch, M. Lanctot, M. Moravčík, R. Kadlec, M. Bowling, "Variance Reduction in Monte Carlo Counterfactual Regret Minimization (VR-MCCFR) for Extensive Form Games Using Baselines," in *Proc. AAAI*, vol. 33, 2019, pp. 2157–2164. [verified: Crossref + arXiv:1809.03057; optional, source of DREAM's baselines]

## Gaps
- **G-a (C1, and the § 1.3 closing sentence): the equilibrium solvers do not adapt, and the adapters are not built on them.**
  - Every family above [2–15] outputs a fixed strategy (or meta-strategy) chosen for its worst case.
  - Consistent with `lit_gaps.md`: write "none of the landmark systems adapts to its opponents", not "nobody adapts". Adaptive transformer agents in Kuhn and Leduc exist (StratFormer, AlphaExploitem; § 1.4), but they are separate from the scalable solvers of this section.
- **G-b (C2): the guarantees are two-player zero-sum.**
  - ReBeL converges to Nash "in any two-player zero-sum game" [13].
  - DREAM converges to Nash only there, and to an extensive-form coarse correlated equilibrium otherwise [4].
  - The 2026 re-evaluation measures exploitability on two-player zero-sum games only [15].
  - None of these neural solvers therefore brings an equilibrium-quality or safety guarantee to the N-player games C2 targets. This matches `lit_gaps.md` (C2 open at the core).
- **G-c (C3): neural solvers are compared through exploitability, which needs an exact best response and a two-player zero-sum game.**
  - [15] had to implement exact exploitability for five larger games to compare methods at all.
  - [2, 3] report exploitability on small games plus head-to-head play.
  - Budgets are counted in different units (iterations, nodes touched, wall-clock time), and the choice changes the conclusion (see Own evidence).
  - Keep this narrow, as `lit_gaps.md` asks: do not claim "no cross-game evaluation exists". The claim is that exploitability-based comparison does not extend to N-player games or measure adaptation.

## Own evidence
- **Tabular beats neural where the table fits.** On OpenSpiel's Leduc at comparable wall-clock time, tabular external-sampling MCCFR reaches exploitability 0.097 (50 000 iterations, 68 s). Deep CFR with a 64×64 network reaches 1.70 (120 iterations × 40 traversals, 95 s). A uniform random policy scores 2.37.
  - Source: `implementation/step05/exploration/logs/day01_results.json`; 2.37 recomputed with OpenSpiel.
  - Caveat: one seed; 40 traversals per iteration against 1 500 in Steinberger's Leduc setup; the Deep CFR value equals the unpatched solver's value (see To verify). Use it at most as "a small-budget replication did not reproduce neural gains on Leduc".
- **NFSP needs orders of magnitude more data.** After 5×10⁴ episodes NFSP on Leduc is at 2.46, up from 2.35 at the start, i.e. no learning. OpenSpiel's own Leduc example uses 2×10⁷ episodes.
  - Source: `logs/day02_results.json`; installed `open_spiel/python/examples/nfsp_leduc_pytorch.py`.
  - Caveat: one seed, default hyper-parameters.
- **A silent failure (candidate for § 1.6, evaluation discipline).** OpenSpiel 1.6.12's PyTorch Deep CFR never trained its advantage networks (`if len(samples.info_state == 0)`), yet ran to completion with plausible output.
  - Source: `implementation/step05/exploration/findings.md`, `_openspiel_patch.py`.
  - Caveat: found independently and fixed upstream on 25 Mar 2026 (commit d499542d, release 1.6.13). Do not present it as a reported contribution.

## Figure candidate
None. The chapter's figures are generic architecture schematics (figs. 17, 18, 20), small-budget curves (figs. 19, 22, 23) or a figure reproduced from another paper (fig. 21). For § 1.3 a compact table serves better and sits outside the page budget. It would be a corrected Table 8: family × representative methods × needs a simulator? × guarantee (two-player zero-sum) × typical evaluation. The table needs the fixes in F05-C07, C11 and S04.

## To verify
- The Deep CFR numbers. The patched 64×64 run gives 1.700–1.706 at every checkpoint (30–120) and 1.704 at 40 iterations (day02). That matches the ≈ 1.69 the chapter reports for the *unpatched* solver. Re-run with OpenSpiel ≥ 1.6.13 (where the fix is upstream), ≥ 3 seeds and more traversals per iteration, and check that exploitability moves, before Chapter I cites any Deep CFR number from step 05.
- AlphaStar's spatial-ResNet and scalar-MLP encoders: confirm in the Nature Methods; only the transformer, LSTM core and autoregressive heads were verified (blog).
- [15] is ICLR 2026 per its arXiv v4 header; confirm the proceedings entry. Whenever it is cited, state its scope: two-player zero-sum, five games, exploitability.
- [3], [4] and [7] are arXiv-only; no peer-reviewed venue was found. [6]'s AAAI 2026 acceptance comes from the arXiv comment only.
- The chapter's "on the order of a million episodes" for NFSP on Leduc was not checked against Heinrich & Silver's Leduc figure.
- Fig. 21 is a screenshot of Steinberger (2019), Fig. 1. Check the arXiv licence before any reuse.
- A Deep CFR implementation for NLHE exists in `implementation/nlhe`. It is outside Chapter 5 and was not examined; it may be better own evidence for § 1.3.
