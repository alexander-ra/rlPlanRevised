# Step 08 — Exploration: seeing safe exploitation work before the theory

Phase 2 of Step 08. Small, fast, **seeded** experiments that build intuition by *running
and tinkering*. Everything is written to be run by you — **none of it has been executed
here** (see [`../../workflow.md`](../../workflow.md)). Every "expected" number below is a
**prediction to verify**, not a measured result.

All scripts **reuse Step 07's validated code** (engines, exact best response, CFR Nash,
the opponent type zoo, the policy currency) via a tiny `sys.path` bootstrap in
[`_bootstrap.py`](_bootstrap.py). Nothing is re-implemented. Shared safe-exploitation metrics
live in [`_soe_tools.py`](_soe_tools.py).

---

## How to run

From this folder (`implementation/step08/exploration/`):

```bash
python exploitation_safety_playground.py
python pareto_curve.py
python naive_exploit_danger.py
python rnr_playground.py
python subgame_peek.py            # GAME="leduc" by default (slower); flip to "kuhn" for speed
```

- **Dependencies:** Python 3.10+ only for the tables. `matplotlib` is optional — without it,
  scripts still print tables and write JSON, just no PNGs.
- **Outputs** (tables to stdout; JSON + PNG to [`figures/`](figures/)) are created on first run.
- **Working dir:** run from *this* folder so the bootstrap and `_soe_tools` import cleanly.
- **Runtime:** Kuhn scripts are seconds. `subgame_peek.py` on Leduc is ~1–3 min (CFR blueprint
  + full-tree best response). Per the compute policy in `workflow.md`, there is no reason to
  scale these up; the RTX 5090 is irrelevant here (all exact/tabular, CPU-bound).

---

## Files

| File | Role |
|------|------|
| [`_bootstrap.py`](_bootstrap.py) | Puts Step 07's `implementation/` on `sys.path` (inherits its safe `importlib` engine loader). Import first. |
| [`_soe_tools.py`](_soe_tools.py) | Shared EXACT metrics: game value, exploitation EV, worst-case EV, exploitability — the two axes every plot lives on. |
| [`exploitation_safety_playground.py`](exploitation_safety_playground.py) | Nash vs full BR vs 50% blend, each scored on profit AND worst-case/exploitability at once. |
| [`pareto_curve.py`](pareto_curve.py) | Sweeps the blend and plots profit vs worst-case loss — the safe-exploitation Pareto picture. |
| [`naive_exploit_danger.py`](naive_exploit_danger.py) | Full BR to a weak type, then measures how exploitable *we* became — and shows the holes. |
| [`rnr_playground.py`](rnr_playground.py) | A **naive** RNR p-sweep (blend), profit and exploitability vs p. NOT canonical RNR (that's in the implementation phase). |
| [`subgame_peek.py`](subgame_peek.py) | Blueprint vs local exploit on Leduc: the deviations are LOCAL (a few info sets), the motivation for subgame solving. |

---

## 1. `exploitation_safety_playground.py`

**What it does.** Builds three hero strategies against `TightPassive` — Nash, full best
response, and a 50/50 behavioral blend — and prints, for each, the EV vs the exploitee, the
EV vs Nash, the worst-case EV (opponent best-responds), and the exploitability.

**How to play with it** (`CONFIG` at the top):

| Knob | Effect | Try |
|------|--------|-----|
| `game` | `"kuhn"` (fast) or `"leduc"` | flip to leduc to see it on a bigger tree (slower) |
| `exploitee` | which weak type to target | try a different zoo type; note how the BR changes |
| `blend_lambda` | weight on Nash in the blend | set 0.25 / 0.75 to watch both axes move together |

**What to watch out for.** Seat 0 in Kuhn carries the **−1/18 ≈ −0.056** disadvantage, so
absolute EVs are small and can be negative — that is the game, not a bug. "Exploitability"
here is *game value minus worst-case EV* (≥ 0), so Nash sits near 0.

**How to read the results (PREDICTION — verify by running).** Full BR wins the most vs
TightPassive but has clearly positive exploitability; Nash has ~0 exploitability but no extra
profit; the blend lands roughly halfway on **both** axes. Halfway is *not* efficient — that's
what the Pareto script and the implementation solvers show.

---

## 2. `pareto_curve.py`

**What it does.** Sweeps the blend λ from 0 (pure BR) to 1 (pure Nash) in 0.1 steps and plots
exploitation **profit** (X) against **worst-case loss** (Y = exploitability). This curve is the
literal picture of the exploitation-safety tradeoff.

**How to play with it** (`CONFIG`): `exploitee`, `game`, `lambdas` (finer grid → smoother curve).

**What to watch out for.** This is the **naive-blend** frontier. It is generally **dominated**:
the real solvers (RNR, Ganzfried in the implementation phase) find strategies with the *same*
worst-case loss and *strictly more* profit, because they choose *where* to deviate rather than
scaling every info set uniformly. Do not read this curve as "the best you can do."

**How to read the results (PREDICTION — verify).** Monotone: as λ→0 (more BR), both profit and
worst-case loss rise. The interesting operating point is the highest profit whose worst-case
loss is within a budget you pick.

---

## 3. `naive_exploit_danger.py`

**What it does.** Computes the full best response to `TightPassive`, then measures *our* own
worst-case value (an adversary best-responds to us) and lists the info sets where the BR
deviates from Nash — the holes.

**How to play with it** (`CONFIG`): `exploitee`, `nash_iters` (blueprint quality).

**What to watch out for.** The BR is deterministic, so "deviation" is flagged where its pure
action is one that Nash mostly avoids. A high exploitability number here is the *expected*,
correct result — that's the lesson, not a bug.

**How to read the results (PREDICTION — verify).** BR wins clearly more vs TightPassive than
Nash does, but its worst-case EV is far worse than Nash's, so its exploitability is clearly
positive. The listed holes should look like "never bluffs X because TightPassive never calls"
— exactly what a Nash opponent would punish.

---

## 4. `rnr_playground.py`

**What it does.** A p-sweep of the **naive** blend `(1−p)·Nash + p·BR`, printing profit and
exploitability against p, and plotting both.

> **FLAG:** this is the raw step's Day-2 *description* (L128–142) and a good intuition tool,
> but it is **not** Johanson's actual Restricted Nash Response. Canonical RNR solves for the
> *equilibrium against a p-restricted opponent* — a constrained optimization that dominates
> this blend. The real solver is [`../implementation/rnr_solver.py`](../implementation/rnr_solver.py);
> both are provided there so you can see the gap.

**How to play with it** (`CONFIG`): `ps` (grid), `exploitee`, `game`.

**What to watch out for.** Don't mistake the playground for the algorithm (see the flag). The
"budget" intuition (you can deviate a fair bit before exploitability bites) holds for both, but
the *numbers* differ.

**How to read the results (PREDICTION — verify).** Profit rises with p; exploitability also
rises, but slowly at first — there's a budget of cheap early exploitation before it gets
expensive.

---

## 5. `subgame_peek.py`

**What it does.** On Leduc, contrasts the blueprint (Nash) action distribution with the local
full-exploit action (BR to `Rock`) at every hero info set, and lists the most-deviating ones —
the candidate "subgames" you'd re-solve in real time.

**How to play with it** (`CONFIG`): `game` (`"leduc"` interesting, `"kuhn"` fast), `top_n`,
`exploitee`.

**What to watch out for.** This does **not** build the safety gadget — it's an intuition
preview. It also uses a *full* BR (perfect knowledge of the type), so it overstates how much a
real, data-limited model would deviate. The gadget-based, provably-safe subgame solver is
[`../implementation/subgame_exploit_solver.py`](../implementation/subgame_exploit_solver.py).

**How to read the results (PREDICTION — verify).** Only a handful of info sets deviate
meaningfully; most stay at the blueprint. That **locality** is the whole reason real-time
subgame solving is worthwhile — you fix your play where it matters and leave the rest alone.

---

## Suggested path through it

1. `exploitation_safety_playground.py` — the three canonical strategies on both axes at once.
2. `pareto_curve.py` — the tradeoff as a curve (and why the naive blend isn't efficient).
3. `naive_exploit_danger.py` — *why* you need safety: BR opens holes.
4. `rnr_playground.py` — the tunable knob (and the naive-vs-canonical flag).
5. `subgame_peek.py` — exploitation is *local*, motivating real-time subgame solving.

---

## Key takeaways for the final summary

- **Profit and exploitability rise together.** Full BR maximizes profit vs a weak type but is
  itself highly exploitable; Nash is unexploitable but wins nothing extra. Safe exploitation is
  choosing where on that tradeoff to sit. (verify via the playground + pareto)
- **The naive Nash/BR blend traces a Pareto curve but is *not* the efficient frontier.**
  Choosing *where* to deviate (the LP solvers) beats scaling every info set uniformly. (verify
  by comparing this curve to the implementation solvers)
- **Best-responding to a weak type creates your own holes** — the exploitability jump is
  concrete and visible in specific info sets. This is *why* the safety machinery exists.
  (verify via naive_exploit_danger)
- **Naive p-blend ≠ canonical RNR** — flagged explicitly; the real algorithm dominates the
  blend and lives in the implementation phase.
- **Exploitation is local:** only a few info sets change between blueprint and exploit, which
  is what makes real-time subgame solving (SES/OX-Search) worthwhile. (verify via subgame_peek)
- **Scale caveat:** Kuhn/Leduc are exact and small; everything converges instantly (Kuhn) or in
  a couple of minutes (Leduc). Do not generalize these speeds to real poker.
