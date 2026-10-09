"""Phase 3 — Target Architecture engine.

Activation-matrix-driven design: A1 publishes per-agent scope modes from the
P2 disposition (DESIGN / VALIDATE_EXISTING / VALIDATE_VENDOR / SKIP_APPROVED),
every admitted route gets a boundary map (A2 always publishes), NFR criteria
carry target-or-UNSET discipline, and A8 runs deterministic cross-domain
consistency checks before G2 binds the planning release to the package hash.
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

from appmod.agents.runtime import AgentOutcome
from appmod.kernel.gates import GateContext, GateResult
from appmod.contracts.schemas import intake_errors

_now = lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _f(fid, cls, statement):
    return {"id": fid, "evidence_class": cls, "statement": statement}


class P3AgentRunner:
    def __init__(self, design_brief: dict[str, Any] | None = None):
        """design_brief: {'app_id', 'disposition', 'primary_language', 'route',
        'components', 'nfr_targets'} — assembled from P1/P2 artifacts by the
        pipeline driver."""
        self.brief = design_brief or {}

    accepts_context = True

    def run(self, agent_spec, inputs, policy, context=None):
        fn = getattr(self, f"_run_{agent_spec['local_id'].lower()}")
        if agent_spec["local_id"] == "A8":
            return fn(agent_spec, inputs, policy, context=context)
        return fn(agent_spec, inputs, policy)

    def fingerprint(self) -> str:
        return "P3:" + hashlib.sha256(json.dumps(self.brief, sort_keys=True, default=str).encode()).hexdigest()[:16]

    @property
    def disposition(self) -> str:
        return self.brief.get("disposition", "Replatform")

    # -- A1 Target Architecture ---------------------------------------------------

    def _run_a1(self, spec, inputs, policy):
        lang = self.brief.get("primary_language", "unknown")
        target = {
            "python": "python-3.12 + framework-current (LTS toolchain)",
            "java": "java-21 LTS + spring-boot-3.x",
            "javascript": "node-24 LTS + express-5",
            "typescript": "node-24 LTS + typed stack",
            "ruby": "ruby-3.4 + rack-3",
            "php": "php-8.4 + laravel-current",
            "go": "go-1.25 stable",
            "csharp": ".NET 8 LTS",
        }.get(lang, "target stack: owner-approved baseline required")
        nfrs = []
        for req in ("availability", "latency_p95", "rpo", "rto", "a11y_baseline"):
            nfrs.append({
                "requirement_id": f"NFR-{req.upper()}",
                "metric": req, "target": "UNSET", "approval_state": "UNSET",
                "note": "targets are engagement policy; never model-invented",
            })
        activation = []
        for agent, mode in (
            ("A2", "DESIGN"), ("A3", "DESIGN"), ("A4", "DESIGN"),
            ("A5", "DESIGN" if self.brief.get("route") == "UI" else "SKIP_APPROVED"),
            ("A6", "DESIGN"), ("A7", "DESIGN"),
        ):
            activation.append({"agent": agent, "mode": mode,
                               "disposition": self.disposition,
                               "applicability": "route-justified"})
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "blueprint_ref": f"P3/blueprint/{self.brief.get('app_id', 'app')}",
                "component_map": [
                    {"component": c, "target": target} for c in self.brief.get("components", ["app"])
                ],
                "technology_evidence": [
                    {"choice": target, "evidence": "DOCUMENTED stack baseline; dated docs verification required at execution"},
                ],
                "nfr_criteria": nfrs,
                "transition_constraints": [
                    f"{self.disposition} route: preserve external behaviour unless approved change",
                ],
                "activation_manifest": activation,
                "proposed_adrs": [
                    {"adr": "ADR-001", "decision": f"target stack: {target}",
                     "status": "PROPOSED", "evidence": "stack baseline"},
                ],
            },
            findings=[_f("A1-F1", "INFERRED",
                         "Targets are proposals pending owner approval; NFR targets remain UNSET until policy sets them")],
            evidence_refs=[{"source": "P2 route + P1 stack evidence", "method": "activation-matrix routing"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": self.disposition},
        )

    # -- A2 Monolith Decomposition --------------------------------------------------

    def _run_a2(self, spec, inputs, policy):
        comps = self.brief.get("components", ["app"])
        boundaries = [
            {"boundary": c, "ownership": "single team", "justification": "domain cohesion (pilot heuristic)"}
            for c in comps[:8]
        ]
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "boundaries": boundaries,
                "ownership": [{"boundary": b["boundary"], "owner_role": "platform team (pilot)"} for b in boundaries],
                "communication_needs": [
                    {"from": b["boundary"], "to": "app-core", "style": "in-process or API"}
                    for b in boundaries[:4]
                ],
                "transition_units": [{"unit": b["boundary"], "route": self.disposition} for b in boundaries],
                "substitution_ref": None,
                "rationale": [
                    "modular monolith preserved where justified; decomposition is evidence-based, not automatic microservices",
                ],
            },
            findings=[_f("A2-F1", "INFERRED",
                         "Boundary proposal from repository structure; Refactor does not imply microservices")],
            evidence_refs=[{"source": "A1 blueprint", "method": "boundary derivation"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": self.disposition},
        )

    # -- A4 Security Architecture -----------------------------------------------------

    def _run_a4(self, spec, inputs, policy):
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "threats": [
                    {"threat": "injection via untrusted input", "stride": "T1"},
                    {"threat": "secret exposure in artifacts", "stride": "I2"},
                ],
                "trust_boundaries": [{"boundary": "app <-> external clients"}],
                "security_constraints": [
                    {"constraint": "secrets via references only; never in artifacts", "source": "P1.A6 evidence"},
                    {"constraint": "input validation at every external boundary"},
                ],
                "control_mapping": [
                    {"control": "secret-hygiene", "maps_to": "P5.A8 implementation + deployment enforcement", "evidence": "P1.A6"},
                ],
                "responsibility_matrix": [
                    {"area": "app-layer controls", "owner": "P5.A8"},
                    {"area": "platform enforcement (mTLS, encryption-at-rest)", "owner": "deployment phase (future P8)"},
                ],
                "validation_criteria": [
                    {"criterion": "no secrets in published artifacts", "method": "pattern scan on store"},
                ],
            },
            findings=[_f("A4-F1", "DOCUMENTED",
                         "Threat model bounded to pilot scope; no regulatory compliance claim")],
            evidence_refs=[{"source": "P1.A6 findings", "method": "control mapping"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": self.disposition},
        )

    # -- A3 Schema Alignment & Data Architecture ------------------------------------------

    def _run_a3(self, spec, inputs, policy):
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "schemas": [
                    {"object": d, "action": "validate-or-align"} for d in self.brief.get("datasets", ["core"])
                ],
                "data_contracts": [
                    {"contract": "system-of-record per object", "owner": "data owner (pilot)"},
                ],
                "migration_design": "batch route (P6 pilot scope): checksums + counts reconciled at matched cutoff; cutover only via P6 G3 release",
                "reconciliation_criteria": [
                    {"criterion": "row counts per object within approved tolerance", "tolerance": "UNSET"},
                ],
                "retention_controls": [{"control": "retention policy", "status": "UNSET — engagement policy"}],
                "recovery_limits": [
                    {"limit": "rollback after cutover requires reconciliation; flags cannot reverse committed data"},
                ],
            },
            findings=[_f("A3-F1", "DOCUMENTED",
                         "No data migration executed in P3; design only (contract rule)")],
            evidence_refs=[{"source": "P1.A3 datasets", "method": "schema alignment"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": self.disposition},
        )

    # -- A5 UI Architecture -------------------------------------------------------------------

    def _run_a5(self, spec, inputs, policy):
        a1 = inputs.get("A1", {})
        mode = next((m["mode"] for m in a1.get("payload", {}).get("activation_manifest", [])
                     if m["agent"] == "A5"), "SKIP_APPROVED")
        if mode == "SKIP_APPROVED":
            return AgentOutcome(
                status="SKIPPED_APPROVED",
                payload={
                    "ui_applicability": "NOT_APPLICABLE",
                    "patterns": [], "service_demands": [], "journey_mapping": [],
                    "acceptance_criteria": [],
                    "skip_record": {
                        "mode": "SKIP_APPROVED", "justification": "headless/API-only route",
                        "consumer_fields": {"platform_demands": "none from UI lane"},
                    },
                },
                findings=[_f("A5-F1", "DOCUMENTED", "Typed headless N/A record; no UI/BFF demand")],
                scope={"app": self.brief.get("app_id", "")},
                applicability={"route": "headless", "skip_policy": "pilot-default"},
            )
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "ui_applicability": "APPLICABLE",
                "patterns": [{"pattern": "server-rendered templates retained", "basis": "P1.A5 route=UI"}],
                "service_demands": [{"demand": "template data APIs", "consumer": "A6"}],
                "journey_mapping": [{"journey": j, "state": "mapped at P1; refined in P5"} for j in self.brief.get("journeys", ["core"])[:5]],
                "acceptance_criteria": [{"criterion": "representative journeys render post-migration", "target": "UNSET"}],
                "skip_record": None,
            },
            findings=[_f("A5-F1", "DOCUMENTED", "UI existence does not require redesign (contract rule)")],
            evidence_refs=[{"source": "P1.A5 journeys", "method": "journey mapping"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": self.disposition},
        )

    # -- A6 Interface & Integration Contracts ------------------------------------------------------

    def _run_a6(self, spec, inputs, policy):
        routes = self.brief.get("routes", [])
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "contract_registry": [
                    {"endpoint": r, "ownership": "app", "versioning": "path or header — UNSET"}
                    for r in routes[:20]
                ],
                "integration_topology": {"style": "single app; direct client calls", "brokers": "none required"},
                "delivery_semantics": [
                    {"semantic": "at-least-once", "boundary": "endpoint level",
                     "note": "exactly-once claims require transactional boundary statement"},
                ],
                "compatibility_criteria": [
                    {"criterion": "existing API contracts preserved unless approved change", "source": "P3 transition constraints"},
                ],
                "platform_demands": [{"demand": "HTTP ingress + TLS", "consumer": "A7"}],
            },
            findings=[_f("A6-F1", "DOCUMENTED",
                         "Contract registry derived from P1 route inventory; schema validity ≠ runtime proof")],
            evidence_refs=[{"source": "P1.A3 integrations", "method": "contract derivation"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": self.disposition},
        )

    # -- A7 Cloud Platform & Capacity -----------------------------------------------------------------

    def _run_a7(self, spec, inputs, policy):
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "platform_blueprint": {
                    "hosting": "local pilot environment (pre-provisioned)",
                    "note": "production platform selection is engagement policy; P8-era work",
                },
                "capacity_model": {"basis": "UNSET — no runtime telemetry in P1 (NOT_ASSESSED propagated)"},
                "bom": [{"item": "app runtime", "qty": 1, "evidence": "target stack from A1"}],
                "observability_design": {"slis": ["availability", "latency_p95"], "targets": "UNSET"},
                "cost_comparison": {"basis": "P2 cost scenarios; platform delta UNSET"},
                "ownership": [{"area": "pilot environment", "owner": "pilot harness"}],
                "verification_requirements": [
                    {"requirement": "capacity validation after telemetry available", "stage": "post-migration"},
                ],
            },
            findings=[_f("A7-F1", "DOCUMENTED",
                         "Capacity provisional: P1 telemetry NOT_ASSESSED propagates; BOM is design, not provisioning")],
            evidence_refs=[{"source": "A6 platform demands", "method": "sizing placeholder"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": self.disposition},
        )

    # -- A8 Architecture Consolidator ---------------------------------------------------------------------

    def _run_a8(self, spec, inputs, policy, context=None):
        sealed = _sealed_artifacts(inputs, (context or {}).get("published", {}))
        checks = _p3_consistency_checks(sealed, self.brief)
        unresolved = [f"{c['check']}: {c['detail']}" for c in checks if c["result"] == "FAIL"]
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "architecture_package": {
                    "components": self.brief.get("components", ["app"]),
                    "target_stack": "see ADR-001",
                },
                "consistency_report": {"checks": checks,
                                       "coverage": "bounded by pilot scope — not a universal contradiction-free claim"},
                "adr_register": [
                    {"adr": "ADR-001", "status": "PROPOSED", "owner_acceptance": "PENDING"},
                ],
                "traceability": [
                    {"requirement": "preserve external behaviour", "maps_to": "P5.A9 differential acceptance"},
                ],
                "unresolved_items": unresolved,
                "phase4_handoff": {
                    "conditions": ["NFR targets to be set by engagement policy before final freeze"],
                },
            },
            findings=[_f("A8-F1", "DOCUMENTED",
                         "A8 cannot rewrite upstream artifacts or self-approve; bounded consistency coverage")],
            evidence_refs=[{"source": "G1 manifest", "method": "deterministic cross-checks"}],
            scope={"app": self.brief.get("app_id", "")},
            applicability={"route": "consolidation"},
        )


def _sealed_artifacts(inputs: dict[str, Any], published: dict[str, Any]) -> dict[str, Any]:
    """Artifacts sealed by G1 (exact id+version), resolved from the run."""
    refs = (inputs.get("G1", {}).get("payload", {}).get("evidence_manifest", {})
            .get("artifact_refs", {}))
    out = {}
    for node, ref in refs.items():
        art = published.get(node)
        if art and ref.get("version") == art.get("artifact_version") \
                and ref.get("content_hash") == art.get("content_hash"):
            out[node] = art
    return out


def _payload(art: dict[str, Any] | None, key: str, default: Any = None) -> Any:
    v = (art or {}).get("payload", {}).get(key, default)
    if isinstance(v, str) and v[:1] in "[{":
        try:
            return json.loads(v)
        except ValueError:
            return default
    return v


def _p3_consistency_checks(sealed: dict[str, Any], brief: dict[str, Any]) -> list[dict[str, Any]]:
    """Deterministic cross-artifact checks over the sealed design candidates."""
    checks: list[dict[str, Any]] = []

    def add(check: str, ok: bool | None, detail: str) -> None:
        checks.append({"check": check, "result": "PASS" if ok else ("REVIEW" if ok is None else "FAIL"),
                       "detail": detail})

    design = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
    missing = [a for a in design if a not in sealed]
    add("all-design-agents-sealed", not missing,
        f"{len(design) - len(missing)}/{len(design)} sealed" + (f"; missing {missing}" if missing else ""))
    failed = [a for a in design if sealed.get(a, {}).get("status") == "FAILED"]
    add("no-failed-design-candidates", not failed, f"failed: {failed}" if failed else "none failed")

    activation = {m.get("agent"): m.get("mode") for m in _payload(sealed.get("A1"), "activation_manifest", [])}
    mismatched = []
    for agent, mode in activation.items():
        st = sealed.get(agent, {}).get("status")
        if mode == "SKIP_APPROVED" and st not in (None, "SKIPPED_APPROVED"):
            mismatched.append(f"{agent} active despite SKIP_APPROVED")
        if mode == "DESIGN" and st == "SKIPPED_APPROVED":
            mismatched.append(f"{agent} skipped despite DESIGN")
    add("activation-manifest-honoured", not mismatched, "; ".join(mismatched) or "modes match statuses")

    comps = {str(c.get("component", "")).lower() for c in _payload(sealed.get("A1"), "component_map", [])
             if isinstance(c, dict)}
    bounds = " ".join(json.dumps(b).lower() for b in _payload(sealed.get("A2"), "boundaries", []))
    uncovered = sorted(c for c in comps if c and c not in bounds)
    add("components-have-boundaries", not uncovered if comps else None,
        f"uncovered: {uncovered[:8]}" if uncovered else f"{len(comps)} components mapped")

    datasets = [str(d) for d in brief.get("datasets", [])]
    schemas = " ".join(json.dumps(s).lower() for s in _payload(sealed.get("A3"), "schemas", []))
    no_design = [d for d in datasets if d.lower() not in schemas]
    add("datasets-have-schema-design", not no_design if datasets else None,
        f"no design for {no_design[:6]}" if no_design else f"{len(datasets)} datasets covered")

    routes = brief.get("routes", [])
    contracts = _payload(sealed.get("A6"), "contract_registry", [])
    add("interfaces-have-contracts", bool(contracts) if routes else None,
        f"{len(contracts)} contracts for {len(routes)} observed routes")

    threats = _payload(sealed.get("A4"), "threats", [])
    controls = _payload(sealed.get("A4"), "control_mapping", [])
    add("threats-mapped-to-controls", bool(controls) if threats else None,
        f"{len(threats)} threats, {len(controls)} control mappings")

    nfrs = _payload(sealed.get("A1"), "nfr_criteria", [])
    unset = [n.get("requirement_id") for n in nfrs if isinstance(n, dict) and n.get("target") == "UNSET"]
    add("nfr-targets-set-by-policy", None if unset else True,
        f"{len(unset)} NFR targets UNSET (release condition)" if unset else "all targets set")
    return checks


# ---------------------------------------------------------------------------
# P3 gate overrides
# ---------------------------------------------------------------------------


def p3_intake_gate(ctx: GateContext) -> GateResult:
    pkg = ctx.run_inputs.get("p2_package", {})
    if not pkg.get("application_id"):
        return GateResult("FAILED", "FAILED", {}, ["no P2 design package supplied"])
    if pkg.get("authorized") is not True:
        return GateResult("FAILED", "FAILED", {},
                          [f"P2 route for {pkg.get('application_id')} is not AUTHORIZED "
                           f"(status={pkg.get('authorization', 'missing')}) — design workflow not admitted"])
    return GateResult("PUBLISHED", "COMPLETE", {
        "intake_manifest": {
            "application_id": pkg["application_id"],
            "disposition": pkg.get("disposition"),
            "p2_candidate_hash": pkg.get("candidate_hash"),
            "policy_version": ctx.policy.version if ctx.policy else "none",
        }
    }, [])


def p3_release_gate(ctx: GateContext) -> GateResult:
    blockers = []
    for node, art in ctx.inputs.items():
        blockers.extend(intake_errors(art))
    if blockers:
        return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)
    a8 = ctx.inputs.get("A8")
    unresolved = (a8 or {}).get("payload", {}).get("unresolved_items", [])
    decision = "READY_FOR_PLANNING" if not unresolved else "CONDITIONAL_PLANNING"
    reviewer = (ctx.policy.reviewers.get("simulated", {}).get("architecture", "sim-arch")
                if ctx.policy else "sim-arch")
    return GateResult("PUBLISHED", "COMPLETE", {
        "decision_record": {
            "status": decision,
            "candidate_hash": a8.get("content_hash") if a8 else None,
            "authorized_by": reviewer,
            "simulated": True,
            "authorized_at": _now(),
            "conditions": ["NFR targets UNSET: planning proceeds; execution gates require policy values"],
            "restrictions": ["no provisioning, code change, migration or cutover authorization"],
        }
    }, [])


P3_GATE_OVERRIDES = {
    "G0": p3_intake_gate,
    "G2": p3_release_gate,
}
