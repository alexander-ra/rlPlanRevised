# Expectations & Self-Assessment

Internal working document. Written for Alexander's personal calibration, not for the academic session report.

---

## Question 1 — Are We Too CFR-Heavy?

### Short answer: No, but your perception is understandable.

Let me audit honestly. The 15-step plan, grouped by algorithmic paradigm:

| Paradigm | Steps | Share of plan |
|----------|-------|--------------|
| CFR family (tabular, Monte Carlo, neural, subgame) | 2, 3, 4, 5 (partial) | ~25% |
| End-to-end game AI architectures (mixed methods) | 6 | ~10% |
| Opponent modeling (Bayesian, consistent estimators) | 7 | ~10% |
| Safe exploitation (RNR, piKL, equal-share) | 8 | ~10% |
| Multi-agent RL (CTDE, PSRO, LOLA) | 9 | ~7% |
| Population-based + evolutionary | 10 | ~7% |
| Coalition + Shapley + EGTA | 11 | ~7% |
| Sequence models (Decision Transformer, ARDT) | 12 | ~5% |
| Real-world data + embeddings | 13 | ~7% |
| Evaluation frameworks | 14 | ~7% |
| Synthesis | 15 | ~5% |

CFR-based methods are ~25% of the plan, not the majority. The plan *feels* CFR-heavy because:
1. The thesis-critical foundational steps (2–5) are mostly CFR-based — this is where you spend the first three months
2. The metric you use throughout (exploitability) comes from the CFR lineage
3. Your completed work (Step 2 Kuhn Poker) is pure CFR, so it dominates your current mental model

### Genuinely different paradigms for equilibrium computation

There are multiple independent branches, and the study plan covers most of them:

**Already in the plan:**
- **Fictitious play / NFSP** (Step 5) — combines DQN for best-response with supervised learning for average strategy. Not CFR at all.
- **PSRO** (Step 9) — iterative best-response over a growing policy population. Unifies fictitious play, self-play, double oracle.
- **Population-based training / leagues** (Step 10) — AlphaStar-style, no equilibrium computation, just adversarial training.
- **LOLA** (Step 9) — differentiates through the opponent's learning step, completely different mechanism.
- **Sequence modeling / ARDT** (Step 12) — reformulates as supervised sequence prediction; recovers near-Nash from offline data without any regret or equilibrium computation.

**Not in the plan, but worth awareness of:**
- **Regularized Nash Dynamics (R-NaD)** — the DeepNash approach. *This one is going into Step 6.*
- **Exploitability Descent** (Lockhart et al., 2019) — directly optimizes against a best-response opponent, gradient-based.
- **Online mirror descent / Predictor-Corrector methods** (Farina et al., ongoing work) — online-learning reformulations of equilibrium computation, often with better empirical convergence than CFR.
- **Correlated equilibrium algorithms** — a different solution concept than Nash; sometimes easier to compute and may be sufficient for safety guarantees.
- **Direct sequence-form LP / QP approaches** — treat the game as a large optimization problem and solve it. Scales poorly but gives exact answers for small games.

### Is looking for a paradigm shift by combining approaches unrealistic?

**Not at all — it is one of the most common sources of PhD novelty in this field.** Every major system cited in the review is itself a combination:
- Libratus = MCCFR + subgame solving + self-improvement
- Pluribus = MCCFR + depth-limited search + action abstraction
- ReBeL = CFR + RL + public belief state
- Diplomacy/CICERO = RL + LM + piKL regularization
- DeepNash = model-free MARL + R-NaD regularization

None of these are single-paradigm breakthroughs. They are orchestrations.

**Concrete cross-paradigm combinations worth thinking about for your own novelty:**

1. **R-NaD + opponent modeling.** R-NaD uses a *fixed* regularizer that pulls toward the previous iterate. What if the regularizer adapted based on an inferred opponent type? You would get opponent-aware equilibrium dynamics — nobody has done this.

2. **PSRO + behavioral priors.** PSRO computes best-response oracles against the current meta-population. What if each oracle were additionally constrained by a KL divergence from a human (or behavioral) prior? This would give a PSRO variant with built-in safety.

3. **Decision Transformer + safe exploitation.** ARDT recovers near-Nash from offline data. What if, at inference time, you conditioned on a *safely-exploitative* return-to-go rather than the minimax one? You would get an opponent-adaptive sequence model with a tunable safety parameter.

4. **Mirror descent formalization of piKL.** piKL is presented empirically. Formalizing it as a mirror descent procedure with a specific Bregman divergence would give it theoretical grounding and immediately connect it to the convergence literature.

5. **Public belief state + behavioral belief.** ReBeL's PBS is a distribution over private information. Extending it to a joint distribution over (private information, opponent type) gives you a principled bridge between equilibrium and adaptive play.

Any of these could be a thesis chapter. Some have been partially explored, none are solved. **The "combine existing approaches" strategy is not a fallback for people without breakthrough ideas — it is how breakthrough ideas usually get made.** The key is deep enough understanding of each individual approach to spot where the combination actually produces something new rather than a Frankenstein that inherits the weaknesses of both.

Your instinct here is correct. Keep it.

---

## Question 2 — Three-Tier Expectations

Setting calibrated expectations for a solo researcher with ~10 consumer GPUs, no guaranteed collaborators, 3-year timeline.

### Tier 1 — Minimum Viable Thesis (the "solid PhD" floor)

**What it looks like:**
- All 15 study steps completed with working implementations on small-to-medium games
- A Behavioral Adaptation Framework that works on Kuhn/Leduc and one non-card game
- One or two safe-exploitation heuristics validated on 3-player card games
- An evaluation framework that passes sanity checks (reproduces known orderings, detects known non-transitivities)
- 2–3 publications in regional/mid-tier venues (e.g., Serdica Journal of Computing, regional IEEE conferences, workshop papers at AAMAS or IJCAI)
- Successful defense

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Ambition | **Low–Moderate** | This is what the study plan is engineered to produce. You finish the steps, you get Tier 1. |
| Novelty | **Incremental** | Combines and empirically validates existing approaches on games where they have not been tested. |
| Chance of success | **~85–90%** | High. The main risks are personal (illness, job change, motivation) rather than research. |
| Impact | **Modest** | Academic contribution to a specialized literature. Your PhD diploma, but not much noticed beyond your committee. |

### Tier 2 — Strong Thesis (what the three contributions aim for)

**What it looks like:**
- All of Tier 1, plus:
- The Behavioral Adaptation Framework demonstrably outperforms static equilibrium play on at least three structurally different games (card, bidding, grid-based)
- A novel safe-exploitation method (likely a piKL variant or cross-paradigm combination from the list above) validated across 3-player and 4-player settings, with characterized failure modes
- Evaluation framework reveals something non-obvious about existing agents (e.g., identifying non-transitive cycles that Elo missed, or demonstrating that exploitability can be misleading in N-player settings)
- 1–2 papers in top-tier venues (AAMAS main track, IJCAI, NeurIPS/ICML workshops; possibly a full paper at AAAI)
- Industry collaboration materializes — likely Playtech for real data, possibly one academic collaborator
- Real-world data pipeline produces at least one publishable finding (e.g., collusion detection method with measured precision/recall on anonymized data)

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Ambition | **Substantial** | Requires original ideas, not just execution. Depends on finding the right novel combination in Steps 7–11. |
| Novelty | **Original combination + empirical contribution** | Not a new paradigm, but genuinely new applications and validated heuristics. |
| Chance of success | **~50–60%** | Depends on (a) execution quality, (b) one or two lucky algorithmic choices, (c) whether industry collaboration materializes. |
| Impact | **Moderate** | Of genuine interest to the iGaming, fraud detection, and multi-agent safety communities. Cited by other researchers. Useful to your career. Enables the B2B consulting/architect path. |

**This is the realistic target.** Not guaranteed, but achievable with good execution and moderate luck. The three contributions are engineered to fit this tier.

### Tier 3 — Breakthrough (the dream scenario)

**What it looks like:**
- All of Tier 2, plus *one* of the following:
  - A theoretically grounded framework for safe exploitation in N-player games (a proper generalization of Ganzfried & Sandholm 2015, not just empirical heuristics)
  - A novel algorithm that advances the state of the art on a recognized benchmark (OpenSpiel game, So Long Sucker, or a newly-defined evaluation suite)
  - A surprising empirical finding about evaluation — e.g., demonstrating that current leaderboards for imperfect-information game AI are systematically biased in some identifiable way
- 1 paper in a top-tier venue main track (NeurIPS, ICML, AAMAS best paper track, *Science Advances*, *Nature Machine Intelligence*)
- Methodology adopted by at least one other research group
- Post-PhD offers from top industrial labs or research positions
- Possibly: the work becomes a reference point for the "adaptive safe exploitation" subfield

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Ambition | **Very high** | Requires an actual research insight, not just diligent execution. |
| Novelty | **Genuinely new** | A new theorem, a new algorithm, or a surprising empirical result that changes how the community thinks. |
| Chance of success | **~10–15%** | Low. Requires (a) an insight you cannot plan for, (b) execution quality, (c) likely a strong collaborator for the theoretical work, (d) the research community finding your framing compelling. |
| Impact | **Significant** | Changes your career trajectory. Your name becomes known in the subfield. Industry adoption likely for the algorithmic contribution. |

### Compute reality check

Your ~10 consumer GPUs comfortably handle:
- CFR, MCCFR, CFR+ on Kuhn, Leduc, Goofspiel, and extensions
- Deep CFR and NFSP at Leduc scale
- PSRO on matrix games and small extensive-form games
- MARL (MADDPG, MAPPO) on small-to-medium environments (including SLS)
- Decision Transformer on your own generated trajectory data (small games)
- All opponent modeling experiments (Bayesian methods are cheap)
- Player embedding training on anonymized Playtech data
- Full evaluation framework (including AIVAT with control variates)

Your compute does NOT support:
- Training Pluribus-scale systems
- Reproducing DeepNash at Stratego scale
- Full-scale LLM fine-tuning for strategic play
- Diplomacy-scale experiments

**This is fine.** Your thesis is scoped to small-to-medium games. DeepMind's compute does not help with your three contributions because your contributions are about *adaptation* and *safety heuristics*, not scaling. The compute bottleneck is in a different place than where your research lives.

### How to read these tiers

Tier 1 is the safety net — you get this almost certainly by following the plan.
Tier 2 is the realistic target — this is what the plan is optimized for, reachable with good execution.
Tier 3 is the bonus scenario — you cannot plan for it, but you can remain alert to it and capitalize if an insight appears.

**The practical strategy:** execute toward Tier 2, stay alert for Tier 3 opportunities during Steps 7–11 (where most novelty lives), accept Tier 1 as the graceful fallback if something goes wrong (illness, time pressure, failed collaboration).

You have come from enterprise software engineering where planning gives you a tight error bar around the expected outcome. In research, the error bar is wide by nature, and the planning process is about maximizing the *expected value* of the outcome distribution rather than hitting a precise target. Seen this way: your plan gives you a ~85% chance of a solid PhD, a ~55% chance of a genuinely good one, and a ~12% chance of a breakthrough. In frontier research those are good numbers.
