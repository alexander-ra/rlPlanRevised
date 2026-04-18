"""
Leduc Poker game engine — matches OpenSpiel leduc_poker exactly.

LEDUC POKER RULES (OpenSpiel implementation):
  - 6 cards: {0,1,2,3,4,5} where rank = card // 2
      Cards 0,1 = rank 0 (Jack)
      Cards 2,3 = rank 1 (Queen)
      Cards 4,5 = rank 2 (King)
  - 2 players each ante 1 chip (starting stack 100, but only
    net change matters for utility)
  - Round 1: betting with raise size 2
  - A community card is revealed (from remaining 4 cards)
  - Round 2: betting with raise size 4
  - Showdown: pair (private rank == community rank) beats high card;
    otherwise higher private rank wins; same rank with no pair = tie
  - Each round: check/call or raise, up to 2 raises per round
  - Fold is only legal when facing a raise

Actions: FOLD=0, CHECK_CALL=1, RAISE=2

Reference: OpenSpiel leduc_poker.h / leduc_poker.cc
"""

# Actions — same numbering as OpenSpiel
FOLD = 0
CHECK_CALL = 1
RAISE = 2
NUM_ACTIONS = 3
ACTION_NAMES = {FOLD: 'f', CHECK_CALL: 'c', RAISE: 'r'}

# Cards are integers 0–5; rank = card // 2
NUM_CARDS = 6
RANK_NAMES = {0: 'J', 1: 'Q', 2: 'K'}

# Game parameters (matching OpenSpiel defaults)
ANTE = 1
RAISE_AMOUNTS = [2, 4]  # round 1, round 2
MAX_RAISES_PER_ROUND = 2


def card_rank(card: int) -> int:
    """Rank of a card (0=J, 1=Q, 2=K)."""
    return card // 2


def card_str(card: int) -> str:
    """Human-readable card string, e.g. 'Ks'."""
    suit = 's' if card % 2 == 0 else 'h'
    return RANK_NAMES[card_rank(card)] + suit


def get_all_deals():
    """All 120 possible (p0_card, p1_card, community_card) triples.

    Drawn without replacement from 6 cards.
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


ALL_DEALS = get_all_deals()  # 120 deals


def _hand_strength(private: int, community: int) -> tuple:
    """Comparable hand strength: (has_pair, rank)."""
    has_pair = card_rank(private) == card_rank(community)
    return (has_pair, card_rank(private))


def showdown_winner(cards: tuple, community: int) -> int:
    """Return +1 if player 0 wins, -1 if player 1 wins, 0 if tie."""
    h0 = _hand_strength(cards[0], community)
    h1 = _hand_strength(cards[1], community)
    if h0 > h1:
        return 1
    elif h0 < h1:
        return -1
    return 0


class LeducState:
    """Represents a game state in Leduc Poker.

    Immutable-style: apply_action() returns a NEW state.
    Matches OpenSpiel's leduc_poker semantics exactly.
    """

    def __init__(self, cards: tuple, community: int):
        """
        Args:
            cards: (player0_card, player1_card) as integers 0–5
            community: community card as integer 0–5
        """
        self.cards = cards
        self.community = community
        self.history = ""           # action chars: 'c','r','f', '/' = round sep
        self.round = 0              # 0 = round 1, 1 = round 2
        self.bets = [ANTE, ANTE]    # cumulative chips committed
        self.num_raises = [0, 0]    # raises in [round0, round1]
        self.round_actions = [0, 0] # actions taken in [round0, round1]
        self.folded = -1            # -1 = nobody folded, else player who folded
        self._is_terminal = False

    def current_player(self) -> int:
        """Player 0 acts first in each round."""
        return self.round_actions[self.round] % 2

    def is_terminal(self) -> bool:
        return self._is_terminal

    def get_info_set(self, player: int) -> str:
        """Information set string for the given player.

        Uses card IDs (0-5) to match OpenSpiel's info state granularity.
        Format: "<card_id>|<history>" in round 0
                "<card_id>:<community_id>|<history>" in round 1+
        """
        card = self.cards[player]
        if self.round >= 1:
            return f"{card}:{self.community}|{self.history}"
        return f"{card}|{self.history}"

    def legal_actions(self) -> list:
        """Return sorted list of legal action indices."""
        if self._is_terminal:
            return []

        actions = [CHECK_CALL]  # can always check/call

        # Can fold only if facing a raise (bets are unequal)
        player = self.current_player()
        opponent = 1 - player
        if self.bets[player] < self.bets[opponent]:
            actions.append(FOLD)

        # Can raise if under the raise cap for this round
        if self.num_raises[self.round] < MAX_RAISES_PER_ROUND:
            actions.append(RAISE)

        return sorted(actions)

    def apply_action(self, action: int) -> 'LeducState':
        """Return a NEW state with the action applied."""
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
        opponent = 1 - player
        self.history += ACTION_NAMES[action]
        self.round_actions[self.round] += 1

        if action == FOLD:
            self.folded = player
            self._is_terminal = True
            return

        if action == RAISE:
            # Match opponent's bet first, then raise
            raise_amt = RAISE_AMOUNTS[self.round]
            self.bets[player] = self.bets[opponent] + raise_amt
            self.num_raises[self.round] += 1
            return

        if action == CHECK_CALL:
            # Match opponent's bet
            self.bets[player] = self.bets[opponent]

            # Round ends when both players have acted and bets are equal
            if self.round_actions[self.round] >= 2 and self.bets[0] == self.bets[1]:
                if self.round == 0:
                    # Move to round 2
                    self.round = 1
                    self.history += '/'  # round separator
                else:
                    # Showdown
                    self._is_terminal = True

    def get_utility(self, player: int) -> float:
        """Net utility for the given player at a terminal state.

        Returns the net change from starting stack — matches OpenSpiel returns.
        """
        assert self._is_terminal

        if self.folded >= 0:
            if self.folded == player:
                return -float(self.bets[player])
            else:
                return float(self.bets[1 - player])

        # Showdown
        result = showdown_winner(self.cards, self.community)
        if result == 0:
            return 0.0  # tie
        elif (result == 1 and player == 0) or (result == -1 and player == 1):
            return float(self.bets[1 - player])
        else:
            return -float(self.bets[player])


def action_to_str(action: int) -> str:
    return ACTION_NAMES[action]
