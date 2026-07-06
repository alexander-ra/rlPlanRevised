# NLHE 6-Max Blueprint — Project Context

Durable reference for what this project is, why it exists, and how its output
gets used later. Purpose: so this doesn't need re-explaining from scratch in a
future session (this repo, an external tool, or a future me). For technical
proposals/tradeoffs on the trainer itself, see `../improvementProposals.md`
(separate document, not duplicated here).

## What this is

A side project alongside Alexander's PhD study plan (see repo root
`CLAUDE.md`/`PLAN.md`): train the strongest reusable No-Limit Hold'em base
strategy achievable on idle personal-machine compute, for 6-max. It is explicitly **not** meant to be a finished,
polished poker AI — it's infrastructure and a starting point for later work.

## Why this exists (the thesis connection)

PhD topic: adaptive strategy learning in multi-agent imperfect-information
environments. Three planned thesis contributions (see `PLAN.md` / the May
report in `deliverables/reports/ruseMay/`):

1. **Behavioral Adaptation Framework** — real-time opponent inference.
2. **Multi-Agent Safe Exploitation** — KL-regularized (πKL) exploitation
   anchored to a safe reference strategy, extended toward N-player games.
3. **Evaluation Methodology** — domain-agnostic adaptability/robustness
   measurement.

The study plan's own testbeds (Kuhn Poker, Leduc Hold'em) are toy games by
design — small enough for exact solutions, but too small to be a compelling
demonstration domain on their own. This project's blueprint is meant to give
the thesis a real-game-scale demonstration:

- The **distilled policy network** (blueprint → NN) is a candidate **πKL
  anchor / safe reference strategy** for Contribution 2, at NLHE scale instead
  of Kuhn/Leduc scale.
- The **6-max environment + baseline bot population** is a testbed for
  Contribution 1 (opponent modeling) and Contribution 3 (evaluation) beyond
  toy games.
- Separately, the user's employer (a poker company) has offered anonymized
  real hand-history data (see `deliverables/dataRequest/`) — pending legal
  sign-off, not yet received. When it arrives, it enables behavioral cloning
  of a **human-prior** policy (as opposed to this project's equilibrium-ish
  blueprint), which is the second kind of anchor the Diplomacy-style πKL
  paradigm uses. That is future, separate work — this project's engine,
  encoding, and eval infrastructure are built to be reusable for it, but no
  real data has been ingested yet.

## Timeframe

- Side project during a ~1 month window of reduced GPU/CPU demand from the
  study plan (started 2026-07-03), but **explicitly continuable indefinitely
  after** that month if useful — nothing here is scoped to finish by a hard
  deadline. Progress is checkpointed/resumable specifically so it can be
  paused and picked back up.
- Rough phase markers so far: system built and gate-checked (2026-07-03) →
  pilot run caught and fixed 3 real bugs (button/traverser bug, eval crash,
  hash-table insert race) → benchmark sweep across bucket sizes → 200-bucket
  long run launched and stable overnight (2026-07-04, currently training,
  ~146k iters/s, several billion iterations in) → current phase: deciding
  whether/how to improve postflop training coverage before committing the
  full ~300–400h budget.

## What "done" looks like, and how the output gets used later

The tabular MCCFR blueprint being trained now is **a seed, not the final
product** — a warm start so that a subsequent self-play (RL) phase doesn't
begin from a random strategy. Concretely, the user's stated plan: use this
blueprint as a base to "mimic play" and train a neural-network version through
self-play, which fills in the fine-grained detail the tabular abstraction
can't (bucket resolution, unvisited states) on top of a solid, sane
foundation.

Architectural framing agreed on for that next phase (from
`../improvementProposals.md`, restated here because it shapes what "good
enough" means for the current run): an **asymmetric spiral**, not a symmetric
tabular↔NN ping-pong. That is — tabular MCCFR does local/exact solving; the
NN generalizes across the abstraction and improves further via self-play
beyond what tabular search alone reaches; that can feed back into finer,
targeted tabular subgame solves; then re-distill. Each round-trip should add
something the other representation couldn't produce on its own (self-play
skill gain, or finer subgame resolution) — not just repeat the same
computation. A GPU sitting idle during the CFR phase is expected: CFR here is
a CPU-bound workload; the GPU's role is card-abstraction bucketing (done),
distillation, and later self-play / NN value estimation.

Because the blueprint is a seed rather than the deliverable, "sensible
everywhere and low-variance" matters more than "deep/precise in a few common
lines" — this reframes how postflop under-coverage (see below) should be
judged: an under-trained-but-not-random postflop is an acceptable, even
expected, intermediate state; a *randomly-playing* postflop is the failure
mode actually worth fixing, because it's exactly the cold start self-play is
meant to avoid paying for twice.

## Current status (brief — see other docs for detail/history)

- Format: 6-max, 100bb, no antes; action abstraction fold/call/pot-raise/allin,
  max 2 raises/street; card buckets 169 preflop (lossless) / 200 postflop
  (flop, turn, river) — chosen after a benchmark sweep across 100/200/400
  showed throughput was roughly flat once a hash-table insert race was fixed
  (200 balances resolution vs. training visits per bucket for this hardware).
- Currently training (run id `20260703_6max_200_v1`), checkpointing and
  evaluating on a schedule, dashboard reachable via a Cloudflare tunnel.
- Known live issue being discussed as of this note: postflop infosets are
  under-visited relative to preflop (preflop converged and sane; postflop
  ~26–35% touched at all, with far less average visit mass per touched
  infoset than preflop). Whether/how to address this via sampling changes
  (not bucket-size changes, which the owner has rejected) is under active
  discussion — see `../improvementProposals.md` for the technical options and
  their status.

## Where to look for more (pointers, not copies)

- `../README.md` — build/run instructions, architecture summary, gates passed.
- `../DEVIATIONS.md` — every deviation from the original plan and why (race
  fix, bucket-count history, rounding fixes, etc.).
- `../BENCHMARK_PROTOCOL.md` — the bucket-size benchmark procedure and results.
- `../improvementProposals.md` + `A/`–`E/` — technical proposals for the
  postflop-coverage problem (sampling changes, algorithmic changes, scale
  changes), staged but not wired into the live trainer.
- Repo root `PLAN.md`, `CLAUDE.md`, `deliverables/reports/ruseMay/` — the PhD
  thesis context this project ultimately serves.
