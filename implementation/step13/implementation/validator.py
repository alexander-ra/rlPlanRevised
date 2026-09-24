"""
validator.py -- two independent validators and an error-injection test (raw step 13, Day 1
"DataValidator ... check for impossible states"; Validation: "Parser: successfully parse 100% of
well-formed hands. Validator catches injected errors (duplicate cards, negative stacks)").

Validators
----------
  own        phh_parser.parse_hand(strict=True): turn order, minimum raise, stack limits, board
             counts, actions after a fold / after the hand ended, truncated hands, duplicate or
             malformed cards, chip conservation and payoff agreement with `finishing_stacks`.
  pokerkit   pokerkit's rules engine (HandHistory -> State replay), run twice: with its warnings
             ignored (the library default) and with warnings promoted to errors.

The test
--------
Take clean hands (both validators accept them), inject exactly one error of each type, and count
how often each validator rejects the result. Also: pokerkit's payoffs vs the parser's net results on
every clean hand, as a cross-check of the parser's accounting.

    python validator.py            # IPN100 (2,000 hands) + Pluribus (2,000 hands), seed 0
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_dataset import list_files, load_hands  # noqa: E402
from config import RESULTS  # noqa: E402
from phh_parser import ParseError, parse_hand  # noqa: E402

KINDS = ["duplicate_card", "out_of_turn", "below_min_raise", "overbet_stack", "action_after_fold",
         "action_after_end", "truncated", "wrong_board_count", "unknown_player", "finishing_stacks"]


def own_check(raw) -> tuple[bool, str]:
    try:
        parse_hand(raw, strict=True)
        return True, ""
    except ParseError as e:
        return False, str(e)
    except Exception as e:  # noqa: BLE001
        return False, "EXC " + repr(e)[:80]


def _pk_fields(raw: dict) -> dict:
    """tomllib reads 0.50 as a float; pokerkit's own loader uses Decimal. Mixing the two makes
    pokerkit raise TypeError, so convert every numeric field the way pokerkit's loader would."""
    from decimal import Decimal

    def conv(x):
        return Decimal(repr(float(x))) if isinstance(x, float) else x

    out = dict(raw)
    for k in ("antes", "blinds_or_straddles", "starting_stacks", "finishing_stacks", "winnings"):
        if k in out:
            out[k] = [conv(x) for x in out[k]]
    if isinstance(out.get("min_bet"), float):
        out["min_bet"] = conv(out["min_bet"])
    return out


def pk_state(raw, warn_as_error: bool):
    from pokerkit import HandHistory
    with warnings.catch_warnings():
        warnings.simplefilter("error" if warn_as_error else "ignore")
        hh = HandHistory(**_pk_fields(raw))
        st = None
        for st in hh:
            pass
        if "finishing_stacks" in raw and st is not None and not st.status:
            fin = [float(x) for x in raw["finishing_stacks"]]
            if any(abs(float(a) - b) > 1e-6 for a, b in zip(st.stacks, fin)):
                raise ValueError("finishing_stacks disagree with pokerkit replay")
        return st


def pk_check(raw, warn_as_error: bool) -> tuple[bool, str]:
    try:
        pk_state(raw, warn_as_error)
        return True, ""
    except Exception as e:  # noqa: BLE001
        return False, type(e).__name__ + ": " + str(e)[:80]


def _player_action_idx(acts):
    # player actions only: skip dealer lines and show/muck ('p5 sm' may carry no cards)
    return [k for k, a in enumerate(acts) if not a.startswith("d ") and a.split()[1] != "sm"]


def _cards(s):
    return [s[i:i + 2] for i in range(0, len(s), 2)] if "?" not in s else []


def inject(raw: dict, kind: str, rng: np.random.Generator):
    """Return a copy of `raw` with one error of type `kind`, or None if it does not apply."""
    r = copy.deepcopy(raw)
    acts = r["actions"]
    n = len(r["players"])
    pidx = _player_action_idx(acts)
    finite = all(float(s) != float("inf") for s in r["starting_stacks"])
    if kind == "duplicate_card":
        db = [k for k, a in enumerate(acts) if a.startswith("d db")]
        if not db:
            return None
        known = []
        for a in acts:
            t = a.split()
            if a.startswith("d dh") and len(t) > 3:
                known += _cards(t[3])
            if a.startswith("d db"):
                known += _cards(t[2])
        k = int(rng.choice(db))
        cs = _cards(acts[k].split()[2])
        j = int(rng.integers(len(cs)))
        cand = [c for c in known if c != cs[j]]
        if not cand:
            return None
        cs[j] = str(rng.choice(cand))
        acts[k] = "d db " + "".join(cs)
    elif kind == "out_of_turn":
        if not pidx:
            return None
        k = int(rng.choice(pidx))
        t = acts[k].split()
        me = int(t[0][1:])
        other = int(rng.choice([p for p in range(1, n + 1) if p != me]))
        acts[k] = " ".join([f"p{other}"] + t[1:])
    elif kind == "below_min_raise":
        rec = parse_hand(raw, strict=True)
        cbr = [a for a in rec.actions if a.kind == "cbr"]
        if not cbr:
            return None
        a = cbr[int(rng.integers(len(cbr)))]
        # locate the action string: the m-th cbr in the list
        m = cbr.index(a)
        ks = [k for k in pidx if acts[k].split()[1] == "cbr"]
        k = ks[m]
        bb = rec.bb
        new_to = (a.cur_bet + 0.25) * bb if a.cur_bet > 0 else 0.5 * bb
        t = acts[k].split()
        acts[k] = f"{t[0]} cbr {new_to:.2f}"
    elif kind == "overbet_stack":
        if not finite:
            return None
        ks = [k for k in pidx if acts[k].split()[1] == "cbr"]
        if not ks:
            return None
        k = int(rng.choice(ks))
        t = acts[k].split()
        me = int(t[0][1:]) - 1
        acts[k] = f"{t[0]} cbr {float(r['starting_stacks'][me]) + float(max(r['blinds_or_straddles'])):g}"
    elif kind == "action_after_fold":
        folds = [k for k in pidx if acts[k].split()[1] == "f"]
        folds = [k for k in folds if any(j > k for j in pidx)]
        if not folds:
            return None
        k = int(rng.choice(folds))
        who = acts[k].split()[0]
        later = [j for j in pidx if j > k]
        j = int(rng.choice(later))
        acts.insert(j + 1, f"{who} cc")
    elif kind == "action_after_end":
        rec = parse_hand(raw, strict=True)
        if rec.resolution != "uncontested":
            return None
        w = [i for i in range(n) if not rec.folded[i]][0]
        last = max(pidx)
        acts.insert(last + 1, f"p{w + 1} cc")
    elif kind == "truncated":
        if len(pidx) < 2:
            return None
        last = max(pidx)
        del acts[last:]
    elif kind == "wrong_board_count":
        db = [k for k, a in enumerate(acts) if a.startswith("d db")]
        if not db:
            return None
        k = db[0]
        cs = _cards(acts[k].split()[2])
        acts[k] = "d db " + "".join(cs[:-1])
    elif kind == "unknown_player":
        if not pidx:
            return None
        k = int(rng.choice(pidx))
        t = acts[k].split()
        acts[k] = " ".join([f"p{n + 1}"] + t[1:])
    elif kind == "finishing_stacks":
        if "finishing_stacks" not in r:
            return None
        fs = list(r["finishing_stacks"])
        i, j = rng.choice(n, 2, replace=False)
        delta = float(max(r["blinds_or_straddles"]))
        fs[i] = fs[i] + delta
        fs[j] = fs[j] - delta
        r["finishing_stacks"] = fs
    return r


def run(source: str, n_hands: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    files = list_files(source)
    if source == "PLURIBUS":
        pick = rng.choice(len(files), n_hands, replace=False)
        raws = [load_hands(files[i], source)[0] for i in pick]
    else:
        pick = rng.choice(len(files), 40, replace=False)
        raws = []
        for i in pick:
            hs = load_hands(files[i], source)
            raws += [hs[j] for j in rng.choice(len(hs), n_hands // 40, replace=False)]
    t0 = time.time()
    clean, stats = [], {"own_reject": 0, "pk_reject": 0, "pk_strict_reject": 0}
    agree = {"compared": 0, "agree": 0, "max_abs_diff_bb": 0.0,
             "disagree_known_cards_mucked": 0, "disagree_other": 0}
    for raw in raws:
        ok1, _ = own_check(raw)
        ok2, _ = pk_check(raw, False)
        ok3, _ = pk_check(raw, True)
        stats["own_reject"] += not ok1
        stats["pk_reject"] += not ok2
        stats["pk_strict_reject"] += not ok3
        if ok1 and ok2 and ok3:
            clean.append(raw)
            rec = parse_hand(raw)
            st = pk_state(raw, False)
            if st is not None and not st.status and not rec.meta.get("implied_allin"):
                pay = [float(x) / rec.bb for x in st.payoffs]
                d = max(abs(a - b) for a, b in zip(pay, rec.net))
                agree["compared"] += 1
                agree["agree"] += int(d < 1e-6)
                agree["max_abs_diff_bb"] = max(agree["max_abs_diff_bb"], d)
                if d >= 1e-6:
                    # the parser evaluates showdowns from cards dealt face up ('d dh p2 JdKs')
                    # even when the show line is 'sm ????'; pokerkit then splits the pot
                    mucked = any(a.split()[1] == "sm" and "?" in a for a in raw["actions"]
                                 if not a.startswith("d "))
                    key = ("disagree_known_cards_mucked"
                           if rec.resolution == "showdown_known" and mucked else "disagree_other")
                    agree[key] += 1
    res = {"source": source, "sampled": len(raws), "clean": len(clean), **stats,
           "payoff_agreement": agree, "injection": {}}
    for kind in KINDS:
        cnt = {"applied": 0, "own": 0, "pk": 0, "pk_strict": 0, "own_msgs": {}}
        for raw in clean:
            bad = inject(raw, kind, rng)
            if bad is None:
                continue
            cnt["applied"] += 1
            ok1, m1 = own_check(bad)
            cnt["own"] += not ok1
            cnt["pk"] += not pk_check(bad, False)[0]
            cnt["pk_strict"] += not pk_check(bad, True)[0]
            if not ok1:
                key = m1.split(":")[0][:40]
                cnt["own_msgs"][key] = cnt["own_msgs"].get(key, 0) + 1
        for v in ("own", "pk", "pk_strict"):
            cnt[v + "_rate"] = cnt[v] / cnt["applied"] if cnt["applied"] else None
        res["injection"][kind] = cnt
        print(f"  {source} {kind:18s} n={cnt['applied']:5d} own={cnt['own_rate']} "
              f"pk={cnt['pk_rate']} pk_strict={cnt['pk_strict_rate']}", flush=True)
    res["runtime_s"] = round(time.time() - t0, 1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    args, _ = ap.parse_known_args()
    out = {"seed": args.seed, "runs": [run("IPN100", args.n, args.seed),
                                       run("PLURIBUS", args.n, args.seed)]}
    RESULTS.mkdir(exist_ok=True)
    json.dump(out, open(RESULTS / "validator.json", "w"), indent=1)


if __name__ == "__main__":
    main()
