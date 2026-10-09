"""Phase 2 — Portfolio engine.

Deterministic portfolio analysis over the P1 handoff packages:

  A1 value (labelled internal benchmarking), A2 complexity + coupled groups,
  A3 per-8R cost scenarios (pilot rate card), A4 rationalization (overlap
  proposals; no app ever drops from the inventory), A5 readiness, A6 strategy
  (8R dispositions + waves), A7 decision consolidator + route register.

Gate behaviour:
  G0 — validates every upstream P1 package (schema + G2 status); DRAFT scope
       marks that app exploratory-only (no scope upgrade inside P2).
  G1 — seals A1–A5 with consistency refs (A3.complexity_ref, A5.rationalization_ref).
  G2 — per-app authorization: AUTHORIZED only for apps whose P1 package is
       READY_FOR_PORTFOLIO_DECISION (draft scope can never authorize); Retain/
       Retire go to the IA02 non-delivery disposition register instead of a
       fabricated design route.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from typing import Any

from appmod.agents.runtime import AgentOutcome
from appmod.kernel.gates import GateContext, GateResult
from appmod.contracts.schemas import intake_errors

_now = lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

DESIGN_ROUTES = ("Rehost", "Replatform", "Refactor", "Rearchitect", "Rebuild", "Replace")
NON_DESIGN_ROUTES = ("Retain", "Retire")


@dataclass
class PortfolioApp:
    app_id: str
    p1_g2_status: str                 # READY_FOR_PORTFOLIO_DRAFT | READY_FOR_PORTFOLIO_DECISION | HOLD
    loc: int = 0
    languages: int = 1
    dependencies: int = 0
    tests: int = 0
    route: str = "API_ONLY"           # UI / API_ONLY / HEADLESS_BATCH
    license: str = "UNKNOWN"
    has_data_layer: bool = False
    primary_language: str = ""
    source_family: str = ""           # e.g. 'realworld', 'js-demo', 'library'
    p1_manifest_hash: str = ""
    non_delivery_proposal: str = ""   # '' | 'Retain' | 'Retire' (owner decision stays PENDING)


def _f(fid: str, cls: str, statement: str) -> dict[str, Any]:
    return {"id": fid, "evidence_class": cls, "statement": statement}


class P2AgentRunner:
    def __init__(self, apps: list[PortfolioApp]):
        self.apps = apps

    def run(self, agent_spec: dict[str, Any], inputs: dict[str, dict],
            policy: Any) -> AgentOutcome:
        local = agent_spec["local_id"]
        return getattr(self, f"_run_{local.lower()}")(agent_spec, inputs, policy)

    def fingerprint(self) -> str:
        from dataclasses import asdict
        return "P2:" + hashlib.sha256(json.dumps([asdict(a) for a in self.apps],
                                                 sort_keys=True).encode()).hexdigest()[:16]

    # -- A1 Business Value & Market ------------------------------------------------

    def _run_a1(self, spec, inputs, policy) -> AgentOutcome:
        profiles = []
        for a in self.apps:
            value_signals = {
                "user_surface": a.route == "UI",
                "api_surface": a.route == "API_ONLY",
                "test_investment": a.tests > 0,
                "data_layer": a.has_data_layer,
            }
            score = sum(1 for v in value_signals.values() if v)
            profiles.append({
                "application_id": a.app_id,
                "value_signals": value_signals,
                "internal_benchmark_score": score,
                "decision_eligibility": "eligible" if a.p1_g2_status == "READY_FOR_PORTFOLIO_DECISION" else "restricted-draft-scope",
            })
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "app_profiles": profiles,
                "capability_map": [
                    {"application_id": a.app_id, "capabilities": [a.route, a.primary_language]}
                    for a in self.apps
                ],
                "value_scores": [
                    {"application_id": p["application_id"], "score": p["internal_benchmark_score"]}
                    for p in profiles
                ],
                "market_sources": [],
                "evidence_gaps": [{
                    "application_id": "*",
                    "gap": "no authorized external market data in pilot",
                    "effect": "labelled internal benchmarking only",
                }],
            },
            findings=[_f("A1-F1", "INFERRED",
                         "Value assessment uses internal benchmarking; external market data absent (labelled)")],
            evidence_refs=[{"source": "P1 packages", "method": "internal benchmark"}],
            scope={"portfolio": [a.app_id for a in self.apps]},
            applicability={"route": "internal-benchmark"},
        )

    # -- A2 Technical Complexity & Impact ----------------------------------------------

    def _run_a2(self, spec, inputs, policy) -> AgentOutcome:
        complexity = []
        for a in self.apps:
            score = min(5, 1 + (a.loc // 20000) + (a.languages // 4) + (a.dependencies // 40))
            complexity.append({
                "application_id": a.app_id,
                "complexity_band": f"L{score}",
                "loc": a.loc, "languages": a.languages, "dependencies": a.dependencies,
            })
        families: dict[str, list[str]] = {}
        for a in self.apps:
            if a.source_family:
                families.setdefault(a.source_family, []).append(a.app_id)
        coupled = [
            {"group": fam, "members": apps, "basis": "shared source family; similarity proposes investigation"}
            for fam, apps in families.items() if len(apps) > 1
        ]
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "complexity": complexity,
                "dependency_edges": [],
                "coupled_groups": coupled,
                "external_dependencies": [
                    {"application_id": a.app_id, "note": "cross-repo dependency analysis not available in corpus"}
                    for a in self.apps
                ],
                "sequencing_constraints": [
                    {"constraint": f"{g['group']} consolidation candidates should not be independently scheduled",
                     "group": g["group"]} for g in coupled
                ],
                "coverage": {"traversal": "repo-local only", "unknown_edges": "preserved as unknown"},
            },
            findings=[_f("A2-F2", "OBSERVED",
                         f"{len(coupled)} coupled groups by source family; cross-repo edges unknown (preserved)")],
            evidence_refs=[{"source": "P1 packages", "method": "size metrics"}],
            scope={"portfolio": [a.app_id for a in self.apps]},
            applicability={"route": "graph"},
        )

    # -- A3 Cost Estimation ---------------------------------------------------------------

    def _run_a3(self, spec, inputs, policy) -> AgentOutcome:
        a2 = inputs.get("A2", {}).get("payload", {})
        comp_by_app = {c["application_id"]: c for c in a2.get("complexity", [])}
        cost_cfg = (policy.bundle.get("cost", {}) if policy else {})
        rate_card = cost_cfg.get("base_rate_person_days", 20)
        option_costs = []
        for a in self.apps:
            band = int(comp_by_app.get(a.app_id, {}).get("complexity_band", "L1")[1])
            options = []
            for route, factor in (("Rehost", 0.4), ("Replatform", 0.8), ("Refactor", 1.2),
                                  ("Rearchitect", 2.0), ("Rebuild", 3.0), ("Replace", 1.5)):
                base = rate_card * band * factor
                options.append({
                    "option": route,
                    "low": round(base * 0.7), "base": round(base), "high": round(base * 1.5),
                })
            option_costs.append({"application_id": a.app_id, "options": options})
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "option_costs": option_costs,
                "baseline_ref": "pilot-rate-card",
                "assumptions": [
                    "pilot-default rate card; scenario ranges are not statistical confidence intervals",
                ],
                "shared_cost_ledger": [
                    {"item": "tooling/environment shared across waves", "counted_once": True},
                ],
                "sensitivities": [{"driver": "complexity band", "effect": "±1 band ≈ ±1x base rate"}],
                "usability": [
                    {"application_id": a.app_id,
                     "usable": a.p1_g2_status == "READY_FOR_PORTFOLIO_DECISION",
                     "reason": "" if a.p1_g2_status == "READY_FOR_PORTFOLIO_DECISION" else "P1 draft scope limits cost usability to exploratory analysis"}
                    for a in self.apps
                ],
                "complexity_ref": inputs.get("A2", {}).get("content_hash", ""),
            },
            findings=[_f("A3-F1", "DOCUMENTED",
                         "Cost scenarios from pilot-default rate card; ranges are assumptions, not statistics")],
            evidence_refs=[{"source": "policy rate card", "method": "parametric estimate"}],
            scope={"portfolio": [a.app_id for a in self.apps]},
            applicability={"route": "estimate"},
        )

    # -- A4 Portfolio Rationalization ----------------------------------------------------------

    def _run_a4(self, spec, inputs, policy) -> AgentOutcome:
        a2 = inputs.get("A2", {}).get("payload", {})
        overlap = [
            {"group": g["group"], "members": g["members"],
             "signal": "same product family implemented twice"}
            for g in a2.get("coupled_groups", [])
        ]
        groups = [
            {"group": o["group"], "candidate": "consolidation",
             "status": "PROPOSED", "owner_decision": "PENDING"}
            for o in overlap
        ]
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "overlap": overlap,
                "consolidation_groups": groups,
                "source_target_map": [],
                "retained_app_ids": [a.app_id for a in self.apps],   # no app disappears
                "constraints": [
                    "similarity proposes investigation; it cannot approve retirement",
                ],
                "owner_decisions": [
                    {"group": g["group"], "decision": "PENDING", "owner": "portfolio owner (simulated)"}
                    for g in groups
                ],
            },
            findings=[_f("A4-F1", "INFERRED",
                         f"{len(overlap)} overlap candidates proposed for investigation; all "
                         f"{len(self.apps)} apps preserved in inventory")],
            evidence_refs=[{"source": "A2 coupled groups", "method": "family analysis"}],
            scope={"portfolio": [a.app_id for a in self.apps]},
            applicability={"route": "rationalization"},
        )

    # -- A5 Readiness ------------------------------------------------------------------------------

    def _run_a5(self, spec, inputs, policy) -> AgentOutcome:
        readiness = []
        for a in self.apps:
            if a.p1_g2_status == "READY_FOR_PORTFOLIO_DECISION":
                state, why = "READY", "decision-scope P1 evidence accepted"
            elif a.p1_g2_status == "HOLD":
                state, why = "HOLD", "P1 held"
            else:
                state, why = "CONDITIONAL", "P1 draft scope: planning conditions apply"
            readiness.append({"application_id": a.app_id, "readiness": state, "basis": why})
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "readiness": readiness,
                "blocker_deltas": [],
                "capacity": [{"period": "pilot", "parallel_apps": policy.budgets.get("max_parallel_agents", 4) if policy else 4}],
                "skills_gaps": [{"skill": "target-stack depth", "state": "NOT_ASSESSED in pilot"}],
                "rationalization_ref": inputs.get("A4", {}).get("content_hash", ""),
            },
            findings=[_f("A5-F1", "DOCUMENTED",
                         "Planning readiness distinct from production readiness; P1 risk reused as evidence only")],
            evidence_refs=[{"source": "P1 G2 statuses", "method": "scope rule"}],
            scope={"portfolio": [a.app_id for a in self.apps]},
            applicability={"route": "readiness"},
        )

    # -- A6 Modernization Strategy -------------------------------------------------------------------

    def _run_a6(self, spec, inputs, policy) -> AgentOutcome:
        readiness = {r["application_id"]: r["readiness"]
                     for r in inputs.get("A5", {}).get("payload", {}).get("readiness", [])}
        complexity = {c["application_id"]: int(c["complexity_band"][1])
                      for c in inputs.get("A2", {}).get("payload", {}).get("complexity", [])}
        decisions, waves, unscheduled = [], [], []

        def propose(a: PortfolioApp, disposition: str, wave: int | None) -> None:
            decisions.append({
                "application_id": a.app_id,
                "proposed_disposition": disposition,
                "readiness": readiness.get(a.app_id, "CONDITIONAL"),
                "approval": "PENDING",
                "consolidation_target_id": None,
                "wave_id": f"W{wave}" if wave else None,
                "rationale": f"pilot heuristic: {a.primary_language} {a.route} app, "
                             f"complexity L{complexity.get(a.app_id, 1)}",
            })

        by_family = {}
        for a in self.apps:
            by_family.setdefault(a.source_family or "solo", []).append(a)
        wave_no = 1
        for family, members in sorted(by_family.items()):
            if family in ("js-demo",):   # handled explicitly below (non-design proposals)
                continue
            for a in sorted(members, key=lambda x: complexity.get(x.app_id, 1)):
                if family == "library":
                    propose(a, "Replatform", wave_no)   # bounded modernization of the library itself
                elif complexity.get(a.app_id, 1) >= 4:
                    propose(a, "Rearchitect", wave_no + 1)
                elif a.has_data_layer and a.route == "UI":
                    propose(a, "Rearchitect", wave_no + 1)
                elif complexity.get(a.app_id, 1) <= 2 and a.loc < 15000:
                    propose(a, "Rehost", wave_no)
                else:
                    propose(a, "Replatform", wave_no)
            wave_no += 1

        # explicit non-design proposals (owner decisions pending — IA02 register)
        for a in self.apps:
            if a.non_delivery_proposal in NON_DESIGN_ROUTES:
                propose(a, a.non_delivery_proposal, None)
                decisions[-1]["rationale"] = (
                    f"proposed {a.non_delivery_proposal} — never auto-decommission; "
                    "owner decision and register entry required")

        for d in decisions:
            if d["wave_id"]:
                waves.append({"wave_id": d["wave_id"], "apps": d["application_id"]})
            elif d["proposed_disposition"] in NON_DESIGN_ROUTES:
                unscheduled.append({"application_id": d["application_id"],
                                    "route": d["proposed_disposition"]})

        return AgentOutcome(
            status="COMPLETE",
            payload={
                "decisions": decisions,
                "alternatives": [
                    {"application_id": d["application_id"], "note": "second-best option recorded"}
                    for d in decisions[:5]
                ],
                "waves": _merge_waves(waves),
                "unscheduled": unscheduled,
                "constraints": ["wave capacity bounded by policy parallelism", "consolidation groups not independently scheduled"],
                "input_manifest_ref": inputs.get("G1", {}).get("content_hash", ""),
            },
            findings=[_f("A6-F1", "INFERRED",
                         "Proposed dispositions are heuristic pilots; Hold is a workflow state and Merge a "
                         "relationship — neither is an R; approval stays PENDING at A6")],
            evidence_refs=[{"source": "A2/A5", "method": "rule-based proposal"}],
            scope={"portfolio": [a.app_id for a in self.apps]},
            applicability={"route": "strategy"},
        )

    # -- A7 Decision Consolidator ----------------------------------------------------------------------

    def _run_a7(self, spec, inputs, policy) -> AgentOutcome:
        a6 = inputs.get("A6", {}).get("payload", {})
        decisions = a6.get("decisions", [])
        manifest = {
            "apps": [
                {
                    "application_id": d["application_id"],
                    "proposed_disposition": d["proposed_disposition"],
                    "readiness": d["readiness"],
                    "approval": "PENDING",   # consolidator recommends; G2 authorizes
                    "wave_id": d["wave_id"],
                }
                for d in decisions
            ],
            "inventory_preserved": len(decisions) == len(self.apps),
        }
        route_register = []
        required_approvals = []
        for d in decisions:
            app = d["application_id"]
            route = d["proposed_disposition"]
            entry = {
                "application_id": app, "route": route,
                "p1_scope": next(a.p1_g2_status for a in self.apps if a.app_id == app),
            }
            if route in NON_DESIGN_ROUTES:
                entry.update({
                    "register": "IA02-non-delivery",
                    "owner": "application owner (simulated)",
                    "review_date": "PENDING",
                    "retirement_authority": "required before any decommissioning",
                })
            route_register.append(entry)
            required_approvals.append({
                "application_id": app,
                "requires": "P1 DECISION scope + owner acceptance"
                            if route in DESIGN_ROUTES else "retirement/retention authority",
            })
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "decision_manifest": manifest,
                "roadmap": _merge_waves(a6.get("waves", [])),
                "portfolio_risks": [
                    {"risk": "consolidation candidates double-scheduled", "state": "controlled by sequencing constraint"},
                ],
                "disagreements": [],
                "route_register": route_register,
                "required_approvals": required_approvals,
            },
            findings=[_f("A7-F1", "DOCUMENTED",
                         "Candidate manifest assembled for independent authorization; "
                         "human identity and approved scope bind to the exact candidate hash at G2")],
            evidence_refs=[{"source": "A6 decisions", "method": "consolidation"}],
            scope={"portfolio": [a.app_id for a in self.apps]},
            applicability={"route": "consolidator"},
        )


def _merge_waves(waves: list[dict]) -> list[dict]:
    """Idempotent wave merge: accepts entries whose `apps` is a single id
    (A6 propose loop) or an already-merged list (A7 consolidation)."""
    merged: dict[str, list[str]] = {}
    for w in waves:
        apps = w.get("apps", [])
        if isinstance(apps, str):
            apps = [apps]
        merged.setdefault(w["wave_id"], []).extend(apps)
    return [{"wave_id": k, "apps": sorted(set(v))} for k, v in sorted(merged.items())]


# ---------------------------------------------------------------------------
# P2 gate overrides
# ---------------------------------------------------------------------------


def p2_intake_gate(ctx: GateContext) -> GateResult:
    packages = ctx.run_inputs.get("p1_packages", [])
    if not packages:
        return GateResult("FAILED", "FAILED", {},
                          ["no P1 handoff packages supplied at G0"])
    bad = [p.get("application_id", "?") for p in packages
           if p.get("schema_version") != "P1.discovery.v3.0"
           or p.get("g2_status") not in ("READY_FOR_PORTFOLIO_DRAFT", "READY_FOR_PORTFOLIO_DECISION")]
    if bad:
        return GateResult("FAILED", "FAILED", {"invalid": bad},
                          [f"P1 package invalid for {bad}"])
    return GateResult("PUBLISHED", "COMPLETE", {
        "intake_manifest": {
            "portfolio": [p["application_id"] for p in packages],
            "scope": {p["application_id"]: p["g2_status"] for p in packages},
            "policy_version": ctx.policy.version if ctx.policy else "none",
        }
    }, [])


def p2_snapshot_gate(ctx: GateContext) -> GateResult:
    required = ["A1", "A2", "A3", "A4", "A5"]
    # G1's graph edges bring only A3+A5; A1–A5 are transitive producers
    # ('Snapshot G1 | A3+A5; transitive A1–A5') so the seal scans the run's
    # published artifacts.
    available = dict(ctx.published or {})
    available.update(ctx.inputs)
    refs: dict[str, Any] = {}
    blockers: list[str] = []
    for node, art in available.items():
        errs = intake_errors(art)
        if errs:
            blockers.extend(errs)
            continue
        refs[node] = {"artifact_id": art["artifact_id"], "version": art["artifact_version"],
                      "content_hash": art["content_hash"], "status": art["status"]}
    for node in required:
        if node not in refs:
            blockers.append(f"required producer {node} missing")
    # G1 consistency: A3 records complexity_ref; A5 records rationalization_ref
    a3 = available.get("A3", {}).get("payload", {})
    if a3 and a3.get("complexity_ref") != refs.get("A2", {}).get("content_hash"):
        blockers.append("A3.complexity_ref does not match sealed A2 version")
    a5 = available.get("A5", {}).get("payload", {})
    if a5 and a5.get("rationalization_ref") != refs.get("A4", {}).get("content_hash"):
        blockers.append("A5.rationalization_ref does not match sealed A4 version")
    if blockers:
        return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)
    manifest_hash = hashlib.sha256(json.dumps(refs, sort_keys=True).encode()).hexdigest()
    return GateResult("PUBLISHED", "COMPLETE", {
        "evidence_manifest": {"artifact_refs": refs, "manifest_hash": manifest_hash,
                              "sealed_at": _now()}
    }, [])


def p2_release_gate(ctx: GateContext) -> GateResult:
    blockers: list[str] = []
    for node, art in ctx.inputs.items():
        blockers.extend(intake_errors(art))
    if blockers:
        return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)

    a7 = ctx.inputs.get("A7", {})
    manifest = a7.get("payload", {}).get("decision_manifest", {})
    register = a7.get("payload", {}).get("route_register", [])
    scope = ctx.run_inputs.get("p1_scope", {})   # app -> P1 G2 status
    authorized, draft_only, non_delivery = [], [], []
    for entry in register:
        app, route = entry["application_id"], entry["route"]
        if route in NON_DESIGN_ROUTES:
            non_delivery.append(app)
        elif scope.get(app) == "READY_FOR_PORTFOLIO_DECISION":
            authorized.append(app)
        else:
            draft_only.append(app)
    reviewer = (ctx.policy.reviewers.get("simulated", {}).get("portfolio", "sim-portfolio")
                if ctx.policy else "sim-portfolio")
    payload = {
        "decision_record": {
            "status": "AUTHORIZED" if authorized else "DRAFT_ONLY",
            "candidate_hash": a7.get("content_hash"),
            "authorized_apps": authorized,
            "draft_only_apps": draft_only,
            "non_delivery_register": {
                "register": "IA02",
                "entries": [e for e in register if e["application_id"] in non_delivery],
            },
            "authorized_by": reviewer,
            "simulated": True,
            "authorized_at": _now(),
            "restrictions": [
                "draft-scope apps limited to exploratory outputs; no final disposition",
                "non-delivery routes enter the disposition register; no decommissioning authority",
            ],
            "accepted_exceptions": [],
        }
    }
    return GateResult("PUBLISHED", "COMPLETE", payload, [])


P2_GATE_OVERRIDES = {
    "G0": p2_intake_gate,
    "G1": p2_snapshot_gate,
    "G2": p2_release_gate,
}
