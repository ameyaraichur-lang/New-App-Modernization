"""An answer that changes P3 scope reopens only the P4 planners that read it."""

from appmod.agents.runtime import MockAgentRunner
from appmod.kernel.audit import AuditJournal
from appmod.kernel.invalidation import affected_planners, events_from_answers, lane_failure_events
from appmod.kernel.orchestrator import PhaseOrchestrator
from appmod.kernel.policy import PolicyService
from appmod.phases.p4.engine import P4_GATE_OVERRIDES
from appmod.store.artifact_store import ArtifactStore

BASE = {
    "scope_manifest": {"workload_ids": ["app"]},
    "p3_package": {"application_id": "app", "status": "READY_FOR_PLANNING",
                   "conditions": [], "candidate_hash": "same"},
    "scope": {"components": ["web", "admin"], "wave": "W1", "disposition": "Refactor"},
}


def _reused(tmp_path, registry, events):
    phase = registry["phases"][4]
    store = ArtifactStore(tmp_path / "store")
    orch = PhaseOrchestrator(phase, store, PolicyService(), AuditJournal(tmp_path / "audit"),
                             MockAgentRunner(phase), gate_overrides=P4_GATE_OVERRIDES, reuse=True)
    first = orch.start_run("p4", "app", BASE)
    orch.run(first)
    second = orch.start_run("p4-again", "app", {**BASE, "replan_events": events})
    orch.run(second)
    return {e["node"]: bool(e.get("reused")) for e in second.outcome_log}


def test_scope_answer_reopens_only_dependent_planners(registry, tmp_path):
    answer = {"kind": "answer", "changes": ["components"], "components": ["web"]}
    reused = _reused(tmp_path, registry, [answer])
    assert reused["G0"] and reused["A1"]
    for node in ("A2", "A3", "A4", "A5", "A6", "A7", "A8", "G1", "A9", "G2"):
        assert reused[node] is False
    assert affected_planners({**BASE, "replan_events": [answer]}) == {"A2", "A3"}


def test_lane_failure_reopens_the_estimate_only(registry, tmp_path):
    event = {"kind": "execution_failure", "changes": ["estimate"], "lane": "T2-code"}
    reused = _reused(tmp_path, registry, [event])
    assert reused["A1"] and reused["A2"] and reused["A3"] and reused["A4"]
    assert reused["A5"] is False
    assert reused["A6"] and reused["A7"] and reused["A8"]
    assert reused["G1"] is False and reused["A9"] is False
    assert lane_failure_events({"A2": "COMPLETE", "A3": "FAILED"}) == [
        {"kind": "execution_failure", "changes": ["estimate"], "lane": "A3"}]


def test_critique_reopens_the_named_planner_only(registry, tmp_path):
    event = {"kind": "critique", "target": "A3", "statement": "task scope drifted"}
    reused = _reused(tmp_path, registry, [event])
    assert reused["A1"] and reused["A2"]
    assert reused["A3"] is False and reused["A4"] is False
    assert events_from_answers([
        {"status": "ANSWERED", "answer": '{"changes": ["components"], "components": ["api"]}'},
        {"status": "ANSWERED", "answer": "plain text does not replan"},
    ])[0]["components"] == ["api"]
