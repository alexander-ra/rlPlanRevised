# Pluribus — Research Notes

> Gather sources and extract architectural detail BEFORE writing prose in
> ../summary/summaryEn.md. Cite every source so claims are traceable.
> System: Pluribus (Brown & Sandholm, 2019).
> NOTE: the paper is famously thin on architecture (cheap/low-compute, high impact) ->
> the architectural depth is in the **supplementary materials** + author talks + secondary
> deep-dives. Those are mined heavily below.

## Sources consulted
<!-- Primary paper, supplement, author talks, blogs, secondary deep-dives. Add links + 1-line relevance. -->
- **[Primary]** Brown, N. & Sandholm, T. (2019), "Superhuman AI for Multiplayer Poker", *Science*
  365(6456):885–890, doi:10.1126/science.aay2400. Full text (author copy):
  https://noambrown.com/papers/19-Science-Superhuman.pdf — the main paper: the multiplayer-equilibrium
  argument, MCCFR + Linear CFR blueprint, depth-limited search with continuation strategies, the two human
  formats, and the headline result. Cited below as **(Science)**.
- **[Primary — the architecture lives here]** Brown & Sandholm (2019), *Supplementary Materials* for the
  above. https://noambrown.com/papers/19-Science-Superhuman_Supp.pdf — the real architecture: exact
  abstraction sizes, the negative-regret-pruning algorithm (Algorithm 1), the nested-search algorithm
  (Algorithm 2), the four continuation strategies (bias ×5), unsafe-search-from-round-start, AIVAT details,
  hardware, per-participant table. **This is the single richest source** and is mined throughout. Cited as
  **(Science Supp)**.
- **[Correction]** The Pluribus paper has **no arXiv version**. The "arXiv:1911.07559 (extended version)"
  link seeded in `planning/rawStepsBg` (and copied into the old `research/{libratus,pluribus}.md` stubs) is
  **incorrect** and is *not* cited here. The relevant Brown–Sandholm arXiv IDs are **1809.04040** (Linear/
  Discounted CFR, AAAI-19) and **1805.08195** (Depth-Limited Solving, NeurIPS-18) — see below.
- **[Secondary, accessible]** Facebook/Meta AI blog, "Facebook, Carnegie Mellon build first AI that beats
  pros in 6-player poker" (11 Jul 2019).
  https://ai.meta.com/blog/pluribus-first-ai-to-beat-pros-in-6-player-poker/ — plain-language architecture
  walk-through; the "$150 / less than $150 of cloud compute" framing; the **Loeliger** 1H+5AI addendum
  (post-submission); the "~$5/hand, ~$1,000/hour, ~5 bb/100" framing; pro quotes. Cited as **(Meta blog)**.
- **[Secondary, accessible]** CMU/CSD news, "Carnegie Mellon and Facebook AI Beats Professionals in
  Six-Player Poker" (Jul 2019).
  https://www.cs.cmu.edu/news/2019/carnegie-mellon-and-facebook-ai-beats-professionals-six-player-poker —
  "blueprint sufficient for the first betting round"; Libratus ≈15M core-hours to build + 1,400 CPU cores at
  play vs Pluribus 12,400 core-hours + 28 cores. Cited as **(CMU news)**.
- **[Author course]** Sandholm, T., CMU 15-888 (Computational Game Solving), Lecture 14, "Pluribus and
  depth-limited subgame solving".
  https://www.cs.cmu.edu/~sandholm/cs15-888F24/Lecture_14_Pluribus_and_depth-limited_subgame_solving.pdf —
  the cleanest architectural slide deck: "Linear MCCFR", "new form of dynamic pruning (not in last two steps)",
  "all players (not just opponents) pick from k continuation strategies", "search starts at the beginning of
  the current betting round", Modicum head-to-head table, "Science Breakthrough of the Year runner-up 2019".
  Cited as **(CMU L14)**.
- **[Primary — the depth-limited-search lineage / the 2p0s precursor]** Brown, N., Sandholm, T. & Amos, B.
  (2018), "Depth-Limited Solving for Imperfect-Information Games", *NeurIPS* 31:7663–7674, arXiv:1805.08195 —
  introduces the continuation-strategy idea and the laptop-scale **Modicum** bot that Pluribus generalizes to
  >2 players. Cited as **(NeurIPS-18 DLS)**.
- **[Primary — the "Linear CFR" engine]** Brown, N. & Sandholm, T. (2019), "Solving Imperfect-Information
  Games via Discounted Regret Minimization", *AAAI* 33:1829–1836 (Distinguished Paper Honorable Mention),
  arXiv:1809.04040 — Linear CFR / discounted CFR; the convergence speedup Pluribus uses for the blueprint and
  subgames. Cited as **(AAAI-19 LCFR)**.
- **[Evaluation method]** Burch, N., Schmid, M., Moravčík, M., Morrill, D. & Bowling, M. (2018), "AIVAT: A
  New Variance Reduction Technique for Agent Evaluation in Imperfect Information Games", *AAAI*,
  arXiv:1612.06915 — the variance-reduction estimator (≈9× variance reduction here); first surfaced in the
  DeepStack work. Cited as **(AIVAT)**.
- **[Context, predecessor — the bridge]** Brown & Sandholm (2018), Libratus (*Science* 359:418–424). The
  two-player ceiling Pluribus departs from; bridge material is in `research/libratus.md` "Hand-off →
  Pluribus". Cited as **(Libratus)**.
- **[Context]** Moravčík et al. (2017), DeepStack (*Science* 356:508–513) — the *other* prior 2p approach to
  depth-limited search (belief-conditional leaf values), contrasted by the Science paper as too expensive to
  scale to 6 players. Cited as **(DeepStack)**.
- **[Context, equilibrium-selection]** Zinkevich, Bowling & Wunder (2011), "The Lemonade Stand Game
  Competition", *ACM SIGecom Exchanges* 10:35–38 — the Fig. 1 example of why independently-chosen Nash
  equilibria need not combine into a Nash equilibrium.
- **[Context, action translation]** Ganzfried & Sandholm (2013), "Action translation in extensive-form
  games", IJCAI — the (randomized/deterministic) **pseudo-harmonic** mapping Pluribus uses for off-tree bets
  on round 1.
- **[Context, information abstraction]** Brown, Ganzfried & Sandholm (2015), AAMAS — the potential-aware /
  earth-mover information-abstraction algorithm used for the buckets.
- **[Modern relevance / test-time compute]** Noam Brown, Sequoia "Training Data" podcast (2024) on o1 /
  test-time compute — frames real-time search (DeepStack/Libratus/Pluribus) as an early instance of
  inference-time deliberation; "adding search was worth ~the same as 100,000× more pretraining/blueprint".
  https://www.sequoiacap.com/podcast/training-data-noam-brown/ (shared thread with the DeepStack/Libratus notes).

---

## Architecture / component breakdown
<!-- Offline vs online components; where NN / CFR / search sit. -->

Pluribus = **abstraction + blueprint (offline, Linear MCCFR)** + **real-time depth-limited search with
continuation strategies (online, Linear CFR)**. Like Libratus and unlike DeepStack/ReBeL/SoG, there are
**no neural networks anywhere** — it is a purely tabular CFR/abstraction system (Science; CMU L14). It
**does not adapt to opponents** (a fixed strategy; no opponent modelling) and uses **no human data**
(Science; Meta blog). It is **not** a three-module pipeline like Libratus — there is **no self-improver**;
the architecture is just *blueprint + search*. Crucially, only **two** things make 6-player feasible:
(1) **depth-limited** search (vs Libratus always solving to the end), and (2) a much **cheaper blueprint**
(Linear MCCFR + pruning).

**Game (Science Supp "Rules"):** 6-player no-limit Texas hold'em (6-max NLHE), the world's most popular poker
format. Each hand: $10,000 stacks (= 100 big blinds), blinds $50/$100, four betting rounds (preflop, flop,
turn, river). Each hand starts with equal stacks so each hand is treated as an i.i.d. sample for win-rate
measurement.

**Module 1 — Blueprint (offline, self-play):**
- Computed by self-play from scratch (random → improves), **no human/prior-AI data** (Science). Self-play is
  "everyone-vs-everyone" — six copies of Pluribus (CMU news; rawStepsBg framing).
- **Equilibrium finder = external-sampling MCCFR + Linear CFR ("Linear MCCFR")** (Science; AAAI-19 LCFR;
  CMU L14). MCCFR designates one player the *traverser* each iteration, simulates a hand, and updates the
  traverser's regrets/strategy by counterfactual reasoning (Fig. 2). For 2p0s, CFR's average strategy → Nash;
  **outside 2p0s there is no such guarantee**, but CFR still guarantees **sublinear (no-)regret** in all
  finite games and eliminates iteratively strictly-dominated actions (Science).
- **Linear CFR** weights iteration *t*'s regret/strategy contribution by *t*, so the bad early ("random")
  iterations decay fast; applied for the **first 400 minutes** only (discount every 10 min by
  (T/10)/((T/10)+1); stop after, since the multiply isn't worth it later). ~**3× convergence speedup**
  (Science Supp; AAAI-19 LCFR).
- **Modified negative-regret pruning ("modified RBP"):** after the first 200 min, in **95% of iterations**
  the traverser **skips actions with regret < −300,000,000** (full traversal in the other 5%). Differences vs
  the pruning in Libratus/Baby Tartanian8: (a) Pluribus does **not** prune on the **last betting round** or on
  **actions leading directly to terminal payoffs** (to avoid pruning inaccuracies where there's no
  abstraction-refinement benefit); (b) Pluribus decides to prune **per iteration** (one RNG draw) rather than
  per action (cheaper). ~**2× speedup**. Side effect: pruning effectively **refines the information
  abstraction**, because rarely-reached infosets in a shared bucket get traversed only 5% as often, so the
  bucket's strategy generalizes to the infosets actually reached in strong play. The gain is *larger* in
  6-player because good play folds most hands early, so even less of the tree is reached. (Science Supp,
  Algorithm 1 "MCCFR with Negative-Regret Pruning".)
- **Memory tricks:** regrets stored as **4-byte ints** (not 8-byte doubles) with a floor at −310,000,000
  (eases "un-pruning", prevents overflow); regret memory for an action sequence is **allocated only when the
  sequence is first encountered** (except round 1, allocated up front) → >2× memory saving, important because
  most 6-player action sequences never occur. Average strategy kept (and used as blueprint) only for round 1;
  post-round-1 the blueprint is built by **averaging disk snapshots** of the current strategy (every 200 min
  after the first 800 min) — roughly halves memory and per-iteration cost (Science Supp).
- **Abstraction (two kinds; Science Supp "abstraction"):**
  - *Action abstraction*: NLHE allows any whole-dollar bet $100–$10,000; the blueprint allows **1–14 raise
    sizes** depending on the spot (all pot-fractions, hand-picked from sizes earlier Pluribus versions used
    with significant probability). **Fine on round 1** (no search there), coarser on round 2, and on rounds
    3–4 at most **three** first-raise sizes (0.5×pot, 1×pot, all-in) and **two** subsequent (1×pot, all-in).
    664,845,654 total blueprint action sequences, of which only 413,507,309 were ever encountered.
  - *Information abstraction* (bucket strategically similar card situations): **lossless on round 1 only**
    (169 / 1,286,792 / 55,190,538 / 2,428,287,420 strategically-unique situations on rounds 1–4 if lossless
    everywhere); **lossy 200 buckets/round** on rounds 2–4 (k-means on domain-specific features). Information
    abstraction is **never used for the current round during live play** — only to reason about *future*
    rounds — because it washes away distinctions that matter for superhuman play (Science).
- Output = the **blueprint strategy** for the whole game, but **coarse**; Pluribus plays it *directly* only
  on the **first betting round** (Science; CMU news).

**Module 2 — Real-time depth-limited search (online):** the most intricate component (Science Supp "real-time
search").
- *When*: search is used on **rounds 2, 3, 4 always**; on **round 1** only if an opponent's raise is >$100
  off every blueprint size **and** ≤4 players remain — otherwise the off-tree bet is mapped with **randomized
  pseudo-harmonic action translation** and blueprint play continues (Science Supp; Science).
- *Subgame root* = a **probability distribution over the nodes of the current public state** (a chance node
  reaching node *h* with normalized reach prob π^σ(h)/Σ_{h'∈G} π^σ(h')), since under hidden information there
  is no single root node (Science Supp, "Structure of … subgames"). Pluribus maintains a belief distribution
  over each player's 1326 possible private-card combos (init 1/1326), **Bayes-updated each round** under σ
  (blueprint, or the previous search output).
- *Depth limit*: round-1 search → end of round (leaves at round-2 chance nodes); round-2 search with >2
  players → leaves at round-3 chance nodes or right after the 2nd raise (whichever is earlier); **all other
  cases → solve to the end of the game** (Science Supp).
- *Leaf values via k=4 continuation strategies* (the key innovation — see below).
- *Subgame solver*: **Monte Carlo Linear CFR** if the subgame is large/early; otherwise an **optimized
  vector-based Linear CFR** that samples one public-board set per thread. Pluribus **plays the final
  iteration's strategy** (not the time-average) to avoid residual bad actions, though σ is still tracked on
  the average (Science Supp). Subgame action abstraction: **1–6 raise sizes**, 100–2,000 action sequences;
  **lossless** info-abstraction for the current round, **lossy 500 buckets/round** later (finer than the
  blueprint's 200).
- *Off-tree opponent bets in search* (the action-translation cure, inherited from Libratus): an off-abstraction
  action is **added as a valid action** and the subgame is **re-searched from the root** — no reverse mapping
  (Science Supp; CMU L14). Only Pluribus's **own already-chosen actions** (for its actual hand) are frozen;
  opponents' actions are not frozen.

**Where the classic pieces sit:** abstraction (Step 4) + MCCFR/Linear CFR (Step 3) build the blueprint;
Linear CFR does the subgame search; "search" = per-decision real-time depth-limited solving. **No neural
component** (contrast DeepStack/ReBeL/SoG). The depth-limited-solving theory (NeurIPS-18 DLS) is the direct
lineage; the multiplayer generalization is Pluribus's contribution.

## Design decisions
<!-- Why these choices; trade-offs made. -->
- **Goal = empirical superhuman play, not a solution concept.** Outside 2p0s, Nash is (a) hard to compute/
  approximate and (b) **not a safety guarantee** — independently-chosen Nash strategies need not form a Nash,
  and you can *lose* while playing an exact Nash (Lemonade Stand Game, Fig. 1). So Brown & Sandholm explicitly
  abandon "find a Nash equilibrium" and instead aim to **consistently beat elite humans empirically**
  (Science; Meta blog). Pluribus's algorithms are **not guaranteed to converge to Nash** outside 2p0s — and
  that is accepted deliberately.
- **Depth-limited search instead of solving-to-the-end** (the reason 6-player is feasible). Libratus always
  solved to the end; with more players, subgames blow up exponentially, so beneficial real-time search on the
  flop with >3 players is "likely infeasible" without a depth limit (Science Supp). DeepStack's
  belief-conditional leaf values were already very expensive in 2p and worse as players grow. Depth-limited
  search "reduces the computational resources and memory needed by probably at least five orders of magnitude"
  (Science Supp).
- **Continuation strategies for ALL players, not just the opponent** — Pluribus's advance over its own 2p
  precursor Modicum. In Modicum only the *opponent* chose among continuation strategies (the searcher only
  played the blueprint); sound in 2p0s but it gives the opponent more power, making the searcher
  **defensive/conservative** with lower EV. Letting the **searcher also choose** among the k strategies
  balances the players and is "more effective, easier, and more elegant" (Science Supp, footnote 1;
  NeurIPS-18 DLS).
- **Unsafe search, but started at the *beginning of the current betting round*.** Pluribus uses *unsafe*
  search (assume opponents played the strategy Pluribus computes for them) because in practice it beats
  modern "safe" search head-to-head, and because it needn't compute strategies for zero-probability hands
  (most 6-player hands are folded 100% immediately → only a small fraction need a strategy → ~4× faster). To
  curb unsafe search's exploitability, Pluribus always solves from the **start of the round** (after a
  large-branching chance node), holding its own already-taken actions fixed but letting opponents have changed
  strategy anywhere in the round; empirically this yields low exploitability in 2p0s (Science Supp).
- **Play the final CFR iteration, not the average** — avoids lingering bad actions in the average strategy;
  the final iterate is "sufficiently unpredictable that any exploitation is infeasible" (Science Supp).
- **No self-improver** (unlike Libratus). Pluribus does not patch its blueprint between sessions; depth-limited
  search on rounds 2–4 plus dense round-1 action abstraction is enough (Science; the only round-1 residual is
  the pseudo-harmonic translation).
- **No opponent adaptation by design** — robustness over exploitation, the same stance as Libratus; the bot
  doesn't even know opponents' identities, so its copies can't deliberately collude in the 1H+5AI format
  (Science).

## Approaches tried / abandoned / evolved during development
<!-- The priority material: dead-ends, engineering compromises, things the paper under-describes. -->
- **Nash equilibrium as the goal — abandoned for >2 players.** The whole prior paradigm ("approximate a Nash
  equilibrium") is explicitly dropped because, with >2 players, Nash is neither efficiently computable, nor
  unique, nor safe (Science §"Theoretical and practical challenges"; Meta blog). This is the conceptual
  pivot, not an engineering tweak.
- **Assuming a single blueprint continuation at leaves — shown to fail.** The naïve perfect-information move
  (fix one value per leaf, e.g. "everyone plays the blueprint after the leaf") produces brittle, unbalanced,
  exploitable strategies (the sequential Rock-Paper-Scissors example, Fig. 3). In the 2p precursor's
  ablation, **"naïve depth-limited solving" (single value) LOST**: −10±8 mbb/g vs Baby Tartanian8 and −1±15
  vs Slumbot; only **continuation-strategy** depth-limited solving WON (+6±5 and +11±9) (NeurIPS-18 DLS,
  Table 1). So the study-step gloss that "Pluribus assumes opponents stick to the blueprint beyond the depth
  limit" is **imprecise** — the design point is the *opposite*: it assumes they may switch among k strategies.
- **Modicum-style (opponent-only continuation strategies) — improved upon.** See design decisions: only the
  opponent choosing leads to over-conservative play; Pluribus lets the searcher choose too (Science Supp fn 1).
- **Safe subgame solving — deliberately *not* used.** Libratus's prized *safe* nested solving is set aside;
  Pluribus uses **unsafe** search because it performs better head-to-head and is ~4× faster in 6-player, even
  though it "lacks theoretical guarantees … and there are cases where it leads to highly exploitable
  strategies" (Science Supp). The round-start trick is the only mitigation. This is a clear, acknowledged
  trade of theory for empirical strength.
- **Limping — learned then discarded.** In early blueprint self-play Pluribus experimented with limping
  (calling the big blind) but gradually abandoned it for everyone except the small blind — independent
  confirmation of human folk wisdom (Science; Meta blog).
- **Donk-betting — kept, against folk wisdom.** Pluribus donk-bets far more than human pros, suggesting the
  folk "donk betting is a mistake" belief is wrong (Science).
- **Under-described in the main text / only in the supplement (or companion papers):** essentially *all* the
  architecture — abstraction sizes, the pruning thresholds/algorithm, the nested-search algorithm, the leaf
  continuation-strategy construction (bias ×5), the unsafe-search-from-round-start justification, AIVAT
  details, and the hardware — lives in the **Supplementary Materials** (Science Supp), not the 6-page article.
  The continuation-strategy theory is in **NeurIPS-18 DLS**; Linear CFR is in **AAAI-19 LCFR**. The main text
  is "thin on architecture" precisely because it is a *Science* article; the depth is deliberately offloaded.
- **No ablation of the innovations.** The authors note that measuring each innovation's individual impact
  "would be too expensive due to the extremely high variance in no-limit poker and the high dollar and time
  cost" of human experiments — so the per-component speedups (≈3×, ≈2×, >2×) are *estimates*, and the overall
  superhuman result is not decomposed (Science Supp).
- **Code never released.** As with Libratus, "because poker is played commercially, the risk associated with
  releasing the code outweighs the benefits"; only **pseudocode** (Algorithms 1 & 2) is provided. The code is
  largely licensed to Sandholm's companies Strategic Machine / Strategy Robot (Science Acknowledgments;
  Meta blog).

## Compute & cost
<!-- The famously low training/serving cost — capture concrete numbers. -->
- **The headline of the paper.** Blueprint trained in **8 days** on a **single 64-core server** (a Bridges
  large-shared-memory node: four 16-core Intel Xeon E5-8860 v3 CPUs) for **12,400 CPU core-hours**, using
  **<512 GB** RAM (the node had 3 TB; <0.5 TB was needed), **no GPUs**. At cloud spot rates ≈ **$144**
  (the "<$150" figure) (Science; Science Supp; Meta blog).
- **Play time:** a single **28-core, 128 GB** node — **two 14-core Intel Haswell E5-2695 v3 CPUs** ("two
  CPUs" / "28 cores"), **<128 GB** RAM, **no GPUs**. Search takes **1–33 s per subgame**; **~20 s/hand** on
  average vs self — **~2× faster than human pros** (Science; Science Supp; CMU L14).
- **The contrast (the whole point):** AlphaGo used 1,920 CPUs + 280 GPUs; Deep Blue 480 custom chips;
  **Libratus used ~100 CPUs at play and ~15M core-hours to build** (Science; CMU news). Pluribus reached a
  *harder* (6-player) milestone for **~1/1000th** of Libratus's build compute and on commodity hardware —
  "millions of dollars" of compute vs **<$150** (Meta blog). The blueprint abstraction was deliberately sized
  so live play fits in ≤128 GB.
- **Lineage cost (NeurIPS-18 DLS):** the 2p precursor **Modicum** used just **700 core-hours**, a **4-core
  CPU**, **16 GB** to beat Baby Tartanian8 (≈2M core-hours, 18 TB) and Slumbot (≈250k core-hours, 2 TB) — and
  DeepStack used **>1,000,000 core-hours** and was never shown to beat a top prior AI. Depth-limited search
  with continuation strategies is *why* the cost collapsed; Pluribus inherits that and scales it to 6 players.
- **Where the cost concentrates:** unlike DeepStack (heavy offline, cheap online) and Libratus (heavy at
  *both* ends), Pluribus is **cheap at both ends** — a cheap blueprint *and* cheap real-time search — which is
  the new thing.

## Evaluation setup & headline result
- **Metric:** mbb/game (milli-big-blinds per game; ~50 mbb/g is a sizable heads-up pro edge). **AIVAT**
  (modified for >2 players) reduced variance by **~9×**; one-tailed t-test for profitability at 95%
  confidence; each hand treated as i.i.d. (Science; Science Supp; AIVAT).
- **Two formats** (six seats, $10k stacks, $50/$100 blinds):
  - **5 humans + 1 AI (5H+1AI):** **13 elite pros** (each won >$1M, many >$10M), 5 drawn per day from the
    pool; **10,000 hands over 12 days**; $50,000 prize pool ($0.40–$1.60/hand by performance); aliases used.
    Result: **Pluribus +47.7 mbb/game (SE 25.0), p = 0.028** — profitable, statistically significant; a very
    high six-max win rate against elite pros (≈**5 bb/100**, ≈$5/hand, ≈$1,000/hr — Meta blog). The 13: Jimmy
    Chou, Seth Davies, Michael Gagliano, Anthony Gregg, Dong Kim, Jason Les, Linus Loeliger, Daniel McAulay,
    **Greg Merson** (2012 WSOP Main Event champ), Nicholas Petrangelo, Sean Ruane, Trevor Savage, Jacob Toole
    (Science Supp).
  - **1 human + 5 AI (1H+5AI):** **Chris "Jesus" Ferguson** (2000 WSOP Main Event champ, 6 bracelets, >$9.2M
    live) and **Darren Elias** (4× WPT titles, >$7.1M live) each played **5,000 hands** (10,000 total) against
    **5 independent copies** of Pluribus (which can't collude — fixed strategy, no opponent ID). Result
    (designed measure = aggregate): **Pluribus +32.7 mbb/game (SE 14.9), p = 0.014**. Per-player (reported
    "for completeness"): **Elias −40.2 (SE 21.9, p = 0.033)**; **Ferguson −25.2 (SE 20.2, p = 0.106)** —
    Ferguson's smaller loss may be variance, skill, or a more fold-biased, conservative style (Science;
    Science Supp).
  - **Addendum (Meta blog, post-submission):** the 1H+5AI experiment was later repeated with **Linus
    Loeliger** — widely regarded as the **best 6-max NLHE cash player in the world**. In aggregate the three
    humans lost **2.3 bb/100**: Elias −4.0 (SE 2.2), Ferguson −2.5 (SE 2.0), **Loeliger −0.5 bb/100 (SE 1.0)**
    — i.e., even the best human in the world was beaten, though Loeliger's margin is not individually
    significant.
- **Robustness of the win:** matches ran over days, giving humans time to adapt; the **steady** win-rate curve
  suggests humans **could not find exploitable weaknesses** (Science, Fig. 5). AIVAT cannot be applied to the
  *humans'* individual rates (their strategies/ranges are unknown), so Table S1's per-human numbers use only a
  modest variance reduction and "no meaningful conclusions can be drawn about any individual participant."
- **Honesty/units caveat:** Pluribus's 48 mbb/game six-max rate is **not directly comparable** to Libratus's
  147 mbb/game heads-up rate (different game, five opponents, different variance), but it is a decisive
  six-max margin (Science; Meta blog).

## Known criticisms / limitations
<!-- No N-player safety guarantee (the gap Contribution #2 targets). -->
- **No N-player safety guarantee — the central, deliberate gap.** Pluribus's algorithms are **not guaranteed
  to converge to a Nash equilibrium** outside 2p0s, and even a Nash would not guarantee safety with >2
  players. Superhuman performance is **empirical**, not certified; there is **no exploitability bound** (the
  thing DeepStack's k₁ε and Libratus's 2Δ each provided). This is exactly the open problem the thesis's
  **Contribution 2** targets (Science; rawStepsBg/cleanSteps; PLAN.md).
- **Uses *unsafe* search** with known (if mitigated) exploitability risk in theory — a conscious trade of
  guarantees for head-to-head strength and speed (Science Supp).
- **Still abstraction- and blueprint-based, purely tabular, no neural generalization.** Nothing transfers
  across situations; the blueprint is a big lookup table; abstraction is hand-tuned. This is the thread
  ReBeL/SoG pick up (not Pluribus) (Science; rawStepsBg).
- **Round-1 action translation survives.** On the first round, sufficiently off-tree bets are still mapped via
  pseudo-harmonic translation (the residual seam Libratus's self-improver chipped at — Pluribus simply lives
  with it) (Science Supp).
- **No per-innovation ablation / no released code** — impact estimates only; reproducibility rests on
  pseudocode (Science Supp).
- **Evaluation caveats:** i.i.d.-hand assumption is only approximate (humans adapt); AIVAT can't score
  individual humans; the strong individual significance is for the *aggregate* (Science Supp, note 45).
- **Not universal beyond poker.** The authors caution the approach may fail where players can **communicate/
  collude** or coordinate (simple coordination games can defeat self-play); poker's limited collusion is part
  of why it works (Meta blog).

## Comparison dimensions (for the master table)
- **Year:** 2019 (*Science* 365:885, published online 11 Jul 2019; Science Breakthrough of the Year
  runner-up, 2019 — CMU L14).
- **Players:** **6** (six-max). The first superhuman result in any benchmark game with **>2 players/teams**.
- **Game type:** 6-max NLHE — six-player no-limit Texas hold'em (imperfect information; **multiplayer /
  general-sum**, *not* 2p0s).
- **Blueprint (offline)?:** **Yes** — a full-game blueprint solved offline with **Linear MCCFR**; played
  *directly* only on the first betting round, used as a scaffold/leaf-continuation thereafter.
- **Neural component:** **None** — purely tabular CFR/abstraction (like Libratus; the contrast with
  DeepStack/ReBeL/SoG).
- **Search mechanism:** **Real-time depth-limited search** with **k=4 continuation strategies** at the leaves
  (nested *unsafe* search, solved from the start of the current betting round); Linear CFR in subgames.
- **Abstraction?:** **Yes** — action abstraction (1–14 blueprint raise sizes; 1–6 in search) + information
  abstraction (lossless round 1; lossy 200 buckets/round later in the blueprint; finer — lossless current
  round, 500 buckets/round later — in search).
- **Perfect-info too?:** **No** (imperfect-information only).
- **Compute:** **Famously cheap.** Blueprint: 8 days, **12,400 core-hours**, one **64-core** server, <512 GB,
  no GPUs, **≈$144**. Play: **2 CPUs (28 cores)**, <128 GB, no GPUs, 1–33 s/subgame. (vs Libratus ~15M
  core-hours + ~100 CPUs; AlphaGo 1,920 CPUs + 280 GPUs.)
- **Key innovation:** First **superhuman multiplayer** poker AI — scales the blueprint-MCCFR + real-time
  search recipe to **6 players** via **depth-limited search with continuation strategies**, winning
  **empirically** on a tiny compute budget, **with no N-player safety guarantee**.

## Modern relevance / legacy (2026 view)
<!-- How the core ideas map to current AI/ML; what is reusable vs superseded; obsolete or living stepping stone. -->
- **Core idea that survived:** **depth-limited real-time search made to work under hidden information by
  letting players choose among multiple continuation strategies at the leaves** — i.e., a leaf value is not a
  single number but a small set of values the opponents (and you) can select among, forcing balance. This is
  the imperfect-information analogue of bounded look-ahead with a fixed evaluator, and it generalizes the
  depth-limited-solving theory (NeurIPS-18 DLS) to N players.
- **The headline legacy is the *economics*:** Pluribus is the canonical proof that **a harder milestone can
  be reached with ~1000× less compute** through better algorithms — search-at-inference plus faster self-play
  — rather than more hardware. Brown repeatedly cites this as an early, concrete instance of the
  **"test-time compute"** thesis later central to o1-style reasoning models (Sequoia 2024). The blueprint-then-
  search split prefigures pretrain-then-search.
- **Direct lineage:** Libratus (2017, 2p) → **Pluribus** (2019, 6p; depth-limited search) → unified by the
  depth-limited-solving theory (NeurIPS-18) → **ReBeL** (2020), which replaces the hand-built blueprint +
  abstraction with **learned** public-belief-state values while keeping search-in-the-loop → **Student of
  Games** (2023). The *neural-generalization* gap Pluribus leaves open is taken up by ReBeL/SoG, **not**
  Pluribus.
- **Most important for THIS thesis:** Pluribus is the **empirical existence proof that Nash-based, search-
  based methods work in N-player imperfect-information games while providing NO safety/exploitability
  guarantee.** That precise gap — N-player safe exploitation under value/structure uncertainty — is the
  thesis's **Contribution 2**, with the depth-limited-solving bounds (Brown & Sandholm 2018) and the
  opponent-adaptation analysis (Milec et al.) as starting points (PLAN.md; cleanSteps).
- **Reusable subsystems today:** (1) **continuation-strategy leaf evaluation** (multi-valued states) for
  robust depth-limited search in hidden-information / multi-agent settings; (2) **Linear/discounted CFR** as a
  drop-in convergence accelerator (now standard, and the launch point for later DCFR/PDCFR work — rawStepsBg
  notes Xu et al. AAAI-26); (3) **negative-regret (regret-based) pruning** for scaling CFR; (4) **AIVAT** as a
  control-variate evaluator (reused from DeepStack); (5) the **add-the-action / re-solve** treatment of
  off-tree bets (from Libratus) that removes reverse-mapping.
- **Superseded parts:** the hand-tuned card/action abstraction and the tabular blueprint — dissolved by the
  learned representations of ReBeL/SoG; and *unsafe* search, which later belief-state methods make
  unnecessary. As a *deployed architecture* Pluribus is superseded; as a *thesis* — "search + cheap self-play
  beats brute-force scale, and multiplayer is empirically tractable but theoretically open" — it is very much
  alive.

## Hand-off ← Libratus (opening bridge material; full bridge text in research/libratus.md)
- Libratus left **two** things open: it was **two-player-only** (its safety leans on 2p0s Nash structure), and
  it was **abstraction/blueprint-heavy with no neural generalization**. Pluribus takes the **first**: it
  removes the two-player crutch and scales the blueprint + real-time search recipe to **six** players — a
  setting where **Nash is neither unique nor a safety guarantee** — and beats elite pros **anyway**,
  empirically, on a famously tiny budget. It **drops** the very safety guarantee Libratus prized; that
  omission is the open multiplayer-safety gap (Contribution 2). The *neural-generalization* gap is left for
  later systems.
- **Opening bridge (one phrasing):** *Libratus showed real-time safe search beats abstraction-and-translation
  in two-player zero-sum — but its safety, and the very meaning of "solving" the game, leaned on 2p0s
  structure. What happens when you remove the two-player crutch entirely?*

## Hand-off → ReBeL (system #4; NOT in Pluribus's section — opens ReBeL's section in subtask #4)
- Pluribus closes the *player-count* gap but **not** the *generalization* or *safety* gaps: it is still
  tabular/abstraction-based (nothing learned, nothing transfers) and uses *unsafe* search with **no**
  exploitability guarantee. ReBeL (2020) returns to **2p0s** but replaces hand-built abstraction + blueprint
  with **learned public-belief-state (PBS) values + AlphaZero-style self-play and search**, recovering
  *provable* guarantees while removing abstraction. (Forward hand-off belongs at the *start* of ReBeL's
  section, per the locked spine.)
