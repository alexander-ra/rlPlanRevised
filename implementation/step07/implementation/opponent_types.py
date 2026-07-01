"""
The opponent "type zoo" for Step 07 -- the cast of characters our models try to identify
and exploit. Types are just policies; they double as (a) the actual opponents we play and
(b) the candidate hypotheses the type-based detector reasons over.

Two design choices worth flagging:

  * EPSILON SMOOTHING. Every type mixes a little uniform noise into its action
    distribution (default eps=0.05). This guarantees no type ever assigns probability
    *exactly* zero to a legal action. Without it, a single "impossible" observation would
    drive a candidate's likelihood to 0 and kill it forever -- a classic and brittle
    failure mode of naive Bayesian opponent models. (See the targetedReading notes.)

  * STRENGTH HEURISTICS for Leduc. Leduc types act on a simple hand-strength reading
    (rank, and whether the private card pairs the board once it is public). This keeps the
    types interpretable so the exploitation results are easy to reason about.

Types are deliberately *well specified*: the detector's candidate set is exactly this zoo,
so detection should work when the opponent is one of these. The `mixture` type and the
non-stationary opponents (in tournament.py) probe the misspecified / shifting cases.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from policies import uniform_policy, blend_policies

# Action ids (kept local so this module does not depend on the engine internals directly).
# They match the engines: Kuhn PASS=0/BET=1; Leduc FOLD=0/CHECK_CALL=1/RAISE=2.
_PASS, _BET = 0, 1
_FOLD, _CALL, _RAISE = 0, 1, 2


# --- smoothing wrapper ---------------------------------------------------------------
def _smoothed(base_fn, eps: float = 0.05):
    """Turn a 'preference' function into a legal, normalized, eps-smoothed policy.

    base_fn(game, state, player) returns desired weights over (a superset of) actions;
    we restrict to the legal actions, renormalize, then mix in `eps` of uniform.
    """
    def policy(game, state):
        legal = game.legal_actions(state)
        player = game.current_player(state)
        base = base_fn(game, state, player)
        restricted = {a: max(0.0, float(base.get(a, 0.0))) for a in legal}
        total = sum(restricted.values())
        if total <= 0.0:
            restricted = {a: 1.0 for a in legal}
            total = float(len(legal))
        unif = 1.0 / len(legal)
        return {a: (1.0 - eps) * (restricted[a] / total) + eps * unif for a in legal}
    return policy


# --- Kuhn type preferences (card: 1=J, 2=Q, 3=K) -------------------------------------
def _kuhn_always_pass(game, state, player):
    return {_PASS: 1.0}


def _kuhn_always_bet(game, state, player):
    return {_BET: 1.0}


def _kuhn_tight_passive(game, state, player):
    # Only ever commits chips with the King; passes/folds otherwise. Very exploitable.
    return {_BET: 1.0} if state.cards[player] == 3 else {_PASS: 1.0}


def _kuhn_loose_aggressive(game, state, player):
    # Bets/calls the large majority of the time regardless of card.
    return {_BET: 0.85, _PASS: 0.15}


def _kuhn_thresholdish(game, state, player):
    # A "reasonable but not optimal" player: bets King always, Queen sometimes, Jack rarely.
    card = state.cards[player]
    if card == 3:
        return {_BET: 0.9, _PASS: 0.1}
    if card == 2:
        return {_BET: 0.4, _PASS: 0.6}
    return {_BET: 0.2, _PASS: 0.8}


_KUHN_BASE = {
    "AlwaysPass": _kuhn_always_pass,
    "AlwaysBet": _kuhn_always_bet,
    "TightPassive": _kuhn_tight_passive,
    "LooseAggressive": _kuhn_loose_aggressive,
    "Thresholdish": _kuhn_thresholdish,
}


# --- Leduc type preferences ----------------------------------------------------------
def _leduc_strength(game, state, player):
    """(rank, paired): rank in {0=J,1=Q,2=K}; paired True if the private card pairs the
    board. The board is only known from round 1 onward, so paired is False in round 0."""
    card = state.cards[player]
    rank = game.card_rank(card)
    paired = (state.round >= 1 and rank == game.card_rank(state.community))
    return rank, paired


def _leduc_station(game, state, player):
    return {_CALL: 1.0}  # never folds, never raises


def _leduc_maniac(game, state, player):
    return {_RAISE: 0.8, _CALL: 0.2}  # raises whenever legal, otherwise calls; never folds


def _leduc_rock(game, state, player):
    rank, paired = _leduc_strength(game, state, player)
    strong = paired or rank == 2          # pair or King
    medium = (not paired) and rank == 1   # bare Queen
    if strong:
        return {_RAISE: 0.7, _CALL: 0.3}
    if medium:
        return {_CALL: 0.8, _RAISE: 0.1, _FOLD: 0.1}
    return {_FOLD: 0.7, _CALL: 0.3}       # bare Jack: fold to pressure, else check


def _leduc_loose_passive(game, state, player):
    _, paired = _leduc_strength(game, state, player)
    if paired:
        return {_CALL: 0.5, _RAISE: 0.5}  # only raises the nuts
    return {_CALL: 1.0}                    # otherwise calls everything down, never folds


_LEDUC_BASE = {
    "CallingStation": _leduc_station,
    "Maniac": _leduc_maniac,
    "Rock": _leduc_rock,
    "LoosePassive": _leduc_loose_passive,
}


# --- public API ----------------------------------------------------------------------
def make_type_zoo(game, eps: float = 0.05, nash_iters: int | None = None,
                  include_nash: bool = True, include_random: bool = True) -> dict:
    """Return an ordered dict {type_name: policy} for `game`.

    The zoo is both the opponent cast and the candidate hypothesis set for the type-based
    detector. `nash_iters` controls the CFR budget for the Nash type (None -> a sensible
    default per game). Nash and Random are not eps-smoothed (Nash already mixes; Random is
    uniform by definition).
    """
    if game.name == "kuhn":
        base = _KUHN_BASE
        default_nash_iters = 30000
    elif game.name == "leduc":
        base = _LEDUC_BASE
        default_nash_iters = 4000
    else:
        raise ValueError(f"No type zoo defined for game {game.name!r}")

    zoo = {name: _smoothed(fn, eps) for name, fn in base.items()}

    if include_nash:
        from nash import solve_nash_cached
        nash_policy, _ = solve_nash_cached(game, nash_iters or default_nash_iters)
        zoo["Nash"] = nash_policy

    if include_random:
        zoo["Random"] = uniform_policy()

    return zoo


def make_mixture(types: dict, weights: dict):
    """A behavioral mixture of named types: the weighted-average action distribution.

    This is an *off-grid* opponent (it is generally not equal to any single candidate
    type), so it is useful for probing how the type detector behaves under
    misspecification. Per-hand *switching* mixtures are handled separately as the
    non-stationarity test in tournament.py.
    """
    names = list(weights)
    return blend_policies([types[n] for n in names], [weights[n] for n in names])


def _selftest():
    import random
    from engines import make_game
    from policies import play_hand

    print("opponent_types self-test")
    print("-" * 50)
    for name in ("kuhn", "leduc"):
        game = make_game(name)
        # Skip Nash here (CFR) to keep the smoke fast; just check the rule-based types.
        zoo = make_type_zoo(game, include_nash=False)
        print(f"[{name}] types: {list(zoo)}")
        rng = random.Random(0)
        for tname, pol in zoo.items():
            # Every type must return a legal, normalized distribution at the root.
            s = game.root(game.deals()[0])
            dist = pol(game, s)
            ok = abs(sum(dist.values()) - 1.0) < 1e-9 and all(
                a in game.legal_actions(s) for a in dist)
            print(f"   {tname:16s} root dist sums to 1 & legal: {ok}")
        # smoke: a couple of hands of Maniac/Rock or LA/TP do not crash
        a = list(zoo.values())[0]
        b = list(zoo.values())[-1]
        h = play_hand(game, [a, b], rng.choice(game.deals()), rng)
        print(f"   sample hand utilities = {h.utilities}")


if __name__ == "__main__":
    _selftest()
