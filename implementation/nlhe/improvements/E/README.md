# E — instrumentation (decide from numbers)

## E1 — flop-reach + coverage scan  (already written)

`scripts/measure_reach.py` already exists (added with the trainer). It runs a
strategy-sampled playout study (flop-reach %, decision points per street) and a
full per-street coverage scan of the table. **This is the step the last session
stalled on** (session limit). It reads a checkpoint read-only, safe alongside a
live run:

```
python implementation/nlhe/scripts/measure_reach.py <run_dir>
```

Run it once now to size B/B2/B4 by evidence, and again after B1 to confirm the
coverage jump. (Needs a checkpoint — not present in a fresh clone.)

## E3 — readable eval  ★ low risk

At 2,000 decks the eval CI is ±155–184 bb/100 — wider than the improvements
between evals, so postflop progress is buried in noise. Bump decks ~10× to shrink
CI ~3.5× (to ±~50). It's an isolated subprocess, so slower eval doesn't slow
training.

### Diff — `config/default.json` : `"eval"`

Current:

```json
  "eval": {
    "interval_hours": 0.25,
    "decks": 10000,
    "pilot_decks": 2000,
    "seat_rotations": 6,
    "threads": 2,
    "baselines": ["random", "calling_station", "tag"]
  },
```

Proposed (raise the pilot/steady deck counts; optionally lengthen interval so the
bigger eval doesn't run too often):

```json
  "eval": {
    "interval_hours": 0.5,
    "decks": 25000,
    "pilot_decks": 25000,
    "seat_rotations": 6,
    "threads": 2,
    "baselines": ["random", "calling_station", "tag"]
  },
```

Tune `decks` to taste; CI scales ~1/sqrt(decks). If eval wall-time grows too
much, raise `threads` (it's an isolated subprocess) rather than dropping decks.

## E2 — per-bucket visit histograms  (sketch)

Add a per-infoset (or per-bucket) visit counter so B4 (stratified dealing) and
B5 (prioritized replay) have targeting data. Cheapest form: a `uint32` array
parallel to the table, incremented in `traverse` at the traverser node. Adds a
little memory + a write; measure throughput impact before keeping it on always.

Risk — Low (E1/E3 config + read-only; E2 is a small additive counter).
