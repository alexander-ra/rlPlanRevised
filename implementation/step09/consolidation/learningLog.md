# Step 09 — Learning Log

> Phase 5 of Step 09. A short, first-person reflection stitched from the per-phase "Key
> takeaways" and the actual runs. Verified numbers only (see `onePager.md` for the table).

---

## What I set out to learn

How reinforcement learning changes when more than one agent is learning at once — and why the
tidy convergence guarantees of Steps 2–8 (CFR → Nash in two-player zero-sum) stop applying. The
organizing idea I wanted to internalize: **non-stationarity**. From any one agent's seat, the
"environment" contains other agents who are themselves updating, so the target keeps moving.

## What clicked, phase by phase

- **Intuition.** The "learning to dance with a partner who is also learning" picture did the
  heavy lifting. It made the three fixes feel inevitable: pretend the partner is the floor
  (IL), give a coach the two-dancer view at practice only (CTDE), or keep a roster of routines
  and always train the counter to the best mixture (PSRO). The Markov-games bridge (§6 of the
  intuition doc) is the piece I keep coming back to: the *vocabulary* maps cleanly (behavioral
  strategy ↔ decentralized policy, info set ↔ observation, counterfactual value ↔ centralized
  critic), but the *guarantees* — CFR convergence and the minimax value anchor — do not cross
  into N>2. That missing anchor is literally Contribution #2's problem statement.

- **Exploration.** Seeing it before proving it paid off. Matching Pennies genuinely refuses to
  converge; the self-play script made the single most useful distinction of the step concrete —
  the **average** iterate's NashConv falls (`0.24 → 0.031` on Kuhn) while the **last** iterate
  keeps oscillating (`0.33–0.83`). That is *why* PSRO mixes over a population instead of
  trusting the latest policy, and it connects straight back to CFR's average-strategy trick.

- **Targeted reading.** The six papers collapse onto two axes: cooperative-vs-competitive and
  static-vs-dynamic-opponent. CTDE is one idea in three flavors (per-agent critic → factorized
  value → single value), and MAPPO's punchline — *simplicity often wins* — is a genuine
  warning for the thesis: don't over-engineer.

- **Implementation + runs.** The build reused Step 07's exact best-response engine as PSRO's
  oracle, so "did MARL converge?" is answered by the very same exploitability number the
  game-theory steps used. That reuse is the cleanest thing about the step.

## Where reality bit back (the instructive part)

Four predictions did not survive contact with the runs, and per the workflow I kept them and
reconciled rather than editing history:

1. **Matching Pennies doesn't orbit at constant radius** — it spirals outward (IGA) or drifts
   to the corners (softmax). Non-convergence is the lesson; the mechanism was subtler than I
   assumed.
2. **PSRO on Leduc is slow** — 20 exact-BR rounds only reach exploitability ~2.16, not the
   predicted < 0.5. Kuhn was machine-zero by round 6. The wall is size, and it rhymes with
   Step 08's global-vs-local scaling finding.
3. **Goofspiel K=4 oscillates** where K=3 converged — the one result I can't yet explain; two
   concrete suspects noted for next session (no BR de-duplication; pure-BR population too weak).
4. **A centralized critic did not solve the climbing game** — nobody reached the optimum, and
   MADDPG actually did worse than independent learners. The critic-variance claim held
   separately (central residual ~`3e-11` vs `0.077`), so the honest takeaway is "CTDE lowers
   critic variance ≠ CTDE fixes hard-exploration coordination."

And a methodological lesson: the two neural effects (critic variance, communication) were
**invisible at smoke scale** and only appeared once trained longer — the smoke config proves
the code runs, not the phenomena.

## Headline lessons I'm keeping

- Non-stationarity is structural, not a compute-budget problem.
- CTDE = centralize the critic at training, decentralize the actor at execution — and it buys
  variance reduction, which is necessary but not sufficient.
- Self-play/PSRO work in the **average/population**, not the last iterate.
- LOLA reframes the opponent as a learner and turns IPD defectors into cooperators
  (`1.04 → 2.82`) — the dynamic complement to Step 7's static opponent model.
- The N>2 minimax gap is the open door to the thesis.

## Open threads

- Fix and re-run the two flagged pieces (Goofspiel K=4; MADDPG counterfactual baseline).
- Push Leduc PSRO further (more rounds and/or an RL/approximate oracle) to see how close to
  Nash a population can get, and at what cost.
- Combine LOLA's dynamic view with Step 7's static opponent model (Contribution #1).
