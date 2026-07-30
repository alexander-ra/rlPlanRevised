"""Ollama HTTP client hardened for an unattended multi-hour run.

Failure policy: a transient error must never kill the run. Connection failures
wait and retry indefinitely (a model swap can take a minute and the server
briefly refuses connections); everything else gets bounded retries.
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request

ENDPOINT = "http://127.0.0.1:11434/api/generate"

# Qwen3.6 runs thinking mode by default and its reasoning leaks into `response`.
# `think: false` turns it off; this strips anything that slips through anyway.
THINK_RE = re.compile(r"<think>.*?</think>\s*", re.DOTALL | re.IGNORECASE)


class OllamaDown(RuntimeError):
    pass


def strip_think(s: str) -> str:
    s = THINK_RE.sub("", s)
    # an unclosed <think> means the model never emitted the closer; drop the head
    if "<think>" in s:
        s = s.split("</think>")[-1] if "</think>" in s else s.split("<think>")[0]
    return s.strip()


# Optional sink for per-request timing. The dashboard needs real tokens/sec, and
# Ollama already returns eval_count/eval_duration on every response - it was simply
# being discarded. Set STATS_SINK to a callable taking a dict.
STATS_SINK = None


def generate(model: str, prompt: str, system: str = "", *, temperature: float = 0.25,
             top_p: float = 0.9, num_predict: int = 2048, num_ctx: int = 16384,
             think: bool = False, seed: int | None = None, keep_alive: str = "2h",
             timeout: int = 900, attempts: int = 4, log=print) -> str:
    """One completion. Returns text with any <think> block removed."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": keep_alive,
        "think": think,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
            "num_predict": num_predict,
            "num_ctx": num_ctx,          # Ollama defaults to 4096 and TRUNCATES silently
        },
    }
    if system:
        payload["system"] = system
    if seed is not None:
        payload["options"]["seed"] = seed

    body = json.dumps(payload).encode()
    last = None

    for i in range(1, attempts + 1):
        try:
            req = urllib.request.Request(
                ENDPOINT, data=body, headers={"Content-Type": "application/json"})
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read())
            if STATS_SINK:
                try:
                    STATS_SINK({
                        "model": model,
                        "wall": time.time() - t0,
                        "out_tokens": data.get("eval_count", 0),
                        "in_tokens": data.get("prompt_eval_count", 0),
                        # eval_duration is nanoseconds
                        "gen_secs": (data.get("eval_duration") or 0) / 1e9,
                        "ts": time.time(),
                    })
                except Exception:  # noqa: BLE001 - telemetry must never break a run
                    pass
            return strip_think(data.get("response", ""))

        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            # 4xx other than 404 won't fix themselves - fail fast
            if 400 <= e.code < 500 and e.code != 404:
                raise RuntimeError(f"ollama rejected request: {e.code} {e.read()[:300]!r}")
            time.sleep(min(60, 5 * i))

        except (urllib.error.URLError, TimeoutError, OSError) as e:
            # server not listening / model swapping / socket dropped -> wait it out
            last = str(e)
            log(f"      ollama unreachable ({last}); waiting {min(60, 10 * i)}s")
            time.sleep(min(60, 10 * i))

        except json.JSONDecodeError as e:
            last = f"bad json: {e}"
            time.sleep(5 * i)

    raise OllamaDown(f"ollama failed after {attempts} attempts: {last}")


def wait_until_up(timeout: int = 900, log=print) -> bool:
    """Block until the server answers. Used at start and after model swaps."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen("http://127.0.0.1:11434/api/version", timeout=10):
                return True
        except Exception:
            log("   waiting for ollama...")
            time.sleep(10)
    return False


def unload(model: str, log=print) -> None:
    """Drop a model from VRAM. Qwen and BgGPT are ~22GB each and cannot
    co-reside in 32GB, so the stage boundary must free the previous one."""
    try:
        body = json.dumps({"model": model, "keep_alive": 0}).encode()
        req = urllib.request.Request(
            ENDPOINT, data=body, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=120).read()
        log(f"   unloaded {model}")
        time.sleep(5)
    except Exception as e:
        log(f"   unload {model} failed (harmless): {e}")
