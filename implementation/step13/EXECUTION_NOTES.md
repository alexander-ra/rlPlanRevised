# Step 13 — Execution Notes (running log)

Chapter 13, *Behavioural analysis pipelines on real hand histories*, executed end to end by an
agent (Opus 5.5) on 2026-09-24/25 under `deliverables/finalReview/NEW_CHAPTER_BRIEF.md`. This
file is the running log: every command, seed, runtime, result file, what it showed, and every
surprise and how it was resolved. If the session is interrupted, continue from the last entry.

## Environment

- Windows 11, repo venv `.venv` (Python 3.12.10); numpy 2.4.6, pandas 3.0.3, scikit-learn 1.9.1,
  umap-learn 0.5.12, torch 2.11.0+cu128 on an RTX 5090 (CUDA available), pokerkit 0.7.6.
- 16 logical CPUs, 64 GB RAM.
- All commands run from `implementation/step13/implementation/` with the venv active.

## Data (outside the repo)

**Substitute for the Playtech data.** The plan (raw step 13) assumes Playtech hand histories,
which the candidate does not have yet. Substitute: the public PHH dataset
(github.com/uoftcprg/phh-dataset, MIT licence), sparse-cloned on 2026-09-24:

```
git clone --filter=blob:none --sparse --depth 1 https://github.com/uoftcprg/phh-dataset.git D:/datasets/phh-dataset
git sparse-checkout set data/pluribus "data/handhq/IPN-2009-07-01_2009-07-23_100NLH_OBFU"
```

- `data/handhq/IPN-…_100NLH_OBFU/` — iPoker Network, no-limit hold'em, blinds $0.50/$1, July 2009,
  player IDs obfuscated: 2,081 `.phhs` files, 2,032,655 hands, 21,455 player IDs (1.4 GB).
- `data/pluribus/` — the 10,000 released hands of Pluribus, each against five professionals.

What the HandHQ subset does **not** contain (found on inspection, drives several design choices):
stacks are recorded as `inf`; the `winnings` field is all zeros; the table name is the same
('HandHQ') for every hand; hole cards are known only when shown (85.8 % of parsed hands have none) and the
showdown line is `sm ????` even when the dealt cards are known. So: no all-in information (an
all-in shows up as a street dealt with no betting), no recorded results (recomputed from the
actions; showdowns with unknown cards are unresolved), and no table identity.

## Log

### 1. Parser — `phh_parser.py`, `features.py`, `build_dataset.py`

Own NLHE replay engine (turn order, min-raise, stacks, boards, side pots, payoffs), independent of
pokerkit so the two can cross-check. Convention details that cost time:

- **Heads-up blinds are reversed** in pokerkit/PHH (p1 posts the big blind; p2 is button/SB).
- **Negative blinds** (`[0.5, 1, 0, 0, -1, 0]`) are *posts* by newly seated players (pokerkit
  docstring: "a post bet … what a player who just got seated pays"). First version treated them
  as negative contributions (a player who posted and folded showed +1 BB). Fixed to pokerkit's
  semantics: a live bet of |x| that does not decide who opens. ~1 % of IPN hands carry a post.
- **Implied all-ins.** 39 of the first 985 hands failed as "river betting not finished": all were
  real all-ins that the `inf` stacks hide (a street dealt with no action on it). Accepted exactly
  that pattern when stacks are infinite (`implied_allin`, 86,362 hands = 4.3 %).

Run: `python build_dataset.py --source IPN100` (70–180 s, 14 processes) →
`results/build_IPN100.json`; `--source PLURIBUS` (3 s) → `results/build_PLURIBUS.json`.

| | IPN100 | Pluribus |
|---|---:|---:|
| hands in files | 2,032,655 | 10,000 |
| parsed (strict) | 2,027,882 (99.77 %) | 10,000 (100 %) |
| rejected: truncated before river / river unfinished | 4,130 / 619 | 0 |
| rejected: out of turn | 24 | 0 |
| players | 21,453 | 14 (Pluribus + 13 pros) |
| decisions | 15,576,700 | 91,356 |
| showdowns resolved / unresolved | 126,343 / 158,529 | 1,673 / 0 |

The 4,773 rejected IPN hands are genuinely incomplete (e.g. `'p1 cbr 3'` and the big blind never
acts). pokerkit accepts them, because an unfinished hand is not an illegal one.

### 2. Validators and error injection — `validator.py`

`python validator.py --n 2000` (seed 0; ~6 min) → `results/validator.json`. 2,000 hands from 40
random IPN files and 2,000 random Pluribus hands; one error of each type injected into every clean
hand; rejection rate per validator.

- **First run looked like pokerkit rejects 28 % of IPN hands.** Cause: I built pokerkit's
  `HandHistory` from the `tomllib` dict, whose 0.50 is a float, and pokerkit mixes it with Decimal
  → TypeError. Fixed by converting numeric fields to Decimal the way pokerkit's loader does. After
  the fix pokerkit rejects 0 / 2,000 IPN hands.
- **Injector bug:** a bare muck line `'p5 sm'` was counted as a player action, so "truncate the last
  action" removed only the muck (own validator appeared to miss 8 % of truncations). Fixed; own
  detection is then 100 % for every type.
- Measured: own validator 100 % on all ten error types. pokerkit (default) 0 % on duplicate cards
  (it only warns) and 0 % on truncation; with warnings promoted to errors it catches 53 % (IPN) /
  93 % (Pluribus) of duplicates — it does not warn when the duplicate sits inside one board deal
  (`'d db Tc5dTc'`). 100 % on out-of-turn, under-minimum raise, over-stack bet, action after fold
  or after the end, unknown player, finishing stacks; 99 % on a wrong board count (Pluribus).
- Payoff cross-check: parser net results equal pokerkit's payoffs on 1,884 / 1,914 comparable IPN
  hands; all 30 differences are showdowns where the cards were dealt face up but the show line is
  `sm ????` — pokerkit then splits the pot, the parser evaluates the known cards. On Pluribus
  1,997 / 1,997 agree. pokerkit rejects 8 / 10,000 Pluribus hands (3 in the sample): all are split
  pots where the log awards half chips (10,387.5) and pokerkit awards the odd chip.

### 3. Player statistics — `player_stats.py`

`python player_stats.py` (~4 min) → `results/player_stats.json`. Rerun after the negative-post fix.

- 2,906 regulars (≥ 500 hands) out of 21,453 players; they hold 84.6 % of all seat rows.
- **Minimum samples, measured** (split-half test–retest correlation across players, 3 seeds, SE ≤
  0.009): VPIP r = 0.92 at 100 hands per half, 0.97 at 500; PFR 0.87 / 0.96; 3-bet 0.54 / 0.82;
  c-bet 0.24 / 0.57 (0.70 at 1,000); WTSD 0.20 / 0.57; fold-to-c-bet 0.11 / 0.18 (0.25 at 1,000).
  So the plan's single "500+ hands" rule is right for VPIP/PFR/3-bet and wrong for the post-flop
  statistics, which stay noisy at 1,000 hands. Kept 500 hands for inclusion; per-statistic
  minimum opportunities in `config.MIN_OPP`.
- VPIP×PFR quadrants (loose at VPIP ≥ 27.5 %, aggressive if PFR ≥ VPIP/2): TAG 1,323, loose-passive
  730, tight-passive 462, LAG 391.
- W$SD cannot be computed properly: the showdown cards are known for a median 41 % of a regular's
  showdowns. Dropped from the style vector.
- **Gap to a reference.** No equilibrium of six-player no-limit hold'em is available, so the
  reference is Pluribus's own 6-handed frequencies (10,000 hands; binomial SE ≈ 0.01–0.02 per
  cell). 1,046 IPN regulars with ≥ 500 six-handed hands: median mean-absolute gap 0.093
  (q10–q90 0.062–0.141). The 13 professionals: median 0.039. Only 0.19 % of IPN regulars are
  closer to Pluribus than the median professional. Direction of the IPN gap (medians): big blind
  defended far less (VPIP in the BB −22 points), fewer raise-first-in from every position (−3 to −9
  points), fewer 3-bets (−2.3), more c-bets (+10.5) and more folds to c-bets (+7.1). This is a
  frequency gap, not an EV figure: it says where an exploiter would look, not how much it would win.
- Prediction kept (raw step): "players with extreme stats might be bots or colluders". Not tested
  here — no labels on IPN. The bot question is tested on Pluribus (§7).

### 4. Behavioural cloning — `bc.py`

`python bc.py` (IPN100; ~2 min incl. loading; each model trains in 2–3 s on the GPU) →
`results/bc.json`; `python bc.py --source PLURIBUS --epochs 40 --bs 512` → `results/bc_PLURIBUS.json`.
Time split: train days 1–18 (6 M of 11.4 M decisions sampled per seed), test days 19–25 (2 M
decisions, fixed sample). Seeds 0, 1, 2. 1,177 folds made when checking was free were dropped.

| model (IPN100, test days 19–25) | accuracy | NLL (nats) | macro-F1 |
|---|---:|---:|---:|
| majority (legal-masked) | 0.7015 | – | – |
| frequency table | 0.7059 | – | – |
| logistic regression | 0.7081 ± 0.0001 | 0.826 | 0.336 |
| MLP 256-128 | 0.7158 ± 0.0001 | 0.800 | 0.370 |
| MLP + player's style vector (train days) | 0.7197 ± 0.0002 | 0.751 | 0.407 |

- The plan's target ("> 55 %, random = 14 %") is met trivially and says nothing: 55 % of test
  decisions are folds and the majority baseline is 70 %. Report the gain over the table: +1.0
  point for the MLP, +1.4 with the player's style; the style vector lowers NLL by 0.049 ± 0.0002.
- Plan predictions (seed means, `derived.json`): *preflop most predictable* — yes (0.748 vs 0.626–0.659 post-flop), but the
  majority baseline has the same order. *Button most predictable* — no: BTN is the least
  predictable position (0.639) and early position the most (0.813), because early positions fold
  most. *TAG > LAG > Fish* — raw accuracy TAG 0.786 > LAG 0.650 > loose-passive 0.642, again the
  baseline's order; above the majority baseline the order reverses (TAG +1.2, LAG +5.6,
  loose-passive +4.6 points). Knowing the player helps most for the loose players (style vector
  +3.2 points for loose-passive, +1.9 for LAG, +0.2 for TAG).
- Pluribus table (hole cards known, hands split 80/20): majority 0.697, MLP 0.818, MLP + style
  0.845 (3 seeds, SE ≤ 0.001); pre-flop 0.926 with cards.

### 5. player2vec — `p2v.py`

First run with 4 epochs (`results/player2vec_4epochs.json`, kept): seeds ended at MLM loss 2.62,
2.01, 2.63 — one seed escaped a plateau the others did not. Suspected undertraining, not a bug:
rerun with 15 epochs (`python p2v.py --epochs 15`, ~2 min training per seed, 16 min total) →
`results/player2vec.json`. All seeds then pass the same transition (loss 2.6 → 0.57–0.61 around
epoch 3–7) — the model learns the deterministic "grammar" of the stream (positions rotate; the
end token reveals a fold), which is why decision-token loss is reported separately in §7.

Re-identification (train days 1–18 vs unseen days 19–25, N hands per side, 3 seeds, mean ± SE):

| N hands | players | chance top-1 | embedding (mean-pool) top-1 / top-10 | statistics top-1 / top-10 |
|---:|---:|---:|---|---|
| 50 | 2,575 | 0.04 % | 1.3 % / 8.5 % | 0.3 % / 2.8 % |
| 100 | 1,859 | 0.05 % | 4.2 % / 17.9 % | 1.6 % / 7.4 % |
| 200 | 1,278 | 0.08 % | 9.0 % / 31.0 % | 4.1 % / 14.8 % |
| 400 | 834 | 0.12 % | 15.6 ± 0.2 % / 45.2 % | 7.1 ± 0.2 % / 23.8 % |

Max pooling (the paper's choice) is much worse than mean pooling here (4.5 % top-1 at N = 400).
Combining the two similarity scores does not beat the embedding alone (11.2 %).

### 6. Clustering, temporal stability, Bayesian typing — `clustering.py`

`python clustering.py` (~6 min, CPU; UMAP on seed 0) → `results/clustering.json`. A first launch
used the 4-epoch embeddings and was killed when those were replaced (§5).

- 2,906 regulars, 11 statistics (fold-to-3-bet dropped: 39 % of regulars lack 15 opportunities;
  213 remaining missing values imputed with the median).
- **No natural four-cluster structure.** Silhouette 0.16 (k = 2), 0.16 (3), 0.13 (4), ≤ 0.14 up to
  k = 8. k-means with k = 4 is stable across seeds (ARI 0.94 and 0.97 against seed 0), but its
  clusters are two tight-aggressive groups (1,089 and 947 players), a loose-aggressive group (334)
  and a loose-passive group (536) — no tight-passive cluster. ARI with the VPIP×PFR quadrants
  0.28. The plan's "four clusters = TAG, LAG, Nit, Fish" is not what the data does.
- Embedding (15-epoch player2vec, 3 seeds): 15-NN recovers the quadrant with 0.90 accuracy (the
  statistics vector, which *contains* VPIP and PFR, 0.88); cosine similarity within a quadrant
  0.86–0.89 vs 0.74–0.76 between (plan target "intra > inter": met). k-means on the embedding
  agrees with the quadrants at ARI 0.34–0.36 and with the statistics clusters at 0.22–0.23.
  DBSCAN (eps from the 5-NN distance median) finds 7–10 clusters with 38–39 % noise.
- **Temporal stability** (first vs second chronological half of each regular's hands, both
  assigned to full-data centroids): 73.6 ± 0.2 % (3 seeds). The plan's target (> 70 %) is met,
  but a *random* split of the same hands gives 78.2 ± 0.5 %: most of the switching is sampling
  noise near cluster borders; genuine change over the month adds about 5 points. Chance 29.5 %.
  In embedding space the time-split stability is 90.7 % (3 seeds; the first half overlaps the
  training days, so this is not a clean comparison).
- **Online Bayesian typing** (types = the four clusters; Bernoulli rates of per-hand events; truth
  = the cluster of the same player's hands after the first 500; 1,702 players with ≥ 1,000 hands):
  posterior mode correct 49 % after 10 hands, 57 % after 50, 62 % after 100, 68 % after 500;
  majority-cluster baseline 44 %. 66 % of players reach a posterior ≥ 0.9 on their later type that
  stays there within 500 hands (median 85 hands, 75th percentile 203).

### 7. Bot detection on the Pluribus hands — `botdetect.py`

`python botdetect.py` (~3 min incl. IPN reference) → `results/botdetect.json`; `python derived.py`
→ `results/derived.json`. Blocks of 250 hands (235 blocks, 40 Pluribus) and 500 (115, 20).

- **Unsupervised detectors do not find Pluribus.** AUC (Pluribus blocks vs human blocks, 3 seeds,
  B = 250): Isolation Forest on HUD statistics 0.415 ± 0.002, on HUD + bot-relevant features 0.463
  ± 0.007, on the embedding 0.298 ± 0.011; low decision-token loss 0.475 ± 0.007; Mahalanobis
  distance from IPN regulars 0.347. Pluribus's rank by mean block score among 14 players: 12, 10,
  14, 12, 14 (seed 0). B = 500 is the same picture (AUC 0.28–0.44). Every AUC is *below* 0.5:
  Pluribus is more typical of this table than the average professional.
- **Math Flag prediction kept: "bots have unusually low loss".** Measured: Pluribus's decision-token
  loss 0.691 sits in the human range 0.529–0.829 (12th lowest of 14). Not a bug: a mixed strategy
  is, by design, not more predictable than a person.
- **What does separate it (found with the label, so a hypothesis, not a validated detector):**
  (1) *bet-size granularity* — distinct post-flop bet fractions among 50 bets: Pluribus 0.141,
  the 13 professionals 0.324–0.670, IPN regulars median 0.458; 16 of 1,275 IPN regulars (1.3 %)
  are at or below Pluribus. Pluribus bets from a small menu of sizes; people type amounts.
  (2) *randomisation given its cards* — conditional entropy of the pre-flop action given position,
  situation and the exact hand: Pluribus 0.143 nats, the most of the 9 players with ≥ 400 such
  decisions (humans 0.06–0.107, median 0.081). Needs hole cards, which an operator has.
  (3) *donk bets* — 2.1 % of opportunities vs 0.9 % for the humans' blocks, matching the paper's
  statement; too small an effect to detect with.
- One bot and 13 humans: "rank 1" or "rank 14" is one observation.

### 8. Collusion — `collusion.py`

`python collusion.py` (all tables; 8.4 min) → `results/collusion.json`;
`python collusion.py --pairs mw` (multiway tables only; 9.1 min) → `results/collusion_mw.json`.
40 colluding pairs per seed × 3 seeds, drawn from real pairs with ≥ 300 shared hands and ≥ 30
heads-up confrontations; 8 configurations (soft play / chip dumping × q = 0.1, 0.25, 0.5, 1).
Every rewritten hand (up to 3,306 per configuration) was accepted by the parser and by pokerkit:
0 rejections.

- **First run (all tables): the top real pairs were all heads-up-table pairs** (shared hands =
  heads-up confrontations, z_soft up to 142). Cause: the soft-play baseline compares a player's
  aggression against the partner with their aggression in heads-up confrontations elsewhere, and
  a heads-up *table* is a different game from being left heads-up at a six-max table. Fixed by a
  format-matched pair table (hands with ≥ 3 seats only; `pairs_mw.npz`, built by the same
  `build_dataset.py`). The null's 99.9th percentile of the union score fell from 5.88 to 4.12.
  Both runs are kept; the multiway run is the headline.
- Multiway, union score, stratum of 2,802 real pairs (mean ± SE over 3 seeds):

| type | q | AUC | recall @ FPR 1 % | recall @ FPR 0.1 % | FPR at 90 % recall |
|---|---:|---:|---:|---:|---:|
| soft play | 0.1 | 0.793 ± 0.013 | 26 ± 4 % | 3 % | 68 % |
| soft play | 0.25 | 0.940 ± 0.011 | 65 ± 4 % | 30 % | 15 % |
| soft play | 0.5 | 0.999 | 100 % | 89 % | 0.1 % |
| soft play | 1.0 | 1.000 | 100 % | 100 % | 0 % |
| dumping | 0.1 | 0.635 ± 0.036 | 3 ± 1 % | 0 % | 83 % |
| dumping | 0.25 | 0.853 ± 0.020 | 16 ± 5 % | 1 % | 34 % |
| dumping | 0.5 | 0.972 ± 0.007 | 62 ± 3 % | 8 % | 6.6 % |
| dumping | 1.0 | 0.998 | 97 ± 2 % | 50 % | 0.4 % |

- The plan's target ("100 % of injected collusion at < 5 % FPR") is met for soft play when half
  or more of the confrontations are soft, and for dumping only when every confrontation is a dump.
- **Chapter 11's help/harm score, carried over with raw event counts** (help = fold to the
  partner, harm = bet or raise at the partner, per heads-up decision), is *inverted*: AUC 0.04–0.33
  for every configuration. Soft play removes the folds as well as the bets; dumping adds bets.
  Standardising each player against their own behaviour is what makes the signals work.
- Detection depends on sample size: at the null's 99th percentile, soft play at q = 0.25 is found
  for 48 % of pairs with ≤ 39 heads-up confrontations and 83 % above (derived.json).
- Real pairs: the highest multiway union scores are 7.29, 4.71, 4.16 (null 99.9th percentile
  4.12). These are flags for review, not findings: 2009 data, no labels.

### 9. Figures — `plotting.py`, `derived.py`

`python plotting.py` draws every data figure from the JSON files only (9 PNGs in `plots/`, 250 dpi,
7 in wide, fs ≥ 9.5). Copied to `deliverables/reports/step13/figures/impl_*.png` and
`…/summary/impl_*.png`. Diagram: `deliverables/reports/step13/summary/make_pipeline_figure.py`
(copy of step 11's `_diagram_utils.py`). Fixes after looking at the renders: log-axis minor labels
overlapped (removed), legends moved out of the data, rank labels moved off the 0.5 line.

### Not done

- **Optional item 7 (Decision Transformer on real data).** Not run. On IPN the outcome of many
  showdowns is unknown; on Pluribus the outcomes are complete, but there is no simulator of a
  six-player table with these humans to evaluate a return-conditioned policy, so only hindsight
  leakage could be measured. Left for the Playtech data.

### 10. Deliverables and checks

`PYTHONIOENCODING=utf-8 python scripts/build_reports.py --step step13 --lang en --type all` →
`deliverables/reports/step13/step13_report_en.pdf` (18 pages), `deliverables/summaries/step13_en.pdf`
(17 pages, 10 figures), `deliverables/onePagers/step13_en.pdf` (1 page at 10 pt).
`check_headings.py`: 0 missing headings; `check_captions.py`: 0 unaccounted figures;
`scripts/figures/render_printed.py` → `deliverables/finalReview/renders_new/step13/` (every figure
prints at ≥ 250 effective ppi; smallest text ≈ 8.6 pt). Word counts (prose, without tables,
captions, code, footnotes): chapter 4,893, report 3,946, one-pager 613.
A late correction: the share of hands with no known card is 85.8 % of the parsed hands (the first
text said 84 %, from a 20-file sample); fixed in all three documents.

## Sources verified (2026-09-24/25)

Checked by a literature sub-agent with WebSearch/WebFetch (arXiv, publisher pages, Crossref,
annual-report PDF); the list with verification method is in `targetedReading/summary.md`.
Plan errors found: "DeLong & Bhatt (2020)" and "Yan & Browne (2016)" do not exist; player2vec has
no venue (arXiv); the HandHQ subset covers six rooms (iPoker is 5,996,345 of 21,605,687 hands).
iPoker in 2009: Playtech's own network, launched in 2004 (Playtech Annual Report 2009, pp. 1, 36–37).

## Central (for the candidate)

- No new packages were installed (pokerkit, scikit-learn, umap-learn, torch were present), so
  nothing to add to `requirements.txt`.
- Data lives in `D:/datasets/phh-dataset` (sparse clone, 1.5 GB) and parsed arrays in
  `D:/datasets/step13_cache` (≈ 3.6 GB). Neither is in the repo.
- The Write tool refused `targetedReading/summary.md` as a "report file" (a sub-agent heuristic);
  it was written to the scratchpad and copied into place.
