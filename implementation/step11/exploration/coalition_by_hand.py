"""
coalition_by_hand.py -- Exploration Day 1 (raw step 11 L106-110): hand-coded coalition
strategies, to see whether a FIXED alliance beats random play and whether BETRAYAL beats a naive
fixed ally.

THE THREE HAND-CODED STRATEGIES
-------------------------------
- random               : uniform over legal actions.
- fixed_ally(a)        : "always help player a" -- prefer placing a's chips; never capture a's
                         piles if avoidable. A loyal (naive) ally.
- betrayer(a, switch)  : help player a for the first `switch` fraction of the game, then flip to
                         treating a as the primary target (capture a, stop helping). Models the
                         form-then-break coalition dynamic that is the heart of the step.

WHAT TO WATCH (raw L110)
------------------------
  Q1: does fixed_ally + its ally dominate random opponents?
  Q2: does betrayer beat a naive fixed_ally in a head-to-head-ish 4-player field?
The primary lesson is behavioral (coalitions form and pay, then get betrayed), not a specific
win rate -- read the DIRECTION, not the digits.

Run from `implementation/step11/exploration/`.  Runtime: seconds-to-a-minute.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Every number is a PREDICTION.
"""

from __future__ import annotations

import numpy as np

import _bootstrap  # noqa: F401
from sls_game import SLSGame, play_game


def random_policy(game, state, rng):
    legal = game.legal_actions(state)
    return legal[int(rng.integers(len(legal)))]


def make_fixed_ally(ally: int):
    """Prefer to (a) place the ally's color when we hold it (HELP), and (b) avoid capturing the
    ally's piles. Fall back to random among the least-harmful legal moves."""
    def policy(game, state, rng):
        legal = game.legal_actions(state)
        me = state.current_player
        if me == ally:  # if I *am* the ally, just avoid self-harm; play random otherwise
            return legal[int(rng.integers(len(legal)))]
        # rank moves: helping the ally best; capturing the ally worst
        def score(a):
            color, target = a
            s = 0.0
            if color == ally:
                s += 2.0                      # placing the ally's chip = HELP
            if target < len(state.piles):
                pile = state.piles[target]
                if len(pile) >= 1 and pile[-1] == color and color == ally:
                    s -= 5.0                  # capturing the ally = betrayal (avoid)
            return s
        best = max(score(a) for a in legal)
        pool = [a for a in legal if score(a) == best]
        return pool[int(rng.integers(len(pool)))]
    return policy


def make_betrayer(ally: int, switch_frac: float = 0.5, horizon: int = 120):
    """Help `ally` early, then betray: after `switch_frac * horizon` turns, target the (former)
    ally -- prefer capturing their piles and stop helping them."""
    def policy(game, state, rng):
        legal = game.legal_actions(state)
        phase_betray = state.turn_count >= switch_frac * horizon

        def score(a):
            color, target = a
            s = 0.0
            captures_ally = (target < len(state.piles)
                             and len(state.piles[target]) >= 1
                             and state.piles[target][-1] == color and color == ally)
            if not phase_betray:
                if color == ally:
                    s += 2.0
                if captures_ally:
                    s -= 5.0
            else:  # betrayal phase
                if captures_ally:
                    s += 3.0                  # now capturing the (ex-)ally is GOOD
                if color == ally:
                    s -= 2.0                  # stop feeding them
            return s
        best = max(score(a) for a in legal)
        pool = [a for a in legal if score(a) == best]
        return pool[int(rng.integers(len(pool)))]
    return policy


def win_rates(game: SLSGame, policies, n_games: int = 300, seed0: int = 0):
    winners = []
    for s in range(n_games):
        final, _ = play_game(game, policies, seed=seed0 + s)
        winners.append(final.winner)
    return np.bincount(np.array(winners), minlength=game.n_players) / n_games


def main():
    print("coalition_by_hand  (PREDICTIONS -- verify on a real run)")
    print("=" * 72)
    game = SLSGame(n_players=4, chips_per_player=7)

    # Q1: P0 & P1 both run fixed_ally toward EACH OTHER, vs random P2, P3.
    p0 = make_fixed_ally(ally=1)
    p1 = make_fixed_ally(ally=0)
    field_q1 = [p0, p1, random_policy, random_policy]
    wr1 = win_rates(game, field_q1)
    print("\nQ1: mutual fixed-ally {P0<->P1} vs random {P2,P3}")
    print(f"    win rates = {np.round(wr1, 3).tolist()}")
    print(f"    PREDICT: P0+P1 combined share > 0.5 (the coalition's ~0.5 fair share) -- the "
          "alliance concentrates wins on the pair. Exact split to verify.")

    # Q2: P0 betrays its ally P1; P1 stays loyally allied to P0; P2,P3 random.
    p0b = make_betrayer(ally=1, switch_frac=0.5)
    p1_loyal = make_fixed_ally(ally=0)
    field_q2 = [p0b, p1_loyal, random_policy, random_policy]
    wr2 = win_rates(game, field_q2)
    print("\nQ2: betrayer P0 (allies P1 early, then turns on P1) vs loyal P1 vs random {P2,P3}")
    print(f"    win rates = {np.round(wr2, 3).tolist()}")
    print(f"    PREDICT: P0 (betrayer) >= P1 (loyal) -- exploiting a coalition then breaking it "
          "beats being the naive partner. Direction is the lesson, not the digits.")


if __name__ == "__main__":
    main()
