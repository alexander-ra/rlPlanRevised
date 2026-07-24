# Step 11 — Execution Notes (measured-vs-predicted dev log)

This is the running dev log for **executing** the Step 11 phases that were authored (unexecuted) in
the `step11 preparations` commit. It follows WORKFLOW §0.1: predictions written during authoring are
kept in place; here we record **what actually happened on a real run**, suspect bugs before blaming a
prediction, and keep honest FAILs red.

## Run environment

- **Date:** 2026-07-24
- **Machine / interpreter:** Windows, repo venv `.venv/Scripts/python.exe`
- **Python:** 3.12.10
- **Packages:** numpy 2.4.6 · scipy 1.18.0 · matplotlib 3.11.0 · torch 2.11.0+cu128
- Because `torch` is present, **nothing SKIPs** — the neural trainer and all validation checks run.

---

## Phase 2 — Exploration

Ran all four scripts from `implementation/step11/exploration/`. Stdout-only (no artifacts written).

### Run-driven fix
- **`play_sls.py`** crashed in the 200-game aggregate: `np.bincount(np.array(winners), minlength=4)`
  rejects the `-1` winner that the engine returns when a game ends by the documented `max_turns`
  tie-break (`sls_game.py` NOTE (c)). Minimal harness fix (no game-logic change): filter `winner < 0`
  out of the bincount and report a separate `no_winner` count. Re-ran clean.

### Measured vs predicted

| Script | Prediction | Measured | Verdict |
|---|---|---|---|
| `shapley_playground` glove | Shapley `(2/3,1/6,1/6)`, core `{(1,0,0)}` | `[0.6667,0.1667,0.1667]`, core non-empty, alloc `[1,0,0]` | ✅ exact |
| `shapley_playground` majority | Shapley `(1/3,1/3,1/3)`, **empty core** | `[0.3333,0.3333,0.3333]`, core non-empty = **False** | ✅ exact |
| `coalition_by_hand` Q1 (fixed-ally) | pair `{0,1}` combined share > 0.5 | win rates `[0.493,0.243,0.143,0.120]` → pair = **0.736** | ✅ direction |
| `coalition_by_hand` Q2 (betrayer) | betrayer P0 ≥ loyal P1 | `[0.497,0.240,0.143,0.120]` → 0.497 ≥ 0.240 | ✅ direction |
| `play_sls` all-random winners | ~uniform `[50,50,50,50]` | `[94,42,33,31]`, no_winner=0, mean_len 45.2 | ⚠️ **P0-skewed** |
| `play_sls` greedy-capture P0 | "greedy P0 slightly above 50" | `[41,83,42,33]`, no_winner=1, mean_len 62.5 | ❌ greedy HURTS P0 (94→41) |
| `sls_shapley_peek` symmetric | credit ≈ `[0.25]*4` | `[0.593,0.240,0.113,0.053]` | ⚠️ **P0-skewed** |
| `sls_shapley_peek` asymmetric `[8,8,1,1]` | credit concentrates on P0,P1; `v({0,1})≈1` | `[0.687,0.313,0,0]`, `v({0,1})=1.000` | ✅ direction (pair) |

### Findings to carry into Phase 4 (implementation)

1. **Large seat-0 / first-mover advantage (the headline surprise).** Under *symmetric* setups
   (all-random, and equal-chip Shapley positions) Player 0 wins ~47–59% instead of the fair 25%,
   and the skew is monotone in seat order (P0 > P1 > P2 > P3). This is real engine behavior, not a
   harness artifact (three independent scripts agree). **Consequence:** it directly threatens
   validation **check 3**'s "symmetric SLS credit spread < 0.15" (observed spread here ≈ 0.54).
   **§0.1 action:** before accepting check 3's result, investigate the engine turn model — the
   documented simplifications `capturer-plays-next` (NOTE a) and `empty-hand skip` (NOTE b) are the
   prime suspects for compounding first-mover advantage. Treat this as *suspect-a-bug-first*, not a
   prediction miss.
2. **Greedy-capture is a *weak* strategy** — it dropped P0 from 94 to 41 wins and lengthened games
   (45→62 turns). Consistent with the README's own hedge ("capturing feeds you prisoners you must
   then manage"). Good qualitative lesson; capturing ≠ good in SLS.
3. **Cooperative-GT toy results are exact** — the glove/majority Shapley + core reproduce the
   textbook values precisely (fairness vs stability; empty core = structural betrayal), so the
   Shapley machinery itself is trustworthy independent of the SLS seat issue.
4. **Directional coalition lessons survive the seat bias** — the ally pair still concentrates wins
   (0.736) and the betrayer still beats the loyal partner; the strong pair's value ≈ 1. The *magnitude*
   is confounded by seat order, but the form-exploit-break story holds.

---

## Phase 4 — Implementation

Ran the [implementation README](implementation/README.md) runbook from
`implementation/step11/implementation/`. Artifacts: `results/smoke_results.json`, `plots/*.png`
(coalition_timeline, shapley_attribution, spinning_top, coalition_graph). Scale run launched in the
background (see the bottom of this file).

### Module self-tests — 9/9 exit 0

`sls_game`, `sls_endgame`, `state_encoding`, `coalition_detector`, `shapley`, `agents`, `sls_egta`,
`sls_ppo` (torch), `coalition_mappo` (torch) all ran and exited 0. Notes:
- `sls_game` 20-game winners `[11,2,2,5]`, `sls_endgame` mismatches=0, `state_encoding` obs_dim=71 /
  action_dim=44 round-trip OK, `coalition_detector` strongest pair `(0,1,10.0)`, `shapley` reference
  games exact, `agents` zero-sum, `sls_ppo`/`coalition_mappo` finite losses.
- `sls_egta` self-test (tiny pool) already showed transitive `0.783` > cyclic `0.622` — an early
  signal of the check-5 result below.

### `validate.py --config smoke` — 3/5 PASS (11 s)

| # | Check | Result | Verdict |
|---|---|---|---|
| 1 | SLS env (endgame vs engine minimax / termination / zero-sum) | 0 mismatches, terminated, zero-sum | **PASS** |
| 2 | Coalition detection (planted `{0,1}`) | strongest_pair = `[0,1]` | **PASS** |
| 3 | Shapley | glove ✓, majority ✓, asym-dominates ✓, **sym_spread = 0.54 (< 0.15?)** | **FAIL** |
| 4 | Coalition-aware training | shapley_score `0.011` > sparse_score `0.007` (win 0.873 vs 0.863) | **PASS** |
| 5 | Spinning top | **transitive = 0.9976, cyclic = 0.069, cyclic > 50%? No** | **FAIL** |

### Tournament comparison (smoke, `results/smoke_results.json`)

| Method | WinRate vs Random | Coalition Score |
|---|---|---|
| Random baseline | 0.250 | 0.000 |
| MAPPO (sparse reward) | 0.863 | 0.007 |
| MAPPO + Shapley (this step) | 0.873 | **0.011** |

→ **Primary target met (raw L560):** Shapley agents' coalition score > sparse agents'. Win-rate
improvement is marginal (0.873 vs 0.863) and secondary, as the raw step says.

### §0.1 reconciliation of the two red FAILs — shared root cause

Both FAILs trace to the **seat-0 / first-mover advantage** first seen in Phase 2, and I suspect the
engine, not the predictions:

- **The evidence it is structural, not noise:** in `coalition_by_hand` Q1 the *same* fixed-ally
  strategy scored 0.493 in seat 0 vs 0.243 in seat 1; symmetric Shapley positions give
  `[0.593,0.24,0.113,0.053]`; all-random winners `[94,42,33,31]`; 20-game engine self-test `[11,2,2,5]`.
  The advantage is monotone in seat order and independent of strategy → a pure turn-order effect.
- **Mechanism (engine, `sls_game.py`):** NOTE (a) *"capturer plays next"* (line 214) lets a capturing
  player keep the turn, and P0 — always seat 0 (`current_player=0` initial) — gets the first capture
  chances; many games reach `max_turns` and are decided by NOTE (c) the *most-total-chips* tie-break
  (`_most_chips`), which rewards the early-capture accumulator (again P0). These are the exact
  simplifications the README's "Likely to break" list says to reconcile with De Carufel & Jerade
  **first** — "far more likely a rule gap than a solver bug."
- **Why it fails check 3:** a symmetric *position* is not symmetric in *outcome* under a strong
  first-mover edge, so win-prob-share credit spreads to 0.54, not < 0.15. Raising `shapley_rollouts`
  will **not** fix a 0.54 structural spread (this is not MC borderline).
- **Why it fails check 5:** a dominant turn-order advantage makes the meta-game a near-perfect
  *skill ladder* (transitive 0.9976), burying the coalition rock-paper-scissors the step predicts.
  The cyclic signal cannot emerge while seat order dictates ~2× the fair win share.

**Decision (WORKFLOW §0.1 + prior-step precedent):** keep both FAILs **red**. Fixing them requires an
SLS turn-model change (which rule is faithful to the paper — e.g. rotating the start seat, or dropping
"capturer-plays-next") — a substantive design decision that belongs in the human's **consolidation /
engine-reconciliation** pass against De Carufel & Jerade, not a silent threshold tweak here. Step 10
likewise shipped an honest red FAIL. The Shapley machinery and detector themselves are sound (checks
2, 3-reference-games, and the exact toys all pass); the seat bias is upstream of them in the engine.

### Static picture confirmed
No SKIPs (torch present); every suite ran for real. `results/smoke_results.json` + 4 PNGs written.
Smoke training is ~seconds (tiny nets), far under the config's conservative estimate.

### Scale run (`results/scale_results.json`) — the headline does NOT survive scale-up

Ran `tournament.py --config scale` (chips=7, `train_games=6000`, bigger nets, `eval_winrate_games=1000`,
`egta_games_per_cell=300`). It finished in **minutes, not the ~1.5–2.5 h** the config conservatively
predicted — SLS rollouts are light and the nets are small. Plots regenerated with `--config scale`;
since `plotting.py` uses fixed filenames, the committed `plots/*.png` now reflect the **scale** config
(the smoke PNGs were transient); `results/` keeps **both** JSONs.

| Method | WinRate vs Random (scale) | Coalition Score (scale) |
|---|---|---|
| Random baseline | 0.250 | 0.000 |
| MAPPO (sparse reward) | 0.829 | **0.003** |
| MAPPO + Shapley (this step) | 0.827 | **0.002** |

**Check 4 flips to FAIL at scale (§0.1 — a real finding, kept red).** At smoke the Shapley agent's
coalition score beat sparse (0.011 > 0.007); at scale the two collapse into noise and the direction
**reverses** (0.002 vs 0.003 → "Shapley > sparse? **False**"), and both are ~4–5× smaller than at
smoke. This is precisely the risk called out in the README "Likely to break" #4: the training reward
uses `proxy_coalition_values` (a synergy-weighted sum of critic value estimates), **not** the true
counterfactual win-probability, and the proxy is too weak to separate the populations once training is
longer / the game is bigger. So the primary thesis signal (raw L560) is **positive at smoke, null at
scale** — the honest headline. Suspected fixes (deferred to consolidation): use the rollout-based
counterfactual coalition value at lower frequency, or tune `alpha` / the credit normalization.

**Check 5 trends toward the prediction but does not reach it.** Cyclic ratio rises with scale
(`0.069 → 0.308`; transitive `0.998 → 0.951`), i.e. a richer trained population injects more
non-transitivity — the direction raw L561 predicts — but the meta-game is **still transitive-dominant**,
because the seat-0 skill-ladder (above) dwarfs the coalition cycling. Check 5 stays **red**.

**Net.** Two independent effects compound: (i) the engine seat-0 bias (checks 3 & 5), and (ii) the
proxy-Shapley weakness (check 4 at scale). Both are documented, reproducible, and left as genuine
findings for the engine-reconciliation + credit-signal work in consolidation — no thresholds were
tweaked and no FAIL was silenced (WORKFLOW §0.1).

---

## Phase 4 refinement — de-confounding checks 3 & 5 (root cause found + fixed)

### The seat-0 bias was a tie-break artifact, not first-mover order
Diagnostic runs (chips=5, 4000 rollouts each) established:
- **The dynamics are symmetric.** Mean end-chips per seat are flat: `[4.236, 4.245, 4.249, 4.247]`.
- **~99.5% of random games end by DEADLOCK** (all alive players have empty hands; `_next_with_chips`
  returns `None`) at ~28 turns — *not* by elimination and *not* by `max_turns` (raising `max_turns`
  200→5000 changed nothing). The winner is therefore `_most_chips`, and chips are near-tied, so
  almost every game is decided by the **tie-break**.
- **The old `_most_chips` broke ties by lowest index** (`total > best` scan), handing seat 0 ~2× its
  fair share. `rotate_start` on the win-prob rollouts made **no** difference (bias isn't first-mover);
  a deterministic salt (`turn_count`) also failed (with 4 players cycling it stays index-correlated).

### Fix: an unbiased *random* deadlock tie-break, threaded through the engine
`sls_game.apply(..., rng=None)` now forwards an optional rng to `_most_chips`, which draws the tied
winner **uniformly** when an rng is supplied (the play/eval/train paths pass theirs: `play_game`,
`win_prob_coalition_values`, `coalition_mappo._play_and_record`). The exact 2-player **endgame
minimax stays deterministic** (no rng → salt fallback), and `verify_endgame_consistency` was switched
to a deterministic optimal-vs-optimal rollout so it matches the minimax tree (otherwise the new random
tie-break spuriously disagreed with minimax on coin-flip positions — that briefly showed as 12 endgame
mismatches before the fix).

### Results (`validate.py --config smoke`): 3/5 → **4/5 PASS**
- **Check 1 env: PASS** (0 endgame mismatches preserved; termination + zero-sum intact).
- **Check 3 Shapley: FAIL → PASS.** Symmetric credit `[0.247,0.257,0.253,0.243]`, spread
  **0.54 → 0.013**; asymmetric strong-pair dominance still holds. All-random winners are now uniform
  (`[0.251,0.238,0.251,0.260]`, spread 0.022).
- **Side effect — win rates de-inflated.** Hero-vs-random win rate fell from ~0.87 to ~0.41, i.e. the
  earlier 0.87 was itself a seat-0 tie-break artifact (hero always sat in seat 0). The fair number is
  ~0.41 (vs 0.25 random floor).
- **Check 4 training: PASS at smoke** (shapley 0.004 > sparse 0.001) — but tiny/single-seed; the
  Part-2 sweep characterizes it properly.

### Check 5: coalition pool surfaces a large cyclic component (still honestly red)
The matchup already de-seats (shuffles seats), so check 5's transitivity was **pool composition**:
`default_baseline_pool` is a skill ladder. Added `coalition_pool()` = ally-different-partner strategies
(`fixed_ally_1/2/3` + `betrayer_1` + `random`); `validate` check 5 now uses it. Measured cyclic ratio:
- original single-agent baseline: **~0.07**; skill-ladder baseline pool: **~0.32**;
- **coalition pool: ~0.57 (60 games/cell) to ~0.69 (200 games/cell)** — a large non-transitive
  component, strongly confirming raw L561's *direction* (FFA coalition dynamics are substantially
  cyclic), but **just under the strict >50%-dominance threshold** (cyclic² ≈ 0.48 < 0.5; transitive
  still marginally larger). **Kept red — the pool was not tuned to cross the line.** Honest finding:
  coalition strategies make SLS meaningfully non-transitive, near-balanced, but not cyclic-*dominant*
  at this scale; the residual likely reflects the 2-type projection discarding 3-/4-player coalition
  effects (raw L600 open confusion) — a consolidation-level question.

Self-tests for all touched modules (`sls_game`, `sls_endgame`, `shapley`, `agents`, `evaluation`)
still exit 0.

---

## Phase 4 investigation — WHEN do coalitions emerge? (the `sweep.py` grid)

To settle whether "coalitions don't emerge from proxy-Shapley at scale" was a real effect or a
single-seed/mis-tuned artifact, `sweep.py` runs a **5-seed paired** grid over
`alpha × credit_mode × synergy` at two tiers, reporting the paired gap
`gap = coalition_score(shapley) − coalition_score(sparse)` with error bars (`results/sweep_*.json`,
`plots/sweep_coalition_gap.png`). A new `credit_mode="counterfactual"` (win-probability-share Shapley,
refreshed per batch under the current policies) was added to test the README's #1 suspected fix.

### Headline cells (5 seeds; `**` = mean gap > 2·SE)

| tier (chips/games) | credit | alpha | synergy | gap (shapley−sparse) | sig |
|---|---|---|---|---|---|
| **scale** (7 / 1500) | proxy | **0.0** | 0.3 | **+0.0376 ± 0.0103** | ** (≈4.4× sparse) |
| scale | proxy | 0.0 | 0.1 | +0.0305 ± 0.0130 | ** |
| scale | counterfactual | 0.0 | – | +0.0128 ± 0.0026 | ** |
| scale | counterfactual | 0.1 | – | +0.0036 ± 0.0016 | ** |
| scale | proxy | 0.1 | 0.1 | +0.0023 ± 0.0011 | ** |
| scale | *any* | ≥0.3 | * | −0.001 … −0.004 | – (negative) |
| smoke (5 / 400) | proxy | 0.0 | 0.1 | +0.0024 ± 0.0008 | ** (tiny) |
| smoke | *any* | ≥0.3 | * | ~0 … −0.003 | – |

(sparse baseline coalition score: smoke 0.0073, scale 0.0109.)

### Findings — this OVERTURNS the earlier "coalitions don't emerge at scale" read
1. **`alpha` is the dominant knob, and the earlier default was in the dead zone.** Coalitions emerge
   (significantly, up to **~4.4× the sparse baseline**) **only at low `alpha`** (≈0, i.e. heavy weight
   on the coalition credit). At **`alpha ≥ 0.3` the gap is negative** in *every* cell — the sparse
   winner-takes-all term suppresses the coalition signal. The original single-config runs used the
   default **`alpha=0.3`**, which is exactly the suppressed regime — that, not a fundamental failure,
   is why check 4 looked null/flippy.
2. **The effect GROWS with game size, opposite to the naive read.** At smoke (chips=5) every gap is
   tiny (≤0.003); at scale (chips=7, longer training) the low-`alpha` gaps are ~10× larger (~0.038).
   The earlier "smoke-positive / scale-null" was an artifact of holding `alpha=0.3` at both — at
   `alpha=0`, **scale ≫ smoke**.
3. **The expensive counterfactual credit is NOT required.** The counterfactual arm is positive and
   significant at low `alpha` (validating it works), but the **cheap critic-value proxy at `alpha=0`
   is the *larger* signal** (+0.038 vs +0.013 at scale), and higher `synergy` (0.3) helps at the
   extreme. So the fix is "weight the coalition credit heavily", not "compute a truer credit."
4. **Coalitions vs winning is a genuine trade-off.** Pure coalition credit (`alpha=0`) drops win-rate
   to ~0.29 (near the 0.25 random floor); moderate `alpha` keeps win-rate ~0.52. This matches raw
   L560 (coalition-*forming* is the primary target, winning secondary) — you buy coalition behavior
   with competitive performance.

### Recommendation (for consolidation, not silently applied)
Lower the training-blend default from `alpha=0.3` toward `alpha≈0.05–0.1` if the goal is coalition
formation — evidence-based, but a config/design choice left to the human. The `alpha=0.3` default and
its (honest) marginal check-4 result are unchanged here (WORKFLOW §0.1: report, don't rig).

**Net after the whole refinement:** the two check-3/5 FAILs were traced to a real engine artifact and
fixed (check 3 now PASS; check 5 hugely improved, honestly still red under strict dominance), and the
check-4 "coalitions don't emerge" question is answered: **they do — robustly and significantly — in the
low-`alpha`, larger-game regime; the earlier null was a mis-set blend weight.**
