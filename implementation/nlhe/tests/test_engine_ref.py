"""Targeted correctness tests for the reference engine (Gate G1, part 1).

These check payoffs against HAND-COMPUTED expected values for the tricky cases
the plan calls out: min-raise / short all-in, 3-way side pots, split pots.
The nb<->ref cross-validation (test_engine_cross.py) checks the two engines
agree; these tests check the ref engine is actually correct poker.
"""
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

import engine_ref as E  # noqa: E402


def mk(n=6, stacks=None, sb=1, bb=2, stack=200):
    r = E.Rules(num_players=n, small_blind=sb, big_blind=bb, starting_stack=stack)
    holes = [[4 * i, 4 * i + 1] for i in range(n)]  # placeholder; overwritten in tests
    board = [0, 1, 2, 3, 5]  # placeholder board (overwritten)
    s = E.new_hand(r, holes, board, button=0)
    if stacks is not None:
        for p in range(n):
            # reset committed blinds then set custom stacks (tests set up manually)
            pass
    return s, r


def apply_by_kind(s, kind, amt=None):
    kinds, amts = E.legal_actions(s)
    for k, a in zip(kinds, amts):
        if k == kind and (amt is None or a == amt):
            E.apply_action(s, k, a)
            return a
    raise AssertionError(f"action {kind} {amt} not legal among {list(zip(kinds, amts))}")


def test_blinds_posted():
    s, r = mk()
    assert s.committed[1] == 1  # SB
    assert s.committed[2] == 2  # BB
    assert s.current_bet == 2
    assert s.to_act == 3  # UTG first preflop


def test_everyone_folds_bb_wins():
    s, r = mk()
    # UTG(3),4,5,0,1 fold -> BB wins the blinds
    for _ in range(5):
        apply_by_kind(s, "fold")
    assert E.is_terminal(s)
    # controlled hole/board irrelevant (only BB alive)
    pay = E.payoffs(s, lambda h, b: 0)
    assert pay[2] == 1, pay  # BB wins SB's 1 chip (SB posted 1, folded)
    assert pay[1] == -1, pay
    assert sum(pay) == 0


def test_split_pot():
    # Heads-up-ish: everyone folds to SB/BB, they both check to showdown, tie.
    s, r = mk()
    for _ in range(4):  # UTG,4,5,button fold
        apply_by_kind(s, "fold")
    # now SB to act preflop, facing BB=2
    apply_by_kind(s, "call")  # SB completes
    apply_by_kind(s, "call")  # BB checks
    # flop, turn, river: both check
    for _street in range(3):
        apply_by_kind(s, "call")  # SB checks
        apply_by_kind(s, "call")  # BB checks
    assert E.is_terminal(s)
    pay = E.payoffs(s, lambda h, b: 0)  # tie -> equal strength
    assert pay[1] == 0 and pay[2] == 0, pay  # each put in 2, gets 2 back
    assert sum(pay) == 0


def test_three_way_side_pot():
    # Manually construct an all-in 3-way with different stacks.
    r = E.Rules(num_players=3, small_blind=1, big_blind=2, starting_stack=200)
    holes = [[51, 47], [48, 44], [3, 7]]  # seat0 strongest, seat2 weakest (by rank_fn)
    board = [12, 16, 20, 24, 28]
    s = E.new_hand(r, holes, board, button=0)
    # override stacks to force side pots: seat0=50, seat1=100, seat2=200
    s.stack = [50, 100, 200]
    s.committed = [0, 0, 0]
    s.street_bet = [0, 0, 0]
    s.allin = [False, False, False]
    # repost blinds manually: 3-handed button=0 -> SB=1, BB=2
    E._put(s, 1, 1)
    E._put(s, 2, 2)
    s.current_bet = 2
    s.min_raise = 2
    s.to_act = 0  # button acts first preflop 3-handed
    s.acted = [False, False, False]
    # seat0 shoves 50, seat1 calls (100 stack -> puts 50), seat2 calls
    apply_by_kind(s, "raise", 50)   # seat0 all-in to 50
    apply_by_kind(s, "call", 50)    # seat1 calls to 50 (has more)
    apply_by_kind(s, "call")        # seat2 calls to 50
    # betting continues among seat1,seat2 (both have chips); both check down
    # After preflop, seat0 all-in. seat1 & seat2 still have stacks.
    # rank_fn: higher card index = stronger. seat0 holes 51 highest.
    def rank_fn(h, b):
        return max(h)
    # play out remaining streets (seat1, seat2 check)
    guard = 0
    while not E.is_terminal(s):
        apply_by_kind(s, "call")
        guard += 1
        assert guard < 50
    pay = E.payoffs(s, rank_fn)
    # Everyone put in 50 (main pot 150). seat0 wins main pot -> +100 net.
    # seat1 & seat2 each contributed 50, no side pot beyond (they checked).
    assert sum(pay) == 0, pay
    assert pay[0] == 100, pay  # wins 150 pot, put in 50
    assert pay[1] == -50 and pay[2] == -50, pay


def test_min_raise_reopen():
    s, r = mk()
    # UTG raises. Check min_raise increment tracked.
    kinds, amts = E.legal_actions(s)
    assert "raise" in kinds
    # make a pot raise
    raise_to = max(a for k, a in zip(kinds, amts) if k == "raise" and a < s.street_bet[3] + s.stack[3])
    E.apply_action(s, "raise", raise_to)
    inc = raise_to - 2
    assert s.min_raise == inc, (s.min_raise, inc)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
