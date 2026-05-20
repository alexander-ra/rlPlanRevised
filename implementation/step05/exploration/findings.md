# Step 05 — Exploration Findings

Observations from the two-day exploration phase. Numbers come from
[logs/day01_results.json](logs/day01_results.json) and
[logs/day02_results.json](logs/day02_results.json); figures live in
[figures/](figures/).

> _Note on the baseline._ Step 03's MCCFR is written against a custom Leduc
> engine, so its exploitability values aren't directly comparable to OpenSpiel's
> `leduc_poker`. For these exploration scripts the MCCFR baseline is OpenSpiel's
> own external-sampling MCCFR — same game, same exploitability function, honest
> head-to-head. Step 03's implementation remains the conceptual reference and
> the from-scratch target for Phase 4.

---

## 0. OpenSpiel PyTorch Deep CFR bug (and patch)

Before the numbers, the most actionable thing this exploration phase produced:
**OpenSpiel 1.6.12's PyTorch `DeepCFRSolver` does not train its advantage
networks.** [_openspiel_patch.py](_openspiel_patch.py) monkey-patches the fix
at import time; both day scripts pull it in.

The bug, in `open_spiel/python/pytorch/deep_cfr.py:565`:

```python
# Ensure some samples have been gathered.
if len(samples.info_state == 0):
    return None
```

`samples.info_state == 0` is an elementwise boolean array of length
`batch_size_advantage` (128 in our setup). `len(...)` returns 128 — always
truthy — so the `return None` triggers every call, *before* the optimizer step
that actually trains the network. The intended check was
`if len(samples.info_state) == 0:` — which is exactly what line 603 (the same
check inside `_learn_strategy_network`) reads. So in stock OpenSpiel:

- the strategy network *does* train (line 603 is correct),
- the advantage networks *never* train (line 565 is broken),
- `solve()` returns advantage losses that are silently all `None`,
- exploitability stays at random-strategy levels regardless of iteration count.

Reproducing the silent failure: run `day01_deep_cfr.py` with the patch import
commented out. You'll see `adv_loss[0][-1]=nan` across all iterations and
exploitability frozen at ~1.69 for `(64, 64)`.

After patching, advantage losses grow from ~300 to ~1500 across 120 iterations
(the sqrt-iteration weighting in `_learn_advantage_network` means CFR regrets
literally scale up), confirming the optimiser is now running.

Convergence at our budgets still isn't impressive (see §1 below). That's
separate from the bug — it's about the iteration count being well below what
the original Deep CFR paper used.

---

## 1. Day 1 — Deep CFR vs tabular MCCFR

### Setup

- Game: `leduc_poker` (936 info sets, info-state tensor size 30, 3 actions)
- Deep CFR (baseline): `(64, 64)` layers, **120** outer iterations, 40
  traversals/iter, lr 1e-3, `batch_size_advantage=128`,
  `batch_size_strategy=1024`, reservoir memory 1e6.
- Tabular MCCFR: external-sampling, 50 000 iterations, checkpointed every 2 500.

See [day01_deep_cfr.py](day01_deep_cfr.py) for the full hyperparameter list and
[figures/day01_deep_cfr_vs_mccfr.png](figures/day01_deep_cfr_vs_mccfr.png) for
the convergence curves.

### Numbers (final values)

| Method                       | Final exploitability | Wall time |
|------------------------------|---------------------:|----------:|
| Tabular MCCFR (50 000 iter)  |               0.0967 |     68 s |
| Deep CFR `(64, 64)` 120 iter |               1.7002 |     95 s |
| Deep CFR `(32, 32)` 120 iter |               1.1441 |     87 s |
| Deep CFR `(128, 128, 128)`   |               1.4908 |    101 s |

Exploitability is on the OpenSpiel scale (chips lost per round vs a worst-case
adversary; Leduc's game value is bounded by the pot).

### What the numbers say

- **Tabular MCCFR wins decisively at this budget.** 0.097 vs ~1.5. Leduc is
  small enough that explicit regret tables fit and improve faster per second
  than any neural method we tried.
- **Deep CFR is not converged at 120 iterations.** The original paper and
  OpenSpiel's own example script use 400+ iterations. With 120 we see training
  is alive (advantage losses grow from ~300 to ~1500) but the strategy network
  hasn't been distilled from enough advantage-network snapshots to land in the
  Nash neighbourhood. The brief's "Deep CFR reaches comparable exploitability
  with FAR fewer iterations" requires ~3× more iterations than we ran here.
- **Smaller network ≠ worse on Leduc.** `(32, 32)` outperformed `(64, 64)` and
  `(128, 128, 128)` at this iteration budget. Plausibly the smaller network
  benefits from data efficiency: at 120 outer iters × 40 traversals there
  aren't *that* many distinct training samples, and the larger nets are
  underfit. With more iterations the ordering would likely flip — the original
  paper recommends bigger networks for bigger games.
- **Per-iteration cost is high.** A Deep CFR outer iteration with 40
  traversals + advantage retrain + 2 forward passes per node takes ~0.7s on
  CPU, vs ~1.4ms for a tabular MCCFR iteration. So Deep CFR is ~500× more
  expensive per "iteration" on Leduc — but the absolute work per iteration is
  roughly constant in game size for Deep CFR (modulo info-state-tensor cost),
  while tabular MCCFR scales with info-set count. *On a game where the
  tabular method's table doesn't fit, Deep CFR's "expensive" iteration is the
  only option.*

### Network-size sweep

See [figures/day01_network_sizes.png](figures/day01_network_sizes.png). Reading
the three curves, the ordering at 120 iterations is `(32, 32)` <
`(128, 128, 128)` < `(64, 64)` exploitability — but the curves are essentially
*flat* across iterations 30 → 120, which is the strongest signal that the
budget is too small to let the strategy network distil meaningful averages.

---

## 2. Day 2 — NFSP and advantage-network internals

### NFSP on Kuhn

- Hidden layers `(64,)`, episodes 20 000, anticipatory `η = 0.1`.
- Final exploitability: **0.2705** (down from 0.46 at episode 1).
- See [figures/day02_nfsp_kuhn.png](figures/day02_nfsp_kuhn.png).

Kuhn is small enough that even 20 000 self-play episodes pull NFSP into a
reasonable neighbourhood — but compare against tabular CFR on Kuhn, which
reaches exploitability < 1e-3 in ~10 ms.

### NFSP on Leduc

- Hidden layers `(128, 128)`, episodes 50 000, anticipatory `η = 0.1`.
- Final exploitability: **2.46**. Essentially no convergence; the curve drifts
  around 2.5 ± 0.6.
- See [figures/day02_nfsp_leduc.png](figures/day02_nfsp_leduc.png).

This matches the warning in the rawSteps brief and in OpenSpiel's
`nfsp_leduc_pytorch.py` example, which uses **`num_train_episodes=2 × 10⁷`** —
*400× more episodes than our exploration budget*. NFSP on Leduc genuinely
needs millions of episodes to converge. The lesson from running it at our
budget: don't trust NFSP curves below ~1e6 episodes on Leduc.

### Deep CFR vs tabular CFR+ at sampled info states

40-iter Deep CFR action probabilities side-by-side with a 400-iter tabular
CFR+ reference (exploitability ≈ 0.00123) at 8 random Leduc info states. See
[figures/day02_advantage_probe.png](figures/day02_advantage_probe.png).

Total-variation distances per info state (smaller = closer to ground truth):

| Info state (truncated)                    | TV(Deep CFR ↔ CFR+) |
|-------------------------------------------|--------------------:|
| `[Private: 3][Pot: 2][Round1: ]`          | 0.260 |
| `[Private: 0][Pot: 4][Round1: 2]`         | 0.617 |
| `[Private: 1][Pot: 2][Round1: ]`          | 0.195 |
| `[Private: 4][Pot: 2][Round1: 1]`         | 0.281 |
| `[Private: 1][Pot: 4][Round1: 1 2]`       | 0.708 |
| `[Private: 0][Pot: 2][Round1: ]`          | 0.420 |
| `[Private: 2][Pot: 2][Round1: 1]`         | 0.163 |
| `[Private: 0][Round2 Public: 4][Round2: ]`| 0.545 |

Median TV ≈ 0.35. Reading the bars in the figure: the neural policy gets the
*direction* right at most info states (e.g. fold-vs-raise decisions match
CFR+'s sign), but its probabilities are systematically pulled toward uniform —
CFR+ converges to near-pure strategies (0.92 / 0.07 on strong hands) while
Deep CFR at 40 iter is closer to (0.73 / 0.27). This is what MSE training on
noisy CF samples gives you with a small budget: an under-confident smoothing
of the true equilibrium.

### Tabular CFR+ as reference

- 400 iterations of CFR+ → exploitability ≈ **0.00123** in 92 s on Leduc.
- This is ~80× better than our 50 000-iteration MCCFR and ~1400× better than
  Deep CFR @ 120 iter, at comparable wall time.
- CFR+ is the gold standard on small enough games — if the table fits, use it.

---

## 3. Phase 2 questions

**1. What are the three components of Deep CFR?**

- **Advantage networks** — one per player, MLP mapping info-state tensor →
  counterfactual value per action. Trained with MSE against CF values sampled
  by external-sampling MCCFR. Replace the tabular cumulative-regret table.
- **Strategy network** — single MLP trained at the *end* of training (in the
  OpenSpiel implementation) on `(info_state, action_distribution)` pairs
  drawn from a strategy reservoir. This is the final Nash approximation.
- **Reservoir-sampled memory buffers** — one per advantage network plus one
  for the strategy buffer. Each new sample is admitted with the
  uniform-retention property of Vitter (1985) reservoir sampling.

**2. How does NFSP differ architecturally from Deep CFR?**

NFSP comes from the *RL* side, not the CFR side. There are no regrets at all.
Each player runs two networks:

- A **best-response network** trained as DQN (off-policy, target network,
  replay buffer) against the *current opponent's average strategy*.
- An **average-policy network** trained with supervised learning on the
  best-response network's recent actions, kept in a reservoir buffer.

At each step the agent samples from the best-response head with probability
`η` and the average-policy head with probability `1−η`. Convergence to Nash
comes from neural-approximate fictitious play, not regret matching. There is
no MCCFR tree traversal — episodes are played end-to-end in the RL environment
and learning is incremental.

**3. What role does reservoir sampling play? Why not just use all the data?**

Two reasons reservoir sampling is non-negotiable in Deep CFR:

- The **average strategy** is, by definition, the time-average across all
  iterations' strategies. The strategy-network training data must therefore be
  sampled uniformly across iterations — a FIFO or recent-only buffer would
  bias toward late-iteration strategies and break the Cesàro-average argument
  that gives CFR its Nash-convergence guarantee.
- The buffer has a *capacity* limit (`memory_capacity=1e6` in our setup), but
  training generates far more `(info_state, target)` pairs than that.
  Vitter's reservoir algorithm keeps a fixed-size sample that is provably
  uniform over all elements ever inserted.

Same logic for NFSP's average-policy reservoir.

**4. On Leduc, which method converges faster? Which reaches lower
exploitability?**

At the budgets used in this exploration, on Leduc:

- **Lowest exploitability**: tabular CFR+ (0.0012 @ 400 iter, 92 s) ≪
  tabular MCCFR (0.097 @ 50 k iter, 68 s) ≪ Deep CFR (~1.5 @ 120 iter,
  95 s) < NFSP (~2.5 @ 50 k ep, 170 s).
- **Wall-clock convergence speed** (time to reach exploitability 0.5):
  CFR+ ≈ 10 s, MCCFR ≈ 5 s, Deep CFR — never reached at our budget,
  NFSP — never reached at our budget.

The expected ordering at scale (full HUNL, abstracted no-limit) is different:
tabular methods *cannot run at all* because the table doesn't fit, Deep CFR
runs and converges, NFSP runs but typically lands at a worse equilibrium.
Leduc is a *teaching* benchmark; it's small enough that the neural methods
look bad against tabular baselines they were never meant to beat.

---

## 4. Bridge to Phase 3 (Reading) and Phase 4 (Implementation)

- The MSE loss on the advantage network is the *one equation* that makes Deep
  CFR different from tabular MCCFR. Brown et al. Eq. 3 is the Phase-3 math
  flag to master.
- The shape of the info-state tensor matters more than network depth. Leduc's
  built-in 30-dim tensor mixes one-hot cards, one-hot history, and pot size.
  The Phase-4 hand-coded version should mirror that structure and document
  each slice for reuse in Steps 6–8.
- Reservoir sampling is small enough to hand-implement in Phase 4 from
  Vitter (1985) — useful to verify the uniform-retention claim above.
- DREAM's outcome sampling + baseline subtraction (Steinberger 2019) is the
  natural next step *after* a working Deep CFR. Defer to post-November per
  the Know-How First compression in the rawSteps header.
- **File a fix upstream.** The OpenSpiel bug in `_learn_advantage_network`
  is a one-character change (`==` → `)==`). Open a GitHub issue / PR; until
  then keep [_openspiel_patch.py](_openspiel_patch.py) in the import path.
