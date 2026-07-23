"""
evo_games.py -- the symmetric matrix games used by the evolutionary-dynamics experiments
(raw step L118-145, L353-405, Validation L486-488).

WHAT THIS IS
------------
Four canonical symmetric games whose replicator dynamics are analytically known, so the
`replicator.py` simulator can be checked against ground truth:

  - prisoners_dilemma : defection strictly dominates -> the population collapses to all-Defect.
  - hawk_dove         : an interior mixed ESS at p(Hawk) = V/C -> the population converges there.
  - rock_paper_scissors : NO ESS -> the replicator orbits (1/3,1/3,1/3) forever (never converges).
  - stag_hunt         : two pure ESS (basins of attraction) -> the outcome depends on x0.

REUSE (per WORKFLOW.md L322: import, never copy the foundations)
----------------------------------------------------------------
Prisoner's Dilemma and Stag Hunt are taken straight from Step 09's `matrix_games.py` (both are
already symmetric there: B == A.T). Rock-Paper-Scissors and Hawk-Dove are the two games Step 10
adds. Everything is exposed as a single symmetric ROW-payoff matrix `A` (player 0's reward),
plus the 2-population pair (A, B=A.T) for the two-population replicator in `replicator.py`.

CONVENTION
----------
A symmetric game is stored as one square `A` (row-player payoff). For the two-population
replicator, the column player's payoff is `B = A.T` (symmetry). A *population state* is a
probability vector over the strategies.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. numpy-only except for the
optional Step 09 reuse (guarded).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class EvoGame:
    name: str
    A: np.ndarray                       # symmetric row-payoff, shape (n, n)
    action_names: tuple = ()
    zero_sum: bool = False
    ess_reference: str = ""             # analytic ESS / replicator fixed point (ground truth)
    nash_profiles: list = field(default_factory=list)   # symmetric Nash population states x*
    replicator_prediction: str = ""     # what the dynamics SHOULD do (a PREDICTION, per WORKFLOW 0)

    @property
    def n(self) -> int:
        return self.A.shape[0]

    @property
    def B(self) -> np.ndarray:
        """Column-player payoff for the two-population form (symmetric game -> A.T)."""
        return self.A.T.copy()

    def fitness(self, x) -> np.ndarray:
        """Fitness of each pure strategy against population state x: (A x)_i."""
        x = np.asarray(x, dtype=float)
        return self.A @ x

    def avg_fitness(self, x) -> float:
        x = np.asarray(x, dtype=float)
        return float(x @ self.A @ x)


# --- the two games Step 10 adds -----------------------------------------------------
# Rock-Paper-Scissors: antisymmetric, zero-sum, unique Nash = uniform, NO ESS (cycles).
_RPS = np.array([[0.0, -1.0, 1.0],
                 [1.0, 0.0, -1.0],
                 [-1.0, 1.0, 0.0]])

# Hawk-Dove with value V and cost C (V < C -> interior mixed ESS at p(Hawk)=V/C).
# Payoff to the ROW animal: Hawk vs Hawk=(V-C)/2, Hawk vs Dove=V, Dove vs Hawk=0, Dove vs Dove=V/2.
_HD_V, _HD_C = 2.0, 4.0
_HAWK_DOVE = np.array([[(_HD_V - _HD_C) / 2.0, _HD_V],
                       [0.0, _HD_V / 2.0]])


def _rps() -> EvoGame:
    return EvoGame(
        name="rock_paper_scissors",
        A=_RPS.copy(),
        action_names=("Rock", "Paper", "Scissors"),
        zero_sum=True,
        ess_reference="Unique Nash = uniform (1/3,1/3,1/3); NO ESS (interior fixed point is a "
                      "centre, not an attractor).",
        nash_profiles=[[1 / 3, 1 / 3, 1 / 3]],
        replicator_prediction="Orbits around (1/3,1/3,1/3) forever; the last iterate NEVER "
                              "converges (closed orbits under continuous replicator dynamics).",
    )


def _hawk_dove() -> EvoGame:
    p_hawk = _HD_V / _HD_C
    return EvoGame(
        name="hawk_dove",
        A=_HAWK_DOVE.copy(),
        action_names=("Hawk", "Dove"),
        zero_sum=False,
        ess_reference=f"Interior mixed ESS at p(Hawk)=V/C={p_hawk:.3f} (V={_HD_V}, C={_HD_C}).",
        nash_profiles=[[p_hawk, 1.0 - p_hawk]],
        replicator_prediction=f"Converges to the interior ESS x*=({p_hawk:.3f},{1 - p_hawk:.3f}) "
                              "from any interior start.",
    )


# --- the two games reused from Step 09 (with an inline fallback) ---------------------
def _pd_stag_from_step09():
    """Return (PD_A, StagHunt_A) reusing Step 09's `matrix_games` if importable, else inline.

    Step 09's PD and Stag Hunt are already symmetric (B == A.T), so only the row payoff `A` is
    needed for the symmetric replicator dynamics.
    """
    try:
        import deps  # noqa: F401  (puts step09/implementation on sys.path)
        from matrix_games import make_matrix_game
        pd = make_matrix_game("prisoners_dilemma").A
        sh = make_matrix_game("stag_hunt").A
        return pd, sh
    except Exception:  # noqa: BLE001 - fall back to the identical inline payoffs
        pd = np.array([[3.0, 0.0], [5.0, 1.0]])   # matches step09 matrix_games PD
        sh = np.array([[4.0, 0.0], [3.0, 3.0]])   # matches step09 matrix_games Stag Hunt
        return pd, sh


def _prisoners_dilemma() -> EvoGame:
    pd, _ = _pd_stag_from_step09()
    return EvoGame(
        name="prisoners_dilemma",
        A=np.asarray(pd, float),
        action_names=("Cooperate", "Defect"),
        zero_sum=False,
        ess_reference="Defect strictly dominates -> all-Defect x*=(0,1) is the unique ESS.",
        nash_profiles=[[0.0, 1.0]],
        replicator_prediction="Cooperator share -> 0; the population collapses to all-Defect.",
    )


def _stag_hunt() -> EvoGame:
    _, sh = _pd_stag_from_step09()
    return EvoGame(
        name="stag_hunt",
        A=np.asarray(sh, float),
        action_names=("Stag", "Hare"),
        zero_sum=False,
        ess_reference="Two pure ESS (Stag,Stag) payoff-dominant and (Hare,Hare) risk-dominant; "
                      "an unstable interior fixed point separates their basins.",
        nash_profiles=[[1.0, 0.0], [0.0, 1.0]],
        replicator_prediction="Converges to all-Stag OR all-Hare depending on x0 (which basin "
                              "the start lands in).",
    )


_BUILDERS = {
    "prisoners_dilemma": _prisoners_dilemma,
    "hawk_dove": _hawk_dove,
    "rock_paper_scissors": _rps,
    "stag_hunt": _stag_hunt,
}

ALL_GAMES = tuple(_BUILDERS.keys())


def make_evo_game(name: str) -> EvoGame:
    key = name.lower()
    if key not in _BUILDERS:
        raise ValueError(f"Unknown evolutionary game {name!r}; choose from {sorted(_BUILDERS)}")
    return _BUILDERS[key]()


def _selftest():
    print("evo_games self-test")
    print("-" * 60)
    for name in ALL_GAMES:
        g = make_evo_game(name)
        print(f"[{name}] n={g.n} zero_sum={g.zero_sum} actions={g.action_names}")
        print(f"   A=\n{np.round(g.A, 3)}")
        print(f"   ESS: {g.ess_reference}")
        # sanity: each listed symmetric Nash is a replicator fixed point (all played strategies
        # share the same fitness), which we PREDICT here (verify on a real run).
        for xe in g.nash_profiles:
            xe = np.asarray(xe, float)
            f = g.fitness(xe)
            played = xe > 1e-9
            if played.sum() > 1:
                spread = float(f[played].max() - f[played].min())
                print(f"   fixed-point check x*={np.round(xe, 3).tolist()}: fitness spread "
                      f"among played strategies = {spread:.3e} (PREDICT ~0 at a Nash)")
            else:
                print(f"   pure fixed point x*={np.round(xe, 3).tolist()}")


if __name__ == "__main__":
    _selftest()
