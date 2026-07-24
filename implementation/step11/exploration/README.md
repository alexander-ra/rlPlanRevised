# Step 11 — Exploration: play So Long Sucker, feel coalitions, compute Shapley before the theory

Phase 2 of Step 11. Small, fast, **seeded** experiments that build intuition by *running and
tinkering*. Everything is written to be run by you — **none of it has been executed here** (see
[`../../WORKFLOW.md`](../../WORKFLOW.md)). Every "PREDICT"/"expected" number below is a
**prediction to verify**, not a measured result.

The two SLS scripts reuse the **shared engine** in [`../implementation/sls_game.py`](../implementation/sls_game.py)
through a tiny `sys.path` shim ([`_bootstrap.py`](_bootstrap.py)) — no rules are re-implemented
here (WORKFLOW §6). The toy-cooperative-game script is pure numpy and needs no bootstrap.

---

## How to run

From this folder (`implementation/step11/exploration/`):

```bash
python play_sls.py            # trace a game + help/harm tally + aggregate stats
python coalition_by_hand.py   # fixed-ally vs betrayal vs random win rates
python shapley_playground.py  # Shapley + core on the glove & 3-player-majority games
python sls_shapley_peek.py    # Shapley credit (= win-prob share) on hand-set SLS positions
```

- **Dependencies:** Python 3.10+ and `numpy` for everything. `scipy` is optional — used only by
  `shapley_playground.py`'s core-feasibility LP (without it the analytic core answers print as
  targets). No `torch` needed in this phase.
- **Working dir:** run from *this* folder so `_bootstrap` / the engine import cleanly.
- **Runtime:** `play_sls` and `coalition_by_hand` are seconds; `shapley_playground` is instant;
  `sls_shapley_peek` is a few seconds (16 coalition subsets × a few hundred rollouts per state).

---

## Files

| File | Role |
|------|------|
| [`_bootstrap.py`](_bootstrap.py) | Puts `../implementation` on `sys.path` so `sls_game` / `sls_endgame` import. Import first in the SLS scripts. |
| [`play_sls.py`](play_sls.py) | Play SLS (random + greedy-capture); print a turn trace, the **help/harm** tally (the raw coalition signal), and aggregate length/winner stats. raw L87-105 |
| [`coalition_by_hand.py`](coalition_by_hand.py) | Hand-coded **fixed-ally** and **betrayer** strategies: does an alliance beat random? does betrayal beat a loyal ally? raw L106-110 |
| [`shapley_playground.py`](shapley_playground.py) | Shapley value + the **core** on the glove game and the 3-player majority game — fairness vs stability, with known answers. raw L112-152 |
| [`sls_shapley_peek.py`](sls_shapley_peek.py) | Shapley credit on hand-set SLS positions, using **coalition value = P(a member wins)**. raw L154-159 |

---

## 1. `play_sls.py` — see the coalition signal in the moves

**What it does.** Traces one random game move-by-move (marking every `[HELP Pj]` — a player
placing another's chip — and every `[CAPTURE]`), then tallies `help[i][j]` / `harm[i][j]` over a
game, then aggregates length + winner counts over 200 games for two policy fields.

**Knobs.**

| Knob | Effect | Try this |
|---|---|---|
| `seed` (trace) | which game you watch | bump it to see different elimination orders |
| policy field | random vs greedy-capture | compare win_counts to see if capturing helps |
| `chips_per_player` (in `main`) | game length / richness | 4 → short games; 10 → longer, more captures |

**Watch out.** With **random** policies the help/harm matrices are roughly symmetric noise — there
is *no real coalition* yet; that is the point (raw L104: basic play shows no coalition concept).
Do not read structure into random tallies.

**How to read it.** Winner counts should be ~uniform `[50,50,50,50]` for all-random (PREDICT).
Greedy-capture for P0 should nudge P0 above 50 — *if* immediate capturing is actually good in SLS,
which is itself worth checking (it may not be, since capturing feeds you prisoners you must then
manage). Runtime: seconds.

## 2. `coalition_by_hand.py` — alliances pay, then get betrayed

**What it does.** Runs two 4-player fields: (Q1) P0 and P1 each play `fixed_ally` toward the other
vs two random players; (Q2) P0 is a `betrayer` (allies P1 early, turns on P1 at the halfway turn)
against a *loyal* P1 and two random players.

**Knobs.**

| Knob | Effect | Try this |
|---|---|---|
| `ally` | who a strategy supports | make a 3-way alliance {0,1,2} vs P3 |
| `switch_frac` (betrayer) | when the knife comes out | 0.3 (early betrayal) vs 0.8 (late) |
| `n_games` | win-rate precision | 1000 for tighter estimates |

**Watch out.** The heuristics are crude (greedy scoring, random tie-break); they demonstrate the
*direction* of the effect, not optimal play. A single seed can mislead — use `n_games` ≥ 300.

**How to read it.** PREDICT: in Q1 the pair {P0,P1} takes a **combined** share > 0.5 (the alliance
concentrates wins on its members). In Q2 the **betrayer ≥ the loyal ally** — exploiting then
breaking a coalition beats being the naive partner (raw L110). The lesson is behavioral; exact
splits are to verify. Runtime: seconds-to-a-minute.

## 3. `shapley_playground.py` — fairness (Shapley) vs stability (core)

**What it does.** Computes the exact Shapley value (all `n!` orders) and tests core non-emptiness
(a feasibility LP) on two games with textbook answers.

**Knobs.**

| Knob | Effect | Try this |
|---|---|---|
| `value_function` | which game | write a 4-player weighted-majority game |
| add a 3rd right glove | scarcity | player 0 becomes less scarce → Shapley shifts |

**Watch out.** `math.factorial` cost is `n!` — fine to `n≈8`, do not push large. Core LP needs
`scipy`; without it the script prints the analytic targets instead of solving.

**How to read it.** Glove: Shapley `(2/3, 1/6, 1/6)`, core `= {(1,0,0)}` — **fairness and stability
disagree**. Majority: Shapley `(1/3,1/3,1/3)`, core **empty** — the SLS-relevant lesson (raw
L325-326): a purely competitive/simple game has no stable allocation, so coalitions *will* be
betrayed. Runtime: instant.

## 4. `sls_shapley_peek.py` — Shapley credit on real positions

**What it does.** For a hand-set SLS position, estimates `v(S) = P(winner ∈ S)` by random rollouts
for all 16 subsets, then Shapley-decomposes it into a per-player **credit** (a share of the
win-probability, summing to 1).

**Knobs.**

| Knob | Effect | Try this |
|---|---|---|
| `chip_counts` (in `_state_with_hands`) | position asymmetry | `[8,8,1,1]` vs `[5,5,5,5]` |
| `n_rollouts` | estimate noise | 100 (fast/noisy) → 2000 (tight) |
| `seed` | rollout draw | vary to see the Monte-Carlo variance |

**Watch out.** `v(S)` is a **noisy** Monte-Carlo estimate; low `n_rollouts` can even make Shapley
credits slightly negative from noise. Read the **ranking**, not the digits. This is the *toy*
version — the implementation uses learned values + counterfactual coalition values.

**How to read it.** Symmetric position → credits ≈ `[0.25]*4`. Asymmetric `[8,8,1,1]` → credit
concentrates on P0, P1, and the pair value `v({0,1}) ≈ 1`. This matches the raw validation target
(raw L559): symmetric → equal credit; asymmetric → the strong pair gets high mutual credit.
Runtime: a few seconds.

---

## Key takeaways for the final summary

- **The coalition signal is literally in the moves.** `help[i][j]` (placing j's chip) and
  `harm[i][j]` (capturing j's chips) are the raw observables; with random play they are noise —
  structure only appears with strategy. This is exactly what the detector formalizes.
- **Alliances pay and then break.** A fixed alliance concentrates wins on its members (combined
  share > fair 0.5-ish), and a betrayer beats a loyal partner — the form-exploit-break cycle, seen
  before any learning. (Directions to verify; digits are heuristic-dependent.)
- **Shapley = fairness, core = stability, and they diverge.** Glove game shows the split; the
  3-player majority game shows an **empty core** — the SLS prediction: no stable coalition, so
  betrayal is structurally guaranteed.
- **Shapley credit on SLS positions is win-probability share.** Symmetric → equal; asymmetric →
  concentrated on the strong pair — the credit signal the coalition-aware trainer will learn from.
