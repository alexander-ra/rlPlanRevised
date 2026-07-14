"""
Shared safe-exploitation metrics for the Step 08 exploration scripts.

These are thin wrappers over Step 07's EXACT best-response / expected-value code (imported
via `_bootstrap`). They define the two axes every exploration plot lives on:

  - EXPLOITATION  = EV of the hero strategy vs a specific (weak) opponent  -> the profit axis.
  - SAFETY        = the hero strategy's WORST-CASE EV (opponent best-responds), and how far
                    that sits below the game value -> the exploitability / risk axis.

Everything is computed exactly on the full tree (no sampling), so the numbers are ground
truth, not estimates -- ideal for building intuition on Kuhn/Leduc.

CONVENTION: `hero` is a seat (0 or 1). In zero-sum, the hero's worst-case value equals the
negative of the opponent's best-response value against the (fixed) hero strategy.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import _bootstrap  # noqa: F401  (side effect: puts Step 07 modules on sys.path)
from best_response import exact_value, best_response_value


def seat_order(hero: int, hero_policy, opp_policy):
    """Return (policy0, policy1) for exact_value given the hero's seat."""
    return (hero_policy, opp_policy) if hero == 0 else (opp_policy, hero_policy)


def game_value(game, nash_policy, hero: int = 0) -> float:
    """The equilibrium value FROM THE HERO'S SEAT (e.g. Kuhn P0 = -1/18)."""
    return exact_value(game, hero, *seat_order(hero, nash_policy, nash_policy))


def exploitation_ev(game, hero_policy, opp_policy, hero: int = 0) -> float:
    """Hero EV vs a fixed opponent -- the exploitation (profit) axis."""
    return exact_value(game, hero, *seat_order(hero, hero_policy, opp_policy))


def worst_case_ev(game, hero_policy, hero: int = 0) -> float:
    """Hero's WORST-CASE EV: the opponent best-responds to the fixed hero strategy.
    In zero-sum this is -(opponent's best-response value)."""
    opp = 1 - hero
    return -best_response_value(game, opp, hero_policy)


def exploitability(game, hero_policy, value_baseline: float, hero: int = 0) -> float:
    """How far the hero's worst-case sits BELOW the game value (>= 0; 0 means unexploitable
    relative to equilibrium). `value_baseline` is the seat's game value from `game_value`."""
    return value_baseline - worst_case_ev(game, hero_policy, hero)
