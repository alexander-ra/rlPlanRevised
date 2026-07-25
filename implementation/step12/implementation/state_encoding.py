"""
state_encoding.py  [CORE / thesis-critical]  -- raw L234-282.

The Decision Transformer's INPUT is a fixed-dimension state tensor. This module builds it, and
it is the single most thesis-relevant artifact in Step 12: the SAME encoding design carries to
Step 13's Playtech behavioral-cloning pipeline (raw L155, L498). Get the features right here and
Step 13 inherits them; get them wrong and every downstream behavioral pattern is distorted.

WHAT WE ENCODE (raw L244-253)
-----------------------------
  - cards      : one-hot of the acting player's private card rank
  - board      : one-hot of the community-card rank (Leduc; all-zero for Kuhn) + a present flag
  - position   : 0/1 dealer indicator (in these engines: player index, player 0 acts first)
  - pot        : normalized pot size (chips in the middle / a fixed per-game scale)
  - stack      : normalized remaining stack (starting stack - own committed) / starting stack
  - history    : the betting sequence, one-hot per ply over the action set (fixed length, padded)
  - round_flag : current betting round (0 preflop / 1 postflop; always 0 for Kuhn)

DESIGN NOTES
------------
- The encoder is GAME-AWARE (Kuhn vs Leduc) but ENGINE-AGNOSTIC in its interface: it reads a
  `state` produced by step07's `make_game(...)` adapters (`KuhnState` or `LeducState`) plus the
  acting `player`. Kuhn is fully validated this session; Leduc is the SCALE-only extension.
- Normalization constants (`pot_scale`, `stack_scale`) are ARBITRARY BUT CONSISTENT -- their job
  is only to keep features O(1); the DT is invariant to the exact choice as long as it is fixed.
- Deterministic and torch-free (pure numpy), so it can be exercised without the neural stack.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# Action ids match the engines (Kuhn PASS=0/BET=1; Leduc FOLD=0/CHECK_CALL=1/RAISE=2).
_KUHN_ACTIONS = 2
_LEDUC_ACTIONS = 3

# Max plies (history length) we reserve slots for, per game. Kuhn's longest pre-terminal history
# is "pb" (len 2); we keep 3 for safety. Leduc can run two rounds of up to a few actions each.
_KUHN_MAX_PLIES = 3
_LEDUC_MAX_PLIES = 8


@dataclass
class EncoderSpec:
    """Immutable description of one game's feature layout (for docs / debugging / Step 13)."""

    game: str
    num_ranks: int          # distinct card ranks (Kuhn 3: J,Q,K; Leduc 3: J,Q,K)
    num_actions: int
    max_plies: int
    has_board: bool
    pot_scale: float
    stack_scale: float
    segments: list = field(default_factory=list)  # (name, size) in order

    @property
    def dim(self) -> int:
        return sum(sz for _, sz in self.segments)


class PokerStateEncoder:
    """Fixed-dim state tensor for the Decision Transformer.

    Usage:
        enc = PokerStateEncoder("kuhn")
        vec = enc.encode(game, state, player)      # np.ndarray, shape (enc.state_dim,)
    """

    def __init__(self, game_name: str):
        name = game_name.lower()
        if name == "kuhn":
            self.spec = self._kuhn_spec()
        elif name == "leduc":
            self.spec = self._leduc_spec()
        else:
            raise ValueError(f"No encoder for game {game_name!r}; use 'kuhn' or 'leduc'.")
        self.game_name = name

    # ---- public ----
    @property
    def state_dim(self) -> int:
        return self.spec.dim

    def feature_names(self) -> list:
        """Human-readable name for every scalar slot (len == state_dim)."""
        names = []
        for seg_name, size in self.spec.segments:
            if size == 1:
                names.append(seg_name)
            else:
                names.extend(f"{seg_name}[{i}]" for i in range(size))
        return names

    def encode(self, game, state, player: int) -> np.ndarray:
        """Encode `state` from `player`'s perspective into a length-`state_dim` float32 vector."""
        if self.game_name == "kuhn":
            return self._encode_kuhn(state, player)
        return self._encode_leduc(state, player)

    # ---- specs ----
    def _kuhn_spec(self) -> EncoderSpec:
        segments = [
            ("card_onehot", 3),
            ("board_onehot", 3),
            ("board_present", 1),
            ("position", 1),
            ("pot", 1),
            ("stack", 1),
            ("history", _KUHN_MAX_PLIES * _KUHN_ACTIONS),
            ("round_flag", 1),
        ]
        return EncoderSpec(
            game="kuhn", num_ranks=3, num_actions=_KUHN_ACTIONS, max_plies=_KUHN_MAX_PLIES,
            has_board=False, pot_scale=4.0, stack_scale=2.0, segments=segments,
        )

    def _leduc_spec(self) -> EncoderSpec:
        segments = [
            ("card_onehot", 3),
            ("board_onehot", 3),
            ("board_present", 1),
            ("position", 1),
            ("pot", 1),
            ("stack", 1),
            ("history", _LEDUC_MAX_PLIES * _LEDUC_ACTIONS),
            ("round_flag", 1),
        ]
        return EncoderSpec(
            game="leduc", num_ranks=3, num_actions=_LEDUC_ACTIONS, max_plies=_LEDUC_MAX_PLIES,
            has_board=True, pot_scale=30.0, stack_scale=15.0, segments=segments,
        )

    # ---- Kuhn ----
    def _encode_kuhn(self, state, player: int) -> np.ndarray:
        # KuhnState: .cards (p0_card, p1_card) in {1,2,3}, .history str of 'p'/'b'.
        card = int(state.cards[player])
        history = state.history

        v = np.zeros(self.state_dim, dtype=np.float32)
        idx = self._layout_index()

        # cards: rank = card-1 (J=1->0, Q=2->1, K=3->2)
        v[idx["card_onehot"] + (card - 1)] = 1.0
        # board: none in Kuhn (board_onehot stays 0, board_present stays 0)
        # position
        v[idx["position"]] = float(player)
        # pot / stack
        pot = 2.0 + history.count("b")  # 2 antes + 1 per bet
        committed = 1.0 + sum(1 for i, ch in enumerate(history) if ch == "b" and i % 2 == player)
        v[idx["pot"]] = pot / self.spec.pot_scale
        v[idx["stack"]] = (self.spec.stack_scale - committed) / self.spec.stack_scale
        # history one-hot per ply (action id: 'p'->0, 'b'->1)
        self._fill_history(v, idx["history"], history, {"p": 0, "b": 1}, _KUHN_ACTIONS)
        # round flag: Kuhn is single-round
        v[idx["round_flag"]] = 0.0
        return v

    # ---- Leduc ----
    def _encode_leduc(self, state, player: int) -> np.ndarray:
        # LeducState: .cards (c0,c1) in 0..5, .community int, .history str ('c','r','f','/'),
        # .round int, .bets [int,int]. rank = card // 2.
        card = int(state.cards[player])
        rank = card // 2
        history = state.history
        rnd = int(getattr(state, "round", 0))

        v = np.zeros(self.state_dim, dtype=np.float32)
        idx = self._layout_index()

        v[idx["card_onehot"] + rank] = 1.0
        if rnd >= 1:  # board is public only from round 1
            board_rank = int(state.community) // 2
            v[idx["board_onehot"] + board_rank] = 1.0
            v[idx["board_present"]] = 1.0
        v[idx["position"]] = float(player)

        bets = list(getattr(state, "bets", [1, 1]))
        pot = float(sum(bets))
        committed = float(bets[player])
        v[idx["pot"]] = pot / self.spec.pot_scale
        v[idx["stack"]] = (self.spec.stack_scale - committed) / self.spec.stack_scale

        # history: drop round separators for the per-ply encoding (round is captured by round_flag)
        actions_only = history.replace("/", "")
        self._fill_history(v, idx["history"], actions_only,
                           {"f": 0, "c": 1, "r": 2}, _LEDUC_ACTIONS)
        v[idx["round_flag"]] = float(min(rnd, 1))
        return v

    # ---- helpers ----
    def _fill_history(self, v: np.ndarray, base: int, history: str,
                      char_to_id: dict, num_actions: int) -> None:
        """One-hot each ply (up to max_plies) at [base + ply*num_actions + action_id]."""
        for ply, ch in enumerate(history[: self.spec.max_plies]):
            aid = char_to_id.get(ch)
            if aid is None:
                continue
            v[base + ply * num_actions + aid] = 1.0

    def _layout_index(self) -> dict:
        """Map each segment name to its starting index in the flat vector."""
        out, cursor = {}, 0
        for name, size in self.spec.segments:
            out[name] = cursor
            cursor += size
        return out


# --- self-test (you run this) --------------------------------------------------------
def _selftest():
    import deps  # noqa: F401  (bootstraps step02/step07 onto sys.path)
    from engines import make_game, KuhnState

    print("state_encoding self-test")
    print("-" * 60)
    enc = PokerStateEncoder("kuhn")
    game = make_game("kuhn")
    print(f"[kuhn] state_dim = {enc.state_dim}")
    print(f"[kuhn] segments  = {enc.spec.segments}")

    # Encode every Kuhn info set (all 12) and check shape + one-hot validity of the card block.
    p0_sets = ["1", "2", "3", "1pb", "2pb", "3pb"]
    p1_sets = ["1p", "2p", "3p", "1b", "2b", "3b"]
    bad = 0
    for iset in p0_sets + p1_sets:
        card = int(iset[0])
        history = iset[1:]
        player = len(history) % 2
        # Put the acting player's card at their seat; the other seat is a dummy distinct card.
        other = 1 if card != 1 else 2
        cards = (card, other) if player == 0 else (other, card)
        s = KuhnState(cards, history)
        vec = enc.encode(game, s, player)
        if vec.shape != (enc.state_dim,):
            bad += 1
        if abs(vec[:3].sum() - 1.0) > 1e-6:  # exactly one card bit set
            bad += 1
    print(f"[kuhn] encoded all 12 info sets; validity failures = {bad} (expect 0)")

    enc_l = PokerStateEncoder("leduc")
    print(f"[leduc] state_dim = {enc_l.state_dim}")
    print(f"[leduc] feature_names[:8] = {enc_l.feature_names()[:8]}")
    print("done.")


if __name__ == "__main__":
    _selftest()
