"""
lola.py -- Learning with Opponent-Learning Awareness on the Iterated Prisoner's Dilemma.

WHAT THIS IS
------------
The reference (numpy-only) implementation of LOLA (Foerster et al. 2018), included because it
is a raw-step reading paper + mandatory Math Flag + thesis Contribution #1 (dynamic opponent
modeling), even though it is not on the strict Phase-4 deliverables checklist.

Setting: the memory-1 IPD, where each agent's policy is 5 cooperation probabilities -- P(C) at
the start and after each previous outcome CC / CD / DC / DD -- and the expected discounted
return has a CLOSED FORM via the stationary Markov chain over outcome pairs (no sampling).

  - NAIVE learning:  theta_i += lr * grad_{theta_i} V_i(theta_1, theta_2).
  - LOLA learning:   theta_1 += lr * grad_{theta_1} V_1(theta_1, theta_2 + lr_opp * grad_{theta_2} V_2),
    i.e. optimize against the opponent's NEXT learning step. The look-ahead is evaluated by
    nested central finite differences, so LOLA's second-order term (the opponent update's
    dependence on OUR parameters -- Math Flag C) is captured automatically. Setting lr_opp=0
    recovers naive learning exactly (the built-in sanity check).

Headline (raw step L250-256): naive-vs-naive -> mutual DEFECTION (return ~1); LOLA-vs-LOLA ->
mutual COOPERATION (return ~3).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. numpy-only.
"""

from __future__ import annotations

import numpy as np

# outcome states 0=CC, 1=CD, 2=DC, 3=DD (action 0 = Cooperate)
_SWAP = [0, 2, 1, 3]                       # (a1,a2) -> (a2,a1): opponent's view of the outcome
_R1 = np.array([3.0, 0.0, 5.0, 1.0])      # agent 1 payoff (CC=3, sucker=0, temptation=5, DD=1)
_R2 = np.array([3.0, 5.0, 0.0, 1.0])      # agent 2 payoff (mirror)

DEFAULT_CONFIG = {"gamma": 0.96, "lr": 1.0, "lr_opp": 1.0, "steps": 200, "eps": 1e-4, "seed": 0}


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def values(theta1, theta2, gamma: float):
    """Exact per-step discounted returns (V1, V2) of the memory-1 IPD joint policy."""
    p1 = _sigmoid(theta1[1:])
    p2 = _sigmoid(theta2[1:])[_SWAP]
    P = np.empty((4, 4))
    for s in range(4):
        a, b = p1[s], p2[s]
        P[s] = [a * b, a * (1 - b), (1 - a) * b, (1 - a) * (1 - b)]
    p1_0, p2_0 = _sigmoid(theta1[0]), _sigmoid(theta2[0])
    p0 = np.array([p1_0 * p2_0, p1_0 * (1 - p2_0), (1 - p1_0) * p2_0, (1 - p1_0) * (1 - p2_0)])
    disc = (1 - gamma) * (p0 @ np.linalg.inv(np.eye(4) - gamma * P))
    return float(disc @ _R1), float(disc @ _R2)


def _grad(fn, theta, eps):
    g = np.zeros_like(theta)
    for i in range(len(theta)):
        d = np.zeros_like(theta)
        d[i] = eps
        g[i] = (fn(theta + d) - fn(theta - d)) / (2 * eps)
    return g


def naive_grads(theta1, theta2, gamma, eps):
    g1 = _grad(lambda t: values(t, theta2, gamma)[0], theta1, eps)
    g2 = _grad(lambda t: values(theta1, t, gamma)[1], theta2, eps)
    return g1, g2


def lola_grad(player, theta1, theta2, gamma, lr_opp, eps):
    """LOLA gradient for `player` (1 or 2). Differentiates through the opponent's naive step."""
    if player == 1:
        def f(t1):
            g2 = _grad(lambda t: values(t1, t, gamma)[1], theta2, eps)
            return values(t1, theta2 + lr_opp * g2, gamma)[0]
        return _grad(f, theta1, eps)
    else:
        def f(t2):
            g1 = _grad(lambda t: values(t, t2, gamma)[0], theta1, eps)
            return values(theta1 + lr_opp * g1, t2, gamma)[1]
        return _grad(f, theta2, eps)


def run(kind: str = "lola", config: dict | None = None):
    """Train two learners of `kind` in {'naive','lola'}. Returns (history, final_returns)."""
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    rng = np.random.default_rng(cfg["seed"])
    theta1 = 0.1 * rng.standard_normal(5)
    theta2 = 0.1 * rng.standard_normal(5)
    hist = {"step": [], "v1": [], "v2": []}
    for t in range(cfg["steps"] + 1):
        v1, v2 = values(theta1, theta2, cfg["gamma"])
        if t % 5 == 0 or t == cfg["steps"]:
            hist["step"].append(t)
            hist["v1"].append(v1)
            hist["v2"].append(v2)
        if t == cfg["steps"]:
            break
        if kind == "naive":
            g1, g2 = naive_grads(theta1, theta2, cfg["gamma"], cfg["eps"])
        elif kind == "lola":
            g1 = lola_grad(1, theta1, theta2, cfg["gamma"], cfg["lr_opp"], cfg["eps"])
            g2 = lola_grad(2, theta1, theta2, cfg["gamma"], cfg["lr_opp"], cfg["eps"])
        else:
            raise ValueError(f"unknown kind {kind!r}; use 'naive' or 'lola'")
        theta1 = theta1 + cfg["lr"] * g1
        theta2 = theta2 + cfg["lr"] * g2
    return hist, values(theta1, theta2, cfg["gamma"])


def validate_cooperation(config: dict | None = None) -> dict:
    """Run naive-vs-naive and LOLA-vs-LOLA; return final returns and the cooperation flag.

    Prediction: naive -> ~1 (defection), LOLA -> ~3 (cooperation), so lola_return > naive_return
    by a clear margin.
    """
    _, naive_final = run("naive", config)
    _, lola_final = run("lola", config)
    return {"naive_return": float(np.mean(naive_final)),
            "lola_return": float(np.mean(lola_final)),
            "lola_cooperates_more": bool(np.mean(lola_final) > np.mean(naive_final) + 0.5)}


def _selftest():
    print("lola self-test")
    print("-" * 60)
    # sanity: LOLA with lr_opp=0 must equal naive learning
    g_naive = naive_grads(np.zeros(5), np.zeros(5), 0.96, 1e-4)[0]
    g_lola0 = lola_grad(1, np.zeros(5), np.zeros(5), 0.96, 0.0, 1e-4)
    close = float(np.max(np.abs(g_naive - g_lola0)))
    print(f"  LOLA(lr_opp=0) vs naive gradient max-diff = {close:.2e} (expect ~0)")
    res = validate_cooperation({"steps": 60})
    print(f"  naive return={res['naive_return']:.3f} (expect ~1), "
          f"LOLA return={res['lola_return']:.3f} (expect ~3)")


if __name__ == "__main__":
    _selftest()
