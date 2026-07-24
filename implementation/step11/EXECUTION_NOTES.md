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
