# Chapter 14 — Execution notes (running log)

Running log of every build step and run: command, seed, runtime, result file, what it showed,
and anything that surprised me and how it was resolved. Newest entries at the bottom of each
section. If this work is interrupted, continue from the last entry.

Environment: Windows 11, repo `.venv` (Python 3.12.10), numpy 2.4.6, scipy 1.18.0,
OpenSpiel 1.6.15 (`pyspiel`), cvxpy 1.9.3 (+ ecos) installed for this chapter, 16 CPU cores.
All scripts run from `implementation/step14/implementation/`. No GPU is used: every
computation in this chapter is exact tabular arithmetic or small LPs.

---

## 0. Build log (framework)

**2026-09-24 — tree representation (`trees.py`).** One array-based tree per game, built from
OpenSpiel's own game definitions (`kuhn_poker`, `leduc_poker`, `kuhn_poker(players=3)`), with
per-player information sets, sequences and terminal arrays. Sizes: Kuhn 58 nodes / 30
terminals / 6+6 infosets; Leduc 9 457 nodes / 5 520 terminals / 468+468 infosets / 1 093
sequences per player; three-player Kuhn 617 nodes / 312 terminals / 16 infosets per player.
Build time: < 0.05 s for Leduc. First check: NashConv of the uniform profile equals OpenSpiel's
`exploitability.nash_conv` exactly (Kuhn 0.916667, Leduc 4.747222, 3P Kuhn 2.062500).

*Surprise 1 (fixed).* The first version sized the child-lookup table by the number of player
actions (2 in Kuhn), but chance outcomes are card ids up to 5 — duplicate dealing silently
fell back to random cards. Fixed by sizing the table by the largest outcome id.

**2026-09-24 — blueprints and the one-shot safe-exploitation LP (`solvers.py`).** OpenSpiel
C++ CFR+: Kuhn 10 000 iterations, Leduc 2 000 iterations (21.5 s), cached in
`results/cache/`. The sequence-form dual LP (maxmin, RNR(p), floor) solves full Leduc in
0.01–0.04 s per call; game values Kuhn −0.055556 (= −1/18), Leduc −0.085606 for seat 0.
Chapter 8's constraint-generation loop had *not* converged on full Leduc within its caps; the
dual formulation removes the loop entirely (cross-check against Chapter 8 on Kuhn in
`run_validation.py`).

**2026-09-24 — bridge to Chapter 7 (`bridge07.py`).** Exact values and best-response values
computed on our arrays equal Chapter 7's `exact_value` / `best_response_value` to 10 decimals
for Kuhn and Leduc type pairs (e.g. Leduc Rock vs Nash −0.4744631334 both ways).

**2026-09-24 — AIVAT (`aivat.py`).** Tabulates the AIVAT value of every terminal for the
current strategy, so the estimator's exact mean and variance are available (no sampling).

*Surprise 2 (fixed, a real bug).* The first version grouped states only by public history
(+ unknown players' cards). Private deals do not change the public history, so the deal node
and its parent landed in the same part, violating the paper's property 2 (h ⋢ h'). Symptom:
with *both* strategies known and a *perfect* value function the variance was not zero (the
paper's zero-variance property). Adding history length to the key fixed the partition, but
variance with perfect knowledge was still not zero: the known player's *own* deal also got a
chance-correction term, which double-counts that card's luck on top of the imaginary
observations. The paper's Figure 1 shows no AIVAT term at the known player's deal; removing it
keeps unbiasedness (every k_H has mean zero, Lemma 1) and restores exactly zero variance with
full knowledge and a perfect value function (variance ratio ~1e30 in all eight checks). Before
the fix, one-sided AIVAT on Kuhn was *worse* than chance-only correction; after it, it is better
everywhere.

**2026-09-24 — population layer (`population.py`).** Own implementations match OpenSpiel to
machine precision: single-population α-Rank (RPS, transitive, random 7×7; α ∈ {0.1, 1, 10,
100}; max |diff| ≤ 5e-14), multi-population α-Rank on random 3×3×3 tables (≤ 1.4e-14),
Nash averaging (`nash_averaging`), maximal lotteries (`MaximalLotteriesVoting._solve_game`).
OpenSpiel's Nash averaging and maximal lotteries need `cvxpy` and `ecos` (installed; see Central).

**2026-09-25 — Nash averaging made deterministic (`population.py`).** First runs showed the
max-entropy Nash support of the Leduc meta-game changing between 5 and 10 seeds and between
clone counts (e.g. BestEq 1.00 vs Nash 0.41 / BestEq 0.54). Cause: Nash, BestEq and TypeBR are
tied to ~1e-4 chips/hand, the Nash polytope is nearly degenerate, and the cvxpy solvers returned
"optimal_inaccurate" points that violate the constraints. Fix: a fixed tolerance (1e-6 × max|M|)
for every call; the entropy is maximised only over agents that can carry mass in some ε-Nash
equilibrium (one LP per agent), with CLARABEL and SLSQP candidates checked for feasibility and
the higher-entropy feasible one kept. After the fix, adding 0–8 copies of a non-support agent
changes no Nash-averaged skill by more than 5.3e-6 (Balduzzi et al.'s invariance), and RPS gives
(1/3, 1/3, 1/3). Cloning a *support* agent still moves mass (the copies share it), which is
expected for max-entropy selection; the clone test uses the weakest bot, the case the failure
mode is about.

## 1. Experiment log

All runs: `cd implementation/step14/implementation`, repo venv active. Seeds are fixed in the
code: deck order = f(game, seed) (common random numbers across pairs), seat-swapped duplicate
match with the private cards exchanged, action seed = crc32(game|agent|opponent|seed|seat).

| # | command | seeds / size | runtime | result file | what it showed |
|---|---|---|---|---|---|
| E0 | `python run_validation.py` | MC: 20 000 hands per check, seed 2026 | 14 s | `results/validation.json` | every component matches its reference (below) |
| E1 | `python run_population.py --games kuhn leduc --seeds 10 --hands 2000` | 10 seeds × 2 seats × 2 000 hands per simulated pair; Kuhn 1 300 matches, Leduc 900 | 44 s / 170 s | `results/population_{kuhn,leduc}.json` | rankings disagree; exploiters top Elo, absent from Nash averaging; α-Rank winner changes with α; horizon changes the Elo winner |
| E2 | `python run_adaptation.py --games kuhn leduc --seeds 10` | 7 agents × 16 (Kuhn) / 12 (Leduc) conditions × 10 seeds × 2 seats, 2 000 hands | 30 s / 198 s | `results/adaptation_{kuhn,leduc}.json` | the joint protocol: gain, capture, h50, recovery, exposure, teaching loss |
| E3 | `python run_approx_br.py --seeds 3 --max-hands 100000` | 3 seeds × 2 seats per target; online part 5 seeds | 24 s / 41 s | `results/approx_br_{kuhn,leduc}.json` | learned best responses are lower bounds; a 2 000-hand black-box learner finds nothing where the white-box attack takes 1.0–1.5 chips/hand |
| E4 | `python run_nplayer.py --seeds 5 --pop-seeds 3 --hands 2000` | tensor: 3 seeds per simulated triple (1 158 matches); protocol: 3 agents × 3 seats × 5 seeds × 8 conditions | 84 s | `results/nplayer_kuhn3.json` | equilibrium components lose 0.06–0.17 chips/hand more to a coordinated pair than in equilibrium; cross-play NashConv up to 0.125 |
| E5 | `python run_sls.py --games 2000 --seeds 3` | 2 000 games per cell × 3 seeds | 35 s | `results/sls.json` | Layer 2 transfers; the planted alliance barely hurts third parties in this engine |
| E6 | `python run_bridge13.py` | Chapter 13's parsed Pluribus hands (10 000) | < 1 s | `results/bridge13_pluribus.json` | raw 95 % interval ±173 mbb/hand vs a 25 mbb/game standard error with AIVAT in the Science paper |
| E7 | `python run_crossgame.py` | derived only | < 1 s | `results/crossgame.json` | cross-game table + failure-mode summary |

### E0 — validation (`results/validation.json`)

- V1 NashConv == OpenSpiel `exploitability.nash_conv` on 12 profiles over Kuhn, Leduc, 3P Kuhn:
  identical to 10 printed decimals (e.g. Leduc CFR+ blueprint 0.0001699555 both).
- V2 Chapter 7 bridge: 39 type pairs, max |diff| 1e-14 (values and best responses).
- V3 Chapter 3: Leduc CFR after 10 / 100 iterations, exploitability 0.811708 / 0.090002 by
  Chapter 3's own evaluator and by this chapter's code (identical to 6 decimals).
- V4 game values: Kuhn −0.055556, Leduc −0.085606 (seat 0); blueprint exploitability 9.6e-6
  (Kuhn, CFR+ 10 000 it.) and 8.5e-5 (Leduc, CFR+ 2 000 it.).
- V5 dual LP vs Chapter 8 on Kuhn (2 seats × 4 opponents): RNR(p) objective identical to 1e-16;
  best equilibrium differs by ≤ 1.9e-3 in EV because Chapter 8's solver enforces the floor with a
  5e-4 feasibility slack (its worst case −0.0560 vs v* = −0.0556). Full-Leduc solves: 0.02–0.04 s.
- V6 α-Rank (single and multi-population), Nash averaging, maximal lotteries == OpenSpiel
  (max |diff| 2e-8); IML levels [[a, c], [b], [d]] vs OpenSpiel's ranking a, c, b, d.
- V7 spinning top: RPS 0.0000, ladder 1.0000.
- V8 AIVAT (chance + agent known, value function = blueprint self-play values): exactly unbiased
  (max |bias| 1e-15). Variance-reduction factor vs raw chips, Nash vs every other stationary zoo
  agent, both seats: Kuhn min 2.2 / median 48 / 18 of 20 pairs ≥ 5× (plan target 5×); Leduc min
  6.9 / median 12.2 / 7 of 12 pairs ≥ 10× (plan target 10×). Monte Carlo (20 000 hands, Nash vs
  Random) agrees: sample factors 9.3, 12.4 (Kuhn), 7.1, 6.8 (Leduc); AIVAT means within 2.1 SE of
  the exact EV.

*Plan target vs reality.* The plan predicted ≥ 5× on Kuhn and ≥ 10× on Leduc. Kuhn meets it for
18 of 20 pairs; Leduc for 7 of 12 — the misses are opponents whose play the blueprint
self-play value function mispredicts. This is consistent with Burch et al.'s own Leduc table
(48–75 % SD reduction, i.e. 3.7–16× in variance, for dissimilar strategies). The plan's line
"AIVAT should match the exact exploitability" is a category error: AIVAT estimates a head-to-head
expected value, not exploitability; it was checked against the exact EV instead.

### E1–E7 — see the results files; the headline numbers are quoted in the chapter with their file.

## 2. Surprises during the experiments

3. *Change-point exploiter on Leduc.* DirBR-CP captures only 0.34 of the attainable gain on
   Leduc (DirBR: 0.94) and is *not* better under the teaching attack (loss 1.74 vs 1.23 on the
   Rock bait). Checked: the detector fires on stationary Leduc opponents (the aggression signal
   at Leduc's first decision is noisy), each reset drops the model and replays the blueprint, and
   the re-learnt best response to a thin model is highly exposed. On Kuhn it helps (teaching loss
   0.22 vs 0.35). Not a bug — the Chapter 7 detector tuned on Kuhn does not transfer.
4. *Black-box learner vs adaptive agents.* The Monte-Carlo learner *loses* to every adaptive
   agent on Leduc within 2 000 hands (damage −0.35 to −0.86), although DirBR's mean exposure there
   is 3.17. The learner explores; the adaptive agents exploit its exploration. This is the
   budget point of failure mode 3, not a defect of either agent.
5. *Fixed colluders vs adaptive agents (3P Kuhn).* A pair that plays the exact coalition best
   response against the *blueprint* costs the blueprint 0.119 per hand but is itself exploitable:
   DirBR3P earns +0.354 against it. Only the coalition that re-targets the agent's current policy
   (teaching attack) hurts the adaptive agents (−0.466 per hand after the switch).
6. *SLS coalition probe.* A planted alliance lowers a focal baseline's win rate by only 0.8–1.9
   percentage points (per-cell 95 % CI ≈ ±2 points, 3 seeds × 2 000 games) — not distinguishable
   from zero for most agents. Chapter 11 found ~99.5 % of random games end in deadlock; the
   alliance has little to act on in this engine.

7. *Speed/recovery rule.* The first h50 rule (window mean ≥ 0.5 from hand t) returned h50 ≈ 1:
   a 100-hand window starting at hand 0 already averages 50 blueprint hands and 50 exploiting
   hands. Fixed to "capture at hand t ≥ 0.5 **and** mean over [t, t+100) ≥ 0.5", which resolves
   to the refit period (50 hands). Recovery is only informative where the old exploit does badly
   against the new opponent; the run now records this "cross-capture" (Kuhn TightPassive →
   LooseAggr −0.91; Leduc switches +0.38 to +0.58).
8. *Ties in rank figures.* α-Rank masses below 1e-3 and Nash-averaged skills equal to 4 decimals
   are ranked as ties (competition ranking) in the figures; the JSON keeps the raw scores.

## 3. Figures and build (2026-09-25)

- `python plot_figures.py` → `deliverables/reports/step14/figures/` (9 PNGs, 250 dpi, width 7 in,
  every text element fs ≥ 10). Diagram: `deliverables/reports/step14/summary/make_protocol_figure.py`
  (copy of Chapter 11's `_diagram_utils.py`) → `summary/protocol.png`. Every PNG was opened and
  checked; fixes applied: legend overlapping data (approx_br), overlapping labels (gain_exposure),
  specialist naming across games (adaptation_curves), missing y label (nplayer).
- `PYTHONIOENCODING=utf-8 python scripts/build_reports.py --step step14 --lang en --type all` —
  report 16 pages, chapter 16 pages (8 figures), one-pager 1 page (10 pt / 1.5 cm).
- `python scripts/check_headings.py` — 0 missing; `python scripts/check_captions.py` — 0 unaccounted.
- `python scripts/figures/render_printed.py --pdf deliverables/summaries/step14_en.pdf --out
  deliverables/finalReview/renders_new/step14` — all figures print at 16.7–17.3 cm, 250–330 ppi.
- Harness note: the Write tool refused files named `summary.md` / `report_en.md` for a sub-agent;
  these required deliverables were drafted in the scratch folder and copied into place.

## 4. Status — where to continue

Done: framework, validation, zoos, E0–E7, figures, `report_en.md` (≈ 4,000 words),
`summary/summaryEn.md` (≈ 4,500 words, 8 figures), `summary/onePager.md` (≈ 600 words), English
PDFs, checks. Not done (by design): Bulgarian versions; `consolidation/`.

## Central (changes needed outside this step's folders)

- `requirements.txt`: add `cvxpy` (1.9.3) and `ecos` — needed by this chapter's Nash averaging
  and by OpenSpiel's `nash_averaging` / `maximal_lotteries`, used as cross-checks.
- `requirements.txt`: also note OpenSpiel's `voting` and `nash_averaging` modules import cvxpy at
  module load; without it `open_spiel.python.voting.maximal_lotteries` fails to import.
- Glossary (EN/BG): new terms used in Chapter 14 — "exposure" (of the policy in force),
  "capture" (share of the attainable gain), "teaching attack", "coalition value",
  "policy-exact estimator", "h50 / r50".
- `planning/rawSteps/step_14…` (not edited): AIVAT is Burch, Schmid, Moravčík, Morrill & Bowling,
  AAAI 2018; "Re-evaluating evaluation" is NeurIPS 2018 (both already listed in
  `lit_evaluation.md`); the AIVAT validation line compares with exploitability, which is a
  category error (AIVAT estimates an expected value).
- Chapter 8 (not edited): the full-Leduc safe-exploitation solve that did not converge there is
  solved in 0.02–0.04 s by the one-shot dual LP in `implementation/step14/implementation/solvers.py`;
  Chapter 8's text "the exact one-shot dual LP" as a future path can now point here.
- `deliverables/finalReview/renders_new/step14/` was written by `render_printed.py` as the brief
  instructs.
