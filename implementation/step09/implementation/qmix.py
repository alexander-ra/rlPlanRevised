"""
qmix.py -- OPTIONAL: a minimal illustration of QMIX's monotonic-mixing / IGM property.

WHY THIS IS HERE (and why it is small)
--------------------------------------
QMIX (Rashid et al. 2018) is a Phase-3 READING paper and a mandatory Math Flag (monotonicity),
but it is NOT on the Phase-4 deliverables checklist. Rather than build and train a full QMIX,
this module demonstrates -- exactly and cheaply -- the ONE idea the Math Flag asks you to
internalize (targetedReading Flag B):

    if  dQ_tot/dQ_i >= 0 for all i  (a MONOTONE mixer),
    then argmax over the JOINT action of Q_tot decomposes into per-agent argmaxes of Q_i.

We build a monotone mixer (non-negative weights, à la QMIX's hypernetwork) and a NON-monotone
mixer (some negative weight), enumerate the joint action space, and check whether the joint
argmax equals the tuple of per-agent argmaxes. The monotone mixer always satisfies it; the
non-monotone one can violate it (the "sacrifice for the team" case QMIX cannot represent).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. numpy-only.
"""

from __future__ import annotations

import itertools

import numpy as np


def monotone_mix(q_values, weights, bias: float = 0.0) -> float:
    """Q_tot = sum_i w_i * Q_i + bias, with w_i >= 0 (monotone). `q_values` is per-agent Q_i."""
    w = np.asarray(weights, dtype=float)
    if np.any(w < 0):
        raise ValueError("monotone_mix requires non-negative weights")
    return float(np.dot(w, q_values) + bias)


def general_mix(q_values, weights, bias: float = 0.0) -> float:
    """Q_tot with ARBITRARY (possibly negative) weights -- may be non-monotone."""
    return float(np.dot(np.asarray(weights, float), q_values) + bias)


def igm_holds(q_tables, mixer, weights, bias: float = 0.0) -> bool:
    """Check the Individual-Global-Max (IGM) property for a mixer over per-agent Q tables.

    `q_tables[i]` is agent i's Q vector over its own actions. Returns True iff the joint
    argmax of Q_tot equals the tuple of per-agent argmaxes.
    """
    n_agents = len(q_tables)
    per_agent_argmax = tuple(int(np.argmax(q)) for q in q_tables)
    best_joint = None
    best_val = None
    for joint in itertools.product(*[range(len(q)) for q in q_tables]):
        qi = [q_tables[i][joint[i]] for i in range(n_agents)]
        val = mixer(qi, weights, bias)
        if best_val is None or val > best_val:
            best_val = val
            best_joint = joint
    return best_joint == per_agent_argmax


def demo() -> dict:
    """Two agents, 3 actions each. Show monotone mixing preserves IGM; a non-monotone one
    can break it."""
    rng = np.random.default_rng(0)
    q0 = rng.standard_normal(3)
    q1 = rng.standard_normal(3)
    q_tables = [q0, q1]

    mono_ok = igm_holds(q_tables, monotone_mix, weights=[0.7, 1.3])
    # a non-monotone mixer with a negative weight on agent 1 can invert its preference
    nonmono_ok = igm_holds(q_tables, general_mix, weights=[1.0, -1.0])
    return {
        "q0": q0.tolist(), "q1": q1.tolist(),
        "monotone_igm_holds": bool(mono_ok),
        "nonmonotone_igm_holds": bool(nonmono_ok),
    }


def _selftest():
    print("qmix monotonic-mixing illustration")
    print("-" * 60)
    d = demo()
    print(f"  per-agent Q0={np.round(d['q0'],3).tolist()} Q1={np.round(d['q1'],3).tolist()}")
    print(f"  monotone mixer -> IGM holds?      {d['monotone_igm_holds']}  (expect True)")
    print(f"  non-monotone mixer -> IGM holds?  {d['nonmonotone_igm_holds']}  "
          f"(expect False: joint argmax != per-agent argmaxes)")
    # the monotone case must always hold; assert it as a self-check
    assert d["monotone_igm_holds"], "monotone mixer must satisfy IGM"


if __name__ == "__main__":
    _selftest()
