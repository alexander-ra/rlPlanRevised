"""
commnet.py -- a CommNet-style mean-field communication channel (raw step L354, L426-431).

WHAT THIS IS
------------
A learned, differentiable communication channel (Sukhbaatar et al. 2016) bolted onto the
cooperative CoopSignal task. Each agent encodes its observation to a hidden vector and emits a
MESSAGE; each agent then receives the MEAN of the others' messages as extra input to its
policy head. The whole thing is trained end-to-end (REINFORCE on the shared reward), so the
protocol is LEARNED, not designed -- the speaker discovers how to encode the target it alone
sees, and the listener learns to decode it.

The point is the raw step's communication validation (L456): with the channel ON the listener
can match the target (reward -> ~1.0); with it OFF the listener is capped at ~1/K (guessing).
`compare(...)` trains both and returns the gap.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Requires torch.
"""

from __future__ import annotations

import numpy as np

from learners import require_torch


def _build(torch, env, hidden, msg_dim):
    nn = torch.nn
    n_agents = env.n_agents

    encoders = nn.ModuleList([nn.Sequential(nn.Linear(env.obs_dim, hidden), nn.Tanh())
                              for _ in range(n_agents)])
    msg_heads = nn.ModuleList([nn.Linear(hidden, msg_dim) for _ in range(n_agents)])
    # policy head sees own hidden + the mean of others' messages
    act_heads = nn.ModuleList([nn.Linear(hidden + msg_dim, env.n_actions) for _ in range(n_agents)])
    return encoders, msg_heads, act_heads


class CommNet:
    def __init__(self, env, config: dict | None = None):
        torch = require_torch()
        self.torch = torch
        self.env = env
        cfg = {"hidden": 64, "msg_dim": None, "lr": 3e-3, "entropy_coef": 0.01, "seed": 0}
        cfg.update(config or {})
        if cfg["msg_dim"] is None:
            cfg["msg_dim"] = env.n_actions
        self.cfg = cfg
        torch.manual_seed(cfg["seed"])
        self.n_agents = env.n_agents
        self.msg_dim = cfg["msg_dim"]
        self.enc, self.msg, self.act = _build(torch, env, cfg["hidden"], self.msg_dim)
        self.opt = torch.optim.Adam(
            list(self.enc.parameters()) + list(self.msg.parameters()) + list(self.act.parameters()),
            lr=cfg["lr"])

    def _forward_logits(self, obs_list, comm: bool):
        """Return per-agent action logits given a batch of observations (list of (T,obs_dim))."""
        torch = self.torch
        hiddens = [self.enc[i](obs_list[i]) for i in range(self.n_agents)]
        messages = [self.msg[i](hiddens[i]) for i in range(self.n_agents)]
        logits = []
        for i in range(self.n_agents):
            if comm and self.n_agents > 1:
                others = [messages[j] for j in range(self.n_agents) if j != i]
                c = torch.stack(others, 0).mean(0)
            else:
                c = torch.zeros_like(messages[i])           # channel OFF: no information flows
            logits.append(self.act[i](torch.cat([hiddens[i], c], -1)))
        return logits

    def train(self, comm: bool = True, episodes: int = 8000, batch_episodes: int = 256):
        torch = self.torch
        history = {"reward": []}
        collected = 0
        while collected < episodes:
            O = [[] for _ in range(self.n_agents)]
            R = []
            AC = [[] for _ in range(self.n_agents)]
            for _ in range(batch_episodes):
                obs, _gs = self.env.reset()
                # sample actions from the current (no-grad) policy
                obs_t = [torch.as_tensor(np.asarray(obs[i], np.float32)).unsqueeze(0)
                         for i in range(self.n_agents)]
                with torch.no_grad():
                    logits = self._forward_logits(obs_t, comm)
                    acts = [int(torch.distributions.Categorical(logits=logits[i]).sample().item())
                            for i in range(self.n_agents)]
                reward, _done, _info = self.env.step(acts)
                for i in range(self.n_agents):
                    O[i].append(np.asarray(obs[i], np.float32))
                    AC[i].append(acts[i])
                R.append(reward)
            self._update(O, AC, R, comm)
            history["reward"].append(float(np.mean(R)))
            collected += batch_episodes
        return history

    def _update(self, O, AC, R, comm):
        torch = self.torch
        obs_t = [torch.as_tensor(np.array(O[i], np.float32)) for i in range(self.n_agents)]
        act_t = [torch.as_tensor(np.array(AC[i], np.int64)) for i in range(self.n_agents)]
        r_t = torch.as_tensor(np.array(R, np.float32))
        baseline = r_t.mean()                       # simple variance reduction
        adv = r_t - baseline
        logits = self._forward_logits(obs_t, comm)  # WITH grad -> message params get gradient
        loss = 0.0
        for i in range(self.n_agents):
            dist = torch.distributions.Categorical(logits=logits[i])
            logp = dist.log_prob(act_t[i])
            loss = loss - (logp * adv).mean() - self.cfg["entropy_coef"] * dist.entropy().mean()
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()

    def greedy_reward(self, comm: bool = True, episodes: int = 2000) -> float:
        torch = self.torch
        total = 0.0
        for _ in range(episodes):
            obs, _ = self.env.reset()
            obs_t = [torch.as_tensor(np.asarray(obs[i], np.float32)).unsqueeze(0)
                     for i in range(self.n_agents)]
            with torch.no_grad():
                logits = self._forward_logits(obs_t, comm)
                acts = [int(torch.argmax(logits[i], -1).item()) for i in range(self.n_agents)]
            total += self.env.step(acts)[0]
        return total / episodes


def compare(env_factory, episodes: int = 8000, batch_episodes: int = 256, seed: int = 0) -> dict:
    """Train CommNet with the channel ON and OFF on freshly-built envs; return final rewards.

    `env_factory` is a zero-arg callable returning a fresh CoopSignal env (so the two runs are
    independent). Prediction (raw step L456): comm ON reward >> comm OFF reward (~1/K).
    """
    on = CommNet(env_factory(), {"seed": seed})
    off = CommNet(env_factory(), {"seed": seed})
    h_on = on.train(comm=True, episodes=episodes, batch_episodes=batch_episodes)
    h_off = off.train(comm=False, episodes=episodes, batch_episodes=batch_episodes)
    r_on = on.greedy_reward(comm=True)
    r_off = off.greedy_reward(comm=False)
    return {"comm_on_reward": r_on, "comm_off_reward": r_off,
            "comm_helps": bool(r_on > r_off + 1e-3),
            "history_on": h_on["reward"], "history_off": h_off["reward"]}


def _selftest():
    print("commnet self-test")
    print("-" * 60)
    from learners import torch_available
    if not torch_available():
        print("[SKIP] torch not installed.")
        return
    from coop_env import CoopSignalEnv
    env = CoopSignalEnv(n_targets=4, comm=True, seed=0)
    net = CommNet(env, {"seed": 0})
    print(f"  built CommNet on CoopSignal(K=4): msg_dim={net.msg_dim}, n_agents={net.n_agents}")
    print("  (run commnet.compare(lambda: CoopSignalEnv(4)) to see comm ON vs OFF.)")


if __name__ == "__main__":
    _selftest()
