<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->
---
title: "Chapter 14 Summary — Evaluation Frameworks and Exploitability Metrics"
subtitle: "Research on the possibilities for applying Artificial Intelligence in computer games"
author: "Alexander Andreev"
date: "September 2026"
lang: en
vars:
  research_focus: "Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments"
---

# Chapter 14 — Evaluation Frameworks and Exploitability Metrics

This chapter is about how to evaluate game-playing agents that **adapt**: agents that watch their
opponents and change their play. It builds the standard toolkit — exact exploitability, population
rankings and variance reduction — validates it, and uses it to measure what it misses. **All
experimental numbers were measured** on three small poker games (two-player Kuhn and Leduc,
three-player Kuhn) and Chapter 11's four-player So Long Sucker, *exactly* wherever the game allows;
where a run contradicted my expectation, both are kept.

**Where this sits in the thesis.** This chapter is Contribution 3 (evaluation methodology). The
September 2026 literature check narrowed that contribution: combining exploitability,
population ranking and confidence is not new on its own — a benchmark for repeated
rock–paper–scissors already scores return and exploitability together, for one game[^rrps]. What
no protocol found reports together is (a) the **gain** against a sub-optimal population, (b) the
**speed** of adaptation and the **recovery** after an opponent switches, and (c) the **worst
case**, or with more than two players a coalition-aware substitute — each with confidence bounds,
applied unchanged across several imperfect-information games. The chapter builds such a protocol
and shows, on concrete agent zoos, where the existing measures break. It is also the yardstick for
Chapter 7's adaptive agents (Contribution 1) and for the question Chapter 8 left open — what
"safe" can mean with three players (Contribution 2).

---

## Why evaluating an adaptive agent is hard

There are two ways to grade a game-playing agent. The first asks *how badly can it be beaten?*
In a two-player zero-sum game the answer is **exploitability**: how far a best-responding
opponent can push the agent below the game value. The second asks *how well does it do against
the opponents it will meet?*, answered by head-to-head win rates and ratings from Elo[^elo1978] to
Nash averaging[^balduzzi2018], α-Rank[^alpharank] and voting-based evaluation[^vase]. The two are
known to disagree: bots indistinguishable head-to-head were about 1,300 mbb/game apart in
exploitability[^deepstack], and the computer poker competition used two winner rules[^bard2013].

An adaptive agent makes the disagreement structural. It leaves equilibrium on purpose, so
exploitability can only count against it however much it gains, and its payoff depends on how
long it plays and what it has seen, so it has no single entry in the payoff matrix that population
rankings assume. With three or more players the worst case changes meaning: NashConv measures
distance from *an* equilibrium[^openspiel], and in three-player Kuhn a player can pass utility to a
second at the third's expense while everyone plays equilibrium strategies[^szafron2013]. The only
coalition worst case the literature check found is the team-maxmin value[^celli2018] — a solution
concept, not an evaluation protocol.

A picture helps. Hiring a negotiator, one reference says "the worst deal a ruthless
counterpart could force on this person", another "how they did in their last twenty
negotiations". Neither says how fast they read a new counterpart, whether they notice a change of
tactics, or whether someone who acts naive and then turns can play them — nor, with three parties,
what happens when the other two coordinate. The chapter's protocol asks all of these, with error
bars.

---

## The framework: three layers and a fourth question

**Layer 1** is the worst case: exact exploitability in small games, a learned best response in
large ones[^timbers2022]. **Layer 2** is the population: round-robin payoffs, Elo, Nash averaging,
the meta-Nash (Chapters 9–10), α-Rank, VasE's maximal lotteries and the "spinning top"
decomposition[^balduzzi2019][^czarnecki2020]. **Layer 3** is confidence: seeds, duplicate dealing
and AIVAT[^aivat]. The fourth question is the chapter's own: how an adaptive agent behaves *over
time*.

![The joint protocol. A bot zoo, including switching and teaching opponents, plays fixed-seat duplicate matches over several seeds; each hand is scored by three estimators and four readouts are reported together.](protocol.png)

Everything rests on one exact engine. Each game is enumerated once from OpenSpiel's definition,
so a strategy is a vector and its expected payoff, best response and exposure are matrix
operations (Leduc: 9,457 nodes, 468 information sets per player, built in 0.04 s). An adaptive
agent is a *sequence* of strategies, one per refit, each scored exactly. The engine reproduces
OpenSpiel, Chapter 3 and Chapter 7 to within rounding (`validation.json`).

The four readouts are defined as follows (chips per hand throughout).

- **Gain**: the agent's expected payoff minus the equilibrium blueprint's, against the same
  opponent in the same seat; its **capture** divides this by what the exact best response would
  gain.
- **Speed and recovery**: *h50* is the first hand at which the capture reaches one half and stays
  there on average over the next 100 hands; *r50* is the same count after the opponent switches.
  The adaptive agents refit every 50 hands, so both are resolved to 50 hands.
- **Exposure**: for two players, how far below the game value v* a best responder could push the
  policy in force — exploitability applied to the current policy rather than to a fixed agent;
  plus the realised loss under a white-box teaching attack. For three players, the **coalition
  value**: the least the other two can hold the agent to with coordinated strategies.
- **Confidence**: 95 % intervals over seeds, with the estimator named. There are three:
  raw chips; AIVAT with the agent's own strategy known; and the *policy-exact* expected payoff of
  the two policies in force, available only when both are bots.

The zoos have 16 agents on Kuhn and 12 on Leduc: the **equilibrium** blueprint (OpenSpiel's
CFR+); Chapter 7's **rule-based types** (AlwaysPass, AlwaysBet, TightPassive, LooseAggr, Threshold
on Kuhn; CallingStation, Maniac, Rock, LoosePassive on Leduc) plus Random; on Kuhn, three
**strategies extracted from language models** in Chapter 12 (Qwen2.5-7B-Instruct, gpt-oss-20b and
OpenThinker3-7B, read from action-token log-probabilities; quantisation not recorded;
OpenThinker3-7B is a weak stand-in, with 34 % of its mass unmappable to an action); a
**specialist**, a static best response to one weak type; and five **adaptive agents** combining
Chapter 7's models with Chapter 8's responses:

- *TypeBR*: a Bayesian posterior over the types, best-responded to;
- *DirBR*: the continuous Dirichlet model, best-responded to;
- *DirBR-CP*: DirBR with Chapter 7's change-point reset;
- *RNR(0.5)*: the continuous model inside a restricted Nash response with p = 0.5[^johanson2007];
- *BestEq*: the best equilibrium against the model — the most it can earn while never falling
  below v*, Ganzfried and Sandholm's best-equilibrium baseline[^ganzfried2015].

Chapter 8's constraint-generation loop for the last two did not converge on full Leduc. Here they
are solved with the sequence-form dual linear program[^kmvs1996][^vonstengel1996]: one LP per method solves full Leduc in
0.02–0.04 s and reproduces Chapter 8's Kuhn results.

---

## Layer 2 — rankings disagree, in predictable ways

Each pair plays 2,000-hand matches in both seats with duplicate cards over 10 seeds (stationary
pairs exactly); Elo is fitted to the probability of finishing a 100-hand session ahead
(`population_{kuhn,leduc}.json`).

![Rank of every Leduc agent under eight methods (1 = best). RNR(0.5) and DirBR lead Elo, population return and RRPS; BestEq and Nash lead exploitability and Nash averaging.](../figures/ranks_leduc.png)

The rankings fall into two camps. **Exploitability, Nash averaging and VasE** favour agents that
never lose: on Leduc the meta-game's maximum-entropy Nash mixture is BestEq 0.88, Nash 0.11,
TypeBR 0.01, and RNR(0.5) and DirBR get zero weight despite the highest population return (+0.807
and +0.890 chips/hand). **Elo, population return and the RRPS score** favour agents that beat many
opponents: Elo on Leduc is RNR(0.5) 1892, DirBR 1848, BestEq 1779, Nash 1763. The Kendall
correlation between the Elo and exploitability rankings is 0.45 on Kuhn and 0.36 on Leduc. For an
exploiting agent the two questions have opposite answers, and a single ranking silently picks one.

Three more predicted failure modes appear. **Clones inflate Elo.** Adding up to eight copies of
the weakest bot widens DirBR's Elo lead over Nash from +166 to +181 points on Kuhn and from +84 to
+113 on Leduc, while no Nash-averaged skill moves by more than 6e-6[^balduzzi2018]. **α-Rank depends on α.** As α grows from 0.01
to 100, three different agents lead on Kuhn (DirBR, RNR(0.5), Nash) and four on Leduc (DirBR,
RNR(0.5), BestEq, Nash). **The horizon matters.** Truncating the same runs to 100 hands puts
TypeBR first in Elo on Kuhn and the *static* specialist BR-Rock first on Leduc; from 300 hands on,
DirBR-CP, then DirBR (Kuhn) and RNR(0.5) (Leduc) lead. An adaptive agent's place in a meta-game is
only defined once the match length is fixed.

![α-Rank mass of the main agents as the selection pressure α grows; the leader moves from DirBR through RNR(0.5) to Nash on Kuhn, and through BestEq to Nash on Leduc.](../figures/alpha_sweep.png)

Ranking confidence is uneven too: over 200 seed resamples Elo keeps its Kuhn winner every time,
α-Rank at α = 10 only in 22 %, because near-tied equilibrium agents make its top unstable[^rowland2019].
And an arena-style rating misorders the LLM-derived strategies: Elo puts the Qwen2.5-7B strategy
7th of 16 and the Threshold bot 10th, although Qwen's exploitability is 0.179 chips/hand against
Threshold's 0.118 (Chapter 12's 0.357 is NashConv; here NashConv/2). LLM arenas that rank by
rating alone inherit this.

---

## Layer 3 — confidence, and what AIVAT taught

AIVAT corrects each hand's result with control variates for chance events and for the actions
of any player whose strategy is known, plus "imaginary observations" over that player's other
possible private cards; the estimate is unbiased for any value function[^aivat]. Tabulating the
AIVAT value of every terminal once per strategy gives the estimator's *exact* mean and variance.

The first implementation had a real bug, and the check that caught it is worth keeping: with
both strategies known and a perfect value function, AIVAT's variance must be zero. It was not:
the known player's own card deal had received a chance-correction term, although the imaginary
observations already average over that card, so its luck was counted twice. Removing it restored
exactly zero variance and made the realistic version, with only the agent's own strategy known,
better than chance-only correction everywhere.

With blueprint self-play values as the value function, the plan's targets — variance divided by
at least 5 on Kuhn and 10 on Leduc — are met for 18 of 20 Kuhn pairs (median factor 48) and 7 of 12
Leduc pairs (median 12.2); the misses are opponents the self-play values predict badly. AIVAT
cannot be used for humans, whose strategy is unknown[^pluribus], and its value function must be
fixed before the data are seen[^kim2026] — here, the blueprint.

![Share of the attainable gain estimated in 100-hand windows from raw chips, AIVAT and exact policy values, for DirBR against LooseAggr (Kuhn) and Maniac (Leduc); mean ±1 SD over 20 matches.](../figures/fm5_estimators.png)

Measuring *adaptation* rather than a final win rate raises the price sharply, because the quantity
of interest lives in short windows. To estimate the capture of one 100-hand window to ±0.25 with
95 % confidence, the median agent–opponent pair needs 3,383 hands with raw chips on Kuhn and 379
with AIVAT; on Leduc, 1,313 and 354. On real data, the 10,000 released Pluribus hands (Chapter 13)
give a raw win rate of −70.9 ± 172.8 mbb/hand (95 % interval), against 48 mbb/game with a standard
error of 25 with AIVAT and Pluribus's strategy[^pluribus]. A third party holding only the hand
histories cannot reach significance on the win rate, let alone on how fast the agent adapts.

---

## The joint protocol on Kuhn and Leduc

Seven agents were run against every sub-optimal stationary zoo member, three opponents that switch
at hand 1,000 of 2,000, and three teaching attacks, each for 10 seeds in both seats
(`adaptation_{kuhn,leduc}.json`). A teaching attack plays a bait strategy until hand 1,000 and
then the exact best response to the agent's current policy, refreshed every 50 hands — the "taught
then exploited" scenario behind adaptation safety[^ge2024].

| Agent | Gain K | Exposure K | Teach loss K | Gain L | Exposure L | Teach loss L |
|---|---:|---:|---:|---:|---:|---:|
| Nash | 0 | 0.000 | 0.000 | 0 | 0.000 | 0.000 |
| BestEq | +0.020 | 0.000 | 0.000 | +0.047 | 0.000 | 0.000 |
| RNR(0.5) | +0.210 | 0.090 | 0.045 | +0.797 | 0.264 | 0.179 |
| DirBR | +0.273 | 0.338 | 0.246 | +0.988 | 2.461 | 1.241 |
| DirBR-CP | +0.230 | 0.305 | 0.199 | +0.441 | 2.459 | 1.757 |
| TypeBR | +0.229 | 0.352 | 0.337 | +0.961 | 1.885 | 2.000 |

: Gain against the sub-optimal population, mean exposure of the policy in force, and loss below v* after a teaching attack, on Kuhn (K) and Leduc (L), chips per hand. 95 % intervals on the gains are at most 0.007.

![Gain over the Nash blueprint against the sub-optimal population, against exposure. Error bars are 95 % intervals over 10 seeds and are smaller than the markers.](../figures/gain_exposure.png)

Read together, the numbers separate agents that every single ranking conflates. **BestEq** is
safe by construction and gains almost nothing: 0.020 and 0.047 chips/hand. **RNR(0.5)** gains 10 to
17 times as much at an exposure of 0.090 on Kuhn and 0.264 on Leduc, and loses at most 0.274
chips/hand to any teaching attack. **DirBR** gains a little more still (0.988 on Leduc) but at an
exposure of 2.46 — almost thirty times the game value — and a teaching attacker takes 1.0–1.5
chips/hand back. Exploitability ranks BestEq and Nash first; Elo ranks them the other way. Only
the pair (gain, exposure) shows that RNR(0.5) buys most of the gain for a small, measured risk.
Exposure is also the upper envelope of the teaching loss: an attacker in step with the refits
takes exactly the current policy's exposure, and the measured losses equal it for every agent
except DirBR-CP, whose resets leave the attacker's response stale.

![Top: gain over Nash when the opponent switches at hand 1,000. Bottom: expected payoff minus the game value under a teaching attack (bait until hand 1,000, then the exact best response, refreshed every 50 hands).](../figures/switch_teach.png)

Speed and recovery separate agents with similar gains. On Kuhn every adaptive agent reaches half
the attainable gain at the first refit (median h50 = 50 hands), in 100 % of matches for DirBR-CP
down to 73 % for RNR(0.5). After the Kuhn switch from TightPassive to LooseAggr, where the old
exploit fails, DirBR-CP recovers in a median of 50 hands, RNR(0.5) in 400 (30 % of matches), DirBR
in 850 (45 %), and TypeBR, whose posterior has absorbed 1,000 hands of TightPassive, never. The
change-point exploiter shows why one game is not enough: on Kuhn it recovers fastest and loses
least to teaching among the best-response agents; on Leduc its detector fires on *stationary*
opponents, it captures only 0.34 of the attainable gain, and it loses 1.76 chips/hand to teaching
against DirBR's 1.24.

---

## Approximate best responses and the RRPS score

In games too large to traverse, exploitability is estimated by learning a best response, which
gives a lower bound[^timbers2022][^lisy2017]; Kuhn and Leduc allow an exact check.

![Exploitability found by a learned best response (tabular Monte-Carlo control, ε = 0.1) divided by the exact exploitability, as the learning budget grows; mean over 3 seeds and both seats.](../figures/approx_br.png)

On Kuhn the learner comes within 4 % of the exact value by 10⁴ hands for every target; on Leduc it
reaches 71 % (Rock) to 98 % (CallingStation) after 10⁵ hands per seat, and after 10³ hands it
*loses* to Rock and Maniac, so a budget-limited evaluator would report both as safe. Against the
adaptive agents the gap is starker: the same learner, playing a 2,000-hand match online, inflicts
no damage on Leduc (the agents earn 0.35–0.86 chips/hand above the game value), while the
white-box attack takes 1.0–1.5 from DirBR. The RRPS benchmark's *within-population*
exploitability has the same blind spot: 0.279 chips/hand for DirBR on Leduc against an exposure of
2.461, ranking DirBR second of twelve. Adversarial policies against superhuman Go programs are the
large-scale version[^wang2023]. An exploiter's number means little without its budget and strength.

---

## Three and four players

With three players the protocol changes in one place, the worst case. Five approximate
equilibria of three-player Kuhn (CFR, CFR+, MCCFR with three seeds) all have near-zero NashConv
yet are not interchangeable: utility moves between seats inside the equilibrium set, as Szafron et
al. describe[^szafron2013], and profiles mixing components from different solvers reach a NashConv
of 0.125. Worse, an equilibrium component
guarantees nothing against a pair. Its coalition value is computed exactly by enumerating one
member's 2¹⁶ pure strategies and best-responding with the other. For the CFR and CFR+ equilibria it
ranges from −0.094 to −0.125 chips/hand, against equilibrium values of −0.029 to +0.050
(`nplayer_kuhn3.json`).

![Left: each seat's equilibrium value and coalition value in the CFR+ and CFR equilibria. Right: Nash, Blend3P and DirBR3P against a fixed colluding pair, under a coalition teaching attack, and their final coalition value.](../figures/nplayer.png)

The three-player adaptive agent DirBR3P extends Chapter 7's continuous model to two opponents and
best-responds to the modelled pair. Against independent sub-optimal pairs it gains +0.372 ± 0.038
chips/hand over the blueprint (capture 0.99 within 50 hands), and population return, a win-share
Elo, α-Rank at α = 0.1 and Nash averaging all put it first. The coalition-aware readout disagrees.
Against two opponents that bait until hand 1,000 and then play the exact coalition best response
to its current policy, DirBR3P earns −0.466 chips/hand, four times the blueprint's −0.119; the
coalition value of its final policy is −0.386. Blending with the blueprint (Blend3P) roughly
halves both the gain and the teaching loss (+0.213; −0.242). A fixed colluding pair aimed at the
blueprint costs the blueprint 0.119 per hand but is itself exploitable: DirBR3P earns +0.354
against it. Adaptation is a defence against a *static* coalition and a liability against an
adaptive one. No ranking built from independently seated opponents can tell these apart, which is
failure mode 8 in the gap analysis.

So Long Sucker supports only the population layer: the pairwise projection is 0.955 transitive and
Nash averaging picks the betrayer, but a planted alliance lowers a focal baseline's win rate by only
0.8–1.9 percentage points, since about 99.5 % of random games end in deadlock (Chapter 11).

---

## Where existing evaluation breaks — a checklist

| Failure mode (gap analysis) | Evidence in this chapter | What the protocol reports instead |
|---|---|---|
| 1. Exploitability only punishes adaptation | BestEq ties Nash for first on exploitability with 0.02–0.05 gain | gain and exposure as a pair |
| 2. No N-player meaning of exploitability | NashConv ≈ 0 components lose 0.06–0.17 more to a pair | the exact coalition value |
| 3. Approximate BRs are lower bounds | learner negative after 10³ hands; online learner finds nothing | exact exposure; exploiter budget stated |
| 4. Rankings over- or under-credit exploitation | clones, α, horizon change the winner | rankings reported as context |
| 5. Variance compounds with adaptation | 3,383 vs 379 hands per window; Pluribus ±173 | estimator named; AIVAT where possible |
| 7. Deceptive opponents untested | teaching attack takes 1.0–2.2 chips/hand on Leduc | teaching loss |
| 8. Collusion evaluated apart from play | DirBR3P first in return, Elo and Nash averaging; −0.47 under a coalition | coalition teaching attack |
| 9. LLM arenas inherit the above | Elo ranks the Qwen strategy above a less exploitable bot | the same readouts for LLM agents |

: The failure modes of `lit_evaluation.md` (point 6, generalisation suites, concerns cooperative substrates and is not tested here) and what this chapter measured.

---

## Honest notes, limitations, and where this hands off

**What did not hold, and why it matters.** Every exact quantity matches an independent reference,
but three plan predictions failed and are kept as stated: "random loses to everyone" (on Kuhn it
beats AlwaysPass); "AIVAT ≥ 10× on Leduc" (7 of 12 pairs); "approximate within 10 % on Leduc"
(4 of 6 targets, only at 10⁵ hands). Two of my own implementation errors were caught by checks,
not by luck: the AIVAT double count, and a Nash averaging solver that returned infeasible
"optimal" points on near-tied agents until a fixed tolerance and support LPs replaced it.

**Limitations.** These are toy games. The exact worst case and the exact coalition value (2¹⁶
strategies per member) exist only because the games are tiny; at scale a learned attacker gives
only a lower bound on either. The policy-exact estimator exists only for bots. The white-box
teaching attacker is a strong adversary but not the worst adaptive one. The adaptive agents are
Chapter 7–8 baselines: the protocol *measures* the missing N-player loss bound; it does not
provide one. So Long Sucker is weak evidence. Chapter 15 refines two details (a tie-break for
BestEq and a per-hand attacker refresh).

**Connections.** The engine absorbs Chapters 3, 7, 8 (now as one LP), 10, 11 and 12, and is the
yardstick for Chapter 15's experiments. For Contribution 2 it supplies the
measurement a safe N-player agent must pass — gain against independent pairs, coalition value and
coalition teaching loss — and the one-shot LP removes the scaling obstacle Chapter 8 met.

---

## Key takeaways for the thesis synthesis

- **Exploitability and rankings give opposite answers for exploiting agents.** On the same Leduc
  zoo, BestEq and Nash lead exploitability and Nash averaging; RNR(0.5) and DirBR lead Elo,
  population return and the RRPS score. The Elo–exploitability rank correlation is 0.36.
- **Gain and exposure reported together separate what single numbers conflate.** On Leduc,
  BestEq gains 0.047 at zero exposure, RNR(0.5) +0.797 at 0.264, DirBR +0.988 at 2.461.
- **With three players the worst case must be coalition-aware.** Equilibrium components
  (NashConv ≈ 0) lose 0.06–0.17 chips/hand more to a coordinated pair; DirBR3P tops the population
  views and loses 0.47 to a coalition teaching attack.
- **Confidence is the binding constraint on measuring adaptation.** A per-window estimate needs
  about 3,400 hands with raw chips against about 380 with AIVAT on Kuhn; on Pluribus's released
  hands the raw 95 % interval is ±173 mbb/hand.
- **Reported exploiters need a stated budget.** A learned best response reports two exploitable
  Leduc bots as safe after 10³ hands, and within-population exploitability misses DirBR's
  exposure by a factor of nine.
- **The C3 claim stays narrow.** The pieces exist; this chapter adds their joint, unchanged
  application across two- and three-player imperfect-information games and shows where each
  existing measure breaks — so far on toy games only.

<!-- Source footnotes. Definitions may sit anywhere at top level; keeping them
     together here keeps the prose readable and the EN/BG pair easy to compare. -->

[^rrps]: Lanctot, M., Schultz, J., Burch, N., Smith, M. O., Hennes, D., Anthony, T. & Pérolat, J. (2023). "Population-based Evaluation in Repeated Rock-Paper-Scissors as a Benchmark for Multiagent Reinforcement Learning." *Transactions on Machine Learning Research*; arXiv:2303.03196 — 43 bots, 1,000-throw matches; population return, within-population exploitability and their difference as an aggregate score.

[^elo1978]: Elo, A. E. (1978). *The Rating of Chessplayers, Past and Present*. New York: Arco.

[^balduzzi2018]: Balduzzi, D., Tuyls, K., Pérolat, J. & Graepel, T. (2018). "Re-evaluating Evaluation." *NeurIPS*; arXiv:1806.02643 — Elo is inflated by copies of beaten agents; Nash averaging is invariant to redundant agents.

[^alpharank]: Omidshafiei, S., Papadimitriou, C., Piliouras, G., Tuyls, K., Rowland, M., Lespiau, J.-B., Czarnecki, W. M., Lanctot, M., Pérolat, J. & Munos, R. (2019). "α-Rank: Multi-Agent Evaluation by Evolution." *Scientific Reports* 9, 9937. DOI 10.1038/s41598-019-45619-9.

[^vase]: Lanctot, M., Larson, K., Bachrach, Y., Marris, L., Li, Z., Bhoopchand, A., Anthony, T., Tanner, B. & Koop, A. (2023). "Evaluating Agents using Social Choice Theory." *arXiv:2312.03121* (v4, 2025) — Voting-as-Evaluation; maximal lotteries recommended.

[^deepstack]: Moravčík, M. et al. (2017). "DeepStack: Expert-level artificial intelligence in heads-up no-limit poker." *Science* 356(6337), 508–513; arXiv:1701.01724 — also reports an 85 % reduction in standard deviation with AIVAT.

[^bard2013]: Bard, N., Hawkin, J., Rubin, J. & Zinkevich, M. (2013). "The Annual Computer Poker Competition." *AI Magazine* 34(2), 112–114 — total-bankroll and instant-runoff winner rules; duplicate play.

[^openspiel]: Lanctot, M. et al. (2019). "OpenSpiel: A Framework for Reinforcement Learning in Games." *arXiv:1908.09453* — NashConv as the sum of each player's incentive to deviate; exploitability = NashConv / n.

[^szafron2013]: Szafron, D., Gibson, R. & Sturtevant, N. (2013). "A Parameterized Family of Equilibrium Profiles for Three-Player Kuhn Poker." *AAMAS*, 247–254.

[^celli2018]: Celli, A. & Gatti, N. (2018). "Computational Results for Extensive-Form Adversarial Team Games." *AAAI* 32(1). DOI 10.1609/aaai.v32i1.11462; see also Zhang, Y., An, B. & Černý, J. (2021). "Computing Ex Ante Coordinated Team-Maxmin Equilibria in Zero-Sum Multiplayer Extensive-Form Games." *AAAI* 35(6), 5813–5821.

[^timbers2022]: Timbers, F., Bard, N., Lockhart, E., Lanctot, M., Schmid, M., Burch, N., Schrittwieser, J., Hubert, T. & Bowling, M. (2022). "Approximate Exploitability: Learning a Best Response." *IJCAI*; arXiv:2004.09677.

[^balduzzi2019]: Balduzzi, D. et al. (2019). "Open-ended Learning in Symmetric Zero-sum Games." *ICML*, PMLR 97, 434–443 — the transitive/cyclic decomposition.

[^czarnecki2020]: Czarnecki, W. M., Gidel, G., Tracey, B., Tuyls, K., Omidshafiei, S., Balduzzi, D. & Jaderberg, M. (2020). "Real World Games Look Like Spinning Tops." *NeurIPS*; arXiv:2004.09468.

[^aivat]: Burch, N., Schmid, M., Moravčík, M., Morrill, D. & Bowling, M. (2018). "AIVAT: A New Variance Reduction Technique for Agent Evaluation in Imperfect Information Games." *AAAI* 32(1); arXiv:1612.06915 — unbiased for any value function (Theorem 1); on Leduc, 48–75 % lower standard deviation for dissimilar strategies.

[^johanson2007]: Johanson, M., Zinkevich, M. & Bowling, M. (2007). "Computing Robust Counter-Strategies." *NIPS 2007* — Restricted Nash Response.

[^ganzfried2015]: Ganzfried, S. & Sandholm, T. (2015). "Safe Opponent Exploitation." *ACM Transactions on Economics and Computation* 3(2), Article 8. DOI 10.1145/2716322 — the best-equilibrium strategy is their baseline; their safe algorithms risk only gifts already won.

[^kmvs1996]: Koller, D., Megiddo, N. & von Stengel, B. (1996). "Efficient Computation of Equilibria for Extensive Two-Person Games." *Games and Economic Behavior* 14(2), 247–259.

[^vonstengel1996]: von Stengel, B. (1996). "Efficient Computation of Behavior Strategies." *Games and Economic Behavior* 14(2), 220–246 — the sequence form.

[^rowland2019]: Rowland, M., Omidshafiei, S., Tuyls, K., Pérolat, J., Valko, M., Piliouras, G. & Munos, R. (2019). "Multiagent Evaluation under Incomplete Information." *NeurIPS*; arXiv:1909.09849.

[^pluribus]: Brown, N. & Sandholm, T. (2019). "Superhuman AI for multiplayer poker." *Science* 365(6456), 885–890. DOI 10.1126/science.aay2400 — 48 mbb/game, standard error 25, over 10,000 hands; AIVAT cannot be applied to the human players.

[^kim2026]: Kim, J. & Sandholm, T. (2026). "Heuristic Pathologies and Further Variance Reduction via Uncertainty Propagation in the AIVAT Family of Techniques." *arXiv:2605.14261*.

[^ge2024]: Ge, Z., Xu, Z., Ding, T., Meng, L., An, B., Li, W. & Gao, Y. (2024). "Safe and Robust Subgame Exploitation in Imperfect Information Games." *ICML*, PMLR 235, 15255–15270 — adaptation safety and the "taught and exploited" problem.

[^lisy2017]: Lisý, V. & Bowling, M. (2017). "Equilibrium Approximation Quality of Current No-Limit Poker Bots." *AAAI-17 Workshop on Computer Poker and Imperfect Information Games*; arXiv:1612.07547 — local best response, a lower bound on exploitability.

[^wang2023]: Wang, T. T., Gleave, A., Tseng, T., Pelrine, K., Belrose, N., Miller, J., Dennis, M. D., Duan, Y., Pogrebniak, V., Levine, S. & Russell, S. (2023). "Adversarial Policies Beat Superhuman Go AIs." *ICML*, PMLR 202, 35655–35739.
