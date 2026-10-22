<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->
---
title: "Chapter 14 One-Pager — Evaluation Frameworks and Exploitability Metrics"
subtitle: "Research on the possibilities for applying Artificial Intelligence in computer games"
author: "Alexander Andreev"
date: "September 2026"
lang: en
---

# Chapter 14 One-Pager — Evaluation Frameworks and Exploitability Metrics

**Problem.** An adaptive agent leaves equilibrium on purpose, so exploitability can only count
against it, and its payoff depends on match length and history, so population rankings have no
fixed entry for it. With three players NashConv measures distance from *an* equilibrium, not a
guarantee. The literature check (C3) found the pieces — worst case, rankings, variance reduction
— but no protocol that reports gain, speed and recovery, and a worst case (coalition-aware for
N > 2) together, with confidence, unchanged across games. The nearest precedent scores return and
exploitability for repeated rock–paper–scissors only.

**Approach.** One exact engine built from OpenSpiel's game definitions (two-player Kuhn and Leduc,
three-player Kuhn) scores any strategy exactly. On it: the plan's three layers — exploitability,
population rankings (Elo, Nash averaging, α-Rank, VasE, spinning top) and confidence (seeds,
duplicate cards, AIVAT) — each validated against OpenSpiel or Chapters 3, 7, 8 and 10. Then a joint
protocol for adaptive agents: **gain** over the blueprint, **speed** (h50) and **recovery** (r50),
**exposure** (worst case below v*; with three players the exact coalition value), and
**confidence**. The zoos (16 Kuhn, 12 Leduc, 9 three-player agents) include Chapter 7–8 adaptive
agents, Chapter 12's LLM-extracted strategies, switching opponents and a white-box teaching
attack. All numbers are measured, 10 seeds unless stated.

**Key results (measured).**

- *The machinery is exact.* NashConv equals OpenSpiel's to 10 decimals; AIVAT is unbiased to 1e-15.
  A one-shot sequence-form LP solves full-Leduc safe exploitation in 0.02–0.04 s, where Chapter
  8's loop had not converged within its caps. A real AIVAT bug — the agent's own card luck counted
  twice — was caught by the zero-variance check.
- *Rankings contradict each other on adaptive agents.* On Leduc, BestEq and Nash lead exploitability
  and Nash averaging, BestEq leads VasE; RNR(0.5) and DirBR lead Elo, population return and the
  RRPS score. α-Rank
  names four winners between α = 0.01 and 100; the match horizon changes the Elo winner; copies of
  a weak bot widen the exploiter's Elo lead (+84 → +113) but leave Nash averaging unchanged.
- *The joint protocol separates what they conflate.* Leduc gain / exposure / teaching loss (chips
  per hand): BestEq 0.047 / 0 / 0; RNR(0.5) 0.797 / 0.26 / ≤ 0.27; DirBR 0.988 / 2.46 / 1.0–1.5.
- *Confidence binds.* One 100-hand window's capture to ±0.25 needs about 3,400 hands with raw
  chips and 380 with AIVAT (Kuhn). On Pluribus's released hands (Chapter 13) the raw 95 % interval
  is ±173 mbb/hand.
- *Budgets matter.* A learned best response calls two exploitable Leduc bots safe after 10³ hands;
  within-population exploitability sees 0.28 of DirBR's 2.46 exposure.
- *Three players break the worst case.* Equilibrium components lose 0.06–0.17 chips/hand more to a
  coordinated pair than in equilibrium. DirBR3P tops population return, Elo and Nash averaging (+0.37 gain) and
  loses 0.47 chips/hand to a coalition teaching attack.

**Thesis connection.** This is Contribution 3 in its narrowed form. The claim is not a new toolkit
but the joint, unchanged application of gain, speed, recovery and exposure across two- and
three-player games, plus a demonstration of where each existing measure fails. It is the yardstick
Contribution 1's adaptive agents must pass. For Contribution 2 it fixes the test a safe N-player
agent must pass: gain against independent pairs *and* its coalition value.

**Open questions.** A learned team best response for coalition exposure beyond tiny games;
anytime-valid stopping for per-window AIVAT estimates; the protocol run on a Contribution 2 agent
with a baseline-relative loss bound; a So Long Sucker engine where alliances matter (here they
cost a focal baseline only 0.8–1.9 percentage points of win rate).
