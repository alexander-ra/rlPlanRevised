<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->
---
title: "Chapter 13 One-Pager — Behavioral Analysis of Real Hand Histories"
subtitle: "Research on the possibilities for applying Artificial Intelligence in computer games"
author: "Alexander Andreev"
date: "September 2026"
lang: en
---

# Chapter 13 One-Pager — Behavioral Analysis of Real Hand Histories

**Problem.** Chapters 2–12 studied games that can be solved. This chapter reads what real players
did: from raw hand histories, describe a player, predict their decisions, recognize them again, type
them online, and detect collusion and bots — and measure how often each is right. Playtech data is
not available yet, so the substitute is 2,032,655 iPoker hands from July 2009 (iPoker was Playtech's
own network then), plus the 10,000 Pluribus hands as the one sample with a known bot. It is 2009
data, not Playtech's current data.

**Approach.** An own replay engine with two validators (itself and pokerkit); tracker statistics
with measured minimum samples; behavioral cloning on real decisions (6 M to train, 2 M from a later week to test); a player2vec-style
Transformer embedding tested by re-identification on unseen days; k-means types with online
Bayesian typing; colluders injected into real sessions; unsupervised bot detection on Pluribus.
Three seeds wherever training or sampling is involved. **All numbers are measured.**

**Key results (measured).**

- *The parser is the foundation.* It replays 99.77 % of the iPoker hands (the rest are incomplete)
  and catches all ten injected error types; pokerkit misses duplicate cards and truncated hands. Three
  data conventions — reversed heads-up blinds, negative "posts", all-ins hidden by missing stacks —
  each corrupted results until two replays were compared.
- *Samples differ by an order of magnitude.* VPIP is reliable (split-half r = 0.92) after 100 hands;
  3-bet needs about 500; fold-to-c-bet is at r = 0.25 after 1,000. The plan's single 500-hand rule is
  right only for the pre-flop statistics.
- *Baselines decide what accuracy means.* Cloning reaches 72.0 %, but always choosing the most
  common legal action scores 70.2 %. The player's style vector adds 0.4 points and lowers the loss
  from 0.800 to 0.751 nats, most for loose players.
- *An embedding fingerprints players.* From 400 hands per side it ranks the right player first among
  834 for 15.6 % of them (statistics 7.1 %, chance 0.12 %).
- *Styles are a continuum.* Silhouette ≤ 0.16; four k-means clusters are two tight-aggressive, one
  loose-aggressive and one loose-passive group. Stability between halves is 73.6 %, but a random
  split gives 78.2 %. Online Bayesian typing reaches a stable 0.9 posterior after a median 85 hands.
- *Collusion is found when strong.* Against 2,802 real pairs, soft play in half the heads-up
  confrontations is found for 100 % of pairs at 1 % false positives, dumping in every confrontation
  for 97 %; light collusion is mostly missed. Chapter 11's raw help/harm counts are inverted (AUC
  0.04–0.33); comparing each player with themselves and like tables with like fixes it.
- *A strong bot is not an outlier.* Five unsupervised detectors rank Pluribus 10th–14th of 14 (AUC
  0.30–0.48). Its bet sizes come from a small menu (0.14 distinct per bet vs 0.32–0.67 for the
  professionals) and it randomizes given its cards — found with the label, so hypotheses.

**Thesis connection.** This is the data layer of Contribution #1: representing, predicting,
classifying and tracking behavior from raw logs, with learned types feeding the Bayesian model of
Chapter 7. The frequency gap to Pluribus (the median regular is 9.3 points off, a professional 3.9)
marks where Chapter 8's safe exploitation would deviate. Collusion detection stays offline here, as
in the literature; coupling it to the agent's play is the open part of C2 and C3.

**Open questions.** Do the thresholds, the embedding and the collusion null carry over to Playtech's
current data? Can information-sharing collusion be injected and detected? Do the two bot signals
hold as pre-registered detectors on data with more than one known bot?
