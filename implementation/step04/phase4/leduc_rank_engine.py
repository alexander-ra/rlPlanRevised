"""Leduc Poker — rank-canonical game engine (lossless suit-isomorphic collapse).

Promoted from `implementation/step04/exploration/leduc_rank_engine.py` for
phase 4. Behaviour is unchanged; only the docstring is expanded to point at
the §6.1 / §6.3 sections of the step-04 deliverable.

The key insight (deliverable §6.1, Gilpin & Sandholm Definition 3.2): in
Leduc the suit-permutation group acts on the signal tree without changing
leaf utilities, so all signal-tree subtrees that differ only by suit are
ordered-game-isomorphic. The deal enumeration shrinks from 120 suit-deals
to 24 canonical rank-deals with integer multiplicities. Summing the
weights recovers 120, and a CFR pass that iterates canonical deals
weighted by their multiplicity produces a regret trajectory mathematically
identical to one that iterates all 120 deals — at ~5x less per-iteration
work.

Info-set count for this engine equals the suit-abstracted count (288),
versus 936 for the original step03 engine.
"""

from collections import Counter

FOLD = 0
CHECK_CALL = 1
RAISE = 2
NUM_ACTIONS = 3
ACTION_NAMES = {FOLD: "f", CHECK_CALL: "c", RAISE: "r"}

NUM_RANKS = 3
COPIES_PER_RANK = 2
ANTE = 1
RAISE_AMOUNTS = [2, 4]
MAX_RAISES_PER_ROUND = 2


def _build_canonical_deals():
    """Enumerate all 120 suit-deals and group by rank triple.

    Returns a sorted list of `((r0, r1, rc), weight)` tuples whose weights
    sum to 120 (the number of unordered (private0, private1, community)
    triples in standard Leduc).
    """
    counts: Counter = Counter()
    num_cards = NUM_RANKS * COPIES_PER_RANK
    for c0 in range(num_cards):
        for c1 in range(num_cards):
            if c1 == c0:
                continue
            for cc in range(num_cards):
                if cc == c0 or cc == c1:
                    continue
                rank_triple = (c0 // 2, c1 // 2, cc // 2)
                counts[rank_triple] += 1
    return sorted(counts.items())


CANONICAL_DEALS = _build_canonical_deals()
TOTAL_DEAL_WEIGHT = sum(w for _, w in CANONICAL_DEALS)  # == 120


def _hand_strength(private_rank: int, community_rank: int) -> tuple:
    return (private_rank == community_rank, private_rank)


def showdown_winner(ranks: tuple, community_rank: int) -> int:
    h0 = _hand_strength(ranks[0], community_rank)
    h1 = _hand_strength(ranks[1], community_rank)
    if h0 > h1:
        return 1
    if h0 < h1:
        return -1
    return 0


class LeducRankState:
    """Leduc Poker state operating directly on ranks.

    `cards` stores `(rank_p0, rank_p1)` and `community` stores the
    community rank. Betting logic is byte-identical to step03's
    `LeducState`; only card storage differs.
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
        rank = self.cards[player]
        if self.round >= 1:
            return f"{rank}:{self.community}|{self.history}"
        return f"{rank}|{self.history}"

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

    def apply_action(self, action: int) -> "LeducRankState":
        s = LeducRankState(self.cards, self.community)
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
                    self.history += "/"
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


if __name__ == "__main__":
    print(f"canonical rank-deals: {len(CANONICAL_DEALS)}")
    print(f"total weight:         {TOTAL_DEAL_WEIGHT}")
    multiplicities = Counter(w for _, w in CANONICAL_DEALS)
    print(f"weight distribution:  {dict(multiplicities)}")
