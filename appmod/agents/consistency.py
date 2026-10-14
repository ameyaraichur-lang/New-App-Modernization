"""k = 3 independent samples for route and boundary decisions.

A majority publishes. A split becomes a review that lists every option and the
evidence cited for it. Two of three is a majority.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

K = 3
ROLES = {(2, "A6"): "routes", (3, "A2"): "boundaries"}


def _ids(payload: dict[str, Any]) -> list[str]:
    found: list[str] = []
    for value in payload.values():
        rows = value if isinstance(value, list) else [value]
        for row in rows:
            if isinstance(row, dict):
                found.extend(str(i) for i in row.get("evidence_ids") or [])
    return found


def _routes(payload: dict[str, Any]) -> dict[str, str]:
    out = {}
    for row in payload.get("decisions") or []:
        if isinstance(row, dict) and row.get("application_id") and row.get("proposed_disposition"):
            out[str(row["application_id"])] = str(row["proposed_disposition"])
    return out


def _boundaries(payload: dict[str, Any]) -> tuple[str, ...]:
    names = [str(row["boundary"]) for row in payload.get("boundaries") or []
             if isinstance(row, dict) and row.get("boundary")]
    return tuple(sorted(names))


def _option(sample: int, payload: dict[str, Any], choice: Any) -> dict[str, Any]:
    return {"sample": sample, "choice": choice, "evidence_ids": _ids(payload)}


def combine(phase: int, node: str, payloads: list[dict[str, Any]]) -> dict[str, Any]:
    """Vote ``payloads`` for one role. ``winner`` is a 1-based sample index, or None."""
    kind = ROLES[(phase, node)]
    usable = [(i, p) for i, p in enumerate(payloads, 1) if p]
    if kind == "routes":
        apps = sorted({app for _, payload in usable for app in _routes(payload)})
        winners: dict[str, str] = {}
        ratios = []
        for app in apps:
            votes = [routes[app] for _, payload in usable if (routes := _routes(payload)).get(app)]
            top = Counter(votes).most_common(1)
            if top and top[0][1] >= 2:
                winners[app] = top[0][0]
                ratios.append(top[0][1] / K)
        agreed = bool(apps) and len(winners) == len(apps)
        options = [_option(i, payload, _routes(payload)) for i, payload in usable]
        winner = next((i for i, payload in usable if _routes(payload) == winners), None) if agreed else None
    else:
        boundary_votes = [_boundaries(payload) for _, payload in usable]
        ranked = Counter(boundary_votes).most_common(1)
        agreed = bool(ranked) and ranked[0][1] >= 2 and bool(ranked[0][0])
        ratios = [ranked[0][1] / K] if ranked else []
        options = [_option(i, payload, list(_boundaries(payload))) for i, payload in usable]
        winner = next((i for i, payload in usable if _boundaries(payload) == ranked[0][0]), None) if agreed else None
    review = None
    if not agreed:
        review = {
            "role": f"P{phase}.{node}",
            "kind": kind,
            "question": f"{kind} disagreed across {K} independent samples",
            "options": options,
        }
    return {"agreed": agreed, "winner": winner, "agreement": (sum(ratios) / len(ratios) if ratios else 0.0),
            "review": review}
