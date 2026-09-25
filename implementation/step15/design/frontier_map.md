# Research frontier map

## "Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments"
## Alexander Andreev — PhD, University of Ruse "Angel Kanchev", 2026–2029

*Chapter 15, September 2026. The map follows the plan's nine sections (raw step 15, Phase 5
Day 1). Gap wording is taken from `deliverables/finalReview/lit_gaps.md` (verified 2026-09-24);
where the plan's 2026-04 map disagrees, the lit_gaps wording is used and the difference is listed
in § 10. Every number names its result file; pilot numbers (P0–P2) are from this chapter's
`implementation/results/` and are feasibility evidence, not the contributions' results.*

---

## 1. Field overview

Imperfect-information games are the standard testbed for decisions under hidden information and
strategic opponents. The field can now compute near-equilibrium strategies at scale — CFR and its
sampled and neural variants, abstraction, safe subgame solving, search — and every landmark
superhuman poker system plays such a strategy (DeepStack, Libratus, Pluribus, ReBeL, Student of
Games). Their guarantees are two-player zero-sum; Pluribus, the one six-player system, has none
and "plays a fixed strategy that does not adapt" (Brown & Sandholm 2019).

Adaptation is where the value against real, sub-optimal opponents lies, and it is an active field
in two-player games: online Bayesian and in-context opponent modelling with conservative
fallbacks (GSCU, OMIS), and poker agents that exploit while staying near equilibrium
(StratFormer, AlphaExploitem). Safe exploitation — deviating from equilibrium without becoming
exploitable — has a mature two-player theory, from Ganzfried & Sandholm's gift characterisation
to adaptation safety (OX-Search) and certified per-deployment guarantees. With three or more
players the anchor of all of it, the minimax value, is gone: equilibria are neither unique nor
safe, opponents can coordinate, and the safety notions that exist are either conservative
(team-maxmin) or provably unattainable against heterogeneous opponents (equal share).
Evaluation has matured along separate axes — worst case, variance-reduced head-to-head,
population ratings, generalisation — and each breaks for adaptive, exploiting or N-player agents.

The thesis sits at the intersection: an agent that starts from an equilibrium-based safe strategy,
infers its opponents during play (C1), deviates only as far as a stated loss bound allows, also
when opponents coordinate (C2), and is measured by a protocol that captures gain, speed and risk
together across games (C3).

---

## 2. Contribution 1 — within-match opponent inference for N-player games

### 2.1 What exists
- Two-player detect → adapt with a conservative fallback, against switching opponents, including
  Kuhn poker: GSCU (Fu et al., ICML 2022); PACE (Ma et al., ICML 2024). **Solved in two-player
  games.**
- In-context opponent modelling with switches *between* episodes: TAO, OMIS, OEOM (Jing et al.
  2024–2025). **Solved between episodes, not within.**
- Poker model-and-exploit near equilibrium, heads-up: StratFormer (CG 2026, preprint),
  AlphaExploitem (2026 preprint). **Solved in small two-player games; N-player and non-stationary
  opponents listed as future work.**
- Opponent models inside depth-limited search, model given: Milec et al. (AAMAS 2024, 2025).
- N-player opponent modelling without safety: Ganzfried, Wang & Chiswick (DAI 2024, three-player
  Kuhn); Shi et al. (2025, multi-player hold'em). **Exists; no safety criterion.**
- Real-log behaviour representation: player2vec-style embeddings, behavioural cloning, style
  clustering (replicated on 2 M real hands in Chapter 13).

### 2.2 The gap (lit_gaps)
Real-time opponent modelling with a conservative fallback exists and works in two-player games;
all of it is two-player, and N-player opponent modelling exists without any safety criterion.
**Open:** online inference in N-player imperfect-information games that handles strategy shifts
*within* a match and is coupled to an explicit safety criterion and a common evaluation protocol.

### 2.3 The thesis's approach
A per-opponent Dirichlet model with hidden cards handled by posterior-weighted soft counts; a type
prior learned from real logs (Chapter 13); multi-signal within-match change detection with partial
resets; a calibrated confidence passed to C2's deviation rule; online collusion signals.
Design: `design/C1.md`; Experiment 1.1 and 1.2 in `design/experiments.md`.

### 2.4 Evidence of feasibility
- Adaptation is fast in small games: median h50 = 50 hands for every adaptive agent on Kuhn;
  within-match recovery ranges from 50 hands (change-point agent) to never (type-based)
  (`implementation/step14/implementation/results/adaptation_kuhn.json`).
- A three-player model works: DirBR3P gains +0.372 ± 0.038 chips/hand over the blueprint against
  independent pairs and captures 0.99 within 50 hands (`step14/…/nplayer_kuhn3.json`).
- Real logs carry the information: re-identification 15.6 % top-1 among 834 players from 400
  hands (chance 0.12 %); 66 % of players reach a confident online type within 500 hands, median
  85; the player's style lowers action NLL from 0.800 to 0.751 nats
  (`implementation/step13/implementation/results/{player2vec,clustering,bc}.json`).
- Collusion leaves a detectable trace when each player is compared with themselves: soft play at
  q = 0.5 AUC 0.999; dumping at q = 0.25 AUC 0.853 (`step13/…/collusion_mw.json`).

### 2.5 Risks and mitigation
Novelty shrinks further if two-player agents extend to N players first → publish the N-player,
within-match, safety-coupled evaluation in 2027 and claim only the coupling. Change detection
misfires (Chapter 14 on Leduc) → multi-signal detection and a reported false-alarm rate. No
labelled real data → injected colluders and the Pluribus hands as ground truth; Playtech data as a
bonus. Details in `design/C1.md` § 9.

---

## 3. Contribution 2 — N-player safe exploitation (the centrepiece)

### 3.1 What exists
- Two-player safe exploitation: ε-safe responses and RNR (Johanson et al. 2007); gift-based
  RWYWE/BEFFE (Ganzfried & Sandholm, ACM TEAC 2015); prime-safe (Jeary & Turrini 2023 preprint);
  SES (Liu et al., NeurIPS 2022); adaptation safety, OX-Search (Ge, Xu, Ding, Meng, An, Li & Gao,
  ICML 2024); beyond the depth limit (Milec et al. 2025); certified restricted responses (Li &
  Huang 2026 preprint); bounded test-time RL degradation (Kubíček et al. 2026 preprint);
  baseline-relative regret, O(1) risk vs Ω(T) gain (Müller et al., ICML 2025). **All two-player
  zero-sum.**
- N-player safety notions: equal share C/n — achievable only against identical, slowly adapting
  opponents, provably not securable against heterogeneous ones (Ge, Wang, Li & Jin, ICML 2025,
  Props. 4.1–4.2); team-maxmin values against a coordinated coalition (Celli & Gatti 2018; Zhang,
  An & Černý 2021; Zhang, Farina & Sandholm 2023); baseline-relative regret (Müller et al. 2025).
  Ganzfried & Sandholm (2015, § 2.3) also remark that their method "applies straightforwardly" to
  multiplayer games with the maximin value in place of the minimax value — stated, not evaluated.
- KL-anchored play in seven-player Diplomacy — anchored to an imitation-learned *human* policy
  for compatibility, no loss bound (Jacob et al., ICML 2022; Bakhtin et al., ICLR 2023).
- Coalitions: synchronous vs asynchronous (Babyak et al. 2024 preprint); utility transfer inside
  the three-player Kuhn equilibrium family (Szafron et al., AAMAS 2013); collusion detection scored
  offline (Mazrooei et al. 2013; Bonjour et al. 2022; Greige et al. 2022; Xu et al. 2025).

### 3.2 The gap (lit_gaps)
Safe exploitation has a mature two-player zero-sum theory. With three or more players the
existing notions are very conservative (team-maxmin) or provably unattainable against
heterogeneous opponents (equal share), KL anchoring is behavioural, and multiplayer exploitation
has no loss bound. **Open (no counter-example found):** exploiting sub-optimal opponents in
N-player imperfect-information games while bounding the loss relative to a baseline, and testing
that bound against colluding opponents. C2 targets this empirically, in small games; it claims no
general N-player safety theorem.

### 3.3 The thesis's approach
Three deviation rules on top of C1's model, each with a stated criterion that is *checked
exactly* in three-player Kuhn: (i) Ganzfried & Sandholm's gift accounting with the team-maxmin
value as the floor (their § 2.3 made concrete, with a coordinated pair as the adversary);
(ii) a sequence-form mixture of blueprint and best response whose worst-case baseline-relative
loss is capped at ε per hand; (iii) a KL-anchored response to the model, anchored to the blueprint
(the thesis's own proposal; loss measured). Equal share is a reference line, not a guarantee.
Design: `design/C2.md`; Experiments 2.0–2.2.

### 3.4 Evidence of feasibility
- Two-player: this chapter's RWYWE (P0–P1) — see `design/C2.md` § 6 and `EXECUTION_NOTES.md`.
- Three-player: the maximin floor and the capped/anchored deviations (P2) — `design/C2.md` § 6.
- The measurement exists: Chapter 14's exact coalition value, now computed on the unique pure
  plans of one opponent in ≈ 5 ms (`implementation/step15/implementation/mmsafe3p.py`).
- A caution on the gap wording: in three-player Kuhn the team-maxmin value is only 0.0076
  chips/hand below equal share on seat average (`maximin3p.json`), so "very conservative" did not
  hold in this one game. The lit_gaps wording is kept; whether this persists in larger games is an
  open question for Experiment 2.1's scaling arm.
- The problem is real: NashConv ≈ 0 equilibrium components lose 0.06–0.17 chips/hand more to a
  coordinated pair than they earn in equilibrium; an unbounded exploiter loses 0.466 to an adaptive
  coalition (`step14/…/nplayer_kuhn3.json`).

### 3.5 Risks and mitigation
No general theorem → the non-claim is stated; each bound is exact by construction or checked by
enumeration, in small games. Exact checks do not scale → learned coalition exploiters with stated
budgets for three-player Leduc, calibrated on three-player Kuhn. The baseline itself can be unsafe
(the blueprint loses 0.119 chips/hand to a fixed pair) → report absolute and baseline-relative
readouts, and the maximin strategy as a second baseline. Details in `design/C2.md` § 9.

---

## 4. Contribution 3 — evaluation methodology

### 4.1 What exists
Exact and learned exploitability; NashConv; LBR; AIVAT and its 2026 refinements; Elo, TrueSkill,
Nash averaging, α-Rank, VasE, deviation ratings; EGTA and spinning tops; Melting Pot; LLM arenas;
the RRPS benchmark (Lanctot et al., TMLR 2023) — population return and within-population
exploitability together, one two-player game. Full list: `lit_evaluation.md`.

### 4.2 The gap (lit_gaps)
**Open:** a protocol that reports gain, adaptation speed and recovery, and worst-case or
coalition-aware robustness, with confidence bounds, applied unchanged across several
imperfect-information games including N-player ones.

### 4.3 The thesis's approach
Chapter 14's joint protocol (gain, capture, h50/r50, exposure or coalition value, teaching loss,
confidence), plus this chapter's match-level safety readout; applied unchanged to two- and
three-player Kuhn and Leduc; the nine failure modes as a detection matrix. Design: `design/C3.md`;
Experiment 3.1.

### 4.4 Evidence of feasibility
Chapter 14 reproduced failure modes 1–5 and 7–9: Elo–exploitability τ = 0.36 on Leduc; clones
widen an exploiter's Elo lead from +84 to +113; α-Rank's leader changes four times with α;
per-window capture needs ≈ 3,383 hands raw vs ≈ 379 with AIVAT; within-population
exploitability sees 0.279 of DirBR's 2.461 exposure; DirBR3P tops Elo and Nash averaging and loses
0.47 chips/hand to a coalition teaching attack (`implementation/step14/implementation/results/`).

### 4.5 Risks and mitigation
"Assembled toolkit" objection → failure-mode framing (plan note P4*). Exact metrics only in toy
games → budgets stated for learned exploiters. So Long Sucker uninformative in its current engine
→ dropped as a C3 testbed unless fixed. Details in `design/C3.md` § 9.

---

## 5. How the contributions interact

C1 turns observations into a model and a *confidence*; C2 decides how far that confidence may move
the agent from its safe baseline, under a stated bound; C3 measures gain, speed, recovery and loss
together, which is the only way C1 and C2 can be claimed at all. The two-player versions (Chapters
7, 8, 14 and this chapter's RWYWE) are the reference points every N-player result is compared
with. The fair-play thread (Chapter 13's collusion and bot detection) enters C2 as the
coalition-aware response (Experiment 2.2) and C3 as the coalition readouts.

## 6. Publication pipeline

Six papers mapped to Chapters II–IV, first publication and venues: `design/publications.md`.

## 7. Experimental infrastructure (what exists)

| Component | Where | Status |
|---|---|---|
| Exact array engine for Kuhn, Leduc, three-player Kuhn (values, best responses, NashConv, AIVAT) | `implementation/step14/implementation/trees.py`, `aivat.py` | validated against OpenSpiel to 10 decimals |
| One-shot sequence-form LPs (maxmin, RNR, floor), full Leduc in 0.02–0.04 s | `step14/…/solvers.py` | validated against Chapter 8 |
| Opponent models (type-based, Dirichlet, change points) and zoos | `implementation/step07/implementation/`, `step14/…/zoo.py`, `nplayer.py` | used in Chapters 7, 8, 14, 15 |
| Gift accounting and RWYWE / BEFEWP / BEFFE | `implementation/step15/implementation/gifts.py`, `safe_agents.py` | replicates G&S Table I (P0) |
| Exact coalition oracle, maximin value, bounded and maximin-floor agents | `step15/…/mmsafe3p.py`, `bounded3p.py`, `maximin3p.py` | P2 |
| Joint evaluation protocol and population tools | `step14/…/run_*.py`, `population.py` | Chapter 14 |
| Real hand histories: parser, statistics, player2vec, collusion and bot detection | `implementation/step13/implementation/` (data in `D:/datasets/`) | Chapter 13 |
| So Long Sucker engine and coalition detector | `implementation/step11/implementation/` | deadlock-prone; not a testbed of record |
| NLHE blueprint project | `implementation/nlhe/` | outside steps 1–15; infrastructure for a large-game arm, if time |

## 8. Scope boundaries

In scope: imperfect-information games of the poker family (two- and three-player Kuhn and Leduc;
real no-limit hand histories for C1's data side); agents that start from an equilibrium-based
strategy; empirical safety criteria checked exactly where the game allows. Out of scope: a general
N-player safety theorem (the non-claim of C2); perfect-information games; purely cooperative MARL
(background only); LLM agents except as extracted fixed strategies in the zoo; human-subject
experiments (the individual plan's "pilot users" are met with anonymised real logs where
available). So Long Sucker is optional, conditional on an engine in which alliances matter.

## 9. Career connection

C1's data side (Chapter 13's pipeline, collusion and bot detection) maps onto fraud and risk
analytics on online game platforms; C2 onto multi-agent strategy under adversarial coordination;
C3's evaluation discipline onto both.

## 10. Corrections to the plan's frontier map (April 2026 → September 2026)

| Plan (raw step 15) | What holds (source) |
|---|---|
| C1 gap: "no unified detect → adapt framework (papers do one, not both)"; "static detection only"; "poker-specific" | narrowed: GSCU, PACE, StratFormer, AlphaExploitem, ABD exist; the open part is N-player, within-match, safety-coupled (lit_gaps C1) |
| C2 gap: "ALL safe exploit is 2-player"; "coalition dynamics unstudied"; "no N-player safety notion" | safe exploitation *is* two-player, but N-player notions exist (equal share, team-maxmin, baseline-relative regret) and coalitions are studied (lit_gaps C2) |
| "Equal share … guarantees at least equal share" (as a guaranteed minimum) | equal share is a target C/n, provably not securable against opponents playing different strategies (Ge et al. 2025, Prop. 4.1); a reference line only |
| OX-Search = "Ge, Kovařík & Lisý (2024)", arXiv "2405.XXXXX" | Ge, Xu, Ding, Meng, An, Li & Gao, ICML 2024, PMLR 235; Kovařík and Lisý co-authored ABD with Milec |
| piKL "within a KL-divergence ball of the Nash policy" | piKL anchors to an imitation-learned human policy (Jacob et al. 2022; Bakhtin et al. 2023); anchoring to a blueprint is the thesis's own proposal |
| "Human-Level Performance in No-Press Diplomacy (Bakhtin et al., 2022)" | that title is Gray, Lerer, Bakhtin & Brown, ICLR 2021; the piKL sources are Jacob 2022 and Bakhtin 2023 |
| C3 gap: "no framework combines exploitability + ranking + confidence"; "no cross-game validation"; "O(n²) scaling" | narrowed: RRPS combines return and exploitability; cross-game ratings exist; adaptive sampling addresses scaling (lit_gaps C3) |
| AIVAT "(2019)", Burch, Johanson & Bowling; spinning top "(2019)" | AIVAT: Burch, Schmid, Moravčík, Morrill & Bowling, AAAI 2018; spinning tops: Czarnecki et al., NeurIPS 2020 (the decomposition: Balduzzi et al., ICML 2019) |
| "Jiawei Ge is co-author of both OX-Search and Equal Share" | not supported by the author lists: OX-Search's first author is Z. Ge (with Xu, Ding, Meng, An, Li, Gao); equal share's is J. Ge (with Wang, Li, Jin) — the "companion papers" link should be dropped |
| Testbeds "Kuhn, Leduc, SLS, Playtech" | SLS optional (engine deadlocks); Playtech data not yet available — public IPN/Pluribus hands used (Chapter 13) |
| First experiment "piKL exploitation on 3-player Kuhn"; KL budget as the safety knob | Experiment 2.1 with three rules and exact bounds; the KL rule has no a-priori bound |
| First publication "NeurIPS 2026 workshop / AAAI-26 workshop", three-layer framework | Paper 1 = the joint protocol with failure modes and match-level safety, IEEE CoG 2027 (AAMAS 2027 as a stretch) |
