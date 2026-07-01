# DeepStack — Research Notes

> Gather sources and extract architectural detail BEFORE writing prose in
> ../summary/summaryEn.md. Cite every source so claims are traceable.
> System: DeepStack (Moravcik et al., 2017). PILOT system — also used to validate the spine.

## Sources consulted
<!-- Primary paper, author talks, blogs, secondary deep-dives. Add links + 1-line relevance. -->
- **[Primary]** Moravčík, Schmid, Burch, Lisý, Morrill, Bard, Davis, Waugh, Johanson, Bowling (2017),
  "DeepStack: Expert-Level Artificial Intelligence in Heads-Up No-Limit Poker", *Science* 356(6337):508–513,
  doi:10.1126/science.aam6960. Preprint: https://arxiv.org/abs/1701.01724 — full text **plus Supplementary
  Materials** (implementation details, lookahead tables, training compute, LBR tables, proof of Theorem 1,
  pseudocode). This is the backbone for every claim below; supplementary cited as "(Supp.)".
- **[Secondary, accessible]** Fermat's Library — annotated/explained edition of the DeepStack paper.
  https://fermatslibrary.com/s/deepstack-expert-level-artificial-intelligence-in-heads-up-no-limit-poker
  — confirms architecture/training passages verbatim; useful as a reader-friendly companion.
- **[Project page / code / talk]** University of Alberta CPRG DeepStack page (overview video + Leduc code
  release `lifrordi/DeepStack-Leduc`). https://poker.cs.ualberta.ca/publications/17science.pdf (paper mirror).
- **[Hand-off, system #2]** Brown & Sandholm (2018), "Superhuman AI for Heads-Up No-Limit Poker: Libratus
  Beats Top Professionals", *Science* 359(6374):418–424, doi:10.1126/science.aao1733 — used ONLY for the
  "what the next system fixes" hand-off (nested safe subgame solving; 147 mbb/g over 120k hands). Full
  treatment is subtask #2.
- **[Hand-off, accessible]** "Libratus: the world's best poker player", The Gradient (2018).
  https://thegradient.pub/libratus-poker/ — plain-language description of blueprint + nested safe subgame
  solving + self-improver.
- **[Context]** Lisý & Bowling (2017), "Equilibrium Approximation Quality of Current No-Limit Poker Bots"
  (LBR), arXiv:1612.07547 — the local-best-response method used to show prior bots are highly exploitable.
- **[Context]** Burch, Johanson & Bowling (2014), "Solving Imperfect Information Games Using Decomposition"
  (AAAI) — the re-solving / CFR-D gadget that continual re-solving generalizes.
- **[Context]** Bowling, Burch, Johanson & Tammelin (2015), "Heads-up Limit Hold'em Poker is Solved"
  (*Science*, Cepheus / CFR+) — the prior milestone (limit poker), contrasts the no-limit jump.
- **[Lineage / modern relevance]** Brown, Bakhtin, Lerer & Hu (2020), ReBeL (NeurIPS), arXiv:2007.13544 —
  "deep RL + search at both training and test time ... best exemplified by AlphaZero ... prior algorithms
  cannot cope with imperfect information"; generalizes DeepStack's depth-limit + learned-value idea via
  public belief states. (System #4; full treatment in subtask #4.)
- **[Lineage / modern relevance]** Schmid et al. (2023), Student of Games (*Science Advances*),
  arXiv:2112.03178 — unifies perfect/imperfect info; **shares DeepStack authors** (Schmid, Moravčík, Burch,
  Bowling). (System #5.)
- **[Modern relevance]** Bakhtin, Brown, Lerer et al. (2022), "Human-level play in the game of Diplomacy …
  (CICERO)", *Science* — self-play "operated similarly to AlphaZero and ReBeL by applying planning 'in the
  loop' … using a learned state value model"; the search+value recipe beyond 2p0s poker.
- **[Modern relevance]** Noam Brown, Sequoia "Training Data" podcast (2024) on o1 / test-time compute —
  frames the shift to inference-time deliberation; notes MCTS "works well for Go but … doesn't work in a game
  like poker," motivating belief-aware search. https://www.sequoiacap.com/podcast/training-data-noam-brown/

---

## Architecture / component breakdown
<!-- Offline vs online components; where NN / CFR / search sit. -->

DeepStack = **continual re-solving** (online) + **deep counterfactual value (CFV) networks** (trained
offline) + **sparse, depth-limited look-ahead**. There is **no stored full-game strategy ("blueprint")**.

**Offline (before play):**
- Train CFV networks that map a public state + both players' ranges → counterfactual values per hand.
- Three networks: **flop network** (values after the 3 flop cards), **turn network** (after the 4th card),
  and an **auxiliary pre-flop network** (speeds up early actions). (Paper, "Deep CFV Networks".)
- Training data = randomly generated poker situations solved with CFR+ (targets = solved CFVs).

**Online (during play), per decision (Paper Fig. 2; Supp. Algorithm 1):**
- Maintain two vectors only: **our own range** `r1` and the **opponent's counterfactual values** `v2`.
- Build a **look-ahead tree** rooted at the *actual* current public state, with a **restricted action set**
  and depth limited to the **end of the current betting round**.
- Run CFR (a vanilla-CFR/CFR+ hybrid) on that tree; at the depth limit, query the CFV network for leaf values.
- Sample an action from the averaged strategy; **discard the strategy**; update `r1` (Bayes) and `v2`.

Three ingredients, framed by the authors as the first *theoretically sound* heuristic search for
imperfect-information games: (1) sound local strategy computation (continual re-solving), (2) depth-limited
look-ahead with a learned value function ("intuition"), (3) restricted set of look-ahead actions. (Paper,
"DeepStack" section.)

**CFV network specifics (Paper "Architecture"; Supp. "Deep CFV Networks"):**
- Standard feed-forward net: **7 fully connected hidden layers × 500 units, PReLU**.
- Wrapped in an **outer zero-sum layer**: from the two players' ranges + raw CFVs it computes two game-value
  estimates that should sum to zero; it subtracts **half their actual sum** to enforce the zero-sum
  constraint. Fully differentiable → trained by gradient descent.
- **Inputs:** pot size (as a fraction of total stacks) + both players' ranges, encoded as distributions over
  **1,000 hand clusters** (k-means with earth-mover's distance over hand-strength features). Pre-flop aux net
  skips bucketing (only 169 strategically distinct pre-flop hands).
- **Outputs:** vector of counterfactual values per hand per player, as **fractions of the pot** (improves
  generalization).

**Where the classic pieces sit:** CFR/CFR+ = the online local solver (and the offline target generator);
neural net = the depth-limit leaf evaluator only; search = the per-decision re-solve. Card "abstraction"
(1,000 buckets) appears **only at the network input**, not as a constraint on what the player knows when
acting (Paper, "Relationship to abstraction-based approaches").

## Design decisions
<!-- Why these choices; trade-offs made. -->
- **Re-solve from the true public state, every action** → always "perfectly understands the current
  situation"; never needs to translate the opponent's bet into an abstraction (Paper, "Continual
  re-solving"; "Relationship to abstraction-based approaches").
- **Track opponent CFVs, not opponent range.** Continual re-solving needs only our range + a vector of
  opponent CFVs that upper-bounds what they could achieve (but ≤ what they'd get by deviating). Updates:
  own action → swap in re-solved CFVs for the chosen action + Bayes-update our range; chance → swap in the
  chance-action CFVs + zero now-impossible hands; **opponent action → no change needed** (Paper, update
  rules (i)–(iii)). This is what avoids action translation.
- **Depth limit = end of the round**, so the CFV net is only queried at the *start* of a round → no need to
  feed "bet faced" as a network input (Supp. "Continual Re-Solving").
- **Sparse betting set in look-ahead:** fold, call, 2–3 bet sizes, all-in (Paper, "Sparse lookahead trees").
  Supp. Table 5 shows **{F, C, P, A}** (pot-sized bet) is a sweet spot: cuts tree size hugely with little CFV
  error; per-round action sets in Supp. Table 4.
- **CFR variant:** hybrid of vanilla CFR + CFR+ (regret-matching+ but uniform weighting & simultaneous
  updates); early iterations omitted from the averages (Supp. "Continual Re-Solving").
- **Range gadget = CFR-D gadget** (Burch et al. 2014), chosen over the **max-margin gadget** (Moravčík et al.
  2016) because it "performed better in early testing" (Supp. "Continual Re-Solving").
- **Values as fractions of the pot**; **Huber loss + Adam**; 7 layers chosen as accuracy/speed/GPU-memory
  trade-off (validation barely improves past 5 layers at the 10M-sample budget) (Supp. "Number of Hidden
  Layers").

## Approaches tried / abandoned / evolved during development
<!-- The priority material: dead-ends, engineering compromises, things the paper under-describes. -->
- **Sparse action abstraction voids the soundness theorem.** Paper states plainly: restricting actions "voids
  the soundness property of Theorem 1, but it allows DeepStack to play at conventional human speeds." So the
  *deployed* system's guarantee is empirical, not proven. (Main text under-emphasizes this; details in Supp.)
- **Self-play values instead of best-response values.** Theorem 2 (Supp.) is proven for best-response
  constraint values, but **DeepStack actually uses self-play values** — "despite lacking a theoretical
  justification," because in early CFR-D tests they were *less* exploitable and stronger head-to-head (Supp.
  "Best-response Values Versus Self-play Values", Fig. 6). A real deviation between the proven and the shipped
  algorithm.
- **River is solved without a net, but with action bucketing.** On the turn, DeepStack solves to the *end of
  the game* (no river network); and it uses **a bucketed abstraction for all river actions** (Supp.
  "Continual Re-Solving"). So abstraction quietly returns at the river for tractability — a caveat the main
  text glosses.
- **Opponent-range warm-starting trades guarantees for speed.** To cut iterations, DeepStack warm-starts the
  opponent range (conservative blend when the opponent has already acted; **aggressive** forcing of a sampled
  estimated range when first to act, b=0.9) — the aggressive variant "sacrifices the re-solving guarantees
  when the opponent's range estimate is wrong" (Supp. "Opponent Ranges in Re-Solving").
- **Pre-flop is the expensive corner.** Re-solving pre-flop must enumerate all **22,100** flops through the
  flop net; the aux net is used only during the *omitted* CFR iterations, with the expensive enumeration kept
  for the averaged iterations, plus **caching of pre-flop re-solves** by betting sequence (Supp.).
- **Gadget choice was empirical**, not derived (CFR-D over max-margin, above).
- **Capacity is data-limited, not depth-limited** — echoes Step 5: more layers help only with more data
  (Supp. Fig. 5). Multiple Nash equilibria mean the CFV targets are non-unique, so reported Huber losses may
  *over*-state true error (Supp. "Neural Network Accuracies").
- **Under-described in the main text (all in Supp.):** the betting abstraction inside the look-ahead, the
  river action bucketing, the self-play-values deviation, range warm-starting, the per-round iteration counts
  (Table 4), and the actual training compute.

## Compute & cost
- **Turn network:** 10M turn situations solved with **1,000 iterations of CFR+** (actions F/C/pot/all-in),
  on **6,144 CPU cores** of Calcul Québec MP2 — **~175 core-years** (Supp. "Deep CFV Networks").
- **Flop network:** 1M flop situations solved via the depth-limited solver using the turn net — **~0.5
  GPU-year on 20 GPUs** (Supp.).
- **Auxiliary network:** 10M situations; targets by enumerating all 22,100 flops and averaging the flop net
  (Supp.).
- **Training each net:** Adam + Huber, mini-batch 1,000, lr 0.001→0.0001 after 200 epochs, ~350 epochs,
  **~2 days on a single GPU** (Supp. "Neural Network Training").
- **Play-time:** single **NVIDIA GTX 1080**; depth + sparsity bring each re-solve to **~10^7 decision points,
  solved in < 5 s**; measured means ~3 s/action, ~7 s/hand — faster than the human players (Supp. Table 7).
- **Contrast (the cost it avoids):** the abstraction baseline "Full Cards" (100 BB, no card abstraction,
  sparse bets + hard translation) took **~2 TB and ~14 CPU-years** to solve and is *still* exploitable by
  off-tree bets (Supp. "Local Best Response").

## Evaluation setup & headline result
- **Human study:** 33 professional players (17 countries), recruited via the International Federation of
  Poker; 3,000-game matches, Nov 7–Dec 12 2016; cash prizes to top 3. (Paper, "Evaluating DeepStack"; Supp.)
- **Variance control:** **AIVAT** (Burch et al. 2017) — provably unbiased low-variance estimator; here an
  **85% reduction in standard deviation**, enabling significance with as few as 3,000 games.
- **Result:** **44,852 games** played; 11 players completed the full 3,000. DeepStack won **492 mbb/g**
  unadjusted (> 4 SD from 0) and **486 mbb/g** by AIVAT (> 20 SD). Among the 11 completers ≈ **394 mbb/g**,
  beating **10 of 11** significantly; only the top human (≈ −70 mbb/g, i.e. losing) was not significant.
  Pros consider 50 mbb/g a sizable margin. (Paper + Supp. Table 2.)
- **Exploitability via LBR (lower bound):** prior ACPC bots are hugely exploitable — Hyperborean 4675,
  Slumbot 4020, Act1 3302 mbb/g (always-fold loses 750). **LBR could not find ANY positive exploitability
  for DeepStack** (it *loses* ≥ 350 mbb/g to DeepStack) under every action set tried (Paper Table 1; Supp.
  Tables 3, 6). Caveat: LBR is only a lower bound; "these experiments do not prove DeepStack is flawless,"
  and the flop (most CFV-net-dependent round) is the natural place to probe.

## Known criticisms / limitations
- **Two-player zero-sum only** (HUNL). No multiplayer; soundness machinery (Nash, re-solving safety) leans on
  the 2p-zero-sum structure.
- **Sparse betting abstraction remains** inside each re-solve (voids the formal guarantee) and **river uses
  action bucketing** — so DeepStack is "abstraction-light," not abstraction-free.
- **CFV-network approximation error** propagates to exploitability (Theorem 1's k₁ε term); flop net has the
  worst validation Huber loss (0.034 of pot vs turn 0.026).
- **Heavy offline compute** for the value nets (175 core-years for the turn net).
- **Per-decision online compute**; re-solves from scratch each action (mitigated by caching pre-flop).
- **No head-to-head vs the strongest abstraction bots or Libratus** — evaluation is vs humans + LBR only;
  the paper notes Libratus's contemporaneous, independent win (note 39).
- **Self-play-values shortcut** ships without proof (above).

## Comparison dimensions (for the master table)
- **Year:** 2017 (arXiv Jan 2017; *Science* Mar 2017).
- **Players:** 2 (heads-up).
- **Game type:** HUNL — heads-up no-limit Texas hold'em (2-player zero-sum, imperfect information; ~10^160
  decision points).
- **Blueprint (offline)?:** **No** full-game strategy stored. Offline work = training CFV nets, not a
  blueprint. (Contrast Libratus/Pluribus.)
- **Neural component:** **Deep counterfactual value networks** (flop, turn, aux) — value-only (no policy net).
- **Search mechanism:** **Continual re-solving** — depth-limited CFR look-ahead re-run every decision.
- **Abstraction?:** **No** abstraction constraining play; but 1,000-bucket hand clustering at the CFV-net
  *input*, sparse betting in the look-ahead, and river action bucketing. ("Lossless in principle, sparse in
  practice.")
- **Perfect-info too?:** **No** (imperfect-information only).
- **Key innovation:** Continual re-solving + learned deep counterfactual values = the **first sound heuristic
  search for imperfect-information games** — online local solving with no stored blueprint and no action
  translation.

## Modern relevance / legacy (2026 view)
<!-- Extrapolation requested for every system: how the core ideas map to current AI/ML, what is reusable,
and whether the system is obsolete or a living stepping stone. -->
- **Core idea that survived:** depth-limited search + a *learned value function at the leaves*, adapted to
  hidden information = the imperfect-info analogue of AlphaGo/AlphaZero value-guided search. It became the
  template, not a dead end.
- **Direct lineage:** DeepStack → Brown & Sandholm (2018) depth-limited solving (theory) → ReBeL (2020,
  PBS + AlphaZero-style self-play) → Student of Games (2023, GT-CFR; shares DeepStack authors). The
  neural-value thread Libratus dropped is the one that ultimately won.
- **Beyond poker:** the "planning in the loop with a learned value model" recipe generalized to multi-agent /
  cooperative settings — e.g., CICERO (Diplomacy, 2022) explicitly "operated similarly to AlphaZero and
  ReBeL."
- **Frontier framing (test-time compute):** DeepStack is an early, clean instance of "spend compute at
  decision time via search guided by learned intuition" rather than a giant precomputed policy — the same
  thesis behind 2024–2026 reasoning models. Caveat (Noam Brown): imperfect info needed *belief-aware* search
  because vanilla MCTS (great for Go) fails in poker.
- **Reusable subsystems today:** (1) the depth-limit + learned-leaf-value pattern; (2) the differentiable
  zero-sum output head for 2p value nets; (3) AIVAT-style variance reduction (a learned value model as a
  control variate for low-variance evaluation of any stochastic agent — reusable far beyond poker);
  (4) pot-fraction value normalization for scale-invariant generalization.
- **Superseded parts:** hand-crafted 1,000-bucket k-means clustering, separate per-round nets, the tuned
  CFR-D gadget → replaced by ReBeL/SoG's general learned representations.
- **Verdict:** as a *deployed poker system*, superseded; as a *paradigm*, foundational and now mainstream — a
  stepping stone whose central idea is state-of-the-art. Thesis hooks: the (range, opponent CFVs) state →
  Contribution 1 (belief-based opponent modelling); the depth-limited error bound → Contribution 2 (safe
  exploitation).

## Hand-off → Libratus (system #2; full treatment in subtask #2)
- Same year, independent (Paper note 39). Libratus kept an **abstraction blueprint (MCCFR)** but added
  **nested *safe* subgame solving** — when the opponent bets off-tree, it builds and solves a finer subgame
  *with that action included*, fitting the result back into the blueprint, **with a provable safety
  guarantee** (no static action translation). Plus a **self-improver** module.
- Match: beat 4 HUNL pros (Les, Kim, McCauley, Chou) by **147 mbb/g over 120,000 hands, 20 days, Jan 2017**,
  99.98% significance (Brown & Sandholm 2018; CMU "Brains vs AI"). Ran on the Bridges supercomputer (~600
  nodes).
- So the cons DeepStack hands forward: the **betting-abstraction / off-tree-action** problem (Libratus →
  exact nested safe subgame solving) and a **larger, more rigorous match**. The **neural-value** idea is what
  ReBeL/SoG later revive and generalize. Multiplayer stays open until Pluribus.
