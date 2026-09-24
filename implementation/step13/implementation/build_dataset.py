"""
build_dataset.py -- raw PHH files -> parsed, validated, flat arrays in CACHE_ROOT (raw step 13,
Day 1 "complete data pipeline: raw data -> parse -> validate -> store structured records").

    python build_dataset.py --source IPN100            # all 2,081 files (~2.0 M hands)
    python build_dataset.py --source IPN100 --max-files 200
    python build_dataset.py --source PLURIBUS          # the 10,000 Pluribus hands

Output (outside the repo): CACHE_ROOT/<source>/{hands,seats,decs,pairs}.npz + players.json,
and results/build_<source>.json with the dataset statistics (hands, players, parse failures by
reason, resolution of showdowns, table-size distribution, hands-per-player quantiles).
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
import sys
import time
import tomllib
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CACHE_ROOT, IPN_DIRS, PLURIBUS_DIR, RESULTS  # noqa: E402
from features import DEC_COLS, DEC_F, PAIR_COLS, PAIR_F, SEAT_COLS, SEAT_F, hand_rows  # noqa: E402
from phh_parser import ParseError, parse_hand  # noqa: E402

RES_CODE = {"uncontested": 0, "showdown_known": 1, "showdown_unknown": 2}
_PID: dict = {}


def list_files(source: str) -> list[str]:
    if source == "PLURIBUS":
        def key(p):
            d = Path(p).parent.name
            m = re.match(r"(\d+)(b?)", d)
            return (int(m.group(1)), m.group(2), int(Path(p).stem))
        return sorted(glob.glob(str(PLURIBUS_DIR / "*" / "*.phh")), key=key)
    root = IPN_DIRS[source]
    files = glob.glob(str(root / "*" / "*.phhs"))
    return sorted(files, key=lambda p: int(re.search(r"_(\d+)-OBFUSCATED", p).group(1)))


def load_hands(path: str, source: str) -> list[dict]:
    with open(path, "rb") as fp:
        d = tomllib.load(fp)
    if source == "PLURIBUS":
        return [d]
    return list(d.values())


def player_ids(files: list[str], source: str) -> list[str]:
    seen: dict[str, int] = {}
    pat = re.compile(r"^players = \[(.*)\]$", re.M)
    for f in files:
        txt = open(f, encoding="utf-8").read()
        for m in pat.finditer(txt):
            for p in m.group(1).split(","):
                p = p.strip().strip("'\"")
                if p not in seen:
                    seen[p] = len(seen)
    return list(seen)


def _init(pid_map):
    global _PID
    _PID = pid_map


def work(args):
    fidx, path, source = args
    hands = load_hands(path, source)
    H, SI, SF, DI, DF, PI, PF, MW = [], [], [], [], [], [], [], []
    errs = collections.Counter()
    k = 0
    for order, raw in enumerate(hands):
        try:
            h = parse_hand(raw)
        except ParseError as e:
            errs[re.sub(r"[-\d.]+", "#", str(e))[:60]] += 1
            continue
        except Exception as e:  # noqa: BLE001 - count anything unexpected, keep going
            errs["EXC " + type(e).__name__] += 1
            continue
        pids = [_PID[p] for p in h.players]
        si, sf, di, df, pi, pf = hand_rows(h, pids, k)
        H.append([fidx, order, h.day, h.time_s, h.n, RES_CODE[h.resolution],
                  int(h.meta.get("implied_allin", False)), sum(1 for v in h.hole.values() if v)])
        SI += si; SF += sf; DI += di; DF += df; PI += pi; PF += pf
        MW += [h.n >= 3] * len(pi)
        k += 1
    hand_ids = [int(raw.get("hand", 0)) for raw in hands]
    out = {
        "H": np.array(H, dtype=np.int32).reshape(-1, 8),
        "SI": np.array(SI, dtype=np.int32).reshape(-1, len(SEAT_COLS)),
        "SF": np.array(SF, dtype=np.float32).reshape(-1, len(SEAT_F)),
        "DI": np.array(DI, dtype=np.int32).reshape(-1, len(DEC_COLS)),
        "DF": np.array(DF, dtype=np.float32).reshape(-1, len(DEC_F)),
        "hid": np.array([hand_ids[h[1]] for h in H], dtype=np.int64),
    }
    # aggregate pair rows within the file (tables persist, so this shrinks them a lot); a second
    # table keeps multiway tables only (>= 3 seats), for the format-matched collusion detector
    pi_all = np.array(PI, dtype=np.int64).reshape(-1, len(PAIR_COLS))
    pf_all = np.array(PF, dtype=np.float64).reshape(-1, len(PAIR_F))
    mw = np.array(MW, dtype=bool)
    for tag, sel in (("", slice(None)), ("m", mw)):
        pi, pf = pi_all[sel], pf_all[sel]
        key = pi[:, 0] * 10_000_000 + pi[:, 1]
        u, inv = np.unique(key, return_inverse=True)
        agg_i = np.zeros((len(u), pi.shape[1] - 2), dtype=np.int64)
        np.add.at(agg_i, inv, pi[:, 2:])
        agg_f = np.zeros((len(u), pf.shape[1]))
        np.add.at(agg_f, inv, pf)
        out["PK" + tag], out["PI" + tag], out["PF" + tag] = u, agg_i, agg_f
    return fidx, out, errs, len(hands)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="IPN100")
    ap.add_argument("--max-files", type=int, default=0)
    ap.add_argument("--procs", type=int, default=14)
    args, _ = ap.parse_known_args()
    t0 = time.time()
    files = list_files(args.source)
    if args.max_files:
        files = files[: args.max_files]
    names = player_ids(files, args.source)
    pid_map = {p: i for i, p in enumerate(names)}
    print(f"{len(files)} files, {len(names)} players ({time.time() - t0:.1f}s pre-pass)", flush=True)
    jobs = [(i, f, args.source) for i, f in enumerate(files)]
    parts = [None] * len(files)
    errs = collections.Counter()
    n_raw = 0
    with Pool(args.procs, initializer=_init, initargs=(pid_map,)) as pool:
        for k, (fidx, out, e, nr) in enumerate(pool.imap_unordered(work, jobs, chunksize=4)):
            parts[fidx] = out
            errs.update(e)
            n_raw += nr
            if (k + 1) % 200 == 0:
                print(f"  {k + 1}/{len(files)} files  {time.time() - t0:.0f}s", flush=True)
    # stitch with global hand indices
    offs = np.cumsum([0] + [len(p["H"]) for p in parts])
    H = np.concatenate([p["H"] for p in parts])
    hid = np.concatenate([p["hid"] for p in parts])
    SI = np.concatenate([p["SI"] for p in parts]); SF = np.concatenate([p["SF"] for p in parts])
    DI = np.concatenate([p["DI"] for p in parts]); DF = np.concatenate([p["DF"] for p in parts])
    so = np.concatenate([np.full(len(p["SI"]), offs[i], np.int32) for i, p in enumerate(parts)])
    do = np.concatenate([np.full(len(p["DI"]), offs[i], np.int32) for i, p in enumerate(parts)])
    SI[:, 0] += so
    DI[:, 0] += do
    out_dir = CACHE_ROOT / args.source
    out_dir.mkdir(parents=True, exist_ok=True)
    for tag in ("m", ""):
        PK = np.concatenate([p["PK" + tag] for p in parts])
        PIa = np.concatenate([p["PI" + tag] for p in parts])
        PFa = np.concatenate([p["PF" + tag] for p in parts])
        u, inv = np.unique(PK, return_inverse=True)
        PI = np.zeros((len(u), PIa.shape[1]), np.int64); np.add.at(PI, inv, PIa)
        PF = np.zeros((len(u), PFa.shape[1])); np.add.at(PF, inv, PFa)
        pa, pb = u // 10_000_000, u % 10_000_000
        if tag == "m":
            np.savez(out_dir / "pairs_mw.npz", a=pa, b=pb, I=PI, F=PF,
                     icols=np.array(PAIR_COLS[2:]), fcols=np.array(PAIR_F))
    np.savez(out_dir / "hands.npz", H=H, hid=hid,
             cols=np.array(["file", "order", "day", "time_s", "n", "res", "implied_allin", "n_known"]))
    np.savez(out_dir / "seats.npz", I=SI, F=SF, icols=np.array(SEAT_COLS), fcols=np.array(SEAT_F))
    np.savez(out_dir / "decs.npz", I=DI, F=DF, icols=np.array(DEC_COLS), fcols=np.array(DEC_F))
    np.savez(out_dir / "pairs.npz", a=pa, b=pb, I=PI, F=PF,
             icols=np.array(PAIR_COLS[2:]), fcols=np.array(PAIR_F))
    json.dump(names, open(out_dir / "players.json", "w"))
    json.dump([str(Path(f).relative_to(Path(f).parents[3])) for f in files],
              open(out_dir / "files.json", "w"))
    # ---------------- dataset statistics ----------------
    n_parsed = len(H)
    hpp = np.bincount(SI[:, 1], minlength=len(names))
    hpp = hpp[hpp > 0]
    stats = {
        "source": args.source, "files": len(files), "hands_raw": int(n_raw),
        "hands_parsed": int(n_parsed), "parse_rate": n_parsed / max(n_raw, 1),
        "parse_failures": dict(errs.most_common()),
        "players": int(len(hpp)), "seat_rows": int(len(SI)), "decisions": int(len(DI)),
        "pairs": int(len(u)),
        "table_size": {int(k): int(v) for k, v in zip(*np.unique(H[:, 4], return_counts=True))},
        "resolution": {name: int((H[:, 5] == c).sum()) for name, c in RES_CODE.items()},
        "implied_allin_hands": int(H[:, 6].sum()),
        "hands_with_known_cards": {int(k): int(v) for k, v in zip(*np.unique(H[:, 7], return_counts=True))},
        "days": {int(k): int(v) for k, v in zip(*np.unique(H[:, 2], return_counts=True))},
        "hands_per_player": {
            "mean": float(hpp.mean()), "median": float(np.median(hpp)),
            "q90": float(np.quantile(hpp, 0.9)), "max": int(hpp.max()),
            **{f"players_ge_{t}": int((hpp >= t).sum()) for t in (100, 500, 1000, 5000)},
            **{f"share_of_seats_ge_{t}": float(hpp[hpp >= t].sum() / hpp.sum()) for t in (100, 500, 1000)},
        },
        "action_classes": {int(k): int(v) for k, v in zip(*np.unique(DI[:, 9], return_counts=True))},
        "runtime_s": round(time.time() - t0, 1),
    }
    RESULTS.mkdir(exist_ok=True)
    json.dump(stats, open(RESULTS / f"build_{args.source}.json", "w"), indent=1)
    print(json.dumps({k: stats[k] for k in ("hands_raw", "hands_parsed", "parse_rate", "players",
                                             "decisions", "pairs", "runtime_s")}))
    print("failures:", dict(errs.most_common(8)))


if __name__ == "__main__":
    main()
