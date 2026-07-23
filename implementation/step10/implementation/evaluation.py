"""
evaluation.py -- shared suite runners used by tournament.py and validate.py.

Everything is deterministic given a seed and returns plain JSON-serializable dicts. The neural
pieces (the PBT league, the self-play baseline) are gated behind torch availability and return a
`{"skipped": True, ...}` marker if torch is absent, so the numpy/exact path (replicator,
spinning-top, PSRO, CFR Nash) always runs.

Four suites (raw step 10 Deliverables L475-484, Validation L486-491):
  - replicator   : evolutionary dynamics on the four matrix games (vs analytic ESS).
  - spinning_top : transitive/cyclic ratio for RPS, a pure-skill game, and the PSRO-Leduc
                   meta-game.
  - league       : the PBT league -- exploitability trajectory + EGTA/diversity final report.
  - baselines    : league vs PSRO vs single self-play vs CFR Nash on Leduc (the comparison).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401  (step09 + step07 on sys.path)
from engines import make_game
from best_response import nash_gap
from nash import solve_nash_cached
from psro import PSRO

import evo_games
import replicator as rep
import spinning_top as st
import egta
import leduc_rl


# --- suite 1: replicator dynamics ---------------------------------------------------
def run_replicator_suite(config: dict) -> dict:
    rc = config["replicator"]
    rng = np.random.default_rng(config["seed"])
    out = {}
    for name in rc["games"]:
        g = evo_games.make_evo_game(name)
        starts = rc.get("starts", {}).get(name)
        if starts is None:
            starts = [rep._normalize(rng.random(g.n) + 0.1).tolist()]
        runs = []
        for x0 in starts:
            xs = rep.simulate_single(g.A, x0, T=rc["T"], dt=rc["dt"])
            final = xs[-1]
            runs.append({
                "x0": [round(v, 4) for v in x0],
                "final": [round(float(v), 4) for v in final],
                "converged": bool(rep.converged(xs)),
                "orbit_radius_vs_uniform": round(rep.orbit_radius(xs, np.ones(g.n) / g.n), 4),
            })
        # ESS check on the analytic Nash population(s)
        ess = [{"x": [round(v, 4) for v in xe], "is_ess": bool(rep.is_ess(g.A, xe))}
               for xe in g.nash_profiles]
        out[name] = {
            "ess_reference": g.ess_reference,
            "prediction": g.replicator_prediction,
            "runs": runs,
            "ess_checks": ess,
        }
    return out


# --- suite 2: spinning-top decomposition --------------------------------------------
def run_spinning_top_suite(config: dict) -> dict:
    sc = config["spinning_top"]
    out = {}
    # RPS -> ~100% cyclic; pure-skill -> ~100% transitive (the two anchors)
    rps = evo_games.make_evo_game("rock_paper_scissors").A
    out["rock_paper_scissors"] = {
        "transitive_ratio_hodge": round(st.transitive_ratio(rps, "hodge"), 5),
        "cyclic_ratio_hodge": round(st.cyclic_ratio(rps, "hodge"), 5),
        "transitive_ratio_svd_rawstep": round(st.transitive_ratio(rps, "svd"), 5),
    }
    skill = st.pure_skill_game(5)
    out["pure_skill"] = {
        "transitive_ratio_hodge": round(st.transitive_ratio(skill, "hodge"), 5),
        "cyclic_ratio_hodge": round(st.cyclic_ratio(skill, "hodge"), 5),
    }
    # PSRO-Leduc meta-game: how transitive is Leduc's population structure?
    rounds = sc.get("psro_leduc_rounds", 8)
    p = PSRO(make_game("leduc"), oracle="exact", seed=config["seed"])
    p.iterate(rounds=rounds)
    out["psro_leduc_metagame"] = {
        "rounds": rounds,
        "pop_size": [len(p.pop[0]), len(p.pop[1])],
        "transitive_ratio_hodge": round(st.transitive_ratio(p.U, "hodge"), 5),
        "cyclic_ratio_hodge": round(st.cyclic_ratio(p.U, "hodge"), 5),
    }
    return out


# --- suite 3: the PBT league --------------------------------------------------------
def run_league_suite(config: dict) -> dict:
    from ppo_agent import torch_available
    if not torch_available():
        return {"skipped": True, "reason": "PyTorch not installed; the PBT league needs torch. "
                                           "The exact suites (replicator/spinning-top/PSRO/CFR) "
                                           "still run."}
    from league import LeducLeague
    game = make_game("leduc")
    league = LeducLeague(game, config["league"])
    league.run()
    report = league.final_report()
    # spinning-top of the league meta-game (how much cycling did the exploiters induce?)
    M = np.asarray(report["egta"]["symmetric_payoff"], dtype=float)
    report["league_metagame_transitive_ratio"] = round(st.transitive_ratio(M, "hodge"), 5)
    report["trajectory"] = {
        "epoch": league.history["epoch"],
        "min_main_exploitability": league.history["min_main_exploitability"],
        "meta_nash_exploitability": league.history["meta_nash_exploitability"],
        "num_active": league.history["num_active"],
        "final_elo": league.history["elo"][-1] if league.history["elo"] else {},
    }
    return report


# --- self-play baseline (single agent, no population) --------------------------------
def run_selfplay_baseline(game, epochs: int, episodes: int, seed: int) -> dict:
    """One PPO agent trained against its OWN start-of-epoch snapshot (pure self-play, no
    exploiters, no population). The control the league is compared against."""
    from ppo_agent import PPOAgent
    agent = PPOAgent(seed=seed)
    rng = np.random.default_rng(seed)
    traj = []
    snap = None
    for e in range(epochs):
        snap = leduc_rl.extract_tabular_policy(game, agent.probs_fn())
        expl = float(nash_gap(game, snap, snap)["nash_conv"])
        traj.append(round(expl, 5))
        agent.train_against(game, [leduc_rl.make_net_policy(agent.probs_fn())], [1.0], episodes, rng)
    final = leduc_rl.extract_tabular_policy(game, agent.probs_fn())
    final_expl = float(nash_gap(game, final, final)["nash_conv"])
    return {"exploitability_trajectory": traj, "final_exploitability": round(final_expl, 5)}


# --- suite 4: baselines comparison --------------------------------------------------
def run_baselines_suite(config: dict) -> dict:
    from ppo_agent import torch_available
    bc = config["baselines"]
    game = make_game("leduc")
    out = {}

    # PSRO on Leduc (Step 09) -- population-based, exact oracle
    rounds = bc["psro_leduc_rounds"]
    psro = PSRO(game, oracle="exact", seed=config["seed"])
    hpsro = psro.iterate(rounds=rounds)
    out["psro"] = {"rounds": rounds, "final_exploitability": round(hpsro["exploitability"][-1], 5),
                   "trajectory": [round(v, 5) for v in hpsro["exploitability"]]}

    # CFR Nash (Step 07) -- the ~0-exploitability reference
    nash_pol, _ = solve_nash_cached(game, iters=bc["cfr_iters"])
    out["cfr_nash"] = {"iters": bc["cfr_iters"],
                       "exploitability": round(float(nash_gap(game, nash_pol, nash_pol)["nash_conv"]), 5)}

    # single self-play agent (torch)
    if torch_available():
        out["selfplay"] = run_selfplay_baseline(game, bc["selfplay_epochs"],
                                                bc["selfplay_episodes_per_epoch"], config["seed"])
    else:
        out["selfplay"] = {"skipped": True, "reason": "torch not installed"}

    return out
