"""
Optional bridge / reachability check against PettingZoo MPE (raw step L133-138, L426-431:
MADDPG/MAPPO/CommNet are canonically demonstrated on MPE `simple_spread`).

WHY THIS IS ONLY A REACHABILITY CHECK
-------------------------------------
Per WORKFLOW.md the CORE cooperative results are validated on the self-contained `coop_env`
(CoopSignal for communication + critic-variance; ClimbingGame for IL-vs-CTDE reward), which
need no third-party envs. PettingZoo is offered as an OPTIONAL external cross-environment: this
script confirms the MPE env is importable and steppable and shows how our learners would attach
to it, but it does NOT train (the parallel-env plumbing + long-horizon rollout loop is out of
scope for a guarded cross-check and would need real compute).

GUARDED: prints SKIP and exits cleanly if PettingZoo is absent.
NOTE (per implementation/WORKFLOW.md): written but NOT executed by the agent.
"""

from __future__ import annotations


def check_mpe_reachable(steps: int = 5):
    try:
        from pettingzoo.mpe import simple_spread_v3
    except ImportError:
        print("[SKIP] PettingZoo not installed. `pip install 'pettingzoo[mpe]'` to enable this "
              "optional cross-environment check. The self-contained coop_env results "
              "(CoopSignal, ClimbingGame) do not need it.")
        return None

    print("PettingZoo MPE simple_spread reachability check")
    print("-" * 64)
    env = simple_spread_v3.parallel_env(N=3, max_cycles=25, continuous_actions=False)
    obs, info = env.reset(seed=0)
    agents = list(obs.keys())
    print(f"  agents={agents}")
    print(f"  obs_dim per agent={ {a: env.observation_space(a).shape for a in agents} }")
    print(f"  n_actions per agent={ {a: env.action_space(a).n for a in agents} }")
    for t in range(steps):
        actions = {a: env.action_space(a).sample() for a in agents}
        obs, rewards, term, trunc, info = env.step(actions)
        if not env.agents:
            break
    env.close()
    print(f"  stepped {t + 1} times OK -- env is reachable and steppable.")
    print("  ATTACH SKETCH: MPE gives per-agent obs + a shared global state (concatenated obs);")
    print("  wire those into MADDPG (centralized critic over global state + joint one-hot acts)")
    print("  and MAPPO (centralized V over the global state), exactly as coop_env exposes them.")
    return True


if __name__ == "__main__":
    check_mpe_reachable()
