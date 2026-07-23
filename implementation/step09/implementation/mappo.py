"""
mappo.py -- MAPPO: PPO with a CENTRALIZED VALUE FUNCTION (raw step L352, L388-390).

WHAT THIS IS
------------
The "surprising effectiveness" method (Yu et al. 2022): plain PPO, but the critic is a
CENTRALIZED value function V(s) over the GLOBAL state instead of a per-agent V(o_i). The actor
stays decentralized (pi_i(a_i | o_i)); only the advantage estimate uses the global state during
training. It is the simplest CTDE method and, per the paper, often the strongest.

Relative to MADDPG here: MAPPO centralizes a single STATE-value V(s) (not a joint-action
Q(s,a)), uses the clipped PPO surrogate on-policy, and needs no counterfactual baseline. We
keep per-agent actors (CoopSignal's speaker/listener are heterogeneous); for homogeneous
agents you would share actor parameters -- a one-line change flagged below.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Requires torch.
"""

from __future__ import annotations

import numpy as np

from learners import require_torch

DEFAULT_MAPPO_CONFIG = {
    "hidden": 64, "lr": 3e-3, "clip": 0.2, "entropy_coef": 0.01,
    "value_coef": 0.5, "epochs": 4, "minibatch": 256, "max_grad_norm": 0.5,
    "share_actor": False, "seed": 0,
}


def _build(torch, env, hidden, share_actor):
    nn = torch.nn
    n_agents = env.n_agents

    def mlp_head(out):
        return nn.Sequential(nn.Linear(env.obs_dim, hidden), nn.Tanh(),
                             nn.Linear(hidden, hidden), nn.Tanh(), nn.Linear(hidden, out))

    if share_actor:
        shared = mlp_head(env.n_actions)
        actors = nn.ModuleList([shared for _ in range(n_agents)])  # same params
    else:
        actors = nn.ModuleList([mlp_head(env.n_actions) for _ in range(n_agents)])
    # centralized value over the GLOBAL state
    critic = nn.Sequential(nn.Linear(env.global_state_dim, hidden), nn.Tanh(),
                           nn.Linear(hidden, hidden), nn.Tanh(), nn.Linear(hidden, 1))
    return actors, critic


class MAPPO:
    def __init__(self, env, config: dict | None = None):
        torch = require_torch()
        self.torch = torch
        self.env = env
        self.cfg = {**DEFAULT_MAPPO_CONFIG, **(config or {})}
        torch.manual_seed(self.cfg["seed"])
        self.n_agents = env.n_agents
        self.actors, self.critic = _build(torch, env, self.cfg["hidden"], self.cfg["share_actor"])
        # unique actor params (share_actor reuses one module, so dedupe by id)
        seen = set()
        actor_params = []
        for m in self.actors:
            if id(m) not in seen:
                seen.add(id(m))
                actor_params += list(m.parameters())
        params = actor_params + list(self.critic.parameters())
        self.opt = torch.optim.Adam(params, lr=self.cfg["lr"])

    def act(self, obs, greedy: bool = False):
        torch = self.torch
        acts, logps = [], []
        for i in range(self.n_agents):
            x = torch.as_tensor(np.asarray(obs[i], np.float32)).unsqueeze(0)
            with torch.no_grad():
                logits = self.actors[i](x)
                dist = torch.distributions.Categorical(logits=logits)
                a = torch.argmax(logits, -1) if greedy else dist.sample()
                lp = dist.log_prob(a)
            acts.append(int(a.item()))
            logps.append(float(lp.item()))
        return acts, logps

    def train(self, episodes: int = 6000, batch_episodes: int = 256, seed: int = 0):
        torch = self.torch
        cfg = self.cfg
        history = {"reward": [], "value_loss": []}
        collected = 0
        while collected < episodes:
            O = [[] for _ in range(self.n_agents)]
            LP = [[] for _ in range(self.n_agents)]
            AC = [[] for _ in range(self.n_agents)]
            GS, R = [], []
            for _ in range(batch_episodes):
                obs, gs = self.env.reset()
                acts, logps = self.act(obs)
                reward, _done, _info = self.env.step(acts)
                for i in range(self.n_agents):
                    O[i].append(np.asarray(obs[i], np.float32))
                    LP[i].append(logps[i])
                    AC[i].append(acts[i])
                GS.append(np.asarray(gs, np.float32))
                R.append(reward)
            vloss = self._update(O, LP, AC, GS, R)
            history["reward"].append(float(np.mean(R)))
            history["value_loss"].append(vloss)
            collected += batch_episodes
        return history

    def _update(self, O, LP, AC, GS, R):
        torch = self.torch
        cfg = self.cfg
        gs_t = torch.as_tensor(np.array(GS), dtype=torch.float32)
        ret_t = torch.as_tensor(np.array(R), dtype=torch.float32)     # one-step return
        obs_t = [torch.as_tensor(np.array(O[i], np.float32)) for i in range(self.n_agents)]
        act_t = [torch.as_tensor(np.array(AC[i], np.int64)) for i in range(self.n_agents)]
        oldlp_t = [torch.as_tensor(np.array(LP[i], np.float32)) for i in range(self.n_agents)]

        T = ret_t.shape[0]
        last_vloss = 0.0
        for _ in range(cfg["epochs"]):
            idx = np.random.permutation(T)
            for start in range(0, T, cfg["minibatch"]):
                mb = torch.as_tensor(idx[start:start + cfg["minibatch"]], dtype=torch.long)
                values = self.critic(gs_t[mb]).squeeze(-1)
                adv = ret_t[mb] - values.detach()
                adv = (adv - adv.mean()) / (adv.std() + 1e-8)
                loss = self.cfg["value_coef"] * ((values - ret_t[mb]) ** 2).mean()
                for i in range(self.n_agents):
                    logits = self.actors[i](obs_t[i][mb])
                    dist = torch.distributions.Categorical(logits=logits)
                    new_lp = dist.log_prob(act_t[i][mb])
                    ratio = torch.exp(new_lp - oldlp_t[i][mb])
                    surr1 = ratio * adv
                    surr2 = torch.clamp(ratio, 1 - cfg["clip"], 1 + cfg["clip"]) * adv
                    loss = loss - torch.min(surr1, surr2).mean() \
                        - cfg["entropy_coef"] * dist.entropy().mean()
                self.opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(
                    [p for g in self.actors for p in g.parameters()] +
                    list(self.critic.parameters()), cfg["max_grad_norm"])
                self.opt.step()
                last_vloss = float(((self.critic(gs_t[mb]).squeeze(-1) - ret_t[mb]) ** 2).mean().item())
        return last_vloss

    def greedy_reward(self, episodes: int = 2000) -> float:
        total = 0.0
        for _ in range(episodes):
            obs, _ = self.env.reset()
            total += self.env.step(self.act(obs, greedy=True)[0])[0]
        return total / episodes


def _selftest():
    print("mappo self-test")
    print("-" * 60)
    from learners import torch_available
    if not torch_available():
        print("[SKIP] torch not installed.")
        return
    from coop_env import CoopSignalEnv
    env = CoopSignalEnv(n_targets=3, comm=False, seed=0)
    algo = MAPPO(env, {"seed": 0})
    print(f"  built MAPPO on CoopSignal: n_agents={algo.n_agents}, "
          f"centralized V over global_state_dim={env.global_state_dim}")
    print("  (run algo.train(...) yourself.)")


if __name__ == "__main__":
    _selftest()
