# ReBeL — Research Notes

> Gather sources and extract architectural detail BEFORE writing prose in
> ../summary/summaryEn.md. Cite every source so claims are traceable.
> System: ReBeL (Brown, Bakhtin, Lerer & Gong, 2020).
> NOTE: the paper is dense on THEORY (PBS, three soundness theorems) and thin on
> step-by-step architecture intuition -> lean on the Meta AI blog, the open-source
> repo, and Noam Brown talks for the architecture/intuition, and on the paper +
> Appendix D for the precise mechanics and the "far less domain knowledge" claim.

## Sources consulted
<!-- Primary paper, supplement/appendices, author talks, blogs, the open-source repo. Add links + 1-line relevance. -->
- **[Primary]** Brown, N., Bakhtin, A., Lerer, A. & Gong, Q. (2020), "Combining Deep Reinforcement Learning
  and Search for Imperfect-Information Games", *NeurIPS 33*. arXiv:2007.13544; official proceedings:
  https://papers.nips.cc/paper_files/paper/2020/file/c61f571dbd2fb949d3fe5ae1608dd48b-Paper.pdf — the main
  paper: the PBS conversion, Theorem 1 (infostate values = supergradient of the PBS value function),
  Algorithm 1 (the self-play RL+search loop), Theorem 2 (value-net error O(1/√T)), Theorem 3 (the soundness/
  safe-search bound), the HUNL + Liar's Dice + TEH experiments, the head-to-head + Dong Kim results, and
  Appendix D (domain knowledge deliberately dropped) + Appendix E (hyperparameters/compute). Cited as **(ReBeL)**.
- **[Correction — authorship]** The planning files (`planning/rawStepsBg`, `planning/cleanSteps`,
  `CHAPTER_PLAN.md`) cite the fourth author as **"Hu, Q."** This is **wrong**. Verified against arXiv, the
  NeurIPS proceedings, the Meta AI research page, and ML Anthology's BibTeX
  (`author = {Brown, Noam and Bakhtin, Anton and Lerer, Adam and Gong, Qucheng}`): the fourth author is
  **Qucheng Gong**, not "Q. Hu". Brown and Bakhtin are *equal-contribution* first authors. Correct citation:
  **Brown, Bakhtin, Lerer & Gong (2020)**. (This mirrors the Pluribus-notes correction of the bogus
  `arXiv:1911.07559` ID — do not trust the planning files' bibliographic framing.)
- **[Secondary, accessible]** Meta AI blog, "ReBeL: A general game-playing AI bot that excels at poker and
  more" (3 Dec 2020).
  https://ai.meta.com/blog/rebel-a-general-game-playing-ai-bot-that-excels-at-poker-and-more/ —
  plain-language architecture walk-through with the Figure 1–4 intuition: the modified Rock-Paper-Scissors
  failure of naïve search, the "referee announces strategies → continuous-state perfect-information game"
  picture, why CFR is used (convexity), the convergence guarantee, and the open-sourcing of the Liar's Dice
  implementation. Also names the limitation (Recon Chess; needs known rules; 2p0s-only). Cited as **(Meta blog)**.
- **[Open-source code]** facebookresearch/rebel, https://github.com/facebookresearch/rebel — "An algorithm
  that generalizes the paradigm of self-play reinforcement learning and search to imperfect-information
  games." The **Liar's Dice** implementation is open-sourced (PyTorch/C++); the **poker** code was
  deliberately *not* released (cheating risk — see Broader Impact). The sharp accessibility contrast with the
  closed Libratus/Pluribus. Cited as **(Repo)**.
- **[Author talk]** Noam Brown, "Combining Deep Reinforcement Learning and Search for Imperfect-Information
  Games" (ReBeL talk). https://www.youtube.com/watch?v=mCldyXOYNok — Brown's own framing: ReBeL is "AlphaZero
  for imperfect information"; PBS as the state on which value/policy are well-defined; CFR at the leaves +
  learned PBS value net; why this removes abstraction/blueprints. Cited as **(Brown talk)**.
- **[Predecessor — the bridge]** Brown & Sandholm (2019), "Superhuman AI for Multiplayer Poker", *Science*
  365:885–890. The system ReBeL bridges *from*: Pluribus closed the player-count gap but stayed purely
  tabular/abstraction-based with nothing learned that generalizes, and leaned on *unsafe* search with no
  guarantee. Bridge material in `research/pluribus.md` "Hand-off → ReBeL". Cited as **(Pluribus)**.
- **[Lineage — the idea ReBeL formalizes/generalizes]** Moravčík et al. (2017), DeepStack (*Science*
  356:508–513), arXiv:1701.01724 — the *first* use of a PBS value function during search; ReBeL explicitly
  builds on it but replaces DeepStack's random-PBS, handcrafted-feature, abstraction-near-the-end value-net
  training with self-play RL and no abstraction. Cited as **(DeepStack)**.
- **[Lineage — the unifying theory]** Brown & Sandholm (2018), "Depth-Limited Solving for Imperfect-Information
  Games", *NeurIPS 31*, arXiv:1805.08195 — the depth-limited-solving theory and the value-error → exploitability
  bound that all five systems instantiate; ReBeL's Theorem 3 is the learned-PBS-value version. Cited as
  **(NeurIPS-18 DLS)**.
- **[Component — the subgame solver]** Burch, Johanson & Bowling (2014), "Solving Imperfect Information Games
  Using Decomposition", *AAAI* — **CFR-D**, the depth-limited CFR-with-decomposition algorithm ReBeL runs
  inside each subgame (with a learned value function at the leaves). Cited as **(CFR-D)**.
- **[Component — convergence accelerator]** Brown & Sandholm (2019), "Solving Imperfect-Information Games via
  Discounted Regret Minimization", *AAAI* 33:1829–1836, arXiv:1809.04040 — **Linear CFR**, used so that the
  *random-iteration* test-time trick (Theorem 3) is not crippled by bad early iterations. Cited as **(AAAI-19 LCFR)**.
- **[Component — evaluation]** Burch, Schmid, Moravčík, Morrill & Bowling (2018), "AIVAT", *AAAI*,
  arXiv:1612.06915 — the variance-reduction estimator used in the Dong Kim match. Cited as **(AIVAT)**.
- **[Successor — forward lineage, NOT this section]** Schmid et al. (2023), "Student of Games", *Science
  Advances* 9(46), arXiv:2112.03178 — generalizes sound search via GT-CFR to perfect- *and*
  imperfect-information games; shares the PBS/sound-search lineage. Used only for the Legacy section's lineage
  note (the forward hand-off opens SoG's own section in subtask #5). Cited as **(SoG)**.
- **[Modern relevance]** Meta (2022), CICERO, "Human-level play in the game of Diplomacy by combining language
  models with strategic reasoning", *Science* 378:1067–1074 — planning/search with learned models in a
  7-player, mixed-motive, natural-language imperfect-information game; the "RL+search / planning" lineage
  beyond 2p0s poker. Cited as **(CICERO)**.
- **[Modern relevance — test-time compute]** Noam Brown, Sequoia "Training Data" podcast (2024) on o1 /
  test-time compute — frames RL+search (DeepStack→Libratus→Pluribus→ReBeL) as an early instance of
  inference-time deliberation. https://www.sequoiacap.com/podcast/training-data-noam-brown/ (shared thread
  with the DeepStack/Libratus/Pluribus notes). Cited as **(Sequoia 2024)**.

---

## Architecture / component breakdown
<!-- Offline vs online components; where NN / CFR / search sit. -->

ReBeL = **AlphaZero-style self-play RL** that trains **two neural nets defined on Public Belief States (PBS)**
— a **PBS value network** and (optionally) a **PBS policy network** — where the "search" run during *both*
training and test time is **CFR (CFR-D / CFR-AVG) solving a depth-limited subgame rooted at a PBS, with the
learned value net supplying leaf values** (ReBeL; Meta blog; Brown talk). Unlike DeepStack/Libratus/Pluribus
there is **no precomputed blueprint** and **no card abstraction** (lossy *or* lossless); unlike Libratus/Pluribus
there *is* a neural component and it is the heart of the system; unlike Pluribus it returns to **two-player
zero-sum (2p0s)** and **recovers a provable guarantee** (ReBeL; Appendix D).

**The key reframing (Section 4 — "From World States to Public Belief States"):**
- A **public belief state (PBS)** is a joint probability distribution over the players' possible *infostates*
  (private states), given the common-knowledge **public** observations and the (assumed common-knowledge)
  policies of all agents (ReBeL §3–4; Meta blog Fig. 3). Intuition (the blog's "referee" picture): imagine a
  game where players *cannot see their own cards* — a referee does, and each player instead announces, for
  every possible private card, the probability of each action; the referee samples the action for the player's
  *true* card. This "belief-representation" game is **strategically identical** to the original but contains
  **no private information** — it is a *continuous-state perfect-information game* whose state is the PBS
  (ReBeL §4; Meta blog).
- Because the belief representation is perfect-information, **values are well-defined on PBSs**: in 2p0s, every
  PBS β has a *unique* value V_i(β) with V₁(β) = −V₂(β), defined by both players playing a Nash equilibrium in
  the subgame rooted at β (ReBeL §4). This is exactly the property poker lacked at the level of public states
  (footnote 6: imperfect-information subgames rooted at a *public state* do **not** have well-defined values —
  you need the *belief* state). **This formalizes and generalizes DeepStack's belief-conditional values**
  (ReBeL §2: "ReBeL builds upon the idea of using a PBS value function during search, which was previously used
  in DeepStack").
- **Why not just run AlphaZero on the belief game?** The belief representation is a very high-dimensional
  *continuous* state/action space (the blog's running card example: 104-dim state, 156-dim action), so MCTS-style
  search is intractable. **But in 2p0s these are convex optimization problems**, so ReBeL searches with a
  **gradient-ascent-like iterative algorithm — CFR** — instead of MCTS (ReBeL §4; Meta blog). Theorem 1: the
  **infostate values** ReBeL's CFR uses are a **supergradient** of the (concave) PBS value function; so ReBeL
  learns an *infostate-value function* v̂ : B → ℝ^(|S₁|+|S₂|) rather than the scalar PBS value (ReBeL §4, Thm 1).

**The AlphaZero-style loop (Section 5, Algorithm 1):**
1. **Construct** a depth-limited subgame rooted at the current PBS β_r.
2. **Solve** it by running T iterations of CFR (CFR-D) **in the discrete representation**, but on each
   iteration set every leaf node z's value to v̂(s_i(z) | β_z^{π^t}) — i.e., the **learned value net** supplies
   leaf values, *conditional on the current iterate's beliefs at that leaf* (so leaf values change every
   iteration — this is what makes it sound under hidden information) (ReBeL §5.1).
3. **Add training data:** the average infostate-value vector at the root, (Σ_t v^{π^t}(β_r))/T, is added to the
   **value-net** dataset D^v; the average subgame policy π̄^T(β) at every PBS β in the subgame is (optionally)
   added to the **policy-net** dataset D^π (ReBeL §5.1–5.3).
4. **Recurse:** sample a leaf PBS β′_r (on a random CFR iteration t — important for soundness, see §test-time)
   and repeat from step 1 until the game ends. Then retrain the nets and iterate the whole loop (ReBeL §5.2).
- Solving is done in the **discrete representation** and converted to the belief representation; ReBeL is
  **flexible in the equilibrium-finder** — the paper shows results for **CFR-D**, the variant **CFR-AVG**
  (Appendix I), and even **fictitious play (FP)** / the novel **FLOP** (Fictitious Linear Optimistic Play,
  Appendix H) (ReBeL §5.1, §8).

**Where the classic pieces sit:** the **value/policy nets** (Step 5 neural approximation) are the learned
"intuition"; **CFR** (Step 3) is the search that solves each depth-limited subgame; **PBS** (the §4 reframing)
is the representation that makes value/policy functions well-defined and lets AlphaZero-style RL+search apply.
**No abstraction** (Step 4) anywhere — the neural value function *replaces* it. The nets are MLPs with GeLU +
LayerNorm; for poker, 6 hidden layers × 1536 units, with card embeddings (ReBeL §7, App. E).

## Design decisions
<!-- Why these choices; trade-offs made. -->
- **Return to 2p0s to recover guarantees.** ReBeL's theory (and experiments) are deliberately limited to 2p0s,
  where the PBS value is unique, the belief game is convex, and CFR converges to Nash — exactly the structure
  Pluribus gave up. The payoff is a *provable* soundness guarantee (Thm 3) that Pluribus could not have
  (ReBeL §3–4, §9; Meta blog "theoretical guarantees are limited to two-player zero-sum games").
- **CFR (not MCTS) for search**, because the belief game's high-dim continuous spaces are convex in 2p0s and
  CFR is a gradient-like solver for them; MCTS would be intractable (ReBeL §4; Meta blog).
- **Learn the value net from SELF-PLAY, not random PBSs** (the key advance over DeepStack). DeepStack trained
  its PBS value net on *randomly generated* PBSs (random belief distributions) + handcrafted features +
  end-game abstraction. ReBeL argues this is like "learning a value function for Go by randomly placing stones
  on the board" — most random PBSs never arise in real play. ReBeL instead generates training PBSs from
  self-play, so it learns values where they matter (ReBeL §2, §5.2, App. D; Brown talk).
- **Sample a leaf on a RANDOM CFR iteration** (uniform over iterations) for the recursive step, so the value
  net is accurate for the leaf PBSs that arise on *every* CFR iteration (leaf values shift each iteration)
  (ReBeL §5.2).
- **Safe search "for free" at test time (Theorem 3).** The same algorithm run at test time — *pick a random
  CFR iteration and assume all players' policies are those of that iteration* — yields a Nash policy *in
  expectation* with **no extra constraints**, unlike prior safe-search methods that bolt on constraints (which
  hurt performance and were never fully used in competitive agents). Crucially this also solves the "we don't
  know the opponent's policy → we don't know the PBS" problem at test time (ReBeL §6, Thm 3).
- **Use Linear CFR** so that picking a random (possibly very early) iteration is not disastrous — Linear CFR
  down-weights bad early iterations (ReBeL §6, §7; AAAI-19 LCFR).
- **Add off-tree opponent actions to the subgame and re-solve** (inherited from Libratus/Pluribus) rather than
  rounding — ReBeL keeps only a small (≤9) hand-chosen bet-size *action* abstraction during self-play but
  responds to any off-tree bet at test time by adding it (ReBeL §7, App. D).
- **One value net for all rounds; always solve only to the END OF THE CURRENT betting round.** A deliberate
  *minimal-domain-knowledge* choice: DeepStack used a separate net per "layer" and solved to the end of the
  game on round 3 (using round-4 abstraction); ReBeL uses a single net and solves to the end of the current
  round only — which forces it to learn **six** "layers" of values vs DeepStack's three, accepting more error
  propagation in exchange for dropping abstraction and per-round nets (ReBeL App. D).
- **Open-source Liar's Dice, withhold poker.** Liar's Dice is released to enable research; the poker agent is
  withheld because ReBeL can solve *arbitrary* stacks/bet sizes in seconds, which raises real cheating risk
  (ReBeL Broader Impact; Repo).

## Approaches tried / abandoned / evolved during development
<!-- The priority material: dead-ends, engineering compromises, things the paper under-describes. -->
- **Domain knowledge deliberately DROPPED (Appendix D — the "far less domain knowledge" claim).** ReBeL
  removes machinery that *every* prior top poker AI (DeepStack, Libratus, Pluribus) relied on:
  (1) **No information abstraction**, lossy *or* lossless — it computes a unique policy per infostate; the net
  input is just the belief distribution over each player's 1326 hands + board + pot/stack + a bet flag.
  (2) **No handcrafted PBS sampling** — training PBSs come purely from self-play (only ε=0.25 exploration).
  (3) **No precomputed all-in expected values** — it learns these itself.
  (4) **No "solve to the end of the game on round 3"** shortcut — always solves to the end of the *current*
  round, so it must learn 6 value layers (more error-propagation surface).
  (5) **A single value net for all situations** (DeepStack used one per round).
  The *only* prominent domain knowledge kept is an **action abstraction of ≤8–9 hand-chosen pot-fraction bet
  sizes** (perturbed ±0.1×pot in training), plus off-tree-bet handling (ReBeL App. D).
- **DeepStack's random-PBS value training — shown to FAIL.** Figure 2 (TEH): a value net trained on *uniform
  random* PBSs (no info abstraction) "fails to learn anything valuable"; self-play training is what makes the
  value net work. So the DeepStack-style recipe without abstraction does not transfer — self-play RL is the fix
  (ReBeL §8).
- **CFR-D's self-play weaknesses → CFR-AVG.** Plain CFR-D has properties that can hurt in a self-play setting,
  so the paper introduces **CFR-AVG** (Appendix I), which conditions leaf values on the *average* policy π̄^t
  rather than the current π^t. Honest caveat: the *efficient* implementation of CFR-AVG they use is **not known
  to be theoretically sound** ("Whether or not this modified form of CFR-AVG is theoretically sound remains an
  open question") even though it works well in poker (ReBeL App. A/I).
- **Safe search historically avoided.** Prior safe-search methods added constraints that "hurt performance in
  practice compared to unsafe search and greatly complicate search, so they were never fully used in any
  competitive agent" — every prior search-based IIG agent used *unsafe* search partly or entirely. ReBeL's
  contribution is showing safe search needs *no* extra constraints (the random-iteration trick) (ReBeL §6).
- **Theory assumes perfect function approximation / common knowledge of policies.** Theorems 2–3 assume an
  idealized value approximator and common-knowledge policies; §6 removes the test-time
  known-opponent-policy assumption, but the convergence theorems still idealize the net. Real nets have error
  δ, which is exactly what the Thm-3 bound is in terms of (ReBeL §5–6).
- **Under-described / in the appendices:** essentially all the architecture/precision lives in the appendices —
  Algorithm 1 detail + pseudocode (App. B), CFR-AVG (App. I), FLOP (App. H), domain knowledge (App. D),
  hyperparameters + the **compute/GPU** numbers (App. E), and the human-experiment protocol (App. E.1). The
  main text is the theory.
- **Compute is GPU-heavy and largely in the appendix** (see below) — the main text only says "data generation
  is the bottleneck; single machine for training, up to 128 machines × 8 GPUs for data generation."

## Compute & cost
<!-- ReBeL trains on GPUs — the contrast with Pluribus's CPU-only $150. Test-time is cheap. -->
- **Training is GPU-cluster-scale (the sharp contrast with Pluribus).** General statement (§7): "we use a
  **single machine for training and up to 128 machines with 8 GPUs each for data generation**" — i.e., the
  bottleneck is generating self-play CFR data, which is parallelized across a large GPU fleet. For the **full
  HUNL** agent (App. E): "We used **90 DGX-1 machines, each with 8 × 32 GB Nvidia V100 GPUs** for data
  generation" (= 720 V100 GPUs), single machine for training, results after **1,750 epochs** (1 epoch =
  2,560,000 examples; batch 1024; 12M circular replay buffer). This is a *fundamentally different* cost shape
  from Pluribus's **CPU-only, single 64-core server, ~$150** blueprint — ReBeL's "intuition" is bought with
  GPU deep-learning compute, not a cheap CPU CFR run. (ReBeL §7, App. E vs Pluribus.)
- **CFR itself runs on a single-thread CPU** (App. D): "We implement CFR only on a single-thread CPU and avoid
  any abstractions." The GPUs are for the *neural* data generation/training, not for CFR.
- **Test/play time is cheap.** In the HUNL human match the bot played **< 2 s per hand on average and never
  more than 5 s per decision**, and it **cached preflop subgames** to go faster (ReBeL §8, App. E.1). So like
  DeepStack, ReBeL is offline-heavy / online-light — but its offline heaviness is GPU deep learning, where
  DeepStack's was CPU CFR target-generation.
- **Smaller experiments are cheap:** the Liar's Dice / value-only setup used a 2-hidden-layer × 256-unit net,
  a **single GPU for training + 60 CPU threads** for data generation, 1024 search iterations (ReBeL App. E).
- **Accessibility:** the *method* is general and the **Liar's Dice implementation is open-sourced** (Repo) — a
  sharp accessibility contrast with the **closed** Libratus and Pluribus (whose code was never released). But
  reproducing the *HUNL* result at full strength needed a large V100 fleet, and the **poker code was withheld**
  (cheating risk). So: open method + open Liar's Dice code, but the headline poker artefact stayed closed and
  GPU-expensive to retrain (ReBeL Broader Impact; Repo).

## Evaluation setup & headline result
<!-- HUNL poker + Liar's Dice. -->
- **Metric:** exploitability (for the convergence experiments) and mbb/g (thousandths of a big blind per game)
  for head-to-head; **AIVAT** variance reduction in the human match (ReBeL §7–8; AIVAT).
- **HUNL head-to-head (Table 1), in mbb/g (±1 SD):** ReBeL beat **Slumbot +45 ± 5** and **BabyTartanian8
  +9 ± 4** (both prior Computer Poker Competition champions), and beat **LBR (local best response) +881 ± 94**
  in the restricted LBR setting. For comparison the table lists DeepStack only vs LBR (+383 ± 112) and Libratus
  vs BabyTartanian8 (+63 ± 14). ReBeL's BabyTartanian8 margin (+9) is smaller than Libratus's (+63), but ReBeL
  wins with **far less domain knowledge / no abstraction** (ReBeL §8, Table 1).
- **HUNL vs human (Appendix E.1 — the superhuman result):** ReBeL played **Dong Kim**, the top HUNL pro who
  had lost the *least* to Libratus, over **7,500 hands** (Kim played from home, up to 4 tables at once,
  incentive-compensated). **AIVAT (variance-reduced) score: Kim lost 165 ± 69** (one standard error) — i.e.,
  **ReBeL won by 165 mbb/g with statistical significance**; raw (unreduced) score was 358 ± 188. Bot: < 5 s/
  decision, < 2 s/hand, preflop caching (ReBeL §8, Table 1, App. E.1).
- **Liar's Dice (Table 2 — the generality demonstration):** ReBeL (CFR-D and FP variants), solving
  depth-2 subgames with 1,024 search iterations, converges to **approximate Nash** across 4 variants (1 die
  with 4/5/6 faces; 2 dice with 3 faces) — e.g., ReBeL CFR-D exploitability 0.017 / 0.015 / 0.024 / 0.017.
  Tabular full-game CFR does better per-iteration but becomes intractable as the game grows; the point is that
  ReBeL *generalizes* beyond poker (ReBeL §8, Table 2; Repo).
- **TEH (turn endgame hold'em, Figure 2):** ReBeL reaches exploitability equivalent to ~125 iterations of
  full-game tabular CFR; a value net trained on *random* PBSs fails — self-play is essential (ReBeL §8).

## Known criticisms / limitations
<!-- 2-player; PBS grows with players/low common knowledge. -->
- **2p0s only (theory and guarantees).** Theorems 1–3, the unique PBS value, and the convexity that justifies
  CFR-search all rely on two-player zero-sum structure. The algorithm *generalizes* (related techniques worked
  empirically with more players, citing Pluribus), but the **guarantees do not** (ReBeL §3–4, §9; Meta blog).
  → master-table "Players" nuance: state guarantees as **2p0s** even though the algorithm is more general.
- **PBS input grows with the number of infostates in a public state.** "The input to its value and policy
  functions currently grows linearly with the number of infostates in a public state" — intractable in games
  with **strategic depth but very little common knowledge**, e.g. **Recon(naissance) Blind) Chess**, where the
  belief space is huge. This is the headline scaling limitation, and it gets worse with more players (more
  hidden hands to believe over) (ReBeL §9; Meta blog "Conclusions").
- **Needs known, exact game rules.** Like AlphaZero (and unlike MuZero), ReBeL assumes the rules/dynamics are
  known — fine for poker/Liar's Dice, problematic for real-world settings; the blog notes a MuZero-style
  extension would be valuable (Meta blog).
- **Approximation error δ feeds the bound.** The guarantee is "up to value-net error" — real nets have δ > 0,
  so play is an δ-dependent approximate-Nash, not exact (ReBeL Thm 3).
- **CFR-AVG efficient variant possibly unsound** (open question), and theorems assume idealized approximation /
  common-knowledge policies (ReBeL App. A/I, §5–6).
- **Poker code withheld** (cheating risk); only Liar's Dice open-sourced — partial reproducibility for the
  headline poker result (ReBeL Broader Impact; Repo).

## Comparison dimensions (for the master table)
- **Year:** 2020 (NeurIPS 2020; arXiv:2007.13544, Jul 2020; Meta blog 3 Dec 2020).
- **Players:** **2 (heads-up).** Guarantees are **2p0s**; the algorithm generalizes to more players but
  *without* the guarantees (state precisely).
- **Game type:** general **2p0s imperfect-information** games; evaluated on **HUNL poker + Liar's Dice** (+ TEH).
  In perfect-information games ReBeL **reduces to an AlphaZero-like algorithm** (the differentiator: it *also*
  handles imperfect info via PBS).
- **Blueprint (offline)?:** **No precomputed blueprint** — instead a **learned PBS value (+policy) network**
  from self-play; the "offline" product is the trained net, not a stored strategy table.
- **Neural component:** **PBS value network** (+ optional **PBS policy network**) — MLP, GeLU/LayerNorm; for
  poker 6×1536 hidden, card embeddings, input = belief over each player's 1326 hands + board + pot + bet flag.
- **Search mechanism:** **CFR (CFR-D / CFR-AVG; also FP/FLOP) on a depth-limited subgame rooted at a PBS**,
  with the learned value net supplying (iteration-dependent) leaf values; **used at BOTH training and test
  time** (AlphaZero-style). Off-tree bets added & re-solved.
- **Abstraction?:** **None** — no card/information abstraction (lossy or lossless); the neural value function
  replaces it. Keeps only a small (≤9) hand-chosen **action** (bet-size) menu, with off-tree bets added live.
- **Perfect-info too?:** **Partially / by reduction** — ReBeL *reduces to an AlphaZero-like algorithm* in
  perfect-information games, but it is presented and evaluated as an imperfect-information method; it is **not**
  the unified perfect+imperfect system (that is SoG's claim). So in the spirit of the table: **No** (it is not
  pitched/evaluated as a perfect-information player), with the nuance that it *degenerates* to AlphaZero-style
  search if private info is removed.
- **Compute:** **GPU-trained** — full HUNL used ~90 DGX-1 nodes × 8 V100 for data generation, single training
  machine, 1,750 epochs; **a contrast with Pluribus's CPU-only ~$150**. CFR on single-thread CPU; play < 2 s/
  hand, ≤ 5 s/decision.
- **Key innovation:** **Public Belief States** + an **AlphaZero-style self-play RL loop that trains a PBS
  value (and policy) network with CFR run in belief space at the leaves** — the first *sound* RL+Search for
  imperfect-information games; recovers a **provable 2p0s Nash guarantee** while **eliminating abstraction and
  the precomputed blueprint**; code (Liar's Dice) open-sourced.

## Modern relevance / legacy (2026 view)
<!-- How the core ideas map to current AI/ML; what is reusable vs superseded; obsolete or living stepping stone. -->
- **Core idea that survived and generalized:** **recast hidden-information decision-making as a
  perfect-information problem over belief states, then apply the full RL+search (AlphaZero) machinery.** PBS is
  now the standard state representation for sound search in imperfect-information games (ReBeL §2–4; Brown talk).
- **Direct lineage:** DeepStack (belief-conditional leaf values, hand-crafted) → **ReBeL** (PBS value/policy
  *learned by self-play RL+search*, no abstraction, provably sound in 2p0s) → **Student of Games** (2023),
  which uses sound search over public/belief states with **GT-CFR** to unify **perfect- and imperfect-information**
  play in one algorithm (the forward hand-off that opens SoG's section). The PBS/RL+search idea also informs
  **CICERO** (2022), planning with learned models in 7-player, mixed-motive, natural-language Diplomacy — the
  "RL+search beyond 2p0s poker" direction (SoG; CICERO; Meta blog applications list).
- **Test-time compute framing:** ReBeL is the cleanest "AlphaZero for imperfect information" — search at both
  *training and test time* — and is part of the lineage Noam Brown cites as an early instance of **test-time
  compute / inference-time deliberation** now central to reasoning models (Sequoia 2024; Brown talk).
- **Reusable subsystems today:** (1) the **PBS state representation** itself (belief over infostates given
  public observations) — the foundation for belief-based opponent modelling (this thesis's Contribution 1
  extends PBS to *beliefs over opponent strategy types*); (2) **learned value (and policy) functions on belief
  states**, trained by self-play; (3) **CFR-as-search-at-the-leaves with a learned leaf evaluator**
  (CFR-D/CFR-AVG); (4) the **random-iteration "safe search for free"** trick (Thm 3) that needs no extra
  constraints; (5) **FLOP** as a simple fast equilibrium finder; (6) **add-the-off-tree-action-and-re-solve**
  (from Libratus/Pluribus).
- **Superseded / limited:** the **per-domain handcrafted features and abstraction** of DeepStack are dissolved
  by ReBeL's no-abstraction self-play; ReBeL itself is then **subsumed** by Student of Games as the *unified*
  perfect+imperfect framework. ReBeL's **own** limits — PBS input growing with infostates (fails under low
  common knowledge / many players), known-rules assumption — are live research frontiers (MuZero-style rules
  learning; scalable belief representations) (ReBeL §9; SoG).
- **Verdict:** as an *idea*, ReBeL is a living stepping stone — PBS + RL+search is foundational and very much
  alive; as a *deployed poker artefact* it is largely superseded by SoG and was never publicly released for
  poker. For THIS thesis it is the **starting point for Contribution 1** (PBS → richer belief state including
  opponent-type beliefs) and a counterpoint to Contribution 2 (ReBeL recovers 2p0s safety that Pluribus gave
  up, but cannot extend the *guarantee* to N players — the gap Contribution 2 targets) (cleanSteps; PLAN.md).

## Hand-off ← Pluribus (opening bridge material; full bridge text in research/pluribus.md "Hand-off → ReBeL")
- Pluribus closed the **player-count** gap but left two things open: it is **purely tabular/abstraction-based**
  (a giant lookup-table blueprint; nothing learned that *generalizes* across situations) and it leaned on
  **unsafe** search with **no exploitability/safety guarantee at all**.
- ReBeL takes the **generalization + soundness** thread (not the player-count one): it **returns to 2p0s** and
  **recovers a provable Nash guarantee** (up to value-net error) while **eliminating the hand-crafted
  abstraction and the precomputed blueprint** that *both* Libratus and Pluribus relied on — by learning **PBS
  value/policy networks** via **AlphaZero-style self-play with CFR search in belief space**.
- **Opening bridge (one phrasing):** *Pluribus won six-handed but stayed purely tabular and abstraction-bound,
  with nothing learned that transfers and no safety guarantee to lean on. What if we go back to two players —
  and instead of hand-crafting an abstraction and a blueprint, LEARN the values by self-play, the way AlphaZero
  does for chess — recovering the guarantees Pluribus gave up while throwing the abstraction out entirely?*

## Hand-off → Student of Games (system #5; NOT in ReBeL's section — opens SoG's section in subtask #5)
- ReBeL is 2p0s-guaranteed and is presented as an imperfect-information method (it *reduces* to AlphaZero in
  perfect-info games but is not pitched as a unified player). Its PBS input also blows up where common
  knowledge is scarce.
- **Student of Games** (Schmid et al., 2023) takes the next step: a **single** algorithm — **Growing-Tree CFR
  (GT-CFR)** + value/policy nets — that unifies **perfect- AND imperfect-information** play (Go, chess, poker,
  Scotland Yard), growing the search tree incrementally rather than assuming a fixed depth-limited subgame.
  (Forward hand-off belongs at the *start* of SoG's section, per the locked spine.)
