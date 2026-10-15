"""Regression gate for a finished eval report.

The merge rule compares failures and point estimates, not Wilson lower bounds. A component
regresses when it has more failures, a lower point estimate, or was assessed before and is
unassessed now. An unassessed component that stays unassessed is unchanged.
"""

from __future__ import annotations

from typing import Any


def _stats(component: dict[str, Any]) -> tuple[int, float]:
    measures = [m for m in component.get("measures") or [] if m.get("n")]
    if measures:
        k = sum(int(m["k"]) for m in measures)
        n = sum(int(m["n"]) for m in measures)
        return n - k, (k / n if n else 1.0)
    return 0, float(component.get("lower_bound") or 0) / 100


def route_flips(previous: dict[str, Any], current: dict[str, Any]) -> list[str]:
    """P2 disposition changes between two e2e reports. Listed, not a merge block."""
    prev = previous.get("app_facts") or {}
    cur = current.get("app_facts") or {}
    flips = []
    for app in sorted(set(prev) & set(cur)):
        old = (prev[app] or {}).get("disposition")
        new = (cur[app] or {}).get("disposition")
        if old and new and old != new:
            flips.append(f"{app}: {old} -> {new}")
    return flips


def regressions(previous: dict[str, Any], current: dict[str, Any]) -> list[str]:
    prev = {c["id"]: c for c in previous["confidence"]["components"]}
    cur = {c["id"]: c for c in current["confidence"]["components"]}
    problems: list[str] = []
    for cid in prev:
        old, new = prev[cid], cur.get(cid)
        if new is None:
            problems.append(f"{cid} missing from the new report")
            continue
        if old.get("assessed") and not new.get("assessed"):
            problems.append(f"{cid} was assessed and is now not assessed")
            continue
        if not old.get("assessed") or not new.get("assessed"):
            continue
        old_failures, old_point = _stats(old)
        new_failures, new_point = _stats(new)
        if new_failures > old_failures:
            problems.append(f"{cid} failures {old_failures} -> {new_failures}")
        if new_point < old_point - 1e-9:
            problems.append(f"{cid} point estimate {old_point:.4f} -> {new_point:.4f}")
    return problems
