"""
evaluation.py -- shared metric + experiment helpers used by tournament.py and validate.py.

Everything here is deterministic given a seed and returns plain JSON-serializable dicts. The
heavy neural pieces (coop CTDE / communication) are gated behind torch availability and return
a `{"skipped": True, ...}` marker if torch is absent, so the numpy-only path (matrix games,
PSRO, LOLA) always runs.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401  (puts step07/implementation on sys.path)
from engines import make_game

from matrix_games import make_matrix_game, classify_outcome, ALL_GAMES
from goofspiel import Goofspiel
from coop_env import CoopSignalEnv, ClimbingGame
import psro as psro_mod
import lola as lola_mod


# --- matrix games: independent softmax policy-gradient (exact gradients) --------------
def independent_learn_matrix(game, steps: int = 4000, lr: float = 0.1, seed: int = 0,
                             init_noise: float = 0.3):
    """Two independent softmax learners on a general n-action matrix game, using EXACT
    gradients (no sampling noise) so the convergence/cycling picture is unambiguous.

    Returns (x, y, history) where x, y are the final action distributions.
    """
    rng = np.random.default_rng(seed)
    n0, n1 = game.n_actions
    th0 = init_noise * rng.standard_normal(n0)
    th1 = init_noise * rng.standard_normal(n1)
    A, B = game.A, game.B
    hist = {"step": [], "x": [], "y": []}

    def softmax(z):
        z = z - z.max()
        e = np.exp(z)
        return e / e.sum()

    for t in range(steps + 1):
        x = softmax(th0)
        y = softmax(th1)
        if t % max(1, steps // 50) == 0:
            hist["step"].append(t)
            hist["x"].append(x.tolist())
            hist["y"].append(y.tolist())
        if t == steps:
            break
        # dV0/dtheta0 = (diag(x) - x x^T) (A y);  dV1/dtheta1 = (diag(y) - y y^T) (B^T x)
        gx = (np.diag(x) - np.outer(x, x)) @ (A @ y)
        gy = (np.diag(y) - np.outer(y, y)) @ (B.T @ x)
        th0 = th0 + lr * gx
        th1 = th1 + lr * gy
    return x, y, hist


def run_matrix_suite(config: dict) -> dict:
    games = config.get("matrix_games", list(ALL_GAMES))
    ml = config.get("matrix_learn", {"steps": 4000, "lr": 0.1, "seeds": [0, 1, 2]})
    out = {}
    for name in games:
        game = make_matrix_game(name)
        per_seed = []
        for seed in ml["seeds"]:
            x, y, _ = independent_learn_matrix(game, ml["steps"], ml["lr"], seed)
            per_seed.append({
                "seed": seed,
                "x": [round(v, 4) for v in x.tolist()],
                "y": [round(v, 4) for v in y.tolist()],
                "nashconv": round(float(game.nashconv(x, y)), 5),
                "classification": classify_outcome(game, x, y),
            })
        out[name] = {
            "zero_sum": bool(game.zero_sum),
            "nash_reference": game.nash_reference,
            "runs": per_seed,
        }
    return out


# --- PSRO across game families -------------------------------------------------------
def run_psro_suite(config: dict) -> dict:
    p = config["psro"]
    out = {}

    # extensive-form: Kuhn (converges to ~0) and Leduc (< 0.5 within 20 iters)
    kuhn = psro_mod.PSRO(make_game("kuhn"), oracle=p.get("oracle", "exact"), seed=config["seed"])
    out["kuhn"] = kuhn.iterate(rounds=p["kuhn_rounds"])
    if p.get("leduc_rounds", 0) > 0:
        leduc = psro_mod.PSRO(make_game("leduc"), oracle=p.get("oracle", "exact"),
                              seed=config["seed"])
        out["leduc"] = leduc.iterate(rounds=p["leduc_rounds"])

    # matrix meta-game (population = pure actions)
    mg = make_matrix_game(p.get("matrix_game", "matching_pennies"))
    out["matrix"] = {"game": mg.name, **psro_mod.psro_matrix(mg, rounds=p["matrix_rounds"],
                                                             seed=config["seed"])}

    # native Goofspiel
    goof = Goofspiel(num_cards=p.get("goofspiel_cards", 3))
    out["goofspiel"] = {"num_cards": goof.num_cards,
                        **psro_mod.psro_goofspiel(goof, rounds=p["goofspiel_rounds"],
                                                  seed=config["seed"])}
    return out


# --- cooperative CTDE / communication (torch) ---------------------------------------
class _StatelessCoopEnv:
    """Adapter that presents a stateless cooperative matrix game (e.g. ClimbingGame) through
    the reset()/step() + shape API the neural learners expect. Single dummy observation, so
    the only thing that matters is the joint action -- exactly the IL-vs-CTDE contrast."""

    n_agents = 2

    def __init__(self, matrix_game):
        self._g = matrix_game
        self.n_actions = matrix_game.n_actions

    obs_dim = 1
    global_state_dim = 1

    def reset(self):
        obs = [np.ones(1, dtype=np.float32), np.ones(1, dtype=np.float32)]
        return obs, np.ones(1, dtype=np.float32)

    def step(self, actions):
        return self._g.step(actions)


def run_coop_suite(config: dict) -> dict:
    from learners import torch_available
    if not torch_available():
        return {"skipped": True, "reason": "PyTorch not installed; neural CTDE/comm experiments "
                                           "require torch. numpy-only checks (matrix/PSRO/LOLA) "
                                           "still run."}
    from learners import IndependentLearners
    from maddpg import MADDPG
    from mappo import MAPPO
    import commnet as commnet_mod

    c = config["coop"]
    seed = c.get("seeds", [0])[0]
    ep = c["episodes"]
    be = c["batch_episodes"]
    K = c["n_targets"]

    # (1) critic-variance comparison on CoopSignal (central critic sees the target + joint acts)
    signal_env = CoopSignalEnv(n_targets=K, comm=False, seed=seed)
    md = MADDPG(signal_env, {"seed": seed})
    md_hist = md.train(episodes=ep, batch_episodes=be, seed=seed)
    critic_cmp = md.critic_variance_comparison(md_hist)

    # (2) IL vs MADDPG reward on the Climbing game (relative overgeneralization -> IL stuck)
    climb_env_il = _StatelessCoopEnv(ClimbingGame())
    il = IndependentLearners(climb_env_il, {"seed": seed})
    il.train(episodes=ep, batch_episodes=be, seed=seed)
    il_reward = il.greedy_reward(episodes=1)      # deterministic (stateless)
    climb_env_md = _StatelessCoopEnv(ClimbingGame())
    md_climb = MADDPG(climb_env_md, {"seed": seed})
    md_climb.train(episodes=ep, batch_episodes=be, seed=seed)
    md_climb_reward = md_climb.greedy_reward(episodes=1)

    # (3) MAPPO reward on the Climbing game (centralized value)
    climb_env_mp = _StatelessCoopEnv(ClimbingGame())
    mp = MAPPO(climb_env_mp, {"seed": seed})
    mp.train(episodes=ep, batch_episodes=be, seed=seed)
    mp_reward = mp.greedy_reward(episodes=1)

    # (4) communication: CommNet with the channel ON vs OFF on CoopSignal
    comm_res = commnet_mod.compare(lambda: CoopSignalEnv(n_targets=K, comm=True, seed=seed),
                                   episodes=ep, batch_episodes=be, seed=seed)

    return {
        "critic_variance": critic_cmp,
        "climbing_reward": {
            "independent": round(il_reward, 3),
            "maddpg": round(md_climb_reward, 3),
            "mappo": round(mp_reward, 3),
            "optimum": 11.0, "safe": 5.0,
        },
        "communication": {
            "comm_on_reward": round(comm_res["comm_on_reward"], 3),
            "comm_off_reward": round(comm_res["comm_off_reward"], 3),
            "no_comm_ceiling": round(1.0 / K, 3),
            "comm_helps": comm_res["comm_helps"],
        },
    }


# --- LOLA on the IPD -----------------------------------------------------------------
def run_lola(config: dict) -> dict:
    lcfg = config.get("lola", {})
    return lola_mod.validate_cooperation(lcfg)
