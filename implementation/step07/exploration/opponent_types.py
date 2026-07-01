"""
A small "opponent type zoo" for Kuhn Poker (Step 07 exploration).

Each type is a fixed policy `type(card, history) -> (p_pass, p_bet)` (the two probs sum
to 1). These are the *ground-truth* strategies an opponent model will try to infer from
behavior. They are deliberately distinct so their behavioral "fingerprints" look nothing
alike (see behavioral_fingerprints.py).

Cards: 1=J, 2=Q, 3=K. A player is "facing a bet" iff the last action was a bet, i.e. the
history ends in 'b' ("b" or "pb"); otherwise they are checking into an open pot.

NOTE: written but not executed here (see implementation/WORKFLOW.md). The Nash type is
built lazily because it requires running the Step 02 CFR trainer.
"""

from kuhn_tools import train_nash


def _facing_bet(history: str) -> bool:
    return history.endswith("b")


# --- Deterministic archetypes -------------------------------------------------------
def always_call(card: int, history: str):
    """Calling station: never raises, never folds. Checks an open pot, calls any bet."""
    if _facing_bet(history):
        return (0.0, 1.0)   # call
    return (1.0, 0.0)       # check


def loose_aggressive(card: int, history: str):
    """Maniac: always bets / raises (and calls), regardless of hand."""
    return (0.0, 1.0)


def tight_passive(card: int, history: str):
    """Rock: only commits chips with the nuts (K). Bets only K; folds J and Q to a bet.

    This is the most exploitable type: it folds far too often, so a bluff prints money.
    """
    strong = (card == 3)
    if _facing_bet(history):
        return (0.0, 1.0) if strong else (1.0, 0.0)   # call only with K, else fold
    return (0.0, 1.0) if strong else (1.0, 0.0)        # bet only with K, else check


# --- Mixtures (for the "what if the opponent fits no single type?" experiment) -------
def mixture(type_a, type_b, weight_a: float = 0.5):
    """A behavioral mixture: at each decision, play type_a w.p. weight_a, else type_b.

    Returned as a single policy whose action probabilities are the weighted average.
    """
    wb = 1.0 - weight_a

    def mixed(card, history):
        pa = type_a(card, history)
        pb = type_b(card, history)
        return (weight_a * pa[0] + wb * pb[0],
                weight_a * pa[1] + wb * pb[1])

    return mixed


# --- Registry -----------------------------------------------------------------------
# The deterministic types are available immediately. "Nash" is added by helpers below
# because it must be trained first.
DETERMINISTIC_TYPES = {
    "AlwaysCall": always_call,
    "TightPassive": tight_passive,
    "LooseAggressive": loose_aggressive,
}


def make_type_zoo(include_nash: bool = True, nash_iterations: int = 20000, seed: int = 0):
    """Return an ordered dict {name: policy} of the opponent types.

    With include_nash=True, trains a Nash policy via Step 02 CFR and adds it as "Nash".
    """
    zoo = dict(DETERMINISTIC_TYPES)
    if include_nash:
        nash_policy, _ = train_nash(iterations=nash_iterations, seed=seed)
        zoo["Nash"] = nash_policy
    return zoo


# Template for adding your own type (a "play with it" hook):
#
#   def my_type(card, history):
#       # return (p_pass, p_bet) summing to 1
#       ...
#   DETERMINISTIC_TYPES["MyType"] = my_type
