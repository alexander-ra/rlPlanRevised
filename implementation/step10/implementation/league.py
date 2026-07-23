"""
league.py -- the PBT League for Leduc, inspired by AlphaStar's league (raw step 10 L207-231,
L408-438; Vinyals et al. 2019). The 🔴 HAND-CODE thesis-relevant mechanism of the step.

WHAT THIS IS
------------
A small population of neural agents that train against each other, with AlphaStar's three
agent ROLES that together solve the diversity problem naive self-play suffers from:

  - MAIN agents          : train against the WHOLE league (live agents + frozen history).
                           Goal: be robust to everything -> low exploitability.
  - MAIN EXPLOITERS       : train against the MAIN agents only. Goal: find the mains' specific
                           weaknesses -> create selection pressure that keeps mains honest
                           (this is "automated opponent modeling", the Contribution-#1 hook).
  - LEAGUE EXPLOITERS     : train against the whole league. Goal: expose anyone's weakness.

Plus the two population mechanisms:
  - FREEZING: periodically snapshot each main agent's CURRENT policy into a frozen historical
    population (so mains must keep beating their past selves -- a self-generated curriculum).
  - PBT (explore/exploit): periodically the weakest main agents COPY the weights of a strong
    main (`exploit`) and PERTURB their hyperparameters (`explore`) -- evolution applied to the
    training run (Jaderberg et al. 2017).

DESIGN CHOICES (documented so the runner understands them)
----------------------------------------------------------
- **Neural agents, exact evaluation.** Agents train by self-play rollouts (`ppo_agent.py`), but
  every reported number -- exploitability, the empirical meta-game, Elo, diversity -- is
  computed EXACTLY by extracting each net into a tabular policy (`leduc_rl.extract_tabular_policy`)
  and using Step 07's exact engine. Training is the only source of stochasticity.
- **Start-of-epoch snapshots as opponents.** Within an epoch, opponents are the tabular
  snapshots taken at the epoch's start (not the live, still-updating nets). This makes each
  agent's epoch a STATIONARY learning problem (cleaner PPO) and makes matchmaking, Elo and
  training all consistent with the same meta-matrix. Non-stationarity re-enters ACROSS epochs
  as everyone updates -- exactly the league dynamic.
- **PFSP matchmaking.** Opponents are sampled with prioritised fictitious self-play weights
  (Vinyals et al. 2019): harder opponents (those that beat the agent) get more weight.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Requires torch (guarded).
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401  (step09 + step07 on sys.path)
from best_response import nash_gap
from leduc_rl import extract_tabular_policy, make_net_policy  # noqa: F401  (make_net_policy: docs)
from ppo_agent import PPOAgent
import egta
import elo as elo_mod
import diversity as div_mod


DEFAULT_LEAGUE_CONFIG = {
    "num_main": 3,
    "num_main_exploiters": 2,
    "num_league_exploiters": 2,
    "hidden": 64,
    "base_lr": 3e-3,
    "base_entropy": 0.02,
    "episodes_per_epoch": 128,     # per agent, per epoch
    "epochs": 40,
    "freeze_every": 5,             # snapshot main agents every K epochs
    "pbt_every": 8,                # PBT explore/exploit cadence
    "pbt_fraction": 0.34,          # bottom fraction of mains replaced by mutated top mains
    "exploiter_reset_every": 0,    # 0 = never; else reinit exploiters every K epochs
    "pfsp_p": 1.0,                 # PFSP hardness exponent (1 -> weight ~ (1 - winrate))
    "elo_k": 16.0,
    "score_scale": 2.0,            # payoff spread for value->winrate logistic (Leduc pots)
    "seed": 0,
}


class LeducLeague:
    """AlphaStar-style league on Leduc. Build, then call `run(epochs)`."""

    def __init__(self, game, config: dict | None = None):
        self.game = game
        self.cfg = {**DEFAULT_LEAGUE_CONFIG, **(config or {})}
        self.rng = np.random.default_rng(self.cfg["seed"])
        self.agents = []          # list of {"id", "role", "agent": PPOAgent}
        self.frozen = []          # list of {"id", "policy" (tabular), "source", "epoch"}
        self.elo = {}             # persistent live-agent Elo ratings
        self.history = {"epoch": [], "main_exploitability": [], "min_main_exploitability": [],
                        "meta_nash_exploitability": [], "elo": [], "num_active": []}
        self._build_agents()

    # ---- construction ----
    def _new_agent(self, seed_offset: int) -> PPOAgent:
        hp = {"hidden": self.cfg["hidden"], "lr": self.cfg["base_lr"],
              "entropy_coef": self.cfg["base_entropy"]}
        return PPOAgent(hyperparams=hp, seed=self.cfg["seed"] + seed_offset)

    def _build_agents(self):
        off = 0
        for r in range(self.cfg["num_main"]):
            self.agents.append({"id": f"main_{r}", "role": "main",
                                "agent": self._new_agent(off)}); off += 1
        for r in range(self.cfg["num_main_exploiters"]):
            self.agents.append({"id": f"mexp_{r}", "role": "main_exploiter",
                                "agent": self._new_agent(off)}); off += 1
        for r in range(self.cfg["num_league_exploiters"]):
            self.agents.append({"id": f"lexp_{r}", "role": "league_exploiter",
                                "agent": self._new_agent(off)}); off += 1
        for entry in self.agents:
            self.elo[entry["id"]] = elo_mod.DEFAULT_RATING

    # ---- per-epoch population snapshot (tabular; exact-eval currency) ----
    def _snapshot(self):
        """Extract each live agent's current tabular policy. Returns parallel lists:
        (ids, roles, policies) for the LIVE agents, then the frozen population appended."""
        ids, roles, policies = [], [], []
        for entry in self.agents:
            ids.append(entry["id"])
            roles.append(entry["role"])
            policies.append(extract_tabular_policy(self.game, entry["agent"].probs_fn()))
        n_live = len(ids)
        for f in self.frozen:
            ids.append(f["id"]); roles.append("frozen"); policies.append(f["policy"])
        return ids, roles, policies, n_live

    # ---- PFSP matchmaking weights for one agent ----
    def _pfsp_weights(self, i: int, opp_indices: list, S: np.ndarray) -> np.ndarray:
        """Prioritised fictitious self-play: weight opponent j by (1 - P[i beats j])^p, so the
        opponents that beat agent i are trained against most. S[i][j] is i's expected score."""
        p = self.cfg["pfsp_p"]
        w = np.array([(1.0 - float(S[i, j])) ** p + 1e-6 for j in opp_indices], dtype=float)
        s = w.sum()
        return w / s if s > 0 else np.ones(len(opp_indices)) / max(len(opp_indices), 1)

    def _opponent_indices(self, i: int, role: str, roles: list, n_total: int) -> list:
        """Which opponents this role trains against (raw step L421-425)."""
        if role == "main_exploiter":
            return [j for j in range(n_total) if j != i and roles[j] == "main"]
        # main + league_exploiter: the whole league (live + frozen)
        return [j for j in range(n_total) if j != i]

    # ---- Elo (persistent over epochs, live agents only) ----
    def _update_elo(self, ids: list, S: np.ndarray, n_live: int):
        k = self.cfg["elo_k"]
        pairs = [(i, j) for i in range(n_live) for j in range(n_live) if i != j]
        self.rng.shuffle(pairs)
        for i, j in pairs:
            ra, rb = self.elo[ids[i]], self.elo[ids[j]]
            na, _ = elo_mod.update_pair(ra, rb, float(S[i, j]), k=k)
            self.elo[ids[i]] = na

    # ---- one training epoch ----
    def train_epoch(self, epoch: int) -> dict:
        ids, roles, policies, n_live = self._snapshot()
        n_total = len(ids)

        # exact meta-matrix over the whole population (matchmaking + Elo + freezing readouts)
        M = egta.symmetric_payoff_matrix(self.game, policies)
        S = egta.score_matrix(M, scale=self.cfg["score_scale"])

        # train each live agent against its role-appropriate, PFSP-weighted opponents
        ep = self.cfg["episodes_per_epoch"]
        for i, entry in enumerate(self.agents):
            opp_idx = self._opponent_indices(i, entry["role"], roles, n_total)
            if not opp_idx:
                continue
            weights = self._pfsp_weights(i, opp_idx, S)
            opp_policies = [policies[j] for j in opp_idx]
            entry["agent"].train_against(self.game, opp_policies, weights, ep, self.rng)

        # Elo progression from the (pre-training) live-live scores
        self._update_elo(ids, S, n_live)

        # main-agent exploitability (exact, on the pre-training snapshots)
        main_expl = [float(nash_gap(self.game, policies[i], policies[i])["nash_conv"])
                     for i, r in enumerate(roles[:n_live]) if r == "main"]

        # meta-Nash of the whole population + its exploitability
        mix = egta.meta_nash_mixture(M)
        meta_expl = egta.meta_nash_exploitability(self.game, policies, mix)
        num_active = len(div_mod.active_policies(mix))

        # record
        self.history["epoch"].append(epoch)
        self.history["main_exploitability"].append([round(v, 5) for v in main_expl])
        self.history["min_main_exploitability"].append(round(min(main_expl), 5) if main_expl else None)
        self.history["meta_nash_exploitability"].append(round(float(meta_expl), 5))
        self.history["elo"].append({a: round(self.elo[a], 1) for a in self.elo})
        self.history["num_active"].append(num_active)

        # freezing: snapshot each main agent into the historical population
        if self.cfg["freeze_every"] > 0 and (epoch + 1) % self.cfg["freeze_every"] == 0:
            for i, entry in enumerate(self.agents):
                if entry["role"] == "main":
                    self.frozen.append({"id": f"{entry['id']}#e{epoch}", "policy": policies[i],
                                        "source": entry["id"], "epoch": epoch})

        # PBT: weakest mains copy a strong main's weights and mutate hyperparameters
        if self.cfg["pbt_every"] > 0 and (epoch + 1) % self.cfg["pbt_every"] == 0:
            self._pbt_step()

        # optional exploiter reset (AlphaStar reinitialises exploiters to keep them fresh)
        if self.cfg["exploiter_reset_every"] > 0 and (epoch + 1) % self.cfg["exploiter_reset_every"] == 0:
            self._reset_exploiters(epoch)

        return {"epoch": epoch, "min_main_exploitability": self.history["min_main_exploitability"][-1],
                "meta_nash_exploitability": self.history["meta_nash_exploitability"][-1],
                "num_active": num_active, "num_frozen": len(self.frozen)}

    def _pbt_step(self):
        """Rank main agents by Elo; bottom `pbt_fraction` clone a top main + perturb hparams."""
        mains = [e for e in self.agents if e["role"] == "main"]
        if len(mains) < 2:
            return
        ranked = sorted(mains, key=lambda e: -self.elo[e["id"]])
        n_replace = max(1, int(round(self.cfg["pbt_fraction"] * len(mains))))
        top = ranked[:max(1, len(mains) - n_replace)]
        bottom = ranked[len(mains) - n_replace:]
        for weak in bottom:
            strong = top[int(self.rng.integers(len(top)))]
            weak["agent"].clone_from(strong["agent"])
            weak["agent"].perturb_hyperparams(self.rng)
            # inherit the strong agent's Elo as a starting point after the weight copy
            self.elo[weak["id"]] = 0.5 * (self.elo[weak["id"]] + self.elo[strong["id"]])

    def _reset_exploiters(self, epoch: int):
        for k, entry in enumerate(self.agents):
            if entry["role"] in ("main_exploiter", "league_exploiter"):
                entry["agent"] = self._new_agent(1000 + epoch * 17 + k)

    # ---- run + final report ----
    def run(self, epochs: int | None = None) -> dict:
        epochs = epochs if epochs is not None else self.cfg["epochs"]
        for e in range(epochs):
            self.train_epoch(e)
        return self.history

    def final_report(self) -> dict:
        """EGTA + diversity over the FINAL population (live + frozen)."""
        ids, roles, policies, n_live = self._snapshot()
        M = egta.symmetric_payoff_matrix(self.game, policies)
        mix = egta.meta_nash_mixture(M)
        egta_rep = egta.analyze_population(self.game, policies, ids)
        div_rep = div_mod.analyze(self.game, policies, mix, M, ids)
        return {
            "num_live": n_live, "num_frozen": len(self.frozen),
            "ids": ids, "roles": roles,
            "egta": egta_rep,
            "diversity": div_rep,
            "final_elo": {a: round(self.elo[a], 1) for a in self.elo},
        }


def _selftest():
    print("league self-test")
    print("-" * 60)
    from ppo_agent import torch_available
    if not torch_available():
        print("[SKIP] torch not installed -> league requires PPOAgent.")
        return
    from engines import make_game
    game = make_game("leduc")
    cfg = {"num_main": 2, "num_main_exploiters": 1, "num_league_exploiters": 1,
           "episodes_per_epoch": 32, "epochs": 3, "freeze_every": 2, "pbt_every": 2, "seed": 0}
    league = LeducLeague(game, cfg)
    league.run(epochs=3)
    print("  min-main-exploitability trajectory:", league.history["min_main_exploitability"])
    print("  meta-Nash exploitability trajectory:", league.history["meta_nash_exploitability"])
    print("  PREDICT: min-main-exploitability trends DOWN over more epochs; meta-Nash <= best "
          "individual (verify with more epochs -- 3 is only a smoke).")


if __name__ == "__main__":
    _selftest()
