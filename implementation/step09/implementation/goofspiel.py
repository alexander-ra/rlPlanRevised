"""
goofspiel.py -- a native, self-contained Goofspiel engine (raw step L122-129, L432-437).

WHAT THIS IS
------------
Goofspiel (a.k.a. the Game of Pure Strategy) is a SIMULTANEOUS-action bidding card game -- the
raw step uses it as a "real game" testbed for MARL, in contrast to the particle envs. This is
a from-scratch 2-player implementation with EXACT solvers for small deck sizes, so PSRO and
MCCFR-style comparisons can be run without OpenSpiel (which is offered as an optional
cross-check in `compare_openspiel.py`).

RULES (point-order variant, deterministic -> exact & small)
-----------------------------------------------------------
- A deck of K "prize" cards is revealed one per round, in a FIXED order (default: descending
  point value K, K-1, ..., 1). Fixing the order removes the chance root so the game is exactly
  solvable for small K; a random order just adds a uniform chance node at the root (a TODO
  cross-check note, not needed for the deliverable).
- Each player holds bid cards 1..K. Each round both SIMULTANEOUSLY play one card; the higher
  bid wins that round's prize points; a tie SPLITS the points. Cards are used once.
- After K rounds the player with more points wins. Terminal utility for player 0 is
  sign(score0 - score1) in {-1, 0, +1} (zero-sum).

Because bids are revealed each round, the game is PERFECT-INFORMATION with simultaneous moves:
the state (round, both hands, both scores) is public. That makes a pure strategy a map from
public states to a card, and it makes best response to a MIXTURE of opponent policies exact
via a single recursion that carries per-component reach weights (see
`best_response_value_vs_mixture`).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. numpy not required.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GoofState:
    round: int
    hand0: tuple           # remaining card indices for player 0 (0-based; bid value = idx+1)
    hand1: tuple
    score0: float
    score1: float


class Goofspiel:
    """2-player point-order Goofspiel with exact solvers for small K."""

    num_players = 2

    def __init__(self, num_cards: int = 4, prize_order: tuple | None = None):
        self.num_cards = int(num_cards)
        if prize_order is None:
            # descending point values revealed round by round
            prize_order = tuple(range(self.num_cards, 0, -1))
        if len(prize_order) != self.num_cards:
            raise ValueError("prize_order length must equal num_cards")
        self.prize_order = tuple(prize_order)
        self.name = f"goofspiel{self.num_cards}"

    # ---- structure ----
    def root(self) -> GoofState:
        hand = tuple(range(self.num_cards))
        return GoofState(0, hand, hand, 0.0, 0.0)

    def is_terminal(self, s: GoofState) -> bool:
        return s.round >= self.num_cards

    def legal_actions(self, s: GoofState, player: int) -> tuple:
        return s.hand0 if player == 0 else s.hand1

    def info_state(self, s: GoofState, player: int):
        """Public state key (perfect information). Player-agnostic apart from the label so a
        policy can be seat-aware if it wants."""
        return (player, s.round, s.hand0, s.hand1,
                round(s.score0, 6), round(s.score1, 6))

    def apply(self, s: GoofState, a0: int, a1: int) -> GoofState:
        prize = float(self.prize_order[s.round])
        bid0, bid1 = a0 + 1, a1 + 1
        sc0, sc1 = s.score0, s.score1
        if bid0 > bid1:
            sc0 += prize
        elif bid1 > bid0:
            sc1 += prize
        else:
            sc0 += prize / 2.0
            sc1 += prize / 2.0
        h0 = tuple(c for c in s.hand0 if c != a0)
        h1 = tuple(c for c in s.hand1 if c != a1)
        return GoofState(s.round + 1, h0, h1, sc0, sc1)

    def utility(self, s: GoofState, player: int) -> float:
        diff = s.score0 - s.score1
        u0 = 1.0 if diff > 1e-9 else (-1.0 if diff < -1e-9 else 0.0)
        return u0 if player == 0 else -u0

    # ---- exact expected value of a profile ----
    def exact_value(self, policy0, policy1) -> float:
        """Exact EV for player 0 when p0 plays policy0 and p1 plays policy1.

        A policy is `policy(game, state, player) -> {action_idx: prob}` over legal actions.
        """
        return self._value(self.root(), policy0, policy1)

    def _value(self, s, policy0, policy1) -> float:
        if self.is_terminal(s):
            return self.utility(s, 0)
        d0 = policy0(self, s, 0)
        d1 = policy1(self, s, 1)
        total = 0.0
        for a0, p0 in d0.items():
            if p0 <= 0.0:
                continue
            for a1, p1 in d1.items():
                if p1 <= 0.0:
                    continue
                total += p0 * p1 * self._value(self.apply(s, a0, a1), policy0, policy1)
        return total

    # ---- exact best response (hero vs a single opponent policy) ----
    def best_response_value(self, hero: int, opp_policy, return_table: bool = False):
        return self.best_response_value_vs_mixture(hero, [opp_policy], [1.0],
                                                   return_table=return_table)

    # ---- exact best response to a MIXTURE of opponent policies ----
    def best_response_value_vs_mixture(self, hero: int, opp_policies, weights,
                                       return_table: bool = False):
        """Best-response value for `hero` vs the opponent's mixed strategy (a distribution
        `weights` over `opp_policies`). Exact for perfect-recall simultaneous-move games:
        because the state is public, at every node the hero commits ONE action for all
        opponent components, and we carry each component's reach weight through the recursion.
        """
        opp = 1 - hero
        table = {} if return_table else None
        w = list(weights)

        def rec(s, reach):  # reach[j] = weight_j * (opp policy j's action-prob product so far)
            if self.is_terminal(s):
                w_sum = sum(reach)
                return w_sum * self.utility(s, hero)
            hero_legal = self.legal_actions(s, hero)
            opp_legal = self.legal_actions(s, opp)
            # opponent's per-component action distributions at this public state
            opp_dists = [opp_policies[j](self, s, opp) if reach[j] > 0.0 else {} for j in range(len(reach))]
            best_val = None
            best_a = hero_legal[0]
            for a_h in hero_legal:
                total = 0.0
                for a_o in opp_legal:
                    new_reach = [reach[j] * opp_dists[j].get(a_o, 0.0) for j in range(len(reach))]
                    if sum(new_reach) <= 0.0:
                        continue
                    if hero == 0:
                        ns = self.apply(s, a_h, a_o)
                    else:
                        ns = self.apply(s, a_o, a_h)
                    total += rec(ns, new_reach)
                if best_val is None or total > best_val:
                    best_val = total
                    best_a = a_h
            if table is not None:
                table[self.info_state(s, hero)] = best_a
            return best_val if best_val is not None else 0.0

        value = rec(self.root(), w) / (sum(w) if sum(w) != 0 else 1.0)
        if return_table:
            return value, table
        return value


# --- common policies ----------------------------------------------------------------
def uniform_policy():
    def policy(game, state, player):
        legal = game.legal_actions(state, player)
        p = 1.0 / len(legal)
        return {a: p for a in legal}
    return policy


def match_prize_policy():
    """Heuristic: bid the card whose value matches the current prize's rank if still held,
    else the highest remaining card. A reasonable non-trivial opponent."""
    def policy(game, state, player):
        legal = game.legal_actions(state, player)
        prize = game.prize_order[state.round]           # a point value in 1..K
        target = prize - 1                              # card index with that bid value
        if target in legal:
            return {target: 1.0}
        best = max(legal)
        return {best: 1.0}
    return policy


def table_policy(table: dict):
    """Wrap an info_state -> action table (from a best response) as a deterministic policy."""
    def policy(game, state, player):
        legal = game.legal_actions(state, player)
        a = table.get(game.info_state(state, player))
        if a is None or a not in legal:
            a = legal[0]
        return {a: 1.0}
    return policy


def behavioral_from_table(table: dict):
    """Alias for table_policy (kept for symmetry with the step07 policy vocabulary)."""
    return table_policy(table)


def _selftest():
    print("goofspiel self-test")
    print("-" * 60)
    for K in (3, 4):
        g = Goofspiel(num_cards=K)
        unif = uniform_policy()
        v = g.exact_value(unif, unif)
        br0 = g.best_response_value(0, unif)
        br1 = g.best_response_value(1, unif)
        print(f"[K={K}] value(uniform,uniform) for P0 = {v:+.4f} (expect ~0 by symmetry)")
        print(f"        BR0 vs uniform = {br0:+.4f}, BR1 vs uniform = {br1:+.4f} "
              f"(a best responder should beat uniform: both > 0 expected)")
        # a best response should be at least as good as playing uniform
        assert br0 >= v - 1e-9, "BR0 must dominate uniform value"


if __name__ == "__main__":
    _selftest()
