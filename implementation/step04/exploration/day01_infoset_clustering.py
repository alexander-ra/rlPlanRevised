"""
Day 1 exploration — Leduc information-set taxonomy vs k-means.

Enumerates all 936 info sets of step03's Leduc engine, groups them two ways:

  (1) MANUAL taxonomy per the step04 raw plan (card-context only):
      - 3 pre-flop groups (private rank J / Q / K)
      - 3 post-flop-paired groups (JJ / QQ / KK)
      - 6 post-flop-non-paired groups (J|Q, J|K, Q|J, Q|K, K|J, K|Q)
      = 12 groups total, ignoring betting history.

  (2) K-MEANS clustering (k=12) on a 7-dim feature vector per info set that
      mixes card and betting features:
          [hand_strength, own_bet, opp_bet, pot_size,
           num_raises_total, facing_raise, round]
      Features are standardised before clustering.

Both groupings are plotted on the same (hand_strength, pot_size) axes with
a small jitter so all 936 points are individually visible. The axes are
directly interpretable: x = card-strength dimension, y = betting-commitment
dimension. The only difference between the two figures is the colour
mapping (manual vs k-means).

Why not PCA? Hand strength turns out to be uncorrelated with every betting
feature in this dataset (within each round, all three ranks are equally
represented at every betting history), so PCA puts zero loading on
hand_strength in the top two components. The explicit axes make the
card-vs-betting contrast readable.

Outputs:
  figures/day01_infosets_manual.png
  figures/day01_infosets_kmeans.png
  + a text summary of the cross-tabulation
"""

import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STEP03 = os.path.abspath(os.path.join(HERE, '..', '..', 'step03'))
sys.path.insert(0, STEP03)

from cfr.leduc_poker import ALL_DEALS, LeducState, NUM_CARDS

RANK_NAMES = {0: 'J', 1: 'Q', 2: 'K'}
FIG_DIR = os.path.join(HERE, 'figures')
os.makedirs(FIG_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Enumerate all 936 information sets
# ---------------------------------------------------------------------------

def enumerate_info_sets():
    """Return dict {info_set_key: representative_state}."""
    seen = {}

    def walk(state):
        if state.is_terminal():
            return
        key = state.get_info_set(state.current_player())
        if key not in seen:
            seen[key] = state
        for a in state.legal_actions():
            walk(state.apply_action(a))

    for deal in ALL_DEALS:
        walk(LeducState((deal[0], deal[1]), deal[2]))
    return seen


def parse_key(key: str):
    """'3:0|cr/' -> (private_rank=1, community_rank=0, history='cr/')

    Private/community are stored as card IDs (0..5) in the key; we strip
    suits by integer division. Returns (private_rank, community_rank_or_None,
    history).
    """
    pipe = key.index('|')
    prefix, history = key[:pipe], key[pipe + 1:]
    if ':' in prefix:
        c, comm = prefix.split(':')
        return int(c) // 2, int(comm) // 2, history
    return int(prefix) // 2, None, history


# ---------------------------------------------------------------------------
# 2. Manual taxonomy
# ---------------------------------------------------------------------------

def manual_group(private_rank, community_rank):
    if community_rank is None:
        return f"pre_{RANK_NAMES[private_rank]}"
    if private_rank == community_rank:
        return f"pair_{RANK_NAMES[private_rank]}"
    return f"post_{RANK_NAMES[private_rank]}|{RANK_NAMES[community_rank]}"


# Deterministic plotting order: pre-flop, pair, then non-paired
MANUAL_ORDER = [
    "pre_J", "pre_Q", "pre_K",
    "pair_J", "pair_Q", "pair_K",
    "post_J|Q", "post_J|K", "post_Q|J",
    "post_Q|K", "post_K|J", "post_K|Q",
]


# ---------------------------------------------------------------------------
# 3. Hand-strength tables (precomputed by direct enumeration)
# ---------------------------------------------------------------------------

def _showdown(my_card, opp_card, community):
    """Return +1 if `my_card` wins, 0 tie, -1 if opp wins. Uses rank pairing."""
    my_r, opp_r, comm_r = my_card // 2, opp_card // 2, community // 2
    my_pair = (my_r == comm_r)
    opp_pair = (opp_r == comm_r)
    if my_pair and not opp_pair:
        return 1
    if opp_pair and not my_pair:
        return -1
    # Either both pair (impossible — only 2 copies per rank) or neither
    if my_r > opp_r:
        return 1
    if my_r < opp_r:
        return -1
    return 0


def _compute_hand_strength_round0(private_rank):
    """P(win) + 0.5 * P(tie), averaging over opp card and community draws."""
    my_card = private_rank * 2  # arbitrary suit choice — outcome is rank-only
    wins = ties = total = 0
    for opp in range(NUM_CARDS):
        if opp == my_card:
            continue
        for cc in range(NUM_CARDS):
            if cc == my_card or cc == opp:
                continue
            r = _showdown(my_card, opp, cc)
            if r > 0:
                wins += 1
            elif r == 0:
                ties += 1
            total += 1
    return (wins + 0.5 * ties) / total


def _compute_hand_strength_round1(private_rank, community_rank):
    """P(win) + 0.5 * P(tie), averaging over opp card only (community fixed)."""
    my_card = private_rank * 2
    comm = community_rank * 2
    if comm == my_card:
        comm += 1  # take the other suit of that rank
    wins = ties = total = 0
    for opp in range(NUM_CARDS):
        if opp == my_card or opp == comm:
            continue
        r = _showdown(my_card, opp, comm)
        if r > 0:
            wins += 1
        elif r == 0:
            ties += 1
        total += 1
    return (wins + 0.5 * ties) / total


HAND_STRENGTH = {}
for _pr in range(3):
    HAND_STRENGTH[(_pr, None)] = _compute_hand_strength_round0(_pr)
    for _cr in range(3):
        HAND_STRENGTH[(_pr, _cr)] = _compute_hand_strength_round1(_pr, _cr)


# ---------------------------------------------------------------------------
# 4. Feature vector per info set
# ---------------------------------------------------------------------------

def features(state, key):
    pr, cr, _ = parse_key(key)
    player = state.current_player()
    opp = 1 - player
    hs = HAND_STRENGTH[(pr, cr)]
    own_bet = state.bets[player]
    opp_bet = state.bets[opp]
    pot = own_bet + opp_bet
    num_raises_total = sum(state.num_raises)
    facing_raise = 1 if state.bets[player] < state.bets[opp] else 0
    round_ind = state.round
    return np.array([hs, own_bet, opp_bet, pot,
                     num_raises_total, facing_raise, round_ind], dtype=float)


FEATURE_NAMES = ['hand_strength', 'own_bet', 'opp_bet',
                 'pot', 'num_raises', 'facing_raise', 'round']


# ---------------------------------------------------------------------------
# 5. K-means (numpy-only)
# ---------------------------------------------------------------------------

def kmeans(X, k, n_iter=200, seed=42):
    """k-means++ init, then Lloyd's algorithm. Returns (labels, centroids)."""
    rng = np.random.default_rng(seed)

    # k-means++ seeding
    centroids = np.empty((k, X.shape[1]))
    centroids[0] = X[rng.integers(len(X))]
    for i in range(1, k):
        d2 = np.min(((X[:, None, :] - centroids[:i]) ** 2).sum(-1), axis=1)
        probs = d2 / d2.sum()
        centroids[i] = X[rng.choice(len(X), p=probs)]

    for _ in range(n_iter):
        d = ((X[:, None, :] - centroids[None, :, :]) ** 2).sum(-1)
        labels = d.argmin(axis=1)
        new = np.stack([
            X[labels == c].mean(axis=0) if np.any(labels == c) else centroids[c]
            for c in range(k)
        ])
        if np.allclose(centroids, new, atol=1e-8):
            break
        centroids = new
    return labels, centroids


# ---------------------------------------------------------------------------
# 6. Plotting
# ---------------------------------------------------------------------------

def _plot_scatter(xy, labels, ordered_labels, title, out_path, cmap_name):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 8))
    n = len(ordered_labels)
    cmap = plt.get_cmap(cmap_name, n)

    for idx, g in enumerate(ordered_labels):
        mask = labels == g
        if not np.any(mask):
            continue
        ax.scatter(xy[mask, 0], xy[mask, 1],
                   color=cmap(idx), label=f"{g} (n={int(mask.sum())})",
                   s=30, alpha=0.65, edgecolors='white', linewidths=0.3)

    ax.set_xlabel('Hand strength (P(win) + 0.5·P(tie))  — jittered')
    ax.set_ylabel('Pot size (total chips committed)  — jittered')
    ax.set_title(title, fontsize=12)
    ax.legend(loc='center left', bbox_to_anchor=(1.01, 0.5),
              fontsize=8, frameon=False)
    ax.grid(alpha=0.25)
    ax.set_xlim(-0.05, 1.1)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  -> {out_path}")


# ---------------------------------------------------------------------------
# 7. Main
# ---------------------------------------------------------------------------

def main():
    print("Enumerating information sets ...")
    info_sets = enumerate_info_sets()
    keys = sorted(info_sets.keys())
    print(f"  total: {len(keys)}")

    print("\nHand-strength table (pre-computed):")
    print("  pre-flop:  J={:.3f}  Q={:.3f}  K={:.3f}".format(
        HAND_STRENGTH[(0, None)], HAND_STRENGTH[(1, None)], HAND_STRENGTH[(2, None)]))
    for pr in range(3):
        for cr in range(3):
            label = "pair" if pr == cr else "post"
            print(f"  {label:<5} {RANK_NAMES[pr]}|{RANK_NAMES[cr]}:  "
                  f"{HAND_STRENGTH[(pr, cr)]:.3f}")

    # Features + labels
    X = np.stack([features(info_sets[k], k) for k in keys])
    manual_labels = np.array([manual_group(*parse_key(k)[:2]) for k in keys])

    # Standardize for k-means
    mean, std = X.mean(0), X.std(0)
    std[std == 0] = 1.0
    X_std = (X - mean) / std

    # K-means (k=12 to match manual)
    print("\nRunning k-means (k=12, k-means++ init, seed=42) on standardised 7-feature space ...")
    km_labels, _ = kmeans(X_std, k=12, seed=42)
    km_labels_str = np.array([f"cluster_{c:02d}" for c in km_labels])

    # Explicit plot axes: hand_strength (x) and pot_size (y), with jitter so
    # overlapping info sets are individually visible. Info sets with
    # identical (card_context, betting_history) do not exist — the 936 are
    # all distinct — but many share one or both coordinates, hence jitter.
    rng = np.random.default_rng(0)
    x_raw = X[:, FEATURE_NAMES.index('hand_strength')]
    y_raw = X[:, FEATURE_NAMES.index('pot')]
    xy = np.stack([
        x_raw + rng.uniform(-0.025, 0.025, size=len(keys)),
        y_raw + rng.uniform(-0.30, 0.30, size=len(keys)),
    ], axis=1)

    # Summary
    print("\nManual-group counts:")
    for g in MANUAL_ORDER:
        n = int((manual_labels == g).sum())
        print(f"  {g:<12} {n:>4}")

    print("\nK-means cluster sizes:")
    for c in range(12):
        n = int((km_labels == c).sum())
        print(f"  cluster_{c:02d}   {n:>4}")

    print("\nCross-tabulation (manual rows × k-means columns, top clusters):")
    for g in MANUAL_ORDER:
        mask = manual_labels == g
        if not np.any(mask):
            continue
        sub = km_labels[mask]
        unique, counts = np.unique(sub, return_counts=True)
        order = counts.argsort()[::-1]
        parts = [f"c{unique[i]:02d}:{counts[i]}" for i in order[:5]]
        print(f"  {g:<12} -> {', '.join(parts)}")

    # Plots
    print("\nWriting figures ...")
    _plot_scatter(
        xy, manual_labels, MANUAL_ORDER,
        title=(f"Leduc info sets — manual taxonomy (12 card-context groups, n={len(keys)})\n"
               "x = hand strength, y = pot size (both jittered)"),
        out_path=os.path.join(FIG_DIR, 'day01_infosets_manual.png'),
        cmap_name='tab20',
    )
    _plot_scatter(
        xy, km_labels_str, [f"cluster_{c:02d}" for c in range(12)],
        title=(f"Leduc info sets — k-means (k=12) on standardised 7-feature space, n={len(keys)}\n"
               "Same axes as the manual plot — only the colour mapping differs"),
        out_path=os.path.join(FIG_DIR, 'day01_infosets_kmeans.png'),
        cmap_name='tab20',
    )

    print("\nDone.")


if __name__ == "__main__":
    main()
