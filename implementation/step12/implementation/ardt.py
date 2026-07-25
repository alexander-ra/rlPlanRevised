"""
ardt.py  [CORE / thesis-critical]  -- raw L327-379. Adversarially Robust Decision Transformer
(Tang et al., NeurIPS 2024, arXiv:2407.18414).

THE PROBLEM ARDT FIXES
----------------------
A vanilla DT conditioned on high return-to-go learns whatever line HAPPENED to produce a high
return in the data. In a competitive game that data was collected against a MIX of opponents,
so a high return often means "I got to exploit a weak opponent." Condition on that and the DT
plays an exploitative, NON-robust strategy that a Nash opponent then punishes. ARDT instead
conditions on the *minimax* return -- the return the protagonist can guarantee against the
WORST-CASE opponent -- so the learned policy is robust and (with full coverage) approaches Nash.

HOW WE APPROXIMATE THE MINIMAX RETURN (expectile regression)
------------------------------------------------------------
For each hero state we have a DISTRIBUTION of returns-to-go across the opponents in the data.
The worst-case (min over opponents) return is the low tail of that distribution. We estimate it
with EXPECTILE REGRESSION: the tau-expectile is the minimizer of the asymmetric squared loss
    L(pred) = E[ |tau - 1{(y - pred) < 0}| * (y - pred)^2 ].
  - tau -> 0   pushes pred toward the MIN  (pessimistic / worst-case  -> what we want)
  - tau = 0.5  gives the MEAN
  - tau -> 1   pushes pred toward the MAX  (optimistic)

>>> MATH FLAG (agent derivation, TO VERIFY vs the paper) <<<
The raw step's sketch (raw L347-360) writes `tau=0.9` and calls it "pessimistic". Under the
standard expectile definition above, tau=0.9 is the OPTIMISTIC (max-side) expectile, not the
pessimistic one. For a worst-case-over-opponent target we therefore default to a LOW tau
(`EXPECTILE_TAU = 0.1`). Additionally, the full ARDT objective is a *two-sided* minimax
expectile (protagonist max over its own actions, adversary min over the adversary's); what we
implement is the single-sided pessimistic-over-outcomes proxy, which is the tractable, honest
approximation for our offline mixed-opponent Kuhn data. Both points are on the verify-list in
targetedReading/summary.md and must be checked against Sections 3-4 of arXiv:2407.18414.

Guarded by torch. All printed numbers are PREDICTIONS to verify (WORKFLOW section 0).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from deps import require_torch, torch_available

torch = require_torch()
nn = torch.nn
F = torch.nn.functional

from trajectory_dataset import PokerTrajectoryDataset
from state_encoding import PokerStateEncoder
from decision_transformer import DecisionTransformer, DecisionTransformerConfig
from train_dt import train_decision_transformer

EXPECTILE_TAU = 0.1  # pessimistic (worst-case-over-opponent) side; see MATH FLAG above.


# --- expectile regression ------------------------------------------------------------
def expectile_loss(pred, target, tau: float = EXPECTILE_TAU):
    """Asymmetric squared (expectile) loss. tau<0.5 -> pessimistic (low-tail) fit."""
    diff = target - pred
    weight = torch.where(diff >= 0, torch.as_tensor(tau, device=pred.device),
                         torch.as_tensor(1.0 - tau, device=pred.device))
    return (weight * diff.pow(2)).mean()


class MinimaxReturnEstimator(nn.Module):
    """MLP state -> scalar: the pessimistic (worst-case) return-to-go for that state."""

    def __init__(self, state_dim: int, hidden_size: int = 64, n_layers: int = 2):
        super().__init__()
        layers = [nn.Linear(state_dim, hidden_size), nn.ReLU()]
        for _ in range(n_layers - 1):
            layers += [nn.Linear(hidden_size, hidden_size), nn.ReLU()]
        layers.append(nn.Linear(hidden_size, 1))
        self.net = nn.Sequential(*layers)

    def forward(self, states):
        return self.net(states).squeeze(-1)


def train_minimax_estimator(estimator: MinimaxReturnEstimator, tensors: dict,
                            tau: float = EXPECTILE_TAU, epochs: int = 60, batch_size: int = 256,
                            lr: float = 1e-3, device: str = "cpu", log_every: int = 20) -> list:
    """Fit the tau-expectile of return-to-go per state over all real steps."""
    states = torch.as_tensor(tensors["states"], dtype=torch.float32, device=device)
    rtg = torch.as_tensor(tensors["returns_to_go"], dtype=torch.float32, device=device).squeeze(-1)
    mask = torch.as_tensor(tensors["mask"], dtype=torch.bool, device=device)
    flat_s = states[mask]
    flat_r = rtg[mask]

    estimator = estimator.to(device)
    opt = torch.optim.Adam(estimator.parameters(), lr=lr)
    n = flat_s.shape[0]
    history = []
    for ep in range(epochs):
        perm = torch.randperm(n, device=device)
        total = 0.0
        for i in range(0, n, batch_size):
            idx = perm[i:i + batch_size]
            pred = estimator(flat_s[idx])
            loss = expectile_loss(pred, flat_r[idx], tau)
            opt.zero_grad()
            loss.backward()
            opt.step()
            total += float(loss) * len(idx)
        avg = total / max(1, n)
        history.append(avg)
        if (ep + 1) % log_every == 0 or ep == 0:
            print(f"[ARDT/expectile tau={tau}] epoch {ep + 1:3d}/{epochs}  loss={avg:.4f}")
    return history


def relabel_returns(estimator: MinimaxReturnEstimator, tensors: dict, device: str = "cpu") -> dict:
    """Replace each step's return-to-go with the estimated minimax (worst-case) return.

    This is the ARDT relabeling: the DT is then trained to reproduce actions CONDITIONED ON THE
    ROBUST RETURN rather than the (opponent-dependent, exploitable) realized return.
    """
    states = torch.as_tensor(tensors["states"], dtype=torch.float32, device=device)
    with torch.no_grad():
        B, T, _ = states.shape
        robust = estimator(states.reshape(B * T, -1)).reshape(B, T, 1).cpu().numpy()
    new = dict(tensors)
    # Zero out padded steps' returns so they never leak into training targets.
    robust = robust * tensors["mask"][:, :, None]
    new["returns_to_go"] = robust.astype(np.float32)
    return new


# --- the ARDT wrapper ----------------------------------------------------------------
@dataclass
class ARDTConfig:
    hidden_size: int = 64
    n_layer: int = 3
    n_head: int = 4
    max_ep_len: int = 16
    expectile_tau: float = EXPECTILE_TAU
    estimator_hidden: int = 64


class AdversariallyRobustDT:
    """A minimax-return estimator + a return-conditioned DT trained on relabeled returns."""

    def __init__(self, state_dim: int, act_dim: int, cfg: ARDTConfig | None = None):
        self.cfg = cfg or ARDTConfig()
        self.state_dim = state_dim
        self.act_dim = act_dim
        self.estimator = MinimaxReturnEstimator(state_dim, self.cfg.estimator_hidden)
        self.dt = DecisionTransformer(DecisionTransformerConfig(
            state_dim=state_dim, act_dim=act_dim, hidden_size=self.cfg.hidden_size,
            n_layer=self.cfg.n_layer, n_head=self.cfg.n_head, max_ep_len=self.cfg.max_ep_len,
        ))

    def train(self, tensors: dict, estimator_epochs: int = 60, dt_epochs: int = 40,
              batch_size: int = 128, lr: float = 1e-3, device: str = "cpu") -> dict:
        est_hist = train_minimax_estimator(self.estimator, tensors, tau=self.cfg.expectile_tau,
                                           epochs=estimator_epochs, batch_size=batch_size, lr=lr,
                                           device=device)
        relabeled = relabel_returns(self.estimator, tensors, device=device)
        dt_hist = train_decision_transformer(self.dt, relabeled, epochs=dt_epochs,
                                             batch_size=batch_size, lr=lr, device=device)
        return {"estimator_loss": est_hist, "dt_loss": dt_hist}

    @torch.no_grad()
    def robust_target(self, state_vec, device: str = "cpu") -> float:
        """The minimax return the estimator predicts for a single encoded state."""
        s = torch.as_tensor(state_vec, dtype=torch.float32, device=device).view(1, -1)
        return float(self.estimator(s).item())


# --- orchestration -------------------------------------------------------------------
def build_and_train_ardt(cfg: dict, device: str = "cpu"):
    """Create MIXED-opponent data + ARDT from a config dict (see config.py). Returns (ardt, ds)."""
    ds = PokerTrajectoryDataset(
        game_name=cfg["game"], recipe="mixed_opponents",
        n_trajectories=cfg["n_trajectories"], cfr_iters=cfg["cfr_iters"],
        exploit_frac=cfg["exploit_frac"], seed=cfg["seed"],
    )
    tensors = ds.to_tensors()
    ardt = AdversariallyRobustDT(ds.state_dim, ds.num_actions, ARDTConfig(
        hidden_size=cfg["hidden_size"], n_layer=cfg["n_layer"], n_head=cfg["n_head"],
        max_ep_len=cfg["max_ep_len"], expectile_tau=cfg.get("expectile_tau", EXPECTILE_TAU),
    ))
    ardt.train(tensors, estimator_epochs=cfg["estimator_epochs"], dt_epochs=cfg["dt_epochs"],
               batch_size=cfg["batch_size"], lr=cfg["lr"], device=device)
    return ardt, ds


def main():
    if not torch_available():
        print("PyTorch not available; skipping ARDT training.")
        return
    from config import active_config
    from strategy_extraction import extract_ardt_strategy
    from evaluation import exploitability_chips

    cfg = active_config()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"ardt: profile={cfg['name']} device={device} (mixed-opponent data)")
    ardt, ds = build_and_train_ardt(cfg, device=device)

    node_map = extract_ardt_strategy(ardt, ds.encoder, ds.game, device=device)
    expl = exploitability_chips(node_map)
    print(f"\n[PREDICTION] ARDT exploitability on Kuhn = {expl:.4f} chips "
          f"(target: below a same-data vanilla DT, and near Nash). VERIFY next session.")


def _selftest():
    torch.manual_seed(0)
    pred = torch.randn(1000, requires_grad=True)
    target = torch.randn(1000)
    lo = expectile_loss(pred.detach(), target, tau=0.1)
    hi = expectile_loss(pred.detach(), target, tau=0.9)
    # Fit a scalar expectile of a skewed sample to sanity-check tau direction.
    y = torch.tensor([-2.0] * 90 + [2.0] * 10)  # mostly -2, a few +2; mean = -1.6
    for tau, label in ((0.1, "low"), (0.9, "high")):
        p = torch.zeros(1, requires_grad=True)
        opt = torch.optim.Adam([p], lr=0.05)
        for _ in range(500):
            opt.zero_grad()
            expectile_loss(p.expand_as(y), y, tau).backward()
            opt.step()
        print(f"expectile tau={tau} ({label}) -> {float(p):+.3f} "
              f"(expect low<mean(-1.6)<high)")
    print("expectile_loss finite:", np.isfinite(float(lo)) and np.isfinite(float(hi)))


if __name__ == "__main__":
    _selftest()
