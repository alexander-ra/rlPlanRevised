"""
config.py  [INF]  -- run profiles, the LLM model roster, and runtime notes for Step 12.

TWO PROFILES
------------
  SMOKE : tiny, CPU-friendly, LLM = offline stub. For a fast end-to-end shakedown that the whole
          pipeline wires together (data -> DT/ARDT/BC -> exploitability -> table) with no GPU.
  SCALE : full sizes for the RTX 5090; LLM points at a real local model (default gpt-oss 20B).

Select with the env var STEP12_PROFILE=SMOKE|SCALE (default SMOKE), e.g. on PowerShell:
    $env:STEP12_PROFILE = "SCALE"; python comparison_table.py

LLM ROSTER (confirmed with the user)
------------------------------------
  default     : gpt-oss 20B          (strong open-weight reasoner; comfortable on 24-32GB VRAM)
  alternative : Qwen2.5-7B-Instruct  (dense, robust, fast; the "base" of the pair below)
  alternative : OpenThinker3-7B      (a reasoning-SFT of the SAME Qwen2.5-7B base -> a clean
                                      base-vs-reasoning-tuned comparison)
Nemotron 3 Nano is deferred unless results are compelling. The client is model-agnostic: every
preset below is just (base_url, model) for an OpenAI-compatible server, so swapping models is a
one-line change. All numbers these produce are PREDICTIONS until the run session.
"""

from __future__ import annotations

import os

# Target returns to sweep for the DT return-conditioning experiment. Kuhn hand payoffs are in
# {-2,-1,+1,+2}; +3 is IMPOSSIBLE (no hand ever returned it) -> the Paster OOD-extrapolation probe.
TARGET_RETURNS = [-2.0, -1.0, 1.0, 2.0]
IMPOSSIBLE_RETURN = 3.0

# "Within 50 mbb/h of Nash" (raw L462) with a 1-chip big blind == exploitability <= 0.05 chips.
ARDT_NASH_TOLERANCE_CHIPS = 0.05


# --- LLM presets (dicts consumed by llm_agent.make_client) ---------------------------
LLM_STUB = {"backend": "stub"}

# OpenAI-compatible local servers. base_url defaults assume LM Studio (port 1234); for Ollama use
# "http://localhost:11434/v1". api_key is unused by local servers (kept for OpenRouter/OpenAI).
LLM_GPT_OSS_20B = {
    "backend": "openai", "base_url": "http://localhost:1234/v1",
    "model": "gpt-oss-20b", "api_key": None, "timeout": 180.0,
}
LLM_QWEN25_7B = {
    "backend": "openai", "base_url": "http://localhost:1234/v1",
    "model": "qwen2.5-7b-instruct", "api_key": None, "timeout": 180.0,
}
LLM_OPENTHINKER3_7B = {
    "backend": "openai", "base_url": "http://localhost:1234/v1",
    "model": "openthinker3-7b", "api_key": None, "timeout": 240.0,  # long CoT -> higher timeout
}

LLM_ROSTER = {
    "stub": LLM_STUB,
    "gpt_oss_20b": LLM_GPT_OSS_20B,
    "qwen2.5_7b": LLM_QWEN25_7B,
    "openthinker3_7b": LLM_OPENTHINKER3_7B,
}


# --- profiles ------------------------------------------------------------------------
SMOKE = {
    "name": "SMOKE",
    "game": "kuhn",
    "seed": 0,
    # data
    "n_trajectories": 5000,
    "cfr_iters": 5000,
    "exploit_frac": 0.5,
    # DT / ARDT / BC model
    "hidden_size": 32,
    "n_layer": 2,
    "n_head": 4,
    "max_ep_len": 8,
    "dt_epochs": 15,
    "estimator_epochs": 20,
    "bc_epochs": 15,
    "batch_size": 128,
    "lr": 1e-3,
    "expectile_tau": 0.1,
    "dt_target_return": 2.0,
    # LLM
    "llm_styles": ["plain", "cot", "gametheory"],
    "llm_temperature": 0.0,   # deterministic for the stub
    "llm_samples": 4,
    "llm_preset": LLM_STUB,
}

SCALE = {
    "name": "SCALE",
    "game": "kuhn",          # Leduc is an optional SCALE extension (see README)
    "seed": 0,
    "n_trajectories": 50000,
    "cfr_iters": 30000,
    "exploit_frac": 0.5,
    "hidden_size": 64,
    "n_layer": 3,
    "n_head": 4,
    "max_ep_len": 16,
    "dt_epochs": 60,
    "estimator_epochs": 80,
    "bc_epochs": 60,
    "batch_size": 256,
    "lr": 1e-3,
    "expectile_tau": 0.1,
    "dt_target_return": 2.0,
    "llm_styles": ["plain", "cot", "gametheory"],
    "llm_temperature": 0.7,
    "llm_samples": 16,
    "llm_preset": LLM_GPT_OSS_20B,
}

PROFILES = {"SMOKE": SMOKE, "SCALE": SCALE}


def active_config() -> dict:
    """Return the profile named by STEP12_PROFILE (default SMOKE). Also honors
    STEP12_LLM=<roster key> to override the LLM preset without editing this file."""
    name = os.environ.get("STEP12_PROFILE", "SMOKE").upper()
    if name not in PROFILES:
        raise ValueError(f"Unknown STEP12_PROFILE={name!r}; choose from {sorted(PROFILES)}")
    cfg = dict(PROFILES[name])  # shallow copy so overrides don't mutate the module constant
    llm_key = os.environ.get("STEP12_LLM")
    if llm_key:
        if llm_key not in LLM_ROSTER:
            raise ValueError(f"Unknown STEP12_LLM={llm_key!r}; choose from {sorted(LLM_ROSTER)}")
        cfg["llm_preset"] = LLM_ROSTER[llm_key]
    return cfg


RUNTIME_NOTES = """
RUNTIME NOTES (verify in the run session)
=========================================
GPU / torch (RTX 5090, Blackwell sm_120):
  - The DT/ARDT here are TINY; SMOKE runs fine on CPU. Only SCALE benefits from CUDA.
  - Blackwell needs a recent CUDA (12.8+) build of PyTorch. If `torch.cuda.is_available()` is
    False on the 5090, install a cu128 (or nightly cu128) wheel. The code auto-falls back to CPU.

Serving a local LLM (OpenAI-compatible; pick ONE):
  - LM Studio: load the model, start its local server; base_url = http://localhost:1234/v1,
    model = the id LM Studio shows. (Default in the presets above.)
  - Ollama:    `ollama pull <model>` then `ollama serve`; base_url = http://localhost:11434/v1,
    model = the pulled tag (e.g. "qwen2.5:7b-instruct").
  - vLLM / OpenRouter / OpenAI: same shape; set base_url, model, and api_key.

Switching models without editing code:
    $env:STEP12_PROFILE = "SCALE"; $env:STEP12_LLM = "qwen2.5_7b"; python comparison_table.py
    $env:STEP12_LLM = "openthinker3_7b"; python comparison_table.py

Roster fit on a 24-32GB card:
  - gpt-oss 20B        : default; run a quantized build if VRAM is tight.
  - Qwen2.5-7B-Instruct: comfortable at bf16/fp16; fast; good robustness baseline.
  - OpenThinker3-7B    : same footprint as Qwen2.5-7B but ALWAYS emits long CoT -> higher latency
                         and more text to parse; budget a larger timeout (already set) and expect
                         a lower throughput than Qwen2.5.
"""


def _selftest():
    print("config self-test")
    print("-" * 50)
    for name in ("SMOKE", "SCALE"):
        os.environ["STEP12_PROFILE"] = name
        cfg = active_config()
        print(f"{name}: game={cfg['game']} n_traj={cfg['n_trajectories']} "
              f"dt_epochs={cfg['dt_epochs']} llm={cfg['llm_preset']['backend']}")
    os.environ["STEP12_PROFILE"] = "SMOKE"
    os.environ["STEP12_LLM"] = "qwen2.5_7b"
    print("override STEP12_LLM=qwen2.5_7b ->", active_config()["llm_preset"]["model"])
    del os.environ["STEP12_LLM"]
    print(f"TARGET_RETURNS={TARGET_RETURNS} IMPOSSIBLE={IMPOSSIBLE_RETURN} "
          f"ARDT_tol={ARDT_NASH_TOLERANCE_CHIPS} chips")


if __name__ == "__main__":
    _selftest()
