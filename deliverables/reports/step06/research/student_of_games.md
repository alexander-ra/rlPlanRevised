# Student of Games (SoG) — Research Notes

> Gather sources and extract architectural detail BEFORE writing prose in
> ../summary/summaryEn.md. Cite every source so claims are traceable.
> System: Student of Games (Schmid et al., 2023). The FINAL system in the chapter.
> NOTE: the paper is long and the main text is high-level; the architecture/hyperparameters/
> compute/proofs live in the Supplementary Text. Lean on the Yannic Kilcher / Martin Schmid
> author interview + the DeepMind framing for the GT-CFR intuition, and on the primary paper's
> Materials and Methods for the precise mechanics, the two theorems, and the headline numbers.

## Sources consulted
<!-- Primary paper, supplement, author interview/talks, secondary deep-dives, the OpenSpiel ecosystem. -->
- **[Primary]** Schmid, M., Moravčík, M., Burch, N., Kadlec, R., Davidson, J., Waugh, K., Bard, N.,
  Timbers, F., Lanctot, M., Holland, G. Z., Davoodi, E., Christianson, A. & Bowling, M. (2023),
  "Student of Games: A unified learning algorithm for both perfect and imperfect information games",
  *Science Advances* **9(46)**, eadg3256. DOI: 10.1126/sciadv.adg3256. arXiv:2112.03178. — the main
  paper: the FOSG/public-belief-state setup, GT-CFR (regret-update + expansion phases), the CVPN,
  modified continual re-solving, sound self-play, **Theorem 1** (GT-CFR convergence) + **Theorem 2**
  (continual-re-solving soundness), and the chess / Go / HUNL poker / Scotland Yard + Leduc results.
  Cited as **(SoG)**.
- **[Correction — TITLE / naming history]** arXiv:2112.03178 was **first posted in Dec 2021 under the
  title "Player of Games" (PoG)**; it was **renamed "Student of Games" (SoG)** for the 2023 *Science
  Advances* publication. **Same paper, same 13 authors, same arXiv ID, same DOI.** Confirmed by: the
  current arXiv abstract (title = "Student of Games"); the *Science Advances* page; the v1 PDF
  (arxiv.org/pdf/2112.03178v1, title = "Player of Games"); the-decoder ("A first version of the paper
  was published in Arxiv in 2021, back then the system was called Player of Games"); and the Kilcher
  interview (titled "Player of Games", Jan 2022). **Consequence for citing secondary sources: the
  Kilcher/Schmid interview, the VentureBeat piece, and OpenSpiel all refer to the system as "Player of
  Games / PoG".** The chapter uses the published name **Student of Games / SoG** and notes PoG = SoG.
- **[Correction — cross-validates the ReBeL fix]** The SoG paper's own reference list (ref 37) cites
  ReBeL as **"N. Brown, A. Bakhtin, A. Lerer, Q. Gong"** — independently confirming the `research/rebel.md`
  correction that the fourth ReBeL author is **Qucheng Gong**, not "Hu". (Do not trust the planning files'
  bibliography; the SoG paper itself is the cross-check.)
- **[Author interview — primary intuition source]** Yannic Kilcher, "Player of Games: All the games, one
  algorithm! (w/ author Martin Schmid)" (YouTube, 2 Jan 2022, 54 min). https://www.youtube.com/watch?v=U0mxx7AoNz0
  — first author Martin Schmid walks through the algorithm: "PoG = a hybrid of **AlphaZero and
  DeepStack**"; the value function maps a *subgame (public state + range)* to per-information-state
  values; the search loop = "**expand the tree, improve the policy, expand the tree, improve the
  policy**" (because in imperfect info "the future changes the past", so after each expansion the whole
  tree must be re-converged with CFR before the next expansion); training = "**train the network to
  predict the result of the search**"; the two named limitations (large belief space; needs a known
  model — the MuZero gap). Cited as **(Kilcher/Schmid)**.
- **[Secondary — DeepMind framing + Schmid quote + compute]** K. Wiggers, "DeepMind makes bet on AI
  system that can play poker, chess, Go, and more", *VentureBeat* (2 Dec 2021).
  https://venturebeat.com/uncategorized/deepmind-makes-bet-on-ai-system-that-can-play-poker-chess-go-and-more/
  — Schmid (DeepMind) by email: "*PoG learns to play from scratch, simply by repeatedly playing the game
  in self-play. This is a step towards generality … while trading away some strength in performance.
  AlphaZero is stronger than PoG in perfect information games, but [it's] not designed for imperfect
  information games.*" Confirms training on **Google TPUv4** and the four challenge domains. Cited as
  **(VentureBeat)**.
- **[Secondary — plain-language summary]** M. Bastian, "Student of Games: Deepmind shows unified learning
  algorithm for games", *the-decoder* (2023).
  https://the-decoder.com/student-of-games-deepmind-shows-unified-learning-algorithm-for-games/ — the
  GT-CFR-grows-the-tree picture; the headline "**in Chess and Go, SoG lost 99.5% of games against
  AlphaZero … nevertheless plays at a very high amateur level**"; the PoG→SoG rename. Cited as **(the-decoder)**.
- **[Ecosystem — code/accessibility]** OpenSpiel (Lanctot et al., 2019, arXiv:1908.09453;
  github.com/google-deepmind/open_spiel) — DeepMind's RL-in-games framework from the same authors. It
  ships **CFR, CFR+, MCCFR, (Linear/Discounted) CFR, R-NaD**, and the **benchmark games** (Leduc,
  Liar's Dice, Scotland Yard, etc.), but **NOT a packaged GT-CFR / Student-of-Games agent** — the full
  SoG implementation and trained networks were *not* released (the *Science Advances* "Data and materials
  availability" mentions only data in the paper/supplement; no code release). So SoG is "open ecosystem,
  closed headline artefact". Cited as **(OpenSpiel)**.
- **[Lineage — closest relative, the BRIDGE-FROM]** Brown, Bakhtin, Lerer & Gong (2020), ReBeL, NeurIPS
  33 (arXiv:2007.13544). SoG §Related work: "**The most closely related algorithm is … ReBeL.**" Both
  combine search + learning + game-theoretic reasoning via self-play; differences: SoG is built on
  (safe) **continual re-solving + sound self-play**, **grows** the tree (vs ReBeL's fixed depth-limited
  subgame), and **decouples test-time search from training** (ReBeL's guarantees require the *same*
  algorithm at test time as in training), and is **validated across game types** (ReBeL: two
  imperfect-info games only). Bridge text in `research/rebel.md` "Hand-off → Student of Games". Cited as **(ReBeL)**.
- **[Lineage — the two parents]** DeepStack (Moravčík et al., 2017, *Science* 356; arXiv:1701.01724) and
  AlphaZero (Silver et al., 2018, *Science* 362). SoG = "**putting together AlphaZero and DeepStack into a
  single big unified algorithm**" (Kilcher/Schmid). From DeepStack: continual re-solving + a value
  function (PBS values) inside search; from AlphaZero: self-play + learned value/policy + a tree that is
  *grown* by guided expansion. SoG §Related work: "main difference from DeepStack is the use of
  substantially **less domain knowledge** (self-play instead of poker-specific heuristics; a **single
  network for all stages**)." Cited as **(DeepStack)**, **(AlphaZero)**.
- **[Component — decomposition / re-solving]** Burch, Johanson & Bowling (2014), "Solving Imperfect
  Information Games Using Decomposition", *AAAI* (SoG ref 36) — the subgame-decomposition + auxiliary-game
  (gadget) machinery SoG's modified continual re-solving builds on. Cited as **(Decomposition)**.
- **[Component — the soundness notion]** Šustr, Schmid, Moravčík, Burch, Lanctot & Bowling (2020),
  "Sound Search in Imperfect Information Games", *AAMAS* (SoG ref 20) — defines *sound* search (searches
  must stay consistent with one another and with the value function); SoG's "sound self-play" is this
  applied to data generation. Cited as **(Sound search)**.
- **[Modern relevance — the model-learning frontier]** MuZero (Schrittwieser et al., 2020, *Nature* 588)
  — the AlphaZero successor that *learns* the environment model. In the interview Schmid places SoG
  "behind the AlphaZero lineage" on exactly this axis: SoG **needs a known model**, MuZero does not. Cited
  via **(Kilcher/Schmid)**; named as **MuZero**.
- **[Modern relevance — beyond 2p0s]** CICERO (Bakhtin et al., 2022, *Science* 378:1067–1074; SoG ref 64)
  — search + learning + game-theoretic reasoning in 7-player, mixed-motive, natural-language Diplomacy:
  the same paradigm applied to a setting *outside* SoG's 2p0s guarantees. Cited as **(CICERO)**.
- **[Modern relevance — test-time compute]** Noam Brown, Sequoia "Training Data" podcast (2024) — the
  DeepStack→ReBeL→SoG search-at-train-and-test thread as an early instance of inference-time deliberation
  (shared thread with the other research notes). Cited as **(Sequoia 2024)**.

---

## Architecture / component breakdown
<!-- Offline (training) vs online (play) components; where NN / CFR / search sit. -->

SoG = **AlphaZero's self-play-with-search loop, with MCTS replaced by GT-CFR (a sound, CFR-based search)
and the value/policy net defined over public belief states** — so the *same* algorithm is sound for both
perfect- and imperfect-information games (SoG abstract, §Discussion; Kilcher/Schmid). Two main components
(SoG §Discussion): **(1) GT-CFR** (the search) and **(2) sound self-play** (the learning procedure that
trains the **CVPN**). It is best understood as the **synthesis of its two parents** — AlphaGo/AlphaZero
(self-play + learned value/policy + a tree grown by guided expansion) and DeepStack (continual re-solving
+ a belief-conditional value function inside the search) — "putting AlphaZero and DeepStack into a single
big unified algorithm" (Kilcher/Schmid; SoG §Related work).

**State representation — public belief states (the ReBeL/DeepStack lineage).** SoG uses the
**Factored-Observation Stochastic Games (FOSG)** formalism (SoG §Background; Kovařík et al. 2022). A
**public state** `s_pub` is the sequence of public observations (in HUNL: stacks/antes + betting history +
board). A **public belief state** is `β = (s_pub, r)`, where the **range** `r` is a *pair* of distributions
over each player's possible **information states** `S_i(s_pub)` — i.e., beliefs over what each player could
privately hold (SoG §Background, Fig. 1). **Perfect-information games are the special case** where each
public state has exactly one information state and the belief is a point mass — which is exactly why one
representation spans both classes (SoG §"Imperfect information search…"; Kilcher/Schmid: "all perfect
information games are just a special case where you have a single possible state").

**(1) GT-CFR — Growing-Tree CFR (the search).** GT-CFR "runs a CFR variant on a public game tree that is
**incrementally grown** over time" (SoG §"Search via GT-CFR"). It starts from an initial tree `L^0`
(the current public state `β` and its children) and alternates **two phases per iteration `t`**:
- **Regret update phase.** Run several iterations of **public-tree CFR** on the *current* tree `L^t`
  (simultaneous updates, **regret-matching⁺**, linearly-weighted policy averaging — i.e., CFR⁺). At each
  *leaf* of the current tree, **query the CVPN** at that leaf's belief state `β'` to get
  `f_θ(β') = (v, p)`, and use the values `v` as the counterfactual-value estimates for the subgame below
  the leaf (SoG §3.2.1). This is depth-limited CFR-with-decomposition: the net stands in for "everything
  below the frontier".
- **Expansion phase.** **Grow** the tree by adding new public states via **simulation-based expansion
  trajectories** (SoG §3.2.2). Sample an information state from the root beliefs, sample a world state,
  then descend by a **PUCT-guided** rule that *mixes* the learned prior/values with the current CFR
  policy: `π_select = ½·π_PUCT + ½·π_CFR`. When the trajectory hits an information state whose public
  state is **not yet in the tree**, add it (and update visit counts). This is the AlphaZero-style
  "expand toward the promising frontier" step, but it expands **public states**, not world states.
- **Notation `SoG(s,c)`:** `s` = total expansion simulations, `c` = expansion simulations per regret-update
  phase; total GT-CFR iterations = `s·⌈c⌉`. Chosen so `s` is directly comparable to AlphaZero's simulation
  count (SoG §Results; e.g., `SoG(8000,10)` = 800 GT-CFR iterations) (SoG §"Search via GT-CFR").
- **`k` — the one knob that adapts the search to the game class.** AlphaZero expands a *single* best
  action (optimal perfect-info policies can be deterministic). SoG expands the **top-`k`** actions by
  prior: **`k = 1` for perfect-information** games (efficiency — one good action suffices, MCTS-like),
  **`k = ∞` (all children) for imperfect-information** games (optimal policies are *stochastic*, so the
  search must keep and mix over multiple actions). With `k = ∞` SoG has a **finite-time** policy-quality
  guarantee, not only an in-the-limit one (SoG §"Search via GT-CFR"). This single switch is the technical
  embodiment of the unification: "reduces to MCTS-like search on perfect-info subtrees, CFR-like iteration
  on imperfect-info ones."

**(2) The CVPN — Counterfactual Value-and-Policy Network.** A *single* network `f_θ(β) = (v, p)` outputs
**counterfactual values `v`** (one per information state, per player) **and prior policies `p`** (one per
information state for the acting player) for the public state `β` (SoG §"CVPN", Fig. 6). One network does
both jobs (value + policy), for **all stages of the game** (vs DeepStack's separate per-round nets) — part
of the "less domain knowledge" claim. Architecture: "standard feed-forward networks and residual networks"
(poker = feed-forward MLP; chess/Go mirror older AlphaZero-style residual nets), details in Supplementary
Text (SoG §"CVPN"; Kilcher/Schmid).

**(2′) Sound self-play (the training loop).** Each player, at each decision, runs a GT-CFR search and
samples an action; this generates two kinds of training data (SoG §Results, §"Data generation"):
- **Search queries** — the public belief states the CVPN was queried at during the regret-update phase.
  Each query is **re-solved by another (recursive) GT-CFR search** to produce **value targets** (this is a
  policy-improvement-by-decomposition step: the search output is a better estimate than the raw net, and
  the net is trained toward it). **Recursive queries** off the main line are added to the buffer with prob
  ≈ 0.1–0.2 so the net is accurate at *all* leaves a search might touch, not just the played line.
- **Full-game trajectories** — give **policy targets** (the search's output policy at played public states)
  and **TD(1)** value targets (the game outcome).
- **"Sound" self-play** = the searches generating data are kept **consistent** with one another and with the
  CVPN (the sound-search requirement of Šustr et al. 2020), achieved by running GT-CFR on the **modified
  safe re-solving auxiliary game**. The CVPN is trained by supervised learning — **Huber loss** for values,
  **cross-entropy** for policy — on a sliding-window replay buffer; actors generate data while trainers fit
  new nets and periodically push them to the actors (asynchronous, distributed; SoG Fig. 8).

**Modified continual re-solving (the generalization beyond poker).** DeepStack's continual re-solving
exploited *poker-specific* properties (strict turn-taking; fully observable actions; the opponent's max
counterfactual value can always be retrieved from the last search). Scotland Yard breaks these (partially
observable actions). So SoG uses a **more general re-solving**: it starts from `s_pub^prev`, the state in
the *previous* search tree closest to the current `s_pub`, initializes a tree with a single branch
`s_pub^prev → s_pub` (off-branch actions as leaves), then **constrains GT-CFR's expansion to grow only
under `s_pub`** (focusing computation on the current decision). It keeps DeepStack's **gadget** (Burch et
al. 2014) and **mixes in the previous opponent range** with `α = 0.5` (regularization that "empirically
improves performance") (SoG §"Modified continual re-solving").

**Where the classic pieces sit:** **CFR/CFR⁺** (Step 3) is the search engine (in the regret-update phase);
**value+policy neural approximation** (Step 5) is the CVPN at the frontier; **PBS / decomposition** (the
ReBeL/DeepStack lineage) is the representation that makes leaf values well-defined; **no card/information
abstraction** (Step 4 is dissolved by the net — the only abstraction is a small *randomized betting* menu
in poker). The novelty is **GT-CFR** (the growing tree) + **sound self-play** binding them into one
algorithm sound for both game classes.

## Design decisions
<!-- Why these choices; trade-offs made. -->
- **Replace MCTS with GT-CFR — the whole point.** MCTS is *unsound* for imperfect information (it assumes
  values can be backed up locally, but under hidden info "you cannot glue together optimal sub-policies" —
  the future changes the past) (SoG §Tree-search; Kilcher/Schmid). CFR is sound there. SoG keeps
  AlphaZero's *grown, guided* tree but runs CFR on it, getting soundness for **both** classes at the cost
  of perfect-info efficiency (SoG §"SoG, like AlphaZero…").
- **Grow the tree instead of fixing a depth-limited subgame (vs ReBeL/DeepStack).** A fixed depth-limited
  tree wastes computation uniformly; GT-CFR is **anytime** and expands **non-uniformly toward the relevant
  states** (guided by the policy net), which matters for the **long horizons** of Scotland Yard (24 rounds)
  that a fixed shallow subgame cannot capture (SoG abstract, §Descriptions; ReBeL contrast).
- **`k = 1` vs `k = ∞` per game class** (above) — the single switch that makes one search sound and
  efficient for perfect info and sound (with a finite-time guarantee) for imperfect info.
- **One CVPN for all game stages, trained from self-play (vs DeepStack's per-round nets + handcrafted PBS
  sampling).** This is the core "**substantially less domain knowledge**" decision (SoG §Related work).
- **Decouple test-time search from training (the key advantage over ReBeL).** ReBeL's soundness *requires*
  the same search at test time as in training. SoG can use **any** belief-based CVPN at test time and, like
  AlphaZero, **scale up search at test time** (AlphaZero trains at 800 sims but plays at far more) — SoG
  shows exactly this scaling (Fig. 4) (SoG §Related work; §Results).
- **Trade peak strength for generality, deliberately.** Schmid: a single algorithm "better than humans" at
  everything is the goal; "MCTS is probably always going to be ahead [in perfect info], but we don't really
  care" (Kilcher/Schmid; VentureBeat).
- **Match AlphaZero's network-call budget, do NOT claim SOTA.** For fair chess/Go comparison they equalize
  *network evaluations* rather than wall-clock/hardware, explicitly avoiding a state-of-the-art claim
  (SoG §Results; Kilcher/Schmid).
- **Keep a small randomized betting abstraction in poker** (20,000 → 4–5 actions) — the one domain-knowledge
  concession (like ReBeL's ≤9 bet sizes), flagged as removable future work (SoG §Results, §Discussion).

## Approaches tried / abandoned / evolved during development
<!-- Dead-ends, engineering compromises, what the paper under-describes. -->
- **DeepStack's poker-specific re-solving had to be replaced** (it relied on turn-taking + fully observable
  actions, absent in Scotland Yard) → the **generalized continual re-solving** from `s_pub^prev` with
  expansion constrained under `s_pub` (SoG §"Modified continual re-solving"). An evolution forced by going
  multi-domain.
- **`c` (expansions per regret update) is under-explored.** "Intuitively we would expect `c = 1` to be the
  best choice … we chose by hand a small number of values for `c > 1`. We did notice that `c = 1` is not
  always the best choice in practice and hope to explore this more thoroughly in the future." (SoG §Results)
- **Quadratic-time search, left unoptimized.** A GT-CFR re-solve with `T` iterations is `O(kT²)` public
  states/CVPN calls (the tree grows each iteration; perfect-info reduces to `O(T)`); the authors note the
  "absolute time cost could be reduced by running the regret-update and expansion phases in parallel" —
  i.e., they did not (SoG §"Performance guarantees"). 
- **Main text is high-level; the engineering is in the Supplementary Text.** The network *architectures*,
  hyperparameters, full pseudocode, the **randomized betting abstraction**, the exact rule for assigning
  value targets (a hyperparameter), the **compute**, and the **proofs of Theorems 1–2** are all in the
  supplement; the main paper states the theorems "only informally" (SoG §Theoretical results,
  §Materials and methods).
- **The training-convergence argument is idealized.** "The training process converges to the optimal values,
  asymptotically, as `T → ∞` and with very large (**exponential**) memory" — an in-principle guarantee;
  practice depends on the net's capacity (SoG §"Consistency of training process").
- **Skipping search at test time degrades play** (tried in spirit): the policy net alone "still plays quite
  good chess, but is far below the full strength of search" — search is necessary, not decoration
  (Kilcher/Schmid).
- **Could have beaten Slumbot by more.** The +7 mbb/hand poker margin is deliberately modest — "we could
  have beaten Slumbot by a lot more, we just decided this is good enough to put into a paper"; the point is
  generality, not max poker strength (Kilcher/Schmid).

## Compute & cost
<!-- TPU-scale training, comparable to AlphaZero; the contrast with Pluribus's $150 and ReBeL's GPUs. -->
- **Training is TPU-cluster-scale, by design comparable to AlphaZero.** AlphaZero baseline: 800 MCTS sims,
  **3,500 concurrent actors each on a single TPUv4**, 800,000 training steps; **"SoG was trained using a
  similar amount of TPU resources"** (SoG §Results). Trained on **Google TPUv4** (VentureBeat). Per-domain
  training-step counts: chess `SoG(400,1)` 3M steps; Go `SoG(400,1)` 1M steps; poker `SoG(10,0.01)` ≤1.1M
  steps; Scotland Yard up to **17M steps** (SoG §Results).
- **Go is the most expensive; poker/Scotland Yard the cheapest.** Schmid: "by far the hardest is Go where we
  used a lot of TPUs … chess [and poker] people can probably train on a few GPUs" (Kilcher/Schmid).
- **Compute is reported *relatively*, not absolutely.** They equalize **network-call budget** with AlphaZero
  rather than wall-clock, explicitly *not* claiming to be stronger; so there is no clean "X core-hours /
  $Y" number like Pluribus's ~$150 — only "similar to AlphaZero" (SoG §Results; Kilcher/Schmid).
- **Search complexity:** `O(kT²)` public-state visits/CVPN calls per re-solve (tree grows each iteration);
  **`O(T)` for perfect-info** (`k=1`, ranges are scalars, a state is evaluated once and re-scaled). "Neural
  network evaluations account for most of the run time" (SoG §"Performance guarantees").
- **Listed limitation:** "**substantial computational resources are used to attain strong play** in challenge
  domains; an interesting question is whether this level of play is achievable with less" (SoG §Discussion).
- **Accessibility / code:** the full **SoG/GT-CFR implementation was NOT released** (no code-availability
  statement beyond "data in the paper/supplement"). The authors' **OpenSpiel** framework provides the CFR
  family + the benchmark games (Leduc, Liar's Dice, Scotland Yard), so the *components and environments* are
  open, but no packaged Student-of-Games agent or trained CVPN is downloadable. So on the headline-artefact
  axis SoG is closed (like Libratus/Pluribus, unlike ReBeL's open Liar's Dice), even though its building
  blocks live in an open library (OpenSpiel).

## Evaluation setup & headline result
<!-- chess, Go, HUNL poker, Scotland Yard + Leduc / small Scotland Yard for exploitability. -->
- **Four challenge games across both classes:** perfect-info **chess** and **Go**; imperfect-info **HUNL
  poker** and **Scotland Yard**. Plus small games where exploitability is computable: **Leduc poker** and a
  **small Scotland Yard map ("glasses")** (SoG §Experimental results). HUNL setup: blinds 100/50, **200-bb
  stacks** (SoG §Descriptions). Scotland Yard: Mr X (evader) vs a **detective team** (treated as one player)
  on a London graph, ≤24 rounds, Mr X visible only on specific rounds — i.e., **two-player zero-sum** (team
  vs evader), with *partially observable actions* (a different kind of hidden info than poker).
- **Chess (relative Elo, Stockfish-1-thread = 0):** `SoG(60000,10)` = **+420**, *above* Stockfish(4 threads,
  1 s) = +382, *below* AlphaZero(8000) = +455 and AlphaZero(60000) = +592. → "stronger than Stockfish using
  4 threads and 1 s; **weaker than AlphaZero**, gap **smaller in chess**" (SoG Table 1, §Results).
- **Go (relative Elo, GnuGo = 0):** `SoG(16000,10)` = **+1970**, *>1100 Elo above* Pachi(100k) = +869;
  AlphaZero(8000) = +2875, AlphaZero(16000) = +3139. `SoG(16000,10)` wins only **0.5% (2/400)** vs
  AlphaZero(8000) → "**lost 99.5%**" to AlphaZero (the-decoder). "Top human amateur, possibly professional
  level"; **weaker than AlphaZero, gap larger in Go** — hypothesized: **MCTS is more efficient than CFR on
  perfect-info games — the price of generality** (SoG Table 1, §Results).
- **Scalability (Fig. 4):** both SoG and AlphaZero improve Elo with more network evaluations — SoG **scales**
  with compute, just from a lower curve than AlphaZero (SoG §Results).
- **HUNL poker (Table 2, AIVAT-corrected, vs Slumbot2019 = best open-source HUNL bot):** `SoG(10,0.01)`
  (≤1.1M steps) wins **+7 ± 3 mbb/hand** (3.1M matches); vs **LBR** (local best response, fold/call +
  poker heuristic) SoG wins **+434 ± 9 mbb/hand** and **LBR fails to find an exploit**. Context from the
  same table: ReBeL +45 vs Slumbot; DeepStack +428 vs LBR; Supremus +176/+951. SoG's Slumbot margin is
  *smaller* than ReBeL's, but SoG is a **unified, minimal-domain-knowledge** algorithm, not a poker
  specialist, and "could have beaten Slumbot by a lot more" (SoG Table 2; Kilcher/Schmid).
- **Scotland Yard (Fig. 5, vs PimBot = state-of-the-art MCTS + determinization + heuristics):**
  `SoG(400,1)` (17M steps) **beats PimBot even at 10 million search simulations (55% win rate)**, while SoG
  searches "a tiny fraction" of the game; PimBot **stops improving** with more search (1M and 10M perform
  the same vs SoG) — illustrating sound learning + search beating a heuristic, unsound searcher (SoG §Results).
- **Exploitability (Fig. 3, Leduc + glasses Scotland Yard):** exploitability **drops with more training
  (lower ε) and more search (larger T)** — the empirical face of Theorem 1, and "**unlike any pure RL
  algorithm**", which is not guaranteed to reduce exploitability with more training (SoG §Results, §Discussion).

## Known criticisms / limitations
<!-- generality vs peak performance; belief-space blowup; known-model requirement; betting abstraction; compute. -->
- **Generality vs peak performance (the central trade-off).** SoG is **weaker than AlphaZero in chess and
  Go given the same resources** — explicitly "the price of SoG's generality" (CFR < MCTS in efficiency on
  perfect info). Strong (expert/pro amateur) but not SOTA in perfect-info games (SoG §Results, §Discussion;
  VentureBeat).
- **Belief-space blowup — Schmid's "main limitation".** SoG "**requires enumerating the information states
  per public state, which can be prohibitively expensive in some games**"; the CVPN's output scales with the
  number of possible private states (in HUNL, ~1,326 hands; far worse elsewhere) → "this is going to fall
  apart if there's a big belief space" (SoG §Discussion; Kilcher/Schmid). **This is the same scaling wall as
  ReBeL's PBS.** Mooted fix: a generative model that *samples* world states instead of enumerating.
- **Needs a known model of the environment (the MuZero gap).** Like AlphaZero (and ReBeL), SoG assumes a
  perfect simulator / known rules; "we currently need a model of the environment and **MuZero doesn't even
  need it** … you can think of PoG as running behind the AlphaZero lineage and trying to generalize, but we
  are still behind in that regard" (Kilcher/Schmid).
- **2p0s for the guarantees.** "Here, we focus on the **two-player zero-sum** setting"; "the theoretical
  guarantee of Nash equilibria outside of this setting is less meaningful … (for example, in games with
  more than two players)." So, like ReBeL, SoG unifies *information structure* (perfect ↔ imperfect) but
  **not player count** — the multiplayer-safety gap (Pluribus's) is *still* open even in the most unified
  system (SoG §Background, §Discussion). → master-table "Players" = 2 / two-player zero-sum (Scotland Yard's
  detectives are one team), exactly as ReBeL.
- **Still keeps a (randomized) betting abstraction in poker** (20,000 → 4–5 actions) — removable in future
  via a general large-action-space reduction (SoG §Discussion).
- **Substantial compute** (TPU-scale; see above) and **quadratic-time search**, both flagged as open
  efficiency questions (SoG §Discussion, §"Performance guarantees").
- **Closed headline artefact:** no SoG agent / network release (only the OpenSpiel ecosystem of components).

## Theoretical results (the signature equation)
<!-- Theorem 1 = GT-CFR convergence; Theorem 2 = continual-re-solving soundness. -->
- **Theorem 1 (GT-CFR convergence; SoG Materials & Methods).** With `N(L)` = tree **interior** (non-leaf,
  non-terminal public states where GT-CFR computes a policy), `F(L)` = **frontier** (non-terminal leaves
  where GT-CFR uses **ε-noisy** CVPN value estimates), `U` = max counterfactual-value gap, `A` = max
  actions, the player-`i` regret after `T` GT-CFR iterations is bounded by

  ```
  R_i^T  ≤  Σ_{t=1..T} |F(L^t)|·ε   +   ( Σ_{s∈N(L^T)} |S_i(s)| )·U·A·√T
  ```

  The **first term** is accumulated **value-function error** at the growing frontier (the price of imperfect
  intuition); the **second term** is **ordinary CFR regret** in the interior (the `√T` growth). Dividing by
  `T` (exploitability ~ average regret), this gives **exploitability ≲ (frontier)·ε + (interior)·U·A/√T =
  O(ε) + O(1/√T)**. The high-level statement: "the exploitability of the final GT-CFR policy is at most
  **O(1/√T)** … so long as the value function is reasonably accurate"; with **no** value error (`ε = 0`)
  GT-CFR provably **converges to a Nash equilibrium** (SoG §Theoretical results). **Crucially this holds for
  BOTH game classes** — the soundness statement is the same whether the tree is a perfect-info game tree or
  an imperfect-info public tree. This is the structural twin of **DeepStack's `k₁ε + k₂/√T`**, Libratus's
  `2Δ`, Pluribus's `R^T/T → 0`, and **ReBeL's `δC₁ + δC₂/√T`** — a value-error term + a CFR-`1/√T` term —
  but uniquely **decomposed into frontier (net) vs interior (CFR)** to reflect the *growing* tree, and
  uniquely **game-class-agnostic**.
- **Theorem 2 (continual-re-solving soundness; SoG Materials & Methods).** Over a whole episode of `D`
  re-solving steps, with interior size ≤ `N`, frontier ≤ `F`, the exploitability of the final SoG policy is
  bounded by `(5D+2)(Fε + NUA/√T)`. So exploitability **decreases with more compute (`T↑`) and lower value
  error (`ε↓`) and grows only *linearly* in game length `D`** — "similar to Theorem 1 of DeepStack, adapted
  to GT-CFR." Theorems 1+2 together = "the search is **sound** up to value-function error" (SoG §Theoretical
  results, §"Performance guarantees"). → **Signature equation choice for the section: Theorem 1's bound**
  (display the frontier-ε + interior-`√T` regret bound, note the `O(ε)+O(1/√T)` exploitability consequence,
  note it holds for both classes; mention Theorem 2's `(5D+2)` game-length factor in prose).

## Modern relevance / legacy (2026 view) — lands the chapter's arc + tees up synthesis
<!-- the unification thesis; AlphaZero+CFR; MuZero/CICERO; one algorithm for both classes. -->
- **The unification thesis (the capstone).** SoG is the chapter's end point on the third progression axis:
  not just abstraction→neural and solve-offline→learn-and-search, but **perfect- and imperfect-information
  play unified in one algorithm** — one search (GT-CFR), one network type (CVPN), one self-play loop, sound
  for both classes, demonstrated on chess, Go, HUNL poker, and Scotland Yard. It is the only system in the
  chapter whose "Perfect-info too?" answer is **YES** (SoG abstract, §Discussion).
- **AlphaZero + CFR, made convergent.** SoG = AlphaZero with MCTS swapped for a *sound* CFR-based search;
  it **reduces to AlphaZero-like (k=1, MCTS-like) search on perfect-info subtrees and to CFR-like iteration
  on imperfect-info ones**, with a convergence guarantee (Thm 1) covering both. The lesson the field took:
  *the* general recipe (self-play + learned value/policy + guided search) extends to hidden information once
  the search is made sound over beliefs (SoG; Kilcher/Schmid).
- **Relation to ReBeL (the predecessor it subsumes as the general framework):** most closely related; SoG
  **grows** the tree (vs fixed depth-limited), **decouples test-time search from training** (more test-time
  search ⇒ better play, like AlphaZero; ReBeL must match train/test search), and is **validated across game
  types** (ReBeL: imperfect-info only). SoG is the *general* sound-search framework ReBeL pointed toward.
- **Relation to MuZero (the open frontier):** SoG is the **CFR-generalized AlphaZero**; MuZero is the
  **model-learning** AlphaZero. SoG still needs known rules — so the natural next step is a **MuZero-style
  learned model + generative belief sampling** to kill *both* of SoG's named limitations at once (Kilcher/Schmid).
- **Relation to CICERO (beyond 2p0s):** CICERO applies search + learning + game-theoretic reasoning to
  **7-player, mixed-motive, natural-language Diplomacy** — the same paradigm in a setting **outside SoG's
  2p0s guarantees**, underscoring that SoG unifies *information structure* but not *player count* (SoG ref 64).
- **Test-time compute.** SoG's Leduc result — more **search at test time lowers exploitability**, "unlike any
  pure RL algorithm" — is a clean statement of the DeepStack→ReBeL→SoG "search-at-train-and-test" thread that
  Noam Brown later frames as **inference-time deliberation / test-time compute** (SoG §Discussion; Sequoia 2024).
- **Reusable subsystems today:** (1) **GT-CFR** — anytime, policy-guided *growing-tree* search usable for
  any game class; (2) the **CVPN** — a single value+policy net over belief states; (3) **sound self-play** —
  bootstrapping targets from recursive, mutually-consistent sub-searches; (4) **generalized continual
  re-solving** (domain-independent, not poker-specific); (5) the `k=1`/`k=∞` switch for adapting one search
  to deterministic vs stochastic optimal policies.
- **Superseded / limited:** DeepStack's per-domain handcrafted PBS sampling + per-round nets are dissolved
  (single self-play-trained CVPN). SoG's *own* limits — belief-space enumeration, known-model requirement,
  CFR<MCTS efficiency on perfect info — are the live frontiers (generative belief models; MuZero-style model
  learning; faster equilibrium search).
- **For THIS thesis (synthesis hand-off):** SoG is the **most general PBS-based sound-search framework**, so
  it is the natural ceiling/context for **Contribution 1** (its belief/range over information states is the
  PBS substrate to be enriched with opponent-*type* beliefs), and its **2p0s-only guarantee** ("Nash less
  meaningful beyond 2p0s") **re-states the exact gap Contribution 2 targets** — unifying game *classes* did
  not close the multi-agent *safety* gap. Capstone observation for subtask #6: **unification across
  information structure ≠ unification across player count.** Completes the per-system arc → master table +
  evolution diagram + component-reuse map (GT-CFR reuses CFR (Step 3); abstraction (Step 4) dissolved;
  value+policy nets (Step 5); PBS + continual re-solving (DeepStack/ReBeL)).

## Comparison dimensions (for the master table)
- **Year:** **2023** (Science Advances 9(46), 15 Nov 2023; arXiv:2112.03178 first posted Dec 2021 as "Player
  of Games").
- **Players:** **2 (two-player zero-sum)** — guarantees and evaluation are 2p0s; Scotland Yard's detectives
  are treated as one team, so it too is 2-player zero-sum. The FOSG formalism is more general, but "Nash is
  less meaningful" beyond 2p0s (same nuance as ReBeL).
- **Game type:** **both perfect- AND imperfect-information** — the only unified system: chess + Go (perfect)
  and HUNL poker + Scotland Yard (imperfect). Reduces to AlphaZero-like search on perfect-info, CFR-like
  iteration on imperfect-info.
- **Blueprint (offline)?:** **No** — the offline product is the **trained CVPN** (a learned value+policy
  network), not a stored strategy table; like ReBeL, no precomputed blueprint.
- **Neural component:** **a single Counterfactual Value-and-Policy Network (CVPN)** — outputs both
  counterfactual *values* (per information state, per player) and a *prior policy*; one net for all game
  stages; feed-forward (poker) / residual (chess, Go).
- **Search mechanism:** **GT-CFR (Growing-Tree CFR)** — an anytime sound search that **alternates a CFR
  regret-update phase (with CVPN values at the leaves) and an AlphaZero-style PUCT expansion phase that
  grows the public tree**; used inside **modified continual re-solving** at every decision, at **both
  training and test time** (decoupled, unlike ReBeL). `k=1` (perfect info) / `k=∞` (imperfect info).
- **Abstraction?:** **None** of the card/information kind (the CVPN replaces it) — keeps only a small
  **randomized betting (action) abstraction in poker** (20,000 → 4–5 actions), like ReBeL's bet-size menu.
- **Perfect-info too?:** **YES** — the distinguishing row; the only system in the chapter demonstrated on
  perfect-information games (chess, Go), with the *same* algorithm/soundness covering both classes.
- **Compute:** **TPU-trained, comparable to AlphaZero** ("similar TPU resources"; Google TPUv4; Go the most
  expensive); reported *relative to AlphaZero's network-call budget*, no single $-figure; search is `O(kT²)`
  (`O(T)` perfect-info); flagged as "substantial". Full code/agent **not released** (OpenSpiel has the
  components + games, not a packaged SoG).
- **Key innovation:** **Growing-Tree CFR + sound self-play** — a single self-play-with-search algorithm,
  **sound for both perfect- and imperfect-information games**, that grows its search tree incrementally
  (guided by the policy net) with a CVPN evaluating unexpanded leaves; **provably converges to Nash
  (`O(ε)+O(1/√T)`, Thm 1–2) across both game classes** — "AlphaZero + DeepStack in one algorithm".

## Hand-off ← ReBeL (opening bridge material; full bridge text in research/rebel.md "Hand-off → Student of Games")
- ReBeL recovered **2p0s soundness** and removed abstraction + blueprint via **PBS + self-play RL + CFR
  search**, but: it is pitched/guaranteed for **imperfect-information 2p0s only** (it merely *reduces* to
  AlphaZero in perfect-info, it does not *unify* the classes); it assumes a **fixed depth-limited subgame**;
  its **test-time search must match training** (coupled); and its **PBS input blows up where common
  knowledge is scarce**.
- **Student of Games** takes the next step: a **single algorithm — GT-CFR + the CVPN — sound for BOTH
  perfect- and imperfect-information play**, **growing** the search tree incrementally rather than fixing a
  depth-limited subgame, **decoupling** test-time search from training, and demonstrated across **chess, Go,
  HUNL poker, and Scotland Yard**. It shares several **DeepStack authors** (Bowling, Moravčík, Burch, Schmid)
  — the **Alberta lineage** — in contrast to ReBeL's FAIR lineage.
- **Opening bridge (one phrasing):** *ReBeL recovered soundness for two-player zero-sum poker and threw out
  the abstraction and the blueprint — but it was still an imperfect-information method that merely* reduces
  *to AlphaZero in perfect-information games, solved a fixed depth-limited subgame, and tied its test-time
  search to its training. What if a single algorithm could play chess, Go, poker, AND Scotland Yard — growing
  its own search tree as needed, sound for perfect and imperfect information alike?*

## NO forward hand-off (SoG is the last system)
- There is **no successor section**. SoG's "Legacy & modern relevance" must instead **land the chapter's
  architectural arc** (abstraction→neural; offline-solve→learn-and-search; perfect/imperfect **unified**)
  and **tee up the synthesis** (subtask #6: master table, evolution diagram, component-reuse map) and the
  thesis hand-off to Steps 7–15 (Contribution 1 = enrich PBS with opponent-type beliefs; Contribution 2 =
  the multi-agent safety gap SoG's 2p0s-only guarantee leaves open).
