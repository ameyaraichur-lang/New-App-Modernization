"""Typed critique requests and the two-round rerun rule.

P1.A10 contradictions, P2.A7 disagreements, P3.A8 consistency issues and P4.A9
revision requests name a target agent. The orchestrator re-runs that agent with
the critique, at most twice. A third occurrence is escalated instead of rerun.
"""

from __future__ import annotations

from typing import Any

MAX_ROUNDS = 2

CRITICS = {
    (1, "A10"): ("contradictions",),
    (2, "A7"): ("disagreements",),
    (3, "A8"): ("consistency_issues",),
    (4, "A9"): ("revision_requests", "conflicts"),
}


def _local_id(value: Any, nodes: set[str]) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    local = value.strip().split(".")[-1]
    return local if local in nodes else None


def _statement(item: dict[str, Any]) -> str:
    for key in ("statement", "issue", "finding", "conflict"):
        if item.get(key):
            return str(item[key])[:500]
    return ""


def _target(item: dict[str, Any], nodes: set[str]) -> str | None:
    for key in ("target", "owner"):
        found = _local_id(item.get(key), nodes)
        if found:
            return found
    for key in ("between", "artifacts"):
        for entry in item.get(key) or []:
            found = _local_id(entry, nodes)
            if found:
                return found
    return None


def critique_requests(phase: int, node: str, payload: dict[str, Any],
                      nodes: set[str]) -> list[dict[str, str]]:
    fields = CRITICS.get((phase, node))
    if not fields:
        return []
    out: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for field in fields:
        for item in payload.get(field) or []:
            if not isinstance(item, dict):
                continue
            target = _target(item, nodes)
            statement = _statement(item)
            if target is None or not statement or (target, statement) in seen:
                continue
            seen.add((target, statement))
            out.append({"source": node, "target": target, "statement": statement})
    return out
