# A — sensible policy for untrained / thin infosets  ★ TOP QUICK WIN

**Problem:** ~87% of postflop infosets are never visited, and both the eval and
the distill path fall back to **uniform random** there. For a self-play seed that
is the worst case — self-play would start cold exactly where we have no data.

**Fix (output-side only, zero training-math risk):**
- **A1 `heuristic_default`** — pot-odds / bucket-equity rule. Always available.
- **A2 `nearest_bucket_strategy`** — borrow the closest *visited* bucket's average
  strategy at the same public state (by mean-equity distance).
- **A3 warm-start** — optionally seed `stratsum` with A1 so early play is sane
  (see note at bottom).

Both live in `default_policy.py` (copy into `../../src/`). Ordering to apply:
try **A2** (uses real learned data when a neighbour exists) → fall back to **A1**.

---

## Wiring 1 — `src/evalmatch.py` : `_blueprint_strategy`

The blueprint's eval behaviour should use the defaults instead of uniform. This
also needs the per-street mean-equity arrays (`eqs`) already loaded in eval, so
pass them through.

Current:

```python
    slot = mccfr.table_find(slot_key, h)
    if slot < 0:
        for a in range(n):
            out[a] = 1.0 / n
        return
    tot = 0.0
    for a in range(n):
        v = stratsum[slot, a]
        out[a] = v if v > 0 else 0.0
        tot += out[a]
    if tot <= 0:
        for a in range(n):
            out[a] = 1.0 / n
    else:
        for a in range(n):
            out[a] /= tot
```

Proposed (add `n_buckets`, `eq_street`, `my_eq` args from the caller; both
fallbacks route through A2 → A1):

```python
    slot = mccfr.table_find(slot_key, h)
    if slot < 0 or _rowsum(stratsum, slot, n) <= 0.0:
        # A2 first (learned neighbour), else A1 heuristic
        if not default_policy.nearest_bucket_strategy(
                st, n_buckets, my_eq, eq_street, slot_key, stratsum, n, out):
            default_policy.heuristic_default(st, p, n, ok, my_eq, out)
        return
    tot = 0.0
    for a in range(n):
        v = stratsum[slot, a]
        out[a] = v if v > 0 else 0.0
        tot += out[a]
    for a in range(n):
        out[a] /= tot
```

Notes:
- `_choose` already computes `eq` for the TAG bot via `_seat_equity`; reuse the
  same per-street mean-equity arrays as `eq_street`, and `my_eq = eq_street[bucket]`.
- `ok` is already available in `_choose`; thread it into `_blueprint_strategy`.
- `_rowsum` is a 3-line njit helper (sum of positive stratsum on the row).

## Wiring 2 — `src/distill.py` : `collect_dataset`

Today untrained states are **skipped** (`slot >= 0 and stratsum[slot].sum() > 0`),
so the NN never learns the cold 87% and interpolates arbitrarily there. To make
the seed sensible everywhere, emit a **default target** for a fraction of
untrained visited states:

```python
            slot = mccfr.table_find(slot_key, h)
            trained = slot >= 0 and stratsum[slot].sum() > 0
            if trained:
                row = stratsum[slot]; tot = row[:n][row[:n] > 0].sum()
                target_from_table = True
            elif rng.random() < cfg["distill"].get("default_label_frac", 0.3):
                # A1/A2 label so the NN learns "reasonable", not random, here
                out = np.zeros(8)
                my_eq = eqs[street][bucket] if street else eqs[0][bucket]
                if not default_policy.nearest_bucket_strategy(
                        st, n_buckets[street], my_eq, eqs[street],
                        slot_key, stratsum, n, out):
                    default_policy.heuristic_default(st, p, n, ok, my_eq, out)
                row = out; tot = out[:n].sum(); target_from_table = False
            else:
                target_from_table = None  # skip
            if target_from_table is not None and tot > 0:
                X[got] = _features(...); ... fill Y/M ...; got += 1
```

Keep the default-labelled fraction modest (~0.3) so real CFR data dominates
where it exists; the defaults only cover the void.

## A3 — heuristic warm-start (optional, separate)

If you also want *training* to start from a sane prior (not just output), after
`build_table` seed a small `stratsum` mass from `heuristic_default` for every
infoset. Cost: one pass over the table. Effect: early strategy is sensible and
CFR refines from there instead of uniform. Low risk, but do it as its own commit
so its effect on convergence is measurable in isolation.

## Risk

**Low.** No change to `regret`, `traverse`, or the CFR update — only the strategy
*read out* for eval and the *labels* handed to distillation. Worst case a
mediocre heuristic, still strictly better than uniform-random.
