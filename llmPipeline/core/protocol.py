"""Numbered-block request protocol.

Lifted from scripts/translate_srt.py, which ran 2,113 items through it tonight
with 0 malformed-reply fallbacks. The contract: N inputs go out as [1]..[N],
exactly N lines must come back, and a reply that fails validation causes the
batch to split rather than the run to fail.
"""
from __future__ import annotations

import re

LINE_RE = re.compile(r"^\s*\[(\d+)\]\s*(.*)$")


def render(items: list[str]) -> str:
    return "\n".join(f"[{i}] {t}" for i, t in enumerate(items, 1))


def parse(reply: str, n: int) -> list[str] | None:
    """Strict: every index 1..n present exactly once, else None (caller splits)."""
    got: dict[int, str] = {}
    for line in reply.splitlines():
        m = LINE_RE.match(line)
        if m:
            k = int(m.group(1))
            if 1 <= k <= n and k not in got:
                got[k] = m.group(2).strip()
    if len(got) != n:
        return None
    return [got[i] for i in range(1, n + 1)]


def run_batched(items: list, call, to_text, on_fail, log=print, depth: int = 0) -> list:
    """Send `items` as one numbered block; on a malformed reply, split and retry.

    call(list_of_str) -> raw reply text
    to_text(item)     -> the string sent for that item
    on_fail(item)     -> value used when a single item cannot be parsed
    """
    n = len(items)
    if n == 0:
        return []
    try:
        reply = call([to_text(x) for x in items])
        out = parse(reply, n)
    except Exception as e:  # noqa: BLE001 - a dead batch must not kill the run
        log(f"      batch of {n} errored: {e}")
        out = None

    if out is not None:
        return out

    if n == 1:
        log("      single item unparseable; using fallback")
        return [on_fail(items[0])]

    mid = n // 2
    log(f"      malformed reply for {n}; splitting")
    return (run_batched(items[:mid], call, to_text, on_fail, log, depth + 1)
            + run_batched(items[mid:], call, to_text, on_fail, log, depth + 1))
