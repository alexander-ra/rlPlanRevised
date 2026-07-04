<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->
# Learning Log

A running log of cross-step connections, confusions (open / partially-addressed / resolved), and
thesis-connection notes. One entry per step; newest at the top. Confusions carry a status so they
can be revisited and closed in later steps.

---

## Step 7 — Opponent Modeling in Imperfect-Information Games

### Connections (to earlier steps)

- **[Step 2] Nash equilibrium ignores opponent identity -> [Step 7] the opponent model uses it.**
  Step 2's equilibrium is the strategy that refuses to adapt; the model is the machinery that
  deviates on purpose. They are the two endpoints of the safety-exploitation spectrum.
- **[Step 3] MCCFR samples opponent actions from the CURRENT strategy -> [Step 7] the model
  samples/reasons from the INFERRED strategy.** Same sampling-over-a-strategy mechanism; the only
  change is the source of the distribution (self-play strategy vs. estimated opponent).
- **[Step 4] Abstraction clusters similar game states -> [Step 7] type-based modeling clusters
  similar opponent strategies.** Same "group for tractability" idea, moved from state space to
  strategy space.
- **[Step 4] Action translation maps unseen bets to known abstractions -> [Step 7] the model maps
  unseen behavior to known types.** Same nearest-neighbour-in-a-reduced-space logic — and its
  failure mode (misspecification) shows up as the "confident-but-wrong" result.
- **[Step 6] Blueprint strategy (Pluribus/ReBeL) = the Nash baseline -> [Step 7] deviation from
  the blueprint = exploitation.** The model decides *how much* to deviate and *in what
  direction*; Step 8 will bound how far.

### Confusions

- **Consistent model, real-time cost.** The sequence-form consistent estimator requires solving a
  convex program per update. Is that fast enough for online play?
  -> **PARTIALLY RESOLVED (empirical).** Verified accurate on Kuhn strategy recovery
  (TV ~0.004-0.021), but the per-refit solve grows with history (seconds per refit at ~20k hands),
  so it is impractical in the naive online loop. Open sub-question: incremental/warm-started
  solving, or Step 8 subgame approximations, to make it real-time.
- **Non-stationary opponents.** All three models assume a stationary opponent for their
  convergence guarantees. How badly do they degrade when the opponent adapts?
  -> **PARTIALLY ADDRESSED.** Change-point forgetting helps exactly when a stale model is harmful
  (Kuhn: -0.116 -> +0.226 after a switch) but can *hurt* when the new opponent is exploitable and
  the detector false-fires (Leduc). A principled treatment (confidence-scaled forgetting, better
  change signals) is deferred — candidate for the Step 14 evaluation framework.
- **Partial observability at scale.** On Leduc, hidden cards already slow convergence markedly
  (continuous-model TV 0.11-0.36 vs 0.006-0.030 on Kuhn). In full No-Limit Hold'em, how many
  hands would recovery need? -> **OPEN.** This is why Step 4 abstraction matters: model in the
  abstract space, not the full one.

### Resolved confusions (closed this step)

- **"Best-respond to observed frequencies."** Confirmed dangerous: on small samples an underfit
  model best-responds to a wrong estimate and can *lose* to an unexploitable opponent (continuous
  vs. Nash on Leduc, -0.175 vs a -0.083 ceiling). Exploitation must be scaled to how earned the
  read is.
- **"A model that fits the data has recovered the true strategy."** False in general — responding
  to the posterior mean can converge to the wrong strategy even with infinite data; the
  sequence-form consistent (FMAP) formulation is the fix.
- **"You can exploit anyone."** No — against a Nash opponent the exact best-response ceiling *is*
  the game value; every model earns approximately that and never more.

### Thesis connection

- **Contribution #1 (Behavioral Adaptation Framework) — the sensor.** This step built the
  component that infers opponent behavior from observations. Step 8 builds the actuator (safe,
  KL-regularized exploitation); the continuous model's Nash self-leak is the empirical motivation,
  and the consistency theory (Ganzfried 2025) is the principled backbone the framework extends.
- **Log for Step 11 (multiplayer).** Modeling several opponents at once is not N x single-opponent:
  the jointly-optimal response differs from combining individual best responses, and the convex
  consistency guarantee no longer holds for N > 2. Revisit shared priors ("all opponents are
  fish") and the compute scaling there.
