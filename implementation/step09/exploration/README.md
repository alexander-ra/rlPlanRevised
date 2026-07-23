# Step 09 — Exploration: seeing multi-agent learning break (and get fixed) before the theory

Phase 2 of Step 09. Small, fast, **seeded** experiments that build intuition by *running and
tinkering*. Everything is written to be run by you — **none of it has been executed here**
(see [`../../WORKFLOW.md`](../../WORKFLOW.md)). Every "expected"/"PREDICT" number below is a
**prediction to verify**, not a measured result.

The matrix-game / PSRO / LOLA scripts are **pure numpy** and self-contained. The one script
that touches Kuhn (`selfplay_vs_nash.py`) reuses Step 07's validated engines + exact best
response via a tiny `sys.path` bootstrap in [`_bootstrap.py`](_bootstrap.py). Shared
matrix-game tools live in [`_marl_tools.py`](_marl_tools.py).

---

## How to run

From this folder (`implementation/step09/exploration/`):

```bash
python matrix_games_playground.py
python nonstationarity_demo.py
python selfplay_vs_nash.py        # uses the Step 07 Kuhn engine
python psro_peek.py
python lola_ipd_playground.py
```

- **Dependencies:** Python 3.10+ and `numpy` for everything. `matplotlib` is optional —
  without it, scripts still print tables and write JSON, just no PNGs.
- **Outputs** (tables to stdout; JSON + PNG to [`figures/`](figures/)) are created on first run.
- **Working dir:** run from *this* folder so `_marl_tools` / `_bootstrap` import cleanly.
- **Runtime:** every script is seconds. `selfplay_vs_nash.py` is the slowest (a few hundred
  exact best responses on Kuhn) — up to ~a minute. Per the compute policy in `WORKFLOW.md`,
  there is no reason to scale these up; the RTX 5090 is irrelevant here (all exact/tabular,
  CPU-bound).

---

## Files

| File | Role |
|------|------|
| [`_bootstrap.py`](_bootstrap.py) | Puts Step 07's `implementation/` on `sys.path` (inherits its safe `importlib` engine loader). Import first in the Kuhn script. |
| [`_marl_tools.py`](_marl_tools.py) | The four matrix games (payoffs + analytic Nash), the independent-learner (IGA) dynamics, a numpy fictitious-play meta-Nash solver, and the JSON/plot helpers. |
| [`matrix_games_playground.py`](matrix_games_playground.py) | All four games under independent learners: what converges, what cycles, what fails. |
| [`nonstationarity_demo.py`](nonstationarity_demo.py) | Matching Pennies orbit vs PD convergence — the moving-target problem, made visible. |
| [`selfplay_vs_nash.py`](selfplay_vs_nash.py) | Fictitious-play self-play on Kuhn: the AVERAGE iterate converges to Nash, the last iterate does not. |
| [`psro_peek.py`](psro_peek.py) | Minimal PSRO on Rock-Paper-Scissors: population + meta-Nash + best-response oracle → exploitability falls. |
| [`lola_ipd_playground.py`](lola_ipd_playground.py) | Naive learners defect, LOLA learners cooperate on the Iterated Prisoner's Dilemma. |

---

## 1. `matrix_games_playground.py`

**What it does.** Runs two independent gradient learners on PD / Matching Pennies / Stag Hunt
/ Battle of the Sexes and prints final action probabilities, payoffs, and a convergence flag.

**How to play with it** (`CONFIG`):

| Knob | Effect | Try |
|------|--------|-----|
| `steps` | training length | raise to make convergence/cycling unambiguous |
| `lr` | learning rate | bigger → faster, but Matching Pennies orbits grow |
| `init` | initial `(p, q)` | flip Stag Hunt / BoS between `(0.9,0.9)` and `(0.1,0.1)` to change the equilibrium reached |

**What to watch out for.** Exact-gradient learners (no sampling) so the dynamics are clean;
"converged" = last 100 steps barely moved. Matching Pennies reporting *not converged* is the
result, not a bug.

**How to read the results (PREDICTIONS — verify).** PD → mutual defection; Matching Pennies →
orbit; Stag Hunt → payoff- or risk-dominant equilibrium by init; BoS → one of the two pure
equilibria by init.

---

## 2. `nonstationarity_demo.py`

**What it does.** Zooms into Matching Pennies and reports the orbit radius (distance from the
50/50 Nash) per time-window — it does *not* shrink — alongside PD, which *does* converge.

**How to play with it** (`CONFIG`): `steps`, `lr` (larger → larger orbit), `init` (start
off-center to make the first loop obvious).

**What to watch out for.** Under exact simultaneous gradient updates the orbit is roughly
energy-preserving (neither spirals in nor out much). Non-convergence is the finding.

**How to read the results (PREDICTIONS — verify).** Matching Pennies: window radii ≈ constant;
PD: distance-to-(defect,defect) → 0.

---

## 3. `selfplay_vs_nash.py`

**What it does.** Fictitious-play self-play on Kuhn (reusing Step 07's exact BR + NashConv):
each player best-responds to the opponent's running average, then updates its own average.
Tracks the **average**-iterate NashConv (→ 0) and the **last**-iterate NashConv (stays high).

**How to play with it** (`CONFIG`): `iters` (more → tighter average), `eval_every` (measurement
cadence; each measurement is a couple of exact BRs).

**What to watch out for.** Fictitious play converges *slowly* (~1/√t); expect the average
NashConv to fall from ~0.9 toward ~0.05–0.1, not to machine zero. Kuhn's value for P0 is
−1/18; it is NashConv that → 0, not the value.

**How to read the results (PREDICTIONS — verify).** Average NashConv trends down toward ~0;
last-iterate NashConv stays large and oscillates. This is *why* averaging (CFR, fictitious
play) matters and why PSRO uses a meta-Nash mixture rather than the last policy.

---

## 4. `psro_peek.py`

**What it does.** A minimal PSRO on Rock-Paper-Scissors: maintain a population of pure
strategies, solve the meta-Nash over it (numpy fictitious play), add the exact best response
to the opponent's meta-Nash mixture, repeat — and watch the mixture's exploitability fall.

**How to play with it** (`CONFIG`): `rounds` (RPS needs ~3 to complete Rock→Paper→Scissors),
`fp_iters` (meta-Nash solve precision).

**What to watch out for.** The BR oracle here is *exact* (argmax over the full action set).
With an approximate RL oracle (as on Leduc in the implementation phase), convergence is
empirical, not guaranteed — the raw step's open question (L487–489). "Exploitability" is the
mixture's NashConv in the *full* game, not the meta-game.

**How to read the results (PREDICTIONS — verify).** Population grows to {Rock, Paper,
Scissors}; mixture → (⅓, ⅓, ⅓); exploitability → ~0.

---

## 5. `lola_ipd_playground.py`

**What it does.** Exact memory-1 Iterated Prisoner's Dilemma: naive gradient learners vs LOLA
learners (each differentiating through the other's learning step, via nested finite
differences). Tracks per-step return over training.

**How to play with it** (`CONFIG`): `gamma` (shadow of the future — cooperation needs it high),
`lr_opp` (the look-ahead step; set to 0 and LOLA degenerates to naive), `lr`, `steps`.

**What to watch out for.** This is demo-grade LOLA (finite-difference look-ahead) — correct
and deterministic but not the fastest; the cleaner version is in the implementation phase.
Cooperation is sensitive to `gamma`/`lr_opp` (that sensitivity is itself instructive).

**How to read the results (PREDICTIONS — verify).** naive vs naive → per-step return ~1
(mutual defection); LOLA vs LOLA → ~3 (mutual cooperation).

---

## Suggested path through it

1. `matrix_games_playground.py` — the four canonical dynamics on one screen.
2. `nonstationarity_demo.py` — *why* independent learning struggles (the moving target).
3. `selfplay_vs_nash.py` — the averaging fix (and why last-iterate self-play misleads).
4. `psro_peek.py` — averaging lifted to a population: the PSRO loop.
5. `lola_ipd_playground.py` — a different fix entirely: look ahead at the opponent's update.

---

## Key takeaways for the final summary

- **Independent learning is the control that fails on purpose.** It converges in PD (dominant
  strategy) but cycles in Matching Pennies and mis-selects in Stag Hunt / BoS — the visceral
  case for coordination machinery. (verify via the playground + nonstationarity demo)
- **Non-stationarity is an orbit, not slow convergence.** The Matching Pennies radius stays
  constant; more compute does not help. (verify via nonstationarity_demo)
- **Self-play converges in the AVERAGE, not the last iterate.** Kuhn fictitious play drives the
  average's NashConv toward 0 while pure best responses stay exploitable — the motivation for
  averaging (CFR) and for PSRO's meta-mixture. (verify via selfplay_vs_nash)
- **PSRO = iterated best response over a population + meta-Nash.** On RPS the population
  discovers the full cycle and exploitability → 0. Exact oracle here; approximate later.
  (verify via psro_peek)
- **LOLA changes the gradient, not just the strategy.** Anticipating the opponent's learning
  step turns defectors into cooperators on IPD — *dynamic* opponent modeling, distinct from
  Step 7's static read. (verify via lola_ipd_playground)
- **Scale caveat:** all toy, exact, CPU-bound; everything runs in seconds. Do not generalize
  these speeds/behaviors to deep-RL MARL at scale.
