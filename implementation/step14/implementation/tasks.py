"""
tasks.py -- one match as a picklable task, for multiprocessing pools.

Opponent specifications (strings):
    "Name"                   a zoo agent
    "SW:A>B@T"               plays A for hands [0, T), then B          (switching opponent)
    "TEACH:A@T"              bait A until T, then white-box best response to the agent under
                             test, re-computed every 50 hands           (teaching attack)
Seeds: the deck order depends only on (game, seed) -- common random numbers across all pairs
of a seed -- and the seat-swapped match reuses it with the private cards exchanged
(duplicate). The action-sampling seed depends on (game, agent, opponent, seed, seat).
"""

from __future__ import annotations

import zlib

import numpy as np

import zoo
import aivat
import simulate
from agents import Switching, TeachingAdversary, MCLearner

N_CARDS = {"kuhn": 3, "leduc": 6}
_AIV: dict = {}


def build(ctx, spec: str):
    if spec.startswith("SW:"):
        body, T = spec[3:].split("@")
        a, b = body.split(">")
        return Switching(spec, ctx.agent(a), ctx.agent(b), int(T))
    if spec == "MC-learner":
        return MCLearner()
    if spec.startswith("TEACH:"):
        a, T = spec[6:].split("@")
        return TeachingAdversary(spec, ctx.agent(a), int(T), refit_every=50)
    return ctx.agent(spec)


def aivat_tab(game, seat):
    key = (game, seat)
    if key not in _AIV:
        _AIV[key] = aivat.AivatTables(zoo.context(game).tg, seat, "chance+x")
    return _AIV[key]


def run(args):
    """args = (game, agent_spec, opp_spec, seed, seat, n_hands). Returns float32 arrays."""
    game, a, o, seed, seat, n = args
    ctx = zoo.context(game)
    decks = simulate.seat_decks(simulate.draw_decks(n, N_CARDS[game], 10_000 + seed), seat)
    act_seed = zlib.crc32(f"{game}|{a}|{o}|{seed}|{seat}".encode()) % (2 ** 31)
    agent, opp = build(ctx, a), build(ctx, o)
    r = simulate.play_match(ctx.tg, ctx.bridge, agent, opp, seat, n, decks, act_seed,
                            aivat_tab(game, seat), ctx.v_ref(seat), ctx.v_star)
    out = {k: np.asarray(v, dtype=np.float32) for k, v in r.items() if isinstance(v, np.ndarray)}
    out["meta"] = (game, a, o, seed, seat, n)
    for k in ("agent_changepoints",):
        if k in r:
            out[k] = r[k]
    return out
