"""
behavioral_cloning.py  [SUP]  -- raw L322-325.

The no-return-conditioning baseline: a plain MLP that maps state -> action, trained by
supervised cross-entropy on the SAME trajectories the DT uses. BC has no notion of
return-to-go, so it simply imitates the average action taken in each state in the data.

WHY IT MATTERS
--------------
BC is the control that isolates what return conditioning buys you. If DT (conditioned on high
return) is no better than BC on exploitability, then the return signal added nothing; if ARDT
beats DT which beats BC, the story "returns help, robust returns help more" holds. On
near-Nash self-play data, BC should roughly recover the data policy's (near-Nash) strategy.

Guarded by deps.require_torch() (import requires torch on purpose).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from dataclasses import dataclass

from deps import require_torch

torch = require_torch()
nn = torch.nn
F = torch.nn.functional


@dataclass
class BCConfig:
    state_dim: int
    act_dim: int
    hidden_size: int = 64
    n_layers: int = 2
    dropout: float = 0.0


class BehavioralCloning(nn.Module):
    """State -> action-logits MLP."""

    def __init__(self, cfg: BCConfig):
        super().__init__()
        self.cfg = cfg
        layers = [nn.Linear(cfg.state_dim, cfg.hidden_size), nn.ReLU()]
        for _ in range(cfg.n_layers - 1):
            layers += [nn.Linear(cfg.hidden_size, cfg.hidden_size), nn.ReLU()]
            if cfg.dropout > 0:
                layers.append(nn.Dropout(cfg.dropout))
        layers.append(nn.Linear(cfg.hidden_size, cfg.act_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, states):
        return self.net(states)

    @torch.no_grad()
    def action_probs(self, states):
        return F.softmax(self.forward(states), dim=-1)


def train_bc(model: "BehavioralCloning", tensors: dict, epochs: int = 30,
             batch_size: int = 256, lr: float = 1e-3, device: str = "cpu",
             log_every: int = 10) -> list:
    """Flatten (state, action) pairs over all real steps and fit cross-entropy.

    `tensors` is a PokerTrajectoryDataset.to_tensors() dict. Returns the loss history.
    """
    states = torch.as_tensor(tensors["states"], dtype=torch.float32)
    actions = torch.as_tensor(tensors["actions"], dtype=torch.long)
    mask = torch.as_tensor(tensors["mask"], dtype=torch.bool)
    # Keep only real (unpadded) steps.
    flat_states = states[mask]                    # (M, state_dim)
    flat_actions = actions[mask]                  # (M,)
    model = model.to(device)
    flat_states, flat_actions = flat_states.to(device), flat_actions.to(device)

    opt = torch.optim.Adam(model.parameters(), lr=lr)
    n = flat_states.shape[0]
    history = []
    for ep in range(epochs):
        perm = torch.randperm(n, device=device)
        total = 0.0
        for i in range(0, n, batch_size):
            idx = perm[i:i + batch_size]
            logits = model(flat_states[idx])
            loss = F.cross_entropy(logits, flat_actions[idx])
            opt.zero_grad()
            loss.backward()
            opt.step()
            total += float(loss.detach()) * len(idx)
        avg = total / max(1, n)
        history.append(avg)
        if (ep + 1) % log_every == 0 or ep == 0:
            print(f"[BC] epoch {ep + 1:3d}/{epochs}  loss={avg:.4f}")
    return history


def _selftest():
    torch.manual_seed(0)
    cfg = BCConfig(state_dim=10, act_dim=2, hidden_size=32)
    model = BehavioralCloning(cfg)
    fake = {
        "states": torch.randn(8, 3, 10).numpy(),
        "actions": torch.randint(0, 2, (8, 3)).numpy(),
        "mask": torch.ones(8, 3).numpy(),
    }
    hist = train_bc(model, fake, epochs=2, batch_size=4, log_every=1)
    probs = model.action_probs(torch.randn(5, 10))
    print("behavioral_cloning self-test")
    print("-" * 50)
    print(f"trained 2 epochs, final loss={hist[-1]:.4f}; probs row-sum ok: "
          f"{torch.allclose(probs.sum(-1), torch.ones(5), atol=1e-5)}")


if __name__ == "__main__":
    _selftest()
