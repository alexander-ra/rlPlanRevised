# Changes Proposal — Final Decisions

> Debate round 2 concluded. Proposals evaluated by user. This document records **final verdicts** and restructures all accepted changes **by step**, including the schedule compression ("Know-How First" pass for Steps 3–5).

---

## Decision Summary

| # | Proposal | Verdict | Rationale |
|---|----------|---------|-----------|
| 1 | Early Playtech data sanity check | **DECLINED** | Data not yet available. Request comes after showing PhD progress. >90% chance of delivery — no plan adjustment needed if data doesn't arrive. |
| 2 | Step 11 fallback benchmark | **ACCEPTED** | Pure documentation, zero cost. |
| 3 | Narrow Contribution #2 scope | **ACCEPTED** | All positions + user converge. Framing only. |
| 4 | Contribution #3 prove evaluation failures | **ACCEPTED*** | Promising but cautious — don't over-commit given tight schedule. |
| 5 | Level-k / cognitive hierarchy → Step 7 | **ACCEPTED** | Both independent positions flagged it. Essential for real-human modeling. |
| 6 | Sequence-form / LP → Steps 2, 8 | **ACCEPTED** | Reading emphasis change, zero schedule cost. |
| 7 | OPE → Steps 13–14 | **DECLINED** | Scope creep risk outweighs benefit for career-first PhD. |
| 8 | Change-point detection → Steps 7, 13 | **ACCEPTED** | One algorithm, two applications. Concrete and career-demonstrable. |
| 9 | Markov-games bridge → Step 9 | **ACCEPTED** | Half a day for conceptual coherence across EFG→MARL transition. |
| 10 | GAIL/IRL fallback → Step 13 | **ACCEPTED** | Documentation of existing fallback. Zero cost. |
| 11 | Meta-learning baseline | **ASTERISK*** | Optional comparison if time allows. One off-the-shelf method, no tuning. |

---

## Schedule Compression — "Know-How First" Pass

Steps 3–5 are foundational tools. Implementation phases halved to proof-of-concept prototypes. Reading and intuition phases fully protected — the know-how chain that Steps 6–8 depend on stays intact.

| Step | Old Duration | New Duration | Days Saved | What changes |
|------|:-----------:|:-----------:|:----------:|-------------|
| Step 3 | 14d | **10d** | 4d | Build one MC-CFR variant (not all). Defer polished multi-variant comparison to implementation phase. |
| Step 4 | 14d | **10d** | 4d | Understand abstraction concepts + one working toy example. Defer full pipeline. |
| Step 5 | 14d | **11d** | 3d | Get Deep CFR running. Understand DREAM conceptually. Defer head-to-head benchmark. |
| **Total** | | | **11d** | Recovered for buffer. |

### Compressed phase allocations

| Phase | Step 3 (10d) | Step 4 (10d) | Step 5 (11d) |
|-------|:-----------:|:-----------:|:-----------:|
| 1. Intuition | 1d | 1d | 1d |
| 2. Exploration | 1d | 1d | 2d |
| 3. Reading | 3d | 3d | 3d |
| 4. Implementation | **3d** | **3d** | **3d** |
| 5. Consolidation | 2d | 2d | 2d |

### New calendar

| Dates | Step | Days | Change |
|-------|------|:----:|--------|
| Apr 1–10 | Step 3: CFR Variants + MC Methods | 10 | −4d |
| Apr 11–20 | Step 4: Abstraction + Scaling | 10 | −4d |
| Apr 21–May 1 | Step 5: Neural Equilibrium (Deep CFR, DREAM) | 11 | −3d |
| May 2–22 | Step 6: End-to-End Game AI (Pluribus→ReBeL→SoG) | 21 | — |
| May 23–Jun 12 | Step 7: Opponent Modeling | 21 | — |
| Jun 13–Jul 3 | Step 8: Safe Exploitation | 21 | — |
| Jul 4–17 | Step 9: MARL | 14 | — |
| Jul 18–31 | Step 10: PBT + Evolutionary GT | 14 | — |
| Aug 1–14 | Step 11: Coalition Formation | 14 | — |
| Aug 15–24 | Step 12: Sequence Models + LLMs | 10 | — |
| Aug 25–Sep 7 | Step 13: Behavioral Analysis Pipelines | 14 | — |
| Sep 8–21 | Step 14: Evaluation Frameworks | 14 | — |
| Sep 22–Oct 1 | Step 15: Research Frontier Mapping | 10 | — |
| **Oct 2–31** | **Buffer** | **30** | **4.3 weeks ✓** |
| November | Chapter 1 + first publication draft | — | — |

---

## Changes By Step

### Step 2 — Game Theory + CFR Basics *(completed, retroactive note)*

**[P6] Sequence-form reading emphasis**
- Add a retroactive note: when reviewing Step 2 material during Step 8, revisit Shoham & Leyton-Brown Chapter 4 on sequence-form representation. The sequence-form is the mathematical backbone of all LP-based equilibrium computation used in Step 8. This is a reading pointer, not a rework.

---

### Step 3 — CFR Variants + MC Methods

**[COMPRESSION] 14d → 10d**
- Phase 4 (Implementation): Cut from 6d to 3d.
- Build **one** MC-CFR variant (External Sampling MC-CFR) to working correctness on Kuhn Poker.
- Defer: polished multi-variant comparison (Outcome Sampling, Robust Sampling). These become first-week tasks in the implementation phase post-November.
- All reading and intuition phases unchanged — the conceptual understanding of all CFR variants is preserved.

---

### Step 4 — Game Abstraction + Scaling

**[COMPRESSION] 14d → 10d**
- Phase 4 (Implementation): Cut from 6d to 3d.
- Build **one** working abstraction example: card bucketing on Extended Leduc.
- Defer: full abstraction pipeline (action abstraction, information abstraction comparison). Revisit with full context during implementation phase.
- All reading and intuition phases unchanged.

---

### Step 5 — Neural Equilibrium Approximation

**[COMPRESSION] 14d → 11d**
- Phase 4 (Implementation): Cut from 6d to 3d.
- Get **Deep CFR running** on Leduc Poker with correct exploitability convergence.
- Understand DREAM conceptually (reading + exploration), but defer full DREAM implementation and head-to-head Deep CFR vs. DREAM benchmark.
- All reading and intuition phases unchanged.

---

### Step 7 — Opponent Modeling (Tier 1, 21d — unchanged)

**[P5] Merge Level-k / Cognitive Hierarchy**
- Phase 3 (Reading): Add **one** paper on Level-k/cognitive hierarchy models (e.g., Camerer, Ho & Chong 2004 or Wright & Leyton-Brown 2014). Surgical read — algorithm description + experimental results only.
- Phase 4 (Implementation): Add a **Level-k opponent type** to the opponent type library alongside existing Bayesian/type-based opponents. This models human suboptimality — critical for Playtech data validation in Step 13.
- Cost: ~1.5d absorbed within 21d Tier 1 allocation.

**[P8] Merge Change-Point Detection**
- Phase 4 (Implementation): Add **Bayesian online changepoint detection** (Adams & MacKay 2007) to the non-stationarity experiment. Instead of ad-hoc "observe what happens when opponent switches type," detect the switch point statistically, then trigger re-modeling.
- Cost: ~0.5d absorbed within 21d allocation.

**[P11*] Meta-Learning Baseline (ASTERISK — optional)**
- If time permits within Step 7 or Step 10: run one off-the-shelf meta-learning method (e.g., MAML or contextual bandit) as a comparison baseline against the Bayesian opponent model. Preempts reviewer question "why not just meta-learn?"
- No tuning. If it works, document the comparison. If not, document that too.
- Only attempt if Step 7 completes ahead of schedule.

---

### Step 8 — Safe Exploitation (Tier 1, 21d — unchanged)

**[P3] Narrow Contribution #2 Scope**
- Reframe the "PhD Contribution Alignment" section: Contribution #2 is **tractable heuristics + empirical validation on small N-player games**, not a general N-player safety theorem.
- Specific targets: piKL-regularized exploitation, equal share baseline (payoff ≥ C/n), adaptation safety extended to 3-player Kuhn/Leduc.
- Explicitly state what it *doesn't* claim: general N-player minimax analog.

**[P6] Sequence-Form LP Understanding**
- Phase 3 (Reading): Ensure LP formulations (RNR, Ganzfried constrained response) are understood as **sequence-form programs**, not black-box solvers. Connect to the sequence-form representation from Shoham & Leyton-Brown Ch. 4 (referenced in Step 2 note above).

---

### Step 9 — MARL (14d — unchanged)

**[P9] Markov-Games Bridge**
- Phase 1 (Orientation): Add a short formal bridge on **Markov games (stochastic games)** before jumping into CTDE/PSRO/LOLA. ~Half-page of notation connecting EFG-style reasoning (game trees, information sets, counterfactual values) to MARL-style reasoning (joint policies, centralized critics, decentralized execution).
- Explains what is preserved (sequential decisions, partial observability) and what is lost (exact game tree structure, regret-based convergence guarantees).
- Cost: ~0.5d absorbed within 14d allocation.

---

### Step 11 — Coalition Formation (14d — unchanged)

**[P2] Fallback Benchmarks**
- Add a "Fallback Benchmarks" section documenting alternatives if So Long Sucker proves too complex or brittle:
  - (a) 3-player Leduc with side agreements
  - (b) Goofspiel (already referenced in Step 9)
  - (c) Simplified custom 4-player game
- Zero schedule cost — documentation only.

**[P3] Narrow Contribution #2 Scope (echo)**
- Adjust "PhD Alignment" section: same framing as Step 8 — tractable heuristics on small N-player games, not general theorem.

---

### Step 13 — Behavioral Analysis Pipelines (14d — unchanged)

**[P8] Change-Point Detection for Collusion**
- Add **Bayesian online changepoint detection** as a signal in the collusion detection composite score. Same algorithm from Step 7, applied to detect collusion onset / bot behavior changes in player timelines.
- Cost: ~0.5d absorbed within 14d allocation.

**[P10] GAIL/IRL Fallback Reference**
- Add explicit Plan B note in Methodology section: "If behavioral cloning accuracy < 55% on action prediction, explore **IQ-Learn** (Garg et al., 2021) as an inverse RL alternative." IQ-Learn is already in supplementary references — this promotes it to documented fallback.
- Zero schedule cost.

---

### Step 14 — Evaluation Frameworks (14d — unchanged)

**[P4*] Prove Evaluation Failure Modes (cautious)**
- Adjust objectives to include explicit "evaluation failure mode" experiments: identify specific scenarios where standard metrics (Elo) mis-rank adaptive agents in non-transitive populations, or where single-metric evaluation misses safety violations.
- Frame as: "existing evaluation is broken in these N-player/adaptive settings, here's what fixes it" — genuine methodological contribution vs. toolkit assembly.
- The spinning top decomposition (Step 10) already provides the diagnostic. This reframes it as a *finding*.
- Proceed cautiously — add as experimental objective, don't over-engineer.

---

### Step 15 — Research Frontier Mapping (10d — unchanged)

**[P3] Contribution #2 Scope (final framing)**
- Ensure contribution design explicitly scopes Contribution #2 to tractable heuristics + empirical validation. State the non-claim (general N-player theorem) in the contribution summary.

**[P4*] Contribution #3 Failure-Mode Framing**
- Contribution #3 description must reference the failure-mode evidence from Step 14. The contribution is "existing evaluation breaks in these settings + our framework catches what it misses," not "we assembled a toolkit."

---

### planArchitecture.md — Global Updates

**Calendar:** Update to compressed schedule (Steps 3–5 shortened, buffer extended to Oct 2–31).

**Contribution #2 description (Section 2):** Reframe to tractable heuristics + empirical validation scope.

**Time budget line:** Update from "28 weeks (Apr 1 → Oct 14)" to "27 weeks 2 days (Apr 1 → Oct 1). Buffer: ~4.3 weeks before November deadline."

---

## What Is NOT Changing

- **Steps 6, 7, 8** (Tier 1, thesis-critical) — fully protected at 21 days each.
- **Steps 9–15** durations — unchanged.
- **Playtech data plans** — remain in architecture as a future capability. Data request comes after showing PhD progress. No schedule dependency.
- **Overall plan macro-structure** — confirmed solid by all three positions.
