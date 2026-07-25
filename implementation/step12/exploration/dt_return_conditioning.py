"""
exploration/dt_return_conditioning.py

PROBE: does a Decision Transformer actually STEER by the return you condition on -- and what
happens when you ask for a return that NEVER occurred in the data (the Paster OOD probe)?

Trains a tiny DT on near-Nash Kuhn self-play, then extracts the induced strategy while
conditioning on a sweep of target returns-to-go: the real ones {-2,-1,+1,+2} plus an IMPOSSIBLE
+3 (no Kuhn hand ever pays +3). We print the exact Step 02 exploitability at each.

PREDICTIONS (verify in the run session):
  - Conditioning on higher (more winning) returns -> the DT plays more like a winner -> lower
    exploitability, up to the in-distribution max.
  - The IMPOSSIBLE +3 either saturates (behaves like +2) or DEGRADES (higher exploitability):
    the model is extrapolating outside its data and there is no magic beyond the best real line.

Torch-guarded; if torch is missing it prints a note and exits. NOT executed here.
"""

from __future__ import annotations

import _bootstrap  # noqa: F401
from deps import torch_available


def main():
    if not torch_available():
        print("PyTorch unavailable; this probe needs torch. (Try the coin-flip probe instead.)")
        return
    import torch
    from trajectory_dataset import PokerTrajectoryDataset
    from decision_transformer import DecisionTransformer, DecisionTransformerConfig
    from train_dt import train_decision_transformer
    from strategy_extraction import extract_dt_strategy
    from evaluation import exploitability_chips, chips_to_mbb_per_hand

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"dt_return_conditioning probe (device={device}) -- predictions only")
    print("-" * 66)

    ds = PokerTrajectoryDataset("kuhn", recipe="self_play_nash",
                                n_trajectories=3000, cfr_iters=3000, seed=0)
    model = DecisionTransformer(DecisionTransformerConfig(
        state_dim=ds.state_dim, act_dim=ds.num_actions, hidden_size=32, n_layer=2, n_head=4))
    train_decision_transformer(model, ds.to_tensors(), epochs=15, batch_size=128,
                               device=device, log_every=5)

    print("\ntarget return -> exploitability (lower = closer to Nash):")
    for R in (-2.0, -1.0, 1.0, 2.0, 3.0):
        nm = extract_dt_strategy(model, ds.encoder, ds.game, target_return=R, device=device)
        expl = exploitability_chips(nm)
        tag = "  <-- IMPOSSIBLE / out-of-distribution" if R == 3.0 else ""
        print(f"  R={R:+.1f}: {expl:.4f} chips ({chips_to_mbb_per_hand(expl):.1f} mbb/h){tag}")
    print("\n(Interpretation and PASS/FAIL live in implementation/validate.py.)")


if __name__ == "__main__":
    main()
