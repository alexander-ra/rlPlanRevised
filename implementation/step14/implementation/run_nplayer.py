"""
run_nplayer.py -- E4: what extends to three-player Kuhn, and what does not
(+ failure modes 2 and 8).

    python run_nplayer.py [--seeds 5] [--hands 2000] [--workers 14]

Part 1 (FM2) equilibria: CFR and CFR+ (100 000 it.) and external-sampling MCCFR (10^6 it.,
        seeds 0-2): NashConv, each seat's value, single-opponent damage and coalition value;
        cross-play of equilibrium components from different solvers.
Part 2 population: 9 agents (2 equilibria, 5 rule-based types, 2 adaptive), the full
        9x9x9 payoff tensor (exact for stationary triples, simulated otherwise), multi-population
        alpha-Rank over seats, a pairwise projection (Elo, Nash averaging, spinning top), VasE
        with each seating of three distinct agents as a voter, and per-agent coalition values.
Part 3 protocol: gain / speed / recovery vs sub-optimal opponent pairs, a fixed colluding pair
        (FM8), and a coalition teaching attack; exposure = coalition value of the policy in force.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import time
import zlib
from multiprocessing import Pool

import numpy as np

import deps
import trees
import solvers
import population as pop
import nplayer
from agents import HandRecord
from trees import pure_strategies
from logutil import Logger

G = "kuhn3"
_CTX = {}


class Ctx3:
    def __init__(self):
        tg = trees.load(G)
        self.tg = tg
        self.eq = {"CFR": solvers.cfr_profile(tg, 100000, algo="cfr"),
                   "CFR+": solvers.cfr_profile(tg, 100000, algo="cfrplus")}
        for s in range(3):
            self.eq[f"MCCFR-s{s}"] = solvers.mccfr_profile(tg, 1000000, s)
        self.blueprint = self.eq["CFR+"]
        self.types = nplayer.kuhn3_types(tg)
        self.profiles = {"Nash": self.eq["CFR+"], "Nash-CFR": self.eq["CFR"], **self.types}
        self.stationary = list(self.profiles)
        self.adaptive = ["DirBR3P", "Blend3P"]
        self.names = self.stationary + self.adaptive
        self.probe = nplayer.CoalitionProbe(tg)
        self._pure = {}

    def pure(self, p):
        if p not in self._pure:
            self._pure[p] = pure_strategies(self.tg, p)
        return self._pure[p]

    def agent(self, name):
        if name in self.profiles:
            return nplayer.Stationary3(name, self.profiles[name])
        if name == "DirBR3P":
            return nplayer.DirBR3P(name, self.blueprint, lam=1.0)
        if name == "Blend3P":
            return nplayer.DirBR3P(name, self.blueprint, lam=0.5)
        if name.startswith("SW:"):
            body, T = name[3:].split("@")
            a, b = body.split(">")
            return nplayer.Switching3(name, self.agent(a), self.agent(b), int(T))
        if name.startswith("COLLUDE:"):       # fixed pair: coalition BR vs the blueprint
            return None
        raise KeyError(name)


def ctx3():
    if "c" not in _CTX:
        _CTX["c"] = Ctx3()
    return _CTX["c"]


def coalition_pair(c, i, B_i):
    """Exact coalition best response (members j<k) against player i's fixed strategy."""
    tg = c.tg
    j, k = [q for q in range(3) if q != i]
    teacher = nplayer.CoalitionTeacher(tg, None, None, 0)
    teacher.pure_j = c.pure(j)

    class V:  # minimal victim stand-in
        seat = i
        def policy(self_inner):
            return B_i
    teacher.victim = V()
    teacher.plan(0)
    return teacher.pair


def play3(c, agents, tested, n, seed, coalition=None):
    """agents: list of 3 Agent objects (None in colluding seats when `coalition` is given)."""
    tg = c.tg
    rng = np.random.default_rng(zlib.crc32(f"{seed}|{[a.name if a else 'col' for a in agents]}|{tested}".encode()))
    drng = np.random.default_rng(20_000 + seed)
    decks = np.stack([drng.permutation(4) for _ in range(n)])
    for s, a in enumerate(agents):
        if a is not None:
            a.start(tg, s, np.random.default_rng(seed * 31 + s))
    ev = np.zeros((n, 3)); chips = np.zeros(n)
    cache, prof = {}, [None] * 3
    for t in range(n):
        for a in agents:
            if a is not None:
                a.begin_hand(t)
        if coalition is not None:
            coalition.step(t)
        for s in range(3):
            prof[s] = agents[s].policy() if agents[s] is not None else coalition.policy(s)
        key = tuple((a.version if a is not None else coalition.version) for a in agents)
        if key not in cache:
            cache = {key: tg.values(prof)}
        term, decisions, chances = tg.sample_hand(prof, rng, chance_seq=decks[t])
        ev[t] = cache[key]
        chips[t] = tg.term_util[term, tested]
        rec = HandRecord(t, term, chances, [a for _, a in decisions], None, decisions)
        for a in agents:
            if a is not None:
                a.observe(rec)
    return ev, chips


class FixedCoalition:
    """Colluding pair: bait profile until T, then the coalition best response against the
    victim's current policy, refreshed every R hands (T = 0 and R = inf: a fixed pair)."""

    def __init__(self, c, victim, bait, T, R):
        self.c, self.victim, self.bait, self.T, self.R = c, victim, bait, T, R
        self.pair, self.version = None, 0

    def step(self, t):
        if t >= self.T and (self.pair is None or (self.R and (t - self.T) % self.R == 0)):
            self.pair = coalition_pair(self.c, self.victim.seat, self.victim.policy())
            self.version += 1

    def policy(self, s):
        if self.pair is None:
            return self.bait[s]
        return self.pair[s]


# ---------------------------------------------------------------- jobs
def job_population(args):
    names, seed, n = args
    c = ctx3()
    agents = [c.agent(x) for x in names]
    ev, _ = play3(c, agents, 0, n, seed)
    return names, seed, ev.mean(axis=0)


def job_protocol(args):
    kind, agent_name, seat, opps, seed, n, T = args
    c = ctx3()
    tg = c.tg
    agent = c.agent(agent_name)
    others = [q for q in range(3) if q != seat]
    agents = [None] * 3
    agents[seat] = agent
    coalition = None
    if kind in ("indep", "switch"):
        for q, o in zip(others, opps):
            agents[q] = c.agent(o)
    elif kind == "collude":        # fixed colluding pair targeted at the blueprint in this seat
        coalition = FixedCoalition(c, _BlueprintStandIn(seat, c.blueprint[seat]), None, 0, 0)
    elif kind == "teach":          # bait with types until T, then coalition BR vs the agent
        bait = [None] * 3
        for q, o in zip(others, opps):
            bait[q] = c.profiles[o][q]
        coalition = FixedCoalition(c, agent, bait, T, 50)
    ev, chips = play3(c, agents, seat, n, seed, coalition)
    final = agent.policy()
    coal = c.probe.value(seat, final)
    return {"kind": kind, "agent": agent_name, "seat": seat, "opps": opps, "seed": seed,
            "ev": ev[:, seat].astype(np.float32), "chips": chips.astype(np.float32),
            "final_coalition_value": coal,
            "final_deviation_gain": None}


class _BlueprintStandIn:
    def __init__(self, seat, B):
        self.seat, self.B = seat, B

    def policy(self):
        return self.B


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--pop-seeds", type=int, default=3)
    ap.add_argument("--hands", type=int, default=2000)
    ap.add_argument("--workers", type=int, default=14)
    args = ap.parse_args()
    log = Logger("nplayer")
    t0 = time.time()
    c = ctx3()
    tg = c.tg
    out = {"game": "kuhn_poker(players=3)"}

    # ------------------------------------------------ Part 1: equilibria (FM2)
    eqs = {}
    for k, prof in c.eq.items():
        nc = tg.nash_conv(prof)
        eqs[k] = {"nash_conv": nc["nash_conv"], "values": nc["values"],
                  "coalition_value": [c.probe.value(i, prof[i]) for i in range(3)],
                  "single_damage": [[nplayer.single_damage(tg, i, prof, j) for j in range(3) if j != i]
                                    for i in range(3)]}
        log(f"P1 {k:9s} NashConv {nc['nash_conv']:.2e} values {np.round(nc['values'], 4).tolist()} "
            f"coalition {np.round(eqs[k]['coalition_value'], 4).tolist()}")
    keys = list(c.eq)
    cross = []
    for combo in itertools.product(keys, repeat=3):
        prof = [c.eq[combo[s]][s] for s in range(3)]
        nc = tg.nash_conv(prof)
        cross.append({"components": list(combo), "nash_conv": nc["nash_conv"], "values": nc["values"]})
    ncs = np.array([x["nash_conv"] for x in cross])
    out["part1"] = {"equilibria": eqs, "crossplay": cross,
                    "crossplay_nash_conv_max": float(ncs.max()),
                    "crossplay_value_range": [[float(min(x["values"][s] for x in cross)),
                                               float(max(x["values"][s] for x in cross))] for s in range(3)]}
    log(f"P1 cross-play of {len(keys)} equilibria: NashConv max {ncs.max():.2e}; value ranges "
        f"{np.round(out['part1']['crossplay_value_range'], 4).tolist()}")

    # ------------------------------------------------ Part 2: population tensor
    names = c.names
    n = len(names)
    Tn = np.zeros((3, n, n, n))
    for a, b, d in itertools.product(range(n), repeat=3):
        if all(names[x] in c.profiles for x in (a, b, d)):
            prof = [c.profiles[names[a]][0], c.profiles[names[b]][1], c.profiles[names[d]][2]]
            Tn[:, a, b, d] = tg.values(prof)
    jobs = [([names[a], names[b], names[d]], s, args.hands)
            for a, b, d in itertools.product(range(n), repeat=3)
            if not all(names[x] in c.profiles for x in (a, b, d)) for s in range(args.pop_seeds)]
    log(f"P2 tensor: {n}^3 triples, {len(jobs)} simulated matches")
    with Pool(args.workers) as pool:
        res = pool.map(job_population, jobs, chunksize=4)
    acc = {}
    for nm, s, v in res:
        acc.setdefault(tuple(nm), []).append(v)
    for nm, vs in acc.items():
        a, b, d = (names.index(x) for x in nm)
        Tn[:, a, b, d] = np.mean(vs, axis=0)
    # symmetric per-agent summary: payoff averaged over seats and opponent pairs
    popret = np.zeros(n)
    for i in range(n):
        vals = [Tn[0, i, b, d] for b in range(n) for d in range(n)] + \
               [Tn[1, a, i, d] for a in range(n) for d in range(n)] + \
               [Tn[2, a, b, i] for a in range(n) for b in range(n)]
        popret[i] = np.mean(vals)
    # pairwise projection: margin of i over j, third seat drawn from the population, all seatings
    Mp = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            m = []
            for k3 in range(n):
                for perm in itertools.permutations([i, j, k3]):
                    si, sj = perm.index(i), perm.index(j) if perm.count(j) == 1 else None
                    if sj is None or perm.count(i) != 1:
                        continue
                    m.append(Tn[si][perm] - Tn[sj][perm])
            Mp[i, j] = 0.5 * np.mean(m)
    Mp = 0.5 * (Mp - Mp.T)
    # VasE: each seating of three distinct agents votes a ranking by payoff
    margin = np.zeros((n, n))
    wins = np.zeros((n, n)); meets = np.zeros((n, n))
    for perm in itertools.permutations(range(n), 3):
        vals = [Tn[s][perm] for s in range(3)]
        for x in range(3):
            for y in range(3):
                if x == y:
                    continue
                meets[perm[x], perm[y]] += 1
                if vals[x] > vals[y] + 1e-12:
                    margin[perm[x], perm[y]] += 1
                    margin[perm[y], perm[x]] -= 1
                    wins[perm[x], perm[y]] += 1
                elif abs(vals[x] - vals[y]) <= 1e-12:
                    wins[perm[x], perm[y]] += 0.5
    Pw = np.where(meets > 0, wins / np.maximum(meets, 1), 0.5)
    np.fill_diagonal(Pw, 0.5)
    alphas = [0.1, 1.0, 10.0, 100.0]
    ar_multi = {}
    for al in alphas:
        pi = pop.alpharank_multipop([Tn[0], Tn[1], Tn[2]], al, 50).reshape(n, n, n)
        ar_multi[str(al)] = {"marginal_by_seat": [pi.sum(axis=(1, 2)).tolist(), pi.sum(axis=(0, 2)).tolist(),
                                                  pi.sum(axis=(0, 1)).tolist()],
                             "top_profile": [names[x] for x in np.unravel_index(pi.argmax(), pi.shape)],
                             "top_mass": float(pi.max())}
    p_star, skill = pop.nash_average(Mp)
    coal = {}
    for nm in c.stationary:
        coal[nm] = [c.probe.value(i, c.profiles[nm][i]) for i in range(3)]
    out["part2"] = {"agents": names, "tensor": Tn.tolist(), "population_return": popret.tolist(),
                    "pairwise_projection": Mp.tolist(), "transitive_ratio": pop.transitive_ratio(Mp),
                    "nash_avg_p": p_star.tolist(), "nash_avg_skill": skill.tolist(),
                    "elo_from_rankings": pop.elo_fit(Pw).tolist(), "pairwise_win_share": Pw.tolist(),
                    "vase_margin": margin.tolist(), "vase_iml_rank": pop.iml_rank(margin).tolist(),
                    "maximal_lottery": pop.maximal_lottery(margin).tolist(),
                    "alpharank_multipop": ar_multi, "coalition_value_stationary": coal}
    log(f"P2 population return: " + ", ".join(f"{names[i]} {popret[i]:+.3f}" for i in np.argsort(-popret)))
    log(f"P2 VasE IML ranks: " + ", ".join(f"{names[i]} {int(r)}" for i, r in enumerate(out['part2']['vase_iml_rank'])))
    for al in alphas:
        log(f"P2 alpha-Rank multipop alpha={al}: top profile {ar_multi[str(al)]['top_profile']} mass {ar_multi[str(al)]['top_mass']:.2f}")

    # ------------------------------------------------ Part 3: protocol
    T = args.hands // 2
    pairs = [("TightPassive", "LooseAggr"), ("AlwaysPass", "AlwaysBet"), ("Random", "Random"),
             ("LooseAggr", "LooseAggr"), ("TightPassive", "TightPassive")]
    tested = ["Nash", "DirBR3P", "Blend3P"]
    jobs = []
    for a in tested:
        for seat in range(3):
            for s in range(args.seeds):
                for op in pairs:
                    jobs.append(("indep", a, seat, op, s, args.hands, T))
                jobs.append(("switch", a, seat, (f"SW:TightPassive>LooseAggr@{T}", "LooseAggr"), s, args.hands, T))
                jobs.append(("collude", a, seat, None, s, args.hands, T))
                jobs.append(("teach", a, seat, ("TightPassive", "TightPassive"), s, args.hands, T))
    log(f"P3 protocol: {len(jobs)} matches")
    with Pool(args.workers) as pool:
        res = pool.map(job_protocol, jobs, chunksize=2)

    def refs(seat, opps):
        prof = [None] * 3
        prof[seat] = c.blueprint[seat]
        for q, o in zip([q for q in range(3) if q != seat], opps):
            prof[q] = c.profiles[o][q]
        return float(tg.values(prof)[seat]), float(tg.best_response(seat, prof))

    proto = {}
    for a in tested:
        R = [r for r in res if r["agent"] == a]
        gains, caps, h50s, coal_final = [], [], [], []
        for r in [x for x in R if x["kind"] == "indep"]:
            nash, br = refs(r["seat"], r["opps"])
            ev = r["ev"].astype(float)
            gains.append(float(np.mean(ev - nash)))
            coal_final.append(r["final_coalition_value"])
            att = br - nash
            if att >= 0.02:
                cap = (ev - nash) / att
                caps.append(float(np.mean(cap[-500:])))
                seg = cap
                cs = np.concatenate([[0], np.cumsum(seg)])
                m = (cs[100:] - cs[:-100]) / 100
                ok = np.where((seg[:len(m)] >= 0.5) & (m >= 0.5))[0]
                h50s.append(int(ok[0]) if len(ok) else np.nan)
        sw = [x for x in R if x["kind"] == "switch"]
        r50s, costs = [], []
        for r in sw:
            nashB, brB = refs(r["seat"], ("LooseAggr", "LooseAggr"))
            ev = r["ev"].astype(float)
            costs.append(float(np.mean(nashB - ev[T:T + 300])))
            cap = (ev - nashB) / (brB - nashB)
            seg = cap[T:]
            cs = np.concatenate([[0], np.cumsum(seg)])
            m = (cs[100:] - cs[:-100]) / 100
            ok = np.where((seg[:len(m)] >= 0.5) & (m >= 0.5))[0]
            r50s.append(int(ok[0]) if len(ok) else np.nan)
        col = [x for x in R if x["kind"] == "collude"]
        col_ev = [float(np.mean(x["ev"])) for x in col]
        col_last = [float(np.mean(x["ev"][-500:])) for x in col]
        te = [x for x in R if x["kind"] == "teach"]
        te_after = [float(np.mean(x["ev"][T:])) for x in te]
        te_before = [float(np.mean(x["ev"][:T])) for x in te]

        def sm(v):
            v = np.asarray([x for x in v if np.isfinite(x)], float)
            return {"mean": float(v.mean()) if len(v) else None,
                    "ci95": float(1.96 * v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else None,
                    "median": float(np.median(v)) if len(v) else None, "n": int(len(v))}
        proto[a] = {"gain": sm(gains), "final_capture": sm(caps), "h50": sm(h50s),
                    "h50_reached_share": float(np.mean(np.isfinite(h50s))) if h50s else None,
                    "switch_r50": sm(r50s), "switch_cost": sm(costs),
                    "colluders_mean_ev": sm(col_ev), "colluders_last500_ev": sm(col_last),
                    "teach_ev_before": sm(te_before), "teach_ev_after": sm(te_after),
                    "coalition_value_final_policy": sm(coal_final)}
        log(f"P3 {a:8s} gain {proto[a]['gain']['mean']:+.3f}±{proto[a]['gain']['ci95']:.3f} capture "
            f"{proto[a]['final_capture']['mean']:.2f} h50 med {proto[a]['h50']['median']} | switch r50 "
            f"{proto[a]['switch_r50']['median']} cost {proto[a]['switch_cost']['mean']:+.3f} | colluders "
            f"{proto[a]['colluders_mean_ev']['mean']:+.3f} (last500 {proto[a]['colluders_last500_ev']['mean']:+.3f}) | "
            f"teach before {proto[a]['teach_ev_before']['mean']:+.3f} after {proto[a]['teach_ev_after']['mean']:+.3f} | "
            f"coalition value of final policy {proto[a]['coalition_value_final_policy']['mean']:+.3f}")
    # curves (mean over seeds, seats) for figures
    curves = {}
    for kind in ("collude", "teach"):
        curves[kind] = {a: np.mean([x["ev"] for x in res if x["agent"] == a and x["kind"] == kind],
                                   axis=0)[::10].tolist() for a in tested}
    out["part3"] = {"tested": tested, "pairs": pairs, "switch_at": T, "protocol": proto, "curves": curves,
                    "seeds": args.seeds, "hands": args.hands}
    out["does_not_extend"] = [
        "exploitability as 'loss below the game value': no game value exists for N > 2",
        "NashConv = 0 is not a guarantee: equilibrium components lose to a coordinated pair",
        "Nash averaging / maximal lotteries need a two-player (or pairwise-projected) meta-game",
        "AIVAT: implemented here for two players only (the formalism allows more; not built)",
        "RNR / best equilibrium / adaptation safety: defined through the two-player minimax value",
    ]
    out["runtime_seconds"] = time.time() - t0
    with open(os.path.join(deps.RESULTS_DIR, "nplayer_kuhn3.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, default=float)
    log(f"done in {out['runtime_seconds']:.0f} s")


if __name__ == "__main__":
    main()
