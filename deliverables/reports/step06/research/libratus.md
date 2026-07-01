# Libratus — Research Notes

> Gather sources and extract architectural detail BEFORE writing prose in
> ../summary/summaryEn.md. Cite every source so claims are traceable.
> System: Libratus (Brown & Sandholm, 2017/2018).

## Sources consulted
<!-- Primary paper, author talks, blogs, secondary deep-dives. Add links + 1-line relevance. -->
- **[Primary]** Brown, N. & Sandholm, T. (2018), "Superhuman AI for Heads-Up No-Limit Poker: Libratus
  Beats Top Professionals", *Science* 359(6374):418–424, doi:10.1126/science.aao1733.
  https://www.science.org/doi/10.1126/science.aao1733 (author copies: NSF PAR 10077416 / 10077470).
  The backbone for the three-module architecture, the subgame-solving theory (Theorem 1), the
  Baby Tartanian8 head-to-head table, and the human-match result. Cited below as "(Science)".
- **[Primary, longer/system view]** Brown, N. & Sandholm, T. (2017), "Libratus: The Superhuman AI for
  No-Limit Poker", *IJCAI-17* (proceedings 0772). https://www.ijcai.org/proceedings/2017/0772.pdf —
  gives the abstraction size (10^161 → 10^12), the **compute breakdown** (~25M core-hours), the
  asymmetric abstraction note, and the node counts. Cited as "(IJCAI)".
- **[Primary, theory]** Brown, N. & Sandholm, T. (2017), "Safe and Nested Subgame Solving for
  Imperfect-Information Games", *NeurIPS-17* (best-paper), arXiv:1705.02955 — the full development of
  Reach / Estimated-Maxmargin nested safe subgame solving that the Science paper summarizes. Cited as
  "(NeurIPS-17 subgame)".
- **[Compute / systems detail]** Sandholm, T., CMU course 15-888 (Computational Game Solving), Fall 2021,
  Lecture 13 "Endgame solving, and Libratus". https://www.cs.cmu.edu/~sandholm/cs15-888F21/lecture13.pdf
  — operational numbers: Bridges node usage, disk (2.6 PB), per-module run sizes/durations. Cited as
  "(CMU L13)".
- **[Secondary, accessible]** CMU/CSD press, "Carnegie Mellon Reveals Inner Workings of Victorious Poker
  AI" (Dec 2017). https://csd.cmu.edu/news/carnegie-mellon-reveals-inner-workings-of-victorious-poker-ai
  — plain-language confirmation of the 3 modules + the "no opponent exploitation" framing of the
  self-improver. Cited as "(CMU news)".
- **[Secondary, accessible]** "Libratus: the world's best poker player", The Gradient (2018).
  https://thegradient.pub/libratus-poker/ — reader-friendly walk-through of blueprint + nested safe
  subgame solving + self-improver.
- **[Author talk]** Noam Brown, "AI for Imperfect-Information Games: Beating Top Humans in No-Limit
  Poker" (Microsoft Research, ~1 h). https://www.youtube.com/watch?v=McV4a6umbAY — Brown's own
  architectural walk-through of Libratus/DeepStack; the blueprint + subgame-solve + self-improve framing.
- **[Context, prior milestone]** Bowling, Burch, Johanson & Tammelin (2015), "Heads-up Limit Hold'em
  Poker is Solved" (*Science*, Cepheus / CFR+) — the ~10^13-node limit-poker milestone Libratus contrasts
  against (HUNL is ~10^161).
- **[Context, abstraction lineage]** Brown & Sandholm (2016), "Baby Tartanian8" (IJCAI-16) and
  Brown, Ganzfried & Sandholm (2015), "Tartanian7" — the ACPC-winning predecessors whose card
  abstraction Libratus reuses; Baby Tartanian8 is the head-to-head benchmark.
- **[Context, action translation]** Ganzfried & Sandholm (2013), "Action translation in extensive-form
  games" (IJCAI) — the "round the bet to the nearest abstract size" baseline that nested subgame solving
  beats by >1 order of magnitude.
- **[Hand-off ← DeepStack]** Moravčík et al. (2017), DeepStack (*Science*), arXiv:1701.01724 — the
  concurrent, independent system; the Science paper's notes 50 + the DeepStack/Libratus contrast
  paragraphs are the bridge material (see ../research/deepstack.md "Hand-off → Libratus").
- **[Hand-off → Pluribus, system #3]** Brown & Sandholm (2019), "Superhuman AI for Multiplayer Poker"
  (*Science* 365:885–890), arXiv:1911.07559 — the 6-player successor that reuses the blueprint + real-time
  depth-limited search recipe; used ONLY for the forward hand-off (full treatment in subtask #3).
- **[Lineage / modern relevance]** Brown, Bakhtin, Lerer & Hu (2020), ReBeL (NeurIPS), arXiv:2007.13544 —
  generalizes safe real-time search via public belief states + learned values (System #4).
- **[Modern relevance]** Noam Brown, Sequoia "Training Data" podcast (2024) on o1 / test-time compute —
  frames real-time search (as in Libratus) as an early instance of inference-time deliberation; the often
  -quoted point that adding search was worth far more than scaling the blueprint.
  https://www.sequoiacap.com/podcast/training-data-noam-brown/

---

## Architecture / component breakdown
<!-- Offline vs online components; where NN / CFR / search sit. -->

Libratus = **abstraction + blueprint (offline, MCCFR)** + **nested safe subgame solving (online, CFR+)** +
**self-improver (overnight, MCCFR/CFR+)**. There are **no neural networks anywhere** — Libratus is a purely
tabular CFR/abstraction system. (Science; IJCAI.) This is the single biggest architectural contrast with
DeepStack, which is built around learned value networks.

**Module 1 — Blueprint (offline):**
- **Abstraction** shrinks HUNL from **10^161 decision points** to **~10^12** (IJCAI). Two kinds:
  - *Action abstraction*: a discrete set of bet sizes (mostly nice pot fractions/multiples, taken from the
    most common bet sizes used by top ACPC AIs; a few early bet sizes set by a parameter-optimization
    algorithm, Brown & Sandholm 2014). An **asymmetric** abstraction gives the opponent *more* actions, to
    reduce action-translation error (IJCAI; Bard et al. 2014).
  - *Card abstraction*: **none on rounds 1–2 (preflop, flop)**. Rounds 3–4 are bucketed **only in the
    blueprint**: 55M turn hand-possibilities → **2.5M buckets**; 2.4B river possibilities → **1.25M
    buckets** (imperfect-recall, k-means-style; same family as Baby Tartanian8 / Tartanian7). (Science.)
- **Equilibrium finding**: an **improved MCCFR** (external-sampling MCCFR with **regret-based pruning** —
  probabilistically skip very-negative-regret actions deeper in the tree). ~**3× speedup**; also mitigates
  imperfect-recall "bucket fighting" because unreached decision points stop updating shared buckets.
  (Science; note 39: skip prob K/(K+C−R(a)) on ~the last half of iterations.)
- Output = the **blueprint strategy**: detailed for rounds 1–2, coarse for rounds 3–4 (used there only to
  *estimate the value of reaching a subgame*, not to play). (Science.)

**Module 2 — Nested safe subgame solving (online / real time):**
- Trigger: on reaching the **3rd betting round** (or any earlier point where the remaining tree is small
  enough — "no additional bets/raises possible", note 44), build a **finer-grained abstraction with NO card
  abstraction** for the remaining subgame and **solve it in real time** with **heavily optimized CFR+**
  (note 46). So **each hand is played individually** in the late game.
- *Safety*: an imperfect-information subgame can't be solved in isolation (its optimal strategy depends on
  unreached subgames). Libratus builds an **augmented subgame** (Fig. 1): the opponent is given the choice
  to *enter* the detailed subgame or take an **alternative payoff = the blueprint estimate of their value**;
  solving it makes the refined strategy **no worse than the blueprint against every opponent hand**.
- **Estimated-Maxmargin** (Theorem 1): uses blueprint *estimates* (not best-response *upper bounds*) of
  opponent values; exploitability rises by **at most 2Δ** if estimates are off by ≤Δ. Three advances over
  prior safe subgame solving (Burch et al. 2014; Moravčík et al. 2016): (1) estimates not upper bounds →
  less conservative; (2) **de-emphasize "unimportant" hands** the opponent would hold only after an earlier
  mistake (raise their alternative reward by the cost of reaching the subgame); (3) **respond to off-tree
  bets exactly** instead of rounding — repeated down the tree = *nested* subgame solving.
- *Off-tree opponent bets*: solve a fresh augmented subgame **including the actual bet**, with the
  alternative payoff = best in-abstraction action. This is the direct cure for the **action-translation**
  weakness. Empirically **>1 order of magnitude** less exploitable than action translation (Table 2).
- *Real-time re-abstraction*: because the subgame is solved live, Libratus **randomly perturbs its own bet
  sizes** (±0–8%, note 49) at the first solve and every later subgame of the hand, forcing the opponent to
  keep adapting.

**Module 3 — Self-improver (background / overnight):**
- Rounds 1–2 still use the blueprint (real-time solving so early would need heavy abstraction, likely no
  better than the already-card-abstraction-free blueprint), so **off-tree opponent bets there are still
  rounded** (action translation). The dense action abstraction limits the error; the self-improver shrinks
  what remains.
- Each day it **aggregated the opponents' most-used first-round bet sizes**, picked **k=3** holes (by
  frequency × distance from the nearest abstract action), and **computed equilibrium responses overnight**
  (note 54: k chosen so ~3 holes fixable in 24 h). Converged branches were **added to the blueprint**.
- Crucially this is **NOT opponent exploitation / opponent modelling** — exploiting opens you to
  counter-exploitation. Libratus instead **patches its own strategy's holes**, and the fixes are
  **universal** (work vs any opponent). (Science; CMU news: "instead of finding and exploiting opponent
  mistakes, it finds and fixes its own weaknesses".)
- Two forms: (a) include a **default sibling bet size** during solving (don't assume the opponent only ever
  uses the added size); (b) **no default** (riskier/exploitative) — used during play only if the opponent
  actually uses that size most of the time.

**Where the classic pieces sit:** abstraction (Step 4) + MCCFR (Step 3) build the blueprint offline;
CFR+ (Step 3) does the online subgame solves; "search" = per-decision real-time subgame solving. **No neural
component** (contrast DeepStack / Step 5). Depth-limited solving theory (Brown & Sandholm 2018) is the
unifying lens but post-dates Libratus.

## Design decisions
<!-- Why these choices; trade-offs made. -->
- **Keep the blueprint, fix it locally** (vs DeepStack's no-blueprint re-solving). The blueprint handles the
  average case cheaply via abstraction; real-time solving fixes abstraction error only where it matters
  (the larger, later rounds). (Science; rawStepsBg "key insight": 3 modules each cover the others' gaps.)
- **No card abstraction in early rounds** (rounds 1–2): they're small enough to afford full resolution; put
  the abstraction only where the state count explodes (rounds 3–4) and then dissolve it at play time via
  subgame solving. (Science.)
- **Estimates over upper bounds** in subgame solving — trades a small, *bounded* exploitability risk
  (Theorem 1, ≤2Δ) for much stronger empirical play (upper-bound/safe solving had historically lost to
  unsafe solving head-to-head; note 48 — its original purpose was just to save space). (Science.)
- **Unsafe once, then safe**: Libratus uses *unsafe* subgame solving the first time it reaches round 3
  (cheaper, needs less precomputation, empirically fine there) and *safe* solving thereafter (note 45).
- **Asymmetric abstraction** (more actions for the opponent) to cut translation error (IJCAI; Bard 2014).
- **Bet-size perturbation** (±0–8%) to deny the opponent a fixed target (note 49).
- **No opponent modelling by design** — robustness (low exploitability) prioritized over exploiting humans;
  the self-improver only fills the AI's *own* gaps (Science "Self-improvement"; CMU news).
- **CFR+ for subgames, MCCFR for the blueprint**: CFR+ converges faster in the small subgames where a
  precise solution is wanted; sampling-based MCCFR scales to the huge blueprint (note 46; IJCAI).

## Approaches tried / abandoned / evolved during development
<!-- The priority material: dead-ends, engineering compromises, things the paper under-describes. -->
- **Action translation → abandoned in the late game.** Rounding off-tree bets to the nearest abstract size
  (the prior standard, Ganzfried & Sandholm 2013) is shown to be **>10× more exploitable** than nested
  subgame solving (Table 2: 1465 vs 119 mbb/game). Libratus keeps translation **only** on rounds 1–2, and
  the self-improver exists precisely to chip away at that residual. So action translation is a known,
  acknowledged weak point that survives in early rounds.
- **Safe subgame solving was historically avoided.** Pre-Libratus, safe solving "performed substantially
  worse than unsafe solving head-to-head" and was used merely to save memory (note 48). Libratus's advances
  (estimates not bounds; de-emphasizing unimportant hands) are what made *safe* solving actually strong —
  i.e., the textbook-safe method had to be re-engineered, not adopted as-is.
- **Imperfect-recall abstraction "bucket fighting."** Because many distinct decision points share one
  bucket's strategy, their differing optima "fight." Regret-based pruning incidentally mitigates this by
  freezing unreached points — a fix discovered as a side effect, not the pruning's original purpose
  (Science).
- **The blueprint alone is *not* superhuman — it even loses to the prior bot.** Raw blueprint **lost** to
  Baby Tartanian8 by 8±15 mbb/game (Table 3). It is real-time subgame solving that flips this to +63 mbb/g.
  This is the clearest evidence that the offline strategy is a scaffold, not the product.
- **Self-improvement is opponent-*driven* but not opponent-*modelling*** — a deliberate, somewhat
  counter-intuitive choice: it uses opponents' bets only as a *search heuristic* for which holes to patch,
  then computes a GT (universal) response, explicitly forgoing exploitation to avoid being exploited
  (Science).
- **Under-described / in supplement or companion papers:** the exact abstraction-bucketing algorithm
  (deferred to the Baby Tartanian8 / Tartanian7 papers), the precise Estimated-Maxmargin LP/CFR machinery
  and proof (NeurIPS-17 subgame + Science supplement), the postprocessing variants on rounds 1–2, and most
  systems/compute detail (only fully laid out in IJCAI + the CMU course notes, not the Science main text).
- **Compute is enormous and largely hidden in the main text** (see below): the Science article gives almost
  no compute figures; they live in IJCAI and the course notes.

## Compute & cost
- **Total ~25 million core-hours** (IJCAI), Jan 2016–Jan 2017, on the **Bridges** supercomputer (Pittsburgh
  Supercomputing Center; ~800 HPE Apollo 2000 nodes, 28 cores + 128 GB each — Libratus used **only 14 of 28
  cores** per node as that was fastest; it was Bridges' single biggest user, ~half, in that window —
  CMU L13).
  - **~6M core-hours**: initial abstraction + blueprint equilibrium finding.
  - **~3M core-hours**: nested subgame solving (during the match).
  - **~3M core-hours**: self-improvement.
  - **~13M core-hours**: exploratory experiments + evaluation. (IJCAI.)
- **Operational footprint (CMU L13):** blueprint runs ≈ **1+195 nodes, ~1–8 weeks**; each real-time endgame
  solve ≈ **50 nodes, ~30–60 s**; each self-improver run ≈ **196–600 nodes, 8–30 h**; **2.6 PB** disk for
  strategies/snapshots; C++, OpenMP (intra-node) + MPI (inter-node).
- **No GPUs, no neural training** — the entire cost is CPU-bound CFR/abstraction. Contrast DeepStack, whose
  offline cost is CFR target-generation (~175 core-years for the turn net) but whose *play-time* cost is one
  GPU < 5 s. Libratus's play-time cost is the opposite: heavy (a small cluster, tens of seconds per late
  decision).
- **Accessibility:** the deployed system was firmly supercomputer-scale at both train and play time — far
  less reproducible by an individual than DeepStack's single-GPU agent. Code was **not released** (HUNL is
  played commercially; risk > benefit), only pseudocode in the supplement (Science Acknowledgments). The
  ideas, however, are application-independent and now run far cheaper on modern hardware/solvers.

## Evaluation setup & headline result
- **Exploitability micro-benchmarks (measurable only on small variants):** safe subgame solving cut
  exploitability **>4×** vs none (Table 1); **nested** subgame solving cut it **>10×** vs action translation
  (Table 2: no-nested 1465 → nested-unsafe 148 → nested-safe 119 mbb/game).
- **Head-to-head vs the prior best AI (full HUNL):** vs **Baby Tartanian8** (2016 ACPC winner): raw
  blueprint **−8±15**; blueprint+postprocessing **+18±21**; on-tree nested solving **+59±28**; full nested
  solving **+63±28** mbb/game (Table 3). For scale, Baby Tartanian8 beat the next two ACPC AIs by 12±10 and
  24±20. **This head-to-head is something DeepStack never reported** — a key evaluation contrast.
- **Human match:** *Brains vs. AI: Upping the Ante*, **January 2017**, Rivers Casino Pittsburgh, **20 days,
  120,000 hands**, **4 top HUNL specialists** (Jason Les, Dong Kim, Daniel McCauley, Jimmy Chou), $200,000
  prize pool. Libratus won by **147 mbb/game**, **99.98% significance, p=0.0002** (hands treated as iid; note
  57), and **beat each human individually** (Science).
- **Variance handling contrast:** Libratus reached significance the "brute-force" way — **120,000 hands**,
  *no* AIVAT-style estimator (the result is the raw win rate). DeepStack instead used **AIVAT** to reach
  significance in ~3,000 hands. (Science; cf. DeepStack notes.) The 2017 competition also used a mirrored/
  duplicate hand structure across the human team to damp card luck (competition format; CMU coverage).
- **Win-rate unit:** mbb/game = milli-big-blinds per game = avg big blinds won per 1,000 hands; ~50 mbb/g is
  a large pro edge, so 147 mbb/g is decisive (note 57).

## Known criticisms / limitations
- **Two-player zero-sum only.** Like DeepStack, the safety machinery (Nash, safe subgame solving) leans on
  2p0s structure; multiplayer is out of scope (→ Pluribus).
- **Still abstraction-based**, and still uses **action translation on rounds 1–2** — an acknowledged
  exploitable seam that the self-improver only *narrows*, never closes (Science).
- **No neural generalization.** Everything is tabular: the blueprint is enormous (multi-TB; 2.6 PB of
  storage across snapshots), and nothing generalizes across situations the way a value net does. This is the
  thread DeepStack/ReBeL/SoG pick up.
- **Supercomputer-scale at play time** (≈50 nodes, tens of seconds/decision) — not deployable on commodity
  hardware, unlike DeepStack's single GPU.
- **Estimated-Maxmargin trades a (bounded) exploitability risk** for strength: using estimates rather than
  upper bounds can, in principle, raise exploitability above the blueprint (bounded by 2Δ, Theorem 1).
- **Unsafe subgame solving used once** at the first round-3 entry (note 45) — a pragmatic crack in the
  otherwise-"safe" story.
- **Evaluation caveat:** humans and AI both adapted, so iid significance is only "intuition"; still,
  147 mbb/g over 120k hands is unambiguous (note 57). No public code for independent verification.

## Comparison dimensions (for the master table)
- **Year:** 2017 (competition Jan 2017; IJCAI 2017; *Science* Dec 2017 / 2018 issue 359:418).
- **Players:** 2 (heads-up).
- **Game type:** HUNL — heads-up no-limit Texas hold'em (2-player zero-sum, imperfect information; ~10^161
  decision points).
- **Blueprint (offline)?:** **Yes** — an abstracted full-game strategy computed offline with MCCFR
  (the defining contrast with DeepStack). Detailed early, coarse late.
- **Neural component:** **None** — purely tabular CFR/abstraction (the contrast with DeepStack/ReBeL/SoG).
- **Search mechanism:** **Nested safe subgame solving** — real-time CFR+ re-solve of the late-game subgame,
  fitted to the blueprint, recomputed for every off-tree opponent bet.
- **Abstraction?:** **Yes** — card abstraction (rounds 3–4, blueprint only) + action abstraction
  (asymmetric); dissolved to *no card abstraction* in the real-time subgames.
- **Perfect-info too?:** **No** (imperfect-information only).
- **Compute:** Offline-heavy *and* online-heavy: ~25M CPU core-hours total on Bridges (~6M blueprint, ~3M
  subgame solving, ~3M self-improvement, ~13M experiments); ~50 nodes & tens of seconds per late decision;
  no GPUs.
- **Key innovation:** A **modular blueprint + real-time nested *safe* subgame solving + self-improvement**
  pipeline — the first to beat top HUNL pros, replacing action translation with provably-safe exact
  responses to off-tree bets.

## Modern relevance / legacy (2026 view)
<!-- Extrapolation requested for every system: how the core ideas map to current AI/ML, what is reusable,
and whether the system is obsolete or a living stepping stone. -->
- **Core idea that survived:** **real-time search on top of a precomputed strategy, made *safe* under hidden
  information.** "Solve the local subgame exactly at decision time, consistently with a coarse global
  strategy" is now standard; nested safe subgame solving is the direct ancestor of Pluribus's real-time
  search and a sibling of DeepStack's continual re-solving.
- **Direct lineage:** Libratus (2017) → **Pluribus** (2019, 6-player; same blueprint-MCCFR + depth-limited
  real-time search recipe, dropping safety guarantees it can't have) → the *depth-limited solving* theory
  (Brown & Sandholm 2018) that unifies it with DeepStack → **ReBeL** (2020), which replaces the hand-built
  blueprint + abstraction with **learned** PBS values while keeping the solve-in-the-loop idea.
- **The road *not* taken (and why it matters):** Libratus is the **high-water mark of the purely tabular,
  abstraction-based, no-neural-network paradigm.** It won *without* deep learning — but the field then moved
  to the *neural* thread (DeepStack→ReBeL→SoG), because abstraction + multi-PB blueprints don't generalize
  and don't scale past 2p0s. So Libratus is "superseded as an architecture, vindicated as a thesis":
  real-time search won, hand-crafted abstraction lost.
- **Frontier framing (test-time compute):** Libratus is an early, dramatic demonstration that **inference-
  time search can be worth more than a much larger precomputed model** — Brown later popularized this as the
  "test-time compute" thesis behind o1-style reasoning models (Sequoia 2024). The blueprint-then-search split
  prefigures pretraining-then-search.
- **Reusable subsystems today:** (1) **safe subgame/endgame solving** as a way to locally refine a global
  policy without breaking its guarantees — directly relevant to verified/constrained policy patching; (2)
  the **augmented-subgame "enter vs. take alternative value" gadget** (a clean way to pin local solutions to
  global value estimates); (3) **regret-based pruning** for scaling CFR; (4) the **self-improver pattern** —
  use observed play to *find and fix your own holes* rather than to exploit the opponent (a robustness-first
  alternative to opponent modelling).
- **Superseded parts:** hand-tuned card/action abstraction, the multi-PB tabular blueprint, and the
  CPU-cluster-at-play-time deployment — all replaced by learned value functions and neural generalization.
- **Verdict:** as a *deployed system*, superseded; as a *set of ideas*, half foundational (real-time safe
  search; search > scale) and half dead-ended (tabular abstraction). Thesis hooks: the **safe subgame-solving
  exploitability bound (≤2Δ)** is a template for Contribution 2 (safe exploitation under value error); the
  **self-improver's "fix your own holes, don't exploit"** stance is the foil against which Contribution 1
  (deliberate, *bounded* opponent adaptation) is defined.

## Hand-off → Pluribus (system #3; full treatment in subtask #3)
- Libratus leaves **two big things open**: (1) it is **two-player only** — its safety guarantees are
  Nash/2p0s-bound; (2) it remains **abstraction- and blueprint-heavy** with no neural generalization.
- Pluribus (Brown & Sandholm 2019) takes the **first** of these: it scales the blueprint-MCCFR + real-time
  depth-limited search recipe to **6-player** no-limit hold'em — where **Nash equilibrium is neither unique
  nor a safety guarantee** — and wins against pros anyway, **empirically** (notably on a fraction of
  Libratus's compute). It deliberately **drops** the safety guarantee Libratus prized: the open
  multiplayer-safety gap is exactly Contribution 2's target. (The neural-generalization gap is taken up later
  by ReBeL/SoG, not Pluribus.)
- So the bridge into Pluribus's section: *Libratus showed real-time safe search beats abstraction-and-
  translation in 2p0s; what happens when you remove the 2-player crutch the safety leans on?*
