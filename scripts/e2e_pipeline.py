"""E2E pipeline driver: Phase 1 -> 6 on one corpus app (spring-petclinic).

Demonstrates the full relation chain with real evidence at every handoff:
P1 discovery (decision mode) -> P2 authorize (8R route) -> P3 target arch ->
P4 planning -> P5 code lane manifests + G2/G3 integration seals -> P6 batch
migration with a REAL local X1 row-copy and checkpoint reconciliation.
"""
import os
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from appmod.kernel.audit import AuditJournal
from appmod.kernel.orchestrator import PhaseOrchestrator
from appmod.kernel.policy import PolicyService
from appmod.registry.compiler import compile_all
from appmod.phases.p1.engine import P1AgentRunner, P1_GATE_OVERRIDES
from appmod.phases.p2.engine import P2AgentRunner, P2_GATE_OVERRIDES, PortfolioApp
from appmod.phases.p3.engine import P3AgentRunner, P3_GATE_OVERRIDES
from appmod.phases.p4.engine import P4AgentRunner, P4_GATE_OVERRIDES
from appmod.phases.p5.engine import P5AgentRunner, P5_GATE_OVERRIDES
from appmod.phases.p6.engine import P6AgentRunner, P6_GATE_OVERRIDES
from appmod.registry.compiler import resolve_registry
from appmod.store.artifact_store import ArtifactStore

APP = os.environ.get("APPMOD_E2E_APP", "spring-petclinic")
# Legacy repo under test (a checkout of the chosen APP); set APPMOD_CORPUS to
# the parent directory of app checkouts (not shipped with the codebase).
CORPUS = Path(os.environ.get("APPMOD_CORPUS", "corpus"))
REPO = CORPUS / APP
SEED_SQL = REPO / "src/main/resources/db/h2/data.sql"

registry = resolve_registry()
policy = PolicyService()
work = Path(__file__).resolve().parents[1] / "runs" / f"e2e-{APP}"
work.mkdir(parents=True, exist_ok=True)
store = ArtifactStore(work / "store")
audit = AuditJournal(work / "audit")


def run_phase(phase, runner, app_id, run_inputs, overrides):
    orch = PhaseOrchestrator(registry["phases"][phase], store, policy, audit, runner,
                             gate_overrides=overrides)
    ctx = orch.start_run(f"e2e-p{phase}-{app_id}", app_id, run_inputs)
    orch.run(ctx)
    bad = [e for e in ctx.outcome_log if e["status"] == "FAILED"]
    return ctx, bad


# ---------------- P1 ------------------------------------------------------------
r1 = P1AgentRunner(confirmed_stakeholder=True)
r1.bind_repo(REPO)
ctx1, bad1 = run_phase(1, r1, APP, {
    "scope_manifest": {"workload_ids": [APP], "route": "derived-at-A5",
                       "boundaries": "pilot corpus repo, read-only"},
    "source_pins": {"repo_path": str(REPO)},
}, P1_GATE_OVERRIDES)
p1_g2 = store.get(f"P1/{APP}/G2")["payload"]["decision_record"]
p1_a1 = store.get(f"P1/{APP}/A1")
p1_a3 = store.get(f"P1/{APP}/A3")
p1_a5 = store.get(f"P1/{APP}/A5")
print(f"P1  OK={ctx1.finished and not bad1}  G2={p1_g2['status']}")
assert p1_g2["status"] == "READY_FOR_PORTFOLIO_DECISION", p1_g2

# ---------------- P2 (single-app portfolio) ---------------------------------------
apps = [PortfolioApp(
    app_id=APP, p1_g2_status=p1_g2["status"],
    loc=p1_a1["payload"]["repositories"][0]["loc"],
    languages=4, dependencies=len(p1_a1["payload"]["dependencies"]),
    tests=1, route=p1_a5["payload"]["capability_route"],
    has_data_layer=bool(p1_a3["payload"]["datasets"]),
    primary_language="java", source_family="solo",
    p1_manifest_hash=store.get(f"P1/{APP}/G1")["payload"]["evidence_manifest"]["manifest_hash"],
)]
ctx2, bad2 = run_phase(2, P2AgentRunner(apps), "PF1", {
    "scope_manifest": {"portfolio_id": "PF1"},
    "p1_packages": [{"application_id": APP, "schema_version": "P1.discovery.v3.0",
                     "g2_status": p1_g2["status"], "manifest_hash": apps[0].p1_manifest_hash}],
    "p1_scope": {APP: p1_g2["status"]},
}, P2_GATE_OVERRIDES)
p2_g2 = store.get("P2/PF1/G2")["payload"]["decision_record"]
disposition = next(e["route"] for e in
                   store.get("P2/PF1/A7")["payload"]["route_register"]
                   if e["application_id"] == APP)
print(f"P2  OK={ctx2.finished and not bad2}  G2={p2_g2['status']}  route={disposition}")
assert APP in p2_g2["authorized_apps"], p2_g2

# ---------------- P3 ---------------------------------------------------------------
routes = [r["endpoint"] for r in p1_a3["payload"]["integrations"]][:12]
datasets = [d["name"] for d in p1_a3["payload"]["datasets"]][:8]
components = [c["name"] for c in p1_a1["payload"]["components"][:5]]
ctx3, bad3 = run_phase(3, P3AgentRunner({
    "app_id": APP, "disposition": disposition, "primary_language": "java",
    "route": apps[0].route, "components": components, "routes": routes,
    "datasets": datasets,
}), APP, {
    "scope_manifest": {"workload_ids": [APP]},
    "p2_package": {"application_id": APP, "authorized": True,
                   "disposition": disposition,
                   "candidate_hash": p2_g2["candidate_hash"]},
}, P3_GATE_OVERRIDES)
p3_g2 = store.get(f"P3/{APP}/G2")["payload"]["decision_record"]
print(f"P3  OK={ctx3.finished and not bad3}  G2={p3_g2['status']}")
assert p3_g2["status"] in ("READY_FOR_PLANNING", "CONDITIONAL_PLANNING")

# ---------------- P4 -----------------------------------------------------------------
ctx4, bad4 = run_phase(4, P4AgentRunner({
    "app_id": APP, "disposition": disposition, "wave": "W1",
}), APP, {
    "scope_manifest": {"workload_ids": [APP]},
    "p3_package": {"application_id": APP, "status": p3_g2["status"],
                   "conditions": p3_g2.get("conditions", [])},
}, P4_GATE_OVERRIDES)
p4_g2 = store.get(f"P4/{APP}/G2")["payload"]["decision_record"]
print(f"P4  OK={ctx4.finished and not bad4}  G2={p4_g2['status']}")

# ---------------- P5 -------------------------------------------------------------------
ctx5, bad5 = run_phase(5, P5AgentRunner({
    "app_id": APP, "disposition": disposition, "repo_path": str(REPO),
    "routes": routes, "datasets": datasets,
    "dependencies": p1_a1["payload"]["dependencies"],
    "tests": ["inventory"], "route": apps[0].route,
}), APP, {
    "scope_manifest": {"workload_ids": [APP]},
    "p4_package": {"application_id": APP, "status": p4_g2["status"]},
    "execution_permit": {"granted": True, "scope": "repo+manifest+test sandbox",
                         "issuer": "pilot operator (simulated)"},
}, P5_GATE_OVERRIDES)
p5_g4 = store.get(f"P5/{APP}/G4")["payload"]["decision_record"]
p5_g3 = store.get(f"P5/{APP}/G3")["payload"]["final_manifest"]
print(f"P5  OK={ctx5.finished and not bad5}  G4={p5_g4['status']}  build={p5_g3['build_digest'][:12]}")

# ---------------- P6 data fixture + batch migration -------------------------------------
def build_fixture():
    src_db = work / "petclinic_source.sqlite"
    dst_db = work / "petclinic_target.sqlite"
    for p in (src_db, dst_db):
        if p.exists():
            p.unlink()
    text = SEED_SQL.read_text(encoding="utf-8", errors="ignore")
    inserts = re.findall(r"INSERT INTO (\w+) VALUES \(([^;]*)\);", text)
    tables: dict[str, int] = {}
    rows: dict[str, list[list]] = {}
    for table, values in inserts:
        vals = []
        for raw in re.findall(r"'(?:[^']|'')*'|[^,]+", values):
            raw = raw.strip()
            if raw == "default":
                vals.append(None)
            elif raw.startswith("'"):
                vals.append(raw.replace("''", "'")[1:-1])
            else:
                vals.append(raw)
        tables[table] = max(tables.get(table, 0), len(vals))
        rows.setdefault(table, []).append(vals)
    con = sqlite3.connect(str(src_db))
    cols = {}
    for t, n in tables.items():
        has_id = any(v[0] is None for v in rows.get(t, []))
        decl = ", ".join((["id INTEGER PRIMARY KEY AUTOINCREMENT"] if has_id else [])
                         + [f"c{i} TEXT" for i in range(1 if has_id else 0, n)])
        con.execute(f'CREATE TABLE "{t}" ({decl})')
        cols[t] = n
    for t, rlist in rows.items():
        n = tables[t]
        ph = ", ".join("?" for _ in range(n))
        con.executemany(f'INSERT INTO "{t}" VALUES ({ph})', rlist)
    con.commit()
    con.close()
    dcon = sqlite3.connect(str(dst_db))
    for t, n in tables.items():
        has_id = any(v[0] is None for v in rows.get(t, []))
        decl = ", ".join((["id INTEGER PRIMARY KEY AUTOINCREMENT"] if has_id else [])
                         + [f"c{i} TEXT" for i in range(1 if has_id else 0, n)])
        dcon.execute(f'CREATE TABLE "{t}" ({decl})')
    dcon.commit()
    dcon.close()
    table_defs = [{"name": t, "columns": n} for t, n in sorted(tables.items())]
    total = sum(len(r) for r in rows.values())
    return str(src_db), str(dst_db), table_defs, total


src_db, dst_db, table_defs, total_rows = build_fixture()
print(f"\nP6 fixture: {len(table_defs)} tables, {total_rows} seed rows from {SEED_SQL.name}")

ctx6, bad6 = run_phase(6, P6AgentRunner({
    "app_id": APP, "route": "batch",
    "source_db": src_db, "target_db": dst_db,
    "tables": table_defs, "p5_build_digest": p5_g3["build_digest"],
}), APP, {
    "scope_manifest": {"workload_ids": [APP]},
    "p5_package": {"application_id": APP, "status": p5_g4["status"]},
    "data_brief": {"app_id": APP, "route": "batch", "source_db": src_db,
                   "target_db": dst_db, "tables": table_defs},
    "migration_permit": {"granted": True, "issuer": "pilot operator (simulated)"},
}, P6_GATE_OVERRIDES)
print(f"P6  OK={ctx6.finished and not bad6}")
for e in ctx6.outcome_log:
    print(f"    {e['node']:>4}  {e['status']}")

p6_g2 = store.get(f"P6/{APP}/G2")["payload"]["checkpoint_manifest"]
p6_a9 = store.get(f"P6/{APP}/A9")["payload"]
p6_g3 = store.get(f"P6/{APP}/G3")["payload"]["decision_record"]
print("\nP6 checkpoint:", p6_g2["checkpoint_id"], "| jobs:", len(p6_g2["jobs"]))
print("P6 reconciliation:", [(r["table"], r["status"]) for r in p6_a9["results"]])
print("P6 G3:", p6_g3["status"])
print("\n=== E2E gate chain ===")
for phase, gate, art in ((1, "G2", f"P1/{APP}/G2"), (2, "G2", "P2/PF1/G2"),
                         (3, "G2", f"P3/{APP}/G2"), (4, "G2", f"P4/{APP}/G2"),
                         (5, "G4", f"P5/{APP}/G4"), (6, "G3", f"P6/{APP}/G3")):
    dec = store.get(art)["payload"]["decision_record"]["status"]
    print(f"  P{phase} {gate}: {dec}")
