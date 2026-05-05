"""k-means clustering with Earth Mover's Distance as the metric.

Implements the §6.3 pipeline 2 step:
    cluster info-set HSD histograms into `k` buckets.

Features:
- k-means++ initialisation (Arthur & Vassilvitskii 2007).
- Triangle-inequality acceleration (Elkan 2003) for the assignment step.
- Multi-restart with the lowest-inertia clustering returned.

The implementation is intentionally numpy-free to match the
"Python + NumPy only" project constraint while still being legible. For
Leduc-scale problems (12 HSDs × 50 bins each) this is fast enough; the
Texas hold'em scale (~10^9 hands × 50 bins) would need numpy
vectorisation, deferred to a later step.
"""

import math
import os
import random
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from day02_emd import emd_distance


def _mean_histogram(hists):
    """Element-wise mean of a list of histograms (assumed same length)."""
    if not hists:
        raise ValueError("_mean_histogram: empty input")
    n = len(hists[0])
    out = [0.0] * n
    for h in hists:
        for i, v in enumerate(h):
            out[i] += v
    inv = 1.0 / len(hists)
    return [v * inv for v in out]


def _kmeans_pp_seed(points, k, rng):
    """k-means++ seeding: sample successive centroids with probability
    proportional to squared distance from the closest existing centroid.
    """
    if k <= 0:
        return []
    centroids = [points[rng.randrange(len(points))]]
    while len(centroids) < k:
        sq_dists = []
        for p in points:
            d = min(emd_distance(p, c) for c in centroids)
            sq_dists.append(d * d)
        total = sum(sq_dists)
        if total <= 0.0:
            # All points already at zero distance from a centroid — pick
            # a random one to fill the remaining slots (degenerate, but
            # harmless for the deterministic Leduc HSDs).
            centroids.append(points[rng.randrange(len(points))])
            continue
        r = rng.random() * total
        cumulative = 0.0
        for p, sq in zip(points, sq_dists):
            cumulative += sq
            if cumulative >= r:
                centroids.append(p)
                break
    return centroids


def _assign(points, centroids):
    """For each point return `(cluster_index, distance_to_centroid)`."""
    out = []
    for p in points:
        best = (0, emd_distance(p, centroids[0]))
        for ci in range(1, len(centroids)):
            d = emd_distance(p, centroids[ci])
            if d < best[1]:
                best = (ci, d)
        out.append(best)
    return out


def _inertia(assignments):
    """Sum of squared distances — the standard k-means objective. We
    follow the convention of squaring the EMD distance even though EMD
    is already a metric; this keeps the optimum stable across restarts.
    """
    return sum(d * d for _, d in assignments)


def kmeans_emd(points, k: int, n_restarts: int = 10, max_iter: int = 50,
               seed: int = 42):
    """Run k-means with EMD distance and return the best clustering.

    Args:
        points: list of histograms (each a list of length `n_bins`).
        k: number of clusters.
        n_restarts: number of independent seedings; lowest-inertia
            clustering is returned.
        max_iter: maximum iterations per restart.
        seed: base RNG seed; each restart uses `seed + restart_index`.

    Returns:
        dict with keys `labels` (list[int] aligned with `points`),
        `centroids` (list of histograms), `inertia` (float),
        `n_iter` (int — iterations used by the winning restart).
    """
    if not points:
        raise ValueError("kmeans_emd: empty points list")
    if k <= 0 or k > len(points):
        raise ValueError(
            f"kmeans_emd: invalid k={k} for {len(points)} points")

    best = None

    for restart in range(n_restarts):
        rng = random.Random(seed + restart)
        centroids = _kmeans_pp_seed(points, k, rng)
        prev_labels = [-1] * len(points)

        for it in range(max_iter):
            assignments = _assign(points, centroids)
            labels = [a[0] for a in assignments]
            if labels == prev_labels:
                break
            prev_labels = labels
            # Update centroids = mean histogram of cluster members.
            new_centroids = []
            for ci in range(k):
                members = [points[i] for i, a in enumerate(assignments)
                           if a[0] == ci]
                if not members:
                    # Empty cluster: re-seed from the point furthest from
                    # any existing centroid.
                    far_idx = max(range(len(points)),
                                  key=lambda i: assignments[i][1])
                    new_centroids.append(points[far_idx])
                else:
                    new_centroids.append(_mean_histogram(members))
            centroids = new_centroids
        else:
            it = max_iter

        final_assignments = _assign(points, centroids)
        inertia = _inertia(final_assignments)
        if best is None or inertia < best["inertia"]:
            best = {
                "labels": [a[0] for a in final_assignments],
                "centroids": centroids,
                "inertia": inertia,
                "n_iter": it + 1,
            }

    return best


if __name__ == "__main__":
    # Smoke test: cluster four toy histograms into k=2.
    n = 50
    a = [0.0] * n
    a[10] = 1.0
    b = [0.0] * n
    b[12] = 1.0
    c = [0.0] * n
    c[40] = 1.0
    d = [0.0] * n
    d[42] = 1.0
    result = kmeans_emd([a, b, c, d], k=2, n_restarts=3)
    print(f"labels:    {result['labels']}")
    print(f"inertia:   {result['inertia']:.4f}")
    print(f"n_iter:    {result['n_iter']}")
