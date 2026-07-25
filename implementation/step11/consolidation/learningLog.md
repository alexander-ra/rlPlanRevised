# Step 11 — Learning Log

> Phase 5 of Step 11. A short, first-person reflection stitched from the per-phase "Key takeaways"
> and the actual runs. Verified numbers only (see [`onePager.md`](onePager.md) for the full table and
> artifact caveats).

---

## What I set out to learn

How temporary **alliances** form, get exploited, and get betrayed in a competitive free-for-all —
the thing that only exists once there is a third player. Concretely: build the first coalition-aware
RL treatment of **So Long Sucker** (the 1950 game Nash, Shapley, Shubik & Hausner designed to study
exactly this), and use it to internalize the qualitative jump from N=2 to N≥3 — where **Nash and
exploitability stop being tractable *and* stop being meaningful**, so "did it work?" can no longer
be a single exploitability number. The organizing question I wanted to answer: *can a learning agent
be made to form coalitions on purpose, and how do you even measure that when there is no best
response to compute against?*

## What clicked, phase by phase

- **Intuition.** The dinner-party picture (four guests, one house, everyone pairs up and then the
  smart move is to have betrayed your partner one turn early) did the work. The unlock was seeing
  that SLS *encodes the whole alliance in the moves themselves* — placing another player's chip is a
  handshake, capturing their pile is the knife — so there is no separate negotiation phase to model.
  And the reframing of all three thesis contributions: adaptation becomes *social-structure*
  adaptation, safety loses its Nash anchor, and evaluation loses exploitability.

- **Exploration.** Seeing it before proving it paid off again. The glove game (`(2/3,1/6,1/6)`, core
  `{(1,0,0)}`) made *fairness ≠ stability* concrete, and the 3-player majority game's **empty core**
  made "coalitions in a competitive game are inherently unstable" a fact rather than a slogan. The
  hand-coded fixed-ally vs betrayer scripts showed the pair concentrating wins and the betrayer
  beating the loyal partner — the form-exploit-break loop, visible before any learning.

- **Targeted reading.** Five sources line up into one arc: SLS-RL exists but is coalition-blind
  (Sharan & Adak), its 2-player endgame is exactly solved (De Carufel & Jerade), the N-player
  safe-play recipe is **piKL** = regularize toward a behavioral prior instead of Nash (Bakhtin), the
  learnable training signal is **Shapley credit** (Wang et al.), all grounded in classical
  cooperative GT (Chalkiadakis). The subtle bit I had to keep honest: I could reproduce the two
  cooperative-GT toy games exactly, but the De Carufel & Jerade *theorem statements* remain a
  verify-when-you-read-it item — my endgame oracle is exact for *my engine's* rules, not a
  transcription of their paper.

- **Implementation + runs.** The build is a native 4-player engine (no external repo), a coalition
  detector (help/harm matrices), Shapley credit reworked for a competitive game (coalition value =
  win-probability, not a shared pot), a masked episodic PPO trained by self-play with a
  Shapley-blended reward, and an EGTA pipeline that projects the 4-player payoff **tensor** to a
  pairwise matrix so Step 09's meta-Nash and Step 10's spinning-top still apply. The cleanest
  decision was accepting up front that **evaluation is empirical** here — win-rate, coalition score,
  EGTA cyclic ratio — with the 2-player minimax endgame as the single exact anchor.

## Where reality bit back (the instructive part)

Two things did not survive contact with the runs; per the workflow I kept the predictions and
reconciled rather than editing history.

1. **The "symmetric" game was not symmetric — and it was a tie-break bug, not first-mover order.**
   Player 0 was winning ~47-59% instead of 25%, monotone in seat order, across three independent
   scripts. My first instinct ("first-mover advantage, probably fine") was wrong on the mechanism:
   ~99.5% of random games end in a **deadlock** decided by `_most_chips`, whose lowest-index
   tie-break quietly handed seat 0 ~2x its fair share. An unbiased random tie-break fixed it —
   symmetric Shapley spread `0.54 → 0.013`, all-random winners now uniform — and, tellingly, revealed
   that the impressive `~0.87` hero win-rate had *also* been the same artifact (hero always sat in
   seat 0); the fair number is `~0.41`. The lesson: in a game that almost always ends in a near-tie,
   the tie-break rule is the most load-bearing line in the engine.

2. **"Coalitions don't emerge at scale" was a mis-set knob, not a failure.** My single-config runs
   used `alpha=0.3` and showed the coalition signal collapse at scale. The 5-seed sweep overturned
   that completely: `alpha` is the dominant knob and `0.3` is a **dead zone**; at `alpha≈0` the
   Shapley agent's coalition score beats sparse by **`+0.038 ± 0.010`** (~4.4x) and the effect
   *grows* with game size, while every `alpha≥0.3` cell is negative. It even turned out the cheap
   critic-value proxy beats the expensive counterfactual credit. So the primary thesis signal is
   real and robust — I had simply been measuring it in the one regime where the sparse term drowns
   it out.

And a methodological echo of Steps 9-10: **a single config hides what a seeded sweep reveals.** Both
of the big corrections here came from refusing to trust one run — a bug diagnosis and a paired grid.

## Headline lessons I'm keeping

- **At N≥3 you trade exact evaluation for empirical evaluation.** No exploitability; instead
  win-rate + coalition score + EGTA cyclic ratio, anchored by the one exactly-solvable subgame
  (2-player endgame).
- **`alpha` (the sparse/Shapley blend) is the coalition knob**, and coalition behavior costs
  competitive performance (`alpha=0` → win-rate ~0.29 near the floor). Forming is primary, winning
  secondary — quantified.
- **Empty core ⇒ structural betrayal.** The majority game's empty core is the SLS situation: no
  stable allocation exists, so coalitions *will* break.
- **Engine rule fidelity matters more than solver code.** Both remaining weaknesses (the seat bias,
  the sub-dominant cyclic ratio) live in the engine's simplifications, not in the Shapley/EGTA math —
  which reproduced its textbook checks exactly.
- **Which population you decompose decides ladder-vs-wheel** (the Step-10 lesson, confirmed): a
  skill-ladder pool looks transitive (`~0.3` cyclic), a coalition pool looks strongly cyclic
  (`~0.57-0.69`).

## Connections (Steps 2-10 → Step 11)

- **[Step 2] Nash → [Step 11] Nash retired.** The equilibrium concept that anchored everything since
  Step 2 is, for the first time, both intractable and strategically empty; the step is built around
  its absence.
- **[Step 7] Opponent model → [Step 11] coalition detector.** Same "observe actions → update
  beliefs" principle, lifted from "what hand does this player hold?" to "who is allied with whom?"
  (Contribution #1) — and it cleanly recovers a planted `{0,1}` coalition (score `10.0`).
- **[Step 8] Safe exploitation vs Nash → [Step 11] safe exploitation vs a behavioral prior.** With
  no minimax anchor, Step 8's "bounded deviation from Nash" becomes piKL's "bounded deviation from a
  human/population prior" — Contribution #2, now concrete because the core is empty.
- **[Step 9] PSRO meta-Nash → [Step 11] meta-Nash on the projected SLS meta-game.** Reused directly
  (`solve_meta_nash`) on the pairwise projection.
- **[Step 10] Spinning-top → [Step 11] tested the "large cyclic component" prediction directly.**
  Confirmed in direction (coalition pool cyclic `~0.57-0.69`), honestly short of strict dominance.
- **[Step 11] → [Step 12] negotiation / [Step 14] EGTA.** The behavioral-prior safety gap points at
  Step 12 (language/negotiation, CICERO/Welfare-Diplomacy), and the EGTA-tensor evaluation is the
  multi-agent generalization of exploitability that Step 14 inherits (Contribution #3).

## Confusions

- **Does my SLS engine match De Carufel & Jerade's rules?** → **OPEN.** The endgame oracle is exact
  for my ruleset, but the paper's turn/capture/tie-break details (and Theorems 1-3) are still a
  verify-when-you-read-it item — and the seat-0 bug (R1) shows the tie-break rule genuinely changes
  outcomes, so this reconciliation is not cosmetic.
- **Is the 2-type pairwise projection throwing away the coalition cycling?** → **LIKELY.** The cyclic
  ratio sits just under strict dominance, and the prime suspect is that projecting a 4-player payoff
  tensor to head-to-head pairs discards 3-/4-player coalition effects (raw L600). A tensor-native or
  3-type decomposition is the open question.
- **Is the cheap proxy credit "good enough" or just good enough *here*?** → **PARTIALLY ANSWERED.**
  The proxy beat the counterfactual on SLS at low `alpha`, but that may be SLS-specific; whether it
  generalizes is untested.
- **Is there a formal N-player safety guarantee?** → **OPEN — the Contribution #2 gap, made
  concrete.** The empty core removes any core-based stability, and piKL gives a behavioral baseline
  with no exploitability bound; formalizing "safe" for an N-player coalition setting is exactly the
  thesis frontier this step frames but does not close.

## Open threads

- Reconcile the engine turn/tie-break model against De Carufel & Jerade, then re-check the spinning-
  top dominance (R1 + R3 likely share this root).
- Adopt `alpha≈0.05-0.1` as the coalition-training default (evidence in the sweep) — a human design
  decision, deliberately not silently applied.
- Try a 3-/4-player-aware EGTA projection to see whether the coalition cycling crosses the strict
  >50% line once 3-way effects are not collapsed away.
- Regenerate the stale post-fix `results/scale_results.json` so the committed scale tournament matches
  the sweep.
