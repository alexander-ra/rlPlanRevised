# Step 10 — Execution Notes (dev log)

**What this is.** Step 10's code was authored but never run ("every number is a prediction to
verify", WORKFLOW §0). This file records the actual execution: measured-vs-predicted, bugs +
minimal fixes, and observations. **Consolidation (Phase 5) and the EN/BG reports are
deliberately left to a later session** — this is raw dev observation, not the write-up.

Run env: repo `.venv` (Python 3.12); numpy 2.4.6, scipy 1.18.0, torch 2.11.0+cu128 (CUDA
present but **unused** — the neural code has no `.to(device)`; the Leduc MLPs are tiny so it
runs on CPU, which is the right call for nets this small). matplotlib 3.11.0. Scripts run from
their own phase folder per the `sys.path`-shim contract. Date: 2026-07-24.

Status: **Phase 2 (Exploration) and Phase 4 (Implementation) executed.** `validate.py` =
**5 PASS / 1 FAIL**, where the one red is a *deliberately-preserved negative finding* (see
Phase 4). No prior-step (07/09) code was touched; all edits are Step-10-only.

---

## Phase 2 — Exploration: 4 scripts (all predictions hold; no bugs)

Run from `implementation/step10/exploration/`. Artifacts: `figures/` — 4 JSON + 3 PNG
(`psro_population_peek` is JSON-only by design — it has no plotting code, so "4 PNG" in the plan
was an over-count, not a missing artifact).

| script | measured | vs prediction |
|---|---|---|
| `replicator_playground` | PD→[0,1] Defect; Hawk-Dove→p(Hawk)=0.500; RPS→orbit final≈[0.24,0.35,0.41] (never converges); Stag Hunt→[1,0] / [0,1] by start | ✅ all four exact |
| `psro_population_peek` (Leduc, reuses Step09 PSRO + Step07 engine) | exploitability 4.75→3.57 over 10 rounds (bounces up to 6.83 mid-way); ACTIVE in meta-Nash **5/11**; effective size 3.03; Hodge transitive ratio **0.4531** | ✅ trends down (non-monotone — same slow/bouncy exact-PSRO-on-Leduc wall as Step 08/09); few policies active (diversity problem); Leduc leans transitive |
| `game_landscape` | RPS ratio **0.0** / 1 3-cycle / rotational disc; skill ladder ratio **1.0** / 0 cycles / points on a line; PSRO-Leduc(9×9) ratio **0.457** / 27 cycles | ✅ RPS≈0, skill≈1, Leduc in between |
| `mini_pbt` | PD diversity 0.202→**0.0** (collapse to Defect); RPS diversity **oscillates 0.065–0.294, mean 0.14** | ✅ see nuance below |

### Nuance (not a bug) — `mini_pbt` RPS endpoint print is a misleading snapshot
The script prints only `end={div[-1]}`, which for RPS was **0.0663** — next to
"PREDICT: diversity stays high / churns" that reads like a partial collapse. Inspecting the full
`diversity_curve` (and the PNG) shows RPS **churns**: it oscillates in [0.065, 0.294], mean 0.14,
and never settles — versus PD which decays monotonically to **exactly 0.0** and stays. So the
prediction (churn on the cyclic game, collapse on the transitive one) is **confirmed**; the
endpoint just happened to catch a trough. Left the code as-is (the README already says "the
dynamic, not the exact numbers, is the point", and the plot shows the oscillation clearly).

---

# Phase 4 — Implementation

Executed after the exploration checkpoint. `validate.py` ends **5 PASS / 1 FAIL**; the red is a
kept negative finding (owner-style decision, WORKFLOW §0.1). Sizes kept modest.

## Module self-tests — all 9 exit 0
`evo_games` (Hawk-Dove ESS p=0.5, RPS centre/no-ESS, Stag-Hunt two pure ESS; fitness spread 0 at
each Nash), `replicator` (PD→Defect, HD→0.5, RPS orbit r=0.128, SH basins), `spinning_top`
(RPS Hodge 0/1, SVD 0.707; skill 1/0; reconstruction err 0), `egta` (Kuhn meta-Nash concentrates
on nash; meta ≤ best), `diversity` (participation ratio, clustering, exploit-coverage<1),
`elo` (A>B>C ranking; RPS spread ~0), `leduc_rl` (OBS_DIM=33, distinct encodings, extracted-uniform
EV == uniform_policy EV), `ppo_agent` (1-epoch train runs; extracted exploitability finite),
`league` (3-epoch smoke: min-main-exploitability 4.67→4.51, meta-Nash 4.63→3.90 trending down).

## `validate.py` — 5 PASS / 1 FAIL (~100 s)

| check | result |
|---|---|
| replicator dynamics match analytic ESS | PASS (PD→[0,1]; HD p(Hawk)=0.500; RPS not-converged r=0.128; SH two basins) |
| spinning-top: RPS ~100% cyclic, skill ~100% transitive | PASS (RPS Hodge 0.0000, skill 1.0000; SVD-on-RPS 0.707 as documented) |
| EGTA meta-Nash ≤ best individual (exact policies) | PASS (0.00858 ≤ 0.00858 — meta-Nash concentrates on the CFR-Nash member) |
| PBT league main-agent exploitability decreases | PASS (start 4.672 → best-second-half 4.342) |
| EGTA meta-Nash ≤ best individual (trained league) | **FAIL (kept red on purpose)** — 3.296 vs 3.166 (final, post-fix run); see finding |
| league meta-Nash comparable to PSRO on Leduc | PASS (league 3.843 vs PSRO(12) 3.037; generous same-order band) |

## The kept-red FAIL — a genuine finding, not a bug (WORKFLOW §0.1)

**Claim under test (raw L490):** the meta-Nash *mixture* over the population is no more
exploitable than the best single agent ("mixing over a diverse population is safer").

**What actually happens on Leduc.** I traced it (probe: a league at seed 1, 10 epochs). The
meta-Nash mixture is **pure — weight 1.0 on a single agent** (participation ratio 1.00). That
agent (index 0, exploitability 3.066) is the population *round-robin king*, **not** the
least-exploitable agent (index 1, 2.748). So `meta_nash_exploitability` (3.066) exactly equals
the king's individual exploitability, which exceeds `best_individual` (2.748) → FAIL. The mixture
machinery is therefore **correct** (a pure mixture reproduces that agent's exploitability to the
digit); the prediction is what's off.

**Why it's pure, and why that's the interesting part.** Leduc's empirical meta-game is *mostly
transitive* (spinning-top ratio ~0.45; and the league's *own* snapshots form a near-perfect
skill ladder, transitive ratio **0.98** — successive training snapshots strictly improve). A
transitive meta-game has a **pure meta-Nash** (the top agent). So EGTA gives **no mixing /
diversity dividend at all here** — it just *selects* the best-against-the-population agent. Then
`meta ≤ best_individual` reduces to "is the population-king also the safest agent?", which is a
different question — one that meta-Nash never optimizes for.

**Characterization across seeds/epochs (probe — collected *before* the `ppo_agent` std fix
below; the fix shifts these by ~0.1–0.2 but never flips the sign — the final post-fix
`validate.py` re-run gives 3.296 vs 3.166, still meta > best):**

| seed | epochs | meta | best_indiv | meta≤best | participation | king==safest |
|---|---|---|---|---|---|---|
| 0 | 10 | 4.197 | 3.719 | ❌ | 1.00 | no |
| 1 | 10 | 3.066 | 2.748 | ❌ | 1.00 | no |
| 2 | 10 | 3.544 | 3.394 | ❌ | 1.00 | no |
| 1 | 30 | 1.416 | 1.416 | ✅ | 1.00 | **yes** |

At 30 epochs the king converges to *also* being the safest (and exploitability roughly halves,
3.07→1.42), so it would then pass — but via **single-agent selection, still never via mixing**.
Forcing a green (e.g. bumping the check to 30 epochs) would falsely read as "mixing helped",
which is exactly the §0 failure in reverse. So the check is **kept red**, with a NOTE comment
added in `validate.py` explaining the reconciliation.

**Lesson (survives the mismatch, and sharpens Contribution #3):** the meta-Nash of the empirical
game ≠ the least-exploitable mixture in the full game. On a transitive game EGTA collapses to
picking the population's best agent and offers no robustness-through-mixing; the L490 prediction
is only reliable when (a) the population is genuinely non-transitive so meta-Nash actually mixes,
or (b) the top agent is also the least exploitable (true only after enough training). This is a
real, thesis-relevant nuance for "meta-Nash exploitability as an evaluation metric".

## Smoke tournament (`results/smoke_results.json`, ~112 s)

- **Replicator:** PD→[0,1], HD→[0.5,0.5], RPS orbit (r=0.095), SH both basins — all ESS-confirmed
  (`is_ess=True` at each predicted fixed point). *(The printed `orbit_radius=0.7071` for the
  converged 2-strategy games is just the corner-to-centre distance and is only meaningful for RPS
  — not a signal for the converged games.)*
- **Spinning top:** RPS (0.0 / 1.0), skill (1.0 / 0.0), PSRO-Leduc (0.457 / 0.890). Note the
  transitive/cyclic *ratios* obey the Hodge Pythagorean identity t²+c²≈1 (0.457²+0.890²≈1.00),
  **not** t+c=1 — expected for an orthogonal (Frobenius) decomposition.
- **League (15 epochs, 7 live):** min-main-exploitability **4.672→3.042** (clear decrease);
  final meta-Nash exploitability **2.665 == best individual 2.665** (here PASS — meta-Nash again
  pure, `num_active=1`, and this time the king *is* the best individual); exploit_coverage 0.625;
  league meta-game transitive ratio **0.98**.
- **Comparison on Leduc:** **CFR Nash 0.033** (the ~0 floor) < **LEAGUE 2.665** < **PSRO(12)
  3.037** < **self-play 3.140**. League beats PSRO and single self-play; self-play weakest — all
  as predicted, and all far above the CFR floor.
- Plots written: `plots/{replicator_portraits,transitive_ratios,league_exploitability,comparison_exploitability}.png`.

## Bug/fix — `ppo_agent.py`: size-1 minibatch NaN-poisons training (crashed the SCALE run)

The first `--config scale` launch **crashed** partway through the league suite:
`ValueError: ... logits ... found invalid values tensor([[nan, nan, nan]])` inside `act`, i.e.
the network weights had gone NaN. The give-away was the warning at the top of the log:

```
ppo_agent.py:136: UserWarning: std(): degrees of freedom is <= 0 ...
  adv = (adv - adv.mean()) / (adv.std() + 1e-8)
```

**Root cause (a real bug, not a prediction miss).** When a minibatch holds **exactly one** hero
transition, torch's *default unbiased* `std()` of a 1-element tensor returns **NaN** (dof ≤ 0).
That NaN flows advantage → policy loss → gradients → the Adam step → the weights become NaN, and
the very next `act()` sees NaN logits and dies. `clip_grad_norm_` does **not** rescue this — a
NaN "norm" leaves the NaN gradient intact. Why scale and not smoke: scale uses 512
episodes/epoch, so `T` frequently crosses the 512-minibatch boundary leaving a **size-1
remainder**, and thin exploiters can collect very few transitions in an epoch; smoke's smaller
batches simply never produced a lone-sample minibatch.

**Minimal fix (behavior-preserving for normal batches):** `adv.std()` → `adv.std(unbiased=False)`.
Biased (population) std returns **0** for a single sample, so a lone-sample minibatch just centers
the advantage instead of NaN-ing. For normal minibatch sizes biased vs unbiased differ by
~√(n/(n−1)) ≈ 1 — negligible for advantage normalization (biased is the common choice anyway), so
**no PASS/FAIL verdict changes** (the `validate.py` league-check numbers move by ~0.1–0.2, within
run-to-run noise — the table above is the final post-fix run; the smoke tournament was run pre-fix
and stands as recorded). Verified with a targeted T=1 `update()` probe: finite stats, all net
params finite (previously NaN). After the fix the scale run was relaunched and completed clean.

## Scale tournament (`results/scale_results.json`, 120-epoch league) — the headline finding

Ran clean after the NaN fix. Exact suites matched smoke: replicator all-4 ESS-confirmed;
spinning-top RPS 0.0/1.0, skill 1.0/0.0, PSRO-Leduc(20) ratio 0.411. The **league** is where
scale is instructive — and it is the most thesis-relevant result of the step.

**Main-agent exploitability is U-SHAPED over 120 epochs (not monotone):**
`4.734 → MIN 1.212 @ epoch 67 → drifts back up to ~2.05 by epoch 120`. Per-epoch meta-Nash
similarly bottoms at **1.323 @ epoch 22** then rises to ~2.96. So the league **learns a strong
agent early, then DEGRADES over the long run.**

- **The league genuinely works, early:** its best-so-far main is **1.212** (epoch 67), and the
  best individual over the whole 56-policy population is **1.305** — *better than* exact
  **PSRO(20) = 2.163**. On a modest neural budget the league beat exact double-oracle's best.
- **But long-horizon league training is unstable:** with 48 accumulated frozen snapshots and
  PFSP over-weighting hard opponents, the live main agents chase a moving population target and
  their **full-game** exploitability regresses (~1.2 → ~2.0) even as they stay strong *against
  the population*. This is exactly the **"heuristic-only safety" gap** the raw step flags for
  **Contribution #2** — the empirical case for *formal* safe population training. Not a bug: the
  exploitability is computed exactly; the min@67 proves the machinery; the rise is a dynamics /
  regularization phenomenon. (A likely secondary contributor: PBT's `perturb_hyperparams` can
  drift `lr` up toward its 1e-1 ceiling over ~10 PBT events — worth a look in consolidation, but
  the degradation is expected league behavior regardless.)

**meta-Nash ≤ best individual — FAILS again, harder, and now WITH mixing** (final report over all
56 policies): meta-Nash exploitability **3.418** vs best individual **1.305** → False. Unlike
smoke (pure meta-Nash), at scale meta-Nash **mixes 3 policies** (participation ratio 1.92,
`num_active=3`) — yet the mixture is *far more* exploitable than the single best agent. This is
the **strongest evidence for the Phase-4 kept-red finding**: the meta-Nash of the empirical game
is **not** the least-exploitable mixture in the full game; a full-game best-responder exploits the
behavioral blend at its seams. A sharp caveat for Contribution #3 (meta-Nash exploitability as an
evaluation metric): it is sensitive to *population composition* — mixing over a partly-degraded
recent population is worse than just keeping the historical best agent.

**Comparison on Leduc (scale):** `CFR(20000) 0.0099` (the ~0 floor ✅) < **league best-individual
1.305** < **PSRO(20) 2.163** < **league final meta-Nash 3.418** < **self-play 3.683** (weakest ✅).
Reconciliation of raw L491-492 ("league comparable to PSRO; self-play weakest"): **mixed** —
the league's *best agent* beats PSRO, but its *final meta-Nash mixture* is worse than PSRO
(dragged up by the late degradation + the non-convex-mixture effect). Self-play is weakest as
predicted. "Comparable order of magnitude" holds (1.3–3.4 vs 2.16).

Diversity (final): `num_active=3`, participation ratio 1.92, 1 behavioral cluster, exploit
coverage 0.571; league meta-game transitive ratio **0.937** (the snapshots again form a near
skill-ladder). Plots regenerated for scale: `plots/{replicator_portraits,transitive_ratios,league_exploitability,comparison_exploitability}.png`.

**Net takeaway (for consolidation):** Step 10's neural league, exactly evaluated, reproduces the
population-training story *and its failure mode*: strong early gains (best agent beats exact
PSRO), then long-horizon degradation from purely-heuristic safety — the concrete motivation for
Contribution #2 — while EGTA meta-Nash exploitability proves a subtle Contribution-#3 metric
(meta-Nash-of-empirical-game ≠ least-exploitable-mixture; sensitive to population quality).

## Files touched (Phase 4)
- `ppo_agent.py` — `adv.std()` → `adv.std(unbiased=False)` (fixes the size-1-minibatch NaN that
  crashed the scale league; behavior-preserving for normal batches).
- `validate.py` — added a NOTE comment + richer FAIL detail string on `check_league_meta_nash`
  documenting the kept-red negative finding (behavior unchanged; still red).
- New generated artifacts: `implementation/results/{smoke,scale}_results.json`,
  `implementation/plots/*.png`, `exploration/figures/*.{json,png}`.

`consolidation/` and `deliverables/reports/step10/` intentionally **not** authored this session
(deferred, per the Step 09 execute/deliverables split).
