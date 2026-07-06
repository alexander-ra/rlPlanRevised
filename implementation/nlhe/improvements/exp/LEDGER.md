# NLHE Improvement Execution — LEDGER

One row per adoption / gate event. Newest at bottom of each phase. Append-only.

---

## Phase 0 — Baseline + readable eval

### 0.1 — Baseline snapshot (2026-07-04)

- **`$PY`** = `C:\Users\UserNIK\projects\rlPlanRevised\.venv\Scripts\python.exe`
  - Confirmed via process tree: daemon parent PID 20020 is `.venv\Scripts\python.exe`
    running `scripts\train.py --run 20260703_6max_200_v1`; its heavy child PID 11256
    (`Python312\python.exe`) is the multiprocessing worker pool. Dashboard = PID 11664/13520.
    Matches the plan's expectation (`LIVE\.venv`).
- **git HEAD (LIVE, master)** = `80567cc3df99cceb7ed94a52216b401c5796b844`
- **`status.json` @ snapshot:** state TRAINING, iteration 11,305,624,000, iters/s 143,776,
  workers 12, ram_gb 15.6, **infosets 214,143,408 (TRIPWIRE value ✓)**, prune_on true,
  last_checkpoint iter 11,206,180,000.
- **Checkpoints:** A = iter 11,206,180,000 (newer, ts 19:21), B = iter 11,075,392,000 (19:06).
  Each ~15.6 GB (regret 6.23 GB + stratsum 6.23 GB + slot_key 3.11 GB), DONE sentinel present.
- **Machine:** 16 logical cores, 61.7 GB RAM (34.1 GB free at snapshot), C: 368 GB free.
- **Latest 2k-deck eval** (iter 11,206,180,000): random +67.1 (±181), calling_station +148.2 (±170),
  **tag −456.7 (±148)**. Last-5-eval TAG mean ≈ **−450 bb/100**, per-eval CI ≈ ±147 (noise dominates —
  the readability problem G0.2 addresses).
- **Config `eval.pilot_decks` = 2000** at snapshot (the key `run_eval.py:28` actually reads;
  `eval.decks`/`threads`/`seat_rotations` confirmed unused/dead).

### 0.2 — Baseline coverage (`baseline_reach.txt`, checkpoint iter 11,206,180,000)

**Gate G0.1: PASS** — completed in ~12 s (numba JIT cached from prior runs; ≪ 30 min limit).
Coverage-scan infoset total = 7,137,208 + 54,461,000 + 75,951,400 + 76,593,800 = **214,143,408 (tripwire ✓)**.

**Playout study (200k hands, all seats = current strategy):**
- Hands ending per street: preflop 34.5% · flop 21.4% · turn 11.5% · river 32.6%
- Hands reaching the flop: **65.2%**
- Sampled decision points per street: preflop **61.6%** · flop 18.8% · turn 11.4% · river 8.2%
  (→ ~61% of sampled training work is preflop — the motivation for B1 flop-start)

**Coverage scan (per-street `strat>1` = the key coverage metric later gates reference):**

| street  | infosets    | regret_nz | strat_nz | **strat>1** | strat>10 | strat>100 | avg_mass |
|---------|-------------|-----------|----------|-------------|----------|-----------|----------|
| preflop | 7,137,208   | 54.2%     | 46.8%    | **28.5%**   | 16.0%    | 8.1%      | 41858.4  |
| flop    | 54,461,000  | 34.3%     | 37.2%    | **25.7%**   | 12.5%    | 5.6%      | 4851.7   |
| turn    | 75,951,400  | 28.7%     | 32.5%    | **23.7%**   | 11.9%    | 5.4%      | 4290.0   |
| river   | 76,593,800  | 25.8%     | 29.5%    | **22.6%**   | 12.0%    | 5.5%      | 5133.9   |

Postflop baseline for later gates: flop/turn/river `strat>1` = **25.7% / 23.7% / 22.6%**
(G3.2 target: mixed ≥1.8× these; G3.6 soak target: baseline +8 pp). Postflop is under-trained
(~65-75% of rows never reach `strat>1`) but *not random on touched rows* — consistent with the
"sensible-but-shallow" seed goal. Note coverage is materially better than the plan's original
"~87% never visited" figure (that was an earlier, lower-iteration snapshot; now at 11.3B iters).

### 0.3 — E3 pre-authorized zero-stop edit (2026-07-04)

Applied the single authorized LIVE edit: `config/default.json` `eval.pilot_decks` **2000 → 25000**.
JSON re-validated (`json.load` OK). Applied at iter ≈ **11,343,496,000**, iters/s 144.7k, tripwire
214,143,408 ✓. Edit made just after an eval cycle (safe ~15-min window before next eval). No daemon
restart needed — the eval subprocess re-reads config each cycle.

### 0.4 — First 25k-deck eval = the "before" baseline (2026-07-04)

**Gate G0.2: PASS.** First eval after the edit (iter **11,465,188,000**):

| baseline        | bb/100   | CI (±) | wall  |
|-----------------|----------|--------|-------|
| random          | −10.55   | 51.8   | 7 s   |
| calling_station | +242.56  | 48.6   | 7 s   |
| **tag**         | **−447.44** | **41.4** | 6 s   |

- Wall-time ~20 s total ≪ 10-min ceiling ✓
- CI(tag) ±41.4 ≤ ±60 ✓ · CI(cs) ±48.6 ≤ ±60 ✓ (CIs shrank ~3.5× vs 2k-deck baseline, as predicted;
  eval is far faster than the ~4-min estimate — duplicate_match is well-parallelized, ~20 s at 25k).
- Tripwire 214,143,408 held across the edit + eval.

**This row is the "before" for every later adoption.** TAG ≈ **−447 bb/100 (±41)** is now confirmed
real signal (the tight CI removes the noise the 2k evals had). random ≈ −11 (±52), CS ≈ +243 (±49).

---

## Phase 0 — COMPLETE ✓ (all gates green)

- G0.1 baseline coverage PASS · G0.2 readable 25k eval PASS · tripwire held throughout.
- LIVE untouched except the one authorized `pilot_decks` edit; daemon healthy (144.7k it/s, iter ~11.47B).
- DEV worktree `improvements-dev` + artifacts junction live; DEV pytest 14 passed.
- Ready for Phase 1 (A1+A2 output-side defaults) — DEV prep is stop-window-free until adoption (stop window #1).

---

## Phase 1 — A1+A2 output-side defaults (DEV work; adoption BLOCKED)

### 1.1 — default_policy + tests: **Gate G1.1 PASS**
Copied `improvements/A/default_policy.py` → DEV `src/`. New `tests/test_default_policy.py`
(A1 valid-row + no-fold-when-check-free over 10k-state fuzz; A2 False on empty table; A2
one-neighbour normalized). Full DEV suite **17 passed**.

### 1.2 — evalmatch wiring: complete, off-path byte-identical
Threaded `use_defaults` int through `duplicate_match → play_hand → _choose → _blueprint_strategy`.
Modes: 0 = uniform (byte-identical to original live behaviour), 1 = A2→A1, 2 = A2-only (A2 else
uniform, no A1). Built harness `improvements/exp/eval_ckpt.py` (loads a checkpoint once, runs
off/on/a2only/all on the same table + deck seed; numba action-RNG pre-seeded for a clean paired A/B).

### 1.3 — Paired offline A/B (25k decks, seed 123): **Gate G1.2 FAIL**

Two runs (ckpt A@11,465,188,000, then 3-arm on ckpt B@11,594,056,000 — daemon rotated):

| arm | random | cs | tag | Δtag vs off |
|-----|--------|-----|-----|-------------|
| off (uniform) | +4.0 (±52) | +245.3 (±49) | −441.1 (±41) | — |
| on (A2→A1) | +317.7 (±50) | +429.3 (±45) | −521.6 (±34) | **−80.5** |
| a2only (A2→uniform) | +4.9 (±52) | +220.2 (±49) | −420.2 (±41) | +20.8 |

**G1.2 requires Δtag ≥ +100 → FAIL** (got −80.5). RANDOM/CS "not worse" ✓, walltime ≤3× ✓.

**Diagnostic finding (from the 3-arm split):**
1. **A2 (nearest-visited-bucket) is a near no-op on this table** — `a2only ≈ off` on all three
   baselines (all Δ within CI). Under-trained nodes tend to have under-trained public-state
   siblings too, so A2 usually misses → uniform. Not a bug; expected at this coverage.
2. **A1 (the pot-odds heuristic) is the entire effect** — it crushes exploitable opponents
   (random +314, cs +184) but *loses more* to a competent aggressor (tag −80 to −101). Classic
   signature of a "reasonable but not game-theoretically sound" heuristic: punishes weak play,
   gets punished by strong play.
3. Dropping A1 (a2only) removes the TAG loss but also throws away the entire random-postflop fix
   → reverts to ~uniform. So it is **not** "A1 vs A2"; it is "A1's big weak-opponent win vs its
   small strong-opponent loss."

**Key scope note:** Phase-1 adoption (`eval.use_default_policy`) changes ONLY the **eval readout** —
it does not touch training or distill labels. The defaults' real intended payoff (sensible-not-random
distill labels for the self-play seed) is the deferred Phase-6 distill wiring, not this eval flag.

**Status: gate failed → STOP, report delivered, awaiting owner go/no-go (no adoption).**
Rollback needs: none (nothing merged/flipped on LIVE; all work is in DEV worktree).

**Owner decision (2026-07-04): option B — park A1/A2 as "ready for Phase 6 distill labels",
keep eval defaults OFF, proceed to Phase 2.** No adoption; no stop window used.

---

## Phase 2 — Config plumbing + small-game POC harness (DEV only; no LIVE impact)

### 2.1 — Betting-tree cache keyed by rules — DONE
`mccfr._betting_tree` now caches as `betting_tree_<sha1(rules)>.npz` with a self-verifying
legacy fallback (`_is_live_rules` compares packed rules arrays — no hardcoded hash). Live rules
sha1 = `5d62bcf706d6`; loads legacy `betting_tree_v1.npz` in 0.0s (no re-enumeration), bases match
exactly (1,077,263 states). `measure_reach.py` routed through `_betting_tree` (was blind-loading v1).
**Safety proven:** small50 (sha1 `569c61d103bd`, is_live=False) created its OWN
`betting_tree_569c61d103bd.npz` and never touched the live tree — exactly the corruption the old
blind load would have caused.

### 2.2 — `--config` plumbing — **Gate G2.1 PASS**
Threaded a config path through `train.py`, `run_eval.py`, `measure_reach.py`, `sizing.py`,
`daemon` (→ forwards `--config` to the eval subprocess argv), and cfg dicts into
`evalmatch._rules_arr/load_eval_artifacts/_bucket_mean_equity` and `mccfr.load_artifacts`.
`measure_reach.py` gained `--threads`/`--hands`/`--json`; `run_eval.py` reads
`eval.use_default_policy` (defaults 0). All defaults preserve live behaviour (backward-compatible).
- pytest: 17 passed. sizing (live cfg): 214,143,408 infosets, betting states {42232,272305,379757,382969}.
- **DEV benchmark (3 workers, live cfg): NEW slots created = 0; infosets = 214,143,408** ✓
  (69,950 it/s alongside live daemon — record-only, machine not quiet).

### 2.3 — small50.json + sizing — **Gate G2.2 PASS**
`improvements/exp/configs/small50.json`: stack 50, buckets 169/100/100/100, max_raises 1, n_workers 3,
eval 25k decks, full_checkpoint 0.1h, planned_iterations 150M (POC budget; discount_interval 600k = /250).
Sizing/build_table: **12,068,030 infosets, 0.9 GB table** (116,699 betting states) — ≤25M ✓, ≤2GB ✓.

### 2.4 — Harness built (`improvements/exp/`)
`eval_ckpt.py` (Phase 1), `exp_run.py` (train→measure_reach→eval→report.json+md), `compare.py`
(gate files → PASS/FAIL + exit code), `compare_preflop.py` (mass-weighted preflop TV; ckpt-ckpt njit
kernel + milestone path). Gate files: `small50_calib` (G2.3), `A_eval` (G1.2), `B1_smallgame` (G3),
`C3_smallgame` (G4). Pipeline smoke-testing in progress.

### 2.5 — Calibration (two 30-min arms) — **Gate G2.3 PASS**

| arm | final iter | mean it/s | flop | turn | river | random | cs | tag |
|-----|-----------|-----------|------|------|-------|--------|-----|-----|
| baseline  | 105.4M | 57,052 | 31.1% | 20.6% | 17.0% | −53.3 (±54) | +91.0 (±49) | −1242.3 (±43) |
| baseline2 | 108.6M | 59,016 | 32.3% | 21.5% | 17.6% | −30.8 (±54) | +97.2 (±49) | −1234.5 (±43) |

- **G2.3 PASS** (flop-based reading, owner-approved): flop 31–32% ≥ 30% ✓; all eval CIs ≤ ±60 ✓;
  end-to-end unattended ✓; reports complete ✓. Combined postflop (flop+turn+river) = 22.1%/22.9%
  — recorded transparently; the low turn/river is by design (more headroom for B1). Calib gate
  updated to `flop_strat_gt1_pct ≥ 30`.
- **Run-to-run spread (training variance; eval decks identical @ seed 7):** coverage ≤1.2 pp/street;
  eval tag ±7.8, cs ±6.2, random ±22.5 bb/100 — all within eval CIs. **→ Phase 3/4 tolerance:** a real
  A/B effect must clear ~8 bb/100 (tag/cs) of training noise on top of eval CI to be attributable;
  coverage-ratio gates (G3.2) are robust (≤1.2 pp noise on a ~22–31% base).

### 2.6 — Preflop-drift baseline: DEFERRED (timing, not blocking)
No live milestone yet (first ~2026-07-04 22:21). Not on the Phase 3 critical path (G3.4 uses
compare_preflop between small-game arm-end checkpoints, which is ready). Backfill when the milestone lands.

## Phase 2 — COMPLETE ✓ (G2.1, G2.2, G2.3 all pass; 2.6 deferred to milestone)
Workbench ready: rules-keyed betting-tree cache, full `--config` plumbing, small50 game (12M/0.9GB),
harness (exp_run/eval_ckpt/compare/compare_preflop) + gate files. Live run untouched throughout
(daemon healthy, tripwire held). Ready for Phase 3 (B1+B3 flop-start).

---

## Phase 3 — B1+B3 flop-start (centerpiece; report-first)

### 3.1 — flop-start wired + tests — **Gate G3.1 PASS**
Copied `improvements/B/mccfr_flopstart.py` → DEV `src/`. Daemon config-gated via a `_train` dispatch
(`mccfr.full_game_fraction` absent or ≥1.0 → stock `run_batch`; else `run_batch_mixed`). New
`tests/test_flopstart.py` (3 tests): all-fold line → `_advance_to_flop` returns 0; flop-reaching lines
are legal (street==1, non-terminal); **100k-iter mixed run on a prepopulated table → ZERO new slots**.
Full DEV suite: 20 passed. `small50_mixed25.json` created (`full_game_fraction: 0.25`).

### ⚠️ Finding (2-min integration smoke): discount-schedule desync
flop-start ENGAGED correctly, but it **rejects preflop-folding hands cheaply**, so the iteration
counter `gi` advances much faster per wall-clock (smoke: ~163k it/s vs stock ~57k). Because the LCFR
discount schedule and prune-enable are keyed to `gi`, the mixed arm races through them faster in
wall-clock → **systematically more discounting of `stratsum` → biases the G3.2 `strat>1` metric AGAINST
flop-start.** 2-min coverage delta (flop 14.4% mixed vs 15.1% stock) is within the ~1.2 pp run-to-run
noise → inconclusive. **Mitigation:** the 45-min A/B captures ALL coverage metrics (`strat_nz` is
discount-robust; `strat>1` is not) + the `gi` each arm reaches, so the report can separate flop-start's
true coverage effect from the schedule confound. Report-first; owner decides.

### 3.2 — 45-min A/B (control vs mixed25) — **VERDICT: FAIL (G3.2)**

| metric | control | mixed (flop-start) | gate | result |
|--------|---------|--------------------|------|--------|
| final iters | 159.8M | 376.9M (2.36×) | — | — |
| postflop strat_nz | 3,832,853 | 3,573,247 | — | 0.93× |
| **postflop strat>1 ratio** | — | — | ≥1.8 | **0.93 FAIL** |
| tag eval | −1186.4 (±43) | −1228.5 (±43) | not worse | PASS (within CI) |
| cs eval | +77.3 (±49) | +104.2 (±49) | not worse | PASS |
| preflop drift | — | 0.098 | ≤0.10 | PASS |
| iters/s ratio | — | 2.35× | ≥0.3 | PASS |

**Flop-start REDUCED postflop coverage (0.93×) instead of raising it (≥1.8× target).** Mechanism:
stock external-sampling already **branches the traverser's preflop actions** (reaching many flop
betting-states per deal); flop-start replaces that with a **single sampled preflop line**, so despite
2.35× more (cheap-reject) iters it covers fewer distinct postflop infosets. `strat_nz` (discount-robust)
agrees with `strat>1` → real coverage loss, not a schedule artifact. Discount-desync worry was a false
alarm (LCFR discount is iteration-keyed, applied identically per arm). **Will be worse on the live game**
(2 raises/street → higher preflop branch factor). Eval gained nothing (within CI) despite 2.36× iters.
G3.2's escalation ("try full_game_fraction 0.5") doesn't apply — 0.5 moves the ratio toward 1.0, not 1.8.

### 3.3 — Report delivered: `results/P3_B1_report.md`. **Recommendation: DO NOT adopt (no-go on stop window #2).**
Nothing merged/flipped on LIVE. The gated method worked: a plausible idea that would have mildly hurt
the live run was caught in a 90-min offline A/B without touching the 300–400h run.

### Interlude (owner-requested, 2026-07-05) — Dashboard v2
Rebuilt the dashboard in DEV (`src/dashboard/index.html` + vendored Chart.js 4.4.7 + rewritten
`serve_dashboard.py`): CI-banded eval charts w/ era filter + regression slopes, TAG rolling-mean panel,
throughput/cumulative charts, checkpoint A/B + milestone + storage panel via new read-only
`/api/overview`, coverage-snapshot panel (from `exp/results/coverage_snapshots.json` — append after each
measure_reach scan), generic tripwire alert (infosets vs first metrics row), eval-log tail, config
viewer. v2 server NEVER writes into the run dir (v1 copied index.html there). Served from DEV on port
8901 → new quick-tunnel URL; old v1 dashboard (8777) left running untouched. LIVE tree/daemon untouched.

### 3.4 — Final review (owner-requested, 2026-07-05): **Phase 3 CLOSED, no-go confirmed.**
Quantitative tie-out: traverser preflop branch multiplier B≈2.1 solved from the arms' own numbers —
flop-start's 2.36× iteration rate exactly cancels vs losing B (same postflop volume, 0.93× diversity).
Root cause: the "60–80% fold preflop" premise measured *sampled play*, not *training work* (fold
branches ~free under external sampling). Variant sweep (fraction tuning / branch-preflop / turn-start /
B2 / B4 / ε-exploration): none can reach G3.2; B2/ε-exploration noted as Phase-6 memo candidates only.
Full analysis in report addendum. **Stop window #2 never used; live run untouched through all of Phase 3.**

---

## Phase 4 — C3 CFR+ regret flooring (report-first; DEV only; live untouched)

C3 = floor regrets at 0 after each update (`regret = max(regret+Δ, 0)`). Config-gated
`mccfr.cfr_plus` (int, default 0 = stock). Under flooring regrets never go negative, so
the regret-prune path (`regret < -3e8`) self-disables. LCFR discounting left ON
(keep-DCFR-+-floor hybrid). All work in DEV worktree; DEV tag `phase4-g41`.

### 4.1 — cfr_plus plumbed + correctness — **Gate G4.1 PASS**
Threaded `cfr_plus` through `mccfr.traverse`/`run_batch` (recursion + both call sites),
`mccfr_flopstart.run_batch_mixed`, and `daemon.setup/_train` (reads `mccfr.cfr_plus`,
prints "CFR+ ON" on engage). `test_kuhn_cfr.py` parametrized on `cfr_plus`:
**exploitability < 0.01 in BOTH modes** (stock + CFR+), alpha relation holds. New
`test_cfrplus.py` (njit path): floor keeps every regret ≥ 0 end-to-end, **zero table
growth**, default-arg (0) = stock (allows negatives). **Full DEV suite: 24 passed.**

### 4.2 — Fresh small-game A/B (45-min arms, seed 7, live daemon up during both) — **Gate G4.2 PASS**

| metric | control (stock) | CFR+ | ratio/Δ |
|--------|-----------------|------|---------|
| final iters (equal 45 min) | 156.3M | 192.3M | 1.23× |
| mean iters/s (post-JIT) | 57,061 | 69,112 | 1.21× |
| preflop / flop / turn / river `strat>1` | 46.5/35.1/24.1/19.4% | 80.5/50.1/30.7/20.7% | flop 1.43× |
| vs random | −94.2 (±54) | −63.7 (±54) | +30.5 |
| vs calling_station | +70.2 (±49) | +104.4 (±50) | +34.2 |
| vs tag | −1212.5 (±43) | −1206.7 (±44) | +5.8 (within CI) |

`compare.py` vs `gates/C3_smallgame.json`: `tag_not_worse` PASS, `cs_not_worse` PASS.
**On a fresh run CFR+ is faster AND far higher coverage AND no eval regression.** Speed
claim subsumed (1.23× more iters same wall-clock). Runs: `20260705-0830_c3-control_s7`,
`20260705-0916_c3-cfrplus_s7`.

### 4.3 — Resume-probe: flooring an already-pruned table (models the live case) — **Gate G4.3 PASS**
Copied finished stock control table aside; resumed with `cfr_plus:1` (prune on →
self-disabled) for +20% iters (156.33M → 187.60M). Eval paired vs control's final row
(defaults off, 25k, seed 7). Run `20260705-1004_c3-resumeprobe_s7`.

| baseline | before (stock) | after (+CFR+) | Δ | comb. CI |
|----------|----------------|---------------|-----|----------|
| tag | −1212.5 (±43.0) | −1224.7 (±42.9) | **−12.2** | ±85.8 |
| calling_station | +70.2 (±49.1) | +70.0 (±49.1) | −0.2 | ±98 |
| random | −94.2 (±53.9) | −100.6 (±53.6) | −6.4 | ±107 |

- **G4.3 gate (tag Δ ≥ −comb CI): PASS** (−12.2 ≫ −85.8). No eval harm from reviving
  buried actions on a pruned table.
- **Preflop drift/churn** (control-final vs resume-final, mass-weighted TV over 675k
  shared rows): **0.0386** (top-1000 mean 0.0376) — small, not catastrophic.
- **Throughput / prune-value proxy:** resume-segment **84.9k it/s** with pruning
  self-disabled — *faster* than stock 57k fresh mean, i.e. disabling pruning cost
  nothing HERE. Caveat: `small50` is a shallow tree (1 raise/street, 50bb); the live
  8B-iter game prunes far more, so its prune value is likely larger and is NOT settled
  by this proxy.

### 4.4 — Decision package delivered: `results/P4_C3_report.md`
**Recommendation: adopt CFR+ into the fresh-run defaults set (D2 / future runs) —
unconditional (faster, more coverage, no eval cost). Do NOT retrofit the LIVE table
mid-run** without the owner-gated quiet prune-value benchmark, because: (1) the change
is **one-way** — floored regrets are unrecoverable, so live rollback = full table
restore from `pre_C3_backup` only (not a config flip-back); (2) live-scale prune value
is unmeasured (small-game proxy can't answer it); (3) no upside urgency — a fresh D2
restart already bundles CFR+ and would capture the coverage win cleanly and reversibly.
**One owner action closes it:** a single quiet stop-window live-config bench of
`run_batch` prune ON vs OFF (prune value at 8B iters). Not run autonomously (requires
stopping the live daemon — owner-gated; Phase 4 is report-first, zero live impact).

## Phase 4 — COMPLETE ✓ (G4.1, G4.2, G4.3 all pass; decision package delivered)
CFR+ recommended for fresh-run defaults; live retrofit deferred pending owner
prune-value bench. Live run untouched throughout (tripwire 214,143,408 held; daemon
healthy ~17.9B iters, 143.9k it/s at probe time). Nothing merged/flipped on LIVE.

---

## Phase 4 — C3 CFR+ LIVE ADOPTION (owner-approved 2026-07-05; first live change of the plan)

Owner opted to apply CFR+ to the **live run** via resume (keep the 21.6B-iter table), not a
fresh restart. Executed the stop→apply→resume procedure:

1. **Backup:** stock final checkpoint copied to `RUN\pre_C3_backup` (slot A, iter
   **21,639,940,000**, 14.5 GB, verified match + DONE). Zero-loss rollback point.
2. **Graceful stop:** sent `CTRL_C_EVENT` to the daemon console (AttachConsole +
   GenerateConsoleCtrlEvent — not a force-kill); daemon wrote its final checkpoint at
   iter 21,639,940,000 and exited cleanly.
3. **Minimal patch** (NOT a full branch merge — avoided dashboard-v2/dormant-proposal/
   betting-tree-cache surface): `cfr_plus` in `src/mccfr.py` (traverse/run_batch) + `src/daemon.py`
   (config read + both run_batch calls) + Kuhn test parametrized. Committed master `f74e8e4`.
4. **Test battery:** `pytest tests/test_kuhn_cfr.py` 2 passed (both modes, exploitability <0.01);
   `train.py --benchmark --seconds 30` → **NEW slots 0, infosets 214,143,408**, 253,885 it/s
   (quiet-machine stock prune-off reference).
5. **Config flip:** `mccfr.cfr_plus: 1`.
6. **Restart + verify:** daemon PID 21972 resumed from checkpoint A @ 21,639,940,000, printed
   **`CFR+ ON: regret flooring at 0`**; within 1 min: state TRAINING, iter advancing,
   **it/s 250,229**, **tripwire 214,143,408 OK**, prune_on True (self-disabled). **No iters/s
   drop** — CFR+ ≈ prune-off throughput (254k bench), as theory predicts. Dashboard restarted
   fresh (v1, port 8777) with new tunnel URL.

**Rollback (if a later eval/soak regresses):** stop daemon → `git revert f74e8e4` (or set
`cfr_plus:0`) → restore `pre_C3_backup` into `checkpoints\A` → restart. One-way caveat: floored
regrets since adoption are unrecoverable, hence the checkpoint restore.
**Monitoring:** first eval cycle (~15 min) for tracebacks; iters/s floor; tripwire each check.

### Phase 4 addendum (2026-07-05, found during Phase 5 prep): eval-harness cfg bug + re-verification

**Bug:** `eval_ckpt.py` accepted `--config` but never passed it into `evalmatch.duplicate_match`,
which silently fell back to the LIVE `default.json`. Every small-game eval in Phases 2–4 was played
under stack-200/2-raise rules + 200-bucket codebooks against stack-50 tables (largely uniform-
fallback play). NOT affected: all coverage gates (measure_reach passes `--config` correctly —
G3.2's flop-start FAIL and G4.2's 1.43× coverage stand), and all LIVE-run evals (live cfg was the
correct cfg there, incl. the Phase-1 A/B and the post-adoption soak).

**Fix:** cfg now threaded through `eval_ckpt._run_one → duplicate_match(cfg=...)`. Re-ran the three
Phase-4 arms at 25k decks / seed 7 / defaults off with correct rules:

| arm | tag (buggy) | tag (fixed) | cs (fixed) | random (fixed) |
|-----|-------------|-------------|------------|----------------|
| control     | −1212.5 (±43) | **−239.7 (±11)** | +34.5 (±12) | −14.2 (±13) |
| cfrplus     | −1206.7 (±44) | **−248.6 (±11)** | +27.4 (±12) | −7.2 (±13) |
| resumeprobe | −1224.7 (±43) | **−245.6 (±11)** | +44.9 (±12) | −16.4 (±13) |

**Gates re-verified:** G4.2 tag Δ = −8.9 (comb. CI ±22) PASS · cs Δ −7.1 (±24) PASS ·
G4.3 tag Δ = −5.9 (±22) PASS. **All Phase-4 conclusions stand.** Bonus: correct small-game CIs are
±11–13 (vs ±41–49 claimed before), so future small-game gates can be ~4× tighter.

### Phase 5 (2026-07-05): Deep CFR bake-off POC — G5.1 PASS, bake-off gate PASS

Full report: `exp/deepcfr/REPORT.md` · design `exp/deepcfr/DESIGN.md` · research `exp/deepcfr/RESEARCH.md`.

| gate | result |
|---|---|
| G5.1 smoke (finite losses, ckpt round-trip, VRAM stable) | **PASS** (VRAM peak 378 MB) |
| Bake-off @ equal 45-min wall-clock vs c3-control (fixed-cfg eval, 25k decks, seed 7) | **PASS — Deep CFR better on all 3 baselines, outside CI** |

| policy | random | cs | tag |
|---|---|---|---|
| tabular control | −14.2 (±13) | +34.5 (±12) | −239.7 (±11) |
| deepcfr strategy net | +5.0 (±13) | +523.7 (±12) | −215.4 (±11) |
| **deepcfr final adv net** | **+26.7 (±13)** | **+598.5 (±12)** | **−211.8 (±11)** |

403 CFR iters, K=3,000, [256,256] MLP, research-informed defaults (no tuning pass needed).
1-min micro-run already matched tabular-45-min vs tag (−263.5 ±41). Final-adv-net > strategy-net
everywhere (supports Phase 7A item 0). Runs: `exp/deepcfr/runs/20260705-212{4,7}_deepcfr-*_s7`,
reports in `exp/results/`. Live daemon unaffected throughout (157k it/s, tripwire OK).
