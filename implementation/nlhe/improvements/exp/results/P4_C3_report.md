# Phase 4 — C3 CFR+ regret flooring: decision package

**Date:** 2026-07-05 · **Tree:** DEV worktree `improvements-dev` · **Live run untouched.**
**Gates:** G4.1 PASS · G4.2 PASS · G4.3 PASS. **Recommendation: adopt CFR+ in the
fresh-run defaults set (D2 / future runs); do NOT retrofit the live table mid-run
without the owner-gated quiet prune-value benchmark (details in §4).**

CFR+ floors regrets at 0 after each update (`regret = max(regret + Δ, 0)`), so a
buried action revives on its first positive update instead of climbing back from a
large negative. Config-gated by `mccfr.cfr_plus` (int, default 0 = stock). Under
flooring, regrets never go negative, so the regret-prune path (`regret < -3e8`)
never fires — pruning self-disables. LCFR discounting is left ON (the "keep DCFR +
add floor" hybrid from `C/README.md`), not removed.

---

## 1. G4.1 — correctness (Kuhn + njit path). PASS

- `test_kuhn_cfr.py` parametrized on `cfr_plus`: exploitability **< 0.01 in both
  modes** (stock and CFR+) on Kuhn, same `regret_matching` primitive the NLHE
  traversal uses. Alpha relationship (bet-K ≈ 3× bet-J) holds in both.
- New `test_cfrplus.py` (njit training path): with `cfr_plus=1` every regret stays
  ≥ 0 end-to-end, the table grows by **zero** slots, and the default arg (0)
  reproduces the stock path (allows negative regrets). **Full DEV suite: 24 passed.**

## 2. G4.2 — fresh small-game A/B (45-min arms, seed 7, live daemon up during both). PASS

Same `small50` game/buckets/budget; only difference is `cfr_plus`. Eval defaults
OFF (raw fallback) to isolate the learning, 25k paired decks.

| metric | control (stock) | CFR+ | ratio / Δ |
|--------|-----------------|------|-----------|
| final iters (equal 45 min) | 156.3M | 192.3M | **1.23×** |
| mean iters/s (post-JIT) | 57,061 | 69,112 | **1.21×** |
| preflop `strat>1` | 46.5% | 80.5% | 1.73× |
| flop `strat>1` | 35.1% | 50.1% | **1.43×** |
| turn `strat>1` | 24.1% | 30.7% | 1.27× |
| river `strat>1` | 19.4% | 20.7% | 1.07× |
| vs random | −94.2 (±54) | −63.7 (±54) | +30.5 |
| vs calling_station | +70.2 (±49) | +104.4 (±50) | +34.2 |
| **vs tag** | **−1212.5 (±43)** | **−1206.7 (±44)** | +5.8 (within CI) |

`compare.py` vs `gates/C3_smallgame.json`: `tag_not_worse` PASS, `cs_not_worse`
PASS. **On a fresh run CFR+ is faster AND covers far more AND does not regress eval.**
The mid-run speed claim is subsumed — CFR+ simply completed 1.23× more iterations in
the same wall-clock. Flooring keeps `regret_matching` well-conditioned early (fewer
all-negative rows → fewer uniform-fallback probes), and on this shallow tree the
pruning it disables was buying little.

## 3. G4.3 — resume-probe: flooring an already-pruned table (models the live case). PASS

Copied the finished stock control table aside, resumed it with `cfr_plus:1` (prune
still "on" but self-disabled) for +20% iters (156.33M → 187.60M). Eval is paired vs
the control's own final row (defaults off, 25k, seed 7).

| baseline | before (stock) | after (+CFR+) | Δ | combined CI |
|----------|----------------|---------------|-----|-------------|
| random | −94.2 (±53.9) | −100.6 (±53.6) | −6.4 | ±107 |
| calling_station | +70.2 (±49.1) | +70.0 (±49.1) | −0.2 | ±98 |
| **tag** | **−1212.5 (±43.0)** | **−1224.7 (±42.9)** | **−12.2** | **±85.8** |

- **G4.3 gate (tag Δ ≥ −combined CI): PASS** (−12.2 ≫ −85.8). No eval regression from
  reviving every buried action on an already-pruned table.
- **Preflop drift/churn** (control-final vs resume-final, mass-weighted TV over
  675k shared rows): **0.0386** (top-1000-by-mass mean 0.0376). Small — reviving
  buried regrets perturbed the mature strategy modestly, not catastrophically.
- **Throughput / prune-value proxy:** resume-segment ran at **84.9k it/s** (fully
  post-warmup, mature table) with pruning self-disabled — *faster* than stock's 57k
  fresh mean, i.e. disabling pruning cost nothing here. **Caveat:** `small50` has
  1 raise/street and a 50bb stack — a shallow tree where pruning skips few branches.
  The live game (2 raises/street, 100bb, 8B iters) prunes a far larger fraction of
  deeply-buried branches, so its prune value is likely larger and is **not** settled
  by this proxy.

## 4. Decision & the one-way caveat

**CFR+ is unambiguously good for fresh runs** → **adopt into the fresh-run defaults
set** (D2 restart and any future run), per the plan. Zero downside observed: faster,
far better coverage, no eval cost, correctness proven on Kuhn.

**For the LIVE table (mid-run retrofit): recommend defer — do not flip on the live
run now.** Rationale:

1. **One-way change.** Floored regrets are unrecoverable — once negatives are
   clipped to 0 the pre-flooring state cannot be reconstructed. Live rollback would
   be a **full table restore from the `pre_C3_backup` checkpoint only** (no config
   flip-back), unlike every prior phase's config-only rollback.
2. **The live prune-value is unmeasured.** The resume-probe shows flooring is *safe*
   (no eval harm, small drift) and *free* on the small game, but cannot quantify what
   pruning is worth at 8B live iters. If live-scale pruning is buying real throughput
   and flooring disarms it, that's a standing cost over the remaining ~300h.
3. **No upside urgency.** The live table is already converged/sane on the trained
   lines; CFR+'s big win is *coverage on under-trained nodes*, which a fresh D2
   restart (which already bundles CFR+) would capture cleanly and reversibly — with
   none of the one-way risk.

**One owner action closes the package definitively:** a single quiet stop-window
live-config benchmark of `run_batch` with pruning forced ON vs OFF (prune-value at
8B iters). If pruning is worth little there too, live retrofit becomes low-risk and
can be reconsidered; if it's worth a lot, defer-to-fresh-run stands. This benchmark
was **not** run autonomously — it requires stopping the live daemon (owner-gated),
and Phase 4 is report-first with no live impact.

## 5. Artifacts

- Code (DEV, tag `phase4-g41`): `src/mccfr.py`, `src/mccfr_flopstart.py`,
  `src/daemon.py`, `tests/test_kuhn_cfr.py`, `tests/test_cfrplus.py`,
  `configs/small50_cfrplus.json`.
- Reports/JSON in `improvements/exp/results/`:
  `20260705-0830_c3-control_s7.*`, `20260705-0916_c3-cfrplus_s7.*`,
  `20260705-1004_c3-resumeprobe_s7.*` (+ `.probe_summary.json`, `.drift.json`).
- Gate: `gates/C3_smallgame.json` (G4.2). Live tripwire held (214,143,408) throughout;
  live daemon healthy (iter ~17.9B, 143.9k it/s) at probe time.
