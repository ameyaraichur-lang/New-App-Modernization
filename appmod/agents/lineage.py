"""Which model-authored field each non-critic P1–P4 role hands to a consumer.

``consumed_by`` is the contract: the named field is on the producer overlay, and
the consumer receives it. Same-phase consumers read it from their upstream
artifact. Cross-phase consumers read it from the lineage bundle on run inputs.
"""

from __future__ import annotations

from typing import Any

# (phase, node) -> (field, (consumer_phase, consumer_node))
LINEAGE: dict[tuple[int, str], tuple[str, tuple[int, str]]] = {
    (1, "A1"): ("module_map", (1, "A2")),
    (1, "A2"): ("relations", (1, "A9")),
    (1, "A3"): ("entities", (3, "A3")),
    (1, "A4"): ("runtime_profile", (1, "A2")),
    (1, "A5"): ("journeys", (1, "A7")),
    (1, "A6"): ("control_findings", (3, "A4")),
    (1, "A7"): ("criteria", (1, "G1")),
    (1, "A8"): ("questions_drafted", (1, "G2")),
    (1, "A9"): ("processes", (1, "G1")),
    (1, "A11"): ("risk_dimensions", (1, "G2")),
    (2, "A1"): ("value_assessments", (2, "A4")),
    (2, "A2"): ("complexity_drivers", (2, "A3")),
    (2, "A3"): ("assumptions", (2, "G1")),
    (2, "A4"): ("overlap", (2, "A5")),
    (2, "A5"): ("blocker_deltas", (2, "G1")),
    (2, "A6"): ("decisions", (2, "A7")),
    (3, "A1"): ("component_map", (3, "A2")),
    (3, "A2"): ("boundaries", (3, "A3")),
    (3, "A3"): ("schemas", (3, "A6")),
    (3, "A4"): ("threats", (3, "A3")),
    (3, "A5"): ("patterns", (3, "A6")),
    (3, "A6"): ("contract_registry", (3, "A7")),
    (3, "A7"): ("bom", (3, "G1")),
    (4, "A1"): ("replan_triggers", (4, "A2")),
    (4, "A2"): ("entry_exit_criteria", (4, "A3")),
    (4, "A3"): ("tasks", (4, "A4")),
    (4, "A4"): ("runbook_steps", (4, "G1")),
    (4, "A5"): ("assignments", (4, "G1")),
    (4, "A6"): ("tool_bindings", (4, "G1")),
    (4, "A7"): ("tests", (4, "A9")),
    (4, "A8"): ("recovery_plans", (4, "G1")),
}

CRITICS = {(1, "A10"), (2, "A7"), (3, "A8"), (4, "A9")}


def project(artifacts: dict[tuple[int, str], dict[str, Any]], consumer_phase: int,
            consumer: str) -> list[dict[str, Any]]:
    """Fields declared for this consumer, taken from already published payloads."""
    items = []
    for (phase, node), (field, (cphase, cnode)) in LINEAGE.items():
        if (cphase, cnode) != (consumer_phase, consumer):
            continue
        payload = artifacts.get((phase, node)) or {}
        if field not in payload:
            continue
        items.append({"producer": f"P{phase}.{node}", "field": field,
                      "consumed_by": f"P{cphase}.{cnode}", "value": payload[field]})
    return items


def project_store(store: Any, app: str, consumer_phase: int) -> list[dict[str, Any]]:
    artifacts: dict[tuple[int, str], dict[str, Any]] = {}
    for phase, node in LINEAGE:
        if phase > consumer_phase:
            continue
        try:
            art = store.get(f"P{phase}/{app}/{node}")
        except Exception:
            continue
        artifacts[(phase, node)] = art.get("payload") or {}
    items = []
    for (phase, node), (field, (cphase, cnode)) in LINEAGE.items():
        if cphase != consumer_phase or (phase, node) not in artifacts:
            continue
        payload = artifacts[(phase, node)]
        if field not in payload:
            continue
        items.append({"producer": f"P{phase}.{node}", "field": field,
                      "consumed_by": f"P{cphase}.{cnode}", "consumer": cnode,
                      "value": payload[field]})
    return items
