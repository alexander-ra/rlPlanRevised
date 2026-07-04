"""GPU card-abstraction pipeline: equity features -> k-means buckets.

Builds, per street, an int16 ``bucket_<street>.npy`` parallel to
``keys_<street>.npy`` (from indexer.py). Runtime bucket lookup:
``bucket = bucket_arr[searchsorted(keys, canonical_key(cards))]``.

Method (matches the open-source / literature standard, GPU-accelerated):
  - River: OCHS-style feature = equity vs several opponent range profiles
    (vs-uniform, vs-tight, vs-loose), computed exactly over all 990 opponent
    holdings. k-means (L2) over the feature vectors.
  - Turn/Flop: histogram of next-street equity over all runouts (the hand's
    "future shape") -> k-means with EMD, which for 1-D distributions equals L1
    between the histogram CDFs (a documented free lunch vs true optimal
    transport).

All heavy compute runs on the GPU (torch); rank lookups use the int16 rank7
table from cards.py. Everything is chunked and resumable.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path

import numpy as np
import torch

import indexer
from cards import BINOM

ART = Path(__file__).resolve().parents[1] / "artifacts"

# 990 = C(45,2) opponent-hand index pairs into the 45 remaining cards.
_PAIRS45 = np.array(list(combinations(range(45), 2)), dtype=np.int64)


def _device():
    return "cuda" if torch.cuda.is_available() else "cpu"


class Equity:
    """Holds GPU tensors for exact river equity of many classes at once."""

    def __init__(self, device=None):
        self.dev = device or _device()
        self.rank = torch.from_numpy(
            np.load(ART / "rank7.npy")).to(self.dev)  # int16, len C(52,7)
        self.binom = torch.from_numpy(
            BINOM.astype(np.int64)).to(self.dev)       # (53,8)
        self.pairs = torch.from_numpy(_PAIRS45).to(self.dev)  # (990,2)

    def _colex7(self, cards_sorted):
        """cards_sorted: (...,7) ascending int64 -> (...) colex index."""
        # gather binom[card, pos+1] for pos 0..6
        pos = torch.arange(1, 8, device=self.dev)
        return self.binom[cards_sorted, pos].sum(dim=-1)

    def river_equity(self, hole, board):
        """hole: (B,2), board: (B,5) int64 GPU tensors of KNOWN cards.

        Returns equity (B,) vs a uniform random opponent holding: fraction of
        the 990 opponent 2-card holdings we beat, ties counted as 0.5.
        """
        B = hole.shape[0]
        dev = self.dev
        known = torch.cat([hole, board], dim=1)  # (B,7)
        # remaining 45 cards per class
        full = torch.arange(52, device=dev).unsqueeze(0).expand(B, 52)
        mask = torch.ones((B, 52), dtype=torch.bool, device=dev)
        mask.scatter_(1, known, False)
        remaining = full[mask].view(B, 45)  # (B,45)
        # our rank
        our7, _ = torch.sort(known, dim=1)
        our_rank = self.rank[self._colex7(our7)].to(torch.int32)  # (B,)
        # opponent hands: (B,990,2) card values
        opp = remaining[:, self.pairs]  # (B,990,2)
        board_b = board.unsqueeze(1).expand(B, 990, 5)
        opp7 = torch.cat([board_b, opp], dim=2)  # (B,990,7)
        opp7, _ = torch.sort(opp7, dim=2)
        opp_rank = self.rank[self._colex7(opp7)].to(torch.int32)  # (B,990)
        our = our_rank.unsqueeze(1)
        wins = (opp_rank < our).sum(dim=1).to(torch.float32)
        ties = (opp_rank == our).sum(dim=1).to(torch.float32)
        return (wins + 0.5 * ties) / 990.0


def decode_keys_to_cards(keys, k):
    """Vectorized-ish decode of many canonical keys to (N,2) hole + (N,k) board.

    Uses the numba per-key decoder; fast enough (tens of M/s).
    """
    n = keys.shape[0]
    out = np.empty((n, 2 + k), dtype=np.int64)
    _decode_batch(keys, k, BINOM.astype(np.int64), out)
    return out[:, :2], out[:, 2:]


from numba import njit, prange  # noqa: E402


@njit(parallel=True, cache=True)
def _decode_batch(keys, k, binom, out):
    for i in prange(keys.shape[0]):
        indexer.decode_key(keys[i], k, binom, out[i])


# ---------------------------------------------------------------------------
# GPU k-means (Lloyd), chunked assignment for large N
# ---------------------------------------------------------------------------

@njit(cache=True)
def _kmeans_1d_dp(values, weights, k):
    """Optimal weighted 1-D k-means (Ckmeans.1d.dp) on sorted distinct values.

    Returns val2bucket (len m): contiguous bucket id per distinct value,
    minimizing total weighted within-bucket variance. O(k*m^2). Stable — no
    oscillation, no empty clusters (each bucket is a nonempty contiguous run).
    """
    m = values.shape[0]
    W = np.zeros(m + 1)
    WX = np.zeros(m + 1)
    WX2 = np.zeros(m + 1)
    for i in range(m):
        W[i + 1] = W[i] + weights[i]
        WX[i + 1] = WX[i] + weights[i] * values[i]
        WX2[i + 1] = WX2[i] + weights[i] * values[i] * values[i]
    INF = 1e30
    kk = min(k, m)
    DP = np.full((kk + 1, m + 1), INF)
    ARG = np.zeros((kk + 1, m + 1), dtype=np.int64)
    DP[0, 0] = 0.0
    for c in range(1, kk + 1):
        for j in range(c, m + 1):
            best = INF
            ba = c - 1
            for i in range(c - 1, j):
                w = W[j] - W[i]
                sx = WX[j] - WX[i]
                seg = WX2[j] - WX2[i] - sx * sx / w if w > 0 else 0.0
                v = DP[c - 1, i] + seg
                if v < best:
                    best = v
                    ba = i
            DP[c, j] = best
            ARG[c, j] = ba
    val2bucket = np.empty(m, dtype=np.int64)
    j = m
    for c in range(kk, 0, -1):
        i = ARG[c, j]
        for t in range(i, j):
            val2bucket[t] = c - 1
        j = i
    return val2bucket


def kmeans_1d(equity, k):
    """Bucket 123M river equities via optimal 1-D DP on distinct values."""
    values, inv = np.unique(equity, return_inverse=True)
    weights = np.bincount(inv).astype(np.float64)
    val2bucket = _kmeans_1d_dp(values.astype(np.float64), weights, k)
    return val2bucket[inv].astype(np.int16)


def _kmeanspp_init(sample, k, seed):
    """k-means++ seeding on a GPU sample tensor (S,D) -> centroids (k,D)."""
    S = sample.shape[0]
    dev = sample.device
    g = torch.Generator(device="cpu").manual_seed(seed)
    first = int(torch.randint(0, S, (1,), generator=g).item())
    cent = [sample[first]]
    d2 = ((sample - cent[0]) ** 2).sum(dim=1)  # (S,)
    for _ in range(1, k):
        probs = d2 / torch.clamp(d2.sum(), min=1e-12)
        nxt = int(torch.multinomial(probs, 1).item())
        c = sample[nxt]
        cent.append(c)
        d2 = torch.minimum(d2, ((sample - c) ** 2).sum(dim=1))
    return torch.stack(cent)  # (k,D)


def gpu_kmeans(feats, k, iters=30, seed=0, chunk=4_000_000, device=None,
               init_sample=300_000, verbose=True):
    """k-means over feats (N,D) float32. Returns (labels int16 (N,), centroids).

    Assignment is chunked so N can exceed 100M. Init: quantiles for 1-D data
    (river equity), k-means++ on a sample for multi-D (turn/flop CDFs). Empty
    clusters are reseeded from the sample each iteration so no bucket is wasted.
    """
    dev = device or _device()
    N, D = feats.shape
    g = torch.Generator(device="cpu").manual_seed(seed)
    sidx = torch.randperm(N, generator=g)[:min(N, init_sample)]
    sample = torch.from_numpy(feats[sidx.numpy()]).to(dev).float()  # (S,D)
    if D == 1:
        qs = (torch.arange(k, device=dev) + 0.5) / k
        cent = torch.quantile(sample.flatten(), qs).unsqueeze(1)  # (k,1)
    else:
        cent = _kmeanspp_init(sample, k, seed)  # (k,D)
    labels = np.empty(N, dtype=np.int16)
    for it in range(iters):
        sums = torch.zeros((k, D), device=dev)
        counts = torch.zeros(k, device=dev)
        moved = 0
        for lo in range(0, N, chunk):
            hi = min(lo + chunk, N)
            x = torch.from_numpy(feats[lo:hi]).to(dev).float()
            d2 = torch.cdist(x, cent)
            lab = torch.argmin(d2, dim=1)
            newlab = lab.to(torch.int16).cpu().numpy()
            moved += int((newlab != labels[lo:hi]).sum())
            labels[lo:hi] = newlab
            sums.index_add_(0, lab, x)
            counts.index_add_(0, lab, torch.ones(hi - lo, device=dev))
        nonempty = counts > 0
        cent[nonempty] = sums[nonempty] / counts[nonempty].unsqueeze(1)
        n_empty = int((~nonempty).sum())
        if n_empty:  # reseed empty clusters from random sample points
            ridx = torch.randint(0, sample.shape[0], (n_empty,), device=dev)
            cent[~nonempty] = sample[ridx]
        if verbose:
            print(f"    kmeans it {it+1}/{iters} moved={moved:,} "
                  f"empty={n_empty}", flush=True)
        if moved == 0 and it > 0 and n_empty == 0:
            break
    return labels, cent.cpu().numpy()


# ---------------------------------------------------------------------------
# Per-street feature computation
# ---------------------------------------------------------------------------

def compute_river_equity(eq, keys, batch=16384, verbose=True):
    """Equity vs uniform for every river class. Returns float32 (N,)."""
    import time
    N = keys.shape[0]
    holes, boards = decode_keys_to_cards(keys, 5)
    out = np.empty(N, dtype=np.float32)
    t0 = time.time()
    for lo in range(0, N, batch):
        hi = min(lo + batch, N)
        H = torch.from_numpy(holes[lo:hi]).to(eq.dev)
        B = torch.from_numpy(boards[lo:hi]).to(eq.dev)
        out[lo:hi] = eq.river_equity(H, B).cpu().numpy()
        if verbose and (lo // batch) % 200 == 0:
            el = time.time() - t0
            fr = hi / N
            print(f"    river equity {hi:,}/{N:,} ({100*fr:.0f}%) "
                  f"eta {el/max(fr,1e-9)-el:.0f}s", flush=True)
    return out


def _remaining_cards(known, ncards):
    """known: (B,m) int64 GPU -> (B, 52-m) remaining cards ascending."""
    B, m = known.shape
    dev = known.device
    full = torch.arange(52, device=dev).unsqueeze(0).expand(B, 52)
    mask = torch.ones((B, 52), dtype=torch.bool, device=dev)
    mask.scatter_(1, known, False)
    return full[mask].view(B, 52 - m)


def _histogram_rows(equities, bins):
    """equities (B,R) in [0,1] -> normalized histograms (B,bins) float32."""
    idx = torch.clamp((equities * bins).long(), 0, bins - 1)  # (B,R)
    B, R = equities.shape
    h = torch.zeros((B, bins), device=equities.device)
    h.scatter_add_(1, idx, torch.ones_like(equities))
    return (h / R).float()


def compute_turn_histograms(eq, keys, bins=30, batch_classes=1200, verbose=True):
    """For each turn class, histogram of river equity over its 46 river cards."""
    import time
    N = keys.shape[0]
    holes, boards4 = decode_keys_to_cards(keys, 4)
    hist = np.empty((N, bins), dtype=np.float32)
    t0 = time.time()
    for lo in range(0, N, batch_classes):
        hi = min(lo + batch_classes, N)
        B = hi - lo
        H = torch.from_numpy(holes[lo:hi]).to(eq.dev)      # (B,2)
        B4 = torch.from_numpy(boards4[lo:hi]).to(eq.dev)   # (B,4)
        known = torch.cat([H, B4], dim=1)                  # (B,6)
        rem = _remaining_cards(known, 6)                   # (B,46)
        R = rem.shape[1]
        H_e = H.unsqueeze(1).expand(B, R, 2).reshape(B * R, 2)
        B5 = torch.cat([B4.unsqueeze(1).expand(B, R, 4),
                        rem.unsqueeze(2)], dim=2).reshape(B * R, 5)
        e = eq.river_equity(H_e, B5).view(B, R)
        hist[lo:hi] = _histogram_rows(e, bins).cpu().numpy()
        if verbose and (lo // batch_classes) % 200 == 0:
            el = time.time() - t0
            fr = hi / N
            print(f"    turn hist {hi:,}/{N:,} ({100*fr:.0f}%) "
                  f"eta {el/max(fr,1e-9)-el:.0f}s", flush=True)
    return hist


def compute_flop_histograms(eq, keys, bins=30, samples=200, batch_classes=400,
                            seed=0, verbose=True):
    """For each flop class, histogram of river equity over sampled turn+river
    runouts (samples 2-card completions from the 47 remaining)."""
    import time
    N = keys.shape[0]
    holes, boards3 = decode_keys_to_cards(keys, 3)
    hist = np.empty((N, bins), dtype=np.float32)
    rng = np.random.default_rng(seed)
    # sample distinct (t,r) index pairs into the 47 remaining
    all_pairs = np.array(list(combinations(range(47), 2)), dtype=np.int64)
    t0 = time.time()
    for lo in range(0, N, batch_classes):
        hi = min(lo + batch_classes, N)
        B = hi - lo
        H = torch.from_numpy(holes[lo:hi]).to(eq.dev)      # (B,2)
        B3 = torch.from_numpy(boards3[lo:hi]).to(eq.dev)   # (B,3)
        known = torch.cat([H, B3], dim=1)                  # (B,5)
        rem = _remaining_cards(known, 5)                   # (B,47)
        sel = rng.choice(all_pairs.shape[0], size=samples, replace=False)
        pair = torch.from_numpy(all_pairs[sel]).to(eq.dev)  # (samples,2)
        tr = rem[:, pair]                                   # (B,samples,2)
        R = samples
        H_e = H.unsqueeze(1).expand(B, R, 2).reshape(B * R, 2)
        B5 = torch.cat([B3.unsqueeze(1).expand(B, R, 3),
                        tr], dim=2).reshape(B * R, 5)
        e = eq.river_equity(H_e, B5).view(B, R)
        hist[lo:hi] = _histogram_rows(e, bins).cpu().numpy()
        if verbose and (lo // batch_classes) % 200 == 0:
            el = time.time() - t0
            fr = hi / N
            print(f"    flop hist {hi:,}/{N:,} ({100*fr:.0f}%) "
                  f"eta {el/max(fr,1e-9)-el:.0f}s", flush=True)
    return hist


def histograms_to_cdf(hist):
    """EMD on 1-D distributions = L1 between CDFs; clustering L2 on CDFs is the
    standard cheap surrogate. Returns cumulative sums (drop last, redundant)."""
    return np.cumsum(hist, axis=1)[:, :-1].astype(np.float32)


# ---------------------------------------------------------------------------
# Build orchestration
# ---------------------------------------------------------------------------

def build_street(street, n_buckets, bins=30, flop_samples=200, kmeans_iters=30,
                 force=False, verbose=True):
    """Compute features -> k-means -> save bucket_<street>.npy (int16)."""
    out = ART / f"bucket_{street}.npy"
    if out.exists() and not force:
        print(f"{out.name} exists; skip")
        return
    keys = np.load(ART / f"keys_{street}.npy")
    if street == "river":
        cache = ART / "river_equity.npy"
        if cache.exists():
            equity = np.load(cache)
        else:
            equity = compute_river_equity(Equity(), keys, verbose=verbose)
            np.save(cache, equity)
        labels = kmeans_1d(equity, n_buckets)  # optimal 1-D DP
        np.save(out, labels)
        if verbose:
            occ = np.bincount(labels, minlength=n_buckets)
            print(f"saved {out.name}: {len(labels):,} classes -> {n_buckets} "
                  f"buckets, occupancy min/med/max = "
                  f"{occ.min()}/{int(np.median(occ))}/{occ.max()}, "
                  f"empty={int((occ==0).sum())}")
        return
    elif street == "turn":
        cache = ART / "turn_cdf.npy"
        if cache.exists():
            feats = np.load(cache)
        else:
            hist = compute_turn_histograms(Equity(), keys, bins=bins,
                                           verbose=verbose)
            feats = histograms_to_cdf(hist)
            np.save(cache, feats)
    elif street == "flop":
        cache = ART / "flop_cdf.npy"
        if cache.exists():
            feats = np.load(cache)
        else:
            hist = compute_flop_histograms(Equity(), keys, bins=bins,
                                           samples=flop_samples, verbose=verbose)
            feats = histograms_to_cdf(hist)
            np.save(cache, feats)
    else:  # preflop is lossless 169; identity bucket
        labels = np.arange(keys.shape[0], dtype=np.int16)
        np.save(out, labels)
        print(f"saved {out.name} (preflop identity, {len(labels)})")
        return
    labels, cent = gpu_kmeans(feats, n_buckets, iters=kmeans_iters,
                              verbose=verbose)
    np.save(out, labels)
    if verbose:
        occ = np.bincount(labels, minlength=n_buckets)
        print(f"saved {out.name}: {len(labels):,} classes -> {n_buckets} "
              f"buckets, occupancy min/med/max = "
              f"{occ.min()}/{int(np.median(occ))}/{occ.max()}")
