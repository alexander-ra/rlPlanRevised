"""
Leduc Poker with lossy card abstraction.

Extends suit abstraction by bucketing ranks:
  J (rank 0) and Q (rank 1) → "low"
  K (rank 2)                → "high"

This is a LOSSY abstraction: the agent can no longer distinguish a Jack
from a Queen. Strategy quality degrades because J and Q have different
showdown strengths (Q beats J at showdown if no pair forms).

Expected effect: fewer info sets than suit-abstracted; higher exploitability
floor in the full game.
"""

FOLD = 0
CHECK_CALL = 1
RAISE = 2
NUM_ACTIONS = 3
ACTION_NAMES = {FOLD: 'f', CHECK_CALL: 'c', RAISE: 'r'}

NUM_CARDS = 6
ANTE = 1
RAISE_AMOUNTS = [2, 4]
MAX_RAISES_PER_ROUND = 2


def card_rank(card: int) -> int:
    return card // 2


def _bucket(rank: int) -> str:
    """J=0, Q=1 → 'low';  K=2 → 'high'."""
    return "low" if rank < 2 else "high"


def get_all_deals():
    deals = []
    for c0 in range(NUM_CARDS):
        for c1 in range(NUM_CARDS):
            if c1 == c0:
                continue
            for cc in range(NUM_CARDS):
                if cc == c0 or cc == c1:
                    continue
                deals.append((c0, c1, cc))
    return deals


ALL_DEALS = get_all_deals()


def _hand_strength(private: int, community: int) -> tuple:
    has_pair = card_rank(private) == card_rank(community)
    return (has_pair, card_rank(private))


def showdown_winner(cards: tuple, community: int) -> int:
    h0 = _hand_strength(cards[0], community)
    h1 = _hand_strength(cards[1], community)
    if h0 > h1:
        return 1
    elif h0 < h1:
        return -1
    return 0


class LeducState:
    """Leduc Poker with lossy abstraction in get_info_set().

    Game mechanics are identical to the original — only info set keys use
    "low"/"high" buckets so J and Q are indistinguishable to the agent.
    """

    def __init__(self, cards: tuple, community: int):
        self.cards = cards
        self.community = community
        self.history = ""
        self.round = 0
        self.bets = [ANTE, ANTE]
        self.num_raises = [0, 0]
        self.round_actions = [0, 0]
        self.folded = -1
        self._is_terminal = False

    def current_player(self) -> int:
        return self.round_actions[self.round] % 2

    def is_terminal(self) -> bool:
        return self._is_terminal

    def get_info_set(self, player: int) -> str:
        """Lossy-bucketed key: J and Q share the same bucket 'low', K → 'high'.

        Format: "<bucket>|<history>" or "<bucket>:<community_bucket>|<history>"
        """
        bkt = _bucket(card_rank(self.cards[player]))
        if self.round >= 1:
            return f"{bkt}:{_bucket(card_rank(self.community))}|{self.history}"
        return f"{bkt}|{self.history}"

    def legal_actions(self) -> list:
        if self._is_terminal:
            return []
        actions = [CHECK_CALL]
        player = self.current_player()
        if self.bets[player] < self.bets[1 - player]:
            actions.append(FOLD)
        if self.num_raises[self.round] < MAX_RAISES_PER_ROUND:
            actions.append(RAISE)
        return sorted(actions)

    def apply_action(self, action: int) -> 'LeducState':
        s = LeducState(self.cards, self.community)
        s.history = self.history
        s.round = self.round
        s.bets = list(self.bets)
        s.num_raises = list(self.num_raises)
        s.round_actions = list(self.round_actions)
        s.folded = self.folded
        s._is_terminal = self._is_terminal
        s._do_action(action)
        return s

    def _do_action(self, action: int):
        player = self.current_player()
        self.history += ACTION_NAMES[action]
        self.round_actions[self.round] += 1

        if action == FOLD:
            self.folded = player
            self._is_terminal = True
            return

        if action == RAISE:
            self.bets[player] = self.bets[1 - player] + RAISE_AMOUNTS[self.round]
            self.num_raises[self.round] += 1
            return

        if action == CHECK_CALL:
            self.bets[player] = self.bets[1 - player]
            if self.round_actions[self.round] >= 2 and self.bets[0] == self.bets[1]:
                if self.round == 0:
                    self.round = 1
                    self.history += '/'
                else:
                    self._is_terminal = True

    def get_utility(self, player: int) -> float:
        assert self._is_terminal
        if self.folded >= 0:
            if self.folded == player:
                return -float(self.bets[player])
            return float(self.bets[1 - player])
        result = showdown_winner(self.cards, self.community)
        if result == 0:
            return 0.0
        if (result == 1 and player == 0) or (result == -1 and player == 1):
            return float(self.bets[1 - player])
        return -float(self.bets[player])
