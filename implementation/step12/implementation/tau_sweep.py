"""
tau_sweep.py  [CORE]  -- the empirical half of MATH FLAG B.

WHY THIS EXISTS
---------------
`ardt.py` defaults to a LOW expectile tau (pessimistic side) and flagged the raw step's
"tau=0.9 is pessimistic" as inverted. Reading the ARDT paper (arXiv:2407.18414) settled the
DEFINITION -- Eq. (6)/(7): alpha->0 is the min (pessimistic), alpha->1 is the max, and the paper
itself runs alpha = 0.01 (Algorithm 1, line 1).

This script settles the BEHAVIOUR on our data: does the low-tau (pessimistic) side actually buy
lower exploitability against Nash, as the theory says it should? We train ARDT at several taus on
the SAME mixed-opponent dataset, with a same-data vanilla DT as the paired baseline, over several
seeds, and report exploitability in chips (+ mbb/h).

Read it as: if the theory and our proxy agree, exploitability should be LOWEST at small tau and
degrade toward tau=0.9 (which conditions on the OPTIMISTIC / best-case return -- i.e. exactly the
"got lucky against a weak opponent" signal ARDT is meant to remove).

Usage (from this folder):
    python tau_sweep.py                     # default taus, 3 seeds, active profile
    python tau_sweep.py --seeds 5 --taus 0.01 0.1 0.5 0.9
Writes results/tau_sweep_<profile>.json.

NOTE: this file was added during the RUN session (unlike the rest of the folder, which was
authored unexecuted). Numbers it prints are MEASUREMENTS, not predictions.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import time

import deps  # noqa: F401
from deps import torch_available

# The paper's own alpha (Alg. 1 line 1) is 0.01; 0.1 is our authored default; 0.5 is the mean
# (no pessimism at all); 0.9 is the raw step's inverted "pessimistic" claim -- the control.
DEFAULT_TAUS = [0.01, 0.1, 0.5, 0.9]


def run_sweep(cfg: dict, taus: list, seeds: list, device: str = "cpu") -> dict:
    import torch  # noqa: F401
    from ardt import AdversariallyRobustDT, ARDTConfig
    from trajectory_dataset import PokerTrajectoryDataset, make_cfr_policy
    from decision_transformer import DecisionTransformer, DecisionTransformerConfig
    from train_dt import train_decision_transformer
    from strategy_extraction import extract_ardt_strategy, extract_dt_strategy, extract_policy_strategy
    from evaluation import exploitability_chips, chips_to_mbb_per_hand

    game_nash = None
    cells: dict = {tau: [] for tau in taus}
    dt_baseline: list = []
    nash_ref: list = []

    for seed in seeds:
        # One mixed-opponent dataset per seed, SHARED by every tau (paired comparison).
        ds = PokerTrajectoryDataset(
            game_name=cfg["game"], recipe="mixed_opponents",
            n_trajectories=cfg["n_trajectories"], cfr_iters=cfg["cfr_iters"],
            exploit_frac=cfg["exploit_frac"], seed=seed,
        )
        tensors = ds.to_tensors()
        game_nash = ds.game

        # Nash reference on the same seed (sanity anchor: should be ~0).
        nash_policy, _ = make_cfr_policy(ds.game, cfg["cfr_iters"], seed)
        nash_ref.append(exploitability_chips(extract_policy_strategy(nash_policy, ds.game)))

        # Paired vanilla-DT baseline on the SAME data.
        torch.manual_seed(seed)
        dt = DecisionTransformer(DecisionTransformerConfig(
            state_dim=ds.state_dim, act_dim=ds.num_actions, hidden_size=cfg["hidden_size"],
            n_layer=cfg["n_layer"], n_head=cfg["n_head"], max_ep_len=cfg["max_ep_len"]))
        train_decision_transformer(dt, tensors, epochs=cfg["dt_epochs"],
                                   batch_size=cfg["batch_size"], lr=cfg["lr"], device=device,
                                   log_every=10 ** 6)
        dt_expl = exploitability_chips(
            extract_dt_strategy(dt, ds.encoder, ds.game, cfg["dt_target_return"], device))
        dt_baseline.append(dt_expl)
        print(f"[seed {seed}] DT(mixed data) = {dt_expl:.4f} chips")

        for tau in taus:
            torch.manual_seed(seed)
            ardt = AdversariallyRobustDT(ds.state_dim, ds.num_actions, ARDTConfig(
                hidden_size=cfg["hidden_size"], n_layer=cfg["n_layer"], n_head=cfg["n_head"],
                max_ep_len=cfg["max_ep_len"], expectile_tau=tau))
            ardt.train(tensors, estimator_epochs=cfg["estimator_epochs"],
                       dt_epochs=cfg["dt_epochs"], batch_size=cfg["batch_size"], lr=cfg["lr"],
                       device=device)
            expl = exploitability_chips(extract_ardt_strategy(ardt, ds.encoder, ds.game, device))
            # What return is the estimator actually asking for? (Diagnoses tau's effect directly.)
            targets = [ardt.robust_target(ds.encoder.encode(ds.game, s, p), device)
                       for s, p in _probe_states(ds.game)]
            cells[tau].append({"exploitability_chips": expl,
                               "mean_robust_target": statistics.fmean(targets)})
            print(f"[seed {seed}] ARDT tau={tau:<5} = {expl:.4f} chips "
                  f"({chips_to_mbb_per_hand(expl):7.1f} mbb/h)  "
                  f"mean relabel target={statistics.fmean(targets):+.3f}")

    def _agg(vals):
        n = len(vals)
        mean = statistics.fmean(vals)
        sd = statistics.stdev(vals) if n > 1 else 0.0
        return {"mean": mean, "std": sd, "se": sd / (n ** 0.5) if n else 0.0, "n": n, "raw": vals}

    return {
        "taus": {str(t): {"exploitability": _agg([c["exploitability_chips"] for c in cells[t]]),
                          "robust_target": _agg([c["mean_robust_target"] for c in cells[t]])}
                 for t in taus},
        "dt_baseline": _agg(dt_baseline),
        "nash_reference": _agg(nash_ref),
        "seeds": seeds,
    }


def _probe_states(game):
    """The 12 Kuhn info sets as (state, player) pairs, for reading the relabel target."""
    from strategy_extraction import KUHN_INFO_SETS, _parse_info_set, _build_kuhn_state

    out = []
    for iset in KUHN_INFO_SETS:
        card, history, player = _parse_info_set(iset)
        out.append((_build_kuhn_state(card, history, player), player))
    return out


def print_table(res: dict) -> None:
    print()
    hdr = f"{'tau':>6}{'expl(chips)':>14}{'+/- se':>10}{'mbb/h':>10}{'relabel target':>16}"
    print(hdr)
    print("-" * len(hdr))
    for tau, cell in res["taus"].items():
        e, r = cell["exploitability"], cell["robust_target"]
        print(f"{tau:>6}{e['mean']:>14.4f}{e['se']:>10.4f}{e['mean'] * 1000:>10.1f}"
              f"{r['mean']:>+16.3f}")
    print("-" * len(hdr))
    print(f"{'DT':>6}{res['dt_baseline']['mean']:>14.4f}{res['dt_baseline']['se']:>10.4f}"
          f"{res['dt_baseline']['mean'] * 1000:>10.1f}{'(baseline)':>16}")
    print(f"{'Nash':>6}{res['nash_reference']['mean']:>14.4f}"
          f"{res['nash_reference']['se']:>10.4f}"
          f"{res['nash_reference']['mean'] * 1000:>10.1f}{'(anchor ~0)':>16}")


def main():
    from config import active_config

    ap = argparse.ArgumentParser(description="ARDT expectile-tau sweep (MATH FLAG B).")
    ap.add_argument("--taus", type=float, nargs="+", default=DEFAULT_TAUS)
    ap.add_argument("--seeds", type=int, default=3)
    args = ap.parse_args()

    if not torch_available():
        print("PyTorch unavailable; tau_sweep needs torch.")
        return

    import torch
    cfg = active_config()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    seeds = list(range(args.seeds))
    print(f"tau_sweep: profile={cfg['name']} device={device} taus={args.taus} seeds={seeds}")
    print("(paper alpha = 0.01, Alg.1 line 1; our authored default = 0.1; "
          "0.9 = the raw step's inverted claim, kept as the control)")
    print("=" * 78)

    t0 = time.time()
    res = run_sweep(cfg, args.taus, seeds, device=device)
    res["profile"] = cfg["name"]
    res["elapsed_sec"] = round(time.time() - t0, 1)
    res["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    print_table(res)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"tau_sweep_{cfg['name']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(f"\nsaved -> {path}  ({res['elapsed_sec']}s)")


if __name__ == "__main__":
    main()
