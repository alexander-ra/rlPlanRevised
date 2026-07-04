# D — reduce the scale (abstraction)

These change the infoset space, so they are **NOT resume-compatible**: they need
a fresh table (`build_table`) and, for card buckets, rebuilt bucket artifacts
(`scripts/build_buckets.py`). Treat as a new run, not a hot patch.

## D1 — coarser postflop card buckets  (rejected by owner)

Lower `buckets.{flop,turn,river}` from 200 → 50–100. Fewer infosets → better
convergence per bucket, but lower resolution ceiling. Owner rejected: wastes the
preflop investment / lowers the ceiling. Listed for completeness.

## D2 — coarser postflop ACTION abstraction  ← preferred scale knob

Shrinks the 207M infoset count *multiplicatively* without touching card
resolution, by reducing branching. Knobs in `config/default.json`:

```json
"abstraction": {
  "raise_fractions": [1.0],          // add/remove bet sizes (more = larger tree)
  "max_raises_per_street": 2         // lower to 1 to cut re-raise branches
}
```

Example coarser variant (fewer postflop lines): keep preflop opens as-is but cap
`max_raises_per_street` at 1 for a smaller tree, or keep a single pot-sized bet.
Because betting states are card-independent, `actions.enumerate_state_counts` /
`sizing_report` will show the new infoset total immediately — run that first to
size the change before committing a run.

**Caveat:** coarser action abstraction means more off-tree bets at deployment →
leans harder on `pseudo_harmonic` translation (already in `actions.py`). Fine for
a seed the NN refines; note it in DEVIATIONS.md if you ship it.

Risk — Low (mechanical), but requires a fresh run.

## D3 — depth-limited solving + leaf value  (sketch, Med risk)

Cap the tree (e.g. stop expanding at the turn) and estimate the leaf value with a
value net or a quick rollout. Dramatically shrinks the tree; standard in modern
solvers. This is really a **spiral-phase** tool (it needs the value net), not a
seed-building change — parked here for when the NN exists.

## D4 — decoupled / nested subgame solving  (sketch, Med risk)

Freeze the trunk, solve postflop subgames on demand with trunk-reconstructed
ranges + NN leaf values (Libratus-style). This is the **tabular half of the
asymmetric spiral** (see improvementProposals.md §Spiral) and the only place
"NN → tabular" earns its keep. Build after self-play, not before.
