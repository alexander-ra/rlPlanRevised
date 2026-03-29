# Step 15 — Research Frontier Mapping + Contribution Design

**Duration:** 10 days (Tier 3)  
**Dependencies:** All prior steps (Steps 1–14)  
**Phase:** G — Integration (capstone)

---

## Objectives

This step synthesizes the entire 15-step learning progression into a structured PhD research plan. It maps the research frontier across three contribution areas, designs the experimental programme, specifies publication targets, and produces the planning documents that guide the transition from the learning phase to the research phase (November 2026 onwards).

By completion, the following questions are answered with precision:
1. What are the three thesis contributions, and what specific gaps in the literature do they address?
2. What experiments will validate each contribution, with what metrics and baselines?
3. What is the publication pipeline (venues, timelines, content)?
4. What is the structure of Chapter I (state of the art + problem analysis)?

---

## Literature Context

### Research Landscape

The thesis title — *"Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments"* — sits at the intersection of three active research areas: opponent modeling and exploitation (Steps 7–8), multi-agent reinforcement learning in games (Steps 9–11), and evaluation methodology for game AI agents (Steps 10, 14). Recent literature searches confirm that while each area has strong individual contributions, the intersection remains unoccupied.

### Key References for Frontier Mapping

**For Contribution #1 (Behavioral Adaptation Framework):**
- Southey, F., Bowling, M., Larson, B., Piccione, C., Burch, N., Billings, D. & Rayner, C. (2005). "Bayes' Bluff: Opponent Modelling in Poker." *UAI.*
- Bard, N. & Bowling, M. (2013). "Determining the Number of Players in a Peer-to-Peer Poker Network." *AAMAS.*
- Wang, Z., Cui, B., Smola, A. et al. (2024). "player2vec: A Language Modeling Approach to Understand Player Behavior." *arXiv:2404.XXXXX.*
- Bakhtin, A. et al. (2022). "Human-Level Play in the Game of Diplomacy by Combining Language Models with Strategic Reasoning." *Science.* (piKL regularization)

**For Contribution #2 (Multi-Agent Safe Exploitation):**
- Ganzfried, S. & Sandholm, T. (2015). "Safe Opponent Exploitation." *ACM TEAC.*
- Liu, S. et al. (2022). "Safe Opponent-Exploitation Subgame Refinement." *AAAI.*
- Jeary, A. & Turrini, P. (2023). "Safe Opponent Exploitation For Epsilon Equilibrium Strategies." *ECAI.*
- Ge, J., Kovařík, V. & Lisý, V. (2024). "Safe and Robust Subgame Exploitation in Imperfect Information Games (OX-Search)." *arXiv:2405.15999.*
- Milec, D., Kovařík, V. & Lisý, V. (2025). "Adapting Beyond the Depth Limit: Counter Strategies in Large Games (ABD)." *AAAI.*
- **Ge, J., Wang, Y., Li, W. & Jin, C. (2024). "Securing Equal Share: A Principled Approach for Learning Multiplayer Symmetric Games." arXiv:2406.04201.** — Defines the "equal share" objective (payoff ≥ C/n) as the natural safety baseline for N-player symmetric constant-sum games. Demonstrates that Nash equilibria in multiplayer games are neither unique nor non-exploitable.
- **Babyak, J., Buck, K., Dichter, L., Jiang, D. & Zumbrun, K. (2024). "Synchronous vs. Asynchronous Coalitions in Multiplayer Games, with Applications to Guts Poker." arXiv:2412.19855.** — Formalizes coalition communication levels (synchronous/asynchronous) with distinct equilibrium values.

**For Contribution #3 (Evaluation Methodology):**
- Omidshafiei, S. et al. (2019). "α-Rank: Multi-Agent Evaluation by Evolution." *Nature Scientific Reports.*
- Lanctot, M. et al. (2023, revised 2025). "Evaluating Agents using Social Choice Theory (VasE)." *arXiv:2312.03121.*
- Burch, N., Johanson, M. & Bowling, M. (2019). "AIVAT: A New Variance Reduction Technique for Agent Evaluation in Imperfect Information Games." *AAAI.*
- Timbers, F. et al. (2020). "Approximate Exploitability: Learning a Best Response in Large Games." *arXiv:2004.09677.*
- Balduzzi, D. et al. (2019). "Re-evaluating Evaluation." *NeurIPS.* (Spinning top decomposition)
- Rowland, M. et al. (2019). "Multiagent Evaluation under Incomplete Information." *arXiv:1909.09849.*

### Frontier Assessment

The freshness scan across all 15 steps (March 2026) confirms:
- **No existing work** combines safe exploitation with N-player settings — the gap for Contribution #2 is genuine and explicitly acknowledged in the literature (OX-Search: "one of the most lucrative unsolved problems in game theory").
- **No existing framework** integrates exploitability measurement, population ranking, and statistical confidence into a unified evaluation pipeline — the gap for Contribution #3 is a methodology gap rather than a theoretical impossibility.
- **No existing pipeline** provides closed-loop detect→adapt→evaluate for opponent strategy inference — the gap for Contribution #1 is an engineering/integration gap with strong theoretical foundations already in place.

---

## Proposed Thesis Contributions

### Contribution #1: Behavioral Adaptation Framework

**Problem:** Given a sequence of observed actions from an opponent in an imperfect-information game, infer the opponent's strategy type in real-time, adapt the exploitation strategy accordingly, and maintain a safety guarantee during adaptation.

**Gap:** Detection papers (Southey 2005, player2vec 2024) stop at classification. Exploitation papers (OX-Search 2024) assume known opponent type. No unified detect→adapt→evaluate pipeline exists.

**Proposed method:** player2vec embedding → Bayesian type posterior → strategy selection conditioned on posterior → online update from outcomes → evaluation via Contribution #3.

**Experimental domains:** Kuhn Poker (proof-of-concept), Leduc Poker (scaling), Playtech data (real-world validation).

### Contribution #2: Multi-Agent Safe Exploitation

**Problem:** Extend safe exploitation guarantees from 2-player zero-sum to N-player settings. In N-player symmetric constant-sum games, Nash equilibria are non-unique and non-exploitable (Ge et al. 2024). The "equal share" value (C/n) replaces the minimax value as the safety baseline.

**Gap:** ALL existing safe exploitation theory requires 2-player zero-sum constraints. The minimax theorem fails for N > 2. No prior work combines exploitation with N-player safety.

**Proposed approaches:**
1. *Conservative:* piKL-regularized exploitation — constrain deviation from equal share policy via KL divergence.
2. *Ambitious:* Redefined adaptation safety — replace minimax value with equal share value in the RNR/OX-Search framework.
3. *Pragmatic:* Population-based safety — validate worst-case performance across a diverse opponent population.

**Experimental domains:** 3-player Kuhn Poker (exact analysis), 3-player Leduc Poker (intermediate), So Long Sucker (4-player, dynamic coalitions).

### Contribution #3: Evaluation Methodology

**Problem:** Produce comprehensive, cross-game evaluation of AI agents in imperfect-information games addressing: (1) exploitability to worst-case adversaries, (2) ranking within a diverse agent population, (3) statistical confidence of measurements.

**Gap:** No existing framework integrates all three evaluation layers. Individual metrics are presented in isolation, and no cross-game validation exists.

**Proposed method:** Three-layer framework (exploitability module + population ranking module + confidence module) applied consistently across multiple game types, with coalition-aware extensions for N-player settings.

**Experimental domains:** Kuhn, Leduc, So Long Sucker, Playtech data.

---

## Experimental Programme

### Experiment 1.1: Behavioral Adaptation on Kuhn Poker
- **Hypothesis:** player2vec embeddings with Bayesian type inference classify opponent types within 50 hands at >80% accuracy.
- **Variables:** Observation window size (10–200 hands), classification accuracy, exploitation gain (mbb/hand), safety (worst-case payoff).
- **Agents:** Bot zoo from Step 14 (7+ agents across four tiers).
- **Baselines:** Static Nash, Oracle (known type), random adaptation.

### Experiment 2.1: N-Player Safe Exploitation on 3-Player Kuhn
- **Hypothesis:** piKL-regularized exploitation achieves payoff > C/3 against sub-optimal opponents while maintaining payoff ≥ C/3 − ε against adversaries.
- **Variables:** KL budget (0.01–5.0), exploitation gain, worst-case safety.
- **Configurations:** All-sub-optimal, mixed, and all-adversarial opponent settings.
- **Baselines:** Equal share policy, unrestricted best response, 2-player safe exploitation methods.

### Experiment 2.2: Coalition-Aware Safe Exploitation on So Long Sucker
- **Hypothesis:** Coalition-aware exploitation outperforms coalition-unaware methods in a 4-player dynamic coalition setting.
- **Variables:** Coalition awareness model (none, static, dynamic), win rate, coalition formation patterns.
- **Baselines:** Static Nash approximation, piKL without coalition awareness.

### Experiment 3.1: Cross-Game Evaluation Framework Validation
- **Hypothesis:** The three-layer framework produces consistent rankings across Kuhn, Leduc, and SLS, and reveals insights missed by single-metric evaluation.
- **Variables:** Agent rankings under Elo vs α-Rank vs VasE, spinning top decomposition, cross-game rank stability.
- **Baselines:** Elo alone, α-Rank alone.

---

## Publication Pipeline

| Deadline | Chapter | Publication Target | Content |
|----------|---------|-------------------|---------|
| 11.2026 | I: State of the Art | Workshop paper (NeurIPS/AAAI 2026 workshop or AAMAS 2027 poster) | Three-layer evaluation framework on Kuhn + Leduc (Contribution #3) |
| 04.2027 | II: Theoretical Research | Full paper (AAMAS 2027 or AAAI 2028) | N-player safe exploitation formal framework + 3-player Kuhn/Leduc (Contribution #2) |
| 04.2027 | II: Theoretical Research | Workshop paper (NeurIPS/ICML 2027 workshop) | Behavioral adaptation pipeline on Kuhn + Leduc (Contribution #1) |
| 01.2028 | III: Practical Problem Solving | Full paper (NeurIPS 2028 or ICML 2028) | Full pipeline on SLS + Playtech data (Contributions #1 + #2) |
| 01.2028 | III: Practical Problem Solving | Industry/applied venue (IEEE, ACM) | Playtech behavioral analysis + collusion detection (Contribution #1) |
| 08.2028 | IV: Experimental Research | Journal paper (JAIR, AIJ, or IEEE TNNLS) | Cross-game unified evaluation with complete experimental results (All contributions) |

**Target:** 4–6 publications by defense (04.2029), minimum 3 required.

---

## Chapter I Outline

*Target: 25–30 pages, deadline November 2026*

1. **Introduction** (2 pp.) — Motivation, scope, research questions
2. **Foundations** (4 pp.) — Game theory prerequisites (extensive-form games, Nash equilibrium, CFR), RL prerequisites, the bridge to neural methods (Deep CFR, DREAM, ReBeL, Student of Games)
3. **Opponent Modeling and Behavioral Adaptation** (5 pp.) — Bayesian opponent models, modern behavioral inference (player2vec, behavioral cloning), online adaptation mechanisms; identification of Contribution #1 gap
4. **Safe Exploitation in Imperfect-Information Games** (6 pp.) — The SOE lineage (Ganzfried → Liu → Jeary → OX-Search), adaptation safety, the N-player gap (minimax failure, non-unique equilibria), equal share objective (Ge 2024), coalition dynamics (Babyak 2024); identification of Contribution #2 gap
5. **Evaluation of Multi-Agent Game AI** (5 pp.) — Exploitability metrics, population-level ranking (Elo, α-Rank, VasE), variance reduction (AIVAT), cross-game challenges; identification of Contribution #3 gap
6. **Research Questions and Proposed Contributions** (3 pp.) — Three research questions mapped to three contributions with proposed methodology
7. **Conclusion and Research Plan** (2 pp.) — Summary of gaps, methodology overview, timeline aligned with dissertation chapters

---

## Deliverables

1. Research frontier map (visual and document) — three contributions with gap analysis, supporting evidence, and feasibility assessment
2. Gap validation log — each gap verified against recent literature, conferences, and dissertations
3. Contribution design documents (3 documents, 2–3 pages each) — problem/prior art/gap/method/experiments/publications/timeline/risk
4. Publication pipeline — 6 publications mapped to 4 dissertation chapters with venues and deadlines
5. Experiment specifications (4 experiments) — hypotheses, variables, protocols, baselines, expected results
6. Chapter I outline — 7 sections, 25–30 pages, aligned with November 2026 deadline
7. First publication draft plan — title, venue, content, target length
8. Mandatory one-pager and Learning Log update

---

## Validation Criteria

- Each contribution gap confirmed against Google Scholar, recent conference proceedings (NeurIPS/ICML/ICLR 2025–2026, AAAI 2026), and recent PhD dissertations from leading groups (CMU, Alberta, DeepMind)
- Experiment specifications include falsifiable hypotheses with quantitative metrics
- Publication pipeline is reviewed against actual venue deadlines and acceptance rates
- Chapter I outline covers all material from Steps 1–14 with no significant gaps
- The research plan is defensible for a 3-year PhD scope (not over-ambitious, not under-ambitious)

---

## PhD Contribution Alignment

**Step 15 is the transition point.** Steps 1–14 constitute the learning phase; Step 15 designs the research phase. The deliverables from this step directly become:
- Chapter I structure → the first dissertation chapter (deadline 11.2026)
- Contribution design documents → the research proposals for Chapters II–IV
- Experiment specifications → the experimental protocol for the next 2 years
- Publication pipeline → the career-building academic output schedule

The three contributions are designed to align with both the university requirements (4 chapters, 4+ publications, defense by 04.2029) and the career targets (Contribution #1 → fraud/risk detection roles, Contribution #2 → MARL architect roles, Contribution #3 → universal evaluation expertise).

---

## Exit Criteria

- [ ] Three contribution gaps identified, validated, and documented with supporting literature evidence
- [ ] Contribution design documents completed for all three contributions
- [ ] Publication pipeline specified with venues, deadlines, and content mapping
- [ ] Four experiment specifications with falsifiable hypotheses and quantitative protocols
- [ ] Chapter I outline complete (7 sections, 25–30 pages target)
- [ ] First publication draft plan specified
- [ ] Research frontier map finalized (visual and document formats)
- [ ] Gap validation log completed
- [ ] Can articulate the thesis scope boundaries (what is and is not covered)
- [ ] One-pager written and committed
- [ ] Learning Log updated with final cross-step connections and PhD research questions
- [ ] Step notes committed to repository

> **[P3] Contribution #2 scope (final framing):** Ensure contribution design explicitly scopes Contribution #2 to tractable heuristics + empirical validation on small N-player games. State the non-claim (general N-player safety theorem) in the contribution summary.

> **[P4*] Contribution #3 failure-mode framing:** Contribution #3 description must reference failure-mode evidence from Step 14. The contribution is “existing evaluation breaks in these settings + our framework catches what it misses,” not “we assembled a toolkit.”

