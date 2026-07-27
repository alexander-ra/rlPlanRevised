"""
leduc_stage0.py  [CORE]  -- does the Kuhn return-conditioning finding survive a richer game?

THE QUESTION THIS EXISTS TO ANSWER
----------------------------------
The headline Kuhn result was that return conditioning does NOT steer a Decision Transformer:
exploitability was flat (~0.68 chips) across target returns, with a sharp collapse at exactly
R = -1 where the DT passed at 11 of 12 info sets. The proposed mechanism was that in Kuhn the
return's MAGNITUDE encodes which betting line was played (|R|=2 <=> someone bet and was called,
|R|=1 <=> a fold or check-check) while its SIGN is pure card luck -- so conditioning selects the
shape of the hand, not the quality of play, and R=-1 (the modal, fold payoff) selects "the folding
line".

That explanation leans hard on Kuhn having only FOUR payoff values. Leduc has FIFTEEN
({-13,-11,...,+13}, measured), so the magnitude<->line coupling is far weaker. If the notch is a
Kuhn artefact it should vanish here; if the mechanism is general it should reappear at Leduc's
modal payoff. Either answer is informative, which is why this is the cheapest useful Leduc test.

SCOPE (deliberately narrow -- "Stage 0")
----------------------------------------
Encoder + dataset + DT training + a return-conditioning sweep, scored by ACTUAL PERFORMANCE
(chips/hand vs a near-Nash opponent). Explicitly NOT here: exact exploitability (that lives in
step03, whose `cfr` package collides with step02's -- see deps.py), LLM rows, ARDT, or the
comparison table. Those are Stage 1+.

TWO THINGS THIS ALSO EXERCISES (both flagged as Leduc risks earlier)
- `PokerStateEncoder` on two streets + a board card (state_dim 35 vs Kuhn's 17).
- LEGAL-ACTION MASKING: Leduc states have 2 OR 3 legal actions, and `DecisionTransformer.
  action_probs` softmaxes over all `act_dim` with no mask. In Kuhn both actions were always legal
  so this never mattered; here, unmasked sampling would emit illegal actions. We mask and
  renormalise, and report how much probability mass the model put on illegal actions -- a
  diagnostic that does not exist in the Kuhn path.

Usage:  python leduc_stage0.py [--trajectories 20000] [--hands 2000]
Writes results/leduc_stage0.json

NOTE: added during the RUN session. All numbers are MEASUREMENTS.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random
import time

import numpy as np

import deps  # noqa: F401
from deps import torch_available
from engines import make_game
from policies import sample_action

from trajectory_dataset import PokerTrajectoryDataset, make_cfr_policy


def dt_action_dist(model, torch, encoder, game, state, player, target_return, tstep,
                   hist_states, hist_actions, device, max_ep_len):
    """DT action distribution at `state`, using this hand's own (R,s,a) prefix, MASKED to legal."""
    vec = encoder.encode(game, state, player)
    s_seq = hist_states + [vec]
    a_seq = hist_actions + [0]                      # placeholder for the action being predicted
    T = len(s_seq)
    states = torch.as_tensor(np.array(s_seq), dtype=torch.float32, device=device).view(1, T, -1)
    actions = torch.as_tensor(a_seq, dtype=torch.long, device=device).view(1, T)
    rtg = torch.full((1, T, 1), float(target_return), dtype=torch.float32, device=device)
    # Reward is terminal-only in poker, so return-to-go is constant within a hand -- matching how
    # the dataset was built.
    ts = torch.as_tensor([min(i, max_ep_len - 1) for i in range(tstep - T + 1, tstep + 1)],
                         dtype=torch.long, device=device).view(1, T).clamp(min=0)
    mask = torch.ones((1, T), dtype=torch.float32, device=device)
    probs = model.action_probs(states, actions, rtg, ts, mask)[0].tolist()

    legal = list(game.legal_actions(state))
    illegal_mass = sum(p for a, p in enumerate(probs) if a not in legal)
    tot = sum(probs[a] for a in legal)
    if tot <= 0:
        dist = {a: 1.0 / len(legal) for a in legal}
    else:
        dist = {a: probs[a] / tot for a in legal}
    return dist, illegal_mass


def play_dt(model, torch, encoder, game, opp_policy, target_return, n_hands, device,
            max_ep_len, seed=0):
    """Mean chips/hand for the DT vs `opp_policy`, seats alternated. Returns (mean, se, diag)."""
    rng = random.Random(seed)
    deals = game.deals()
    utils, illegal_masses = [], []
    for h in range(n_hands):
        dt_seat = h % 2
        state = game.root(rng.choice(deals))
        tcount = {0: 0, 1: 0}
        hist_s, hist_a = [], []
        while not game.is_terminal(state):
            p = game.current_player(state)
            if p == dt_seat:
                dist, im = dt_action_dist(model, torch, encoder, game, state, p, target_return,
                                          tcount[p], hist_s, hist_a, device, max_ep_len)
                illegal_masses.append(im)
                a = sample_action(dist, rng)
                hist_s.append(encoder.encode(game, state, p))
                hist_a.append(a)
            else:
                a = sample_action(opp_policy(game, state), rng)
            tcount[p] += 1
            state = game.apply(state, a)
        utils.append(game.utility(state, dt_seat))
    arr = np.array(utils, dtype=np.float64)
    return (float(arr.mean()), float(arr.std() / max(1, len(arr)) ** 0.5),
            {"mean_illegal_mass": float(np.mean(illegal_masses)) if illegal_masses else 0.0})


def main():
    ap = argparse.ArgumentParser(description="Stage 0: Leduc DT return-conditioning sweep.")
    ap.add_argument("--trajectories", type=int, default=20000)
    ap.add_argument("--cfr-iters", type=int, default=8000)
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--hands", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    if not torch_available():
        print("PyTorch unavailable; Stage 0 needs torch.")
        return
    import torch
    from decision_transformer import DecisionTransformer, DecisionTransformerConfig
    from train_dt import train_decision_transformer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    max_ep_len = 8
    print(f"Leduc Stage 0: trajectories={args.trajectories} cfr_iters={args.cfr_iters} "
          f"epochs={args.epochs} device={device}")
    print("=" * 78)

    t0 = time.time()
    ds = PokerTrajectoryDataset("leduc", recipe="self_play_nash",
                                n_trajectories=args.trajectories, cfr_iters=args.cfr_iters,
                                seed=args.seed)
    tensors = ds.to_tensors()
    game, encoder = ds.game, ds.encoder
    stats = ds.return_stats()
    print(f"data: {len(ds.trajectories)} trajectories, state_dim={ds.state_dim}, "
          f"actions={ds.num_actions}, built in {time.time() - t0:.0f}s")
    for s in (0, 1):
        print(f"  seat{s} mean return = {stats[s]['mean']:+.4f} +/- {stats[s]['se']:.4f}")

    flat = tensors["returns_to_go"][:, :, 0][tensors["mask"].astype(bool)]
    dist = collections.Counter(np.round(flat, 2).tolist())
    modal = max(dist, key=dist.get)
    print(f"  return-to-go: {len(dist)} distinct values; MODAL = {modal:+.0f} "
          f"({dist[modal] / len(flat):.1%} of steps)  [Kuhn: 4 values, modal -1 at 41.7%]")

    torch.manual_seed(args.seed)
    model = DecisionTransformer(DecisionTransformerConfig(
        state_dim=ds.state_dim, act_dim=ds.num_actions, hidden_size=64, n_layer=3, n_head=4,
        max_ep_len=max_ep_len))
    train_decision_transformer(model, tensors, epochs=args.epochs, batch_size=256, lr=1e-3,
                               device=device, log_every=10)

    nash_policy, _ = make_cfr_policy(game, args.cfr_iters, args.seed)
    targets = sorted({float(v) for v in dist}) + [15.0]     # +15 is IMPOSSIBLE (max is +13)
    print(f"\ntarget return -> chips/hand vs near-Nash ({args.hands} hands each, seats alternated)")
    print(f"{'target R':>10}{'chips/hand':>14}{'+/- se':>9}{'illegal mass':>14}{'data share':>12}")
    print("-" * 59)
    rows = {}
    for R in targets:
        mean, se, diag = play_dt(model, torch, encoder, game, nash_policy, R, args.hands,
                                 device, max_ep_len, args.seed)
        share = dist.get(R, 0) / len(flat)
        tag = "  <-- IMPOSSIBLE/OOD" if R not in dist else ("  <-- MODAL" if R == modal else "")
        rows[str(R)] = {"chips_per_hand": mean, "se": se, "data_share": share,
                        "mean_illegal_mass": diag["mean_illegal_mass"]}
        print(f"{R:>10.0f}{mean:>14.4f}{se:>9.4f}{diag['mean_illegal_mass']:>14.4f}"
              f"{share:>11.1%}{tag}")
    print("-" * 59)

    # Does performance RISE with the conditioned return? This is the step's original prediction,
    # which FAILED on Kuhn (flat, ~0.68 chips at every target). Fit only the IN-DISTRIBUTION
    # targets; the impossible +15 is an extrapolation probe, not part of the trend.
    in_dist = [(float(k), rows[k]["chips_per_hand"]) for k in rows if float(k) in dist]
    xs = np.array([x for x, _ in in_dist])
    ys = np.array([y for _, y in in_dist])
    slope, intercept = np.polyfit(xs, ys, 1)
    pearson = float(np.corrcoef(xs, ys)[0, 1])
    rank = float(np.corrcoef(np.argsort(np.argsort(xs)), np.argsort(np.argsort(ys)))[0, 1])
    ood_key = str(15.0)
    best_real = max(in_dist, key=lambda t: t[1])

    vals = [rows[k]["chips_per_hand"] for k in rows]
    spread = max(vals) - min(vals)
    print(f"return-conditioning trend (in-distribution targets only):")
    print(f"  slope = {slope:+.5f} chips per unit of target return")
    print(f"  Pearson r = {pearson:+.3f}   Spearman rho = {rank:+.3f}")
    print(f"  best real target R={best_real[0]:+.0f} -> {best_real[1]:+.4f}; "
          f"IMPOSSIBLE R=+15 -> {rows[ood_key]['chips_per_hand']:+.4f} "
          f"({'saturates/degrades' if rows[ood_key]['chips_per_hand'] <= best_real[1] else 'exceeds best real (!)'})")
    if pearson > 0.5:
        print("  -> RETURN CONDITIONING STEERS on Leduc (higher target -> better play), which it "
              "did NOT do on Kuhn. Supports the payoff-alphabet explanation.")
    elif pearson < -0.5:
        print("  -> Conditioning steers BACKWARDS (higher target -> worse play). Investigate.")
    else:
        print("  -> No monotone steering on Leduc either; the Kuhn null result generalises.")
    modal_perf = rows[str(modal)]["chips_per_hand"]
    others = [rows[k]["chips_per_hand"] for k in rows if float(k) != modal]
    modal_gap = float(np.mean(others)) - modal_perf
    modal_se = rows[str(modal)]["se"]
    print(f"performance spread across targets = {spread:.4f} chips/hand")
    print(f"modal target R={modal:+.0f}: {modal_perf:+.4f} vs mean of others "
          f"{float(np.mean(others)):+.4f}  -> gap {modal_gap:+.4f} "
          f"({modal_gap / modal_se:.1f} SE)")
    if modal_gap > 2 * modal_se:
        print("-> NOTCH REPRODUCES: the modal return is a distinctly WORSE conditioning target, "
              "as in Kuhn. The mechanism generalises beyond a 4-value payoff ladder.")
    else:
        print("-> NO NOTCH: the Kuhn collapse at the modal return does NOT reproduce on Leduc's "
              "15-value payoff ladder -- evidence it was a small-payoff-alphabet artefact.")

    payload = {"game": "leduc", "trajectories": args.trajectories, "cfr_iters": args.cfr_iters,
               "epochs": args.epochs, "hands_per_target": args.hands, "device": device,
               "state_dim": ds.state_dim, "num_actions": ds.num_actions,
               "seat0_mean": stats[0]["mean"], "seat0_se": stats[0]["se"],
               "return_distribution": {str(k): v / len(flat) for k, v in sorted(dist.items())},
               "modal_return": modal, "performance_spread": spread,
               "trend_slope": float(slope), "trend_pearson": pearson, "trend_spearman": rank,
               "modal_gap_chips": modal_gap, "modal_gap_se": modal_gap / modal_se,
               "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"), "targets": rows}
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "leduc_stage0.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"\nsaved -> {path}  (total {time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
