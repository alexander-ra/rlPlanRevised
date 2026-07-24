"""
coalition_mappo.py -- coalition-aware multi-agent self-play for So Long Sucker (raw step 11
L467-499, L550). 🔴 HAND-CODE: the novel training signal of the step.

THE ONE NEW IDEA (raw L476-493)
-------------------------------
Replace the sparse winner-takes-all reward with a BLEND of sparse + Shapley-decomposed credit:

    R = alpha * sparse  +  (1 - alpha) * shapley_credit_centered

where `sparse` is +1 to the winner / -1/(N-1) to losers, and `shapley_credit_centered` is the
per-player Shapley credit (from `shapley.proxy_coalition_values` over the agents' value estimates),
centered to sum to zero so the blend stays zero-sum. This gives a learning signal about WHO each
agent was really helping -- the signal needed for coalition-aware play (raw L298-299).

  >>> NOTE (raw L462-464, honest caveat): the Shapley credit here uses the PROXY coalition value
  (a synergy-weighted sum of critic value estimates), NOT the true counterfactual win-probability
  (too expensive to roll out every game). It is a heuristic dense signal; the rigorous
  win-probability Shapley is used only for the validation harness on hand-set states. <<<

Returns are assigned at EPISODE granularity: every transition made by player p gets return R[p]
(a one-step return, mirroring Step 09's one-step MAPPO). Each agent is then PPO-updated on its own
transitions. Per-agent nets (raw L473); egocentric encoding would also permit sharing.

COMPARISON (raw L496-499): `train(use_shapley=False)` is the Sharan & Adak-style sparse baseline;
`train(use_shapley=True)` is this step's contribution. The primary metric is the COALITION SCORE
(via `coalition_detector`), not win rate (raw L560).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Requires torch.
"""

from __future__ import annotations

from dataclasses import replace

import numpy as np

import deps  # noqa: F401
from learners import torch_available
from sls_game import SLSGame, winner_rewards
from state_encoding import encode_state, legal_action_mask, action_index_to_move, obs_dim, action_dim
from sls_ppo import SLSPPOAgent, make_ppo_policy
from shapley import shapley_credit_from_values
from coalition_detector import mean_offdiagonal_coalition


class CoalitionAwareMAPPO:
    """A population of `n_players` PPO agents trained by SLS self-play with an optional
    Shapley-blended reward."""

    def __init__(self, n_players: int = 4, chips_per_player: int = 7, config: dict | None = None,
                 seed: int = 0):
        self.game = SLSGame(n_players=n_players, chips_per_player=chips_per_player)
        self.n_players = n_players
        od, ad = obs_dim(n_players), action_dim(n_players)
        self.agents = [SLSPPOAgent(od, ad, {**(config or {}), "seed": seed + i})
                       for i in range(n_players)]

    # ---- one self-play game, recording transitions --------------------------------------
    def _play_and_record(self, seed: int):
        game = self.game
        n = self.n_players
        rng = np.random.default_rng(seed)   # tie-break rng (unbiased deadlock winner)
        buf = [{"obs": [], "act": [], "logp": [], "mask": [], "val": []} for _ in range(n)]
        state = game.initial_state()
        while not game.is_terminal(state):
            legal = game.legal_actions(state)
            if not legal:
                nxt = game._next_with_chips([list(h) for h in state.hands], set(state.eliminated),
                                            state.current_player)
                if nxt is None:
                    break
                state = replace(state, current_player=nxt)
                continue
            p = state.current_player
            obs = encode_state(game, state)
            mask = legal_action_mask(game, state)
            idx, logp, val = self.agents[p].act(obs, mask, greedy=False)
            buf[p]["obs"].append(obs)
            buf[p]["act"].append(idx)
            buf[p]["logp"].append(logp)
            buf[p]["mask"].append(mask)
            buf[p]["val"].append(val)
            state = game.apply(state, action_index_to_move(game, state, idx), rng=rng)
        return state, buf

    def _blended_rewards(self, state, buf, use_shapley: bool, alpha: float,
                         credit_mode: str = "proxy", synergy: float = 0.1, cf_credit=None):
        """Per-player reward vector R = alpha*sparse + (1-alpha)*credit_centered (raw L476-493).

        `credit_mode`:
          - "proxy"          : Shapley credit from the critic value estimates recorded THIS game
                               (cheap, per-game; the default / README caveat L462-464).
          - "counterfactual" : `cf_credit`, a per-BATCH Shapley credit computed from actual
                               win-probability share under the current policies (see
                               `_counterfactual_credit`) -- the README's #1 suspected stronger signal.
        `synergy` tunes the proxy coalition-value synergy bonus (sweep axis)."""
        n = self.n_players
        sparse = winner_rewards(n, state.winner)
        if not use_shapley:
            return sparse
        if credit_mode == "counterfactual":
            credit_centered = cf_credit if cf_credit is not None else np.zeros(n)
        else:
            # proxy agent values = mean recorded critic value per agent (0 if it never moved)
            agent_values = np.array([float(np.mean(buf[p]["val"])) if buf[p]["val"] else 0.0
                                     for p in range(n)])
            credit = shapley_credit_from_values(agent_values, synergy)   # sums to ~1
            credit_centered = credit - credit.mean()                     # center -> zero-sum blend
        return alpha * sparse + (1.0 - alpha) * credit_centered

    def _counterfactual_credit(self, n_rollouts: int, seed: int) -> np.ndarray:
        """Per-batch coalition credit = Shapley of v(S)=P(winner in S), estimated by rollouts from
        the initial state under the CURRENT (greedy) policies. Centered to sum to zero. This is
        the 'true win-probability-share' signal (vs the critic-value proxy); refreshed each batch
        as the policies improve, per the README's 'use the rollout value at lower frequency'."""
        from shapley import win_prob_coalition_values, shapley_credit
        s0 = self.game.initial_state()
        pols = self.policies(greedy=True)
        vals, _ = win_prob_coalition_values(self.game, s0, n_rollouts=n_rollouts, policies=pols,
                                            seed=seed, rotate_start=True)
        credit = shapley_credit(self.n_players, vals)
        return credit - credit.mean()

    # ---- training loop ------------------------------------------------------------------
    def train(self, n_games: int = 2000, batch_games: int = 128, use_shapley: bool = True,
              alpha: float = 0.3, seed: int = 0, credit_mode: str = "proxy",
              synergy: float = 0.1, cf_rollouts: int = 150):
        """Self-play for `n_games`, PPO-updating every `batch_games`. Returns a history dict with
        per-batch mean coalition score, mean winner reward, and losses.

        `credit_mode` ("proxy"|"counterfactual"), `synergy`, `cf_rollouts` feed the sweep
        (sweep.py): they select which coalition-credit signal shapes the reward and how strong it
        is. The counterfactual credit is refreshed once per batch under the current policies."""
        rng = np.random.default_rng(seed)
        n = self.n_players
        history = {"coalition_score": [], "value_loss": [], "win_counts": np.zeros(n),
                   "n_games": n_games, "use_shapley": use_shapley, "alpha": alpha,
                   "credit_mode": credit_mode, "synergy": synergy}
        batch = [{"obs": [], "act": [], "logp": [], "mask": [], "ret": []} for _ in range(n)]
        coal_scores = []
        games_since_update = 0
        cf_credit = None
        for g in range(n_games):
            if use_shapley and credit_mode == "counterfactual" and games_since_update == 0:
                cf_credit = self._counterfactual_credit(cf_rollouts, seed=seed + g + 1)
            state, buf = self._play_and_record(int(rng.integers(1 << 30)))
            R = self._blended_rewards(state, buf, use_shapley, alpha, credit_mode, synergy, cf_credit)
            if state.winner is not None and 0 <= state.winner < n:
                history["win_counts"][state.winner] += 1
            coal_scores.append(mean_offdiagonal_coalition(n, state.move_log))
            for p in range(n):
                k = len(buf[p]["act"])
                if k == 0:
                    continue
                batch[p]["obs"].extend(buf[p]["obs"])
                batch[p]["act"].extend(buf[p]["act"])
                batch[p]["logp"].extend(buf[p]["logp"])
                batch[p]["mask"].extend(buf[p]["mask"])
                batch[p]["ret"].extend([R[p]] * k)     # episode-level return per transition
            games_since_update += 1
            if games_since_update >= batch_games:
                vloss = self._update_all(batch)
                history["coalition_score"].append(float(np.mean(coal_scores[-batch_games:])))
                history["value_loss"].append(vloss)
                batch = [{"obs": [], "act": [], "logp": [], "mask": [], "ret": []}
                         for _ in range(n)]
                games_since_update = 0
        history["mean_coalition_score"] = float(np.mean(coal_scores)) if coal_scores else 0.0
        return history

    def _update_all(self, batch):
        vlosses = []
        for p in range(self.n_players):
            if not batch[p]["act"]:
                continue
            stats = self.agents[p].update(
                np.array(batch[p]["obs"], np.float32), np.array(batch[p]["act"], np.int64),
                np.array(batch[p]["logp"], np.float32), np.array(batch[p]["mask"], bool),
                np.array(batch[p]["ret"], np.float32))
            vlosses.append(stats["value_loss"])
        return float(np.mean(vlosses)) if vlosses else 0.0

    # ---- evaluation ---------------------------------------------------------------------
    def policies(self, greedy: bool = True):
        """The trained agents as SLS policies (for play_game / EGTA)."""
        return [make_ppo_policy(self.agents[p], self.game, greedy=greedy) for p in range(self.n_players)]

    def win_rate_vs_random(self, hero: int = 0, n_games: int = 400, seed: int = 0):
        """Greedy hero (agent `hero`) vs random opponents; fraction of games hero wins."""
        from sls_game import play_game

        rng = np.random.default_rng(seed)

        def random_policy(g, s, r):
            legal = g.legal_actions(s)
            return legal[int(r.integers(len(legal)))]

        hero_pol = make_ppo_policy(self.agents[hero], self.game, greedy=True)
        wins = 0
        for _ in range(n_games):
            pols = [random_policy] * self.n_players
            pols[hero] = hero_pol
            final, _ = play_game(self.game, pols, seed=int(rng.integers(1 << 30)))
            wins += 1 if final.winner == hero else 0
        return wins / n_games


def _selftest():
    print("coalition_mappo self-test  (PREDICTIONS -- verify on a real run)")
    print("-" * 72)
    if not torch_available():
        print("[SKIP] torch not installed -> coalition-aware MAPPO unavailable.")
        return
    trainer = CoalitionAwareMAPPO(n_players=4, chips_per_player=5,
                                  config={"minibatch": 256, "epochs": 2}, seed=0)
    hist = trainer.train(n_games=16, batch_games=8, use_shapley=True, alpha=0.3, seed=0)
    print(f"  ran 16 self-play games; batches updated={len(hist['value_loss'])}; "
          f"mean coalition score={hist['mean_coalition_score']:.3f} "
          f"(a finite number; magnitude to verify)")
    print(f"  win_counts over training = {hist['win_counts'].astype(int).tolist()} "
          f"(sums to 16; distribution to verify)")


if __name__ == "__main__":
    _selftest()
