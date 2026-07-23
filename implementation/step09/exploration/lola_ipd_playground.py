"""
lola_ipd_playground.py -- naive learners DEFECT, LOLA learners COOPERATE (Iterated PD).

WHAT IT DOES
------------
The headline LOLA result (Foerster et al. 2018, raw step L231-256): in the Iterated
Prisoner's Dilemma, two NAIVE gradient learners spiral into mutual defection, but two LOLA
learners -- each of which differentiates through the OTHER's learning step -- discover
tit-for-tat-like COOPERATION. We reproduce it exactly on the memory-1 IPD, where the expected
discounted return has a closed form via the stationary Markov chain over outcome pairs (no
sampling, so the contrast is crisp).

Each agent's policy is 5 cooperation probabilities: P(C) at the start and after each of the
four previous outcomes CC / CD / DC / DD. Naive learning ascends its own return; LOLA ascends
its return under the assumption that the opponent will first take one naive gradient step (the
"look-ahead"). We compute the LOLA look-ahead by finite differences so the second-order term
-- the dependence of the opponent's update on OUR parameters -- is captured automatically.

HOW TO PLAY WITH IT (edit CONFIG)
---------------------------------
  gamma      : discount. Cooperation needs a long enough shadow of the future (try 0.8 vs 0.96).
  lr         : agent learning rate.
  lr_opp     : the LOLA look-ahead step size (how far ahead you assume the opponent moves).
  steps      : training steps.

WHAT TO WATCH OUT FOR
---------------------
- This is a DEMO-grade LOLA (nested finite differences for the look-ahead gradient). It is
  correct and deterministic but not the fastest; the point is the qualitative contrast, not
  speed. A cleaner analytic version is in the implementation phase (`lola.py`).
- LOLA cooperation depends on gamma and lr_opp. If you crank gamma down or lr_opp to 0, LOLA
  degenerates to naive learning and you get defection back -- that is expected.
- "Cooperation" is read off the per-step return: ~3 means mutual C, ~1 means mutual D.

HOW TO READ THE RESULTS (PREDICTIONS -- verify by running)
----------------------------------------------------------
- naive vs naive: both per-step returns fall toward ~1 (mutual defection).
- LOLA vs LOLA : both per-step returns rise toward ~3 (mutual cooperation).

RUNTIME: a few seconds (nested finite differences over a 5-dim policy).
"""

from __future__ import annotations

import numpy as np

from _marl_tools import save_json, get_plt, figures_dir

# outcome states, indexed 0=CC, 1=CD, 2=DC, 3=DD  (action 0 = Cooperate).
_SWAP = [0, 2, 1, 3]           # (a1,a2) -> (a2,a1): the opponent's view of the same outcome
_R1 = np.array([3.0, 0.0, 5.0, 1.0])   # agent 1 payoff: CC=3, sucker=0, temptation=5, DD=1
_R2 = np.array([3.0, 5.0, 0.0, 1.0])   # agent 2 payoff (mirror)

CONFIG = {
    "gamma": 0.96,
    "lr": 1.0,
    # The LOLA look-ahead step. At the original default (1.0) the finite-difference LOLA
    # settles into an ASYMMETRIC partial-cooperation fixed point (~1.2 / ~2.5) rather than the
    # headline mutual cooperation -- the look-ahead is too small relative to this IPD's value
    # scale. lr_opp=5.0 robustly reaches near-symmetric cooperation (~2.5-2.9 each) across seeds
    # while lr_opp=0 still degenerates to the naive gradient (the guardrail). See EXECUTION_NOTES.
    "lr_opp": 5.0,
    "steps": 200,
    "eps": 1e-4,
    "seed": 0,
    "save_plot": True,
}


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def _values(theta1, theta2, gamma):
    """Exact per-step discounted returns (V1, V2) of the memory-1 IPD joint policy."""
    p1 = _sigmoid(theta1[1:])                    # coop prob after each state (agent 1 view)
    p2 = _sigmoid(theta2[1:])[_SWAP]             # agent 2's coop prob in agent 1's state order
    P = np.empty((4, 4))
    for s in range(4):
        a, b = p1[s], p2[s]
        P[s] = [a * b, a * (1 - b), (1 - a) * b, (1 - a) * (1 - b)]
    p1_0, p2_0 = _sigmoid(theta1[0]), _sigmoid(theta2[0])
    p0 = np.array([p1_0 * p2_0, p1_0 * (1 - p2_0), (1 - p1_0) * p2_0, (1 - p1_0) * (1 - p2_0)])
    inv = np.linalg.inv(np.eye(4) - gamma * P)
    disc = (1 - gamma) * (p0 @ inv)
    return float(disc @ _R1), float(disc @ _R2)


def _grad(fn, theta, eps):
    """Central finite-difference gradient of scalar fn at theta."""
    g = np.zeros_like(theta)
    for i in range(len(theta)):
        d = np.zeros_like(theta)
        d[i] = eps
        g[i] = (fn(theta + d) - fn(theta - d)) / (2 * eps)
    return g


def _naive_grads(theta1, theta2, gamma, eps):
    g1 = _grad(lambda t: _values(t, theta2, gamma)[0], theta1, eps)
    g2 = _grad(lambda t: _values(theta1, t, gamma)[1], theta2, eps)
    return g1, g2


def _lola_grad1(theta1, theta2, gamma, lr_opp, eps):
    """LOLA gradient for agent 1: d/dtheta1 of V1(theta1, theta2 + lr_opp * naive_grad2).

    The opponent's naive step is recomputed at each perturbed theta1, so the finite
    difference captures LOLA's second-order (through-our-params) term automatically.
    """
    def f(t1):
        g2 = _grad(lambda t: _values(t1, t, gamma)[1], theta2, eps)  # opponent naive step
        t2_hat = theta2 + lr_opp * g2
        return _values(t1, t2_hat, gamma)[0]
    return _grad(f, theta1, eps)


def _lola_grad2(theta1, theta2, gamma, lr_opp, eps):
    def f(t2):
        g1 = _grad(lambda t: _values(t, t2, gamma)[0], theta1, eps)
        t1_hat = theta1 + lr_opp * g1
        return _values(t1_hat, t2, gamma)[1]
    return _grad(f, theta2, eps)


def _run(kind, cfg):
    rng = np.random.default_rng(cfg["seed"])
    theta1 = 0.1 * rng.standard_normal(5)
    theta2 = 0.1 * rng.standard_normal(5)
    hist = {"step": [], "v1": [], "v2": []}
    for t in range(cfg["steps"] + 1):
        v1, v2 = _values(theta1, theta2, cfg["gamma"])
        if t % 5 == 0 or t == cfg["steps"]:
            hist["step"].append(t)
            hist["v1"].append(v1)
            hist["v2"].append(v2)
        if t == cfg["steps"]:
            break
        if kind == "naive":
            g1, g2 = _naive_grads(theta1, theta2, cfg["gamma"], cfg["eps"])
        else:  # lola
            g1 = _lola_grad1(theta1, theta2, cfg["gamma"], cfg["lr_opp"], cfg["eps"])
            g2 = _lola_grad2(theta1, theta2, cfg["gamma"], cfg["lr_opp"], cfg["eps"])
        theta1 = theta1 + cfg["lr"] * g1
        theta2 = theta2 + cfg["lr"] * g2
    return hist, (float(_values(theta1, theta2, cfg["gamma"])[0]),
                  float(_values(theta1, theta2, cfg["gamma"])[1]))


def main():
    cfg = CONFIG
    print("LOLA vs naive learners on the Iterated Prisoner's Dilemma")
    print("=" * 78)

    naive_hist, naive_final = _run("naive", cfg)
    lola_hist, lola_final = _run("lola", cfg)

    print(f"\nnaive vs naive : final per-step return V1={naive_final[0]:.3f}, V2={naive_final[1]:.3f}")
    print(f"  PREDICT: -> ~1.0 each (mutual DEFECTION).")
    print(f"LOLA  vs LOLA  : final per-step return V1={lola_final[0]:.3f}, V2={lola_final[1]:.3f}")
    print(f"  PREDICT: -> ~3.0 each (mutual COOPERATION).")

    path = save_json("lola_ipd_playground.json", {
        "config": cfg,
        "naive": {"history": naive_hist, "final": naive_final},
        "lola": {"history": lola_hist, "final": lola_final},
    })
    print(f"\nsaved {path}")

    if cfg["save_plot"]:
        _plot(naive_hist, lola_hist)


def _plot(naive_hist, lola_hist):
    plt = get_plt()
    if plt is None:
        print("[plot] matplotlib not installed -> skipping PNG.")
        return
    import os
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(naive_hist["step"], naive_hist["v1"], "-o", ms=3, label="naive (agent 1)")
    ax.plot(lola_hist["step"], lola_hist["v1"], "-s", ms=3, label="LOLA (agent 1)")
    ax.axhline(3.0, ls="--", c="g", alpha=0.5, label="mutual cooperation (3)")
    ax.axhline(1.0, ls="--", c="r", alpha=0.5, label="mutual defection (1)")
    ax.set_xlabel("training step")
    ax.set_ylabel("per-step discounted return")
    ax.set_title("IPD: LOLA reaches cooperation where naive learners defect")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    out = os.path.join(figures_dir(), "lola_ipd_playground.png")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    print(f"[plot] wrote {out}")


if __name__ == "__main__":
    main()
