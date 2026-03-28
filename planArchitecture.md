# Plan: 15-Step PhD Preparation Roadmap + Career Alignment

**TL;DR:** A 15-step learning progression (2 done + 13 new, April–mid October 2026) that builds from your completed CFR/RL foundations to cutting-edge multi-agent adaptive strategy. Uses a 3-tier duration system: Tier 1 (3 weeks) for thesis-critical steps, Tier 2 (2 weeks) for standard steps, Tier 3 (10 days) for survey-dominant steps. Generalized beyond poker per professor feedback. Anchored to a career-maximizing PhD goal. Includes an honest career review, step structure template, and wildcard analysis.

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

## 3. The 15-Step Plan (Titles + Dependencies)

### Duration Tiers

Steps are not equal in complexity. A 3-tier system ensures thesis-critical material gets the depth it needs while lighter survey steps don't get padded.

| Tier | Duration | Criteria | Steps |
|------|----------|----------|-------|
| **Tier 1 — Deep Dive** | 3 weeks | Thesis-critical, multi-paper, complex implementation | 6, 7, 8 |
| **Tier 2 — Standard** | 2 weeks | Important, well-scoped, clear deliverables | 3, 4, 5, 9, 10, 11, 13, 14 |
| **Tier 3 — Focused** | 10 days | Survey-dominant, lighter implementation | 12, 15 |

**Why variable durations:** Steps 6–8 each cover multiple major papers/systems and are thesis-critical — cramming them into 2 weeks risks shallow understanding of the exact material the PhD builds on. Steps 12 and 15 are lighter: survey-oriented reading + synthesis, not algorithmically dense. The extra week for Tier 1 goes primarily to the implementation phase.

### Dependency Graph (Tree Structure)

```
                    ┌─── Step 3 ─── Step 4 ───┐
Step 1 ── Step 2 ──┤                           ├── Step 5 ── Step 6 ──┐
                    └───────────────────────────┘                      │
                                                                       │
                    ┌──────────────────────────────────────────────────┘
                    │
                    ├── Step 7 ── Step 8 ──────────────────────────────┐
                    │      │         │                                  │
                    │      │         └── Step 9 ── Step 10 ── Step 11 ─┤
                    │      │                                            │
                    │      └── Step 12 ── Step 13 ─────────────────────┤
                    │                                                   │
                    └───────────────────────────────────────────Step 14 ── Step 15
```

### Step List

**Phase A: Foundation (Done)**
- **Step 1** ✅ — Reinforcement Learning Basics *(Done: DQN, PPO, Gym)*
- **Step 2** ✅ — Game Theory + CFR Basics *(Done: Vanilla CFR, Kuhn Poker)*

**Phase B: Scaling the Toolbox (April)** `[4 weeks]`
- **Step 3** — CFR Variants + Monte Carlo Methods *(2 weeks, Tier 2)* — depends on: Step 2
- **Step 4** — Game Abstraction + Scaling Imperfect-Information Games *(2 weeks, Tier 2)* — depends on: Steps 2, 3

**Phase C: Neural Methods for Games (May → early June)** `[5 weeks]`
- **Step 5** — Neural Equilibrium Approximation (Deep CFR, DREAM) *(2 weeks, Tier 2)* — depends on: Steps 1, 3, 4
- **Step 6** — End-to-End Game AI Architectures (Pluribus → ReBeL → Student of Games) *(3 weeks, Tier 1)* — depends on: Steps 3, 4, 5

**Phase D: Opponent Modeling + Exploitation (June → mid July)** `[6 weeks]`
- **Step 7** — Opponent Modeling — Inference from Behavioral Traces *(3 weeks, Tier 1)* — depends on: Steps 2, 6
- **Step 8** — Safe Exploitation — Theory, Algorithms, and Real-Time Search *(3 weeks, Tier 1)* — depends on: Steps 6, 7

**Phase E: Multi-Agent Dynamics (mid July → August)** `[6 weeks]`
- **Step 9** — Multi-Agent RL — Coordination, Competition, and Communication *(2 weeks, Tier 2)* — depends on: Steps 1, 6
- **Step 10** — Population-Based Training + Evolutionary Game Theory *(2 weeks, Tier 2)* — depends on: Steps 7, 8, 9
- **Step 11** — Dynamic Coalition Formation in Competitive FFA Games *(2 weeks, Tier 2)* — depends on: Steps 7, 9, 10 **[NEW — WILDCARD B]**

**Phase F: Data-Driven Approaches (late August → September)** `[3.5 weeks]`
- **Step 12** — Sequence Models + LLM Agents in Strategic Settings *(10 days, Tier 3)* — depends on: Steps 5, 7 **[TITLE UPDATED — WILDCARD A FOLDED IN]**
- **Step 13** — Behavioral Analysis Pipelines + Real-World Data *(2 weeks, Tier 2)* — depends on: Steps 7, 12

**Phase G: Integration (late September → mid October)** `[3.5 weeks]`
- **Step 14** — Evaluation Frameworks + Exploitability Metrics *(2 weeks, Tier 2)* — depends on: Steps 8, 11, 13
- **Step 15** — Research Frontier Mapping + Contribution Design *(10 days, Tier 3)* — depends on: all prior steps

### Calendar

| Dates | Step | Tier | Duration |
|-------|------|------|----------|
| Apr 1–14 | Step 3: CFR Variants + MC Methods | T2 | 2 weeks |
| Apr 15–28 | Step 4: Game Abstraction + Scaling | T2 | 2 weeks |
| Apr 29–May 12 | Step 5: Neural Equilibrium (Deep CFR, DREAM) | T2 | 2 weeks |
| May 13–Jun 2 | Step 6: End-to-End Game AI (Pluribus→ReBeL→SoG) | **T1** | **3 weeks** |
| Jun 3–23 | Step 7: Opponent Modeling | **T1** | **3 weeks** |
| Jun 24–Jul 14 | Step 8: Safe Exploitation | **T1** | **3 weeks** |
| Jul 15–28 | Step 9: MARL — Coordination, Competition, Comms | T2 | 2 weeks |
| Jul 29–Aug 11 | Step 10: PBT + Evolutionary Game Theory | T2 | 2 weeks |
| Aug 12–25 | **Step 11: Coalition Formation in FFA Games [NEW]** | T2 | 2 weeks |
| Aug 26–Sep 5 | Step 12: Sequence Models + LLM Agents | T3 | 10 days |
| Sep 6–19 | Step 13: Behavioral Analysis Pipelines | T2 | 2 weeks |
| Sep 20–Oct 3 | Step 14: Evaluation Frameworks + Exploitability | T2 | 2 weeks |
| Oct 4–14 | Step 15: Research Frontier Mapping | T3 | 10 days |
| Oct 15–31 | **Buffer** | — | **~2.5 weeks** |
| November | Chapter 1 + first publication draft | — | — |

**Time budget:** 9 weeks (Tier 1) + 16 weeks (Tier 2) + 3 weeks (Tier 3) = **28 weeks** (Apr 1 → Oct 14). Buffer: ~2.5 weeks before November deadline.

### Why this ordering:
- **Months 1–2 (Steps 3–6, Apr–early Jun):** Complete the algorithmic toolbox. You can't model opponents or evaluate agents without first knowing how equilibria are computed, scaled, and approximated neurally. Student of Games (Step 6) gets 3 weeks (Tier 1) — it unifies perfect and imperfect information into one framework, which is the generalization proof your professors want.
- **Month 3 (Steps 7–8, Jun–mid Jul):** The exploitation core. This is the thesis heartbeat. 3 weeks each (Tier 1) because these two steps ARE the PhD. Step 7 builds the "sensor" (opponent modeling), Step 8 builds the "actuator" (safe exploitation). Together they're Contribution #1.
- **Month 4 (Steps 9–11, mid Jul–Aug):** The multi-agent extension. MARL foundations → population training → then coalition dynamics in FFA games. Step 11 is the new frontier step — nearly unstudied in competitive settings (only "So Long Sucker" benchmark exists, 2411.11057), direct PhD differentiator. Together = Contribution #2.
- **Month 5 (Steps 12–13, late Aug–Sep):** The data bridge. Sequence models + LLM survey (10 days, Tier 3 — the field is too young for more) → Playtech data pipeline. Connects theory to Contribution #3.
- **Month 6 (Steps 14–15, late Sep–mid Oct):** Integration. Evaluation framework (Contribution #3) → research frontier map → exit ready for the research phase.
- **November:** Write Chapter 1 + first publication draft. (Meets the 11.2026 deadline.)

### Toy game progression:
- Steps 3–8: Kuhn / Leduc as primary testbeds (consistent with your completed work)
- Steps 9–10: Introduce Goofspiel or matrix games for generalization
- **Step 11: So Long Sucker (arXiv 2411.11057) as primary testbed — the first competitive FFA coalition benchmark**
- Steps 12–13: LLM benchmarks (TextArena) + Playtech data
- Steps 14–15: Test evaluation framework on 2+ game types for domain-agnostic evidence

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

## 5. Wildcard Evaluation

### Wildcard A: LLM Agents in Strategic Settings → Folded into Step 12

| Factor | Assessment |
|--------|------------|
| Academic relevance | Hot (32 arXiv papers in 2025, ICLR 2025 "Do LLM Agents Have Regret?"), but mostly benchmarking, not algorithmic |
| PhD contribution fit | Weak. None of the 3 thesis contributions require LLM expertise. An LLM baseline in experiments is a 2-day task, not a 2-week step |
| Career value | High. Both career paths (MARL architect, fraud/risk) intersect with LLMs. Understanding their strategic limitations is career insurance |
| Implementation depth | Shallow. Running TextArena or prompting GPT-4 to play poker doesn't build transferable algorithmic skill |
| Frontier density | Crowded. Everyone is writing LLM+game theory papers right now. Low differentiation for a PhD |

**Decision:** Fold into Step 12 title ("Sequence Models + LLM Agents in Strategic Settings"). Cover TextArena + 1–2 key papers in the orientation phase. Don't make it a full step.

**Key references:** "Game Theory Meets LLM and Agentic AI" (Zhu, 2507.10621), "Do LLM Agents Have Regret?" (ICLR 2025), TextArena benchmark.

### Wildcard B: Dynamic Coalition Formation in Competitive FFA Games → New Step 11

| Factor | Assessment |
|--------|------------|
| Academic relevance | Frontier. "So Long Sucker" (2411.11057) is essentially the only competitive FFA MARL benchmark. AAMAS 2025 coalition detection paper (2502.16339) confirms the area is just opening up |
| PhD contribution fit | Strong. Maps directly to Contribution #2 (N-player safe exploitation). Coalition dynamics are the mechanism by which N-player safety guarantees collapse — when agents form temporary alliances, 2-player assumptions break |
| Career value | Medium. Multi-agent reasoning transfers to fraud ring detection (collusive actors) |
| Implementation depth | High. Implementing a coalition-forming agent in an FFA game is a genuine coding challenge |
| Frontier density | Sparse. Almost no competition. Google Scholar returned only cooperative coalition formation results (UAVs, resource allocation) — the competitive FFA angle is nearly unstudied. Could become a thesis chapter |

**Decision:** Add as standalone Step 11. PhD differentiator. The sparse frontier means high novelty potential.

**Key references:** "So Long Sucker" MARL benchmark (2411.11057), "Dynamic Coalition Structure Detection" (Kulkarni+, AAMAS 2025, 2502.16339).

---

## 6. Job Market Stress Test

The 15-step plan was validated against 10 real job postings from Glassdoor (March 2026) spanning both career paths.

### Path 1.1 — MARL / AI Architect roles
| Role | Salary | Steps that hit |
|------|--------|----------------|
| Serve Robotics — RL Lead | $160–300k | 5, 6, 9, 10 |
| GM — Vehicle AI Staff Engineer | $189–290k | 5, 6, 9 |
| PARTech — AI Engineer | $200–215k | 5, 6, 7, 9 |
| Zillow — Principal ML Engineer | $204–327k | 5, 7, 13 |
| Cloud Resources — AI Solutions Architect | Unlisted | 6, 9, 14 |

### Path 1.2 — Fraud / Risk / Adversarial AI roles
| Role | Salary | Steps that hit |
|------|--------|----------------|
| Whatnot — ML Scientist, Risk & Fraud | $245–345k | 7, 8, 12, 13 |
| Adobe — Sr AI/ML Engineer, Fraud | $143–271k | 7, 8, 13 |
| PayPal — Staff ML Engineer, Fraud | $179–265k | 7, 8, 12, 13 |
| Home Depot — Staff Engineer, Fraud | $140–220k | 7, 8, 13 |
| Intuit — Staff AI Engineer, Fraud | $202–278k | 7, 8, 13, 14 |

### Coverage verdict
- **Steps 7–8** (Opponent Modeling + Safe Exploitation) are the highest-value steps, hitting 9/10 job scenarios
- **Steps 5, 6, 9** cover the MARL architect path well
- **Steps 12–13** (Sequence Models + Behavioral Pipelines) cover the fraud path's data requirements
- **Gap noted:** Production/MLOps skills (5/10 jobs mention deployment) — out of scope for learning phase, but flagged for future
- **LLM awareness** (3/10 jobs mention LLM) — covered via Step 12 title update

---

## 7. Summary of Changes from Original 14-Step Plan

| Change | Details |
|--------|---------|
| **+1 step** | New Step 11: "Dynamic Coalition Formation in Competitive FFA Games" — PhD frontier differentiator |
| **LLM folded in** | Step 12 title: "Sequence Models + LLM Agents in Strategic Settings" — career insurance without overinvesting |
| **Renumbered** | Old Steps 11→12, 12→13, 13→14, 14→15 |
| **Variable durations** | Steps 6, 7, 8 → 3 weeks (Tier 1). Steps 12, 15 → 10 days (Tier 3). Rest → 2 weeks (Tier 2) |
| **Timeline** | April 1 → October 14, with ~2.5 weeks buffer before November deadline |
| **Total effort** | 28 weeks (was 24 in the flat 12×2 plan) — more realistic for the material |

---

## Further Considerations
1. **Cutting-edge paper discovery:** Each step's "Day 3 — Landscape Survey" should include a search for 2025-2026 papers on that step's topic. ArXiv, Semantic Scholar, and conference proceedings (NeurIPS 2025, ICML 2025, AAAI 2026) should be checked.
2. **Toy game progression:** Steps 3–8 use Kuhn/Leduc. Step 11 uses So Long Sucker. Steps 12–13 use TextArena + Playtech data. Steps 14–15 test on 2+ game types for generalization evidence.
3. **Playtech data:** Partial access is available. Step 13 should design the data pipeline with both synthetic and real data paths, so research isn't blocked if data access changes.
4. **Tier 1 implementation emphasis:** The extra week in Tier 1 steps should go primarily to the implementation phase (Phase 3 in the template), extending it from 5 days to 8 days.

---

## Source Files
- `oldSources/docPlan_EN.md` — Original 8-step plan (Steps 1-2 completed)
- `oldSources/ind_plan_A_Andreev_EN.md` — University individual plan (Phase 1 deadline: 11.2026)
- `oldSources/safeOpponentExploitation.md` — SOE literature review (feeds into Steps 7-8)
- `oldSources/singleFuturePlan.md` — Bulgaria career plan (reviewed in Section 1)
- `oldSources/coopFuturePlan.md` — Partnership career plan (reviewed in Section 1)
