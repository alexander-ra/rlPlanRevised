"""Serve the training dashboard over the LAN so you can glance from a phone.

  python implementation/nlhe/scripts/serve_dashboard.py <run_dir> [--port 8777]

Binds 0.0.0.0 and prints every reachable URL (localhost + LAN IPs). The page
polls status.json / metrics.jsonl / eval/*.json in <run_dir>. Near-zero load:
static files only. For access from OUTSIDE your LAN, tunnel it (tailscale/ssh);
do not expose this port to the public internet.
"""
from __future__ import annotations

import argparse
import re
import shutil
import socket
import subprocess
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
TOOLS = Path(__file__).resolve().parent.parent / "tools"


def start_tunnel(port):
    """Launch a Cloudflare quick tunnel (outbound; works from closed networks).

    Prints the public https://*.trycloudflare.com URL. The dashboard is
    read-only telemetry; the URL is unguessable but world-reachable, so treat it
    as semi-public. Requires tools/cloudflared.exe (downloaded separately)."""
    exe = TOOLS / "cloudflared.exe"
    if not exe.exists():
        print(f"[tunnel] {exe} not found; download cloudflared to enable --tunnel")
        return None
    proc = subprocess.Popen(
        [str(exe), "tunnel", "--url", f"http://localhost:{port}", "--no-autoupdate"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    def watch():
        for line in proc.stdout:
            m = re.search(r"https://[-\w.]+\.trycloudflare\.com", line)
            if m:
                print("\n" + "=" * 60)
                print(f"  PUBLIC DASHBOARD URL:  {m.group(0)}")
                print("  (open from any device, anywhere; keep it private)")
                print("=" * 60 + "\n", flush=True)
    threading.Thread(target=watch, daemon=True).start()
    return proc


def lan_ips():
    ips = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None):
            ip = info[4][0]
            if "." in ip and not ip.startswith("127."):
                ips.add(ip)
    except Exception:
        pass
    return sorted(ips)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--port", type=int, default=8777)
    ap.add_argument("--tunnel", action="store_true",
                    help="also expose via a Cloudflare quick tunnel (remote access)")
    a = ap.parse_args()
    run = Path(a.run_dir).resolve()
    run.mkdir(parents=True, exist_ok=True)
    # copy the dashboard into the run dir so it's served alongside the data
    shutil.copy(SRC / "dashboard" / "index.html", run / "index.html")
    handler = partial(SimpleHTTPRequestHandler, directory=str(run))
    httpd = ThreadingHTTPServer(("0.0.0.0", a.port), handler)
    print(f"dashboard serving {run}")
    print(f"  http://localhost:{a.port}")
    for ip in lan_ips():
        print(f"  http://{ip}:{a.port}   (from another device on your network)")
    tunnel = start_tunnel(a.port) if a.tunnel else None
    print("Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if tunnel:
            tunnel.terminate()


if __name__ == "__main__":
    main()
