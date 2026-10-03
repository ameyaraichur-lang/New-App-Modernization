"""M1 smoke test: run Phase 1 Discovery end-to-end on a corpus repo with the
real tool-backed P1 engine. Prints the G2 decision + key evidence."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from appmod.kernel.audit import AuditJournal
from appmod.kernel.orchestrator import PhaseOrchestrator
from appmod.kernel.policy import PolicyService
from appmod.registry.compiler import resolve_registry
from appmod.phases.p1.engine import P1AgentRunner, P1_GATE_OVERRIDES
from appmod.store.artifact_store import ArtifactStore

if len(sys.argv) < 2:
    sys.exit("usage: python scripts/p1_smoke.py <repo-path>")
REPO = Path(sys.argv[1])

registry = resolve_registry()
work = Path(__file__).resolve().parents[1] / "runs" / "p1-smoke"
work.mkdir(parents=True, exist_ok=True)
store = ArtifactStore(work / "store")
audit = AuditJournal(work / "audit")
policy = PolicyService()
runner = P1AgentRunner()
runner.bind_repo(REPO)

orch = PhaseOrchestrator(registry["phases"][1], store, policy, audit, runner,
                         gate_overrides=P1_GATE_OVERRIDES)
ctx = orch.start_run("p1-smoke-1", REPO.name, {
    "scope_manifest": {"workload_ids": [REPO.name], "route": "derived-at-A5",
                       "boundaries": "pilot corpus repo, read-only"},
    "source_pins": {"repo_path": str(REPO)},
})
events = orch.run(ctx)

print(f"finished={ctx.finished}")
for e in ctx.outcome_log:
    print(f"  {e['node']:>4}  {e['status']}")

g2 = store.get(f"P1/{REPO.name}/G2")
decision = g2["payload"]["decision_record"]
print("\nG2 decision:", decision["status"])
print("  restrictions:", decision["restrictions"])
print("  reviewer:", decision["authorized_by"], "(simulated)" if decision["simulated"] else "")
a1 = store.get(f"P1/{REPO.name}/A1")
print("\nA1 evidence:")
print("  files/LOC:", a1["payload"]["repositories"][0])
print("  dependencies:", len(a1["payload"]["dependencies"]))
print("  findings:", [f["statement"][:90] for f in a1["findings"]])
a5 = store.get(f"P1/{REPO.name}/A5")
print("\nA5 route:", a5["payload"]["capability_route"], "status:", a5["status"])
g1 = store.get(f"P1/{REPO.name}/G1")
print("\nG1 seal:", g1["payload"]["evidence_manifest"]["manifest_hash"][:16],
      "| A8:", g1["payload"]["evidence_manifest"]["artifact_refs"]["A8"])
