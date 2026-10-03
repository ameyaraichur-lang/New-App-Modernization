"""M2 portfolio run (T4.5): P1 discovery over the whole corpus, then P2
portfolio analysis over the assembled handoff packages.

Decision-mode apps (simulated HUMAN_CONFIRMED stakeholder evidence accepted at
P1 G2) can be AUTHORIZED at P2 G2; the rest stay DRAFT_ONLY; Retain/Retire
proposals land in the IA02 non-delivery register.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from appmod.kernel.audit import AuditJournal
from appmod.kernel.orchestrator import PhaseOrchestrator
from appmod.kernel.policy import PolicyService
from appmod.registry.compiler import resolve_registry
from appmod.phases.p1.engine import P1AgentRunner, P1_GATE_OVERRIDES
from appmod.phases.p2.engine import P2AgentRunner, P2_GATE_OVERRIDES, PortfolioApp
from appmod.store.artifact_store import ArtifactStore

# Corpus of legacy repos to discover; set APPMOD_CORPUS to a directory of
# checkouts named like the FAMILY keys below (not shipped with the codebase).
CORPUS = Path(os.environ.get("APPMOD_CORPUS", "corpus"))
DECISION_MODE = {"spring-petclinic", "flask-tutorial"}

FAMILY = {
    "django-realworld": "realworld", "express-realworld": "realworld",
    "todomvc": "js-demo", "react-redux-realworld": "js-demo",
    "sinatra14": "library", "golang-example": "library",
    "flask-tutorial": "library", "spring-petclinic": "solo",
    "laravel58": "solo", "musicstore": "solo",
}

registry = resolve_registry()
policy = PolicyService()
work = Path(__file__).resolve().parents[1] / "runs" / "portfolio"
work.mkdir(parents=True, exist_ok=True)
store = ArtifactStore(work / "store")
audit = AuditJournal(work / "audit")

def _lang_count(a1):
    import re as _re
    for f in a1["findings"]:
        m = _re.search(r"across (\d+) languages", f["statement"])
        if m:
            return int(m.group(1))
    return 1


def _primary_lang(a1):
    findings = a1["findings"]
    for f in findings:
        if "primary:" in f["statement"]:
            return f["statement"].split("primary:")[-1].strip()
    return "unknown"

apps_meta = []
for repo_dir in sorted(CORPUS.iterdir()):
    if not repo_dir.is_dir():
        continue
    app_id = repo_dir.name
    runner = P1AgentRunner(confirmed_stakeholder=app_id in DECISION_MODE)
    runner.bind_repo(repo_dir)
    orch = PhaseOrchestrator(registry["phases"][1], store, policy, audit, runner,
                             gate_overrides=P1_GATE_OVERRIDES)
    ctx = orch.start_run(f"portfolio-p1-{app_id}", app_id, {
        "scope_manifest": {"workload_ids": [app_id], "route": "derived-at-A5",
                           "boundaries": "pilot corpus repo, read-only"},
        "source_pins": {"repo_path": str(repo_dir)},
    })
    orch.run(ctx)
    g2 = store.get(f"P1/{app_id}/G2")
    a1 = store.get(f"P1/{app_id}/A1")
    a5 = store.get(f"P1/{app_id}/A5")
    g1 = store.get(f"P1/{app_id}/G1")
    status = "OK" if ctx.finished else "INCOMPLETE"
    print(f"P1 {app_id:<24} {status:<12} G2={g2['payload']['decision_record']['status']}")
    apps_meta.append((app_id, g2, a1, a5, g1))

# ---- assemble portfolio packages ---------------------------------------------
portfolio_apps = []
p1_packages = []
p1_scope = {}
for app_id, g2, a1, a5, g1 in apps_meta:
    repo = {
        "loc": a1["payload"]["repositories"][0].get("loc", 0),
        "files": a1["payload"]["repositories"][0].get("files", 0),
    }
    portfolio_apps.append(PortfolioApp(
        app_id=app_id,
        p1_g2_status=g2["payload"]["decision_record"]["status"],
        loc=repo["loc"],
        languages=_lang_count(a1),
        dependencies=len(a1["payload"]["dependencies"]),
        tests=1 if any("No test files" not in f["statement"] for f in a1["findings"]) else 0,
        route=a5["payload"]["capability_route"],
        license="from-P1",
        has_data_layer=True,   # refined below
        primary_language=_primary_lang(a1),
        source_family=FAMILY.get(app_id, "solo"),
        non_delivery_proposal={"todomvc": "Retire", "react-redux-realworld": "Retain"}.get(app_id, ""),
        p1_manifest_hash=g1["payload"]["evidence_manifest"]["manifest_hash"],
    ))
    p1_packages.append({
        "application_id": app_id,
        "schema_version": "P1.discovery.v3.0",
        "g2_status": g2["payload"]["decision_record"]["status"],
        "manifest_hash": g1["payload"]["evidence_manifest"]["manifest_hash"],
    })
    p1_scope[app_id] = g2["payload"]["decision_record"]["status"]

# data-layer refinement from P1 A3 artifacts
for pa in portfolio_apps:
    try:
        a3 = store.get(f"P1/{pa.app_id}/A3")
        has_data = bool(a3["payload"]["datasets"])
        pa.has_data_layer = has_data
    except Exception:
        pass

# ---- P2 ------------------------------------------------------------------------
runner2 = P2AgentRunner(portfolio_apps)
orch2 = PhaseOrchestrator(registry["phases"][2], store, policy, audit, runner2,
                          gate_overrides=P2_GATE_OVERRIDES)
ctx2 = orch2.start_run("portfolio-p2-1", "PORTFOLIO-10", {
    "scope_manifest": {"portfolio_id": "PORTFOLIO-10", "apps": [a.app_id for a in portfolio_apps]},
    "p1_packages": p1_packages,
    "p1_scope": p1_scope,
})
orch2.run(ctx2)
print(f"\nP2 finished={ctx2.finished}")
for e in ctx2.outcome_log:
    print(f"  {e['node']:>4}  {e['status']}")

g2p2 = store.get("P2/PORTFOLIO-10/G2")
dec = g2p2["payload"]["decision_record"]
print("\nP2 G2:", dec["status"])
print("  AUTHORIZED :", dec["authorized_apps"])
print("  DRAFT_ONLY :", dec["draft_only_apps"])
print("  IA02 reg   :", [(e["application_id"], e["route"]) for e in dec["non_delivery_register"]["entries"]])

a7 = store.get("P2/PORTFOLIO-10/A7")
print("\nRoute register (proposed):")
for e in a7["payload"]["route_register"]:
    print(f"  {e['application_id']:<24} {e['route']:<14} wave={e.get('wave_id','-') if 'wave_id' in e else '-'}")
a6 = store.get("P2/PORTFOLIO-10/A6")
print("\nWaves:", a6["payload"]["waves"])
print("Unscheduled:", a6["payload"]["unscheduled"])

