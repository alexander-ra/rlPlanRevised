"""
phh_parser.py -- parse PHH hand histories into structured hand records (raw step 13, Day 1-2,
"hand history parser"; the plan's `PlaytechHandParser`, pointed at the PHH format instead).

WHAT IT DOES
------------
`parse_hand(raw)` takes one hand as the dict that `tomllib` produces from a `.phh` / `.phhs` entry
and replays it with a small no-limit hold'em betting engine written here. The replay yields, for
every action, the public state the actor faced (street, position, pot, amount to call, raises so
far, players still to act ...) and, for the hand, every player's contribution, the winner(s) where
they can be determined, and the net result.

It is deliberately independent of `pokerkit`: `validator.py` replays the same hands through
pokerkit's rules engine and compares, so the two act as cross-checks on each other.

CONVENTIONS (PHH, as implemented by pokerkit)
---------------------------------------------
* Players are listed in post-flop acting order: p1 = small blind, p2 = big blind, ..., pn = button
  (n > 2). Heads-up (n = 2): pokerkit reverses the blinds, so p1 posts the big blind and p2 is the
  button/small blind; p2 acts first pre-flop, p1 first post-flop.
* 'cbr X' = complete/bet/raise TO a street total of X; 'cc' = check or call; 'f' = fold;
  'sm' = show or muck; 'd dh' deals hole cards ('????' = unknown); 'd db' deals board cards.
* IPN stacks are recorded as `inf` and the `winnings` field is all zeros in the HandHQ subset, so
  results are recomputed here: uncontested pots are exact; a showdown is exact only when every
  showdown player's cards are known, otherwise it is marked unresolved and split equally (the same
  imputation pokerkit's payoffs make for unknown cards).

All amounts in the returned records are in big blinds.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from config import CALL, CHECK, FOLD, RAISE_L, RAISE_M, RAISE_S, SIZE_EDGES

# Position codes (seats counted back from the button; blinds separate).
POS_NAMES = ["SB", "BB", "EP", "LJ", "HJ", "CO", "BTN"]
SB, BB, EP, LJ, HJ, CO, BTN = range(7)

RANKS = "23456789TJQKA"


class ParseError(Exception):
    """Raised when a hand cannot be replayed (malformed or rule-breaking)."""


@dataclass
class ActionRec:
    actor: int
    street: int
    kind: str                 # 'f' | 'cc' | 'cbr'
    cls: int                  # behavioural-cloning class (config.ACTION_NAMES)
    to: float                 # cbr: street total after the action (BB); else 0
    paid: float               # chips added by this action (BB)
    pot_before: float         # total pot before the action (BB)
    to_call: float            # amount needed to call (BB)
    cur_bet: float            # street bet level before the action (BB)
    n_raises: int             # voluntary bets/raises already made on this street
    n_active: int             # players not folded before the action
    n_behind: int             # players still to act after this one in this round
    size_frac: float          # raise size / (pot + to_call); NaN unless cbr
    pf_aggressor: int         # index of the last pre-flop raiser (-1 if none)
    prev_street_aggr: int     # index of the last bettor on the previous street (-1 if none)
    in_position: bool         # post-flop: actor is last to act among active players
    my_prev: int              # actor's previous action on this street: 0 none,1 check,2 call,3 raise


@dataclass
class HandRec:
    hand_id: int
    n: int
    players: list
    bb: float
    positions: list           # position code per player index
    actions: list             # ActionRec list
    board: list               # board cards as strings ('Ah')
    hole: dict                # player index -> 'AhKd' (known only)
    contrib: list             # BB contributed per player
    net: list                 # BB net result per player (imputed if unresolved)
    folded: list              # bool per player
    saw_street: list          # highest street index each player was active at (0..3)
    showdown: list            # bool per player: reached showdown
    resolution: str           # 'uncontested' | 'showdown_known' | 'showdown_unknown'
    win: list = field(default_factory=list)   # BB won per player (imputed if unresolved)
    day: int = 0
    time_s: int = 0
    meta: dict = field(default_factory=dict)


def positions_for(n: int) -> list[int]:
    if n == 2:
        return [BB, BTN]
    pos = [EP] * n
    pos[0], pos[1] = SB, BB
    back = [BTN, CO, HJ, LJ]
    for k, code in enumerate(back):
        i = n - 1 - k
        if i >= 2:
            pos[i] = code
    return pos


def _num(x) -> float:
    if isinstance(x, str):
        return float(x)
    return float(x)


def _cards(s: str) -> list[str]:
    s = s.strip()
    if "?" in s:
        return []
    return [s[i:i + 2] for i in range(0, len(s), 2)]


def size_class(frac: float) -> int:
    if frac <= SIZE_EDGES[0]:
        return RAISE_S
    if frac <= SIZE_EDGES[1]:
        return RAISE_M
    return RAISE_L


def parse_hand(raw: dict, strict: bool = True, prefix: bool = False) -> HandRec:
    """Replay one PHH hand. Raises ParseError on anything that breaks the rules it checks
    (turn order, minimum raise, stack limits, board counts, actions after the hand ended)."""
    players = list(raw["players"])
    n = len(players)
    if n < 2:
        raise ParseError("fewer than two players")
    blinds = [_num(b) for b in raw["blinds_or_straddles"]]
    antes = [_num(a) for a in raw.get("antes", [0] * n)]
    stacks0 = [_num(s) for s in raw["starting_stacks"]]
    if not (len(blinds) == len(antes) == len(stacks0) == n):
        raise ParseError("field length mismatch")
    if n == 2:  # pokerkit convention: heads-up blinds are reversed
        blinds = [blinds[1], blinds[0]]
    # A negative entry is a "post": a newly seated player pays |x| to play at once (pokerkit
    # semantics: a live bet of |x| that does not decide who opens the betting).
    posts = [abs(b) for b in blinds]
    if not any(b > 0 for b in blinds):
        raise ParseError("no big blind")
    bb = max(b for b in blinds if b > 0)

    stack = stacks0[:]
    contrib = [0.0] * n
    street_bet = [0.0] * n
    folded = [False] * n
    allin = [False] * n
    for i in range(n):
        a = min(antes[i], stack[i])
        stack[i] -= a
        contrib[i] += a
    for i in range(n):
        b = min(posts[i], stack[i])
        stack[i] -= b
        contrib[i] += b
        street_bet[i] = b
        if stack[i] <= 0 and stacks0[i] != math.inf:
            allin[i] = True
    cur_bet = max(street_bet)
    last_raise = bb                      # minimum raise increment
    street = 0
    sgn = [(b > 0) - (b < 0) for b in blinds]
    big_idx = max(range(n), key=lambda i: (street_bet[i] * sgn[i], i))
    order0 = [(big_idx + 1 + k) % n for k in range(n)]   # pre-flop acting order
    need = set(i for i in range(n) if not allin[i])
    n_raises = 0
    pf_aggr = -1
    street_aggr = -1
    prev_street_aggr = -1
    my_prev = [0] * n
    saw = [0] * n
    board: list[str] = []
    hole: dict[int, str] = {}
    shown: dict[int, str] = {}
    acts: list[ActionRec] = []
    ended = False
    last_actor = None
    acts_this_street = 0
    implied_allin = False
    inf_stacks = any(x == math.inf for x in stacks0)

    def active():
        return [i for i in range(n) if not folded[i]]

    def next_actor():
        """Next player (in order) who still needs to act this round."""
        if not need:
            return None
        order = order0 if street == 0 else list(range(n))
        if last_actor is None:
            for i in order:
                if i in need:
                    return i
            return None
        start = order.index(last_actor)
        for k in range(1, n + 1):
            i = order[(start + k) % n]
            if i in need:
                return i
        return None

    def round_done():
        return not need

    for a in raw["actions"]:
        tok = a.split()
        if not tok:
            continue
        if tok[0] == "d":
            if tok[1] == "dh":
                pi = int(tok[2][1:]) - 1
                if not 0 <= pi < n:
                    raise ParseError(f"deal to unknown player {tok[2]}")
                cs = _cards(tok[3]) if len(tok) > 3 else []
                if cs:
                    hole[pi] = "".join(cs)
            elif tok[1] == "db":
                cs = _cards(tok[2])
                if not round_done() and len([i for i in active() if not allin[i]]) > 1:
                    # HandHQ records stacks as inf, so a real all-in shows up as a street dealt
                    # with no betting on the previous one. Accept exactly that pattern.
                    if inf_stacks and street > 0 and acts_this_street == 0:
                        implied_allin = True
                        need = set()
                    elif strict:
                        raise ParseError("board dealt before betting round finished")
                if len(active()) < 2:
                    raise ParseError("board dealt after hand ended")
                expect = {0: 3, 1: 1, 2: 1}.get(street)
                if expect is None:
                    raise ParseError("too many board cards")
                if len(cs) != expect:
                    raise ParseError(f"street {street + 1} dealt {len(cs)} cards, expected {expect}")
                board.extend(cs)
                street += 1
                street_bet = [0.0] * n
                cur_bet = 0.0
                last_raise = bb
                prev_street_aggr = street_aggr
                street_aggr = -1
                n_raises = 0
                my_prev = [0] * n
                last_actor = None
                acts_this_street = 0
                need = set(i for i in active() if not allin[i])
                if len(need) < 2 or implied_allin:
                    need = set()           # all-in run-out: no more betting
                for i in active():
                    saw[i] = street
            continue
        # player action
        pi = int(tok[0][1:]) - 1
        if not 0 <= pi < n:
            raise ParseError(f"unknown player {tok[0]}")
        kind = tok[1]
        if kind == "sm":
            cs = _cards(tok[2]) if len(tok) > 2 else []
            if cs:
                shown[pi] = "".join(cs)
            continue
        if ended:
            raise ParseError("action after hand ended")
        if folded[pi]:
            raise ParseError(f"action by folded player p{pi + 1}")
        if strict:
            exp = next_actor()
            if exp is None:
                raise ParseError("action when no one is due to act")
            if exp != pi:
                raise ParseError(f"out of turn: p{pi + 1} acted, p{exp + 1} was due")
        to_call = max(0.0, cur_bet - street_bet[pi])
        cur_bet_before = cur_bet
        pot_before = sum(contrib)
        act_list = active()
        n_act = len(act_list)
        # players still to act after this one (in this round), excluding the actor
        n_behind = len([i for i in need if i != pi])
        if street > 0:
            live = [i for i in act_list]
            in_pos = live[-1] == pi if live else False
        else:
            in_pos = False
        frac = float("nan")
        to = 0.0
        if kind == "f":
            paid = 0.0
            cls = FOLD
            folded[pi] = True
            need.discard(pi)
        elif kind == "cc":
            paid = min(to_call, stack[pi])
            stack[pi] -= paid
            contrib[pi] += paid
            street_bet[pi] += paid
            if stack[pi] <= 0 and stacks0[pi] != math.inf:
                allin[pi] = True
            cls = CALL if to_call > 0 else CHECK
            need.discard(pi)
            my_prev[pi] = 2 if to_call > 0 else 1
        elif kind == "cbr":
            to = _num(tok[2])
            if to <= cur_bet:
                raise ParseError(f"raise to {to} not above current bet {cur_bet}")
            paid = to - street_bet[pi]
            if paid > stack[pi] + 1e-9:
                raise ParseError(f"p{pi + 1} bets {paid} with only {stack[pi]} behind")
            is_allin = abs(paid - stack[pi]) < 1e-9 and stacks0[pi] != math.inf
            inc = to - cur_bet
            if strict and inc + 1e-9 < last_raise and not is_allin:
                raise ParseError(f"raise increment {inc} below minimum {last_raise}")
            frac = inc / max(pot_before + to_call, 1e-9)
            cls = size_class(frac)
            stack[pi] -= paid
            contrib[pi] += paid
            street_bet[pi] = to
            if inc >= last_raise:
                last_raise = inc
            cur_bet = to
            n_raises_before = n_raises
            n_raises += 1
            if is_allin:
                allin[pi] = True
            need = set(i for i in active() if i != pi and not allin[i])
            if street == 0:
                pf_aggr = pi
            street_aggr = pi
            my_prev[pi] = 3
        else:
            raise ParseError(f"unknown action kind {kind}")
        rec = ActionRec(
            actor=pi, street=street, kind=kind, cls=cls, to=to / bb, paid=paid / bb,
            pot_before=pot_before / bb, to_call=to_call / bb, cur_bet=cur_bet_before / bb,
            n_raises=(n_raises - 1 if kind == "cbr" else n_raises),
            n_active=n_act, n_behind=n_behind, size_frac=frac,
            pf_aggressor=pf_aggr if not (kind == "cbr" and street == 0) else _prev_pf(acts),
            prev_street_aggr=prev_street_aggr if street > 0 else -1,
            in_position=in_pos, my_prev=_my_prev_before(acts, pi, street),
        )
        acts.append(rec)
        acts_this_street += 1
        last_actor = pi
        if len(active()) == 1:
            ended = True
            need = set()

    if prefix:
        # replay of an unfinished action list (used to rewrite hands for collusion injection)
        return {"street": street, "cur_bet": cur_bet, "street_bet": street_bet[:],
                "last_raise": last_raise, "need": set(need), "last_actor": last_actor,
                "order0": order0, "board": board[:], "contrib": contrib[:], "folded": folded[:],
                "bb": bb, "n": n, "hole": dict(hole)}
    # --- hand end checks -------------------------------------------------------------
    live = active()
    if len(live) >= 2:
        # must have reached the river with the betting finished (or an all-in run-out)
        if street < 3:
            raise ParseError("hand truncated before the river with several players left")
        if need:
            if inf_stacks and acts_this_street == 0:
                implied_allin = True          # river dealt after an unrecorded all-in
            else:
                raise ParseError("hand truncated: river betting not finished")
    # --- showdown / payoff -----------------------------------------------------------
    pot = sum(contrib)
    win = [0.0] * n
    sd = [False] * n
    if len(live) == 1:
        win[live[0]] = pot
        resolution = "uncontested"
    else:
        for i in live:
            sd[i] = True
        cards = {i: (hole.get(i) or shown.get(i)) for i in live}
        known = all(cards[i] for i in live) and len(board) == 5
        if known:
            strength = _strengths(cards, board)
            resolution = "showdown_known"
        else:
            strength = {i: 0 for i in live}   # equal -> equal split (imputation)
            resolution = "showdown_unknown"
        # side pots by contribution layers
        levels = sorted(set(contrib[i] for i in range(n) if contrib[i] > 0))
        prev = 0.0
        for lv in levels:
            layer = sum(min(contrib[i], lv) - min(contrib[i], prev) for i in range(n))
            elig = [i for i in live if contrib[i] >= lv - 1e-12]
            if not elig:            # only folded players reached this level: give to top live
                elig = [max(live, key=lambda i: contrib[i])]
            best = max(strength[i] for i in elig)
            ws = [i for i in elig if strength[i] == best]
            for i in ws:
                win[i] += layer / len(ws)
            prev = lv
    net = [(win[i] - contrib[i]) / bb for i in range(n)]
    # duplicate-card check across everything known
    allc = []
    for s in list(hole.values()) + list(shown.values()):
        allc.extend(_cards(s))
    allc.extend(board)
    allc_unique = set(allc)
    # a card shown at showdown can repeat the dealt hole card of the same player
    dup = False
    seen: dict[str, int] = {}
    for i, s in list(hole.items()):
        for c in _cards(s):
            if c in seen:
                dup = True
            seen[c] = i
    for c in board:
        if c in seen:
            dup = True
        seen[c] = -1
    for i, s in shown.items():
        for c in _cards(s):
            if c in seen and seen[c] != i:
                dup = True
    if dup or any(len(c) != 2 or c[0] not in RANKS or c[1] not in "cdhs" for c in allc_unique):
        raise ParseError("duplicate or malformed card")
    # finishing-stack check (Pluribus has finite stacks and finishing_stacks)
    if "finishing_stacks" in raw:
        fin = [_num(x) for x in raw["finishing_stacks"]]
        if abs(sum(fin) - sum(stacks0)) > 1e-6:
            raise ParseError("chips not conserved in finishing_stacks")
        if resolution != "showdown_unknown":
            mine = [stacks0[i] - contrib[i] + win[i] for i in range(n)]
            if any(abs(mine[i] - fin[i]) > 1e-6 for i in range(n)):
                raise ParseError("finishing_stacks disagree with replayed payoffs")
    return HandRec(
        hand_id=int(raw.get("hand", 0)), n=n, players=players, bb=bb,
        positions=positions_for(n), actions=acts, board=board, hole={**hole, **shown},
        contrib=[c / bb for c in contrib], net=net, folded=folded, saw_street=saw,
        showdown=sd, resolution=resolution, win=[w / bb for w in win],
        day=int(raw.get("day", 0)),
        time_s=_time_s(raw.get("time")),
        meta={"implied_allin": implied_allin},
    )


def _prev_pf(acts: list) -> int:
    for r in reversed(acts):
        if r.street == 0 and r.kind == "cbr":
            return r.actor
    return -1


def _my_prev_before(acts: list, pi: int, street: int) -> int:
    for r in reversed(acts):
        if r.street != street:
            break
        if r.actor == pi:
            return {"cc": 2 if r.to_call > 0 else 1, "cbr": 3, "f": 0}[r.kind]
    return 0


def _time_s(t) -> int:
    if t is None:
        return 0
    try:
        return t.hour * 3600 + t.minute * 60 + t.second
    except AttributeError:
        h, m, s = str(t).split(":")
        return int(h) * 3600 + int(m) * 60 + int(float(s))


_EVAL_CACHE: dict = {}


def _strengths(cards: dict, board: list) -> dict:
    """Comparable hand strengths via pokerkit's standard high-hand evaluator."""
    from pokerkit import StandardHighHand
    b = "".join(board)
    out = {}
    for i, h in cards.items():
        hand = StandardHighHand.from_game(h, b)
        out[i] = hand
    # map to integer ranks so equality means a split
    ordered = sorted(set(out.values()))
    rank = {h: k for k, h in enumerate(ordered)}
    return {i: rank[h] for i, h in out.items()}
