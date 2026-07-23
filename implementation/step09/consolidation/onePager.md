# Step 09 — Consolidation (internal weave)

> Phase 5 of Step 09. Written **after** the code was executed, from **verified** run artifacts
> only (`implementation/step09/implementation/results/{smoke,scale}_results.json` and
> `exploration/figures/*.json`). This is the internal weave of the per-phase "Key takeaways";
> the externally-shared write-up is `deliverables/reports/step09/`.

---

## The one-sentence step

Multi-agent RL is single-agent RL where **the environment is also learning**, so the whole
step is a tour of the structural fixes for that non-stationarity — independent learning (the
control that fails), CTDE (centralize the critic at training only), PSRO (bring game theory to
a *population*), communication (learn a channel), and LOLA (differentiate through the
opponent's update) — validated on small exact testbeds against ground-truth equilibria.

---

## What each experiment actually showed (measured)

| Experiment | Prediction | Measured (scale unless noted) | Verdict |
|---|---|---|---|
| Matrix — PD | mutual defection | NashConv `0.00126`, x→[0,1] | confirmed |
| Matrix — Stag Hunt | a pure NE (init-dependent) | all seeds → **Hare** (risk-dominant), NashConv `0.00126` | confirmed (+ note: always risk-dominant) |
| Matrix — Battle of the Sexes | a pure NE (init-dependent) | all seeds → one pure NE, NashConv `0.00127` | confirmed (+ note: no seed diversity) |
| Matrix — Matching Pennies | orbit around (½,½) | **no last-iterate convergence**; softmax learner drifts to corners (NashConv 1.4–1.8), IGA (exploration) spirals **outward** (radius `0.30→0.48`) | lesson holds, mechanism differs (§0.1) |
| Self-play (Kuhn, exploration) | average → Nash, last iterate cycles | avg NashConv `0.24→0.031`; last-iterate oscillates `0.33–0.83` | confirmed |
| PSRO — Kuhn | exploitability → 0 | `0.917 → ~2e-16` by round 6 | confirmed |
| PSRO — matrix (MP) | → 0 | `2.0 → 0` by round 2 | confirmed |
| PSRO — RPS (exploration) | → uniform, exploitability → 0 | mixture → `(.335,.336,.329)`, exploitability `2.0→0.017` | confirmed |
| PSRO — Leduc | `< 0.5` within 20 iters | `4.75 → 2.16`, decreasing but **» 0.5** | contradicted; genuine slow convergence (§0.1) |
| PSRO — Goofspiel | non-increasing | K=3 `1.33→0`; **K=4 oscillates `1.4↔2.0`** | K=3 confirmed; K=4 anomaly, to investigate (§0.1) |
| CTDE — critic variance | central « independent | central `3.2e-11` vs indep `0.077` | confirmed (only at scale) |
| CTDE — climbing game | CTDE → optimum 11, beats IL | none reach 11; **MADDPG `5` < IL `7` = MAPPO `7`** | contradicted; honest negative (§0.1) |
| Communication (CommNet) | ON » OFF (≈1/K) | ON `0.795` vs OFF `0.204` (ceiling `0.2`) | confirmed (only at scale) |
| LOLA (IPD) | naive~1, LOLA~3 | naive `1.04`, LOLA `2.82` | confirmed (direction; ~2.8 not 3) |

---

## The five reconciliations (kept predictions + what really happened)

1. **Matching Pennies never settles — by two different routes.** The exploration IGA learner
   and the implementation softmax learner both fail to converge in the *last* iterate, but one
   spirals outward and the other drifts to the corners; neither is the clean constant-radius
   orbit first imagined. The lesson (non-stationarity ⇒ no last-iterate convergence; the
   *time-average* is the thing that converges) is intact and is exactly why PSRO uses a
   meta-Nash mixture rather than the last policy.

2. **PSRO on Leduc converges, but slowly.** Exact-BR double oracle drives Kuhn to machine zero
   in 6 rounds; on the far larger Leduc tree, 20 rounds only reach exploitability ~2.16 (from
   ~4.75). The "< 0.5 in 20 iters" target was optimistic for a pure-strategy population; the
   monotone-ish downward trend is the real, correct behavior.

3. **Goofspiel K=4 is the one anomaly.** K=3 converges to 0 cleanly; K=4 oscillates between
   ~1.4 and ~2.0 and does not settle. Documented, not fixed (per the chosen path). Prime
   suspects for a future session: `psro_goofspiel` never de-duplicates best responses, and a
   pure-BR population may be too weak to represent the mixed meta-Nash of the larger game.

4. **A centralized critic alone does not solve the climbing game.** None of IL / MADDPG /
   MAPPO escape the –30-penalty trap to the optimum 11; worse, MADDPG (5) *underperforms* IL
   and MAPPO (7). The CTDE-variance claim (central critic has near-zero residual) is separately
   confirmed on CoopSignal — so the honest split is: **CTDE reduces critic variance, but that
   is not sufficient to overcome hard-exploration/relative-overgeneralization**, and the
   MADDPG counterfactual-baseline actor deserves scrutiny next.

5. **Smoke hides the two neural effects.** At smoke sizes the critic-variance gap and the
   communication benefit are both invisible (comm ON=OFF=`0.24`; critic losses near-equal);
   only the scale config reveals them. Methodological lesson: report the trained-to-convergence
   config for the neural claims.

---

## Threads handed to the deliverables / next steps

- PSRO is the game-theory ↔ MARL bridge and the empirical backbone of the step (Kuhn = clean,
  Leduc = the scaling wall, echoing Step 08's global-vs-local finding).
- Two flagged code items (Goofspiel K=4 oscillation; MADDPG < IL on climbing) — investigate
  before reusing those two pieces in later steps.
- Thesis hooks confirmed: LOLA = *dynamic* opponent modeling (Contribution #1); PSRO's
  meta-game = evaluation methodology (Contribution #3); the missing N>2 minimax anchor
  (Contribution #2) is stated but untouched here.
