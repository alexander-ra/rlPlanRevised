# Experiment specifications (Chapter 15)

*Written against Chapter 14's joint protocol (`implementation/step14/implementation/`,
definitions in its README) and Chapter 13's pipeline (`implementation/step13/implementation/`).
Every experiment reports the protocol's readouts with 95 % intervals over seeds, names its
estimator, fixes and records its seeds, and keeps the plan's original hypothesis next to any
revision. "Pilot" rows point to the feasibility runs of this chapter (`EXECUTION_NOTES.md`,
`implementation/results/`). Pilot numbers are feasibility evidence, not results of the
contribution.*

Common conventions:

- **Seeds.** Deck order from the seed (common random numbers across agents), duplicate seats
  for two players, seat rotation for three; ≥ 10 seeds for two-player claims, ≥ 5 seeds × all
  seats for three-player claims; a claim about a difference uses paired comparisons on the same
  seeds.
- **Statistics.** Mean ± 1.96·SE over seeds; paired t-test (or Wilcoxon signed-rank when the
  per-seed differences are clearly non-normal) on per-seed differences; Holm correction across
  the opponents of one table; effect sizes in chips/hand next to every p-value; no
  "indistinguishable" without an equivalence margin stated in advance.
- **Estimators.** Policy-exact EV for bot-vs-bot runs (no card noise), AIVAT with the agent's
  strategy known where the opponent is unknown, raw chips only for human data.
- **Budgets.** Every learned exploiter or learned coalition is reported with its training
  budget; exact worst cases are used wherever the game allows enumeration.

---

## Experiment 1.1 — within-match opponent inference (C1)

**Plan's hypothesis (kept):** player2vec embeddings + Bayesian type inference classify
opponent types from the bot zoo within 50 hands with > 80 % accuracy on Kuhn.

**Revised hypothesis H1.1.** In three-player Kuhn and three-player Leduc, a per-opponent
Dirichlet model with posterior-weighted hidden cards, a log-learned prior and multi-signal change
detection (a) reaches half of the attainable gain (capture ≥ 0.5) against stationary sub-optimal
opponents within h50 ≤ 200 hands (Kuhn) / ≤ 1,000 (Leduc); (b) recovers after a within-match
switch with r50 finite in ≥ 80 % of matches; (c) raises ≤ 1 false change alarm per 1,000 hands
against stationary opponents; (d) has calibrated confidence (predicted vs realised window gain,
calibration slope within [0.8, 1.2]). *Why revised:* classification accuracy of zoo types is a
means, not the aim; Chapter 13 found no natural four-type structure in real players
(silhouette ≤ 0.16), and Chapter 14 showed that the operative quantities are gain, speed and
recovery.

| Item | Specification |
|---|---|
| Independent variables | opponent model (type-based / Dirichlet / Dirichlet + log prior); change detection (none / single-signal BOCPD / multi-signal with partial reset); game (Kuhn, Leduc, 3-player Kuhn, 3-player Leduc); opponent schedule (stationary, one switch at T/2, switches every 500 hands, teaching bait) |
| Dependent variables | gain, capture, h50, r50, switch cost (300 hands), false-alarm rate, calibration slope; with C2's deviation rule attached: baseline-relative loss L and realised loss |
| Protocol | Chapter 14's `run_adaptation.py` / `run_nplayer.py` harness; 2,000 hands (two-player, three-player Kuhn), 5,000 (three-player Leduc); refit every 50 hands |
| Baselines | blueprint (floor); oracle best response to the true opponent (ceiling); DirBR3P (Chapter 14); a GSCU-style bandit between blueprint and greedy response (Fu et al. 2022) |
| Success criteria | H1.1 (a)–(d); all four on three-player Kuhn is the Stage II milestone |
| Statistics | 10 seeds × seats; median h50/r50 with bootstrap intervals; share of matches reaching r50 |
| Compute | ≈ 20 min (Kuhn), ≈ 2 h (three-player Leduc, 16 cores) |
| Evidence so far | Kuhn h50 = 50 hands for every adaptive agent; r50 50–850 hands or never; change-point detector misfires on Leduc; DirBR3P captures 0.99 within 50 hands against independent pairs (Chapter 14) |

**Experiment 1.2 — real-data arm.** Chapter 13's online Bayesian typing and embedding run
chronologically over the IPN hand histories (2,906 regulars): hands to a confident type (≥ 0.9),
agreement with the type of the player's later hands, re-identification across days, and the
collusion scores computed online. Success: the online model's confident type agrees with the
later-hands type ≥ 70 % (Chapter 13 offline: 66 % confident within 500 hands, median 85). On
Playtech data if access is granted; otherwise IPN only.

---

## Experiment 2.0 — the two-player C2 baseline (done in this chapter: Pilot P1)

Ganzfried & Sandholm's RWYWE, BEFEWP and best equilibrium against Chapter 14's Kuhn and Leduc
populations, switching opponents and a teaching attacker that re-targets every hand; readouts as
above plus match-level safety S. Result files `protocol2p_{kuhn,leduc}.json`; the replication of
G&S's Table I is `gs_replication.json`. This is the two-player reference every N-player method
of C2 is compared with, and the baseline Chapter 8 lacked (TRIAGE R1).

**Outcome (10 seeds × 2 seats × 2,000 hands).** RWYWE gains +0.062 ± 0.002 (Kuhn) and +0.113 ±
0.001 (Leduc) over the blueprint — 3.1× and 2.4× the best equilibrium — and is safe over the match
in all 120 attacked matches; RNR(0.5) gains +0.210 and +0.797 with no guarantee; DirBR falls below
v* in 52 of 120 attacked matches. The replication reproduces G&S's safety result and orderings,
with the safe algorithms 0.001–0.033 chips/hand below their levels; the best-response row is not
reproduced (open).

**Follow-ups for Stage II.** Within-hand gift detection (G&S § 8.3) and a less pessimistic
off-path assumption, since the showdown-only bank stayed at 0.01–0.02 chips on Leduc; the
equal-budget Leduc comparison of TRIAGE R2 is superseded by Chapter 14's one-shot LP, which
solves every Leduc safe response in 0.02–0.04 s.

---

## Experiment 2.1 — N-player safe exploitation on three-player Kuhn (C2)

**Plan's hypothesis (kept):** piKL-regularised exploitation can achieve payoff > C/3 against
sub-optimal opponents while maintaining payoff ≥ C/3 − ε against adversarial opponents.
*Why it cannot stand as written:* equal share C/n is provably not securable against opponents
that play different strategies (Ge et al. 2025, Prop. 4.1), and piKL anchors to a human-imitation
policy, not to an equilibrium (Jacob et al. 2022; Bakhtin et al. 2023).

**Revised hypotheses.**

- **H2.1a (baseline-relative cap).** A deviation from the blueprint whose worst-case
  baseline-relative loss L(σ) (maximum over all coordinated opponent pairs of the blueprint's
  payoff minus the agent's) is capped at ε per hand keeps a share of the unbounded exploiter's gain
  against heterogeneous independent pairs that grows with ε, and its realised baseline-relative
  loss under fixed and adaptive colluding pairs never exceeds ε.
- **H2.1b (maximin floor).** Ganzfried & Sandholm's gift accounting with the team-maxmin value
  v_mm in place of v* (their § 2.3) earns more than the stationary maximin strategy against
  sub-optimal pairs while its match-level safety S = mean(EV − v_mm) stays ≥ 0 against *every*
  opponent condition, including adaptive colluders.
- **H2.1c (KL anchoring).** A KL-anchored response to the model (anchor: the blueprint — the
  thesis's own proposal) reaches a better gain-for-L trade-off than the sequence-form mixture.

| Item | Specification |
|---|---|
| Independent variables | deviation rule (mixture with cap ε; KL anchor with β; maximin-floor RWYWE; unbounded best response); ε ∈ {0.01, 0.03, 0.1, 0.3, ∞}; β ∈ {1, 3, 10, 30}; confidence schedule n₀; card observation for the gift accounting (always / showdown only) |
| Opponent configurations | seven independent pairs (weak–weak, weak–equilibrium, homogeneous and heterogeneous); a fixed colluding pair (the exact coalition best response to the blueprint); an adaptive colluding pair (bait, then the exact coalition best response to the agent's current policy, every 50 hands) |
| Dependent variables | gain over the blueprint (seat-averaged); L(σ_t) of every policy in force (exact); realised per-hand baseline-relative loss; coalition value of the final policy; match-level S against v_mm; seat-averaged EV against the equal-share line (0) and the maximin line |
| Protocol | 3 seats × ≥ 5 seeds × 2,000 hands; exact per-hand EVs of the agent and of the blueprint against the same opponent strategies |
| Baselines | Nash blueprint; the stationary maximin strategy; DirBR3P (unbounded); Blend3P (fixed 50/50 behaviour mix); the best maximin strategy against the model (k fixed at 0) |
| Success criteria | H2.1a: realised loss ≤ ε in every hand, and at ε = 0.1 a gain ≥ 25 % of DirBR3P's; H2.1b: S ≥ 0 within its 95 % interval in every condition, and gain > the stationary maximin strategy's against sub-optimal pairs; H2.1c: KL's gain at equal L above the mixture's line |
| Statistics | per-seed seat averages; paired comparisons against the blueprint on the same seeds |
| Compute | ≈ 15 min on 14 cores (exact enumeration: 6,561–10,000 unique pure plans of one opponent per call) |
| Pilot | P2 (`bounded3p.json`, `maximin3p.json`) — see `EXECUTION_NOTES.md` |
| Pilot outcome (2026-09-25, 5 seeds × 3 seats; hypotheses above were written before the run) | H2.1a: the cap held in every hand (yes); gain at ε = 0.1 was 16 % of DirBR3P's (no; 49 % at ε = 0.3). H2.1b: S ≥ 0 in every match of every condition (yes); MM-RWYWE +0.082 vs the maximin strategy's +0.032 (yes). H2.1c: no for L ≤ 0.7, yes near full deviation — but KL is clearly better on EV under adaptive colluders, so the two robustness readouts rank the rules differently |
| Scaling arm (Stage III) | three-player Leduc: exact enumeration is impossible, so L and the coalition value come from a learned coalition exploiter with a stated budget, calibrated against the exact values on three-player Kuhn |

---

## Experiment 2.2 — coalition-aware exploitation (C2 × C1)

**Plan's version (kept for the record):** coalition-aware safe exploitation on So Long Sucker,
with win rate as the metric. **Replaced by three-player Kuhn and Leduc with colluding pairs**,
because Chapter 14 measured that a planted alliance costs a focal So Long Sucker baseline only
0.8–1.9 percentage points of win rate, and Chapter 11 that ≈ 99.5 % of random games in the
engine deadlock; the alliance has little to act on. So Long Sucker returns only if its engine is
fixed (negotiation, no deadlock), as a four-player demonstration.

**Hypothesis H2.2.** Coupling an online collusion detector (Chapter 13's standardised soft-play
and chip-dumping scores; the help/harm idea of Chapter 11 made self-relative) to the deviation
budget — shrink the deviation, or switch to the maximin strategy, while a pair is flagged —
reduces the loss to colluding pairs relative to the same agent without the detector, and costs
≤ 10 % of its gain against independent pairs.

| Item | Specification |
|---|---|
| Independent variables | coalition awareness (none / flag → shrink ε / flag → maximin strategy); colluder type (fixed coalition best response, adaptive coalition teaching, soft play, chip dumping, card sharing); collusion intensity q ∈ {0.1, 0.25, 0.5, 1} (Chapter 13's injection scheme) |
| Dependent variables | loss to colluders (absolute and baseline-relative); gain against independent pairs; detection delay (hands to flag); false flags per 1,000 hands on independent pairs; coalition value of the policies in force |
| Protocol | as Experiment 2.1, colluders drawn from the listed types; 5 seeds × 3 seats × 2,000 hands (Kuhn), 5,000 (Leduc) |
| Baselines | the coalition-unaware C2 agent; the stationary maximin strategy; the blueprint |
| Success criteria | loss to colluders reduced by ≥ 30 % at a false-flag rate ≤ 1 per 1,000 hands and a gain cost ≤ 10 % |
| Statistics | paired comparisons with and without the detector on the same seeds; detection delay with bootstrap intervals |

---

## Experiment 3.1 — cross-game validation of the protocol (C3)

**Plan's hypothesis (kept):** the three-layer framework produces consistent agent rankings
across Kuhn, Leduc and So Long Sucker and reveals insights that Elo alone misses.

**Revised hypothesis H3.1.** Applied unchanged to two-player Kuhn and Leduc and three-player Kuhn
and Leduc, (a) the protocol's joint readouts order the same agent *designs* (blueprint, best
equilibrium, RWYWE, RNR, bounded mixture, KL anchor, maximin-floor RWYWE, unbounded best
response) consistently across games (Kendall τ ≥ 0.6 for each readout between every pair of
games); (b) every one of the eight failure modes tested in Chapter 14 (1–5, 7–9) is detected by at
least one protocol readout in every game where it can occur, while each single metric (Elo,
exploitability/NashConv, Nash averaging, α-Rank, VasE, RRPS score) misses at least three.

| Item | Specification |
|---|---|
| Independent variables | game; evaluation method; match horizon (100 / 300 / 2,000 hands); population composition (with and without clones of weak bots); exploiter budget (10³–10⁵ hands) |
| Dependent variables | rankings and Kendall τ between methods and games; the failure-mode detection matrix; hands to a ±0.25 capture interval per window (raw vs AIVAT); learned/exact exploiter ratio vs budget |
| Protocol | Chapter 14's `run_population.py`, `run_adaptation.py`, `run_approx_br.py`, `run_nplayer.py`, extended to three-player Leduc and to the C1/C2 agents |
| Baselines | each single metric used alone; the RRPS aggregate score (Lanctot et al. 2023) |
| Success criteria | H3.1 (a) and (b) |
| Statistics | bootstrap over seeds for rank stability (as Chapter 14: 200 resamples); τ with bootstrap intervals |
| Evidence so far | Chapter 14 reproduced failure modes 1–5, 7–9 on Kuhn, Leduc and three-player Kuhn; Pilot P1 adds the match-level safety readout |
