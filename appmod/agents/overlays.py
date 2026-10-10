"""Per-agent LLM overlays for P1–P4.

An overlay says *how* the model participates in one agent:
  tier      — model tier (reasoning / coding / fast)
  tools     — gateway allowlist (deny-by-default)
  fields    — payload fields the model contributes, as Azure strict schemas,
              each with a merge mode:
                append  — seed items + model items (array fields)
                replace — model value replaces the seed value
                decide  — postprocess applies model decisions onto seed items
  guidance  — agent-specific method, on top of the registry charter
  postprocess(seed_payload, llm_fields, ctx) -> payload  — re-derives any
              structural fields consumers read, so contracts stay intact

Every model item carries ``evidence_class`` + ``evidence_ids``; the
EvidenceValidator downgrades uncited OBSERVED/DOCUMENTED claims.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Callable

from appmod.contracts.schemas import EVIDENCE_CLASS_ENUM
from appmod.tools.builtin import ARTIFACT_TOOLS, REPO_TOOLS

# -- strict-schema helpers -------------------------------------------------------


def S(desc: str | None = None) -> dict[str, Any]:
    return {"type": "string", **({"description": desc} if desc else {})}


def N(desc: str | None = None) -> dict[str, Any]:
    return {"type": ["string", "null"], **({"description": desc} if desc else {})}


def I(desc: str | None = None) -> dict[str, Any]:
    return {"type": "integer", **({"description": desc} if desc else {})}


def NUM(desc: str | None = None) -> dict[str, Any]:
    return {"type": "number", **({"description": desc} if desc else {})}


def B(desc: str | None = None) -> dict[str, Any]:
    return {"type": "boolean", **({"description": desc} if desc else {})}


def E(*values: str, desc: str | None = None) -> dict[str, Any]:
    return {"type": "string", "enum": list(values), **({"description": desc} if desc else {})}


def A(item: dict[str, Any], desc: str | None = None) -> dict[str, Any]:
    return {"type": "array", "items": item, **({"description": desc} if desc else {})}


def O(**props: dict[str, Any]) -> dict[str, Any]:
    return {"type": "object", "properties": props, "required": list(props),
            "additionalProperties": False}


EVC = E(*EVIDENCE_CLASS_ENUM)
EVIDS = A(S(), desc="Evidence ids you were given (ev-..., art:..., seed:...). Never invent ids.")


def item(**props: dict[str, Any]) -> dict[str, Any]:
    return O(**props, evidence_class=EVC, evidence_ids=EVIDS)


SEV = E("critical", "high", "medium", "low", "info")
R8 = ("Retain", "Retire", "Rehost", "Replatform", "Refactor", "Rearchitect", "Rebuild", "Replace")


@dataclass
class Overlay:
    tier: str = "reasoning"
    effort: str = "medium"
    tools: list[str] = field(default_factory=lambda: list(ARTIFACT_TOOLS))
    fields: dict[str, tuple[dict[str, Any], str]] = field(default_factory=dict)
    guidance: str = ""
    postprocess: Callable[[dict[str, Any], dict[str, Any], dict[str, Any]], dict[str, Any]] | None = None
    max_turns: int = 10

    def fields_schema(self) -> dict[str, Any]:
        return O(**{k: v[0] for k, v in self.fields.items()})

    def prompt_version(self, charter: str) -> str:
        blob = json.dumps({"c": charter, "g": self.guidance, "f": self.fields_schema(),
                           "t": sorted(self.tools), "tier": self.tier}, sort_keys=True)
        return "pv-" + hashlib.sha256(blob.encode()).hexdigest()[:10]


REPO = REPO_TOOLS + ARTIFACT_TOOLS
REPO_SEC = REPO + ["vulnerability_scan", "secret_scan", "static_analysis", "sbom_packages"]

# -- postprocess hooks ------------------------------------------------------------


def _pp_p1_a11(seed: dict, llm: dict, ctx: dict) -> dict:
    out = dict(seed)
    by_dim = {d["dimension"]: d for d in llm.get("risk_dimensions", [])}
    dims = []
    for d in seed.get("risk_dimensions", []):
        m = by_dim.pop(d["dimension"], None)
        dims.append({**d, **({"score": max(1, min(5, int(m["score"]))), "basis": m["basis"],
                              "drivers": m["drivers"], "evidence_class": m["evidence_class"],
                              "evidence_ids": m["evidence_ids"], "origin": "llm"} if m else {})})
    unassessed = {u["dimension"] for u in seed.get("unassessed_dimensions", [])}
    for name, m in by_dim.items():
        if name not in unassessed:
            dims.append({"dimension": name, "score": max(1, min(5, int(m["score"]))), "basis": m["basis"],
                         "drivers": m["drivers"], "evidence_class": m["evidence_class"],
                         "evidence_ids": m["evidence_ids"], "origin": "llm"})
    out["risk_dimensions"] = dims
    out["scores"] = [{"dimension": d["dimension"], "score": d["score"]} for d in dims]
    out["blockers"] = list(seed.get("blockers", [])) + [dict(b, origin="llm") for b in llm.get("blockers", [])]
    out["mitigations"] = list(seed.get("mitigations", [])) + [dict(m, origin="llm") for m in llm.get("mitigations", [])]
    return out


def _pp_p2_a6(seed: dict, llm: dict, ctx: dict) -> dict:
    out = dict(seed)
    by_app = {d["application_id"]: d for d in llm.get("decisions", [])}
    decisions, waves, unscheduled = [], {}, []
    for d in seed.get("decisions", []):
        m = by_app.get(d["application_id"])
        nd = dict(d)
        if m and m["proposed_disposition"] in R8:
            nd.update(proposed_disposition=m["proposed_disposition"], rationale=m["rationale"],
                      second_best=m["second_best"], evidence_class=m["evidence_class"],
                      evidence_ids=m["evidence_ids"], origin="llm")
            if m["proposed_disposition"] in ("Retain", "Retire"):
                nd["wave_id"] = None
            else:
                nd["wave_id"] = f"W{max(1, min(6, int(m['wave'])))}"
        decisions.append(nd)
        if nd["wave_id"]:
            waves.setdefault(nd["wave_id"], []).append(nd["application_id"])
        elif nd["proposed_disposition"] in ("Retain", "Retire"):
            unscheduled.append({"application_id": nd["application_id"], "route": nd["proposed_disposition"]})
    out["decisions"] = decisions
    out["waves"] = [{"wave_id": w, "apps": ",".join(a)} for w, a in sorted(waves.items())]
    out["unscheduled"] = unscheduled
    out["alternatives"] = [{"application_id": m["application_id"], "option": m["second_best"],
                            "why_not": m["why_not_second_best"], "origin": "llm"}
                           for m in llm.get("decisions", [])] or seed.get("alternatives", [])
    return out


def _pp_p4_a3(seed: dict, llm: dict, ctx: dict) -> dict:
    out = dict(seed)
    seed_ids = {t["task_id"] for t in seed.get("tasks", [])}
    tasks = list(seed.get("tasks", []))
    edges = list(seed.get("dependency_edges", []))
    llm_tasks = llm.get("tasks", [])
    ids = seed_ids | {t["task_id"] for t in llm_tasks}
    for t in llm_tasks:
        if t["task_id"] in seed_ids:
            continue
        tasks.append({"task_id": t["task_id"], "phase": t["phase"], "kind": t["kind"],
                      "owner_role": t["owner_role"], "acceptance": t["acceptance"],
                      "component": t["component"], "estimate_days": t["estimate_days"],
                      "evidence_class": t["evidence_class"], "evidence_ids": t["evidence_ids"],
                      "origin": "llm"})
        for dep in t["depends_on"]:
            if dep in ids and dep != t["task_id"]:
                edges.append({"from": dep, "to": t["task_id"]})
    edges = _acyclic(edges)
    ctx_hash = hashlib.sha256(json.dumps({"tasks": tasks, "edges": edges}, sort_keys=True).encode()).hexdigest()
    out.update(tasks=tasks, dependency_edges=edges,
               context_manifest={"context_hash": ctx_hash,
                                 "note": "single immutable version consumed by all five planners"},
               acceptance_links=[{"task": t["task_id"], "acceptance": t["acceptance"]} for t in tasks],
               phase_routes=[{"task": t["task_id"], "phase": t["phase"]} for t in tasks])
    out["estimate_assumptions"] = list(seed.get("estimate_assumptions", [])) + [
        dict(e, origin="llm") for e in llm.get("estimate_assumptions", [])]
    return out


def _acyclic(edges: list[dict[str, str]]) -> list[dict[str, str]]:
    """Drop edges that would close a cycle (keeps the first-seen order)."""
    kept: list[dict[str, str]] = []
    adj: dict[str, set[str]] = {}

    def reaches(a: str, b: str) -> bool:
        stack, seen = [a], set()
        while stack:
            x = stack.pop()
            if x == b:
                return True
            if x in seen:
                continue
            seen.add(x)
            stack.extend(adj.get(x, ()))
        return False

    for e in edges:
        if e["from"] == e["to"] or reaches(e["to"], e["from"]):
            continue
        if e["to"] in adj.get(e["from"], set()):
            continue
        adj.setdefault(e["from"], set()).add(e["to"])
        kept.append(e)
    return kept


# -- P1 Discovery -------------------------------------------------------------------

P1 = {
    "A1": Overlay(
        tier="reasoning", tools=REPO + ["loc_metrics", "sbom_packages"],
        guidance=(
            "Build a real module map: open entry points, build files and the main packages. "
            "Classify each module's responsibility and layer. Record concrete technical debt "
            "(outdated frameworks/runtimes, deprecated APIs, dead code, missing tests) with file "
            "evidence. Build status stays UNKNOWN unless a build was executed — never infer passing "
            "builds or coverage."),
        fields={
            "module_map": (A(item(name=S(), path=S(), responsibility=S(),
                                  layer=E("ui", "api", "service", "domain", "data", "infra", "test",
                                          "config", "other"),
                                  key_files=A(S()))), "append"),
            "technical_debt": (A(item(title=S(), location=S(), severity=SEV, detail=S(),
                                      remediation=S())), "append"),
            "build_and_doc_gaps": (A(item(gap=S(), impact=S())), "append"),
        }),
    "A2": Overlay(
        tier="reasoning", tools=REPO,
        guidance=(
            "Derive the architecture from code: layers, request flow, framework conventions, "
            "persistence boundaries and cross-module coupling. Inferred decisions are INFERRED "
            "unless an ADR/doc states them (DOCUMENTED). Runtime call paths are not observable."),
        fields={
            "relations": (A(item(**{"from": S(), "to": S()}, kind=E("calls", "imports", "persists",
                                                              "renders", "configures", "extends"),
                                 detail=S())), "append"),
            "coupling_findings": (A(item(module=S(), signal=S(), severity=SEV)), "append"),
            "inferred_decisions": (A(item(decision=S(), rationale=S())), "append"),
            "c4_refs": (A(item(level=E("C4-Context", "C4-Container", "C4-Component"),
                               element=S(), description=S())), "append"),
        }),
    "A3": Overlay(
        tier="reasoning", tools=REPO,
        guidance=(
            "Identify the data model (entities, tables, ORM models, migrations), datastores and "
            "external integrations from code and config. Describe lineage you can observe (which "
            "code writes/reads which entity). Volumes and latency are NOT_ASSESSED without runtime "
            "metadata — never estimate them."),
        fields={
            "entities": (A(item(name=S(), store=S(), defined_in=S(), key_fields=A(S()),
                                relationships=A(S()))), "append"),
            "lineage_observations": (A(item(entity=S(), writer=S(), reader=S(), detail=S())), "append"),
            "integration_details": (A(item(endpoint_or_system=S(), direction=E("inbound", "outbound"),
                                           protocol=S(), purpose=S())), "append"),
        }),
    "A4": Overlay(
        tier="fast", effort="low", tools=REPO,
        guidance=(
            "Profile hosting/runtime from descriptors only (Dockerfiles, compose, CI, IaC, config). "
            "Utilization and recovery are NOT_ASSESSED without telemetry; say so as gaps."),
        fields={
            "runtime_profile": (A(item(aspect=E("runtime", "container", "ci", "config", "database",
                                                "cache", "messaging", "secrets", "other"),
                                       detail=S(), source_file=S())), "append"),
            "portability_findings": (A(item(finding=S(), effect_on_migration=S())), "append"),
        }),
    "A5": Overlay(
        tier="fast", effort="low", tools=REPO,
        guidance=(
            "Identify user journeys and personas from routes, templates and controllers. The "
            "capability route (UI/API_ONLY/HEADLESS_BATCH) is computed deterministically; review it "
            "and flag disagreement with evidence. Analytics are unavailable unless provided."),
        fields={
            "journeys": (A(item(name=S(), persona=S(), steps=A(S()), entry_route=S())), "append"),
            "personas": (A(item(name=S(), goals=S())), "append"),
            "friction_findings": (A(item(journey=S(), issue=S(), severity=SEV)), "append"),
            "route_review": (O(agrees=B(), proposed_route=E("UI", "API_ONLY", "HEADLESS_BATCH"),
                               rationale=S(), evidence_ids=EVIDS), "replace"),
        }),
    "A6": Overlay(
        tier="reasoning", tools=REPO_SEC,
        guidance=(
            "Run vulnerability_scan, secret_scan and static_analysis. Triage results: map each "
            "material finding to a control, severity and remediation. Cite tool evidence ids. "
            "No regulatory compliance claim without documented obligations."),
        fields={
            "vulnerabilities": (A(item(id=S(), package=S(), severity=SEV, summary=S(),
                                       remediation=S())), "append"),
            "control_findings": (A(item(control=S(), file=S(), severity=SEV, finding=S(),
                                        remediation=S())), "append"),
            "license_review_flags": (A(item(scope=S(), license=S(), review=S())), "append"),
        }),
    "A7": Overlay(
        tier="fast", effort="low", tools=REPO,
        guidance=(
            "Evaluate UX/DX against concrete criteria (forms, labels, error states, navigation, API "
            "error contracts). Sample templates or API handlers with read_file. When the seed is "
            "SKIPPED_APPROVED, verify the skip reason and report agreement."),
        fields={
            "criteria": (A(item(criterion=S(), result=E("met", "partially_met", "not_met",
                                                         "not_assessed"), detail=S())), "append"),
            "observations": (A(item(observation=S(), location=S())), "append"),
        }),
    "A8": Overlay(
        tier="reasoning", effort="low", tools=ARTIFACT_TOOLS,
        guidance=(
            "Draft 3-8 NEW stakeholder questions specific to THIS application that would resolve its "
            "open discovery gaps. Read the upstream artifacts (gaps, NOT_ASSESSED items, risky "
            "dependencies, data stores, integrations) and ask about those concretely, naming the "
            "component, dataset or dependency. Do NOT restate the generic seed questions already in the "
            "payload (criticality / compliance / ownership) - only ask what they leave open. Fill "
            "resolves_gap with the gap you target. You cannot answer them: any answer you write is "
            "HYPOTHETICAL. Confirmed responses only come from recorded human answers."),
        fields={
            "questions_drafted": (A(item(question=S(), why=S(), target_role=S(),
                                         resolves_gap=S())), "append"),
        }),
    "A9": Overlay(
        tier="reasoning", tools=REPO,
        guidance=(
            "Reconstruct business processes and business rules from controllers, services, "
            "validators and models. Locate them with search_code first — one natural-language "
            "query per candidate process (e.g. 'register a new user', 'place an order', "
            "'follow another user') — then read_file the hits. For each process and rule name the "
            "implementing function or method and its file, and cite the search_code and read_file "
            "evidence ids. Owner confirmation is PENDING — never mark rules as confirmed."),
        fields={
            "processes": (A(item(name=S(), trigger=S(), steps=A(S()), file=S(),
                                 function=S("implementing function/method"))), "append"),
            "business_rules": (A(item(rule=S(), file=S(), function=S("enforcing function/method"),
                                      enforcement=S())), "append"),
            "exception_paths": (A(item(process=S(), condition=S(), handling=S())), "append"),
        }),
    "A10": Overlay(
        tier="reasoning", tools=ARTIFACT_TOOLS,
        guidance=(
            "Synthesize the sealed discovery: read the upstream artifacts (get_artifact for A1–A9) "
            "and write a domain-by-domain summary. Preserve contradictions — do not resolve them. "
            "Every summary sentence must trace to an artifact id."),
        fields={
            "domain_summaries": (A(item(domain=S(), summary=S(), sources=A(S()))), "append"),
            "contradictions": (A(item(between=A(S()), statement=S())), "append"),
            "gaps": (A(item(area=S(), impact=S())), "append"),
        }),
    "A11": Overlay(
        tier="reasoning", tools=ARTIFACT_TOOLS + ["repo_summary", "vulnerability_scan", "eol_lookup"],
        guidance=(
            "Score technical, security and data risk with the G0 policy rubric: read "
            "get_artifact('G0') field intake_manifest.risk_taxonomy.rubric — it is the approved run "
            "policy (labelled pilot-default), so apply it; do not record its absence as a blocker. "
            "Score = 1 + one point per matched anchor, capped at 5. The seed already applied the "
            "anchors it can check deterministically (see each seed dimension's drivers); verify them, "
            "add anchors the seed cannot check (e.g. an end-of-life framework — check it with "
            "eol_lookup — or a shared database) only with cited evidence, and return every assessable dimension with its drivers and "
            "evidence ids. Unassessed dimensions stay unassessed — never average them in."),
        fields={
            "risk_dimensions": (A(item(dimension=E("technical", "security", "data"), score=I(),
                                       basis=S(), drivers=A(S()))), "decide"),
            "blockers": (A(item(blocker=S(), dimension=S())), "append"),
            "mitigations": (A(item(**{"for": S()}, action=S())), "append"),
        },
        postprocess=_pp_p1_a11),
}

# -- P2 Portfolio ---------------------------------------------------------------------

PF_TOOLS = ARTIFACT_TOOLS + ["repo_summary", "list_dependencies", "grep", "read_file"]

P2 = {
    "A1": Overlay(
        tier="reasoning", tools=PF_TOOLS,
        guidance=(
            "Assess business value per application from P1 evidence (journeys, processes, "
            "capabilities). Without market data the assessment is internal benchmarking (INFERRED)."),
        fields={
            "value_assessments": (A(item(application_id=S(), value_score=I(desc="1-5"),
                                         capabilities=A(S()), rationale=S())), "append"),
            "evidence_gaps": (A(item(application_id=S(), gap=S(), effect=S())), "append"),
        }),
    "A2": Overlay(
        tier="reasoning", tools=PF_TOOLS,
        guidance=(
            "Assess technical complexity per app (framework age, coupling, data layer, test "
            "coverage) and cross-app dependencies/shared components. Complexity band is computed; "
            "add your qualitative drivers and sequencing constraints."),
        fields={
            "complexity_drivers": (A(item(application_id=S(), driver=S(), impact=SEV)), "append"),
            "dependency_edges": (A(item(**{"from": S(), "to": S()}, kind=S())), "append"),
            "sequencing_constraints": (A(item(constraint=S(), applications=A(S()))), "append"),
        }),
    "A3": Overlay(
        tier="fast", effort="low", tools=ARTIFACT_TOOLS,
        guidance=(
            "Review the parametric cost scenarios: state the assumptions that drive them for each "
            "app and the main sensitivities. Do not invent rates; ranges are not statistics."),
        fields={
            "assumptions": (A(item(application_id=S(), assumption=S())), "append"),
            "sensitivities": (A(item(driver=S(), effect=S())), "append"),
        }),
    "A4": Overlay(
        tier="fast", effort="low", tools=PF_TOOLS + ["app_similarity"],
        guidance=(
            "Look for functional overlap between applications (same domain, duplicate capability). "
            "Call app_similarity first: it measures code overlap from embeddings (share of "
            "near-duplicate chunks = copied code; mean best-match cosine = same capability even "
            "across languages; centroid cosine; closest chunk pairs). Report each pair's "
            "measured overlap, then confirm or reject a functional overlap from P1 capabilities "
            "and processes. Similarity proposes investigation only; never approve retirement."),
        fields={
            "overlap": (A(item(group=S(), members=A(S()), signal=S(),
                               code_overlap=NUM("app_similarity overlap share 0-1"))), "append"),
            "constraints": (A(item(constraint=S())), "append"),
        }),
    "A5": Overlay(
        tier="fast", effort="low", tools=ARTIFACT_TOOLS,
        guidance=(
            "Assess delivery readiness per app: blockers carried from P1 risk, skills needed for "
            "the stack, test safety net. Planning readiness ≠ production readiness."),
        fields={
            "blocker_deltas": (A(item(application_id=S(), blocker=S(), state=S())), "append"),
            "skills_gaps": (A(item(skill=S(), applications=A(S()), state=S())), "append"),
        }),
    "A6": Overlay(
        tier="reasoning", effort="high", tools=PF_TOOLS,
        guidance=(
            "Decide one 8R disposition per application (Retain, Retire, Rehost, Replatform, "
            "Refactor, Rearchitect, Rebuild, Replace) from the P1/P2 evidence: framework/runtime age, "
            "vulnerabilities, complexity, value, coupling, test coverage. Give the rationale, the "
            "second-best option and why not, and a wave (1 = first). Approval stays PENDING. "
            "Retire/Retain need explicit owner decisions — propose them only with strong evidence."),
        fields={
            "decisions": (A(item(application_id=S(), proposed_disposition=E(*R8), rationale=S(),
                                 second_best=E(*R8), why_not_second_best=S(), wave=I())), "decide"),
        },
        postprocess=_pp_p2_a6),
    "A7": Overlay(
        tier="reasoning", tools=ARTIFACT_TOOLS,
        guidance=(
            "Consolidate the portfolio: check that decisions, costs, readiness and sequencing are "
            "consistent; record disagreements and portfolio-level risks. You recommend; G2 authorizes."),
        fields={
            "portfolio_risks": (A(item(risk=S(), applications=A(S()), mitigation=S())), "append"),
            "disagreements": (A(item(between=A(S()), issue=S())), "append"),
        }),
}

# -- P3 Target architecture -------------------------------------------------------------

P3 = {
    "A1": Overlay(
        tier="reasoning", effort="high", tools=REPO + ["eol_lookup"],
        guidance=(
            "Propose the target architecture for the approved disposition: target runtime and "
            "framework versions, component mapping from current modules, and ADRs with rationale "
            "and consequences. Ground every runtime/framework version choice in eol_lookup "
            "(endoflife.date: current version's cycle and EOL date, supported target cycle) and "
            "cite it. NFR targets stay UNSET (engagement policy) — never invent numbers."),
        fields={
            "component_map": (A(item(component=S(), current=S(), target=S(), change=E(
                "keep", "upgrade", "replace", "split", "merge", "retire"))), "append"),
            "technology_evidence": (A(item(choice=S(), rationale=S())), "append"),
            "proposed_adrs": (A(item(adr=S(), decision=S(), rationale=S(), consequences=S(),
                                     status=E("PROPOSED"))), "append"),
            "transition_constraints": (A(item(constraint=S())), "append"),
        }),
    "A2": Overlay(
        tier="reasoning", tools=REPO,
        guidance=(
            "Define service/module boundaries from the code's domain structure. A modular monolith "
            "is a valid answer; justify any split with coupling evidence."),
        fields={
            "boundaries": (A(item(boundary=S(), modules=A(S()), justification=S())), "append"),
            "communication_needs": (A(item(**{"from": S(), "to": S()}, style=S())), "append"),
            "rationale": (A(item(point=S())), "append"),
        }),
    "A3": Overlay(
        tier="reasoning", tools=REPO,
        guidance=(
            "Design the target data architecture: schema alignment per entity, data contracts, and "
            "the migration approach with reconciliation criteria. Design only — no migration runs."),
        fields={
            "schemas": (A(item(object=S(), action=E("keep", "align", "split", "merge", "retire"),
                               detail=S())), "append"),
            "data_contracts": (A(item(contract=S(), owner=S(), detail=S())), "append"),
            "reconciliation_criteria": (A(item(criterion=S(), method=S())), "append"),
        }),
    "A4": Overlay(
        tier="reasoning", tools=REPO_SEC,
        guidance=(
            "Threat-model the target (STRIDE) using real P1 findings: vulnerabilities, secrets, "
            "auth code, input handling. Map each threat to a control and a validation criterion."),
        fields={
            "threats": (A(item(threat=S(), stride=E("S", "T", "R", "I", "D", "E"), asset=S(),
                               control=S())), "append"),
            "security_constraints": (A(item(constraint=S(), source=S())), "append"),
            "validation_criteria": (A(item(criterion=S(), method=S())), "append"),
        }),
    "A5": Overlay(
        tier="fast", effort="low", tools=REPO,
        guidance=(
            "If UI applies: map current templates/pages to target UI patterns and the service "
            "demands they create. If the seed is SKIPPED_APPROVED, verify the headless reason."),
        fields={
            "patterns": (A(item(pattern=S(), applies_to=S(), basis=S())), "append"),
            "service_demands": (A(item(demand=S(), consumer=S())), "append"),
        }),
    "A6": Overlay(
        tier="reasoning", tools=REPO,
        guidance=(
            "Build the interface contract registry from the code's real endpoints (methods, paths, "
            "payloads) and outbound integrations. State compatibility criteria per contract."),
        fields={
            "contract_registry": (A(item(endpoint=S(), method=S(), handler=S(), payload=S(),
                                         versioning=S())), "append"),
            "compatibility_criteria": (A(item(criterion=S(), source=S())), "append"),
        }),
    "A7": Overlay(
        tier="fast", effort="low", tools=ARTIFACT_TOOLS + ["repo_summary"],
        guidance=(
            "Propose the platform bill of materials (runtime, database, cache, ingress, "
            "observability) for the target. Capacity stays provisional without telemetry."),
        fields={
            "bom": (A(item(**{"item": S()}, purpose=S(), sizing_basis=S())), "append"),
            "verification_requirements": (A(item(requirement=S(), stage=S())), "append"),
        }),
    "A8": Overlay(
        tier="reasoning", tools=ARTIFACT_TOOLS,
        guidance=(
            "Cross-check A1–A7 for consistency (stack vs. components, data design vs. contracts, "
            "threats vs. controls). Report each inconsistency as a traceability gap. You cannot "
            "rewrite upstream artifacts or approve the package."),
        fields={
            "traceability": (A(item(requirement=S(), maps_to=S())), "append"),
            "consistency_issues": (A(item(issue=S(), artifacts=A(S()), severity=SEV)), "append"),
        }),
}

# -- P4 Planning -----------------------------------------------------------------------------

P4 = {
    "A1": Overlay(
        tier="fast", effort="low", tools=ARTIFACT_TOOLS,
        guidance="Translate the portfolio wave into logical wave architecture and replan triggers.",
        fields={"replan_triggers": (A(item(trigger=S(), response=S())), "append"),
                "infeasibilities": (A(item(issue=S(), effect=S())), "append")}),
    "A2": Overlay(
        tier="fast", effort="low", tools=ARTIFACT_TOOLS,
        guidance="Specify the wave: component scope, entry/exit criteria and inter-wave constraints.",
        fields={"entry_exit_criteria": (A(item(gate=S(), criterion=S())), "append"),
                "interwave_constraints": (A(item(constraint=S())), "append")}),
    "A3": Overlay(
        tier="coding", tools=ARTIFACT_TOOLS + ["repo_summary", "list_dir", "grep"],
        guidance=(
            "Generate the concrete task DAG for this app's modernization from the P3 architecture: "
            "one task per meaningful unit of change (dependency upgrades, module refactors, data "
            "changes, test work). Use ids 'L-T<n>', depends_on referencing other task ids (seed "
            "ids T1-baseline, T2-code, T3-data-auth, T4-validate are valid). Phase is P5 for code "
            "and P6 for data. Estimates are assumptions."),
        fields={
            "tasks": (A(item(task_id=S(), phase=E("P5", "P6"), kind=S(), component=S(),
                             owner_role=S(), acceptance=S(), depends_on=A(S()),
                             estimate_days=NUM())), "decide"),
            "estimate_assumptions": (A(item(task=S(), estimate=S())), "append"),
        },
        postprocess=_pp_p4_a3),
    "A4": Overlay(
        tier="fast", effort="low", tools=ARTIFACT_TOOLS,
        guidance="Draft runbook steps for the generated tasks; unresolved bindings stay declared.",
        fields={"runbook_steps": (A(item(step=I(), action=S(), task=S(), gate=S())), "append")}),
    "A5": Overlay(
        tier="fast", effort="low", tools=ARTIFACT_TOOLS,
        guidance=("Propose a role assignment for EVERY task_id in the A3 task list (read it with "
                  "get_artifact A3 field 'tasks'), including L-T* tasks; the 'task' value must be the "
                  "exact task_id. Add skill needs; proposals are not commitments."),
        fields={"assignments": (A(item(task=S(), role=S(), skills=A(S()))), "append"),
                "coverage_gaps": (A(item(gap=S())), "append")}),
    "A6": Overlay(
        tier="fast", effort="low", tools=ARTIFACT_TOOLS + ["list_dependencies"],
        guidance="Select concrete tools/versions per task (build, test, migration, scanning).",
        fields={"tool_bindings": (A(item(tool=S(), version=S(), tasks=A(S()), why=S())), "append")}),
    "A7": Overlay(
        tier="fast", effort="low", tools=ARTIFACT_TOOLS + ["grep"],
        guidance="Plan validation: tests per requirement, test data and evidence per gate.",
        fields={"tests": (A(item(test=S(), criterion=S(), stage=S())), "append"),
                "requirement_coverage": (A(item(requirement=S(), test=S())), "append")}),
    "A8": Overlay(
        tier="fast", effort="low", tools=ARTIFACT_TOOLS,
        guidance="Plan rollback/contingency per irreversible step; name the decision authority.",
        fields={"recovery_plans": (A(item(scope=S(), route=S())), "append"),
                "risk_responses": (A(item(risk=S(), response=S())), "append")}),
    "A9": Overlay(
        tier="reasoning", tools=ARTIFACT_TOOLS,
        guidance=(
            "Validate the plan set: every task has an owner, a tool binding, a test and a recovery "
            "route; context hashes agree. Report conflicts precisely; never repair producers."),
        fields={"conflicts": (A(item(conflict=S(), owner=S())), "append"),
                "revision_requests": (A(item(finding=S(), owner=S())), "append")}),
}

OVERLAYS: dict[int, dict[str, Overlay]] = {1: P1, 2: P2, 3: P3, 4: P4}


def overlay_for(phase: int, local_id: str) -> Overlay | None:
    return OVERLAYS.get(phase, {}).get(local_id)
