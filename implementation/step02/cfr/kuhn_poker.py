"""
Kuhn Poker game engine.

KUHN POKER RULES:
  - 3 cards: {1, 2, 3} (Jack, Queen, King)
  - 2 players each ante 1 chip
  - Each player is dealt 1 card (private information)
  - Players alternate, starting with Player 1
  - On a turn, a player may PASS or BET (bet = add 1 chip to pot)
  - Terminal conditions:
      pass-pass     → higher card wins 1 chip
      pass-bet-pass → bettor (player 2) wins 1 chip
      pass-bet-bet  → higher card wins 2 chips
      bet-pass      → bettor (player 1) wins 1 chip
      bet-bet       → higher card wins 2 chips

The known optimal game value for player 1 is: -1/18 ≈ -0.0556
"""

# The two possible actions
PASS = 0
BET = 1
NUM_ACTIONS = 2

# Card names for display
CARD_NAMES = {1: 'J', 2: 'Q', 3: 'K'}

# All possible card deals (permutations of 2 from 3 cards)
ALL_DEALS = [(c1, c2) for c1 in [1, 2, 3] for c2 in [1, 2, 3] if c1 != c2]


def get_player(history: str) -> int:
    """Player 0 acts on even turns, player 1 on odd turns."""
    return len(history) % 2


def get_info_set(card: int, history: str) -> str:
    """Construct information set string: card + action history."""
    return str(card) + history


def is_terminal(history: str) -> bool:
    """Check if the history represents a terminal game state."""
    if len(history) < 2:
        return False
    return history[-1] == 'p' or history[-2:] == 'bb'


def get_terminal_utility(cards: list, history: str, player: int) -> float:
    """
    Compute utility for the given player at a terminal state.

    Args:
        cards: [player1_card, player2_card, unused_card]
        history: string of actions ("p"=pass, "b"=bet)
        player: the player whose utility to compute

    Returns:
        utility from perspective of `player`
    """
    opponent = 1 - player
    is_higher = cards[player] > cards[opponent]

    if history == "pp":
        return 1 if is_higher else -1
    elif history[-1] == 'p':
        # someone folded — the player who just passed loses
        return 1  # current player at terminal is the one who folded
    elif history[-2:] == 'bb':
        return 2 if is_higher else -2
    raise ValueError(f"Not a terminal history: {history}")


def action_to_str(action: int) -> str:
    """Convert action index to history character."""
    return "p" if action == PASS else "b"
