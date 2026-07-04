# B — flop-start (rejection) sampling + soft-freeze mix

**Problem:** ~60–80% of deals fold out before the flop, so most of the 400h
re-trains the already-converged preflop trunk while postflop starves.

**Fix:**
- **B1 flop-start (rejection):** play preflop with the current strategy (all
  seats sample, no updates), discard hands that end preflop, run the normal
  learning traversal from the flop. Bias-free for the postflop subgame given the
  current trunk (ranges entering the flop are self-consistent) → **no importance
  weights**. Preflop sampling is ~microseconds, so discarded deals are ~free.
- **B3 soft-freeze:** keep a `full_game_fraction` (~0.25) of ordinary full-game
  iters so the preflop trunk keeps adapting as postflop tightens. Hard-freezing
  preflop now would lock in distortions (it converged vs random postflop).

Implementation: `mccfr_flopstart.py` (copy into `../../src/`). It reuses
`mccfr.traverse` and primitives unchanged — only the game *start* differs.

## Wiring — daemon train loop

Replace the training call:

```python
# before
mccfr.run_batch(batch, gi, rules_arr, slot_key, regret, stratsum,
                *art_tuple, prune_below, prune_on)
# after
import mccfr_flopstart
mccfr_flopstart.run_batch_mixed(batch, gi, cfg["mccfr"]["full_game_fraction"],
                rules_arr, slot_key, regret, stratsum,
                *art_tuple, prune_below, prune_on)
```

(`benchmark()` in `scripts/train.py` and the daemon both call `run_batch`; only
the daemon's steady-state loop needs switching — keep `run_batch` for the G5
throughput benchmark so numbers stay comparable.)

## Config (add to `config/default.json` -> `"mccfr"`)

```json
"full_game_fraction": 0.25,
"_full_game_fraction_note": "B3 soft-freeze: fraction of iters that are ordinary full-game (preflop keeps adapting). Rest are B1 flop-start."
```

## Verify

Run `scripts/measure_reach.py` (proposal E1) before and after: expect the
per-street coverage for flop/turn/river to climb substantially, and the
"sampled decision points by street" to shift away from preflop.

## Risk — Medium

- **Correctness:** B1 is unbiased for the postflop subgame **given the current
  trunk**. The only subtlety is that the trunk keeps moving; the B3 full-game
  fraction is what keeps trunk and postflop consistent. Don't set
  `full_game_fraction` to 0.
- **Coverage of preflop-terminal spots:** flop-start never trains all-preflop
  lines; B3's full-game share covers them. 0.25 is a safe start.
- **Throughput:** `_advance_to_flop` adds a cheap sampled preflop rollout per
  Type-B iter; measure that the net postflop visits/s still rises.

## Not implemented here (sketch only)

- **B2 tempered sampling** (`q ∝ p^α`): bias the traverser's hole-card class
  toward uniform-over-169 and multiply the traversal's returned utility by
  `p/q`. Needs a per-class sampling table + the correction applied at the root.
  Med risk (variance); add after B1 is verified, start α≈0.5.
- **B4 stratified-by-coverage dealing:** maintain per-bucket visit counts
  (proposal E2) and bias the flop deal toward cold buckets, with `p/q`
  correction. Needs a live counter array.
- **B5 prioritized subgame replay:** queue under-visited public states and start
  there with trunk-reconstructed ranges. Larger; belongs with the spiral phase.
