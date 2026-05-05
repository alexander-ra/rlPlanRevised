"""Extended Leduc — 4-rank, 2-suit Leduc variant.

Built on the same skeleton as `mini_nl_leduc.py` but with the rank set
expanded from `{J, Q, K}` to `{J, Q, K, A}`, two suits per rank → 8
cards. Two betting rounds. Two bet-size options per round (small +
large). Showdown identical to Leduc: pair (private rank == community
rank) beats high card; tie within rank.

Reasons for this engine to exist:
- Day 4 of phase 4 needs a game whose info-set count is large enough
  that unabstracted full-traversal CFR is slow. Standard Leduc has 936
  info sets — fine for everything in days 1–3, but too small to make
  combined abstraction (suits + buckets + actions) interesting.
- Extended Leduc inflates that count to several thousand while keeping
  the structural similarity to Leduc that lets us reuse the §6.1–§6.3
  abstraction families with only minor parameterisation.

This module is tagged 🟡 AI-ASSISTED in the raw plan: it's a structural
extension of `mini_nl_leduc.py`. Reviewers should verify the
`legal_actions` / `_do_action` logic separately; the day-4 trainer is
the integration test.
"""

from collections import Counter

FOLD = 0
CHECK_CALL = 1
BET_SMALL = 2
BET_LARGE = 3
NUM_ACTIONS = 4
ACTION_NAMES = {FOLD: "f", CHECK_CALL: "c", BET_SMALL: "s", BET_LARGE: "l"}

NUM_RANKS = 4
COPIES_PER_RANK = 2
NUM_CARDS = NUM_RANKS * COPIES_PER_RANK  # 8
RANK_NAMES = {0: "J", 1: "Q", 2: "K", 3: "A"}

ANTE = 1
STARTING_STACK = 30
RAISE_AMOUNTS_R0 = {BET_SMALL: 2, BET_LARGE: 4}
RAISE_AMOUNTS_R1 = {BET_SMALL: 4, BET_LARGE: 8}
MAX_RAISES_PER_ROUND = 2


def card_rank(card: int) -> int:
    return card // 2


def get_all_deals():
    """All ordered (private0, private1, community) triples with distinct
    cards. With 8 cards this is `8 * 7 * 6 = 336` deals.
    """
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


def get_canonical_rank_deals():
    """Suit-isomorphic collapse: group `ALL_DEALS` by rank triple and
    keep the multiplicity. Mirrors the rank-canonical engine for Leduc.
    """
    counts = Counter()
    for c0, c1, cc in ALL_DEALS:
        counts[(c0 // 2, c1 // 2, cc // 2)] += 1
    return sorted(counts.items())


CANONICAL_DEALS = get_canonical_rank_deals()
TOTAL_DEAL_WEIGHT = sum(w for _, w in CANONICAL_DEALS)  # == 336


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


class ExtendedLeducState:
    """Extended-Leduc state. `abstracted=True` removes `BET_LARGE`
    (parallel to `mini_nl_leduc`); `rank_canonical=True` switches the
    state to use ranks directly instead of card ids.
    """

    def __init__(self, cards: tuple, community: int,
                 abstracted: bool = False,
                 rank_canonical: bool = False):
        self.cards = cards
        self.community = community
        self.abstracted = abstracted
        self.rank_canonical = rank_canonical
        self.history = ""
        self.round = 0
        self.bets = [ANTE, ANTE]
        self.stacks = [STARTING_STACK - ANTE, STARTING_STACK - ANTE]
        self.num_raises = [0, 0]
        self.round_actions = [0, 0]
        self.folded = -1
        self._is_terminal = False

    def current_player(self) -> int:
        return self.round_actions[self.round] % 2

    def is_terminal(self) -> bool:
        return self._is_terminal

    def _rank_of(self, idx: int) -> int:
        if self.rank_canonical:
            return self.cards[idx]
        return card_rank(self.cards[idx])

    def _community_rank(self) -> int:
        if self.rank_canonical:
            return self.community
        return card_rank(self.community)

    def get_info_set(self, player: int) -> str:
        # In full mode these are card ids; in rank-canonical mode the
        # state stores ranks directly. This is the suit-isomorphism
        # switch.
        private = self.cards[player]
        if self.round >= 1:
            return f"{private}:{self.community}|{self.history}"
        return f"{private}|{self.history}"

    def _raise_amounts(self):
        return RAISE_AMOUNTS_R0 if self.round == 0 else RAISE_AMOUNTS_R1

    def legal_actions(self) -> list:
        if self._is_terminal:
            return []
        actions = [CHECK_CALL]
        player = self.current_player()
        opp = 1 - player
        if self.bets[player] < self.bets[opp]:
            actions.append(FOLD)
        if self.num_raises[self.round] < MAX_RAISES_PER_ROUND:
            owed = self.bets[opp] - self.bets[player]
            amounts = self._raise_amounts()
            if self.stacks[player] >= owed + amounts[BET_SMALL]:
                actions.append(BET_SMALL)
            if (not self.abstracted
                    and self.stacks[player] >= owed + amounts[BET_LARGE]):
                actions.append(BET_LARGE)
        return sorted(actions)

    def apply_action(self, action: int) -> "ExtendedLeducState":
        s = ExtendedLeducState(self.cards, self.community,
                               abstracted=self.abstracted,
                               rank_canonical=self.rank_canonical)
        s.history = self.history
        s.round = self.round
        s.bets = list(self.bets)
        s.stacks = list(self.stacks)
        s.num_raises = list(self.num_raises)
        s.round_actions = list(self.round_actions)
        s.folded = self.folded
        s._is_terminal = self._is_terminal
        s._do_action(action)
        return s

    def _do_action(self, action: int):
        player = self.current_player()
        opp = 1 - player
        self.history += ACTION_NAMES[action]
        self.round_actions[self.round] += 1

        if action == FOLD:
            self.folded = player
            self._is_terminal = True
            return

        if action == CHECK_CALL:
            owed = self.bets[opp] - self.bets[player]
            self.stacks[player] -= owed
            self.bets[player] = self.bets[opp]
            if self.round_actions[self.round] >= 2 and self.bets[0] == self.bets[1]:
                if self.round == 0:
                    self.round = 1
                    self.history += "/"
                else:
                    self._is_terminal = True
            return

        amounts = self._raise_amounts()
        raise_inc = amounts[action]
        owed = self.bets[opp] - self.bets[player]
        total = owed + raise_inc
        self.stacks[player] -= total
        self.bets[player] = self.bets[opp] + raise_inc
        self.num_raises[self.round] += 1

    def get_utility(self, player: int) -> float:
        assert self._is_terminal
        if self.folded >= 0:
            if self.folded == player:
                return -float(self.bets[player])
            return float(self.bets[1 - player])
        ranks = (self._rank_of(0), self._rank_of(1))
        result = showdown_winner(ranks, self._community_rank())
        if result == 0:
            return 0.0
        if (result == 1 and player == 0) or (result == -1 and player == 1):
            return float(self.bets[1 - player])
        return -float(self.bets[player])


def enumerate_info_sets(abstracted: bool = False,
                        rank_canonical: bool = False) -> dict:
    """Walk the full tree and return `{info_set_key: sample_state}`."""
    seen = {}
    deals = (CANONICAL_DEALS if rank_canonical else
             [(d, 1) for d in ALL_DEALS])

    def walk(state):
        if state.is_terminal():
            return
        key = state.get_info_set(state.current_player())
        if key not in seen:
            seen[key] = state
        for a in state.legal_actions():
            walk(state.apply_action(a))

    if rank_canonical:
        for (r0, r1, rc), _w in deals:
            walk(ExtendedLeducState((r0, r1), rc, abstracted=abstracted,
                                    rank_canonical=True))
    else:
        for d, _ in deals:
            walk(ExtendedLeducState((d[0], d[1]), d[2],
                                    abstracted=abstracted))
    return seen


if __name__ == "__main__":
    full = enumerate_info_sets(abstracted=False, rank_canonical=False)
    abst_a = enumerate_info_sets(abstracted=True, rank_canonical=False)
    full_r = enumerate_info_sets(abstracted=False, rank_canonical=True)
    abst_r = enumerate_info_sets(abstracted=True, rank_canonical=True)
    print(f"Full extended Leduc info sets:                     {len(full):>6}")
    print(f"Action-abstracted extended Leduc info sets:        {len(abst_a):>6}")
    print(f"Rank-canonical (suit-iso) info sets:               {len(full_r):>6}")
    print(f"Rank-canonical + action-abstracted info sets:      {len(abst_r):>6}")
    print(f"Standard Leduc reference info sets (step03):           936")
