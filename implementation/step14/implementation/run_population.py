"""
run_population.py -- E1: round-robin over the bot zoo + Layer-2 rankings + failure modes 4 and 9.

    python run_population.py [--games kuhn leduc] [--seeds 5] [--hands 2000] [--workers 14]

For every ordered pair of zoo agents, the payoff per hand averaged over both seats:
  * stationary x stationary : exact (tree evaluation), no sampling
  * any pair with an adaptive agent : simulated, K = 2000 hands per match, both seats with
    duplicate cards, `seeds` independent matches; the entry is the mean policy-exact EV of
    the hands played (the chips and AIVAT means are stored alongside)
Horizon dependence: the first H hands of a K-hand match ARE an H-hand match (agents do not
know K), so matrices for H in {100, 300, 1000, 2000} come from the same runs.

Outputs results/population_<game>.json with the matrices, per-seed matrices, per-agent
exploitability / exposure, and the analysis (Elo, Nash averaging, meta-Nash, alpha-Rank sweep,
VasE maximal lotteries, spinning top, RRPS-style aggregate score, clone test, bootstrap rank
stability).
"""

from __future__ import annotations

import argparse
import json
import os
import time
from multiprocessing import Pool

import numpy as np

import deps
import zoo
import tasks
import population as pop
from logutil import Logger

HORIZONS = [100, 300, 1000, 2000]
ALPHAS = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]
SESSION = 100      # hands per "game" for win/loss-based ratings (Elo, VasE)
CLONE = {"kuhn": "AlwaysPass", "leduc": "CallingStation"}


def exact_block(ctx):
    names = ctx.stationary_names
    n = len(names)
    tg = ctx.tg
    M = np.zeros((n, n)); SD = np.zeros((n, n))
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            ms, vs = [], []
            for s in (0, 1):
                prof = [None, None]
                prof[s] = ctx.profiles[a][s]
                prof[1 - s] = ctx.profiles[b][1 - s]
                P = tg.terminal_probs(prof)
                u = tg.term_util[:, s]
                m = float(P @ u)
                ms.append(m); vs.append(float(P @ (u - m) ** 2))
            M[i, j] = 0.5 * (ms[0] + ms[1])
            SD[i, j] = np.sqrt(0.5 * (vs[0] + vs[1]) + 0.25 * (ms[0] - ms[1]) ** 2)
    expl = {a: tg.nash_conv(ctx.profiles[a])["exploitability"] for a in names}
    return M, SD, expl


def analyze(M, SD, names, expl, session=SESSION):
    n = len(names)
    P = pop.session_win_prob(M, SD, session)
    margin = P - P.T
    elo = pop.elo_fit(P)
    p_star, skill = pop.nash_average(M)
    meta = pop.meta_nash(M)
    ar = {str(a): pop.alpharank(M, a, 50).tolist() for a in ALPHAS}
    ml = pop.maximal_lottery(margin)
    iml = pop.iml_rank(margin)
    pop_ret = np.array([np.mean([M[i, j] for j in range(n) if j != i]) for i in range(n)])
    wpe = np.array([max(-M[i, j] for j in range(n) if j != i) for i in range(n)])
    ex = np.array([expl[a] for a in names])
    out = {
        "win_prob_session": P.tolist(),
        "elo": elo.tolist(),
        "nash_avg_p": p_star.tolist(), "nash_avg_skill": skill.tolist(),
        "meta_nash": meta.tolist(),
        "alpharank": ar,
        "maximal_lottery": ml.tolist(), "iml_rank": iml.tolist(),
        "population_return": pop_ret.tolist(),
        "within_pop_exploitability": wpe.tolist(),
        "rrps_aggregate": (pop_ret - wpe).tolist(),
        "exploitability": ex.tolist(),
        "transitive_ratio": pop.transitive_ratio(M),
    }
    ranks = {"elo": pop.ranks_from_scores(elo), "population_return": pop.ranks_from_scores(pop_ret),
             "nash_avg": pop.ranks_from_scores(skill + 1e-9 * p_star),
             "alpharank_a1": pop.ranks_from_scores(np.array(ar["1.0"])),
             "alpharank_a10": pop.ranks_from_scores(np.array(ar["10.0"])),
             "alpharank_a100": pop.ranks_from_scores(np.array(ar["100.0"])),
             "vase_iml": iml.astype(int),
             "exploitability": pop.ranks_from_scores(-ex),
             "rrps_aggregate": pop.ranks_from_scores(pop_ret - wpe)}
    out["ranks"] = {k: np.asarray(v).tolist() for k, v in ranks.items()}
    keys = list(ranks)
    out["kendall_tau"] = {f"{a}|{b}": pop.tau(ranks[a], ranks[b]) for i, a in enumerate(keys)
                          for b in keys[i + 1:]}
    return out


def clone_test(M, SD, names, clone, kmax=8):
    """Add k copies of `clone`; report Elo, Nash-averaged skill, maximal-lottery mass and
    alpha-Rank (alpha = 10) for the ORIGINAL agents."""
    c = names.index(clone)
    n = len(names)
    rows = []
    for k in range(kmax + 1):
        idx = list(range(n)) + [c] * k
        Mk = M[np.ix_(idx, idx)]; SDk = SD[np.ix_(idx, idx)]
        Pk = pop.session_win_prob(Mk, SDk, SESSION)
        elo = pop.elo_fit(Pk)[:n]
        p, skill = pop.nash_average(Mk)
        ml = pop.maximal_lottery(Pk - Pk.T)
        ar = pop.alpharank(Mk, 10.0, 50)
        # fold the copies' mass back onto the cloned agent for comparability
        ml_f = ml[:n].copy(); ml_f[c] += ml[n:].sum()
        ar_f = ar[:n].copy(); ar_f[c] += ar[n:].sum()
        rows.append({"k": k, "elo": elo.tolist(), "nash_avg_skill": skill[:n].tolist(),
                     "maximal_lottery": ml_f.tolist(), "alpharank_a10": ar_f.tolist(),
                     "population_return": [float(np.mean(np.delete(Mk[i], i))) for i in range(n)]})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="+", default=["kuhn", "leduc"])
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--hands", type=int, default=2000)
    ap.add_argument("--workers", type=int, default=14)
    args = ap.parse_args()
    log = Logger("population")
    for game in args.games:
        t0 = time.time()
        ctx = zoo.context(game)
        names = ctx.names
        n = len(names)
        Mst, SDst, expl = exact_block(ctx)
        ns = len(ctx.stationary_names)
        log(f"[{game}] {n} agents ({ns} stationary, exact block done); seeds {args.seeds}, "
            f"K={args.hands}")
        # simulated pairs: the adaptive agent is always the one under test
        jobs, pairs = [], []
        for i in range(n):
            for j in range(i + 1, n):
                a, b = names[i], names[j]
                if not (ctx.is_adaptive(a) or ctx.is_adaptive(b)):
                    continue
                tested, other, sign = (a, b, 1) if ctx.is_adaptive(a) else (b, a, -1)
                pairs.append((i, j, tested, other, sign))
                for s in range(args.seeds):
                    for seat in (0, 1):
                        jobs.append((game, tested, other, s, seat, args.hands))
        log(f"[{game}] {len(pairs)} simulated pairs, {len(jobs)} matches")
        with Pool(args.workers) as pool:
            res = pool.map(tasks.run, jobs, chunksize=2)
        by = {}
        for r in res:
            g, a, o, s, seat, _ = r["meta"]
            by[(a, o, s, seat)] = r
        H = HORIZONS
        Ms = {h: np.zeros((args.seeds, n, n)) for h in H}
        Mchips = {h: np.zeros((n, n)) for h in H}
        Maiv = {h: np.zeros((n, n)) for h in H}
        SD = np.zeros((n, n))
        expo_adapt = {a: [] for a in ctx.adaptive_names}
        for h in H:
            Ms[h][:, :ns, :ns] = Mst[None]
            Mchips[h][:ns, :ns] = Mst
            Maiv[h][:ns, :ns] = Mst
        SD[:ns, :ns] = SDst
        for (i, j, tested, other, sign) in pairs:
            chips_all = []
            for h in H:
                for s in range(args.seeds):
                    ev = np.mean([by[(tested, other, s, seat)]["ev"][:h].mean() for seat in (0, 1)])
                    Ms[h][s, i, j] = sign * ev
                    Ms[h][s, j, i] = -sign * ev
                ch = np.mean([by[(tested, other, s, seat)]["chips"][:h].mean()
                              for s in range(args.seeds) for seat in (0, 1)])
                av = np.mean([by[(tested, other, s, seat)]["aivat"][:h].mean()
                              for s in range(args.seeds) for seat in (0, 1)])
                Mchips[h][i, j], Mchips[h][j, i] = sign * ch, -sign * ch
                Maiv[h][i, j], Maiv[h][j, i] = sign * av, -sign * av
            for s in range(args.seeds):
                for seat in (0, 1):
                    r = by[(tested, other, s, seat)]
                    chips_all.append(r["chips"])
                    expo_adapt[tested].append(float(np.mean(r["expo"])))
            SD[i, j] = SD[j, i] = float(np.concatenate(chips_all).std())
        for a in ctx.adaptive_names:
            expl[a] = float(np.mean(expo_adapt[a]))
        out = {"game": game, "agents": names, "adaptive": ctx.adaptive_names,
               "seeds": args.seeds, "hands": args.hands, "horizons": H, "session": SESSION,
               "v_star": list(ctx.v_star), "exploitability": expl,
               "exploitability_note": "stationary: exact exploitability = NashConv/2 of the agent's "
                                      "self-play profile; adaptive: time-averaged seat exposure "
                                      "(v*_seat - worst case of the played policy) over its matches",
               "SD": SD.tolist(), "matrices": {}, "analysis": {}}
        for h in H:
            M = Ms[h].mean(axis=0)
            out["matrices"][str(h)] = {"ev": M.tolist(), "per_seed_ev": Ms[h].tolist(),
                                       "chips": Mchips[h].tolist(), "aivat": Maiv[h].tolist()}
            out["analysis"][str(h)] = analyze(M, SD, names, expl)
        # bootstrap rank stability over seeds (Rowland et al. 2019: ranking confidence)
        rng = np.random.default_rng(0)
        Mh = Ms[H[-1]]
        boot = {"elo": [], "nash_avg": [], "alpharank_a10": [], "vase_iml": [], "population_return": []}
        for _ in range(200):
            pick = rng.integers(0, args.seeds, args.seeds)
            M = Mh[pick].mean(axis=0)
            an = analyze(M, SD, names, expl)
            for k in boot:
                boot[k].append(an["ranks"][k])
        out["bootstrap_ranks"] = {k: np.asarray(v).tolist() for k, v in boot.items()}
        out["clone_test"] = {"clone": CLONE[game],
                             "rows": clone_test(Ms[H[-1]].mean(axis=0), SD, names, CLONE[game])}
        out["runtime_seconds"] = time.time() - t0
        path = os.path.join(deps.RESULTS_DIR, f"population_{game}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1, default=float)
        a = out["analysis"][str(H[-1])]
        order = np.argsort(a["ranks"]["elo"])
        log(f"[{game}] done in {out['runtime_seconds']:.0f} s -> {path}")
        log(f"[{game}] transitive ratio {a['transitive_ratio']:.3f}; Elo order: "
            + ", ".join(f"{names[k]} {a['elo'][k]:.0f}" for k in order))
        log(f"[{game}] Nash-avg support: " + ", ".join(
            f"{names[k]} {a['nash_avg_p'][k]:.2f}" for k in range(n) if a['nash_avg_p'][k] > 1e-4))
        log(f"[{game}] Kendall tau: " + ", ".join(f"{k} {v:+.2f}" for k, v in a["kendall_tau"].items()
                                                  if k.startswith("elo|") or k.startswith("exploitability|")))


if __name__ == "__main__":
    main()
