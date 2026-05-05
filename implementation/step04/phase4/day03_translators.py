"""Action translators for off-tree opponent bets.

Three translators are provided, in increasing sophistication. Each takes:

- `b`: the off-tree bet fraction the opponent played (e.g. 0.7 of pot),
- `b_low`, `b_high`: the two nearest in-abstraction bet fractions
  (e.g. 0.5 and 1.0 of pot).

…and returns a `dict[in_abstraction_bet_fraction, probability_mass]`.
For deterministic translators the dict has a single key with mass 1.0;
for stochastic translators the mass splits between `b_low` and `b_high`.

The three translators (matching §3.2 / §6.4 of the deliverable):

1. `nearest_action(b, b_low, b_high)` — round to the closer endpoint on
   the linear bet-amount scale.
2. `probability_split_linear(b, b_low, b_high)` — assign mass linearly
   between `b_low` and `b_high`.
3. `pseudo_harmonic(b, b_low, b_high)` — Ganzfried & Sandholm 2013 form,
   interpolating in pot-fraction-odds space:

       f(b) = ((b_high − b) (1 + b_low)) /
              ((b_high − b_low) (1 + b))

   gives the probability mass placed on `b_low`; the remainder on
   `b_high`.

A unified entry point `translate(name, b, b_low, b_high)` dispatches by
translator name.
"""

from typing import Dict


def nearest_action(b: float, b_low: float, b_high: float) -> Dict[float, float]:
    """Deterministic: pick the endpoint at smaller absolute distance."""
    if b_high <= b_low:
        return {b_low: 1.0}
    if abs(b - b_low) <= abs(b - b_high):
        return {b_low: 1.0}
    return {b_high: 1.0}


def probability_split_linear(b: float, b_low: float,
                             b_high: float) -> Dict[float, float]:
    """Linear mixture between `b_low` and `b_high`."""
    if b_high <= b_low:
        return {b_low: 1.0}
    if b <= b_low:
        return {b_low: 1.0}
    if b >= b_high:
        return {b_high: 1.0}
    span = b_high - b_low
    p_high = (b - b_low) / span
    p_low = 1.0 - p_high
    return {b_low: p_low, b_high: p_high}


def pseudo_harmonic(b: float, b_low: float,
                    b_high: float) -> Dict[float, float]:
    """Ganzfried & Sandholm 2013 — pot-fraction-odds interpolation.

    Boundary handling: clamp `b` to `[b_low, b_high]`, return a single
    endpoint at the boundary.
    """
    if b_high <= b_low:
        return {b_low: 1.0}
    if b <= b_low:
        return {b_low: 1.0}
    if b >= b_high:
        return {b_high: 1.0}
    numerator = (b_high - b) * (1.0 + b_low)
    denominator = (b_high - b_low) * (1.0 + b)
    p_low = numerator / denominator
    p_low = max(0.0, min(1.0, p_low))
    return {b_low: p_low, b_high: 1.0 - p_low}


_DISPATCH = {
    "nearest": nearest_action,
    "probability_split": probability_split_linear,
    "pseudo_harmonic": pseudo_harmonic,
}


def translate(name: str, b: float, b_low: float,
              b_high: float) -> Dict[float, float]:
    """Dispatch by translator name. Names are 'nearest',
    'probability_split', and 'pseudo_harmonic'.
    """
    if name not in _DISPATCH:
        raise ValueError(
            f"unknown translator: {name!r} (valid: {list(_DISPATCH)})")
    return _DISPATCH[name](b, b_low, b_high)


if __name__ == "__main__":
    # Demonstrate each translator on a 0.7-pot bet between 0.5 and 1.0.
    test_b = 0.7
    test_low = 0.5
    test_high = 1.0
    print(f"Off-tree bet {test_b}, abstraction = ({test_low}, {test_high}):")
    for name in _DISPATCH:
        result = translate(name, test_b, test_low, test_high)
        formatted = ", ".join(f"{k}: {v:.4f}" for k, v in result.items())
        print(f"  {name:>20}: {{{formatted}}}")
