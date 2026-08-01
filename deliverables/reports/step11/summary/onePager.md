<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->
---
title: "Chapter 11 One-Pager — Dynamic Coalition Formation in Competitive FFA Games"
subtitle: "Research on the possibilities for applying Artificial Intelligence in computer games"
author: "Alexander Andreev"
date: "July 2026"
lang: en
---

# Chapter 11 One-Pager — Dynamic Coalition Formation in Competitive FFA Games (So Long Sucker)

**Problem.** Chapters 2-10 all leaned on one crutch: a two-player game with an exact best-response
and exploitability oracle, so "did it work?" was one number. Add a third player and alliances
become possible — form, exploit, betray — while Nash turns both intractable and strategically
empty, since it ignores coalitions entirely. Chapter 11 removes the crutch deliberately. This is the
thesis frontier, not a consolidation step.

**Approach.** A native 4-player **So Long Sucker** engine — the 1950 game Nash, Shapley, Shubik
and Hausner built to study alliances — implemented from the De Carufel & Jerade formalization,
with a 2-player **minimax endgame** as its only exact anchor. On top: a **coalition detector**
(help/harm from chip placement), **Shapley credit** redefined as the value of a member's win
probability, a **coalition-aware MAPPO** trainer blending coalition and winner-takes-all reward by
a weight `alpha`, and **EGTA + spinning-top** analysis reused from Chapter 10. **All numbers below
are measured**, with one caveat: `scale_results.json` is a **pre-fix** run cited only as evidence
of the bug below — the authoritative figures are `sweep_scale.json` (5 seeds) and post-fix
`smoke_results.json`.

**Key results (measured).**

- *Certified wherever exactness exists.* 100/100 random games terminate, all rewards are
  zero-sum, `endgame_mismatches: 0` against exact minimax. The detector recovers a **planted
  `{0,1}` alliance** from the move stream alone (pair score **10.0**, cross-pair entries 0 or -1),
  and Shapley reproduces the glove and majority toys exactly, core emptiness included.
- *The step's biggest finding is a bug, and its lesson outlived it.* Two red checks shared one
  cause: **~99.5% of random games end in deadlock**, so the winner falls to `_most_chips`, whose
  lowest-index tie-break gave seat 0 twice its fair share (all-random winners `[94,42,33,31]`).
  With an unbiased tie-break, symmetric Shapley spread fell **0.525 -> 0.013** and winners went
  uniform; the same fix deflated an impressive **0.87** hero win rate to an honest **~0.41**
  against a 0.25 floor. In a game that nearly always ends near-tied, the tie-break rule is
  load-bearing.
- *"Coalitions don't emerge at scale" was overturned by finding the right knob.* `alpha` dominates
  and the **0.3 default sits in a dead zone**: at `alpha ~ 0` the proxy-credit gap is **+0.0376
  +/- 0.0103** (~4.4x the sparse **0.0109**), while **every `alpha >= 0.3` cell is negative**. The
  effect *grows* with game size (~10x smoke), and the cheap critic-value proxy beats the expensive
  counterfactual credit (**+0.038 vs +0.013**).
- *Coalition behaviour is bought, not free.* `alpha = 0` drops hero win rate to **~0.29**,
  essentially the random floor, while `alpha >= 0.1` holds **~0.52**.
- *Strongly cyclic, honestly short of the bar.* The skill-ladder pool is transitive-dominant
  (cyclic **0.25-0.31**), but a coalition pool pushes cyclic to **~0.57-0.69** — large, yet still
  failing the strict ">50% dominance" rule, so the check stays red. Harness: **4/5 PASS**.

**Thesis connection.** Contribution #1 generalises cleanly: opponent modelling lifts from "what
kind of player is this" to "who is allied with whom", read straight off the moves. Contribution #2
gets its problem statement sharpened rather than solved — with an **empty core** and no Nash
anchor, "safe" cannot mean bounded deviation from equilibrium and must become
behavioural/population-based (piKL). Contribution #3 gains a working substitute for
exploitability in EGTA plus the spinning-top decomposition, inheriting Chapter 10's caveat that the
population you assemble decides whether you see a ladder or a wheel.

**Open questions.** Reconciling the engine's turn and tie-break model against De Carufel & Jerade
is the highest-value follow-up — both the seat-0 bug and the red cyclic check trace to documented
simplifications, and the theorems remain an unverified reading item. Whether a 3- or
4-player-aware EGTA projection surfaces the cycling the 2-type collapse discards. And what "safe"
can mean at all when the core is empty.
