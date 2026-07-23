"""
maddpg.py -- CTDE with a CENTRALIZED CRITIC and DECENTRALIZED ACTORS (raw step L351, L380-388).

WHAT THIS IS
------------
A discrete-action member of the MADDPG / centralized-critic family (Lowe et al. 2017). The
defining CTDE asymmetry (their Eq 5):

  - each agent's ACTOR pi_i(a_i | o_i) sees ONLY its own observation (decentralized execution);
  - a CENTRALIZED CRITIC Q(s, a_1, ..., a_N) sees the global state AND every agent's action
    (centralized training).

MADDPG's original actor update is the deterministic policy gradient; for DISCRETE actions we
use the equivalent stochastic-policy update with a COMA-style COUNTERFACTUAL baseline computed
FROM the centralized critic:

    advantage_i = Q(s, a_i, a_{-i}) - sum_{a'_i} pi_i(a'_i | o_i) Q(s, a'_i, a_{-i}),
    grad_i = E[ grad_theta_i log pi_i(a_i | o_i) * advantage_i ].

This keeps the exact CTDE structure (local actor, joint-action critic) while staying discrete
and differentiable-free on the actor side.

WHY WE ALSO BUILD AN INDEPENDENT CRITIC
---------------------------------------
The raw step's validation (L453) asks whether the centralized critic has LOWER VARIANCE than
independent critics. We therefore train, on the SAME data, a centralized critic Q(s, joint a)
and per-agent independent critics Q_i(o_i), and expose both loss curves. Prediction: because
Q(s, joint a) conditions on everything, its regression target (the reward) is near-
deterministic -> low residual; Q_i(o_i) cannot see the other agents, so identical o_i maps to
different rewards -> higher residual variance. `critic_variance_comparison()` returns both.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Requires torch.
"""

from __future__ import annotations

import numpy as np

from learners import require_torch


def _one_hot(idx, n, torch):
    v = torch.zeros(len(idx), n)
    v[torch.arange(len(idx)), idx] = 1.0
    return v


def _build(torch, env, hidden):
    nn = torch.nn
    n_agents = env.n_agents
    n_act = env.n_actions
    obs_dim = env.obs_dim
    gs_dim = env.global_state_dim

    actors = nn.ModuleList([
        nn.Sequential(nn.Linear(obs_dim, hidden), nn.Tanh(),
                      nn.Linear(hidden, hidden), nn.Tanh(), nn.Linear(hidden, n_act))
        for _ in range(n_agents)
    ])
    # centralized critic: global state + one-hot of ALL agents' actions -> scalar
    central = nn.Sequential(nn.Linear(gs_dim + n_agents * n_act, hidden), nn.Tanh(),
                            nn.Linear(hidden, hidden), nn.Tanh(), nn.Linear(hidden, 1))
    # independent critics: each sees only its own observation
    indep = nn.ModuleList([
        nn.Sequential(nn.Linear(obs_dim, hidden), nn.Tanh(), nn.Linear(hidden, 1))
        for _ in range(n_agents)
    ])
    return actors, central, indep


class MADDPG:
    """Discrete centralized-critic CTDE. See module docstring."""

    def __init__(self, env, config: dict | None = None):
        torch = require_torch()
        self.torch = torch
        self.env = env
        cfg = {"hidden": 64, "lr": 3e-3, "entropy_coef": 0.01, "seed": 0}
        cfg.update(config or {})
        self.cfg = cfg
        torch.manual_seed(cfg["seed"])
        self.n_agents = env.n_agents
        self.n_act = env.n_actions
        self.actors, self.central, self.indep = _build(torch, env, cfg["hidden"])
        params = list(self.actors.parameters()) + list(self.central.parameters())
        self.opt_ac = torch.optim.Adam(params, lr=cfg["lr"])
        self.opt_indep = torch.optim.Adam(self.indep.parameters(), lr=cfg["lr"])

    def _act_dist(self, agent, obs_t):
        return self.torch.distributions.Categorical(logits=self.actors[agent](obs_t))

    def act(self, obs, greedy: bool = False):
        torch = self.torch
        actions = []
        for i in range(self.n_agents):
            x = torch.as_tensor(np.asarray(obs[i], np.float32)).unsqueeze(0)
            with torch.no_grad():
                logits = self.actors[i](x)
                a = torch.argmax(logits, -1) if greedy else \
                    torch.distributions.Categorical(logits=logits).sample()
            actions.append(int(a.item()))
        return actions

    def train(self, episodes: int = 8000, batch_episodes: int = 256, seed: int = 0):
        torch = self.torch
        history = {"reward": [], "central_critic_loss": [], "indep_critic_loss": []}
        collected = 0
        while collected < episodes:
            O = [[] for _ in range(self.n_agents)]      # per-agent obs
            GS, A, R = [], [], []                        # global states, joint actions, rewards
            for _ in range(batch_episodes):
                obs, gs = self.env.reset()
                acts = self.act(obs)
                reward, _done, _info = self.env.step(acts)
                for i in range(self.n_agents):
                    O[i].append(np.asarray(obs[i], np.float32))
                GS.append(np.asarray(gs, np.float32))
                A.append(acts)
                R.append(reward)
            metrics = self._update(O, GS, A, R)
            history["reward"].append(float(np.mean(R)))
            history["central_critic_loss"].append(metrics["central_loss"])
            history["indep_critic_loss"].append(metrics["indep_loss"])
            collected += batch_episodes
        return history

    def _update(self, O, GS, A, R):
        torch = self.torch
        T = len(R)
        gs_t = torch.as_tensor(np.array(GS), dtype=torch.float32)
        r_t = torch.as_tensor(np.array(R), dtype=torch.float32)
        acts_t = torch.as_tensor(np.array(A), dtype=torch.long)          # (T, n_agents)
        obs_t = [torch.as_tensor(np.array(O[i]), dtype=torch.float32) for i in range(self.n_agents)]

        # joint one-hot action feature
        joint = torch.cat([_one_hot(acts_t[:, i], self.n_act, torch) for i in range(self.n_agents)], -1)

        # ---- centralized critic regression to the (one-step) return ----
        q = self.central(torch.cat([gs_t, joint], -1)).squeeze(-1)
        central_loss = ((q - r_t) ** 2).mean()

        # ---- independent critics regression to the same return ----
        indep_loss = 0.0
        indep_losses = []
        for i in range(self.n_agents):
            qi = self.indep[i](obs_t[i]).squeeze(-1)
            li = ((qi - r_t) ** 2).mean()
            indep_losses.append(li)
        indep_loss_t = torch.stack(indep_losses).mean()

        # ---- actor update: COMA-style counterfactual advantage from the centralized critic ----
        actor_loss = 0.0
        q_detached_all = self.central(torch.cat([gs_t, joint], -1)).squeeze(-1).detach()
        for i in range(self.n_agents):
            dist = self._act_dist(i, obs_t[i])
            logp = dist.log_prob(acts_t[:, i])
            # counterfactual baseline: expected Q if agent i re-sampled its action, others fixed
            probs = dist.probs.detach()                       # (T, n_act)
            baseline = torch.zeros(T)
            for a_alt in range(self.n_act):
                alt = acts_t.clone()
                alt[:, i] = a_alt
                joint_alt = torch.cat([_one_hot(alt[:, k], self.n_act, torch)
                                       for k in range(self.n_agents)], -1)
                q_alt = self.central(torch.cat([gs_t, joint_alt], -1)).squeeze(-1).detach()
                baseline = baseline + probs[:, a_alt] * q_alt
            advantage = (q_detached_all - baseline)
            actor_loss = actor_loss - (logp * advantage).mean() \
                - self.cfg["entropy_coef"] * dist.entropy().mean()

        ac_loss = central_loss + actor_loss
        self.opt_ac.zero_grad()
        ac_loss.backward()
        self.opt_ac.step()

        self.opt_indep.zero_grad()
        indep_loss_t.backward()
        self.opt_indep.step()

        return {"central_loss": float(central_loss.item()),
                "indep_loss": float(indep_loss_t.item())}

    def greedy_reward(self, episodes: int = 2000) -> float:
        total = 0.0
        for _ in range(episodes):
            obs, _ = self.env.reset()
            total += self.env.step(self.act(obs, greedy=True))[0]
        return total / episodes

    def critic_variance_comparison(self, history: dict) -> dict:
        """Summary for the raw-step L453 check: final centralized vs independent critic loss
        (a proxy for residual value-target variance). Prediction: central < independent."""
        return {
            "central_final_loss": float(history["central_critic_loss"][-1]),
            "indep_final_loss": float(history["indep_critic_loss"][-1]),
            "central_lower": bool(history["central_critic_loss"][-1] <
                                  history["indep_critic_loss"][-1]),
        }


def _selftest():
    print("maddpg self-test")
    print("-" * 60)
    from learners import torch_available
    if not torch_available():
        print("[SKIP] torch not installed.")
        return
    from coop_env import CoopSignalEnv
    env = CoopSignalEnv(n_targets=3, comm=False, seed=0)
    algo = MADDPG(env, {"seed": 0})
    print(f"  built MADDPG on CoopSignal: n_agents={algo.n_agents}, n_act={algo.n_act}")
    print("  (run algo.train(...) then algo.critic_variance_comparison(history) yourself.)")


if __name__ == "__main__":
    _selftest()
