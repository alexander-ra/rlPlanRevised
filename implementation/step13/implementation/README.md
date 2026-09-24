# Step 13 — Implementation: behavioural analysis on real hand histories

Everything here was **run** (September 2026) on real data: 2.03 M iPoker hands from July 2009 and
the 10,000 released Pluribus hands (PHH dataset; see `config.py` and `../EXECUTION_NOTES.md` for
how the data was fetched). Results are in `results/*.json`, logs in `logs/`, figures in `plots/`
(drawn from the JSON only).

## Module map (raw step 13 deliverable → file)

| Deliverable (raw step, Phase 4) | File | Output |
|---|---|---|
| Hand-history parser (Day 1) | `phh_parser.py` | `HandRec` per hand |
| Data validator + injected errors (Day 1, Validation) | `validator.py` | `results/validator.json` |
| Pipeline raw → parsed → stored (Day 1) | `build_dataset.py`, `features.py` | cache in `D:/datasets/step13_cache`, `results/build_*.json` |
| State encoding for real hold'em (Day 1–2) | `bc.py: encode()` | 42 public features (+17 card features on Pluribus) |
| Player statistics, thresholds, VPIP×PFR, gap (Day 2) | `player_stats.py` | `results/player_stats.json` |
| Behavioural cloning (Day 2) | `bc.py` | `results/bc.json`, `results/bc_PLURIBUS.json` |
| player2vec embedding (Day 3) | `p2v.py` | `results/player2vec.json` (+ `player2vec_4epochs.json`, the first run) |
| Style clustering, temporal stability, Bayesian typing (Day 4, Math Flag) | `clustering.py` | `results/clustering.json` |
| Collusion detection with injected colluders (Day 5) | `collusion.py` | `results/collusion.json`, `results/collusion_mw.json` |
| Bot detection (Phase 1 goal; Math Flag on loss) | `botdetect.py` | `results/botdetect.json` |
| Derived numbers quoted in the chapter | `derived.py` | `results/derived.json` |
| Figures | `plotting.py` | `plots/*.png` |

Not built: the Decision Transformer on real data (Day 6, optional in the brief) — see the notes.

## How to reproduce (order matters; from this folder, venv active)

```bash
python build_dataset.py --source IPN100      # 2-3 min, 14 processes
python build_dataset.py --source PLURIBUS    # seconds
python validator.py --n 2000                 # ~6 min
python player_stats.py                       # ~4 min
python bc.py                                 # ~2 min (GPU)
python bc.py --source PLURIBUS --epochs 40 --bs 512
python p2v.py --epochs 15                    # ~16 min (GPU), writes embeddings + models to the cache
python clustering.py                         # ~6 min
python botdetect.py                          # ~3 min
python collusion.py                          # ~8 min
python collusion.py --pairs mw               # ~9 min
python derived.py && python plotting.py
```

Seeds: every training or sampling step runs seeds 0, 1, 2 (`config.SEEDS`); the test sample of
BC decisions is fixed (seed 12345).

## Validation targets (raw step) vs measured

| Target | Measured | Verdict |
|---|---|---|
| Parse 100 % of well-formed hands | 99.77 % of IPN hands parse; the 0.23 % rejected are truncated (e.g. the big blind never acts); Pluribus 100 % | met (rejects are malformed) |
| Validator catches injected errors | own validator 100 % on 10 error types; pokerkit misses duplicates (default) and truncation | met |
| Encoding: no NaN/Inf, fixed dimension | 42 features on every table size 2–10 | met |
| BC accuracy > 55 % | 72.0 % — but the majority baseline is 70.2 % | met, uninformative |
| BC accuracy TAG > LAG > Fish | raw accuracy yes; above the majority baseline the order reverses | not as intended |
| Embedding clusters match VPIP×PFR; intra > inter similarity | 15-NN recovers the quadrant 90 %; cosine 0.87 within vs 0.75 between | met |
| 4 clusters = recognisable archetypes | 2 TAG-like clusters, 1 LAG, 1 loose-passive; silhouette ≤ 0.16 | not met |
| Temporal stability > 70 % | 73.6 % (random split 78.2 %) | met, mostly noise-limited |
| Collusion: 100 % detected at < 5 % FPR | soft play yes from q = 0.5; dumping only at q = 1 | partly |

## Likely to break

- **Paths.** `STEP13_DATA` / `STEP13_CACHE` environment variables override `D:/datasets/…`.
- **Memory.** The IPN cache is ~3.6 GB on disk; `p2v.py` and `collusion.py` hold the full seat and
  decision arrays (~10 GB RAM peak).
- **pokerkit and floats.** Build `HandHistory` objects through `validator._pk_fields()`; tomllib
  floats mixed with pokerkit's Decimals raise TypeError.
- **Heads-up blinds** are reversed in PHH/pokerkit; **negative blinds** are posts. Both are handled
  in `phh_parser.py`; any new parser must do the same.

## Key takeaways for the final summary

- A careful parser matters more than any model: three data conventions (reversed heads-up blinds,
  negative posts, hidden all-ins) each changed results before they were handled.
- Every headline number needs its baseline: 72 % action accuracy is +1.8 points over "always the
  most common action"; 73.6 % temporal stability is 4.6 points under a random split.
- The embedding beats the hand-crafted statistics at recognising a player on unseen days
  (15.6 % vs 7.1 % top-1 among 834, chance 0.12 %).
- Collusion signals work only when each player is compared with their own behaviour; Chapter 11's
  raw help/harm counts point the wrong way on poker data.
- Generic anomaly detection does not find Pluribus; its bet-size menu and its randomisation do.
