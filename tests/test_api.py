"""HTTP API: auth roles, run lifecycle, approvals/questions over HTTP, events, SSE."""

import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

CORPUS = Path(__file__).resolve().parents[2] / "corpus"
MICROBLOG = CORPUS / "microblog"
TOKENS = "op=olivia:operator;rv=rita:reviewer;sh=sam:stakeholder;vw=victor:viewer"


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("APPMOD_RUNS_DIR", str(tmp_path))
    monkeypatch.setenv("APPMOD_API_TOKENS", TOKENS)
    monkeypatch.setenv("APPMOD_AUTH_MODE", "token")
    monkeypatch.setenv("APPMOD_MAX_ACTIVE_RUNS_PER_USER", "1")
    from appmod.config import get_settings
    from appmod.server import api, auth
    get_settings.cache_clear()
    auth.reset()
    api._db = None
    api._jobs.clear()
    with TestClient(api.app) as c:
        yield c
    for j in list(api._jobs.values()):
        if j.running:
            j.cancel()
            j.thread.join(10)
    api._jobs.clear()
    api._db = None
    get_settings.cache_clear()
    auth.reset()


def H(tok):
    return {"Authorization": f"Bearer {tok}"}


def test_auth_required_and_roles(client):
    assert client.get("/api/health").status_code == 200
    assert client.get("/api/runs").status_code == 401
    assert client.get("/api/runs", headers=H("nope")).status_code == 401
    assert client.get("/api/runs", headers=H("vw")).status_code == 200
    assert client.get("/api/me", headers=H("rv")).json() == {"user": "rita", "roles": ["reviewer"]}
    assert client.post("/api/runs", json={"repo": "/tmp"}, headers=H("vw")).status_code == 403
    assert client.post("/api/runs", json={"repo": "/does/not/exist"}, headers=H("op")).status_code == 400
    assert client.post("/api/runs", json={"repo": "https://evil.example/x.git"},
                       headers=H("op")).status_code == 400


def test_admin_token_generated_at_startup(tmp_path, monkeypatch):
    monkeypatch.setenv("APPMOD_RUNS_DIR", str(tmp_path))
    monkeypatch.setenv("APPMOD_API_TOKENS", "")
    monkeypatch.setenv("APPMOD_AUTH_MODE", "token")
    from appmod.config import get_settings
    from appmod.server import api, auth
    get_settings.cache_clear()
    auth.reset()
    api._db = None
    try:
        with TestClient(api.app) as c:
            tok_file = tmp_path / ".admin_token"
            assert tok_file.is_file() and oct(tok_file.stat().st_mode & 0o777) == "0o600"
            assert c.get("/api/me", headers=H(tok_file.read_text().strip())).json()["roles"] == ["admin"]
    finally:
        api._db = None
        get_settings.cache_clear()
        auth.reset()


def test_health_tools(client):
    r = client.get("/api/health/tools", headers=H("vw")).json()
    assert {"astra", "analyzers", "tools", "mcp"} <= set(r)
    names = {t["name"] for t in r["tools"]}
    assert {"read_file", "grep", "get_artifact", "vulnerability_scan"} <= names
    assert "key" not in str(r["astra"]).lower()


@pytest.mark.skipif(not MICROBLOG.is_dir(), reason="corpus not cloned")
def test_restart_recovers_and_resumes(client, tmp_path):
    from appmod.server import api
    from appmod.server.jobs import PipelineJob
    job = PipelineJob(repos=[str(MICROBLOG)], llm=False, include_p5_p6=False, db=api.db(), owner="olivia")
    job.state["status"] = "RUNNING"
    job._persist(force=True)
    api._jobs.clear()
    api._recover_jobs()
    snap = client.get(f"/api/runs/{job.job_id}", headers=H("vw")).json()
    assert snap["status"] == "INTERRUPTED"
    assert client.post(f"/api/runs/{job.job_id}/resume", headers=H("op")).status_code == 200
    api._jobs[job.job_id].thread.join(60)
    assert client.get(f"/api/runs/{job.job_id}", headers=H("vw")).json()["status"] == "COMPLETED"


@pytest.mark.skipif(not MICROBLOG.is_dir(), reason="corpus not cloned")
def test_human_run_over_http(client):
    r = client.post("/api/runs", json={"repo": str(MICROBLOG), "review_mode": "human", "llm": False},
                    headers=H("op"))
    assert r.status_code == 200, r.text
    job = r.json()["job_id"]
    assert client.post("/api/runs", json={"repo": str(MICROBLOG)}, headers=H("op")).status_code == 429

    decided, answered, stale_checked = set(), 0, False
    deadline = time.time() + 120
    while time.time() < deadline:
        snap = client.get(f"/api/runs/{job}", headers=H("vw")).json()
        if snap["status"] in ("COMPLETED", "FAILED", "CANCELLED"):
            break
        for q in client.get(f"/api/runs/{job}/questions?status=OPEN", headers=H("vw")).json():
            assert client.post(f"/api/questions/{q['question_id']}/answer", json={"answer": "x"},
                               headers=H("rv")).status_code == 403
            assert client.post(f"/api/questions/{q['question_id']}/answer",
                               json={"answer": "Owned by the platform team"},
                               headers=H("sh")).status_code == 200
            answered += 1
        for rv in client.get(f"/api/reviews?job_id={job}&status=PENDING", headers=H("vw")).json():
            if not stale_checked:
                bad = client.post(f"/api/reviews/{rv['review_id']}/decision",
                                  json={"decision": "approve", "candidate_hash": "stale"}, headers=H("rv"))
                assert bad.status_code == 409
                assert client.post(f"/api/reviews/{rv['review_id']}/decision",
                                   json={"decision": "approve", "candidate_hash": rv["candidate_hash"]},
                                   headers=H("op")).status_code == 403
                stale_checked = True
            ok = client.post(f"/api/reviews/{rv['review_id']}/decision",
                             json={"decision": "approve", "candidate_hash": rv["candidate_hash"],
                                   "comment": "looks right"}, headers=H("rv"))
            if ok.status_code == 200:
                decided.add((rv["phase"], rv["app"]))
        time.sleep(0.3)
    snap = client.get(f"/api/runs/{job}", headers=H("vw")).json()
    assert snap["status"] == "COMPLETED", (snap["status"], snap["error"],
                                           [l["msg"] for l in snap["log"] if l["level"] == "error"])
    assert answered >= 3 and stale_checked
    assert {p for p, _ in decided} >= {1, 2, 3, 4}
    g2 = client.get(f"/api/runs/{job}/artifacts/P1/microblog/G2", headers=H("vw")).json()
    rec = g2["payload"]["decision_record"]
    assert rec["authorized_by"] == "rita" and rec["simulated"] is False
    a8 = client.get(f"/api/runs/{job}/artifacts/P1/microblog/A8", headers=H("vw")).json()
    assert all(c["respondent"] == "sam" for c in a8["payload"]["confirmed_responses"])

    evs = client.get(f"/api/runs/{job}/events?kinds=NODE,PHASE,REVIEW_PENDING", headers=H("vw")).json()
    assert any(e["kind"] == "REVIEW_PENDING" for e in evs)
    with client.stream("GET", f"/api/runs/{job}/stream?token=vw&after=0") as s:
        body = b""
        for chunk in s.iter_bytes():
            body += chunk
            if b"event: END" in body:
                break
    assert b"event: NODE" in body and b"event: END" in body
