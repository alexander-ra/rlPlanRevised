# Chapter I — outline

**Глава I. Анализ на състоянието на проблема** (*Analysis of the state of the problem*)

Built from the 13 step extracts, `lit_gaps.md` and `lit_evaluation.md` (September 2026).
Budget: 26 standard pages ≈ 6,500 EN words of running text (1 page ≈ 250 EN words ≈ 1,800
BG characters); tables, figure captions and references are outside it, leaving headroom to
30 pages. Citations are written here as author–year keys; they become one numbered `[n]`
sequence at drafting. Every key below is verified in an extract or a lit file unless marked ⚠.

## The argument in one paragraph

Imperfect-information games with several players are the standard testbed for strategic
decision-making under uncertainty, and the field has learned to compute near-equilibrium
strategies for them at scale (§ 1.2–1.3). Every landmark superhuman system plays a fixed
approximate equilibrium: its designers chose safety over exploitation, and adaptation was
too sample-hungry (§ 1.3). Opponent modelling recovers value against sub-optimal opponents,
and in two-player games it now works in real time, near equilibrium (§ 1.4). Exploitation
reintroduces risk; safe exploitation bounds that risk — but every bound rests on the
two-player minimax value. With three or more players the available safety notions are
either very conservative or provably unattainable, coalitions and collusion break the
picture further, and no method exploits with a checked loss bound (§ 1.5). Evaluation tools
measure worst case, head-to-head strength and population rank separately, and each breaks
for adaptive, exploiting or N-player agents (§ 1.6). Hence the goal, tasks and thesis (§ 1.7).

The official problem statement of the individual plan — landmark poker AIs are near-GTO,
rarely adapt and do not address fraud/collusion; the goal is an agent that starts from a
safe strategy and improves against sub-optimal opponents — maps onto this argument
directly: adaptation → C1, safe start + bounded improvement → C2, collusion → § 1.5.3 and
C2/C3, "measurable improvement" → C3.

---

## § 1.1 Въведение: актуалност и постановка на проблема — 2 p, ~500 words

1. **Games as the proving ground of AI.** Chess, Go, then imperfect information: heads-up
   limit hold'em essentially solved [Bowling 2015]; superhuman heads-up no-limit [Moravčík
   2017; Brown 2018]; six-player [Brown 2019]. Imperfect information + many players is what
   separates games from puzzles and brings them close to security, markets and online
   platforms (one sentence, no overclaim).
2. **Relevance for computer games and online platforms** (the dissertation's official
   topic). Adaptive opponents in games; online multiplayer platforms where bots and colluding
   players threaten fair play — collusion detection is an established problem [Mazrooei
   2013; Greige 2022]. Keep to 2–3 sentences; no company data.
3. **The problem.** The landmark systems play a fixed strategy: Pluribus "plays a fixed
   strategy that does not adapt to the observed tendencies of the opponents", because
   exploitation "opens oneself up to exploitation" and existing techniques "require too many
   samples … outside of small games" [Brown 2019]; Libratus "to a first approximation … did
   not do opponent exploitation" [Brown 2018]. Against sub-optimal opponents — most real
   ones — a fixed equilibrium leaves value unclaimed; with several players it does not even
   guarantee against losing [Brown 2019]. → Need: an agent that starts safe, adapts, bounds
   its risk, and copes with coordinating opponents.
4. **Scope.** Imperfect-information games, primarily the poker family (Kuhn, Leduc, their
   N-player variants) and one small N-player bargaining game (So Long Sucker) as testbeds;
   agents that begin from an equilibrium-based strategy. Out of scope: perfect-information
   games, cooperative MARL except as background, general N-player safety *theorems*.
5. **Structure of the chapter** (3 lines).

## § 1.2 Теоретични основи — 4 p, ~1,000 words

*Ends with:* equilibrium is computable at scale by sampling, abstraction and search — as an
approximation, with guarantees that are two-player zero-sum.

1. **Sequential decisions (≈ 230 w).** MDP, Bellman, DP [Sutton & Barto 2018; Bellman 1957];
   TD, Q-learning [Sutton 1988; Watkins & Dayan 1992]; deep RL: DQN [Mnih 2015], policy
   gradient, TRPO, PPO+GAE [Williams 1992; Schulman 2015, 2016, 2017]. **Why games break the
   assumptions:** decision points are information sets [Shoham & Leyton-Brown 2008]; learning
   opponents make the environment non-stationary [Hernandez-Leal 2017]; independently trained
   policies overfit to their partners [Lanctot 2017]; plain RL diverged on Leduc where
   fictitious self-play did not [Heinrich & Silver 2016]; greedy policies cannot represent the
   mixed strategies equilibria need.
2. **Games and equilibria (≈ 250 w).** Extensive form, information sets, behaviour strategies
   [Kuhn 1953; Shoham & Leyton-Brown 2008]. Minimax theorem [von Neumann 1928], Nash
   existence [Nash 1950]; in two-player zero-sum games equilibrium = minimax = safe. Beyond:
   PPAD-completeness [Chen 2009; Daskalakis 2009 — three players]; in three-player Kuhn one
   player can shift utility between the others inside an equilibrium family [Szafron 2013];
   independently chosen equilibria need not form an equilibrium [Brown 2019].
3. **Computing equilibria (≈ 280 w).** Regret matching, average regret O(1/√T) [Blackwell
   1956; Hart & Mas-Colell 2000]; CFR and its bound, linear in the number of information sets
   [Zinkevich 2007, Thm 4]. CFR+ [Tammelin 2014; Tammelin 2015; proof repaired Burch 2019];
   HULHE essentially weakly solved by full-traversal CFR+ (3.19×10¹⁴ infosets, 1,579
   iterations) [Bowling 2015]; DCFR [Brown & Sandholm 2019a]. MCCFR: sampled, unbiased, bound
   with high probability, external-sampling iteration O(√|H|) [Lanctot 2009]; variance
   reduction by baselines [Schmid 2019]. Exploitability/NashConv defined here, used in § 1.6
   [Lanctot 2019 OpenSpiel].
4. **Scaling by abstraction (≈ 240 w).** Game sizes: HUNL 6.37×10¹⁶¹ infosets [Johanson
   2013]. Lossless abstraction solved Rhode Island hold'em [Gilpin & Sandholm 2007]; lossy
   bounds, NP-completeness, clustering [Kroer & Sandholm 2014, 2016]; EMD / potential-aware
   imperfect-recall abstraction [Johanson 2013b; Ganzfried & Sandholm 2014]; pathologies —
   refining can hurt [Waugh 2009]; CFR-BR [Johanson 2012]. Action translation, pseudo-harmonic
   mapping [Ganzfried & Sandholm 2013]; safe and nested subgame solving, ≈ 10× less
   exploitable than translation in one test game, two-player zero-sum only [Burch 2014;
   Brown & Sandholm 2017].

*Own evidence:* none needed (reference implementations). At most one clause that the
foundations were re-implemented and cross-validated against OpenSpiel — only if § 1.1
mentions the study programme.

## § 1.3 Невронни методи и системи от най-високо ниво — 3.5 p, ~875 words

*Ends with:* every landmark system targets an approximate equilibrium and none adapts to its
opponents; where guarantees exist they stop at two-player zero-sum.

1. **Function approximation replaces tables (≈ 300 w).** Why (memory ∝ infosets; abstraction
   loss). Families: regret-based — Deep CFR [Brown 2019b], Single Deep CFR [Steinberger 2019],
   DREAM (model-free; CCE outside 2p0s) [Steinberger 2020], ESCHER [McAleer 2023], D(P)DCFR
   [Xu 2026]; RL-based — NFSP [Heinrich & Silver 2016], PSRO [Lanctot 2017], league training
   [Vinyals 2019]; changed dynamics — NeuRD [Hennes 2020], R-NaD / DeepNash in Stratego
   [Perolat 2022], MMD [Sokota 2023]; search+learning — ReBeL, SoG (next). **2026 twist:**
   generic policy gradient (PPO, MMD) matches the specialised methods on five games
   [Rudolph 2026]. Trade-offs in one sentence per family.
2. **Five landmark systems (≈ 350 w + Table 1.1).** Lineage paragraph from `step06b_extract`
   (DeepStack's continual re-solving → Libratus's nested safe subgame solving → depth-limited
   solving [Brown, Sandholm & Amos 2018] → Pluribus → ReBeL's public belief states → SoG).
   Key numbers only in the table.
3. **What they share (≈ 225 w).** (a) Guarantees: k₁ε + k₂/√T [Moravčík 2017], 2Δ [Brown
   2018], ReBeL and SoG bounds — all two-player zero-sum; Pluribus none, "unsafe" search.
   (b) No adaptation, in the authors' own words (Table 1.1 last column) — and the stated
   reasons: counter-exploitation risk and sample cost. (c) Their belief machinery tracks
   cards under an equilibrium assumption, not opponents. (d) Beyond two players,
   search+learning reached seven-player Diplomacy [FAIR 2022; Bakhtin 2023] outside any
   equilibrium guarantee.

**Table 1.1** (outside budget): System · year/venue · players · target · search at play
time · guarantee · adapts? Condensed from the comparison-table rows in `step06a_extract`
and `step06b_extract` (all cells sourced). Optional rows: DeepNash, CICERO.

*Wording rule:* "none of the landmark superhuman systems adapts to its opponents" — never
"nobody adapts" [lit_gaps C1].

## § 1.4 Моделиране на противника и поведенческа адаптация → C1 — 4.5 p, ~1,125 words

*Ends with the C1 gap* (below).

1. **The safety–exploitation spectrum (≈ 150 w + Fig. 1.1).** Equilibrium: unexploitable
   but blind; best response: maximal value, maximal risk; opponent modelling sits between
   [Albrecht & Stone 2018; Nashed & Zilberstein 2022]. **Fig. 1.1** = the dial (step 07 fig.
   31, redrawn: BG labels, legible, no "GTO", thesis terms at the ends).
2. **Bayesian opponent models (≈ 300 w).** Types vs Dirichlet over actions; partial
   observability — actions seen, cards only at showdown, marginalise over hidden hands
   [Southey 2005]; payoff against the posterior equals payoff against its mean [Ganzfried &
   Sun 2018, Thm 2.1]; game-theoretic opponent modelling from equilibrium deviations
   [Ganzfried & Sandholm 2011]; implicit modelling over a portfolio [Bard 2013].
   **Consistency:** standard Bayesian responses can fail to converge to the true strategy even
   with unlimited data; the sequence-form MAP estimator converges under identifiability,
   positive prior density, interior truth and persistent visitation [Ganzfried 2025, Props.
   2, 4 — ⚠ arXiv preprint, cite version].
3. **Adaptation to non-stationary opponents (≈ 250 w).** Taxonomy: ignore, forget, respond
   to targets, learn models, theory of mind [Hernandez-Leal 2017]; change-point detection
   [Adams & MacKay 2007]; **detect–adapt–fall back with a regret guarantee, tested in Kuhn
   against switching and adapting opponents** [Fu 2022 GSCU]; context-aware exploration
   [Ma 2024 PACE]; opponent-learning awareness, two-player differentiable games [Foerster
   2018 LOLA].
4. **Sequence models and language models (≈ 300 w).** In-context opponent modelling:
   offline [Jing 2024a TAO], with decision-time search and between-episode switches [Jing
   2024b OMIS], open-ended populations [Jing 2025]; **in poker, transformer agents that model
   and exploit while staying near equilibrium** [Caen 2026 StratFormer; Murgoci 2026
   AlphaExploitem — ⚠ preprints]; opponent models inside depth-limited search in large games,
   model given [Milec 2025]. Return-conditioned sequence models fail under stochasticity
   [Chen 2021 DT; Paster 2022]; ARDT assumes deterministic transitions [Tang 2024; CART 2025].
   LLM agents: prompted ToM agent adapts in Leduc [Guo 2023]; reflection [Zhang 2024];
   memory needed for exploitation [Lin 2026 ⚠]; LLMs far from equilibrium, actions diverge
   from stated reasoning [Lin M. 2026 ToolPoker]; all scored by chips/win rate.
5. **Own evidence (≈ 75 w, two sentences max).** In controlled Kuhn/Leduc experiments: a
   type-based model that does not contain the true type stayed confidently wrong past hand
   100 in ≈ 13 % of 300 runs; a free-form model that under-samples loses to an equilibrium
   opponent (−0.175 vs −0.083 ceiling); change-point resets helped in Kuhn and cost in Leduc.
   (Numbers from `step07_extract`, 5-seed means.) Optionally one LLM sentence: exploitation
   and exploitability move in opposite directions (Qwen2.5-7B: 0.177 vs 0.110 chips/hand
   gain, 0.357 vs 0.006 exploitability).
6. **Gap C1 (≈ 50 w)** — see *Gap statements*.

## § 1.5 Безопасна експлоатация и многоагентно разширение → C2 — 5.5 p, ~1,375 words

*Ends with the C2 gap.*

1. **Two-player safe exploitation (≈ 450 w + Table 1.2).**
   - Exploitation as an optimisation with a worst-case floor; linear in sequence form [von
     Stengel 1996; Koller 1996]; constraint generation / double oracle [McMahan 2003].
   - ε-safe responses [McCracken & Bowling 2004 ⚠ not read]; restricted Nash response and its
     concave frontier [Johanson 2007]; data-biased responses [Johanson & Bowling 2009].
   - Ganzfried–Sandholm safety over the repeated game: deviate beyond equilibrium only by
     risking "gifts" already won (RWYWE, BEFFE), significantly better than the best
     equilibrium against the model [Ganzfried & Sandholm 2015].
   - Relaxations for approximate equilibria: prime-safe [Jeary & Turrini 2023 ⚠ preprint];
     adaptation safety — no more exploitable than the blueprint, "being taught and exploited"
     [Ge 2024 OX-Search]. Real-time: SES bound [Liu 2022]; beyond the depth limit [Milec 2025];
     certified per-deployment guarantees [Li & Huang 2026 ⚠]; bounded degradation of test-time
     RL [Kubíček 2026 ⚠]; baseline-relative regret, O(1) risk vs Ω(T) gain [Müller 2025].
   - **All two-player zero-sum.**
2. **Beyond two players (≈ 450 w).** MARL in brief: Markov games [Littman 1994];
   non-stationarity and independent learners [Tan 1993; Claus & Boutilier 1998]; gradient
   dynamics cycle [Singh 2000]; CTDE [Lowe 2017; Foerster 2018b; Rashid 2018; Yu 2022] —
   centralised critic need not reduce policy-gradient variance [Lyu 2021]; PSRO and leagues
   [Lanctot 2017; Vinyals 2019] — empirical robustness, no loss bound; CFR in three-player
   Leduc fails to reach equilibrium [Abou Risk & Szafron 2010]. **N-player safety notions:**
   team-maxmin against a coordinated team — very conservative [Celli & Gatti 2018; Zhang 2021,
   2023]; equal share C/n — **provably not securable against opponents playing different
   strategies** [Ge 2025, Props. 4.1–4.2]; baseline-relative criteria [Müller 2025].
   KL-regularised play in seven-player Diplomacy anchors to an imitation-learned *human*
   policy, no loss bound [Jacob 2022; Bakhtin 2023]. Opponent modelling in three-player Kuhn
   beats equilibrium strategies, with no safety notion [Ganzfried 2024].
3. **Coalitions and collusion (≈ 300 w).** Nash guards only against unilateral deviation;
   coalition-proof equilibrium [Bernheim 1987]; Shapley value [Shapley 1953]; the core of an
   essential constant-sum game is empty [⚠ textbook source needed — Owen], so winner-takes-all
   alliances are temporary by construction; synchronous vs asynchronous coalitions [Babyak
   2024]. Collusion detection — collusion tables [Mazrooei 2013], mutual information [Bonjour
   2022], social-graph features [Greige 2022], probe games [Xu 2025] — **scored offline, not
   coupled to the detecting agent's play.** Testbed: So Long Sucker, a four-player bargaining
   game [Hausner et al. 1964 — not 1950]; RL agents reach ≈ half the maximum reward, coalitions
   named as future work [Sharan & Adak 2024]; endgame solved [De Carufel & Jerade 2024].
4. **Own evidence (≈ 100 w).** A per-hand floor at the game value admits only equilibrium
   strategies and gains 0.002–0.076 per hand in Kuhn — Ganzfried–Sandholm's best-equilibrium
   baseline, which their gift-based algorithms outperform (sentence frames R1 as motivation,
   not as a result). A teaching attack: an unconstrained best response still profits (+0.051/
   hand) while violating the safety floor at every refit — profit hides unsafety (→ § 1.6).
   A help/harm detector reads a planted alliance from the moves (easy case; one scripted pair).
5. **Gap C2 (≈ 75 w).**

**Table 1.2** (outside budget): safety notions — Ganzfried–Sandholm / prime-safe / adaptation
safety / SES / (N-player) team-maxmin / equal share / baseline-relative: floor · requirement ·
players · weakness. From `step08_extract` (figure candidate) + `lit_gaps.md`.

## § 1.6 Оценяване на агенти в многоагентни игри → C3 — 3.5 p, ~875 words

*Ends with the C3 gap.* Source: `lit_evaluation.md` (digest + 9 failure modes).

1. **Worst case (≈ 180 w).** Exploitability exact in small games, accelerated BR [Johanson
   2011]; lower bounds only at scale: LBR [Lisý & Bowling 2017], learned BR [Timbers 2022];
   NashConv for N players measures distance from *an* equilibrium, not a guarantee [Lanctot
   2019]. The two families disagree: indistinguishable head-to-head, ≈ 1,300 mbb/g apart in LBR
   [Moravčík 2017]; less exploitable can be worse one-on-one [Davis 2014]; ACPC's two winner
   rules [Bard 2013].
2. **Head-to-head and variance (≈ 150 w).** Duplicate play [Bard 2013]; DIVAT [Billings & Kan
   2006], unbiased estimators [Zinkevich 2006], AIVAT [Burch 2018] — not for humans [Brown
   2019], pitfalls if tuned post hoc [Kim & Sandholm 2026 ⚠], anytime-valid stopping [Li 2026
   ⚠]; ranking under noise [Rowland 2019].
3. **Populations (≈ 200 w).** Elo/TrueSkill assume transitivity [Elo 1978; Herbrich 2006];
   Elo meaningless in cycles, inflated by copies; Nash averaging [Balduzzi 2018]; limits on
   transitive games [Bertrand 2023]; α-Rank [Omidshafiei 2019]; VasE, SCO, active evaluation
   [Lanctot 2023a ⚠ arXiv, 2025, 2026]; N-player ratings [Marris 2022, 2025 ⚠; Liu 2025]. EGTA
   [Wellman 2006; Tuyls 2020; Wellman 2025]; transitive/cyclic decomposition [Balduzzi 2019];
   spinning tops [Czarnecki 2020].
4. **Generalisation and benchmarks (≈ 150 w).** Melting Pot — held-out co-players, per-capita
   return, no exploitability [Leibo 2021; Agapiou 2022]; **RRPS: the one protocol scoring
   population return and within-population exploitability together, for one two-player game**
   [Lanctot 2023b]; adversarial policies beat "superhuman" agents [Wang 2023]; LLM arenas rank
   fixed agents by win rate/rating [Duan 2024; Guertler 2025; Wang 2026 ⚠; Provost 2026 ⚠].
5. **Where it breaks (≈ 150 w).** Condense failure modes 1, 2, 4, 5, 7, 8: exploitability only
   penalises adaptation; no N-player meaning; population scores are relative (own evidence: a
   meta-Nash mixture 2.6× more exploitable than the least exploitable agent it gave zero
   weight — NashConv, one PBT run on Leduc); per-segment adaptation estimates need even more
   data; switching/deceptive opponents untested; collusion measured apart from play.
6. **Gap C3 (≈ 45 w).**

## § 1.7 Изводи, цел, задачи и теза — 3 p, ~750 words

1. **Conclusions of the analysis** (numbered, ≈ 250 w): (1) equilibrium computation is mature
   and scales, with two-player guarantees; (2) the landmark systems do not adapt, by design;
   (3) two-player opponent modelling and safe exploitation are mature and now combined in
   small games; (4) beyond two players no exploitation method carries a checked loss bound,
   and coalitions/collusion are handled only by offline detection; (5) evaluation measures
   worst case, strength and rank separately and cannot yet capture adaptation, safety and
   coalition robustness together.
2. **Goal (цел).** To develop and evaluate an adaptive agent for multi-agent
   imperfect-information games that starts from an equilibrium-based safe strategy, infers its
   opponents' strategies during play, and exploits sub-optimal opponents while keeping its
   loss relative to that baseline within an explicit, empirically verified bound, including
   when some opponents coordinate. *(Plan wording: "starts from a safe strategy but improves
   its outcome against sub-optimal opponents" — kept.)*
3. **Research questions.**
   - **RQ1 (C1):** How can an agent infer, during a match, the strategies of several
     opponents in an imperfect-information game — including shifts within the match — fast
     and reliably enough to act on the inference?
   - **RQ2 (C2):** How can deviation from an equilibrium baseline be bounded in N-player
     imperfect-information games so that exploitation gain is traded against a stated,
     empirically verifiable loss bound, also against coordinating opponents?
   - **RQ3 (C3):** How should adaptive agents be evaluated so that gain, speed of adaptation
     and worst-case (coalition-aware) robustness are measured together, with confidence, and
     unchanged across different games?
4. **Tasks (задачи)** — the plan's seven tasks, refined:
   1. Analyse existing approaches to adaptive AI in games (this chapter).
   2. Design the agent: equilibrium blueprint + online opponent inference + confidence-scaled,
      bounded deviation + detection of coordinating opponents (plan task 2, "detect fraud
      attempts").
   3. Build a simulation environment with a common agent interface for two- and N-player
      imperfect-information games (plan task 3).
   4. Create a diverse opponent population: stationary types, switching, adaptive and colluding
      opponents (plan task 4).
   5. Develop and train the adaptive agent against that population (plan tasks 5–6).
   6. Develop the evaluation methodology and test the system, including on human play or
      anonymised real game logs where available (plan task 7, "pilot users").
5. **Thesis (теза).** An agent that starts from an approximate equilibrium strategy and
   deviates from it in proportion to the confidence of its online opponent inference can
   obtain a measurable gain against sub-optimal opponents in multi-agent imperfect-information
   games while keeping its loss relative to the equilibrium baseline within a predefined,
   empirically verified bound — including when some opponents coordinate — provided that
   adaptation and robustness are measured jointly.
6. **Route through the dissertation** (≈ 80 w): Chapter II — formal framework (C1 inference,
   C2 bounded deviation, safety notions for N players); Chapter III — the system (environment,
   opponents, agent); Chapter IV — experiments and the evaluation methodology (C3). Plus the
   stage-1 report/article.

## Gap statements — the only permitted wording

Taken from `lit_gaps.md` (verified September 2026). Chapter I may narrow these, never widen.

- **C1.** Real-time opponent modelling with a conservative fallback exists and works in
  two-player games, including poker [Fu 2022; Caen 2026; Murgoci 2026], and opponent models
  have entered depth-limited search [Milec 2025]. All of it is two-player; N-player opponent
  modelling exists without any safety criterion [Ganzfried 2024]. **Open:** online inference
  in N-player imperfect-information games that handles strategy shifts *within* a match and
  is coupled to an explicit safety criterion and a common evaluation protocol.
- **C2.** Safe exploitation has a mature two-player zero-sum theory. With three or more
  players the existing notions are very conservative (team-maxmin) or provably unattainable
  against heterogeneous opponents (equal share), KL anchoring is behavioural, and multiplayer
  exploitation has no loss bound. **Open (no counter-example found):** exploiting sub-optimal
  opponents in N-player imperfect-information games while bounding the loss relative to a
  baseline, and testing that bound against colluding opponents. C2 targets this empirically,
  in small games; it claims no general N-player safety theorem.
- **C3.** Evaluation is well developed along separate axes; one benchmark combines population
  return and exploitability, for one two-player game [Lanctot 2023b]. **Open:** a protocol
  that reports gain, adaptation speed and recovery, and worst-case or coalition-aware
  robustness, with confidence bounds, applied unchanged across several imperfect-information
  games including N-player ones.

## Claims Chapter I must not make

From the extracts' "To verify" sections and the review:

- "Nobody adapts" / "no detect → adapt framework exists" / "opponent modelling is static"
  (C1 is narrowed).
- Equal share as a "guaranteed minimum"; piKL anchored to Nash; "coalition dynamics are
  unstudied"; "no N-player safety notion exists".
- "Combines exploitability + ranking + confidence" as novelty; "no cross-game evaluation".
- Any step-04 action-abstraction number (harness bug), step-05 Deep CFR number (needs rerun),
  step-11 "coalitions can be learned" (vacuous credit), the step-08 "Ganzfried" result as
  Ganzfried–Sandholm's method (it is their best-equilibrium baseline).
- So Long Sucker "1950" (published 1964); DeepStack's opponents as "top professionals";
  Loeliger rematch; the "holy grail" / "test-time compute" quotations; Libratus compute other
  than 25 M core-hours [Brown & Sandholm 2017 IJCAI demo].
- MCCFR "the only tractable approach" / "a traversal longer than the age of the universe"
  (HULHE was solved by full-traversal CFR+).
- Numbers without the model name and quantisation for LLM results.

## Open items before drafting

1. ⚠ sources marked above: read or replace (McCracken & Bowling 2004; Owen for the empty core;
   status of the 2026 preprints; Ganzfried 2025 version).
2. Decide whether § 1.1 mentions the NLHE blueprint project (`implementation/nlhe`) as
   infrastructure — it is outside steps 01–12.
3. Candidate's choices in `GLOSSARY_DECISIONS.md` (blueprint, self-play, bootstrapping) fix
   the BG terms Chapter I uses.
4. Citation format — provisional numbered IEEE-like; confirm with the supervisors.
