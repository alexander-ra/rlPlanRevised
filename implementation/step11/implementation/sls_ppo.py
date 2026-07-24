"""
sls_ppo.py -- a masked, episodic PPO agent for ONE So Long Sucker seat (raw step 11 L467-499). 🔴

WHY NEW CODE (not Step 09 MAPPO / Step 10 ppo_agent)
----------------------------------------------------
Those learners are ONE-STEP / 2-player. SLS is sequential, VARIABLE-LENGTH, 4-player and needs
ACTION MASKING over a fixed action space. So this reuses only the *idea* (clipped-surrogate PPO,
Schulman et al. 2017) and reimplements it for SLS. torch is guarded via Step 09's `require_torch`
(reuse, not reinvent -- WORKFLOW S6).

THE AGENT
---------
- an actor-critic MLP: shared body -> policy logits (action_dim) + state value (scalar).
- `act(obs, mask)` samples a LEGAL action (illegal logits set to a finite -1e9, per Step 10's note
  -- never -inf, so `0 * -1e9` in the entropy term stays finite).
- `update(...)` does the clipped-PPO update from a batch of transitions the trainer collected
  (the trainer -- `coalition_mappo.py` -- owns the self-play loop and assigns the returns, which is
  where the sparse-vs-Shapley reward choice lives).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Requires torch.
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401  (Step 10 + Step 09 on sys.path)
from learners import require_torch, torch_available  # reuse Step 09's lazy torch guard

MASK_NEG = -1e9  # finite mask sentinel (NOT -inf; keeps entropy finite -- Step 10 lesson)

DEFAULT_PPO_CONFIG = {
    "hidden": 128, "lr": 3e-4, "clip": 0.2, "entropy_coef": 0.01, "value_coef": 0.5,
    "epochs": 4, "minibatch": 512, "max_grad_norm": 0.5, "seed": 0,
}


def _make_net(torch, obs_dim, action_dim, hidden):
    nn = torch.nn

    class ActorCritic(nn.Module):
        def __init__(self):
            super().__init__()
            self.body = nn.Sequential(nn.Linear(obs_dim, hidden), nn.Tanh(),
                                      nn.Linear(hidden, hidden), nn.Tanh())
            self.pi = nn.Linear(hidden, action_dim)
            self.v = nn.Linear(hidden, 1)

        def forward(self, x):
            h = self.body(x)
            return self.pi(h), self.v(h).squeeze(-1)

    return ActorCritic()


class SLSPPOAgent:
    """A single-seat masked PPO agent for SLS."""

    def __init__(self, obs_dim: int, action_dim: int, config: dict | None = None):
        torch = require_torch()
        self.torch = torch
        self.cfg = {**DEFAULT_PPO_CONFIG, **(config or {})}
        torch.manual_seed(self.cfg["seed"])
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        self.net = _make_net(torch, obs_dim, action_dim, self.cfg["hidden"])
        self.opt = torch.optim.Adam(self.net.parameters(), lr=self.cfg["lr"])

    def _masked_logits(self, logits, mask_t):
        return logits.masked_fill(~mask_t, MASK_NEG)

    def act(self, obs: np.ndarray, mask: np.ndarray, greedy: bool = False):
        """Return (action_idx, logp, value). `mask` is a bool array of legal actions."""
        torch = self.torch
        x = torch.as_tensor(np.asarray(obs, np.float32)).unsqueeze(0)
        m = torch.as_tensor(np.asarray(mask, bool)).unsqueeze(0)
        with torch.no_grad():
            logits, value = self.net(x)
            logits = self._masked_logits(logits, m)
            dist = torch.distributions.Categorical(logits=logits)
            a = torch.argmax(logits, -1) if greedy else dist.sample()
            lp = dist.log_prob(a)
        return int(a.item()), float(lp.item()), float(value.item())

    def value(self, obs: np.ndarray) -> float:
        torch = self.torch
        x = torch.as_tensor(np.asarray(obs, np.float32)).unsqueeze(0)
        with torch.no_grad():
            _, v = self.net(x)
        return float(v.item())

    def update(self, obs, actions, old_logps, masks, returns):
        """One clipped-PPO update from a batch of this seat's transitions (numpy arrays).

        obs (T,obs_dim) · actions (T,) int · old_logps (T,) · masks (T,action_dim) bool ·
        returns (T,) value targets (the trainer's chosen reward-to-go). Returns mean losses.
        """
        torch = self.torch
        cfg = self.cfg
        T = len(actions)
        if T == 0:
            return {"policy_loss": 0.0, "value_loss": 0.0, "entropy": 0.0}
        obs_t = torch.as_tensor(np.asarray(obs, np.float32))
        act_t = torch.as_tensor(np.asarray(actions, np.int64))
        oldlp_t = torch.as_tensor(np.asarray(old_logps, np.float32))
        mask_t = torch.as_tensor(np.asarray(masks, bool))
        ret_t = torch.as_tensor(np.asarray(returns, np.float32))

        p_loss = v_loss = ent = 0.0
        n = 0
        for _ in range(cfg["epochs"]):
            idx = np.random.permutation(T)
            for start in range(0, T, cfg["minibatch"]):
                mb = torch.as_tensor(idx[start:start + cfg["minibatch"]], dtype=torch.long)
                logits, values = self.net(obs_t[mb])
                logits = self._masked_logits(logits, mask_t[mb])
                dist = torch.distributions.Categorical(logits=logits)
                new_lp = dist.log_prob(act_t[mb])
                adv = ret_t[mb] - values.detach()
                # unbiased=False: a lone-sample minibatch returns std 0, not NaN (Step 10 bug)
                adv = (adv - adv.mean()) / (adv.std(unbiased=False) + 1e-8)
                ratio = torch.exp(new_lp - oldlp_t[mb])
                surr1 = ratio * adv
                surr2 = torch.clamp(ratio, 1 - cfg["clip"], 1 + cfg["clip"]) * adv
                policy_loss = -torch.min(surr1, surr2).mean()
                value_loss = ((values - ret_t[mb]) ** 2).mean()
                entropy = dist.entropy().mean()
                loss = policy_loss + cfg["value_coef"] * value_loss - cfg["entropy_coef"] * entropy
                self.opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.net.parameters(), cfg["max_grad_norm"])
                self.opt.step()
                p_loss += float(policy_loss.item())
                v_loss += float(value_loss.item())
                ent += float(entropy.item())
                n += 1
        return {"policy_loss": p_loss / n, "value_loss": v_loss / n, "entropy": ent / n}


def make_ppo_policy(agent: "SLSPPOAgent", game, greedy: bool = False):
    """Adapt an SLSPPOAgent into an SLS policy `policy(game, state, rng) -> action` so it can play
    in `sls_game.play_game` / the EGTA tournament. Encodes the state egocentrically and decodes
    the chosen action index back to `(color, pile_target)`."""
    from state_encoding import encode_state, legal_action_mask, action_index_to_move

    def policy(g, state, rng):
        obs = encode_state(g, state)
        mask = legal_action_mask(g, state)
        idx, _lp, _v = agent.act(obs, mask, greedy=greedy)
        return action_index_to_move(g, state, idx)

    return policy


def _selftest():
    print("sls_ppo self-test  (PREDICTIONS -- verify on a real run)")
    print("-" * 72)
    if not torch_available():
        print("[SKIP] torch not installed -> SLS PPO agent unavailable.")
        return
    from state_encoding import obs_dim, action_dim
    n = 4
    agent = SLSPPOAgent(obs_dim(n), action_dim(n), {"seed": 0})
    print(f"  built SLSPPOAgent: obs_dim={obs_dim(n)}, action_dim={action_dim(n)}")
    # a tiny synthetic update to prove shapes line up (random obs/mask/returns)
    T, A = 40, action_dim(n)
    rng = np.random.default_rng(0)
    obs = rng.standard_normal((T, obs_dim(n))).astype(np.float32)
    masks = rng.random((T, A)) > 0.5
    masks[:, 0] = True  # guarantee >=1 legal action per row
    actions = np.array([int(np.argmax(masks[i])) for i in range(T)])
    old_logps = np.zeros(T, np.float32)
    returns = rng.standard_normal(T).astype(np.float32)
    stats = agent.update(obs, actions, old_logps, masks, returns)
    print(f"  1-batch update ran: losses finite? "
          f"{all(np.isfinite(v) for v in stats.values())} (must be True)")


if __name__ == "__main__":
    _selftest()
