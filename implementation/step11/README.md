# Step 11 — Dynamic Coalition Formation in Competitive FFA Games (So Long Sucker)

**Source spec:** [`planning/rawSteps/step_11_coalition_formation_ffa.md`](../../planning/rawSteps/step_11_coalition_formation_ffa.md)
**Tier / duration:** Tier 2, 14 days · **Plan phase:** E (Multi-Agent Dynamics)
**Depends on:** Step 07 (opponent modeling — the parent of the coalition detector), Step 09
(MARL: MAPPO / PSRO / `meta_nash`), Step 10 (spinning-top decomposition + EGTA).
**PhD connection (the THESIS FRONTIER — raw L7-16):** everything from Steps 2–10 built existing
tools; Step 11 enters unstudied territory. Three thesis hooks:
- **Contribution #1 (Behavioral Adaptation):** the coalition detector lifts opponent modeling
  from "what kind of player is this?" to "who is allied with whom?" — adapting to the *social
  structure* of the game.
- **Contribution #2 (Multi-Agent Safe Exploitation):** the central gap crystallizes here. In
  2-player games "safe" = bounded deviation from Nash; in N-player FFA, Nash is intractable
  **and** strategically useless (it ignores coalitions), so the safe baseline must be
  behavioral / population-based (Bakhtin et al.'s **piKL**). So Long Sucker (SLS) is the testbed.
- **Contribution #3 (Evaluation Methodology):** standard exploitability has no meaning against a
  coalition; the **EGTA meta-game + Shapley credit** is the alternative. SLS is where it is
  prototyped.

> **In one line:** the moment a third player joins, *alliances* become possible — form them,
> exploit them, betray them. This step builds a native 4-player **So Long Sucker** engine, a
> **coalition detector** (help/harm inference from chip placement), **Shapley credit assignment**
> for a purely-competitive game, a **coalition-aware MAPPO** trainer, and an **EGTA + spinning-top**
> analysis of the resulting agent population — the first RL treatment of dynamic coalitions on a
> game literally designed by Nash, Shapley, Shubik & Hausner to study them.

---

## The one architectural shift from Steps 7–10 (read this first)

Steps 7–10 were **2-player** games with an **exact** net→tabular best-response evaluation via the
Step 07 engine (exploitability = the load-bearing metric). **Step 11 is 4-player FFA**, and the raw
step (PhD-Connection L9-16; Math Flags L320-329) is explicit that **Nash / exploitability are both
intractable and strategically meaningless here.** Consequences baked into this folder:

- **No exact best-response, no exploitability number.** Evaluation is **empirical**: win-rate vs
  random, coalition scores (the detector), the EGTA **payoff tensor**, and the spinning-top
  transitive/cyclic ratio on a **projected pairwise** matrix.
- **The one exact anchor** is the **2-player endgame** (De Carufel & Jerade, raw L195-207): it is
  analytically solved, so it verifies the environment's correctness.

Everything reused from Steps 07/09/10 is used **only where it still applies** (the 2-player
projected meta-game gets `meta_nash` + `spinning_top`; the 4-player game does not).

---

## How this folder is built

Per the per-phase contract in [`../WORKFLOW.md`](../WORKFLOW.md), with the scope decision for this
session:

- **Phases 1–4 are authored; execution + Phase 5 are deferred.** This session wrote the
  *intuition*, *exploration*, *targeted reading*, and the full *implementation* (code + harness).
  **Nothing has been executed here** (WORKFLOW §0: write everything, run nothing). The
  measured-vs-predicted dev log (`EXECUTION_NOTES.md`), the `consolidation/` one-pager + learning
  log, and the EN/BG reports all require verified run results and are left for the post-run session.
- **No fabricated results.** Every number in these docs is a **prediction / target to verify**
  (raw Deliverables L546-554, Validation L556-561).
- **SLS is implemented natively** from the De Carufel & Jerade formalization, not by cloning
  Sharan & Adak's external repo — the core must run on the repo's own code (WORKFLOW §4.2/§6),
  mirroring how Step 09 kept OpenSpiel/PettingZoo optional.
- Foundations are **imported, not copied** (see below).

---

## Phase folders

| Folder | Phase | Contains |
|--------|-------|----------|
| [`intuition/`](intuition/) | 1 — Intuition | `intuition.md`: why the third player changes everything, the poker soft-play analogy, the menu of approaches (Nash vs Shapley/core/nucleolus; static vs dynamic coalitions; Shapley-credit MARL vs piKL behavioral prior), a dated lineage (1950 SLS → 2024 SLS-RL), misconceptions, and a self-check. |
| [`exploration/`](exploration/) | 2 — Exploration | Small, seeded, runnable scripts: play SLS (random + heuristic), hand-coded coalition strategies (fixed-ally vs betrayal), Shapley + core on the glove & 3-player-majority games (exact reference values), and Shapley credit on hand-set SLS states — plus a README (all numbers as predictions). |
| [`targetedReading/`](targetedReading/) | 3 — Targeted Reading | `summary.md`: VIP-only notes on the five core papers (Sharan & Adak, De Carufel & Jerade, Bakhtin piKL, Chalkiadakis book ch2-4, Wang Shapley-Q) + supplementary, with cited sections/equations, three worked **Math Flags** (Shapley by hand, core-LP emptiness, piKL), a synthesis, and a verify-list. |
| [`implementation/`](implementation/) | 4 — Implementation | The full build: `sls_game` + `sls_endgame` + `state_encoding`; the 🔴 core `coalition_detector` + `shapley` + `sls_ppo` + `coalition_mappo` + `sls_egta`; `agents` baselines; `config`/`evaluation`/`tournament`/`plotting`/`validate` — plus a README with the verification runbook, predictions, and a static self-review. |

*(Phase 5 `consolidation/`, `EXECUTION_NOTES.md`, and `deliverables/reports/step11/` were authored in
later sessions once the code had been executed and results verified — see the build status below.)*

---

## Imported foundations (never copied — WORKFLOW §6)

See [`implementation/deps.py`](implementation/deps.py), which bootstraps **Step 10** and **Step 09**
onto `sys.path`:

- **Step 10** — [`../step10/implementation/spinning_top.py`](../step10/implementation/spinning_top.py)
  (`transitive_ratio` / `spinning_top_decomposition`, the **Hodge** split — applied to the projected
  pairwise SLS matrix), and the EGTA meta-Nash-mixture pattern from
  [`../step10/implementation/egta.py`](../step10/implementation/egta.py).
- **Step 09** — [`../step09/implementation/meta_nash.py`](../step09/implementation/meta_nash.py)
  (`solve_meta_nash` for the projected 2-player meta-game),
  [`../step09/implementation/learners.py`](../step09/implementation/learners.py)
  (`torch_available` / `require_torch` — the lazy torch guard).

**Step 07** is the *conceptual* parent (the coalition detector generalizes its opponent-modeling
"observe actions → update beliefs" principle, raw L344/L424) but is re-derived fresh here as
help/harm matrices — nothing is imported from it.

> **Why the SLS PPO is new code, not an import.** Step 09's MAPPO and Step 10's `ppo_agent` are
> **one-step / 2-player** learners; SLS is a **sequential, variable-length, 4-player** turn game
> with action masking, so [`implementation/sls_ppo.py`](implementation/sls_ppo.py) is written from
> scratch (reusing only the clipped-surrogate objective idea).

---

## Scope notes (per WORKFLOW.md + the confirmed plan)

- **Native 4-player engine, empirical evaluation.** No exact solver exists for N=4; all reported
  metrics are win-rate / coalition-score / EGTA-tensor based. The only exact check is the 2-player
  endgame oracle.
- **Self-contained numpy core, guarded neural half.** The env, coalition detector, Shapley credit,
  EGTA tensor, projection, meta-Nash and spinning-top run on `numpy` (+ `scipy` for the meta-Nash
  LP, with a fictitious-play fallback). The coalition-aware MAPPO trainer needs `torch` and SKIPs
  cleanly if it's absent.
- **P2 fallback (raw L621-624):** if SLS proves too brittle, documented alternatives are 3-player
  Leduc with side agreements, Goofspiel, or a simplified custom 4-player game.
- **P3 scope (raw L626):** Contribution #2 here is *tractable heuristics + empirical validation on
  small N-player games*, **not** a general N-player safety theorem.

---

## Build status

- [x] Scaffold (this README + the four phase folders + `deps.py`)
- [x] `intuition/intuition.md`
- [x] `exploration/` (code + README) — **written, not executed**
- [x] `targetedReading/summary.md`
- [x] `implementation/` (code + README + validation harness) — **executed**; artifacts in `implementation/results/` + `implementation/plots/`
- [x] `EXECUTION_NOTES.md` — measured-vs-predicted dev log (seat-0 tie-break fix + `alpha` sweep)
- [x] `consolidation/` — `onePager.md` + `learningLog.md`, drafted from verified run artifacts
- [x] `deliverables/reports/step11/` — EN report (`report_en.md`) + summary (`summary/summaryEn.md`) +
  `figures/` (5 experiment PNGs copied + manifest) + `summary/` conceptual-diagram scripts. **Human
  steps remaining:** run `summary/make_*_figure.py` (needs matplotlib) for the 4 conceptual PNGs, then
  `python3 scripts/build_reports.py --step step11 --lang en` for the two PDFs (pandoc + tectonic not
  present on the authoring machine).
