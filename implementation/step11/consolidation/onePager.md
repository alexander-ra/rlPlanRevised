# Step 11 — Consolidation (internal weave)

> Phase 5 of Step 11. Written **after** the code was executed, from **verified** run artifacts only
> (`implementation/results/{smoke_results.json, sweep_smoke.json, sweep_scale.json}` and the
> measured-vs-predicted dev log [`../EXECUTION_NOTES.md`](../EXECUTION_NOTES.md)). This is the
> internal weave of the per-phase "Key takeaways"; per the confirmed scope no external
> `deliverables/reports/step11/` write-up was produced.
>
> **Artifact caveat (read once):** `results/scale_results.json` is a **pre-fix** tournament run
> (symmetric spread `0.525`, hero win `0.829`, `shapley_higher_coalition:false`, `alpha=0.3`). It is
> cited below only as evidence of the seat-0 bug; its post-fix successor was **not** regenerated, so
> the authoritative scale-tier numbers here come from the 5-seed `sweep_scale.json`, and the
> authoritative single-config numbers from the post-fix `smoke_results.json`.

---

## The one-sentence step

Take everything that made Steps 7-10 tractable — a 2-player game with an **exact** best-response /
exploitability oracle — and remove it: So Long Sucker is 4-player free-for-all, where Nash and
exploitability are both intractable and strategically empty, so the step builds a native SLS engine
(with the 2-player **minimax endgame** as its only exact anchor), a **coalition detector**
(help/harm from chip placement), **Shapley credit** adapted to a purely-competitive game, a
**coalition-aware MAPPO** trainer, and an **EGTA + spinning-top** population analysis — and then
learns, from real runs, that the headline coalition signal is real but lives in a narrow
low-`alpha` regime, and that the game's competitive structure is strongly (though not strictly
dominantly) cyclic.

---

## What each experiment actually showed (measured)

| Experiment | Prediction | Measured (verified artifact) | Verdict |
|---|---|---|---|
| Env — 2-player endgame vs minimax | 0 mismatches | `endgame_mismatches:0`, all terminate, zero-sum (smoke JSON) | confirmed |
| Detector — planted `{0,1}` | strongest pair `{0,1}` | `strongest_pair:[0,1]`, score `10.0` (both JSONs) | confirmed |
| Shapley — glove | `(2/3,1/6,1/6)`, core `{(1,0,0)}` | `[0.6667,0.1667,0.1667]`, core non-empty, alloc `[1,0,0]` | exact |
| Shapley — majority | `(1/3,1/3,1/3)`, **empty core** | `[0.3333]*3`, core non-empty `False` | exact |
| Shapley — symmetric SLS credit | spread `< 0.15` | **post-fix `0.013`** (smoke JSON); pre-fix `0.525` (stale scale JSON) = the bug | confirmed after fix (§R1) |
| Shapley — asymmetric `[8,8,1,1]` | strong pair dominates | strong-pair credit `1.0` > weak `0.0`; `v({0,1})=1.0` | confirmed |
| Training — coalition score, default `alpha=0.3` | Shapley > sparse | smoke `0.0042 > 0.0013` (marginal); **default scale reversed** | superseded by the sweep (§R2) |
| Training — 5-seed `alpha` sweep (scale) | — | at `alpha≈0` proxy syn0.3 gap **+0.0376 ± 0.0103** (~4.4x sparse `0.0109`); counterfactual `alpha0` **+0.0128 ± 0.0026**; every `alpha≥0.3` cell **negative** | coalitions emerge at low `alpha` (§R2) |
| Training — 5-seed `alpha` sweep (smoke) | — | tiny; only proxy `alpha0/syn0.1` sig `+0.0024 ± 0.0008`; `alpha≥0.3` ~0/negative | effect grows with game size (§R2) |
| EGTA / spinning-top — skill-ladder pool | cyclic > 50% | cyclic `0.253` (smoke JSON) / `0.308` (scale JSON) — transitive-dominant | contradicted for this pool (§R3) |
| EGTA / spinning-top — coalition pool | cyclic > 50% | cyclic **~0.57 (60 g/cell) - 0.69 (200 g/cell)** (EXECUTION_NOTES check 5) | large but just under strict dominance (§R3) |
| Win rate vs random (hero), post-fix | > 0.25 floor | smoke sparse `0.44` / shapley `0.41`; sweep ~`0.34-0.54` | confirmed (de-inflated from the `0.87` artifact, §R1) |
| Coalition vs winning trade-off | forming primary, winning secondary (raw L560) | `alpha=0` → win `~0.29` (near floor); `alpha≥0.1` → win `~0.52` | confirmed (§R4) |

Validation harness net: **`validate.py --config smoke` = 4/5 PASS** after the fix (env, detector,
Shapley, training-at-smoke pass; spinning-top honestly red under the strict >50% dominance rule).

---

## The reconciliations (kept predictions + what really happened)

Per WORKFLOW §0.1 the pre-run predictions are kept; what actually happened is appended.

### R1 — The two red FAILs shared one root cause: a deadlock tie-break bug, not first-mover order
Checks 3 (symmetric Shapley spread) and 5 (cyclic dominance) both failed on the first run, and three
independent scripts showed a monotone **seat-0 advantage** (all-random winners `[94,42,33,31]`;
symmetric Shapley credit `[0.593,0.24,0.113,0.053]`; fixed-ally scored `0.493` in seat 0 vs `0.243`
in seat 1). Suspecting a bug before the prediction (§0.1), diagnostics found the real mechanism:
**~99.5% of random games end in a deadlock** (all live hands empty at ~28 turns), so the winner is
decided by `_most_chips` — whose **lowest-index tie-break** handed seat 0 ~2x its fair share
(rotating the start seat changed nothing; the bias was the tie-break, not turn order). Fix: an
**unbiased random deadlock tie-break** threaded through `sls_game.apply(..., rng=...)` on the
play/eval/train paths, with the exact endgame minimax kept deterministic (and
`verify_endgame_consistency` switched to a deterministic optimal-vs-optimal rollout so it still
matches the minimax tree). Result: symmetric spread **`0.54 → 0.013`** (check 3 FAIL→PASS),
all-random winners now uniform (`[0.251,0.238,0.251,0.260]`). A side effect exposed a second
artifact: the impressive `~0.87` hero win-rate was *itself* the seat-0 tie-break (the hero always
sat in seat 0); the fair number is **`~0.41`** vs the `0.25` random floor. Lesson survives and
sharpens: in a game that almost always ends in a near-tie, the **tie-break rule is load-bearing**,
and a symmetric *position* is not a symmetric *outcome* until it is unbiased.

### R2 — "Coalitions don't emerge at scale" was overturned: it was a mis-set blend weight
The first single-config runs (default `alpha=0.3`) showed the Shapley coalition score beating sparse
at smoke (`0.0042 > 0.0013`) but **collapsing/reversing at scale** — read at the time as "the proxy
credit is too weak once training is longer." The 5-seed paired sweep over `alpha × credit_mode ×
synergy` refutes that: `alpha` is the dominant knob, and **`0.3` sits in the dead zone**. Coalitions
emerge **significantly only at low `alpha`** — at `alpha≈0`, proxy credit with `synergy=0.3` gives a
paired gap of **`+0.0376 ± 0.0103`** (~4.4x the sparse baseline `0.0109`), while **every `alpha≥0.3`
cell is negative** (the sparse winner-takes-all term suppresses the coalition signal). Two further
surprises: the effect **grows with game size** (scale low-`alpha` gaps ~10x the smoke ones — opposite
to the naive "smoke-positive / scale-null" read, which was an artifact of holding `alpha=0.3` at
both), and the **cheap critic-value proxy beats the expensive counterfactual** credit (`+0.038` vs
`+0.013` at scale). So the primary thesis signal (raw L560) is **real and robust** — in the right
regime — and the fix is "weight the coalition credit heavily," not "compute a truer credit."

### R3 — The SLS meta-game is strongly cyclic, but not (yet) strictly cyclic-dominant
Step 10 predicted FFA coalition games would have a large cyclic component. Measured, it depends
entirely on **which population** you decompose (the Step-10 lesson repeats): the default
**skill-ladder** pool is transitive-dominant (cyclic `0.25`/`0.31`), but a **coalition pool**
(ally-different-partner strategies) pushes cyclic to **~0.57-0.69**, a large non-transitive
component that strongly confirms the *direction* of raw L561. It stays **honestly red** under the
strict ">50% dominance" threshold (cyclic² still just under 0.5; transitive marginally larger, and
the pool was not tuned to cross the line). The likely residual: the **2-type pairwise projection
discards 3-/4-player coalition effects** — an open, consolidation-level modeling question (raw
L600).

### R4 — Coalition behavior is bought with competitive performance (a genuine trade-off)
Pure coalition credit (`alpha=0`) drops hero win-rate to **~0.29** (near the `0.25` random floor),
while `alpha≥0.1` keeps it **~0.52**. This is exactly the raw-L560 framing — coalition *forming* is
the primary target, winning secondary — made quantitative: you do not get coalition behavior for
free.

---

## Threads handed to the deliverables / next steps

- **Config recommendation (evidence-based, left as a human design choice, not silently applied):**
  lower the training blend default from `alpha=0.3` toward **`alpha≈0.05-0.1`** if the goal is
  coalition formation; the `0.3` default and its honest marginal result are unchanged in the code
  (§0.1: report, don't rig).
- **Engine reconciliation is the highest-value follow-up.** The seat-0 bug (R1) and the still-red
  cyclic check (R3) both trace to the engine's documented simplifications (`_most_chips` tie-break,
  `capturer-plays-next`, `empty-hand skip`). Reconciling the turn/tie-break model against **De
  Carufel & Jerade** (still the outstanding verify-list item) is where correctness and the cyclic
  signal both improve.
- **Credit signal:** the cheap proxy is sufficient (R2), so the counterfactual credit is a
  *robustness* option, not a requirement; the open question is whether a 3-/4-player-aware EGTA
  projection (not the 2-type collapse) surfaces the coalition cycling that R3 leaves on the table.
- **Housekeeping:** regenerate `results/scale_results.json` post-fix so the committed scale
  tournament JSON matches the sweep (currently stale).
- **Thesis hooks confirmed on real runs:** Contribution #1 — the detector cleanly recovers a planted
  coalition (opponent-modeling lifted to social structure); Contribution #2 — with an **empty core**
  (majority game) and no Nash baseline, the N-player "safe" strategy must be behavioral/population
  (piKL), the open gap this step frames but does not close; Contribution #3 — EGTA + spinning-top is
  the working multi-agent evaluation methodology that replaces exploitability, and it inherits Step
  10's "which population you build decides whether you see a ladder or a wheel" caveat.
