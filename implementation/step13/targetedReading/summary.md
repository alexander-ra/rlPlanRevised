# Step 13 — Targeted reading (verified sources only)

Every entry below was checked online on 2026-09-24/25 (arXiv abstract or HTML, publisher or
proceedings page, Crossref; the check is named in brackets). Two papers in the raw step's reading
list could not be found and are replaced (see "Corrections to the plan").

## Corrections to the plan

- **"DeLong & Bhatt (2020), Towards Collusion Detection in Poker"** — not found in Crossref, on the
  web or by title search. Treated as non-existent. The closest real work is Bonjour, Aggarwal &
  Bhargava (2022) and Mazrooei, Archibald & Bowling (2013), below.
- **"Yan & Browne (2016), Collusion Detection in Online Poker"** — not found; Jeff Yan's publication
  list has no co-author Browne. Yan (2010, AAAI) is a position paper on collusion in *bridge*.
- **Kim et al. (2025) on MMORPG bots** is also an ICPR 2024 proceedings paper (cite the proceedings).
- **player2vec** has no venue: it is an arXiv preprint (KTH/King), part of a KTH doctoral thesis.

## Sources

### Wang et al. (2024) — player2vec  *(role: the embedding method this step adapts)*
Wang, T., Honari-Jahromi, M., Katsarou, S., Mikheeva, O., Panagiotakopoulos, T., Asadi, S. &
Smirnov, O. (2024). "player2vec: A Language Modeling Approach to Understand Player Behavior in
Games." arXiv:2404.04234. [arXiv abstract + HTML v3; KTH DiVA record]
- **Idea.** In-game events are tokens, a session is a sentence; a Longformer is pre-trained with
  masked language modelling (MLM) on 125,000 sessions of 10,000 players of a casual mobile game over
  15 days; final-layer token states are max-pooled into one vector per player.
- **Evaluation.** MLM accuracy/perplexity by model size (e.g. large: accuracy 0.958 ± 0.007) and a
  qualitative reading of 8 Gaussian-mixture clusters. No quantitative test of what the embedding
  captures (no retrieval, no silhouette/ARI).
- **For this step.** Same recipe, poker tokens (position × table size; street × facing × multiway ×
  action; hand end). Added what the paper lacks: a quantitative test (re-identification of the same
  player on unseen days) and a comparison with hand-crafted statistics.

### Kumar, Hong, Singh & Levine (2022)  *(role: when cloning is the right baseline)*
Kumar, A., Hong, J., Singh, A. & Levine, S. (2022). "When Should We Prefer Offline Reinforcement
Learning Over Behavioral Cloning?" *ICLR 2022*. arXiv:2204.05618. [arXiv abstract + ar5iv]
- **Claim.** Under sparse rewards or noisy data, offline RL can beat BC, even BC on expert data,
  especially at long horizons; BC is competitive when data is expert and the structural conditions
  are absent.
- **For this step.** Poker logs are noisy human play with sparse, luck-dominated rewards, so BC is
  a *description* of behaviour (a baseline), not a strong policy. This step uses BC only to model
  and predict behaviour, not to play.

### Collusion detection in poker
- **Mazrooei, P., Archibald, C. & Bowling, M. (2013).** "Automating Collusion Detection in
  Sequential Games." *AAAI* 27(1), 675–682. [full text] Three-player limit hold'em; colluders are
  synthetic (CFR strategies with utility û_i = u_i + λu_j); "collusion tables" score pairs by
  impact on value. They were "not aware of a suitable human dataset with known colluders".
- **Bonjour, T., Aggarwal, V. & Bhargava, B. (2022).** "Information Theoretic Approach to Detect
  Collusion in Multi-Agent Games." *UAI*, PMLR 180, 223–232. [full text] Pairwise conditional
  mutual information; three-player RPS and Leduc; synthetic colluders; over 95 % accuracy after
  about 1,000–1,800 Leduc hands. States that no public dataset with known collusion exists.
- **Smed, J., Knuutila, T. & Hakonen, H. (2007).** "Towards Swift and Accurate Collusion
  Detection." *GAME-ON 2007*, 103–107. [full text] Argues synthetic data should come first and be
  verified later on real cases; builds a synthetic testbench.
- **Vallvè-Guionnet, C. (2005).** "Finding Colluders in Card Games." *ITCC 2005*, Vol. II,
  774–775. [Crossref] Short paper listing detection ideas.
- **Yampolskiy, R. V. (2008).** "Detecting and Controlling Cheating in Online Poker." *IEEE CCNC*,
  848–853. [Crossref] Taxonomy of cheating; bot prevention by a CAPTCHA-like mechanism.
- **Greige, L. et al. (2022).** "Collusion Detection in Team-Based Multiplayer Games."
  arXiv:2203.05121 (real data, not poker; Isolation Forest + social graph). [lit_gaps.md]
- **Synthesis.** Every poker collusion paper found validates on synthetic colluders. None couples
  detection to what the detecting agent does next (lit_gaps.md, C2 "Collusion detection").

### Southey et al. (2005) — Bayes' Bluff  *(role: the Bayesian typing re-used from Chapter 7)*
Southey, F., Bowling, M., Larson, B., Piccione, C., Burch, N., Billings, D. & Rayner, C. (2005).
"Bayes' Bluff: Opponent Modelling in Poker." *UAI 2005*, 550–558. arXiv:1207.1411. [arXiv]
- Posterior over opponent strategies from observed actions (and cards at showdown). In this step
  the "types" are learned clusters of real players and the posterior is updated hand by hand.

### Brown & Sandholm (2019) — Pluribus  *(role: the known bot and the strong reference)*
Brown, N. & Sandholm, T. (2019). "Superhuman AI for multiplayer poker." *Science* 365(6456),
885–890. [main text + supplement PDFs]
- 10,000 hands over 12 days; each day five of 13 professionals; blinds 50/100, every hand starts
  at 10,000 chips (100 big blinds); 48 mbb/game, standard error 25, after AIVAT.
- Style: Pluribus "confirms the conventional human wisdom that limping ... is suboptimal for any
  player except the 'small blind' player" and "disagrees with the folk wisdom that 'donk betting'
  ... is a mistake; Pluribus does this far more often than professional humans do." It considers
  between 1 and 14 bet sizes per decision; it "plays a fixed strategy that does not adapt".
- **For this step.** The ground truth for bot detection, and the 6-player reference for the "gap".

### Kim et al. (2024) — collectively-behaving bots  *(role: embedding + clustering for bots)*
Kim, H., Kim, J. H., Son, J., Song, J. & Lee, E. (2024). "A Framework for Mining
Collectively-Behaving Bots in MMORPGs." *ICPR 2024*, LNCS 15309, 400–419; arXiv:2501.10461.
[arXiv + Crossref] Transformer trajectory encoder (contrastive + masked-cell prediction), then
DBSCAN; evaluated without precision/recall (no labels).

### Paster, McIlraith & Ba (2022)  *(role: the luck warning, from Chapter 12)*
Paster, K., McIlraith, S. & Ba, J. (2022). "You Can't Count on Luck: Why Decision Transformers and
RvS Fail in Stochastic Environments." *NeurIPS 35*, 38966–38979. [NeurIPS proceedings]

### Data and tools
- Kim, J. (2024). "Recording and Describing Poker Hands." *IEEE CoG 2024*;
  arXiv:2312.11753 (v1 titled "Poker Hand History File Format Specification"). [arXiv + Crossref]
- Kim, J. (2025). "PokerKit: A Comprehensive Python Library for Fine-Grained Multivariant Poker
  Game Simulations." *IEEE Transactions on Games* 17(1), 32–39. [Crossref]
- phh-dataset (github.com/uoftcprg/phh-dataset, MIT on GitHub, CC-BY-4.0 on Zenodo): HandHQ subset of
  21,605,687 no-limit hands, July 2009, six rooms; iPoker Network 5,996,345 of them.
- Playtech Limited (2010), *Annual Report and Accounts 2009*: iPoker launched by Playtech in 2004;
  "Playtech's exclusive poker network, iPoker"; "designed to protect licensees and players against
  collusion and fraud" (pp. 1, 36–37). [annual report PDF]

### Real-data context
- Teófilo, L. F. & Reis, L. P. (2011). "Identifying Player's Strategies in No Limit Texas Hold'em
  Poker through the Analysis of Individual Moves." *EPIA 2011*; arXiv:1301.5943 — clustered
  158,035 real players (7 types); defines AF = (bets + raises) / calls.
- Siler, K. (2010). "Social and Psychological Challenges of Poker." *J. Gambling Studies* 26(3),
  401–420 — ~27 million online hands; tight-aggressive play more prevalent at higher stakes.
- Potter van Loon, R. J. D., van den Assem, M. J. & van Dolder, D. (2015). "Beyond Chance? The
  Persistence of Performance in Online Poker." *PLOS ONE* 10(3), e0115479.

## Worked math flag — Bayesian typing (to be checked)

Types t ∈ {1..4} with per-hand event rates θ_t,e (VPIP, PFR, limp per hand; 3-bet, c-bet, WTSD,
steal per opportunity). After hands 1..n with event indicators x and opportunity indicators o,

  log P(t | data) = log π_t + Σ_hands Σ_e o_e [x_e log θ_t,e + (1 − x_e) log(1 − θ_t,e)] + const.

Worked example in the spirit of the plan (100 hands, VPIP 35 %): two types differing only in VPIP
(0.22 vs 0.35), equal priors. The VPIP log-likelihood ratio is
35 ln(0.35/0.22) + 65 ln(0.65/0.78) = 16.25 − 11.85 = 4.40, a posterior of about 0.988 for the
loose type from VPIP alone. The real types in this step differ on several events at once; the
measured concentration speed is in `implementation/results/clustering.json` ("bayes").

## Verify when you read it

- player2vec's pooling (max) and model sizes (Table 1) — this step uses mean pooling by default and
  reports max pooling alongside.
- Mazrooei et al.'s numbers (colluders rank 1–4 of 91 pairs) before citing them.
- Bonjour et al.'s hands-to-95 % figures (§5) before citing them.

## Key takeaways for the final summary

- The embedding method is a preprint without a quantitative evaluation of the embedding itself;
  this step adds one (re-identification on unseen days).
- All published poker collusion detectors were validated on synthetic colluders; this step injects
  colluders into *real* sessions, which is closer to deployment but still synthetic collusion.
- Pluribus's paper names its behavioural differences (donk bets, no limping outside the small
  blind) — the natural first features for a bot detector.
