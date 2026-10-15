"""Pause model work while the Astra endpoint is unreachable.

A network drop or a sleeping host fails every deployment at once, so tier
failover cannot help and per-agent retries are spent in minutes. The gate
turns that into a pause: the first caller to see the outage probes the
endpoint with backoff (no tokens) while every other caller waits, and all of
them resume the same request once it answers. Agent retry budgets are not
touched. The wait is bounded by ``max_wait_s`` of awake time.
"""

from __future__ import annotations

import threading
import time
from typing import Any, Callable

OutageHook = Callable[[str, dict[str, Any]], None]


class _Outage:
    def __init__(self) -> None:
        self.over = threading.Event()
        self.restored = False


class OutageGate:
    def __init__(self, probe: Callable[[], bool], *, max_wait_s: float = 6 * 3600,
                 first_delay_s: float = 5.0, max_delay_s: float = 120.0,
                 on_change: OutageHook | None = None, stop: threading.Event | None = None):
        self.probe = probe
        self.max_wait_s = max_wait_s
        self.first_delay_s = first_delay_s
        self.max_delay_s = max_delay_s
        self.on_change = on_change
        self.stop = stop
        self.outages = 0
        self._lock = threading.Lock()
        self._current: _Outage | None = None

    def reachable(self) -> bool:
        try:
            return bool(self.probe())
        except Exception:
            return False

    def wait(self) -> bool:
        """Block until the endpoint answers again. False if the wait was cancelled or timed out."""
        with self._lock:
            outage, lead = self._current, False
            if outage is None:
                outage, lead = _Outage(), True
                self._current = outage
                self.outages += 1
        if not lead:
            outage.over.wait()
            return outage.restored
        try:
            outage.restored = self._probe_until_back()
        finally:
            with self._lock:
                self._current = None
            outage.over.set()
        return outage.restored

    def _probe_until_back(self) -> bool:
        started, wall = time.monotonic(), time.time()
        self._notify("LOST", {})
        delay, probes = self.first_delay_s, 0
        while time.monotonic() - started < self.max_wait_s:
            if self.stop is not None and self.stop.wait(delay):
                self._notify("GAVE_UP", {"reason": "cancelled", "probes": probes,
                                         "waited_s": round(time.time() - wall)})
                return False
            if self.stop is None:
                time.sleep(delay)
            probes += 1
            if self.reachable():
                self._notify("RESTORED", {"probes": probes, "waited_s": round(time.time() - wall)})
                return True
            delay = min(delay * 2, self.max_delay_s)
        self._notify("GAVE_UP", {"reason": "max wait exceeded", "probes": probes,
                                 "waited_s": round(time.time() - wall)})
        return False

    def _notify(self, status: str, info: dict[str, Any]) -> None:
        if self.on_change is not None:
            try:
                self.on_change(status, info)
            except Exception:
                pass  # reporting must never break the wait
