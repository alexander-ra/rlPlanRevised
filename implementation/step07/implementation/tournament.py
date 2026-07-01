"""
The Step 07 tournament -- the experiment that produces the headline results.

It runs three studies on each configured game and writes everything to results/<game>_<cfg>.json:

  1. DETECTION   -- can each model figure out who it is playing? For the type-based model we
                    report the posterior on the true type and whether the MAP is correct;
                    for all models we report the mean total-variation distance between the
                    estimated and true opponent strategy (lower = better recovery).

  2. EXPLOITATION -- how much does best-responding to each model actually win, vs each
                    opponent type? Alongside every realized number we compute two EXACT,
                    analytical references: `nash_ev` (what equilibrium earns vs that
                    opponent) and `ceiling` (the exact best-response value -- the most that
                    is extractable). A good exploiter sits between them and climbs toward the
                    ceiling. (Crucially, these references are exact math, not simulated, so
                    they are the trustworthy yardstick for the simulated curves.)

  3. NON-STATIONARITY -- the opponent switches style mid-match. We compare an exploiter with
                    and without change-point detection; with detection it should recover
                    faster after the switch.

NOTHING HERE IS RUN BY THE AGENT. You run it:  python tournament.py --config smoke
Read implementation/README.md for how to interpret the output and the expected outcomes.
"""

from __future__ import annotations

import os
import json
import time
import random
import argparse

from engines import make_game
from policies import play_hand, materialize
from observation_buffer import ObservationBuffer
from opponent_types import make_type_zoo
from level_k import add_level_k_types
from type_based_model import TypeBasedModel
from continuous_model import ContinuousModel
from consistent_model import ConsistentModel
from adaptive_exploiter import AdaptiveExploiter, stationary, switching, exploitation_references
import config as cfgmod

# --- lightweight progress + 30s heartbeat --------------------------------------------
# The scale config runs for many minutes; without this, buffered stdout shows nothing until
# the end. `_set_status` prints a flushed, timestamped checkpoint line; a daemon thread
# re-prints the current status every HEARTBEAT_SEC so a long single step still pulses.
import sys
import threading

HEARTBEAT_SEC = 30
_T0 = time.time()
_STATUS = "starting"


def _elapsed() -> str:
    s = int(time.time() - _T0)
    return f"{s // 60:d}m{s % 60:02d}s"


def _set_status(msg: str):
    global _STATUS
    _STATUS = msg
    print(f"  [{_elapsed()}] {msg}", flush=True)


def _start_heartbeat(interval: int = HEARTBEAT_SEC):
    def _beat():
        while True:
            time.sleep(interval)
            print(f"  [{_elapsed()}] ... still working: {_STATUS}", flush=True)
    threading.Thread(target=_beat, daemon=True).start()


# --- resumable checkpointing ---------------------------------------------------------
# The scale run is long, so we persist partial results keyed by work-item. On restart the
# tournament skips items already in the checkpoint and continues where it left off. Results
# are flushed to disk every CHECKPOINT_SEC (and once more when each game finishes). The Nash
# CFR training is already disk-cached separately (nash._cache/), so it is not redone either.
CHECKPOINT_SEC = 300  # 5 minutes


class Checkpoint:
    def __init__(self, path: str, interval: int = CHECKPOINT_SEC):
        self.path = path
        self.interval = interval
        self.data: dict = {}
        self._last_flush = time.time()
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as fh:
                    self.data = json.load(fh)
                if self.data:
                    print(f"  [{_elapsed()}] resuming from checkpoint "
                          f"({len(self.data)} items done): {path}", flush=True)
            except Exception:
                self.data = {}

    def has(self, key: str) -> bool:
        return key in self.data

    def get(self, key: str):
        return self.data[key]

    def set(self, key: str, value, force_flush: bool = False):
        self.data[key] = value
        if force_flush or (time.time() - self._last_flush) >= self.interval:
            self.flush()

    def flush(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self.data, fh)
        os.replace(tmp, self.path)  # atomic replace
        self._last_flush = time.time()


# --- small metrics -------------------------------------------------------------------
def tv_distance(p: dict, q: dict) -> float:
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def mean_policy_tv(game, opp: int, est_policy, true_policy) -> float:
    est = materialize(game, est_policy, opp)
    true = materialize(game, true_policy, opp)
    isets = set(est) | set(true)
    if not isets:
        return 0.0
    return sum(tv_distance(est.get(i, {}), true.get(i, {})) for i in isets) / len(isets)


def build_model(name: str, game, hero: int, zoo: dict):
    if name == "type_based":
        return TypeBasedModel(game, hero, zoo)
    if name == "continuous":
        return ContinuousModel(game, hero, prior_strength=1.0)
    if name == "consistent":
        return ConsistentModel(game, hero)
    raise ValueError(f"unknown model {name!r}")


def collect_observations(game, hero, opp_policy, hands, rng, hero_policy):
    opp = 1 - hero
    buf = ObservationBuffer(game, hero)
    pols = [None, None]
    pols[hero] = hero_policy
    pols[opp] = opp_policy
    for _ in range(hands):
        buf.record(play_hand(game, pols, rng.choice(game.deals()), rng))
    return buf


# --- 1. detection --------------------------------------------------------------------
def detection_experiment(game, hero, zoo, cfg, ckpt) -> dict:
    opp = 1 - hero
    nash = zoo["Nash"]
    targets = list(zoo)  # well-specified: every type is also a candidate
    out = {}
    for ti, truth in enumerate(targets):
        key = f"{game.name}|detection|{truth}"
        if ckpt.has(key):
            out[truth] = ckpt.get(key)
            continue
        _set_status(f"{game.name} detection: {truth} ({ti + 1}/{len(targets)})")
        per_model = {m: {"posterior_true": [], "map_correct": [], "tv": []}
                     for m in cfg["models"]}
        for seed in cfg["seeds"]:
            rng = random.Random(1000 + seed)
            buf = collect_observations(game, hero, zoo[truth], cfg["detection_hands"],
                                       rng, hero_policy=nash)
            for mname in cfg["models"]:
                model = build_model(mname, game, hero, zoo)
                model.observe(buf)
                rec = per_model[mname]
                if isinstance(model, TypeBasedModel):
                    post = model.posterior()
                    rec["posterior_true"].append(post.get(truth, 0.0))
                    rec["map_correct"].append(1.0 if model.map_type() == truth else 0.0)
                rec["tv"].append(mean_policy_tv(game, opp, model.predicted_policy(), zoo[truth]))
        result = {m: {k: (sum(v) / len(v) if v else None) for k, v in d.items()}
                  for m, d in per_model.items()}
        out[truth] = result
        ckpt.set(key, result)
    return out


# --- 2. exploitation -----------------------------------------------------------------
def exploitation_experiment(game, hero, zoo, cfg, ckpt) -> dict:
    nash = zoo["Nash"]
    targets = list(zoo)
    out = {}
    for ti, truth in enumerate(targets):
        refs = exploitation_references(game, hero, zoo[truth], nash)
        per_model = {}
        for mname in cfg["models"]:
            key = f"{game.name}|exploitation|{truth}|{mname}"
            if ckpt.has(key):
                per_model[mname] = ckpt.get(key)
                continue
            _set_status(f"{game.name} exploitation: {truth} [{mname}] "
                        f"({ti + 1}/{len(targets)} types)")
            means = []
            rep_curve = None
            for seed in cfg["seeds"]:
                rng = random.Random(2000 + seed)
                model = build_model(mname, game, hero, zoo)
                ex = AdaptiveExploiter(
                    game, hero, model, nash_policy=nash,
                    refit_every=cfg["refit_every"], safety=cfg["safety"],
                    min_hands_before_exploit=cfg["min_hands_before_exploit"])
                res = ex.run(stationary(zoo[truth]), cfg["exploit_hands"], rng)
                means.append(res["mean_per_hand"])
                if rep_curve is None:
                    rep_curve = res["cumulative"]
            result = {
                "mean_per_hand": sum(means) / len(means),
                "mean_per_hand_by_seed": means,
                "cumulative_seed0": _downsample(rep_curve, 400),
            }
            per_model[mname] = result
            ckpt.set(key, result)
        out[truth] = {"references": refs, "models": per_model}
    return out


# --- 3. non-stationarity -------------------------------------------------------------
def nonstationarity_experiment(game, hero, zoo, cfg, ckpt) -> dict:
    ns = cfg["nonstationarity"]
    nash = zoo["Nash"]
    # first/second may be a plain type name or a per-game {game_name: type_name} map,
    # since the Kuhn and Leduc zoos use different type names.
    def _resolve(spec):
        return spec[game.name] if isinstance(spec, dict) else spec
    first, second = _resolve(ns["first"]), _resolve(ns["second"])
    seg = switching([(0, zoo[first]), (ns["switch_at"], zoo[second])])
    out = {"first": first, "second": second, "switch_at": ns["switch_at"],
           "total": ns["total"], "variants": {}}
    for use_cp in (False, True):
        variant = "changepoint" if use_cp else "static"
        key = f"{game.name}|nonstationarity|{variant}"
        if ckpt.has(key):
            out["variants"][variant] = ckpt.get(key)
            continue
        _set_status(f"{game.name} non-stationarity: {variant}")
        rng = random.Random(4242)
        model = ContinuousModel(game, hero)
        ex = AdaptiveExploiter(game, hero, model, nash_policy=nash,
                               refit_every=cfg["refit_every"], safety=cfg["safety"],
                               min_hands_before_exploit=cfg["min_hands_before_exploit"],
                               use_changepoint=use_cp)
        res = ex.run(seg, ns["total"], rng)
        after = res["profits"][ns["switch_at"]:]
        variant_result = {
            "mean_per_hand": res["mean_per_hand"],
            "mean_after_switch": (sum(after) / len(after)) if after else None,
            "changepoints": res["changepoints"],
            "cumulative": _downsample(res["cumulative"], 600),
        }
        out["variants"][variant] = variant_result
        ckpt.set(key, variant_result)
    return out


def _downsample(seq, k):
    """Keep at most k evenly spaced points (JSON/plot friendliness)."""
    n = len(seq)
    if n <= k:
        return list(seq)
    step = n / k
    return [seq[min(n - 1, int(i * step))] for i in range(k)]


# --- driver --------------------------------------------------------------------------
def run_game(game_name: str, cfg: dict, ckpt: "Checkpoint") -> dict:
    game = make_game(game_name)
    hero = cfg["hero"]
    print(f"\n=== {game_name.upper()} ({cfg['name']}) | hero=player {hero} ===", flush=True)
    t0 = time.time()

    _set_status(f"{game_name}: building type zoo (trains Nash via CFR; disk-cached)")
    zoo = make_type_zoo(game, nash_iters=cfg["nash_iters"][game_name])
    if cfg["include_level_k"]:
        add_level_k_types(zoo, game, cfg["level_k_levels"])
    print(f"  types: {list(zoo)}", flush=True)

    print("  [1/3] detection ...", flush=True)
    detection = detection_experiment(game, hero, zoo, cfg, ckpt)
    print("  [2/3] exploitation ...", flush=True)
    exploitation = exploitation_experiment(game, hero, zoo, cfg, ckpt)
    print("  [3/3] non-stationarity ...", flush=True)
    nonstat = nonstationarity_experiment(game, hero, zoo, cfg, ckpt)
    ckpt.flush()  # persist everything once the game is complete

    elapsed = time.time() - t0
    _print_summary(game_name, detection, exploitation, nonstat)
    print(f"  ({game_name} done in {elapsed:.1f}s)", flush=True)

    return {"game": game_name, "config": cfg["name"], "elapsed_sec": elapsed,
            "types": list(zoo), "detection": detection,
            "exploitation": exploitation, "nonstationarity": nonstat}


def _print_summary(game_name, detection, exploitation, nonstat):
    def cell(value, fmt):
        return format(value, fmt) if value is not None else "-"

    print(f"\n  -- detection ({game_name}) --")
    print(f"  {'true type':16s} {'tb post':>8s} {'tb MAP':>7s} {'tb TV':>7s} {'cont TV':>8s}")
    for truth, bym in detection.items():
        tb = bym.get("type_based", {})
        cont = bym.get("continuous", {})
        print(f"  {truth:16s} "
              f"{cell(tb.get('posterior_true'), '.2f'):>8s} "
              f"{cell(tb.get('map_correct'), '.2f'):>7s} "
              f"{cell(tb.get('tv'), '.3f'):>7s} "
              f"{cell(cont.get('tv'), '.3f'):>8s}")

    print(f"\n  -- exploitation: realized mean/hand vs exact ceiling ({game_name}) --")
    header = f"  {'true type':16s} {'nash_ev':>8s} {'ceiling':>8s}"
    model_names = list(next(iter(exploitation.values()))["models"].keys()) if exploitation else []
    for m in model_names:
        header += f" {m[:10]:>11s}"
    print(header)
    for truth, blk in exploitation.items():
        refs = blk["references"]
        line = f"  {truth:16s} {refs['nash_ev']:>8.3f} {refs['ceiling']:>8.3f}"
        for m in model_names:
            line += f" {blk['models'][m]['mean_per_hand']:>11.3f}"
        print(line)

    print(f"\n  -- non-stationarity ({game_name}): {nonstat['first']} -> {nonstat['second']}"
          f" at hand {nonstat['switch_at']} --")
    for variant, blk in nonstat["variants"].items():
        msa = blk["mean_after_switch"]
        print(f"  {variant:12s} mean/hand={blk['mean_per_hand']:+.3f} "
              f"after_switch={(f'{msa:+.3f}' if msa is not None else '-')} "
              f"changepoints={blk['changepoints']}")


def main():
    parser = argparse.ArgumentParser(description="Step 07 opponent-modeling tournament")
    parser.add_argument("--config", default="smoke", choices=list(cfgmod.CONFIGS))
    parser.add_argument("--game", default=None, help="override: run a single game")
    parser.add_argument("--no-plot", action="store_true")
    parser.add_argument("--fresh", action="store_true",
                        help="ignore any existing checkpoint and recompute from scratch")
    args = parser.parse_args()

    cfg = cfgmod.get_config(args.config)
    games = [args.game] if args.game else cfg["games"]

    os.makedirs(cfgmod.RESULTS_DIR, exist_ok=True)

    # Resumable checkpoint (kept in the git-ignored _cache/). Keyed by config so smoke and
    # scale don't collide; --game runs still share the config's checkpoint (they just fill
    # different keys). --fresh wipes it to force a clean recompute.
    ckpt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "_cache", f"tournament_{cfg['name']}.ckpt.json")
    if args.fresh and os.path.exists(ckpt_path):
        os.remove(ckpt_path)
        print(f"  --fresh: removed {ckpt_path}", flush=True)
    ckpt = Checkpoint(ckpt_path)
    _start_heartbeat()

    all_results = {}
    for game_name in games:
        result = run_game(game_name, cfg, ckpt)
        all_results[game_name] = result
        path = os.path.join(cfgmod.RESULTS_DIR, f"{game_name}_{cfg['name']}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
        print(f"  wrote {path}")

    if cfg["plot"] and not args.no_plot:
        try:
            import plotting
            plotting.plot_all(all_results, cfgmod.PLOTS_DIR)
            print(f"  wrote plots to {cfgmod.PLOTS_DIR}")
        except ImportError:
            print("  (matplotlib not installed -> skipping plots; results JSON is complete)")


if __name__ == "__main__":
    main()
