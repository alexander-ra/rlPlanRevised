"""
bridge07.py -- connect this chapter's OpenSpiel-built trees to Chapter 7's engines and models.

Chapter 7's opponent models (type-based Bayesian, continuous Dirichlet, change-point detector)
speak Chapter 7's `Game` interface: policies are callables policy(game07, state07) and hands
are `Hand` namedtuples. This chapter simulates on its own array trees (for exact evaluation).
The bridge does three things:

  * state07(node)     : the Chapter 7 state that corresponds to a node of our tree
  * materialize(...)  : read a Chapter 7 policy callable into a behaviour array
  * hand07(...)       : turn a hand simulated on our tree into a Chapter 7 `Hand`

Card and action encodings: Kuhn -- OpenSpiel cards 0..2 are Chapter 2's 1..3, actions
pass=0 / bet=1 in both. Leduc -- Chapter 3's engine uses OpenSpiel's card ids 0..5 and
actions fold=0 / call=1 / raise=2 (it was built to match OpenSpiel exactly). The mapping is
verified in run_validation.py by comparing exact values computed both ways.
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401  (puts Step 07 on sys.path)
from engines import make_game, KuhnState          # Step 07
from policies import Hand, replay                 # Step 07

from trees import TabularGame, CHANCE, DECISION


class Bridge:
    def __init__(self, tg: TabularGame, name: str):
        assert name in ("kuhn", "leduc")
        self.tg, self.name = tg, name
        self.g07 = make_game(name)
        # representative node per (player, infoset)
        self.rep_node = [dict() for _ in range(tg.n_players)]
        for i in tg._dec_nodes:
            p, I = int(tg.player[i]), int(tg.infoset[i])
            self.rep_node[p].setdefault(I, int(i))
        self._state_cache = {}

    # ---------------------------------------------------------------- paths
    def path(self, node: int):
        """[(is_chance, action), ...] from the root to `node`."""
        tg = self.tg
        out = []
        while tg.parent[node] >= 0:
            par = tg.parent[node]
            out.append((tg.kind[par] == CHANCE, int(tg.action_in[node])))
            node = par
        return out[::-1]

    def deal07(self, chances):
        """Chapter 7 deal tuple from our chance outcomes (board filled if not dealt)."""
        if self.name == "kuhn":
            return (chances[0] + 1, chances[1] + 1)
        c0, c1 = chances[0], chances[1]
        if len(chances) >= 3:
            return (c0, c1, chances[2])
        filler = next(c for c in range(6) if c not in (c0, c1))
        return (c0, c1, filler)

    def state07(self, node: int):
        if node in self._state_cache:
            return self._state_cache[node]
        pth = self.path(node)
        chances = [a for ch, a in pth if ch]
        actions = [a for ch, a in pth if not ch]
        g = self.g07
        if self.name == "kuhn":
            st = KuhnState(self.deal07(chances), "".join("p" if a == 0 else "b" for a in actions))
        else:
            st = g.root(self.deal07(chances))
            for a in actions:
                st = g.apply(st, a)
        self._state_cache[node] = st
        return st

    # ---------------------------------------------------------------- policies
    def materialize(self, policy07, p: int) -> np.ndarray:
        tg = self.tg
        P = tg.players[p]
        B = np.zeros((len(P.infoset_strings), tg.n_actions))
        for I, node in self.rep_node[p].items():
            dist = policy07(self.g07, self.state07(node))
            for a, pr in dist.items():
                B[I, a] = pr
        return tg.normalize(p, B)

    def as_policy07(self, profile: list):
        """Wrap behaviour arrays as a Chapter 7 policy callable (looked up by info-set key)."""
        table = {}
        for p in range(self.tg.n_players):
            for I, node in self.rep_node[p].items():
                key = self.g07.info_set(self.state07(node), p)
                table[key] = {a: float(profile[p][I, a]) for a in self.tg.players[p].legal[I]}

        def policy(game, state):
            dist = table.get(game.info_set(state))
            if dist is None:
                legal = game.legal_actions(state)
                return {a: 1.0 / len(legal) for a in legal}
            return dist
        return policy

    # ---------------------------------------------------------------- hands
    def hand07(self, chances, actions):
        g = self.g07
        deal = self.deal07(chances)
        if self.name == "kuhn":
            st = KuhnState(deal, "")
        else:
            st = g.root(deal)
        for a in actions:
            st = g.apply(st, a)
        decisions = replay(g, deal, actions)
        util = (g.utility(st, 0), g.utility(st, 1))
        return Hand(tuple(deal), tuple(actions), tuple(decisions), util,
                    frozenset(g.revealed_privates(st)))
