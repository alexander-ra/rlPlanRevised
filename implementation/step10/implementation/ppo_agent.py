"""
ppo_agent.py -- a compact discrete PPO agent that plays Leduc, with ACTION MASKING and
per-agent mutable hyperparameters for PBT (raw step 10 L341-349 "Use your Step 1 PPO...",
L408-438).

WHAT THIS IS
------------
The neural building block of the league. It mirrors Step 01's / Step 09's clipped-surrogate
PPO objective (Schulman et al. 2017), rewritten for Leduc's variable-length imperfect-info
episodes:

  - actor-critic MLP: obs (leduc_rl.OBS_DIM) -> shared body -> policy logits (3) + value (1);
  - ACTION MASKING: illegal Leduc actions get a large negative logit so they are never
    sampled and never carry gradient (fold is illegal unless facing a raise, etc.);
  - Monte-Carlo returns: Leduc pays only at the terminal, so every hero decision this hand
    shares the terminal utility as its value target (undiscounted, gamma=1 -- standard for a
    single hand);
  - PBT knobs: `lr` and `entropy_coef` are per-agent and MUTABLE, so PBT can `clone_from` a
    strong agent's weights and then `perturb_hyperparams` (the explore/exploit of PBT).

torch is imported lazily (via Step 09's `learners.torch_available`) so importing this module
never hard-requires torch; the league guards on availability.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401  (step09 + step07 on sys.path)
from learners import torch_available, require_torch   # reuse Step 09's lazy torch guard
from leduc_rl import OBS_DIM, N_ACTIONS, rollout

_NEG = 1.0e9   # finite masking constant: exp(-1e9) underflows to exactly 0.0 (no NaNs)

DEFAULT_HYPERPARAMS = {
    "hidden": 64,
    "lr": 3e-3,
    "clip": 0.2,
    "entropy_coef": 0.01,
    "value_coef": 0.5,
    "epochs": 4,
    "minibatch": 512,
    "max_grad_norm": 0.5,
}


def _build_net(torch, obs_dim, n_actions, hidden):
    nn = torch.nn

    class ActorCritic(nn.Module):
        def __init__(self):
            super().__init__()
            self.body = nn.Sequential(nn.Linear(obs_dim, hidden), nn.Tanh(),
                                      nn.Linear(hidden, hidden), nn.Tanh())
            self.pi = nn.Linear(hidden, n_actions)
            self.v = nn.Linear(hidden, 1)

        def forward(self, x):
            h = self.body(x)
            return self.pi(h), self.v(h).squeeze(-1)

    return ActorCritic()


class PPOAgent:
    """A maskable discrete-PPO agent for Leduc. `act` plugs straight into `leduc_rl.rollout`;
    `probs` plugs into `leduc_rl.extract_tabular_policy`."""

    def __init__(self, hyperparams: dict | None = None, seed: int = 0,
                 obs_dim: int = OBS_DIM, n_actions: int = N_ACTIONS):
        torch = require_torch()
        self.torch = torch
        self.hp = {**DEFAULT_HYPERPARAMS, **(hyperparams or {})}
        self.seed = seed
        self.obs_dim = obs_dim
        self.n_actions = n_actions
        torch.manual_seed(seed)
        self.net = _build_net(torch, obs_dim, n_actions, self.hp["hidden"])
        self.opt = torch.optim.Adam(self.net.parameters(), lr=self.hp["lr"])

    # ---- acting ----
    def act(self, obs, legal_actions):
        """Sample a LEGAL action; return (action, logp) under the masked policy. Matches the
        `act_fn(obs, legal_actions)` contract of `leduc_rl.rollout`."""
        torch = self.torch
        x = torch.as_tensor(np.asarray(obs, dtype=np.float32)).unsqueeze(0)
        mask = torch.full((1, self.n_actions), -_NEG)
        mask[0, list(legal_actions)] = 0.0
        with torch.no_grad():
            logits, _ = self.net(x)
            dist = torch.distributions.Categorical(logits=logits + mask)
            action = dist.sample()
            logp = dist.log_prob(action)
        return int(action.item()), float(logp.item())

    def probs(self, obs) -> np.ndarray:
        """FULL (unmasked) softmax over all actions. `leduc_rl.make_net_policy` re-masks to the
        legal set and renormalizes -- which equals the masked play distribution exactly, since
        softmax restricted to a subset == softmax over that subset."""
        torch = self.torch
        x = torch.as_tensor(np.asarray(obs, dtype=np.float32)).unsqueeze(0)
        with torch.no_grad():
            logits, _ = self.net(x)
            p = torch.softmax(logits, dim=-1).squeeze(0).cpu().numpy()
        return p

    # ---- learning ----
    def update(self, obs, actions, old_logps, returns, masks) -> dict:
        """One PPO update from a batch. `masks` is (T, n_actions) 0/1 legal masks; the masked
        log-softmax makes the recomputed log-probs consistent with `act`."""
        torch = self.torch
        obs_t = torch.as_tensor(np.asarray(obs, np.float32))
        act_t = torch.as_tensor(np.asarray(actions, np.int64))
        oldlp_t = torch.as_tensor(np.asarray(old_logps, np.float32))
        ret_t = torch.as_tensor(np.asarray(returns, np.float32))
        mask_t = torch.as_tensor(np.asarray(masks, np.float32))
        neg_inf = (mask_t - 1.0) * _NEG           # 0 where legal, -1e9 where illegal

        T = obs_t.shape[0]
        hp = self.hp
        p_loss = v_loss = ent = 0.0
        n = 0
        for _ in range(hp["epochs"]):
            idx = np.random.permutation(T)
            for start in range(0, T, hp["minibatch"]):
                mb = torch.as_tensor(idx[start:start + hp["minibatch"]], dtype=torch.long)
                logits, values = self.net(obs_t[mb])
                masked = logits + neg_inf[mb]
                logsoft = torch.log_softmax(masked, dim=-1)
                probs = torch.softmax(masked, dim=-1)
                new_lp = logsoft.gather(1, act_t[mb].unsqueeze(1)).squeeze(1)
                entropy = -(probs * logsoft).sum(dim=-1).mean()   # illegal terms are 0*(-1e9)=0
                adv = ret_t[mb] - values.detach()
                adv = (adv - adv.mean()) / (adv.std() + 1e-8)
                ratio = torch.exp(new_lp - oldlp_t[mb])
                surr1 = ratio * adv
                surr2 = torch.clamp(ratio, 1 - hp["clip"], 1 + hp["clip"]) * adv
                policy_loss = -torch.min(surr1, surr2).mean()
                value_loss = ((values - ret_t[mb]) ** 2).mean()
                loss = policy_loss + hp["value_coef"] * value_loss - hp["entropy_coef"] * entropy
                self.opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.net.parameters(), hp["max_grad_norm"])
                self.opt.step()
                p_loss += float(policy_loss.item())
                v_loss += float(value_loss.item())
                ent += float(entropy.item())
                n += 1
        return {"policy_loss": p_loss / max(n, 1), "value_loss": v_loss / max(n, 1),
                "entropy": ent / max(n, 1), "mean_return": float(np.mean(returns))}

    # ---- one epoch of self-play training against an opponent pool ----
    def train_against(self, game, opponents, weights, episodes: int, rng) -> dict:
        """Collect `episodes` hands (each vs an opponent sampled by `weights`, hero seat drawn
        uniformly so the agent learns both positions) and do one PPO update.

        `opponents` : list of Step 07 policies (net policies of other agents / frozen snapshots).
        `weights`   : matchmaking distribution over `opponents` (sums to 1).
        """
        if not opponents:
            return {"episodes": 0, "note": "no opponents"}
        w = np.asarray(weights, dtype=float)
        w = w / w.sum() if w.sum() > 0 else np.ones(len(opponents)) / len(opponents)
        b_obs, b_act, b_lp, b_ret, b_mask = [], [], [], [], []
        ep_returns = []
        for _ in range(episodes):
            j = int(rng.choice(len(opponents), p=w))
            hero_seat = int(rng.integers(2))
            transitions, u = rollout(game, hero_seat, self.act, opponents[j], rng)
            ep_returns.append(u)
            for obs, a, lp, mask in transitions:
                b_obs.append(obs); b_act.append(a); b_lp.append(lp); b_ret.append(u); b_mask.append(mask)
        if not b_obs:
            return {"episodes": episodes, "mean_return": float(np.mean(ep_returns) if ep_returns else 0.0),
                    "note": "no hero decisions collected"}
        stats = self.update(np.array(b_obs), np.array(b_act), np.array(b_lp),
                            np.array(b_ret), np.array(b_mask))
        stats["episodes"] = episodes
        stats["mean_episode_return"] = float(np.mean(ep_returns))
        return stats

    # ---- PBT explore/exploit primitives ----
    def clone_from(self, other: "PPOAgent"):
        """Copy the other agent's network weights (PBT 'exploit'). A fresh optimizer is created
        with THIS agent's current lr; call `perturb_hyperparams` afterwards for 'explore'."""
        self.net.load_state_dict(other.net.state_dict())
        self.opt = self.torch.optim.Adam(self.net.parameters(), lr=self.hp["lr"])

    def perturb_hyperparams(self, rng, lr_factors=(0.8, 1.25), ent_factors=(0.5, 2.0)):
        """PBT 'explore': multiplicatively perturb lr and entropy_coef, then rebuild the
        optimizer at the new lr. Bounds keep values sane."""
        self.hp["lr"] = float(np.clip(self.hp["lr"] * rng.choice(lr_factors), 1e-5, 1e-1))
        self.hp["entropy_coef"] = float(np.clip(self.hp["entropy_coef"] * rng.choice(ent_factors),
                                                1e-4, 0.5))
        self.opt = self.torch.optim.Adam(self.net.parameters(), lr=self.hp["lr"])

    def probs_fn(self):
        """Return the deterministic obs->probs callable for `leduc_rl.extract_tabular_policy`."""
        return self.probs


def _selftest():
    print("ppo_agent self-test")
    print("-" * 60)
    if not torch_available():
        print("[SKIP] torch not installed -> PPOAgent unavailable.")
        return
    from engines import make_game
    from policies import uniform_policy
    from leduc_rl import extract_tabular_policy
    from best_response import nash_gap
    game = make_game("leduc")
    agent = PPOAgent(seed=0)
    rng = np.random.default_rng(0)
    stats = agent.train_against(game, [uniform_policy()], [1.0], episodes=64, rng=rng)
    print(f"  trained 1 epoch vs uniform: {stats}")
    tab = extract_tabular_policy(game, agent.probs_fn())
    gap = nash_gap(game, tab, tab)["nash_conv"]
    print(f"  extracted-policy exploitability (NashConv) = {gap:.4f} "
          f"(PREDICT: finite; should DECREASE with more training epochs vs the league)")


if __name__ == "__main__":
    _selftest()
