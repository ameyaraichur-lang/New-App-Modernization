"""Live done-when checks that the Step 33 gate does not cover.

Each check reads finished artifacts, audit events, or report JSON.
A check with no observations does not pass.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from appmod.kernel.critique import MAX_ROUNDS
from appmod.retrieval.memory import AGENT_INPUT_TOKEN_CAP, over_budget

STRUCTURE_ROLES = ((2, "A6"), (3, "A1"), (3, "A2"), (3, "A3"), (4, "A3"))
FIRST_PASS_MIN = 0.95
CRITIQUE_MIN = 0.95
EVIDENCE_MIN = 60.0
ROUTE_MIN = 0.90
ROUTE_MEASURE = "P2 A6 disposition identical across runs"


def _rate(k: int, n: int) -> float | None:
    return k / n if n else None


def first_pass_validity(artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    """Share of the five structure roles whose latest artifact was valid on the first submission."""
    rows = [a for a in artifacts if (a.get("phase"), a.get("agent")) in STRUCTURE_ROLES]
    k = sum(1 for a in rows if (a.get("llm") or {}).get("first_pass_valid") is True)
    n = len(rows)
    rate = _rate(k, n)
    return {"k": k, "n": n, "rate": rate, "pass": rate is not None and rate >= FIRST_PASS_MIN}


def critique_convergence(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Share of critique requests that resolved within two reruns.

    An escalated request, or one still open at the end of the audit, did not converge.
    """
    items: dict[tuple[Any, ...], dict[str, Any]] = {}
    for ev in events:
        kind = ev.get("kind")
        if kind not in ("CRITIQUE_RERUN", "CRITIQUE_RESOLVED", "CRITIQUE_ESCALATED"):
            continue
        key = (ev.get("run_id"), ev.get("node"), ev.get("target"), ev.get("statement"))
        state = items.setdefault(key, {"state": "open", "rounds": 0})
        if kind == "CRITIQUE_ESCALATED":
            state["state"] = "escalated"
            state["rounds"] = int(ev.get("rounds") or state["rounds"])
        elif kind == "CRITIQUE_RESOLVED" and state["state"] != "escalated":
            state["state"] = "resolved"
            state["rounds"] = int(ev.get("rounds") or state["rounds"])
        elif kind == "CRITIQUE_RERUN" and state["state"] == "open":
            state["rounds"] = max(int(state["rounds"]), int(ev.get("round") or 0))
    n = len(items)
    k = sum(1 for s in items.values()
            if s["state"] == "resolved" and int(s["rounds"]) <= MAX_ROUNDS)
    rate = _rate(k, n)
    return {"k": k, "n": n, "rate": rate, "escalated": sum(1 for s in items.values()
                                                           if s["state"] == "escalated"),
            "pass": rate is not None and rate >= CRITIQUE_MIN}


def observed_share(evaluation: dict[str, Any], phases: tuple[str, ...] = ("P2", "P3"),
                   minimum: float = EVIDENCE_MIN) -> dict[str, Any]:
    """OBSERVED/DOCUMENTED share for the named phases. An empty phase is not a pass."""
    mix = evaluation.get("evidence_mix") or {}
    shares: dict[str, float | None] = {}
    ok = True
    for phase in phases:
        cell = mix.get(phase) or {}
        total = cell.get("total") or 0
        share = cell.get("share_pct") if total else None
        shares[phase] = share
        if share is None or share < minimum:
            ok = False
    return {"shares": shares, "minimum": minimum, "pass": ok}


def ofbiz_completed(e2e: dict[str, Any]) -> dict[str, Any]:
    """OFBiz published a successful artifact for every P1, P3, and P4 agent."""
    agents = [a for a in e2e.get("agents") or [] if a.get("app") == "ofbiz"]
    phases: dict[int, dict[str, Any]] = {}
    for phase in (1, 3, 4):
        rows = [a for a in agents if a.get("phase") == phase]
        phases[phase] = {"n": len(rows), "succeeded": sum(1 for a in rows if a.get("success") is True)}
    problems = over_budget(e2e, AGENT_INPUT_TOKEN_CAP)
    complete = all(p["n"] and p["succeeded"] == p["n"] for p in phases.values())
    return {"phases": phases, "over_budget": problems, "cap": AGENT_INPUT_TOKEN_CAP,
            "pass": complete and not problems}


def route_agreement(stability: dict[str, Any], minimum: float = ROUTE_MIN) -> dict[str, Any]:
    """P2 route agreement on a stability harness. The point estimate is k/n, not the lower bound."""
    for measure in stability.get("measures") or []:
        if measure.get("name") != ROUTE_MEASURE:
            continue
        n = int(measure.get("n") or 0)
        k = int(measure.get("k") or 0)
        rate = _rate(k, n)
        return {"k": k, "n": n, "rate": rate, "minimum": minimum,
                "pass": rate is not None and rate >= minimum}
    return {"k": 0, "n": 0, "rate": None, "minimum": minimum, "pass": False}


def read_audit(path: Path) -> list[dict[str, Any]]:
    files = [path] if path.is_file() else sorted(path.glob("audit-*.jsonl"))
    events: list[dict[str, Any]] = []
    for audit_file in files:
        for line in audit_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
    return events
