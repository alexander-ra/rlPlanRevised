"""
play_sls.py -- Exploration Day 1: play So Long Sucker and WATCH coalition signals appear
(raw step 11 L87-110).

WHAT IT DOES
------------
Runs full SLS games with simple policies (random / a "greedy-capture" heuristic) and prints:
  1. a readable turn-by-turn TRACE of one game (who placed whose chip, captures, eliminations);
  2. a HELP/HARM tally per game -- the raw signal the coalition detector will formalize
     (help[i][j] = times i placed j's chip; harm[i][j] = times i captured j's chips);
  3. aggregate stats over many games (mean length, winner spread).

The point (raw L99): a coalition is ENCODED in chip-placement -- placing another player's chip is
an implicit HELP; capturing their pile is HARM. Basic policies show little structure; you will
build agents that exploit this signal in the implementation phase.

Run from `implementation/step11/exploration/`.  Runtime: seconds.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Every number is a PREDICTION.
"""

from __future__ import annotations

import numpy as np

import _bootstrap  # noqa: F401
from sls_game import SLSGame, MoveEvent, play_game


# --- policies ---------------------------------------------------------------------------
def random_policy(game, state, rng):
    legal = game.legal_actions(state)
    return legal[int(rng.integers(len(legal)))]


def greedy_capture_policy(game, state, rng):
    """Prefer a move that immediately captures a pile (top two same color after the placement);
    otherwise play randomly. A weak heuristic -- it captures whoever it can, ally or not."""
    legal = game.legal_actions(state)
    capturing = []
    for (color, target) in legal:
        if target < len(state.piles):
            pile = state.piles[target]
            if len(pile) >= 1 and pile[-1] == color:   # placing `color` would match the top
                capturing.append((color, target))
    pool = capturing if capturing else legal
    return pool[int(rng.integers(len(pool)))]


# --- help / harm tally (a preview of coalition_detector.py) -----------------------------
def tally_help_harm(n_players: int, move_log) -> tuple:
    help_m = np.zeros((n_players, n_players))
    harm_m = np.zeros((n_players, n_players))
    for mv in move_log:
        assert isinstance(mv, MoveEvent)
        if mv.is_help:
            help_m[mv.player][mv.helped_player] += 1
        if mv.captured_by != -1:
            # the capturer took prisoners of several colors -> harm to each non-self victim
            for col in mv.victim_colors:
                if col != mv.captured_by:
                    harm_m[mv.captured_by][col] += 1
    return help_m, harm_m


def print_trace(game: SLSGame, seed: int = 0):
    rng = np.random.default_rng(seed)
    state = game.initial_state()
    print(f"\n=== TRACE of one random game (seed={seed}) ===")
    step = 0
    while not game.is_terminal(state) and step < 60:
        legal = game.legal_actions(state)
        if not legal:
            break
        p = state.current_player
        action = random_policy(game, state, rng)
        state = game.apply(state, action)
        mv = state.move_log[-1]
        tag = ""
        if mv.is_help:
            tag += f"  [HELP P{mv.helped_player}]"
        if mv.captured_by != -1:
            tag += f"  [CAPTURE by P{mv.captured_by}, prisoners={list(mv.victim_colors)}]"
        print(f"  t{step:02d}: P{p} places color {mv.color} on pile {mv.pile_target}{tag}")
        step += 1
    print(f"  -> winner: P{state.winner} after {state.turn_count} turns "
          f"(eliminated order emerges from the trace)")


def main():
    print("play_sls  (PREDICTIONS -- verify on a real run)")
    print("=" * 72)
    game = SLSGame(n_players=4, chips_per_player=7)

    print_trace(game, seed=0)

    print("\n=== help/harm tally for one game (seed=1) ===")
    final, rewards = play_game(game, [random_policy] * 4, seed=1)
    help_m, harm_m = tally_help_harm(game.n_players, final.move_log)
    print("  help[i][j] = times i placed j's chip:")
    print("  " + str(help_m.astype(int).tolist()))
    print("  harm[i][j] = times i captured j's chips:")
    print("  " + str(harm_m.astype(int).tolist()))
    print(f"  winner P{final.winner}; rewards={np.round(rewards, 3).tolist()} "
          f"(PREDICT +1 to winner, -1/3 to each loser; help/harm roughly symmetric for random play)")

    print("\n=== aggregate over 200 games (random vs greedy-capture) ===")
    for name, pols in [("all-random", [random_policy] * 4),
                       ("P0 greedy-capture vs 3 random",
                        [greedy_capture_policy] + [random_policy] * 3)]:
        lengths, winners = [], []
        for seed in range(200):
            final, _ = play_game(game, pols, seed=seed)
            lengths.append(final.turn_count)
            winners.append(final.winner)
        warr = np.array(winners)
        no_winner = int((warr < 0).sum())           # games ended by the max_turns tie-break (winner=-1)
        wc = np.bincount(warr[warr >= 0], minlength=4)
        print(f"  {name:32s}: mean_len={np.mean(lengths):5.1f}  win_counts={wc.tolist()} "
              f"no_winner={no_winner} "
              f"(PREDICT random ~uniform [50,50,50,50]; greedy P0 slightly above 50 -- to verify)")


if __name__ == "__main__":
    main()
