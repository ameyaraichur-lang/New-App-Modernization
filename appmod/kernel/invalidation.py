"""Replan predicates: new evidence reopens only the P4 planners that read it.

An answer, critique, or upstream revision names the facts it changes. Each planner
declares the facts it reads. Downstream planners reopen because their upstream
artifact version changes; planners that do not read the fact stay reusable.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from appmod.contracts.schemas import canonical_json
from appmod.store.artifact_store import ArtifactStore

# Facts a planner reads directly. Downstream nodes are not listed; a new version
# of a dependency reopens them through the normal input hash.
NODE_FACTS: dict[str, frozenset[str]] = {
    "A1": frozenset({"wave"}),
    "A2": frozenset({"components", "wave"}),
    "A3": frozenset({"components", "wave", "disposition"}),
    "A5": frozenset({"estimate"}),
}

REPLAN_TRIGGERS = (
    {"trigger": "p3_scope", "response": "reopen planners that read components",
     "fact": "components"},
    {"trigger": "wave", "response": "reopen planners that read the wave",
     "fact": "wave"},
    {"trigger": "estimate", "response": "reopen the resource estimate for the failed lane",
     "fact": "estimate"},
)

_EVENT_KEYS = ("kind", "changes", "lane", "target", "statement", "components", "wave",
               "disposition", "estimate")


def events_from_answers(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """JSON answers may declare ``changes`` (for example ``["components"]``)."""
    events = []
    for question in questions:
        if question.get("status") != "ANSWERED":
            continue
        try:
            data = json.loads(question.get("answer") or "")
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict) or not data.get("changes"):
            continue
        event: dict[str, Any] = {"kind": "answer"}
        for key in _EVENT_KEYS:
            if key in data:
                event[key] = data[key]
        event["changes"] = list(data["changes"])
        events.append(event)
    return events


def lane_failure_events(lanes: dict[str, Any]) -> list[dict[str, Any]]:
    events = []
    for lane, info in sorted(lanes.items()):
        status = info.get("status") if isinstance(info, dict) else info
        if status == "FAILED":
            events.append({"kind": "execution_failure", "changes": ["estimate"], "lane": lane})
    return events


def _apply(scope: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    merged = dict(scope)
    for event in events:
        for fact in event.get("changes") or []:
            if fact in event:
                merged[fact] = event[fact]
    return merged


def scope_token(node: str, run_inputs: dict[str, Any]) -> str:
    """Stable per-planner identity of the facts and events that planner reads."""
    facts = NODE_FACTS.get(node, frozenset())
    events = list(run_inputs.get("replan_events") or [])
    scope = _apply(run_inputs.get("scope") or {}, events)
    parts: dict[str, Any] = {fact: scope.get(fact) for fact in sorted(facts)}
    relevant = []
    for event in events:
        if event.get("kind") == "critique" and event.get("target") == node:
            relevant.append({k: event.get(k) for k in ("kind", "target", "statement")})
        elif facts.intersection(event.get("changes") or []):
            relevant.append({k: event.get(k) for k in ("kind", "changes", "lane", "statement")
                             if k in event})
    if relevant:
        parts["events"] = relevant
    if not parts:
        return ""
    return hashlib.sha256(canonical_json(parts).encode()).hexdigest()[:16]


def affected_planners(run_inputs: dict[str, Any]) -> set[str]:
    """Planners whose scope token differs from the same inputs with no replan events."""
    baseline = {k: v for k, v in run_inputs.items() if k != "replan_events"}
    return {node for node in NODE_FACTS
            if scope_token(node, run_inputs) != scope_token(node, baseline)}


@dataclass
class InvalidationRecord:
    origin: tuple[str, int]
    new_version: int
    stale: list[dict[str, Any]] = field(default_factory=list)


class InvalidationEngine:
    """A new artifact version marks every consumer of an older version stale (H17)."""

    def __init__(self, store: ArtifactStore):
        self.store = store

    def supersede(self, artifact_id: str) -> InvalidationRecord:
        versions = self.store.versions(artifact_id)
        if len(versions) < 2:
            current = versions[-1] if versions else 0
            return InvalidationRecord((artifact_id, current), current, [])
        latest = versions[-1]
        stale: dict[tuple[str, int], dict[str, Any]] = {}
        for older in versions[:-1]:
            for desc in self.store.descendants_of(artifact_id, older):
                stale.setdefault((desc["artifact_id"], desc["artifact_version"]), desc)
        return InvalidationRecord((artifact_id, latest - 1), latest, list(stale.values()))

    def stale_for_run(self, run_id: str, record: InvalidationRecord) -> list[str]:
        return [d["artifact_id"] for d in record.stale if d.get("run_id") == run_id]
