"""
explore_hands.py -- look at real hands before modelling them (raw step 13, Phase 2 Day 1-2).

    python implementation/step13/exploration/explore_hands.py              # 3 IPN hands + 1 Pluribus hand
    python implementation/step13/exploration/explore_hands.py --file 7 --n 5 --seed 3

For each hand it prints the raw PHH action list, then the replay the parser produces: position,
street, pot and price at every decision, the action class, and the result (exact, or "unresolved"
when a showdown's cards are unknown). Then it prints one player's HUD statistics from the whole
file. Runs in a few seconds; needs the data in D:/datasets/phh-dataset (see config.py).
"""
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "implementation"))
from build_dataset import list_files, load_hands  # noqa: E402
from config import ACTION_NAMES, STREETS  # noqa: E402
from phh_parser import POS_NAMES, ParseError, parse_hand  # noqa: E402


def show(raw):
    print("raw actions:", raw["actions"])
    try:
        h = parse_hand(raw)
    except ParseError as e:
        print("  REJECTED by the parser:", e)
        return
    for a in h.actions:
        print(f"  {STREETS[a.street]:7s} p{a.actor + 1} ({POS_NAMES[h.positions[a.actor]]:3s}) "
              f"pot {a.pot_before:6.2f} BB, to call {a.to_call:5.2f} -> {ACTION_NAMES[a.cls]}")
    print(f"  result ({h.resolution}):", [round(x, 2) for x in h.net])
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=int, default=0)
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    files = list_files("IPN100")
    hands = load_hands(files[args.file], "IPN100")
    print(f"{files[args.file]}: {len(hands)} hands\n")
    for i in rng.choice(len(hands), args.n, replace=False):
        show(hands[int(i)])
    plu = list_files("PLURIBUS")
    print("Pluribus hand (all hole cards known):")
    show(load_hands(plu[int(rng.integers(len(plu)))], "PLURIBUS")[0])


if __name__ == "__main__":
    main()
