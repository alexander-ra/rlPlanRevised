"""Pure-Python 6-max No-Limit Hold'em reference engine.

This is the readable *specification by code*. `engine_nb.py` reimplements the
identical rules as numba kernels for speed; Gate G1 cross-validates them on
10k random action-scripted playouts.

Conventions
-----------
- Seats 0..N-1. Button fixed at seat 0 for training (positions are relative;
  evaluation rotates seats externally). SB = seat 1, BB = seat 2, first to act
  preflop = seat 3 (or wraps for short-handed). Postflop first to act = first
  non-folded, non-allin seat clockwise from the button.
- Chips are integers. Default 200-chip (100bb) stacks, blinds 1/2, no ante.
- Abstract actions (indices): 0 FOLD, 1 CHECK/CALL, then raise sizes from the
  abstraction config (pot fractions), then ALLIN as the last index. Concrete
  raise amounts are computed from the live pot here in the engine.
- Payoff = net chips (final - committed) per seat, summing to zero.

Betting rules implemented: min-raise (raise increment >= last increment, BB
preflop), short all-ins do NOT reopen action, uncalled bets are returned, side
pots by contribution level, odd chips to the earliest seat left of the button.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

FOLD = 0
CALL = 1  # check or call

# Result of enumerating legal actions: parallel lists of (kind, to_amount).
# kind: 'fold' | 'call' | 'raise'  (allin is a 'raise' whose to == stack cap)


@dataclass
class Rules:
    num_players: int = 6
    starting_stack: int = 200
    small_blind: int = 1
    big_blind: int = 2
    ante: int = 0
    raise_fractions: tuple = (1.0,)
    include_allin: bool = True
    use_preflop_open: bool = False
    preflop_open_bb: float = 2.25
    max_raises_per_street: int = 2


@dataclass
class State:
    rules: Rules
    button: int = 0
    stack: List[int] = field(default_factory=list)       # remaining chips
    committed: List[int] = field(default_factory=list)    # total in pot this hand
    street_bet: List[int] = field(default_factory=list)    # in pot this street
    folded: List[bool] = field(default_factory=list)
    allin: List[bool] = field(default_factory=list)
    acted: List[bool] = field(default_factory=list)        # acted since last raise
    street: int = 0                # 0 pre,1 flop,2 turn,3 river
    to_act: int = 0
    current_bet: int = 0           # max street_bet this street
    min_raise: int = 0             # minimum raise INCREMENT
    raises_this_street: int = 0
    board: List[int] = field(default_factory=list)         # up to 5 ints
    holes: List[List[int]] = field(default_factory=list)   # [seat][2]
    finished: bool = False

    def clone(self) -> "State":
        s = State(self.rules)
        s.button = self.button
        s.stack = self.stack[:]
        s.committed = self.committed[:]
        s.street_bet = self.street_bet[:]
        s.folded = self.folded[:]
        s.allin = self.allin[:]
        s.acted = self.acted[:]
        s.street = self.street
        s.to_act = self.to_act
        s.current_bet = self.current_bet
        s.min_raise = self.min_raise
        s.raises_this_street = self.raises_this_street
        s.board = self.board[:]
        s.holes = [h[:] for h in self.holes]
        s.finished = self.finished
        return s


def new_hand(rules: Rules, holes, board, button=0) -> State:
    """Create a fresh hand. holes: [N][2], board: list of 5 ints (dealt lazily
    by street via `street`). Blinds posted."""
    n = rules.num_players
    s = State(rules)
    s.button = button
    s.stack = [rules.starting_stack] * n
    s.committed = [0] * n
    s.street_bet = [0] * n
    s.folded = [False] * n
    s.allin = [False] * n
    s.acted = [False] * n
    s.street = 0
    s.board = list(board)
    s.holes = [list(h) for h in holes]
    # antes
    if rules.ante:
        for p in range(n):
            _put(s, p, min(rules.ante, s.stack[p]))
        # antes are dead money; reset street_bet so they don't count as "to call"
        for p in range(n):
            s.street_bet[p] = 0
    sb = (button + 1) % n
    bb = (button + 2) % n
    _put(s, sb, min(rules.small_blind, s.stack[sb]))
    _put(s, bb, min(rules.big_blind, s.stack[bb]))
    s.current_bet = rules.big_blind
    s.min_raise = rules.big_blind
    s.raises_this_street = 0
    s.to_act = (button + 3) % n if n > 3 else (button + 1) % n
    # skip any all-in (short blind) players
    s.to_act = _next_to_act(s, s.to_act, include_current=True)
    return s


def _put(s: State, p: int, amt: int):
    amt = min(amt, s.stack[p])
    s.stack[p] -= amt
    s.committed[p] += amt
    s.street_bet[p] += amt
    if s.stack[p] == 0:
        s.allin[p] = True


def _active(s: State, p: int) -> bool:
    return not s.folded[p] and not s.allin[p]


def _next_to_act(s: State, start: int, include_current=False) -> int:
    n = s.rules.num_players
    p = start
    for i in range(n):
        q = (start + i) % n
        if i == 0 and not include_current:
            continue
        if _active(s, q):
            return q
    return -1


def legal_actions(s: State):
    """Return (kinds, amounts): kind in {'fold','call','raise'}; amount = chips
    the actor's street_bet becomes (the 'raise-to'/call-to). Deduped."""
    r = s.rules
    p = s.to_act
    kinds, amounts = [], []
    call_to = s.current_bet
    call_amt = call_to - s.street_bet[p]
    stack = s.stack[p]
    max_to = s.street_bet[p] + stack  # all-in "to"

    # fold only if facing a bet
    if call_amt > 0:
        kinds.append("fold")
        amounts.append(0)
    # check/call (call is capped by stack -> all-in call)
    kinds.append("call")
    amounts.append(min(call_to, max_to))

    # raises
    can_raise = (stack > call_amt) and (s.raises_this_street < r.max_raises_per_street)
    if can_raise:
        pot = sum(s.committed)  # total pot before this action
        raise_tos = []
        # NB: use int(x+0.5) truncation to match engine_nb exactly (Python's
        # round() is banker's rounding and would diverge).
        if (r.use_preflop_open and s.street == 0
                and s.current_bet == r.big_blind and s.raises_this_street == 0):
            # preflop open: fixed size in BB
            open_to = int(r.preflop_open_bb * r.big_blind + 0.5)
            raise_tos.append(open_to)
            for f in r.raise_fractions:
                raise_tos.append(s.current_bet + int(f * (pot + call_amt) + 0.5))
        else:
            for f in r.raise_fractions:
                raise_tos.append(s.current_bet + int(f * (pot + call_amt) + 0.5))
        # min raise legal 'to'
        min_to = s.current_bet + max(s.min_raise, r.big_blind - s.current_bet)
        min_to = s.current_bet + s.min_raise
        seen = set()
        for rt in raise_tos:
            rt = max(rt, min_to)
            rt = min(rt, max_to)
            if rt <= s.current_bet:  # not a real raise
                continue
            if rt in seen:
                continue
            seen.add(rt)
            kinds.append("raise")
            amounts.append(rt)
    # all-in (as a raise to max_to) if it raises and not already included
    if r.include_allin and stack > 0:
        if max_to > s.current_bet and max_to not in amounts:
            # only add as raise if it exceeds current bet (a raise); an all-in
            # that only calls is already the 'call' action
            if s.raises_this_street < r.max_raises_per_street or True:
                # 4th-raise-allin-only: all-in always allowed as the shove
                kinds.append("raise")
                amounts.append(max_to)
    return kinds, amounts


def apply_action(s: State, kind: str, to_amount: int):
    """Apply a concrete action and advance state (may finish the hand)."""
    r = s.rules
    p = s.to_act
    if kind == "fold":
        s.folded[p] = True
    elif kind == "call":
        _put(s, p, to_amount - s.street_bet[p])
    elif kind == "raise":
        inc = to_amount - s.current_bet
        _put(s, p, to_amount - s.street_bet[p])
        # a full raise (>= min_raise) reopens action; short all-in does not
        if inc >= s.min_raise:
            s.min_raise = inc
            for q in range(r.num_players):
                if q != p and _active(s, q):
                    s.acted[q] = False
        s.current_bet = max(s.current_bet, s.street_bet[p])
        s.raises_this_street += 1
    s.acted[p] = True

    # everyone but one folded -> hand ends immediately
    if _num_alive(s) <= 1:
        _return_uncalled(s)
        s.finished = True
        return

    # advance
    if _betting_closed(s):
        _advance_street(s)
    else:
        nxt = _next_to_act(s, p)
        s.to_act = nxt
        if nxt == -1:
            _advance_street(s)


def _betting_closed(s: State) -> bool:
    # closed when every active player has acted and matched current_bet
    for p in range(s.rules.num_players):
        if _active(s, p):
            if not s.acted[p] or s.street_bet[p] != s.current_bet:
                return False
    return True


def _num_alive(s: State) -> int:
    return sum(0 if s.folded[p] else 1 for p in range(s.rules.num_players))


def _return_uncalled(s: State):
    """Return the uncalled portion of the top street bet to its owner.

    'second' is the second-highest street_bet counting DUPLICATES: if two or
    more players match the top bet, it is fully called and nothing is returned.
    """
    n = s.rules.num_players
    top = -1
    second = -1
    for p in range(n):
        v = s.street_bet[p]
        if v > top:
            second = top
            top = v
        elif v > second:
            second = v
    if top > second and second >= 0:
        for p in range(n):
            if s.street_bet[p] == top:
                refund = top - second
                s.stack[p] += refund
                s.committed[p] -= refund
                s.street_bet[p] = second
                break


def _advance_street(s: State):
    _return_uncalled(s)
    # hand ends if <=1 alive
    if _num_alive(s) <= 1:
        s.finished = True
        return
    # if <=1 active (rest all-in), run out remaining streets to showdown
    n = s.rules.num_players
    for p in range(n):
        s.street_bet[p] = 0
        s.acted[p] = False
    s.current_bet = 0
    s.min_raise = s.rules.big_blind
    s.raises_this_street = 0
    if s.street == 3:
        s.finished = True
        return
    s.street += 1
    active_cnt = sum(1 for p in range(n) if _active(s, p))
    first = _next_to_act(s, (s.button + 1) % n, include_current=True)
    if active_cnt <= 1 or first == -1:
        # no more betting possible; recurse to deal out remaining streets
        _advance_street(s)
        return
    s.to_act = first


def is_terminal(s: State) -> bool:
    return s.finished


def payoffs(s: State, rank_fn) -> List[int]:
    """Net chips per seat at terminal. rank_fn(hole2, board_list)->int strength.

    Board must be complete enough for showdown (5 cards) when >1 alive.
    """
    n = s.rules.num_players
    contrib = s.committed[:]
    payoff = [-c for c in contrib]
    alive = [p for p in range(n) if not s.folded[p]]
    if len(alive) == 1:
        payoff[alive[0]] += sum(contrib)
        return payoff
    strengths = {p: rank_fn(s.holes[p], s.board) for p in alive}
    levels = sorted(set(c for c in contrib if c > 0))
    prev = 0
    for lvl in levels:
        contributors = [p for p in range(n) if contrib[p] >= lvl]
        pot_layer = (lvl - prev) * len(contributors)
        elig = [p for p in alive if contrib[p] >= lvl]
        if elig and pot_layer > 0:
            best = max(strengths[p] for p in elig)
            winners = [p for p in elig if strengths[p] == best]
            share = pot_layer // len(winners)
            rem = pot_layer - share * len(winners)
            for w in winners:
                payoff[w] += share
            order = sorted(winners, key=lambda q: (q - (s.button + 1)) % n)
            for i in range(rem):
                payoff[order[i]] += 1
        prev = lvl
    return payoff
