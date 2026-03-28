# Plan: 14-Step PhD Preparation Roadmap + Career Alignment

**TL;DR:** A 14-step learning progression (2 done + 12 new, ~2 weeks each, April–September 2026) that builds from your completed CFR/RL foundations to cutting-edge multi-agent adaptive strategy. Generalized beyond poker per professor feedback. Anchored to a career-maximizing PhD goal. Includes an honest career review and a step structure template for content generation.

---

## 1. Career Plan Review

### Single Plan (Bulgaria B2B Strategy) — Verdict: Solid, minor adjustments

| # | Target | Verdict | Notes |
|---|--------|---------|-------|
| 1 | B2B MARL Solutions Architect | **STRONG AGREE** | Best target. PhD + 10 YOE SWE = rare. €140-220k B2B from Bulgaria is achievable. |
| 2 | iGaming/Fintech Fraud Consultant | **STRONG AGREE** | Natural evolution from Playtech. PhD maps directly to fraud/bot detection. |
| 3 | Web3/DeFi MEV Researcher | **CAUTION** | Pays well but crypto is volatile. Keep as opportunistic, not primary. |
| 4 | AI Tooling MLOps UX | **FAIR** | Safe fallback but may undersell the PhD. |
| 5 | Indie Game Dev | **AGREE** | Lottery ticket, correctly identified. |
| Traps | All three | **AGREE** | Consulting agency is especially dangerous. |

**Proposed change:** Reorder priority. Target #2 (Fraud/Risk) should be elevated to co-primary with #1. The PhD's opponent modeling + safe exploitation research maps 1:1 to adversarial detection, and you already have industry access via Playtech. This gives you TWO high-probability paths instead of one.

### Coop Plan (Oxford Partnership) — Verdict: Good ideas, significant dependency risk

**Critical risk: Partner is only applying this cycle.** If rejected, the entire plan timeline shifts by 1-2 years. The PhD must be designed so YOUR career doesn't depend on HIS acceptance.

| # | Target | Verdict | Notes |
|---|--------|---------|-------|
| 1 | B2B Fraud/AML Engine | **VIABLE** | Tech doable, but temper expectations: first contracts more like €30-80k, not €100-300k |
| 2 | Private Credit AI | **DIFFICULT** | Hot market but competing with well-funded startups (Preqin, Atominvest). Could work as niche consultancy, unlikely as SaaS product. |
| 3 | Treasury Hedging | **DEPRIORITIZE** | Regulatory overhead is extreme for a 2-person startup. CFOs are conservative buyers. |
| 4 | MEV/DeFi Fund | **HIGH RISK** | Raising €2-5M requires track record. Oxford MBA alone isn't enough for crypto fund investors. Only if partner has warm family office connections. |
| 5 | Alternative Data | **SKIP** | Dominated by incumbents. Hard to differentiate without proprietary data sources. |

**Proposed reorder:** 1 > 2 > 4 > 5 > 3. Treasury hedging should be last priority. Private Credit AI could work if framed as a consultancy (project-based, not SaaS). The 3-year sync plan timeline is good IF the partner gets in; build a contingency.

---

## 2. PhD Goal Alignment

### Proposed Research Focus
**"Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments"**

### Why this framing:
- **Game-theory themed** ✓ — imperfect-information games as testbed (satisfies university)
- **Generalized** ✓ — algorithms work for any multi-agent strategic interaction (satisfies professors)
- **Career-boosting** ✓ — transfers directly to fraud detection, adversarial AI, autonomous systems, financial strategy
- **Cutting-edge** ✓ — multi-agent safe exploitation is explicitly an open frontier (per SOE survey: "one of the most lucrative unsolved problems")
- **Realistic for 3 years** ✓ — tractable problem scope with clear sub-contributions

### Expected Thesis Contributions (draft):
1. **Behavioral Adaptation Framework** — A general method for inferring and adapting to opponent strategies from observed action sequences in real-time, applicable to any imperfect-information game
2. **Multi-Agent Safe Exploitation** — Extending safe exploitation guarantees from 2-player zero-sum to N-player settings (the open problem flagged in OX-Search)
3. **Evaluation Methodology** — A general framework for measuring agent adaptability and robustness across different game environments and opponent populations

### Why this beats a poker-only PhD:
The word "poker" doesn't appear in any contribution. Poker is merely one experimental domain. The same framework applies to: cybersecurity (adversarial network agents), market making (competing trading agents), autonomous driving (multi-agent navigation), and fraud detection (modeling adversarial actors). This is what makes it future-proof against AI automation — you're not training models, you're designing the strategic architecture.

---

## 3. The 14-Step Plan (Titles + Dependencies)

### Dependency Graph (Tree Structure)

```
                    ┌─── Step 3 ─── Step 4 ───┐
Step 1 ── Step 2 ──┤                           ├── Step 5 ── Step 6 ──┐
                    └───────────────────────────┘                      │
                                                                       │
                    ┌──────────────────────────────────────────────────┘
                    │
                    ├── Step 7 ── Step 8 ───────────────────┐
                    │      │                                 │
                    │      └── Step 9 ── Step 10 ───────────┤
                    │                                        │
                    └── Step 11 ── Step 12 ─────────────────┤
                                                             │
                                                     Step 13 ── Step 14
```

### Step List

**Phase A: Foundation (Done)**
- **Step 1** ✅ — Reinforcement Learning Basics *(Done: DQN, PPO, Gym)*
- **Step 2** ✅ — Game Theory + CFR Basics *(Done: Vanilla CFR, Kuhn Poker)*

**Phase B: Scaling the Toolbox (April)**
- **Step 3** — CFR Variants + Monte Carlo Methods *(depends on: Step 2)*
- **Step 4** — Game Abstraction + Scaling Imperfect-Information Games *(depends on: Steps 2, 3)*

**Phase C: Neural Methods for Games (May)**
- **Step 5** — Neural Equilibrium Approximation (Deep CFR, DREAM) *(depends on: Steps 1, 3, 4)*
- **Step 6** — End-to-End Game AI Architectures (Pluribus → ReBeL → Student of Games) *(depends on: Steps 3, 4, 5)*

**Phase D: Opponent Modeling + Exploitation (June)**
- **Step 7** — Opponent Modeling — Inference from Behavioral Traces *(depends on: Steps 2, 6)*
- **Step 8** — Safe Exploitation — Theory, Algorithms, and Real-Time Search *(depends on: Steps 6, 7)*

**Phase E: Multi-Agent Dynamics (July)**
- **Step 9** — Multi-Agent RL — Coordination, Competition, and Communication *(depends on: Steps 1, 6)*
- **Step 10** — Population-Based Training + Evolutionary Game Theory *(depends on: Steps 7, 8, 9)*

**Phase F: Modern Data-Driven Approaches (August)**
- **Step 11** — Sequence Models for Strategic Decision-Making *(depends on: Steps 5, 7)*
- **Step 12** — Behavioral Analysis Pipelines + Real-World Data *(depends on: Steps 7, 11)*

**Phase G: Integration (September)**
- **Step 13** — Evaluation Frameworks + Exploitability Metrics *(depends on: Steps 8, 10, 12)*
- **Step 14** — Research Frontier Mapping + Contribution Design *(depends on: all prior steps)*

### Why this ordering:
- **Months 1-2 (Steps 3-6):** Complete the algorithmic toolbox. You can't model opponents or evaluate agents without first knowing how equilibria are computed, scaled, and approximated neurally. Student of Games (Step 6) is the capstone — it unifies perfect and imperfect information into one framework, which is the generalization your professors want.
- **Month 3 (Steps 7-8):** The exploitation core. This is the thesis heartbeat. Step 7 builds the "sensor" (opponent modeling), Step 8 builds the "actuator" (safe exploitation). Together they're Contribution #1.
- **Month 4 (Steps 9-10):** The multi-agent extension. This is where the PhD becomes unique. Extending SOE to N-player is the open problem. PSRO gives you the population framework. Together they're Contribution #2.
- **Month 5 (Steps 11-12):** The data bridge. Sequence models + real data pipelines prepare you for the empirical work. This connects theory to Contribution #3 (evaluation framework).
- **Month 6 (Steps 13-14):** Integration. Build the evaluation framework, map the research frontier, and draft your first experiment. Exit ready for the research phase.
- **October:** Buffer month.
- **November:** Write Chapter 1 + first publication draft. (Meets the 11.2026 deadline.)

### Toy game progression:
- Steps 3–8: Kuhn / Leduc as primary testbeds (consistent with your completed work)
- Steps 9–10: Introduce at least one non-poker game (Goofspiel, matrix games, or Hanabi) for generalization
- Steps 13–14: Test on 2+ game types to demonstrate domain-agnostic evaluation

---

## 4. Step Structure Template

### Per-Step Structure (each step ≈ 2 weeks)

```
## Step N — [Title]

**Duration:** ~2 weeks (14 days)
**Dependencies:** Steps [X, Y, Z]
**Phase:** [A/B/C/D/E/F/G]

---

### Phase 1: Orientation (Days 1–3)
Build intuition BEFORE formalism. No papers yet.

**Day 1 — General Audience Content**
- [2-3 specific video lectures, conference talks, or blog posts]
- [1 podcast episode or interview if available]
- Goal: Understand WHAT the problem is and WHY it matters. No math yet.

**Day 2 — Interactive Exploration**
- [Specific sandboxes, demos, or existing tools to play with]
- [Run existing implementations from OpenSpiel / PettingZoo / etc.]
- Goal: Get hands dirty. See the algorithms behave before reading about them.

**Day 3 — Landscape Survey**
- [Skim 2-3 survey papers or textbook chapters for the big picture]
- [Search arxiv/Semantic Scholar for 2025-2026 papers on this topic]
- [Identify the 2-3 KEY papers you'll deep-read in Phase 2]
- Goal: Know where you are in the field. Build a mental map.

---

### Phase 2: Core Reading (Days 4–7)
Focused deep reading. Algorithmic/logical emphasis over pure notation.

**Primary Papers (2-3, rank-ordered by importance):**
| # | Paper | Year | Focus While Reading |
|---|-------|------|---------------------|
| 1 | [Most important paper] | [Year] | [What to focus on, what to skim] |
| 2 | [Second paper] | [Year] | [What to focus on, what to skim] |
| 3 | [Third paper — optional/cutting-edge 2024-2026] | [Year] | [What to focus on, what to skim] |

**Algorithmic Focus:**
- [Specific algorithm(s) to understand step-by-step, pseudocode-level]
- [Key insight or "aha moment" to look for]

**Math Deep-Dive (only if essential):**
- [Specific theorem/proof that's actually needed, if any]
- [Otherwise: "The math in Section X formalizes what you already understand
   algorithmically — skim for notation familiarity only"]

---

### Phase 3: Implementation (Days 8–12)
The core of each step. ~40% of total time.

**Practical Project:**
- [Clear, specific coding task]
- [Implementation language and framework]
- [What to build from scratch vs. what to use from libraries]

**Deliverables:**
- [ ] [Specific output 1 — e.g., working solver, trained agent, plot]
- [ ] [Specific output 2 — e.g., comparison with baseline, validation against known result]
- [ ] [Specific output 3 — e.g., documented state representation, reusable module]

**Validation:**
- [How to verify correctness — e.g., compare with OpenSpiel,
   check against analytical solution, measure exploitability]

---

### Phase 4: Gap-Filling + Consolidation (Days 13–14)
Skim reference material. Connect to the PhD.

**Reference Skim:**
- [Book chapters or long papers to skim for completeness]
- [Focus on: gaps in your understanding, alternative perspectives, historical context]

**PhD Connection:**
- [How this step feeds into the thesis — which contribution does it support?]
- [What open question from this step becomes a research opportunity?]

**Step Notes (to document):**
- [ ] Key algorithms understood (list with 1-line summary each)
- [ ] Open questions / things that confused me
- [ ] Connections to other steps discovered
- [ ] Candidate papers for Chapter 1 literature review
```

---

## Further Considerations
1. **Cutting-edge paper discovery:** Each step's "Day 3 — Landscape Survey" should include a search for 2025-2026 papers on that step's topic. ArXiv, Semantic Scholar, and conference proceedings (NeurIPS 2025, ICML 2025, AAAI 2026) should be checked.
2. **Toy game progression:** Steps 3-8 should use Kuhn/Leduc as primary testbeds. Steps 9-10 should introduce at least one non-poker game (e.g., Goofspiel, simple matrix games, or a cooperative game like Hanabi). Steps 13-14 should test on 2+ game types for generalization evidence.
3. **Playtech data:** Partial access is available. Step 12 should design the data pipeline with both synthetic and real data paths, so research isn't blocked if data access changes.

---

## Source Files
- `oldSources/docPlan_EN.md` — Original 8-step plan (Steps 1-2 completed)
- `oldSources/ind_plan_A_Andreev_EN.md` — University individual plan (Phase 1 deadline: 11.2026)
- `oldSources/safeOpponentExploitation.md` — SOE literature review (feeds into Steps 7-8)
- `oldSources/singleFuturePlan.md` — Bulgaria career plan (reviewed in Section 1)
- `oldSources/coopFuturePlan.md` — Partnership career plan (reviewed in Section 1)
