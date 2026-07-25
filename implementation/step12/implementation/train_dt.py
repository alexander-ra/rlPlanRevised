"""
train_dt.py  [SUP]  -- raw L295-325.

Trains the self-contained Decision Transformer on Kuhn self-play data and runs the two
signature experiments of the step:

  1. RETURN CONDITIONING (raw L314-319). Condition the trained DT on a range of target
     returns-to-go -- low, medium, high, and an IMPOSSIBLE one (higher than anything in the
     data, the Paster extrapolation probe) -- extract the induced Kuhn strategy, and measure
     exploitability with the EXACT Step 02 metric. Prediction: higher target return -> the DT
     plays more like a winner -> lower exploitability, up to the point where conditioning on an
     impossible return degrades (out-of-distribution).

  2. LUCK vs SKILL (raw L321, Paster et al.). Break the DT's root-node bet frequency down BY
     CARD. Because return-to-go in poker is the final payoff (which depends on the deal), a DT
     that conditions on high return tends to bet more with cards that HAPPENED to win in the
     data -- i.e. it keys on LUCK, not the situation. We report bet-prob-by-card under high vs
     low conditioning to expose this.

Everything here is guarded by torch. All printed numbers are PREDICTIONS to verify next
session (WORKFLOW section 0).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from deps import require_torch, torch_available

torch = require_torch()
F = torch.nn.functional

from trajectory_dataset import PokerTrajectoryDataset
from state_encoding import PokerStateEncoder
from decision_transformer import DecisionTransformer, DecisionTransformerConfig


# --- training ------------------------------------------------------------------------
def train_decision_transformer(model: DecisionTransformer, tensors: dict, epochs: int = 40,
                               batch_size: int = 128, lr: float = 1e-3, device: str = "cpu",
                               log_every: int = 10) -> list:
    """Standard DT supervised training: predict a_t from (R_hat_<=t, s_<=t, a_<t)."""
    states = torch.as_tensor(tensors["states"], dtype=torch.float32, device=device)
    actions = torch.as_tensor(tensors["actions"], dtype=torch.long, device=device)
    rtg = torch.as_tensor(tensors["returns_to_go"], dtype=torch.float32, device=device)
    timesteps = torch.as_tensor(tensors["timesteps"], dtype=torch.long, device=device)
    mask = torch.as_tensor(tensors["mask"], dtype=torch.float32, device=device)

    model = model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    N = states.shape[0]
    history = []
    for ep in range(epochs):
        perm = torch.randperm(N, device=device)
        total, count = 0.0, 0
        for i in range(0, N, batch_size):
            idx = perm[i:i + batch_size]
            logits = model(states[idx], actions[idx], rtg[idx], timesteps[idx], mask[idx])
            b_mask = mask[idx].bool()
            loss = F.cross_entropy(logits[b_mask], actions[idx][b_mask])
            opt.zero_grad()
            loss.backward()
            opt.step()
            total += float(loss.detach()) * int(b_mask.sum())
            count += int(b_mask.sum())
        avg = total / max(1, count)
        history.append(avg)
        if (ep + 1) % log_every == 0 or ep == 0:
            print(f"[DT] epoch {ep + 1:3d}/{epochs}  loss={avg:.4f}")
    return history


# --- experiment 1: return conditioning ----------------------------------------------
def return_conditioning_experiment(model: DecisionTransformer, encoder: PokerStateEncoder,
                                   game, target_returns, device: str = "cpu") -> dict:
    """For each target return, extract the induced strategy and score exploitability (chips)."""
    from strategy_extraction import extract_dt_strategy
    from evaluation import exploitability_chips, bluff_freq, value_bet_freq

    out = {}
    for R in target_returns:
        node_map = extract_dt_strategy(model, encoder, game, target_return=float(R),
                                       device=device)
        out[R] = {
            "exploitability_chips": exploitability_chips(node_map),
            "bluff_freq_J": bluff_freq(node_map),
            "value_bet_freq_K": value_bet_freq(node_map),
        }
    return out


# --- experiment 2: luck vs skill ----------------------------------------------------
def luck_vs_skill_experiment(model: DecisionTransformer, encoder: PokerStateEncoder, game,
                             high_return: float, low_return: float, device: str = "cpu") -> dict:
    """Root-node P(bet) by card under high vs low return conditioning.

    A situation-driven (skilled) player bets mostly with the King; a luck-driven DT will shift
    ALL cards' bet-freq up when told to 'aim high', including the Jack -- the Paster signature.
    """
    from strategy_extraction import dt_root_bet_prob_by_card

    high = dt_root_bet_prob_by_card(model, encoder, game, high_return, device)
    low = dt_root_bet_prob_by_card(model, encoder, game, low_return, device)
    return {card: {"p_bet_high": high[card], "p_bet_low": low[card]} for card in high}


# --- orchestration -------------------------------------------------------------------
def build_and_train(cfg: dict, device: str = "cpu"):
    """Create data + DT from a config dict (see config.py) and train. Returns (model, ds)."""
    ds = PokerTrajectoryDataset(
        game_name=cfg["game"], recipe="self_play_nash",
        n_trajectories=cfg["n_trajectories"], cfr_iters=cfg["cfr_iters"], seed=cfg["seed"],
    )
    tensors = ds.to_tensors()
    dt_cfg = DecisionTransformerConfig(
        state_dim=ds.state_dim, act_dim=ds.num_actions,
        hidden_size=cfg["hidden_size"], n_layer=cfg["n_layer"], n_head=cfg["n_head"],
        max_ep_len=cfg["max_ep_len"],
    )
    model = DecisionTransformer(dt_cfg)
    train_decision_transformer(model, tensors, epochs=cfg["dt_epochs"],
                               batch_size=cfg["batch_size"], lr=cfg["lr"], device=device)
    return model, ds


def main():
    if not torch_available():
        print("PyTorch not available; skipping DT training. (Torch-free suites still run.)")
        return
    from config import active_config, TARGET_RETURNS, IMPOSSIBLE_RETURN

    cfg = active_config()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"train_dt: profile={cfg['name']} device={device}")

    model, ds = build_and_train(cfg, device=device)
    game, encoder = ds.game, ds.encoder

    print("\n== Experiment 1: return conditioning (exploitability in CHIPS; predictions) ==")
    targets = list(TARGET_RETURNS) + [IMPOSSIBLE_RETURN]
    rc = return_conditioning_experiment(model, encoder, game, targets, device=device)
    for R, m in rc.items():
        tag = " (IMPOSSIBLE/OOD)" if R == IMPOSSIBLE_RETURN else ""
        print(f"  target R={R:+.1f}{tag}: exploitability={m['exploitability_chips']:.4f} chips, "
              f"bluffJ={m['bluff_freq_J']:.2f}, valueK={m['value_bet_freq_K']:.2f}")

    print("\n== Experiment 2: luck vs skill (root P(bet) by card; predictions) ==")
    ls = luck_vs_skill_experiment(model, encoder, game,
                                  high_return=max(TARGET_RETURNS),
                                  low_return=min(TARGET_RETURNS), device=device)
    for card, m in sorted(ls.items()):
        print(f"  card {card}: P(bet|high)={m['p_bet_high']:.2f}  P(bet|low)={m['p_bet_low']:.2f}")

    # RUN-SESSION ADDITION: persist both experiments so `plotting.py` can draw the real
    # figures from measured data. Without this nothing on disk backs the plots and the only
    # PNG-producing code path was plotting's own self-test on HARD-CODED numbers -- which
    # would have put a fabricated figure in the repo (WORKFLOW section 0).
    import json
    import os
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"dt_experiments_{cfg['name']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "profile": cfg["name"],
            "impossible_return": IMPOSSIBLE_RETURN,
            "return_conditioning": {str(R): m for R, m in rc.items()},
            "luck_vs_skill": {str(c): m for c, m in ls.items()},
        }, f, indent=2)
    print(f"\nsaved -> {path}")


if __name__ == "__main__":
    main()
