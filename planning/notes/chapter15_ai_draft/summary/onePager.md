<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->
---
title: "Chapter 15 One-Pager — Research Frontier Mapping and Contribution Design"
subtitle: "Research on the possibilities for applying Artificial Intelligence in computer games"
author: "Alexander Andreev"
date: "September 2026"
lang: en
---

# Chapter 15 One-Pager — Research Frontier Mapping and Contribution Design

**Problem.** Fourteen chapters built a toolbox; a thesis needs three defensible claims. The April
2026 plan overclaimed. Real-time opponent modelling already works in two-player games (GSCU,
StratFormer); one benchmark already combines return with exploitability; equal share is not a
guarantee; piKL anchors to a human policy, not to Nash. Only C2 is open at its core: exploitation
with a checked loss bound beyond two players, tested against colluders.

**Approach.** A frontier map per contribution (what exists, the verified gap, the approach,
evidence, risks); design documents for C1–C3; six experiment specifications; a six-paper pipeline.
Two pilots were run on Chapter 14's exact engine. **P1:** Ganzfried and Sandholm's RWYWE, which
risks only the gains it can prove the opponent gave, replicated against their table and measured
with Chapter 14's protocol. **P2:** three-player Kuhn, with three bounded deviation rules against
independent, fixed-colluding and adaptively colluding pairs. All numbers are measured, 5–10 seeds.

**Key results (measured).**

- *The contributions, as they may now be claimed.* C1: within-match inference for N players,
  coupled to a safety criterion. C2: exploitation beyond two players with a checked loss
  criterion; no general theorem, small games, equal share as a reference line. C3: a joint protocol
  that catches what existing measures miss, plus match-level safety.
- *RWYWE replicates where it matters.* All safe algorithms stay above the game value in 400 of 400
  matches against an opponent that best-responds every hand. The best-response row is not
  reproduced (0.328 vs 0.470; open).
- *RWYWE is the two-player baseline Chapter 8 lacked.* Its gain over the blueprint is +0.062
  (Kuhn) and +0.113 (Leduc), 3.1× and 2.4× the best equilibrium's. It stays safe over the match in
  all 120 attacked matches, but gains only 14–30 % of what RNR(0.5) gains with no guarantee.
  Proving gifts is the bottleneck: with cards seen only at showdown, its Leduc bank stays at
  0.01–0.02 chips.
- *Safety is a match-level property.* RWYWE spends a 2.19-chip bank within ~100 hands of an attack
  while the match stays above v* (S = +0.112). C3 adds this readout.
- *Three players, exact checks.* The team-maxmin value of three-player Kuhn is −0.0076 per seat on
  average, close to equal share. Ganzfried and Sandholm's bank with that floor gains +0.082 against
  independent pairs. It keeps −0.007 under adaptive colluders, where the blueprint gets −0.119, and
  is safe in all 135 matches. A capped mixture holds its per-hand relative bound exactly, but gains
  only 16 % of the unbounded exploiter's gain at ε = 0.1.
- *Two robustness readouts disagree.* A KL anchor loses to the mixture on worst-case loss relative
  to the blueprint, but keeps far more against an adaptive coalition (−0.286 vs −0.379).
- *A defect found.* LP ties returned a degenerate equilibrium that never bluffs and never bets the
  King; breaking ties toward the blueprint fixed it.

**Thesis connection.** This is the bridge from Chapter I to Chapters II–IV. The goal and thesis of
§ 1.7 stand. RQ1 now asks for calibrated inference, RQ2 for relative and absolute bounds, RQ3 for
match-level safety. The first publication is the joint protocol paper for IEEE CoG 2027
(1 March 2027), with AAMAS 2027 as a stretch.

**Open questions.** Within-hand gift detection to make gifts provable; learned coalition
exploiters for three-player Leduc, calibrated on three-player Kuhn; whether the maximin value
stays close to equal share in larger games; the unexplained best-response gap in the replication.
