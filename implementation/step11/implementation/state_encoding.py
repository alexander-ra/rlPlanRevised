"""
state_encoding.py -- turn an `SLSState` into a fixed-length feature vector + a legal-action mask
for the neural agents (`sls_ppo.py` / `coalition_mappo.py`). Supporting infra (🟡).

DESIGN CHOICES
--------------
- EGOCENTRIC. Everything is rotated so the CURRENT player is index 0 (`rot`/`unrot` below). This
  makes all four seats look identical to the network, so a single shared policy is valid (raw
  L473 keeps per-agent nets, but egocentric encoding also permits sharing -- a one-line switch).
- FIXED ACTION SPACE. SLS actions are `(color, pile_target)`. We cap the number of addressable
  piles at `MAX_PILES`; the action index is `ego_color * (MAX_PILES + 1) + pile_slot`, where
  pile_slot `0..MAX_PILES-1` are existing piles and `MAX_PILES` means "start a NEW pile". Illegal
  entries are masked. `action_dim = n_players * (MAX_PILES + 1)`.

  >>> NOTE: if the live pile count ever exceeds MAX_PILES, piles beyond the cap are NOT
  addressable this turn (they simply carry no legal action index). MAX_PILES=10 is comfortably
  above what 4x7 SLS reaches in practice, but if a run warns about clipping, raise it. <<<

FEATURE LAYOUT (egocentric; n = n_players):
    [ hands        ]  n * n     -- hands[player][color], players & colors rotated so me = 0
    [ piles        ]  MAX_PILES * (1 + n)  -- per pile: normalized height + top-color one-hot
    [ eliminated   ]  n         -- rotated elimination mask
    [ turn_frac    ]  1         -- turn_count / max_turns
  obs_dim = n*n + MAX_PILES*(1+n) + n + 1

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

from sls_game import SLSGame, SLSState

MAX_PILES = 10


def action_dim(n_players: int, max_piles: int = MAX_PILES) -> int:
    return n_players * (max_piles + 1)


def obs_dim(n_players: int, max_piles: int = MAX_PILES) -> int:
    n = n_players
    return n * n + max_piles * (1 + n) + n + 1


def rot(idx: int, me: int, n: int) -> int:
    """Absolute player/color index -> egocentric (me -> 0)."""
    return (idx - me) % n


def unrot(ego_idx: int, me: int, n: int) -> int:
    """Egocentric index -> absolute."""
    return (ego_idx + me) % n


def encode_state(game: SLSGame, state: SLSState, max_piles: int = MAX_PILES) -> np.ndarray:
    """Egocentric fixed-length feature vector for the current player."""
    n = game.n_players
    me = state.current_player
    feats = []

    # hands: rotate BOTH the player axis and the color axis so "me" is player 0 / color 0
    hands = np.zeros((n, n))
    for p in range(n):
        for c in range(n):
            hands[rot(p, me, n)][rot(c, me, n)] = state.hands[p][c]
    feats.append(hands.reshape(-1) / max(game.chips_per_player, 1))

    # piles: per addressable pile, normalized height + rotated top-color one-hot
    pile_feat = np.zeros((max_piles, 1 + n))
    for i, pile in enumerate(state.piles[:max_piles]):
        pile_feat[i, 0] = len(pile) / max(game.chips_per_player, 1)
        if pile:
            pile_feat[i, 1 + rot(pile[-1], me, n)] = 1.0
    feats.append(pile_feat.reshape(-1))

    # elimination mask (rotated) + turn fraction
    elim = np.zeros(n)
    for p in state.eliminated:
        elim[rot(p, me, n)] = 1.0
    feats.append(elim)
    feats.append(np.array([state.turn_count / max(game.max_turns, 1)]))

    return np.concatenate(feats).astype(np.float32)


def legal_action_mask(game: SLSGame, state: SLSState, max_piles: int = MAX_PILES) -> np.ndarray:
    """Boolean mask over the fixed action space; True = legal for the current player NOW."""
    n = game.n_players
    me = state.current_player
    mask = np.zeros(action_dim(n, max_piles), dtype=bool)
    n_piles = len(state.piles)
    for (color, pile_target) in game.legal_actions(state):
        if pile_target < n_piles:
            if pile_target >= max_piles:
                continue  # NOTE: pile beyond the cap is not addressable this turn
            pile_slot = pile_target
        else:
            pile_slot = max_piles  # "new pile"
        idx = rot(color, me, n) * (max_piles + 1) + pile_slot
        mask[idx] = True
    return mask


def action_index_to_move(game: SLSGame, state: SLSState, idx: int, max_piles: int = MAX_PILES):
    """Decode a (masked) action index back to the engine's `(abs_color, pile_target)`."""
    n = game.n_players
    me = state.current_player
    ego_color, pile_slot = divmod(idx, max_piles + 1)
    abs_color = unrot(ego_color, me, n)
    pile_target = len(state.piles) if pile_slot == max_piles else pile_slot
    return (abs_color, pile_target)


def move_to_action_index(game: SLSGame, state: SLSState, move, max_piles: int = MAX_PILES) -> int:
    """Encode an engine `(color, pile_target)` into its fixed action index."""
    n = game.n_players
    me = state.current_player
    color, pile_target = move
    pile_slot = max_piles if pile_target >= len(state.piles) else pile_target
    return rot(color, me, n) * (max_piles + 1) + pile_slot


def _selftest():
    print("state_encoding self-test  (PREDICTIONS -- verify on a real run)")
    print("-" * 72)
    game = SLSGame(n_players=4, chips_per_player=7)
    s0 = game.initial_state()
    x = encode_state(game, s0)
    mask = legal_action_mask(game, s0)
    print(f"  obs_dim={x.shape[0]} (expect {obs_dim(4)}); action_dim={mask.shape[0]} "
          f"(expect {action_dim(4)})")
    print(f"  legal actions at open = {int(mask.sum())} "
          f"(PREDICT 1: only color 0 held, only 'new pile' available)")
    # round-trip: every legal engine action maps to a set mask bit and back
    ok = True
    for a in game.legal_actions(s0):
        idx = move_to_action_index(game, s0, a)
        back = action_index_to_move(game, s0, idx)
        ok = ok and (back == a) and mask[idx]
    print(f"  action index round-trip consistent? {ok} (must be True)")


if __name__ == "__main__":
    _selftest()
