# Step 03 — Exploration: CFR Variants on Kuhn & Leduc Poker

Empirical comparison of CFR algorithm family on two benchmark games.
All scripts run from `implementation/step03/exploration/`.

---

## Scripts

| Script | Game | What it does |
|---|---|---|
| `implDayOne1.py` | Kuhn Poker | First working MCCFR prototype (ES + OS + custom CFR) |
| `implDayOne1_test.py` | Kuhn Poker | Full comparison: ES-MCCFR, OS-MCCFR, custom CFR, OpenSpiel CFR, CFR+ |
| `leduc_comparison.py` | Leduc Poker | ES-MCCFR, OS-MCCFR, OpenSpiel CFR, CFR+ up to 5k iterations |
| `leduc_race.py` | Leduc Poker | 5-minute wall-clock race: CFR+ vs ES-MCCFR vs OS-MCCFR |

Outputs (plots + caches) go to `figures/`.

---

## Findings: Kuhn Poker (`implDayOne1_test.py`)

Kuhn Poker is a minimal 3-card game (J/Q/K, one betting round, 12 information sets).

**Result at 5,000 iterations:**

| Algorithm | Exploitability | Time |
|---|---|---|
| Custom CFR | ~0.00035 | < 1s |
| OpenSpiel CFR | ~0.0015 | ~2s |
| CFR+ | ~0.0003 | ~2s |
| External Sampling MCCFR | ~0.004 | ~1s |
| Outcome Sampling MCCFR | ~0.025 | ~1s |

**Key observations:**
- On a 12-infoset game, even vanilla CFR converges rapidly. CFR+ is fastest in practice due to regret floor (`max(r, 0)`) and linear averaging.
- Custom CFR matches OpenSpiel CFR, validating the implementation.
- Both MCCFR variants are slower to converge per iteration due to sampling noise, but are cheap per iteration.

---

## Findings: Leduc Poker (`leduc_comparison.py`)

Leduc Poker adds a community card and two betting rounds (~936 information sets — ~78× larger than Kuhn).

**At 5,000 iterations (log-log plots):**

| Algorithm | Exploitability @5k iters | Seconds for 5k iters |
|---|---|---|
| CFR+ | ~0.000054 | ~859s |
| CFR | ~0.0076 | ~747s |
| External Sampling MCCFR | ~1.17 | ~7s |
| Outcome Sampling MCCFR | ~3.08 | ~5s |

The full-tree methods (CFR, CFR+) are dramatically better per-iteration but cost ~100× more time per iteration than MCCFR variants.

---

## Findings: 5-Minute Race (`leduc_race.py`)

Fixed wall-clock budget (300 seconds each), measuring exploitability throughout.

**Final values at 300 seconds:**

| Algorithm | Exploitability | Iterations in 5 min |
|---|---|---|
| CFR+ | ~0.00042 | ~300 |
| External Sampling MCCFR | see `leduc_race_cache.json` | ~200k+ |
| Outcome Sampling MCCFR | ~0.527 | ~millions |

**Key observations:**

1. **CFR+ dominates on small games.** Full tree traversal is cheap enough (~1s/iter on Leduc) that CFR+ completes ~300 high-quality updates in 5 minutes, reaching near-Nash performance.

2. **Outcome Sampling is the weakest variant here.** Each iteration samples a single trajectory, so most information sets are updated rarely. After 5 minutes and millions of iterations, exploitability is still ~0.53 — ~1,250× worse than CFR+.

3. **External Sampling is the competitive MCCFR variant.** Unlike OS-MCCFR, it samples the traversing player's actions but traverses *all* opponent actions, dramatically reducing variance. It is the standard MCCFR variant used in practice.

4. **Game size is everything.** On Leduc, full traversal is fast, so there is no reason to use MCCFR. On games like full Texas Hold'em ($10^{14}$ info sets), CFR+ cannot traverse the tree at all, and MCCFR (especially ES variant) becomes the only practical option.

---

## Takeaway for the Thesis

> Monte Carlo methods trade **per-iteration quality** for **per-iteration speed**.
> The crossover point — where sampling beats full traversal — is well above Leduc's size.
> Steps 4–6 (abstraction, deep learning, end-to-end agents) address the scalability problem that CFR variants hit on real-world game sizes.
