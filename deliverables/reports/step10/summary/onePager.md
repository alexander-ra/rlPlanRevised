<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->
---
title: "Step 10 One-Pager — Population-Based Training and Evolutionary Game Theory"
subtitle: "Research on the possibilities for applying Artificial Intelligence in computer games"
author: "Alexander Andreev"
date: "July 2026"
lang: en
---

# Step 10 One-Pager — Population-Based Training and Evolutionary Game Theory

**Problem.** Self-play can go in circles: in a cyclic game (rock-paper-scissors) "get better" has no
meaning, so a population that only trains against itself spins instead of improving. Step 10 is the
population-level layer of the thesis — how to *diagnose* whether a game/population is a skill ladder
or a wheel of counters, and how to *train and evaluate* a whole population of agents. It is the launch
point for automated opponent modeling (#1), population safe-exploitation without a minimax anchor
(#2), and population-level evaluation (#3).

**Approach.** Two halves, both graded against exact references. **Part I — evolutionary game theory
as a diagnostic:** replicator dynamics on four solvable matrix games (checked against analytic
ESS/Nash) and the transitive/cyclic **spinning-top** decomposition. **Part II — an AlphaStar-style
PBT league** of neural PPO agents on Leduc Hold'em (three agent types: main / main-exploiter /
league-exploiter, plus freezing and PFSP), evaluated with **EGTA/meta-Nash**, Elo, and diversity
metrics — every neural policy extracted to a *tabular* policy so Step 07's **exact** best response
measures its exploitability. **All numbers below are measured.**

**Key results (measured).**

- *Replicator dynamics reproduce every analytic outcome.* Prisoner's Dilemma → all-Defect; Hawk-Dove
  → the interior $0.5$ ESS (orbit radius $0.0$); **Rock-Paper-Scissors never converges** (orbits the
  centre, radius $0.095$); Stag Hunt → a basin-dependent pure ESS.
- *The spinning-top diagnostic works, and Leduc's structure depends on the population.* Hodge
  decomposition gives RPS transitive $0.0$ / cyclic $1.0$ and a skill ladder $1.0$ / $0.0$ (the SVD
  rank-1 method wrongly gives RPS $0.707$). The **PSRO best-response** meta-game on Leduc is mostly
  **cyclic** ($\approx0.45$ transitive, 27 three-cycles); the **league snapshot** meta-game is mostly
  **transitive** ($\approx0.94$-$0.98$) — a contradicted prediction, §4/§7 of the report.
- *The league produces strong individuals.* Its best frozen snapshot reaches exploitability **$1.305$**
  (scale), beating exact PSRO ($2.163$) and self-play ($3.683$); CFR-Nash floor is $0.0099$.
- *Honest negatives (kept predictions).* League exploitability is **non-monotone at scale**
  ($4.73 \to$ min $\approx1.21 \to 2.05$ over 120 epochs) — the live agents regress late; the best
  agents are frozen snapshots. And the **meta-Nash mixture is *more* exploitable than its best member**
  at scale ($3.418 > 1.305$) — meta-Nash minimizes meta-game regret, not full-game exploitability, so
  mixing behavioral policies can hurt. Diversity is thin (participation ratio $1.9$, a single
  behavioral cluster).

**Thesis connection.** The league is Step 9's PSRO made asynchronous with neural oracles, reusing Step
07's exact best response as the yardstick; main exploiters are automated opponent modelers
(Contribution #1); EGTA/meta-Nash is the population evaluation methodology (Contribution #3). The
league's missing guarantee — it can regress, and its mixture can be exploitable — is the population
form of the **missing $N>2$ safety anchor** (Contribution #2). The transitive/cyclic diagnostic
predicts Step 11's FFA coalition games will be strongly cyclic.

**Open questions.** Does best-snapshot retention / population regularization remove the late
regression (a training fix) or is it inherent to the three-type design (a design fix)? Should a
population ship a selected best-response-robust member or a diversity-regularized meta-solver instead
of the meta-Nash mixture? And underneath both: with no minimax value for a population, what does
"safe" mean, and can the exploiter mechanism be given a guarantee rather than staying heuristic
(Contribution #2)?
