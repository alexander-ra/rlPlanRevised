"""
exploration/luck_vs_skill_coinflip.py

PROBE (the heart of the whole step): why return-to-go conditioning fails in a STOCHASTIC world,
in the smallest possible example -- a one-step bandit, pure numpy, no torch.

Setup (a Paster-style luck trap):
  - Action A ("skilled/safe") : deterministic reward = 0.5.
  - Action B ("lucky/risky")  : reward = 1.0 with prob 0.4, else 0.0  ->  E[B] = 0.4 < 0.5.
  So the SKILLED choice is A (higher expected value). But the only way to ever see a return of
  1.0 is to take B and GET LUCKY.

A Decision Transformer conditions its action on the desired return-to-go. If we ask it for the
highest return seen (1.0), the ONLY trajectories that achieved it took action B. So return
conditioning on "aim for 1.0" learns "take B" -- it chases LUCK, not SKILL, and picks the action
with the WORSE expected value. That is exactly the failure ARDT is built to avoid.

We reproduce this by collecting uniform-random data and doing "return-conditioned behavior
cloning": P(action | return-to-go bucket). Everything is exact/frequency-based.

PREDICTION (verify in the run session):
  - P(action=B | return-to-go = 1.0)  ~ 1.00   (conditioning on the lucky return -> risky action)
  - The expected-value-optimal action is A. So high-return conditioning is MISALIGNED with skill.
"""

from __future__ import annotations

import numpy as np


def simulate(n: int = 200000, p_win_B: float = 0.4, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    actions = rng.integers(0, 2, size=n)          # 0 = A (safe), 1 = B (risky)
    rewards = np.where(
        actions == 0,
        0.5,                                       # A: deterministic 0.5
        (rng.random(n) < p_win_B).astype(float),   # B: 1.0 w.p. p_win_B else 0.0
    )
    return {"actions": actions, "rewards": rewards}


def return_conditioned_bc(data: dict, target_return: float, tol: float = 1e-6) -> dict:
    """Frequency estimate of P(action | return-to-go == target_return)."""
    a, r = data["actions"], data["rewards"]
    sel = np.abs(r - target_return) <= tol
    if sel.sum() == 0:
        return {"count": 0, "p_A": float("nan"), "p_B": float("nan")}
    chosen = a[sel]
    return {"count": int(sel.sum()),
            "p_A": float((chosen == 0).mean()),
            "p_B": float((chosen == 1).mean())}


def main():
    print("luck_vs_skill_coinflip probe -- predictions only (numpy, no torch)")
    print("-" * 66)
    data = simulate()
    ev_A, ev_B = 0.5, data["rewards"][data["actions"] == 1].mean()
    print(f"empirical E[A]={ev_A:.3f}  E[B]={ev_B:.3f}  -> SKILLED (EV-optimal) action = "
          f"{'A' if ev_A > ev_B else 'B'}")

    for R in (0.0, 0.5, 1.0):
        res = return_conditioned_bc(data, R)
        print(f"\ncondition on return-to-go = {R:.1f}  (n={res['count']}):")
        print(f"  P(action=A|R)={res['p_A']:.2f}   P(action=B|R)={res['p_B']:.2f}")
        if R == 1.0:
            print("  ^ conditioning on the LUCKY high return -> the RISKY action B, "
                  "even though A is EV-optimal. This is the luck-vs-skill trap ARDT fixes.")


if __name__ == "__main__":
    main()
