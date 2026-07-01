# Step 07 — Targeted Reading: condensed VIP notes

Phase 3 of Step 07. The "cropped" version of the reading list in
[`step_07_opponent_modeling.md`](../../../planning/rawSteps/step_07_opponent_modeling.md)
(Phase 3, lines 158-318): the equations, theorems, algorithms, and results that matter —
without the surrounding bloat.

**Sourcing & confidence (per [`../../WORKFLOW.md`](../../WORKFLOW.md) §0 — no fabrication):**
- Papers **3 (Ganzfried & Sun 2016)** and **5 (Ganzfried 2025)** were read from their open
  arXiv full text; equations/theorems/numbers below are quoted/derived from those and are
  high-confidence.
- Paper **4 (Ganzfried, Wang & Chiswick 2022/2024)** is summarized from its arXiv abstract
  plus how the 2025 paper cites it — **medium confidence on internals**.
- Papers **1 (Southey 2005)** and **2 (Bard 2013)** are UAlberta PDFs I could not fetch; they
  are summarized from well-established secondary descriptions (notably the verbatim quotes
  Ganzfried & Sun 2016 reproduce) plus the raw step's reading guide — **so specific equation
  numbers / algorithm line numbers are flagged "verify" rather than asserted.**

The single most reused result in the whole list: **you only ever need to respond to the
*mean* of your posterior over opponent strategies, never the full distribution**
(Ganzfried & Sun 2016, Thm 2.1). Keep it in mind through everything below.

---

## Paper 1 — Southey, Bowling, Larson, Piccione, Burch, Billings, Rayner, "Bayes' Bluff: Opponent Modelling in Poker" (UAI 2005)

PDF: https://poker.cs.ualberta.ca/publications/UAI05.pdf

**Role.** The foundational paper: it casts opponent modeling as **Bayesian inference** and
defines the response strategies everyone else builds on (or attacks).

**Key idea.** Treat the opponent's strategy as unknown, put a **prior** over strategies,
update to a **posterior** with observed actions, and respond to the posterior. Three
responses are introduced:
- **Bayesian Best Response (BBR):** best-respond to the posterior **mean** strategy.
- **Maximum a Posteriori (MAP) Response:** best-respond to the single **most probable**
  strategy under the posterior.
- **Thompson's Response:** **sample** one strategy from the posterior and best-respond to it.

**Key math (verify exact numbering in the PDF).**
- Bayesian update: `posterior(σ | obs) ∝ prior(σ) · P(obs | σ)` (raw step flags this as
  "Eq. 3-4").
- **Dirichlet prior** over each action distribution (raw step: "Section 3.2") — chosen
  because it is the **conjugate prior** of the multinomial, so updates stay closed-form
  (see Math Flag B).
- The exact response requires an **integral over the space of opponent strategies**, which
  they note is generally intractable and approximate by **importance sampling**.

**Headline result.** Bayesian modeling extracts value even from a broad, weak prior. The
authors' own caveat (quoted in Ganzfried & Sun 2016): *"This makes the exact BBR an ideal
goal rather than a practical approach. For real play, we must consider approximations to
BBR."* — i.e. they ship the **sampling heuristics** (BBR/MAP/Thompson), not an exact method.
And: *"The independent Dirichlet prior is very broad… It is encouraging that the Bayesian
approach is able to exploit even this weak information."*

**Why it matters for the thesis.** This is the explicit-Bayesian template the implementation
phase reproduces (type-based + continuous models). It is also the method the 2025 paper
later proves **inconsistent**.

---

## Paper 2 — Bard, "Online Implicit Agent Modelling" (AAMAS 2013)

PDF: https://poker.cs.ualberta.ca/publications/AAMAS13-bard.pdf
*(Summarized from secondary sources + the raw step's guide — medium/low confidence on internals; verify.)*

**Role.** Introduces the **implicit** alternative to explicit Bayesian modeling.

**Key idea (explicit vs implicit — the conceptual axis to take away).**
- **Explicit** (Southey): maintain a *belief over opponent strategies*, then respond to it.
  Interpretable, but you must represent and update a distribution over a huge space.
- **Implicit** (Bard): **don't** maintain a belief over types. Instead keep a portfolio of
  precomputed **response strategies** and use **online learning** (an experts / regret-
  minimization rule) to adapt *which response to play* from observed outcomes. The opponent
  model is never written down — it is implicit in the response that online learning selects.

**Key math (verify in PDF).** An **online/incremental update** (raw step: "Algorithm 1")
with an online-learning regret guarantee bounding how much worse you do than the best fixed
response in your portfolio.

**Headline result (verify).** Implicit modeling is competitive with explicit modeling on
poker, is simpler to implement, and scales better — at the cost of interpretability.

**Why it matters for the thesis.** The explicit/implicit split is a framing axis for the
Behavioral Adaptation Framework. The thesis likely uses **explicit** modeling (for the
interpretability the implementation phase's models give you).

---

## Paper 3 — Ganzfried & Sun, "Bayesian Opponent Exploitation in Imperfect-Information Games" (CIG 2016/2018)

arXiv: https://arxiv.org/abs/1603.03491  ·  *(read in full — high confidence)*

**Role.** Turns Southey's "ideal goal" into the **first exact** Bayesian-best-response
algorithm for a natural class of imperfect-information games, and supplies the theory.

**Key math.**
- **Theorem 2.1 (the workhorse):** `u_i(σ_i, f̄_{-i}) = u_i(σ_i, f_{-i})`. Your payoff against
  a *distribution* `f_{-i}` over opponent mixed strategies equals your payoff against its
  **mean** `f̄_{-i}`. **Corollary 2.2** applies it to the posterior. Consequence: you never
  represent the full posterior — **just its mean**.
- **Algorithm 1 (meta-algorithm):** keep a prior `p_0`; each round set model `M_t = mean of
  the posterior`, play `R_t = r_t(M_t)` where `r_t` is any response function (best response,
  or a *safe/restricted* response).
- **Dirichlet conjugacy:** with observed private info, posterior is Dirichlet with counts
  added; mean = play each action ∝ updated counts (this is just **fictitious play**). The
  hard part: **in imperfect-information games you don't see the private card**, so you don't
  know which counter to increment. Their fix marginalizes over the hidden card; for multiple
  observations the posterior is **no longer Dirichlet**, giving Eq. (2) with a number of
  terms **exponential in #private-states n and horizon T but polynomial in T for fixed n**.
  They tame the Beta-function products with a **Stirling-based closed form (Thm 4.1)**.

**Headline results (the paper's own numbers).**
- Their **EBBR** (exact BBR) beats the Southey sampling heuristics; with only 10 samples the
  gap is large (BBR degrades, EBBR stable). Table 3 (Dirichlet α=2): `FullBR ≈ +0.497`,
  `Nash = −0.375`, `EBBR ≈ 0.000`, `BBR ≈ −0.066 → −0.31` as iterations grow.
- **The thesis-critical finding:** when the opponent's private info is *never* observed,
  *none* of the methods improve with more observations — *"to successfully learn beyond the
  prior in imperfect-information settings, algorithms will need access to some of the
  opponents' private information."* (Showdowns are exactly that access.)
- Practical caveat: numerical instability (NaN rates jump for large `n`).
- **Robustness:** a full BR to a point estimate can be very exploitable; payoff is **continuous
  in the opponent's strategy** (a small model error → small EV loss), and **restricted Nash
  response** is the safe alternative (the bridge to Step 08).

---

## Paper 4 — Ganzfried, Wang & Chiswick, "Opponent Modeling in Multiplayer Imperfect-Information Games" (DAI 2022/2024)

arXiv: https://arxiv.org/abs/2212.06027  ·  *(abstract + cross-references — medium confidence)*

**Role.** Extends Bayesian opponent modeling from 1 opponent to **N**.

**Key idea.** Collect observations of *several* opponents through repeated play and exploit
them jointly. The 2025 paper refers to this as the **sampled-BBR approach extended to
multiplayer games**. The conceptual complication (raw step): the posterior is now over
**tuples** of opponent strategies, and the optimal response to A and B **jointly** is not the
combination of the individual best responses.

**Headline result (verified from abstract).** On **3-player Kuhn poker**, against a wide
variety of real opponents *and* the exact Nash equilibrium strategies, *"our algorithm
significantly outperforms all of the agents, including the exact Nash equilibrium
strategies."*

**Why it matters.** Direct input to thesis Contribution #2 (multi-agent safe exploitation)
and Step 11. **Verify in PDF:** the exact modeling algorithm and the experimental tables.

---

## Paper 5 — Ganzfried, "Consistent Opponent Modeling in Imperfect-Information Games" (2025, rev. 2026)

arXiv: https://arxiv.org/abs/2508.17671  ·  *(read in full — high confidence; the current frontier)*

**Role.** Shows the whole BBR line has a hidden flaw and fixes it with a convex,
sequence-form method. This is the paper the thesis most directly extends.

**The flaw — consistency.**
- **Definition 1 (consistency):** an algorithm is *consistent* if its opponent model
  `M_t → σ*_{-i}` as `t → ∞` against a static opponent, **for every** set of internal samples.
- **Proposition 1:** **BBR is not consistent.** RPS example: if `σ* = (0.8, 0.1, 0.1)` and your
  sampled strategies don't span it, the model — always a *convex combination of the samples* —
  cannot reach `σ*`.
- **Proposition 2:** BBR is **not consistent even when `σ*` is inside the convex hull** of the
  samples. RPS with `σ* = (1/3,1/3,1/3)` and 3 samples averaging to it: asymptotically the
  posterior weight on a sample `(x1,x2,x3)` behaves like `x1^{t/3} x2^{t/3} x3^{t/3}`, so the
  single highest-product sample wins with probability → 1 and the model collapses to **one
  sample**, not the true mix.

**The fix — sequence-form MAP via convex optimization.**
- Use the **sequence-form** (Koller–Megiddo–von Stengel): realization probabilities `y_r` over
  action sequences, constrained by `F y = f, y ≥ 0` (linear, **polynomial** in tree size vs.
  exponential normal form).
- **Observability function** `o_i(ℓ)` = the set of trajectories consistent with what player `i`
  actually saw at leaf `ℓ` (fold → opponent card hidden; showdown → revealed). This is the
  formal handle on partial observability.
- **Likelihood** of one observation: `Σ_{r ∈ o_i(ℓ_t)} q_r y_r` (with `q_r` the normalized
  chance probabilities).
- **Log-posterior, maximized — Eq. (1):**

```
max_y   Σ_r (α_r − 1) log(y_r)  +  Σ_t log( Σ_{r ∈ o_i(ℓ_t)} q_r y_r )
s.t.    F y = f ,   y ≥ 0
```

- **Proposition 3:** if `α_r ≥ 1`, this is a **concave maximization** (⇒ convex minimization by
  negation) — any local optimum is global.
- **Algorithm:** **projected gradient descent**. Gradient `r`-th component:
  `(1 − α_r)/y_r − Σ_{t: r∈o_i(ℓ_t)} q_r / (Σ_{r'} q_{r'} y_{r'})`; step `z = y − η ∇f`; then a
  **projection** `argmin_{Fy=f, y≥0} ‖y − z‖²` (a convex QP, solved with Gurobi in their code).
  They call the method **FMAP** ("full MAP" — it returns the posterior **mode**, not the mean).
- **Proposition 4 (consistency under persistent excitation):** under (i) `σ*` in the interior
  of the feasible set with positive prior density, (ii) **identifiability** (distinct
  strategies ⇒ distinct observation distributions), and (iii) **persistent excitation** (every
  opponent info set visited infinitely often), the posterior **concentrates at `σ*`** and MAP
  estimates converge a.s. to `σ*`.

**Headline results (the paper's own numbers, Kuhn poker, Dirichlet α=2, T=3000, 100 opponents
from the prior, samplers use k=10).** `BestResponse = 0.576` (oracle ceiling),
`BestNash = 0.173`, game value to P1 `= −1/18 ≈ −0.056`. **FMAP ≈ 0.573** (nearly the BR
ceiling) and surpasses the samplers within ~100 hands; `BBR = 0.557`, `Thompson = 0.547`,
`MAP = 0.537`. Honest caveats from the paper: FMAP returns the **mode**, which is *consistent*
but **not the payoff-optimal mean** (computing the mean is intractable here); and the
multiplayer extension is **no longer convex** (products of variables).

**Why it matters.** This is the most recent, most principled model and the natural backbone
for the thesis's Behavioral Adaptation Framework. The implementation phase reproduces it
(`consistent_model.py`).

---

## Supplementary book — Shoham & Leyton-Brown, *Multiagent Systems* (2008), Ch. 7 "Learning and Teaching"

Free PDF: http://www.masfoundations.org/download.html  ·  *(framing only — read §7.1-7.3)*

**Role / takeaway.** Frames opponent modeling as a **learning problem in repeated games**
with partial feedback. §7.1-7.3 give the formal vocabulary (fictitious play, rational
learning, targeted optimality / safety, the "learning vs. teaching" tension — your actions
both *exploit* and *teach* the opponent). It is the connective tissue under all five papers.
You know the game-theory prerequisites (normal/extensive form, Nash) from Steps 2-4.

---

## Cross-source synthesis (the through-line)

```
Southey 2005      explicit Bayesian model; BBR/MAP/Thompson; exact integral intractable -> sampling
   |
Bard 2013         implicit alternative: adapt the RESPONSE online, don't store a belief
   |
Ganzfried&Sun 16  Thm 2.1: respond to the MEAN; first EXACT BBR; but w/o private info you
   |                can't learn beyond the prior  ->  showdowns matter
Ganzfried+ 2022   extend (sampled) BBR to N players; beats exact Nash in 3-player Kuhn
   |
Ganzfried 2025    BBR is INCONSISTENT (Props 1-2); fix = sequence-form convex MAP (FMAP),
                  consistent under identifiability + persistent excitation (Prop 4)
```

Two orthogonal axes recur: **explicit vs implicit** (store a belief vs. adapt the response),
and **what you optimize** — the posterior **mean** (payoff-optimal, Thm 2.1, often
intractable) vs. the **mode/MAP** (FMAP — tractable & consistent, slightly sub-optimal). The
**safety** half (restricted Nash response, ε-safe best response) is repeatedly cited but
deferred to **Step 08**.

---

## Worked Math Flags (raw step, lines 308-318)

> These are the agent's worked derivations to build intuition. **They must be checked by
> hand when you read the papers** — they are not copied from the sources.

### A. Bayesian posterior update — by hand (Math Flag #1)
Three candidate types; at one info set their probability of **bet** is `T1=0.8, T2=0.5,
T3=0.1`. Uniform prior `(1/3, 1/3, 1/3)`. Observe **bet**:

```
posterior ∝ prior × P(bet|type)
         ∝ (1/3·0.8, 1/3·0.5, 1/3·0.1) = (0.267, 0.167, 0.033)
normalize (÷0.467)         -> (0.571, 0.357, 0.071)
observe a 2nd bet, multiply by (0.8,0.5,0.1) again, normalize
                            -> (0.711, 0.278, 0.011)
```

The belief concentrates on the bet-happy type T1 — and would do so faster the more the types
disagree. (This is exactly what `exploration/bayesian_type_detector.py` does numerically.)

### B. Dirichlet–multinomial conjugacy (Math Flag #2)
Prior `Dir(α_1,…,α_K)` over an action distribution; observe action counts `n_1,…,n_K`. Then
the posterior is **closed-form, again Dirichlet**:

```
posterior = Dir(α_1 + n_1, …, α_K + n_K)
posterior mean of action i = (α_i + n_i) / Σ_j (α_j + n_j)
```

Why it's *the* prior here: conjugacy means updating is **just adding observed counts to
pseudo-counts** — no integral, no MCMC. The `α_i` act as **Laplace-smoothing** pseudo-counts,
which is exactly the continuous model in Phase 4. (Standard result; high confidence.)

### C. Sequence-form convex formulation (Math Flag #3 — Ganzfried 2025, Eq. 1 / Prop 3)
Maximize the log-posterior over realization probabilities `y` subject to the sequence-form
constraints (see Paper 5 above for the full statement). It is **concave** because
`(α_r−1)log y_r` is concave for `α_r ≥ 1`, and `log(Σ_r q_r y_r)` is a log of an affine
function (concave by the composition rule); the constraints `Fy=f, y≥0` are affine. Hence a
unique global optimum, reachable by **projected gradient descent**. This convexity — only
visible in sequence form — is the entire reason the consistent method is tractable.

---

## Verify when you read it (don't trust this doc for these)

- **Southey 2005:** exact equation numbers for the Bayesian update ("Eq. 3-4") and the
  Dirichlet section ("3.2"); the real-poker experimental win rates.
- **Bard 2013:** the actual implicit-update algorithm and its regret guarantee; the
  explicit-vs-implicit experimental comparison.
- **Ganzfried & Sun 2016:** the exact Eq. (2) term count and the Stirling approximation
  (Thm 4.1) details — only if you need the efficiency argument.
- **Ganzfried, Wang & Chiswick 2022:** the multiplayer modeling algorithm and result tables
  (I summarized from the abstract).
- **Ganzfried 2025:** the precise sequence-form matrices `E, F, A` for Kuhn (their Tables
  1-3) and the gradient/projection step-size details, before you reimplement `consistent_model.py`.

---

## Key takeaways for the final summary

- **Opponent modeling = Bayesian inference, and you only ever respond to the posterior
  *mean*** (Ganzfried & Sun 2016, Thm 2.1) — not the whole distribution.
- **Dirichlet is the natural prior** because of multinomial conjugacy: updating = adding
  observed counts to pseudo-counts (Math Flag B); this *is* the continuous model.
- **Partial observability is the crux:** without seeing the opponent's private card you can't
  increment the right counter, and (Ganzfried & Sun 2016) you **can't learn beyond the prior**
  — showdowns are the information that lets you.
- **Two design axes:** explicit vs implicit (store a belief vs adapt the response), and
  mean vs mode (payoff-optimal-but-intractable vs FMAP's consistent-but-slightly-suboptimal).
- **The current frontier is *consistency*** (Ganzfried 2025): BBR can converge to the wrong
  strategy even with infinite data (Props 1-2); the sequence-form **convex MAP** fixes it
  (Prop 3-4) and is what `implementation/consistent_model.py` reproduces.
- **Exploitation needs a safety valve** (restricted Nash / ε-safe response) — repeatedly
  flagged here, formalized in **Step 08**.
- **Multiplayer is not N× single-opponent** (Ganzfried+ 2022): joint best response ≠ combined
  individual best responses; and the 2025 convex result **breaks** for N>2.
