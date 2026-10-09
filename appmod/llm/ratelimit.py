"""Process-wide tokens-per-minute limiter shared by all parallel agents."""

from __future__ import annotations

import threading
import time


class TokenBucket:
    def __init__(self, tokens_per_minute: int):
        self.capacity = max(1000, int(tokens_per_minute))
        self.rate = self.capacity / 60.0
        self.tokens = float(self.capacity)
        self.updated = time.monotonic()
        self._cv = threading.Condition()

    def _refill(self) -> None:
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.rate)
        self.updated = now

    def acquire(self, n: int, timeout: float = 300.0) -> None:
        n = min(int(n), self.capacity)
        deadline = time.monotonic() + timeout
        with self._cv:
            while True:
                self._refill()
                if self.tokens >= n:
                    self.tokens -= n
                    return
                wait = (n - self.tokens) / self.rate
                if time.monotonic() + wait > deadline:
                    raise TimeoutError(f"TPM limiter: {n} tokens unavailable within {timeout}s")
                self._cv.wait(min(wait, 2.0))

    def settle(self, estimated: int, actual: int) -> None:
        """Correct the bucket once real usage is known (refund or charge)."""
        with self._cv:
            self.tokens = min(self.capacity, self.tokens + estimated - actual)
            self._cv.notify_all()
