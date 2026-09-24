"""
simulate.py -- the match runner (two-player, fixed seats, duplicate dealing).

A *match* is `n_hands` hands between an agent under test (fixed seat) and an opponent. For
every hand the runner records four estimates of the agent's result:

    chips   : the realised payoff (what a human-facing leaderboard would count)
    aivat   : AIVAT with chance + the agent's own strategy known (opponent unknown)
    ev      : the exact expected payoff of the two policies in force for this hand
              ("policy-exact"; only available when both strategies are visible, as in a
              bot-vs-bot simulation -- it removes all card and action luck)
    expo    : the agent's current seat exposure  v*_seat - worst-case value  (>= 0)

Duplicate dealing: the deck order of hand t is drawn from `deal_seed`; the seat-swapped
match reuses it with the two private cards exchanged, so the agent holds the same cards in
both seats (the standard duplicate-poker protocol, Bard et al. 2013).
"""

from __future__ import annotations

import numpy as np

from agents import HandRecord, TeachingAdversary
from solvers import seat_exposure


def draw_decks(n_hands: int, n_cards: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.stack([rng.permutation(n_cards) for _ in range(n_hands)])


def seat_decks(decks: np.ndarray, seat: int) -> np.ndarray:
    """Deck orders as seen from `seat`: the agent always receives the card at position 0."""
    if seat == 0:
        return decks
    d = decks.copy()
    d[:, [0, 1]] = d[:, [1, 0]]
    return d


def play_match(tg, bridge, agent, opp, seat: int, n_hands: int, decks: np.ndarray,
               act_seed: int, aivat_tab=None, v_ref=None, v_star=None,
               track_exposure: bool = True) -> dict:
    rng = np.random.default_rng(act_seed)
    agent.start(tg, seat, np.random.default_rng(act_seed + 1))
    opp.start(tg, 1 - seat, np.random.default_rng(act_seed + 2))
    if isinstance(opp, TeachingAdversary):
        opp.attach(agent)
    need07 = agent.needs_hand07 or opp.needs_hand07
    chips = np.zeros(n_hands)
    ev = np.zeros(n_hands)
    aiv = np.zeros(n_hands)
    expo = np.zeros(n_hands)
    ev_cache = {}
    last_a_version = None
    aiv_table = None
    cur_expo = np.nan
    prof = [None, None]
    for t in range(n_hands):
        agent.begin_hand(t)
        opp.begin_hand(t)
        Ba, Bo = agent.policy(), opp.policy()
        prof[seat], prof[1 - seat] = Ba, Bo
        if agent.version != last_a_version:
            last_a_version = agent.version
            ev_cache = {k: v for k, v in ev_cache.items() if k[0] == agent.version}
            if aivat_tab is not None:
                aiv_table = aivat_tab.table(Ba, v_ref)
            if track_exposure and v_star is not None:
                cur_expo = seat_exposure(tg, seat, Ba, v_star[seat])
        key = (agent.version, opp.version)
        if key not in ev_cache:
            ev_cache[key] = float(tg.values(prof)[seat])
        term, decisions, chances = tg.sample_hand(prof, rng, chance_seq=decks[t])
        chips[t] = tg.term_util[term, seat]
        ev[t] = ev_cache[key]
        aiv[t] = aiv_table[term] if aiv_table is not None else np.nan
        expo[t] = cur_expo
        actions = [a for _, a in decisions]
        h07 = bridge.hand07(chances, actions) if need07 else None
        rec = HandRecord(t, term, chances, actions, h07, decisions)
        agent.observe(rec)
        opp.observe(rec)
    out = {"chips": chips, "ev": ev, "aivat": aiv, "expo": expo}
    for nm, ag in (("agent", agent), ("opp", opp)):
        if hasattr(ag, "changepoints"):
            out[f"{nm}_changepoints"] = list(ag.changepoints)
    return out
