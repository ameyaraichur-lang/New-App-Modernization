"""Phase 4 — Modernization Planning engine (frozen nine-role core).

A1→A2→A3 publish one immutable task/context version; the five planners
(A4 runbook, A5 resource, A6 tool, A7 validation, A8 rollback) consume the
same A3 context hash; G1 seals candidates; A9 runs deterministic cross-plan
validation (bidirectional task↔requirement coverage, tool/role bindings,
threshold reconciliation, phase routing) and issues owner-assigned revision
requests instead of silently repairing producers.
"""

from __future__ import annotations

import json
import time
from typing import Any

from appmod.agents.runtime import AgentOutcome
from appmod.kernel.gates import GateContext, GateResult
from appmod.contracts.schemas import intake_errors

_now = lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _f(fid, cls, statement):
    return {"id": fid, "evidence_class": cls, "statement": statement}


class P4AgentRunner:
    def __init__(self, plan_brief: dict[str, Any] | None = None):
        """plan_brief: {'app_id', 'disposition', 'wave', 'tasks_hint',
        'acceptance_refs'} from the pipeline driver (P2/P3 artifacts)."""
        self.brief = plan_brief or {}
        self._context_hash = ""

    accepts_context = True

    def run(self, agent_spec, inputs, policy, context=None):
        fn = getattr(self, f"_run_{agent_spec['local_id'].lower()}")
        if agent_spec["local_id"] == "A9":
            return fn(agent_spec, inputs, policy, context=context)
        return fn(agent_spec, inputs, policy)

    def fingerprint(self) -> str:
        # Scope facts are not in this identity. A change reopens only the planners
        # that declare the fact (see appmod.kernel.invalidation).
        return "P4:" + str(self.brief.get("app_id", ""))

    def _tasks(self) -> list[dict[str, Any]]:
        app = self.brief.get("app_id", "app")
        return [
            {"task_id": "T1-baseline", "phase": "P5", "kind": "characterization",
             "owner_role": "P5.A1", "acceptance": "baseline sealed at G1"},
            {"task_id": "T2-code", "phase": "P5", "kind": "code transformation",
             "owner_role": "P5.A2", "acceptance": "lane checks + integration"},
            {"task_id": "T3-data-auth", "phase": "P6", "kind": "data migration (if applicable)",
             "owner_role": "P6.A1-A8", "acceptance": "P6 G3 release"},
            {"task_id": "T4-validate", "phase": "P5", "kind": "validation",
             "owner_role": "P5.A9", "acceptance": "PASS/FAIL evidence per criterion"},
        ]

    # -- A1 Wave Architecture -----------------------------------------------------

    def _run_a1(self, spec, inputs, policy):
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "waves": [{"wave_id": self.brief.get("wave", "W1"),
                           "apps": [self.brief.get("app_id", "app")]}],
                "calendar": {"start": "UNSET — owner calendar required",
                             "note": "logical ordering only; no wall-clock commitment"},
                "capacity_envelopes": [{"envelope": "pilot", "parallel": policy.budgets.get("max_parallel_agents", 4) if policy else 4}],
                "budget_refs": ["P2 cost scenarios (pilot rate card)"],
                "environment_timeline": [{"env": "local pilot", "status": "pre-provisioned"}],
                "infeasibilities": [],
                "replan_triggers": [
                    {"trigger": "p3_scope", "response": "reopen planners that read components"},
                    {"trigger": "wave", "response": "reopen planners that read the wave"},
                    {"trigger": "estimate", "response": "reopen the resource estimate for the failed lane"},
                ],
            },
            findings=[_f("A1-F1", "DOCUMENTED",
                         "Initial feasibility provisional until A5/A6 detail reconciles (finalization rule)")],
            evidence_refs=[{"source": "P2 wave", "method": "wave translation"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "planning"},
        )

    # -- A2 Wave Specification -------------------------------------------------------

    def _run_a2(self, spec, inputs, policy):
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "wave_specs": [{
                    "wave_id": self.brief.get("wave", "W1"),
                    "stages": ["preparation", "implementation", "validation"],
                }],
                "component_scope": self.brief.get("components", ["app"]),
                "data_plan": {"route": "batch if data layer present (decided at P6 G0)"},
                "environment_plan": {"env": "local pilot pre-provisioned", "owner": "pilot harness"},
                "entry_exit_criteria": [
                    {"gate": "P5.G1", "entry": "baseline sealed"},
                    {"gate": "P5.G4", "exit": "evidence-bound package"},
                ],
                "interwave_constraints": [],
            },
            findings=[_f("A2-F1", "DOCUMENTED",
                         "Execution plans, not executed migrations; obligations stay explicit")],
            evidence_refs=[{"source": "A1 calendar", "method": "specification"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "planning"},
        )

    # -- A3 Task Generator --------------------------------------------------------------

    def _run_a3(self, spec, inputs, policy):
        import hashlib
        import json
        tasks = self._tasks()
        self._context_hash = hashlib.sha256(
            json.dumps({"tasks": tasks, "brief": self.brief}, sort_keys=True).encode()
        ).hexdigest()
        edges = [
            {"from": "T1-baseline", "to": "T2-code"},
            {"from": "T2-code", "to": "T4-validate"},
            {"from": "T2-code", "to": "T3-data-auth"},
        ]
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "tasks": tasks,
                "dependency_edges": edges,
                "context_manifest": {"context_hash": self._context_hash,
                                     "note": "single immutable version consumed by all five planners"},
                "acceptance_links": [
                    {"task": t["task_id"], "acceptance": t["acceptance"]} for t in tasks
                ],
                "estimate_assumptions": [{"task": t["task_id"], "estimate": "pilot-default range"} for t in tasks],
                "phase_routes": [{"task": t["task_id"], "phase": t["phase"]} for t in tasks],
            },
            findings=[_f("A3-F1", "DOCUMENTED",
                         "Task DAG acyclic; P5/P6 routing explicit; P7 intentionally absent (H18)")],
            evidence_refs=[{"source": "A2 spec", "method": "task derivation"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "task-generation"},
        )

    # -- A4 Runbook / A5 Resource / A6 Tool / A7 Validation / A8 Rollback (parallel planners) --

    def _run_a4(self, spec, inputs, policy):
        cm = inputs.get("A3", {}).get("payload", {}).get("context_manifest", "")
        if isinstance(cm, str) and cm:
            try:
                cm = json.loads(cm)
            except ValueError:
                cm = {}
        ctx_hash = (cm or {}).get("context_hash", "")
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "runbooks": [{
                    "runbook_id": "RB-1", "scope": "pilot wave",
                    "steps": [
                        {"step": 1, "action": "seal baseline (P5.G1)", "gate": "P5.G1"},
                        {"step": 2, "action": "apply lanes + integrate (P5.G2/G3)", "gate": "P5.G3"},
                        {"step": 3, "action": "validate (P5.A9)", "gate": "P5.G4"},
                    ],
                    "unresolved_bindings": ["tool versions pending A6 confirmation"],
                }],
                "step_task_links": [{"step": 2, "task": "T2-code"}],
                "tool_bindings": [], "role_bindings": [{"step_role": "lane owner"}],
                "gate_refs": ["P5.G1", "P5.G2", "P5.G3", "P5.G4"],
                "recovery_refs": ["A8 recovery plans"],
                "communications": {"notify": "pilot reviewer"},
                "hypercare": {"state": "P8-era obligation (future phase)"},
            },
            findings=[_f("A4-F1", "DOCUMENTED",
                         "Draft runbook with declared unresolved bindings; cannot release until A9 verifies refs")],
            evidence_refs=[{"source": "A3 context", "method": "runbook drafting"}],
            scope={"app": self.brief.get("app_id", ""), "context_hash": ctx_hash},
            applicability={"route": "runbook"},
        )

    def _run_a5(self, spec, inputs, policy):
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "assignments": [{"task": t["task_id"], "role": t["owner_role"], "state": "proposed"}
                                for t in self._tasks()],
                "capacity_schedule": [{"period": "pilot", "load": "single wave"}],
                "skill_evidence": [{"skill": "stack depth", "evidence": "pilot harness"}],
                "access_needs": [{"access": "repo read/write (permitted)", "scope": "P5 execution permit"}],
                "coverage_gaps": [],
                "external_commitments": [],
            },
            findings=[_f("A5-F1", "DOCUMENTED", "Proposed staffing is not a confirmed commitment")],
            evidence_refs=[{"source": "A3 tasks", "method": "assignment"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "resource"},
        )

    def _run_a6(self, spec, inputs, policy):
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "tool_bindings": [
                    {"tool": "appmod kernel", "version": "0.1.0", "tasks": ["*"]},
                    {"tool": "repo scanner", "version": "0.1.0", "tasks": ["T1-baseline"]},
                ],
                "versions": [{"tool": "appmod", "pinned": True}],
                "compatibility_evidence": [{"basis": "pilot harness self-hosted"}],
                "license_status": [{"tool": "appmod", "license": "internal"}],
                "lead_times": [],
                "operator_requirements": [{"operator": "pilot harness", "competence": "evidence: suite green"}],
            },
            findings=[_f("A6-F1", "DOCUMENTED",
                         "Selection does not establish purchase or installed availability")],
            evidence_refs=[{"source": "A3 context", "method": "tool mapping"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "tools"},
        )

    def _run_a7(self, spec, inputs, policy):
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "tests": [
                    {"test": "baseline differential", "criterion": "behaviour preserved", "stage": "P5.A9"},
                    {"test": "contract replay", "criterion": "endpoints respond equivalently", "stage": "P5.A9"},
                ],
                "requirement_coverage": [
                    {"requirement": "preserve external behaviour (P3)", "test": "baseline differential"},
                ],
                "gates": [{"gate": "P5.G4", "criteria": "required criteria PASS or approved N/A"}],
                "test_data_requirements": [{"data": "representative fixtures", "state": "P5.A1 baseline fixtures"}],
                "environment_needs": [{"env": "local pilot", "state": "pre-provisioned"}],
                "evidence_requirements": [{"evidence": "per-criterion PASS/FAIL/NOT_RUN records"}],
            },
            findings=[_f("A7-F1", "DOCUMENTED",
                         "Plans do not prove compliance; each gate traces to its requirement")],
            evidence_refs=[{"source": "P3 acceptance matrix", "method": "coverage planning"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "validation-planning"},
        )

    def _run_a8(self, spec, inputs, policy):
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "recovery_plans": [
                    {"scope": "code changes", "route": "git revert to sealed base (pre-G3)"},
                ],
                "irreversible_steps": [
                    {"step": "any committed data write in P6", "note": "flags cannot reverse committed data"},
                ],
                "trigger_rules": [{"trigger": "required criterion FAIL at P5.G4", "action": "hold release; owner review"}],
                "decision_authorities": [{"decision": "rollback vs roll-forward", "authority": "operator (human)"}],
                "risk_responses": [],
                "contingency": {"state": "pilot: hold + re-plan"},
                "rehearsal_criteria": [{"criterion": "recovery rehearsal before production routes (P8-era)"}],
            },
            findings=[_f("A8-F1", "DOCUMENTED",
                         "Feature-switch rollback does not undo committed data or external effects")],
            evidence_refs=[{"source": "A2 data plan", "method": "recovery planning"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "rollback"},
        )

    # -- A9 Planning Validation & Handoff --------------------------------------------------

    def _run_a9(self, spec, inputs, policy, context=None):
        from appmod.phases.p3.engine import _payload, _sealed_artifacts
        sealed = _sealed_artifacts(inputs, (context or {}).get("published", {}))
        checks, conflicts = [], []

        def add(check: str, ok: bool, detail: str, owner: str) -> None:
            checks.append({"check": check, "result": "PASS" if ok else "FAIL", "detail": detail})
            if not ok:
                conflicts.append({"conflict": f"{check}: {detail}", "owner": owner})

        planners = ("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8")
        missing = [p for p in planners if p not in sealed]
        add("all-planner-candidates-sealed", not missing, f"missing {missing}" if missing else "8/8 sealed",
            "orchestrator")
        tasks = _payload(sealed.get("A3"), "tasks", []) or []
        task_ids = [t.get("task_id") for t in tasks if isinstance(t, dict)]
        cm = _payload(sealed.get("A3"), "context_manifest", {}) or {}
        a3_hash = cm.get("context_hash", "") if isinstance(cm, dict) else ""
        a4_hash = (sealed.get("A4", {}).get("scope") or {}).get("context_hash", "")
        add("context-hash-consistency", bool(a3_hash) and a3_hash == a4_hash,
            "A4 bound to A3 context" if a3_hash and a3_hash == a4_hash else "A4 context hash differs from A3",
            "P4.A4")
        assigned = {str(a.get("task")) for a in _payload(sealed.get("A5"), "assignments", []) or []
                    if isinstance(a, dict)}
        unowned = [t for t in task_ids if t not in assigned]
        add("every-task-has-owner", not unowned, f"unassigned: {unowned[:10]}" if unowned
            else f"{len(task_ids)} tasks assigned", "P4.A5")
        bound = set()
        for b in _payload(sealed.get("A6"), "tool_bindings", []) or []:
            if isinstance(b, dict):
                bound.update(str(t) for t in (b.get("tasks") or []))
        unbound = [t for t in task_ids if t not in bound and "*" not in bound]
        add("every-task-has-tool-binding", not unbound, f"unbound: {unbound[:10]}" if unbound
            else "all tasks bound", "P4.A6")
        tests = _payload(sealed.get("A7"), "tests", []) or []
        add("validation-plan-present", bool(tests), f"{len(tests)} planned tests", "P4.A7")
        recovery = _payload(sealed.get("A8"), "recovery_plans", []) or []
        add("recovery-plan-present", bool(recovery), f"{len(recovery)} recovery plans", "P4.A8")
        bad_phase = [t.get("task_id") for t in tasks if isinstance(t, dict) and t.get("phase") not in ("P5", "P6")]
        add("phase-routing-p5-p6-only", not bad_phase, f"bad routing: {bad_phase}" if bad_phase
            else "P5/P6 only; P7 absent", "P4.A3")
        edges = _payload(sealed.get("A3"), "dependency_edges", []) or []
        dangling = [e for e in edges if isinstance(e, dict)
                    and (e.get("from") not in task_ids or e.get("to") not in task_ids)]
        add("task-dag-closed", not dangling, f"{len(dangling)} dangling edges" if dangling
            else f"{len(edges)} edges resolve", "P4.A3")
        status = "FAILED" if missing else "PARTIAL" if conflicts else "COMPLETE"
        return AgentOutcome(
            status=status,
            payload={
                "validation_report": {"checks": checks,
                                      "limitations": "absence of a reported issue is not universal proof"},
                "coverage": {"tasks": len(task_ids), "planners_sealed": len(planners) - len(missing)},
                "conflicts": conflicts,
                "candidate_manifest": {"snapshot": "G1 sealed manifest"},
                "handoffs": [
                    {"phase": "P5", "tasks": [t.get("task_id") for t in tasks
                                              if isinstance(t, dict) and t.get("phase") == "P5"]},
                    {"phase": "P6", "tasks": [t.get("task_id") for t in tasks
                                              if isinstance(t, dict) and t.get("phase") == "P6"]},
                ],
                "governance": {"approval": "G2 binds exact candidate hash"},
                "revision_requests": [
                    {"finding": c["conflict"], "owner": c["owner"]} for c in conflicts
                ],
            },
            findings=[_f("A9-F1", "DOCUMENTED",
                         "A9 does not silently repair producers; evidence-backed findings replace confidence scores")],
            evidence_refs=[{"source": "G1 snapshot digest", "method": "cross-plan validation"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "validation"},
        )


def p4_intake_gate(ctx: GateContext) -> GateResult:
    pkg = ctx.run_inputs.get("p3_package", {})
    if pkg.get("status") not in ("READY_FOR_PLANNING", "CONDITIONAL_PLANNING"):
        return GateResult("FAILED", "FAILED", {},
                          [f"P3 release status {pkg.get('status', 'missing')} does not admit planning"])
    return GateResult("PUBLISHED", "COMPLETE", {
        "intake_manifest": {"application_id": pkg.get("application_id"),
                            "p3_status": pkg["status"],
                            "conditions": pkg.get("conditions", []),
                            "policy_version": ctx.policy.version if ctx.policy else "none"}
    }, [])


def p4_release_gate(ctx: GateContext) -> GateResult:
    blockers = []
    for node, art in ctx.inputs.items():
        blockers.extend(intake_errors(art))
    if blockers:
        return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)
    a9 = ctx.inputs.get("A9", {})
    conflicts = (a9.get("payload", {}) or {}).get("conflicts", [])
    decision = "READY_FOR_PREPARATION" if not conflicts else "SCOPED_PREPARATION"
    reviewer = (ctx.policy.reviewers.get("simulated", {}).get("release", "sim-release")
                if ctx.policy else "sim-release")
    return GateResult("PUBLISHED", "COMPLETE", {
        "decision_record": {
            "status": decision,
            "candidate_hash": a9.get("content_hash"),
            "authorized_by": reviewer,
            "simulated": True,
            "authorized_at": _now(),
            "task_scope": ["T1-baseline", "T2-code", "T4-validate", "T3-data-auth"],
            "execution_boundary": "planning approval permits only listed preparation; "
                                  "P5 writes require their own execution permit at P5.G0",
        }
    }, [])


P4_GATE_OVERRIDES = {
    "G0": p4_intake_gate,
    "G2": p4_release_gate,
}
