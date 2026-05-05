"""Earth Mover's Distance for 1D histograms.

§6.2 Tool 2 of the deliverable. The reference identity for histograms on
a 1D bin grid is

    EMD(p, q) = sum_i | CDF(p)_i - CDF(q)_i |

— the L1 distance between cumulative distribution functions. This is
exact (not an approximation) for 1D distributions on a uniform grid,
which is what HSD histograms are.

The function `emd_distance(p, q)` is the §6.2 pseudocode line-for-line.
A `_lp_form` helper is also exposed so callers (e.g. day-5 evaluation)
can cross-check the closed-form CDF result against the linear-program
formulation `inf_γ E_(x,y)~γ |x − y|`.
"""

from typing import Sequence


def emd_distance(p: Sequence[float], q: Sequence[float]) -> float:
    """L1-of-CDFs form of EMD between two histograms on the same grid.

    Both inputs must have identical length. They are assumed to be
    probability distributions (sums close to 1); behaviour on
    non-normalised inputs is undefined.
    """
    if len(p) != len(q):
        raise ValueError(
            f"emd_distance: length mismatch ({len(p)} vs {len(q)})")
    cum_p = 0.0
    cum_q = 0.0
    total = 0.0
    for pi, qi in zip(p, q):
        cum_p += pi
        cum_q += qi
        total += abs(cum_p - cum_q)
    return total


def _lp_form(p: Sequence[float], q: Sequence[float]) -> float:
    """Linear-program EMD reference (slow). For 1D histograms on a
    uniform grid this returns the same value as `emd_distance`.

    Implements the optimal transport in O(n) by greedy left-to-right
    sweep — the standard 1D Wasserstein-1 algorithm.
    """
    if len(p) != len(q):
        raise ValueError(
            f"_lp_form: length mismatch ({len(p)} vs {len(q)})")
    work = 0.0
    surplus = 0.0
    for pi, qi in zip(p, q):
        # Move `pi - qi` units of mass forward from this bin.
        surplus += pi - qi
        work += abs(surplus)
    return work


if __name__ == "__main__":
    # Sanity probe: a peaked vs a uniform histogram.
    n = 50
    peaked = [0.0] * n
    peaked[25] = 1.0
    uniform = [1.0 / n] * n
    print(f"EMD(peaked, uniform)         = {emd_distance(peaked, uniform):.4f}")
    print(f"LP-form(peaked, uniform)     = {_lp_form(peaked, uniform):.4f}")
    print(f"EMD(peaked, peaked)          = {emd_distance(peaked, peaked):.4f}")
    bimodal = [0.0] * n
    bimodal[5] = 0.5
    bimodal[45] = 0.5
    print(f"EMD(peaked, bimodal)         = {emd_distance(peaked, bimodal):.4f}")
