"""Evidence validator — kernel-side honesty rules applied to every outcome
before envelope assembly (the model never decides its own evidence class).

  E1  model claims OBSERVED/DOCUMENTED without a valid citation -> INFERRED
  E2  model claims HUMAN_CONFIRMED -> HYPOTHETICAL (only recorded human
      answers confirm; they enter through the questions store, not the model)
  E3  citations to ids not in the run's evidence ledger are stripped
  E4  COMPLETE with an open NOT_ASSESSED gap -> PARTIAL
  E5  configured secrets anywhere in the outcome are redacted
"""

from __future__ import annotations

import json
from typing import Any

from appmod.agents.runtime import AgentOutcome

CITED_CLASSES = ("OBSERVED", "DOCUMENTED")


def _fix_item(obj: dict[str, Any], known: set[str] | None, where: str,
              events: list[dict[str, Any]]) -> None:
    if obj.get("origin") != "llm" or "evidence_class" not in obj:
        return
    ids = obj.get("evidence_ids")
    if ids is None:
        ids = [r for r in obj.get("evidence_refs", []) if isinstance(r, str)]
    if known is not None:
        valid = [i for i in ids if i in known]
        if len(valid) != len(ids):
            events.append({"rule": "E3", "where": where, "stripped": sorted(set(ids) - set(valid))})
        ids = valid
        if "evidence_ids" in obj:
            obj["evidence_ids"] = valid
        if "evidence_refs" in obj:
            obj["evidence_refs"] = valid
    cls = obj["evidence_class"]
    if cls == "HUMAN_CONFIRMED":
        obj["evidence_class"] = "HYPOTHETICAL"
        events.append({"rule": "E2", "where": where, "from": cls, "to": "HYPOTHETICAL"})
    elif cls in CITED_CLASSES and not ids:
        obj["evidence_class"] = "INFERRED"
        events.append({"rule": "E1", "where": where, "from": cls, "to": "INFERRED"})


def enforce(outcome: AgentOutcome, secrets: list[str] | None = None) -> list[dict[str, Any]]:
    """Mutates ``outcome`` in place; returns the list of enforcement events."""
    events: list[dict[str, Any]] = []
    known = outcome.known_evidence
    for i, f in enumerate(outcome.findings):
        _fix_item(f, known, f"findings[{i}]", events)
    for key, value in (outcome.payload or {}).items():
        if isinstance(value, list):
            for j, it in enumerate(value):
                if isinstance(it, dict):
                    _fix_item(it, known, f"payload.{key}[{j}]", events)
        elif isinstance(value, dict):
            _fix_item(value, known, f"payload.{key}", events)

    if outcome.status == "COMPLETE" and any(
            isinstance(g, dict) and g.get("state") == "NOT_ASSESSED" for g in outcome.gaps):
        outcome.status = "PARTIAL"
        events.append({"rule": "E4", "where": "status", "from": "COMPLETE", "to": "PARTIAL"})

    if secrets:
        blob = json.dumps([outcome.payload, outcome.findings, outcome.gaps, outcome.notes],
                          default=str)
        if any(s in blob for s in secrets):
            for s in secrets:
                blob = blob.replace(json.dumps(s)[1:-1], "[REDACTED]")
            payload, findings, gaps, notes = json.loads(blob)
            outcome.payload, outcome.findings, outcome.gaps, outcome.notes = payload, findings, gaps, notes
            events.append({"rule": "E5", "where": "outcome", "action": "redacted configured secret"})
    return events
