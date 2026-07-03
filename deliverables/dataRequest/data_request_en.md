---
title: "Research Data Request — Anonymized Poker Hand Histories"
author: "Alexander Andreev — PhD candidate, Ruse University \"Angel Kanchev\""
date: "July 2026"
geometry: margin=2.4cm
fontsize: 11pt
colorlinks: true
---

**Dissertation topic:** Adaptive strategy learning in multi-agent imperfect-information environments — AI agents that infer opponent behavior in real time and exploit it *safely*. The PhD is individual and independent of the company; this request is for anonymized research data only.

# The request — 30-second version

- **On the order of 30–100 million anonymized cash-game hands** — the upper end is a comfortable ceiling, not a requirement (volume analysis in Details).
- **Player diversity beats volume:** the ideal shape is roughly **2,000–5,000 distinct players with 20–30k hands each** — the research studies how fast an agent can profile a new opponent, which needs many distinct players more than deep individual histories.
- **One consistent format:** single table size (6-max preferred), cash game, narrow stakes band.
- **Stable pseudonymous player IDs** — the same ID across all of a player's hands. No real identities, names, or account data needed, ever.
- **Per hand:** full action sequence with exact bet sizes, positions, starting stacks, board cards, timestamp.
- **High-value bonus if logged:** hole cards for *all* hands the platform knows them for (including mucked at showdown and folded hands, if server-side logs exist). This removes the largest statistical bias in hand-history research — see Details.

**Commitments up front:** I will sign any NDA the company requires. The data stays on a single encrypted machine, is never shared with third parties, and is deleted on request. Only aggregate statistical results would ever appear in publications — and only after company review and approval. The company can be acknowledged or remain entirely unnamed, at its choice.

# What the research does with it

Three parts of the dissertation are currently limited to synthetic data; real hands upgrade each one:

1. **Human behavioral prior.** Train a policy network by imitation learning on real play, then use it as the *anchor* for KL-regularized safe exploitation — the paradigm behind Meta's human-level Diplomacy agent (Science, 2022), not yet applied to poker in the literature.
2. **Opponent modeling from few observations.** Algorithms that infer a player's type and tendencies within tens of hands — validated against a real player population instead of scripted bots, which is the difference between a toy result and a credible one.
3. **Evaluation on real behavioral data.** The dissertation's evaluation-methodology contribution explicitly targets validation on anonymized real-world game logs; this dataset *is* that validation.

# Potential value for the company

- The opponent-modeling machinery is the same machinery that detects **anomalous play: bots, collusion, multi-accounting**. Anomaly detection is a stated application track of the dissertation — findings and methods can flow back.
- **Population-level insights** into player pool tendencies as a byproduct of the behavioral analysis.
- Association with **published academic AI research** (with full veto rights over anything that references the company or its data).

# Data-handling commitments

| Concern | Commitment |
|---|---|
| Legal | NDA / data-use agreement on the company's terms, signed before transfer |
| Storage | Single encrypted local machine; no cloud copies, no third-party access |
| Identity | No re-identification attempts; pseudonymous IDs only |
| Publication | Aggregate results only; company reviews and approves before any submission |
| Lifecycle | Data deleted on request or at project end, whichever the company prefers |

# Details (optional reading)

**On the requested volume.** The headline figure is deliberately a ceiling; useful research begins far lower. Per player, the common behavioral tendencies (looseness, aggression, positional habits) stabilize statistically within roughly 1,000–2,000 hands, while rarer situational patterns — responses to re-raises, street-by-street betting lines — occur in only a few percent of hands and need on the order of 10,000–20,000 hands per player to estimate reliably. Beyond ~50,000 hands per player, additional depth mainly serves niche studies of how a player's style drifts over time. Across the population, behavioral clustering and rapid-profiling experiments benefit from breadth: about 500 players is the working minimum, 2,000–5,000 is the sweet spot, and past ~10,000 the returns flatten. Combining the two axes, the golden initial dataset is about **2,000–5,000 players with 20,000–30,000 hands each**; volumes above ~100 million hands add storage cost without research gain. If the full ask is impractical, a floor of ~500 players × 10,000 hands (roughly 5 million total) already supports the core experiments at reduced statistical power. One further economy: a single 6-max hand provides observations for all six seats, so if the players form an overlapping pool, the number of distinct table-hands needed shrinks several-fold.

**Research context.** The dissertation develops three contributions: (1) a *Behavioral Adaptation Framework* — real-time inference of opponent strategy from observed actions; (2) *Multi-Agent Safe Exploitation* — exploiting weaker opponents while bounding worst-case losses, extending two-player safety theory toward N-player games; (3) an *Evaluation Methodology* for measuring adaptability and robustness. State-of-the-art poker AI (Libratus, Pluribus) plays a fixed equilibrium strategy identically against everyone; the research gap is principled, safe *adaptation* — and adaptation research is only as good as the behavioral data it is validated on.

**Why hole-card completeness matters.** Public hand histories reveal hole cards only at showdown (~25–30% of hands), and showdown hands are a biased sample — passive lines reach showdown far more often than aggressive ones. Models trained only on shown-down hands inherit that bias. If the platform's server-side logs retain dealt hole cards for mucked or folded hands, including them turns a biased 25% sample into a complete unbiased dataset — the single largest quality difference achievable in this kind of research.

**Ideal field list per hand.** Hand ID; timestamp; table size and stakes; button position; per-seat pseudonymous player ID and starting stack; blinds/antes posted; full ordered action sequence (fold / check / call / bet / raise with exact amounts, per street); board cards per street; hole cards where known; showdown result and pot distribution. Any standard hand-history export format is fine — parsing is my job, not the company's.

**Timeline.** No urgency on the company's side is implied. My infrastructure (parsing, storage, training pipeline) will be ready ahead of time; the data can arrive whenever the legal side is settled.
