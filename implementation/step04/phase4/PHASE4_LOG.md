# Phase 4 — Implementation Log

Six "days" of work that turn the §6 algorithm catalogue from the step-04
deliverable into running code. Every day is logically self-contained — it
adds new modules and an entry-point trainer that exercises them. No code
introduced in one day is later rewritten by another; later days only
*compose* the earlier modules.

The user explicitly asked for code without algorithm verification at this
stage; trainers are runnable but not exhaustively benchmarked here. Day 5
(quality evaluation) is where systematic measurement lives.

---

## Sources reused as foundation

These modules are imported (not copied) from the surrounding repository:

- `implementation/step03/cfr/leduc_poker.py` — the canonical 6-card Leduc
  engine + `ALL_DEALS` (120 deals).
- `implementation/step03/cfr/info_set_node.py` — `InfoSetNode` (regret-
  matching node used by every CFR variant).
- `implementation/step03/evaluate/best_response.py` — info-set-constrained
  best response over the full game.
- `implementation/step04/exploration/leduc_rank_engine.py` — rank-canonical
  Leduc with 24 canonical deals (lossless suit-isomorphic collapse).
- `implementation/step04/exploration/day02/mini_nl_leduc.py` — variable-bet
  Leduc variant used to stress action abstraction.

The promoted modules under `phase4/` re-export those interfaces with
phase-4-specific extensions; they do not silently re-implement them.

---

## Day 1 — Lossless abstraction on Leduc (suit isomorphism)

**Goal.** Demonstrate that the rank-canonical engine's 24-deal traversal
produces an equilibrium that matches the original 120-deal traversal at
every iteration, and quantify the wall-clock speedup.

**New modules:**

- `phase4/leduc_full_engine.py` — thin shim re-exporting step03's
  `LeducState` and `ALL_DEALS` so phase-4 trainers can target the original
  game without reaching across two repo levels.
- `phase4/leduc_rank_engine.py` — promoted from `exploration/`. Same source
  with a docstring update pointing at the §6.1 / §6.3 sections of the
  deliverable.
- `phase4/day01_suit_isomorphism.py` — a runtime check matching the
  `is_lossless_merge` pseudocode in §6.1 of the deliverable. Operates on
  pairs of (rank-canonical-state, rank-canonical-state) sibling info sets
  and verifies the recursive isomorphism + leaf-utility equality. Used as
  a sanity probe rather than an active merge driver, because the rank
  engine has the merges already baked in.
- `phase4/cfr_trainer.py` — a generic vanilla-CFR loop that traverses any
  state class implementing the standard interface (`is_terminal`,
  `current_player`, `get_info_set`, `legal_actions`, `apply_action`,
  `get_utility`). Takes a `deals_iterable` argument so the same trainer
  drives the full and rank-canonical engines. Implements the buffered
  regret update to match step03's vanilla CFR semantics.
- `phase4/exploitability.py` — wraps step03's best-response routine so it
  can score *any* node-map (regardless of which engine produced it)
  against the *full* Leduc game — the only honest way to measure
  exploitability of a lossless abstraction.
- `phase4/day01_train.py` — runs vanilla CFR for a fixed iteration budget
  on (a) the full 6-card engine and (b) the 24-canonical-deal rank engine,
  saves their node-maps, and reports info-set count + wall-clock per
  iteration for each.

**Deliverable mapping.** This day operationalises §6.1 (lossless merging
criterion) and §6.3 pipeline 1 (GameShrink for Leduc — here trivialised to
the suit-isomorphism rule, because Leduc admits exactly that one
isomorphism family).

---

## Day 2 — Lossy card bucketing

**Goal.** Implement the §6.3 pipeline 2 (HSD + EMD + k-means) on Leduc and
sweep `k ∈ {2, 3, 5, full}` to show how exploitability degrades as
buckets coarsen.

**New modules:**

- `phase4/day02_hand_strength.py` — computes the hand-strength
  distribution (HSD) per (private rank, community rank) Leduc info set by
  enumerating opponent rank rollouts. Returns a 50-bin histogram on
  `[0, 1]`. Mirrors the §6.1 Level 3 / §6.2 EMD-proxy worked example.
- `phase4/day02_emd.py` — both the LP-form `EMD(p, q) = inf_γ ...`
  reference and the 1D `L1`-of-CDFs fast path. Matches the §6.2
  `emd_distance` pseudocode line-for-line.
- `phase4/day02_kmeans_emd.py` — k-means with EMD as the distance metric,
  k-means++ initialisation, multi-restart, triangle-inequality
  acceleration. Returns `cluster_id_per_info_set`.
- `phase4/day02_card_bucketing.py` — applies the cluster output as a
  "card-bucket" abstraction over Leduc info sets. Two flavours:
  *perfect-recall* (the trail of bucket ids per round is preserved) and
  *imperfect-recall* (only the current round's bucket is observed).
- `phase4/day02_train.py` — sweeps `k ∈ {2, 3, 5, full}` × `{perfect,
  imperfect}` recall, runs CFR on each, dumps strategies + exploitabilities
  scored in the full game.

**Deliverable mapping.** §6.3 pipeline 2 + §6.1 Level 3 (empirical
similarity).

---

## Day 3 — Action abstraction + action translation

**Goal.** Reproduce the §3.2 / §6.4 contrast: a strategy trained on a
restricted action set (`{fold, call, pot-bet}`) will do worse on the full
no-limit-shaped game unless the off-tree action is translated.

**New modules:**

- `phase4/mini_nl_leduc.py` — promoted from `exploration/day02/`. No
  semantic change.
- `phase4/day03_translators.py` — three translators of off-tree opponent
  bets: nearest-action, linear probability-split, and the pseudo-harmonic
  mapping of Ganzfried & Sandholm 2013. Each takes the off-tree bet
  fraction and returns either an in-abstraction action (deterministic) or
  a probability mixture (stochastic).
- `phase4/day03_train.py` — trains CFR on the full bet-set and on the
  restricted bet-set. Evaluates the restricted-set strategy by playing it
  in the full game with each of the three translators, reporting the
  exploitability gap of each translator.

**Deliverable mapping.** §3.2 (translator catalogue) + §6.4 patch 2 as the
"non-translator" reference. Pseudo-harmonic is implemented but not
deployed inside subgame solving (deferred to step 6 architectures).

---

## Day 4 — Extended Leduc + combined abstraction

**Goal.** Build a Leduc variant whose info-set count is large enough that
unabstracted CFR is uncomfortable (10 000+ info sets) and apply *all
three* abstraction families simultaneously: suit isomorphism + card
bucketing + action abstraction.

**New modules:**

- `phase4/extended_leduc.py` — 4 ranks `(J, Q, K, A) × 2 suits → 8 cards`,
  same two-round structure as Leduc, two bet-size options per round
  (small + large) borrowed from `mini_nl_leduc`. New module — nothing
  comparable in step03 or exploration.
- `phase4/day04_combined.py` — orchestrator that applies suit
  isomorphism (engine-level, like day 1) → card bucketing with `k=3`
  (info-set-level, like day 2) → action abstraction (`{fold, call,
  small-bet}`, like day 3) on the Extended Leduc engine. Reports
  info-set count after each successive abstraction.
- `phase4/day04_train.py` — runs MCCFR external sampling on the
  triple-abstracted game (full traversal would be slow on Extended
  Leduc) and saves the resulting strategy for day-5 evaluation.

**Deliverable mapping.** §6.3 pipelines 1 + 2 composed, plus §3.2 action
abstraction. The Extended Leduc engine is the only piece tagged
🟡 AI-ASSISTED in the raw plan; it is shaped on the same skeleton as
`mini_nl_leduc.py` to keep the diff small.

---

## Day 5 — Abstraction quality evaluation + Pareto frontier

**Goal.** Aggregate every previous day's strategies and produce the
deliverable's §8 Pareto frontier: info-set count vs exploitability gap
across all configurations.

**New modules:**

- `phase4/day05_exploitability_gap.py` — wraps day-1's exploitability
  evaluator and the §6.2 Tool 3 `cfr_br` definition. For each
  configuration, computes:
    1. abstract-game strategy exploitability in the full game
       (`exploit_G(T(σ̂*))`),
    2. CFR-BR strategy exploitability in the full game
       (`exploit_G(σ_CFR-BR)`),
    3. their difference, which is the §6.2 "abstraction error vs
       solving error" decomposition.
- `phase4/day05_emd_evaluator.py` — direct analogue of §6.2 Tool 2:
  computes the EMD distance between an abstract info-set's HSD and the
  full-game info-set HSDs it covers, summed over the partition. Returns a
  scalar per configuration that should track the empirical
  exploitability gap.
- `phase4/day05_pareto.py` — collates the configuration table:
  `(name, info_sets, exploit_gap, EMD_proxy, solve_time)` and writes a
  CSV.
- `phase4/day05_plots.py` — matplotlib figure: `info_sets` (x-axis,
  log-scale) vs `exploit_gap` (y-axis, log-scale), one point per
  configuration, with EMD-proxy values shown as marker size. Output goes
  into `phase4/figures/`.
- `phase4/day05_train.py` — entry point that loads all prior days'
  strategies and produces the table and figures.

**Deliverable mapping.** §6.2 (all three tools) + §8 (Pareto frontier).

---

## Day 6 — Cross-validation + write-up prep

**Goal.** Sanity-check phase-4's CFR strategies against OpenSpiel where
applicable, and inventory the artefacts ready for the §13 deliverable
integration step.

**New modules:**

- `phase4/day06_openspiel_compare.py` — loads phase-4's full-Leduc
  strategy from day 1 and OpenSpiel's CFR output for the same game, and
  reports max-strategy-difference at matching info sets. Mirrors
  `step03/compare_openspiel.py` but is graceful when OpenSpiel is not
  installed.
- `phase4/day06_summary.md` — tradeoff table from day 5 written up in the
  deliverable's §7 / §8 voice. Acts as the bridge between this directory
  and the §7 "Implementation results" section that the deliverable's
  step 13 will fill.

**Deliverable mapping.** §7 / §9 / §10 of the deliverable inherit from
this day's outputs.

---

## Status — all six days landed in this pass

- Day 1 — [done]: `leduc_full_engine.py`, `leduc_rank_engine.py`,
  `day01_suit_isomorphism.py`, `cfr_trainer.py`, `exploitability.py`,
  `day01_train.py`.
- Day 2 — [done]: `day02_hand_strength.py`, `day02_emd.py`,
  `day02_kmeans_emd.py`, `day02_card_bucketing.py`, `day02_train.py`.
- Day 3 — [done]: `mini_nl_leduc.py`, `day03_translators.py`,
  `day03_train.py`.
- Day 4 — [done]: `extended_leduc.py`, `day04_combined.py`,
  `day04_train.py`.
- Day 5 — [done]: `day05_exploitability_gap.py`,
  `day05_emd_evaluator.py`, `day05_pareto.py`, `day05_plots.py`,
  `day05_train.py`.
- Day 6 — [done]: `day06_openspiel_compare.py`, `day06_summary.md`.

All entry-point scripts are written and the default smoke-test budgets
have been run. The known issues / open questions for review live at the
bottom of `day06_summary.md`.

This log is the canonical record of what landed each day. The deliverable
reports on outcomes; this log records what happened.
