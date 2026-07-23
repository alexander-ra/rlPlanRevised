"""
replicator.py -- the replicator dynamics simulator (raw step 10 L353-380, Math Flag L323).

WHAT THIS IS
------------
The 🔴 HAND-CODE evolutionary-game-theory foundation of the step. The replicator equation is
the mathematical formalization of "the strong reproduce, the weak die out" applied to a
population of strategies:

    single population (symmetric game A):   dx_i/dt = x_i * ( f_i(x) - f_bar(x) )
        where the fitness of strategy i is  f_i(x) = (A x)_i
        and the average fitness is          f_bar(x) = x . A x

    two populations (row payoff A, col B):  dx_i/dt = x_i * ( (A y)_i - x.A.y )
                                            dy_j/dt = y_j * ( (B^T x)_j - y.B^T.x )

INTERPRETATION (why the fixed points matter -- the thesis hook)
---------------------------------------------------------------
- A REST POINT of the replicator dynamics (dx/dt = 0 for all played strategies) is exactly a
  point where every played strategy earns the average payoff -> a symmetric NASH equilibrium.
- A rest point that is also an ATTRACTOR (nearby populations flow back to it) is an
  EVOLUTIONARY STABLE STRATEGY (ESS).
- For non-transitive games (Rock-Paper-Scissors) the interior rest point is a CENTRE, not an
  attractor: trajectories orbit it forever and never converge. This is the dynamical-systems
  face of the "self-play cycles on non-transitive games" problem the spinning-top
  decomposition (`spinning_top.py`) diagnoses.

Everything is EXACT numpy (discrete Euler integration of the ODE); no game engine needed.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np


def _normalize(v: np.ndarray) -> np.ndarray:
    v = np.clip(v, 0.0, None)
    s = v.sum()
    if s <= 0.0:
        return np.ones_like(v) / len(v)
    return v / s


def simulate_single(A, x0, T: int = 4000, dt: float = 0.01, renormalize: bool = True):
    """Single-population replicator dynamics on a symmetric game `A` (row payoff).

    Returns the trajectory `xs` (list of length T+1 of population states). Discrete Euler
    step of dx_i = x_i (f_i - f_bar) dt, with defensive renormalization for numerical
    stability (the continuous flow stays on the simplex exactly; the Euler step does not).
    """
    A = np.asarray(A, dtype=float)
    x = _normalize(np.asarray(x0, dtype=float).copy())
    xs = [x.copy()]
    for _ in range(T):
        fitness = A @ x
        avg = float(x @ fitness)
        x = x + x * (fitness - avg) * dt
        x = _normalize(x) if renormalize else np.clip(x, 0.0, None)
        xs.append(x.copy())
    return xs


def simulate_replicator(payoff_A, payoff_B, x0, y0, T: int = 1000, dt: float = 0.01):
    """Two-population replicator dynamics (raw step L353-373 signature).

    x = row-player strategy distribution, y = column-player distribution. Row payoff
    `payoff_A`, column payoff `payoff_B`. Returns (xs, ys) trajectories.
    """
    A = np.asarray(payoff_A, dtype=float)
    B = np.asarray(payoff_B, dtype=float)
    x = _normalize(np.asarray(x0, dtype=float).copy())
    y = _normalize(np.asarray(y0, dtype=float).copy())
    xs, ys = [x.copy()], [y.copy()]
    for _ in range(T):
        fx = A @ y              # fitness of each row strategy vs y
        fy = B.T @ x            # fitness of each column strategy vs x
        avg_fx = float(x @ fx)
        avg_fy = float(y @ fy)
        x = _normalize(x + x * (fx - avg_fx) * dt)
        y = _normalize(y + y * (fy - avg_fy) * dt)
        xs.append(x.copy())
        ys.append(y.copy())
    return xs, ys


def is_rest_point(A, x, tol: float = 1e-6) -> bool:
    """True if `x` is a replicator rest point: all PLAYED strategies share the same fitness
    (so dx_i/dt = 0 for every i with x_i > 0)."""
    A = np.asarray(A, dtype=float)
    x = np.asarray(x, dtype=float)
    fitness = A @ x
    played = x > tol
    if played.sum() <= 1:
        return True
    return float(fitness[played].max() - fitness[played].min()) < 1e-4


def is_ess(A, x, epsilon: float = 1e-3, tol: float = 1e-6) -> bool:
    """Numerical ESS test via the standard invasion condition.

    x* is an ESS iff for every other strategy y: either f(x*, x*) > f(y, x*), or
    f(x*, x*) = f(y, x*) and f(x*, y) > f(y, y) (Maynard Smith). We check the pure-strategy
    invaders y = e_k (necessary; for the small games here it is also sufficient because the
    boundary faces are pure). Returns a boolean PREDICTION to verify.
    """
    A = np.asarray(A, dtype=float)
    x = np.asarray(x, dtype=float)
    n = len(x)
    fxx = float(x @ A @ x)
    for k in range(n):
        ek = np.zeros(n)
        ek[k] = 1.0
        f_kx = float(ek @ A @ x)              # payoff of invader k against resident x
        if f_kx > fxx + tol:
            return False                       # invader does strictly better -> not stable
        if abs(f_kx - fxx) <= tol:
            # tie on the resident: second-order condition on the invader's own turf
            f_xk = float(x @ A @ ek)
            f_kk = float(ek @ A @ ek)
            if f_kk > f_xk + tol:
                return False
    return True


def converged(xs, window: int = 200, tol: float = 1e-3) -> bool:
    """True if the trajectory settled: the last `window` states barely move. RPS should
    report False (it orbits); PD/Hawk-Dove/Stag Hunt should report True."""
    if len(xs) <= window + 1:
        window = max(1, len(xs) // 4)
    tail = np.array(xs[-window:])
    return float(np.max(np.ptp(tail, axis=0))) < tol


def orbit_radius(xs, center, window: int = 200) -> float:
    """Mean distance of the last `window` states from `center` -- a positive, roughly constant
    value signals a persistent orbit (RPS); a value -> 0 signals convergence."""
    center = np.asarray(center, dtype=float)
    tail = np.array(xs[-window:]) if len(xs) > window else np.array(xs)
    return float(np.mean(np.linalg.norm(tail - center, axis=1)))


def _selftest():
    import numpy as _np
    from evo_games import make_evo_game, ALL_GAMES
    print("replicator self-test  (PREDICTIONS -- verify on a real run, WORKFLOW 0)")
    print("-" * 72)
    rng = _np.random.default_rng(0)
    for name in ALL_GAMES:
        g = make_evo_game(name)
        x0 = _normalize(rng.random(g.n) + 0.1)
        xs = simulate_single(g.A, x0, T=6000, dt=0.01)
        conv = converged(xs)
        final = _np.round(xs[-1], 3).tolist()
        note = "converges" if conv else "does NOT converge (orbit)"
        print(f"[{name}] x0={_np.round(x0,3).tolist()} -> final={final}  [{note}]")
        print(f"        PREDICT: {g.replicator_prediction}")
    # RPS-specific: orbit radius should stay clearly positive.
    rps = make_evo_game("rock_paper_scissors")
    xs = simulate_single(rps.A, [0.4, 0.35, 0.25], T=8000, dt=0.01)
    r = orbit_radius(xs, [1 / 3, 1 / 3, 1 / 3])
    print(f"[rps] orbit radius (last 200) = {r:.4f}  (PREDICT clearly > 0: never converges)")


if __name__ == "__main__":
    _selftest()
