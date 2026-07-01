<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->

# Step 07 — Opponent Modeling: Implementation-Phase Report

**Environment:** July 2026
**Games:** Kuhn Poker (3-card) and Leduc Hold'em (6-card, 2 rounds) — both exact-solvable, imported from Steps 02/03
**Phase covered:** Phase 4 (Implementation) — the full Bayesian opponent-modeling + adaptive-exploitation build
**PhD connection:** First half of **Contribution #1 (Behavioral Adaptation Framework)** — the *sensor* (the opponent model) plus a first *actuator* (safe adaptive exploitation), which Step 08 formalizes.
**Status:** Validated — `validate.py` **8/8 PASS**; the full **`scale`** tournament ran end-to-end on both games (Kuhn 102 s, Leduc 22 min; 5 seeds, 20k-hand matches, 200k/40k-iter Nash). Two correctness bugs and one tractability problem were found and fixed during execution. OpenSpiel cross-check skipped (no `pyspiel` on this Windows environment). All numbers below are from the scale run unless noted.

> **Note on process.** Per `implementation/WORKFLOW.md`, this code was *written but never run* by the agent that authored it. This report covers **running, debugging, and validating** it. Every number below is a **measured result** from a real run on this machine.

---

## 1. What was built

One uniform interface — *consume observed hands → emit a predicted opponent policy* — with **three opponent models** behind it, an **adaptive exploiter** that best-responds to the model (with a Nash safety blend and optional change-point forgetting), and a **validation harness** + **tournament** that measure everything against exact analytical yardsticks.

| Component | What it is |
|---|---|
| `engines.py` / `policies.py` | Uniform `Game` adapter over the Kuhn & Leduc engines; the `policy → {action: prob}` currency; `replay` for partial-observability reasoning. |
| `opponent_types.py` / `level_k.py` | The type "zoo" per game + Nash + Random + Level-k cognitive-hierarchy opponents. |
| `observation_buffer.py` / `inference.py` | The single home of **partial observability** — marginalizing the opponent's hidden card over consistent deals; the eps-smoothed marginal log-likelihood. |
| `type_based_model.py` | Dirichlet-multinomial posterior over K types; MAP type + model-averaged policy. |
| `continuous_model.py` | Per-information-set Dirichlet estimate (showdowns → hard counts, folds → soft/EM counts). |
| `consistent_model.py` | **Ganzfried (2025)** sequence-form MAP via a SciPy convex solve. |
| `best_response.py` / `nash.py` | Exact info-set-constrained best response and `nash_gap` (=NashConv); CFR Nash baseline. |
| `adaptive_exploiter.py` / `changepoint.py` | observe→model→BR→act loop with a Nash safety blend and Bayesian online change-point detection. |
| `validate.py` / `tournament.py` / `plotting.py` | The verification harness (PASS/FAIL vs the raw step's targets) and the headline experiment + plots. |

The three models share one exact best-response, so exploitation is compared apples-to-apples; every learning curve is bounded by an **exact** `nash_ev` (equilibrium can't be exploited) and `ceiling` (true best-response value).

---

## 2. Correctness — `validate.py` (8 / 8 PASS)

| Check | Result |
|---|---|
| Kuhn Nash value (−1/18) | `exact_value(Nash,Nash) = −0.0556` ✓ |
| Kuhn Nash unexploitable | `NashConv = 0.0020` (< 0.05) ✓ |
| BR beats uniform (both games) | Kuhn +0.500, Leduc +2.087 ✓ |
| Type-based detection | posterior[true] = 1.000, MAP correct ✓ |
| Continuous recovers strategy | mean TV = 0.016 (< 0.15) ✓ |
| Consistent recovers strategy | P(BET\|King) = 0.987 (> 0.75) ✓ |
| Exploiter beats Nash, under ceiling | realized +0.165, nash_ev −0.047, ceiling +0.167 ✓ |
| Change-point helps non-stationary | post-switch: static −0.181, changepoint **+0.211** ✓ |

The exact Nash checks (value = −1/18, NashConv ≈ 0) stand in for the OpenSpiel cross-validation, which is unavailable here.

---

## 3. Detection — who is the opponent?

Both games, all types. **Type-based detection is essentially perfect**: the posterior concentrates fully on the true type and the MAP is correct (total-variation distance 0.000) — with **one instructive exception**. On Kuhn the higher Level-k opponents collide: Level-2 and Level-3 converge to the *same* behavioral policy, so the type posterior splits 0.50/0.50 between them and the MAP for the true Level-3 lands on Level-2 (wrong). This is not a bug — two types that play identically are genuinely indistinguishable *by their actions*, which is exactly what a type detector reasons over. The **continuous** and **consistent** models, which estimate the actual policy rather than a label, recover both cleanly (TV ≈ 0.005).

The **continuous** model's mean TV to the truth is small on Kuhn (0.006–0.030) but larger on Leduc (0.11–0.36) — as predicted: Leduc has far more information sets and heavier partial observability, so a free-form per-info-set estimator needs many more hands to converge; rarely-visited info sets dominate the residual error. The **consistent** model (Kuhn detection) matches or beats the continuous model's recovery (TV ≈ 0.004–0.021), as its sequence-form MAP is designed to.

---

## 4. Exploitation — how much does modeling win?

Realized mean profit per hand over 20k-hand matches (×5 seeds) against the exact best-response **ceiling**. The type-based model tracks the ceiling almost exactly on both games; the continuous model matches it on Kuhn and tracks close on Leduc, sitting a little below for the hardest-to-fit types (undersampling, as in §3). *(The consistent model refits a convex program and is impractical in a per-refit online match, so exploitation uses type-based + continuous; the consistent model is evaluated where its strength lies — recovery/detection. See §6.)*

**Kuhn** (ceiling / type-based / continuous):

| Opponent | ceiling | type-based | continuous |
|---|---:|---:|---:|
| AlwaysPass | 0.975 | 0.966 | 0.966 |
| AlwaysBet | 0.333 | 0.335 | 0.335 |
| LooseAggressive | 0.333 | 0.337 | 0.330 |
| TightPassive | 0.167 | 0.168 | 0.168 |
| **Nash** | −0.055 | −0.055 | −0.053 |

**Leduc** (ceiling / type-based / continuous):

| Opponent | ceiling | type-based | continuous |
|---|---:|---:|---:|
| Level1 | 3.056 | 3.061 | 2.672 |
| Maniac | 2.177 | 2.199 | 2.038 |
| CallingStation | 1.464 | 1.451 | 1.434 |
| Rock | 0.937 | 0.912 | 0.848 |
| **Nash** | −0.083 | −0.085 | **−0.175** |

![Exploitation vs opponent type (Leduc, scale): type-based (blue) hugs the exact BR ceiling for every type; continuous (orange) tracks close but sits below for the hardest-to-fit types; both drop below zero against Nash.](figures/impl_exploitation_leduc.png)

Two results carry the thesis message:

1. **You cannot exploit an equilibrium.** Against the Nash opponent every model earns ≈ the (negative) Nash EV, never more — the exact ceiling is essentially the game value. This is the sanity check that the exploitation is *real* and not an artifact.
2. **A confident-but-underfit model makes you exploitable.** On Leduc the continuous model *loses* to Nash (−0.175 vs the −0.083 ceiling) — with imperfect data it best-responds to a *wrong* estimate of an unexploitable opponent, opening a leak in its own play. (At the smaller smoke sample this was a starker −0.40; more data shrinks but does not remove it.) This is the exploitation-vs-safety tension made concrete, and the direct motivation for Step 08's safe (KL-regularized) exploitation.

---

## 5. Non-stationarity — the two-sided finding

The opponent switches style mid-match; we compare a **static** continuous model against one with **change-point forgetting** (detect a style change → reset the model → drop to safe play → re-learn). The result is **scenario-dependent**, which is itself the finding:

| Game | Switch (at hand 10k of 20k) | static (after switch) | change-point (after switch) |
|---|---|---:|---:|
| Kuhn | TightPassive → LooseAggressive | **−0.116** | **+0.226** |
| Leduc | Rock → Maniac | **+1.940** | **+0.525** |

![Non-stationarity (Kuhn): after the switch the static model bleeds (exploiting a phantom), while change-point detection resets and recovers.](figures/impl_nonstationarity_kuhn.png)

![Non-stationarity (Leduc): here the static model wins — the Maniac is so exploitable that continuous adaptation captures it, and the detector's false-positive resets cost more than they save.](figures/impl_nonstationarity_leduc.png)

- **Kuhn — change-point wins.** The stale anti-rock strategy (bluff-heavy) *actively loses* to the new maniac (who calls everything), so the static model goes negative; detecting the switch and re-learning recovers to +0.20.
- **Leduc — change-point loses.** The maniac leaks 2+/hand, so the continuously-adapting static model exploits it well without any reset; meanwhile the detector fires several **false positives** during the stable phase (visible as the reset dips in the plot), each dropping to safe play and discarding data.

**The lesson:** change-point forgetting rescues you exactly when a stale model is *harmful*, but its naive form — a low-signal Bernoulli detector that occasionally false-triggers, plus a full reset-to-safe on every detection — can underperform simple continuous adaptation when the new opponent is exploitable enough that staleness costs little. Cheaper reactions (partial forgetting instead of a hard reset; a lower false-positive rate) are the obvious next step, and a clean motivation for the thesis's non-stationarity thread.

---

## 6. Bugs found and fixed (first-execution engineering record)

Two correctness defects and one tractability problem in the written-but-never-run code, plus cleanups:

1. **Change-point detection was inert.** The exploiter reacted only when `changepoint_prob(window=3) > 0.5`, but that posterior mass **peaks at ≈ 0.37** after a real switch (the detection-lag mass concentrates around run-length ≈ 6, *outside* a width-3 window), so it **never fired** — the whole non-stationarity feature was dead. Fixed by keying on the **MAP run-length collapse** (150+ → ≈6 at detection), the standard BOCPD signal. This is what makes §5 (and validate.py's change-point check) meaningful.
2. **Leduc non-stationarity crashed** (`KeyError: 'TightPassive'`) — the config hard-coded Kuhn type names for the switching opponents, absent from the Leduc zoo. Fixed with **game-specific** opponents (Kuhn: TightPassive→LooseAggressive; Leduc: Rock→Maniac).
3. **The consistent model made `scale` intractable.** In the exploitation loop it refits a convex program *every 200 hands over a growing buffer up to 20k hands* — measured fit time grows ~0.3 s → 3.2 s (N = 200 → 6000), extrapolating to a match cost of ~15 min × 50 matches ≈ 12 h on Kuhn (and worse on Leduc). The first scale run hung on the first such match for 24 min and was killed. **Resolution:** the consistent model is evaluated where its Ganzfried-2025 strength lies — **recovery (detection)** — and left out of the online exploitation loop (which type-based + continuous already characterise against exact ceilings). Detection runs it on Kuhn (one bounded solve per item); Leduc consistent detection is deferred (its sequence-form program is large).
4. **Cleanups & run infrastructure:** silenced benign SciPy solver warnings (singular constraint Jacobian / locally-linear objective — handled correctly, result validated); git-ignored the Nash CFR cache and run logs; and added tournament observability/robustness — a 30 s progress heartbeat, a resumable checkpoint (per-item, incl. per-seed, flushed every 5 min so a crash resumes rather than restarts), and a timestamped tee'd log file.

Per WORKFLOW §0.1, each mismatch was traced to a real cause before being called correct-or-fixed.

---

## 7. Scope, limits, and what's left

- **Consistent-model *exploitation*** is intentionally not measured (§6.3); its recovery is reported in detection. If its exploitation curve is wanted, a Kuhn-only coarse-refit-cadence variant is the tractable way to get it (≈ +1 h; expected to roughly track the continuous model).
- **Leduc consistent detection** is deferred — the sequence-form convex program is large, so a one-shot solve per (type, seed) is slow. A single-seed Leduc pass is the cheap way to add the data point.
- **OpenSpiel cross-check skipped** — `pyspiel` does not install cleanly on this Windows environment; the exact internal Nash checks (value = −1/18, NashConv ≈ 0) substitute.
- **Change-point false-positive rate** (§5) is the clearest quality gap and a genuine research hook (partial forgetting instead of a hard reset; a less trigger-happy detector), not a blocker.

---

## 8. Reproduction

```bash
# From implementation/step07/implementation/ , with the repo .venv active (needs numpy, scipy, matplotlib):

python validate.py                         # 8/8 PASS
python tournament.py --config smoke         # Kuhn quick pass (~3 s)
python tournament.py --config scale         # full headline run: Kuhn ~2 min, Leduc ~22 min
python tournament.py --config scale --fresh # ignore any checkpoint and recompute from scratch

# individual model/plumbing self-tests each have a __main__ (e.g. python changepoint.py)
```

A long run prints a timestamped progress line per work-item plus a 30 s heartbeat, tees everything to `logs/tournament_<config>_<startdate>.log` (git-ignored), and checkpoints partial results to `_cache/tournament_<config>.ckpt.json` — so an interrupted run **resumes where it left off** on the next invocation. Results write to `results/*.json`; plots to `plots/*.png`. *Figures reproduced in this report (prefixed `impl_`) are copied to `deliverables/reports/step07/figures/`.*
