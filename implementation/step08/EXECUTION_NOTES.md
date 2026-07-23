# Step 08 — Execution Notes (dev log)

**What this is.** Step 08's code was authored but never run ("every number in the docs is a
prediction to verify"). This file records the *first actual execution* of Phase 2 (Exploration)
and Phase 4 (Implementation): what passed, measured-vs-predicted numbers, bugs found + the
minimal fixes applied, and the one substantive finding. **Consolidation (Phase 5) is
deliberately left to another agent** — this is raw dev observation, not the write-up.

Run env: repo `.venv` (Python 3.12.10); numpy 2.4.6, scipy 1.18.0, matplotlib 3.11.0, OpenSpiel
(`pyspiel`) all present. Every script run from its own phase folder (`implementation/` or
`exploration/`) per the sys.path shim contract. Date: 2026-07-23.

---

## TL;DR

- **All 9 implementation self-tests pass; `validate.py` = 7/7 PASS (`failed=0`)**, including the
  OpenSpiel cross-check, which matches **exactly** (|delta| = 0.000000 on both games — better
  than the predicted 0.001/0.01 tolerances).
- **Smoke (Kuhn) fully executed**: pareto + tournament + OpenSpiel; artifacts written to
  `implementation/results/` and `implementation/plots/`.
- **Scale (Kuhn) executed** in full (6 opponents, 11-pt RNR sweep, SES, 20k-hand online
  pipeline, teaching attack).
- **Scale (Leduc) = bounded** (per owner decision): the pieces that converge (nash, full_br,
  single-texture SES) run to completion; the full-game exact safe solvers are capped + flagged
  non-converged — see the finding below.
- **5 bugs fixed**, all in `ganzfried_solver.py` / `rnr_solver.py` / `validate.py` (Step 07 code
  untouched). Details below.

---

## THE finding (for the consolidation agent)

**Exact constraint-generation safe exploitation does not scale to the full Leduc tree.** The
solvers here realize the safety constraint `worst_case(hero) >= floor` by single-best-response
cutting planes (double-oracle): solve master LP → adversary BR → add cut → repeat. This is
mathematically correct and converges quickly where the number of relevant pure best responses is
small:

- **Kuhn** (13 hero sequences): converges in ~4 iterations.
- **Single-texture Leduc subgame** (one flop card, ~150 free info sets, the rest *pinned* to the
  safe blueprint): converges in ~260 iterations (~45 s), `gadget_satisfied=True`.

It does **not** converge on the **full Leduc tree** (~468 free info sets): with everything free,
the adversary always finds a fresh ~0.1–0.2-exploitable hole, so cuts accumulate without the
worst-case climbing to the floor.

Measured (Leduc, hero P0, floor = game value v* = −0.086; full game, all info sets free):

| solver | max_iters | worst-case reached | floor | safe? | time |
|---|---|---|---|---|---|
| ganzfried | 500 | −0.2031 | −0.086 | NO | 175 s |
| adaptation | 500 | −0.1984 | −0.120 (blueprint) | NO | 132 s |
| prime_safe | 500 | −0.1984 | −0.120 | NO | 132 s |

Progress *is* monotone but tail-slow (full postflop subgame: wc −0.62 @30 it → −0.44 @80 → −0.14
@800), so more iterations would eventually get there — but at minutes-per-solve and thousands of
iterations it is not practical, and the online pipeline (a full solve per refit × 40 refits × 5
seeds) is entirely infeasible on Leduc with this method.

**Why it matters (thesis hook):** this is exactly the wall that pushes the field from *exact
tabular* safe exploitation to **CFR-based subgame solving / gadget games / function
approximation** — i.e. the NLHE blueprint side-project and the later study steps. The
single-texture SES result shows the escape hatch: *pin most of the tree to a safe blueprint and
only re-solve the small subgame you are actually in* (real-time search). That converges.

---

## Bugs found + minimal fixes

All fixes are in Step 08 code only; Step 07 modules were not modified.

### 1. `rnr_solver.py` — canonical RNR LP unbounded on the first iterate
`canonical_rnr` solves a max-min with an auxiliary worst-case variable `t` bounded only by
adversary cuts `t <= c_adv·x`. The loop added the first cut *after* the first solve, so
iteration 0 had **no** cuts and `maximize t` was unbounded → `HiGHS Unbounded` (crash at every
p, seen first at p=0). **Fix:** seed one adversary cut before the loop (the opponent's BR to the
hero's BR-vs-model — a natural first restricted adversary). Endpoints now correct: p=0
exploitability +0.0000, p=1 EV +0.1667 = full BR.

### 2. `ganzfried_solver.py` — `safe_exploit` crashed / returned unsafe strategies
Several coupled issues in the shared constraint-generation core:
- **Infeasible-crash.** The floor (an approximate Nash's *self-play* value) can sit marginally
  ABOVE the game's true achievable max-min (Kuhn: −0.0555 vs true −0.05556, a ~6e-5 overshoot).
  Requiring the exact `wc >= floor` then makes the master eventually **infeasible** →
  `RuntimeError` crash (self-test), and on unlucky opponent-dependent cut paths it returned a
  wildly **unsafe** strategy (ganzfried vs LooseAggressive: wc −0.1222 vs floor −0.0555).
- **Fixes:**
  - Cut enforced at `floor − _FEAS_SLACK` (`_FEAS_SLACK = 5e-4`), a small tol-independent
    feasibility slack that keeps the master feasible (the true max-min strategy satisfies it)
    without lowering the safety bar by the full convergence tolerance. *(Earlier I mistakenly
    used `floor − tol`; that broke the Leduc subgame, whose `tol=1e-2` slackened the safety bar
    by a full 0.01 and stopped it converging — decoupling `_FEAS_SLACK` from `tol` fixed it.)*
  - DONE check `wc >= floor − tol − 1e-9`: the master exploits down to the binding cut, so the
    converged `wc` lands exactly on the constraint; a tiny numerical slack makes "landed on the
    constraint" reliably count as converged instead of oscillating for `max_iters`.
  - Graceful handling if a solve is still infeasible (return the last feasible strategy instead
    of crashing) — a safety net; not normally triggered now.
  - Final `safe` flag computed against `floor − tol − 1e-9` (was hard-coded `False`).
  - Default `tol` 1e-6 → 1e-3 (1e-6 was far tighter than the CFR/approximation error and
    inconsistent with `safety_checker.is_safe`'s 1e-3). Default `max_iters` 30 → 300 (30 was
    far too low for any Leduc subgame; Kuhn early-returns so no cost).
- **Result:** ganzfried now returns a within-tolerance-safe strategy against **every** opponent
  (Kuhn wc −0.0560 = v* − 5e-4, uniformly; converges in ~4 iters).

### 3. `validate.py` — subgame check used a non-converging predicate
`check_subgame_differs_and_safe` used `leduc_postflop` (ALL postflop textures jointly, ~450
free info sets) which does not converge (see finding) → `gadget=False` FAIL. **Fix:** switched
to `leduc_flop_rank(2)` (one flop texture, "after a King" — raw step L146), which is the actual
real-time subgame SES re-solves, with the Leduc tolerance `tol=1e-2` and `max_iters=400`. This
genuinely validates all three SES properties (differs / improves / gadget-safe) and converges in
~45 s. `leduc_flop_rank` already existed in the module for exactly this.

---

## Phase 4 — Implementation results

### Self-tests (all exit 0)
`seq_form` is the key gate: LP best response == Step 07 exact BR to `< 1e-6` — Kuhn P0 +0.16667 /
P1 +0.31729, Leduc P0 +0.936977 / P1 +1.120880. All other module self-tests pass.

### `validate.py` — 7/7 PASS
| check | result |
|---|---|
| seq-form LP BR == exact BR (kuhn) | PASS (match < 1e-6) |
| RNR endpoints (p=0 safe, p=1 = full BR) | PASS (p=0 expl +0.0000; p=1 EV +0.1667 = full BR) |
| Ganzfried safe (≥ v*) & profitable | PASS (wc −0.0560 vs v* −0.0555 within 0.001; EV −0.0442 ≥ Nash EV −0.0469) |
| prime-safe floor = v* − ε | PASS (ε +0.0141; floor −0.0696; wc −0.0701) |
| adaptation-safety inequality | PASS (expl(exploit) +0.0146 ≤ expl(blueprint) +0.0141 within tol) |
| subgame differs + improves + safe (leduc) | PASS (maxTV 0.80; EV +0.223 vs blueprint +0.198; gadget True) |
| OpenSpiel NashConv cross-check | PASS — **exact**: kuhn 0.916667, leduc 4.747222, \|delta\| 0.000000 |

### Smoke (Kuhn) — exact method × opponent table (game value −0.0555)
- `ganzfried` safe (wc −0.0560) against **all** opponents (post-fix).
- `full_br` genuinely unsafe (wc down to −0.5000) — the intended cautionary point.
- `rnr_0.5` partially exploitable (wc −0.11 vs LooseAggressive) — a tradeoff point, expected.
- Canonical RNR **dominates** the naive Nash/BR blend at equal exploitability; ganzfried point
  sits above the RNR safe frontier (EV −0.0442 at expl ≈ 0).

### Scale (Kuhn) — 6 opponents incl. AlwaysBet/AlwaysPass, 200k-iter Nash
`ganzfried` −0.0561 (safe) across all six opponents; the better Nash removes the approximate-
baseline `!` on `nash` itself (wc −0.0559). Teaching attack (TightPassive→Nash @10k, 5 seeds)
ran; `nash`/safe methods stay near baseline, `full_br` swings.

### Scale (Leduc) — BOUNDED run (`results/leduc_bounded_scale.json`)
Converging pieces run to completion; full-game exact safe solvers capped at 40 iters and
flagged. `*` = capped/non-converged, `!` = worst-case below the Nash floor (v* = −0.0862,
Leduc tol 1e-2). SES uses the single-texture subgame (`leduc_flop_rank(King)`).

```
  opponent           nash    full_br  ses_subgame   rnr_0.5  ganzfried prime_safe adaptation
  Rock       EV     0.2011    0.9370     0.2468      0.4941    0.6238    0.6355    0.6355
             wc    -0.0893   -1.6333!   -0.1297!    -0.8124*! -0.8378*! -0.7444*! -0.7444*!
  Maniac     EV     0.4381    2.1772     0.6818      2.0494    1.8060    1.8416    1.8416
             wc    -0.0893   -1.1000!   -0.1296!    -0.8992*! -0.6379*! -0.6567*! -0.6567*!
  CallingSt. EV     0.5591    1.4640     0.6631      1.3064    1.3416    1.3634    1.3634
             wc    -0.0893   -1.0000!   -0.1296!    -0.7801*! -0.9150*! -0.6863*! -0.6863*!
  Nash       EV    -0.0862   -0.0826    -0.0911     -0.1255   -0.0835   -0.0833   -0.0833
             wc    -0.0893   -0.8417!   -0.1293!    -0.7953*! -0.3763*! -0.3247*! -0.3247*!
```
Reading it:
- **nash**: safe everywhere (wc −0.0893 ≈ v*) and already beats even-money vs the weak types.
- **full_br**: biggest EV, catastrophic worst-case (−1.0 to −4.2) — the cautionary point, and it
  is far more dramatic on Leduc than on Kuhn.
- **ses_subgame** (CONVERGED, ~200 iters): exploits **more** than nash (e.g. Rock 0.247 > 0.201)
  while holding worst-case ≈ −0.13, i.e. at the blueprint's own guarantee (−0.1197) within the
  1e-2 tolerance. The `!` is only vs the *Nash* floor; SES guarantees the *blueprint* floor. This
  is the whole point: **safe local real-time exploitation works** where the full-game solve does
  not.
- **rnr_0.5 / ganzfried / prime_safe / adaptation** (CAPPED, `*!`): at 40 iters they are still in
  the exploitative phase with worst-case −0.6…−1.3 — nowhere near safe. This is the documented
  non-convergence, shown rather than hidden.

*(No Leduc online-pipeline or teaching-attack: each refit is a full non-converging Leduc solve,
so those are infeasible with the exact method — deferred by design.)*

---

## Phase 2 — Exploration results (all 5 scripts)
| script | key measured result vs prediction |
|---|---|
| `exploitation_safety_playground` | Nash expl 0.0013, Full BR expl 0.4445, 50% blend halfway — matches. |
| `pareto_curve` | monotone profit↔worst-case-loss frontier; JSON+PNG written. |
| `naive_exploit_danger` | Full BR exploitability +0.4445; deviates from Nash at info sets 1, 2pb, 3 (the "holes"). |
| `rnr_playground` | naive p-sweep monotone; JSON+PNG written. |
| `subgame_peek` (Leduc) | blueprint EV vs Rock +0.201, full exploit +0.937. **Nuance:** the *full* BR deviates at **239/468** info sets, not the "handful" the caption predicts — locality is per-decision (each subgame is small), not globally sparse. |

---

## Measurement artifacts worth knowing (not bugs)
- **Approximate-Nash baseline.** At 30k CFR iters the Nash strategy's own worst-case (−0.0568)
  sits ~0.0013 below its self-play game value (−0.0555), so the strict Nash-floor display check
  (`wc >= v − 1e-3`) flags even **Nash** as `!` in the smoke table, and the online-pipeline
  `safety_violations` counts Nash as violating its own floor. At 200k iters (scale) the gap
  closes and Nash shows clean. Not a solver defect — an artifact of using an approximate baseline
  with a tight absolute tolerance.
- **prime_safe / adaptation floor at the blueprint** (`v* − ε`, −0.0701), by design *below* the
  Nash floor. Their `!` against the Nash floor is expected — their guarantee is relative to the
  blueprint, not to Nash.

---

## Artifacts written
- `implementation/results/`: `pareto_kuhn.json`, `kuhn_smoke.json`, `kuhn_scale.json`,
  `leduc_bounded_scale.json`.
- `implementation/plots/`: `pareto_kuhn.png`, `methods_kuhn.png`, `teaching_kuhn.png`.
- `exploration/figures/`: `pareto_curve_kuhn.{json,png}`, `rnr_playground_kuhn.{json,png}`.

## Open items for the human / consolidation agent
- **Scale Leduc is bounded, not complete** (owner decision): full-game exact safe solvers are
  documented as non-converging, not run to completion; no Leduc online-pipeline / teaching-attack
  (each refit is a non-converging full solve).
- The config `ses_predicate` for Leduc is still `leduc_postflop` in `config.py`; the *converging*
  real-time subgame is a single texture (`leduc_flop_rank`). If a future run wants SES in the
  standard `tournament.py --config scale --game leduc`, switch that predicate (and register a
  single-texture entry in `tournament._PREDICATES` / `pipeline`). Left unchanged here to avoid
  editing the shared config beyond the validated path.
- Possible next step (algorithmic, beyond "minimal fix"): a blueprint-**regularized** master
  (proximal / πKL term) to accelerate safety convergence on larger trees — directly echoes the
  thesis's πKL-regularized-exploitation direction.
