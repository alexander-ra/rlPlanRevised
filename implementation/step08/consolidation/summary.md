# Step 08 — Summary: Safe Exploitation

**One-pager + learning-log entry.** Phase 5 (consolidation), written from **verified** results.
Full detail + figures + reconciliations: [`report.md`](report.md).

---

## The step in one paragraph

Step 07 built the *sensor* (an opponent model); Step 08 is the *actuator* — turning a model into
profit **without becoming exploitable**. Every safe-exploitation method reduces to the same
program: *maximize EV against the opponent model, subject to a safety floor on your worst-case
value*, solved on one sequence-form LP by constraint generation (Step 07's exact best response is
the worst-case oracle). Five families differ only in the floor: **RNR** (tunable `p`), **Ganzfried**
(≥ Nash value `v*`), **prime-safe** (≥ `v* − ε` for an ε-equilibrium baseline), **SES** (subgame
gadget, ≥ blueprint value locally), **adaptation** (≤ blueprint exploitability). The runs confirm
the theory on fully-solvable **Kuhn** and expose where it stops scaling on **Leduc**.

## What the runs established (verified)

- **Ganzfried is the safe-and-profitable sweet spot on Kuhn.** Safe (worst-case ≥ `v*` within
  1e-3) against *every* opponent, while beating Nash's own EV on every exploitable type — e.g.
  vs `AlwaysPass` **+0.222** (Nash +0.146); `full_br` earns +0.975 but its worst-case collapses to
  **−0.5** (unsafe). This is the central result.
- **Prime-safe/adaptation spend a measured ε = 0.0074 budget** below `v*` (worst-case
  `v* − 0.0079`), earning a bit more than Ganzfried. ε was *measured* from early-stopped CFR, never
  fabricated.
- **Canonical RNR is bang-bang, not a smooth frontier** (safe corner for `p ≤ 0.6`, full BR for
  `p ≥ 0.7`) — a small-game LP-vertex effect; the *naive blend* is the smooth-but-dominated line.
- **Teaching attack: the safety-violation count is the real signal.** `full_br` violated 40/40
  refits, Ganzfried 0/40 — but a *Nash* "revealer" is too gentle to make `full_br` lose in realized
  profit (its bait windfall isn't clawed back). A worst-case/adaptive punisher is needed to show
  that in profit.
- **Leduc headline — global safe-exploitation does not converge; SES does.** Ganzfried/prime-safe/
  adaptation all **hit the 40-iteration cap unsafe** (worst-case −0.64…−1.33); the **subgame method
  converged** (194–350 iters) and stayed near-safe (worst-case ≈ −0.13) while extracting +0.25…+0.68
  vs weak types. The global-vs-local safety gap, measured at Leduc scale.

## Prediction misses worth remembering

1. **"RNR sweep is monotone"** → it is **bang-bang** in Kuhn (vertex switch); dominance holds only
   at the safe corner. 2. **"Ganzfried safe on Leduc"** → **fails within a practical iteration cap**
   (constraint generation doesn't converge). Both were the exact spots the pre-run "likely to break"
   list flagged; the human hardened the solver (feasibility slack, infeasibility handling, iteration
   caps, a bounded Leduc driver) in response.

## Numbers to trust

Kuhn game value −0.0556 (≈ −1/18 ✓); Leduc −0.0862. Runtimes: Kuhn 1.4 s (smoke) / 10.3 s (scale);
Leduc minutes (SES cells 10–79 s). All CPU/LP-bound — GPU irrelevant, as predicted.

## Still open

- **N-player safety** — the `v*` anchor is 2p-zero-sum only (thesis Contribution #2).
- **Scalable safety** — adopt the exact one-shot dual-LP *or* commit to local/subgame safety; the
  Leduc non-convergence is direct evidence for the latter.
- **SES residual exploitability** (0.04 > 0.01 tol) — gadget-to-blueprint vs tolerance vs pin leak?
- **Not yet captured:** `validate.py` PASS/FAIL and the OpenSpiel cross-check — re-run to close.

---

## Learning-log entry

> **Step 08 — Safe Exploitation.** Built one sequence-form LP + constraint-generation engine and
> five safe-exploitation solvers (RNR, Ganzfried, prime-safe, SES subgame, adaptation) on top of
> Step 07's engines/best-response/Nash. **Verified on Kuhn:** Ganzfried is safe vs every opponent
> and beats Nash's EV on every exploitable type (+0.222 vs AlwaysPass), where full best response
> earns more (+0.975) but is wildly exploitable (worst-case −0.5); prime-safe/adaptation legitimately
> use a *measured* ε = 0.0074 budget below `v*`. **Two instructive misses:** canonical RNR is
> bang-bang (not a smooth frontier) in a game this small, and — the headline — on **Leduc** the
> *global* solvers fail to converge within a practical iteration cap (worst-case −0.64…−1.33) while
> the **subgame method (SES) converges** and stays near-safe. That is the global-vs-local safety
> theory→practice gap made empirical, and the concrete argument for real-time subgame methods and/or
> an exact dual-LP. The teaching attack showed the safety-violation count (full_br 40, Ganzfried 0)
> is a truer signal than realized profit against a gentle Nash revealer. Everything is 2p-zero-sum;
> the N-player extension is the open thesis problem. Next: close `validate.py`/OpenSpiel, resolve the
> SES residual exploitability, and re-run Leduc global solvers with the exact dual-LP or a larger cap.
