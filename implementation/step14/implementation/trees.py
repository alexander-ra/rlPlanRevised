"""
trees.py -- one exact, array-based representation of a small imperfect-information game.

Every metric in Chapter 14 (exploitability, head-to-head values, AIVAT, the safe-exploitation
LPs, the coalition best response) needs the same few primitives: enumerate the game tree once,
index each player's information sets and sequences, and evaluate a strategy profile exactly.
This module builds that representation from OpenSpiel's own game definitions, so the numbers
can be cross-checked against OpenSpiel directly (same information-state strings), and it works
for any number of players (two-player Kuhn and Leduc, three-player Kuhn).

Conventions
-----------
* A *behaviour policy* for player p is an array B[p] of shape (n_infosets_p, n_actions) whose
  rows sum to 1 over the legal actions (zeros elsewhere). Action ids are OpenSpiel's.
* A *realization plan* r[p] (sequence form) has one entry per sequence of player p; entry 0 is
  the empty sequence (= 1).
* Values are in chips per hand, from the stated player's seat.
* NashConv(pi) = sum_p [max_{pi_p'} u_p(pi_p', pi_-p) - u_p(pi)]; OpenSpiel's exploitability is
  NashConv / n_players (Lanctot et al. 2019, OpenSpiel). Both names are used exactly.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

import numpy as np
import pyspiel

CHANCE, DECISION, TERMINAL = 0, 1, 2


@dataclass
class PlayerIndex:
    """Information sets and sequences of one player."""
    infoset_strings: list = field(default_factory=list)
    infoset_index: dict = field(default_factory=dict)
    legal: list = field(default_factory=list)            # list of legal-action lists
    rep_history: list = field(default_factory=list)      # a representative OpenSpiel history
    parent_seq: list = field(default_factory=list)       # sequence preceding the infoset
    depth: list = field(default_factory=list)            # own-decision depth of the infoset
    seq_id: np.ndarray | None = None                     # (nI, A) -> sequence id or -1
    seq_infoset: np.ndarray | None = None                # sequence -> infoset (-1 for empty)
    seq_action: np.ndarray | None = None
    n_seq: int = 1
    levels: list = field(default_factory=list)           # infosets grouped by depth


class TabularGame:
    """The full tree of a small OpenSpiel game, flattened into numpy arrays."""

    def __init__(self, game_string: str):
        self.game_string = game_string
        self.game = pyspiel.load_game(game_string)
        self.n_players = self.game.num_players()
        self.n_actions = self.game.num_distinct_actions()
        self.players = [PlayerIndex() for _ in range(self.n_players)]
        self._build()

    # ------------------------------------------------------------------ build
    def _build(self):
        n = self.n_players
        kind, player, infoset, parent, action_in = [], [], [], [], []
        chance_prob, reach_chance = [], []
        own_seq = []          # per node: tuple of each player's current sequence id
        priv = []             # per node: tuple of private cards (-1 if not dealt)
        pub = []              # per node: public-history key (string)
        children = []         # per node: list of (action, child)
        term_util = {}
        # temporary sequence allocation (sequence ids assigned on first visit of (I, a))
        seq_alloc = [dict() for _ in range(n)]  # (I, a) -> id
        next_seq = [1] * n

        def visit(state, par, a_in, cp, rc, seqs, cards, pubkey, n_decisions, hist):
            idx = len(kind)
            parent.append(par)
            action_in.append(a_in)
            chance_prob.append(cp)
            reach_chance.append(rc)
            own_seq.append(tuple(seqs))
            priv.append(tuple(cards))
            pub.append(pubkey)
            children.append([])
            if state.is_terminal():
                kind.append(TERMINAL); player.append(-4); infoset.append(-1)
                term_util[idx] = np.asarray(state.returns(), dtype=float)
                return idx
            if state.is_chance_node():
                kind.append(CHANCE); player.append(-1); infoset.append(-1)
                private_deal = (n_decisions == 0 and any(c < 0 for c in cards))
                for a, p in state.chance_outcomes():
                    if private_deal:
                        k = cards.index(-1)
                        nc = list(cards); nc[k] = a
                        child = visit(state.child(a), idx, a, p, rc * p, seqs, nc, pubkey,
                                      n_decisions, hist + [a])
                    else:
                        child = visit(state.child(a), idx, a, p, rc * p, seqs, cards,
                                      pubkey + f"|c{a}", n_decisions, hist + [a])
                    children[idx].append((a, child))
                return idx
            p = state.current_player()
            s = state.information_state_string(p)
            P = self.players[p]
            if s not in P.infoset_index:
                P.infoset_index[s] = len(P.infoset_strings)
                P.infoset_strings.append(s)
                P.legal.append(list(state.legal_actions()))
                P.rep_history.append(list(hist))
                P.parent_seq.append(seqs[p])
                P.depth.append(0)
            I = P.infoset_index[s]
            kind.append(DECISION); player.append(p); infoset.append(I)
            for a in state.legal_actions():
                key = (I, a)
                if key not in seq_alloc[p]:
                    seq_alloc[p][key] = next_seq[p]
                    next_seq[p] += 1
                ns = list(seqs); ns[p] = seq_alloc[p][key]
                child = visit(state.child(a), idx, a, 1.0, rc, ns, cards,
                              pubkey + f"|{p}:{a}", n_decisions + 1, hist + [a])
                children[idx].append((a, child))
            return idx

        root = self.game.new_initial_state()
        visit(root, -1, -1, 1.0, 1.0, [0] * n, [-1] * n, "", 0, [])

        self.n_nodes = len(kind)
        self.kind = np.asarray(kind, dtype=np.int8)
        self.player = np.asarray(player, dtype=np.int16)
        self.infoset = np.asarray(infoset, dtype=np.int32)
        self.parent = np.asarray(parent, dtype=np.int32)
        self.action_in = np.asarray(action_in, dtype=np.int32)
        self.chance_prob = np.asarray(chance_prob, dtype=float)
        self.reach_chance = np.asarray(reach_chance, dtype=float)
        self.node_seq = np.asarray(own_seq, dtype=np.int32)      # (N, n_players)
        self.priv = np.asarray(priv, dtype=np.int16)              # (N, n_players)
        self.pub = pub
        self.children = children
        # child lookup table (node, action) -> child id
        width = 1 + max(a for ch in children for a, _ in ch)
        self.child_width = width
        self.child_of = -np.ones((self.n_nodes, width), dtype=np.int32)
        for i, ch in enumerate(children):
            for a, c in ch:
                self.child_of[i, a] = c
        # terminals
        self.term_nodes = np.asarray(sorted(term_util), dtype=np.int32)
        self.n_term = len(self.term_nodes)
        self.term_id = -np.ones(self.n_nodes, dtype=np.int32)
        self.term_id[self.term_nodes] = np.arange(self.n_term)
        self.term_util = np.stack([term_util[i] for i in self.term_nodes])  # (Z, n)
        self.term_chance = self.reach_chance[self.term_nodes]
        self.term_seq = self.node_seq[self.term_nodes]                       # (Z, n)

        # per-player sequence tables and depth levels
        for p, P in enumerate(self.players):
            nI = len(P.infoset_strings)
            P.n_seq = next_seq[p]
            P.seq_id = -np.ones((nI, self.n_actions), dtype=np.int32)
            P.seq_infoset = -np.ones(P.n_seq, dtype=np.int32)
            P.seq_action = -np.ones(P.n_seq, dtype=np.int32)
            for (I, a), sid in seq_alloc[p].items():
                P.seq_id[I, a] = sid
                P.seq_infoset[sid] = I
                P.seq_action[sid] = a
            P.parent_seq = np.asarray(P.parent_seq, dtype=np.int32)
            depth = np.zeros(nI, dtype=np.int32)
            for I in range(nI):
                d, s = 0, P.parent_seq[I]
                while s != 0:
                    d += 1
                    s = P.parent_seq[P.seq_infoset[s]]
                depth[I] = d
            P.depth = depth
            P.levels = [np.where(depth == d)[0] for d in range(depth.max() + 1)]
            P.legal_mask = np.zeros((nI, self.n_actions), dtype=bool)
            for I, acts in enumerate(P.legal):
                P.legal_mask[I, acts] = True
        self._dec_nodes = np.where(self.kind == DECISION)[0]

    # ------------------------------------------------------------------ policies
    def uniform(self, p: int) -> np.ndarray:
        m = self.players[p].legal_mask.astype(float)
        return m / m.sum(axis=1, keepdims=True)

    def uniform_profile(self) -> list:
        return [self.uniform(p) for p in range(self.n_players)]

    def normalize(self, p: int, B: np.ndarray) -> np.ndarray:
        """Restrict to legal actions and renormalise (uniform on an all-zero row)."""
        m = self.players[p].legal_mask
        B = np.where(m, np.maximum(B, 0.0), 0.0)
        s = B.sum(axis=1, keepdims=True)
        U = m / m.sum(axis=1, keepdims=True)
        return np.where(s > 0, B / np.where(s > 0, s, 1.0), U)

    def realization(self, p: int, B: np.ndarray) -> np.ndarray:
        P = self.players[p]
        r = np.zeros(P.n_seq)
        r[0] = 1.0
        for lvl in P.levels:
            par = r[P.parent_seq[lvl]]                       # (k,)
            sids = P.seq_id[lvl]                             # (k, A)
            mask = sids >= 0
            vals = par[:, None] * B[lvl]
            r[sids[mask]] = vals[mask]
        return r

    def behaviour_from_realization(self, p: int, r: np.ndarray, fill: np.ndarray | None = None):
        P = self.players[p]
        nI = len(P.infoset_strings)
        B = np.zeros((nI, self.n_actions))
        par = r[P.parent_seq]
        for I in range(nI):
            for a in P.legal[I]:
                B[I, a] = r[P.seq_id[I, a]]
        s = B.sum(axis=1, keepdims=True)
        ok = (par > 1e-12)[:, None] & (s > 1e-12)
        U = fill if fill is not None else self.uniform(p)
        B = np.where(ok, B / np.where(s > 0, s, 1.0), U)
        return self.normalize(p, B)

    # ------------------------------------------------------------------ evaluation
    def _reach_terms(self, profile: list, skip: int | None = None) -> np.ndarray:
        w = self.term_chance.copy()
        for q in range(self.n_players):
            if q == skip:
                continue
            r = self.realization(q, profile[q])
            w *= r[self.term_seq[:, q]]
        return w

    def values(self, profile: list) -> np.ndarray:
        """Exact expected utility of every player under a behaviour profile."""
        w = self._reach_terms(profile)
        return w @ self.term_util

    def terminal_probs(self, profile: list) -> np.ndarray:
        return self._reach_terms(profile)

    def best_response(self, p: int, profile: list, return_policy: bool = False):
        """Exact best-response value of player p against the others' fixed behaviour."""
        P = self.players[p]
        w = self._reach_terms(profile, skip=p) * self.term_util[:, p]
        cv = np.bincount(self.term_seq[:, p], weights=w, minlength=P.n_seq)
        return self._br_backward(p, cv, return_policy)

    def _br_backward(self, p: int, cv: np.ndarray, return_policy: bool):
        P = self.players[p]
        childsum = np.zeros(P.n_seq)
        best_a = np.zeros(len(P.infoset_strings), dtype=np.int32)
        for lvl in reversed(P.levels):
            sids = P.seq_id[lvl]
            mask = sids >= 0
            vals = np.where(mask, cv[np.maximum(sids, 0)] + childsum[np.maximum(sids, 0)], -np.inf)
            best = vals.max(axis=1)
            best_a[lvl] = vals.argmax(axis=1)
            np.add.at(childsum, P.parent_seq[lvl], best)
        value = cv[0] + childsum[0]
        if not return_policy:
            return float(value)
        B = np.zeros((len(P.infoset_strings), self.n_actions))
        B[np.arange(len(B)), best_a] = 1.0
        return float(value), B

    def nash_conv(self, profile: list) -> dict:
        v = self.values(profile)
        br = [self.best_response(p, profile) for p in range(self.n_players)]
        gains = [br[p] - v[p] for p in range(self.n_players)]
        return {"values": v.tolist(), "br_values": br, "deviation_gains": gains,
                "nash_conv": float(sum(gains)),
                "exploitability": float(sum(gains)) / self.n_players}

    # ------------------------------------------------------------------ node values
    def node_values(self, profile: list, p: int) -> np.ndarray:
        """Expected utility of player p at every node under the profile (backward pass)."""
        V = np.zeros(self.n_nodes)
        V[self.term_nodes] = self.term_util[:, p]
        # nodes are in DFS preorder: children have larger ids than parents
        for i in range(self.n_nodes - 1, -1, -1):
            k = self.kind[i]
            if k == TERMINAL:
                continue
            ch = self.children[i]
            if k == CHANCE:
                V[i] = sum(self.chance_prob[c] * V[c] for _, c in ch)
            else:
                q = self.player[i]
                row = profile[q][self.infoset[i]]
                V[i] = sum(row[a] * V[c] for a, c in ch)
        return V

    # ------------------------------------------------------------------ two-player LP data
    def payoff_matrix_2p(self):
        """Sparse A with u0 = r0^T A r1 (two-player games only)."""
        import scipy.sparse as sp
        assert self.n_players == 2
        A = sp.coo_matrix((self.term_chance * self.term_util[:, 0],
                           (self.term_seq[:, 0], self.term_seq[:, 1])),
                          shape=(self.players[0].n_seq, self.players[1].n_seq)).tocsr()
        return A

    def treeplex_matrix(self, p: int):
        """F with F r = e_0 : row 0 pins the empty sequence, one row per infoset."""
        import scipy.sparse as sp
        P = self.players[p]
        nI = len(P.infoset_strings)
        rows, cols, vals = [0], [0], [1.0]
        for I in range(nI):
            rows.append(I + 1); cols.append(int(P.parent_seq[I])); vals.append(-1.0)
            for a in P.legal[I]:
                rows.append(I + 1); cols.append(int(P.seq_id[I, a])); vals.append(1.0)
        F = sp.coo_matrix((vals, (rows, cols)), shape=(nI + 1, P.n_seq)).tocsr()
        f = np.zeros(nI + 1); f[0] = 1.0
        return F, f

    # ------------------------------------------------------------------ openspiel bridge
    def state_for(self, p: int, I: int):
        s = self.game.new_initial_state()
        for a in self.players[p].rep_history[I]:
            s.apply_action(a)
        return s

    def from_pyspiel_policy(self, pol) -> list:
        """Convert an OpenSpiel (C++ or python) policy into behaviour arrays."""
        prof = []
        for p, P in enumerate(self.players):
            B = np.zeros((len(P.infoset_strings), self.n_actions))
            for I in range(len(P.infoset_strings)):
                st = self.state_for(p, I)
                probs = pol.action_probabilities(st)
                for a, pr in probs.items():
                    B[I, a] = pr
            prof.append(self.normalize(p, B))
        return prof

    def to_openspiel_tabular(self, profile: list):
        from open_spiel.python import policy as os_policy
        tab = os_policy.TabularPolicy(self.game)
        for p, P in enumerate(self.players):
            for I, s in enumerate(P.infoset_strings):
                row = tab.state_lookup[s]
                tab.action_probability_array[row, :] = 0.0
                for a in P.legal[I]:
                    tab.action_probability_array[row, a] = profile[p][I, a]
        return tab

    # ------------------------------------------------------------------ sampling
    def sample_hand(self, profile: list, rng: np.random.Generator, chance_seq=None):
        """Play one hand. `chance_seq` (optional) fixes the chance outcomes in order,
        for duplicate dealing; missing/illegal entries fall back to sampling.
        Returns (terminal_id, list of (node, action) decisions, chance outcomes)."""
        i = 0
        decisions, chances = [], []
        ci = 0
        while self.kind[i] != TERMINAL:
            ch = self.children[i]
            if self.kind[i] == CHANCE:
                a = None
                if chance_seq is not None and ci < len(chance_seq):
                    want = chance_seq[ci]
                    if 0 <= want < self.child_width and self.child_of[i, want] >= 0:
                        a = want
                if a is None:
                    probs = np.array([self.chance_prob[c] for _, c in ch])
                    a = ch[rng.choice(len(ch), p=probs / probs.sum())][0]
                ci += 1
                chances.append(a)
                i = self.child_of[i, a]
            else:
                q = self.player[i]
                row = profile[q][self.infoset[i]]
                acts = [a for a, _ in ch]
                pr = np.array([row[a] for a in acts])
                a = acts[rng.choice(len(acts), p=pr / pr.sum())]
                decisions.append((i, a))
                i = self.child_of[i, a]
        return int(self.term_id[i]), decisions, chances


def pure_strategies(tg: TabularGame, p: int):
    """Enumerate all pure behaviour strategies of player p as realization plans (small games
    only). Returns an array of shape (n_pure, n_seq)."""
    P = tg.players[p]
    nI = len(P.infoset_strings)
    choices = [P.legal[I] for I in range(nI)]
    total = int(np.prod([len(c) for c in choices]))
    R = np.zeros((total, P.n_seq))
    R[:, 0] = 1.0
    # iterate combos in blocks
    for k, combo in enumerate(itertools.product(*choices)):
        for lvl in P.levels:
            for I in lvl:
                a = combo[I]
                R[k, P.seq_id[I, a]] = R[k, P.parent_seq[I]]
    return R


GAMES = {"kuhn": "kuhn_poker", "leduc": "leduc_poker", "kuhn3": "kuhn_poker(players=3)"}

_CACHE: dict = {}


def load(name: str) -> TabularGame:
    if name not in _CACHE:
        _CACHE[name] = TabularGame(GAMES.get(name, name))
    return _CACHE[name]
