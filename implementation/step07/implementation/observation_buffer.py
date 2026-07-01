"""
The observation buffer -- the modeler's memory, and the single place partial observability
is handled.

When the hero models the opponent, every hand yields:
  - the hero's own private card (always known),
  - the public board card if it was revealed (Leduc round 2; never in Kuhn),
  - the full public action sequence,
  - the opponent's private card ONLY if there was a showdown (a fold hides it).

The buffer stores these raw facts and exposes the two operations the models need:

  * candidate_deals(obs)            -> the deals consistent with what the hero saw. If the
                                       opponent's card was shown, this is a single deal; if
                                       the hand was folded out, it is every card the
                                       opponent could have held (the marginalization set).
  * opp_decisions_for_deal(obs, d)  -> the opponent's (info_set, action, legal_actions)
                                       decisions, reconstructed by replaying the public
                                       action sequence under a hypothesized deal `d`.

That second operation is the workhorse: because the action sequence is public, replaying it
with a guessed opponent card tells us exactly which opponent info sets a candidate strategy
would have been queried at -- which is what lets the likelihoods marginalize over the cards
we never got to see.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from collections import namedtuple

from policies import replay

Observation = namedtuple(
    "Observation",
    ["hero", "opp", "hero_private", "community", "actions", "opp_private", "hero_util"],
)


def candidate_deals(game, obs: "Observation") -> list:
    """Deals consistent with the hero's knowledge for one observation (free function so the
    models can use it without holding a buffer instance).

    If the opponent's card was revealed, both private cards (and the board) are pinned;
    otherwise we return every deal matching the hero's card and the known board -- the set
    the likelihoods marginalize over.
    """
    if obs.opp_private is not None:
        out = []
        for d in game.deals():
            if d[obs.hero] != obs.hero_private or d[obs.opp] != obs.opp_private:
                continue
            if obs.community is not None and game.community(d) != obs.community:
                continue
            out.append(d)
        return out
    return game.consistent_deals(obs.hero, obs.hero_private, obs.community)


class ObservationBuffer:
    """Records hands from `hero`'s perspective (modeling the opponent = 1 - hero)."""

    def __init__(self, game, hero: int):
        self.game = game
        self.hero = hero
        self.opp = 1 - hero
        self.observations: list = []

    # ---- recording ----
    def record(self, hand) -> Observation:
        opp_private = hand.deal[self.opp] if self.opp in hand.revealed else None
        community = self._public_board(hand)
        obs = Observation(
            hero=self.hero, opp=self.opp,
            hero_private=hand.deal[self.hero],
            community=community,
            actions=hand.actions,
            opp_private=opp_private,
            hero_util=hand.utilities[self.hero],
        )
        self.observations.append(obs)
        return obs

    def _public_board(self, hand):
        """The community card if it became public this hand, else None."""
        if not self.game.has_public_board:
            return None
        state = self.game.root(hand.deal)
        reached_round2 = getattr(state, "round", 0) >= 1
        for a in hand.actions:
            state = self.game.apply(state, a)
            if getattr(state, "round", 0) >= 1:
                reached_round2 = True
        return self.game.community(hand.deal) if reached_round2 else None

    # ---- partial-observability helpers ----
    def candidate_deals(self, obs: Observation) -> list:
        """Deals consistent with the hero's knowledge for this hand (see module-level
        `candidate_deals`)."""
        return candidate_deals(self.game, obs)

    def opp_decisions_for_deal(self, obs: Observation, deal):
        """The opponent's decisions [(info_set, action, legal_actions), ...] reconstructed
        by replaying the public actions under `deal`."""
        decisions = replay(self.game, deal, obs.actions)
        return [(d.info_set, d.action, d.legal_actions)
                for d in decisions if d.player == self.opp]

    # ---- conveniences ----
    def __len__(self):
        return len(self.observations)

    def __iter__(self):
        return iter(self.observations)

    def summary(self) -> dict:
        n = len(self.observations)
        showdowns = sum(1 for o in self.observations if o.opp_private is not None)
        return {
            "hands": n,
            "showdowns": showdowns,
            "folds_hiding_opp": n - showdowns,
            "showdown_rate": (showdowns / n) if n else 0.0,
        }


def _selftest():
    import random
    from engines import make_game
    from policies import play_hand, uniform_policy

    print("observation_buffer self-test")
    print("-" * 50)
    for name in ("kuhn", "leduc"):
        game = make_game(name)
        buf = ObservationBuffer(game, hero=1)  # model player 0
        rng = random.Random(3)
        pols = [uniform_policy(), uniform_policy()]
        for _ in range(200):
            buf.record(play_hand(game, pols, rng.choice(game.deals()), rng))
        s = buf.summary()
        print(f"[{name}] {s}")
        # For a showdown hand, candidate_deals must be a single deal; the opponent's
        # reconstructed decisions must be non-empty when the opponent actually acted.
        for o in buf:
            if o.opp_private is not None:
                cd = buf.candidate_deals(o)
                decs = buf.opp_decisions_for_deal(o, cd[0])
                print(f"   showdown example: #candidate_deals={len(cd)} "
                      f"(want 1), opp_decisions={len(decs)}")
                break


if __name__ == "__main__":
    _selftest()
