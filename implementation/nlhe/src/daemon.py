"""Training orchestrator: runs MCCFR, checkpoints, writes dashboard status/metrics,
and periodically evaluates. One supervisor process; numba threads do the work.

  python implementation/nlhe/scripts/train.py --run <id>            # start/resume
  python implementation/nlhe/scripts/train.py --pilot-hours 24      # bounded pilot

Cadences come from config (checkpoint/eval/metrics). Everything survives Ctrl+C
and hard reboot: on exit and every checkpoint interval a full A/B checkpoint is
written atomically; --resume reloads the newest valid one.
"""
from __future__ import annotations

import json
import signal
import sys
import time
from pathlib import Path

import numpy as np

import checkpoint as CK

ROOT = Path(__file__).resolve().parents[1]


class Daemon:
    def __init__(self, cfg, run_id, pilot_hours=None, pilot_iters=None):
        self.cfg = cfg
        self.run_id = run_id
        self.run_dir = ROOT / "runs" / run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        (self.run_dir / "eval").mkdir(exist_ok=True)
        self.pilot_hours = pilot_hours
        self.pilot_iters = pilot_iters
        self.stop = False
        self.gi = 0
        self.iters_per_sec = 0.0
        self.eval_history = []

    # -- setup ------------------------------------------------------------
    def setup(self):
        import numba
        import engine_ref as ER
        import engine_nb as EN
        import mccfr
        self.mccfr = mccfr
        self.EN = EN
        a = self.cfg["abstraction"]
        rules = ER.Rules(
            num_players=self.cfg["game"]["num_players"],
            starting_stack=self.cfg["game"]["starting_stack"],
            small_blind=self.cfg["game"]["small_blind"],
            big_blind=self.cfg["game"]["big_blind"], ante=self.cfg["game"]["ante"],
            raise_fractions=tuple(a["raise_fractions"]),
            include_allin=a["include_allin"], use_preflop_open=a["use_preflop_open"],
            preflop_open_bb=a["preflop_open_bb"],
            max_raises_per_street=a["max_raises_per_street"])
        self.rules = EN.pack_rules(rules)
        self.art = mccfr.load_artifacts(self.cfg["buckets"])
        numba.set_num_threads(self.cfg["mccfr"]["n_workers"])
        try:
            import psutil
            psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        except Exception:
            pass
        ckpt, it = CK.latest_checkpoint(self.run_dir)
        if ckpt is not None:
            self.slot_key, self.regret, self.stratsum, meta = CK.load_full(ckpt)
            assert self.slot_key.dtype == np.uint64, \
                "checkpoint predates the uint64/prepopulation fix; start a fresh run"
            self.gi = it
            print(f"resumed from {ckpt} at iteration {it:,}")
        else:
            # pre-populate all reachable infosets single-threaded so the
            # multi-threaded training loop NEVER inserts (no duplicate race)
            self.slot_key, self.regret, self.stratsum, tinfo = \
                mccfr.build_table(self.rules, self.cfg["buckets"])
            self._save_config()
        self._args = (self.rules, self.slot_key, self.regret, self.stratsum,
                      self.art["kpre"], self.art["bpre"], self.art["kflop"],
                      self.art["bflop"], self.art["kturn"], self.art["bturn"],
                      self.art["kriver"], self.art["briver"], self.art["rank"],
                      self.art["binom"], self.art["perms"],
                      float(self.cfg["mccfr"]["prune_threshold"]))

    def _save_config(self):
        import subprocess
        try:
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=str(ROOT)).decode().strip()
        except Exception:
            commit = "unknown"
        (self.run_dir / "config.json").write_text(json.dumps(
            {"config": self.cfg, "git_commit": commit,
             "started": time.time()}, indent=2))

    # -- main loop --------------------------------------------------------
    def run(self):
        self.setup()
        m = self.cfg["mccfr"]
        ck = self.cfg["checkpoint"]
        prune_after = int(m["planned_iterations"] * m["prune_enabled_after_fraction"])
        warmup_end = int(m["planned_iterations"] * m["discount_warmup_fraction"])
        disc_int = m["discount_interval"]
        batch = m["batch_iters_per_call"] * self.cfg["mccfr"]["n_workers"]
        print("warming up JIT...", flush=True)
        self.mccfr.run_batch(2000, self.gi, *self._args, False)
        self.gi += 2000
        t0 = time.time()
        last_metrics = last_ckpt = last_ms = last_eval = t0
        self._eval_interval = self.cfg["eval"]["interval_hours"] * 3600
        self._next_eval_ts = t0 + self._eval_interval
        gi_at_last_metrics = self.gi
        next_disc = ((self.gi // disc_int) + 1) * disc_int
        deadline = t0 + self.pilot_hours * 3600 if self.pilot_hours else None
        print(f"training from iter {self.gi:,}", flush=True)
        while not self.stop:
            prune_on = self.gi >= prune_after
            self.mccfr.run_batch(batch, self.gi, *self._args, prune_on)
            self.gi += batch
            # LCFR discounting during warmup
            if self.gi >= next_disc and self.gi < warmup_end:
                t = self.gi
                self.mccfr.discount(self.regret, self.stratsum,
                                    np.float32(t / (t + disc_int)))
                next_disc += disc_int
            now = time.time()
            if now - last_metrics >= ck["metrics_seconds"]:
                self.iters_per_sec = (self.gi - gi_at_last_metrics) / (now - last_metrics)
                gi_at_last_metrics = self.gi
                last_metrics = now
                self._write_status(now, prune_on)
            if now - last_ckpt >= ck["full_checkpoint_hours"] * 3600:
                self._checkpoint()
                last_ckpt = now
            if now - last_ms >= ck["milestone_hours"] * 3600:
                self._milestone()
                last_ms = now
            if now - last_eval >= self._eval_interval:
                self._evaluate()
                last_eval = now
                self._next_eval_ts = last_eval + self._eval_interval
            if deadline and now >= deadline:
                break
            if self.pilot_iters and self.gi >= self.pilot_iters:
                break
        print("stopping; final checkpoint...", flush=True)
        self._checkpoint()
        self._milestone()

    # -- periodic tasks ---------------------------------------------------
    def _used(self):
        return int((self.slot_key != 0).sum())

    def _write_status(self, now, prune_on):
        used = self._used()
        ram = self.slot_key.nbytes + self.regret.nbytes + self.stratsum.nbytes
        ck_dir, ck_it = CK.latest_checkpoint(self.run_dir)
        ck_ts = None
        if ck_dir is not None:
            ck_ts = json.loads((ck_dir / "meta.json").read_text())["ts"]
        status = {
            "run_id": self.run_id, "state": "TRAINING", "iteration": int(self.gi),
            "iters_per_sec": round(self.iters_per_sec, 1),
            "prune_rate": None, "ram_gb": round(ram / 1e9, 1),
            "workers": self.cfg["mccfr"]["n_workers"], "infosets": used,
            "last_checkpoint": ({"iter": ck_it, "ts": ck_ts} if ck_ts else None),
            "next_eval_ts": getattr(self, "_next_eval_ts",
                                    now + getattr(self, "_eval_interval", 21600)),
            "gpu_job": None, "prune_on": prune_on,
        }
        (self.run_dir / "status.json").write_text(json.dumps(status))
        with open(self.run_dir / "metrics.jsonl", "a") as f:
            f.write(json.dumps({"ts": now, "iteration": int(self.gi),
                                "iters_per_sec": round(self.iters_per_sec, 1),
                                "infosets": used, "ram_gb": round(ram / 1e9, 1)}) + "\n")

    def _checkpoint(self):
        which = CK.next_slot(self.run_dir)
        dt = CK.save_full(self.run_dir, which, self.slot_key, self.regret,
                          self.stratsum, self.gi)
        print(f"  checkpoint {which} @ iter {self.gi:,} ({dt:.0f}s)", flush=True)

    def _milestone(self):
        day = int((time.time() - self._t0()) / 86400)
        CK.save_milestone(self.run_dir, self.slot_key, self.stratsum, self.gi, day)

    def _t0(self):
        try:
            return json.loads((self.run_dir / "config.json").read_text())["started"]
        except Exception:
            return time.time()

    def _evaluate(self):
        """Launch eval as an ISOLATED subprocess (non-blocking). A crash or
        slowness in eval can never touch training, and training never pauses.
        Eval reads the latest checkpoint, so it needs one to exist first."""
        import subprocess
        # skip if a previous eval is still running (don't pile up)
        if getattr(self, "_eval_proc", None) is not None and \
                self._eval_proc.poll() is None:
            print("  (previous eval still running; skipping this cycle)", flush=True)
            return
        ck, _ = CK.latest_checkpoint(self.run_dir)
        if ck is None:
            return  # no checkpoint yet; eval needs one
        log = open(self.run_dir / "eval" / "eval.log", "a")
        self._eval_proc = subprocess.Popen(
            [sys.executable, str(ROOT / "scripts" / "run_eval.py"),
             str(self.run_dir)], stdout=log, stderr=subprocess.STDOUT,
            cwd=str(ROOT))
        print(f"  eval subprocess launched @ iter {self.gi:,} "
              f"(pid {self._eval_proc.pid})", flush=True)

    def handle_signal(self, *_):
        self.stop = True


def main(run_id, pilot_hours=None, pilot_iters=None, cfg=None):
    if cfg is None:
        cfg = json.loads((ROOT / "config" / "default.json").read_text())
    d = Daemon(cfg, run_id, pilot_hours, pilot_iters)
    signal.signal(signal.SIGINT, d.handle_signal)
    signal.signal(signal.SIGTERM, d.handle_signal)
    d.run()
