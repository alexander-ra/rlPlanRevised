# Phase 1 report — A1+A2 output-side defaults

**Date:** 2026-07-04 · **Gate G1.1:** PASS · **Gate G1.2:** **FAIL** (−80.5 vs +100 required)
**Decision:** delivered, awaiting owner go/no-go. **Nothing adopted; LIVE untouched.**

## What was built (all in DEV worktree `improvements-dev`)
- `src/default_policy.py` (A1 heuristic + A2 nearest-bucket), `tests/test_default_policy.py` (3 tests, green; full suite 17 passed).
- `src/evalmatch.py` wired config-gated: `use_defaults` ∈ {0 uniform (byte-identical to live), 1 = A2→A1, 2 = A2-only}.
- `exp/eval_ckpt.py` harness (one table load → off/on/a2only/all arms, paired deck+action seed).

## Result — paired offline A/B, 25k decks, seed 123 (live checkpoint ~11.5–11.6B iters)

| arm | vs random | vs calling_station | vs tag |
|-----|-----------|--------------------|--------|
| **off** (uniform fallback) | +4.0 (±52) | +245.3 (±49) | −441.1 (±41) |
| **on** (A2 → A1) | **+317.7** (±50) | **+429.3** (±45) | **−521.6** (±34) |
| **a2only** (A2 → uniform) | +4.9 (±52) | +220.2 (±49) | −420.2 (±41) |

Δ vs off — **on:** random **+314**, cs **+184**, tag **−80.5** · **a2only:** ~0 everywhere.

## Interpretation
- **A2 is a near no-op here.** Under-trained infosets usually have under-trained public-state siblings, so A2's nearest-*visited*-bucket search misses → uniform. `a2only ≈ off`.
- **A1 carries the whole effect.** The pot-odds/equity heuristic makes cold-spot play *sensible*: it crushes exploitable bots (random +314, calling-station +184) but is itself exploitable by a disciplined aggressor (tag −80 to −101). That is the expected behaviour of a reasonable-but-unsolved heuristic.
- The gate's "+100 vs TAG" implicitly asked the heuristic to also beat the *strongest* benchmark; it does the opposite there while achieving the project's actual stated goal — **eliminating random postflop play** (PROJECT_CONTEXT: "a randomly-playing postflop is the failure mode actually worth fixing").

## Scope of the adoption decision
Phase-1 adoption (`eval.use_default_policy: true`) changes **only the eval readout** — not training, not the blueprint, not distill labels. It is fully reversible (config flip). The defaults' real intended payoff is as **distill labels** for the self-play seed (deferred Phase-6 wiring), where "sensible not random in the cold ~75%" is exactly what's wanted and there is no adversarial-eval concern.

## Options for the owner
- **(A) Adopt mode 1 for eval anyway** — accept the TAG gate miss; weights the random-postflop fix over the TAG metric. Caveat: A1 backfills cold spots regardless of training, so eval becomes a *less* sensitive signal of postflop training progress, and the headline TAG number worsens.
- **(B) Keep eval defaults OFF (status quo); reserve A1/A2 for distill labels (Phase 6)** — their true purpose as a seed. Recommended default: the eval stays a clean training-progress signal; the "sensible-not-random" property is applied where it actually matters (the NN seed).
- **(C) Tune A1 to be less exploitable, then re-test** — e.g. reduce auto-fold-facing-bet / rebalance call vs fold, aiming to shrink the −80 TAG loss while keeping the weak-opponent gains, before any adoption.

**Recommendation:** (B) as the standing choice, with (C) as the follow-up if you want the heuristic robust vs strong opponents before it seeds distillation. (A) is defensible if you specifically want eval to reflect deployed (defaults-on) play.
