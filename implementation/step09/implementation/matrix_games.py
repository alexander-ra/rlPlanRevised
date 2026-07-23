"""
matrix_games.py -- the canonical 2-player matrix-game testbed (raw step L363-378, L451).

WHAT THIS IS
------------
Small, exact, self-contained normal-form games with their KNOWN analytic Nash equilibria, so
every learner's outcome can be checked against ground truth. Prisoner's Dilemma, Matching
Pennies, Stag Hunt, and Battle of the Sexes cover the four qualitatively different cases:
  - dominant-strategy equilibrium (PD),
  - unique mixed equilibrium / cycling (Matching Pennies, zero-sum),
  - multiple pure equilibria with a risk/payoff-dominance tension (Stag Hunt),
  - multiple pure equilibria as a coordination/selection problem (Battle of the Sexes).

CONVENTION
----------
A `MatrixGame` stores two payoff tensors `A` (row/player-0 reward) and `B` (col/player-1
reward), each shape (n0, n1); action 0 is listed first. A *profile* is (x, y) with x a
distribution over player 0's actions and y over player 1's.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. numpy-only.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class MatrixGame:
    name: str
    A: np.ndarray                      # player-0 payoff, shape (n0, n1)
    B: np.ndarray                      # player-1 payoff, shape (n0, n1)
    action_names: tuple = ()
    nash_reference: str = ""           # human-readable analytic Nash (ground truth)
    nash_profiles: list = field(default_factory=list)  # list of (x, y) analytic equilibria

    @property
    def n_actions(self):
        return self.A.shape

    @property
    def zero_sum(self) -> bool:
        return bool(np.allclose(self.A + self.B, 0.0))

    def expected_payoffs(self, x, y):
        """Expected (player-0, player-1) reward under mixed profile (x, y)."""
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        return float(x @ self.A @ y), float(x @ self.B @ y)

    def best_response_value(self, player: int, opp_mix):
        """Best pure response value + action for `player` vs the opponent's mixed strategy."""
        opp_mix = np.asarray(opp_mix, dtype=float)
        if player == 0:
            payoffs = self.A @ opp_mix            # value of each of player 0's actions
        else:
            payoffs = opp_mix @ self.B            # value of each of player 1's actions
        a = int(np.argmax(payoffs))
        return float(payoffs[a]), a

    def nashconv(self, x, y) -> float:
        """Sum of both players' best-response gains at profile (x, y) (0 at a Nash)."""
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        u0, u1 = self.expected_payoffs(x, y)
        br0, _ = self.best_response_value(0, y)
        br1, _ = self.best_response_value(1, x)
        return (br0 - u0) + (br1 - u1)


def _g(name, A, B, actions, nash_reference, nash_profiles):
    return MatrixGame(name, np.array(A, float), np.array(B, float), tuple(actions),
                      nash_reference, nash_profiles)


# Each nash_profiles entry is (x, y) as plain lists (distributions over actions).
_REGISTRY = {
    "prisoners_dilemma": _g(
        "prisoners_dilemma",
        A=[[3, 0], [5, 1]], B=[[3, 5], [0, 1]],
        actions=["Cooperate", "Defect"],
        nash_reference="Unique NE (Defect, Defect)=(1,1); Defect strictly dominates.",
        nash_profiles=[([0.0, 1.0], [0.0, 1.0])],
    ),
    "matching_pennies": _g(
        "matching_pennies",
        A=[[1, -1], [-1, 1]], B=[[-1, 1], [1, -1]],
        actions=["Heads", "Tails"],
        nash_reference="Unique mixed NE (1/2,1/2) each; zero-sum; value 0.",
        nash_profiles=[([0.5, 0.5], [0.5, 0.5])],
    ),
    "stag_hunt": _g(
        "stag_hunt",
        A=[[4, 0], [3, 3]], B=[[4, 3], [0, 3]],
        actions=["Stag", "Hare"],
        nash_reference="Pure NE (Stag,Stag)=(4,4) payoff-dominant and (Hare,Hare)=(3,3) "
                       "risk-dominant; plus a mixed NE.",
        nash_profiles=[([1.0, 0.0], [1.0, 0.0]), ([0.0, 1.0], [0.0, 1.0])],
    ),
    "battle_of_the_sexes": _g(
        "battle_of_the_sexes",
        A=[[2, 0], [0, 1]], B=[[1, 0], [0, 2]],
        actions=["Opera", "Football"],
        nash_reference="Pure NE (Opera,Opera)=(2,1) and (Football,Football)=(1,2); plus a "
                       "mixed NE x=(2/3,1/3), y=(1/3,2/3).",
        nash_profiles=[([1.0, 0.0], [1.0, 0.0]), ([0.0, 1.0], [0.0, 1.0]),
                       ([2 / 3, 1 / 3], [1 / 3, 2 / 3])],
    ),
}

ALL_GAMES = tuple(_REGISTRY.keys())


def make_matrix_game(name: str) -> MatrixGame:
    key = name.lower()
    if key not in _REGISTRY:
        raise ValueError(f"Unknown matrix game {name!r}; choose from {sorted(_REGISTRY)}")
    g = _REGISTRY[key]
    # return a fresh copy so callers can't mutate the registry payoffs
    return MatrixGame(g.name, g.A.copy(), g.B.copy(), g.action_names, g.nash_reference,
                      [(list(x), list(y)) for x, y in g.nash_profiles])


def classify_outcome(game: MatrixGame, x, y, tol: float = 0.05) -> str:
    """Label a learned profile against the analytic equilibria (for validation printouts)."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    for xe, ye in game.nash_profiles:
        if np.allclose(x, xe, atol=tol) and np.allclose(y, ye, atol=tol):
            return f"matches analytic NE x={np.round(xe,3).tolist()}, y={np.round(ye,3).tolist()}"
    nc = game.nashconv(x, y)
    return f"not at a listed NE (NashConv={nc:.3f})"


def _selftest():
    print("matrix_games self-test")
    print("-" * 60)
    for name in ALL_GAMES:
        g = make_matrix_game(name)
        print(f"[{name}] zero_sum={g.zero_sum}  actions={g.action_names}")
        for xe, ye in g.nash_profiles:
            nc = g.nashconv(xe, ye)
            u = g.expected_payoffs(xe, ye)
            ok = "OK " if nc < 1e-9 else "FAIL"
            print(f"   [{ok}] NE x={np.round(xe,3).tolist()} y={np.round(ye,3).tolist()} "
                  f"payoffs={tuple(round(v,3) for v in u)} NashConv={nc:.2e}")


if __name__ == "__main__":
    _selftest()
