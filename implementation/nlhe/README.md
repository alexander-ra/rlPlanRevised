# NLHE 6-Max Blueprint 🟢

**🟢 AI-GENERATED** (per PLAN.md §4.4 ownership tags). A side project outside the
numbered study steps: train the strongest reusable No-Limit Hold'em base
strategy achievable on this machine in ~300–400 GPU/CPU hours, as a future
anchor for thesis work (πKL safe exploitation, opponent modeling). It is a
**blueprint, not a refined agent** — no real-time search (a possible later
phase), coarse card abstraction, competent-but-not-superhuman.

Full design and rationale: `../../` plan file
`please-review-the-deliverables-studyplan-*.md`. Deviations from it are logged
in [DEVIATIONS.md](DEVIATIONS.md).

## Approach

Pluribus-recipe: **linear Monte-Carlo CFR** with regret pruning on a
**card + action abstraction**, run on CPU (numba, all cores); the finished
average strategy is **distilled to a policy network** on the GPU (the
thesis-reusable artifact). The GPU also computes the card abstraction up front.

Config lives in [config/default.json](config/default.json) — nothing is
hardcoded.

## Status (2026-07-03)

Foundation layer complete and validated:

| Component | File | Gate | Status |
|-----------|------|------|--------|
| Card encoding + 7-card rank table | `src/cards.py` | G2 | ✅ table built (255 MB), matches phevaluator on 200k random hands |
| Suit-isomorphism indexer | `src/indexer.py` | G3 | ✅ preflop 169 / flop 1,286,792 / turn 13,960,050 exact; river deferred (memory-safe builder ready) |
| Reference NLHE engine | `src/engine_ref.py` | G1 | ✅ side-pot / split-pot / min-raise unit tests |
| Numba NLHE engine | `src/engine_nb.py` | G1 | ✅ agrees with reference on 10k random playouts (all buttons) |
| Action abstraction + infoset hash + sizing | `src/actions.py` | G6 | ✅ 421M infosets → ~27 GB, fits budget |

Not yet built: `buckets.py` (GPU), `mccfr.py` (core + Kuhn/Leduc gates G4/G5),
`checkpoint.py`, `daemon.py`, dashboard, `evalmatch.py`, `distill.py`.

## G6 sizing (the feasibility answer)

Final abstraction: **fold / check-call / pot-raise / all-in, max 2 raises per
street**, card buckets 169 / 400 / 400 / 400 (pre/flop/turn/river).

```
betting states/street : {preflop: 42232, flop: 272305, turn: 379757, river: 382969}
infosets              : ~421,000,000
infoset table         : open-addressed hash, 671,088,640 slots x 40 B = 26.8 GB
                        (load factor ~0.63)
```

Comfortably inside the 30 GB table budget on 62 GB RAM. (The plan's original
5000-bucket menu would have been ~11 billion infosets ≈ 600 GB — infeasible;
Gate G6 caught this and the abstraction was narrowed. See DEVIATIONS.md.)

## Build / run

```bash
# from repo root, with .venv active
python implementation/nlhe/scripts/build_tables.py --rank      # 7-card rank table (~2.5 min)
python implementation/nlhe/scripts/build_tables.py --indexer   # preflop/flop/turn keys
python implementation/nlhe/scripts/sizing.py                   # G6 report
python -m pytest implementation/nlhe/tests/ -q                 # G1, G2, engine correctness
```

Artifacts (gitignored, regenerable) land in `artifacts/`; training output will
go in `runs/`.

## Monitoring the run

```bash
# LAN access (from any device on the same network):
python implementation/nlhe/scripts/serve_dashboard.py runs/<run_id>
#   -> prints http://<machine-lan-ip>:8777

# Remote access from OUTSIDE a closed network (e.g. university PC -> phone):
python implementation/nlhe/scripts/serve_dashboard.py runs/<run_id> --tunnel
#   -> also prints a public https://<random>.trycloudflare.com URL
```

The `--tunnel` flag launches a Cloudflare quick tunnel (outbound-only, so it
works from closed networks with no inbound ports) via `tools/cloudflared.exe`.
The URL is unguessable but world-reachable; the page is read-only telemetry with
no controls, but treat the URL as semi-private. Tested working end-to-end.

The dashboard shows a status badge (TRAINING/STALLED), iteration, iters/sec,
last-checkpoint age (red if stale >4h), live bb/100 vs each baseline, and a
preflop strategy heatmap. It polls static JSON files, so it adds ~no load.

## Card / state conventions

- Card int `0..51 = rank*4 + suit`, rank `0..12 = 2..A`, suit `0..3 = cdhs`
  (identical to phevaluator's int convention — verified).
- Rank table stores `7462 - phevaluator_rank`, so **larger = stronger**.
- Engine seats `0..5`, button fixed at seat 0 for training (seats rotated
  externally for evaluation); SB=1, BB=2.
