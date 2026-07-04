# C — more learning per visit (algorithmic)

## C3 — CFR+ regret flooring  ★ cheap, low risk

Vanilla regret-matching lets regrets go arbitrarily negative, so an action that
was bad early takes many iterations to "come back" once the context changes.
**CFR+** floors regrets at 0 after each update, which empirically converges
faster and is what most modern solvers use.

### Diff — `src/mccfr.py` : `traverse`

Current update (traverser branch):

```python
        for a in range(n):
            regret[slot, a] += util[a] - node
        return node
```

Proposed (CFR+ floor):

```python
        for a in range(n):
            r = regret[slot, a] + (util[a] - node)
            regret[slot, a] = r if r > 0.0 else 0.0   # CFR+ : no negative regret
        return node
```

### Interactions to handle (important)

1. **Pruning.** The current regret pruning tests `regret[slot, a] < prune_below`
   with `prune_below ≈ -3e8`. Under CFR+ regrets never go negative, so that
   prune path **never fires**. Either:
   - drop regret-pruning when CFR+ is on (simplest), or
   - switch to a CFR+-appropriate prune (skip actions whose regret has been 0 for
     a long run). Recommend dropping it initially and re-measuring throughput.
2. **Discounting.** `discount()` (LCFR) scales regret + stratsum by `factor`.
   CFR+ typically pairs with *linear averaging* (weight stratsum by iteration `t`)
   rather than geometric discounting. Two clean options:
   - **Keep DCFR** (leave `discount()` as-is) and only add the floor — a valid
     hybrid, low risk. Start here.
   - **Full CFR+**: remove regret discounting, weight the stratsum contribution
     by `t`. Bigger change; do it only if the hybrid underperforms.

### Risk — Low
One-line math change with two well-understood interactions (pruning, discount).
Reversible. Validate on the Kuhn/Leduc tests (`tests/test_kuhn_cfr.py`) first —
they share `regret_matching` / the update, so convergence should improve or hold.

---

## C1 — vector / public-chance-sampling CFR  (sketch, Med–High risk)

Carry a vector over all buckets at each public state; showdown utilities become a
matmul. Coverage per game scales with bucket count instead of ×1, and it's the
only variant with a GPU-shaped inner loop. **But** 200-wide vectors are small for
a 5090 — needs heavy batching across subgames to saturate it. Large rewrite
(public-tree representation, dense per-node arrays instead of the hash table).
Better value in the self-play/spiral phase than for building the seed → deferred.

## C2 — simultaneous multi-traverser  (sketch, Low–Med risk)

Update all six seats' regrets per game instead of rotating one (~6× tree work,
~6× signal). Can be a net coverage win. Moderate change to `traverse` (branch all
seats) — try only if B1 doesn't lift coverage enough.

## C4 — Deep CFR / DREAM  (separate track, High risk)

NN function approximator: generalizes across infosets (no coverage gap), output
IS the NN seed (no distill step), uses the 5090. "May be a lot better or worse."
**Do not fold into the committed 400h.** Run a short prototype and bake it off
against the MCCFR blueprint with the existing eval (`evalmatch.py` /
`scripts/run_eval.py`); adopt only if it's clearly better AND stable. See
improvementProposals.md §C4 for the gate.
