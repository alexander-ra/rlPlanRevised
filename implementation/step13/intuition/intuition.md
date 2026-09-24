# Step 13 — Intuition: behavioural analysis on real hand histories

## The problem in one paragraph

Chapters 2–12 computed what a strong strategy *should* do in a game we could solve. This step turns
the telescope around: it looks at what real people *did*, in a record of millions of online poker
hands, and asks what can be learned about them from that record alone. A poker site logs every
action: who bet, how much, who folded, who won. From such logs one can try to describe a player
(tight or loose, passive or aggressive, predictable or not), predict their next action, recognise
the same person again, notice when two accounts help each other (collusion) and notice when an
account is not a person at all (a bot). None of this needs the game to be solved; all of it needs a
careful data pipeline, because every later number inherits every parsing mistake.

## A picture to hold onto

A casino security room with the cameras switched off and only the dealer's logbook left. The log
says "seat 3 raised to 4, seat 5 folded". A floor manager who reads enough pages learns each
regular's habits, spots the two who never raise each other, and notices the one who plays at three
tables all day with the same rhythm. The pipeline in this step is that floor manager, written
down: parse the logbook, summarise each player, model their decisions, compare pairs, flag the odd
ones — and, crucially, measure how often the flags are right.

## The approaches, compared

| Approach | What it does | Reach for it when | Main weakness |
|---|---|---|---|
| Tracker statistics (VPIP, PFR, 3-bet, c-bet, WTSD …) | Count / opportunities, per player | You need interpretable profiles | Noisy on small samples; each needs its own number of hands |
| Behavioural cloning | Predicts the action from the state | You want a baseline model of "what people do here" | Most decisions are easy folds, so raw accuracy flatters it |
| Sequence embeddings (player2vec) | Learns a vector per player from their action stream | You want similarity, retrieval, clustering without choosing features | Harder to interpret; depends on the tokenisation |
| Clustering into archetypes | Groups players by style | You want a small set of types (e.g. a prior for Bayesian modelling) | Real styles form a continuum; "four archetypes" is a convention |
| Pairwise collusion signals | Compares how two players treat each other with how they treat everyone | Fair-play monitoring | No real labels exist; must be validated on injected cases |
| Anomaly detection for bots | Flags accounts unlike the rest | Fair-play monitoring | A strong bot can look like a strong human |

## How the field got here (short timeline)

- **2003–2008** — collusion in online card games is described and taxonomised (information sharing,
  soft play, chip dumping); early proposals, few experiments.
- **2005** — *Bayes' Bluff* (Southey et al.): Bayesian opponent models over strategy types in poker.
- **2009–2015** — large hand-history datasets are sold commercially and used by economists and
  psychologists to study skill and risk taking in online poker.
- **2011** — first attempts to cluster real online players into types and to clone their play from
  logs (Teófilo & Reis).
- **2013** — *collusion tables* (Mazrooei, Archibald & Bowling): collusion detection in three-player
  limit hold'em, validated on synthetic colluders because no labelled human data exists.
- **2019** — Pluribus beats professionals at six-player no-limit hold'em and its hands are released.
- **2022** — information-theoretic collusion detection (Bonjour et al.), again on synthetic colluders.
- **2024** — *player2vec*: language-model embeddings of player event streams in a mobile game; open,
  machine-readable poker hand histories (PHH format, PokerKit).

## Easy to get wrong

- **Accuracy without a baseline.** In real data more than half of all decisions are folds. A model
  that always folds when facing a bet is right most of the time. Always report the majority and the
  frequency-table baseline next to the model.
- **Statistics on too few hands.** VPIP is stable after about a hundred hands; fold-to-c-bet is not
  stable after a thousand. One threshold for all statistics is wrong.
- **"Detected 100 %" without a false-positive rate.** Any detector can flag every pair. The number
  that matters is recall at a fixed, small false-positive rate over thousands of real pairs.
- **Real data has no collusion labels.** Validation must use injected colluders, and the real pairs
  used as negatives are *presumed* clean, not known to be.
- **Luck is in the outcome.** Conditioning a model on how a hand ended leaks information the player
  did not have (Paster et al. 2022, Chapter 12).
- **The data is not the future data.** This step uses iPoker hands from July 2009. The Playtech data
  the plan assumes remains the real validation.

## You should be able to answer

1. What do VPIP, PFR, 3-bet %, c-bet % and WTSD measure, and what is the *opportunity* for each?
2. Why is 70 % action-prediction accuracy unimpressive on this data, and what number should be quoted instead?
3. How can a player embedding be tested when there are no labels?
4. What are soft play and chip dumping, and which statistic reveals each?
5. Why can a collusion detector be validated only on injected collusion here?
6. What would make a bot look human, and what would give it away?

## Key takeaways for the final summary

- The pipeline is the C1 core: represent (statistics, embeddings), classify (clusters, Bayesian types),
  predict (cloning) and track (temporal stability) behaviour from raw logs.
- Every claim needs a baseline and a sample size; the step measures both explicitly.
- Collusion and bot detection are validated on injected cases and on the one known bot; real-data
  flags stay flags, not findings.
