"""
sls_endgame.py -- an EXACT solver for the 2-player So Long Sucker endgame, the one exact
correctness anchor for the 4-player engine (raw step 11 L195-207, L382, L557).

WHY THIS EXISTS
---------------
Steps 7-10 evaluated 2-player games EXACTLY (best response / exploitability). No such exact
oracle exists for 4-player FFA (raw L320-329: Nash / exploitability are intractable AND
meaningless there). But De Carufel & Jerade (2024, arXiv:2403.17302) prove the 2-player endgame
of SLS is COMPLETELY solved analytically (their Theorems 1-3). So the 2-player endgame is the
place we can check the engine against ground truth.

WHAT THIS IS (and an honest caveat -- WORKFLOW S0)
--------------------------------------------------
This module computes the exact winner under optimal play by backward-induction MINIMAX over the
2-player game tree of THIS engine's rules (`sls_game.SLSGame`). Because each capture strictly
removes one chip from the game and non-capturing play is bounded by the chips in hand, the
2-player tree is finite, so memoized minimax terminates.

  >>> NOTE / TODO (verify against the paper -- WORKFLOW S0) <<<
  `optimal_winner` is the exact ground truth *for this engine's (simplified) ruleset*. It is NOT
  a transcription of De Carufel & Jerade's Theorems 1-3 (which I have not verified line-by-line).
  The correctness check therefore proves two things: (1) the engine terminates and is internally
  consistent under optimal play, and (2) simulated optimal play matches exhaustive minimax. The
  REMAINING check -- that this engine's endgame outcomes agree with the paper's theorems -- is on
  the "verify when you read it" list in targetedReading/summary.md. Read Section 2-3 of the paper
  and confirm the winning conditions before trusting endgame results.

Keep chip counts SMALL for the exact solver (2-3 chips/player); the tree grows fast.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from functools import lru_cache

from sls_game import SLSGame, SLSState


def _state_key(state: SLSState):
    """A hashable canonical signature of a 2-player position for memoization."""
    return (state.hands, state.piles, state.current_player, state.eliminated, state.done,
            state.winner)


def optimal_winner(game: SLSGame, state: SLSState, _memo: dict | None = None) -> int:
    """Exact winner under optimal play from `state`, by memoized minimax. Both players play to
    WIN (win/loss backward induction). Returns the winning player's index.

    Assumes exactly two non-eliminated players (a 2-player endgame). Raises if called on a
    position with more than two live players (there is no exact solver for N>2 -- that is the
    whole point of the step).
    """
    if _memo is None:
        _memo = {}

    if game.is_terminal(state):
        return state.winner

    alive = [p for p in range(game.n_players) if p not in state.eliminated]
    if len(alive) > 2:
        raise ValueError(
            f"optimal_winner is a 2-PLAYER endgame solver; got {len(alive)} live players "
            f"({alive}). N>2 SLS has no exact solver -- see raw L320-329."
        )

    key = _state_key(state)
    if key in _memo:
        return _memo[key]

    mover = state.current_player
    legal = game.legal_actions(state)
    if not legal:
        # stuck: engine routes the turn onward; emulate by advancing to the other live player
        other = [p for p in alive if p != mover]
        if not other:
            _memo[key] = mover
            return mover
        # No legal move for the mover; the engine's play_game skips them. Model as: the other
        # player is now to move from an equivalent position. Guard against ping-pong via memo.
        from dataclasses import replace
        nxt_state = replace(state, current_player=other[0])
        res = optimal_winner(game, nxt_state, _memo)
        _memo[key] = res
        return res

    # The mover prefers any action whose optimal continuation makes THEM the winner.
    result = None
    for action in legal:
        w = optimal_winner(game, game.apply(state, action), _memo)
        if w == mover:
            result = mover
            break
        result = w  # fall back to whatever the last line yields (the opponent)
    _memo[key] = result
    return result


def optimal_policy_factory(game: SLSGame):
    """A policy that plays the exact minimax-optimal move (win-preserving if one exists).

    Shares one memo across calls so repeated evaluation is cheap. For use as an SLS policy:
    `pol = optimal_policy_factory(game); pol(game, state, rng)`.
    """
    memo: dict = {}

    def policy(g: SLSGame, state: SLSState, rng):
        legal = g.legal_actions(state)
        mover = state.current_player
        winning = [a for a in legal if optimal_winner(g, g.apply(state, a), memo) == mover]
        pool = winning if winning else legal
        return pool[int(rng.integers(len(pool)))]

    return policy


def verify_endgame_consistency(chips_per_player: int = 2, n_trials: int = 20, seed: int = 0):
    """Check that simulated OPTIMAL play from fresh 2-player positions ends with the
    minimax-predicted winner. Returns a dict with pass/fail + per-trial details.

    This is the environment-correctness harness item (raw Validation L557), modulo the paper
    cross-check flagged above.
    """
    import numpy as np
    from dataclasses import replace

    game = SLSGame(n_players=2, chips_per_player=chips_per_player)
    pol = optimal_policy_factory(game)
    rng = np.random.default_rng(seed)

    mismatches = 0
    details = []
    memo: dict = {}
    for t in range(n_trials):
        s0 = game.initial_state()
        predicted = optimal_winner(game, s0, memo)
        # Simulate optimal-vs-optimal with the DETERMINISTIC engine tie-break (apply rng=None),
        # matching how `optimal_winner`'s minimax tree resolves ties. The policy rng only breaks
        # ties among equally-winning MOVES. (play_game now injects a random deadlock tie-break for
        # unbiased N-player evaluation; using it here would spuriously disagree with the minimax on
        # coin-flip tie positions -- see EXECUTION_NOTES.md.)
        s = s0
        while not game.is_terminal(s):
            legal = game.legal_actions(s)
            if not legal:
                nxt = game._next_with_chips([list(h) for h in s.hands], set(s.eliminated),
                                            s.current_player)
                if nxt is None:
                    break
                s = replace(s, current_player=nxt)
                continue
            s = game.apply(s, pol(game, s, rng))     # rng=None inside apply -> deterministic tie-break
        ok = (s.winner == predicted)
        mismatches += 0 if ok else 1
        details.append({"trial": t, "predicted": predicted, "played": s.winner, "ok": ok})
    return {
        "chips_per_player": chips_per_player,
        "n_trials": n_trials,
        "mismatches": mismatches,
        "passed": mismatches == 0,
        "details": details,
    }


def _selftest():
    print("sls_endgame self-test  (PREDICTIONS -- verify on a real run)")
    print("-" * 72)
    game = SLSGame(n_players=2, chips_per_player=2)
    s0 = game.initial_state()
    w = optimal_winner(game, s0)
    print(f"  2-player, 2 chips each: minimax winner from the opening = P{w} "
          f"(a fixed value; note SLS is known to favor certain positions -- verify vs paper)")
    rep = verify_endgame_consistency(chips_per_player=2, n_trials=10, seed=0)
    print(f"  optimal-play vs minimax over 10 openings: mismatches={rep['mismatches']} "
          f"(PREDICT 0 -- simulated optimal play must reach the minimax winner)")


if __name__ == "__main__":
    _selftest()
