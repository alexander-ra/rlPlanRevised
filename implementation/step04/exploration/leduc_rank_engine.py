"""
Leduc Poker — rank-canonical game engine (regime 2, lossless).

The state uses rank labels (0=J, 1=Q, 2=K) directly in place of card IDs.
Because suits never affect legal actions, betting, or showdown outcome in
Leduc, this is a lossless collapse of the original 6-card engine:

- ranks 0..2 replace card IDs 0..5,
- showdown_winner is unchanged (already a function of ranks),
- apply_action / legal_actions / get_utility are byte-identical to step03's
  leduc_poker.py modulo the state field names.

The key move: deal enumeration is reduced from 120 suit-deals to 24
**canonical rank-deals** with integer multiplicities. Summing the weights
recovers 120, so training that iterates canonical deals and weights regret
updates by multiplicity produces mathematically identical regret trajectories
to training on the full 120-deal set — but at ~5× less per-iteration work.

Info-set count for this engine equals the step04 suit-abstracted count (288).
The difference from leduc_suit_abstracted.py is structural: that file
bucketed only the policy and still iterated 120 deals, whereas this file
actually shrinks the game tree by eliminating suit-equivalent branches.

Usage from a trainer:

    from leduc_rank_engine import (
        LeducRankState, CANONICAL_DEALS, TOTAL_DEAL_WEIGHT,
    )
    for (r0, r1, rc), weight in CANONICAL_DEALS:
        state = LeducRankState((r0, r1), rc)
        # pass `weight` as the opening chance reach (or divide by
        # TOTAL_DEAL_WEIGHT for a proper probability)
"""

from collections import Counter

FOLD = 0
CHECK_CALL = 1
RAISE = 2
NUM_ACTIONS = 3
ACTION_NAMES = {FOLD: 'f', CHECK_CALL: 'c', RAISE: 'r'}

NUM_RANKS = 3
COPIES_PER_RANK = 2
ANTE = 1
RAISE_AMOUNTS = [2, 4]
MAX_RAISES_PER_ROUND = 2


def _build_canonical_deals():
    """Enumerate all 120 suit-deals and group by rank triple.

    Returns:
        deals: list of ((r0, r1, rc), weight) tuples. Sum of weights = 120.
    """
    counts: Counter = Counter()
    num_cards = NUM_RANKS * COPIES_PER_RANK  # 6
    for c0 in range(num_cards):
        for c1 in range(num_cards):
            if c1 == c0:
                continue
            for cc in range(num_cards):
                if cc == c0 or cc == c1:
                    continue
                rank_triple = (c0 // 2, c1 // 2, cc // 2)
                counts[rank_triple] += 1
    # Sort for deterministic iteration order
    return sorted(counts.items())


CANONICAL_DEALS = _build_canonical_deals()
TOTAL_DEAL_WEIGHT = sum(w for _, w in CANONICAL_DEALS)  # == 120


def _hand_strength(private_rank: int, community_rank: int) -> tuple:
    """(has_pair, rank) — comparable showdown strength."""
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
    """Leduc Poker state operating on ranks directly.

    `cards` stores (rank_p0, rank_p1) and `community` stores the community rank.
    All betting logic is identical to step03's LeducState.
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
        """Rank-based key. Matches the suit-abstracted keys used elsewhere.

        Round 0: "<rank>|<history>"
        Round 1: "<rank>:<community_rank>|<history>"
        """
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

    def apply_action(self, action: int) -> 'LeducRankState':
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


if __name__ == "__main__":
    # Self-check: canonical weights sum to 120, count is 24.
    print(f"canonical rank-deals: {len(CANONICAL_DEALS)}")
    print(f"total weight:         {TOTAL_DEAL_WEIGHT}")
    multiplicities = Counter(w for _, w in CANONICAL_DEALS)
    print(f"weight distribution:  {dict(multiplicities)}")
    print()
    print("first five canonical deals:")
    for d, w in CANONICAL_DEALS[:5]:
        print(f"  ranks={d} weight={w}")
