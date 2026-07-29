<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->
---
title: "Step 4 One-Pager — Game Abstraction and Scaling"
subtitle: "Research on the possibilities for applying Artificial Intelligence in computer games"
author: "Alexander Andreev"
date: "May 2026"
lang: en
---

# Step 4 One-Pager — Game Abstraction and Scaling Imperfect-Information Games

**Problem.** Step 3 established that a solver's reach is bounded by tree size, so the classical
route to real poker is not a better solver but a *smaller game*: shrink it, solve the shrunken
version, translate the strategy back, and pay an exploitability tax for the distinctions you
threw away. Step 4 measures that tax. The question is not "does abstraction help" but which
axis of compression is safe, and whether the compute a reduction buys ever repays the strategic
information it destroys.

**Approach.** A Leduc-family pipeline that compresses along three axes and evaluates every
resulting strategy **in its own full game**: **lossless suit isomorphism** (Leduc payoffs depend
only on rank and on whether the private card pairs the board, so suit-isomorphic information
sets merge with no loss), **lossy card bucketing** (hand-strength features, EMD-style distances,
k-means, in perfect- and imperfect-recall regimes), and **action abstraction plus translation**
(nearest-action, probability-split, pseudo-harmonic) on a variable-bet Mini-NL Leduc. Benchmarked
with CFR+ under a common **180-second** budget, 3 seeds, on fixed-limit Leduc, Mini-NL Leduc and
a 4-rank Extended Leduc. **All numbers below are measured.**

**Key results (measured).**

- *Lossless compression is the highest-value move, and it wins by buying iterations.* Suit
  isomorphism cuts fixed-limit Leduc from **936 to 288** information sets and reaches
  **3.13e-6** exploitability against full CFR+'s **4.44e-5** in the same wall clock — because it
  completes **14,185** iterations instead of **2,655**. Confirmed at scale on Extended Leduc:
  **10,304 -> 2,968** info sets (-71%), **0.0272 -> 0.00126**, roughly 6x the iterations.
- *Lossy card buckets install a floor that compute cannot lift.* `k2` **0.571**, `k3` **0.382**,
  `k5` **0.382** — all at 11,000+ iterations, i.e. 4x more solving than the full game and four
  orders of magnitude worse. The error is in the abstraction, not the budget.
- *Action abstraction is the dangerous axis.* Mini-NL: the full 4,704-info-set game reaches
  **0.00692**, while the 936-info-set action abstraction reaches **0.673** despite 5x the
  iterations — roughly **100x worse** for a 5x smaller tree. Extended Leduc is starker still:
  suit+action **4.696** and suit+action+buckets **4.734**, both far worse than simply solving
  the unabstracted game. Translation error dominates the total.
- *A measured artifact, not a law.* `k5` matches `k3` exactly because Leduc's post-flop
  hand-strength distributions collapse into three effective shapes; the bucket-count ordering
  seen here is a property of this tiny game.
- *Stated limitations.* CFR+ is deterministic, so the three seeds are not independent stochastic
  runs; the action-abstraction numbers depend on the current translator and deployment
  semantics and should be read as a diagnostic failure mode; and the OpenSpiel comparison aligns
  all 936 information sets as a sanity check, not as proof of identical solver dynamics.

**Thesis connection.** The reporting format is the transferable part: strategy quality is
meaningless without game size beside it, and the Pareto frontier of the two is an early seed of
Contribution #3's evaluation methodology. The mechanism transfers as well — Step 7's type-based
opponent modelling is this same "group for tractability" idea moved from state space to strategy
space, and its confident-but-wrong failure is action translation's misspecification in another
costume.

**Open questions.** Static translation is brittle by construction, which points at subgame and
nested solving (Step 6) as the production-grade answer to off-tree actions. Whether the ordering
measured here — card abstraction survivable, action abstraction ruinous — holds in a game with
enough hand-strength diversity that `k5` genuinely differs from `k3`. And whether an abstraction
can be adapted to the opponent rather than fixed in advance, which is where this step touches
the adaptive framework directly.
