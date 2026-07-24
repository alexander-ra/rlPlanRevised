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
