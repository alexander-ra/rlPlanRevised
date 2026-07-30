#!/usr/bin/env python3
"""Read-only dashboard for the corpus translation run.  http://localhost:8780

Reads out/run_state.json (written atomically by run_all.py), nvidia-smi, and the
Ollama API. It has no write endpoints and cannot influence the run, which is why
it is safe to expose through a tunnel without auth.

The log it serves is status lines only, never translated text, so sharing the
link cannot leak draft thesis prose.
"""
from __future__ import annotations

import json
import subprocess
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE = HERE.parent / "out" / "run_state.json"
PAGE = HERE / "static" / "dash.html"
PORT = 8780

_gpu_cache = {"t": 0.0, "v": {}}


def gpu() -> dict:
    """nvidia-smi is ~50ms; cache briefly so many phone refreshes stay cheap."""
    if time.time() - _gpu_cache["t"] < 2:
        return _gpu_cache["v"]
    q = ("utilization.gpu,memory.used,memory.total,temperature.gpu,"
         "power.draw,power.limit,fan.speed,clocks.sm")
    try:
        out = subprocess.run(
            ["nvidia-smi", f"--query-gpu={q}", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=8).stdout.strip().split("\n")[0]
        p = [x.strip() for x in out.split(",")]
        v = {"util": float(p[0]), "vram_used": float(p[1]), "vram_total": float(p[2]),
             "temp": float(p[3]), "power": float(p[4]), "power_max": float(p[5]),
             "fan": p[6], "clock": p[7]}
    except Exception:  # noqa: BLE001
        v = {}
    _gpu_cache.update(t=time.time(), v=v)
    return v


def ollama_ps() -> dict:
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/ps", timeout=5) as r:
            m = json.loads(r.read()).get("models", [])
        if not m:
            return {"loaded": None}
        a = m[0]
        tot = a.get("size", 0) or 1
        vram = a.get("size_vram", 0)
        return {"loaded": a.get("name"), "size_gb": round(tot / 1e9, 1),
                "gpu_pct": round(vram / tot * 100), "ctx": a.get("context_length")}
    except Exception:  # noqa: BLE001
        return {"loaded": None}


def state() -> dict:
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def build() -> dict:
    s = state()
    now = time.time()
    files = s.get("files", {})
    done_w = s.get("done_words", 0)
    total_w = s.get("total_words", 1)
    started = s.get("started", now)
    elapsed = max(1.0, now - started)

    cur = s.get("current")
    # fraction of the current file already processed (5 passes)
    cur_frac = 0.0
    if cur and cur.get("blocks"):
        cur_frac = ((cur.get("pass", 1) - 1) + cur.get("block", 0) / cur["blocks"]) / 5
    effective_done = done_w + (cur["words"] * cur_frac if cur else 0)

    rate = effective_done / elapsed                      # words/sec, whole-run average
    remaining = max(0, total_w - effective_done)
    eta_all = remaining / rate if rate > 0.01 else None
    eta_cur = ((cur["words"] * (1 - cur_frac)) / rate
               if cur and rate > 0.01 else None)

    steps = {}
    for path, f in files.items():
        steps.setdefault(f["step"], {})[f["kind"]] = {
            "status": f["status"], "words": f["words"], "secs": f["secs"],
            "defects": f.get("defects", 0), "parity": f.get("parity"),
        }
    done_recent = sorted(
        [{"step": f["step"], "kind": f["kind"], "secs": f["secs"],
          "defects": f.get("defects", 0), "parity": f.get("parity"), "words": f["words"]}
         for f in files.values() if f["status"] == "done"],
        key=lambda x: -x["secs"])[:8]

    alive = (now - s.get("heartbeat", 0)) < 180 and not s.get("finished")
    return {
        "alive": alive, "finished": s.get("finished"),
        "stale_for": round(now - s.get("heartbeat", now)),
        "files_done": s.get("done_files", 0), "files_total": s.get("total_files", 0),
        "words_done": round(effective_done), "words_total": total_w,
        "pct": round(effective_done / total_w * 100, 1) if total_w else 0,
        "elapsed": round(elapsed), "eta_all": round(eta_all) if eta_all else None,
        "eta_cur": round(eta_cur) if eta_cur else None,
        "finish_at": (time.strftime("%H:%M", time.localtime(now + eta_all))
                      if eta_all else None),
        "wpm": round(rate * 60),
        "current": cur, "cur_frac": round(cur_frac * 100),
        "steps": steps, "recent": done_recent,
        "tps": s.get("tps"), "tps_series": s.get("tps_series", [])[-60:],
        "tokens_out": s.get("tokens_out", 0), "requests": s.get("requests", 0),
        "retries": s.get("retries", 0), "failures": s.get("failures", 0),
        "reverted": s.get("reverted", 0),
        "log": s.get("log", [])[-14:],
        "gpu": gpu(), "llm": ollama_ps(),
    }


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path.startswith("/api"):
            b = json.dumps(build(), ensure_ascii=False).encode()
            ct = "application/json; charset=utf-8"
        else:
            b = PAGE.read_bytes()
            ct = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)


if __name__ == "__main__":
    print(f"dashboard: http://localhost:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
