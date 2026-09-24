"""
zoo.py -- the bot zoo for two-player Kuhn and Leduc.

Tiers (each agent's provenance is recorded in ZOO_NOTES):
  equilibrium : Nash -- OpenSpiel C++ CFR+ average strategy (Kuhn 10 000 it., Leduc 2 000 it.)
  trivial     : Random (uniform)
  rule-based  : Chapter 7's type zoo, eps-smoothed (Kuhn: AlwaysPass, AlwaysBet, TightPassive,
                LooseAggr, Threshold; Leduc: CallingStation, Maniac, Rock, LoosePassive)
  LLM-derived : Chapter 12's Kuhn strategies extracted from real language models
                (next-token log-probabilities, temperature 0.7, plain prompt):
                Qwen2.5-7B-Instruct, gpt-oss-20b, OpenThinker3-7B
  specialist  : a static exact best response to one weak type (BR-Tight / BR-Rock) -- maximal
                gain against that type, no adaptation
  adaptive    : Chapter 7 models x Chapter 8 responses
                TypeBR   -- type-based Bayesian posterior, best response
                DirBR    -- continuous Dirichlet model, best response
                DirBR-CP -- DirBR + Bayesian change-point reset (Chapter 7)
                RNR(0.5) -- continuous model, restricted Nash response p = 0.5 (Chapter 8)
                BestEq   -- continuous model, best equilibrium (max EV vs model s.t. worst
                            case >= v*): Ganzfried-Sandholm's best-equilibrium baseline
"""

from __future__ import annotations

import json
import os

import numpy as np

import deps
import trees
import solvers
from bridge07 import Bridge
from agents import Stationary, Adaptive, make_lps
from opponent_types import make_type_zoo           # Step 07

BLUEPRINT_ITERS = {"kuhn": 10000, "leduc": 2000}

TYPES = {"kuhn": {"AlwaysPass": "AlwaysPass", "AlwaysBet": "AlwaysBet",
                  "TightPassive": "TightPassive", "LooseAggr": "LooseAggressive",
                  "Threshold": "Thresholdish"},
         "leduc": {"CallingStation": "CallingStation", "Maniac": "Maniac", "Rock": "Rock",
                   "LoosePassive": "LoosePassive"}}
LLM_FILES = {"LLM-Qwen7B": "strategy_qwen2.5-7b-instruct_plain.json",
             "LLM-GPT20B": "strategy_openai_gpt-oss-20b_plain.json",
             "LLM-OT7B": "strategy_openthinker3-7b_plain.json"}
SPECIALIST = {"kuhn": ("BR-Tight", "TightPassive"), "leduc": ("BR-Rock", "Rock")}
ADAPTIVE = ["TypeBR", "DirBR", "DirBR-CP", "RNR(0.5)", "BestEq"]
REFIT_EVERY, MIN_HANDS = 50, 25


class Context:
    def __init__(self, name: str):
        self.name = name
        self.tg = trees.load(name)
        self.bridge = Bridge(self.tg, name)
        self.blueprint = solvers.cfr_profile(self.tg, BLUEPRINT_ITERS[name])
        self.lps = make_lps(self.tg)
        self.v_star = tuple(lp.game_value() for lp in self.lps)
        self.types07 = make_type_zoo(self.bridge.g07)
        self.profiles = {"Nash": self.blueprint, "Random": self.tg.uniform_profile()}
        for short, long in TYPES[name].items():
            pol = self.types07[long]
            self.profiles[short] = [self.bridge.materialize(pol, 0),
                                    self.bridge.materialize(pol, 1)]
        if name == "kuhn":
            for short, fn in LLM_FILES.items():
                self.profiles[short] = self._llm_profile(fn)
        spec, target = SPECIALIST[name]
        tprof = self.profiles[target]
        sp = []
        for s in (0, 1):
            prof = [None, None]
            prof[s] = self.tg.uniform(s)
            prof[1 - s] = tprof[1 - s]
            sp.append(self.tg.best_response(s, prof, return_policy=True)[1])
        self.profiles[spec] = sp
        self.stationary_names = list(self.profiles)
        self.adaptive_names = list(ADAPTIVE)
        self.names = self.stationary_names + self.adaptive_names
        self._vref = {}

    def _llm_profile(self, fn: str):
        with open(os.path.join(deps.STEP12_RESULTS, fn), encoding="utf-8") as fh:
            strat = json.load(fh)["strategy"]
        prof = []
        for p in (0, 1):
            P = self.tg.players[p]
            B = np.zeros((len(P.infoset_strings), self.tg.n_actions))
            for I, s in enumerate(P.infoset_strings):
                key = str(int(s[0]) + 1) + s[1:]
                B[I, :] = strat[key]
            prof.append(self.tg.normalize(p, B))
        return prof

    def v_ref(self, seat: int):
        """Node values for `seat` under blueprint self-play (AIVAT's value function)."""
        if seat not in self._vref:
            self._vref[seat] = self.tg.node_values(self.blueprint, seat)
        return self._vref[seat]

    def agent(self, name: str):
        if name in self.profiles:
            return Stationary(name, self.profiles[name])
        common = dict(bridge=self.bridge, blueprint=self.blueprint,
                      refit_every=REFIT_EVERY, min_hands=MIN_HANDS,
                      type_zoo07=self.types07, v_star=self.v_star, lps=self.lps)
        if name == "TypeBR":
            return Adaptive(name, model="type", response="br", **common)
        if name == "DirBR":
            return Adaptive(name, model="cont", response="br", **common)
        if name == "DirBR-CP":
            return Adaptive(name, model="cont", response="br", changepoint=True, **common)
        if name == "RNR(0.5)":
            return Adaptive(name, model="cont", response="rnr", p=0.5, **common)
        if name == "BestEq":
            return Adaptive(name, model="cont", response="besteq", **common)
        raise KeyError(name)

    def is_adaptive(self, name: str) -> bool:
        return name in self.adaptive_names


_CTX: dict = {}


def context(name: str) -> Context:
    if name not in _CTX:
        _CTX[name] = Context(name)
    return _CTX[name]
