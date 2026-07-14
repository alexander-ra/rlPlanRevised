"""
A one-subgame peek: blueprint vs local exploitation (raw step L144-150).

The real-time exploitation idea (Pluribus/ReBeL, Step 06) is: play a Nash *blueprint*
everywhere, but at a specific decision point, re-solve LOCALLY assuming the opponent plays a
weak type -- deviating there while the rest of the tree stays Nash.

This exploration is the *lightweight* preview of that idea on Leduc. It does NOT build the
safety gadget (that is `implementation/subgame_exploit_solver.py`). Instead it simply
contrasts, at each of the hero's information sets:
  - the BLUEPRINT action distribution (Nash), and
  - the LOCAL exploit action (the full best response to the weak `Rock` type at that info set),
and lists the info sets where they differ most -- i.e. where a subgame solve would change
your play. Seeing that the deviations are LOCAL (a handful of info sets, not the whole tree)
is the whole intuition.

Run:  python subgame_peek.py
Runtime: ~1-3 min on Leduc (CFR blueprint + full-tree best response); set GAME="kuhn" for a
         seconds-fast (if less interesting) version.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import _bootstrap  # noqa: F401
from engines import make_game
from nash import solve_nash_cached
from opponent_types import make_type_zoo
from best_response import best_response_policy
from policies import materialize

import _soe_tools as tools

CONFIG = {
    "game": "leduc",           # "leduc" (interesting) or "kuhn" (fast)
    "hero": 0,
    "exploitee": {"leduc": "Rock", "kuhn": "TightPassive"},
    "nash_iters": {"kuhn": 30000, "leduc": 8000},
    "top_n": 8,                # how many most-deviating info sets to list
}


def _fmt(game, dist):
    return ", ".join(f"{game.action_name(a)}={p:.2f}" for a, p in sorted(dist.items()))


def _tv(p, q):
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def main():
    cfg = CONFIG
    game = make_game(cfg["game"])
    hero = cfg["hero"]
    exploitee_name = cfg["exploitee"][game.name]
    nash, _ = solve_nash_cached(game, cfg["nash_iters"][game.name])
    zoo = make_type_zoo(game, nash_iters=cfg["nash_iters"][game.name])
    opp = zoo[exploitee_name]
    v_star = tools.game_value(game, nash, hero)

    br = best_response_policy(game, hero, opp)
    nash_tbl = materialize(game, nash, hero)
    br_tbl = materialize(game, br, hero)

    # Global scores, for context: the blueprint's EV vs Rock and the full-exploit EV vs Rock.
    print(f"subgame peek  game={game.name} hero=P{hero} exploitee={exploitee_name}")
    print(f"game value (P{hero}) = {v_star:+.4f}")
    print(f"blueprint (Nash) EV vs {exploitee_name} = "
          f"{tools.exploitation_ev(game, nash, opp, hero):+.4f}")
    print(f"full exploit    EV vs {exploitee_name} = "
          f"{tools.exploitation_ev(game, br, opp, hero):+.4f}")
    print("-" * 74)

    deviations = []
    for iset in set(nash_tbl) | set(br_tbl):
        tv = _tv(nash_tbl.get(iset, {}), br_tbl.get(iset, {}))
        deviations.append((tv, iset))
    deviations.sort(reverse=True)

    n_changed = sum(1 for tv, _ in deviations if tv > 0.05)
    print(f"hero info sets: {len(deviations)} total; {n_changed} where the local exploit "
          f"deviates from the blueprint (TV > 0.05).")
    print(f"top {cfg['top_n']} deviating info sets (each is a candidate 'subgame' to re-solve):")
    for tv, iset in deviations[:cfg["top_n"]]:
        print(f"  {iset:>10s}  TV={tv:.2f}  "
              f"blueprint[{_fmt(game, nash_tbl.get(iset, {}))}]  "
              f"exploit[{_fmt(game, br_tbl.get(iset, {}))}]")

    print("-" * 74)
    print("intuition (PREDICTION -- verify): the exploit changes play at only a HANDFUL of "
          "info sets,\nnot the whole tree -- exactly the locality that makes real-time "
          "subgame solving worthwhile.\nThe safety gadget that keeps such a local deviation "
          "SAFE is in implementation/subgame_exploit_solver.py.")


if __name__ == "__main__":
    main()
