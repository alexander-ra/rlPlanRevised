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

## 4. Learning Methodology & Step Blueprint

This chapter defines HOW each step is learned. It codifies the learning style, resource standards, coding rules, and exit criteria that every generated step must follow. These rules are based on feedback from completing Steps 1–2.

### 4.1 The 5-Phase Learning Cycle

Every step follows the same 5-phase cycle. The phases are sequential — each builds on the cognitive state created by the previous one. The same structure applies to all three tiers; only the number of days per phase changes.

| Phase | Purpose | Mode | Core question |
|-------|---------|------|---------------|
| **1. Intuition** | What is this? Why does it matter? | Passive absorption — videos, talks, blogs | Could I explain this problem to a non-expert? |
| **2. Exploration** | How does it behave? | Active play — sandboxes, existing code, demos | Have I seen the algorithm succeed AND fail? |
| **3. Targeted Reading** | How does it work? | Surgical paper reading — algorithm-first, skip filler | Can I trace the algorithm step-by-step on paper? |
| **4. Implementation** | Can I build it? | Code — from-scratch core + AI-assisted scaffolding | Does my implementation match known results? |
| **5. Consolidation** | What did I miss? How does this connect? | Gap-fill — skim books, write one-pager, update logs | Am I ready for the exit checklist? |

**Design rationale:** This cycle front-loads intuition and hands-on play BEFORE formalism. Feedback from Steps 1–2 showed that reading papers cold leads to focus loss on redundant intros and boilerplate sections. Seeing the algorithm behave first makes the paper reading 2-3x more efficient because you already know what to look for.

### 4.2 Day Allocation by Tier

Same 5 phases, scaled proportionally. Implementation stays at ~45% for all tiers.

| Phase | Tier 1 (21 days) | Tier 2 (14 days) | Tier 3 (10 days) |
|-------|----------------:|----------------:|----------------:|
| 1. Intuition | 2 days | 1 day | 1 day |
| 2. Exploration | 2 days | 2 days | 1 day |
| 3. Targeted Reading | 4 days | 3 days | 2 days |
| 4. Implementation | 10 days | 6 days | 4 days |
| 5. Consolidation | 3 days | 2 days | 2 days |

**Why Exploration gets 2 days in Tier 2:** Sandbox time was the biggest learning accelerator in Steps 1-2. Tier 3 drops to 1 day because those steps are survey-dominant (less to "play with").

**Tier 1 implementation note:** The 10-day implementation phase for Tier 1 steps should be sub-structured as: 2 days architecture + scaffolding → 6 days core algorithm → 2 days validation + benchmarking.

### 4.3 Phase Details

#### Phase 1: Intuition
No papers. No math. No code. Only:
- 2–3 video lectures or conference talks (YouTube links, with duration and speaker)
- 1 podcast episode or long-form interview if available
- Blog posts or accessible explainers
- **Goal:** Be able to explain the problem to a non-expert by end of phase

#### Phase 2: Exploration
No reading yet. Only:
- Run existing implementations (OpenSpiel, PettingZoo, published GitHub repos)
- Interactive web tools, sandboxes, Colab notebooks
- Modify parameters, break things, observe behavior
- **Goal:** See the algorithm work (and fail) before knowing the formal "why"

#### Phase 3: Targeted Reading
This is the anti-filler phase. Papers are NOT read front-to-back. Each step prescribes a **surgical reading protocol** per paper:

```
Paper: [Full Title] ([Author], [Year])
Link: [arXiv / DOI URL]
├── READ:  Sections X, Y (the algorithm description, the experiments/results)
├── SKIM:  Abstract, Intro (for framing only), Related Work (for bibliography mining)
├── SKIP:  [Specific sections that repeat content already covered in prior steps]
├── MATH:  [One of the following:]
│          → "Theorem N matters — work through the proof. WHY: [explanation of why
│             this cannot be substituted by algorithmic understanding alone, e.g.,
│             'the bound in Theorem 2 is what makes safe exploitation SAFE — without
│             understanding the proof, you can't know when the guarantee breaks']"
│          → "Section X math formalizes what you already understand algorithmically
│             from Phase 2 exploration — skim for notation familiarity only"
└── KEY INSIGHT: [The one sentence/figure that captures why this paper matters]
```

**Book chapters rule:** When a step assigns specific chapters (e.g., Chapters 5-7 out of 15), the step must include:
- A 2–3 sentence summary of what Chapters 1-4 covered (so you're not lost at the start)
- A 1–2 sentence note on what Chapters 8+ cover (so you know what's coming / what you're skipping and why)
- This prevents the "dropped into the middle" disorientation without requiring you to read the preceding chapters

**Reading priority:** Always prefer the algorithmic/logical explanation. Math is mandatory only when explicitly flagged with a WHY justification. When flagged, the step will explain exactly why the algorithmic understanding alone is insufficient (e.g., "the convergence bound proof is what tells you how many iterations you actually need" or "the safety guarantee derivation is what your thesis extends — you must be able to modify it").

#### Phase 4: Implementation
The core of each step (~45% of total time). Sub-structured as:

| Sub-phase | Tier 1 | Tier 2 | Tier 3 | Purpose |
|-----------|--------|--------|--------|---------|
| Architecture + scaffolding | 2 days | 1 day | 1 day | Design code structure, set up environment, data loading |
| Core algorithm | 6 days | 4 days | 2 days | The novel algorithmic implementation |
| Validation + benchmarking | 2 days | 1 day | 1 day | Compare against known results, generate plots |

Each step must specify:
- **Practical project:** Clear, specific coding task
- **Language + framework:** (default: Python + PyTorch, unless step requires otherwise)
- **Deliverables:** Concrete outputs (working solver, trained agent, comparison plot, etc.)
- **Validation method:** How to verify correctness (compare with OpenSpiel, check against analytical solution, measure exploitability, etc.)

**AI assistance rules** are specified per-step in Section 4.4 below. Each step's implementation section will explicitly state which components are hand-code vs. AI-assisted.

#### Phase 5: Consolidation
The gap-filler + PhD connector:
- Skim the "big reference" for this topic (textbook, long survey) — targeted to gaps found during implementation
- Write the **mandatory one-pager** (see Section 4.7)
- Update the **Learning Log** (see Section 4.8)
- Explicitly connect to PhD contributions: which thesis contribution does this step feed? What open question emerged?

### 4.4 Code Ownership Rules

Every step must explicitly tag each implementation component with one of the following labels:

| Label | Rule | Litmus test |
|-------|------|-------------|
| **🔴 HAND-CODE** | Write from scratch, line by line. No AI generation. AI may be used to explain a concept if stuck, but not to produce the code. | "Would I need to re-derive/re-implement this on a whiteboard during a PhD viva?" → If yes, hand-code. |
| **🟡 AI-ASSISTED** | AI generates a first draft. You review every line, understand it, modify it, and own it. The AI output is a starting point, not a deliverable. | "Do I need to deeply understand this, but line-by-line struggle won't add insight beyond what review gives me?" → AI-assist. |
| **🟢 AI-GENERATED** | AI generates, you review for correctness and integration. Acceptable for boilerplate that must work but isn't intellectually novel. | "Is this plumbing/glue code where my time is better spent on the algorithm itself?" → AI-generate. |

**Typical tagging pattern (will vary per step):**

| Component | Typical tag | Why |
|-----------|-------------|-----|
| Core algorithm loop | 🔴 HAND-CODE | It's in the thesis. You must own every line. Understanding comes from struggling with indexing, edge cases, convergence. |
| Algorithm variant (2nd+ implementation of same family) | 🟡 AI-ASSISTED | Once you've built MCCFR from scratch, outcome-sampling MCCFR can be AI-drafted and reviewed — the insight transfers. |
| Data pipeline / environment wrappers | 🟢 AI-GENERATED | Loading data, plotting, gym wrappers. Must work, but line-by-line struggle adds no insight. |
| Test harness / tournament framework | 🟡 AI-ASSISTED | Structure can be AI-generated, but evaluation metrics (e.g., exploitability computation) you must understand deeply. |
| Debugging | 🟢 AI-GENERATED | Using AI to diagnose convergence issues is pragmatic, not lazy. |

**Per-step override:** When generating each step's content, every deliverable will be explicitly tagged 🔴/🟡/🟢 with a one-line justification. This removes ambiguity at execution time.

### 4.5 Resource Quality Standards

Every resource referenced in a generated step must meet these standards. No vague references. No "read the X paper" without a link.

| Resource type | Required format |
|---------------|----------------|
| Video lecture / talk | Direct YouTube or platform URL + duration + speaker name |
| Blog post / article | Direct URL + author |
| Book (freely available) | Direct PDF/HTML link (e.g., Sutton & Barto on incompleteideas.net) |
| Book (paid only) | Purchase link (Amazon/publisher) + library/alternative if known |
| Paper | arXiv link preferred (always free). DOI link as fallback. Never paywalled-only without a free alternative |
| Playground / demo | Direct URL or GitHub repo link + setup command (`pip install X` / `git clone Y`) |
| Framework / library | pip/conda install command + quickstart page URL |
| Dataset | Download URL or API command + license note |

**Example of UNACCEPTABLE:** "Read the Zinkevich 2007 paper on CFR."
**Example of ACCEPTABLE:** "Read [Regret Minimization in Games with Incomplete Information](https://arxiv.org/abs/0709.2092) (Zinkevich et al., 2007)."

### 4.6 Freshness Scan Protocol

Before generating each step's content, the following scan must be executed to ensure no important recent work is missed:

1. **ArXiv search** — Search each subtopic keyword, sort by date, check 2024–2026 papers
2. **Semantic Scholar** — Sort by citation count for the foundational layer (identify top 5 most-cited works)
3. **Conference proceedings** — Check NeurIPS 2025, ICML 2025, ICLR 2025/2026, AAAI 2026 for accepted papers on the step's subtopic
4. **GitHub trending / Papers With Code** — Check if new frameworks or reference implementations have emerged since the plan was written
5. **Cross-reference against prior steps** — Avoid assigning the same paper to multiple steps unless it genuinely spans both topics

Each generated step must include a **"Freshness Note"** at the top documenting:
- What searches were run and when
- Any newly discovered papers that weren't in the original plan
- Any papers that were planned but have been superseded by newer work

### 4.7 Mandatory One-Pager

At the end of every step, write a **one-page summary** (literally one page, ~400-500 words). This is not a report — it's a distillation exercise. Structure:

```
# Step N — [Title]: One-Pager

**Problem:** What problem does this step's field address? (2-3 sentences)
**Core Algorithm(s):** The main algorithm(s) studied, in plain language. (3-5 sentences)
**Key Result:** What did the foundational papers achieve? What's the state of the art? (2-3 sentences)
**My Implementation:** What I built, what it validates. (2-3 sentences)
**Open Question:** The most interesting unsolved problem I encountered. (1-2 sentences)
**PhD Connection:** How this feeds into my thesis. (1-2 sentences)
```

**Why mandatory:** By Step 15, you have 13 one-pagers. Assembled sequentially, they form a first draft of Chapter 1's literature review structure. Each one-pager becomes a subsection seed.

### 4.8 Learning Log

A single running markdown file (`learningLog.md`) maintained throughout all steps. Contains two sections:

**Connections:** Tracks cross-step links as they emerge.
```
- [Step 3] MCCFR's sampling strategy → directly affects [Step 5] Deep CFR's training stability
- [Step 7] Bayesian opponent model → extends to [Step 11] coalition detection (agents as "opponents")
```

**Confusions:** Tracks things that didn't click. Often, Step 7's confusion gets answered in Step 10. Having it written down means you actually revisit it.
```
- [Step 3] Why does external sampling converge faster in practice but has worse theoretical guarantees?
  → RESOLVED in [Step 5]: Deep CFR essentially learns to approximate the value of external sampling
- [Step 5] How does DREAM handle the variance from opponent sampling?
  → OPEN: revisit in Step 8 (safe exploitation may provide the framework to think about this)
```

**Maintenance rule:** Update at the end of each step during Phase 5 (Consolidation). Review all OPEN entries from prior steps — mark resolved ones with the step that resolved them.

### 4.9 Hard Gate Exit Criteria

**Each step has a hard gate.** You do NOT proceed to the next step until all items are checked. If a deliverable doesn't validate, you fix it — you don't move on and "revisit later." Dedication is everything.

```
## Step N — Exit Checklist

- [ ] All deliverables working and validated against known results
- [ ] Can explain the main algorithm(s) from memory (whiteboard test)
- [ ] AI-assistance rules were followed (all 🔴 components hand-coded)
- [ ] One-pager written and committed to repo
- [ ] Learning Log updated (new connections + new confusions + resolved confusions)
- [ ] Key insight documented in 1-2 sentences
- [ ] Open questions logged in Learning Log
- [ ] PhD connection noted (which thesis contribution does this feed?)
- [ ] Candidate papers for Chapter 1 literature review identified
- [ ] Step notes committed to repo
```

**If the gate blocks:** It's a signal that the step needs more time, not that the gate is too strict. Use buffer days from the schedule, or borrow from the October buffer. Never borrow from the NEXT step — that creates cascading debt.

### 4.10 Step Content Template

When generating the actual content for each step, use this structure:

```
# Step N — [Title]

**Duration:** [X days] (Tier [1/2/3])
**Dependencies:** Steps [X, Y, Z]
**Phase:** [B/C/D/E/F/G]
**Freshness Note:** [Searches run, date, any updates to planned content]

---

## Phase 1: Intuition ([X days])
- [Specific videos with YouTube URLs, duration, speaker]
- [Podcasts / interviews if available]
- [Blog posts with direct URLs]

## Phase 2: Exploration ([X days])
- [Specific sandboxes with URLs / GitHub links / setup commands]
- [Existing implementations to run, with exact commands]
- [What to observe / what parameters to tweak]

## Phase 3: Targeted Reading ([X days])
### Paper 1: [Title] ([Author], [Year])
[Surgical reading protocol — READ/SKIM/SKIP/MATH/KEY INSIGHT]

### Paper 2: [Title] ([Author], [Year])
[Surgical reading protocol]

### Book Chapters (if applicable):
**Book:** [Title] ([Author])  
**Link:** [Free link or purchase link]  
**Assigned chapters:** [N–M]  
**Context — what comes before (Ch 1–N-1):** [2-3 sentence summary so you're not lost]  
**Context — what comes after (Ch M+1–end):** [1-2 sentence note on what you're skipping and why]  
**Reading focus:** [What to pay attention to, what to skim]

### Math Flags (if any):
🔢 **[Theorem/Proof name]** — Must work through with pen and paper.  
**WHY this can't be substituted by algorithmic understanding:** [Specific explanation]

## Phase 4: Implementation ([X days])
### Project: [Clear description]

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| [Component 1] | 🔴 HAND-CODE | [Why] |
| [Component 2] | 🟡 AI-ASSISTED | [Why] |
| [Component 3] | 🟢 AI-GENERATED | [Why] |

### Deliverables:
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

### Validation:
- [How to verify correctness]

## Phase 5: Consolidation ([X days])
- **Reference skim:** [Book/survey to skim for gaps]
- **One-pager:** Write and commit
- **Learning Log:** Update connections + confusions
- **PhD Connection:** [Which contribution this feeds]

## Exit Checklist
- [ ] All deliverables working and validated
- [ ] Whiteboard test passed
- [ ] AI-assistance rules followed
- [ ] One-pager committed
- [ ] Learning Log updated
- [ ] Step notes committed
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
