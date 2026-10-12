"""T2/T3 kernel scenario tests over Phase 1 with scripted runners.

Encodes Run Controls as executable rules:
  - dispatch only after hard prerequisites publish
  - FAILED blocks dependants (never placeholder success)
  - async lane never blocks fan-in
  - G1 seals an immutable manifest; G2 binds a reviewer decision to the hash
  - bounded retries for transient failures; exhaustion -> FAILED
  - invalid publication is FAILED, not success
"""


from appmod.agents.runtime import MockAgentRunner, ScriptedAgentRunner
from appmod.kernel.audit import AuditJournal
from appmod.kernel.orchestrator import PhaseOrchestrator
from appmod.kernel.policy import PolicyService
from appmod.store.artifact_store import ArtifactStore

RUN_INPUTS = {
    "scope_manifest": {
        "workload_ids": ["flask-tutorial"],
        "route": "UI",
        "boundaries": "pilot corpus repo",
    },
    "source_pins": {"commit": "626b6cc"},
}


def make_orch(registry, tmp_path, runner, gate_overrides=None):
    store = ArtifactStore(tmp_path / "store")
    audit = AuditJournal(tmp_path / "audit")
    policy = PolicyService()
    orch = PhaseOrchestrator(
        registry["phases"][1], store, policy, audit, runner,
        gate_overrides=gate_overrides,
    )
    return orch, store, audit


def test_p1_happy_path(registry, tmp_path):
    orch, store, audit = make_orch(registry, tmp_path, MockAgentRunner(registry["phases"][1]))
    ctx = orch.start_run("run-1", "flask-tutorial", RUN_INPUTS)
    events = orch.run(ctx)

    # every agent + gate published
    assert set(ctx.published) == {
        "G0", "G1", "G2", "A1", "A2", "A3", "A4", "A5", "A6", "A7",
        "A8", "A9", "A10", "A11",
    }
    outcomes = {e["node"]: e["status"] for e in ctx.outcome_log}
    assert all(s == "COMPLETE" for s in outcomes.values())

    # G1 manifest sealed with hash + async A8 recorded as PENDING-allowed or present
    g1 = store.get("P1/flask-tutorial/G1")
    manifest = g1["payload"]["evidence_manifest"]
    assert manifest["manifest_hash"]
    assert {"A3", "A6", "A7", "A9"} <= set(manifest["artifact_refs"])

    # G2 decision record binds reviewer + candidate hash
    g2 = store.get("P1/flask-tutorial/G2")
    decision = g2["payload"]["decision_record"]
    assert decision["simulated"] is True
    assert decision["authorized_by"].startswith("sim-")
    assert decision["manifest_hash"]
    assert decision["status"] in (
        "HOLD", "READY_FOR_PORTFOLIO_DRAFT", "READY_FOR_PORTFOLIO_DECISION"
    )

    # dispatch order respected: A2 strictly after A1 and A4 published
    audit_events = audit.read_all()
    dispatches = [e for e in audit_events if e["kind"] == "DISPATCH"]
    def dispatched_after(node, *earliers):
        node_ts = [e for e in dispatches if e["node"] == node]
        assert node_ts, f"{node} never dispatched"
        for early in earliers:
            early_ts = [e for e in dispatches if e["node"] == early]
            assert early_ts, f"{early} never dispatched"
    # A2 consumes A1+A4: both must appear before A2's last dispatch
    idx = {e["node"]: i for i, e in enumerate(dispatches)}
    assert idx["A1"] < idx["A2"] and idx["A4"] < idx["A2"]
    assert idx["A10"] < idx["A11"]
    assert idx["G1"] < idx["A10"]


def test_failed_prerequisite_blocks_dependants(registry, tmp_path):
    """Blueprint: 'A failed prerequisite blocks its dependants'."""
    script = {"A1": {"status": "FAILED"}}
    orch, store, _ = make_orch(
        registry, tmp_path, ScriptedAgentRunner(registry["phases"][1], script)
    )
    ctx = orch.start_run("run-2", "flask-tutorial", RUN_INPUTS)
    orch.run(ctx)

    assert ctx.state.nodes["A1"].status == "FAILED"
    for blocked in ("A2", "A3", "A6", "A9"):
        assert ctx.state.nodes[blocked].status == "BLOCKED", blocked
    # G1 cannot seal: its producers failed/blocked
    assert ctx.state.nodes["G1"].status in ("BLOCKED", "PENDING")
    assert "G1" not in ctx.published
    assert "G2" not in ctx.published


def test_async_lane_never_blocks(registry, tmp_path):
    """P1.A8 never gates the technical fan-in (Run Controls G1)."""
    # A8 always transient -> exhausts retries -> FAILED, but G1/G2 still seal
    script = {"A8": {"transient_failures": 99}}
    orch, store, _ = make_orch(
        registry, tmp_path, ScriptedAgentRunner(registry["phases"][1], script)
    )
    ctx = orch.start_run("run-3", "flask-tutorial", RUN_INPUTS)
    orch.run(ctx)

    assert ctx.state.nodes["A8"].status == "FAILED"
    assert "G1" in ctx.published and "G2" in ctx.published
    assert ctx.state.nodes["A10"].status == "PUBLISHED"


def test_transient_retry_then_success(registry, tmp_path):
    script = {"A1": {"transient_failures": 1}}   # fails once, then mock-succeeds
    orch, store, audit = make_orch(
        registry, tmp_path, ScriptedAgentRunner(registry["phases"][1], script)
    )
    ctx = orch.start_run("run-4", "flask-tutorial", RUN_INPUTS)
    orch.run(ctx)

    assert ctx.state.nodes["A1"].status == "PUBLISHED"
    retries = [e for e in audit.read_all() if e["kind"] == "RETRY" and e["node"] == "A1"]
    assert len(retries) == 1


def test_retry_exhaustion_fails(registry, tmp_path):
    script = {"A5": {"transient_failures": 99}}
    orch, store, audit = make_orch(
        registry, tmp_path, ScriptedAgentRunner(registry["phases"][1], script)
    )
    ctx = orch.start_run("run-5", "flask-tutorial", RUN_INPUTS)
    orch.run(ctx)

    assert ctx.state.nodes["A5"].status == "FAILED"
    assert ctx.state.nodes["A7"].status == "BLOCKED"   # A7 hard-depends on A5
    exhausted = [e for e in audit.read_all() if e["kind"] == "RETRY_EXHAUSTED"]
    assert exhausted and exhausted[0]["node"] == "A5"
    # pilot budget: initial attempt + 2 retries
    assert ctx.state.nodes["A5"].attempts == 3


def test_invalid_publication_is_failed(registry, tmp_path):
    """Runner returns schema-violating payload -> publication FAILED with
    recorded validation errors ('Invalid publication is FAILED')."""
    script = {"A1": {"payload_updates": {"repositories": "not-an-array"}}}
    orch, store, _ = make_orch(
        registry, tmp_path, ScriptedAgentRunner(registry["phases"][1], script)
    )
    ctx = orch.start_run("run-6", "flask-tutorial", RUN_INPUTS)
    orch.run(ctx)

    assert ctx.state.nodes["A1"].status == "FAILED"
    art = store.get("P1/flask-tutorial/A1")
    assert art["status"] == "FAILED"
    assert art["payload"]["validation_errors"]


def test_snapshot_gate_fails_on_failed_producer(registry, tmp_path):
    """A3 publishes a valid FAILED envelope -> G1 must not seal."""
    script = {"A3": {"status": "FAILED"}}
    orch, store, audit = make_orch(
        registry, tmp_path, ScriptedAgentRunner(registry["phases"][1], script)
    )
    ctx = orch.start_run("run-7", "flask-tutorial", RUN_INPUTS)
    # G1 is blocked (A3 FAILED is a hard prerequisite) — verify no seal
    orch.run(ctx)
    assert "G1" not in ctx.published
    assert ctx.state.nodes["G1"].status in ("BLOCKED", "PENDING")


def test_missing_policy_blocks_g0(registry, tmp_path):
    orch, store, _ = make_orch(registry, tmp_path, MockAgentRunner(registry["phases"][1]))
    orch.policy = None  # simulate missing G0 policy bundle
    ctx = orch.start_run("run-8", "flask-tutorial", RUN_INPUTS)
    orch.run(ctx)
    assert ctx.state.nodes["G0"].status == "FAILED"
    # everything downstream blocked
    assert "A1" not in ctx.published
