"""
diversity.py -- population diversity metrics for the league (raw step 10 L347 [AI-ASSISTED],
L465-472; the "diversity problem" L96-108).

WHAT THIS IS
------------
Three complementary readouts of "how diverse is the population, really?" -- the question
AlphaStar's exploiters exist to keep answering "very":

  1. EFFECTIVE POPULATION SIZE -- how many agents actually matter. Two views: the count with
     meta-Nash weight above a threshold, and the participation ratio 1 / sum(w_i^2) (inverse
     Simpson index), which is smooth and penalises weight concentrating on a few agents.
  2. STRATEGY CLUSTERING -- group agents by BEHAVIOUR (their action distributions on a shared
     set of info sets). Many clusters = genuinely different strategies; one cluster = the
     population collapsed to a single style (the failure the league is designed to avoid).
  3. EXPLOIT COVERAGE -- for each agent, is there another agent that beats it by a margin
     (an "exploiter" for it)? Full coverage means no agent is left un-pressured.

Behaviour features come from Step 07's `materialize` (the exact per-info-set distributions), so
clustering reflects what the agents actually play. numpy-only; no sklearn dependency.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401  (step07 on sys.path)
from policies import materialize


def active_policies(mixture, threshold: float = 0.01) -> list:
    """Indices of agents with meta-Nash weight above `threshold` (raw step L102-105)."""
    mixture = np.asarray(mixture, dtype=float)
    return [int(i) for i, w in enumerate(mixture) if w > threshold]


def effective_population_size(mixture, threshold: float = 0.01) -> dict:
    """Effective diversity of the meta-Nash mixture."""
    mixture = np.asarray(mixture, dtype=float)
    s = mixture.sum()
    m = mixture / s if s > 0 else np.ones_like(mixture) / len(mixture)
    participation_ratio = float(1.0 / np.sum(m ** 2)) if np.sum(m ** 2) > 0 else 0.0
    return {
        "num_agents": int(len(mixture)),
        "num_active": len(active_policies(m, threshold)),
        "participation_ratio": round(participation_ratio, 3),   # inverse Simpson / "effective #"
        "active_threshold": threshold,
    }


def behavioral_features(game, policies) -> np.ndarray:
    """Feature matrix (n_policies, n_features): each policy's action-probability vector,
    concatenated over the UNION of info sets both seats can reach. Missing info sets for a
    policy contribute a uniform distribution (via the tabular fallback), so all rows share the
    same length and ordering."""
    # union of info sets across all policies, both seats, in a stable sorted order
    tables = []
    keys = set()
    for pol in policies:
        t = materialize(game, pol, 0)
        t.update(materialize(game, pol, 1))
        tables.append(t)
        keys.update(t.keys())
    ordered = sorted(keys)
    # collect the action ids present per info set (stable)
    action_ids = {}
    for k in ordered:
        acts = set()
        for t in tables:
            if k in t:
                acts.update(t[k].keys())
        action_ids[k] = sorted(acts)
    feats = []
    for t in tables:
        row = []
        for k in ordered:
            acts = action_ids[k]
            dist = t.get(k)
            if dist is None:
                row.extend([1.0 / len(acts)] * len(acts))
            else:
                total = sum(dist.get(a, 0.0) for a in acts) or 1.0
                row.extend([dist.get(a, 0.0) / total for a in acts])
        feats.append(row)
    return np.asarray(feats, dtype=float)


def strategy_clustering(features, distance_threshold: float = 0.3) -> dict:
    """Cluster policies by behaviour via single-linkage on L1 distance (union-find over edges
    below `distance_threshold`). Returns labels + number of clusters. Dependency-free."""
    X = np.asarray(features, dtype=float)
    n = X.shape[0]
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    dmax = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            d = float(np.mean(np.abs(X[i] - X[j]))) if X.shape[1] else 0.0
            dmax = max(dmax, d)
            if d < distance_threshold:
                union(i, j)
    roots = [find(i) for i in range(n)]
    remap = {r: c for c, r in enumerate(sorted(set(roots)))}
    labels = [remap[r] for r in roots]
    return {"labels": labels, "num_clusters": len(remap), "max_pairwise_distance": round(dmax, 4),
            "distance_threshold": distance_threshold}


def exploit_coverage(symmetric_payoff, margin: float = 0.25) -> dict:
    """For each agent i, is there some agent j that beats it by more than `margin`
    (M[j][i] > margin)? Returns per-agent coverage + the covered fraction (raw step L468-469)."""
    M = np.asarray(symmetric_payoff, dtype=float)
    n = M.shape[0]
    covered = []
    for i in range(n):
        beaten_by = [j for j in range(n) if j != i and M[j, i] > margin]
        covered.append(len(beaten_by) > 0)
    frac = float(np.mean(covered)) if n else 0.0
    return {"covered": covered, "fraction_covered": round(frac, 3), "margin": margin}


def analyze(game, policies, mixture, symmetric_payoff, agent_ids=None) -> dict:
    """Full diversity report combining the three metrics."""
    ids = list(agent_ids) if agent_ids is not None else list(range(len(policies)))
    feats = behavioral_features(game, policies)
    return {
        "ids": ids,
        "effective_population": effective_population_size(mixture),
        "clustering": strategy_clustering(feats),
        "exploit_coverage": exploit_coverage(symmetric_payoff),
    }


def _selftest():
    print("diversity self-test")
    print("-" * 60)
    # effective size on a peaked vs uniform mixture
    print(f"  eff-size peaked [0.9,0.05,0.05] = {effective_population_size([0.9, 0.05, 0.05])}")
    print(f"  eff-size uniform [1/3,1/3,1/3]   = {effective_population_size([1/3, 1/3, 1/3])}")
    # clustering on toy features: two identical + one different -> 2 clusters
    feats = np.array([[1.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    print(f"  clustering {feats.tolist()} -> {strategy_clustering(feats)}")
    # exploit coverage on a transitive ladder margin matrix
    M = np.array([[0.0, 0.5, 0.9], [-0.5, 0.0, 0.5], [-0.9, -0.5, 0.0]])
    print(f"  exploit_coverage(ladder) = {exploit_coverage(M)} "
          f"(PREDICT the top agent is uncovered -> fraction < 1)")


if __name__ == "__main__":
    _selftest()
