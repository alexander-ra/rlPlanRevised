# Benchmark Protocol → Overnight Pilot (executor handoff)

State as of 2026-07-03 (post-fix): the duplicate-slot race is FIXED via table
pre-population (verified: 10M multithreaded iters → 0 new slots, 0 duplicates,
249,772 iters/sec at 100 buckets). All 14 tests pass. Bucket artifact sets for
100/200/400 exist (`artifacts/bucket_<street>_<N>.npy`, all occupancy-clean).
Old runs are invalid (raced tables) and deleted.

## Step 1 — three 15-minute benchmark runs (sequential, NOT parallel)

From repo root, venv python:

```
.venv/Scripts/python.exe implementation/nlhe/scripts/train.py --benchmark --buckets 100 --seconds 900
.venv/Scripts/python.exe implementation/nlhe/scripts/train.py --benchmark --buckets 200 --seconds 900
.venv/Scripts/python.exe implementation/nlhe/scripts/train.py --benchmark --buckets 400 --seconds 900
```

Each prints: iters/sec, infoset count, table GB, `NEW slots created (must be 0)`,
and `iterations/infoset` over a 400h budget. **If NEW slots ≠ 0 for any run,
STOP — the race fix regressed; do not start the pilot.**

Record the three `iters/sec` and `iterations/infoset (400h)` numbers.

## Step 2 — decision rule for bucket count

Let `V(N) = iters_per_sec(N) / infosets(N)` (proportional to per-infoset visits).
Infosets: 100 → 110.6M, 200 → 214.5M(≈), 400 → 421.1M (the benchmark prints
exact values).

**Pick the LARGEST N with V(N) ≥ 0.40 × V(100), requiring also
iterations/infoset(400h) ≥ 300.** If none qualify beyond 100, pick 100.
Rationale: bigger N buys card resolution but dilutes visits; below ~300
iterations/infoset the blueprint won't converge acceptably.

## Step 3 — set the chosen size in config (do NOT rely on --buckets for the pilot)

Edit `implementation/nlhe/config/default.json` → `"buckets"`: set `flop`,
`turn`, `river` to the chosen N. (Eval reads the config independently, so the
config must match the run.)

## Step 4 — launch the overnight pilot + dashboard (detached)

PowerShell:

```powershell
$root="C:\Users\UserNIK\projects\rlPlanRevised"; $py="$root\.venv\Scripts\python.exe"
$runid="20260704_6max_pilot"; $rundir="$root\implementation\nlhe\runs\$runid"
New-Item -ItemType Directory -Force $rundir | Out-Null
Start-Process -FilePath $py -ArgumentList "`"$root\implementation\nlhe\scripts\train.py`" --run $runid --pilot-hours 24" -WorkingDirectory $root -RedirectStandardOutput "$rundir\train_out.log" -RedirectStandardError "$rundir\train_err.log" -WindowStyle Hidden
Start-Sleep 3
Start-Process -FilePath $py -ArgumentList "`"$root\implementation\nlhe\scripts\serve_dashboard.py`" `"$rundir`" --tunnel" -WorkingDirectory $root -RedirectStandardOutput "$rundir\dash_out.log" -RedirectStandardError "$rundir\dash_err.log" -WindowStyle Hidden
```

Then grep the public URL and give it to the user:
`grep -oE "https://[-a-z0-9.]+\.trycloudflare\.com" $rundir/dash_out.log | head -1`

## Step 5 — health checks after launch (all must hold)

1. `status.json` appears within ~3 min; `iters_per_sec` within 2× of the
   benchmark number for the chosen N.
2. `infosets` in status.json equals the prepopulated count and NEVER grows.
3. First checkpoint lands ≤ 20 min (15-min cadence + write time).
4. First eval lands ≤ 25 min and appears in `eval/index.json`; expect NEGATIVE
   bb/100 early (untrained). It should trend upward over hours.
5. Tunnel URL serves `status.json` (curl → 200).

## Success criteria for the pilot itself (Gate G7, check in the morning)

- bb/100 vs random and vs calling_station clearly positive with CI clear of 0.
- checkpoint age on dashboard never exceeded ~20 min.
- iters/sec roughly stable after the first hour (±30%).
- Then: the long run resumes THE SAME run id (nothing is lost):
  `train.py --run 20260704_6max_pilot` (no --pilot-hours).

## Known-good reference numbers (for sanity)

- prepopulate: 110.6M infosets / 4.4s (100 buckets); table 8.0 GB, load 0.55.
- 100-bucket quick benchmark (40s window): ~250k iters/sec.
- Kuhn G4 exploitability < 0.01; engine cross-val G1 zero mismatches; 14 tests.
