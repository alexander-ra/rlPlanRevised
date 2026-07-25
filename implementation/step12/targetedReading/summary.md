# Step 12 — Targeted Reading (Phase 3)

VIP-only notes on the papers behind Step 12. The rule (per [`../../WORKFLOW.md`](../../WORKFLOW.md)):
read for the **specific thing the implementation needs**, cite the section, and mark any math I
re-derived as **"agent derivation, TO VERIFY"** rather than asserting it. Two such derivations
are worked below (Paster Theorem 2.1; ARDT minimax expectile regression) and both are on the
verify-list at the end.

Arxiv ids are given so the exact source can be pulled in the run session.

---

## Core papers

### 1. Decision Transformer — Chen et al., 2021 (arXiv:2106.01345)
**Need it for:** the whole `decision_transformer.py` design and the return-conditioning idea.
- **Reframing (§3):** RL as conditional sequence modeling. The trajectory is tokenized as
  `(R̂₁, s₁, a₁, R̂₂, s₂, a₂, …)` where `R̂ₜ = Σ_{t'≥t} r_{t'}` is the **return-to-go**. A causal
  GPT predicts `aₜ` from the tokens up to and including `sₜ`. **No value function, no dynamic
  programming** — pure supervised learning on offline data.
- **Conditioning at test time (§3, §5):** you *specify* a target return, feed it as `R̂₁`, act,
  then decrement the target by the realized reward. On deterministic benchmarks, higher target →
  higher achieved return, often up to and slightly beyond the best trajectory in the data.
- **What I mirror in code:** the `(R,s,a)` token order, per-timestep positional embedding, and
  reading the action prediction from the **state** token. I use an `nn.Embedding` for discrete
  input actions and a categorical head (poker actions are discrete), which is the standard
  discrete-DT variant rather than the paper's continuous-control setup.
- **Caveat the paper is honest about (§5.x):** DT's return conditioning is reliable in
  (near-)deterministic environments; **stochasticity breaks the guarantee** — which is exactly
  Paster's paper next.

### 2. "You Can't Count on Luck" / ESPER — Paster, McIlraith, Ba, 2022 (arXiv:2205.15967)
**Need it for:** the luck-vs-skill caveat that motivates ARDT and Step 13's data pipeline.
- **The failure (§2):** in a **stochastic** environment, conditioning on a high return-to-go
  selects trajectories that were **lucky**, not skilled. The policy that reproduces them can have
  arbitrarily bad *expected* return, because the high return was an outcome of environment
  randomness the agent does not control.
- **Their fix (ESPER, §3):** cluster trajectories and condition on **expected** return of a
  learned latent ("average return you can actually cause"), not the realized return — decoupling
  the agent's influence from luck via an adversarial clustering objective.
- **What I take:** the *diagnosis*, realized as the `luck_vs_skill_coinflip.py` probe and the
  "bet-frequency by card" DT test. I do **not** implement ESPER; ARDT is our chosen robustness
  route (adversary-focused rather than general-stochasticity-focused).

> **MATH FLAG A (agent derivation, TO VERIFY vs Paster §2 / their Theorem 2.1).**
> *Claim to check:* return-conditioned cloning can be arbitrarily suboptimal under stochasticity.
> *My minimal derivation on the coin-flip bandit in the exploration probe:* two actions, A gives
> `r=0.5` deterministically, B gives `r=1` w.p. `p=0.4` else `0` (so `E[B]=0.4<0.5=E[A]`). Under
> a uniform data policy, condition on `R̂ = 1`. Only B can produce `r=1`, so
> `P(a=B | R̂=1) = 1`. The return-conditioned policy therefore plays B with certainty and earns
> `E = 0.4`, while the optimal policy plays A and earns `0.5`. The suboptimality gap is
> `0.5 − 0.4 = 0.1`, and by scaling B's payoff and lowering `p` the gap can be made to approach
> the full return range — "arbitrarily bad." *To verify:* that this matches the constant/scaling
> in Paster's formal Theorem 2.1 (their bound is stated over general MDPs; check the exact
> quantity — regret vs competitive ratio — and the assumptions on coverage).

### 3. Adversarially Robust Decision Transformer (ARDT) — Tang et al., NeurIPS 2024 (arXiv:2407.18414)
**Need it for:** the entire `ardt.py`.
- **The setting (§3):** two-player zero-sum / adversarial. A vanilla DT conditioned on high
  return learns to exploit the *specific* opponents in the data; against a strong (Nash)
  opponent it is punished. ARDT wants the return the protagonist can **guarantee against the
  worst-case adversary** — a minimax return.
- **Minimax expectile regression (§4):** they relabel each state's conditioning target with an
  estimate of the **worst-case return-to-go**, computed via **expectile regression** — an
  asymmetric-squared-loss quantile-like estimator — taking the *protagonist-max, adversary-min*
  over the branching. Training a return-conditioned DT on these relabeled targets yields a robust
  policy; **with full data coverage it provably approaches the minimax (Nash) value.**
- **What I implement (documented simplification):** a single-sided **pessimistic** expectile of
  the realized return-to-go per state (a worst-case-over-outcomes proxy), then DT training on the
  relabeled returns (`MinimaxReturnEstimator` + `relabel_returns` + `AdversariallyRobustDT`). The
  two-sided protagonist-max/adversary-min recursion is the full method; my proxy is the tractable
  offline version for our mixed-opponent Kuhn data. Flagged below.

> **MATH FLAG B (agent derivation, TO VERIFY vs ARDT §4).**
> *Expectile definition and tau direction.* The τ-expectile `m_τ(Y)` minimizes
> `E[ ρ_τ(Y − m) ]` with `ρ_τ(u) = |τ − 𝟙{u<0}| · u²`. The first-order condition is
> `τ·E[(Y−m)_+] = (1−τ)·E[(Y−m)_-]`, i.e. positive residuals (underestimates, `Y>m`) get weight
> `τ` and negative residuals weight `1−τ`. *Consequence I rely on:* `τ→0` pushes `m` toward the
> **min** (pessimistic), `τ=0.5` gives the mean, `τ→1` toward the **max** (optimistic). Therefore
> for a **worst-case-over-opponent** target I use a **low** `τ` (default `0.1`). *This contradicts
> the raw step's sketch* (raw L347-360), which writes `τ=0.9` and calls it "pessimistic" — under
> the standard definition `0.9` is the *optimistic* side. *To verify:* the exact objective and the
> τ-convention used in ARDT §4 (some works flip the sign of `u`, which swaps the τ meaning), and
> whether ARDT applies the low-τ expectile over the *adversary's* branch specifically rather than
> over the pooled outcome distribution as my proxy does. This is the single most important thing
> to reconcile before trusting the ARDT numbers.

### 4. TextArena — Guertler et al., 2025 (arXiv:2504.11442)
**Need it for:** the optional `textarena_agent.py` and framing LLM-agent evaluation.
- **What it is (§1-3):** 57+ competitive **text** games (negotiation, deduction, board/word
  games) with a unified env API and **online TrueSkill** leaderboards for model-vs-model and
  model-vs-human play. Emphasis on *soft* skills (theory of mind, bluffing, negotiation) that
  static benchmarks miss.
- **What I take:** the *interface shape* (`make(env_id)` → `reset` → `get_observation` /
  `step(action=text)` → `close`→rewards), wrapped thinly so the same `LLMClient` plays it. Kept
  optional/guarded because the package is not a repo dependency and the API version must be
  checked at run time.

### 5. Trajectory Transformer — Janner, Li, Levine, 2021 (arXiv:2106.02039)
**Need it for:** context on the DT design space (why DT, not TT, here).
- **What it is (§3-4):** tokenize **everything** (discretized states, actions, rewards) and treat
  model-based RL as **sequence modeling + beam search** over future tokens. Planning, not just
  return-conditioned generation.
- **Why not here:** TT's discretization + beam search is heavier and aimed at planning in
  continuous control; DT's return-conditioning is the right minimal tool for the Kuhn
  offline-strategy question. Noted so the "why DT" choice is deliberate, not defaulted.

---

## Supplementary (skim; cited where they touch the build)

- **Conservative Q-Learning (CQL) — Kumar et al., 2020 (arXiv:2006.04779).** The value-based
  offline-RL baseline DT is contrasted with; pessimism on OOD actions. We do **not** implement it
  (BC is our simpler control), but it is the "other road" for the intuition menu.
- **Divide-Fuse-Conquer (2025).** LLMs for many games via decompose-then-compose prompting;
  relevant to the prompt-style axis (plain/CoT/game-theory) in `llm_agent.py`.
- **Suspicion-Agent — 2023 (arXiv:2309.17277).** GPT-4 + explicit **theory-of-mind** for
  imperfect-information games (incl. Leduc); a template for the game-theory prompt and for the
  opponent-adaptation metric.
- **SpinGPT (2025).** LLM + **CFR** hybrid for heads-up poker: use the solver for strategy, the
  LLM for language/robustness. The concrete "LLM + formal tool" combination our comparison
  gestures at.

---

## Cross-source synthesis

- **Two roads to Nash from data.** CFR/Deep-CFR (Step 05) reach equilibrium by **online
  self-play iteration**; ARDT reaches it by **offline supervised learning with minimax return
  conditioning**. Same destination, opposite data regime — and ARDT is the one that transfers to
  the fixed Playtech logs in Step 13.
- **Luck is the through-line.** DT (2021) assumes benign stochasticity; Paster (2022) shows it
  isn't; ARDT (2024) fixes the *adversarial* slice of it via expectile relabeling; ESPER fixes the
  *general* slice via latent clustering. Our build picks the ARDT slice and keeps the Paster probe
  as the diagnostic.
- **LLMs are orthogonal.** TextArena/Suspicion-Agent/SpinGPT measure *language-native* strategic
  skill; the honest result is usually **where** LLMs deviate from Nash (bluff frequency, illegal
  moves), not a headline win — which is exactly what `evaluation.py` measures on Kuhn.

---

## Verify-when-you-read list (do these against the PDFs in the run session)

1. **MATH FLAG A:** reconcile the coin-flip suboptimality gap with Paster's Theorem 2.1 — exact
   bounded quantity (regret vs competitive ratio) and its coverage assumptions.
2. **MATH FLAG B (highest priority):** confirm the expectile objective and **τ direction** in
   ARDT §4; decide whether the pessimistic side is low-τ (my default `0.1`) or the raw step's
   `0.9`, and whether the min-expectile is taken over the **adversary branch** specifically.
3. **DT extrapolation:** does Chen et al. actually report gains from conditioning on returns
   **above** the data max, or only up to it? (Sets the expectation for the impossible-+3 probe.)
4. **ARDT coverage → Nash:** the precise theorem statement linking full data coverage to
   recovering the minimax/Nash value (assumptions we likely violate at SMOKE sizes).
5. **TextArena API:** the exact current signatures of `make`/`reset`/`get_observation`/`step`/
   `close` for the installed version (the wrapper targets the documented shape).
6. **Exploitability units:** confirm the mbb/h ↔ chips convention (1-chip ante = big blind) used
   in `evaluation.py` matches how the raw step's "50 mbb/h" was intended.
