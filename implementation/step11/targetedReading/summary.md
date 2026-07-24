# Step 11 — Targeted Reading: coalitions, Shapley credit, and the N-player safety shift

> Phase 3 of Step 11. The cropped, VIP-only distillation of the step's sources (raw
> [`step_11_coalition_formation_ffa.md`](../../../planning/rawSteps/step_11_coalition_formation_ffa.md),
> L162-329). **Anti-hallucination contract (WORKFLOW §0, §4.3):** short glosses only; every
> formula/result cites a section or equation *as numbered in the source*; where I could not verify
> a number against an open copy I say so explicitly; my own derivations under "Math Flags" are
> labelled **TO VERIFY**. Nothing here was executed or re-derived on a machine this session.

**Reading status disclosure.** These notes are built from the papers' open arXiv abstracts +
structure, the raw step's READ/MATH/KEY-INSIGHT annotations, and standard textbook knowledge of
the cooperative-GT concepts. Section/equation numbers are cited **as the raw step cites them**;
confirm them against the PDFs (see the "verify when you read it" list). Where a paper is not open
access (Chalkiadakis book; CICERO in *Science*) I summarize from the raw step + public material
and flag it.

---

## Paper 1 — Sharan & Adak, "Reinforcing Competitive Multi-Agents for Playing 'So Long Sucker'" (2024)

**Link:** https://arxiv.org/abs/2411.11057 · **Role:** the *first* RL paper on SLS and the direct
starting point for the environment + baselines.

- **Key idea (2-4 sentences).** Formalize SLS as a multi-agent RL environment (state encoding,
  action space, reward for a game where 3 of 4 players LOSE) and train self-play agents with
  standard value-based deep RL — DQN, Double DQN, Dueling DQN. Agents learn to play *legally* and
  beat a random baseline, reaching roughly half of the maximum attainable reward, but exhibit **no
  coalition-aware mechanism** — each decision is made independently with no notion of alliance.
- **Where the meat is (raw L169-176).** §2 = game formalization (state representation for the net,
  action space, reward structure — *the* thing to lift for our env); §3 = self-play training setup
  (which DQN variants, training horizon, number of games); §4 = results (~50% of max reward,
  outperforms random; look for any emergent coalition-like patterns — the raw step's answer is
  "likely none").
- **Key math.** None substantive — the raw step's MATH note (L180-182) says explicitly "no complex
  math; read the state representation carefully." The one design question worth extracting: **how do
  you reward an agent when only 1 of 4 wins?** (their reward shaping is the reference point for our
  sparse `+1 / -1/(N-1)` vector).
- **Headline result.** Trained agents reach ≈50% of the maximum reward and beat random; **no
  coalition behavior emerges** from vanilla DQN. *(Percentage cited from the raw step's summary
  L176/L184-187; verify the exact figure and its definition of "maximum reward" in §4.)*
- **Why it's in the step (KEY INSIGHT, raw L183-187).** This is the **gap statement**: the first
  RL treatment of SLS uses coalition-*blind* DQN. Step 11 fills the gap by adding (i) coalition
  detection (Step 7's opponent model → alliance model) and (ii) coalition-aware training (Shapley
  credit assignment).

## Paper 2 — De Carufel & Jerade, "So Long Sucker: Endgame Analysis" (2024)

**Link:** https://arxiv.org/abs/2403.17302 · **Role:** the definitive formal rules + the exact
2-player endgame — our environment-correctness ground truth.

- **Key idea.** Give a precise mathematical formalization of SLS and completely characterize the
  **2-player endgame**: when only two players remain, who wins (and how) is analytically decidable.
  The 4-player mid-game (where coalition dynamics live) is left as the hard, open part.
- **Where the meat is (raw L195-201).** §2 = the definitive formal rules (use to verify our
  engine); §3 = endgame characterization (2-player winning conditions). §§4-5 = deeper combinatorial
  analysis (skim). The paper is ~51 pages — **read theorem statements, skip proofs** (raw L201).
- **Key math (theorems, raw L202-207).** **Theorems 1-3** characterize the winning conditions in
  the 2-player endgame. *I have NOT verified the exact statements against the PDF* — the raw step
  instructs "READ STATEMENTS, skip proofs" and use them as ground truth for evaluating whether an
  agent that reaches a 2-player endgame is playing optimally. **Assumptions to check when you read:**
  the exact rule variant they formalize (chip counts, the "kill"/prisoner rule, turn order after a
  capture) — our engine (`sls_game.py`) makes explicit simplifications (its `# NOTE (a)/(b)/(c)`)
  that must be reconciled with their §2 before the endgame check is fully trustworthy.
- **Headline result.** The 2-player endgame is **completely solved**; the interesting complexity is
  in the ≥3-player game.
- **Why it's in the step (KEY INSIGHT, raw L205-207).** A perfect, exact evaluation anchor for a
  subgame of an otherwise unsolvable game — exactly what `sls_endgame.py` uses (exact minimax on our
  ruleset, pending the paper cross-check).

## Paper 3 — Bakhtin et al., "Mastering the Game of No-Press Diplomacy" (2022)

**Link:** https://arxiv.org/abs/2210.05492 · **Role:** the template for N-player play and the source
of **piKL** — the N-player replacement for a Nash safety baseline (thesis Contribution #2).

- **Key idea.** In a 7-player, simultaneous-move, implicit-alliance game, don't chase Nash (it is
  intractable and, in Diplomacy, degenerate). Instead run a **regularized policy search (piKL)** that
  keeps the agent's policy close to a **human-behavioral prior** while improving expected value, and
  use sampled-rollout search for real-time planning. This yields human-level no-press Diplomacy.
- **Where the meat is (raw L214-228).** §2 = handling N>2 players + **piKL** (§2.2 the regularizer);
  §3 = search (sampled rollouts + evaluation — the N-player analog of Step 6 subgame solving, but
  with no single "opponent"); §4 = results + emergent alliance/betrayal patterns.
- **Key math — piKL (§2.2, raw L234-238, Math Flag L328-329).** The regularized objective, in the
  raw step's notation:

  > πKL solves, per player, `argmin_π  KL(π ‖ π_human) + λ · E[loss]` — i.e. maximize expected value
  > (minimize expected loss) while staying KL-close to the human anchor `π_human`, trading the two
  > off with `λ`.

  Equivalent reading: it is an entropy/KL-regularized best response toward `π_human` rather than
  toward uniform. **Assumptions / what breaks:** you need a good behavioral prior `π_human` (learned
  from human games); as `λ→∞` you recover greedy value-maximization (drift away from interpretable
  play), as `λ→0` you collapse onto the prior. *I am paraphrasing the objective from the raw step's
  Math Flag; verify the exact form, the direction of `λ`, and any temperature term against §2.2.*
- **Headline result.** Human-level no-press Diplomacy; agents form and break alliances.
- **Why it's in the step (KEY INSIGHT, raw L239-245).** The **profound shift**: in N-player games
  the "safe" baseline is no longer Nash but a **behavioral prior** — deviate only when provably
  profitable. This is the seed of thesis Contribution #2 (safe exploitation in N-player FFA uses a
  behavioral/population baseline, not an equilibrium one).

## Paper 4 — Chalkiadakis, Elkind & Wooldridge, "Computational Aspects of Cooperative Game Theory" (2011)

**Link:** Morgan & Claypool Synthesis Lecture (~160 pp; via university library — **not open
access**). **Role:** the reference textbook for the cooperative-GT solution concepts.

- **Key idea.** Cooperative GT asks "*which coalitions form and how is the payoff divided?*"
  (contrast the non-cooperative "what does each individual do?" of Steps 2-8). It makes the classical
  concepts **algorithmic**: representation, computation, and complexity of each solution concept.
- **What to read (raw L254-257).** Ch. 1 = coop vs non-coop (skim; much is familiar). **Ch. 2-3
  (READ)** = the solution concepts: **Shapley value, core, nucleolus, bargaining set** — for each:
  informal meaning, formula, *existence* (some games have an empty core!), and computational
  complexity. **Ch. 4 (READ)** = **coalition-structure generation** — finding the optimal partition
  of players; the search space is `2^N` coalitions / `B_N` (Bell number) partitions, so it grows
  super-exponentially. Ch. 5+ = extensions (externalities, overlapping/dynamic coalitions) — skim
  titles (this is where the thesis's *dynamic* gap lives).
- **Key math (raw L260-266, Math Flags L322-326).**
  - **Shapley value:** `φ_i(v) = Σ_{S ⊆ N\{i}} [ |S|!(n-|S|-1)! / n! ] · [ v(S∪{i}) − v(S) ]` — the
    average marginal contribution of `i` over all join orders. (Worked below.)
  - **Core:** the set of allocations `x` with `Σ_i x_i = v(N)` (efficiency) and, for every coalition
    `S`, `Σ_{i∈S} x_i ≥ v(S)` (no group can do better alone). A **linear-programming** feasibility
    region; it can be **empty**.
  - **Nucleolus:** lexicographically minimizes the sorted vector of coalition "excesses"
    `e(S,x)=v(S)−Σ_{i∈S}x_i`; always exists, lies in the core when the core is non-empty.
- **Headline.** Cooperative GT hands you the *tools* to analyze coalitions, but classical theory
  assumes **static** coalitions fixed before play.
- **Why it's in the step (KEY INSIGHT, raw L267-271).** The tools (who cooperates, how to divide,
  when stable) are exactly what we need — but the **dynamic** case (coalitions forming/dissolving
  *during* play) is unaddressed. That gap is the Step 11 / thesis frontier.

## Paper 5 — Wang, Zhang, Kim & Gu, "Shapley Q-value: A Local Reward Approach to Solve Global Reward Games" (AAAI 2020)

**Link:** https://arxiv.org/abs/1907.05707 · **Role:** the concrete recipe for turning Shapley into a
MARL **credit-assignment** signal — the training mechanism of this step.

- **Key idea.** In cooperative MARL with only a global team reward, decompose the joint action-value
  into per-agent **Shapley Q-values**: each agent's credit is its average marginal contribution to
  the team's Q across all coalition orderings. This gives every agent a **local** reward derived
  from the **global** one — solving the credit-assignment problem.
- **Where the meat is (raw L279-289).** §3 = the Shapley Q-value definition; §4 = the algorithm
  (exact = sum over `2^N` subsets; practical = **Monte-Carlo over sampled permutations**). §5 =
  cooperative-game experiments (headline only).
- **Key math — Shapley Q-value (Eq. 3-5, raw L290-294, Math Flag L322-323).**

  > `Q^Shapley_i(s,a) = Σ_{S ⊆ N\{i}} [ |S|!(n−|S|−1)!/n! ] · ( Q(s, a_{S∪{i}}) − Q(s, a_S) )`

  i.e. Shapley's formula with **coalition VALUE replaced by the coalition's Q-value**. The key
  approximation (their §4): **sample random permutations** instead of summing all subsets, averaging
  the marginal `Q(s,a_{S∪{i}})−Q(s,a_S)`. *Equation numbers cited per the raw step (Eq. 3-5); verify
  against §3.*
- **Headline.** Shapley-Q credit assignment improves learning on global-reward cooperative games vs
  naive shared reward.
- **Why it's in the step (KEY INSIGHT, raw L295-299).** For SLS: replace the sparse winner-takes-all
  reward with per-agent Shapley credit, so each action carries the signal "who did this really
  help?" — the exact signal needed for coalition-aware learning. Our adaptation (below and in
  `shapley.py`): SLS is *competitive*, so "coalition value" is redefined as a **counterfactual
  increase in winning probability**, not a shared team Q.

---

## Supplementary references (skim only — raw L302-318, L569-580)

- **Li et al. (2021, KDD), "Shapley Counterfactual Credits for MARL"** — https://arxiv.org/abs/2106.00285.
  Combines Shapley with **counterfactual baselines** (echoing CFR's counterfactual regret, Steps 2-4).
  Skim §3 for the counterfactual-Shapley mechanism — a candidate refinement of our SLS credit.
- **Wang et al. (2025), "Shapley Machine: N-Agent Ad Hoc Teamwork"** — https://arxiv.org/abs/2506.11285.
  Ad hoc teamwork = implicit coalition formation with unknown teammates — exactly the "will my new
  ally cooperate or betray?" problem. Skim the method for the Shapley↔ad-hoc-team connection.
- **Meta AI, CICERO (Science 2022)** — https://www.science.org/doi/10.1126/science.ade9097 (not open).
  Full-press Diplomacy: LM negotiation + game-theoretic planning. Skim §2 (planning) for how
  coalition reasoning integrates into search. **We do NOT implement language negotiation.**
- **Mukobi et al. (2023), "Welfare Diplomacy"** — https://arxiv.org/abs/2310.08901. LLM cooperation
  benchmark; a Step 12 bridge. Abstract only.

---

## Worked Math Flags (my derivations — **TO VERIFY** on a real read/run)

### MF-1 — Shapley value by hand on the glove game (raw L322-323, L137)
Players `{0,1,2}`; `0` has the only LEFT glove, `1,2` each a RIGHT glove; `v(S)=min(#left,#right)`.
So `v` is 1 exactly for coalitions containing player 0 **and** at least one of `{1,2}`:
`v({0,1})=v({0,2})=v({0,1,2})=1`, all others `=0`.

Player 0 (`n=3`, so weights `|S|!(2−|S|)!/3!`): sum over `S ⊆ {1,2}`:
- `S=∅` (w=`0!·2!/3!=1/3`): `v({0})−v(∅)=0−0=0`.
- `S={1}` (w=`1!·1!/3!=1/6`): `v({0,1})−v({1})=1−0=1` → `1/6`.
- `S={2}` (w=`1/6`): `v({0,2})−v({2})=1` → `1/6`.
- `S={1,2}` (w=`2!·0!/3!=1/3`): `v({0,1,2})−v({1,2})=1−0=1` → `1/3`.
- **φ₀ = 1/6 + 1/6 + 1/3 = 2/3.** By symmetry `φ₁=φ₂=(1−2/3)/2 = 1/6`. → **(2/3, 1/6, 1/6)** ✓
  (matches raw L137; `shapley_playground.py` recomputes it — verify equality on a run).

**Core** of the glove game: efficiency `x₀+x₁+x₂=1`; constraints `x₀+xⱼ≥1` (j=1,2) and `xⱼ≥0`.
Adding the two pair constraints: `2x₀+x₁+x₂≥2 ⇒ x₀+(x₀+x₁+x₂)≥2 ⇒ x₀≥1`. With efficiency and
`x≥0` this forces `x=(1,0,0)`. → **core = {(1,0,0)}**, disjoint from the Shapley point. ✓ (raw L146.)

### MF-2 — the core can be EMPTY: the 3-player majority (simple) game (raw L325-326)
`v(S)=1` iff `|S|≥2`. Core needs `x₀+x₁+x₂=1` and `xᵢ+xⱼ≥1` for all pairs. Summing the three pair
constraints: `2(x₀+x₁+x₂)≥3 ⇒ 2·1≥3`, i.e. `2≥3` — **contradiction**. So the **core is empty**:
no allocation is immune to a pair deviating. This is the SLS-relevant lesson (raw L325-326): a
zero-sum / one-winner game has no stable coalition structure, so **coalitions are inherently
unstable and will be betrayed**. `shapley_playground.py`'s core LP should report infeasible — verify.

### MF-3 — piKL as a KL-regularized best response (raw L328-329)
Reading Bakhtin §2.2's objective `min_π KL(π‖π_human) + λ·E_π[loss]`: the stationary policy is the
softmax-tilt of the prior toward high value, `π(a) ∝ π_human(a) · exp(−λ · loss(a))` (the standard
KL-regularized-optimization solution; a Gibbs/Boltzmann update on the prior). **Interpretation for
Contribution #2:** the N-player "safe" strategy is the behavioral prior `π_human`, and exploitation
is a *bounded, temperature-`λ` tilt* away from it — the direct analog of Step 8's "bounded deviation
from Nash," with `π_human` replacing Nash. *This closed form is my inference from the regularizer,
not a quoted equation; verify the exact objective and whether the paper uses this Gibbs form or an
iterative search.*

---

## Verify when you read it (claims to confirm against the sources)

1. **De Carufel & Jerade Theorems 1-3** — the exact 2-player winning conditions, and the precise
   rule variant (§2): reconcile with `sls_game.py`'s `# NOTE (a)/(b)/(c)` simplifications before
   trusting `sls_endgame.py`.
2. **Sharan & Adak §4** — the "~50% of max reward" figure and its definition; whether *any*
   coalition-like behavior is reported.
3. **Bakhtin §2.2** — the exact piKL objective, the sign/role of `λ`, and whether it is solved in
   closed form or by iterative regularized search.
4. **Wang et al. §3 Eq. 3-5** — the Shapley-Q formula and the permutation-sampling approximation
   (§4); confirm the equation numbers.
5. **Chalkiadakis Ch. 2-4** — the Shapley/core/nucleolus formulas and the complexity of
   coalition-structure generation (Bell-number search space).

---

## Key takeaways for the final summary

- **The through-line (raw L162-329).** SLS-RL exists but is coalition-blind (Sharan & Adak); its
  2-player endgame is exactly solved (De Carufel & Jerade); the *general* N-player safe-play recipe
  is **piKL** = behavioral-prior regularization (Bakhtin); the training signal that makes coalitions
  learnable is **Shapley credit** (Wang et al.), grounded in classical cooperative GT (Chalkiadakis).
- **Two equations to own:** the **Shapley value** `φ_i = Σ_S [|S|!(n−|S|−1)!/n!](v(S∪i)−v(S))` and
  the **core** constraints `Σ_{i∈S}x_i ≥ v(S)`, `Σx_i=v(N)` — worked in MF-1/MF-2, with the SLS
  punchline that its core is (almost certainly) **empty**.
- **The safety shift (Contribution #2):** Nash → **behavioral prior** as the N-player safe baseline;
  exploitation = bounded (KL-`λ`) tilt away from it (MF-3). This is the single most important
  conceptual import of the step.
- **The credit shift (Contributions #1/#3):** Shapley-Q re-purposed for a *competitive* game, with
  coalition value = **counterfactual win-probability increase** — the dense signal for coalition-aware
  training and the seed of the EGTA/coalition evaluation methodology.
- **Everything above is cited-or-flagged**: the theorem statements and the "~50%" figure are the two
  items most in need of a PDF check before any result leans on them.
