"""
sls_game.py -- a native, deterministic engine for So Long Sucker (SLS), the 4-player
free-for-all game invented in 1950 by Nash, Shapley, Shubik & Hausner to study coalition
formation and betrayal (raw step 11 L44-77, L354-382; env deliverable L547).

WHY NATIVE (not the Sharan & Adak external repo)
------------------------------------------------
WORKFLOW.md (S4.2/S6) requires the core to run on the repo's own code; Step 09 kept OpenSpiel /
PettingZoo optional for the same reason. So SLS is implemented here from the rules, to be
verified against De Carufel & Jerade's formalization via `sls_endgame.py` (raw L195-207, L557).

RULES IMPLEMENTED (from raw L92-98) -- with SIMPLIFICATIONS flagged
-------------------------------------------------------------------
- `n_players` players (default 4); each starts with `chips_per_player` (default 7) chips of
  their OWN color. A "hand" is a multiset over colors (you can hold other players' chips once
  you capture them -- that is the alliance mechanic).
- On a turn, the current player places ONE chip of a color they hold onto a pile: either an
  EXISTING pile (extends it) or a NEW pile.
- CAPTURE: when the top two chips of a pile share a color C, the player of color C captures --
  takes every chip BELOW the top into their hand (as prisoners they may later replay), and the
  top chip (color C) is "killed" (removed from the game). The pile is then removed. Capturing
  another player's chips and replaying them = the HELP signal the coalition detector reads.
- ELIMINATION: a player with NO chips in hand AND no chips on any pile is eliminated (raw L98).
- Last player standing wins.

  >>> NOTE / TODO (verify against De Carufel & Jerade, raw L195-207) <<<
  The real SLS specifies several details this engine SIMPLIFIES for a clean, terminating game;
  each is flagged with `# NOTE:` at its site and must be reconciled before trusting endgame runs:
    (a) after a capture the CAPTURER plays next (classic SLS lets the *matched* player choose who
        moves next -- a strategic lever this engine omits);
    (b) a player with an empty hand but chips still on the board is SKIPPED (passes) until a
        capture refills their hand -- classic SLS has richer "stuck"/forced-play rules;
    (c) `max_turns` + a most-chips tie-break resolves the (rare) all-stuck deadlock, rather than
        the formal draw/rotation rule.

DETERMINISM: the engine itself has NO chance nodes (SLS is a perfect-information deal). The only
randomness is in stochastic agent policies, which receive their own seeded RNG. So a fixed set
of policies + seeds is fully reproducible.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

NEW_PILE = "new"


@dataclass(frozen=True)
class SLSState:
    """An immutable snapshot of an SLS position.

    hands[p][c]   : number of color-c chips held by player p (a multiset per player).
    piles         : tuple of piles, each a tuple of colors bottom -> top.
    eliminated    : frozenset of eliminated player indices.
    current_player: whose turn it is (guaranteed not eliminated / not stuck, or `done`).
    done, winner  : terminal flag + winner (None until terminal; -1 on a deadlock tie-break).
    turn_count    : number of placements so far (for the max_turns safeguard).
    move_log      : tuple of MoveEvent, the full action history the coalition detector reads.
    """

    n_players: int
    hands: tuple
    piles: tuple
    eliminated: frozenset
    current_player: int
    done: bool = False
    winner: int | None = None
    turn_count: int = 0
    move_log: tuple = field(default_factory=tuple)


@dataclass(frozen=True)
class MoveEvent:
    """One recorded action + its coalition-relevant consequences (fed to CoalitionDetector)."""

    player: int            # who moved
    color: int             # the color chip they placed
    pile_target: int       # index of the pile extended, or len(piles) for a new pile
    is_help: bool          # placed a color != self (helps/handles that color's owner)
    helped_player: int     # the owner of the placed color (== color); -1 if self
    captured_by: int       # player who captured on this move (-1 if no capture)
    victim_colors: tuple   # colors (excluding the killed top) taken as prisoners by the capturer


class SLSGame:
    """Rules engine for So Long Sucker. Pure functions over `SLSState` (create -> legal_actions
    -> apply -> ... -> terminal). Hold no per-game mutable state so it is safe to reuse across
    self-play / Shapley rollouts."""

    def __init__(self, n_players: int = 4, chips_per_player: int = 7, max_turns: int = 400):
        if n_players < 2:
            raise ValueError("SLS needs at least 2 players.")
        self.n_players = n_players
        self.chips_per_player = chips_per_player
        self.max_turns = max_turns

    # ---- construction -----------------------------------------------------------------
    def initial_state(self) -> SLSState:
        """Deal: player p holds `chips_per_player` chips of color p, nothing else."""
        hands = tuple(
            tuple(self.chips_per_player if c == p else 0 for c in range(self.n_players))
            for p in range(self.n_players)
        )
        return SLSState(
            n_players=self.n_players,
            hands=hands,
            piles=(),
            eliminated=frozenset(),
            current_player=0,
        )

    # ---- queries ----------------------------------------------------------------------
    def current_player(self, state: SLSState) -> int:
        return state.current_player

    def is_terminal(self, state: SLSState) -> bool:
        return state.done

    def legal_actions(self, state: SLSState) -> list:
        """Actions for the current player: place a held color c on an existing pile index, or on
        a new pile (`pile_target == len(piles)`). Empty list if the player holds no chips."""
        if state.done:
            return []
        p = state.current_player
        hand = state.hands[p]
        colors = [c for c in range(self.n_players) if hand[c] > 0]
        n_piles = len(state.piles)
        actions = []
        for c in colors:
            for pile_idx in range(n_piles):
                actions.append((c, pile_idx))
            actions.append((c, n_piles))  # start a new pile
        return actions

    # ---- transition -------------------------------------------------------------------
    def apply(self, state: SLSState, action: tuple, rng=None) -> SLSState:
        """Place one chip, resolve a possible capture, update eliminations, advance the turn.

        `action = (color, pile_target)` with `pile_target in range(len(piles))` (extend) or
        `== len(piles)` (new pile). Returns a new terminal-or-ongoing `SLSState`.

        `rng`: optional numpy Generator used ONLY to break a most-chips deadlock/timeout tie
        uniformly (see `_most_chips`). Pass it from play/eval/train loops for an unbiased winner;
        omit it (exact endgame minimax) to keep the deterministic salt fallback.
        """
        if state.done:
            raise RuntimeError("apply() called on a terminal state.")
        color, pile_target = action
        p = state.current_player
        if state.hands[p][color] <= 0:
            raise ValueError(f"Player {p} does not hold color {color}: {state.hands[p]}")
        n_piles = len(state.piles)
        if not (0 <= pile_target <= n_piles):
            raise ValueError(f"pile_target {pile_target} out of range for {n_piles} piles.")

        hands = [list(h) for h in state.hands]
        piles = [list(pl) for pl in state.piles]

        # 1) place the chip (remove from hand, push onto pile top)
        hands[p][color] -= 1
        if pile_target == n_piles:
            piles.append([color])
        else:
            piles[pile_target].append(color)

        # 2) capture check on the touched pile: top two chips share a color?
        captured_by = -1
        victim_colors: tuple = ()
        touched = piles[pile_target]
        if len(touched) >= 2 and touched[-1] == touched[-2]:
            cap_color = touched[-1]
            captured_by = cap_color
            prisoners = touched[:-1]          # NOTE: everything below the killed top chip
            victim_colors = tuple(prisoners)
            for chip in prisoners:
                hands[cap_color][chip] += 1   # prisoners (incl. one own chip) go to the capturer
            # the top chip (color cap_color) is KILLED -- removed from the game entirely
            piles.pop(pile_target)

        # 3) recompute eliminations (no chips in hand AND none on any pile) -- raw L98
        eliminated = set(state.eliminated)
        on_board = [False] * self.n_players
        for pl in piles:
            for chip in pl:
                on_board[chip] = True
        for q in range(self.n_players):
            if q in eliminated:
                continue
            if sum(hands[q]) == 0 and not on_board[q]:
                eliminated.add(q)

        move = MoveEvent(
            player=p,
            color=color,
            pile_target=pile_target,
            is_help=(color != p),
            helped_player=(color if color != p else -1),
            captured_by=captured_by,
            victim_colors=victim_colors,
        )
        new_log = state.move_log + (move,)
        turn_count = state.turn_count + 1

        # 4) terminal checks
        alive = [q for q in range(self.n_players) if q not in eliminated]
        if len(alive) <= 1:
            winner = alive[0] if alive else -1
            return replace(
                state, hands=tuple(tuple(h) for h in hands), piles=tuple(tuple(pl) for pl in piles),
                eliminated=frozenset(eliminated), current_player=p, done=True, winner=winner,
                turn_count=turn_count, move_log=new_log,
            )

        # 5) choose the next mover
        if captured_by != -1 and captured_by not in eliminated and sum(hands[captured_by]) > 0:
            nxt = captured_by  # NOTE (a): capturer plays next (simplification)
        else:
            nxt = self._next_with_chips(hands, eliminated, start_after=p)

        if nxt is None:
            # NOTE (c): all-stuck deadlock -> tie-break by most total chips (hand + board)
            winner = self._most_chips(hands, piles, alive, salt=turn_count, rng=rng)
            return replace(
                state, hands=tuple(tuple(h) for h in hands), piles=tuple(tuple(pl) for pl in piles),
                eliminated=frozenset(eliminated), current_player=p, done=True, winner=winner,
                turn_count=turn_count, move_log=new_log,
            )

        done = turn_count >= self.max_turns
        winner = self._most_chips(hands, piles, alive, salt=turn_count, rng=rng) if done else None
        return replace(
            state, hands=tuple(tuple(h) for h in hands), piles=tuple(tuple(pl) for pl in piles),
            eliminated=frozenset(eliminated), current_player=nxt, done=done, winner=winner,
            turn_count=turn_count, move_log=new_log,
        )

    # ---- turn helpers -----------------------------------------------------------------
    def _next_with_chips(self, hands, eliminated, start_after: int):
        """Next player (clockwise from `start_after`) who is not eliminated and holds >=1 chip.
        NOTE (b): players with an empty hand but chips on the board are SKIPPED here."""
        for step in range(1, self.n_players + 1):
            q = (start_after + step) % self.n_players
            if q in eliminated:
                continue
            if sum(hands[q]) > 0:
                return q
        return None

    def _most_chips(self, hands, piles, alive, salt: int = 0, rng=None) -> int:
        """Tie-break winner = alive player controlling the most total chips (hand + board).

        Ties among equal-chip leaders are broken FAIRLY, not by lowest index. The original
        `total > best` scan silently handed every tie to the lowest-indexed player, which gave
        seat 0 a large systematic advantage (~2x fair share on symmetric positions) and
        confounded validation checks 3 and 5 (see EXECUTION_NOTES.md / WORKFLOW S0.1). The SLS
        dynamics themselves are symmetric (mean end-chips per seat are flat) and ~99% of random
        games end in a chip TIE, so the tied winner MUST be drawn uniformly:
          - if an `rng` is supplied (the normal play/eval/train path), pick uniformly at random;
          - else fall back to a `salt`-rotated deterministic pick (used by the exact endgame
            minimax, which must stay reproducible -- ties there are rare/small).
        A deterministic salt alone is insufficient: with 4 players cycling, any trajectory-derived
        integer (turn_count, move sums) stays correlated with seat index, so genuine randomness is
        required for an unbiased draw."""
        board = [0] * self.n_players
        for pl in piles:
            for chip in pl:
                board[chip] += 1
        totals = [sum(hands[q]) + board[q] for q in range(self.n_players)]
        best = max(totals[q] for q in alive)
        tied = [q for q in alive if totals[q] == best]
        if len(tied) == 1:
            return tied[0]
        if rng is not None:
            return int(tied[int(rng.integers(len(tied)))])
        return tied[salt % len(tied)]


def play_game(game: SLSGame, policies, seed: int = 0):
    """Run one full game. `policies[p](game, state, rng) -> action` picks a legal action for the
    player to move. Returns (final_state, rewards) with rewards = +1 winner / (-1/(N-1)) losers
    (raw L491). Deterministic given the policies + seed.
    """
    import numpy as np

    rng = np.random.default_rng(seed)
    state = game.initial_state()
    while not game.is_terminal(state):
        legal = game.legal_actions(state)
        if not legal:
            # current player is stuck; force-advance (defensive -- apply normally routes around this)
            nxt = game._next_with_chips([list(h) for h in state.hands], set(state.eliminated),
                                        state.current_player)
            if nxt is None:
                break
            state = replace(state, current_player=nxt)
            continue
        p = state.current_player
        action = policies[p](game, state, rng)
        state = game.apply(state, action, rng=rng)
    rewards = winner_rewards(game.n_players, state.winner)
    return state, rewards


def winner_rewards(n_players: int, winner: int | None):
    """Zero-sum-ish reward vector: +1 to the winner, -1/(N-1) to each loser (raw L489-491)."""
    import numpy as np

    r = np.full(n_players, -1.0 / (n_players - 1), dtype=float)
    if winner is not None and 0 <= winner < n_players:
        r[winner] = 1.0
    return r


def _selftest():
    import numpy as np

    print("sls_game self-test  (PREDICTIONS -- verify on a real run)")
    print("-" * 72)
    game = SLSGame(n_players=4, chips_per_player=7)
    s0 = game.initial_state()
    print(f"  initial: {game.n_players} players x {game.chips_per_player} chips; "
          f"legal actions for P0 = {len(game.legal_actions(s0))} "
          f"(PREDICT {game.n_players}: 1 color x (0 piles + 1 new) ... = 1 here)")

    def random_policy(g, s, rng):
        legal = g.legal_actions(s)
        return legal[int(rng.integers(len(legal)))]

    lengths, winners = [], []
    for seed in range(20):
        final, rewards = play_game(game, [random_policy] * 4, seed=seed)
        lengths.append(final.turn_count)
        winners.append(final.winner)
        assert final.done, "game did not terminate"
        assert abs(float(np.sum(rewards))) < 1e-9, "rewards must be zero-sum"
    print(f"  20 random games: all terminated; mean length={np.mean(lengths):.1f} turns; "
          f"winner distribution={np.bincount(np.array(winners), minlength=4).tolist()} "
          f"(PREDICT roughly uniform ~5 each; exact numbers to verify)")


if __name__ == "__main__":
    _selftest()
