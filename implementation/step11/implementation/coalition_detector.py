"""
coalition_detector.py -- infer IMPLICIT coalitions from observed So Long Sucker play (raw step 11
L344, L384-424, L548). 🔴 HAND-CODE: this IS the thesis-relevant mechanism.

THE IDEA (Contribution #1: behavioral adaptation, lifted to the social structure)
---------------------------------------------------------------------------------
Step 07 inferred an opponent's HIDDEN HAND from their betting; here we infer who is ALLIED WITH
WHOM from their chip placements. Same Bayesian-flavored principle -- observe actions, update
beliefs -- on a different observation space (raw L424):

  help[i][j] = number of times player i placed player j's colored chip  (an implicit HELP)
  harm[i][j] = number of times player i captured player j's chips        (an implicit HARM)

Net directed support   net[i][j] = help[i][j] - harm[i][j]
Pairwise coalition score  C[i][j] = net[i][j] + net[j][i]   (symmetric: mutual support)

A pair with C[i][j] above a threshold is flagged as an active coalition. Tracking C over turns
gives the coalition FORMATION / DISSOLUTION timeline (raw L543).

This reads directly off `sls_game.MoveEvent`, so it works on hand-crafted logs (for validation)
and on learned self-play games alike.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

from sls_game import MoveEvent


class CoalitionDetector:
    """Accumulates help/harm evidence from a stream of `MoveEvent`s and reports coalition scores."""

    def __init__(self, n_players: int):
        self.n_players = n_players
        self.help_matrix = np.zeros((n_players, n_players))
        self.harm_matrix = np.zeros((n_players, n_players))

    def reset(self):
        self.help_matrix[:] = 0.0
        self.harm_matrix[:] = 0.0

    def update(self, move: MoveEvent):
        """Fold one move's help/harm evidence into the matrices."""
        if move.is_help and move.helped_player >= 0:
            self.help_matrix[move.player][move.helped_player] += 1.0
        if move.captured_by != -1:
            for victim in move.victim_colors:
                if victim != move.captured_by:
                    self.harm_matrix[move.captured_by][victim] += 1.0

    def ingest(self, move_log):
        for mv in move_log:
            self.update(mv)
        return self

    def net_support(self) -> np.ndarray:
        """net[i][j] = help[i][j] - harm[i][j] (directed support from i to j)."""
        return self.help_matrix - self.harm_matrix

    def get_coalition_scores(self) -> np.ndarray:
        """Symmetric pairwise coalition strength C = net + net.T (raw L409-412). Diagonal zeroed."""
        net = self.net_support()
        C = net + net.T
        np.fill_diagonal(C, 0.0)
        return C

    def detect_coalitions(self, threshold: float = 2.0) -> list:
        """Pairs (i, j, score) with mutual coalition score above `threshold` (raw L414-422)."""
        C = self.get_coalition_scores()
        out = []
        for i in range(self.n_players):
            for j in range(i + 1, self.n_players):
                if C[i][j] > threshold:
                    out.append((i, j, float(C[i][j])))
        return sorted(out, key=lambda t: -t[2])

    def strongest_pair(self):
        """The (i, j, score) with the highest coalition score (or None if all <= 0)."""
        C = self.get_coalition_scores()
        best = None
        for i in range(self.n_players):
            for j in range(i + 1, self.n_players):
                if best is None or C[i][j] > best[2]:
                    best = (i, j, float(C[i][j]))
        return best


def coalition_score_from_log(n_players: int, move_log) -> np.ndarray:
    """Convenience: full-game symmetric coalition-score matrix from a completed move log."""
    return CoalitionDetector(n_players).ingest(move_log).get_coalition_scores()


def mean_offdiagonal_coalition(n_players: int, move_log) -> float:
    """A single scalar summary: mean of |C[i][j]| over pairs -- 'how much coalition structure is
    present?'. Higher for games with strong alliances, ~0 for structureless random play. This is
    the metric the training comparison uses (coalition-aware agents should score HIGHER)."""
    C = coalition_score_from_log(n_players, move_log)
    n = n_players
    vals = [abs(C[i][j]) for i in range(n) for j in range(i + 1, n)]
    return float(np.mean(vals)) if vals else 0.0


def coalition_timeline(n_players: int, move_log):
    """Per-turn coalition-score snapshots for the formation/dissolution plot (raw L541-543).
    Returns (turns, scores) where scores[t] is the flattened upper-triangle of C after turn t."""
    det = CoalitionDetector(n_players)
    turns, series = [], []
    pairs = [(i, j) for i in range(n_players) for j in range(i + 1, n_players)]
    for t, mv in enumerate(move_log):
        det.update(mv)
        C = det.get_coalition_scores()
        series.append([C[i][j] for (i, j) in pairs])
        turns.append(t)
    return turns, np.array(series) if series else np.zeros((0, len(pairs))), pairs


# --- hand-crafted validation log (raw L425) --------------------------------------------
def make_cooperative_log(n_players: int = 4, allies=(0, 1), n_helps: int = 5):
    """Synthesize a move log in which `allies` clearly cooperate (repeatedly place each other's
    chips) and occasionally harm the outsiders. Used to check the detector fires on a KNOWN
    coalition (raw Validation L558)."""
    a, b = allies
    log = []
    for _ in range(n_helps):
        log.append(MoveEvent(player=a, color=b, pile_target=0, is_help=True, helped_player=b,
                             captured_by=-1, victim_colors=()))
        log.append(MoveEvent(player=b, color=a, pile_target=0, is_help=True, helped_player=a,
                             captured_by=-1, victim_colors=()))
    outsiders = [p for p in range(n_players) if p not in allies]
    for victim in outsiders:
        log.append(MoveEvent(player=a, color=a, pile_target=0, is_help=False, helped_player=-1,
                             captured_by=a, victim_colors=(victim,)))
    return tuple(log)


def _selftest():
    print("coalition_detector self-test  (PREDICTIONS -- verify on a real run)")
    print("-" * 72)
    log = make_cooperative_log(4, allies=(0, 1), n_helps=5)
    det = CoalitionDetector(4).ingest(log)
    C = det.get_coalition_scores()
    print("  coalition score matrix (allies 0<->1 helped each other 5x each):")
    print("  " + str(np.round(C, 1).tolist()))
    pair = det.strongest_pair()
    print(f"  strongest pair = {pair} (PREDICT (0, 1, ~10.0) -- the cooperating pair)")
    detected = det.detect_coalitions(threshold=2.0)
    print(f"  detected coalitions (>2.0) = {detected} (PREDICT the (0,1) pair present)")
    assert pair[0] == 0 and pair[1] == 1, "detector failed to identify the planted coalition"


if __name__ == "__main__":
    _selftest()
