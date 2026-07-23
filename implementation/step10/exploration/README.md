# Step 10 — Exploration: seeing populations evolve, cycle, and collapse before the theory

Phase 2 of Step 10. Small, fast, **seeded** experiments that build intuition by *running and
tinkering*. Everything is written to be run by you — **none of it has been executed here**
(see [`../../WORKFLOW.md`](../../WORKFLOW.md)). Every "expected"/"PREDICT" number below is a
**prediction to verify**, not a measured result.

The replicator / matrix-game / PBT scripts are **pure numpy** and self-contained via
[`_evo_tools.py`](_evo_tools.py). The two scripts that touch Leduc (`psro_population_peek.py`,
`game_landscape.py`) reuse Step 09's exact PSRO and Step 07's Leduc engine through a tiny
`sys.path` bootstrap in [`_bootstrap.py`](_bootstrap.py).

---

## How to run

From this folder (`implementation/step10/exploration/`):

```bash
python replicator_playground.py
python psro_population_peek.py     # uses Step 09 PSRO + Step 07 Leduc engine
python game_landscape.py           # uses Step 09 PSRO + Step 07 Leduc engine
python mini_pbt.py
```

- **Dependencies:** Python 3.10+ and `numpy` for everything. `matplotlib` is optional — without
  it, scripts still print tables and write JSON, just no PNGs.
- **Outputs** (tables to stdout; JSON + PNG to [`figures/`](figures/)) are created on first run.
- **Working dir:** run from *this* folder so `_evo_tools` / `_bootstrap` import cleanly.
- **Runtime:** the numpy scripts are seconds. `psro_population_peek.py` / `game_landscape.py`
  run exact PSRO on Leduc — Step 09's "slow one" — so budget ~a minute at the default 8–10
  rounds; raising `rounds` toward the raw step's "50+" is minutes.

---

## Files

| File | Role |
|------|------|
| [`_bootstrap.py`](_bootstrap.py) | Puts Step 09's + Step 07's `implementation/` on `sys.path`. Import first in the Leduc scripts. |
| [`_evo_tools.py`](_evo_tools.py) | The four symmetric games, replicator dynamics, the Hodge transitive ratio, effective-diversity, and JSON/plot savers. Self-contained numpy. |
| [`replicator_playground.py`](replicator_playground.py) | Replicator dynamics on PD / Hawk-Dove / RPS / Stag Hunt: what converges, what orbits, what splits into basins. |
| [`psro_population_peek.py`](psro_population_peek.py) | PSRO *is* population-based training: watch exploitability fall, count active vs dead policies, measure meta-game transitivity. |
| [`game_landscape.py`](game_landscape.py) | Skill ladder vs rock-paper-scissors cycles: transitive ratio, 3-cycle count, and a 2D embedding of the strategies. |
| [`mini_pbt.py`](mini_pbt.py) | A fast PBT proxy showing **diversity collapse** on a transitive game and diversity churn on a cyclic one. |

---

## 1. `replicator_playground.py`

**What it does.** Runs single-population replicator dynamics on the four games and prints the
final population state + a convergence flag; saves phase portraits.

**How to play with it** (`CONFIG`):

| Knob | Effect | Try |
|------|--------|-----|
| `T` | number of Euler steps | raise to make convergence/cycling unambiguous |
| `dt` | integration step | smaller → smoother orbits (RPS), slower convergence |
| `starts` | initial population state per game | flip Stag Hunt starts to land in the other basin |

**What to watch out for.** Discrete Euler on RPS is *near*-energy-preserving; the orbit may
drift slightly but must **not** converge — that non-convergence is the finding, not a bug.

**How to read the results (PREDICTIONS — verify).** PD → all-Defect; Hawk-Dove → p(Hawk)=0.5;
RPS → orbit (never converges); Stag Hunt → all-Stag or all-Hare by start.

---

## 2. `psro_population_peek.py`

**What it does.** Runs Step 09's exact PSRO on Leduc, then inspects the population: exploitability
vs population size, how many policies are *active* in the meta-Nash (weight > 1%), and the
meta-game's Hodge transitive ratio.

**How to play with it** (`CONFIG`): `game` (`"kuhn"` is far faster if you want many rounds),
`rounds` (raise toward 50 on Leduc only if you have the minutes), `active_threshold`.

**What to watch out for.** Exact PSRO on Leduc gets slow as the population grows (a full-tree
best response per player each round). "Exploitability" is the meta-mixture's NashConv in the
*full* game, not the meta-game.

**How to read the results (PREDICTIONS — verify).** Exploitability trends down; only a handful
of policies carry meta-Nash weight (the diversity problem); Leduc's meta-game is *mostly
transitive* (ratio well above 0), so self-play works reasonably here — unlike the FFA games of
Step 11.

---

## 3. `game_landscape.py`

**What it does.** Compares three payoff matrices — pure-cyclic RPS, a pure-skill ladder, and
the exact PSRO-Leduc meta-game — by transitive ratio, 3-cycle count, and a 2D embedding.

**How to play with it** (`CONFIG`): `leduc_rounds` (bigger Leduc population), `beat_tol`.

**What to watch out for.** The 2D embedding uses the top-2 singular vectors of the
antisymmetric part; for a purely transitive game the second coordinate collapses (points lie on
a line). Sign/orientation of the embedding is arbitrary.

**How to read the results (PREDICTIONS — verify).** RPS → transitive ratio ~0, many 3-cycles, a
rotational disc; skill ladder → ratio ~1, zero cycles, points on a line; Leduc → in between.

---

## 4. `mini_pbt.py`

**What it does.** A fast PBT proxy (strategy-vector "agents", round-robin, replace bottom 20%
with mutated top 20%) tracking population diversity per generation.

**How to play with it** (`CONFIG`): `pop_size`, `generations`, `replace_fraction`,
`mutation_std` (bigger → more exploration, slower collapse), `games`.

**What to watch out for.** This is a strategy-level proxy, not full PPO agents — deliberately, to
stay fast. The dynamic (collapse vs churn) is the point, not the exact numbers.

**How to read the results (PREDICTIONS — verify).** PD → diversity → ~0 (collapse to Defect);
RPS → diversity stays high / churns (no single best answer). The contrast motivates AlphaStar's
exploiters.

---

## Suggested path through it

1. `replicator_playground.py` — the four evolutionary dynamics on one screen.
2. `psro_population_peek.py` — PSRO as a growing population; the diversity problem appears.
3. `game_landscape.py` — *why* some games cycle: transitive vs cyclic structure made visible.
4. `mini_pbt.py` — naive PBT collapses diversity; the seed of why exploiters exist.

---

## Key takeaways for the final summary

- **Replicator dynamics are the ODE behind self-play.** Fixed points are Nash; attractors are
  ESS; RPS has a *centre* (orbit) not an attractor — the dynamical face of non-transitive
  cycling. (verify via replicator_playground)
- **PSRO is population-based training.** Exploitability falls as the population grows, but only a
  few policies stay active in the meta-Nash — the diversity problem AlphaStar's league targets.
  (verify via psro_population_peek)
- **Transitive vs cyclic is measurable.** The Hodge transitive ratio separates a skill ladder
  (ratio ~1) from RPS (ratio ~0); Leduc sits in between and leans transitive. (verify via
  game_landscape)
- **Naive PBT collapses diversity on transitive games and churns on cyclic ones.** Neither is
  the robust population you want — hence exploiters + freezing in Phase 4. (verify via mini_pbt)
- **Scale caveat:** all toy/exact/CPU-bound; do not generalize these speeds/behaviors to
  deep-RL population training at AlphaStar scale.
