# Step 10 — Consolidation (internal weave)

> Phase 5 of Step 10. Written **after** the code was executed, from **verified** run artifacts
> only (`implementation/step10/implementation/results/{smoke,scale}_results.json` and
> `exploration/figures/*.json`). This is the internal weave of the per-phase "Key takeaways";
> the externally-shared write-up is `deliverables/reports/step10/`.

---

## The one-sentence step

Two lenses on **populations** of strategies: **evolutionary game theory** (replicator dynamics +
the transitive/cyclic "spinning-top" decomposition) tells you *what kind of game you are in*, and
a small **AlphaStar-style PBT league** of neural PPO agents on Leduc tells you *what happens when a
population trains itself* — both validated against Step 07's exact best-response / exploitability
oracle so "did it work?" is answered by the same NashConv number used since Step 2.

---

## What each experiment actually showed (measured)

| Experiment | Prediction | Measured | Verdict |
|---|---|---|---|
| Replicator — Prisoner's Dilemma | Cooperator share -> 0 | `x -> [0,1]`, converged, orbit radius `0.71` | confirmed |
| Replicator — Hawk-Dove | interior ESS `V/C = 0.5` | `x -> [0.5,0.5]`, converged, orbit radius `0.0` | confirmed |
| Replicator — Rock-Paper-Scissors | closed orbit, never converges | `converged:false`, orbit radius `0.095` around `(1/3,1/3,1/3)` | confirmed |
| Replicator — Stag Hunt | basin-dependent pure ESS | `x0=[0.8,0.2] -> [1,0]`; `x0=[0.2,0.8] -> [0,1]` | confirmed |
| Spinning-top — RPS | purely cyclic | transitive `0.0` / cyclic `1.0` (Hodge); SVD gives `0.707` (documented caveat) | confirmed (Hodge) |
| Spinning-top — pure skill ladder | purely transitive | transitive `1.0` / cyclic `0.0` | confirmed |
| Spinning-top — PSRO-Leduc meta-game | "Leduc is transitive" | transitive `0.41-0.46`, **cyclic `0.89-0.91`**, 27 three-cycles | contradicted; BR-populations cycle (§R2) |
| League — main-agent exploitability | monotone decrease | smoke `4.67 -> 3.04`; scale `4.73 -> min ~1.21 -> back to 2.05` | confirmed early, **degrades late at scale** (§R3) |
| League — best individual vs baselines | league competitive | best snapshot `1.31` < PSRO `2.16` < self-play `3.68` (scale) | confirmed |
| EGTA — meta-Nash <= best individual | meta-Nash no worse | smoke `2.665 = 2.665` (true); **scale `3.42` > `1.31` (false)** | contradicted at scale (§R1) |
| Elo — skill progression | meaningful spread | live agents `~1176-1211` (smoke), `~1198-1210` (scale) | confirmed (compressed) |
| Diversity — effective population | grows with size | active `1` (smoke) -> `3`, participation `1.92` (scale); behavior clusters -> `1` | mixed (§note) |
| Baseline — CFR-Nash floor | ~0 exploitability | `0.033` (2k iters) / `0.0099` (20k iters) | confirmed |

---

## The three reconciliations (kept predictions + what really happened)

Per WORKFLOW §0.1 the pre-run predictions are kept; what actually happened is appended.

1. **Meta-Nash of the league is NOT less exploitable than its best member — at scale.** The raw
   step's Exit Checklist expected "meta-Nash of the league is less exploitable than any individual
   agent." Smoke confirmed it trivially (the meta-Nash put weight `1.0` on the single best agent, so
   meta = best = `2.665`). At scale the meta-Nash spreads weight (`0.645` on one agent plus a tail)
   and its collapsed behavioral mixture scores exploitability `3.42`, **worse** than the best single
   snapshot (`1.31`). This is a genuine phenomenon, not a mixing bug (the identical
   `mixture_behavioral_policy` code path gave meta = best in smoke): the meta-Nash minimizes
   *meta-game regret* (do well against the population), which is **not** the same objective as
   minimizing *full-game exploitability*, and a realization-weighted mixture of behavioral policies
   can be *more* exploitable than its components (the mixture creates info-set "tells" a best
   responder punishes). The lesson survives inverted and sharper: population evaluation must report
   full-game exploitability of the collapsed mixture, not assume mixing helps.

2. **The PSRO-Leduc meta-game is mostly cyclic, even though Leduc "feels" transitive.** The intuition
   doc framed poker as a skill ladder. Measured, the *meta-game among exact best responses* on Leduc
   is `~0.45` transitive / `~0.89-0.91` cyclic with 27 three-cycles (exploration and both configs
   agree). The **league** meta-game, by contrast, is `~0.94-0.98` transitive. Reconciliation, not a
   bug: a population of *best responses* cycles (A beats the mixture, B beats A, a later BR beats B) —
   exactly Balduzzi's spinning-top; a population of *training-trajectory snapshots* forms a
   transitive skill ladder because later snapshots are (mostly) better than earlier ones. Which
   population you build decides whether you see cycles or a ladder.

3. **League exploitability is non-monotonic at scale — it improves, then degrades.** Predicted a
   monotone decrease. Smoke (15 epochs) shows a clean drop `4.67 -> 3.04` and ends at its minimum.
   Scale (120 epochs) drops `4.73 -> ~1.21` (min-main around epoch 64; meta-Nash bottoms `~1.32` and
   plateaus `~1.60`) and then **rises back to `~2.05` (min-main) / `~2.96` (meta-Nash)** by epoch 119.
   The best *frozen snapshot* (`1.31`) is therefore captured mid-run, while the *live* main agents
   regress late. This is the honest headline of the scale run: under sustained exploiter pressure the
   main agents chase their exploiters and lose ground on absolute exploitability (churn / partial
   forgetting), and it is only visible once training is long enough — smoke proves the loop runs, not
   that it keeps improving. Flagged for a follow-up (freeze-the-best / population regularization);
   documented, not fixed.

Minor: behavioral **clustering collapses to a single cluster** at scale (`max_pairwise_distance 0.48`
> threshold `0.30`, but single-linkage merges everything) even with `num_active = 3` and
participation ratio `1.92`. Diversity here is *weight-level* (the meta-Nash spreads support), not
*behavior-level* (the policies are near-identical) — and the metric is threshold-sensitive.

---

## Threads handed to the deliverables / next steps

- **EGT is a diagnostic, not just theory:** the transitive/cyclic ratio predicts *before training*
  whether naive self-play/PBT will converge (transitive) or cycle (cyclic). This is the tool Step 14
  inherits for population-level evaluation, and the reason Step 11's FFA coalition games (predicted
  large cyclic component) will need explicit diversity machinery.
- **The population-safety gap is now concrete (Contribution #2):** the AlphaStar exploiter mechanism
  is the population analog of Step 08's safe exploitation, but §R1 and §R3 show it carries **no
  guarantee** — the meta-Nash can be more exploitable than a member, and the main agents can regress.
  Formalizing "safe" for a population with no minimax anchor is exactly the open door.
- **Two flagged code items** to resolve before reusing at larger scale: the late-training exploitability
  regression (§R3: add best-snapshot retention / regularization) and whether the meta-Nash-mixing
  result (§R1) motivates reporting the best-response-robust member instead of the mixture.
- **Thesis hooks confirmed:** main exploiters = automated opponent modelers (Contribution #1, the
  population lift of Step 07); league = asynchronous PSRO with neural oracles (Step 09 -> Step 10);
  EGTA/meta-Nash = the evaluation methodology (Contribution #3).
