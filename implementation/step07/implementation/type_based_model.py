"""
Type-based Bayesian opponent model.

The simplest useful model: assume the opponent is one of K known *types* (the zoo) and keep
a Bayesian posterior over which one. Each hand multiplies in the (partial-observability-
marginalized) likelihood of the opponent's actions under each type; we renormalize in log
space.

  posterior(t) proportional to  prior(t) * product over hands of  P(hand | type t)

Two ways to turn the posterior into a strategy estimate:
  - map_policy()        : just play the single most likely type (decisive, can whipsaw).
  - predicted_policy()  : Bayesian model averaging -- the posterior-weighted behavioral
                          mixture of the types (smoother, and what we exploit by default).

Strengths: data-efficient and fast when the opponent really is (close to) one of the types.
Weakness: if the true opponent is off-grid, the posterior collapses onto the *nearest*
type, which may still be a poor fit -- the continuous/consistent models address that.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import math

from bayesian_model import OpponentModel
from observation_buffer import candidate_deals
from inference import marginal_loglik, logsumexp
from policies import blend_policies, tabular_policy


class TypeBasedModel(OpponentModel):
    name = "type_based"

    def __init__(self, game, hero: int, types: dict, prior: dict | None = None,
                 track: bool = True):
        super().__init__(game, hero)
        self.type_names = list(types)
        self.type_policies = [types[n] for n in self.type_names]
        if prior is None:
            lp = -math.log(len(self.type_names))
            self.log_post = [lp for _ in self.type_names]
        else:
            total = sum(prior.values())
            self.log_post = [math.log(max(prior[n], 1e-300) / total) for n in self.type_names]
        self.track = track
        self.history = []  # list of posterior dicts after each update (for plotting)
        if track:
            self.history.append(self.posterior())

    # ---- inference ----
    def update(self, obs):
        cds = candidate_deals(self.game, obs)
        for i, policy in enumerate(self.type_policies):
            self.log_post[i] += marginal_loglik(self.game, self.opp, cds, obs.actions, policy)
        z = logsumexp(self.log_post)
        if z != -math.inf:
            self.log_post = [lp - z for lp in self.log_post]
        if self.track:
            self.history.append(self.posterior())

    # ---- readouts ----
    def posterior(self) -> dict:
        z = logsumexp(self.log_post)
        if z == -math.inf:
            n = len(self.type_names)
            return {name: 1.0 / n for name in self.type_names}
        return {name: math.exp(lp - z) for name, lp in zip(self.type_names, self.log_post)}

    def map_type(self) -> str:
        post = self.posterior()
        return max(post, key=post.get)

    def map_policy(self):
        return self.type_policies[self.type_names.index(self.map_type())]

    def predicted_policy(self):
        """Bayesian model averaging: the posterior-weighted behavioral mixture of types."""
        post = self.posterior()
        weights = [post[name] for name in self.type_names]
        return blend_policies(self.type_policies, weights)

    def reset(self):
        lp = -math.log(len(self.type_names))
        self.log_post = [lp for _ in self.type_names]
        self.history = [self.posterior()] if self.track else []


def _selftest():
    import random
    from engines import make_game
    from policies import play_hand
    from opponent_types import make_type_zoo

    print("type_based_model self-test")
    print("-" * 50)
    game = make_game("kuhn")
    zoo = make_type_zoo(game, include_nash=False)  # skip CFR for a fast smoke
    hero = 1
    opp = 0

    # Pick a hidden true type and see whether the posterior concentrates on it.
    truth = "TightPassive"
    rng = random.Random(7)
    model = TypeBasedModel(game, hero, zoo)
    opp_policy = zoo[truth]
    # Hero just plays uniformly here; we are only testing identification.
    from policies import uniform_policy
    hero_policy = uniform_policy()
    pols = [None, None]
    pols[opp] = opp_policy
    pols[hero] = hero_policy
    for _ in range(300):
        hand = play_hand(game, pols, rng.choice(game.deals()), rng)
        from observation_buffer import Observation
        # Build an observation from the hero's seat directly.
        opp_priv = hand.deal[opp] if opp in hand.revealed else None
        obs = Observation(hero, opp, hand.deal[hero], None, hand.actions, opp_priv,
                          hand.utilities[hero])
        model.update(obs)
    post = model.posterior()
    print(f"[kuhn] true type = {truth}")
    for name, p in sorted(post.items(), key=lambda kv: -kv[1]):
        print(f"   {name:16s} {p:6.3f}")
    print(f"[kuhn] MAP = {model.map_type()} (want {truth})")


if __name__ == "__main__":
    _selftest()
