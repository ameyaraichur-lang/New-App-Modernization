"""Interval bounds for proportions measured on finite samples."""

from __future__ import annotations

from math import sqrt

Z95 = 1.959964


def wilson_lower(k: int, n: int, z: float = Z95) -> float | None:
    """95 % Wilson score lower bound for k successes out of n; None when n == 0."""
    if n <= 0:
        return None
    p = k / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    margin = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, (centre - margin) / denom)
