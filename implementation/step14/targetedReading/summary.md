# Chapter 14 — Targeted reading (Phase 3)

Five sources from the plan (L249–314), three supplementary ones that the gap analysis
(`deliverables/finalReview/lit_evaluation.md`) makes necessary, and two corrections to the plan.
How each was checked: AIVAT, α-Rank and the repeated-RPS benchmark were read in the arXiv PDFs
(text extracted); VasE, ISMCTS-BR and Rowland et al. from their arXiv abstracts plus
`lit_evaluation.md`'s verified entries; the others from `lit_evaluation.md` / `lit_gaps.md`.

**Corrections to the plan.** AIVAT is Burch, Schmid, Moravčík, Morrill & Bowling, *AAAI 2018*
(arXiv v2, January 2017, lists the first four), not "Burch, Johanson & Bowling (2019)".
"Re-evaluating evaluation" is *NeurIPS 2018*, not 2019. The plan's AIVAT validation line
("should match the exact exploitability") mixes two quantities: AIVAT estimates a head-to-head
expected value.

---

## 1. Timbers et al. (2022) — Approximate exploitability: learning a best response

Timbers, F., Bard, N., Lockhart, E., Lanctot, M., Schmid, M., Burch, N., Schrittwieser, J.,
Hubert, T. & Bowling, M. *IJCAI 2022*; arXiv:2004.09677.
**Role:** the bridge from exact exploitability (Kuhn, Leduc) to games too large to traverse.

**Key idea.** ISMCTS-BR, a search-based deep-RL algorithm, *learns* a best response to a fixed
agent; the value it achieves estimates the agent's worst case. It is demonstrated in several
two-player zero-sum games against several agents, including AlphaZero-based ones (abstract).

**Key math.** The value of any strategy against the target is at most the best-response value,
so a learned response gives a **lower bound** on exploitability. (This inequality is the
definition of a best response; the abstract speaks of "approximating worst-case performance".)

**What this chapter did with it.** A tabular Monte-Carlo learner stands in for ISMCTS-BR on Kuhn
and Leduc, where the exact value is known (`run_approx_br.py`): on Leduc it reaches 71–98 % of
the exact exploitability after 10⁵ hands per seat and is *negative* after 10³ hands for two of
six targets (Rock, Maniac).

## 2. Lanctot et al. (2023/2025) — Evaluating agents using social choice theory (VasE)

Lanctot, M., Larson, K., Bachrach, Y., Marris, L., Li, Z., Bhoopchand, A., Anthony, T., Tanner,
B. & Koop, A. arXiv:2312.03121 (v4, June 2025; no venue listed — cite as arXiv).
**Role:** the axiomatic population ranking.

**Key idea.** Each task (or each match) is a voter that ranks the agents; the evaluation is an
election. The authors recommend **maximal lotteries**, which "satisfy important consistency
properties relevant to evaluation", are polynomial in the data and identify game-theoretic
cycles; VasE is reported more robust than Elo and Nash averaging and predicts outcomes better
than Elo in a seven-player game (abstract).

**Key math.** With margin matrix D (D_ij = voters preferring i to j minus the reverse), a
maximal lottery p satisfies pᵀD ≥ 0: it is the maximin strategy of the symmetric zero-sum game
D, one LP. The iterative variant (IML) ranks by peeling off support levels.

**Math Flag, worked (agent's derivation, checked by `population.maximal_lottery`).** Three
agents A, B, C and five voters: A≻B≻C twice, B≻C≻A twice, C≻A≻B once. Margins: A over B +1,
B over C +3, C over A +1 — a cycle. For a 3-cycle with margins a (A≻B), b (B≻C), c (C≻A) the
lottery is p ∝ (b, c, a) = (3, 1, 1)/5: every column of pᵀD is zero (for A: 0.6·0 − 0.2·1 +
0.2·1 = 0). A gets the most weight because it beats B, which beats C by the largest margin.

## 3. Rowland et al. (2019) — Multiagent evaluation under incomplete information

Rowland, M., Omidshafiei, S., Tuyls, K., Pérolat, J., Valko, M., Piliouras, G. & Munos, R.
*NeurIPS 2019*; arXiv:1909.09849. **Role:** confidence in rankings.

**Key idea.** Payoffs estimated from noisy matches make rankings noisy. The paper derives
sample-complexity guarantees for confidently ranking agents, links match-outcome uncertainty to
ranking uncertainty, and proposes adaptive sampling algorithms with correctness guarantees;
experiments include Bernoulli games, a soccer meta-game and Kuhn poker (abstract).
**What this chapter did:** bootstrap rank stability over seeds (`run_population.py`): α-Rank at
α = 10 keeps its Kuhn winner in 22 % of resamples, Elo in 100 %.

## 4. Burch et al. (2018) — AIVAT

Burch, N., Schmid, M., Moravčík, M., Morrill, D. & Bowling, M. "AIVAT: A New Variance Reduction
Technique for Agent Evaluation in Imperfect Information Games." *AAAI 2018*; arXiv:1612.06915.
**Role:** Layer 3, and the estimator that makes per-segment adaptation measurable.

**Key idea.** Combine MIVAT-style control variates for chance events with control variates for
the *actions of agents whose strategy is known*, plus imaginary observations over the known
agent's private cards. Any value function can be used; the estimate stays unbiased.

**Key math (paper Eq. 1, Lemma 1, Theorem 1).** AIVAT(z) = Σ_{z'∈W} π_a(z') v(z') / Σ π_a(z')
+ Σ_H k_H(z), with k_H(z) = Σ_a Σ_{h∈H} π_a(h·a) u_h(a) / Σ_{h∈H} π_a(h) − Σ_{h∈H} π_a(h·a_O)
u_h(a_O) / Σ_{h∈H} π_a(h·a_O). Lemma 1: E[k_H] = 0 for every part H; Theorem 1: the sum has
expectation 0. Assumptions: the partition keeps the unknown players' reach constant inside a
part, no part contains a history and its prefix, and action sets align.

**Headline numbers (paper, Leduc, 100 000 games).** Self-play with both strategies known: SD cut
by "a little less than 99.9 %"; one-sided: 99.8 %. Nash vs a call/raise agent: 48–75 % SD
reduction, against 25 % for MIVAT with imaginary observations. HUNL: a bit more than 68 %.

**Math Flag, worked.** Unbiasedness is Lemma 1: sum over the terminals below H, write
π = π_a·π_o, and the two terms collapse to the same Σ_a Σ_h π(h·a) u_h(a). *What the
implementation taught:* the known player's **own** card deal must get no correction term (the
paper's Fig. 1 has none); keeping one double-counts that card's luck. The check "both strategies
known plus a perfect value function gives zero variance" failed until that term was removed
(EXECUTION_NOTES, surprise 2).

## 5. Omidshafiei et al. (2019) — α-Rank

Omidshafiei, S., Papadimitriou, C., Piliouras, G., Tuyls, K., Rowland, M., Lespiau, J.-B.,
Czarnecki, W. M., Lanctot, M., Pérolat, J. & Munos, R. *Scientific Reports* 9, 9937;
arXiv:1903.01373. **Role:** the evolutionary population ranking.

**Key idea.** Build a Markov chain over monomorphic populations; a single mutant fixates with a
probability set by the Fermi rule with ranking intensity α and population size m; the
stationary distribution is the ranking. It runs in polynomial time in the number of pure
profiles, "whereas computing a Nash equilibrium for a general-sum game is known to be
intractable"; the link to the MCC solution concept holds for large α (abstract).

**Key math (paper Eqs. 4–9).** Fixation probability ρ = (1 − e^{−α Δf}) / (1 − e^{−m α Δf})
(1/m when Δf = 0); transition C[s → s'] = η ρ with η = 1 / Σ_k(|S_k| − 1).

**Math Flag, worked (α = 1, m = 50, RPS, single population with OpenSpiel's local selection
model).** Δf = ±2, so ρ(Paper invades Rock) = (1 − e^{−2}) / (1 − e^{−100}) = 0.8647 and the
reverse ≈ 0. With η = 1/2: C[R→P] = C[P→S] = C[S→R] = 0.432, self-loops 0.568 — a rotating chain
whose stationary distribution is (1/3, 1/3, 1/3), matching OpenSpiel's `alpharank.compute` to
1e-16.

## Supplementary

- **Balduzzi, D., Tuyls, K., Pérolat, J. & Graepel, T. (2018). "Re-evaluating evaluation."
  *NeurIPS*.** Elo is meaningless in cyclic games and is inflated by adding copies of beaten
  agents; **Nash averaging** (skill against the maximum-entropy Nash of the meta-game) is
  invariant to redundant agents. Reproduced here: 0–8 copies of the weakest bot widen the Elo
  gaps of the exploiters over Nash by 15–29 points, and move Nash-averaged skills by < 6e-6.
- **Lanctot, M. et al. (2023). "Population-based evaluation in repeated rock-paper-scissors as a
  benchmark for multiagent reinforcement learning." *TMLR*.** 43 bots, K = 1000 throws;
  PopulationReturn = mean return against a bot drawn from the population; WithinPopExpl =
  maximum over population bots of their return against the agent; AggregateScore =
  PopulationReturn − WithinPopExpl. Within-population exploitability reached 75.2 % of an
  externally learned exploiter's on average (§2.3). The nearest precedent for C3.
- **Balduzzi et al. (2019, ICML)** — the transitive + cyclic decomposition; **Czarnecki et al.
  (2020, NeurIPS)** — the "spinning top" geometry. Cite both.

## Synthesis

The sources split into worst-case tools (exploitability, ISMCTS-BR), population tools (Elo,
Nash averaging, α-Rank, VasE) and confidence tools (AIVAT, Rowland et al.). Each is exact about
its own question and silent about the others; only the RRPS benchmark joins return and
robustness, and only for one simultaneous-move two-player game. None of them models an agent
whose policy changes during the match: population methods need a fixed payoff entry, AIVAT
needs a known strategy per hand, and exploitability is defined for a fixed strategy. The
chapter's protocol treats the adaptive agent as a *sequence* of policies, which every one of
these tools can score exactly in small games — and which shows where each breaks.

## Verify when you read it

- ISMCTS-BR: which games, and how close the learned response gets to exact values where known.
- VasE: the axioms that single out maximal lotteries, and the seven-player game used.
- Rowland et al.: the exact form of the sample-complexity bound (it depends on payoff gaps).
- AIVAT: the AAAI version's author list and any change from arXiv v2's numbers.

## Key takeaways for the final summary

- Learned best responses are lower bounds; their budget must be reported (ISMCTS-BR).
- Maximal lotteries and Nash averaging are both equilibria of a meta-game — both give zero weight
  to an agent that beats only weak opponents.
- AIVAT's unbiasedness holds for any value function; its variance does not, and the known
  player's own deal must not be corrected twice.
- α-Rank's ranking depends on α by construction; swept from 0.01 to 100 it names three different
  winners on each two-player zoo.
