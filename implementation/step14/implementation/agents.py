"""
agents.py -- the bot zoo's agent classes (two-player Kuhn / Leduc).

Every agent exposes the same small interface to the match runner:

    agent.start(tg, seat, rng)    # new match, fixed seat
    agent.policy()  -> B          # behaviour array for its seat (n_infosets x n_actions)
    agent.observe(rec)            # one finished hand (what it could see is decided inside)
    agent.version                 # incremented whenever policy() changes

Agents
------
* Stationary        : a fixed strategy (Nash blueprint, rule-based types, LLM-extracted,
                      static best responses).
* Switching         : plays agent A until hand T, then agent B (non-stationary opponent).
* TeachingAdversary : plays a bait strategy until hand T, then the exact best response to
                      the victim's CURRENT policy, recomputed every R hands (white-box
                      "teach-then-exploit" attack, the scenario adaptation safety targets).
* Adaptive          : Chapter 7's opponent models (type-based Bayesian posterior, continuous
                      Dirichlet model, optional Bayesian change-point reset) driving
                      Chapter 8's responses (full best response, RNR(p), best equilibrium),
                      refitted every `refit_every` hands, playing the blueprint until
                      `min_hands` observations have accrued (Chapter 7's AdaptiveExploiter
                      semantics, re-hosted on this chapter's exact arrays).
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401
from observation_buffer import ObservationBuffer          # Step 07
from type_based_model import TypeBasedModel                # Step 07
from continuous_model import ContinuousModel               # Step 07
from changepoint import BernoulliBOCPD, aggression_signal  # Step 07

from solvers import SafeLP


class HandRecord:
    """What happened in one hand (the runner fills it; agents read what they may see)."""
    __slots__ = ("t", "term", "chances", "actions", "hand07", "decisions")

    def __init__(self, t, term, chances, actions, hand07=None, decisions=None):
        self.t, self.term, self.chances, self.actions, self.hand07 = t, term, chances, actions, hand07
        self.decisions = decisions   # [(node, action), ...] in play order


class Agent:
    name = "agent"
    adaptive = False
    needs_hand07 = False

    def start(self, tg, seat, rng):
        self.tg, self.seat, self.rng = tg, seat, rng
        self.version = 0

    def policy(self):
        raise NotImplementedError

    def observe(self, rec: HandRecord):
        pass

    def begin_hand(self, t: int):
        pass


class Stationary(Agent):
    def __init__(self, name: str, profile: list):
        self.name, self.profile = name, profile

    def policy(self):
        return self.profile[self.seat]


class Switching(Agent):
    """Agent A for hands [0, T), agent B afterwards (both started on the same seat)."""
    adaptive = True

    def __init__(self, name: str, first: Agent, second: Agent, switch_at: int):
        self.name, self.first, self.second, self.T = name, first, second, switch_at
        self.needs_hand07 = first.needs_hand07 or second.needs_hand07

    def start(self, tg, seat, rng):
        super().start(tg, seat, rng)
        self.first.start(tg, seat, rng)
        self.second.start(tg, seat, rng)
        self.t = 0

    def _cur(self):
        return self.first if self.t < self.T else self.second

    def begin_hand(self, t):
        before = self._cur()
        self.t = t
        self._cur().begin_hand(t)
        if self._cur() is not before:
            self.version += 1

    def policy(self):
        return self._cur().policy()

    def observe(self, rec):
        v = self._cur().version
        self._cur().observe(rec)
        if self._cur().version != v:
            self.version += 1


class TeachingAdversary(Agent):
    """Bait until hand T, then best-respond (exactly, white-box) to the victim's current
    policy, re-computed every `refit_every` hands."""
    adaptive = True

    def __init__(self, name: str, bait: Agent, switch_at: int, refit_every: int = 50):
        self.name, self.bait, self.T, self.R = name, bait, switch_at, refit_every
        self.victim = None

    def attach(self, victim: Agent):
        self.victim = victim

    def start(self, tg, seat, rng):
        super().start(tg, seat, rng)
        self.bait.start(tg, seat, rng)
        self.t = 0
        self.B = None

    def begin_hand(self, t):
        self.t = t
        if t >= self.T and (self.B is None or (t - self.T) % self.R == 0):
            prof = [None, None]
            prof[1 - self.seat] = self.victim.policy()
            prof[self.seat] = self.tg.uniform(self.seat)
            _, self.B = self.tg.best_response(self.seat, prof, return_policy=True)
            self.version += 1

    def policy(self):
        return self.bait.policy() if self.t < self.T else self.B


class Adaptive(Agent):
    """Chapter 7 model + Chapter 8 response, refitted every `refit_every` hands."""
    adaptive = True
    needs_hand07 = True

    def __init__(self, name: str, bridge, blueprint: list, model: str = "cont",
                 response: str = "br", p: float = 0.5, changepoint: bool = False,
                 refit_every: int = 50, min_hands: int = 25, type_zoo07: dict | None = None,
                 v_star: tuple | None = None, lps: tuple | None = None):
        self.name = name
        self.bridge = bridge
        self.blueprint = blueprint
        self.model_kind = model
        self.response = response
        self.p = p
        self.use_cp = changepoint
        self.refit_every = refit_every
        self.min_hands = min_hands
        self.type_zoo07 = type_zoo07
        self.v_star = v_star
        self.lps = lps

    def start(self, tg, seat, rng):
        super().start(tg, seat, rng)
        g07 = self.bridge.g07
        if self.model_kind == "type":
            self.model = TypeBasedModel(g07, seat, self.type_zoo07, track=False)
        else:
            self.model = ContinuousModel(g07, seat)
        self.buffer = ObservationBuffer(g07, seat)
        self.detector = BernoulliBOCPD(hazard=1.0 / 150.0) if self.use_cp else None
        self.B = self.blueprint[seat]
        self.mode = "blueprint"
        self.n_seen = 0
        self.since_reset = 0
        self.changepoints = []
        self.refits = []

    def policy(self):
        return self.B

    def _response(self, opp_B):
        tg, s = self.tg, self.seat
        if self.response == "br":
            prof = [None, None]
            prof[s] = tg.uniform(s)
            prof[1 - s] = opp_B
            return tg.best_response(s, prof, return_policy=True)[1]
        lp = self.lps[s]
        if self.response == "rnr":
            return lp.rnr(opp_B, self.p, fill=self.blueprint[s])[0]
        if self.response == "besteq":
            return lp.floor(opp_B, self.v_star[s] - 1e-7, fill=self.blueprint[s])[0]
        raise ValueError(self.response)

    def observe(self, rec: HandRecord):
        obs = self.buffer.record(rec.hand07)
        self.model.update(obs)
        self.n_seen += 1
        self.since_reset += 1
        if self.use_cp:
            sig = aggression_signal(self.bridge.g07, obs)
            if sig is not None:
                self.detector.update(sig)
                # Chapter 7's detection rule: MAP run length < 10, at least 30 hands apart
                if self.since_reset > 30 and self.detector.map_change_detected(10):
                    self.model.reset()
                    self.detector.reset_runs()
                    self.changepoints.append(rec.t)
                    self.since_reset = 0
                    self.B = self.blueprint[self.seat]
                    self.mode = "blueprint"
                    self.version += 1
        if self.n_seen % self.refit_every == 0:
            if self.since_reset >= self.min_hands:
                opp_B = self.bridge.materialize(self.model.predicted_policy(), 1 - self.seat)
                self.B = self._response(opp_B)
                self.mode = self.response
            else:
                self.B = self.blueprint[self.seat]
                self.mode = "blueprint"
            self.refits.append(rec.t)
            self.version += 1


def make_lps(tg):
    return (SafeLP(tg, 0), SafeLP(tg, 1))


class MCLearner(Agent):
    """A black-box learned best response: tabular every-visit Monte-Carlo control with
    epsilon-greedy exploration over its own information sets. It sees only its own cards,
    the public actions and its payoff. `policy()` is the epsilon-greedy behaviour; `greedy()`
    the learned deterministic strategy (the approximate best response)."""
    adaptive = True

    def __init__(self, name: str = "MC-learner", eps: float = 0.1):
        self.name, self.eps = name, eps

    def start(self, tg, seat, rng):
        super().start(tg, seat, rng)
        P = tg.players[seat]
        self.Q = np.zeros((len(P.infoset_strings), tg.n_actions))
        self.N = np.zeros_like(self.Q)
        self.mask = P.legal_mask
        self._refresh()

    def _refresh(self):
        Qm = np.where(self.mask, self.Q, -np.inf)
        best = Qm.argmax(axis=1)
        G = np.zeros_like(self.Q)
        G[np.arange(len(G)), best] = 1.0
        self.G = G
        U = self.mask / self.mask.sum(axis=1, keepdims=True)
        self.B = (1 - self.eps) * G + self.eps * U
        self.version += 1

    def policy(self):
        return self.B

    def greedy(self):
        return self.G

    def observe(self, rec):
        u = self.tg.term_util[rec.term, self.seat]
        changed = False
        for node, a in rec.decisions:
            if self.tg.player[node] == self.seat:
                I = self.tg.infoset[node]
                self.N[I, a] += 1
                self.Q[I, a] += (u - self.Q[I, a]) / self.N[I, a]
                changed = True
        if changed and (rec.t + 1) % 10 == 0:
            self._refresh()
