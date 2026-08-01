<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->
---
title: "Chapter 9 One-Pager — Multi-Agent Reinforcement Learning"
subtitle: "Research on the possibilities for applying Artificial Intelligence in computer games"
author: "Alexander Andreev"
date: "July 2026"
lang: en
---

# Chapter 9 One-Pager — Multi-Agent Reinforcement Learning

**Problem.** Chapters 2–8 lived inside two-player zero-sum games, where a Nash strategy secures a
value `v*` against anyone and CFR provably converges to it. Chapter 9 is the pivot into the
multi-agent world, where the defining difficulty is **non-stationarity**: every agent is
learning at once, so from any one agent's seat the environment (which contains the others) never
holds still. This is the launch point for the thesis's multi-agent contributions — dynamic
opponent modeling (#1), safe exploitation without a minimax anchor (#2), and population-level
evaluation (#3).

**Approach.** Build and compare the field's four structural answers to non-stationarity on
small, *exactly-solvable* testbeds, so every learner is graded against ground truth.
**Independent learning** (the control that fails) on four canonical matrix games; **CTDE** —
centralize the critic at training, decentralize the actor at execution — via MADDPG and MAPPO on
cooperative tasks; **PSRO** — a game played over a *population* of policies (meta-Nash +
best-response oracle), reusing Chapter 07's exact best response as both oracle and exploitability
metric — on Kuhn, Leduc, a matrix game, and a native Goofspiel; **learned communication**
(CommNet); and **LOLA** (differentiate through the opponent's learning step) on the Iterated
Prisoner's Dilemma. **All numbers below are measured.**

**Key results (measured).**

- *Independent learning fails exactly where theory says.* It converges to Nash on Prisoner's
  Dilemma (defection), Stag Hunt (the risk-dominant corner), and Battle of the Sexes, but
  **Matching Pennies never converges** — its distance-to-Nash actually *grows* ($0.30\to0.48$),
  a sharper-than-predicted non-convergence (a contradicted prediction, §9 of the report).
- *PSRO is the game-theory↔MARL bridge, and it works on the small games.* Exploitability →
  machine zero on **Kuhn** ($0.917\to2\times10^{-16}$, 6 rounds), → 0 on the matrix game and
  Rock–Paper–Scissors. Self-play confirms the mechanism: on Kuhn the **average**-iterate NashConv
  falls $0.24\to0.031$ while the **last** iterate keeps oscillating — why a population/averaging
  is needed.
- *A centralized critic is a near-zero-variance teacher.* On CoopSignal the centralized critic's
  residual is `3.2e-11` vs the independent critic's `0.077` — the CTDE variance-reduction claim,
  confirmed.
- *Communication clears the guessing ceiling.* CommNet with the channel ON scores `0.795` vs
  `0.204` OFF (ceiling 1/K = 0.2) — a learned, not designed, protocol.
- *LOLA turns defectors into cooperators.* IPD per-step return rises from `1.04` (naive
  defection) to `2.82` (LOLA cooperation); zeroing the look-ahead recovers the naive gradient
  exactly (the mechanism check).
- *Honest negatives (kept predictions, §9).* PSRO on **Leduc** declines but hits a scaling wall
  (`4.75→2.16` after 20 rounds, not `<0.5`); **Goofspiel K=4** oscillates rather than converging
  (a flagged code anomaly, documented not fixed); and on the **climbing game** no method reaches
  the optimum 11 (IL/MAPPO 7, MADDPG 5) — a centralized critic lowers variance but does not by
  itself solve hard-exploration coordination.

**Thesis connection.** PSRO is Chapter 2's iterated best response lifted to a population and the
empirical backbone here; LOLA is *dynamic* opponent modeling, the moving-target complement to
Chapter 7's static read (Contribution #1); PSRO's meta-game is a population-level evaluation
methodology (Contribution #3). The Leduc scaling wall echoes Chapter 8's global-vs-local finding,
and the place where every two-player guarantee stops — the **missing `N>2` minimax anchor** — is
exactly Contribution #2's problem statement.

**Open questions.** Can an approximate (RL) oracle push Leduc PSRO close to Nash, and at what
cost to the guarantee? What breaks the Goofspiel-K=4 oscillation (de-duplication? a mixed
population? a different meta-solver?), and why does a centralized critic *hurt* on the climbing
game? And underneath all of it: with no minimax value for `N>2`, what does "safe" mean for a
population, and can PSRO's meta-game supply the substitute (Contribution #2)?
