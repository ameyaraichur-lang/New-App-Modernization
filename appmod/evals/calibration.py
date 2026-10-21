"""Calibration of model confidence (C6).

Pairs are (stated confidence, was the item correct). ECE is the bin-weighted gap between mean
confidence and accuracy over ten equal-width bins. C6 is 1 - ECE at the 95th percentile of a
seeded bootstrap, so a small sample cannot look well calibrated by luck. The calibration map
(accuracy per bin) is fitted on tune repos and checked on held-out repos; it is reported, and
nothing in the pipeline reads it.
"""

from __future__ import annotations

import random
from typing import Any

BINS = 10
BOOTSTRAP = 1000
SEED = 7

Pair = tuple[float, bool]


def _bin(conf: float) -> int:
    return min(BINS - 1, int(conf * BINS))


def ece(pairs: list[Pair]) -> float | None:
    if not pairs:
        return None
    sums: dict[int, list[float]] = {}
    for conf, ok in pairs:
        s = sums.setdefault(_bin(conf), [0.0, 0.0, 0.0])
        s[0] += conf
        s[1] += ok
        s[2] += 1
    return sum(abs(c - a) for c, a, _ in sums.values()) / len(pairs)


def ece_upper(pairs: list[Pair], q: float = 0.95) -> float | None:
    if not pairs:
        return None
    rng = random.Random(SEED)
    stats = sorted(ece([rng.choice(pairs) for _ in pairs]) or 0.0 for _ in range(BOOTSTRAP))
    return stats[min(BOOTSTRAP - 1, int(q * BOOTSTRAP))]


def reliability(pairs: list[Pair]) -> list[dict[str, Any]]:
    rows = []
    for b in range(BINS):
        hits = [(c, ok) for c, ok in pairs if _bin(c) == b]
        if hits:
            rows.append({"bin": f"{b / BINS:.1f}-{(b + 1) / BINS:.1f}", "n": len(hits),
                         "mean_confidence": round(sum(c for c, _ in hits) / len(hits), 3),
                         "accuracy": round(sum(ok for _, ok in hits) / len(hits), 3)})
    return rows


def fit_map(pairs: list[Pair]) -> dict[int, float]:
    """Observed accuracy per confidence bin (histogram binning)."""
    return {b: sum(ok for c, ok in pairs if _bin(c) == b) / n
            for b in range(BINS) if (n := sum(1 for c, _ in pairs if _bin(c) == b))}


def apply_map(cmap: dict[int, float], pairs: list[Pair]) -> list[Pair]:
    return [(cmap.get(_bin(c), c), ok) for c, ok in pairs]


def summarize(pairs_by_split: dict[str, list[Pair]]) -> dict[str, Any]:
    pairs = [p for ps in pairs_by_split.values() for p in ps]
    out: dict[str, Any] = {"n": len(pairs), "ece": _r(ece(pairs)), "ece_upper95": _r(ece_upper(pairs)),
                           "reliability": reliability(pairs)}
    tune, holdout = pairs_by_split.get("tune", []), pairs_by_split.get("holdout", [])
    if tune and holdout:
        cmap = fit_map(tune)
        out["holdout"] = {"n": len(holdout), "ece_raw": _r(ece(holdout)),
                          "ece_mapped": _r(ece(apply_map(cmap, holdout))),
                          "map": {f"{b / BINS:.1f}": round(a, 3) for b, a in sorted(cmap.items())}}
    return out


def _r(x: float | None) -> float | None:
    return None if x is None else round(x, 4)
