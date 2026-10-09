"""Live trial: run P1 on one repo with the Astra agent loop and print per-agent results.

    python scripts/llm_phase_trial.py ../corpus/microblog [A1,A3]
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from appmod.agents.llm_runner import LLMAgentRunner  # noqa: E402
from appmod.kernel.audit import AuditJournal  # noqa: E402
from appmod.kernel.orchestrator import PhaseOrchestrator  # noqa: E402
from appmod.kernel.policy import PolicyService  # noqa: E402
from appmod.phases.p1.engine import P1_GATE_OVERRIDES, P1AgentRunner  # noqa: E402
from appmod.registry.compiler import resolve_registry  # noqa: E402
from appmod.store.artifact_store import ArtifactStore  # noqa: E402
from appmod.tools.gateway import ToolEnv  # noqa: E402


def main() -> None:
    repo = Path(sys.argv[1]).resolve()
    app = repo.name
    work = Path("runs/trial") / f"{app}-{int(time.time())}"
    reg = resolve_registry()["phases"][1]
    store, audit = ArtifactStore(work / "store"), AuditJournal(work / "audit")
    base = P1AgentRunner(confirmed_stakeholder=True)
    base.bind_repo(repo)

    def env_factory(c):
        return ToolEnv(application_id=app, phase=1, repo_root=repo, store=store,
                       published=c.get("published", {}))

    runner = LLMAgentRunner(base, reg, env_factory=env_factory)
    orch = PhaseOrchestrator(reg, store, PolicyService(), audit, runner, gate_overrides=P1_GATE_OVERRIDES)
    orch.event_listener = lambda e: print(f"   . {e['node']} {e['kind']} "
                                          f"{e.get('tool') or e.get('deployment') or ''} "
                                          f"{e.get('status', '')}", flush=True) \
        if e["kind"] in ("TOOL_CALL", "SUBMISSION_REJECTED") else None
    ctx = orch.start_run(f"trial-{app}", app, {"scope_manifest": {"workload_ids": [app]},
                                                "source_pins": {"repo_path": str(repo)}})
    t0 = time.time()
    orch.run(ctx, on_event=lambda c, ev: print(f"{ev['node']:>4} -> {ev['status']}", flush=True))
    print(f"\n== {app}: {time.time() - t0:.0f}s")
    for node in sorted(ctx.inputs_by_node, key=lambda n: (n[0], int(n[1:]))):
        art = ctx.inputs_by_node[node]
        llm = art["execution_metadata"].get("llm", {})
        print(f"{node:>4} {art['status']:<17} enriched={llm.get('enriched')!s:<5} turns={llm.get('turns')} "
              f"tools={llm.get('tool_calls')} tok={llm.get('input_tokens', 0) + llm.get('output_tokens', 0)} "
              f"{llm.get('error', '')[:120]}")
    print("store:", work)
    if len(sys.argv) > 2:
        for n in sys.argv[2].split(","):
            print(json.dumps(ctx.inputs_by_node[n]["payload"], indent=1)[:4000])


if __name__ == "__main__":
    main()
