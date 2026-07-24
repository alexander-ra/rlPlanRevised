"""
agents.py -- baseline SLS policies for comparison + the EGTA population (raw step 11 L106-110,
L349, L533-538). 🟡 AI-ASSISTED: standard baselines, verify behavior on a run.

Every policy has the signature `policy(game, state, rng) -> action` (an SLS `(color, pile_target)`
tuple), matching `sls_game.play_game` and the EGTA drivers. The learned agents from
`coalition_mappo` plug in via `sls_ppo.make_ppo_policy`.

BASELINES
- `random_policy`          : uniform over legal actions (the 25%-each reference, raw L536).
- `greedy_capture_policy`  : prefer an immediately-capturing move (weak heuristic).
- `make_fixed_ally(a)`     : always help player a, avoid capturing a's piles (a loyal coalition).
- `make_betrayer(a, ...)`  : help a early, then turn on a (form-then-break coalition dynamics).

These mirror the exploration heuristics but are the CANONICAL versions used by the EGTA meta-game
and the validation harness.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations


def random_policy(game, state, rng):
    legal = game.legal_actions(state)
    return legal[int(rng.integers(len(legal)))]


def greedy_capture_policy(game, state, rng):
    """Prefer a placement that immediately captures (top two of a pile would match), else random."""
    legal = game.legal_actions(state)
    capturing = []
    for (color, target) in legal:
        if target < len(state.piles):
            pile = state.piles[target]
            if pile and pile[-1] == color:
                capturing.append((color, target))
    pool = capturing if capturing else legal
    return pool[int(rng.integers(len(pool)))]


def make_fixed_ally(ally: int):
    """Prefer placing `ally`'s chip (HELP); avoid capturing `ally`'s piles (no betrayal)."""
    def policy(game, state, rng):
        legal = game.legal_actions(state)
        me = state.current_player
        if me == ally:
            return legal[int(rng.integers(len(legal)))]

        def score(a):
            color, target = a
            s = 0.0
            if color == ally:
                s += 2.0
            if target < len(state.piles):
                pile = state.piles[target]
                if pile and pile[-1] == color and color == ally:
                    s -= 5.0
            return s

        best = max(score(a) for a in legal)
        pool = [a for a in legal if score(a) == best]
        return pool[int(rng.integers(len(pool)))]

    return policy


def make_betrayer(ally: int, switch_frac: float = 0.5, horizon: int = 120):
    """Help `ally` for the first `switch_frac` of `horizon` turns, then betray (capture the
    ex-ally, stop feeding them)."""
    def policy(game, state, rng):
        legal = game.legal_actions(state)
        betray = state.turn_count >= switch_frac * horizon

        def score(a):
            color, target = a
            captures_ally = (target < len(state.piles) and state.piles[target]
                             and state.piles[target][-1] == color and color == ally)
            s = 0.0
            if not betray:
                if color == ally:
                    s += 2.0
                if captures_ally:
                    s -= 5.0
            else:
                if captures_ally:
                    s += 3.0
                if color == ally:
                    s -= 2.0
            return s

        best = max(score(a) for a in legal)
        pool = [a for a in legal if score(a) == best]
        return pool[int(rng.integers(len(pool)))]

    return policy


BASELINE_FACTORY = {
    "random": lambda: random_policy,
    "greedy_capture": lambda: greedy_capture_policy,
    "fixed_ally_1": lambda: make_fixed_ally(1),
    "fixed_ally_2": lambda: make_fixed_ally(2),
    "fixed_ally_3": lambda: make_fixed_ally(3),
    "betrayer_1": lambda: make_betrayer(1),
}


def default_baseline_pool():
    """A small, torch-free agent pool for the EGTA meta-game self-tests / smoke run.
    Deliberately a rough SKILL LADDER (random < greedy/ally < betrayer) -- used by the tournament
    comparison. For the cyclicity question (check 5) use `coalition_pool()` instead."""
    names = ["random", "greedy_capture", "fixed_ally_1", "betrayer_1"]
    return names, [BASELINE_FACTORY[n]() for n in names]


def coalition_pool():
    """A pool of COALITION strategies that ally with DIFFERENT partners -- the natural candidate
    for non-transitive (rock-paper-scissors) coalition dynamics (raw L561). Each `fixed_ally_k`
    concentrates help on a different player, so in a shared 4-player game they induce different
    alliance structures; whether that produces a CYCLIC meta-game is exactly the empirical
    question check 5 asks (we report the measured ratio honestly -- no pool is tuned to pass)."""
    names = ["fixed_ally_1", "fixed_ally_2", "fixed_ally_3", "betrayer_1", "random"]
    return names, [BASELINE_FACTORY[n]() for n in names]


def _selftest():
    import numpy as np

    from sls_game import SLSGame, play_game

    print("agents self-test  (PREDICTIONS -- verify on a real run)")
    print("-" * 72)
    game = SLSGame(n_players=4, chips_per_player=5)
    names, pool = default_baseline_pool()
    rng = np.random.default_rng(0)
    final, rewards = play_game(game, pool, seed=0)
    print(f"  pool = {names}")
    print(f"  one 4-way game: winner=P{final.winner}, rewards={np.round(rewards, 2).tolist()} "
          f"(sums to 0; distribution to verify)")


if __name__ == "__main__":
    _selftest()
