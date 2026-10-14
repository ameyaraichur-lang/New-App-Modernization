"""The model authors structural fields. The engine validates and falls back to the seed.

First-pass validity means the model's structure was accepted with no repair and no
seed substitution. An invalid structure publishes the seed, so the contract (C1)
still holds.
"""

from __future__ import annotations

from typing import Any

CHANGES = {"keep", "upgrade", "replace", "split", "merge", "retire"}
SCHEMA_ACTIONS = {"keep", "align", "split", "merge", "retire"}
PHASES = {"P5", "P6"}


def _rows(value: Any, required: set[str], enums: dict[str, set[str]] | None = None) -> bool:
    if not isinstance(value, list) or not value:
        return False
    for row in value:
        if not isinstance(row, dict) or not required <= set(row):
            return False
        for key in required:
            if key in (enums or {}):
                continue
            if isinstance(row.get(key), list):
                if key == "modules" and not row[key]:
                    return False
                continue
            if not str(row.get(key) or "").strip():
                return False
        for key, allowed in (enums or {}).items():
            if row.get(key) not in allowed:
                return False
    return True


def accept_component_map(rows: Any) -> bool:
    return _rows(rows, {"component", "current", "target", "change"}, {"change": CHANGES})


def accept_boundaries(rows: Any) -> bool:
    return _rows(rows, {"boundary", "modules", "justification"})


def accept_schemas(rows: Any) -> bool:
    return _rows(rows, {"object", "action", "detail"}, {"action": SCHEMA_ACTIONS})


def accept_tasks(rows: Any) -> bool:
    if not _rows(rows, {"task_id", "phase", "kind", "owner_role", "acceptance", "depends_on"},
                 {"phase": PHASES}):
        return False
    ids = {row["task_id"] for row in rows}
    if len(ids) != len(rows):
        return False
    edges: list[tuple[str, str]] = []
    for row in rows:
        deps = row["depends_on"]
        if not isinstance(deps, list) or any(dep not in ids or dep == row["task_id"] for dep in deps):
            return False
        edges.extend((dep, row["task_id"]) for dep in deps)
    return _acyclic(edges)


def _acyclic(edges: list[tuple[str, str]]) -> bool:
    adj: dict[str, set[str]] = {}
    for src, dst in edges:
        adj.setdefault(src, set()).add(dst)

    def reaches(start: str, goal: str) -> bool:
        stack, seen = [start], set()
        while stack:
            current = stack.pop()
            if current == goal:
                return True
            if current in seen:
                continue
            seen.add(current)
            stack.extend(adj.get(current, ()))
        return False

    for src, dst in edges:
        if reaches(dst, src):
            return False
    return True


def author_list(seed: dict[str, Any], model: dict[str, Any], field: str,
                accept) -> tuple[dict[str, Any], bool]:
    """Replace ``field`` when the model list is valid. Otherwise keep the seed."""
    out = dict(seed)
    rows = model.get(field)
    if accept(rows):
        out[field] = rows
        return out, True
    return out, False
