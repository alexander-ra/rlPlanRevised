# Step 07 — Implementation (Phase 4): Bayesian Opponent Modeler + Adaptive Exploiter

Full, runnable code for the opponent-modeling project on **Kuhn Poker** (Step 02 engine) and
**Leduc Hold'em** (Step 03 engine). It implements all three opponent models, best-response
against an inferred model, the adaptive exploitation pipeline, a tournament with a
non-stationarity test, plotting, and a validation harness.

> **This code was written but NOT run** (per `implementation/WORKFLOW.md` §0). Every number
> below is a **prediction / target to verify**, not a measurement. You run it, validate it
> against the raw step's targets, and refine. The "Likely-to-break" and "Static self-review"
> sections are here precisely because the author could not smoke-test anything.

Source of truth for *what* to build: `planning/rawSteps/step_07_opponent_modeling.md`
(Phase 4 deliverables **L448–458**, validation targets **L460–465**, day-by-day **L342–446**).

---

## 0. Conventions & dependencies

- **Import, never copy** (WORKFLOW §6): the two engines are loaded *directly from their
  files* via `importlib` in `engines.py`. This is deliberate — step02 and step03 both ship a
  package named `cfr`, and putting both on `sys.path` would merge them into one namespace
  package and silently cross-wire `cfr.info_set_node` (Kuhn's 2-action node vs Leduc's
  3-action node). Loading the standalone engine files under unique names sidesteps that
  entirely.
- **Run from this folder.** Each module imports its siblings by plain name
  (`from engines import ...`), so launch scripts with `implementation/step07/implementation/`
  as the working directory.
- **Dependencies:** core needs only the Python stdlib. `consistent_model.py` needs
  **numpy + scipy**. `plotting.py` needs **matplotlib**. `compare_openspiel.py` needs
  **open_spiel**. All optional deps are guarded with clear messages.
- **Determinism:** every script seeds its RNG and exposes the seed.
- **Compute reality (config.py):** this step is **CPU-bound and tabular** — CFR, exact tree
  traversal, a small SciPy convex program. **The RTX 5090 does not speed any of it up** (no
  GPU kernels here). "Scale" just means more hands / CFR iterations. The GPU matters in later
  (function-approximation) steps, not this one.

---

## 1. What was built — module map

Each file has a `__main__` self-test you can run in isolation (great for incremental
debugging). Mapping is to the raw step's Phase-4 deliverables (L448–458) / day plan.

| File | What it is | Raw-step deliverable / day |
|------|-----------|-----------------------------|
| `engines.py` | Uniform `Game` adapter over the Kuhn & Leduc engines (legal actions, info sets, utilities, **observability**: who is revealed at showdown vs fold). | starting point (L327) |
| `policies.py` | The common `policy(game,state)->{action:prob}` currency; `play_hand`, **`replay`** (re-derive info sets under a hypothesized deal), tabular/uniform/blend constructors. | infra (Day 1, L344) |
| `opponent_types.py` | The type zoo for both games + Nash + Random + a behavioral `mixture`; eps-smoothed so no type ever has a zero-probability action. | type library (L449, Day 1 L346–348) |
| `level_k.py` | **[P5]** Level-k / cognitive-hierarchy opponents (L0=uniform, Lk = BR to L(k−1)). | enrichment opponent |
| `observation_buffer.py` | Records hands from the modeler's seat; the single home of **partial observability** (`candidate_deals`, `opp_decisions_for_deal`). | observation buffer (L450, Day 1 L349–353) |
| `inference.py` | `logsumexp` + the marginalized opponent log-likelihood (scores only the opponent's actions, marginalizing hidden cards). | likelihood (Day 2 L356–361, Day 4 L374–379) |
| `bayesian_model.py` | The tiny shared model interface (`update` / `observe` / `predicted_policy`). | bayesian skeleton (L356) |
| `type_based_model.py` | Discrete **Dirichlet-multinomial** posterior over K types; MAP type + model-averaged policy. | type-based model (L451, Day 3 L365–372) |
| `continuous_model.py` | Per-info-set **Dirichlet** estimate; showdowns → hard counts, folds → soft (EM) counts. | continuous model (L452, Day 5 L383–389) |
| `consistent_model.py` | **Ganzfried 2025** sequence-form MAP via a SciPy convex solve; reads back a behavioral strategy. | consistent model (L453, Day 6 L394–401) |
| `best_response.py` | Exact info-set-constrained BR against **any** opponent policy; `exact_value`; `nash_gap` (=NashConv). | BR vs model (L454, Day 7 L403–410) |
| `nash.py` | Engine-agnostic vanilla CFR → Nash baseline (cached to `_cache/`). | Nash baseline / safety |
| `adaptive_exploiter.py` | observe→model→BR→act loop; Nash **safety** blend; **[P8]** change-point forgetting; opponent schedules. | pipeline (L455, Day 8 L412–418) |
| `changepoint.py` | **[P8]** Bayesian online change-point detection (Adams & MacKay) on opponent aggression. | non-stationarity (Day 9 L432–435) |
| `tournament.py` | Runs detection + exploitation (with exact ceilings) + non-stationarity; prints tables; writes `results/*.json`. | comparison + curves (L456–457, Day 9) |
| `plotting.py` | Exploitation bars, cumulative curves, non-stationarity, posterior evolution. | plots (L457) |
| `config.py` | `smoke` (fast default) vs `scale` configs; runtime notes. | two configs (WORKFLOW §7) |
| `validate.py` | **The verification harness** — checks the raw step's targets, prints PASS/FAIL. | validation (L460–465) |
| `compare_openspiel.py` | Guarded OpenSpiel cross-check of NashConv (mapping-free). | cross-validation (L458, L465) |

**Main entry points:** `python validate.py` (correctness) and
`python tournament.py --config smoke` (the headline experiment).

---

## 2. How to verify (run in this order)

All commands are run from `implementation/step07/implementation/`.

1. **Engines & plumbing self-tests** (each prints OK-style lines; nothing should raise):
   ```bash
   python engines.py        # #deals 6/120; 0 zero-sum violations; known Kuhn payoffs OK
   python policies.py       # replay reproduces sampled hands
   python nash.py           # Kuhn exact_value(Nash,Nash) ~ -1/18; NashConv ~ 0; 12 info sets
   python best_response.py  # BR vs uniform > 0 for both games
   python opponent_types.py # every type returns a legal, normalized distribution
   python level_k.py        # Level1 beats Level0; tables cache
   python observation_buffer.py  # showdown rate sensible; candidate_deals=1 at showdowns
   ```
2. **Model self-tests:**
   ```bash
   python type_based_model.py   # posterior concentrates on the hidden TightPassive
   python continuous_model.py   # recovered P(BET|Jack) ~ LooseAggressive's 0.85 (minus eps)
   python consistent_model.py   # 13 Kuhn sequences; solver succeeds; King-bet ~ 1-eps
   python changepoint.py        # detects a 0.1->0.9 aggression switch near the true point
   python adaptive_exploiter.py # positive mean/hand vs TightPassive
   ```
3. **The validation harness (the important one):**
   ```bash
   python validate.py           # prints PASS/FAIL per raw-step target; exit 0 if all pass
   ```
4. **The tournament + plots:**
   ```bash
   python tournament.py --config smoke      # Kuhn only, < ~1 min CPU; writes results/ + plots/
   python tournament.py --config scale      # Kuhn+Leduc+consistent; minutes-to-longer (see config)
   ```
5. **Optional cross-validation:**
   ```bash
   python compare_openspiel.py  # SKIPs cleanly if open_spiel is absent
   ```

### Pass/fail thresholds (raw step Validation, L460–465) — framed as targets

| Check (`validate.py`) | Target | Source |
|---|---|---|
| Kuhn Nash value | `exact_value(Nash,Nash)` within 0.01 of **−1/18** | game value (L17 of kuhn engine) |
| Kuhn Nash unexploitable | `NashConv(Nash,Nash) < 0.05` | self-consistency |
| BR beats uniform | `BR0 vs uniform > 0` (Kuhn & Leduc) | sanity |
| Type-based detection | posterior on true type **high** & MAP correct | L461 (~90% within ~20 hands) |
| Continuous recovery | mean TV(estimate, truth) small | L462 (within 5% after 500 obs) |
| Consistent recovery | recovers a known strategy; constraints satisfied | L463 |
| Exploiter vs Nash | realized mean/hand **> Nash EV** and **≤ exact ceiling** | L464 |
| Cross-validation | NashConv matches OpenSpiel within 0.001 (Kuhn)/0.01 (Leduc) | L465 |

> The harness uses slightly **looser, robust** thresholds than the raw step's headline
> numbers (e.g. it checks the type posterior after ~500 hands, not exactly 20). Reasons are
> in "Expected outcomes" — tighten them once a clean run confirms the qualitative behavior.

---

## 3. Expected outcomes (PREDICTIONS — verify; nothing was run)

- **Detection (type-based).** Against a hidden type that is in the zoo, the posterior should
  concentrate on the truth. The raw step's "≈90% within ~20 hands" (L461) is realistic for a
  *very* distinct type (e.g. TightPassive vs a small candidate set). Here the candidate set
  is larger (Nash, Random, Level-k as distractors) and types are **eps-smoothed (0.05)**, so
  expect concentration to be **a bit slower** and to plateau **below 1.0** (eps caps it).
  To hit the strict L461 target, shrink the candidate set and lower eps.
- **Detection (continuous).** Mean total-variation distance to the true strategy should fall
  toward ~0 with data. Frequently-visited info sets converge fast; **rarely-reached** ones
  (and Leduc's many info sets under partial observability) need far more hands — this is the
  predicted reason Leduc "converges slowly" (raw step Learning-Log L512).
- **Detection (consistent).** The recovered strategy should match the truth **and** be a
  valid realization plan (the SciPy solve enforces the sequence-form constraints exactly).
  Predicted to be the most accurate under partial observability — and the most likely to need
  a debugging pass (see below).
- **Exploitation.** For exploitable types (TightPassive, Maniac, CallingStation, …) the
  realized mean/hand should be **strictly positive** and climb toward the **exact BR ceiling**
  the tournament prints alongside it; against **Nash** it should sit ≈ the Nash EV (you
  **cannot** exploit an equilibrium — a key sanity result, raw step Day 7 L410). The exact
  `nash_ev` and `ceiling` are **analytical**, so they are the trustworthy yardstick for the
  simulated curves.
- **Non-stationarity.** With change-point detection ON, post-switch mean/hand should recover
  faster than with a static model (which keeps exploiting a stale read). Predicted: the
  `changepoint` variant's `mean_after_switch` ≥ the `static` variant's (raw step Day 9
  L432–435; the static consistent model is expected to handle switches **poorly** — logged as
  the open question).

---

## 4. Likely-to-break list (where to look first on a real run)

1. **`consistent_model.fit()` (highest risk).** The SciPy `trust-constr` solve with
   `jac=True`, bounds, and the treeplex equality constraints is the most fragile piece. If it
   fails to converge or returns junk: (a) try `method="SLSQP"`; (b) raise
   `prior_pseudocount` (more interior, better-conditioned); (c) print
   `SequenceForm.num_seq` and the constraint matrix rank; (d) sanity-check that
   `_behavioral_from_y` sums to 1 per info set. **Start with Kuhn** (13 sequences); only try
   Leduc once Kuhn is clean (Leduc's program is much larger and slower).
2. **Type-detection thresholds.** If `validate.py`'s type check fails, it is almost certainly
   the eps-smoothing + distractor types making the posterior plateau below the target, **not**
   a logic bug. Confirm with `type_based_model.py`'s self-test first.
3. **Continuous model on rarely-visited info sets.** TV can stay high purely from
   undersampling specific info sets. Increase hands or inspect `model.counts` coverage before
   suspecting the estimator.
4. **Leduc runtime.** Full-tree CFR + traversals + (optionally) the consistent solve over
   Leduc's larger tree are the slow paths. If `--config scale` drags, lower `nash_iters` or
   keep `include_consistent=False` for Leduc.
5. **OpenSpiel mapping.** `compare_openspiel.py`'s primary check is mapping-free and should be
   solid; the *second* (mapping our trained Nash into OpenSpiel) is an explicit **TODO** —
   verify OpenSpiel's `information_state_string` format before trusting it.
6. **Nash quality (Leduc).** The safety baseline and the `nash_ev`/`ceiling` references use
   CFR-trained Nash; too few iters → a weak baseline. Bump `nash_iters` if references look off.
7. **Adaptive exploiter + consistent model.** Refitting the convex program every
   `refit_every` hands is expensive; for long matches prefer the type-based/continuous models,
   or increase `refit_every`.

---

## 5. Static self-review (what was checked by reading, since nothing ran)

- **Engine integration matches the real APIs.** Verified against `kuhn_poker.py` /
  `leduc_poker.py`: Kuhn's `get_terminal_utility` is only valid for the player-to-act, so
  `KuhnGame.utility` reuses the validated `cur`-player + sign-flip pattern from the
  exploration's `kuhn_tools.py`; Leduc uses `LeducState`'s variable `legal_actions` and the
  `folded` flag for observability.
- **Zero-sum & observability** invariants are spot-checked in `engines.py`'s self-test
  (utilities antisymmetric; showdown reveals both, fold reveals neither).
- **Best response** generalizes step03's iterative info-set BR (counterfactual reach excludes
  the hero's own action probabilities; chance folded in via `deal_prob`); `nash_gap` returns
  `br0+br1`, which equals OpenSpiel's NashConv in zero-sum games (used by the cross-check).
- **CFR** is the standard vanilla full-tree form (regret-matching, reach-weighted average,
  player-1 regrets negated); cross-checked by the Kuhn value target.
- **Likelihoods** score only the opponent's actions and marginalize hidden cards via
  `candidate_deals` + deterministic `replay`; a log-probability floor prevents `-inf`
  blow-ups (Nash/BR can assign exact zeros).
- **eps-smoothing** guarantees no candidate type kills a hypothesis on one surprising action.
- **Consistent model:** the sequence-form objective is **concave** (log of a sum of
  realization weights + a non-negative `log y` regularizer) and the constraints are the exact
  treeplex equalities — so the program is convex (the children-only prior is a deliberate,
  documented simplification to preserve concavity).
- **No `cfr` namespace clash** (importlib loads engines under unique names).
- **Results are JSON-serializable** (plain floats/lists/strings only); curves are downsampled.
- **Could NOT be verified without running:** numerical convergence rates, exact threshold
  attainment, SciPy solver behavior on Leduc, and matplotlib/OpenSpiel availability. These are
  exactly what the runbook in §2 and the harness in `validate.py` exist to confirm.

---

## Key takeaways for the final summary

- **One interface, three models.** Type-based (Dirichlet over K types), continuous
  (per-info-set Dirichlet), and consistent (sequence-form MAP) all reduce to "consume
  observations → emit a policy," which the **same** exact best-response then exploits. This
  uniformity is the prototype of Contribution #1's "sensor."
- **Partial observability lives in one place.** Folds hide the opponent's card; the model
  *marginalizes* over the consistent cards using deterministic replay of the public action
  sequence. Showdowns are strictly more informative (single candidate deal) — quantify the
  "~3× more informative" claim (raw step L381) when you run it.
- **The exploitation ceiling is exact, so it is the yardstick.** `nash_ev` (equilibrium can't
  be exploited → ≈0 gain) and `ceiling` (true best response) bound every learning curve; the
  gap to ceiling **is** the modeling error (raw step L443–444).
- **Sequence form = convexity.** Estimating in realization-plan space turns the
  partial-observability MAP into a convex program with a clean global solution — the thesis-
  critical idea from Ganzfried (2025).
- **Stationarity is the load-bearing assumption.** All three models assume it; the
  change-point detector ([P8]) is the minimal fix that lets the exploiter recover after a
  switch — directly motivating the non-stationarity thread for the thesis (raw step L496).
- **Predicted model trade-off** (to confirm empirically): type-based fastest *when
  well-specified*, continuous most robust *off-grid*, consistent most principled *but
  costliest* — the basis for a "structural prior early, consistent model as data grows"
  hybrid (raw step L492).
