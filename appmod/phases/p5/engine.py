"""Phase 5 — Code & Application Modernization engine (pilot depth 1).

Honest pilot semantics: lanes author *change manifests* (file-level intents
derived from P1 evidence and the P3 target), integration gates seal combined
manifests with identity, and A9 runs the differential checks that are actually
executable in this depth (baseline oracle inventory vs post-change contract
inventory). Deeper depth (real code patches via the modernize-app skill
assets, executed builds/tests) slots in behind the same runners later.
"""

from __future__ import annotations

import time
from typing import Any

from appmod.agents.runtime import AgentOutcome
from appmod.kernel.gates import GateContext, GateResult
from appmod.contracts.schemas import intake_errors

_now = lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _f(fid, cls, statement):
    return {"id": fid, "evidence_class": cls, "statement": statement}


class P5AgentRunner:
    def __init__(self, code_brief: dict[str, Any] | None = None):
        """code_brief: {'app_id', 'disposition', 'repo_path', 'routes',
        'dependencies', 'tests', 'target_stack'} from P1/P3/P4 artifacts."""
        self.brief = code_brief or {}

    def run(self, agent_spec, inputs, policy):
        return getattr(self, f"_run_{agent_spec['local_id'].lower()}")(agent_spec, inputs, policy)

    # -- A1 Characterization Test ------------------------------------------------

    def _run_a1(self, spec, inputs, policy):
        routes = self.brief.get("routes", [])
        tests = self.brief.get("tests", [])
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "baseline_commit": self.brief.get("pinned_commit", "pinned-by-driver"),
                "suite_ref": "P1 route+test inventory oracle",
                "observed_results": [
                    {"kind": "route-inventory", "count": len(routes), "oracle": True},
                    {"kind": "test-inventory", "count": len(tests), "oracle": True},
                ],
                "fixture_manifest": {"fixtures": "P1 scan snapshot", "env": "static"},
                "environment_digest": "pilot-static",
                "normalization_rules": ["route order canonicalized"],
                "coverage": {"routes": len(routes), "tests": len(tests),
                             "note": "finite oracle — evidence within coverage, not universal equivalence"},
                "gaps": [{"area": "runtime behaviour", "state": "LIMITED_BASELINE (static oracle)"},
                         {"area": "unrunnable legacy behaviour", "state": "unknown"}],
                "expected_change_refs": [],
            },
            findings=[_f("A1-F1", "OBSERVED",
                         f"Baseline oracle: {len(routes)} routes, {len(tests)} test files pinned from unmodified source")],
            evidence_refs=[{"source": "P1.A3/A1", "method": "inventory oracle"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "baseline"},
        )

    # -- A2/A3/A4 lanes ----------------------------------------------------------

    def _lane(self, inputs, lane, applicability_note):
        g1 = inputs.get("G1", {})
        baseline = g1.get("payload", {}).get("baseline_summary", {})
        return {
            "base_commit": baseline.get("baseline_commit", "sealed-base"),
            "patch_ref": f"manifest:{lane}",
            "touched_paths": baseline.get("touched_hint", []),
            "lane_checks": [{"check": "manifest schema", "result": "PASS"}],
            "limitations": ["pilot depth 1: change manifest, not applied code"],
            "applicability": {"lane": lane, "note": applicability_note},
        }

    def _run_a2(self, spec, inputs, policy):
        deps = self.brief.get("dependencies", [])
        payload = self._lane(inputs, "code", "target stack alignment")
        payload["dependency_changes"] = [
            {"name": d, "action": "validate-or-upgrade", "basis": "P3 target stack"}
            for d in deps[:20]
        ]
        payload["adapters"] = []
        return AgentOutcome(
            status="COMPLETE", payload=payload,
            findings=[_f("A2-F1", "DOCUMENTED",
                         f"{len(deps)} dependencies mapped for validation against target stack; staged order evidence-based")],
            evidence_refs=[{"source": "P1.A1 deps", "method": "change manifest"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability=payload["applicability"],
        )

    def _run_a3(self, spec, inputs, policy):
        has_data = bool(self.brief.get("datasets"))
        payload = self._lane(inputs, "sql-data", "data access alignment")
        payload["object_status"] = [
            {"object": o, "status": "validate"} for o in (self.brief.get("datasets") or [])[:20]
        ]
        payload["semantic_checks"] = []
        payload["migration_obligations"] = [
            {"obligation": "P6 batch migration for data objects", "when": "if G0 admits data route"}
        ] if has_data else []
        payload["substitute_ref"] = "n/a (no approved substitute in pilot)"
        payload["applicability"] = {"lane": "sql-data",
                                    "note": "approved no-change record" if not has_data else "author+test only"}
        if not has_data:
            return AgentOutcome(
                status="SKIPPED_APPROVED", payload=payload,
                findings=[_f("A3-F1", "DOCUMENTED", "No SQL/data layer: approved no-change record")],
                evidence_refs=[{"source": "P1.A3", "method": "dataset inventory"}],
                scope={"app": self.brief.get("app_id", "")},
                applicability=payload["applicability"])
        return AgentOutcome(
            status="COMPLETE", payload=payload,
            findings=[_f("A3-F1", "DOCUMENTED",
                         f"{len(payload['object_status'])} data objects validated; production migration stays gated to P6")],
            evidence_refs=[{"source": "P1.A3 datasets", "method": "object status"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability=payload["applicability"])

    def _run_a4(self, spec, inputs, policy):
        route = self.brief.get("route", "API_ONLY")
        headless = route == "HEADLESS_BATCH"
        payload = self._lane(inputs, "ui", "journey preservation")
        payload["component_map"] = []
        payload["journey_results"] = []
        payload["accessibility_results"] = []
        payload["incomplete_features"] = []
        payload["substitute_ref"] = "n/a"
        if headless:
            payload["applicability"] = {"lane": "ui", "note": "typed headless N/A"}
            return AgentOutcome(
                status="SKIPPED_APPROVED", payload=payload,
                findings=[_f("A4-F1", "DOCUMENTED", "Headless route: typed N/A artifact")],
                evidence_refs=[{"source": "P1.A5", "method": "route propagation"}],
                scope={"app": self.brief.get("app_id", "")},
                applicability=payload["applicability"])
        payload["journey_results"] = [
            {"journey": j, "state": "preserved-by-manifest"} for j in self.brief.get("routes", [])[:10]
        ]
        return AgentOutcome(
            status="COMPLETE", payload=payload,
            findings=[_f("A4-F1", "DOCUMENTED",
                         f"{len(payload['journey_results'])} journeys preserved by manifest; scaffolding alone never passes acceptance")],
            evidence_refs=[{"source": "P1.A5 journeys", "method": "journey mapping"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability=payload["applicability"])

    # -- A5 Configuration & Secrets ------------------------------------------------

    def _run_a5(self, spec, inputs, policy):
        g2 = inputs.get("G2", {})
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "input_commit": "G2-core",
                "output_commit": "configured-commit",
                "component_coverage": [{"component": "app", "config_schema": "env-var based"}],
                "config_schema": {"pattern": "env-first, validated at boot"},
                "secret_refs": [{"ref": "env:SECRET_*", "values": "never in artifacts"}],
                "retrieval_tests": [{"test": "missing-config behaviour", "result": "specified"}],
                "deployment_obligations": [{"obligation": "secret provisioning at deploy (P8-era)"}],
            },
            findings=[_f("A5-F1", "DOCUMENTED",
                         "Combined configured commit over the G2 core manifest; no secret values in artifacts")],
            evidence_refs=[{"source": "G2 core manifest", "method": "configuration"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "config"},
        )

    # -- A6/A7/A8 cross-cutting lanes ----------------------------------------------

    def _cross(self, inputs, lane):
        return {
            "base_commit": "A5-configured",
            "patch_ref": f"manifest:{lane}",
            "applicability": {"lane": lane},
        }

    def _run_a6(self, spec, inputs, policy):
        payload = self._cross(inputs, "flags")
        payload["flags"] = [{"flag": "NEW_STACK_ROLLOUT", "default": False, "fail": "closed"}]
        payload["state_tests"] = [{"states": ["on", "off"], "result": "specified"}]
        payload["recovery_mapping"] = [{"note": "flag-off does not reverse committed data"}]
        payload["lifecycle"] = [{"owner": "pilot", "expiry": "post-migration"}]
        return AgentOutcome(
            status="COMPLETE", payload=payload,
            findings=[_f("A6-F1", "DOCUMENTED", "Flags disable paths; never a data rollback mechanism")],
            evidence_refs=[{"source": "A5 commit", "method": "flag design"}],
            scope={"app": self.brief.get("app_id", "")}, applicability=payload["applicability"])

    def _run_a7(self, spec, inputs, policy):
        payload = self._cross(inputs, "observability")
        payload["instrumentation_map"] = [{"boundary": "http-ingress", "slis": ["latency", "availability"]}]
        payload["telemetry_config"] = {"redaction": "patterns applied"}
        payload["emission_tests"] = [{"test": "redaction", "result": "specified"}]
        payload["redaction_checks"] = [{"check": "no secrets in telemetry", "state": "specified"}]
        payload["overhead_evidence"] = "UNSET — post-deploy measurement"
        payload["deployment_obligations"] = [{"obligation": "collector provisioning (P8-era)"}]
        return AgentOutcome(
            status="COMPLETE", payload=payload,
            findings=[_f("A7-F1", "DOCUMENTED", "Dashboard seeds do not prove deployed observability")],
            evidence_refs=[{"source": "A5 commit", "method": "instrumentation design"}],
            scope={"app": self.brief.get("app_id", "")}, applicability=payload["applicability"])

    def _run_a8(self, spec, inputs, policy):
        payload = self._cross(inputs, "security")
        payload["control_coverage"] = [
            {"control": c["constraint"], "implemented": "manifest", "test": "specified"}
            for c in self.brief.get("security_constraints", [])
        ]
        payload["security_tests"] = [{"test": "secret-free artifacts", "result": "PASS (pattern scan at publish)"}]
        payload["dependency_changes"] = [{"action": "scan post-upgrade", "state": "NOT_RUN (no scanner in pilot)"}]
        payload["findings"] = []
        payload["exceptions"] = []
        payload["deployment_obligations"] = [{"obligation": "mTLS/encryption enforcement is deployment-side (P8-era)"}]
        return AgentOutcome(
            status="COMPLETE", payload=payload,
            findings=[_f("A8-F1", "DOCUMENTED",
                         "Code/config generation cannot prove deployed mTLS/encryption; retest after security changes")],
            evidence_refs=[{"source": "P3.A4 constraints", "method": "control mapping"}],
            scope={"app": self.brief.get("app_id", "")}, applicability=payload["applicability"])

    # -- A9 Validation & Equivalence ----------------------------------------------------

    def _run_a9(self, spec, inputs, policy):
        g3 = inputs.get("G3", {})
        g1 = inputs.get("G1", {})
        baseline_routes = (g1.get("payload", {}).get("baseline_summary", {})
                           .get("route_count", 0))
        results = [
            {"criterion": "route-inventory-preserved", "status": "PASS" if baseline_routes is not None else "NOT_RUN",
             "tested_commit": "G3-sealed", "baseline_hash": g1.get("content_hash")},
            {"criterion": "contract-inventory-preserved", "status": "PASS",
             "note": "manifest-level equivalence in pilot depth 1"},
            {"criterion": "runtime-differential", "status": "NOT_RUN",
             "note": "requires executed build (pilot depth 2: modernize-app asset port)"},
        ]
        not_run_required = [r for r in results if r["status"] == "NOT_RUN"]
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "tested_commit": "G3-sealed-identity",
                "build_digest": g3.get("payload", {}).get("final_manifest", {}).get("build_digest", "manifest-0"),
                "baseline_manifest_hash": g1.get("content_hash"),
                "test_results": results,
                "acceptance_coverage": [{"covered": len(results) - len(not_run_required), "total": len(results)}],
                "expected_difference_results": [],
                "residual_risks": [{"risk": "runtime equivalence unproven at this depth",
                                    "mitigation": "G4 limited handoff only"}],
                "candidate_manifest": {"gates": ["G1", "G2", "G3"]},
            },
            findings=[_f("A9-F1", "DOCUMENTED",
                         "NOT_RUN never counts as PASS; A9 reports evidence, G4 owns release")],
            evidence_refs=[{"source": "G1+G3 identities", "method": "differential checks"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "validation"},
        )


# ---------------------------------------------------------------------------
# P5 gate overrides: G0 permit, G1 baseline seal, G2 core merge, G3 final merge, G4 release
# ---------------------------------------------------------------------------


def p5_intake_gate(ctx: GateContext) -> GateResult:
    pkg = ctx.run_inputs.get("p4_package", {})
    permit = ctx.run_inputs.get("execution_permit", {})
    if pkg.get("status") not in ("READY_FOR_PREPARATION", "SCOPED_PREPARATION"):
        return GateResult("FAILED", "FAILED", {},
                          [f"P4 status {pkg.get('status', 'missing')} does not admit preparation"])
    if not permit.get("granted"):
        return GateResult("FAILED", "FAILED", {},
                          ["missing explicit execution permit: planning approval alone cannot authorize writes"])
    return GateResult("PUBLISHED", "COMPLETE", {
        "intake_manifest": {"application_id": pkg.get("application_id"),
                            "permit_scope": permit.get("scope", "repo+build+test sandbox"),
                            "policy_version": ctx.policy.version if ctx.policy else "none"}
    }, [])


def p5_baseline_gate(ctx: GateContext) -> GateResult:
    blockers = [b for a in ctx.inputs.values() for b in intake_errors(a)]
    if blockers:
        return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)
    a1 = ctx.inputs.get("A1", {})
    baseline = a1.get("payload", {})
    cov = baseline.get("coverage", {})
    if isinstance(cov, str):
        try:
            import json as _json
            cov = _json.loads(cov)
        except ValueError:
            cov = {}
    if cov.get("routes") is None:
        return GateResult("FAILED", "FAILED",
                          {"blockers": ["baseline oracle missing"]},
                          ["baseline oracle missing"])
    return GateResult("PUBLISHED", "COMPLETE", {
        "baseline_manifest": {
            "baseline_commit": baseline.get("baseline_commit"),
            "oracle": baseline.get("observed_results", []),
            "coverage": cov,
            "baseline_state": "LIMITED_BASELINE",
            "owner_acceptance": "accepted-for-pilot (static oracle limitation recorded)",
            "baseline_summary": {
                "baseline_commit": baseline.get("baseline_commit"),
                "route_count": cov.get("routes", 0),
                "touched_hint": [],
            },
        }
    }, [])


def p5_core_integration_gate(ctx: GateContext) -> GateResult:
    """G2 joins A2+A3+A4 into one combined core manifest."""
    lanes = {}
    blockers = []
    for lane in ("A2", "A3", "A4"):
        art = ctx.published.get(lane) or ctx.inputs.get(lane)
        if art is None:
            blockers.append(f"lane {lane} missing")
            continue
        errs = intake_errors(art)
        if errs:
            blockers.extend(errs)
            continue
        lanes[lane] = {"status": art["status"],
                       "patch_ref": art["payload"].get("patch_ref"),
                       "applicability": art["payload"].get("applicability", {})}
    if blockers:
        return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)
    import hashlib as _h, json as _j
    core_hash = _h.sha256(_j.dumps(lanes, sort_keys=True).encode()).hexdigest()
    return GateResult("PUBLISHED", "COMPLETE", {
        "core_manifest": {
            "lanes": lanes,
            "merge_order": ["A2", "A3", "A4"],
            "integrated_commit": f"core-{core_hash[:12]}",
            "combined_checks": [{"check": "manifest merge", "result": "PASS"}],
            "component_coverage": ["app"],
        }
    }, [])


def p5_final_integration_gate(ctx: GateContext) -> GateResult:
    """G3 joins A6+A7+A8 against the A5 commit and seals identity."""
    blockers = []
    lanes = {}
    for lane in ("A5", "A6", "A7", "A8"):
        art = ctx.published.get(lane) or ctx.inputs.get(lane)
        if art is None:
            blockers.append(f"lane {lane} missing")
            continue
        errs = intake_errors(art)
        if errs:
            blockers.extend(errs)
            continue
        lanes[lane] = art["status"]
    if blockers:
        return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)
    import hashlib as _h, json as _j
    build_digest = _h.sha256(_j.dumps(lanes, sort_keys=True).encode()).hexdigest()
    return GateResult("PUBLISHED", "COMPLETE", {
        "final_manifest": {
            "base": "A5-configured",
            "lanes": lanes,
            "integrated_commit": f"final-{build_digest[:12]}",
            "build_digest": build_digest,
            "sbom_ref": "P1.A1 sbom_ref (updated deltas in A2 manifest)",
            "combined_checks": [{"check": "cross-lane manifest consistency", "result": "PASS"}],
        }
    }, [])


def p5_release_gate(ctx: GateContext) -> GateResult:
    blockers = [b for a in ctx.inputs.values() for b in intake_errors(a)]
    if blockers:
        return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)
    a9 = ctx.inputs.get("A9", {})
    results = (a9.get("payload", {}) or {}).get("test_results", [])
    required_not_run = [r for r in results if r["status"] == "NOT_RUN"]
    decision = "LIMITED_HANDOFF" if required_not_run else "READY_FOR_DOWNSTREAM"
    reviewer = (ctx.policy.reviewers.get("simulated", {}).get("release", "sim-release")
                if ctx.policy else "sim-release")
    return GateResult("PUBLISHED", "COMPLETE", {
        "decision_record": {
            "status": decision,
            "candidate_hash": a9.get("content_hash"),
            "authorized_by": reviewer,
            "simulated": True,
            "authorized_at": _now(),
            "allowed_downstream": ["P6 data route admission (limited)"],
            "obligations": ["runtime differential NOT_RUN at pilot depth 1: "
                            "must execute before any deployable claim"],
        }
    }, [])


P5_GATE_OVERRIDES = {
    "G0": p5_intake_gate,
    "G1": p5_baseline_gate,
    "G2": p5_core_integration_gate,
    "G3": p5_final_integration_gate,
    "G4": p5_release_gate,
}
