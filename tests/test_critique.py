"""An injected contradiction re-runs its target and is audited when resolved."""

from appmod.agents.runtime import AgentOutcome, MockAgentRunner
from appmod.kernel.audit import AuditJournal
from appmod.kernel.critique import critique_requests
from appmod.kernel.orchestrator import PhaseOrchestrator
from appmod.kernel.policy import PolicyService
from appmod.store.artifact_store import ArtifactStore

RUN_INPUTS = {
    "scope_manifest": {"workload_ids": ["flask-tutorial"], "route": "UI",
                       "boundaries": "pilot corpus repo"},
    "source_pins": {"commit": "626b6cc"},
}
STATEMENT = "A1 licence statement disagrees with the repository"


class _Critic:
    accepts_context = True

    def __init__(self, phase, *, resolve: bool):
        self.mock = MockAgentRunner(phase)
        self.resolve = resolve
        self.a1 = 0
        self.saw_critique = False

    def fingerprint(self):
        return "critique-test"

    def run(self, spec, inputs, policy, context=None):
        out = self.mock.run(spec, inputs, policy)
        if spec["local_id"] == "A1":
            self.a1 += 1
            if (context or {}).get("critiques"):
                self.saw_critique = True
        if spec["local_id"] == "A10":
            if not self.resolve or self.a1 < 2:
                out.payload["contradictions"] = [
                    {"between": ["A1", "A6"], "statement": STATEMENT, "target": "A1"}]
            else:
                out.payload["contradictions"] = []
        return out


def _run(tmp_path, registry, runner, escalate=None):
    phase = registry["phases"][1]
    orch = PhaseOrchestrator(
        phase, ArtifactStore(tmp_path / "store"), PolicyService(),
        AuditJournal(tmp_path / "audit"), runner, escalate=escalate)
    ctx = orch.start_run("run-critique", "flask-tutorial", RUN_INPUTS)
    orch.run(ctx)
    return ctx, orch.audit.read_all()


def test_injected_contradiction_reruns_and_resolves(registry, tmp_path):
    runner = _Critic(registry["phases"][1], resolve=True)
    ctx, audit = _run(tmp_path, registry, runner)
    kinds = [e["kind"] for e in audit]
    assert "CRITIQUE_RERUN" in kinds
    assert "CRITIQUE_RESOLVED" in kinds
    assert runner.saw_critique
    assert runner.a1 == 2
    assert ctx.state.nodes["A1"].status == "PUBLISHED"
    resolved = [c for c in ctx.critiques if c["state"] == "resolved"]
    assert resolved and resolved[0]["target"] == "A1"
    assert resolved[0]["rounds"] == 1


def test_unresolved_critique_escalates_after_two_rounds(registry, tmp_path):
    runner = _Critic(registry["phases"][1], resolve=False)
    parked = []

    def escalate(source, target, statement):
        parked.append((source, target, statement))
        return True

    ctx, audit = _run(tmp_path, registry, runner, escalate=escalate)
    reruns = [e for e in audit if e["kind"] == "CRITIQUE_RERUN"]
    assert len(reruns) == 2
    assert any(e["kind"] == "CRITIQUE_ESCALATED" for e in audit)
    assert parked == [("A10", "A1", STATEMENT)]
    assert ctx.state.nodes["A1"].status == "AWAITING_INPUT"
    assert runner.a1 == 3


def test_request_shapes():
    nodes = {"A1", "A3", "A4"}
    assert critique_requests(2, "A7", {"disagreements": [
        {"issue": "route split", "target": "A6"}]}, nodes) == []
    assert critique_requests(4, "A9", {"revision_requests": [
        {"finding": "context hash differs", "owner": "P4.A3"}]}, nodes) == [
        {"source": "A9", "target": "A3", "statement": "context hash differs"}]
    assert critique_requests(3, "A8", {"consistency_issues": [
        {"issue": "schema drift", "artifacts": ["A2"], "target": "A1"}]}, nodes)[0]["target"] == "A1"


def test_context_mentions_an_open_critique():
    from types import SimpleNamespace
    from appmod.agents.llm_runner import LLMAgentRunner
    from appmod.tools.gateway import ToolEnv
    text = LLMAgentRunner._context_message(
        SimpleNamespace(phase=1), {"id": "P1.A1", "name": "Inventory"},
        AgentOutcome("COMPLETE", {}), {}, ToolEnv("app", 1), None, False,
        [{"rounds": 1, "statement": STATEMENT}])
    assert "Critique to resolve" in text
    assert STATEMENT in text
