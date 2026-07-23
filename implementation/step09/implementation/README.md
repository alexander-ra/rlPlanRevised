# Step 09 — Multi-Agent RL: `implementation/`

The build phase. Every method the raw step asks for, on small self-contained testbeds, wired
so the qualitative MARL results are checkable against ground truth. **Code is written but NOT
executed here** (per [WORKFLOW.md](../../WORKFLOW.md)); run it yourself with the runbook below.

The through-line: **game theory (Steps 02–08) meets learning**. PSRO is the bridge — it reuses
Step 07's exact best-response engine as its oracle and exact NashConv as its progress metric,
so "did MARL converge?" is answered by the *same* exploitability number the CFR/solver steps
used.

---

## Design decisions (and why)

- **Self-contained testbeds, guarded external bridges.** `requirements.txt` has neither
  PettingZoo nor OpenSpiel, and WORKFLOW.md says the core must run on the repo's own code. So
  the primary envs are numpy/torch-only (`matrix_games`, `coop_env`, native `goofspiel`), and
  PettingZoo/OpenSpiel are optional cross-checks that **SKIP** cleanly when absent.
- **Exact where possible.** Matrix games, PSRO's oracle (Kuhn/Leduc/Goofspiel), the meta-Nash
  LP, and LOLA are all exact/tabular — no sampling noise to muddy the qualitative claims. The
  neural methods are deliberately tiny MLPs on one-step tasks: the point is the *phenomenon*
  (CTDE beats IL, comm helps, central critic has lower variance), not throughput. **A GPU is
  not needed at this scale.**
- **Reuse Step 07, don't copy it.** `deps.py` puts `step07/implementation/` on `sys.path`;
  PSRO imports `exact_value`, `best_response_policy`, `nash_gap`, and the policy vocabulary
  directly. The one non-obvious bit — collapsing a meta-Nash *mixture over behavioral policies*
  into a single realization-equivalent behavioral policy so the exact BR engine applies — is
  `mixture_behavioral_policy` (valid by Kuhn's theorem; Kuhn/Leduc have perfect recall).

---

## Module map (→ raw-step lines)

### Testbeds & solvers (numpy-only)

| Module | What | Raw step |
|---|---|---|
| `deps.py` | Path bootstrap: reuse Step 07's `engines`/`best_response`/`policies`. | — |
| `matrix_games.py` | 4 canonical 2×2 games (PD, Matching Pennies, Stag Hunt, Battle of the Sexes) + analytic Nash + NashConv. | L363–378, L451 |
| `goofspiel.py` | Native 2-player point-order Goofspiel; exact value + exact best response **to a mixture**. | L122–129, L432–437 |
| `coop_env.py` | `CoopSignal` (partial-obs referential game + global state) and `ClimbingGame` (IL trap). | L133–138, L426–431, L453, L456 |
| `meta_nash.py` | Meta-strategy solver: zero-sum LP (scipy HiGHS) + fictitious-play fallback; general-sum FP. | L281, L400–405 |

### Learning methods

| Module | What | Raw step |
|---|---|---|
| `learners.py` | Discrete clipped-PPO learner + `IndependentLearners` (the IL 🔴 baseline). | L349–350, L363–378, L387 |
| `maddpg.py` | Centralized critic `Q(s, joint a)` + decentralized actors (discrete, COMA-style counterfactual baseline) + independent-critic comparison. | L351, L380–388, L453 |
| `mappo.py` | PPO with a **centralized value** `V(s)`. | L352, L388–390 |
| `psro.py` | 🔴 PSRO: population + meta-Nash + exact BR oracle. Drivers for EFG (Kuhn/Leduc), matrix, and Goofspiel. | L353, L395–424, L481–485 |
| `commnet.py` | Learned mean-field message channel; ON-vs-OFF comparison. | L354, L426–431, L456 |
| `lola.py` | LOLA on the memory-1 IPD (exact value + nested finite-difference look-ahead). | L250–256 (reading + Math Flag) |
| `qmix.py` | **Bonus, optional:** exact illustration of the monotonic-mixing / IGM property. | L351 reading + Math Flag B |

### Infrastructure

| Module | What |
|---|---|
| `config.py` | `smoke` / `scale` configs + compute reality check + runtime notes. |
| `evaluation.py` | Shared metric helpers + suite runners (matrix / PSRO / coop / LOLA). |
| `tournament.py` | Runnable entry: runs the suites, prints comparison tables, writes `results/<config>_results.json`. |
| `plotting.py` | Guarded matplotlib plots of a results JSON (SKIP if matplotlib absent). |
| `compare_openspiel.py` | Guarded: NashConv(uniform) cross-check on Kuhn/Leduc (validates the BR engine PSRO relies on) + mapping TODOs. |
| `compare_pettingzoo.py` | Guarded: MPE `simple_spread` reachability + attach sketch (no training). |
| `validate.py` | PASS/FAIL/SKIP harness encoding the raw-step targets. |

---

## How to verify (runbook)

Everything runs from this folder. Each module also has a `__main__` self-test.

```bash
# 0. per-module smoke self-tests (fast; some SKIP without torch/scipy)
python matrix_games.py
python meta_nash.py
python goofspiel.py
python coop_env.py
python lola.py
python qmix.py
python psro.py            # PSRO on Kuhn: watch exploitability fall toward 0

# 1. the full validation harness (the load-bearing check; a few minutes)
python validate.py

# 2. the comparison-table runner + results JSON
python tournament.py --config smoke
python tournament.py --config scale        # adds Leduc PSRO (20 iters) + larger coop runs

# 3. optional plots / external cross-checks (all SKIP cleanly if deps absent)
python plotting.py --config smoke
python compare_openspiel.py
python compare_pettingzoo.py
```

### Pass/fail thresholds (targets — verify when you run)

| Check | Target | Source |
|---|---|---|
| Matrix outcomes vs analytic Nash | PD→Defect; MP time-average→(½,½) (last-iterate cycles); Stag Hunt & BoS→a pure NE (all seeds NashConv<0.05) | raw L451 |
| PSRO Kuhn exploitability | → ~0 (`< 0.05` within 15 rounds) | raw L454 |
| PSRO Leduc exploitability | `< 0.5` within 20 iters | raw L455 |
| PSRO Goofspiel exploitability | non-increasing over rounds | raw L432–437 |
| MADDPG central critic variance | central final critic loss `<` independent critic loss | raw L453 |
| Communication (CommNet) | comm ON reward `>>` comm OFF (≈ 1/K) | raw L456 |
| CTDE vs IL (climbing) | MADDPG reward `>` IL reward (IL trapped near the safe 5, MADDPG →optimum 11) | raw L363–378 |
| LOLA on IPD | LOLA return ≈ 3 (cooperate) `>` naive ≈ 1 (defect); and LOLA(lr_opp=0)==naive gradient | raw L250–256 |
| OpenSpiel cross-check | NashConv(uniform) matches within 1e-3 (Kuhn) / 1e-2 (Leduc) | raw L482–485 |

---

## Expected outcomes (predictions, not yet run)

- **Matrix games.** Independent exact-gradient learners **defect** in PD, **cycle** in Matching
  Pennies (the canonical non-stationarity picture: last iterate orbits, time-average →Nash),
  and **converge to one of the pure equilibria** in Stag Hunt / Battle of the Sexes with the
  chosen equilibrium depending on initialization (the selection problem).
- **PSRO.** Exploitability decreases monotone-ish as the population grows; with an *exact* BR
  oracle, double-oracle drives Kuhn to ≈0 and Leduc below 0.5 well within 20 rounds. Goofspiel
  shows the same shrinking-exploitability trend on a "real" simultaneous-move game.
- **CTDE vs IL.** On the climbing game, independent PPO learners get trapped near the safe
  payoff 5 (relative overgeneralization); the centralized-critic learner reaches the optimum
  11. On CoopSignal the centralized critic's regression target is near-deterministic → **much
  lower** final loss than the independent critics.
- **Communication.** CommNet with the channel ON lets the listener track the target (reward
  →~1); with it OFF the listener is stuck at 1/K.
- **LOLA.** Naive-vs-naive →mutual defection (~1); LOLA-vs-LOLA →mutual cooperation (~3). The
  `lr_opp=0` sanity check must exactly reproduce the naive gradient.

---

## Likely to break (and why)

- **PSRO on Leduc is the slow one.** Each round recomputes the new meta row/column via exact
  tree traversals and one full-tree best response per player; cost grows ~quadratically in the
  population size. Keep `leduc_rounds` modest in `smoke`; only push to 20 in `scale`. If it's
  too slow, lower the rounds — the trend is visible early.
- **Matrix-game last iterate ≠ average.** Matching Pennies does **not** converge in the last
  iterate; a check on the *final* profile would wrongly FAIL. `validate.py` checks the
  **time-average** (which does converge). This is the intended lesson, not a bug.
- **Stag Hunt / BoS equilibrium selection.** Different seeds land on different pure equilibria;
  the check only requires reaching *some* listed NE, not a specific one.
- **`mixture_behavioral_policy` correctness rests on perfect recall.** It is valid for
  Kuhn/Leduc/Goofspiel (all perfect-recall). Do not reuse it on an imperfect-recall game
  without re-deriving the realization weighting.
- **Neural results are qualitative.** The tiny MLPs + one-step tasks make the *direction* of
  each effect robust, but exact reward/loss numbers will vary with seed and torch version. The
  checks are inequalities, not equalities, for this reason.
- **Goofspiel exact solvers are exponential.** `best_response_value_vs_mixture` recurses over a
  `(K!)²`-leaf tree; K≤4 is instant-ish, K=5 is the practical ceiling for the exact path.
- **CoopSignal without comm caps IL/MADDPG/MAPPO reward at 1/K** (no channel), so on that env
  those three are compared on **critic variance**, not reward; the reward contrast lives on the
  climbing game and the comm contrast on CommNet. This split is intentional.

---

## Static self-review (what I'd check first when running)

- `torch.as_tensor` dtype: neural modules build tensors as `torch.as_tensor(np.array(x, dtype))`
  (numpy dtype inside `np.array`, not passed positionally to `as_tensor`) — a class of bug I
  specifically fixed in `mappo.py`/`commnet.py`.
- PSRO meta-matrix bookkeeping: `_extend_meta` fills only the new row/col; confirm it agrees
  with a full `_build_meta_from_scratch` on a tiny case if you touch it.
- The EFG policy calling convention is `policy(game, state)` (2 args); Goofspiel's is
  `policy(game, state, player)` (3 args). They are separate vocabularies on separate games —
  don't cross them.
- LOLA gradient signs: gradient **ascent** on each agent's own value; the `lr_opp=0`==naive
  self-test is the guardrail.

---

## Key takeaways

1. **Non-stationarity is the whole problem.** Independent learners cycle (Matching Pennies) or
   miscoordinate (climbing game) precisely because each agent's environment is another learner.
2. **CTDE tames it by centralizing training only.** A critic/value that sees the global state +
   joint actions gives low-variance, near-stationary targets while execution stays
   decentralized (MADDPG, MAPPO).
3. **PSRO is the game-theory bridge.** Population + meta-Nash + best-response oracle = the
   double-oracle method from Steps 02–08 lifted to policies, measured by the *same* exact
   exploitability. This is the thesis-critical connective tissue.
4. **Two more MARL flavors:** learned **communication** (CommNet) solves partial observability
   the critic can't, and **opponent-learning-awareness** (LOLA) reshapes the dynamics so
   self-interested agents cooperate — the seed of dynamic opponent modeling.
