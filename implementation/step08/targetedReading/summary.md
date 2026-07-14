# Step 08 — Targeted Reading: Safe Opponent Exploitation

> Phase 3 of Step 08. The cropped, VIP-only distillation of the step's sources — the meat
> without the bloat. Built from the raw step's per-paper READ/MATH/KEY-INSIGHT blocks
> ([`step_08_safe_exploitation.md`](../../../planning/rawSteps/step_08_safe_exploitation.md),
> L160–378) and your own survey
> [`oldSources/safeOpponentExploitation.md`](../../../oldSources/safeOpponentExploitation.md).

**Anti-hallucination guardrails (per `workflow.md` §4.3).** Equation/section/theorem numbers
below are cited **as the raw step names them**; where the raw step does not pin an exact
number, this doc says so and marks the reference approximate (`~`). Nothing is quoted at
length (copyright). Every worked derivation in "Math Flags" is **the agent's own and must be
checked against the PDF** — it is a *scaffold for your pen-and-paper pass*, not an authority.
Where a paper is not open-access, the notes are built from the abstract/author copy plus the
raw step's own summary, and that is flagged inline.

---

## The through-line in one paragraph

Safe exploitation is one idea refined six times: **exploitation = maximize value against your
opponent model, subject to a safety constraint.** Johanson (2007) introduces the tunable knob
(RNR) and the LP template. Ganzfried & Sandholm (2015) prove the safety *theorem* for a
perfect Nash baseline (via minimax). Liu (2022) makes it *real-time* by localizing safety to a
subgame with a gadget. Jeary & Turrini (2023) fix the fatal "perfect Nash" assumption for
ε-equilibrium baselines (prime-safe). Ge (2024) relaxes safety to "no more exploitable than the
blueprint" (adaptation safety) and bounds loss per info set, defeating teaching attacks. Milec
(2025) pushes exploitation *past the search depth limit* with matrix-valued states. Every step
weakens one assumption to gain tractability while preserving a safety guarantee — and **all six
require 2-player zero-sum**, which is the thesis gap.

---

## Paper 1 — Johanson, Zinkevich & Bowling, "Computing Robust Counter-Strategies" / "Data-Biased Robust Counter-Strategies" (NIPS 2007; AAMAS 2009)

- **Links:** https://poker.cs.ualberta.ca/publications/Johanson07.pdf (2007),
  https://poker.cs.ualberta.ca/publications/AAMAS09-johanson.pdf (2009).
- **Role:** the origin of principled safe exploitation — the **Restricted Nash Response (RNR)**
  and the constrained-optimization template every later paper reuses.

**Key idea (2–4 sentences).** Instead of best-responding to an opponent model (maximally
exploitative, maximally fragile), compute an equilibrium of a *modified* game in which the
opponent is **restricted**: with probability `p` they must play the fixed model `σ_fix`, and
with probability `1 − p` they play freely (adversarially). The best response to *that*
restricted opponent is the RNR. Sweeping `p` from 0 to 1 traces a curve from Nash (`p=0`) to
full best response (`p=1`), and RNR **bounds your exploitability as a function of `p`**.

**Key math.**
- **RNR LP (raw step cites "Eq. 3–4", L178, L377).** RNR is a linear program in sequence form:
  maximize expected value against `σ_fix`, subject to (a) the strategy being a valid
  realization plan (treeplex/sequence-form flow constraints) and (b) the opponent's freedom
  being weighted by `1 − p`. The `p` knob enters as the mixing weight between "exploit the
  model" and "stay safe against a free opponent." *(The raw step names Eq. 3–4 but this is a
  secondary summary of the LP; confirm the exact equation numbers and the precise objective in
  the PDF — see Math Flag C.)*
- The 2009 "data-biased" variant makes `p` **depend on how much data** you have about each
  info set (more data → exploit more there), rather than a single global `p`.

**Algorithm (pseudocode sketch, to verify).**
```
for p in [0, 0.1, ..., 1.0]:
    build restricted game: opponent plays σ_fix w.p. p, free w.p. 1-p
    σ_RNR(p) = equilibrium strategy for the hero in the restricted game   # an LP / CFR solve
    record: EV(σ_RNR(p) vs σ_fix)        # exploitation
            exploitability(σ_RNR(p))     # safety
```

**Headline result.** On Kuhn/Leduc-scale games and hold'em abstractions, RNR gives a
**smooth, tunable** frontier: small `p` buys real exploitation for little exploitability; the
optimal `p` depends on the opponent. *(The raw step points to "Section 4 — Experiments on Kuhn
and Leduc"; specific bb/hand numbers are not reproduced here to avoid inventing figures — read
them off Section 4.)*

**KEY INSIGHT (raw step L183–187).** RNR establishes the template: *exploitation = constrained
optimization where the constraint is a safety bound.* Ganzfried proves the guarantee, Liu
localizes it, Ge relaxes it — all variations on this LP.

---

## Paper 2 — Ganzfried & Sandholm, "Safe Opponent Exploitation" (ACM TEAC, 2015)

- **Links:** https://www.sganzfried.com/safe-exploitation.pdf ,
  https://dl.acm.org/doi/10.1145/2716315 .
- **Role:** the theoretical anchor — the **safety theorem** the thesis extends.

**Key idea.** If you hold a **perfect Nash equilibrium** `σ*`, you can deviate toward
exploiting an opponent model **without ever dropping below the Nash game value** against *any*
opponent. The allowed deviation is bounded by a "safety margin" — the gap between the opponent
model and equilibrium play. The paper also introduces *gift*-based reasoning: you may only
deviate to the extent the opponent has given you "gifts" (played dominated / mistaken actions).

**Key math.**
- **Theorem 1 — safety guarantee (raw step L208–213, Math Flag A).** For a Nash equilibrium
  `σ*` and opponent model `σ_opp`, the safe-exploitation strategy `σ_SE` satisfies
  `v(σ_SE, σ') ≥ v(σ*, σ')` for **all** opponent strategies `σ'`. The proof uses the **minimax
  theorem**. *(Read the statement + proof sketch; skip the full proof — raw step L207.)*
- **Algorithm (raw step L200–204, "Section 4").** Compute `σ_SE` as a constrained
  optimization: maximize `v(·, σ_opp)` subject to `min_{σ'} v(σ_SE, σ') ≥ v*`. The inner
  minimization (worst-case opponent) is itself a best-response computation.

**Headline result.** On poker domains, safe exploitation earns strictly more than Nash against
exploitable opponents while its worst-case value provably never falls below `v*`. *(Section 5;
numbers to be read from the PDF, not reproduced here.)*

**KEY INSIGHT (raw step L221–226).** Safe exploitation is *solved* — but only under strong
assumptions: **perfect Nash baseline, 2-player zero-sum, full-game computation.** Every later
paper relaxes one. The value guarantee `v(σ*, σ') = v*` for all `σ'` is **exactly** the
2p-zero-sum minimax fact — and exactly where N-player breaks (§ Math Flag A, and intuition §7).

---

## Paper 3 — Liu, Wang, Guo & Xing, "Safe Opponent-Exploitation Subgame Refinement" (NeurIPS 2022)

- **Link:** NeurIPS 2022 proceedings (search "Safe Opponent-Exploitation Subgame Refinement");
  check OpenReview / author pages for the PDF. *(Not confirmed open-access; notes below combine
  the raw step's summary L229–259 with the survey — flagged.)*
- **Role:** the theory→practice bridge — makes safe exploitation **real-time** via a subgame
  gadget. The algorithm is **SES (Safe Exploitation Search)**.

**Key idea.** Don't re-solve the whole game when the model updates. At a **subgame root**,
interpolate between the Nash blueprint and an exploitation strategy inside a **gadget** game
that *guarantees* the resolved subgame is no worse than the blueprint value. Safety becomes a
**local** property of one subgame instead of a **global** property of the whole tree.

**Key math.**
- **SES gadget construction (raw step L246–249, "Section 3.2", Math Flag — related to C).** The
  gadget augments the subgame root with a virtual "fall back to Nash / opt out" action carrying
  the known blueprint value. Solving the augmented subgame with standard CFR/LP then yields the
  most exploitative strategy that still beats the fallback — i.e. bounded exploitability by
  construction. The "ghost" opt-out action is what enforces safety locally.

**Headline result.** SES outperforms Nash against weak opponents while bounding exploitability,
at real-time (subgame-sized) cost rather than full-game cost. *(Section 5; numbers from PDF.)*

**KEY INSIGHT (raw step L255–259).** SES converts safe exploitation from a global constraint
(Ganzfried: safe across the entire tree) into a **local** one (safe within *this* subgame),
which is what makes it feasible in games like NLHE. **Caveat:** it still needs the opponent
model to be accurate *within* the subgame, so "deep deception" can strain the bounds.

---

## Paper 4 — Jeary & Turrini, "Safe Opponent Exploitation For Epsilon Equilibrium Strategies" (arXiv 2023)

- **Link:** https://arxiv.org/abs/2307.12338 (open access).
- **Role:** fixes Ganzfried's fatal assumption — real baselines are ε-equilibria, not perfect
  Nash. Introduces **prime-safe** exploitation.

**Key idea.** When your baseline is an **ε-equilibrium** (which every real bot's is, because of
abstraction — Step 04), Ganzfried's "never lose vs Nash value" guarantee is **void**: the
baseline itself is exploitable, so anchoring to the exact Nash value `v*` is unjustified.
Prime-safe redefines the safety floor as the **worst-case value of your specific ε-baseline**,
roughly `v* − ε`, and re-solves the exploitation LP against that adjusted floor.

**Key math.**
- **Definition 1 — ε-safe exploitation (raw step L279–283, Math Flag — compare with A).**
  Safety becomes "never earn less than the worst-case value of the ε-equilibrium baseline"
  rather than "never earn less than the Nash value." `ε` is measured as the baseline's own
  exploitability. *(Read Def 1 carefully; the "prime" refers to the adjusted value.)*

**Headline result.** With the adjusted floor, imperfect (abstracted) bots can safely exploit
without stepping outside their own (already-imperfect) safety net. *(Section 5; numbers from
PDF.)* The survey notes real-time prime-safe computation is still expensive.

**KEY INSIGHT (raw step L289–293).** The theory↔practice gap in safe exploitation *is* baseline
quality: papers assume perfect Nash, real systems have ε-error from abstraction. Prime-safe
closes it — and is the guarantee the **thesis should build on**, because the thesis baseline
will always be approximate.

---

## Paper 5 — Ge, Zhu, et al., "Safe and Robust Subgame Exploitation in Imperfect Information Games" (ICML 2024)

- **Link:** ICML 2024 proceedings, https://proceedings.mlr.press/ (ICML 2024 volume); check
  authors' Scholar pages for a preprint. *(Open-access status unconfirmed; notes combine the raw
  step L295–333 with the survey — flagged.)*
- **Role:** current bleeding edge — **adaptation safety** and the **OX-Search** algorithm.

**Key idea.** Demanding strict safety (never lose vs perfect play) is overly rigorous because
blueprints are *already* exploitable due to compute limits. Redefine: an exploiting strategy is
**adaptation-safe** if it is **no more exploitable than the blueprint** was to begin with.
OX-Search (Opponent eXploitation Search) bounds worst-case profit loss at **every information
set** in real time, neutralizing the **teaching attack** (an adversary deliberately playing
badly to bait a bigger deviation, then punishing it).

**Key math.**
- **Definition 2 — Adaptation Safety (raw step L315–319, Math Flag B).** `σ_exploit` is
  adaptation-safe iff `exploitability(σ_exploit) ≤ exploitability(σ_blueprint)`. Strictly weaker
  than Ganzfried's "safe vs perfect play," because the blueprint is already ε-exploitable —
  so it is *achievable* where strict safety is not.
- **Theorem 1 — OX-Search guarantees (raw step L320–322).** OX-Search gives *per-information-set*
  bounds on exploitation safety — finer-grained than SES's single global bound. *(Read the
  statement; skip appendix proofs.)*

**Headline result.** OX-Search matches or beats SES and standard subgame solving on poker while
holding adaptation safety per info set and resisting teaching attacks. *(Section 5; numbers from
PDF.)*

**KEY INSIGHT (raw step L329–333).** Adaptation safety is the safety notion that makes
exploitation **practical** — "if my blueprint already loses 0.5 bb/hand to abstraction, it's
safe to exploit as long as I lose at most 0.5 bb/hand." **But it works only in 2-player
zero-sum**; the authors explicitly flag that the guarantees break for 3+ players — the thesis
Contribution #2 open problem.

---

## Paper 6 — Milec, Kovařík & Lisý, "Adapting Beyond the Depth Limit" (arXiv 2025)

- **Link:** https://arxiv.org/abs/2501.10464 (open access).
- **Role:** exploitation *past the search horizon* — the **ABD** algorithm; matters because real
  games are too deep for full-depth search.

**Key idea.** Prior methods assume they can evaluate the entire subgame they solve; in practice
search must be **depth-limited**, and the standard trick (assume rational play beyond the limit)
throws away opponent-model information exactly where mistakes happen. ABD keeps a **portfolio**
of strategies and represents the depth-limit value not as a scalar but as a **matrix** capturing
how utility depends on the opponent's strategy beyond the limit — so the model can be exploited
past the horizon.

**Key math.**
- **Matrix-valued states (raw step L350–354, "Section 3.2").** At the depth limit, instead of a
  single scalar value, ABD stores a matrix over (our portfolio strategy) × (opponent
  continuation), letting the solve pick the portfolio mix that best exploits the modeled
  opponent beyond the horizon. *(Understand the concept; skip proofs.)*

**Headline result.** On poker and battleship, ABD achieves **>2× utility increase** when
opponents err beyond the depth limit, versus depth-limited methods that assume rational
continuation. *(Raw step L346–347; confirm the exact factor and domains in Section 4.)*

**KEY INSIGHT (raw step L355–359).** ABD is the first method to fully use opponent-model
information beyond the depth limit — critical for scaling safe exploitation to games with too
many levels for full search.

---

## Book (supplementary) — Shoham & Leyton-Brown, *Multiagent Systems* (2008)

- **Link:** http://www.masfoundations.org/download.html . **Sections:** 3.4 (Computing Nash
  Equilibria), 4.6 (Computing Best Responses).
- **Role (raw step L364–367):** revisit equilibrium/BR computation *with exploitation in mind* —
  **best response IS the exploitation algorithm**, and **Nash IS the safety baseline**. Section 4
  is the **sequence-form** machinery underneath every RNR/Ganzfried LP in this step (raw step
  L638 [P6]): the LPs are sequence-form programs, not black-box solvers.

---

## Cross-source synthesis (how the line of work progresses)

```
        assumption relaxed          safety floor                  scope
RNR 2007      (introduces knob)     exploitability bound f(p)     global (whole game)
Ganzfried'15  perfect Nash needed   >= Nash value v*              global
Liu '22 (SES) full-game -> subgame  >= blueprint value in subgame LOCAL (gadget)
Jeary '23     perfect -> eps-Nash   >= v* - eps  (prime-safe)     global (eps-adjusted)
Ge '24 (OX)   strict -> adaptation  <= blueprint exploitability   LOCAL, per-info-set
Milec '25     full-depth -> limited (uses model past horizon)     depth-limited portfolio
```

- **Agreements.** All six treat exploitation as constrained optimization; all preserve a safety
  guarantee; all rely on 2p-zero-sum minimax for that guarantee.
- **Tensions.** Global vs local safety (Ganzfried/Jeary vs Liu/Ge); strict vs relaxed floor
  (Ganzfried vs Ge); model-accuracy assumptions (SES needs an accurate subgame model; OX-Search
  hardens against teaching attacks but still needs a *reasonable* blueprint).
- **The common crack.** The value guarantee `v(σ*, σ') ≥ v*` for all `σ'` is a 2p-zero-sum fact
  (minimax). No paper here escapes it — the N-player extension is genuinely open.

---

## Math Flags (worked by the agent — TO BE CHECKED against the PDFs)

> These are **my derivations/scaffolds**, provided so your pen-and-paper pass has something to
> react to. Treat every line as "claimed, verify," per `workflow.md` §0/§4.3.

### Flag A — Ganzfried & Sandholm 2015, Theorem 1 (safety guarantee) — proof sketch + failure point

**Claim to reproduce.** For Nash `σ*` in a 2-player zero-sum game with value `v*` (to the hero),
and a safe-exploitation strategy `σ_SE` constructed by deviating toward `BR(σ_opp)` only within
the "gift" budget, `v(σ_SE, σ') ≥ v*` for **all** `σ'`.

**Sketch (verify).**
1. In a 2p zero-sum game, minimax gives: a Nash strategy `σ*` guarantees the game value against
   *any* opponent — `min_{σ'} v(σ*, σ') = v*`. *(This is the load-bearing step.)*
2. Construct `σ_SE` so that at every info set it only shifts probability toward the exploitative
   action **when doing so cannot lower the worst-case value below `v*`** (a "gift" — the
   opponent has ceded value there). This is a per-decision safety check.
3. Because each shift preserves the `≥ v*` worst-case (step 1 gives the anchor, step 2 keeps
   deviations within the slack), the whole strategy retains `min_{σ'} v(σ_SE, σ') ≥ v*`. ∎

**Where it breaks (the two extension points, raw step L214–220):**
- **Imperfect Nash.** If `σ*` is only an ε-equilibrium, step 1 weakens to
  `min_{σ'} v(σ*, σ') ≥ v* − ε`, so the floor is `v* − ε`, not `v*` → **Jeary 2023 (prime-safe)**.
- **N > 2 players.** Step 1 **fails entirely**: a Nash strategy does *not* guarantee a fixed
  value against arbitrary opponents (payoffs don't sum to zero across the others; they can
  coordinate). There is no `v*` anchor → **thesis Contribution #2**. *This is the single most
  important thing to internalize in this step.*

### Flag B — Ge 2024, Definition 2 (adaptation safety) vs Ganzfried safety

**Claim.** `σ_exploit` is adaptation-safe iff `exploitability(σ_exploit) ≤ exploitability(σ_blueprint)`.

**Comparison to verify.**
- Ganzfried: `worst_case_value(σ_SE) ≥ v*` (absolute floor, needs perfect Nash).
- Ge: `worst_case_value(σ_exploit) ≥ worst_case_value(σ_blueprint)` — equivalently
  `exploitability(σ_exploit) ≤ exploitability(σ_blueprint)` (relative floor, any blueprint).
- The **difference is exactly ε = exploitability(blueprint)**: Ge's floor is Ganzfried's floor
  minus ε. When the blueprint is a perfect Nash (ε = 0) the two coincide.
- **Pitfall to note (raw step L610):** if the blueprint is *terrible* (huge ε), adaptation
  safety is trivially satisfied by almost anything — so a *minimum baseline quality* is an open
  requirement.

### Flag C — Johanson 2007, RNR as a sequence-form LP (Eq. 3–4)

**Claim.** RNR is a sequence-form linear program: `max_x  c(σ_fix)·x` s.t. `x` is a valid
realization plan (treeplex flow: `x_∅ = 1`, `Σ_a x_{Ia} = x_{seq(I)}`, `x ≥ 0`) and the
opponent's `(1 − p)` free component is handled by the equilibrium/minimax constraints of the
restricted game.

**To verify.** (a) That `EV(hero vs σ_fix)` is **linear** in the hero realization plan `x` (it
is: EV = Σ over terminals of chance × opp-reach × payoff × `x_{hero seq}` = `c·x`); (b) that the
restricted-opponent equilibrium reduces to adding the opponent's free-play best-response
constraints weighted by `1 − p`; (c) the exact form of Eq. 3–4 in the PDF (the objective and the
`p`-weighting) — the numbering and precise constraint form should be confirmed, as this doc
reconstructs the *structure*, not the paper's exact notation. The Step 08 implementation builds
this LP on Step 07's `SequenceForm` treeplex + SciPy `linprog`.

---

## "Verify when you read it" checklist

- [ ] **Ganzfried Thm 1:** confirm the minimax step is stated exactly as "Nash guarantees `v*`
      vs any opponent," and that the proof does not smuggle in another 2p-zero-sum assumption
      elsewhere.
- [ ] **Ganzfried "gifts":** confirm the deviation budget is defined via dominated/gifted actions
      (does my per-decision "slack" sketch in Flag A match their construction?).
- [ ] **Jeary Def 1:** confirm the prime-safe floor is the ε-equilibrium's *worst-case* value and
      that `ε` is measured as baseline exploitability (not some other quantity).
- [ ] **Ge Def 2:** confirm adaptation safety is the *exploitability inequality* (Flag B) and check
      whether they impose any minimum-blueprint-quality condition.
- [ ] **Ge Thm 1:** confirm OX-Search's bound is genuinely *per-information-set* (vs SES's global).
- [ ] **Liu SES gadget:** confirm the gadget's opt-out action carries the *blueprint* value (not
      the exact Nash value) and how it enforces the local bound.
- [ ] **Milec ABD:** confirm the ">2× utility" figure and the exact domains (poker + battleship?).
- [ ] **Johanson Eq. 3–4:** confirm the exact objective and `p`-weighting; confirm the 2009
      data-biased variant makes `p` info-set-dependent.
- [ ] **Which papers are open-access:** Liu 2022 and Ge 2024 links were not confirmed open —
      locate the PDFs and check the notes above against the real text.

---

## Key takeaways for the final summary

- **One template, six refinements:** exploitation = max EV vs model s.t. a safety constraint;
  the papers differ only in the constraint (bound f(p) → ≥ v* → ≥ blueprint-value-in-subgame →
  ≥ v*−ε → ≤ blueprint-exploitability) and its scope (global → local/gadget → per-info-set).
- **Ganzfried Thm 1 is the thesis foundation, and its minimax step is the attack point.**
  Imperfect Nash weakens the floor to `v*−ε` (Jeary); **N > 2 players destroys the floor
  entirely** (Contribution #2). Be able to reproduce the sketch and name where each breaks.
- **Adaptation safety (Ge Def 2) is the practical safety notion** and differs from Ganzfried by
  exactly ε = blueprint exploitability — but is vacuous if the blueprint is bad (open: minimum
  baseline quality).
- **RNR is a sequence-form LP** (Flag C) — the computational backbone the implementation phase
  builds directly on Step 07's treeplex; understanding it as an LP (not a black box) is what
  lets us swap Ganzfried's / Jeary's / Ge's constraints into the *same* solver.
- **Local beats global for real-time:** SES/OX-Search localize safety to a subgame via a gadget,
  the theory→practice bridge; ABD extends exploitation past the depth limit with matrix-valued
  states.
- **Everything here is 2-player zero-sum.** The survey's own "Areas to Explore" and Ge's
  discussion both flag multi-agent safe exploitation as the lucrative open problem — the bridge
  into Step 09 (MARL) and the thesis.
