"""
Engine adapters for Step 07 (Opponent Modeling).

WHAT THIS IS
------------
A single, uniform `Game` interface over the two validated engines we already built:

  - Kuhn Poker   -> implementation/step02/cfr/kuhn_poker.py
  - Leduc Hold'em -> implementation/step03/cfr/leduc_poker.py

We *import* those engines (never copy them) and wrap each in a small adapter so the
opponent-modeling code (models, best-response, pipeline, tournament) can be written
once and run on either game.

WHY importlib INSTEAD OF `from cfr.kuhn_poker import ...`
--------------------------------------------------------
step02 and step03 BOTH ship a package literally named `cfr` (and an `info_set_node`
inside it). If we put both step02 and step03 on `sys.path`, Python merges them into a
single `cfr` namespace package and `cfr.info_set_node` resolves to whichever directory
comes first on the path -- a silent, nasty bug (Kuhn's 2-action node shadowing Leduc's
3-action node, or vice-versa). Both engine files are self-contained (they import nothing
from their own `cfr` package), so we sidestep the whole problem by loading each engine
file *directly* under a unique module name with importlib. No `cfr` package is ever
imported, so there is nothing to collide.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Run the self-test
yourself: `python implementation/step07/implementation/engines.py`.
"""

from __future__ import annotations

import os
import importlib.util
from abc import ABC, abstractmethod


# --- Load the two engines directly from their files (no `cfr` package) --------------
def _load_module(path: str, mod_name: str):
    """Load a standalone .py file as a uniquely-named module (avoids package clashes)."""
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import spec for {path!r}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_HERE = os.path.dirname(os.path.abspath(__file__))
# step07/implementation/  ->  ../.. -> implementation/
_IMPL_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
_KUHN_PATH = os.path.join(_IMPL_ROOT, "step02", "cfr", "kuhn_poker.py")
_LEDUC_PATH = os.path.join(_IMPL_ROOT, "step03", "cfr", "leduc_poker.py")

kuhn = _load_module(_KUHN_PATH, "step07_kuhn_engine")
leduc = _load_module(_LEDUC_PATH, "step07_leduc_engine")


# --- A tiny immutable Kuhn state (the Kuhn engine is function-based) -----------------
class KuhnState:
    """(cards, history) wrapper so Kuhn looks state-based like Leduc."""

    __slots__ = ("cards", "history")

    def __init__(self, cards: tuple, history: str = ""):
        self.cards = cards          # (p0_card, p1_card)
        self.history = history      # e.g. "pb"

    def __repr__(self):
        return f"KuhnState(cards={self.cards}, history={self.history!r})"


# --- The uniform game interface ------------------------------------------------------
class Game(ABC):
    """Everything the opponent-modeling code needs from a 2-player, zero-sum,
    imperfect-information game with a single chance move (the deal) at the root."""

    name: str = "abstract"
    num_players: int = 2
    has_public_board: bool = False  # Leduc has a public community card; Kuhn does not

    # ---- structure ----
    @abstractmethod
    def deals(self) -> list:
        """All chance outcomes (deals) at the root."""

    def deal_prob(self, deal) -> float:
        """Prior probability of a deal (uniform here)."""
        return 1.0 / len(self.deals())

    @abstractmethod
    def root(self, deal):
        """Initial (post-deal) state for a deal."""

    @abstractmethod
    def is_terminal(self, state) -> bool: ...

    @abstractmethod
    def current_player(self, state) -> int: ...

    @abstractmethod
    def legal_actions(self, state) -> list: ...

    @abstractmethod
    def info_set(self, state, player: int | None = None) -> str:
        """Information set string for `player` (the acting player if None)."""

    @abstractmethod
    def apply(self, state, action):
        """Return the NEW state after `action`."""

    @abstractmethod
    def utility(self, state, player: int) -> float:
        """Terminal utility for `player` (zero-sum: u(0) = -u(1))."""

    # ---- information / observability ----
    def private(self, deal, player: int):
        """The private card dealt to `player`."""
        return deal[player]

    def community(self, deal):
        """The public board card, or None if the game has no board."""
        return None

    @abstractmethod
    def revealed_privates(self, state) -> set:
        """At a terminal state, the set of players whose private card becomes public
        (a showdown reveals both; a fold reveals neither)."""

    @abstractmethod
    def action_name(self, action: int) -> str: ...

    # ---- the chance posterior used for partial-observability marginalization ----
    def consistent_deals(self, observer: int, observer_private, community=None) -> list:
        """All deals consistent with what `observer` knows: their own private card and
        (if it became public) the community card.  Used to marginalize over the
        opponent's hidden card.  Uniform prior, so each returned deal is equally likely.
        """
        out = []
        for d in self.deals():
            if d[observer] != observer_private:
                continue
            if community is not None and self.community(d) != community:
                continue
            out.append(d)
        return out


# --- Kuhn adapter --------------------------------------------------------------------
class KuhnGame(Game):
    name = "kuhn"
    has_public_board = False

    def deals(self) -> list:
        return list(kuhn.ALL_DEALS)

    def root(self, deal):
        return KuhnState(tuple(deal), "")

    def is_terminal(self, state) -> bool:
        return kuhn.is_terminal(state.history)

    def current_player(self, state) -> int:
        return kuhn.get_player(state.history)

    def legal_actions(self, state) -> list:
        # PASS and BET are always available until the hand is terminal.
        return [kuhn.PASS, kuhn.BET]

    def info_set(self, state, player: int | None = None) -> str:
        if player is None:
            player = self.current_player(state)
        return kuhn.get_info_set(state.cards[player], state.history)

    def apply(self, state, action):
        return KuhnState(state.cards, state.history + kuhn.action_to_str(action))

    def utility(self, state, player: int) -> float:
        # The Kuhn engine's get_terminal_utility is written from the perspective of the
        # player *to act* at the terminal node, and its fold branch returns +1 for that
        # player regardless of the `player` arg -- so we must call it with `cur` and flip.
        h = state.history
        cur = kuhn.get_player(h)
        u_cur = kuhn.get_terminal_utility(list(state.cards), h, cur)
        p0 = u_cur if cur == 0 else -u_cur
        return p0 if player == 0 else -p0

    def revealed_privates(self, state) -> set:
        h = state.history
        # A pass *in response to a bet* is a fold (reveals nobody). "pp" is a check-check
        # showdown; "bb"/"pbb" are call showdowns -- all reveal both cards.
        folded = h.endswith("p") and "b" in h
        return set() if folded else {0, 1}

    def action_name(self, action: int) -> str:
        return kuhn.action_to_str(action)


# --- Leduc adapter -------------------------------------------------------------------
class LeducGame(Game):
    name = "leduc"
    has_public_board = True

    def deals(self) -> list:
        return list(leduc.ALL_DEALS)

    def root(self, deal):
        c0, c1, cc = deal
        return leduc.LeducState((c0, c1), cc)

    def is_terminal(self, state) -> bool:
        return state.is_terminal()

    def current_player(self, state) -> int:
        return state.current_player()

    def legal_actions(self, state) -> list:
        return state.legal_actions()

    def info_set(self, state, player: int | None = None) -> str:
        if player is None:
            player = state.current_player()
        return state.get_info_set(player)

    def apply(self, state, action):
        return state.apply_action(action)

    def utility(self, state, player: int) -> float:
        return state.get_utility(player)

    def community(self, deal):
        return deal[2]

    def revealed_privates(self, state) -> set:
        # A fold ends the hand with no showdown; otherwise both cards are shown.
        return set() if state.folded >= 0 else {0, 1}

    def action_name(self, action: int) -> str:
        return leduc.ACTION_NAMES[action]

    def card_rank(self, card: int) -> int:
        return leduc.card_rank(card)


# --- Factory -------------------------------------------------------------------------
_GAMES = {"kuhn": KuhnGame, "leduc": LeducGame}


def make_game(name: str) -> Game:
    """make_game("kuhn") or make_game("leduc")."""
    key = name.lower()
    if key not in _GAMES:
        raise ValueError(f"Unknown game {name!r}; choose from {sorted(_GAMES)}")
    return _GAMES[key]()


# --- Self-test (you run this) --------------------------------------------------------
def _selftest():
    print("engines self-test")
    print("-" * 50)
    for name in ("kuhn", "leduc"):
        g = make_game(name)
        deals = g.deals()
        print(f"[{name}] #deals = {len(deals)} (expect kuhn=6, leduc=120)")

        # Zero-sum check over a full uniform traversal using a uniform random policy.
        # We only check terminal utilities are exactly antisymmetric on a few rollouts.
        import random
        rng = random.Random(0)
        bad = 0
        for _ in range(200):
            deal = rng.choice(deals)
            s = g.root(deal)
            while not g.is_terminal(s):
                a = rng.choice(g.legal_actions(s))
                s = g.apply(s, a)
            u0, u1 = g.utility(s, 0), g.utility(s, 1)
            if abs(u0 + u1) > 1e-9:
                bad += 1
        print(f"[{name}] zero-sum violations in 200 rollouts: {bad} (expect 0)")

    # Spot-check known Kuhn payoffs (player 0's perspective).
    g = make_game("kuhn")
    checks = [((3, 1), "pp", +1), ((1, 3), "pp", -1), ((3, 1), "bp", +1),
              ((1, 3), "pbp", -1), ((3, 1), "bb", +2), ((1, 3), "pbb", -2)]
    for cards, hist, want in checks:
        s = KuhnState(cards, hist)
        got = g.utility(s, 0)
        ok = "OK " if abs(got - want) < 1e-9 else "FAIL"
        print(f"[kuhn] [{ok}] u0({cards},{hist!r}) = {got:+.0f} (want {want:+d})")


if __name__ == "__main__":
    _selftest()
