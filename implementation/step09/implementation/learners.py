"""
learners.py -- a compact discrete PPO learner + the Independent-Learners baseline.

WHAT THIS IS
------------
- `PPOLearner`: a small, self-contained discrete-action PPO (clipped surrogate objective,
  Schulman et al. 2017) -- the same objective as Step 01's PPO, rewritten for the tiny
  matrix/coop testbeds (one-step / short episodes) instead of Gym rollout loops. It is the
  building block MAPPO and the PSRO RL oracle reuse (raw step L349, L387).
- `IndependentLearners`: N PPO learners, one per agent, each treating the others as part of a
  fixed environment. This is the raw step's 🔴 HAND-CODE baseline (L350, L363-378) whose
  FAILURE MODES (non-stationarity, coordination failure) motivate everything else.

torch is imported lazily so modules that only need the numpy core (matrix_games, meta_nash,
goofspiel, psro) do not require it. Call `torch_available()` to decide whether to run the
neural experiments; `require_torch()` raises a helpful error if you instantiate a learner
without torch installed.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

_TORCH = None


def torch_available() -> bool:
    global _TORCH
    if _TORCH is None:
        try:
            import torch  # noqa: F401
            _TORCH = True
        except ImportError:
            _TORCH = False
    return _TORCH


def require_torch():
    if not torch_available():
        raise ImportError(
            "PyTorch is required for the neural learners (PPO/MADDPG/MAPPO/CommNet). "
            "Install it (`pip install torch`) or run only the numpy-based experiments "
            "(matrix games, PSRO on Kuhn/Leduc via the exact oracle, Goofspiel)."
        )
    import torch
    return torch


DEFAULT_PPO_CONFIG = {
    "hidden": 64,
    "lr": 3e-3,
    "clip": 0.2,
    "entropy_coef": 0.01,
    "value_coef": 0.5,
    "epochs": 4,
    "minibatch": 256,
    "max_grad_norm": 0.5,
    "seed": 0,
}


def _make_nets(torch, obs_dim, n_actions, hidden):
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


class PPOLearner:
    """Discrete-action PPO over vector observations. Value target = discounted return; for
    the one-step testbeds here the return is simply the immediate reward."""

    def __init__(self, obs_dim: int, n_actions: int, config: dict | None = None):
        torch = require_torch()
        self.torch = torch
        self.cfg = {**DEFAULT_PPO_CONFIG, **(config or {})}
        torch.manual_seed(self.cfg["seed"])
        self.obs_dim = obs_dim
        self.n_actions = n_actions
        self.net = _make_nets(torch, obs_dim, n_actions, self.cfg["hidden"])
        self.opt = torch.optim.Adam(self.net.parameters(), lr=self.cfg["lr"])

    # ---- acting ----
    def act(self, obs, greedy: bool = False):
        torch = self.torch
        x = torch.as_tensor(np.asarray(obs, dtype=np.float32)).unsqueeze(0)
        with torch.no_grad():
            logits, value = self.net(x)
            dist = torch.distributions.Categorical(logits=logits)
            action = torch.argmax(logits, dim=-1) if greedy else dist.sample()
            logp = dist.log_prob(action)
        return int(action.item()), float(logp.item()), float(value.item())

    def action_probs(self, obs):
        """Full action distribution at `obs` (numpy), for exact evaluation / mixtures."""
        torch = self.torch
        x = torch.as_tensor(np.asarray(obs, dtype=np.float32)).unsqueeze(0)
        with torch.no_grad():
            logits, _ = self.net(x)
            probs = torch.softmax(logits, dim=-1).squeeze(0).cpu().numpy()
        return probs

    # ---- learning ----
    def update(self, obs, actions, old_logps, returns):
        """One PPO update from a batch of transitions (numpy arrays).

        obs        : (T, obs_dim)
        actions    : (T,)  int
        old_logps  : (T,)  log pi_old(a|s) at collection time
        returns    : (T,)  value targets (= immediate reward for one-step episodes)
        Returns a dict of averaged losses AND the critic-target variance (used by the
        MADDPG-vs-independent critic-variance validation).
        """
        torch = self.torch
        obs_t = torch.as_tensor(np.asarray(obs, np.float32))
        act_t = torch.as_tensor(np.asarray(actions, np.int64))
        oldlp_t = torch.as_tensor(np.asarray(old_logps, np.float32))
        ret_t = torch.as_tensor(np.asarray(returns, np.float32))

        T = obs_t.shape[0]
        cfg = self.cfg
        p_loss = v_loss = ent = 0.0
        n = 0
        for _ in range(cfg["epochs"]):
            idx = np.random.permutation(T)
            for start in range(0, T, cfg["minibatch"]):
                mb = idx[start:start + cfg["minibatch"]]
                mb_t = torch.as_tensor(mb, dtype=torch.long)
                logits, values = self.net(obs_t[mb_t])
                dist = torch.distributions.Categorical(logits=logits)
                new_lp = dist.log_prob(act_t[mb_t])
                adv = ret_t[mb_t] - values.detach()
                adv = (adv - adv.mean()) / (adv.std() + 1e-8)
                ratio = torch.exp(new_lp - oldlp_t[mb_t])
                surr1 = ratio * adv
                surr2 = torch.clamp(ratio, 1 - cfg["clip"], 1 + cfg["clip"]) * adv
                policy_loss = -torch.min(surr1, surr2).mean()
                value_loss = ((values - ret_t[mb_t]) ** 2).mean()
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
        return {"policy_loss": p_loss / n, "value_loss": v_loss / n, "entropy": ent / n,
                "return_var": float(np.var(np.asarray(returns, np.float32)))}


class IndependentLearners:
    """N independent PPO learners. Each sees ONLY its own observation and reward; from each
    learner's view the others are a (non-stationary) part of the environment.

    Works on any env exposing: reset() -> (obs_list, global_state), step(actions) ->
    (reward, done, info), and attributes n_agents / n_actions / obs_dim. The shared reward is
    handed to every agent (team reward); swap in per-agent rewards for competitive tasks.
    """

    def __init__(self, env, config: dict | None = None):
        require_torch()
        self.env = env
        self.n_agents = env.n_agents
        self.learners = [PPOLearner(env.obs_dim, env.n_actions,
                                    {**(config or {}), "seed": (config or {}).get("seed", 0) + i})
                         for i in range(self.n_agents)]

    def train(self, episodes: int = 4000, batch_episodes: int = 256, seed: int = 0):
        """Collect batches of episodes and PPO-update each learner independently.
        Returns per-agent training histories (mean reward + critic-target variance)."""
        rng = np.random.default_rng(seed)
        history = {"reward": [], "critic_var": [[] for _ in range(self.n_agents)]}
        collected = 0
        while collected < episodes:
            buf = [{"obs": [], "act": [], "logp": [], "ret": []} for _ in range(self.n_agents)]
            ep_rewards = []
            for _ in range(batch_episodes):
                obs, _ = self.env.reset()
                acts, logps = [], []
                for i in range(self.n_agents):
                    a, lp, _v = self.learners[i].act(obs[i])
                    acts.append(a)
                    logps.append(lp)
                reward, _done, _info = self.env.step(acts)
                ep_rewards.append(reward)
                for i in range(self.n_agents):
                    buf[i]["obs"].append(np.asarray(obs[i], np.float32))
                    buf[i]["act"].append(acts[i])
                    buf[i]["logp"].append(logps[i])
                    buf[i]["ret"].append(reward)     # team reward, one-step return
            for i in range(self.n_agents):
                m = self.learners[i].update(np.array(buf[i]["obs"]), np.array(buf[i]["act"]),
                                            np.array(buf[i]["logp"]), np.array(buf[i]["ret"]))
                history["critic_var"][i].append(m["value_loss"])
            history["reward"].append(float(np.mean(ep_rewards)))
            collected += batch_episodes
        return history

    def greedy_reward(self, episodes: int = 2000) -> float:
        """Average team reward under greedy actions (evaluation)."""
        total = 0.0
        for _ in range(episodes):
            obs, _ = self.env.reset()
            acts = [self.learners[i].act(obs[i], greedy=True)[0] for i in range(self.n_agents)]
            total += self.env.step(acts)[0]
        return total / episodes


def _selftest():
    print("learners self-test")
    print("-" * 60)
    if not torch_available():
        print("[SKIP] torch not installed -> neural learners unavailable.")
        return
    from coop_env import CoopSignalEnv
    env = CoopSignalEnv(n_targets=3, comm=False, seed=0)
    il = IndependentLearners(env, {"seed": 0})
    print("  built IndependentLearners on CoopSignal(no comm): "
          f"n_agents={il.n_agents}, obs_dim={env.obs_dim}, n_actions={env.n_actions}")
    print("  (run il.train(...) yourself; without comm the listener is capped at ~1/K).")


if __name__ == "__main__":
    _selftest()
