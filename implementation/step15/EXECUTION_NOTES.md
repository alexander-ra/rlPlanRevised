# Chapter 15 — Execution notes (running log)

Chapter 15, *Research frontier mapping and contribution design*, executed end to end by an agent
(Opus 5.5) on 2026-09-25 under `deliverables/finalReview/NEW_CHAPTER_BRIEF.md` (NN = 15). This is
the running log: every command, seed, runtime, result file, what it showed, and every surprise and
how it was resolved. If the session is interrupted, continue from the last entry.

The plan is `planning/rawSteps/step_15_research_frontier_mapping.md`. It predates the September
2026 gap validation; where they disagree `deliverables/finalReview/lit_gaps.md` wins (OX-Search is
Ge, Xu, Ding, Meng, An, Li & Gao; piKL anchors to a human-imitation policy; equal share is a
target that is provably not securable against heterogeneous opponents).

## Environment

- Windows 11, repo `.venv` (Python 3.12.10), numpy 2.4.6, scipy 1.18.0 (HiGHS LPs), OpenSpiel
  1.6.15, 16 logical CPUs. No GPU is used: every computation here is exact tabular arithmetic,
  small LPs or an exact enumeration.
- All commands run from `implementation/step15/implementation/` with the venv active.
- Chapter 14's engine is imported read-only through `boot.py` (Chapter 14's folder appended to
  `sys.path`; Chapter 14's cached blueprints are read, never written). No other chapter's file
  is edited.

## Inputs read (2026-09-25)

`NEW_CHAPTER_BRIEF.md`; the raw plan; `lit_gaps.md`; `lit_evaluation.md`; `CHAPTER1_OUTLINE.md`;
`TRIAGE.md` (§ B: R1 RWYWE, R2 equal-budget Leduc, R4 coalition credit); the Gaps/Own-evidence
sections of all 13 `stepNN_extract.md`; Chapter 13's and 14's `EXECUTION_NOTES.md` and
`summaryEn.md`; Chapter 8's and 14's one-pagers and reports; the individual study plan
(`oldSources/ind_plan_A_Andreev_EN.md`: one "report (publication of an article)" per stage,
stages due 11.2026, 04.2027, 01.2028, 08.2028; defence 04.2029).

## Sources verified for this chapter

- **Ganzfried & Sandholm (2015), ACM TEAC 3(2), Art. 8.** Full text read (PDF from the authors'
  CMU page, `cs.cmu.edu/~sandholm/safeExploitation.teac15.pdf`, fetched 2026-09-25; the EC'12
  version was also read for comparison). What the code relies on: Def. 4.1 (safe = ≥ v* per
  period in expectation); Alg. 2 RWYWE (k_1 = 0; play the k_t-safe best response to the model;
  k_{t+1} = k_t + u(π_t, a_t) − v*, expectation over *our* randomisation — RWYW, which uses the
  realised payoff, is not safe, Prop. 6.1); Alg. 3 BEFFE and Alg. 4 BEFEWP; § 6.3 best
  equilibrium (their baseline); Alg. 6 (extensive form, opponent's private information observed:
  τ̂ = best response to π_t constrained to the observed actions with the observed card) and
  § 8.2.2 (card not observed: constrained to the observed actions with *some* card); § 9
  experiments (Kuhn, frequency model with a Dirichlet prior of 5 equilibrium hands, card assumed
  observed, 40,000 opponents per class, 1,000-hand matches, Table I). § 2.3 also states that the
  methodology "applies straightforwardly" to multiplayer games if the minimax value is replaced
  by the maximin value — relevant to C2's prior art.
- Venue dates (for `design/publications.md`): AAMAS 2027 main track — abstract 1 Oct 2026,
  paper 8 Oct 2026, conference 3–7 May 2027, Hanoi (official call page, warwick.ac.uk/…/aamas2027);
  IEEE CoG 2027 — full papers 1 Mar 2027, Aizuwakamatsu (search listing of the official site;
  conference dates differ between listings, to confirm); CompSysTech (University of Ruse) —
  the 2026 edition's deadline was 30 Mar 2026 (official site), the 2027 date is not announced;
  University of Ruse 65th Annual Scientific Conference — 23–24 Oct 2026, proceedings "Proceedings
  of the University of Ruse" (official site; deadline not shown). Deadlines from aggregator sites
  (ICML, IJCAI, NeurIPS 2027) were found unreliable — one "ICML 2027" call was a linguistics
  conference — and are given as estimates from the annual cycle.

---

## Log

### P0 — gift accounting and the RWYWE agent (`gifts.py`, `safe_agents.py`)

- `gifts.constrained_br_value`: the opponent's best response with some information sets forced to
  the observed action (Chapter 14's backward pass with a mask). With nothing forced it equals the
  plain worst case exactly (Kuhn seat 0: −0.0555644 both ways).
- `gifts.gift`: Alg. 6 when the card is observed; § 8.2.2 (minimum over every card consistent
  with the replay) when it is not. Check on 300 random hands of the blueprint against Random:
  mean gift 0.0285 with the card observed, ≈ 0 with it hidden (the minimum over cards removes
  it), and hidden ≤ observed on every hand.
- `safe_agents.GiftSafe`: RWYWE / BEFEWP / BEFFE / best equilibrium / best response, with G&S's
  frequency model or Chapter 7's continuous model. Safety checks on single matches (Kuhn, both
  seats, Random and a dynamic nemesis): exposure of the policy in force never above k_t (0
  violations); k never below −1e-4.
  *Note.* k's minimum of about −9e-5 over 1,000 hands is the LP's floor margin (the floor is
  enforced at v* − k − 1e-7, as in Chapter 14's BestEq) accumulating against a nemesis: ~1e-7
  chips per hand.
- *Exact shortcut added:* when k_t ≥ the exploitability of the full best response to the model,
  the floor is slack and the k-safe best response *is* that best response, so no LP is solved.

*Surprise 1 (resolved) — LP ties.* A first 14-opponent smoke run of the Table I replication gave
best-equilibrium and RWYWE values against G&S's "sophisticated" opponents about 0.01 below the
paper (−0.028 vs −0.0148). Suspected a bug first. Checks: (i) the opponent generator — drawing
each probability uniformly within 0.2 of the equilibrium (truncated to [0, 1]) gives a mean
best-response value of 0.0707, consistent with G&S's learning best response (0.0548); the
alternative reading "equilibrium + U(−0.2, 0.2), clipped" gives 0.0386, below their number, so
it is ruled out. (ii) With the *true* opponent strategy as the model, the best equilibrium
earns −0.0112 (G&S's learning version: −0.0148) — the solver is right. (iii) With the prior
alone (an equilibrium model) every equilibrium of player 1 is optimal, and HiGHS returns the
vertex that never bluffs the Jack and never bets the King (−0.0338 against these opponents).
Cause: ties on the LP's optimal face are broken arbitrarily. `safe_agents.floor_tiebreak` adds a
second stage that picks, among the model-optimal solutions, the one closest (L1, sequence form)
to the blueprint. On 40 sophisticated opponents: best equilibrium −0.0211 → −0.0159 (G&S
−0.0148), RWYWE −0.0185 → −0.0127 (G&S −0.0110). The replication is therefore run with the
tie-break (primary) and without it (to show the effect); Chapter 14's BestEq, which has no
tie-break, is kept as it is in the protocol pilot for comparability, with RWYWE-tb added.

### P0 — replication of Ganzfried & Sandholm (2015), Table I (`run_gs_table.py`)

`python run_gs_table.py` (tie-break on; 400 opponents per class, 200 equilibrium opponents, 5
algorithms, 1,000 hands; 7,000 matches; 2,315 s on 14 processes) → `results/gs_replication.json`.
`python run_gs_table.py --no-tiebreak` (858 s) → `results/gs_replication_notb.json`.
Seeds: opponent strategy and deals from crc32("gs|class|i") / crc32("deal|class|i"), the same
deals for every algorithm against a given opponent (as G&S did).

Policy-exact EV per hand (95 % CI over opponents), with G&S's Table I in brackets:

| | random | near-equilibrium ("sophisticated") | dynamic |
|---|---|---|---|
| RWYWE | 0.332 ± 0.025 (0.364) | −0.0144 ± 0.0016 (−0.0110) | −0.0271 ± 0.0016 (−0.0204) |
| BEFEWP | 0.322 ± 0.024 (0.355) | −0.0138 ± 0.0016 (−0.0115) | −0.0272 ± 0.0017 (−0.0214) |
| BEFFE | 0.176 ± 0.010 (0.200) | −0.0150 ± 0.0016 (−0.0131) | −0.0403 ± 0.0007 (−0.0397) |
| Best equilibrium | 0.133 ± 0.008 (0.145) | −0.0177 ± 0.0015 (−0.0148) | −0.0365 ± 0.0007 (−0.0352) |
| Best response | 0.328 ± 0.025 (0.470) | +0.0395 ± 0.0048 (+0.0548) | −0.1695 ± 0.0028 (−0.1209) |

Against the equilibrium opponent every algorithm's mean EV equals v* = −0.0556 to four decimals.

What it shows. (1) **Safety reproduces as the theory says:** against the dynamic class (a random
strategy for 100 hands, then a best response to the current strategy every hand) all four safe
algorithms stay above v* in all 400 matches, and the exposure of the policy in force never
exceeded k_t in any hand of any match; the best response falls to −0.170 (400 of 400 matches below
v*). (2) **The orderings reproduce:** random — RWYWE ≈ BEFEWP > BEFFE > best equilibrium;
dynamic — RWYWE ≈ BEFEWP > best equilibrium > BEFFE, as in G&S. (3) **The safe algorithms'
levels are 0.001–0.033 chips/hand below G&S's** (e.g. RWYWE 0.332 vs 0.364 on random opponents,
−0.0271 vs −0.0204 on dynamic ones). Without the LP tie-break (`gs_replication_notb.json`) they
lose a further 0.002–0.046 (RWYWE on random opponents 0.286), confirming surprise 1.

*Surprise 2 (not resolved) — the best-response row.* Our model-based best response earns 0.328 on
random opponents against G&S's 0.470 (and −0.170 vs −0.121 against dynamic ones). Checked: (i)
tie-breaking of the best response toward the blueprint: identical result on 80 opponents
(0.3697 both ways); (ii) three readings of G&S's "random" class — a random mixed strategy (used;
mean exact best-response value 0.582, best-equilibrium ceiling 0.170), the uniform strategy
(best response 0.500 at most; our learners on 60 opponents: best response 0.193, RWYWE 0.239,
best equilibrium 0.102) and a random pure strategy (at most 0.654; our best-response learner
0.383 on 64 opponents). No reading reproduces 0.470. Under the random-pure reading the *safe* rows come closer to
G&S's values than under the reading used (64 opponents, wide intervals: RWYWE 0.397 ± 0.083,
BEFEWP 0.377 ± 0.080, BEFFE 0.195 ± 0.032, best equilibrium 0.141 ± 0.023, against 0.364 / 0.355 /
0.200 / 0.145), so G&S's "random" class may have been random pure strategies; the best response
still falls short (0.383 ± 0.076). The main run keeps the random-mixed reading, the more natural
reading of "chooses a mixed strategy in advance". Our learner is greedy: it best-responds to
the model and so never visits some of the opponent's information sets, which keep their prior;
G&S's text does not say how theirs avoided this. The safe rows, which are what this chapter uses,
are much closer. Recorded as an open discrepancy; scratch checks in
`…/scratchpad/step15/checks/{br_ties,random_pure}.py`.

### P1 — RWYWE under Chapter 14's joint protocol (`run_protocol2p.py`)

`python run_protocol2p.py --game kuhn` (8 agents × 16 conditions × 10 seeds × 2 seats = 2,560
matches of 2,000 hands; 171 s) → `results/protocol2p_kuhn.json`.
`python run_protocol2p.py --game leduc --tol 0.01 --agents Nash BestEq "RNR(0.5)" DirBR RWYWE RWYWE-rev BEFEWP`
(1,680 matches; 1,471 s; RWYWE ≈ 34 s per match, 488 LP solves per match) →
`results/protocol2p_leduc.json`. The re-solve tolerance on Leduc (0.01 chips) only delays the use
of banked gifts; safety is unaffected (a policy is never solved for a k larger than the bank).
Timing check before the run (Leduc, one match): tol 0 vs 0.01 against Maniac 0.537 vs 0.528 mean
EV, 28 vs 22 s.

Chapter 14's agents reproduce exactly in this harness (Kuhn gains BestEq +0.020, RNR(0.5)
+0.210, DirBR +0.273; Leduc +0.047, +0.797, +0.988 — Chapter 14's numbers).

| Agent | Kuhn gain | Kuhn exposure | Leduc gain | Leduc exposure | matches with S < 0 under teaching (Kuhn / Leduc, of 60) |
|---|---:|---:|---:|---:|---|
| Nash | 0 | 0 | 0 | 0 | 0 / 0 |
| BestEq | +0.020 | 0 | +0.047 | 0 | 0 / 0 |
| BEFEWP | +0.053 ± 0.003 | 0.029 | +0.049 | 0.004 | 0 / 0 |
| RWYWE (showdown) | +0.062 ± 0.002 | 0.030 | +0.113 ± 0.001 | 0.006 | 0 / 0 |
| RWYWE-tb | +0.063 ± 0.002 | 0.031 | — | — | 0 / — |
| RWYWE (cards shown) | +0.148 ± 0.004 | 0.087 | +0.134 ± 0.001 | 0.010 | 0 / 0 |
| RNR(0.5) | +0.210 ± 0.002 | 0.090 | +0.797 ± 0.007 | 0.264 | 1 (S = −0.0007) / 0 |
| DirBR | +0.273 ± 0.001 | 0.338 | +0.988 ± 0.005 | 2.461 | 21 (min −0.104) / 31 (min −0.534) |

Gain: chips/hand over the blueprint against the sub-optimal population, 95 % CI over 10 seeds.
Exposure: mean over the match of v*_seat − worst case of the policy in force. S: mean over the
match of EV − v*_seat, per match, under the three teaching attacks (attacker re-targets every hand).

What it shows. (1) RWYWE is the two-player baseline Chapter 8 lacked: it earns 3.1× (Kuhn) and
2.4× (Leduc) the best equilibrium's gain and is safe over the match in every attacked match.
(2) It earns far less than RNR(0.5): 30 % of RNR's gain on Kuhn and 14 % on Leduc. (3) The
pessimistic accounting is the bottleneck: with the card used only at showdown, RWYWE's bank at
the switch is 0.01 chips after 1,000 hands of the TightPassive bait (Kuhn) and 0.01–0.02 after
every Leduc bait, while with cards always shown it reaches 8.5 (Kuhn, LooseAggr bait) — yet even
then its Leduc gain rises only to +0.134, because the nemesis assumed off the path of play is
very pessimistic in a game with 468 information sets per player. (4) Per-hand readouts mislead
for RWYWE: under the LooseAggr bait its bank (2.19 at hand 1,000) is spent within about 100 hands
of the switch; the per-hand teaching-loss readout charges that to the agent although the match
stays above v* (S = +0.112 ± 0.025). This is the reason for C3's match-level safety readout.
(5) RNR(0.5) was almost match-safe in these attacks (1 of 120 attacked matches below v*, by
0.0007) without any guarantee; DirBR was not (52 of 120).

*Surprise 3 (kept as observed).* The gift-banking agents recover poorly after an opponent switch
(r50 reached in ≤ 20 % of the Kuhn TightPassive → LooseAggr matches, against 30 % for RNR(0.5) and
45 % for DirBR): the bank built against the first opponent is spent on a deviation fitted to it,
and the model follows Chapter 14's refit schedule without forgetting.

### P2a — the team-maxmin value of three-player Kuhn (`maximin3p.py`)

`python maximin3p.py` (7 s) → `results/maximin3p.json`. Constraint generation, 15 / 23 / 14 cuts
per seat, LP upper bound equal to the oracle value. Seat values: maximin −0.0379 / −0.0265 /
+0.0417 (seat average −0.0076); the CFR+ blueprint in self-play −0.0269 / −0.0208 / +0.0477 and its
coalition values −0.125 / −0.106 / −0.125.

*Surprise 4 (kept, with its caveat).* The gap analysis calls team-maxmin "very conservative". In
three-player Kuhn the seat-averaged maximin value is only 0.0076 chips/hand below equal share,
and the maximin strategy's coalition value is 0.11 above the blueprint's. Checked: the oracle
equals Chapter 14's enumeration (12 random strategies, to 1e-9), the LP bound equals the oracle
value, and the maximin strategy's EV against the adaptive colluders equals its coalition value
(−0.0076). Whether the value stays this close to equal share in larger games is open; the
lit_gaps wording is not changed.

### P2b — the Experiment 2.1 pilot (`run_bounded3p.py`)

`python run_bounded3p.py` (16 agents × 9 conditions × 3 seats × 5 seeds = 2,160 matches of 2,000
hands; 1,938 s; MM-RWYWE ≈ 72 s per match) → `results/bounded3p.json`.
A fast exact oracle (`mmsafe3p.CoalitionOracle`: the unique pure plans of the smaller opponent,
6,561 or 10,000 instead of 65,536) replaced Chapter 14's enumeration: ≈ 4.5 ms instead of 102 ms
per call, equal to 1e-9 on 12 random strategies.
*Fix during the smoke test:* at k = 0 the maximin-floor LP sits on a degenerate face and
constraint generation cycled (400 iterations at the same objective); an acceptance tolerance of
2e-6 on the oracle's check (`ACCEPT_TOL`) fixed it (9–12 iterations at k > 0). An unconverged
solve would fall back to the maximin strategy (safe); none occurred.

Seat-averaged, 95 % CI over 5 seeds (independent pairs: gain over the blueprint; adaptive
colluders: EV over hands 1,000–1,999):

| Agent | gain, independent pairs | worst-case L | EV, fixed colluders | EV, adaptive colluders | coalition value (final) |
|---|---:|---:|---:|---:|---:|
| Nash (blueprint) | 0 | 0 | −0.119 | −0.119 | −0.119 |
| DirBR3P | +0.303 ± 0.001 | 1.06 | +0.353 | −0.464 ± 0.019 | −0.289 |
| Blend3P | +0.173 | 0.56 | +0.117 | −0.239 | −0.127 |
| BD(0.01 / 0.03 / 0.1 / 0.3 / ∞) | +0.004 / +0.014 / +0.048 / +0.149 / +0.260 | 0.010 / 0.029 / 0.095 / 0.285 / 1.00 | −0.112 … +0.287 | −0.119 / −0.120 / −0.132 / −0.217 / −0.379 | −0.117 … −0.228 |
| KL(1 / 3 / 10 / 30) | +0.048 / +0.151 / +0.273 / +0.301 | 0.24 / 0.68 / 0.91 / 0.96 | −0.080 … +0.354 | −0.140 / −0.181 / −0.286 / −0.372 | −0.119 / −0.120 / −0.137 / −0.171 |
| Maximin (stationary) | +0.032 | 0.24 | +0.003 | −0.0076 | −0.0076 |
| MM-BestEq | +0.034 | 0.24 | +0.003 | −0.0076 | −0.0076 |
| MM-RWYWE (cards shown) | +0.082 ± 0.001 | 0.97 | +0.003 | −0.0070 ± 0.0008 | −0.0076 |
| MM-RWYWE (showdown) | +0.063 ± 0.001 | 0.74 | +0.003 | −0.0071 ± 0.0006 | −0.0076 |

Checks. BD(ε): L of every policy in force ≤ ε (max 0.010 / 0.029 / 0.095 / 0.285) and the
realised per-hand baseline-relative loss never above ε (max 0.004 / 0.011 / 0.057 / 0.285 under
the adaptive colluders). MM agents: match-level S = mean(EV − v_mm) ≥ 0 in all 105 + 15 + 15
matches of each agent (adaptive colluders: min +0.0029); the coalition value of the policy in
force never fell more than 5e-7 below its floor (re-checked on 27 matches,
`…/scratchpad/step15/checks/mm_cv_margin.py`; the run's 1e-6 counter flags a few hands within
the oracle's 2e-6 acceptance tolerance); 0 unconverged solves.

Against the hypotheses written in `design/experiments.md` before the run:
- H2.1a — cap holds in every hand: **yes**. Gain at ε = 0.1 ≥ 25 % of DirBR3P's: **no** (16 %;
  49 % at ε = 0.3).
- H2.1b — S ≥ 0 in every condition: **yes**; gain above the stationary maximin strategy: **yes**
  (+0.082 / +0.063 vs +0.032).
- H2.1c — KL better than the mixture at equal L: **no** for L ≤ 0.7 (KL(1) +0.048 at L = 0.24,
  where the mixture's line gives ≈ +0.12); **yes** near full deviation (KL(10) +0.273 at 0.91 vs
  ≈ +0.25). But KL is much better on a *different* robustness readout: at similar gain, KL(10)
  gets −0.286 under adaptive colluders and keeps a coalition value of −0.137; BD(∞) −0.379 and
  −0.228. The two readouts (baseline-relative worst case vs absolute coalition exposure) rank
  the rules differently — kept as a finding for C3.

What the pilot does and does not show. It shows that, in three-player Kuhn, an agent can exploit
independent weak pairs while holding an exactly checked guarantee against coordinated pairs
(MM-RWYWE: +0.08 over the blueprint, and −0.007 instead of the blueprint's −0.119 under adaptive
colluders), and that a per-hand baseline-relative cap can be enforced exactly. It shows nothing
beyond one tiny game; the exact checks rely on enumeration that does not scale; the opponent
model and schedules are Chapter 14's; 5 seeds; the maximin agents' gains are small (27 % of the
unbounded exploiter's); and nothing here is a theorem beyond Ganzfried and Sandholm's argument
transposed to a coordinated pair.

## 2. Figures (2026-09-25)

`python plot_pilots.py` → `deliverables/reports/step15/figures/` (5 PNGs, 250 dpi, 7 in wide,
fs ≥ 10), drawn from the JSON only. Diagrams: `deliverables/reports/step15/summary/
make_frontier_figure.py`, `make_timeline_figure.py`, `make_bank_figure.py` (copy of Chapter 11's
`_diagram_utils.py` via Chapter 14). Every PNG was opened and checked; fixes: overlapping tick
labels (replication), clipped dots (dynamic panel), overlapping point labels (frontier), text
overflow in three diagram boxes, a label over the data (teaching figure).

## 3. Deliverables, build and checks (2026-09-25)

- `deliverables/reports/step15/report_en.md` (≈ 3,200 words of prose, 5 figures, 4 tables),
  `summary/summaryEn.md` (≈ 4,330 words, 8 figures), `summary/onePager.md` (≈ 570 words).
  Drafted in the scratch folder (`…/scratchpad/step15/drafts/`) and copied into place; the Write
  tool refuses some file names for sub-agents (the same harness quirk Chapters 13–14 recorded).
- `PYTHONIOENCODING=utf-8 python scripts/build_reports.py --step step15 --lang en --type all` —
  report 15 pages, chapter 16 pages (8 figures), one-pager 1 page (10 pt / 1.8 cm).
- `python scripts/check_headings.py` — 54 PDFs, 0 missing headings;
  `python scripts/check_captions.py` — 29 PDFs, 0 unaccounted figures.
- `python scripts/figures/render_printed.py --pdf deliverables/summaries/step15_en.pdf --out
  deliverables/finalReview/renders_new/step15` — 8 figures, printed at 17.3–17.6 cm, 250–331
  effective ppi; text at fs 10 on a 7-inch canvas prints at ≈ 9.8 pt. Printed pages inspected.

## 4. Status — where to continue

Done: frontier map and design documents (`design/`), intuition, exploration, targeted reading,
pilots P0–P2 with results and logs, figures, the three English deliverables, PDFs and checks.
Not done: Bulgarian versions (a later pass); `consolidation/` (human-written); the plan's reading
of recent dissertations (left to the candidate, `targetedReading/summary.md` § 9).
Open items for the candidate: the best-response row of the replication (Surprise 2); whether
to try the AAMAS 2027 stretch (paper due 8 Oct 2026) for Paper 1; the national publication
requirements for the degree (not checked).

## Central (changes needed outside this step's folders)

- **Chapter 8 (not edited, as instructed):** its "Ganzfried" method is the best-equilibrium
  baseline; the RWYWE result it lacked is here (`results/protocol2p_{kuhn,leduc}.json`: +0.062 /
  +0.113 chips/hand vs best equilibrium +0.020 / +0.047, safe over the match in 120 of 120 attacked
  matches). TRIAGE R1 can point here. TRIAGE R2 (equal-budget Leduc rerun) is superseded by
  Chapter 14's one-shot LP (full Leduc in 0.02–0.04 s per solve), which this chapter used for 488
  RWYWE solves per Leduc match.
- **Chapter 14 (not edited):** its `BestEq` LP leaves ties to HiGHS, which returns a degenerate
  equilibrium against equilibrium-like models (`exploration/lp_ties.py`: −0.034 vs the
  blueprint's −0.019 against near-equilibrium opponents). A tie-break toward the blueprint
  (`safe_agents.floor_tiebreak`) would change its small gains slightly (Kuhn +0.063 vs +0.062 for
  RWYWE with and without it). Its teaching attacker refreshes every 50 hands; for agents whose
  policy changes every hand it must refresh every hand (done here as `TEACH1`).
- **Chapter I (`CHAPTER1_OUTLINE.md`, § 1.7):** refined research questions proposed — RQ1
  calibrated inference; RQ2 relative and absolute bounds; RQ3 match-level safety. § 1.5 own
  evidence can use RWYWE (two-player) and, with caution, the three-player pilot. § 1.5's
  "team-maxmin very conservative" may add "(in three-player Kuhn its value is within 0.008 of equal
  share; one game)".
- **Glossary (EN/BG):** new terms — gift bank (k), match-level safety S, team-maxmin (maximin)
  value v_mm, baseline-relative loss L, capped mixture BD(ε), KL anchor KL(β), coordinated pair,
  maximin-floor RWYWE.
- **`requirements.txt`:** nothing new (numpy, scipy, OpenSpiel, matplotlib, PyMuPDF already used).
- **`lit_gaps.md` (not edited):** G&S (2015) § 2.3 states that the method extends to multiplayer
  games with the maximin value — prior art for C2's maximin-floor rule, to be cited wherever C2 is
  described.
- **`planning/rawSteps/step_15…` (not edited):** corrections listed in `design/frontier_map.md`
  § 10 (OX-Search authors, piKL anchor, equal share, AIVAT and spinning-top attributions, the
  "Jiawei Ge co-author" line, the Bakhtin 2022 Diplomacy title).
