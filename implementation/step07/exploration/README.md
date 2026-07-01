# Step 07 — Exploration: seeing opponent modeling work before the theory

Phase 2 of Step 07. Small, fast, **seeded** Kuhn-Poker experiments that build intuition by
*running and tinkering*. Everything is written to be run by you — **none of it has been
executed here** (see [`../../WORKFLOW.md`](../../WORKFLOW.md)). Every "expected" number
below is a **prediction to verify**, not a measured result.

All scripts build on the validated **Step 02 Kuhn engine** (imported, never copied) via a
tiny `sys.path` bootstrap in [`kuhn_tools.py`](kuhn_tools.py).

---

## How to run

From the repo root (or anywhere — the scripts locate Step 02 themselves):

```bash
python implementation/step07/exploration/kuhn_tools.py              # self-test of the helpers
python implementation/step07/exploration/behavioral_fingerprints.py
python implementation/step07/exploration/exploitation_opportunity.py
python implementation/step07/exploration/bayesian_type_detector.py
```

- **Dependencies:** Python 3.10+ only. `matplotlib` is optional — if it's missing, scripts
  still print tables and save JSON, just no PNGs.
- **Outputs** (tables to stdout; JSON + PNG to [`figures/`](figures/)) are created on first run.
- **Runtime:** each script is **< 1 second**. Kuhn is tiny and exact-solvable, so there is
  **no reason to scale these up** (per the compute policy in `WORKFLOW.md`); the RTX 5090
  is irrelevant here. Scale-up starts to matter in Leduc / the implementation phase.

---

## Files

| File | Role |
|------|------|
| [`kuhn_tools.py`](kuhn_tools.py) | Shared helpers: exact payoff, exact EV, exact best response (by enumerating Kuhn's 64 pure strategies), a Nash policy via Step 02 CFR, and a hand simulator. Run it directly for a self-test. |
| [`opponent_types.py`](opponent_types.py) | The "type zoo": `AlwaysCall`, `TightPassive`, `LooseAggressive`, `Nash`, plus a `mixture(...)` helper and a template for adding your own. |
| [`behavioral_fingerprints.py`](behavioral_fingerprints.py) | Measures each type's action frequencies per info set — its "fingerprint". |
| [`exploitation_opportunity.py`](exploitation_opportunity.py) | Nash EV vs best-response EV against each type. The gap = money left on the table. |
| [`bayesian_type_detector.py`](bayesian_type_detector.py) | The belief-update loop: a posterior over types that concentrates as it observes play. |
| [`mixture_recovery.py`](mixture_recovery.py) | Asks *"what **mixture** of types are you?"* instead of *"which one?"* — fits mixing weights over the types by EM and recovers a blend (e.g. 70% rock + 30% maniac) that the single-type detector collapses onto Nash. |
| [`robustness_sweep.py`](robustness_sweep.py) | 500 hands × 300 seeds on the out-of-set mixture: shows Nash is always the final winner and never falls once locked, but a *wrong* type can confidently lead for 100–200+ hands first. Backs report §4.3. |

---

## 1. `behavioral_fingerprints.py`

**What it does.** Plays each type against a 50/50 "prober" (to force every info set to be
visited) and records the empirical `P(bet)` at each info set, next to the type's true
`P(bet)`.

**How to play with it** (`CONFIG` at the top):

| Knob | Effect | Try |
|------|--------|-----|
| `hands_per_type` | More hands → less sampling noise | drop to 100 to *see* the noise, raise to 20000 to remove it |
| `seed` | Changes the random stream | run a few seeds; watch rare info sets wobble |
| add a type | Put a new policy in `DETERMINISTIC_TYPES` | invent a "bluffy" type and look at its fingerprint |

**What to watch out for.** Info sets with few `visits` have unreliable `emp p_bet` — that
sampling noise is exactly what makes opponent modeling hard with little data. The prober
is uniform *only* to get coverage; it is not a serious opponent.

**How to read the results (expected — verify by running).** The four fingerprints should
look obviously different: `LooseAggressive` ≈ 1.0 everywhere; `TightPassive` ≈ 0 except
with K; `AlwaysCall` ≈ 0 when checking into an open pot but ≈ 1.0 when facing a bet; `Nash`
fractional/mixed. At well-visited info sets `emp p_bet` should track `true p_bet`.

---

## 2. `exploitation_opportunity.py`

**What it does.** For each type and each seat, computes (exactly) the Nash hero's EV, the
best-response EV (the exploitation ceiling), and the gap. Also prints the actual
best-response policy against `TightPassive` so you can see *how* you'd exploit it.

**How to play with it** (`CONFIG`): `nash_iterations` (Nash quality) and `seed`.

**What to watch out for.** Kuhn's first player (seat 0) carries the known **−1/18 ≈ −0.056**
disadvantage, so seat-0 EVs are small and often negative — that's the game, not a bug.
Best response here assumes you *already know* the type perfectly; a real model only
approaches this ceiling as it gathers data.

**How to read the results (expected — verify by running).**
- Against **`Nash`**, the gap should be ≈ 0 (Nash is unexploitable — best response can't beat
  the game value).
- Against **`TightPassive` / `LooseAggressive` / `AlwaysCall`**, the gap should be clearly
  positive — that's the exploitation opportunity.
- The printed best response to `TightPassive` should **bluff** (bet weak hands), because that
  type folds everything but K. Seeing that concretely is the point.

---

## 3. `bayesian_type_detector.py`

**What it does.** Maintains a posterior over the four types and updates it after every
observed opponent action (`posterior ∝ prior × Π P(action | type, info_set)`). Runs two
scenarios: a hidden `TightPassive`, and a hidden 50/50 mixture of `TightPassive` and
`LooseAggressive`.

**How to play with it** (`CONFIG`):

| Knob | Effect | Try |
|------|--------|-----|
| `hands` | Length of the observation stream | shorten to see how fast it commits |
| `epsilon` | Likelihood smoothing | set `0.0` to allow **hard elimination** (one impossible action kills a type); raise it to make the detector cautious |
| `seed` | Random stream | confirm conclusions hold across seeds |
| true policy | What the hidden opponent actually plays | point scenario 1 at `LooseAggressive`, or build your own mixture |

**What to watch out for.**
- **Partial observability is faked here.** The detector uses the opponent's *true card* when
  scoring likelihoods — as if every hand went to showdown. Real play hides the card, so the
  realistic detector must average over the opponent's possible hands; convergence is slower.
  That marginalization is built in the **implementation phase**, not here.
- **Deterministic types + `epsilon=0`** → a single "impossible" action drives a type's
  posterior to exactly 0. With smoothing it only gets *unlikely*. Don't over-read hard zeros.
- **Do not** "best-respond to the raw observed frequencies" — on tiny samples that overfits
  and makes you maximally exploitable. The whole reason to carry a posterior/prior is to
  avoid that.

**How to read the results (expected — verify by running).**
- Scenario 1: the posterior should pile onto **`TightPassive`** within roughly **5–15 hands**
  (it's a very distinctive type).
- Scenario 2: the posterior should **split between `TightPassive` and `LooseAggressive`** and
  stay low on `Nash`/`AlwaysCall` — the model has no exact match, so it blends the nearest
  ones. This is the motivation for the *continuous* model in Phase 4.

**What actually happened (observed on a real run — the prediction above was half right).**
The posterior did **not** split; it **committed hard to one type at a time and jumped**:
`AlwaysCall` (hands 1–2) → `LooseAggressive` (hands ~5–40) → **`Nash` (hand ~43+, ≈1.0)**.
This is *correct* Bayesian behavior, not a bug — the confusion came from two different
meanings of "mixture":

- The prediction pictured a **per-hand pick** (this hand play the rock, next hand the maniac);
  against that, "split between the two nearest types" would be the natural read.
- But [`opponent_types.mixture`](opponent_types.py) is a **per-action average**: with J/Q it
  plays a true `(0.5, 0.5)`, and always bets K. That smooth blend looks like `Nash`, not like
  either extreme. Every time it bets a J/Q, `TightPassive` (which never does) eats an ε-sized
  likelihood penalty; every time it checks a J/Q, `LooseAggressive` eats one. Only `Nash`
  assigns real probability to *both*, so a long stream must converge to `Nash`. The early hop
  to `LooseAggressive` is just that type scoring likelihood 1.0 on all the K-bets and J/Q-bets
  until enough check-contradictions accumulate to overturn it.

The lesson survives — a type-based model has no honest home for an opponent it can't represent,
so it lands on the nearest *mixed* type (`Nash`) rather than reporting genuine uncertainty. That
is still the motivation for the *continuous* model in Phase 4. (To actually see a two-type split,
make the mixture a **per-hand** pick instead of a per-action average.)

---

## 4. `mixture_recovery.py`

**What it does.** Directly answers the question `bayesian_type_detector.py` cannot: instead of
*"which single type are you?"* it asks *"what **mixture** of types are you?"* It fits **mixing
weights** over the four types by **Expectation–Maximization** (soft-credit each observation to the
types, average the credit, iterate) and compares that to the old single-type posterior and to the
ground-truth blend. Runs two hidden opponents: a 50/50 and a 70/30 blend of `TightPassive` and
`LooseAggressive`.

**How to play with it** (`CONFIG`): `ratios` (which blends to fit), `hands` (more → less sampling
noise), `epsilon` (likelihood smoothing), `em_iters`.

**What to watch out for.** A **hard** per-hand tally (argmax the best-fit type each hand, then
count) is *confounded by overlapping types* — `AlwaysCall` and `TightPassive` both check a weak
hand, so the argmax can't separate them. That is why EM uses *soft* responsibilities and iterates;
don't replace it with a hard count.

**How to read the results (expected — verify by running).** The single-type posterior collapses to
`Nash ≈ 1.0` (the §3 failure), while the **EM mixing weights recover the true blend** — `≈ (0.50,
0.50)` for the 50/50 opponent and `≈ (0.70, 0.30)` for the 70/30 opponent, near-zero on the other
two types. The weights are re-fit after every hand, so the PNGs are **per-hand line trajectories**
(the mixture analogue of the detector's posterior-over-time charts): after some early thrashing the
two active components climb to the dotted true-weight lines while `AlwaysCall` and `Nash` decay to
zero. This is the interpretable fix for "no honest home", and the smallest rung on the ladder to the
*continuous* and *consistent* models of Phase 4.

---

## Suggested path through it

1. `python .../kuhn_tools.py` — confirm the payoffs/Nash sanity checks read sensibly.
2. `behavioral_fingerprints.py` — *what* a type looks like.
3. `exploitation_opportunity.py` — *why* you'd bother modeling (the money gap).
4. `bayesian_type_detector.py` — *how* you infer the type from behavior, and where it breaks.
5. `mixture_recovery.py` — *how to fix* the break: recover the blend instead of collapsing to Nash.
6. `robustness_sweep.py` — *how bad the break can get*: a wrong type can lead confidently for 100–200 hands.

---

## Key takeaways for the final summary

- **Different opponent types have visibly distinct fingerprints**, and recovering a
  fingerprint from observed actions is the whole modeling task. (verify via fingerprints)
- **The exploitation opportunity is real and measurable:** ≈ 0 against Nash, clearly
  positive against exploitable types — and exploiting `TightPassive` concretely means
  *bluffing more*. (verify via exploitation_opportunity)
- **The Bayesian belief-update loop works and is fast on distinctive types**, degrades
  gracefully to a blend of nearest types when the opponent fits none, and can hard-eliminate
  types without smoothing. (verify via the detector)
- **Ask "what mixture?" not "which type?" to handle blends.** A single-type posterior
  collapses a blended opponent onto the nearest mixed type (Nash, at a misleading ≈1.0);
  fitting mixing weights by EM recovers the actual blend (≈70% rock + 30% maniac). The
  posterior is *relative* ("best of these four"), not an absolute goodness-of-fit.
  (verify via mixture_recovery)
- **Two limits show up immediately and motivate Phase 4:** (1) partial observability — we
  cheated by using the opponent's card; the real likelihood must marginalize over hidden
  hands; (2) type-based models need a *continuous* fallback when the opponent matches no type.
- **Scale caveat:** Kuhn is tiny and exact, so everything here converges almost instantly.
  Do not generalize these speeds to Leduc / real poker — that's what later phases test.
