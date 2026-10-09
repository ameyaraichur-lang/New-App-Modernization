"""Gate service: deterministic evaluation + human decision capture.

Blueprint: gates are deterministic services/review steps, never model agents.
Release-style gates bind reviewer identity/time/policy/scope to the exact
candidate hash ('A11 recommendation or model confidence cannot authorize
release alone'). Pilot runs use simulated reviewer principals whose events
are always recorded with simulated=true.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from appmod.contracts.schemas import canonical_json, intake_errors


@dataclass
class GateResult:
    outcome: str                      # PUBLISHED | FAILED | BLOCKED
    status: str                       # artifact status (COMPLETE / FAILED / ...)
    payload: dict[str, Any]
    reasons: list[str] = field(default_factory=list)


class GenericGates:
    """Phase-agnostic gate implementations.

    Phase engines (M1+) override predicates via `overrides`; the generic
    versions already enforce the cross-phase invariants:

    G0 intake   — policy present, intake package fields, scope manifest
    G1 snapshot — every named producer published & consumable; async lanes
                  allowed PENDING with an explicit marker; manifest hash-sealed
    G2 release  — no FAILED/missing mandatory inputs in the referenced
                  snapshot; reviewer decision bound to candidate hash
    """

    # -- G0 ------------------------------------------------------------------

    @staticmethod
    def intake_gate(ctx: "GateContext") -> GateResult:
        reasons: list[str] = []
        if ctx.policy is None:
            reasons.append("missing policy bundle (Run Controls G0: required configuration)")
        if not ctx.run_inputs.get("scope_manifest"):
            reasons.append("missing scope manifest (workload IDs, boundaries, route)")
        if reasons:
            return GateResult("FAILED", "FAILED", {}, reasons)
        payload = {
            "intake_manifest": {
                "scope": ctx.run_inputs["scope_manifest"],
                "policy_version": ctx.policy.version,
                "source_pins": ctx.run_inputs.get("source_pins", {}),
            }
        }
        return GateResult("PUBLISHED", "COMPLETE", payload, [])

    # -- G1 snapshot -----------------------------------------------------------

    @staticmethod
    def snapshot_gate(ctx: "GateContext") -> GateResult:
        """ctx.required_producers: nodes whose artifacts must be in the seal.
        Producers may be transitive (workbook G1 rows say 'A3+A5; transitive
        A1–A5'), so the seal considers every published artifact of the run."""
        required: list[str] = ctx.gate_cfg.get("required_producers", [])
        allow_pending: list[str] = ctx.gate_cfg.get("allow_pending", [])
        available = dict(ctx.published or {})
        available.update(ctx.inputs)
        refs: dict[str, Any] = {}
        blockers: list[str] = []
        for node, art in available.items():
            errs = intake_errors(art)
            if errs:
                blockers.extend(errs)
                continue
            refs[node] = {
                "artifact_id": art["artifact_id"],
                "version": art["artifact_version"],
                "status": art["status"],
                "content_hash": art["content_hash"],
            }
        for node in required:
            if node not in refs and node not in allow_pending:
                blockers.append(f"required producer {node} missing from snapshot")
        for node in allow_pending:
            if node not in refs:
                refs[node] = {"state": "PENDING", "rule": "async lane; never blocks fan-in"}

        if blockers:
            return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)

        manifest_hash = hashlib.sha256(canonical_json(refs).encode()).hexdigest()
        digest = {
            node: {"status": art.get("status"),
                   "route": (art.get("applicability") or {}).get("route")
                   if isinstance(art.get("applicability"), dict) else None}
            for node, art in available.items()
        }
        payload = {
            "evidence_manifest": {
                "artifact_refs": refs,
                "snapshot_digest": digest,
                "manifest_hash": manifest_hash,
                "policy_version": ctx.policy.version if ctx.policy else "none",
                "sealed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
        }
        return GateResult("PUBLISHED", "COMPLETE", payload, [])

    # -- release gates (G2/G3/G4) -----------------------------------------------

    @staticmethod
    def release_gate(ctx: "GateContext") -> GateResult:
        """ctx.gate_cfg: {'decision_values': [...], 'default': ...}
        Evaluates blockers from inputs (candidate chain), then records the
        reviewer decision bound to the candidate hash."""
        blockers: list[str] = []
        for node, art in ctx.inputs.items():
            errs = intake_errors(art)
            blockers.extend(errs)
        if blockers:
            return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)

        candidate = ctx.gate_cfg.get("candidate_node")
        cand = ctx.inputs.get(candidate) if candidate else None
        cand_hash = cand["content_hash"] if cand else None

        reviewer = (ctx.policy.reviewers.get("simulated", {}).get("release", "sim-release")
                    if ctx.policy else "sim-release")
        decision_values = ctx.gate_cfg.get(
            "decision_values",
            ["HOLD", "READY_FOR_PORTFOLIO_DRAFT", "READY_FOR_PORTFOLIO_DECISION"],
        )
        # generic pilot rule: everything consumable -> widest permitted decision
        decision = ctx.gate_cfg.get("default", decision_values[-1])
        payload = {
            "decision_record": {
                "status": decision,
                "candidate_ref": cand["artifact_id"] if cand else None,
                "manifest_hash": cand_hash,
                "policy_version": ctx.policy.version if ctx.policy else "none",
                "authorized_by": reviewer,
                "simulated": True,  # pilot reviewer — always labeled
                "authorized_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "restrictions": [],
                "accepted_exceptions": [],
            }
        }
        return GateResult("PUBLISHED", "COMPLETE", payload, [])


@dataclass
class GateContext:
    run_id: str
    application_id: str
    gate_id: str
    policy: Any                      # PolicyService | None
    inputs: dict[str, dict]          # node_id -> artifact envelope (edge-connected)
    run_inputs: dict[str, Any]       # orchestrator-supplied run inputs (scope manifest...)
    gate_cfg: dict[str, Any] = field(default_factory=dict)
    published: dict[str, dict] = field(default_factory=dict)  # ALL published artifacts this run


GATE_IMPLS: dict[str, Callable[[GateContext], GateResult]] = {
    "G0": GenericGates.intake_gate,
    "G1": GenericGates.snapshot_gate,
}
for _g in ("G2", "G3", "G4"):
    GATE_IMPLS[_g] = GenericGates.release_gate


def gate_impl_for(gate_id: str) -> Callable[[GateContext], GateResult]:
    if gate_id not in GATE_IMPLS:
        raise KeyError(f"no gate implementation for {gate_id}")
    return GATE_IMPLS[gate_id]
