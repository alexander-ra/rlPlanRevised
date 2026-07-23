"""
_evo_tools.py -- self-contained numpy helpers for the Step 10 exploration scripts:
the four symmetric games, replicator dynamics, a Hodge transitive/cyclic ratio, effective
diversity, and JSON/plot savers (matplotlib guarded).

Kept independent of the Phase-4 implementation modules on purpose (exploration should run on
its own). The payoffs match `implementation/evo_games.py`.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. numpy-only (+ optional
matplotlib for PNGs).
"""

from __future__ import annotations

import json
import os

import numpy as np

FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")

# Symmetric row-payoff matrices (match implementation/evo_games.py).
GAMES = {
    "prisoners_dilemma": {
        "A": np.array([[3.0, 0.0], [5.0, 1.0]]),
        "actions": ("Cooperate", "Defect"),
        "predict": "Cooperator share -> 0 (defection dominates); converges.",
    },
    "hawk_dove": {
        "A": np.array([[-1.0, 2.0], [0.0, 1.0]]),   # V=2, C=4 -> ESS p(Hawk)=0.5
        "actions": ("Hawk", "Dove"),
        "predict": "Converges to interior ESS p(Hawk)=V/C=0.5.",
    },
    "rock_paper_scissors": {
        "A": np.array([[0.0, -1.0, 1.0], [1.0, 0.0, -1.0], [-1.0, 1.0, 0.0]]),
        "actions": ("Rock", "Paper", "Scissors"),
        "predict": "Orbits (1/3,1/3,1/3) forever; NEVER converges.",
    },
    "stag_hunt": {
        "A": np.array([[4.0, 0.0], [3.0, 3.0]]),
        "actions": ("Stag", "Hare"),
        "predict": "Converges to all-Stag OR all-Hare depending on x0 (two basins).",
    },
}


def normalize(v):
    v = np.clip(np.asarray(v, dtype=float), 0.0, None)
    s = v.sum()
    return v / s if s > 0 else np.ones_like(v) / len(v)


def replicator_step(A, x, dt=0.01):
    """One Euler step of single-population replicator dynamics dx_i = x_i (f_i - f_bar) dt."""
    A = np.asarray(A, dtype=float)
    fitness = A @ x
    avg = float(x @ fitness)
    return normalize(x + x * (fitness - avg) * dt)


def simulate(A, x0, T=6000, dt=0.01):
    x = normalize(x0)
    xs = [x.copy()]
    for _ in range(T):
        x = replicator_step(A, x, dt)
        xs.append(x.copy())
    return np.array(xs)


def converged(xs, window=200, tol=1e-3):
    tail = xs[-window:] if len(xs) > window else xs
    return float(np.max(np.ptp(tail, axis=0))) < tol


def orbit_radius(xs, center, window=200):
    tail = xs[-window:] if len(xs) > window else xs
    return float(np.mean(np.linalg.norm(tail - np.asarray(center, float), axis=1)))


def transitive_ratio_hodge(payoff):
    """||T||/||A_anti|| via the combinatorial-Hodge (ratings-difference) decomposition.
    RPS -> ~0 (pure cyclic); a total skill order -> ~1. See implementation/spinning_top.py for
    the full discussion of why NOT to use a rank-1 SVD here."""
    A = np.asarray(payoff, dtype=float)
    A_anti = (A - A.T) / 2.0
    r = A_anti.sum(axis=1) / A_anti.shape[0]
    T = r[:, None] - r[None, :]
    denom = np.linalg.norm(A_anti, ord="fro")
    return float(np.linalg.norm(T, ord="fro") / denom) if denom > 1e-12 else 0.0


def effective_size(mixture, threshold=0.01):
    m = normalize(mixture)
    active = int(np.sum(m > threshold))
    participation = float(1.0 / np.sum(m ** 2)) if np.sum(m ** 2) > 0 else 0.0
    return {"active": active, "participation_ratio": round(participation, 3)}


def save_json(name, payload):
    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = os.path.join(FIGURES_DIR, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"wrote {path}")
    return path


def get_plt():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        print("[note] matplotlib not installed -> skipping PNG (JSON + stdout still produced).")
        return None
