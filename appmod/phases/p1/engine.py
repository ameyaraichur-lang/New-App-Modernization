"""Phase 1 — Discovery engine.

11 tool-backed runners over the deterministic repo scanner, plus the two
phase-specific gate behaviours:

  G1 snapshot — seals A3/A6/A7/A9 (transitively A1–A7, A9) and takes the
                available A8 snapshot or an explicit PENDING marker; embeds a
                payload digest so A10 synthesizes from the sealed manifest.
  G2 release  — binds the decision to evidence scope: with no HUMAN_CONFIRMED
                stakeholder responses the only permitted release is
                READY_FOR_PORTFOLIO_DRAFT (blueprint F05/F10: simulated
                business input restricts — never widens — decision scope).

All payload facts carry evidence classes; telemetry the corpus cannot provide
is NOT_ASSESSED, never a healthy default (A4 contract rule).
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any, Callable

from appmod.agents.runtime import AgentOutcome
from appmod.kernel.gates import GateContext, GateResult
from appmod.tools import analyzers
from appmod.tools.repo_intel import CODE_LANGUAGES, RepoScan, parse_dependencies, scan_repo

_now = lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _finding(fid: str, cls: str, statement: str, **extra) -> dict[str, Any]:
    out = {"id": fid, "evidence_class": cls, "statement": statement}
    out.update(extra)
    return out


class P1AgentRunner:
    """Deterministic P1 agent runner: every agent's payload is derived from
    the authorized repository snapshot (run_inputs.source_pins.repo_path) and
    its upstream artifacts. No model calls — M1 keeps discovery fully
    evidence-bound; LLM enrichment slots in later behind this same runner."""

    def __init__(self, confirmed_stakeholder: bool = False, use_analyzers: bool | None = None) -> None:
        self._scan: RepoScan | None = None
        if use_analyzers is None:
            from appmod.config import get_settings
            use_analyzers = get_settings().analyzers == "on"
        self.use_analyzers = use_analyzers
        # callable -> recorded questions/answers (human mode)
        self.answers_provider: Callable[[], list[dict[str, Any]]] | None = None
        # Pilot decision mode: designated apps receive simulated stakeholder
        # confirmations recorded as HUMAN_CONFIRMED with an explicit
        # pilot-simulated basis, and G2 records them as accepted exceptions
        # (blueprint G2: unresolved issues "explicitly accepted by an
        # authorized reviewer" — never silently upgraded).
        self.confirmed_stakeholder = confirmed_stakeholder

    # -- shared scan ----------------------------------------------------------

    @property
    def scan(self) -> RepoScan:
        if self._scan is None:
            raise RuntimeError("repo_path not set: call bind_repo first")
        return self._scan

    def bind_repo(self, repo_path: Path) -> None:
        if self._scan is None or self._scan.root != Path(repo_path).resolve():
            self._scan = scan_repo(Path(repo_path))
        return None

    # -- dispatch ---------------------------------------------------------------

    def run(self, agent_spec: dict[str, Any], inputs: dict[str, dict],
            policy: Any) -> AgentOutcome:
        local = agent_spec["local_id"]
        handler = getattr(self, f"_run_{local.lower()}", None)
        if handler is None:
            raise RuntimeError(f"P1 has no runner for {local}")
        return handler(agent_spec, inputs, policy)

    # -- A1 Repo Intelligence -----------------------------------------------------

    def _run_a1(self, spec, inputs, policy) -> AgentOutcome:
        s = self.scan
        deps = parse_dependencies(s)
        code_dirs: dict[str, int] = {}
        for f in s.files:
            if f["language"] in CODE_LANGUAGES and f["language"] != "sql":
                top = f["path"].split("/")[0]
                code_dirs[top] = code_dirs.get(top, 0) + 1
        components = [
            {"name": d, "code_files": n} for d, n in sorted(code_dirs.items(), key=lambda kv: -kv[1])[:12]
        ]
        sbom: dict[str, Any] = {
            "format": "appmod-lite-sbom/1",
            "generated_at": _now(),
            "packages": [
                {"name": d["name"], "source": d["source"]} for d in deps
            ],
            "license": s.license or {"type": "UNKNOWN"},
        }
        disabled: dict[str, Any] = {"status": "DISABLED"}
        syft = analyzers.sbom(s.root) if self.use_analyzers else disabled
        scc = analyzers.loc_metrics(s.root) if self.use_analyzers else disabled
        if syft.get("status") == "OK":
            sbom.update(format="syft-json/summary", generator=syft.get("version"),
                        package_count=syft["package_count"], by_type=syft["by_type"],
                        packages=[{k: p[k] for k in ("name", "version", "type", "purl")}
                                  for p in syft["packages"][:250]])
        content = {k: v for k, v in sbom.items() if k != "generated_at"}
        sbom_ref = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()[:32]
        findings: list[dict[str, Any]] = [
            _finding("A1-F1", "OBSERVED",
                     f"{len(s.files)} source files, {s.loc} LOC across "
                     f"{len(s.languages)} languages ({s.code_loc} code LOC); primary: "
                     f"{s.primary_language}"),
        ]
        gaps: list[dict[str, Any]] = []
        if scc.get("status") == "OK":
            top = ", ".join(f"{x['language']} {x['code']}" for x in scc["languages"][:4])
            findings.append(_finding("A1-F5", "OBSERVED",
                                     f"scc: {scc['total_code']} code lines, cyclomatic complexity "
                                     f"{scc['total_complexity']} ({top})"))
        if syft.get("status") == "OK":
            findings.append(_finding("A1-F6", "OBSERVED",
                                     f"syft SBOM: {syft['package_count']} packages "
                                     f"({', '.join(f'{k}={v}' for k, v in syft['by_type'].items())})"))
        else:
            gaps.append({"requirement": "SBOM generation", "impact": "package inventory from manifests only",
                         "state": "NOT_ASSESSED", "reason": syft.get("detail", syft.get("status"))})
        lic_type = (s.license or {}).get("type")
        if lic_type and lic_type != "UNKNOWN":
            findings.append(_finding(
                "A1-F2", "DOCUMENTED", f"License: {lic_type} ({s.license['file']})"))
        elif lic_type == "UNKNOWN":
            findings.append(_finding("A1-F2", "UNKNOWN",
                                     f"License file present but unrecognized ({s.license['file']})"))
        else:
            findings.append(_finding("A1-F2", "UNKNOWN", "No license file found"))
        if not s.tests:
            findings.append(_finding("A1-F3", "OBSERVED", "No test files discovered"))
        if not s.entry_candidates:
            findings.append(_finding("A1-F4", "INFERRED", "No obvious application entry point; library-style repo"))
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "repositories": [{
                    "path": str(s.root), "files": len(s.files), "loc": s.loc,
                    "code_loc": s.code_loc,
                    "primary_language": s.primary_language,
                    "languages": dict(sorted(s.languages.items(), key=lambda kv: -kv[1])),
                    "test_files": len(s.tests),
                    "commit": s.commit,
                }],
                "components": components,
                "dependencies": deps,
                "sbom_ref": sbom_ref,
                "coverage": {
                    "measured": False,
                    "test_files": len(s.tests),
                    "test_paths": list(s.tests[:200]),
                    "note": "Runtime coverage not measured in discovery; test inventory only.",
                },
                "build_status": "UNKNOWN",
                "loc_metrics": ({"tool": scc.get("version"), "languages": scc["languages"][:12],
                                 "total_code": scc["total_code"],
                                 "total_complexity": scc["total_complexity"]}
                                if scc.get("status") == "OK" else {"status": scc.get("status")}),
                "findings": [f["id"] for f in findings],
            },
            findings=findings,
            gaps=gaps,
            evidence_refs=[{"source": "repo-scan", "method": "deterministic file/manifest scan"}]
            + ([{"source": "scc", "method": "LOC/complexity metrics"}] if scc.get("status") == "OK" else [])
            + ([{"source": "syft", "method": "SBOM"}] if syft.get("status") == "OK" else []),
            scope={"repo": s.root.name, "boundary": "authorized snapshot"},
            applicability={"route": "full"},
        )

    # -- A4 Infrastructure & Runtime Profiler -----------------------------------------

    def _run_a4(self, spec, inputs, policy) -> AgentOutcome:
        s = self.scan
        return AgentOutcome(
            status="PARTIAL",
            payload={
                "resources": [
                    {"kind": "repo-infra-file", "path": p} for p in s.infra_files[:30]
                ],
                "observation_window": {
                    "available": False,
                    "note": "Corpus repository has no live runtime; utilization NOT_ASSESSED.",
                },
                "utilization": [],
                "runtime_relations": [],
                "recovery_evidence": [],
                "portability_findings": [
                    _finding("A4-F1", "DOCUMENTED",
                             f"{len(s.infra_files)} infra/CI descriptor files present")
                    if s.infra_files else
                    _finding("A4-F1", "OBSERVED",
                             "No Dockerfile/CI/IaC descriptors found; hosting model code-inferred only"),
                ],
            },
            findings=[_finding("A4-F2", "UNKNOWN",
                               "Runtime telemetry, RTO/RPO and restore evidence unavailable for corpus repos")],
            gaps=[{"requirement": "runtime utilization baseline", "impact": "capacity unknown",
                   "state": "NOT_ASSESSED"}],
            evidence_refs=[{"source": "repo-scan", "method": "infra descriptor inventory"}],
            scope={"repo": s.root.name},
            applicability={"route": "static-only", "label": "static-only view (no runtime telemetry)"},
        )

    # -- A5 Journey Intelligence -----------------------------------------------------

    def _run_a5(self, spec, inputs, policy) -> AgentOutcome:
        s = self.scan
        if s.has_ui():
            route = "UI"
        elif s.routes:
            route = "API_ONLY"
        else:
            route = "HEADLESS_BATCH"
        journeys = [
            {"name": r["route"] or "(root)", "framework": r["framework"], "file": r["file"]}
            for r in s.routes[:40]
        ]
        if route == "HEADLESS_BATCH":
            return AgentOutcome(
                status="SKIPPED_APPROVED",
                payload={
                    "capability_route": "HEADLESS_BATCH",
                    "journeys": [], "personas": [], "friction_findings": [],
                    "analytics_window": None,
                },
                findings=[_finding("A5-F1", "OBSERVED",
                                   "No UI templates and no HTTP routes: approved headless/batch skip")],
                scope={"repo": s.root.name},
                applicability={"route": "HEADLESS_BATCH",
                               "skip_policy": "pilot-default G0 route classification"},
            )
        return AgentOutcome(
            status="PARTIAL",
            payload={
                "capability_route": route,
                "journeys": journeys,
                "personas": [{"name": "end-user", "basis": "INFERRED"}],
                "friction_findings": [],
                "analytics_window": None,
            },
            findings=[_finding("A5-F1", "DOCUMENTED",
                               f"{len(journeys)} HTTP endpoints mapped as journey proxies; no behavioral analytics")],
            gaps=[{"requirement": "observed usage analytics", "impact": "friction unmeasured",
                   "state": "NOT_ASSESSED"}],
            evidence_refs=[{"source": "route-scan", "method": "route decorator/pattern extraction"}],
            scope={"repo": s.root.name},
            applicability={"route": route},
        )

    # -- A2 Architecture ----------------------------------------------------------------

    def _run_a2(self, spec, inputs, policy) -> AgentOutcome:
        s = self.scan
        a1 = inputs.get("A1", {}).get("payload", {})
        relations: list[dict[str, Any]] = []
        import_counts: dict[str, int] = {}
        py_files = [f for f in s.files if f["language"] == "python"]
        internal_modules = {
            f["path"].replace("/", ".").rsplit(".", 1)[0] for f in py_files
        }
        for f in py_files:
            p = s.root / f["path"]
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            src_mod = f["path"].replace("/", ".").rsplit(".", 1)[0]
            for m in re.finditer(r"^\s*(?:from\s+([\w.]+)|import\s+([\w.]+))", text, re.M):
                mod = (m.group(1) or m.group(2) or "").split(".")[0]
                if not mod:
                    continue
                import_counts[mod] = import_counts.get(mod, 0) + 1
                if mod in {im.split(".")[0] for im in internal_modules} and mod != src_mod.split(".")[0]:
                    relations.append({"from": f["path"], "to": mod, "kind": "internal-import"})
        coupling = [
            {"module": mod, "import_count": n, "signal": "shared dependency"}
            for mod, n in sorted(import_counts.items(), key=lambda kv: -kv[1])[:8]
        ]
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "components": a1.get("components", []),
                "relations": relations[:200],
                "c4_refs": [{"level": "C4-Container", "note": "single-repo static view"}],
                "coupling_findings": coupling,
                "inferred_decisions": [],
            },
            findings=[_finding("A2-F1", "OBSERVED",
                               f"{len(relations)} internal import relations across {len(py_files)} python files"),
                      _finding("A2-F2", "INFERRED",
                               "Static-only architecture view: no runtime telemetry to confirm call paths")],
            evidence_refs=[{"source": "import-graph", "method": "static import parse"}],
            scope={"repo": s.root.name, "view": "static"},
            applicability={"route": "static-only"},
        )

    # -- A3 Data Intelligence ---------------------------------------------------------------

    def _run_a3(self, spec, inputs, policy) -> AgentOutcome:
        s = self.scan
        datasets = [
            {"name": p, "kind": "sql-file"} for p in s.sql_files[:30]
        ] + [
            {"name": p, "kind": "model-file"} for p in s.model_files[:30]
        ]
        integrations = [
            {"endpoint": r["route"] or "(root)", "framework": r["framework"], "file": r["file"]}
            for r in s.routes[:40]
        ]
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "datasets": datasets,
                "integrations": integrations,
                "api_contract_refs": [i["endpoint"] for i in integrations[:20]],
                "lineage_observations": [],
                "volume_evidence": [],
            },
            findings=[_finding(
                "A3-F1", "OBSERVED",
                f"Data estate: {len(s.sql_files)} SQL files, {len(s.model_files)} model files, "
                f"{len(s.migrations)} migration entries; volumes NOT_ASSESSED")],
            gaps=[{"requirement": "data volumes/latency", "impact": "sizing unknown",
                   "state": "NOT_ASSESSED"}],
            evidence_refs=[{"source": "repo-scan", "method": "SQL/model/migration inventory"}],
            scope={"repo": s.root.name},
            applicability={"route": "metadata-only", "note": "no credentials, metadata only"},
        )

    # -- A6 Compliance ---------------------------------------------------------------------

    def _run_a6(self, spec, inputs, policy) -> AgentOutcome:
        s = self.scan
        a1 = inputs.get("A1", {})
        deps = a1.get("payload", {}).get("dependencies", [])
        on = self.use_analyzers
        def off(tool: str) -> dict[str, Any]:
            return {"status": "DISABLED", "tool": tool}
        osv = analyzers.vulnerabilities(s.root) if on else off("osv-scanner")
        leaks = analyzers.secrets(s.root) if on else off("gitleaks")
        sast = analyzers.static_analysis(s.root) if on else off("semgrep")
        control_findings = [
            {"file": f["file"], "kind": f["kind"], "severity": "high", "source": "pattern-scan"}
            for f in s.secret_findings[:30]
        ]
        if leaks.get("status") == "OK":
            control_findings += [{"file": f["file"], "line": f["line"], "kind": f"secret:{f['rule']}",
                                  "severity": "high", "source": "gitleaks"} for f in leaks["findings"][:50]]
        if sast.get("status") == "OK":
            control_findings += [{"file": f["path"], "line": f["line"], "kind": f["rule"],
                                  "severity": _sast_sev(f["severity"]), "message": f["message"],
                                  "source": "semgrep"} for f in sast["findings"][:80]]
        vulns = []
        if osv.get("status") == "OK":
            seen: set[str] = set()
            for v in sorted(osv["vulnerabilities"], key=lambda v: -_cvss(v["severity"])):
                key = f"{v['id']}|{v['package']}"
                if key in seen:
                    continue
                seen.add(key)
                vulns.append({"id": v["id"], "aliases": v["aliases"], "package": f"{v['package']}@{v['version']}",
                              "ecosystem": v["ecosystem"], "cvss": v["severity"] or None,
                              "severity": _cvss_band(v["severity"]), "summary": v["summary"],
                              "manifest": v["manifest"], "source": "osv-scanner"})
        license_flags = []
        lic_type = (s.license or {}).get("type", "UNKNOWN")
        if lic_type in ("UNKNOWN", "GPL"):
            license_flags.append({"scope": "repository", "license": lic_type,
                                  "review": "license identification/compatibility review required"})

        def ctl(name: str, res: dict, method: str) -> dict:
            return {"control": name, "status": "ASSESSED" if res.get("status") == "OK" else "NOT_ASSESSED",
                    "method": method, "tool": res.get("version") or res.get("tool"),
                    **({} if res.get("status") == "OK" else {"reason": res.get("detail", res.get("status"))})}

        controls = [
            ctl("secret-hygiene", leaks, "gitleaks dir scan (values redacted) + pattern scan"),
            {"control": "license-review", "status": "ASSESSED", "method": "license file detection"},
            ctl("vulnerability-scan", osv, "osv-scanner source scan with transitive resolution"),
            ctl("static-code-analysis", sast, "semgrep p/default"),
        ]
        findings = [_finding("A6-F1", "OBSERVED",
                             f"{len(s.secret_findings)} secret-pattern matches; gitleaks: "
                             f"{leaks.get('finding_count', 'not run')} findings")]
        gaps = []
        for res, req, impact in ((osv, "dependency vulnerability scan", "CVE exposure unknown"),
                                 (sast, "static code analysis", "code-level weaknesses unknown"),
                                 (leaks, "secret scan", "hardcoded secret exposure partly unknown")):
            if res.get("status") != "OK":
                gaps.append({"requirement": req, "impact": impact, "state": "NOT_ASSESSED",
                             "reason": res.get("detail", res.get("status"))})
        if osv.get("status") == "OK":
            crit = sum(1 for v in vulns if v["severity"] in ("critical", "high"))
            findings.append(_finding("A6-F2", "OBSERVED",
                                     f"osv-scanner: {len(vulns)} distinct advisories across dependencies; "
                                     f"{crit} critical/high"))
        else:
            findings.append(_finding("A6-F2", "UNKNOWN", "Dependency vulnerability scan NOT_RUN"))
        if sast.get("status") == "OK":
            findings.append(_finding("A6-F3", "OBSERVED",
                                     f"semgrep p/default: {sast['finding_count']} findings"))
        return AgentOutcome(
            status="COMPLETE" if not gaps else "PARTIAL",
            payload={
                "applicable_controls": controls,
                "vulnerabilities": vulns[:150],
                "control_findings": control_findings,
                "license_review_flags": license_flags,
                "assessment_coverage": {
                    "dependencies_declared": len(deps),
                    "scanners": [r.get("tool") for r in (osv, leaks, sast) if r.get("status") == "OK"],
                    "not_run": [r.get("tool") for r in (osv, leaks, sast) if r.get("status") != "OK"],
                },
            },
            findings=findings,
            gaps=gaps,
            evidence_refs=[{"source": r.get("tool", "?"), "method": "static analyzer"}
                           for r in (osv, leaks, sast) if r.get("status") == "OK"]
            + [{"source": "license-detect", "method": "deterministic patterns"}],
            scope={"repo": s.root.name},
            applicability={"route": "static"},
        )

    # -- A7 UX Evaluator ------------------------------------------------------------------------

    def _run_a7(self, spec, inputs, policy) -> AgentOutcome:
        a5 = inputs.get("A5", {})
        route = a5.get("payload", {}).get("capability_route")
        if route in ("HEADLESS_BATCH", None):
            return AgentOutcome(
                status="SKIPPED_APPROVED",
                payload={
                    "evaluation_route": "NOT_APPLICABLE",
                    "criteria": [], "observations": [], "coverage": {"assessed": 0},
                    "evidence_refs": [{"source": "A5", "method": "route propagation"}],
                },
                findings=[_finding("A7-F1", "DOCUMENTED",
                                   "A5 headless/batch route propagates a reasoned skip (not a zero score)")],
                scope={"repo": self.scan.root.name},
                applicability={"route": "skip-propagated", "skip_policy": "pilot-default"},
            )
        s = self.scan
        criteria = [
            {"criterion": "template-form-labels", "status": "sampled",
             "note": "heuristic HTML inspection"},
        ]
        label_hits = 0
        for t in s.templates[:50]:
            try:
                text = (s.root / t).read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if re.search(r"<label|aria-label", text):
                label_hits += 1
        observations = [
            _finding("A7-F1", "OBSERVED",
                     f"{label_hits}/{min(len(s.templates), 50)} templates contain label/aria-label markup"),
        ]
        return AgentOutcome(
            status="PARTIAL",
            payload={
                "evaluation_route": "UI_HEURISTIC" if route == "UI" else "API_DX",
                "criteria": criteria,
                "observations": [o["statement"] for o in observations],
                "coverage": {"assessed": min(len(s.templates), 50),
                             "basis": "heuristic criteria subset; not full accessibility audit"},
                "evidence_refs": [{"source": "template-scan", "method": "markup heuristics"}],
            },
            findings=observations,
            gaps=[{"requirement": "full accessibility evaluation", "impact": "a11y compliance unknown",
                   "state": "NOT_ASSESSED"}],
            scope={"repo": s.root.name},
            applicability={"route": route},
        )

    # -- A9 Business Process --------------------------------------------------------------------

    def _run_a9(self, spec, inputs, policy) -> AgentOutcome:
        s = self.scan
        processes = [
            {"name": f"{r['framework']}:{r['route'] or '(root)'}", "trigger": "HTTP",
             "file": r["file"], "basis": "INFERRED"}
            for r in s.routes[:40]
        ]
        return AgentOutcome(
            status="PARTIAL",
            payload={
                "processes": processes,
                "business_rules": [],
                "exception_paths": [],
                "component_links": [],
                "owner_confirmations": [],
            },
            findings=[_finding("A9-F1", "INFERRED",
                               f"{len(processes)} candidate business processes inferred from routes; "
                               "no confirmed process documentation")],
            gaps=[{"requirement": "business criticality confirmation", "impact": "downstream decision scope restricted",
                   "state": "PENDING_HUMAN"}],
            evidence_refs=[{"source": "route-scan", "method": "route-to-process inference"}],
            scope={"repo": s.root.name},
            applicability={"route": "code-derived"},
        )

    # -- A8 Stakeholder Elicitation (async, simulated in pilot) -----------------------------------

    def _run_a8(self, spec, inputs, policy) -> AgentOutcome:
        if self.answers_provider is not None:
            return self._run_a8_recorded()
        if self.confirmed_stakeholder:
            confirmed = [
                {
                    "question": "What is the business criticality of this application?",
                    "answer": "medium-high (serves representative user journeys)",
                    "respondent": "pilot-simulated-business-owner",
                    "date": _now(),
                    "evidence_class": "HUMAN_CONFIRMED",
                    "basis": "PILOT SIMULATION recorded as accepted exception at G2",
                },
                {
                    "question": "Which compliance obligations apply?",
                    "answer": "standard corporate baseline; no regulated-data scope in pilot",
                    "respondent": "pilot-simulated-compliance-owner",
                    "date": _now(),
                    "evidence_class": "HUMAN_CONFIRMED",
                    "basis": "PILOT SIMULATION recorded as accepted exception at G2",
                },
            ]
            unresolved = [
                {"question": "roadmap ownership and funding window", "state": "PENDING"},
            ]
        else:
            confirmed = []
            unresolved = [
                {"question": "business criticality", "state": "PENDING"},
                {"question": "compliance obligations", "state": "PENDING"},
            ]
        return AgentOutcome(
            status="COMPLETE" if confirmed else "PARTIAL",
            payload={
                "questions": [
                    "What is the business criticality of this application?",
                    "Which compliance obligations apply?",
                    "Who owns the data and the roadmap?",
                ],
                "confirmed_responses": confirmed,
                "requirements": [
                    {"requirement": r["answer"][:80], "source": r["respondent"]}
                    for r in confirmed
                ],
                "unresolved_items": unresolved,
                "hypothetical_examples": [
                    {"note": "PILOT SIMULATION — HYPOTHETICAL, never decision evidence",
                     "example_question": "Is this app business-critical?",
                     "example_answer": "(simulated yes/no is intentionally not recorded as evidence)"},
                ],
            },
            findings=[_finding(
                "A8-F1",
                "HUMAN_CONFIRMED" if confirmed else "HYPOTHETICAL",
                "Pilot mode: simulated stakeholder evidence; "
                + ("confirmations recorded as accepted exceptions (decision scope possible)"
                   if confirmed else "no human respondents; decision scope restricted to DRAFT"))],
            gaps=[] if confirmed else [
                {"requirement": "stakeholder responses", "impact": "G2 restricted to DRAFT scope",
                 "state": "PENDING"}],
            evidence_refs=[{"source": "pilot-policy", "method": "simulated elicitation"}],
            scope={"repo": "pilot"},
            applicability={"route": "async-simulated"},
        )

    def _run_a8_recorded(self) -> AgentOutcome:
        """Human mode: confirmations are exactly the answers recorded through
        the questionnaire API (respondent identity + timestamp kept)."""
        qs = (self.answers_provider() if self.answers_provider else None) or []
        answered = [q for q in qs if q.get("status") == "ANSWERED"]
        open_qs = [q for q in qs if q.get("status") != "ANSWERED"]
        confirmed = [{
            "question_id": q["question_id"], "question": q["question"], "answer": q["answer"],
            "respondent": q["respondent"], "date": q["answered_at"],
            "evidence_class": "HUMAN_CONFIRMED", "basis": "recorded answer via questionnaire API",
        } for q in answered]
        questions = [q["question"] for q in qs] or list(SEED_QUESTIONS)
        return AgentOutcome(
            status="COMPLETE" if confirmed and not open_qs else "PARTIAL",
            payload={
                "questions": questions,
                "confirmed_responses": confirmed,
                "requirements": [{"requirement": c["answer"][:200], "source": c["respondent"],
                                  "question_id": c["question_id"]} for c in confirmed],
                "unresolved_items": [{"question": q["question"], "question_id": q["question_id"],
                                      "state": "PENDING"} for q in open_qs],
                "hypothetical_examples": [],
            },
            findings=[_finding("A8-F1", "HUMAN_CONFIRMED" if confirmed else "UNKNOWN",
                               f"{len(confirmed)} recorded stakeholder answers; {len(open_qs)} open")],
            gaps=[{"requirement": "stakeholder responses", "impact": "decision scope restricted",
                   "state": "PENDING_HUMAN", "open": len(open_qs)}] if open_qs else [],
            evidence_refs=[{"source": "questionnaire-api", "method": "recorded human answers"}],
            scope={"repo": self.scan.root.name},
            applicability={"route": "async-recorded"},
        )

    def fingerprint(self) -> str:
        return json.dumps({"engine": "P1", "commit": self.scan.commit, "root": str(self.scan.root),
                           "analyzers": self.use_analyzers, "sim": self.confirmed_stakeholder,
                           "recorded": self.answers_provider is not None}, sort_keys=True)

    # -- A10 Synthesis ---------------------------------------------------------------------------

    def _run_a10(self, spec, inputs, policy) -> AgentOutcome:
        g1 = inputs.get("G1", {})
        digest = g1.get("payload", {}).get("evidence_manifest", {}).get("snapshot_digest", {})
        domains = [
            {"domain": "technical",
             "sources": ["A1", "A2", "A3", "A4"],
             "summary": f"technical evidence: {len(digest.get('A1', {}).get('components', []))} components, "
                        f"{digest.get('A1', {}).get('loc', 0)} LOC; runtime telemetry NOT_ASSESSED"},
            {"domain": "experience",
             "sources": ["A5", "A7"],
             "summary": f"experience route: {digest.get('A5', {}).get('route', 'unknown')}; "
                        "analytics unavailable"},
            {"domain": "business/control",
             "sources": ["A6", "A8", "A9"],
             "summary": "controls: static scan only; stakeholder evidence PENDING (pilot); "
                        "processes code-inferred"},
        ]
        contradictions = digest.get("contradictions", [])
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "domain_summaries": domains,
                "report_ref": g1.get("payload", {}).get("evidence_manifest", {}).get("manifest_hash", ""),
                "evidence_index": sorted(digest.keys()),
                "contradictions": contradictions,
                "gaps": digest.get("gaps", []),
                "confidence_basis": {
                    "technical": "OBSERVED/DOCUMENTED",
                    "experience": "DOCUMENTED/INFERRED",
                    "business": "INFERRED/HYPOTHETICAL — decisions restricted",
                },
            },
            findings=[_finding("A10-F1", "DOCUMENTED",
                               "Synthesis bound to sealed G1 manifest; unresolved conflicts preserved, not resolved")],
            evidence_refs=[{"source": "G1", "method": "sealed manifest digest"}],
            scope={"repo": "sealed-snapshot"},
            applicability={"route": "synthesis"},
        )

    # -- A11 Risk Scoring ---------------------------------------------------------------------------

    def _run_a11(self, spec, inputs, policy) -> AgentOutcome:
        taxonomy = policy.get("risk_taxonomy") if policy else None
        drivers = self._risk_drivers()
        dims = []
        unassessed = []
        for dim in (taxonomy or {}).get("dimensions", ["technical", "security", "data", "operational", "organizational"]):
            if dim == "operational":
                unassessed.append({"dimension": "operational", "reason": "no runtime telemetry (A4 PARTIAL)"})
            elif dim == "organizational":
                unassessed.append({"dimension": "organizational", "reason": "stakeholder input PENDING (A8)"})
            elif (matched := drivers.get(dim)) is None:
                unassessed.append({"dimension": dim, "reason": "required analyzer not available (NOT_ASSESSED)"})
            else:
                dims.append({"dimension": dim, "score": min(5, 1 + len(matched)),
                             "basis": f"rubric {policy.version if policy else 'none'}: 1 + one point per "
                                      f"matched anchor ({len(matched)} matched)",
                             "drivers": matched, "evidence": "repo scan + analyzers"})
        return AgentOutcome(
            status="COMPLETE",
            payload={
                "risk_dimensions": dims,
                "scores": [{"dimension": d["dimension"], "score": d["score"]} for d in dims],
                "unassessed_dimensions": unassessed,
                "blockers": [],
                "mitigations": [
                    {"for": "organizational", "action": "obtain stakeholder confirmations before final decisions"},
                ],
                "handoff_recommendation": "READY_FOR_PORTFOLIO_DRAFT",
            },
            findings=[_finding("A11-F1", "DOCUMENTED",
                               f"Scoring under rubric {policy.version if policy else 'none'} "
                               f"({(policy.bundle.get('label') if policy else '') or 'no label'}); "
                               "unassessed dimensions listed, not averaged")],
            evidence_refs=[{"source": "policy-rubric", "method": "configured scoring"}],
            scope={"policy": policy.version if policy else "none"},
            applicability={"route": "capstone"},
        )

    def _risk_drivers(self) -> dict[str, list[str] | None]:
        """Rubric anchors matched by deterministic evidence; None = dimension not assessable."""
        s = self.scan
        tech = []
        if s.code_loc > 5000:
            tech.append(f"code LOC > 5,000 ({s.code_loc})")
        if s.code_loc > 50000:
            tech.append("code LOC > 50,000")
        if not s.tests:
            tech.append("no automated tests found")
        n_deps = len(parse_dependencies(s))
        if n_deps > 40:
            tech.append(f"more than 40 declared dependencies ({n_deps})")
        security: list[str] | None = None
        if self.use_analyzers:
            osv = analyzers.vulnerabilities(s.root)
            if osv.get("status") == "OK":
                bands = {_cvss_band(v.get("severity")) for v in osv.get("vulnerabilities", [])}
                n = len(osv.get("vulnerabilities", []))
                security = []
                if n:
                    security.append(f"any known vulnerability (OSV: {n})")
                if bands & {"medium", "high", "critical"}:
                    security.append("any medium-or-worse vulnerability")
                if bands & {"high", "critical"}:
                    security.append("any high-or-worse vulnerability")
                if "critical" in bands or s.secret_findings:
                    security.append("any critical vulnerability or hardcoded secret")
        data = []
        if s.has_data_layer():
            data.append("has a persistent data layer (models, SQL or migrations)")
            if len(s.model_files) > 10:
                data.append(f"more than 10 model/entity files ({len(s.model_files)})")
            if s.sql_files or len(s.migrations) > 20:
                data.append("raw SQL files or more than 20 migrations")
        return {"technical": tech, "security": security, "data": data}


# ---------------------------------------------------------------------------
# P1 gate overrides
# ---------------------------------------------------------------------------


def p1_snapshot_gate(ctx: GateContext) -> GateResult:
    """P1 G1: seal technical fan-in + available A8 snapshot (or PENDING)."""
    required = ["A3", "A6", "A7", "A9"]
    refs: dict[str, Any] = {}
    blockers: list[str] = []
    digest: dict[str, Any] = {}
    for node, art in ctx.inputs.items():
        errs = _intake_blockers(art)
        if errs:
            blockers.extend(errs)
            continue
        refs[node] = {
            "artifact_id": art["artifact_id"], "version": art["artifact_version"],
            "status": art["status"], "content_hash": art["content_hash"],
        }
        payload = art.get("payload", {})
        digest[node] = {
            "status": art["status"],
            "route": payload.get("capability_route") or payload.get("evaluation_route") or payload.get("applicability", {}).get("route"),
            "components": payload.get("components", [])[:5],
            "loc": (payload.get("repositories") or [{}])[0].get("loc", 0) if payload.get("repositories") else 0,
            "gaps": art.get("gaps", [])[:5],
        }
    for node in required:
        if node not in refs:
            blockers.append(f"required producer {node} missing from snapshot")
    a8 = ctx.published.get("A8")
    if a8 and not _intake_blockers(a8):
        refs["A8"] = {"artifact_id": a8["artifact_id"], "version": a8["artifact_version"],
                      "state": "AVAILABLE"}
        digest["A8"] = {"status": a8["status"],
                        "confirmed": len(a8.get("payload", {}).get("confirmed_responses", []))}
    else:
        refs["A8"] = {"state": "PENDING", "rule": "async lane; never blocks fan-in"}
        digest["A8"] = {"status": "PENDING", "confirmed": 0}

    if blockers:
        return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)

    manifest_hash = hashlib.sha256(json.dumps(refs, sort_keys=True).encode()).hexdigest()
    payload = {
        "evidence_manifest": {
            "artifact_refs": refs,
            "snapshot_digest": digest,
            "manifest_hash": manifest_hash,
            "policy_version": ctx.policy.version if ctx.policy else "none",
            "sealed_at": _now(),
        }
    }
    return GateResult("PUBLISHED", "COMPLETE", payload, [])


def p1_release_gate(ctx: GateContext) -> GateResult:
    """P1 G2: scope-controlled release. No HUMAN_CONFIRMED stakeholder
    evidence -> READY_FOR_PORTFOLIO_DRAFT only (never DECISION)."""
    blockers: list[str] = []
    for node, art in ctx.inputs.items():
        blockers.extend(_intake_blockers(art))
    if blockers:
        return GateResult("FAILED", "FAILED", {"blockers": blockers}, blockers)

    a11 = ctx.inputs.get("A11")
    # A8 snapshot availability comes from the run's published artifacts (the
    # async lane has no graph edge into G2)
    a8 = ctx.published.get("A8")
    confirmed = len(a8.get("payload", {}).get("confirmed_responses", [])) if a8 else 0
    if confirmed > 0:
        decision = "READY_FOR_PORTFOLIO_DECISION"
        restrictions = []
        exceptions = [{
            "item": "stakeholder evidence",
            "basis": "pilot-simulated HUMAN_CONFIRMED responses",
            "accepted_by": "sim-pilot-portfolio-reviewer",
        }]
    else:
        decision = "READY_FOR_PORTFOLIO_DRAFT"
        restrictions = [
            "stakeholder evidence pending: exploratory portfolio analysis only",
            "no final disposition, investment approval or wave commitment",
        ]
        exceptions = []

    cand = a11
    reviewer = (ctx.policy.reviewers.get("simulated", {}).get("portfolio", "sim-portfolio")
                if ctx.policy else "sim-portfolio")
    payload = {
        "decision_record": {
            "status": decision,
            "candidate_ref": cand["artifact_id"] if cand else None,
            "manifest_hash": cand["content_hash"] if cand else None,
            "policy_version": ctx.policy.version if ctx.policy else "none",
            "authorized_by": reviewer,
            "simulated": True,
            "authorized_at": _now(),
            "restrictions": restrictions,
            "accepted_exceptions": exceptions,
        }
    }
    return GateResult("PUBLISHED", "COMPLETE", payload, [])


SEED_QUESTIONS = (
    "What is the business criticality of this application?",
    "Which compliance obligations apply?",
    "Who owns the data and the roadmap?",
)


def _cvss(v: str | None) -> float:
    try:
        return float(v or 0)
    except ValueError:
        return 0.0


def _cvss_band(v: str | None) -> str:
    x = _cvss(v)
    if not v:
        return "unknown"
    return "critical" if x >= 9 else "high" if x >= 7 else "medium" if x >= 4 else "low"


def _sast_sev(v: str | None) -> str:
    return {"ERROR": "high", "WARNING": "medium", "INFO": "low"}.get((v or "").upper(), "low")


def _intake_blockers(art: dict[str, Any]) -> list[str]:
    from appmod.contracts.schemas import intake_errors
    return intake_errors(art)


P1_GATE_OVERRIDES = {
    "G1": p1_snapshot_gate,
    "G2": p1_release_gate,
    "G1:cfg": {"required_producers": ["A3", "A6", "A7", "A9"], "allow_pending": []},
    "G2:cfg": {"decision_values": ["HOLD", "READY_FOR_PORTFOLIO_DRAFT",
                                    "READY_FOR_PORTFOLIO_DECISION"]},
}
