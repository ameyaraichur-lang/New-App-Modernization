import json
import sqlite3
import subprocess
from pathlib import Path

import pytest

from appmod.evals.confidence import score
from appmod.evals.run import components
from appmod.evals.stability import compare, merge, pipeline_version, snapshot
from appmod.store.artifact_store import ArtifactStore


def _app(route="UI", disposition="Rehost", boundaries=("orders", "users"), risk=None):
    return {"route": route, "disposition": disposition, "boundaries": sorted(boundaries),
            "risk": risk if risk is not None else {"technical": 3, "security": 2}}


def _measure(r, prefix):
    return next(m for m in r["measures"] if m["name"].startswith(prefix))


def test_identical_replicates_are_fully_stable():
    r = compare([{"a": _app(), "b": _app(route="API_ONLY")}] * 3)
    assert r["apps"] == ["a", "b"] and r["flagged"] == []
    assert [(m["k"], m["n"]) for m in r["measures"]] == [(2, 2), (2, 2), (2, 2), (4, 4)]
    assert r["agent_agreement"] == {"P1 A5 capability route": 1.0, "P2 A6 disposition": 1.0}


def test_changed_decisions_are_counted_and_flagged():
    reps = [{"a": _app(), "b": _app()},
            {"a": _app(route="API_ONLY", risk={"technical": 5, "security": 2}), "b": _app()},
            {"a": _app(route="API_ONLY", boundaries=("billing",)), "b": _app(disposition="Retain")}]
    r = compare(reps)
    assert (_measure(r, "P1 A5")["k"], _measure(r, "P1 A5")["n"]) == (1, 2)
    assert (_measure(r, "P2 A6")["k"], _measure(r, "P2 A6")["n"]) == (1, 2)
    assert (_measure(r, "P3 A2")["k"], _measure(r, "P3 A2")["n"]) == (1, 2)
    assert (_measure(r, "P1 A11")["k"], _measure(r, "P1 A11")["n"]) == (3, 4)
    flagged = {(f["agent"], f["app"]) for f in r["flagged"]}
    assert flagged == {("P1 A5 capability route", "a"), ("P2 A6 disposition", "b"),
                       ("P3 A2 boundaries", "a"), ("P1 A11 risk score", "a")}
    assert r["per_app"]["a"]["route"]["modal"] == "API_ONLY"


def test_apps_in_one_replicate_only_are_ignored_and_halves_merge():
    tune, holdout = {"a": _app()}, {"b": _app()}
    r = compare([merge([tune, holdout]), {"a": _app()}])
    assert r["apps"] == ["a"]
    with pytest.raises(ValueError):
        merge([tune, tune])


def test_snapshot_reads_the_decisions_of_a_finished_job(tmp_path: Path):
    store = ArtifactStore(tmp_path / "store")

    def put(aid, payload):
        store.publish({"artifact_id": aid, "artifact_version": 1, "producer_id": "t", "run_id": "r",
                       "application_id": aid.split("/")[1], "phase_id": aid[:2], "status": "PUBLISHED",
                       "payload": payload})

    put("P1/app/A5", {"capability_route": "UI"})
    put("P1/app/A11", {"risk_dimensions": [{"dimension": "technical", "score": 3},
                                           {"dimension": "data", "score": "unknown"}]})
    put("P2/PF1/A6", {"decisions": [{"application_id": "app", "proposed_disposition": "Replatform"}]})
    put("P3/app/A2", {"boundaries": [{"boundary": "src"}, {"boundary": "src"}]})
    db = sqlite3.connect(tmp_path / "appmod.db")
    db.execute("CREATE TABLE jobs (job_id TEXT, state TEXT)")
    db.execute("INSERT INTO jobs VALUES (?, ?)",
               ("job-1", json.dumps({"apps": ["app", "missing"], "facts": {"store_path": str(tmp_path / "store")}})))
    db.commit()
    snap = snapshot(tmp_path, "job-1")
    assert snap["app"] == {"route": "UI", "disposition": "Replatform", "boundaries": ["src"],
                           "risk": {"technical": 3}}
    assert snap["missing"] == {"route": None, "disposition": None, "boundaries": None, "risk": {}}


def test_pipeline_version_ignores_eval_code_and_flags_dirty_trees(tmp_path: Path):
    def git(*a):
        subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True)

    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (tmp_path / "appmod" / "evals").mkdir(parents=True)
    (tmp_path / "appmod" / "agent.py").write_text("v1\n")
    (tmp_path / "appmod" / "evals" / "x.py").write_text("v1\n")
    git("add", "-A")
    git("commit", "-qm", "one")
    v1 = pipeline_version(root=tmp_path)
    (tmp_path / "appmod" / "evals" / "x.py").write_text("v2\n")
    assert pipeline_version(root=tmp_path) == v1
    git("commit", "-qam", "evals only")
    assert pipeline_version(root=tmp_path) == v1
    (tmp_path / "appmod" / "agent.py").write_text("v2\n")
    assert pipeline_version(root=tmp_path) == v1 + "+dirty"
    git("commit", "-qam", "agent")
    assert pipeline_version(root=tmp_path) not in (v1, v1 + "+dirty")


def test_stability_report_assesses_c5():
    result = {"schema_valid_after_repair": {"valid": 1, "total": 1}, "evidence_resolvability": {"resolved": 1, "cited": 1},
              "hallucinated_paths": {"count": 0, "checked": 1}, "hallucinated_symbols": {"count": 0, "checked": 1},
              "golden_agreement": {}}
    stab = compare([{"a": _app()}, {"a": _app(route="API_ONLY")}])
    c5 = next(c for c in score(components(result, [], stab))["components"] if c["id"] == "C5")
    assert c5["assessed"] and c5["measures"][0]["k"] == 0 and c5["lower_bound"] == 0.0
