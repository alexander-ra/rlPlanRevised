"""
Shared helpers for the Step 07 exploration scripts (Kuhn Poker).

WHAT THIS IS
------------
A thin analysis layer *on top of* the validated Step 02 Kuhn engine. We import the
engine (never copy it) and add the small pieces the opponent-modeling exploration needs:

  - kuhn_p0_payoff(...)        exact terminal payoff for player 0
  - exact_ev(pol0, pol1)       exact expected value of a strategy profile (no sampling)
  - best_response_value(...)   exact info-set-constrained best response vs a fixed policy
  - train_nash(...)            an approximate Nash policy via the Step 02 CFR trainer
  - play_hand(...)             simulate one hand, returning every decision + the payoff
  - materialize_policy(...)    turn a policy function into an info_set -> [p_pass, p_bet] dict

NOTE (per implementation/WORKFLOW.md): this code is written but NOT executed here.
Run it yourself: `python implementation/step07/exploration/kuhn_tools.py` runs a self-test.

Policy convention
-----------------
A "policy" is a callable `policy(card: int, history: str) -> (p_pass, p_bet)` where the two
probabilities sum to 1. The acting player is implied by `history` (player = len(history) % 2),
and `card` is that player's private card (1=J, 2=Q, 3=K).
"""

import os
import sys
import math
import random
import itertools

# --- Bootstrap: make the Step 02 engine importable (import, never copy) ---------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_STEP02 = os.path.abspath(os.path.join(_HERE, "..", "..", "step02"))
if _STEP02 not in sys.path:
    sys.path.insert(0, _STEP02)

from cfr.kuhn_poker import (  # noqa: E402  (import after sys.path bootstrap)
    PASS, BET, CARD_NAMES, ALL_DEALS,
    get_player, get_info_set, is_terminal, get_terminal_utility, action_to_str,
)

CARDS = [1, 2, 3]  # J, Q, K


# --- Exact payoff -------------------------------------------------------------------
def kuhn_p0_payoff(p0_card: int, p1_card: int, history: str) -> float:
    """Exact terminal utility for PLAYER 0, given both cards and the action history.

    The engine's `get_terminal_utility` is written from the perspective of the player
    *to act* at the terminal node (the CFR convention). We call it with that player and
    flip the sign when that player is player 1, so the result is always player 0's payoff.
    """
    cards = [p0_card, p1_card]
    cur = get_player(history)               # the player "to act" at the terminal node
    u_cur = get_terminal_utility(cards, history, cur)
    return u_cur if cur == 0 else -u_cur


# --- Exact expected value of a strategy profile (no sampling) ------------------------
def exact_ev(policy0, policy1) -> float:
    """Expected value FOR PLAYER 0 of (policy0 vs policy1), averaged over all deals."""
    total = 0.0
    for (c0, c1) in ALL_DEALS:
        total += _ev_node([c0, c1], "", policy0, policy1)
    return total / len(ALL_DEALS)


def _ev_node(cards, history, policy0, policy1) -> float:
    if is_terminal(history):
        return kuhn_p0_payoff(cards[0], cards[1], history)
    player = get_player(history)
    policy = policy0 if player == 0 else policy1
    p_pass, p_bet = policy(cards[player], history)
    ev = 0.0
    if p_pass > 0.0:
        ev += p_pass * _ev_node(cards, history + action_to_str(PASS), policy0, policy1)
    if p_bet > 0.0:
        ev += p_bet * _ev_node(cards, history + action_to_str(BET), policy0, policy1)
    return ev


# --- Exact info-set-constrained best response ---------------------------------------
def _acting_histories(player: int):
    """The (non-terminal) histories at which `player` is to act, in Kuhn."""
    return [h for h in ["", "p", "b", "pb"]
            if (not is_terminal(h)) and get_player(h) == player]


def hero_info_sets(hero: int):
    """List of (card, history) info sets owned by `hero` (6 of them in Kuhn)."""
    return [(card, h) for card in CARDS for h in _acting_histories(hero)]


def _deterministic_policy(assignment):
    """Build a policy callable from an {(card, history): action} dict."""
    def policy(card, history, _a=assignment):
        return (1.0, 0.0) if _a[(card, history)] == PASS else (0.0, 1.0)
    return policy


def best_response_value(hero: int, opp_policy, return_policy: bool = False):
    """Exact best-response value for `hero` against a fixed `opp_policy`.

    Kuhn has only 6 info sets per player, so we simply enumerate all 2**6 = 64 pure
    strategies and take the one with the highest EV. A pure best response always exists,
    so this is exact (and trivially fast).
    """
    infosets = hero_info_sets(hero)
    best_ev = -math.inf
    best_assignment = None
    for combo in itertools.product([PASS, BET], repeat=len(infosets)):
        assignment = {iset: a for iset, a in zip(infosets, combo)}
        hero_pol = _deterministic_policy(assignment)
        if hero == 0:
            hero_ev = exact_ev(hero_pol, opp_policy)
        else:
            hero_ev = -exact_ev(opp_policy, hero_pol)   # player 1's EV = -(player 0's EV)
        if hero_ev > best_ev:
            best_ev = hero_ev
            best_assignment = assignment
    if return_policy:
        return best_ev, best_assignment
    return best_ev


def hero_value(hero: int, hero_policy, opp_policy) -> float:
    """EV for `hero` when playing `hero_policy` against `opp_policy`."""
    if hero == 0:
        return exact_ev(hero_policy, opp_policy)
    return -exact_ev(opp_policy, hero_policy)


# --- Approximate Nash via the Step 02 CFR trainer -----------------------------------
def train_nash(iterations: int = 20000, seed: int = 0):
    """Return (nash_policy_callable, info_set_table) for Kuhn, via Step 02's CFR.

    Deterministic given `seed` (the trainer uses the global `random` module).
    Runtime: well under a second for 20k iterations.
    """
    from cfr.cfr_trainer import KuhnTrainer
    random.seed(seed)
    trainer = KuhnTrainer()
    trainer.train(iterations)
    table = {iset: node.get_average_strategy() for iset, node in trainer.node_map.items()}

    def nash_policy(card, history):
        probs = table.get(get_info_set(card, history), [0.5, 0.5])
        return (probs[PASS], probs[BET])

    return nash_policy, table


# --- Simulation ---------------------------------------------------------------------
def play_hand(cards, policy0, policy1, rng):
    """Play one hand. Returns (decisions, p0_utility, history).

    decisions is a list of dicts, one per action taken:
        {player, card, history, info_set, action}
    `cards` is (p0_card, p1_card). `rng` is a `random.Random` instance (for determinism).
    """
    history = ""
    decisions = []
    while not is_terminal(history):
        player = get_player(history)
        policy = policy0 if player == 0 else policy1
        p_pass, p_bet = policy(cards[player], history)
        norm = p_pass + p_bet
        # defensive normalization (policies should already sum to 1)
        threshold = p_pass / norm if norm > 0 else 0.5
        action = PASS if rng.random() < threshold else BET
        decisions.append({
            "player": player,
            "card": cards[player],
            "history": history,
            "info_set": get_info_set(cards[player], history),
            "action": action,
        })
        history += action_to_str(action)
    return decisions, kuhn_p0_payoff(cards[0], cards[1], history), history


def random_deal(rng):
    """Sample a (p0_card, p1_card) deal uniformly (without replacement)."""
    return tuple(rng.sample(CARDS, 2))


# --- Utilities ----------------------------------------------------------------------
def materialize_policy(policy, players=(0, 1)):
    """Return {info_set: [p_pass, p_bet]} for the info sets owned by `players`."""
    table = {}
    for player in players:
        for (card, history) in hero_info_sets(player):
            p_pass, p_bet = policy(card, history)
            table[get_info_set(card, history)] = [p_pass, p_bet]
    return table


def info_set_label(info_set: str) -> str:
    """Pretty label, e.g. '1pb' -> 'J after pb'."""
    card = CARD_NAMES.get(int(info_set[0]), info_set[0])
    hist = info_set[1:] if len(info_set) > 1 else "(open)"
    return f"{card} | {hist}"


# --- Self-test (run this file directly) ---------------------------------------------
def _selftest():
    print("kuhn_tools self-test")
    print("-" * 40)

    # 1) Payoffs at known terminals (player 0's perspective)
    checks = [
        # (p0_card, p1_card, history, expected_p0_payoff, description)
        (3, 1, "pp", +1, "K vs J, check-check -> P0 wins 1"),
        (1, 3, "pp", -1, "J vs K, check-check -> P0 loses 1"),
        (3, 1, "bp", +1, "P0 bets, P1 folds -> P0 wins 1"),
        (1, 3, "pbp", -1, "P1 bets, P0 folds -> P0 loses 1"),
        (3, 1, "bb", +2, "K vs J, bet-call -> P0 wins 2"),
        (1, 3, "pbb", -2, "J vs K, P0 calls -> P0 loses 2"),
    ]
    for p0c, p1c, hist, expected, desc in checks:
        got = kuhn_p0_payoff(p0c, p1c, hist)
        status = "OK " if abs(got - expected) < 1e-9 else "FAIL"
        print(f"  [{status}] payoff {hist:4s} = {got:+.0f} (want {expected:+d})  {desc}")

    # 2) Nash value: first player (P0) value in Kuhn is the known -1/18.
    nash, _ = train_nash(iterations=30000, seed=0)
    v = exact_ev(nash, nash)
    print(f"\n  exact_ev(Nash, Nash) = {v:+.4f}   (known game value for P0 ~= {-1/18:+.4f})")

    # 3) Best response to Nash should be ~ the game value (Nash is unexploitable).
    br0 = best_response_value(0, nash)
    br1 = best_response_value(1, nash)
    print(f"  BR(P0) vs Nash = {br0:+.4f} ,  BR(P1) vs Nash = {br1:+.4f}")
    print(f"  NashConv-ish (BR0 + (-(-BR1)))... see exploitation_opportunity.py for the proper metric")


if __name__ == "__main__":
    _selftest()
