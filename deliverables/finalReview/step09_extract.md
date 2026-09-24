# Step 09 — Chapter I extract
**Feeds:** § 1.5 (primary), § 1.4 (LOLA as dynamic opponent modelling)

## Digest

Beyond two-player zero-sum games, the anchors of equilibrium computation and safe exploitation disappear. In a Markov game [15] transitions and rewards depend on the joint action, so whenever the other agents learn, each agent faces a non-stationary environment [16, 20]. Independent learners, which treat the other agents as part of the environment [14], lose the convergence guarantees of single-agent RL. They also suffer coordination failures such as relative over-generalisation, illustrated by the climbing game [12, 13]. Even exact gradient dynamics in 2×2 games need not converge. When the only equilibrium is mixed, the strategies cycle, although their average payoffs converge to equilibrium values [11]. With three or more players CFR loses its guarantee of converging to a Nash equilibrium, and in three-player Leduc hold'em it empirically fails to reach one [18].

The field's structural responses fall into a few families.

- **Centralised training with decentralised execution** conditions a critic on global state and joint actions during training only [5]. Its main variants are counterfactual baselines [6], monotonic value factorisation [7] and PPO with a centralised value function, which is a simple and strong baseline [8]. The usual motivation, that a centralised critic lowers variance, holds for the critic's regression target but not necessarily for the policy gradient. With converged critics, a centralised critic yields policy updates with at least as much variance as decentralised ones [9].
- **Learned communication** lets cooperating agents exchange differentiable messages at execution time [10].
- **Policy-Space Response Oracles (PSRO)** lift iterated best response to populations. Each round a meta-game over the current policies is solved, and a best response to the resulting meta-strategy is added. PSRO generalises fictitious play and the double-oracle method [1, 2] and connects MARL to empirical game-theoretic analysis [3]. Its progress is measured as exploitability.
- **Learning with opponent-learning awareness (LOLA)** differentiates through the opponent's anticipated learning step [4]. In the iterated prisoner's dilemma it produces tit-for-tat cooperation where independent gradient learners defect, and in repeated matching pennies it converges to the equilibrium. LOLA thus treats the opponent as a learner rather than a fixed strategy. It is a form of dynamic opponent modelling, but it assumes a differentiable learning rule and two-player learning dynamics.

None of these families limits an exploiting agent's risk among more than two players: CTDE and communication target cooperation, PSRO equilibrium computation and evaluation, and LOLA a single learning opponent.

## Key sources
1. M. Lanctot, V. Zambaldi, A. Gruslys, A. Lazaridou, K. Tuyls, J. Pérolat, D. Silver, T. Graepel, "A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning," in *Proc. NIPS*, 2017. arXiv:1711.00832. [verified: arXiv abstract, incl. "generalizes … InRL, iterated best response, double oracle, and fictitious play"]
2. H. B. McMahan, G. J. Gordon, A. Blum, "Planning in the Presence of Cost Functions Controlled by an Adversary," in *Proc. ICML*, 2003, pp. 536–543. [verified: bibliographic listing via web search; not read]
3. K. Tuyls, J. Pérolat, M. Lanctot, E. Hughes, R. Everett, J. Z. Leibo, C. Szepesvári, T. Graepel, "Bounds and dynamics for empirical game theoretic analysis," *Auton. Agents Multi-Agent Syst.*, vol. 34, no. 1, art. 7, 2020. DOI 10.1007/s10458-019-09432-y. [verified: Crossref metadata only]
4. J. Foerster, R. Y. Chen, M. Al-Shedivat, S. Whiteson, P. Abbeel, I. Mordatch, "Learning with Opponent-Learning Awareness," in *Proc. AAMAS*, 2018, pp. 122–130. arXiv:1709.04326. [verified: arXiv abstract (IPD tit-for-tat, matching-pennies convergence) + Crossref]
5. R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, I. Mordatch, "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments," in *Proc. NIPS*, 2017. arXiv:1706.02275. [verified: arXiv abstract; venue not re-checked]
6. J. Foerster, G. Farquhar, T. Afouras, N. Nardelli, S. Whiteson, "Counterfactual Multi-Agent Policy Gradients," in *Proc. AAAI*, vol. 32, no. 1, 2018. DOI 10.1609/aaai.v32i1.11794. [verified: Crossref + arXiv abstract]
7. T. Rashid, M. Samvelyan, C. Schroeder de Witt, G. Farquhar, J. Foerster, S. Whiteson, "QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning," in *Proc. ICML*, 2018. arXiv:1803.11485. [verified: arXiv abstract]
8. C. Yu, A. Velu, E. Vinitsky, J. Gao, Y. Wang, A. Bayen, Y. Wu, "The Surprising Effectiveness of PPO in Cooperative, Multi-Agent Games," in *NeurIPS Datasets and Benchmarks Track*, 2022. arXiv:2103.01955. [verified: arXiv abstract]
9. X. Lyu, Y. Xiao, B. Daley, C. Amato, "Contrasting Centralized and Decentralized Critics in Multi-Agent Reinforcement Learning," in *Proc. AAMAS*, 2021, pp. 844–852. arXiv:2102.04402. Journal version: X. Lyu, A. Baisero, Y. Xiao, B. Daley, C. Amato, "On Centralized Critics in Multi-Agent Reinforcement Learning," *J. Artif. Intell. Res.*, vol. 77, pp. 295–354, 2023. DOI 10.1613/jair.1.14386. [verified: arXiv PDF text (variance result) + Crossref; JAIR abstract]
10. S. Sukhbaatar, A. Szlam, R. Fergus, "Learning Multiagent Communication with Backpropagation," in *Proc. NIPS*, 2016. arXiv:1605.07736. [verified: arXiv abstract]
11. S. Singh, M. Kearns, Y. Mansour, "Nash Convergence of Gradient Dynamics in General-Sum Games," in *Proc. UAI*, 2000, pp. 541–548. arXiv:1301.3892. [verified: arXiv PDF text (abstract; Fig. 1 limit cycles); pages from ACM DL listing]
12. C. Claus, C. Boutilier, "The Dynamics of Reinforcement Learning in Cooperative Multiagent Systems," in *Proc. AAAI*, 1998, pp. 746–752. [verified: AAAI/dblp listing via web search; not read]
13. L. Matignon, G. J. Laurent, N. Le Fort-Piat, "Independent reinforcement learners in cooperative Markov games: a survey regarding coordination problems," *Knowl. Eng. Rev.*, vol. 27, no. 1, pp. 1–31, 2012. DOI 10.1017/S0269888912000057. [verified: Crossref metadata only]
14. M. Tan, "Multi-Agent Reinforcement Learning: Independent vs. Cooperative Agents," in *Proc. ICML*, 1993, pp. 330–337. DOI 10.1016/B978-1-55860-307-3.50049-6. [verified: Crossref metadata only]
15. M. L. Littman, "Markov Games as a Framework for Multi-Agent Reinforcement Learning," in *Proc. ICML*, 1994, pp. 157–163. DOI 10.1016/B978-1-55860-335-6.50027-1. [verified: bibliographic listing via web search]
16. K. Zhang, Z. Yang, T. Başar, "Multi-Agent Reinforcement Learning: A Selective Overview of Theories and Algorithms," in *Handbook of Reinforcement Learning and Control*, Springer, 2021, pp. 321–384. arXiv:1911.10635. [verified: Springer listing via web search]
17. S. V. Albrecht, F. Christianos, L. Schäfer, *Multi-Agent Reinforcement Learning: Foundations and Modern Approaches*. MIT Press, 2024, Ch. 5 and 9. [verified: chapter titles on marl-book.com]
18. N. Abou Risk, D. Szafron, "Using Counterfactual Regret Minimization to Create Competitive Multiplayer Poker Agents," in *Proc. AAMAS*, 2010, pp. 159–166. [verified: AAMAS 2010 preprint PDF read; pages from listing]
19. L. Kraemer, B. Banerjee, "Multi-agent reinforcement learning as a rehearsal for decentralized planning," *Neurocomputing*, vol. 190, pp. 82–94, 2016. DOI 10.1016/j.neucom.2016.01.031. [verified: Crossref metadata only]
20. P. Hernandez-Leal, M. Kaisers, T. Baarslag, E. Munoz de Cote, "A Survey of Learning in Multiagent Environments: Dealing with Non-Stationarity," arXiv:1707.09183, 2017. [verified in the step-07 review (arXiv abstract); not re-checked here]
21. H. W. Kuhn, "Extensive Games and the Problem of Information," in *Contributions to the Theory of Games II*, 1953, pp. 193–216. DOI 10.1515/9781400881970-012. [verified: Crossref]
22. J. Robinson, "An Iterative Method of Solving a Game," *Ann. Math.*, vol. 54, no. 2, pp. 296–301, 1951. DOI 10.2307/1969530. [verified: Crossref]

## Gaps
- **G-a (C2): the MARL method families offer no loss bound for an exploiting agent among more than two players.**
  - What the families target: CTDE [5–8] and communication [10] target cooperation; PSRO [1, 3] targets equilibrium computation and population evaluation.
  - Where the anchor goes: with N > 2, CFR's Nash guarantee disappears [18] and so does the minimax value.
  - How this relates to `lit_gaps.md` (C2), which it is consistent with and narrows:
    - N-player safety *notions* do exist (equal share with impossibility results [Ge 2025], team-maxmin [Celli & Gatti 2018]), so the gap is not "no N-player safety concept".
    - The gap is that no method exploits sub-optimal opponents in N-player imperfect-information games while bounding its loss relative to a baseline.
- **G-b (C1): opponent-learning awareness is shown in differentiable two-player games only.** LOLA [4] is demonstrated on the IPD, matching pennies and a grid-world social dilemma. It assumes the opponent follows a (known or modelled) gradient rule. In the sources read, it is not combined with an explicit static model of the opponent, and it is not applied to imperfect-information card games. Follow-ups exist (e.g. POLA, Zhao et al., NeurIPS 2022, found in Crossref but not read), so the gap must be checked before it is claimed.
- **G-c (C3): PSRO evaluates by distance to equilibrium, not by adaptation.** The meta-game [1, 3] ranks a population by the exploitability of its meta-Nash mixture. It says nothing about how fast an agent adapts to, or recovers from, an opponent's change within a match. This is consistent with `lit_gaps.md` C3: population ratings exist, but adaptation within a match is not measured.
- **G-d (C1, C2): "centralised critic = lower variance" is not a safe premise.** Lyu et al. [9] prove the policy-gradient variance can increase with a centralised critic. Any thesis design that relies on a centralised critic to stabilise learning of N-player adaptation must measure it rather than assume it.

## Own evidence
- **PSRO with an exact best-response oracle:** Kuhn exploitability 0.917 → ~2×10⁻¹⁶ in 6 rounds; Leduc 4.75 → 2.16 after 20 rounds. The Leduc decline is not monotone: it peaks at 6.83 in round 1 and oscillates until round 7.
  - Source: `implementation/step09/implementation/results/scale_results.json` (`psro`).
  - Caveat: pure-strategy population, deterministic single run, toy games.
- **Last iterate vs average:** in fictitious-play self-play on Kuhn, the average strategy's NashConv falls 0.24 → 0.031 in 200 iterations while the last iterate stays in 0.33–0.83.
  - Source: `exploration/figures/selfplay_vs_nash.json`.
  - Caveat: Kuhn only.
- **Independent learners in Matching Pennies do not converge:** NashConv is 1.44–1.84 across 5 seeds (softmax learners). With a fixed step of 0.1, gradient ascent spirals outward (radius 0.30 → 0.48).
  - Source: `scale_results.json` (`matrix`), `exploration/figures/nonstationarity_demo.json`.
  - Caveat: the outward spiral is a finite-step effect (see To verify).
- **A better critic is not coordination:** the centralised critic's fit residual is 3.2×10⁻¹¹ vs 0.077 for an independent one. Yet on the climbing game no method reaches the optimum 11 (IL 7, MAPPO 7, a COMA-style "MADDPG" 5).
  - Source: `scale_results.json` (`coop`).
  - Caveat: one seed, one-step and stateless tasks. The residual is not policy-gradient variance [9].
- **LOLA:** per-step return on the IPD rises from 1.04 (naive) to 2.82 (LOLA). With the look-ahead rate set to zero, LOLA's gradient reduces exactly to the naive one.
  - Source: `scale_results.json` (`lola`).
  - Caveat: memory-1 IPD with exact gradients, one seed; a replication of [4], not new evidence.

## Figure candidate
None recommended. The chapter's diagrams are textbook material (the PSRO loop, the CTDE architecture), and the results figures are toy replications. If § 1.5 needs a map of the field, fig. 46 (`deliverables/reports/step09/summary/make_methods_spectrum_figure.py`, methods on centralisation × competitiveness axes) is the only candidate. It would first need the fixes in F09-G03 (overlapping boxes, IL placement, type size), and it should add where the thesis sits: competitive, N-player, adaptive.

## To verify
- [5] and [19]: that MADDPG uses the phrase "centralized training with decentralized execution" and that Kraemer & Banerjee are the appropriate origin of the CTDE framing. Only metadata or the abstract was read. The alternative, Oliehoek et al. 2008 (JAIR), was not checked.
- [9]: the variance theorem assumes converged on-policy value functions. State this condition whenever the result is cited.
- [4]: the "dynamic opponent modelling" label is this corpus's reading of LOLA, not the paper's wording. In the paper, "opponent modelling" refers only to the variant that learns the opponent's parameters (the grid-world experiment).
- [11]: the limit-cycle (orbit) statement holds for infinitesimal gradient ascent. Chapter I must not present the step-09 outward spiral as evidence that non-stationarity worsens with more training (F09-C02).
- [2], [12]–[15]: existence and metadata only; not read.
- [17]: only chapter-level titles were checked; confirm the section coverage (CTDE, value decomposition, PSRO) before citing chapters.
- "There is no single game value for N > 2": standard, but give it a textbook source (e.g. Shoham & Leyton-Brown 2008, verified in the step-07 extract) rather than leaving it unsourced.
- The "MADDPG" numbers in step 09 come from a COMA-style variant (`implementation/step09/implementation/maddpg.py`). Do not cite them as MADDPG results.
- G-b: check LOLA's follow-ups (SOS, COLA, POLA, M-FOS) before claiming that nothing extends opponent-learning awareness to imperfect-information or N-player settings.
