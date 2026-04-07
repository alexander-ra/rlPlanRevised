# Step 15 — Research Frontier Mapping + Contribution Design

**Duration:** 10 days (Tier 3)  
**Dependencies:** ALL prior steps (Steps 1–14)  
**Phase:** G — Integration (capstone)  


## Table of Contents
- [Phase 1: Intuition (1 day)](#phase-1-intuition-1-day)
  - [Talks and Overviews](#talks-and-overviews)
  - [Blog Posts / Accessible Reads](#blog-posts-accessible-reads)
- [Phase 2: Exploration (1 day)](#phase-2-exploration-1-day)
  - [Activity 1: Build the Frontier Map (half day)](#activity-1-build-the-frontier-map-half-day)
  - [Activity 2: Gap Validation (half day)](#activity-2-gap-validation-half-day)
- [Phase 3: Targeted Reading (2 days)](#phase-3-targeted-reading-2-days)
  - [Day 1: Contribution #2 Anchoring (the thesis centerpiece)](#day-1-contribution-2-anchoring-the-thesis-centerpiece)
  - [Paper 1: "Securing Equal Share: A Principled Approach for Learning Multiplayer Symmetric Games" (Ge, Wang, Li & Jin, 2024)](#paper-1-securing-equal-share-a-principled-approach-for-learning-multiplayer-symmetric-games-ge-wang-li-jin-2024)
  - [Paper 2: "Safe and Robust Subgame Exploitation in Imperfect Information Games" (Ge, Kovařík & Lisý, 2024 — OX-Search)](#paper-2-safe-and-robust-subgame-exploitation-in-imperfect-information-games-ge-kovařík-lisý-2024-ox-search)
  - [Paper 3: "Synchronous vs. Asynchronous Coalitions in Multiplayer Games" (Babyak et al., 2024)](#paper-3-synchronous-vs-asynchronous-coalitions-in-multiplayer-games-babyak-et-al-2024)
  - [Day 2: Contribution Design Integration + Publication Targeting](#day-2-contribution-design-integration-publication-targeting)
  - [Paper 4: "Human-Level Performance in No-Press Diplomacy" (Bakhtin et al., 2022 — CICERO precursor / piKL regularization)](#paper-4-human-level-performance-in-no-press-diplomacy-bakhtin-et-al-2022-cicero-precursor-pikl-regularization)
  - [Paper 5: "Evaluating Agents using Social Choice Theory" (Lanctot et al., 2023/2025 — VasE)](#paper-5-evaluating-agents-using-social-choice-theory-lanctot-et-al-20232025-vase)
  - [Reading: Recent PhD Dissertations (for structure and scope calibration)](#reading-recent-phd-dissertations-for-structure-and-scope-calibration)
- [Phase 4: Implementation (4 days)](#phase-4-implementation-4-days)
  - [Day 1: Contribution Design Documents](#day-1-contribution-design-documents)
  - [Day 2: Publication Pipeline Design](#day-2-publication-pipeline-design)
  - [Day 3: Experiment Design Specification](#day-3-experiment-design-specification)
  - [Day 4: November Deliverables Specification](#day-4-november-deliverables-specification)
- [Phase 5: Consolidation (2 days)](#phase-5-consolidation-2-days)
  - [Day 1: The Complete Research Frontier Map](#day-1-the-complete-research-frontier-map)
  - [Day 2: Final Consolidation](#day-2-final-consolidation)
- [Exit Checklist](#exit-checklist)
  - [Knowledge Gates](#knowledge-gates)
  - [Deliverables Gates](#deliverables-gates)
  - [Process Gates](#process-gates)
  - [Ready-for-Research Gates](#ready-for-research-gates)

## Phase 1: Intuition (1 day)

The goal: understand what "research frontier mapping" MEANS as a practical activity (not just "read more papers"), WHY contribution design must happen BEFORE experiments (the contribution shapes the experiment, not the reverse), and HOW the 14 prior steps converge into three specific thesis contributions that are defensible, publishable, and career-relevant.

End of day: you should be able to explain to a non-expert: "I've spent 6 months studying how AI agents play games — from simple card games to multiplayer free-for-all competitions. I now know three things the field hasn't solved yet: (1) How to automatically detect and adapt to HOW a specific opponent plays, not just that they play well or badly, but their specific style — from their actual actions during the game. (2) How to exploit opponents who play sub-optimally WITHOUT losing your safety guarantee — and critically, how to do this when there are MORE THAN TWO players at the table, which breaks ALL existing theory. (3) How to rigorously EVALUATE whether an AI agent is actually good — not just 'it won more games' but a principled framework that works across different games and opponent types. My PhD will attack these three gaps. By the end of today, I'll have a map of exactly where each gap sits in the research landscape, what's already been tried, what hasn't, and what my first experiments should be."

### Talks and Overviews

- **Stanford CS224R — Lecture 1: Class Intro + MDPs (Spring 2025)**  
  https://www.youtube.com/watch?v=EvHRQhMX7_w  
  Duration: ~53m | Instructor: Chelsea Finn (Stanford)  
  *"Why study deep RL?" — a field overview of where deep reinforcement learning stands today, what problems remain open, and the landscape of current research directions.*

- **Stanford CS230 — Lecture 1: Introduction to Deep Learning (Autumn 2025)**  
  https://www.youtube.com/watch?v=_NLHFoVNlbg  
  Duration: ~1h | Instructor: Andrew Ng (Stanford)  
  *Andrew Ng's perspective on where deep learning is heading: current capabilities, limitations, and frontier research directions. Broad context for positioning the thesis within the AI landscape.*

- **Parables on the Power of Planning in AI: From Poker to Diplomacy**  
  https://www.youtube.com/watch?v=eaAonE58sLU  
  Duration: ~57m | Speaker: Noam Brown (OpenAI) | Channel: Paul G. Allen School  
  *The broadest game AI overview available: the full trajectory from poker to Go to Diplomacy. Brown identifies open problems including N-player safety, opponent modeling, and real-time adaptation — directly adjacent to all three thesis contributions.*

### Blog Posts / Accessible Reads

- **BAIR Blog / AI Blogs — "Looking Back at Game-Playing AI"**  
  Search: "game playing AI research frontier blog 2024 2025"  
  *Any recent retrospective on game AI post-CICERO. Look for identification of open problems, unresolved challenges, and new directions.*

- **Your own 13 one-pagers from Steps 2–14**  
  **Re-read ALL of them sequentially.** This is the single most valuable intuition exercise: seeing the through-line from CFR basics (Step 2) through evaluation frameworks (Step 14). Mark in the margin of each: "Contribution #1 / #2 / #3" — which contribution does this step's open question feed? Some will feed multiple.

---

## Phase 2: Exploration (1 day)

### 🎮 Interactive Exploration
- **[OpenAI Gym / Farama Gymnasium](https://gymnasium.farama.org/)** — Browse the frontier of standardized RL environments where current models are being pushed to their limits.


No new implementations. Instead, this exploration phase is about MAPPING — visually organizing everything you know into a structured research landscape.

### Activity 1: Build the Frontier Map (half day)

Create a large visual map (draw.io, Miro, or even paper + photograph) with three columns:

```
┌──────────────────────┬──────────────────────┬──────────────────────┐
│  CONTRIBUTION #1     │  CONTRIBUTION #2     │  CONTRIBUTION #3     │
│  Behavioral          │  Multi-Agent Safe    │  Evaluation          │
│  Adaptation          │  Exploitation        │  Methodology         │
│  Framework           │  (N-player)          │                      │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ [WHAT EXISTS]        │ [WHAT EXISTS]        │ [WHAT EXISTS]        │
│ • Southey 2005       │ • Ganzfried 2015     │ • Elo (ubiquitous)   │
│ • Bard 2013          │ • Liu 2022           │ • α-Rank (2019)      │
│ • player2vec 2024    │ • Jeary 2023         │ • VasE (2023/2025)   │
│ • Decision Transf.   │ • OX-Search 2024     │ • AIVAT (2019)       │
│ • BC/Offline RL      │ • ABD (Milec 2025)   │ • ISMCTS-BR (2022)   │
│ • piKL (Diplomacy)   │ • Equal Share 2024   │ • Spinning top (2019)│
│                      │ • Pluribus meta-alg  │ • EGTA (2018)        │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ [THE GAP]            │ [THE GAP]            │ [THE GAP]            │
│ ❌ No unified        │ ❌ ALL safe exploit  │ ❌ No framework      │
│   framework for      │   is 2-player        │   combines exploit-  │
│   detect → adapt     │   zero-sum           │   ability + ranking  │
│   (papers do one,    │ ❌ Minimax theorem   │   + confidence       │
│   not both)          │   fails N>2          │ ❌ No cross-game     │
│ ❌ Static detection  │ ❌ "Equal share" is  │   validation         │
│   only — no temporal │   NEW, no           │ ❌ N-player eval     │
│   adaptation         │   exploitation on    │   needs coalition-   │
│ ❌ Not cross-game;   │   top of it          │   aware metrics      │
│   poker-specific     │ ❌ Coalition dynamics│ ❌ Scaling: O(n²)    │
│                      │   unstudied          │   full payoff matrix │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ [MY THESIS FILLS]    │ [MY THESIS FILLS]    │ [MY THESIS FILLS]    │
│ • player2vec →       │ • Equal share as     │ • Three-layer        │
│   BC → Bayesian      │   safety baseline    │   framework          │
│   update cycle       │ • piKL-style safety  │ • Applied to Kuhn,   │
│ • Cross-game:        │   for N-player       │   Leduc, SLS,        │
│   Kuhn→Leduc→SLS→    │ • Coalition-aware    │   Playtech           │
│   Playtech           │   safe exploitation  │ • Coalition-aware    │
│ • Temporal: detect   │ • Tested on SLS      │   exploitability     │
│   SHIFTS in style    │   (dynamic coalitns) │ • VasE + α-Rank      │
│                      │ • Tested on poker    │   comparison         │
│                      │   (Playtech data)    │ • AIVAT integration  │
└──────────────────────┴──────────────────────┴──────────────────────┘
```

For each cell, annotate with **Step numbers** that provided the knowledge. This traces the full learning path to each contribution.

### Activity 2: Gap Validation (half day)

For each of the three gaps, attempt to DISPROVE it:
1. **Search Google Scholar** for any paper that fills the gap. Use queries like:
   - "behavioral adaptation framework imperfect information games"
   - "safe exploitation N-player multiplayer"
   - "evaluation framework cross-game multi-agent"
2. **Search recent conference proceedings** (NeurIPS 2025, ICML 2025, ICLR 2025/2026, AAAI 2026):
   - Check the accepted paper lists for any title matching the three contribution areas
3. **Check recent PhD dissertations** in the field:
   - Search Google Scholar: "dissertation" + "imperfect information game" + "opponent modeling" / "safe exploitation" / "evaluation"
   - Look at recent graduates from CMU (Sandholm/Brown group), DeepMind (Lanctot/Tuyls group), MILA, Alberta (Bowling group)
4. **Check Semantic Scholar** for citation chains from key papers:
   - Who cited OX-Search (Ge 2024)? Anyone extending to N-player?
   - Who cited Ge et al. "Equal Share" (2024)? Anyone combining with exploitation?
   - Who cited Lanctot VasE (2023)? Anyone applying cross-game?

Document findings in a **Gap Validation Log**: for each gap, either "CONFIRMED — no existing work fills this" or "PARTIALLY FILLED BY [paper] — need to refine the contribution."

The goal is NOT to be surprised during the PhD. If someone has already done what you plan to do, you want to know NOW, in October 2026, not in 2028 when you're writing up.

---

## Phase 3: Targeted Reading (2 days)

This reading phase is DIFFERENT from all prior steps. You are not learning a new algorithm — you are reading for POSITIONING. Every paper is read with the question: "Where does my work fit relative to this?"

### Day 1: Contribution #2 Anchoring (the thesis centerpiece)

Contribution #2 (Multi-Agent Safe Exploitation) is the strongest thesis differentiator — it addresses an explicitly stated open problem with no prior attempts. Day 1 focuses on solidifying the reading base.

### Paper 1: "Securing Equal Share: A Principled Approach for Learning Multiplayer Symmetric Games" (Ge, Wang, Li & Jin, 2024)
Link: [arXiv:2406.04201](https://arxiv.org/abs/2406.04201)
```
├── READ:  Sections 1 (Introduction), 3 (Main Results), 4 (Algorithms), 5 (Experiments)
│          The algorithms section is critical: understand what "equal share" means formally 
│          (expected payoff ≥ C/n - ε in n-player symmetric constant-sum game with total 
│          payoff C). Understand the no-regret construction.
├── SKIM:  Section 2 (Preliminaries — much already known from Steps 2, 9), 
│          Section 6 (Lower bounds — skim for what's NOT achievable)
├── SKIP:  Appendix proofs (use for reference, not study)
├── MATH:  Theorem 1 (conditions for equal share tractability) matters — study the 
│          CONDITIONS, not the full proof. WHY: the conditions tell you exactly WHICH 
│          N-player games your thesis can claim safe exploitation for. If SLS satisfies 
│          the conditions, your thesis testbed is validated. If it doesn't, you need 
│          to prove it separately or choose a different testbed.
└── KEY INSIGHT: "In N-player games, Nash equilibria are non-unique and provide NO 
    exploitation guarantee. The natural safety baseline is 'equal share' — securing 
    at least your fair share of the total pot. This replaces minimax value as the 
    safety benchmark when N > 2."
```
**PhD Connection:** This paper provides the FORMAL OBJECTIVE for Contribution #2. Where OX-Search defined "adaptation safety" for 2 players, Ge et al. define "equal share" for N players. Your thesis contribution is the BRIDGE: safe opponent exploitation that guarantees at least equal share while exploiting sub-optimal opponents.

### Paper 2: "Safe and Robust Subgame Exploitation in Imperfect Information Games" (Ge, Kovařík & Lisý, 2024 — OX-Search)
Link: [arXiv:2405.XXXXX](https://arxiv.org/abs/2405.15999) *(re-read from Step 8)*
```
├── RE-READ:  Section 6 (Discussion/Limitations) — with fresh eyes from equal share
│             Look specifically for: what prevents extension to N-player?
│             What assumptions require 2-player zero-sum?
├── SKIM:  Section 4 (Adaptation Safety definition) — refresh the formal definition
├── KEY QUESTION: Can adaptation safety be redefined as "equal share safety"?
│               i.e., "the exploiting strategy never does worse than C/n" 
│               instead of "never does worse than Nash"?
└── KEY INSIGHT: Adaptation safety requires a BASELINE value that defines "safe."
    In 2-player zero-sum → minimax value. In N-player → equal share (Ge 2024).
    The adaptation safety MECHANISM (RNR, subgame re-solving) may transfer if 
    the baseline is redefined. This is the thesis contribution.
```

### Paper 3: "Synchronous vs. Asynchronous Coalitions in Multiplayer Games" (Babyak et al., 2024)
Link: [arXiv:2412.19855](https://arxiv.org/abs/2412.19855)
```
├── READ:  Introduction + Section 2 (the three values: Nash / async optimal / sync optimal)
│          Key result: asynchronous coalition optimization is NONCONVEX.
├── SKIM:  Sections 3-4 (RPS and Guts poker examples) — for intuition
├── SKIP:  Technical proofs (use the results, not the machinery)
├── KEY INSIGHT: "Coalition quality depends on COMMUNICATION level, not just coalition 
    membership. Full communication (synchronous) strictly dominates partial communication 
    (asynchronous) which dominates no coalition (Nash). The safe exploitation guarantee 
    must specify which coalition model applies."
└── PhD Connection: In online poker (Playtech), colluding players have imperfect 
    communication (they can see each other's actions but can't perfectly coordinate 
    pre-game). This is EXACTLY the asynchronous coalition model. The thesis can 
    formalize collusion detection as: "is this player pair achieving above-Nash 
    payoff consistent with asynchronous coalition play?"
```

### Day 2: Contribution Design Integration + Publication Targeting

### Paper 4: "Human-Level Performance in No-Press Diplomacy" (Bakhtin et al., 2022 — CICERO precursor / piKL regularization)
Re-read from Step 11 context. Focus on: piKL policy regularization as behavioral safety constraint in N-player games.
```
├── RE-READ:  piKL section — how Bakhtin constrains the policy to not deviate too 
│             far from a "human-like" baseline. This is a BEHAVIORAL safety 
│             constraint, not a game-theoretic one.
├── KEY INSIGHT: When game-theoretic safety (minimax, Nash) fails in N-player, 
│   BEHAVIORAL safety ("don't deviate too far from a known-good policy") provides 
│   an alternative guarantee. piKL regularization ensures the exploiting policy 
│   stays within a KL-divergence ball of the Nash policy.
└── PhD Connection: piKL could be the MECHANISM for Contribution #2.
    Instead of proving minimax-style safety (impossible in N-player),
    constrain deviation from the equal share policy via KL regularization.
    This gives a tractable safety guarantee with tunable aggressiveness.
```

### Paper 5: "Evaluating Agents using Social Choice Theory" (Lanctot et al., 2023/2025 — VasE)
Re-read from Step 14. Focus on: evaluation as a research contribution — how Lanctot frames methodology work as publishable science.
```
├── RE-READ:  Introduction (for framing) + Section 5 (experimental validation)
├── KEY QUESTION: How did Lanctot make an "evaluation paper" publishable at a top venue?
│   Answer: (1) axiomatically grounded — shows VasE satisfies specific mathematical 
│   axioms, (2) compared against all alternatives on the same data, (3) showed 
│   surprising failures of existing methods (Elo fails on specific games).
└── PhD Connection: Contribution #3 must follow the same pattern:
    (1) Axiomatic grounding for the three-layer framework
    (2) Head-to-head comparison of evaluation methods
    (3) Surprising result — e.g., "evaluation using VasE reveals that Agent X, 
    ranked #1 by Elo, is actually dominated in a cyclic component — it's only 
    'best' because it beats common opponents, not because it's strategically strong."
```

### Reading: Recent PhD Dissertations (for structure and scope calibration)

Skim the table of contents and contribution chapters of 2–3 recent dissertations from the field. Don't read fully — look at SCOPE (how many contributions? how deep? what constitutes a "contribution"?) and STRUCTURE (chapter organization):

- **Michael Bowling group (Alberta):** Search Google Scholar for recent dissertations by students working on poker AI / game solving (e.g., Dustin Morrill, Ryan D'Orazio, Marc Lanctot's earlier work)
- **Tuomas Sandholm group (CMU):** Search for dissertations on safe exploitation, game abstraction (e.g., Noam Brown's thesis if accessible — it covers Libratus + Pluribus)
- **Karl Tuyls group (DeepMind → Liverpool):** Evaluation-focused dissertations, α-Rank related

**What to extract from each dissertation:**
1. How many contributions? (Typically 2–4)
2. How deep is each? (One paper per contribution? Multiple papers?)
3. How are contributions connected? (Sequential? Parallel? Unified framework?)
4. What's the evaluation strategy? (One game? Multiple games? Real-world data?)
5. How long was the PhD? (Typically 3–5 years)

This calibrates your expectations: your 3 contributions with 4 experimental domains (Kuhn, Leduc, SLS, Playtech) is AMBITIOUS for a 3-year PhD. You may need to scope down (drop one domain or one contribution) — better to know this now.

---

## Phase 4: Implementation (4 days)

This is not a coding phase in the traditional sense. The "implementation" for the capstone step produces the PLANNING DOCUMENTS that guide the entire PhD research phase (November 2026 → 2029). These documents are the deliverables.

### Day 1: Contribution Design Documents

For each of the three contributions, write a structured design document (2–3 pages each):

#### Contribution #1 Design Document: Behavioral Adaptation Framework
🟡 AI-ASSISTED — AI can help draft structure; you fill in the precise technical content from Steps 7, 12, 13.

| Section | Content |
|---------|---------|
| **Problem Statement** | Given: sequence of observed actions from an opponent in an imperfect-information game. Goal: (i) infer the opponent's strategy type in real-time, (ii) adapt exploitation strategy accordingly, (iii) maintain safety guarantee during adaptation. |
| **Prior Art** | Bayesian opponent model (Southey 2005), handrange inference (Bard 2013), player2vec embeddings (Wang 2024), behavioral cloning from action sequences (Step 13), piKL regularization (Bakhtin 2022). |
| **The Gap** | No existing work provides a UNIFIED detect→adapt→evaluate pipeline: detection papers stop at classification, exploitation papers assume known opponent type, evaluation papers measure after-the-fact. The thesis proposes a CLOSED LOOP: observe → infer type → select exploitation strategy → evaluate outcome → update inference. |
| **Proposed Method** | Phase 1: player2vec embedding (from game histories) → opponent type posterior. Phase 2: Strategy selection conditioned on type posterior (mixture of pre-computed exploitation strategies). Phase 3: Online Bayesian update of type posterior from match outcomes. Phase 4: Evaluate via three-layer framework (Contribution #3). |
| **Experimental Plan** | Testbeds: Kuhn (proof-of-concept), Leduc (scaling), Playtech data (real-world). Opponent pool: bot zoo from Step 14. Metrics: adaptation speed (hands to correct classification), exploitation gain (mbb/hand above Nash baseline), safety (never worse than Nash vs adversarial opponents). |
| **Expected Publications** | (1) Workshop/poster: "Real-Time Opponent Type Inference in Poker via Behavioral Embeddings" (NeurIPS workshops, AAAI workshop). (2) Full paper: "Adaptive Strategy Selection in Imperfect-Information Games: A Closed-Loop Framework" (AAMAS, AAAI main). |
| **PhD Timeline Fit** | Chapter II (theoretical research, deadline 04.2027): the framework design + Kuhn/Leduc experiments. Chapter III (practical solving, deadline 01.2028): Playtech data experiments + full pipeline. |
| **Risk Assessment** | Low risk: Kuhn/Leduc experiments are straightforward. Medium risk: Playtech data quality (collusion labeling). Mitigation: synthetic ground truth via injected colluders. |

#### Contribution #2 Design Document: Multi-Agent Safe Exploitation
🔴 HAND-CODE the design — this is the thesis centerpiece. Every word must be yours.

| Section | Content |
|---------|---------|
| **Problem Statement** | Given: N-player imperfect-information game (N > 2). A safety baseline strategy exists (e.g., equal share policy from Ge 2024). Problem: exploit sub-optimal opponents while guaranteeing expected payoff ≥ C/n - ε (equal share minus tolerance). Challenge: minimax theorem fails for N > 2; Nash equilibria are non-unique and non-exploitable; coalition dynamics create non-stationary opponent distributions. |
| **Prior Art** | Safe exploitation: Ganzfried & Sandholm (2015), Liu et al. (2022), Jeary & Turrini (2023), Ge et al. OX-Search (2024), Milec et al. ABD (2025). All 2-player zero-sum. N-player safety: Ge et al. Equal Share (2024) — defines the objective but doesn't provide exploitation. Coalition dynamics: Babyak et al. (2024) — formalizes communication levels. Behavioral safety: Bakhtin et al. piKL (2022) — KL-constrained policies in Diplomacy. |
| **The Gap** | NO existing work combines safe exploitation with N-player settings. The "equal share" paper defines WHAT to guarantee but not HOW to exploit. The OX-Search paper defines HOW to exploit but only for N=2. The thesis fills the gap at the intersection: safe exploitation that guarantees equal share in N-player games. |
| **Proposed Method** | Approach 1 (conservative): piKL-regularized exploitation. Start from equal share policy, allow exploitation deviation bounded by KL divergence. The KL budget is the "safety knob" — more KL = more exploitation risk but potentially more gain. Approach 2 (ambitious): Adaptation safety redefined for N-player. Replace minimax value with equal share value in the RNR framework from OX-Search. Prove (or conjecture + validate empirically) that the resulting strategy guarantees equal share. Approach 3 (pragmatic): Population-based safety. Train exploitation policy against a population of opponents (PBT from Step 10), then evaluate worst-case performance across the population. If worst-case ≥ equal share, declare "population-safe." |
| **Experimental Plan** | Testbeds: (1) 3-player Kuhn Poker (small enough for exact analysis), (2) 3-player Leduc Poker (medium complexity), (3) So Long Sucker (4-player with dynamic coalitions — Step 11 testbed). Metrics: (a) Exploitation gain vs. sub-optimal opponents (mbb/hand above equal share), (b) Safety: worst-case payoff vs. adversarial opponents (must be ≥ C/n - ε), (c) Adaptation speed: hands required to achieve positive exploitation, (d) Coalition robustness: exploitation maintains safety even when other players form coalitions. |
| **Expected Publications** | (1) Full paper (flagship): "Safe Exploitation in Multiplayer Games: Guaranteeing Equal Share While Adapting to Opponents" (NeurIPS, ICML, or AAAI main track). This is THE thesis paper. (2) Supporting paper: "Coalition-Aware Safe Exploitation in Free-For-All Games" (AAMAS or game theory conference). (3) Workshop paper: "Extending Adaptation Safety from Two-Player to N-Player Imperfect-Information Games" (NeurIPS workshops — GFAI, MARL workshop). |
| **PhD Timeline Fit** | Chapter II (deadline 04.2027): Formal framework + 3-player Kuhn analysis. Chapter III (deadline 01.2028): Leduc + SLS experiments. Chapter IV (deadline 08.2028): Playtech data + full evaluation via Contribution #3. |
| **Risk Assessment** | High risk: proving formal guarantees (may need to settle for empirical validation). Medium risk: SLS testbed complexity (dynamic coalitions are hard to control). Mitigation: use 3-player Kuhn as proof-of-concept (small enough for exhaustive analysis). If formal proofs fail, pivot to empirical contribution: "we show empirically that piKL-regularized exploitation maintains equal share in N-player poker." |
| **Scope Decision** | If formal guarantees are achievable → Approach 2 (strongest contribution). If only empirical results → Approach 1 (piKL) as primary, with Approach 3 (population-based) as validation. Decision point: by end of Chapter II (04.2027). |

#### Contribution #3 Design Document: Evaluation Methodology
🟡 AI-ASSISTED — the framework design already exists from Step 14; this structures it for publication.

| Section | Content |
|---------|---------|
| **Problem Statement** | Given: a set of AI agents for an imperfect-information game. Goal: produce a comprehensive evaluation that answers: (1) How exploitable is each agent? (2) How do they rank against each other? (3) How confident are these measurements? No existing framework combines all three answers. |
| **Prior Art** | Exploitability: exact (Kuhn/Leduc), approximate ISMCTS-BR (Timbers 2022), ApproxED (Martin 2025). Ranking: Elo (ubiquitous), α-Rank (Omidshafiei 2019), VasE (Lanctot 2025), Nash averaging, spinning top (Balduzzi 2019). Confidence: AIVAT (Burch 2019), sample complexity for α-Rank (Rowland 2019). |
| **The Gap** | (1) No existing framework integrates all three layers. Papers present individual metrics, not a unified pipeline. (2) No cross-game validation: exploitability is computed for one game, ranking for another, confidence for a third. (3) N-player evaluation needs coalition-aware metrics (from Step 14 confusions). |
| **Proposed Method** | The three-layer evaluation framework from Step 14, enhanced with: (a) Cross-game consistency analysis (apply same framework to Kuhn, Leduc, SLS, Playtech → check if agent rankings are consistent across games → generalization evidence), (b) Coalition-aware exploitability for N-player (marginal exploitability conditioned on coalition structures from Step 11), (c) VasE + α-Rank comparison with spinning top diagnostic (identify when and why they disagree). |
| **Experimental Plan** | Apply the full framework to: (1) Kuhn poker (exact ground truth available — validation), (2) Leduc poker (medium — approximate methods needed), (3) SLS (N-player coalition game), (4) Playtech data (real-world, noisy). Compare framework with existing approaches: "what insights does the three-layer framework provide that Elo alone misses? That α-Rank alone misses?" |
| **Expected Publications** | (1) Full paper: "A Three-Layer Evaluation Framework for Multi-Agent Imperfect-Information Games" (AAMAS or JAIR). (2) Combined with Contribution #1 data: "Evaluating Adaptive Agents in Poker: Exploitability, Ranking, and Confidence Across Game Variants" (could target IEEE TNNLS or similar journal). |
| **PhD Timeline Fit** | Chapter I (deadline 11.2026): Framework design + Kuhn/Leduc results (FIRST PUBLICATION). Chapter IV (deadline 08.2028): Cross-game analysis + full experimental evaluation. |
| **Risk Assessment** | Low risk: the framework components already work from Step 14. The risk is in NOVELTY — "just combining existing metrics" may not be considered a sufficient contribution. Mitigation: the novelty is in (a) cross-game validation — no one has applied the same framework to 4 different game types, (b) coalition-aware exploitability — genuinely new metric, (c) surprising diagnostic insights from VasE vs α-Rank disagreement. |

### Day 2: Publication Pipeline Design

Create the **Publication Pipeline** — a 4-column table mapping each dissertation chapter to publications:

🟡 AI-ASSISTED — AI can format the table; you fill in the content from the contribution design documents.

```
┌─────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│ DEADLINE             │ CHAPTER              │ PUBLICATION TARGET   │ CONTENT SOURCE       │
├─────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ 11.2026              │ Chapter I:           │ Pub 1: Workshop or   │ Contribution #3:     │
│ (Step 15 + buffer)   │ State of the Art     │ short paper at       │ Three-layer          │
│                      │ + Problem Analysis   │ AAAI-26 workshop /   │ evaluation framework │
│                      │                      │ NeurIPS-26 workshop  │ on Kuhn + Leduc.     │
│                      │                      │ / AAMAS-27 poster    │ Derived from Steps   │
│                      │                      │                      │ 14 + 15 code.        │
├─────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ 04.2027              │ Chapter II:          │ Pub 2: Full paper at │ Contribution #2:     │
│                      │ Theoretical          │ AAMAS-27 or AAAI-28  │ N-player safe        │
│                      │ Research             │ (submit ~12.2026)    │ exploitation formal  │
│                      │                      │                      │ framework + 3-player │
│                      │                      │ Pub 3: Workshop at   │ Kuhn/Leduc results.  │
│                      │                      │ NeurIPS-27 / ICML-27 │ Contribution #1:     │
│                      │                      │                      │ Behavioral adaptation│
│                      │                      │                      │ on Kuhn + Leduc.     │
├─────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ 01.2028              │ Chapter III:         │ Pub 4: Full paper at │ Contribution #1 +    │
│                      │ Practical Problem    │ NeurIPS-28 / ICML-28 │ Contribution #2:     │
│                      │ Solving              │ (submit ~05.2027)    │ Full pipeline on     │
│                      │                      │                      │ SLS + Playtech data. │
│                      │                      │ Pub 5: Industry/     │ Contribution #1:     │
│                      │                      │ applied (IEEE, ACM)  │ Playtech behavioral  │
│                      │                      │                      │ analysis + collusion.│
├─────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ 08.2028              │ Chapter IV:          │ Pub 6: Journal paper │ All Contributions:   │
│                      │ Experimental         │ (JAIR, AIJ, or       │ Cross-game unified   │
│                      │ Research             │ IEEE TNNLS)          │ evaluation. Complete  │
│                      │                      │ (submit ~02.2028)    │ experimental results.│
├─────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ 09.2028              │ General conclusions  │ (covered by pubs)    │ Synthesis of all     │
│                      │ and contributions    │                      │ contributions.       │
├─────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ 04.2029              │ Defense              │ 4-6 total pubs       │ Full dissertation.   │
│                      │                      │ (3 min for defense)  │                      │
└─────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
```

**Publication venue research:** For each target venue, note:
- Submission deadline (approximate annual cycle)
- Acceptance rate (to calibrate expectations)
- Typical paper length
- Whether the venue has published similar work (search proceedings for keywords)

### Day 3: Experiment Design Specification

For each proposed experiment across the three contributions, write a mini-specification:

🔴 HAND-CODE — experiment design is a core research skill. These specs ARE the PhD research plan.

#### Experiment 1.1: Behavioral Adaptation on Kuhn Poker
```
Hypothesis: player2vec embeddings + Bayesian type inference can classify opponent 
            types (from Step 14 bot zoo) within 50 hands with >80% accuracy.
Independent variable: Number of observed hands (10, 25, 50, 100, 200).
Dependent variables: 
  - Classification accuracy (type inference vs ground truth)
  - Exploitation gain (mbb/hand above Nash baseline)
  - Safety (worst-case mbb/hand vs adversarial opponent)
Agents: 7+ Kuhn bot zoo from Step 14 (trivial, heuristic, computed, advanced tiers).
Protocol: 
  1. For each agent pair (adaptive agent vs opponent): play 10,000 hands.
  2. Every N hands, record: inferred type posterior, selected strategy, mbb/hand so far.
  3. Repeat for all opponents and all observation windows.
Baselines: 
  - Static Nash (no adaptation — floor)
  - Oracle (knows opponent type — ceiling)
  - Random adaptation (picks exploitation strategy uniformly)
Evaluation: Three-layer framework from Step 14 (exploitability + ranking + AIVAT confidence).
Expected result: Adaptation converges to near-oracle performance by 100 hands for 
                 heuristic opponents, slower for advanced opponents.
```

#### Experiment 2.1: N-Player Safe Exploitation on 3-Player Kuhn
```
Hypothesis: piKL-regularized exploitation can achieve payoff > C/3 against sub-optimal 
            opponents while maintaining payoff ≥ C/3 - ε against adversarial opponents.
Independent variable: KL budget (0.01, 0.1, 0.5, 1.0, 5.0).
Dependent variables:
  - Exploitation gain vs sub-optimal opponents (vs equal share baseline)
  - Worst-case payoff vs adversarial opponents (must be ≥ C/3 - ε)
  - The Pareto frontier of exploitation gain vs safety loss
Agents: 
  - Player 1: piKL-regulated adaptive agent (our method)
  - Players 2-3: varied — all-sub-optimal, one-adversarial, both-adversarial
Game: 3-player Kuhn Poker (small enough for exact computation of equal share value)
Protocol:
  1. Compute equal share value for 3-player Kuhn (exact).
  2. Compute piKL-exploiting policy for each KL budget.
  3. For each (KL budget, opponent configuration): play 100,000 hands.
  4. Measure exploitation gain and worst-case safety.
Baselines:
  - Equal share policy (safety floor)
  - Unrestricted best response to estimated opponents (maximum exploitation, no safety)
  - 2-player safe exploitation (Ganzfried 2015) applied to 3-player (to show it fails)
Evaluation: Exploitation-safety Pareto curve + three-layer framework.
Expected result: piKL with moderate KL budget achieves significant exploitation gain 
                 while maintaining safe payoff. 2-player methods fail to maintain safety.
```

#### Experiment 2.2: Coalition-Aware Safe Exploitation on SLS
```
Hypothesis: Safe exploitation that accounts for coalition dynamics (help/harm matrices 
            from Step 11) outperforms coalition-unaware safe exploitation in SLS.
Independent variable: Coalition awareness model (none, static, dynamic).
Dependent variables:
  - Win rate (SLS has a single winner — the clearest metric)
  - Exploitation-safety tradeoff (payoff distribution across coalition configurations)
  - Coalition formation frequency (does the safe agent get targeted?)
Game: "So Long Sucker" (4 players, dynamic coalition formation)
Protocol:
  1. Deploy 4 agents: 1 adaptive (ours), 3 varied (random, heuristic, RL-trained from Step 11).
  2. Run 10,000 games for each configuration.
  3. Track: coalition formation events, betrayal timing, win distribution.
Baselines:
  - Static Nash approximation (from Step 11 RL training)
  - piKL without coalition awareness
  - Random strategy
Evaluation: Win rate + help/harm matrix analysis + three-layer framework.
Expected result: Coalition-aware method exploits opponents while avoiding being 
                 consistently targeted for elimination.
```

#### Experiment 3.1: Cross-Game Evaluation Framework Validation
```
Hypothesis: The three-layer evaluation framework produces consistent agent rankings 
            across Kuhn, Leduc, and SLS, AND reveals insights that single-metric 
            evaluation (Elo alone) misses.
Independent variable: Game type, evaluation metric used.
Dependent variables:
  - Agent rankings under each metric and game
  - Rank correlation between metrics (Elo vs α-Rank vs VasE)
  - Spinning top decomposition (transitive vs cyclic fraction per game)
  - Cross-game rank stability (does agent X rank similarly in Kuhn and Leduc?)
Games: Kuhn, Leduc, SLS.
Agents: Full bot zoo for each game (from Step 14).
Protocol:
  1. For each game: run full round-robin tournament (all agent pairs).
  2. Compute: exploitability (Layer 1), Elo + α-Rank + VasE (Layer 2), AIVAT confidence (Layer 3).
  3. Generate spinning top decomposition for each game.
  4. Compare rankings across games and metrics.
Baselines: 
  - Elo alone (the standard — show what it misses)
  - α-Rank alone (show what VasE adds)
Evaluation: Framework meta-evaluation — does the framework ITSELF provide actionable insights?
Expected result: (1) Elo fails for SLS (intransitive dynamics), (2) VasE detects cycles 
                 that α-Rank smooths over, (3) cross-game analysis reveals which agent 
                 DESIGNS generalize (not just which agents win in one game).
```

### Day 4: November Deliverables Specification

The October 15 → November deadline is the FIRST PhD milestone: Chapter I + first publication draft. Day 4 creates the precise plan for what gets written:

🟡 AI-ASSISTED — AI can help with outline structure; technical content is yours.

#### Chapter I Outline (25–30 pages target, per ind_plan_A_Andreev_EN.md)

```
Chapter I: Analysis of the State of the Problem
  "Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments"

1.1 Introduction (2 pages)
    - Motivation: Why adaptive strategy in multi-agent games matters
    - Scope: imperfect-information games as testbed for general multi-agent strategy
    - The three research questions (mapped to contributions)

1.2 Foundations (4 pages)
    - Game theory prerequisites: extensive-form games, Nash equilibrium, CFR (Steps 2-3)
    - RL prerequisites: policy optimization, convergence (Steps 1, 5)
    - The bridge: Deep CFR, DREAM, ReBeL, Student of Games (Steps 5-6)

1.3 Opponent Modeling and Behavioral Adaptation (5 pages) [→ Contribution #1]
    - Bayesian opponent models (Southey 2005, Bard 2013) (Step 7)
    - Modern behavioral inference (player2vec 2024, BC, Offline RL) (Steps 12-13)
    - Online adaptation: from detection to exploitation (Step 7-8)
    - Gap: no unified detect→adapt→evaluate pipeline

1.4 Safe Exploitation in Imperfect-Information Games (6 pages) [→ Contribution #2]
    - The SOE lineage: Ganzfried→Liu→Jeary→OX-Search (Step 8)
    - Adaptation safety: not losing while exploiting (Step 8)
    - The N-player gap: minimax fails, Nash is non-unique (Steps 9, 11)
    - Equal share: a new safety objective for multiplayer (Ge 2024) [NEW]
    - Coalition dynamics and their impact on exploitation (Steps 11, Babyak 2024) [NEW]
    - Gap: NO safe exploitation for N>2

1.5 Evaluation of Multi-Agent Game AI (5 pages) [→ Contribution #3]
    - Single-agent metrics: exploitability, approximate exploitability (Steps 3, 8, 14)
    - Population metrics: Elo, α-Rank, Nash averaging, VasE (Steps 10, 14)
    - Variance reduction: AIVAT (Step 14)
    - Gap: no unified cross-game framework

1.6 Research Questions and Proposed Contributions (3 pages)
    - RQ1: How can opponent strategy be inferred and adapted to in real-time?
    - RQ2: How can safe exploitation guarantees extend to N-player games?
    - RQ3: How can agent evaluation be unified across diverse game types?
    - The three expected contributions (refined from planArchitecture.md)

1.7 Conclusion and Research Plan (2 pages)
    - Summary of gaps identified
    - Proposed methodology overview
    - Timeline (mapped to Chapters II-IV)
```

#### First Publication Draft

**Title (working):** "Evaluating Game AI Agents: A Three-Layer Framework for Exploitability, Ranking, and Confidence"

**Target venue:** NeurIPS 2026 Workshop on Game-Theoretic Approaches (or similar workshop with Jun-Sep 2026 deadline). If no suitable workshop, target AAMAS 2027 (deadline ~Oct 2026).

**Content:**
- The three-layer evaluation framework (from Step 14)
- Applied to Kuhn and Leduc bot zoos (from Step 14)
- Results: how Elo, α-Rank, VasE compare; where they disagree; spinning top diagnostic
- Short: 4–6 pages (workshop format)

**Why this first:** Contribution #3 is the LOWEST RISK publication target. The framework and experiments already exist from Step 14. It doesn't require N-player formal proofs (Contribution #2) or Playtech data access issues (Contribution #1). It establishes the evaluation methodology that ALL subsequent papers use.

---

## Phase 5: Consolidation (2 days)

### Day 1: The Complete Research Frontier Map

Finalize the frontier map from Phase 2 into a publication-quality document. This is not a deliverable to submit — it's the NAVIGATION TOOL for the next 3 years.

🔴 HAND-CODE — this map IS the PhD plan. You must own every assessment.

#### The Frontier Map Document

Structure:

```
# Research Frontier Map
## "Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments"
## Alexander Andreev — PhD, Ruse University, 2026–2029

### 1. Field Overview
[2-3 paragraphs situating the thesis in the broader landscape of game AI research]

### 2. Contribution #1: Behavioral Adaptation Framework
#### 2.1 State of the Art (what exists)
[Key papers with 1-line assessment: solved/unsolved]
#### 2.2 The Gap (what's missing)
[Precise description of the gap with evidence from literature]
#### 2.3 Proposed Approach (what the thesis does)
[Method outline]
#### 2.4 Evidence of Feasibility
[Which Steps (1-14) demonstrated components that make this feasible]
#### 2.5 Risks and Mitigation
[What could go wrong, and what the fallback is]

### 3. Contribution #2: Multi-Agent Safe Exploitation
[Same 5-subsection structure]

### 4. Contribution #3: Evaluation Methodology
[Same 5-subsection structure]

### 5. Contribution Interactions
[How the three contributions connect — Contribution #3 evaluates #1 and #2;
 Contribution #1 provides the behavioral model that #2 exploits;
 Contribution #2 extends the safety theory from 2-player (where #1 was validated)]

### 6. Publication Pipeline
[The table from Phase 4, Day 2]

### 7. Experimental Infrastructure
[What code/data already exists from Steps 1-14 that the PhD builds on]

### 8. Scope Boundaries
[What the thesis does NOT cover — explicitly bound the scope:
 - NOT: LLM-based game agents (Step 12 surveyed, not core)
 - NOT: perfect-information games (no chess, Go, etc.)
 - NOT: cooperative-only games (purely cooperative MARL is out of scope)
 - NOT: human experiments (all evaluation is agent-vs-agent)]

### 9. Career Connection
[How each contribution maps to the career targets from planArchitecture.md:
 - Contribution #1 → Fraud/Risk roles (behavioral detection)
 - Contribution #2 → MARL Architect roles (multi-agent strategy)
 - Contribution #3 → Both (evaluation is universally valued)]
```

### Day 2: Final Consolidation

#### Mandatory One-Pager

```
# Step 15 — Research Frontier Mapping + Contribution Design: One-Pager

**Problem:** After 14 steps of intensive study spanning CFR, deep game AI, opponent 
modeling, safe exploitation, multi-agent dynamics, population training, coalition 
formation, sequence models, behavioral analysis, and evaluation frameworks — how do 
these converge into a defensible, publishable PhD?

**Core Activity:** Research frontier mapping: systematically identifying what exists, 
what's missing, and what the thesis uniquely contributes. Combined with contribution 
design: specifying the precise methodology, experiments, and publication targets for 
each of three thesis contributions.

**Key Result:** Three contributions identified, validated against the literature, and 
designed with full experimental specifications:
(1) Behavioral Adaptation Framework — closed-loop detect→adapt→evaluate pipeline 
    for opponent strategy inference in imperfect-information games.
(2) Multi-Agent Safe Exploitation — extending safe exploitation guarantees from 
    2-player zero-sum to N-player using equal share as the safety objective 
    (piKL-regularized or adaptation safety redefined). THE thesis centerpiece.
(3) Evaluation Methodology — three-layer framework (exploitability + population 
    ranking + confidence) validated across 4 game types.

**My Implementation:** Contribution design documents (3 × 2-3 pages), publication 
pipeline (6 publications over 3 years), 4 experiment specifications with hypotheses 
and protocols, Chapter I outline (25-30 pages), first publication draft plan.

**Open Question:** Can formal safety guarantees (Approach 2 for Contribution #2) be 
proven for N-player games, or must the thesis settle for empirical validation 
(Approach 1)? This is the single highest-impact decision point, to be resolved by 
04.2027 (Chapter II deadline).

**PhD Connection:** This step IS the PhD launch. Everything before it was learning. 
Everything after it is research. The frontier map and contribution designs ARE the 
research plan for 2027–2029.
```

#### Learning Log Update

- **Connections:**
  - [Step 2→15] CFR's regret minimization → equal share's no-regret foundation (Ge 2024). Full circle: the first algorithm you learned (Step 2) provides the theoretical tool for the thesis's central contribution.
  - [Step 7→15] Bayesian opponent model → Contribution #1's real-time inference pipeline. Step 7's handrange inference scales up via player2vec (Step 13) into the full behavioral adaptation framework.
  - [Step 8→15] OX-Search's adaptation safety → Contribution #2's foundational mechanism. The 2-player guarantee from Step 8 is what the thesis EXTENDS to N-player.
  - [Step 8→15] Jiawei Ge is co-author of BOTH OX-Search and Equal Share. The same researcher who defined adaptation safety (2-player) also defined equal share (N-player). These are companion papers — the thesis bridges them.
  - [Step 10→15] PBT + spinning top → Contribution #3's diagnostic backbone. Population diversity from Step 10 creates the agent populations that Step 14's evaluation framework ranks.
  - [Step 11→15] SLS coalition dynamics → Contribution #2's hardest testbed. Coalition formation, betrayal, and instability in SLS are the features that make N-player safe exploitation genuinely difficult.
  - [Step 11→15] Babyak et al. (2024) formalizes sync/async coalitions → directly connects to Playtech collusion detection (asynchronous coalition model).
  - [Step 13→15] Playtech data pipeline → real-world validation for ALL three contributions. The Playtech data is the bridge between toy games and industry relevance.
  - [Step 14→15] Three-layer evaluation framework → Contribution #3, but also the MEASUREMENT TOOL for Contributions #1 and #2. You can't claim "our method works" without the evaluation framework proving it.

- **Confusions (resolved across the full 15-step journey):**
  - [Step 3] Why does external sampling converge faster in practice? → RESOLVED in [Step 5]: Deep CFR learned to approximate external sampling's value prediction.
  - [Step 5] How does DREAM handle variance from opponent sampling? → PARTIALLY RESOLVED in [Step 8]: safe exploitation provides the framework (control variance by staying close to Nash).
  - [Step 8] How does safe exploitation work in N-player? → ADDRESSED in [Step 15]: Equal Share (Ge 2024) provides the objective; piKL (Bakhtin 2022) provides the mechanism. Full resolution requires Contribution #2 research.
  - [Step 11] What does "safe" mean in FFA games? → ADDRESSED in [Step 15]: Equal share (C/n) replaces minimax value. Coalition-awareness adds another dimension. Full resolution is Contribution #2.

- **Confusions (remaining — these ARE the PhD research questions):**
  - [Step 15] Can adaptation safety be formally proven for N-player with equal share baseline? → THE central research question.
  - [Step 15] How sensitive is piKL-based safety to the KL budget in practice? Is there a principled way to set it, or is it always empirical tuning? → Experiment 2.1 resolves this.
  - [Step 15] Does the three-layer evaluation framework genuinely add insight beyond what individual metrics provide? Or is it "just" a collection? → Experiment 3.1 resolves this.
  - [Step 14] VasE vs α-Rank: when do they disagree, and what does it mean? → Experiment 3.1 provides data.
  - [Step 14] Can spinning top analysis scale beyond O(n²) full payoff matrix computation? → Open for future work / Contribution #3 extension.

#### Final Assessment: The 15-Step Journey

Summarize your readiness across the three contribution areas:

| Contribution | Knowledge State (Steps) | Code State (Steps) | Open Research (Steps) |
|---|---|---|---|
| #1: Behavioral Adaptation | Theory: 7, 12, 13. Methods: player2vec, BC, Bayesian. | Code: Step 13 pipeline + Step 14 bot zoo. | Gap: unified pipeline untested end-to-end. |
| #2: N-Player Safe Exploitation | Theory: 8, 9, 11. Methods: OX-Search, piKL, Equal Share. | Code: Step 8 safety checker + Step 11 SLS agents. | Gap: THE thesis centerpiece. No prior work. |
| #3: Evaluation Methodology | Theory: 10, 14. Methods: α-Rank, VasE, AIVAT, spinning top. | Code: Step 14 three-layer framework. | Gap: cross-game validation + novelty justification. |

**Verdict:** The 15-step learning plan has achieved its goal. You enter the research phase (November 2026) with: deep understanding of the field (14 steps), working code infrastructure (Steps 3-14 deliverables), three validated contribution gaps (Step 15 frontier map), and a publication-ready first paper (Step 14/15 evaluation framework).

---

## Exit Checklist

### Knowledge Gates
- [ ] Can explain from memory: the three thesis contributions and why each is a genuine gap
- [ ] Can explain from memory: the "equal share" objective and why it replaces minimax in N-player games
- [ ] Can explain from memory: how Contributions #1, #2, #3 connect to each other (the loop: #1 detects → #2 exploits → #3 evaluates)
- [ ] Can explain from memory: the first publication target (venue, topic, content)
- [ ] Can explain from memory: the Chapter I outline (all 7 sections)
- [ ] Can trace each contribution back to the specific steps that built it

### Deliverables Gates
- [ ] Frontier map (visual): three-column map with WHAT EXISTS / THE GAP / MY THESIS FILLS — for all three contributions
- [ ] Gap validation log: each gap verified against Google Scholar, conference proceedings, recent dissertations
- [ ] Contribution #1 design document (2-3 pages) with problem/prior art/gap/method/experiments/publications/timeline/risk
- [ ] Contribution #2 design document (2-3 pages) — 🔴 HAND-CODED
- [ ] Contribution #3 design document (2-3 pages)
- [ ] Publication pipeline table: 6 publications mapped to 4 dissertation chapters with venue/deadline/content
- [ ] Experiment specification 1.1 (Behavioral Adaptation on Kuhn) with hypothesis/IV/DV/protocol
- [ ] Experiment specification 2.1 (N-Player Safe Exploitation on 3-Player Kuhn) with hypothesis/IV/DV/protocol
- [ ] Experiment specification 2.2 (Coalition-Aware Safe Exploitation on SLS) with hypothesis/IV/DV/protocol
- [ ] Experiment specification 3.1 (Cross-Game Evaluation Framework) with hypothesis/IV/DV/protocol
- [ ] Chapter I outline (25-30 pages target, all 7 sections specified)
- [ ] First publication draft plan (title, venue, content, length)
- [ ] Research frontier map document (9 sections: overview, 3 contributions × 5 subsections each, interactions, pipeline, infrastructure, scope, career)

### Process Gates
- [ ] All 13 one-pagers from Steps 2-14 re-read and annotated with contribution labels
- [ ] All prior step confusions from Learning Log reviewed — resolved ones marked, unresolved ones transferred to PhD research questions
- [ ] One-pager written and committed
- [ ] Learning Log updated with final connections and all remaining confusions documented as research questions
- [ ] Final assessment table completed (knowledge state / code state / open research per contribution)
- [ ] Step notes committed to repo

> **[P3] Contribution #2 scope (final framing):** Ensure contribution design explicitly scopes Contribution #2 to tractable heuristics + empirical validation on small N-player games. State the non-claim (general N-player safety theorem) in the contribution summary.

> **[P4*] Contribution #3 failure-mode framing:** Contribution #3 description must reference failure-mode evidence from Step 14. The contribution is “existing evaluation breaks in these settings + our framework catches what it misses,” not “we assembled a toolkit.”

### Ready-for-Research Gates
- [ ] Can answer: "What is your first experiment?" (→ Experiment 2.1: piKL exploitation on 3-player Kuhn)
- [ ] Can answer: "What is your first publication?" (→ Evaluation framework workshop paper, NeurIPS/AAAI 2026 workshop)
- [ ] Can answer: "What is the riskiest part of your thesis?" (→ Formal safety guarantees for Contribution #2)
- [ ] Can answer: "What is your fallback if the formal proofs don't work?" (→ Empirical validation with piKL; Contributions #1 and #3 are lower-risk)
- [ ] Can answer: "Why should the committee approve this PhD?" (→ Three validated gaps, working code infrastructure, realistic publication pipeline, direct career applicability)
