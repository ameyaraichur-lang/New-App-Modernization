"""Every non-critic P1–P4 role hands a model field to the consumer it names."""

from appmod.agents.lineage import CRITICS, LINEAGE, project
from appmod.agents.overlays import OVERLAYS
from appmod.agents.runtime import MockAgentRunner
from appmod.kernel.audit import AuditJournal
from appmod.kernel.orchestrator import PhaseOrchestrator
from appmod.kernel.policy import PolicyService
from appmod.registry.compiler import resolve_registry
from appmod.store.artifact_store import ArtifactStore

RUN_INPUTS = {
    "scope_manifest": {"workload_ids": ["flask-tutorial"], "route": "UI",
                       "boundaries": "pilot corpus repo"},
    "source_pins": {"commit": "626b6cc"},
}


def test_every_non_critic_declares_a_consumed_field():
    reg = resolve_registry()
    roles = [(phase, agent["local_id"])
             for phase in (1, 2, 3, 4)
             for agent in reg["phases"][phase]["agents"]
             if (phase, agent["local_id"]) not in CRITICS]
    assert len(roles) == 31
    assert set(LINEAGE) == set(roles)
    for (phase, node), (field, (cphase, cnode)) in LINEAGE.items():
        assert field in OVERLAYS[phase][node].fields
        assert cnode


def test_each_declared_field_reaches_its_consumer():
    artifacts = {(phase, node): {field: f"marker-{phase}-{node}"}
                 for (phase, node), (field, _consumer) in LINEAGE.items()}
    seen = set()
    for (phase, node), (field, (cphase, cnode)) in LINEAGE.items():
        items = project(artifacts, cphase, cnode)
        match = [item for item in items if item["producer"] == f"P{phase}.{node}"]
        assert match and match[0]["value"] == f"marker-{phase}-{node}"
        assert match[0]["consumed_by"] == f"P{cphase}.{cnode}"
        seen.add((phase, node))
    assert seen == set(LINEAGE)


def test_p1_a2_receives_a1_module_map(tmp_path):
    reg = resolve_registry()["phases"][1]

    class Stamp:
        def __init__(self):
            self.mock = MockAgentRunner(reg)
            self.seen = {}

        def run(self, spec, inputs, policy, context=None):
            out = self.mock.run(spec, inputs, policy)
            if spec["local_id"] == "A1":
                out.payload["module_map"] = [{"module": "MARKER"}]
            if spec["local_id"] == "A2":
                self.seen = inputs
            return out

    runner = Stamp()
    orch = PhaseOrchestrator(reg, ArtifactStore(tmp_path / "store"), PolicyService(),
                             AuditJournal(tmp_path / "audit"), runner)
    orch.run(orch.start_run("lineage", "flask-tutorial", RUN_INPUTS))
    assert runner.seen["A1"]["payload"]["module_map"] == [{"module": "MARKER"}]


def test_context_quotes_the_consumed_field():
    from types import SimpleNamespace
    from appmod.agents.llm_runner import LLMAgentRunner
    from appmod.agents.runtime import AgentOutcome
    from appmod.tools.gateway import ToolEnv
    text = LLMAgentRunner._context_message(
        SimpleNamespace(phase=3), {"id": "P3.A3", "name": "Data"},
        AgentOutcome("COMPLETE", {}), {}, ToolEnv("app", 3), None, False, None,
        [{"producer": "P1.A3", "field": "entities", "consumed_by": "P3.A3",
          "value": [{"name": "Order"}]}])
    assert "consumed_by P3.A3" in text
    assert "Order" in text
