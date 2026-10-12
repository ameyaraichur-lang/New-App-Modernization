"""T1 store tests: immutability, versioning, lineage."""

import pytest

from appmod.store.artifact_store import ArtifactStoreError


def base_artifact(n=1, parents=None):
    return {
        "schema_version": "P1.discovery.v3.0",
        "artifact_id": f"P1/app/A{n}",
        "artifact_version": 1,
        "run_id": "run-1",
        "application_id": "app",
        "phase_id": 1,
        "producer_id": f"P1.A{n}",
        "input_manifest_ref": "{}",
        "input_hash": "a" * 64,
        "policy_version": "p",
        "status": "COMPLETE",
        "scope": {}, "applicability": {},
        "evidence_refs": [], "findings": [], "gaps": [], "contradictions": [],
        "payload": {},
        "created_at": "2026-10-03T00:00:00Z",
        "execution_metadata": {"parent_refs": parents or []},
        "access_classification": "INTERNAL",
        "content_hash": None,
    }


def publish(store, art):
    from appmod.contracts.schemas import content_hash
    art["content_hash"] = content_hash(art)
    return store.publish(art)


def test_publish_and_get(tmp_store):
    art = base_artifact()
    publish(tmp_store, art)
    got = tmp_store.get("P1/app/A1")
    assert got["artifact_id"] == "P1/app/A1"
    assert got["content_hash"] == art["content_hash"]


def test_immutable_identity(tmp_store):
    publish(tmp_store, base_artifact())
    changed = base_artifact()
    changed["payload"] = {"different": True}
    with pytest.raises(ArtifactStoreError, match="immutable"):
        publish(tmp_store, changed)


def test_idempotent_republish(tmp_store):
    p1 = publish(tmp_store, base_artifact())
    p2 = publish(tmp_store, base_artifact())
    assert p1["content_hash"] == p2["content_hash"]


def test_versioning(tmp_store):
    art = base_artifact()
    publish(tmp_store, art)
    v2 = base_artifact()
    v2["artifact_version"] = 2
    v2["status"] = "PARTIAL"
    publish(tmp_store, v2)
    assert tmp_store.versions("P1/app/A1") == [1, 2]
    latest = tmp_store.get("P1/app/A1")
    assert latest["artifact_version"] == 2


def test_lineage_descendants(tmp_store):
    a1 = base_artifact(1)
    publish(tmp_store, a1)
    a2 = base_artifact(2, parents=["P1/app/A1@1"])
    publish(tmp_store, a2)
    a3 = base_artifact(3, parents=["P1/app/A2@1"])
    publish(tmp_store, a3)

    kids = tmp_store.children_of("P1/app/A1", 1)
    assert [k["artifact_id"] for k in kids] == ["P1/app/A2"]

    desc = tmp_store.descendants_of("P1/app/A1", 1)
    assert {d["artifact_id"] for d in desc} == {"P1/app/A2", "P1/app/A3"}


def test_query_filters(tmp_store):
    publish(tmp_store, base_artifact(1))
    a2 = base_artifact(2)
    a2["application_id"] = "other-app"
    publish(tmp_store, a2)
    assert len(list(tmp_store.query(application_id="app"))) == 1
    assert len(list(tmp_store.query(phase_id=1))) == 2
