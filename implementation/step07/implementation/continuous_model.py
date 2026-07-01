"""
Continuous (non-parametric) Bayesian opponent model.

Instead of assuming a small menu of types, estimate the opponent's action probabilities
directly at *every* info set with an independent Dirichlet-multinomial:

    P(action a at info set I) = (count[I][a] + alpha) / (sum_b count[I][b] + |A| alpha)

This is just "count what they did, smoothed by a Dirichlet prior." It can represent any
strategy (no menu to be off-grid of), at the cost of needing more data per info set.

PARTIAL OBSERVABILITY. When the opponent's card is shown (showdown), we know exactly which
info sets they acted at -> add 1 to each. When the card is hidden (they folded), we do not
know which card-specific info set was visited, so we spread a *fractional* count across the
consistent cards, weighted by how likely each card is under the current estimate. Visiting
the data once in observation order is online stochastic EM; `refine_em()` does the proper
batched EM iterations if you want them.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from bayesian_model import OpponentModel
from observation_buffer import candidate_deals
from policies import replay
from inference import opp_logprob, logsumexp


class ContinuousModel(OpponentModel):
    name = "continuous"

    def __init__(self, game, hero: int, prior_strength: float = 1.0, prior_policy=None):
        super().__init__(game, hero)
        self.prior_strength = float(prior_strength)
        self.prior_policy = prior_policy  # None -> symmetric (uniform) Dirichlet prior
        self.counts: dict = {}            # info_set -> {action: float count}
        self.observations: list = []      # kept so refine_em() can reprocess

    # ---- helpers ----
    def _opp_decisions(self, deal, actions):
        return [(d.info_set, d.action)
                for d in replay(self.game, deal, actions) if d.player == self.opp]

    def _add(self, iset, action, weight):
        slot = self.counts.setdefault(iset, {})
        slot[action] = slot.get(action, 0.0) + weight

    def _alpha(self, game, state, legal):
        if self.prior_policy is None:
            a = self.prior_strength / len(legal)
            return {x: a for x in legal}
        pd = self.prior_policy(game, state)
        return {x: self.prior_strength * pd.get(x, 0.0) for x in legal}

    # ---- inference ----
    def update(self, obs):
        self.observations.append(obs)
        self._fold_in(obs, snapshot_policy=None)

    def _fold_in(self, obs, snapshot_policy):
        cds = candidate_deals(self.game, obs)
        if not cds:
            return
        if len(cds) == 1:
            for iset, action in self._opp_decisions(cds[0], obs.actions):
                self._add(iset, action, 1.0)
            return
        # Hidden card: soft counts weighted by P(card | data) under the current estimate.
        policy = snapshot_policy if snapshot_policy is not None else self.predicted_policy()
        lps = [opp_logprob(self.game, self.opp, d, obs.actions, policy) for d in cds]
        z = logsumexp(lps)
        if z == -float("inf"):
            weights = [1.0 / len(cds)] * len(cds)
        else:
            import math
            weights = [math.exp(lp - z) for lp in lps]
        for d, w in zip(cds, weights):
            if w <= 0.0:
                continue
            for iset, action in self._opp_decisions(d, obs.actions):
                self._add(iset, action, w)

    def refine_em(self, passes: int = 3):
        """Proper batched EM: repeatedly recompute soft counts from scratch using the
        latest estimate. Optional; improves the hidden-card estimates at extra cost."""
        for _ in range(passes):
            snapshot = self.predicted_policy()
            self.counts = {}
            for obs in self.observations:
                self._fold_in(obs, snapshot_policy=snapshot)
        return self

    # ---- readout ----
    def predicted_policy(self):
        counts = self.counts
        get_alpha = self._alpha

        def policy(game, state):
            legal = game.legal_actions(state)
            iset = game.info_set(state)
            alpha = get_alpha(game, state, legal)
            seen = counts.get(iset, {})
            numer = {a: seen.get(a, 0.0) + alpha[a] for a in legal}
            total = sum(numer.values())
            if total <= 0.0:
                p = 1.0 / len(legal)
                return {a: p for a in legal}
            return {a: numer[a] / total for a in legal}

        return policy

    def reset(self):
        self.counts = {}
        self.observations = []


def _selftest():
    import random
    from engines import make_game
    from policies import play_hand, uniform_policy
    from observation_buffer import Observation
    from opponent_types import make_type_zoo
    from best_response import exact_value

    print("continuous_model self-test")
    print("-" * 50)
    game = make_game("kuhn")
    hero, opp = 1, 0
    truth = make_type_zoo(game, include_nash=False)["LooseAggressive"]
    model = ContinuousModel(game, hero, prior_strength=1.0)
    rng = random.Random(11)
    pols = [None, None]
    pols[opp] = truth
    pols[hero] = uniform_policy()
    for _ in range(2000):
        hand = play_hand(game, pols, rng.choice(game.deals()), rng)
        opp_priv = hand.deal[opp] if opp in hand.revealed else None
        model.update(Observation(hero, opp, hand.deal[hero], None, hand.actions,
                                 opp_priv, hand.utilities[hero]))
    # The recovered bet frequency at an open node should be close to LooseAggressive's ~0.85.
    est = model.predicted_policy()
    s = game.root((1, 2))  # player 0 to act with the Jack, empty history
    dist = est(game, s)
    print(f"[kuhn] estimated P(BET | Jack, open) = {dist.get(1, 0.0):.3f} "
          f"(LooseAggressive ~0.85 minus eps-smoothing)")
    print(f"[kuhn] #info sets estimated = {len(model.counts)}")


if __name__ == "__main__":
    _selftest()
