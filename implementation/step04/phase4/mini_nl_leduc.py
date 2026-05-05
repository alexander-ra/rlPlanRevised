"""Mini-NL Leduc — variable-bet-size Leduc variant.

Promoted from `implementation/step04/exploration/day02/mini_nl_leduc.py`
for phase 4 day 3. Behaviour is unchanged.

Same card structure as standard Leduc (6 cards, 3 ranks × 2 suits, 2
betting rounds, identical showdown), but with two bet-size options per
round instead of the fixed-limit single size:

    FOLD
    CHECK_CALL
    BET_SMALL   — +2 in round 0, +4 in round 1
    BET_LARGE   — +4 in round 0, +8 in round 1

When `abstracted=True` the constructor hides `BET_LARGE` from
`legal_actions()`, collapsing the action tree to the fixed-limit-shaped
game where the only raise is `BET_SMALL`. Day 3 trains on both flavours
and evaluates the abstracted-game strategy in the full game via the
translators in `day03_translators.py`.
"""

FOLD = 0
CHECK_CALL = 1
BET_SMALL = 2
BET_LARGE = 3
NUM_ACTIONS = 4
ACTION_NAMES = {FOLD: "f", CHECK_CALL: "c", BET_SMALL: "s", BET_LARGE: "l"}

NUM_CARDS = 6
RANK_NAMES = {0: "J", 1: "Q", 2: "K"}

ANTE = 1
STARTING_STACK = 20
RAISE_AMOUNTS_R0 = {BET_SMALL: 2, BET_LARGE: 4}
RAISE_AMOUNTS_R1 = {BET_SMALL: 4, BET_LARGE: 8}
MAX_RAISES_PER_ROUND = 2


def card_rank(card: int) -> int:
    return card // 2


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


ALL_DEALS = get_all_deals()  # 120 deals


def _hand_strength(private: int, community: int) -> tuple:
    return (card_rank(private) == card_rank(community), card_rank(private))


def showdown_winner(cards: tuple, community: int) -> int:
    h0 = _hand_strength(cards[0], community)
    h1 = _hand_strength(cards[1], community)
    if h0 > h1:
        return 1
    if h0 < h1:
        return -1
    return 0


class MiniNLLeducState:
    """State machine for mini-NL Leduc. `abstracted=True` removes
    `BET_LARGE` from the legal-action menu.
    """

    def __init__(self, cards: tuple, community: int, abstracted: bool = False):
        self.cards = cards
        self.community = community
        self.abstracted = abstracted
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

    def get_info_set(self, player: int) -> str:
        card = self.cards[player]
        if self.round >= 1:
            return f"{card}:{self.community}|{self.history}"
        return f"{card}|{self.history}"

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

    def apply_action(self, action: int) -> "MiniNLLeducState":
        s = MiniNLLeducState(self.cards, self.community, self.abstracted)
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
        result = showdown_winner(self.cards, self.community)
        if result == 0:
            return 0.0
        if (result == 1 and player == 0) or (result == -1 and player == 1):
            return float(self.bets[1 - player])
        return -float(self.bets[player])
