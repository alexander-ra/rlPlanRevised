"""Tiny logger: prints and appends to logs/<name>.log with a timestamp."""

from __future__ import annotations

import datetime as _dt
import os

import deps


class Logger:
    def __init__(self, name: str):
        self.path = os.path.join(deps.LOGS_DIR, f"{name}.log")
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(f"\n===== {name} started {_dt.datetime.now().isoformat(timespec='seconds')} =====\n")

    def __call__(self, msg: str):
        line = f"[{_dt.datetime.now().strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
