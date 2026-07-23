# Step 10 — Targeted Reading: PBT, the League, Spinning Top, EGTA, Replicator Dynamics

> Phase 3 of Step 10. VIP-only notes on the five core papers + supplementary skims, with
> **cited** sections/theorems, four worked **Math Flags**, a synthesis, and a "verify when you
> read it" list. Built on the raw step's reading list
> ([`step_10_population_training_evo_gt.md`](../../../planning/rawSteps/step_10_population_training_evo_gt.md), L147–329).
>
> ⚠ **Anti-hallucination note (WORKFLOW §4.3):** section/theorem numbers are transcribed from
> the raw step's reading plan; the *derivations* in the Math Flags are **my reconstructions**,
> flagged as such — verify them against the actual papers before citing in the thesis.

---

## Core Paper 1 — Jaderberg et al., "Population Based Training of Neural Networks" (2017)

arXiv 1711.09846.

- **§2 (the algorithm) — the load-bearing read.** A population of models trains in parallel.
  Periodically each member is compared to the rest; a poor performer runs **exploit** (copy a
  better member's weights) then **explore** (perturb its hyperparameters). No complex math —
  PBT is an *evolutionary algorithm applied to meta-optimization* (hyperparameter choice).
- **§3 (experiments) — skim.** PBT beats grid/random search at equal or less compute.
- **Why it matters here:** the two PBT primitives map directly onto
  [`ppo_agent.py`](../implementation/ppo_agent.py)'s `clone_from` (exploit) and
  `perturb_hyperparams` (explore), and onto [`league.py`](../implementation/league.py)'s
  `_pbt_step`. **Key insight:** the population is *also* a diverse opponent set — PBT solves
  tuning and opponent-diversity at once.

## Core Paper 2 — Jaderberg et al., "Human-Level … Population-Based DRL" (FTW, Science 2019)

arXiv 1807.01281.

- **§2 (FTW architecture) — read.** Population members are matched against each other → a
  *natural curriculum*; internal rewards and population dynamics are co-evolved.
- **§2.4 (Elo) — the MATH note.** Elo is a *relative* skill measure; in a population the **Elo
  matrix is the meta-game** — it says who is strong against whom. Implemented in
  [`elo.py`](../implementation/elo.py) and tracked over epochs in the league.
- **Key insight:** population training is an *implicit curriculum* — weak face weak, strong
  face strong; the population self-organizes into a difficulty ladder with no hand-design.

## Core Paper 3 — Vinyals et al., "Grandmaster Level in StarCraft II" (AlphaStar, Nature 2019)

Nature s41586-019-1724-z / arXiv 1911.12254.

- **§2.3 (the AlphaStar League) — THE read.** Three agent roles:
  - **Main agents** — trained against the *full* league → be robust to everything.
  - **Main exploiters** — trained against the *main agents only* → punish their specific
    weaknesses (artificial selection pressure).
  - **League exploiters** — trained against the *full* league → probe anyone's holes.
  Plus a **priority (PFSP) matchmaking** mechanism for choosing opponents.
- **Methods (Nash matchmaking) — the MATH note.** Matchups use an approximate **Nash of the
  meta-game** (the game between league policies) → *AlphaStar's league IS large-scale PSRO*
  with neural agents as oracles, trained continuously rather than in discrete rounds.
- **Key insight:** exploiters solve PBT/PSRO **diversity collapse** — without them the
  population converges to one dominant style. This is the *multi-agent analog of Step 8's
  exploitation–safety tradeoff*; the roles are mirrored in
  [`league.py`](../implementation/league.py) `_opponent_indices`.

## Core Paper 4 — Balduzzi et al., "Open-Ended Learning in Symmetric Zero-Sum Games" (ICLR 2019)

arXiv 1901.01753.

- **§3 (spinning-top decomposition) — read the statement (Theorem 1).** Every antisymmetric
  payoff matrix `A = T + C`, a **transitive** part `T` (a total skill order A > B > C) plus a
  **cyclic** part `C` (pure RPS). Big cyclic component ⇒ self-play / naive PBT *cannot* converge
  (improvement is illusory — you rotate, not climb).
- **§3.2 (game-theoretic strength) — read the definition.** The transitive component defines a
  "true skill" rating; the cyclic component is noise in the ranking.
- **§4 (rectification) — skim.** Modify PSRO so only *genuinely improving* policies are added.
- **Why it matters here:** implemented in [`spinning_top.py`](../implementation/spinning_top.py)
  — see its Math Flag below and the important **Hodge-vs-SVD** correctness note.

## Core Paper 5 — Tuyls, Pérolat, Lanctot et al., "A Generalised Method for EGTA" (AAMAS 2018)

arXiv 1803.06376.

- **§3 (EGTA framework) — read.** Analyze a huge game via a **finite** strategy set: sample
  strategies, build the **empirical game** (payoff matrix between them); its Nash approximates
  the true Nash.
- **§4 (bounds) — read Theorem 1's statement.** The empirical Nash converges to the true Nash as
  the strategy sample grows; the rate depends on game structure. *This is PSRO's convergence
  rationale* (PSRO = EGTA with an expanding sample).
- **Key insight:** EGTA is the **evaluation framework** — ask "how good is the Nash of the
  empirical game my population defines?" not "how good is my one agent?" (thesis Contribution
  #3). Implemented in [`egta.py`](../implementation/egta.py).

## Supplementary skims

- **Hofbauer & Sigmund (1998/2003), "Evolutionary Game Dynamics"** — §2 (replicator equation),
  §3 (ESS). The mathematical backbone; see the replicator Math Flag below.
- **Yao et al. (2023), "Policy Space Diversity for Non-Transitive Games"** (arXiv 2306.16884) —
  §3 diversity regularization to fight PSRO collapse. Relevant to
  [`diversity.py`](../implementation/diversity.py).
- **De La Fuente et al. (2024)** (arXiv 2412.20523) — survey connecting game theory ↔
  evolutionary MARL; conceptual overview.
- **Hill (2025)** (arXiv 2509.03771) — adversarial auto-curricula; forward pointer to Step 11.
- **Xu et al. (2025)** (arXiv 2510.18407) — heterogeneous adversarial play for diversity.

---

## Math Flags (worked — **my derivations, verify against the sources**)

### 🔢 1. Replicator dynamics (Hofbauer & Sigmund) — *must understand*

Single population, symmetric game with row-payoff `A`, population state `x` on the simplex.
Fitness of pure strategy `i` and mean fitness:

\[ f_i(x) = (A x)_i, \qquad \bar f(x) = x^\top A x . \]

**Replicator equation:**

\[ \dot x_i = x_i\,\big(f_i(x) - \bar f(x)\big). \]

- **Interpretation:** a strategy's share grows iff it beats the population average — "fitter than
  average ⇒ reproduce". The simplex is invariant (\(\sum_i \dot x_i = 0\)).
- **Fixed points ↔ Nash (my derivation to verify):** at a rest point every *played* strategy
  (\(x_i>0\)) has \(f_i(x)=\bar f(x)\) — all played strategies earn the same, so no unilateral
  switch helps ⇒ a **symmetric Nash** equilibrium.
- **ESS ↔ attractor:** an interior/face rest point that is *asymptotically stable* is an
  **ESS** (Maynard Smith's invasion condition: no mutant strategy can do better against the
  incumbent mix). RPS's interior rest point is a **centre**, not an attractor ⇒ **orbits, never
  converges**.
- **Predicted outcomes** (verified by [`replicator.py`](../implementation/replicator.py) +
  `validate.py`): PD → all-Defect; Hawk-Dove → interior ESS \(p(\text{Hawk})=V/C\); RPS →
  orbit; Stag Hunt → two basins.

### 🔢 2. Spinning-top decomposition (Balduzzi et al., Theorem 1) — *statement + a correctness caveat*

An antisymmetric payoff matrix decomposes as `A = T + C`, transitive + cyclic. The transitive
ratio \( \lVert T\rVert_F / \lVert A\rVert_F \in [0,1] \) measures "how much is real skill".

- ⚠ **Correctness caveat I hit while implementing (a Math Flag to verify).** The raw step
  (L389–398) sketches taking `T` as the **rank-1 truncated SVD** of `A`. That does **not** give
  "RPS is 100% cyclic": a real antisymmetric matrix has singular values in *equal pairs*
  \((s,s,0,\dots)\), so its rank-1 SVD keeps half the Frobenius mass — RPS scores ≈ 0.707, not 0.
  The decomposition that yields "RPS = 100% cyclic" (and matches the step's own validation
  target) is the **combinatorial Hodge / HodgeRank** split that Balduzzi §3.2's "game-theoretic
  strength" is built on:
  \[ r_i = \tfrac1n\!\sum_j A_{ij}, \qquad T_{ij}=r_i-r_j, \qquad C = A - T. \]
  For RPS every row sums to 0 ⇒ all ratings 0 ⇒ `T=0` ⇒ transitive ratio 0. So
  [`spinning_top.py`](../implementation/spinning_top.py) uses the **Hodge** version and keeps the
  SVD sketch only for comparison (with this note). **Verify** which decomposition Balduzzi's
  Theorem 1 actually states before citing it.

### 🔢 3. EGTA approximation bound (Tuyls et al., Theorem 1) — *statement*

Let \(G\) be the true game and \(\hat G\) the empirical game over a finite strategy sample. The
Nash of \(\hat G\) is an **\(\epsilon\)-Nash of \(G\)**, with \(\epsilon\) shrinking as the
sample grows (rate depends on game structure / payoff-estimation error). *Consequence:* PSRO's
meta-Nash exploitability → 0 as the population covers the relevant strategy space — the
population-size ↔ exploitability curve in [`egta.py`](../implementation/egta.py) /
`psro_population_peek.py`. Here payoffs are computed **exactly** (extracted tabular policies +
Step 07's exact engine), so the *only* approximation is which policies made it into the sample.

### 🔢 4. Elo (FTW §2.4) — *the meta-game readout*

Expected score of A vs B and the update after observing score \(S_A\):

\[ E_A = \frac{1}{1+10^{(R_B-R_A)/400}}, \qquad R_A \leftarrow R_A + K\,(S_A - E_A). \]

- **Interpretation:** a logistic model of win-probability from rating differences; the update
  nudges ratings toward consistency with observed results.
- **"Elo matrix IS the meta-game":** the pairwise expected-score matrix over the population is
  exactly the empirical (meta) game's normal form. Implemented in
  [`elo.py`](../implementation/elo.py), driven by the **exact** expected scores from the league
  payoff matrix. **Caveat (verify):** Elo assumes a *transitive* skill model — in a purely
  cyclic population it degenerates (all ratings ≈ equal), which is itself informative and links
  back to the spinning top.

---

## Cross-source synthesis

- **One thread from 1978 to 2019.** Replicator dynamics (what a population *converges to*) →
  PBT (evolve weights **and** hyperparameters) → FTW (population = curriculum, Elo = meta-game)
  → AlphaStar (roles + exploiters to keep the population diverse) → Balduzzi (spinning top:
  *why* diversity is needed — cyclic structure) → Tuyls EGTA (*how to evaluate* a population).
- **The engineering ⇄ theory bridge.** AlphaStar's league is a *practical* answer to the
  *theoretical* problem Balduzzi diagnoses (non-transitivity) and Tuyls formalizes (empirical
  games). PSRO (Step 9) is the discrete-round version; the league is its continuous, role-based
  cousin.
- **Where this step lands in the thesis.** Contribution #1 (opponent modeling) ↔ exploiters as
  automated weakness-finders; Contribution #2 (safety) ↔ the *missing* formal guarantee that
  main agents stay non-exploitable (the league is heuristic); Contribution #3 (evaluation) ↔ the
  meta-Nash of the empirical game as the multi-agent generalization of exploitability.
- **Leduc vs FFA.** Leduc is predicted *mostly transitive* (self-play works reasonably; the
  league should still help a bit and won't hurt); Step 11's coalition/FFA games are predicted
  *heavily cyclic* (the diversity machinery becomes essential). The spinning-top ratio is the
  number that will tell us.

---

## Verify when you read the source

- [ ] **Replicator (H&S §2–3):** confirm the fixed-point ↔ Nash and ESS ↔ asymptotic-stability
  statements, and that RPS's interior rest point is a centre (orbits).
- [ ] **Spinning top (Balduzzi Thm 1, §3.2):** confirm *which* decomposition the theorem states
  (Hodge/ratings-based vs SVD) — my implementation uses Hodge for the RPS→0 result; the raw
  step's SVD sketch does not satisfy that target.
- [ ] **EGTA bound (Tuyls Thm 1):** transcribe the exact \(\epsilon\)-bound and its dependence on
  sample size / structure.
- [ ] **Elo (FTW §2.4):** confirm the K-factor / scale used and that "Elo matrix = meta-game" is
  stated as I paraphrased.
- [ ] **AlphaStar (§2.3 + Methods):** confirm the three roles' exact opponent sets and the PFSP
  weighting formula (my `_pfsp_weights` uses \((1-\text{winrate})^p\)).

---

## Key takeaways for the final summary

- **Replicator dynamics** give equilibria a *dynamical* meaning: fixed points ↔ Nash,
  attractors ↔ ESS, centres ↔ non-transitive cycling.
- **PBT** = exploit (copy strong weights) + explore (perturb hyperparameters); the population
  doubles as a diverse opponent set.
- **AlphaStar's league** = PBT + three roles (main / main-exploiter / league-exploiter) + frozen
  history + Nash/PFSP matchmaking; it is continuous-time large-scale PSRO and its purpose is
  fighting diversity collapse.
- **Spinning top** = the transitive+cyclic decomposition; the transitive ratio diagnoses whether
  self-play can work. **Implementation note:** use the Hodge decomposition (not rank-1 SVD) to
  reproduce "RPS = 100% cyclic".
- **EGTA** = evaluate a population by the meta-Nash of its empirical game; the multi-agent
  generalization of exploitability and the basis for thesis Contribution #3.
