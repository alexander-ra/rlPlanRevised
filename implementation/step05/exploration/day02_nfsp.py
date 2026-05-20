"""
Day 2 exploration — NFSP on Kuhn + Leduc, and inspection of a Deep CFR
advantage / strategy network's predictions against tabular CFR ground truth.

Three sub-tasks from the Phase 2 brief:

  1. Train NFSP on Kuhn and on Leduc; track exploitability every 1k episodes.
  2. After training Deep CFR, feed in specific Leduc info states whose Nash
     strategy is known (computed here via OpenSpiel's tabular CFR+ to high
     precision) and compare network probabilities to the tabular table.
  3. Answer four conceptual questions about Deep CFR / NFSP / reservoir
     sampling / convergence. Answers live in findings.md.

Outputs:
  figures/day02_nfsp_kuhn.png       NFSP exploitability vs episodes on Kuhn
  figures/day02_nfsp_leduc.png      same, on Leduc
  figures/day02_advantage_probe.png bar plots: Deep CFR vs tabular at sampled info states
  logs/day02_results.json           raw curves + per-infoset probabilities
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from dataclasses import dataclass, field, asdict

# Make sibling `_openspiel_patch.py` importable when run as a script.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pyspiel
import torch

from open_spiel.python import policy as policy_lib
from open_spiel.python import rl_environment
from open_spiel.python.algorithms import cfr, exploitability
from open_spiel.python.pytorch import deep_cfr, nfsp

import _openspiel_patch  # noqa: F401 — monkey-patches Deep CFR advantage-net training


HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, "figures")
LOG_DIR = os.path.join(HERE, "logs")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# NFSP wrapper: joint policy that queries either the SL (avg) or RL head
# ---------------------------------------------------------------------------

class NFSPJointPolicy(policy_lib.Policy):
    """Wraps a list of NFSP agents into a Policy queryable by exploitability."""

    def __init__(self, game, agents, mode, num_players):
        super().__init__(game, list(range(num_players)))
        self._agents = agents
        self._mode = mode
        self._num_players = num_players
        self._obs = {
            "info_state": [None] * num_players,
            "legal_actions": [None] * num_players,
        }

    def action_probabilities(self, state, player_id=None):
        cur = state.current_player()
        legal = state.legal_actions(cur)
        self._obs["current_player"] = cur
        self._obs["info_state"][cur] = state.information_state_tensor(cur)
        self._obs["legal_actions"][cur] = legal
        ts = rl_environment.TimeStep(
            observations=self._obs, rewards=None, discounts=None, step_type=None,
        )
        with self._agents[cur].temp_mode_as(self._mode):
            probs = self._agents[cur].step(ts, is_evaluation=True).probs
        return {a: probs[a] for a in legal}


@dataclass
class NFSPRun:
    game_name: str
    episodes: int
    eval_every: int
    checkpoints: list = field(default_factory=list)   # episode count
    exploitabilities: list = field(default_factory=list)
    wall_times: list = field(default_factory=list)
    rl_losses: list = field(default_factory=list)
    sl_losses: list = field(default_factory=list)


def train_nfsp(
    game_name: str,
    episodes: int,
    eval_every: int,
    hidden_layers: tuple,
    anticipatory_param: float,
    seed: int,
) -> NFSPRun:
    print(f"\n[NFSP] {game_name}: episodes={episodes}, eval_every={eval_every}, "
          f"hidden={hidden_layers}, eta={anticipatory_param}")
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)

    env = rl_environment.Environment(game_name)
    info_state_size = env.observation_spec()["info_state"][0]
    num_actions = env.action_spec()["num_actions"]
    num_players = env.game.num_players()

    kwargs = dict(
        replay_buffer_capacity=int(2e5),
        reservoir_buffer_capacity=int(2e5),
        min_buffer_size_to_learn=1000,
        anticipatory_param=anticipatory_param,
        batch_size=128,
        learn_every=64,
        rl_learning_rate=0.01,
        sl_learning_rate=0.01,
        optimizer_str="sgd",
        loss_str="mse",
        update_target_network_every=19200,
        discount_factor=1.0,
        epsilon_decay_duration=max(1, episodes),
        epsilon_start=0.06,
        epsilon_end=0.001,
    )
    agents = [
        nfsp.NFSP(idx, info_state_size, num_actions, list(hidden_layers), **kwargs)
        for idx in range(num_players)
    ]
    joint = NFSPJointPolicy(env.game, agents, nfsp.MODE.AVERAGE_POLICY, num_players)

    run = NFSPRun(game_name=game_name, episodes=episodes, eval_every=eval_every)
    t0 = time.perf_counter()
    for ep in range(1, episodes + 1):
        ts = env.reset()
        while not ts.last():
            pid = ts.observations["current_player"]
            out = agents[pid].step(ts)
            ts = env.step([out.action])
        for ag in agents:
            ag.step(ts)

        if ep == 1 or ep % eval_every == 0 or ep == episodes:
            expl = exploitability.exploitability(env.game, joint)
            elapsed = time.perf_counter() - t0
            run.checkpoints.append(ep)
            run.exploitabilities.append(expl)
            run.wall_times.append(elapsed)
            run.rl_losses.append(
                [float(a.loss[0]) if a.loss[0] is not None else float("nan")
                 for a in agents]
            )
            run.sl_losses.append(
                [float(a.loss[1]) if a.loss[1] is not None else float("nan")
                 for a in agents]
            )
            print(f"  ep={ep:>7d} | expl={expl:.4f} | elapsed={elapsed:6.1f}s")
    return run


def plot_nfsp(run: NFSPRun, out_path: str):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(run.checkpoints, run.exploitabilities, marker="o", color="C2",
            label="NFSP (avg policy)")
    ax.set_xlabel("Episodes")
    ax.set_ylabel("Exploitability (log)")
    ax.set_yscale("log")
    ax.set_title(f"NFSP on {run.game_name}")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  saved {out_path}")


# ---------------------------------------------------------------------------
# Sub-task 2: probe Deep CFR's learned policy at sampled Leduc info states
# ---------------------------------------------------------------------------

def train_tabular_cfr_reference(
    game: pyspiel.Game, iterations: int
) -> policy_lib.TabularPolicy:
    """Tabular CFR+ run to near-convergence for ground-truth strategies."""
    print(f"\n[Tabular CFR+] reference on {game.get_type().short_name}, "
          f"iters={iterations}")
    solver = cfr.CFRPlusSolver(game)
    t0 = time.perf_counter()
    for i in range(1, iterations + 1):
        solver.evaluate_and_update_policy()
        if i % max(1, iterations // 5) == 0 or i == iterations:
            avg_policy = solver.average_policy()
            expl = exploitability.exploitability(game, avg_policy)
            print(f"  iter={i:>5d} | expl={expl:.5f} | "
                  f"elapsed={time.perf_counter()-t0:5.1f}s")
    return solver.average_policy()


def collect_info_states(game: pyspiel.Game, num: int, seed: int) -> list:
    """Walk random trajectories and snapshot info states (with their legal
    actions and current player). Deduplicates by information_state_string."""
    rng = random.Random(seed)
    seen = {}
    while len(seen) < num:
        state = game.new_initial_state()
        while not state.is_terminal():
            if state.is_chance_node():
                outcomes, probs = zip(*state.chance_outcomes())
                a = rng.choices(outcomes, weights=probs, k=1)[0]
                state.apply_action(a)
                continue
            pid = state.current_player()
            key = state.information_state_string(pid)
            if key not in seen:
                seen[key] = {
                    "info_state_string": key,
                    "player": pid,
                    "legal_actions": list(state.legal_actions(pid)),
                    "info_state_tensor": list(state.information_state_tensor(pid)),
                    "history": state.history_str(),
                }
            legal = state.legal_actions()
            a = rng.choice(legal)
            state.apply_action(a)
            if len(seen) >= num:
                break
    return list(seen.values())[:num]


def probe_policies(
    game: pyspiel.Game,
    deep_cfr_solver: deep_cfr.DeepCFRSolver,
    tabular_policy: policy_lib.TabularPolicy,
    samples: list,
) -> list:
    """For each sampled info state: query Deep CFR and tabular CFR, return
    side-by-side action probabilities plus a TV-distance summary."""
    rows = []
    for s in samples:
        # We need a real State object to pass through Deep CFR's API; cheapest
        # path is to play the recorded history back in a fresh state.
        state = game.new_initial_state()
        for tok in s["history"].split(", "):
            if not tok:
                continue
            state.apply_action(int(tok))

        dc_probs = deep_cfr_solver.action_probabilities(state)
        # tabular_policy returns the full action distribution as a numpy vector
        tab_probs_vec = tabular_policy.policy_for_key(s["info_state_string"])
        legal = s["legal_actions"]
        dc_vec = np.array([float(dc_probs.get(a, 0.0)) for a in legal])
        tab_vec = np.array([float(tab_probs_vec[a]) for a in legal])
        # Deep CFR's action_probabilities returns raw softmax outputs filtered
        # to legal actions, so they don't sum to 1 when some actions are
        # illegal. Renormalize for a fair comparison against the tabular policy
        # (which is already a distribution over legal actions).
        if dc_vec.sum() > 0:
            dc_vec = dc_vec / dc_vec.sum()
        if tab_vec.sum() > 0:
            tab_vec = tab_vec / tab_vec.sum()
        tv = 0.5 * float(np.abs(dc_vec - tab_vec).sum())
        rows.append({
            "info_state_string": s["info_state_string"],
            "player": s["player"],
            "legal_actions": legal,
            "deep_cfr": dc_vec.tolist(),
            "tabular_cfr_plus": tab_vec.tolist(),
            "tv_distance": tv,
        })
    return rows


def plot_probe(rows: list, out_path: str, max_panels: int = 8):
    rows_to_plot = rows[:max_panels]
    n = len(rows_to_plot)
    cols = 2
    plot_rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(plot_rows, cols, figsize=(11, 2.8 * plot_rows))
    axes = np.atleast_2d(axes).flatten()
    action_names = {0: "Fold", 1: "Call", 2: "Raise"}
    for i, row in enumerate(rows_to_plot):
        ax = axes[i]
        legal = row["legal_actions"]
        labels = [action_names.get(a, str(a)) for a in legal]
        x = np.arange(len(legal))
        w = 0.35
        ax.bar(x - w/2, row["deep_cfr"], w, color="C3", label="Deep CFR")
        ax.bar(x + w/2, row["tabular_cfr_plus"], w, color="C0", label="CFR+ (tabular)")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1)
        ax.set_title(f"{row['info_state_string']}\n  TV={row['tv_distance']:.3f}",
                     fontsize=8)
        if i == 0:
            ax.legend(fontsize=8)
    for j in range(len(rows_to_plot), len(axes)):
        axes[j].axis("off")
    fig.suptitle("Deep CFR vs tabular CFR+: action probabilities at sampled Leduc info states")
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  saved {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true",
                        help="Smoke-test (tiny iteration / episode counts).")
    parser.add_argument("--kuhn-episodes", type=int, default=20_000)
    parser.add_argument("--kuhn-eval-every", type=int, default=2_000)
    parser.add_argument("--leduc-episodes", type=int, default=50_000)
    parser.add_argument("--leduc-eval-every", type=int, default=5_000)
    parser.add_argument("--deep-cfr-iters", type=int, default=40)
    parser.add_argument("--deep-cfr-traversals", type=int, default=40)
    parser.add_argument("--tabular-cfr-iters", type=int, default=400)
    parser.add_argument("--probe-samples", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.quick:
        args.kuhn_episodes = 2_000
        args.kuhn_eval_every = 500
        args.leduc_episodes = 2_000
        args.leduc_eval_every = 500
        args.deep_cfr_iters = 4
        args.deep_cfr_traversals = 8
        args.tabular_cfr_iters = 50
        args.probe_samples = 4

    # ---- Sub-task 1: NFSP on Kuhn and Leduc ----
    kuhn_run = train_nfsp(
        game_name="kuhn_poker",
        episodes=args.kuhn_episodes,
        eval_every=args.kuhn_eval_every,
        hidden_layers=(64,),
        anticipatory_param=0.1,
        seed=args.seed,
    )
    plot_nfsp(kuhn_run, os.path.join(FIG_DIR, "day02_nfsp_kuhn.png"))

    leduc_run = train_nfsp(
        game_name="leduc_poker",
        episodes=args.leduc_episodes,
        eval_every=args.leduc_eval_every,
        hidden_layers=(128, 128),
        anticipatory_param=0.1,
        seed=args.seed,
    )
    plot_nfsp(leduc_run, os.path.join(FIG_DIR, "day02_nfsp_leduc.png"))

    # ---- Sub-task 2: Deep CFR vs tabular CFR+ on Leduc info states ----
    leduc = pyspiel.load_game("leduc_poker")
    print(f"\n[Deep CFR] training for probe: iters={args.deep_cfr_iters}, "
          f"traversals={args.deep_cfr_traversals}")
    torch.manual_seed(args.seed)
    dc_solver = deep_cfr.DeepCFRSolver(
        leduc,
        policy_network_layers=(64, 64),
        advantage_network_layers=(64, 64),
        num_iterations=args.deep_cfr_iters,
        num_traversals=args.deep_cfr_traversals,
        learning_rate=1e-3,
        batch_size_advantage=128,
        batch_size_strategy=1024,
        memory_capacity=int(1e6),
        seed=args.seed,
    )
    t0 = time.perf_counter()
    _, adv_losses, policy_loss = dc_solver.solve()
    policy_loss_f = float(policy_loss) if policy_loss is not None else float("nan")
    print(f"  Deep CFR trained in {time.perf_counter()-t0:.1f}s. "
          f"policy_loss={policy_loss_f:.4f}")
    dc_avg_policy = policy_lib.tabular_policy_from_callable(
        leduc, dc_solver.action_probabilities
    )
    dc_expl = exploitability.exploitability(leduc, dc_avg_policy)
    print(f"  Deep CFR exploitability = {dc_expl:.4f}")

    tabular_policy = train_tabular_cfr_reference(leduc, args.tabular_cfr_iters)

    samples = collect_info_states(leduc, args.probe_samples, args.seed)
    probe_rows = probe_policies(leduc, dc_solver, tabular_policy, samples)
    plot_probe(probe_rows, os.path.join(FIG_DIR, "day02_advantage_probe.png"))

    print("\n[probe summary]")
    for r in probe_rows:
        print(f"  {r['info_state_string']}  TV={r['tv_distance']:.3f}  "
              f"DC={r['deep_cfr']}  CFR+={r['tabular_cfr_plus']}")

    # ---- Persist ----
    out = {
        "args": vars(args),
        "nfsp_kuhn": asdict(kuhn_run),
        "nfsp_leduc": asdict(leduc_run),
        "deep_cfr_probe": {
            "exploitability": dc_expl,
            "policy_loss": policy_loss_f,
            "rows": probe_rows,
        },
    }
    def _json_default(o):
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(f"not JSON serializable: {type(o)}")

    out_path = os.path.join(LOG_DIR, "day02_results.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=_json_default)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
