"""T2 invalidation engine tests (AH06/H17)."""

from appmod.kernel.invalidation import InvalidationEngine

from test_store import base_artifact, publish


def test_supersede_marks_descendants_stale(tmp_store):
    # A1 v1 -> A2 consumes it -> A10 consumes A2
    publish(tmp_store, base_artifact(1))
    publish(tmp_store, base_artifact(2, parents=["P1/app/A1@1"]))
    publish(tmp_store, base_artifact(10, parents=["P1/app/A2@1"]))

    engine = InvalidationEngine(tmp_store)
    # no new version yet -> nothing stale
    rec = engine.supersede("P1/app/A1")
    assert rec.stale == []

    # late evidence: A1 v2 arrives
    v2 = base_artifact(1)
    v2["artifact_version"] = 2
    v2["payload"] = {"late": "evidence"}
    publish(tmp_store, v2)

    rec = engine.supersede("P1/app/A1")
    stale_ids = {d["artifact_id"] for d in rec.stale}
    assert stale_ids == {"P1/app/A2", "P1/app/A10"}   # H17: downstream stale
    assert rec.origin == ("P1/app/A1", 1) and rec.new_version == 2


def test_stale_filtering_by_run(tmp_store):
    publish(tmp_store, base_artifact(1))
    a2 = base_artifact(2, parents=["P1/app/A1@1"])
    publish(tmp_store, a2)
    v2 = base_artifact(1)
    v2["artifact_version"] = 2
    publish(tmp_store, v2)

    engine = InvalidationEngine(tmp_store)
    rec = engine.supersede("P1/app/A1")
    assert engine.stale_for_run("run-1", rec) == ["P1/app/A2"]
    assert engine.stale_for_run("other-run", rec) == []
