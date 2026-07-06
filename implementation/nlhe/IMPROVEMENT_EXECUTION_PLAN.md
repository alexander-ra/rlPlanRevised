# NLHE Trainer Improvements — Gated Execution Plan

**Audience:** a junior/lesser-model executor. Follow phases in order. Every change is
config-gated and default-off, adopted one at a time with numeric gates and a rollback.
When a gate fails or an abort-if fires: stop, write the report, wait for the owner.

## Context

Live run `20260703_6max_200_v1` (started 2026-07-03): external-sampling MCCFR, 6-max 100bb,
~8B iters at ~145k it/s, 12/16 cores, 214,143,408 infosets (169 preflop / 200×3 postflop buckets),
15.6 GB table, A/B checkpoints every 15 min, eval subprocess every 15 min. Preflop is converged
and sane; **~87% of postflop infosets are never visited** → uniform fallback = near-random postflop
(latest eval: −498 bb/100 vs TAG). Eval at 2k decks has ±150–180 bb/100 CIs — noise hides everything.

The blueprint is a **seed for a later self-play (NN) phase** — "sensible everywhere + low
variance" beats "deep anywhere". Proposals A–E live in `implementation/nlhe/improvements/`
(A and B ship ready code; nothing is wired in). Machine: 16 logical cores, 61.7 GB RAM,
RTX 5090 (idle during CFR — expected), ~390 GB free disk.

**Owner decisions (2026-07-04):**
1. Pause windows allowed: graceful stop ≤2h, then resume (daemon writes a final checkpoint on Ctrl+C; nothing is lost).
2. Auto-adopt **output-side only** (eval decks fix, A1/A2 defaults). B1/B3 and C3: deliver report, wait for go/no-go.
3. GPU work this round: **C4 Deep CFR bake-off POC only** (report-only). Distill cadence + self-play rehearsal deferred.
4. Live table must survive: only resume-compatible changes on the live run. D-bucket (fresh table) = discussion package only.

**Conventions:** `LIVE` = `c:\Users\UserNIK\projects\rlPlanRevised`, `NL` = `implementation\nlhe`,
`RUN` = `LIVE\NL\runs\20260703_6max_200_v1`, `DEV` = worktree `c:\Users\UserNIK\projects\rlPlanRevised-dev`,
`$PY` = the interpreter the live daemon uses (record it in Phase 0; expect `LIVE\.venv`). Use the same
`$PY` from both trees (each script inserts its own `src/` on sys.path, so DEV scripts run DEV code).

---

## Hard guardrails (memorize)

1. **Never modify `LIVE` while the daemon runs** — the eval subprocess re-imports `src/` and re-reads
   `config/default.json` every cycle. All dev + POC runs happen in `DEV`. LIVE changes only inside a
   stop window via `git merge` + config flip. **Single pre-authorized exception:** Phase 0 step 3
   (one config value, exact diff given).
2. Never edit/delete/rename anything in `NL\artifacts\` (DEV junctions into it). Treat `RUN` as
   read-only except creating `pre_<phase>_backup\` dirs.
3. **Tripwire:** `RUN\status.json` → `infosets` must equal **214143408** at every check. Any other
   value = an insert happened (tree mismatch/corruption) → abort + rollback immediately.
4. POC run-ids live under `DEV\NL\runs\` and never reference the live run id.
5. `measure_reach.py` always runs **raw** (uniform fallback) — it must show true coverage, never A-masked.
6. One improvement per stop window; separate adoptions by ≥2 eval cycles so deltas stay attributable.
7. Test battery around every code change: `$PY -m pytest NL\tests -x -q` (+ new tests) and
   `$PY NL\scripts\train.py --benchmark --seconds 30` with the relevant config. Live-config benchmark
   numbers are only *gated* inside stop windows (quiet machine); elsewhere record-only.

**Stop → apply → resume procedure** (every adoption):
1. Confirm no eval in flight (`Get-Process python` — only the daemon + helpers; evals finish ≤5 min).
2. Ctrl+C in the daemon console (ask owner if you don't own that console). **Never `taskkill /F`.**
3. Wait for `stopping; final checkpoint...` + exit; verify newest `RUN\checkpoints\<A|B>\DONE` exists
   and `meta.json.iteration` ≥ last `status.json.iteration`. Log the iteration in `improvements/exp/LEDGER.md`.
4. If the change touches training math (Phase 3/4): copy that checkpoint dir to `RUN\pre_<phase>_backup\`
   (~15.6 GB — check ≥30 GB free first; verify sizes match). A/B slots rotate every 15 min — without
   this copy the rollback point is destroyed within 30 min of restart.
5. Apply: `git -C LIVE merge <phase tag from DEV>` → run test battery (benchmark must print
   `PASS` and `NEW slots created during run (must be 0): 0`).
6. Flip this phase's config key(s) only.
7. Restart: `$PY NL\scripts\train.py --run 20260703_6max_200_v1`. Within 15 min verify: console
   `resumed from ... at iteration <N>` matches step 3, `status.json` updating, tripwire holds,
   iters/s above the phase floor. Watch the first eval complete in `RUN\eval\eval.log`.

**Abort-if (any time):** tripwire fires → stop+rollback · `status.json` stale >5 min → daemon hung,
collect console output, involve owner (no hard kill) · iters/s below phase floor for 15 min → stop
window + revert last change · `Traceback` in `eval.log` → training may continue; fix eval in DEV only ·
free RAM <8 GB → don't launch measure_reach/eval jobs · `RUN` >130 GB → delete oldest *passed*-phase
backup (only after its gate passed +24h).

---

## Phase 0 — Baseline + readable eval (day 1; no stop window)

1. Record `$PY` (owner confirms daemon interpreter), snapshot `RUN\status.json`, last 20 lines of
   `RUN\eval\eval.log`, `git -C LIVE log -1 --format=%H` → start `improvements/exp/LEDGER.md`.
2. Baseline coverage (read-only, safe alongside):
   `$PY NL\scripts\measure_reach.py NL\runs\20260703_6max_200_v1 | Tee-Object baseline_reach.txt`
   **Gate G0.1:** completes <30 min. Record flop-reach %, per-street decision split, per-street
   `strat>1` coverage — every later gate references these numbers.
3. **E3, pre-authorized zero-stop edit:** in `LIVE\NL\config\default.json` set `"pilot_decks": 25000`
   (this is the key `run_eval.py` actually reads; `eval.decks`/`threads`/`seat_rotations` are dead keys —
   cleanup happens in stop window #1). Effect: next eval ~4 min instead of ~15 s (measured 4–6 s/baseline
   at 2k decks), CI shrinks ~3.5×. Interval stays 0.25h (4 min ≪ 15 min; daemon skips overlaps anyway).
   **Gate G0.2:** next eval completes ≤10 min with CI(tag) and CI(cs) ≤ ±60 bb/100 (expect ~±45).
4. Record the 25k-deck baseline eval row (random/CS/TAG ±CI) in the ledger — the "before" for everything.
5. Worktree: `git -C LIVE worktree add ..\rlPlanRevised-dev -b improvements-dev` then
   `cmd /c mklink /J DEV\NL\artifacts LIVE\NL\artifacts` (artifacts are gitignored, 4.5 GB).
   In DEV: full pytest green (first run pays numba JIT — allow ~10 min).

## Phase 1 — A1+A2 output-side defaults (days 1–3; auto-adopt approved)

1. In DEV: copy `improvements/A/default_policy.py` → `NL\src\`. New `tests/test_default_policy.py`:
   rows sum to 1 (±1e-6), no negatives/NaN over a 10k-state fuzz; zero fold mass when `call_amt == 0`;
   `nearest_bucket_strategy` returns False on an empty table, normalized row with one populated
   neighbor. **Gate G1.1:** pytest green.
2. Wire `evalmatch._blueprint_strategy` per `A/README.md` (A2 nearest-visited-bucket → A1 pot-odds
   heuristic), config-gated: thread a `use_defaults` int (from `eval.use_default_policy`, default
   false) through `duplicate_match → play_hand → _choose → _blueprint_strategy`. Off-path byte-identical.
3. Build `improvements/exp/eval_ckpt.py` (harness piece, spec below) and run the **paired offline A/B**
   on the same live checkpoint (read from DEV; pass the newer of `RUN\checkpoints\A|B` explicitly —
   the older slot gets overwritten first): 25k decks, same seed (evals are deck-paired by design,
   fixed seed 123), defaults off vs on.
   **Gate G1.2:** TAG(on) − TAG(off) ≥ **+100 bb/100**; RANDOM and CS each not worse than −(CI_on+CI_off);
   eval wall-time(on) ≤ 3× off (A2 does O(buckets) probes per cold decision).
4. **Stop window #1** (bundled, one restart): merge; set `eval.use_default_policy: true`;
   `run_eval.py` → use `eval.decks` (25000) and delete the dead keys from config; add the **STOP-file
   sentinel** to the daemon loop (if `RUN\STOP` exists → clean break; delete file on start) — 5-line
   ops patch so future stops are scriptable; *(only if owner pre-approves)* `mccfr.n_workers` 12→13.
   **Gate G1.3:** next two live evals: TAG ≥ offline TAG(on) − 2×CI, no tracebacks; tripwire holds;
   iters/s ≥ 130k. **Gate G1.4** (only if workers=13): 1h mean iters/s ≥ 152k, else revert to 12 next window.
   Rollback: flip `use_default_policy: false` (config-only).
5. A3 warm-start: **not** for the live table — small-game experiment only (Phase 6 candidate for future fresh runs).

## Phase 2 — Config plumbing + small-game POC harness (days 2–4; DEV only)

*The workbench every later phase uses. Nothing here touches LIVE.*

1. **Betting-tree cache keyed by rules** (critical — currently `betting_tree_v1.npz` is loaded blindly;
   a small-game run would silently prepopulate the wrong tree, then racy-insert the real states):
   cache file `betting_tree_<sha1(rules_arr.tobytes())[:12]>.npz`, with legacy fallback for the live
   rules hash; route `measure_reach.py` through `mccfr._betting_tree` (it loads the npz directly today).
2. `--config PATH` on `train.py`, `run_eval.py`, `measure_reach.py`, `sizing.py`; daemon passes the
   path through to the eval subprocess argv; `evalmatch._rules_arr`/`load_eval_artifacts`/
   `mccfr.load_artifacts` accept a cfg dict; `measure_reach.py` gains `--threads` (default 6) and `--hands`.
   **Gate G2.1:** pytest green; DEV `--benchmark --seconds 30` (3 workers, live config) prints
   `NEW slots ...: 0` and `infosets: 214,143,408`; betting-state counts identical pre/post cache change.
3. `improvements/exp/configs/small50.json`: stack 50, buckets 169/100/100/100 (artifacts exist),
   `max_raises_per_street: 1`, `n_workers: 3`, `eval.decks: 25000`, `checkpoint.full_checkpoint_hours: 0.1`,
   and **`planned_iterations` = the POC budget** (else pruning never enables and discount warmup never
   ends — the live 5e9 value would silently invalidate every A/B), `discount_interval` scaled ~1/250.
   Run `sizing.py --config ...`. **Gate G2.2:** ≤25M infosets, ≤2 GB table (else stack 40 or buckets
   169/100/60/60 and re-size — iterate here, it's seconds).
4. Build the harness (spec below): `exp_run.py`, `eval_ckpt.py`, `compare.py`, `compare_preflop.py`.
5. Calibration: `exp_run.py --config configs\small50.json --arm baseline --minutes 30 --seed 7`.
   **Gate G2.3:** end-to-end unattended; postflop `strat>1` ≥30% at 30 min; eval CIs ≤ ±60;
   `report.json` complete. Then run a **second** identical arm to measure run-to-run spread — this
   spread calibrates the tolerance used in Phase 3/4 gates (training is non-reproducible: unseeded
   per-thread numba RNG; eval *is* reproducible: seeded).
6. Backfill the preflop-drift baseline: `compare_preflop.py` between the latest daily milestone and
   the latest checkpoint of the live run (first milestone lands ~24h after run start).

**POC protocol:** A/B arms run back-to-back, same worker count (3), same machine state (live daemon
running during both) — consistent contention beats quiet-but-unequal. Pause windows are reserved for
adoptions and clean benchmarks, not POC arms.

## Phase 3 — B1+B3 flop-start (days 4–8; the centerpiece; report-first)

1. In DEV: copy `improvements/B/mccfr_flopstart.py` → `NL\src\`; daemon switch config-gated
   (`mccfr.full_game_fraction` absent or ≥1.0 → stock `run_batch`). New `tests/test_flopstart.py`:
   stacked-deck all-fold preflop → `_advance_to_flop` returns 0; all-call line → street==1 and legal
   state; used-slot count identical before/after a 100k-iter mixed run on a prepopulated small table.
   **Gate G3.1:** pytest green, zero table growth.
2. Small-game A/B (45-min arms, seed 7, back-to-back): `small50.json` control vs
   `small50_mixed25.json` (`full_game_fraction: 0.25`). `compare.py` gates:
   - **G3.2** postflop `strat>1` count: mixed ≥ **1.8×** control;
   - **G3.3** TAG and CS eval: mixed ≥ control − (CI_m + CI_c), raw fallback (defaults off) to isolate learning;
   - **G3.4** preflop drift (weighted TV on rows with mass ≥1000): ≤ 0.10 between arm-end tables;
   - **G3.5** iters/s(mixed) ≥ 0.3× control (catastrophe floor only — mixed iters legitimately do more
     postflop work; the real metric is G3.2 at equal wall-clock).
   If G3.2 passes but G3.3 fails: try a `full_game_fraction: 0.5` arm before escalating.
3. **Deliver report to owner; wait for go.** Include recommended live `full_game_fraction`.
4. On approval — **stop window #2:** backup checkpoint (procedure step 4) → merge → set
   `full_game_fraction: 0.25` → capture the one-time quiet-machine stock benchmark (the only
   uncontended live-config number we'll ever get) → restart.
   **24h soak gates G3.6:** tripwire holds at every check; iters/s ≥ 40k floor (a drop is expected
   and fine); TAG mean of last 5 evals ≥ pre-adoption 5-eval mean − 40 bb/100; `measure_reach` at
   +24h: postflop `strat>1` ≥ baseline + 8 pp; preflop drift vs backup ≤ 3× the Phase 2 daily-drift baseline.
   Rollback: stop → remove config key → delete `checkpoints\A`+`B` → copy `pre_B_backup` → `checkpoints\A`
   → restart → verify resumed iteration equals backup iteration.

## Phase 4 — C3 CFR+ hybrid (days 8–11; report-first; can interleave with Phase 3 soak)

*New finding (V5): on the 8B-iter live table, flooring revives every buried action (−3e8 → 0 on first
touch) and permanently disarms pruning. Default recommendation is **fresh-runs-only**; the resume-probe
below is the decision-maker.*

1. Parameterize the update: `cfr_plus` int through `run_batch`/`traverse` (default 0 = stock, floor
   when 1); CFR+ mode in `tests/test_kuhn_cfr.py`. **Gate G4.1:** Kuhn exploitability <0.01 both modes.
2. Small-game fresh A/B (45-min arms): **Gate G4.2:** CFR+ TAG/CS ≥ control − combined CI; mid-run
   (15-min checkpoint) eval ≥ control's as the speed claim (report-only if noisy).
3. **Resume-probe (models the live situation):** resume the finished control table for +20% iterations
   with `cfr_plus: 1`, prune on. **Gate G4.3:** eval delta ≥ −combined CI; record iters/s + drift churn.
4. Deliver decision package: G4.2/G4.3 numbers, prune-value benchmark (stop-window live-config bench
   with prune forced off, quantifying what pruning is worth at 8B iters), and the one-way caveat
   (floored regrets are unrecoverable → rollback = table restore from backup only). CFR+ goes into
   the fresh-run defaults set (D2 restart, future runs) regardless of the live decision.

## Phase 5 — GPU: C4 Deep CFR bake-off POC (days 9–14; report-only; owner-selected)

Standalone under `improvements/exp/deepcfr/` — zero imports from it in live-run code paths.

1. **Design doc first (1 page, owner reviews before any implementation** — cheapest guard against
   the biggest engineering sink in this plan): variant (external-sampling Deep CFR w/ reservoir
   buffers, per Brown et al. 2019; single advantage net + policy net on the 33-dim features from
   `distill._features` — seat one-hot already encodes position), batching strategy (torch can't be
   called inside njit — lockstep/wave-batched traversals in Python, GPU forward per wave), expected
   throughput estimate, and an explicit **feasibility exit**: if after 1 day of implementation the
   prototype can't complete a micro-config iteration loop, stop and report "needs senior design".
2. Train on `small50.json` game (or micro variant if throughput demands), GPU for net training.
   **Gate G5.1 (smoke):** loss curves finite, VRAM stable, checkpoint save/load works.
3. **Bake-off:** equal wall-clock vs the tabular Phase 2 baseline arm, identical eval protocol
   (25k paired decks, 3 baselines, defaults off for the tabular arm). Report bb/100 ±CI, stability
   notes, wall-time, VRAM. **No adoption path — owner decides the fork.**

## Phase 6 — Deferred / owner-discussion packages (no default action)

- **E2** per-infoset uint32 visit counters (+856 MB, one write per traverser visit): small-game
  benchmark gate ≥0.95× throughput first; prerequisite for B2/B4 targeting.
- **B2/B4** tempered/stratified sampling: only if E2 data shows residual cold spots after B1 soak.
- **D2** coarser postflop action abstraction: **fresh table required**. Deliverable is a sizing memo
  (`sizing.py --config` variants: max_raises 1, fraction sets) + projected visits/infoset at measured
  post-B1 throughput. Restart is the owner's call; if taken, bundle CFR+ (Phase 4) and A3 warm-start.
- **A-labels for distill** (`default_label_frac` wiring from A/README) + `scripts/run_distill.py`
  CLI + smoke-first protocol (200k states; full 2M-state collect is a slow pure-Python loop) —
  parked with the deferred distill/self-play round.
- Checkpoint interval 0.25→0.5h only if logged save time exceeds ~20 s (else skip — not worth a knob).

## Phase 7 — Candidate discovery round 2: profiling, hyperparameters, GPU offload (added 2026-07-05; report-first)

*Context at creation: CFR+ adopted live (iter 21.64B, ~250k it/s quiet / ~145-200k contended,
config commit `f74e8e4`, rollback = `pre_C3_backup`). Eval TAG −447 → −327 and climbing. The
regret-prune path is now moot under flooring. Same rules as ever: DEV/small-game first, gates,
one live change per stop window, tripwire 214,143,408.*

### 7.1 — Profile before guessing (the candidate-ranking step; DEV, ~half day)

Hyperparameter and GPU speculation is worthless without knowing where the time goes. Profile the
stock loop on the live config (3-worker DEV run alongside the daemon, record-only; repeat quiet in
the next stop window if numbers matter):
- Wall-time split of `traverse`: showdown eval (`payoffs_nb`), bucket lookup (`player_bucket`),
  hash probe (`table_find_or_insert`), RNG/deal, regret-matching, recursion overhead. Method:
  njit-friendly sampling — run variant kernels with pieces stubbed (e.g. fixed bucket, no payoff)
  and difference the throughputs; cross-check with VTune/py-spy on a 1-worker run if inconclusive.
- Memory-bound check: throughput vs n_workers curve (1/3/6/12) — if it flattens well before 12,
  the loop is RAM-bandwidth-bound and neither more workers nor most micro-opts will help (points
  to layout/dtype work or GPU residency instead).
**Deliverable:** 1-page ranked cost table → picks which 7A/7B arms are worth running.
**Gate G7.1:** the split accounts for ≥85% of wall time and is reproducible across two runs.

### 7A — Hyperparameter sweep (small-game harness; adopt-on-gates like Phase 4)

Candidates, ranked by expected value / risk (each = one 30–45-min A/B pair via `exp_run.py`,
`compare.py` gates: eval not-worse in combined CI, plus per-knob gate below):
0. **Current-policy vs average-policy eval (ZERO training cost; literature-backed):** Pluribus
   plays its *final-iteration* strategy, not the weighted average (Science supplement — the average
   retains bad actions that haven't washed out). Our checkpoints store both tables: `regret` →
   regret-matched current policy, `stratsum` → average policy. Run `eval_ckpt` twice on the same
   live checkpoint (25k paired decks) and compare. If current-policy wins, ship *that* to
   distill/eval — a free improvement, no training change, no stop window.
1. **`n_workers` 12→13/14** (deferred from window #1): live machine has 16 logical cores;
   daemon + eval + dashboard need headroom. Gate: 1h mean iters/s ≥ +5% with no eval-cycle
   overruns, else revert. Live-adoptable via config alone (stop window not strictly needed —
   restart required since threads are set at startup).
2. **`batch_iters_per_call` 1000→2000/4000**: fewer Python-loop round-trips between njit calls;
   costs status/checkpoint granularity (still fine at 4000×12 = 48k iters ≈ 0.25 s). Gate: ≥ +3% it/s.
3. **Fresh-run config hygiene (no live effect; folds into D2 defaults):** drop
   `prune_threshold`/`prune_skip_prob`/`prune_enabled_after_fraction` when `cfr_plus:1`
   (dead knobs under flooring); recalibrate `planned_iterations` (live run is at 21B+ vs the
   5e9 the discount/prune schedule was keyed to — for fresh runs pick the real budget).
4. **Full-CFR+ averaging** (C/README option 2): replace LCFR stratsum discounting with linear
   (t-weighted) averaging when `cfr_plus:1` — the textbook CFR+ pairing. Small-game A/B gate:
   eval ≥ control − combined CI AND faster convergence at the 15-min checkpoint. Fresh-runs-only
   (changes the meaning of accumulated stratsum mid-run; do NOT flip on the live table).
5. **`regret_dtype`/stratsum dtype experiments** only if 7.1 shows memory-bandwidth-bound.

*Literature remarks (research pass 2026-07-05, see `improvements/exp/deepcfr/RESEARCH.md` §2):*
- *Fresh-run discounting:* **DCFR (α=1.5, β=0, γ=2)** empirically beats plain LCFR (Brown &
  Sandholm 2019); **dynamic α/γ schedules** beat static settings (arXiv:2404.09097). Both are
  fresh-run/D2 candidates — not mid-run changes.
- *Pluribus exacts:* regret **floor −310M** (clamp, keeps actions revivable) + prune skip p=0.95
  below −300M, never last street, LCFR discount only first 400 min, **final-iteration play**
  (item 0 above). Our stock trainer had the prune without the clamp; CFR+ (floor 0, now live) is
  the stronger form of the same fix. For fresh runs, the exact Pluribus combo (−310M floor +
  prune) is the literature-faithful alternative to CFR+ — one small-game A/B would settle which
  seeds better.
**Deliverable:** sweep table + recommended live flips (each its own stop window) + fresh-run
default set. **Abort-if:** any knob that touches training math goes through the same
backup-before-flip procedure as Phase 4.

### 7B — GPU offload of MCCFR (feasibility memo FIRST; no code before owner reads it)

Honest prior: external-sampling MCCFR is a branchy, recursive, hash-table-random-access workload —
the classic *worst case* for GPU. The 5090's realistic roles, in increasing ambition:
1. **Table residency + wave-batched kernels**: regret/stratsum (12.5 GB) fits in 32 GB VRAM.
   Lockstep-batch thousands of hands in Python/CuPy waves: gather rows → regret-match → scatter
   updates on GPU; tree control flow stays CPU. Risk: PCIe/HtoD chatter and wave divergence
   (hands finish at different depths) eat the gains. Micro-benchmark FIRST: GPU gather+RM+scatter
   throughput on random 15.6 GB-table indices vs numba's measured rate — if the microbench can't
   beat CPU by ≥3× on the isolated op, stop there.
2. **C1 vector / public-chance-sampling CFR**: carry all 200 buckets per public state as a vector;
   showdown becomes a matmul. The only *true* "CFR on GPU" shape. Large rewrite (public-tree
   representation, dense per-node arrays replacing the hash table) — value is highest for the
   post-blueprint subgame-solve phase, not the current seed run.
3. **Deep CFR** — already scoped as Phase 5; GPU-native by construction; don't duplicate.
**Deliverable:** 1-page memo (options, microbench numbers for #1, effort estimates, recommendation)
— same owner-review-before-implementation rule as Phase 5.1. **Feasibility exit:** if the #1
microbench fails its 3× bar and #2 is estimated >1 week, the memo recommends "GPU stays on
distill/self-play duty" and Phase 7B closes with no code.

**Phase 7 done when:** G7.1 profile delivered · 7A sweep table + adoptions (if any) gated and
logged in LEDGER · 7B memo delivered. Owner decision points: which 7A knobs go live; 7B go/no-go.

---

## Experiment harness spec (`implementation/nlhe/improvements/exp/`)

```
exp/
  configs/   small50.json, small50_mixed25.json, small50_cfrplus.json
  gates/     A_eval.json, B1_smallgame.json, C3_smallgame.json    # {"metric": {"op": ">=", "value": X}}
  exp_run.py           # ONE command per arm: train → measure_reach → eval → report.json+md
  eval_ckpt.py         # eval any checkpoint dir: --ckpt --config --decks --seed --defaults on|off --out
  compare.py           # two report.json + gates file → PASS/FAIL table, exit code
  compare_preflop.py   # drift: two checkpoints/milestones → weighted preflop TV (mass≥1000 rows + top-1000 mean)
  results/             # committed: report.json/md per run, baseline_reach.txt, LEDGER.md
  runs/                # gitignored POC run dirs
```

- Run naming `<YYYYMMDD-HHMM>_<exp><arm>_s<seed>`. `exp_run.py` shells existing entry points
  (`train.py --run <name> --config <cfg> --pilot-hours <m/60>` — note `--pilot-iters` is an *absolute*
  iteration threshold), then writes `report.json`: exp/arm/seed, config path+sha256, git commit,
  threads, live_daemon_running flag, final_iteration, mean iters/s (excluding first 3 min JIT),
  per-street coverage `{total, regret_nz, strat_nz, strat_gt1, strat_gt10, avg_mass}`, eval per
  baseline `{bb100, ci, decks, seconds, seed}`, notes.
- `compare_preflop.py`: rules → `_betting_tree` → preflop bases × 169 buckets → `mix_bucket` →
  `table_find` in both tables → normalized rows → mass-weighted TV. Accepts checkpoint dirs and
  zstd milestones.

## Reporting & definition of done

Each phase ends with a one-page report in `results/` and a LEDGER row (change, gates, adopted y/n,
live iteration at adoption). **Done when:** E3 + A1/A2 live with post-adoption gates green; B1/B3
report delivered (adopted + 24h soak green if approved); C3 decision package delivered; C4 bake-off
report delivered; ledger complete. Owner decision points along the way: workers 12→13 (window #1),
B1 go/no-go (after Phase 3.3), C3 go/no-go (after Phase 4.4), Deep CFR design doc (Phase 5.1),
D2 restart discussion (Phase 6), 7A live flips + 7B GPU go/no-go (Phase 7).
