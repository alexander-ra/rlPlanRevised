# Step 10 — Learning Log

> Phase 5 of Step 10. A short, first-person reflection stitched from the per-phase "Key
> takeaways" and the actual runs. Verified numbers only (see `onePager.md` for the table).

---

## What I set out to learn

How to reason about, and train, **populations** of agents. Two halves. First, the evolutionary
game-theory lens: replicator dynamics (which strategy shares grow?) and the spinning-top
decomposition (is this game a skill ladder or a rock-paper-scissors wheel?). Second, the machinery
that turns a population into a training signal: an AlphaStar-style **PBT league** — main agents,
main exploiters, league exploiters, freezing, PFSP matchmaking — with EGTA (empirical game-theoretic
analysis) and Elo to evaluate it. The organizing question I wanted to internalize: **when does a
self-training population converge, and when does it cycle?**

## What clicked, phase by phase

- **Intuition.** The "dojo" picture did the work: main agents are students, exploiters are sparring
  partners whose only job is to find and punish a weakness, and freezing keeps a museum of past
  selves so nobody forgets how to beat an old style. The key mental unlock was separating
  *transitive* skill (there is a best) from *cyclic* structure (there is no best, only
  counters) — because that single distinction predicts whether naive self-play will settle or spin.

- **Exploration.** Seeing it before proving it paid off again. The replicator playground made RPS
  visibly *orbit* (never settling) while Prisoner's Dilemma collapsed to all-Defect; the mini-PBT toy
  showed diversity **collapse to zero** on the transitive game but **churn forever** (0.07-0.29) on
  the cyclic one; and the PSRO-population peek on Leduc already flashed the surprise that its
  meta-game is mostly *cyclic* (transitive ratio `~0.45`), not the skill ladder I assumed.

- **Targeted reading.** Jaderberg's PBT, the FTW/AlphaStar league, Balduzzi's spinning-top, and Tuyls'
  EGTA line up into one idea: evaluate and evolve a *population*, and use its game-theoretic structure
  (transitive vs cyclic, meta-Nash) as both the diagnosis and the training target. The subtle bit I
  had to get right in code was the spinning-top decomposition — the SVD rank-1 method mislabels RPS as
  ~70% transitive, while the combinatorial-Hodge (ratings-difference) method correctly gives 0.

- **Implementation + runs.** The build wires neural PPO agents to Leduc via an info-state encoder, then
  extracts each network into a *tabular* policy so Step 07's **exact** best response grades it. That
  reuse is the cleanest thing about the step: "did the league improve?" is answered by the very same
  exploitability number as every game-theory step before it.

## Where reality bit back (the instructive part)

Three predictions did not survive contact with the scale run; per the workflow I kept them and
reconciled rather than editing history:

1. **The league's meta-Nash was supposed to be less exploitable than any member — and at scale it
   wasn't.** Smoke confirmed it (meta-Nash put all weight on the single best agent). Scale spread the
   weight and the collapsed behavioral mixture scored `3.42` against a best member of `1.31`. It is not
   a bug — the meta-Nash minimizes *meta-game regret*, not *full-game exploitability*, and mixing
   behavioral policies can *add* exploitable tells. The takeaway flips: report the exploitability of
   the actual collapsed mixture; don't assume mixing helps.

2. **Leduc's meta-game is mostly cyclic, not transitive.** The best-response meta-game came out
   `~0.45` transitive / `~0.90` cyclic (27 three-cycles), while the league's snapshot meta-game was
   `~0.95` transitive. Same game, two populations, opposite structure: best responses cycle; training
   snapshots form a ladder. This reframed the whole "is poker transitive?" question as "*which
   population* are you decomposing?"

3. **League exploitability is non-monotonic.** I expected a monotone decrease. Scale dropped from
   `4.73` to a minimum near `1.21`, then **rose back to ~2.05** (min-main) / `~2.96` (meta-Nash) over
   120 epochs. The best *frozen* snapshot (`1.31`) is from mid-run; the *live* agents regressed late
   under exploiter pressure. Smoke's 15 epochs were too short to show it — it ends exactly at its
   minimum. The honest lesson: a league loop running is not a league loop improving.

And a methodological echo of Step 09: **scale reveals what smoke hides.** Here it is the late-training
regression and the meta-Nash-mixing failure — both invisible in the fast config.

## Headline lessons I'm keeping

- The transitive/cyclic ratio is a *pre-training diagnostic*: cyclic games will cycle under naive
  self-play/PBT and need explicit diversity or population machinery.
- Meta-Nash over a population optimizes meta-game regret, **not** full-game exploitability — the two
  can disagree (§R1), so evaluate the collapsed mixture directly.
- A PBT league produces strong *individuals* (best snapshot `1.31` beat PSRO `2.16` and self-play
  `3.68`) but carries **no monotonicity or safety guarantee** — it can regress (§R3).
- Exact evaluation is the anchor: extracting neural policies to tabular and scoring them with Step
  07's exact best response makes every population claim ground-truthed.

## Connections (Steps 2-9 -> Step 10)

- **[Step 2] Nash equilibrium -> [Step 10] Nash of the meta-game.** The Step 2 solver now runs one
  level up: equilibria over *populations of policies* (EGTA meta-Nash), not actions in a game.
- **[Step 7] Opponent model -> [Step 10] main exploiters as automated opponent modelers.** The
  exploiters find weaknesses in the main agents — the population-level analog of Step 7's Bayesian
  read (Contribution #1).
- **[Step 8] Safe exploitation -> [Step 10] the three-agent-type league IS a safety mechanism.**
  Exploiters supply the selection pressure that is supposed to keep main agents honest — but §R1/§R3
  show it is heuristic, with no guarantee (Contribution #2).
- **[Step 9] PSRO -> [Step 10] the league is asynchronous PSRO with neural oracles.** Exact best
  response becomes neural best response; Step 9's meta-Nash becomes Step 10's EGTA.
- **[Step 10] Spinning-top -> [Step 11] prediction:** FFA coalition games will have a *large cyclic
  component* (A+B beat C, B+C beat A, C+A beat B), so naive PBT will cycle and need diversity methods.
- **[Step 10] EGTA -> [Step 14] prediction:** meta-Nash of the agent population becomes a core
  evaluation tool — the multi-agent generalization of exploitability (Contribution #3).

## Confusions

- **Does the AlphaStar league design make sense at Leduc scale (7-8 agents vs ~600)?** ->
  **PARTIALLY ANSWERED.** The exploiter mechanism does drive early improvement even here (main-agent
  exploitability `4.73 -> ~1.21` at scale), and produces individuals that beat PSRO and self-play. But
  the diversity payoff is thin (behavior clusters to 1; Elo spread compressed to `~1198-1211`), and
  the late-training regression (§R3) suggests the design needs its safety/retention pieces even at
  small scale.
- **Replicator dynamics assume a fixed payoff matrix, but league agents are learning.** How does that
  non-stationarity interact with the EGT analysis? -> **OPEN** (links to Step 9's learning-dynamics
  question; the non-monotone league trajectory §R3 is this non-stationarity showing up empirically).
- **Spinning-top needs the full O(n^2) payoff matrix between all agents.** Is there an efficient
  approximation for large populations? -> **OPEN** (relevant to Step 14 scaling).
- **Is there a formal population-safety guarantee?** Step 8 proved safe exploitation for two players;
  the AlphaStar exploiters are heuristic and, as measured, do not prevent the meta-Nash from being
  more exploitable than a member or the mains from regressing. -> **OPEN — this is the Contribution #2
  gap made concrete.**

## Open threads

- Fix §R3: add best-snapshot retention / population regularization and re-run to see whether the
  late regression disappears; if it does, the guarantee gap is a *training* issue, if not it is a
  *design* one.
- Decide whether population evaluation should report the meta-Nash mixture or the best-response-robust
  member (§R1) — and whether a diversity-regularized meta-solver changes the answer.
- Carry the transitive/cyclic diagnostic into Step 11's FFA games and test the "large cyclic
  component" prediction directly.
