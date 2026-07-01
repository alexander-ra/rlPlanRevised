"""
The common opponent-model interface.

Every model -- type-based, continuous, consistent -- is something that consumes
observations and produces a *policy* (its current best guess of how the opponent plays).
That policy is all the rest of the system needs: the best-response code turns it into an
exploit, and exact_value scores how good that exploit really is.

    model.update(obs)          # fold in one observed hand
    model.observe(iterable)    # fold in many
    model.predicted_policy()   # -> policy(game, state) -> {action: prob}

Keeping the interface this small is what lets the tournament treat all three models
interchangeably.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class OpponentModel(ABC):
    name = "abstract"

    def __init__(self, game, hero: int):
        self.game = game
        self.hero = hero
        self.opp = 1 - hero

    @abstractmethod
    def update(self, obs):
        """Incorporate a single Observation."""

    def observe(self, observations):
        """Incorporate many observations (a buffer is iterable)."""
        for obs in observations:
            self.update(obs)
        return self

    @abstractmethod
    def predicted_policy(self):
        """Return the current estimate of the opponent's strategy as a policy callable."""

    def reset(self):
        """Forget all observations (override if the model keeps state)."""
        raise NotImplementedError
