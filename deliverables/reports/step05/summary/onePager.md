<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->
---
title: "Chapter 5 One-Pager — Neural Networks for Imperfect-Information Games"
subtitle: "Research on the possibilities for applying Artificial Intelligence in computer games"
author: "Alexander Andreev"
date: "May 2026"
lang: en
---

# Chapter 5 One-Pager — Neural Networks for Imperfect-Information Games

**Problem.** Chapters 2-4 all store a strategy as a table indexed by information set, and Chapter 4
showed both escapes from that table — a better solver, a smaller game — running out. The third
escape is to stop enumerating: replace the regret table with a function approximator that
*generalises* across similar information states, at fixed memory. Chapter 5 studies that
substitution — Deep CFR, its single-network variants, NFSP — and what it costs in guarantees.

**Approach.** Scope, stated honestly: **this chapter stopped after exploration and reading — there
is no from-scratch Phase-4 implementation and no implementation report**, and the survey's
closing synthesis is still a stub. The measured work is a two-day exploration against
OpenSpiel's reference solvers on Leduc and Kuhn — Deep CFR at three network sizes, NFSP on both
games, tabular MCCFR and CFR+ as baselines — graded by OpenSpiel's own exploitability so the
head-to-head is honest (Chapter 3's MCCFR runs on a custom engine and is not comparable). **All
numbers below are measured**
(`implementation/step05/exploration/logs/day0{1,2}_results.json`).

**Key results (measured).**

- *The step's most actionable artifact is a library bug.* OpenSpiel 1.6.12's PyTorch
  `DeepCFRSolver` **never trains its advantage networks**: `if len(samples.info_state == 0)`
  takes `len` of an elementwise comparison, always truthy, so it returns before the optimiser
  step. Advantage losses come back silently `None` and exploitability sits at random-strategy
  level (**~1.69**) whatever the iteration count. A one-character fix, patched locally.
- *Where the table fits, the table wins — decisively.* Leduc at comparable wall time: CFR+
  **0.00123** (400 iter, 92 s), tabular MCCFR **0.0967** (50k iter, 68 s), Deep CFR **1.49-1.70**
  (120 iter, ~95 s), NFSP **2.46** (50k episodes) — CFR+ roughly **1,400x** better than Deep CFR.
- *Those neural numbers are budget artifacts, not verdicts.* Deep CFR's curves are flat from
  iteration 30 to 120 where the paper uses 400+, and OpenSpiel's own NFSP Leduc example runs
  **2e7** episodes — **400x** our budget. Rule adopted: distrust an NFSP Leduc curve below ~1e6
  episodes.
- *Smaller network won at this budget.* `(32,32)` **1.1441** beat `(64,64)` **1.7002** and
  `(128,128,128)` **1.4908** — consistent with underfitting on few distinct samples, and
  expected to reverse with more iterations.
- *What under-training looks like inside the policy.* Against a 400-iteration CFR+ reference,
  Deep CFR at 40 iterations has **median total-variation 0.35** across 8 sampled Leduc info
  states (range 0.163-0.708): the direction of each decision is usually right, but the
  probabilities are pulled toward uniform (**0.73/0.27** where CFR+ is **0.92/0.07**) — MSE
  regression on noisy counterfactual samples buys an under-confident smoothing of equilibrium.
- *The cost structure that justifies the family anyway.* A Deep CFR outer iteration costs
  **~0.7 s** against a tabular MCCFR iteration's **~1.4 ms** (~500x), but its per-iteration work
  is roughly constant in game size while the tabular cost scales with information-set count.
  Leduc is a teaching benchmark, where neural methods lose to baselines they were never meant to
  beat.

**Thesis connection.** Deep CFR's advantage network is Chapter 1's value network with a
counterfactual target — the joint that lets Chapters 6-8 leave table-sized games behind. More
pointedly, the under-confident smoothing measured here is the failure mode Chapter 7 later prices:
a model with the right direction and the wrong frequency is what makes best-responding to an
imperfect read lose to Nash.

**Open questions.** The step's own gate is unmet: a hand-coded Deep CFR with a Vitter reservoir
sampler, and DREAM's outcome sampling with baseline subtraction, both remain outstanding, so
"can I build it" is unanswered. Untested: whether the tabular-versus-neural ordering flips
exactly at Chapter 3's node-count crossover, and whether the info-state tensor's structure really
matters more than network depth.
