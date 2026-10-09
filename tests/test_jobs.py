"""Job driver: multi-app flow, human review gates, recorded answers, reuse."""

import threading
import time
from pathlib import Path

import pytest

from appmod.server.jobs import PipelineJob, validate_repo_input
from appmod.server.rundb import RunDB, StaleReview

CORPUS = Path(__file__).resolve().parents[2] / "corpus"
MICROBLOG = CORPUS / "microblog"

needs_corpus = pytest.mark.skipif(not MICROBLOG.is_dir(), reason="corpus not cloned")


def _reviewer(db: RunDB, job_id: str, stop: threading.Event, seen: list, answer=True):
    while not stop.is_set():
        if answer:
            for q in db.list_questions(job_id, status="OPEN"):
                db.answer(q["question_id"], f"scripted answer to: {q['question'][:40]}",
                          "scripted-stakeholder")
        for r in db.list_reviews(job_id, "PENDING"):
            seen.append((r["phase"], r["app"], r["proposal"].get("status")))
            db.decide(r["review_id"], "approve", "scripted-reviewer", "ok", r["candidate_hash"])
        time.sleep(0.2)


@needs_corpus
def test_human_review_flow(tmp_path):
    db = RunDB(tmp_path / "appmod.db")
    job = PipelineJob(repos=[str(MICROBLOG)], runs_root=tmp_path, llm=False, review_mode="human",
                      include_p5_p6=False, db=db)
    stop, seen = threading.Event(), []
    t = threading.Thread(target=_reviewer, args=(db, job.job_id, stop, seen), daemon=True)
    t.start()
    job._execute()
    stop.set()
    snap = job.snapshot()
    assert snap["status"] == "COMPLETED", snap["error"]
    assert {p for p, _, _ in seen} >= {1, 2, 3, 4}
    a8 = job.store.get("P1/microblog/A8")["payload"]
    assert a8["confirmed_responses"] and all(c["evidence_class"] == "HUMAN_CONFIRMED"
                                             and c["respondent"] == "scripted-stakeholder"
                                             for c in a8["confirmed_responses"])
    g2 = job.store.get("P1/microblog/G2")["payload"]["decision_record"]
    assert g2["authorized_by"] == "scripted-reviewer" and g2["simulated"] is False
    assert db.list_reviews(job.job_id, "PENDING") == []


@needs_corpus
def test_reject_fails_gate(tmp_path):
    db = RunDB(tmp_path / "appmod.db")
    job = PipelineJob(repos=[str(MICROBLOG)], runs_root=tmp_path, llm=False, review_mode="human",
                      include_p5_p6=False, db=db)

    def rejector():
        while True:
            for r in db.list_reviews(job.job_id, "PENDING"):
                db.decide(r["review_id"], "reject", "qa", "insufficient evidence", r["candidate_hash"])
                return
            time.sleep(0.1)

    threading.Thread(target=rejector, daemon=True).start()
    job._execute()
    snap = job.snapshot()
    assert snap["status"] == "FAILED"
    p1 = next(p for p in snap["phases"] if p["phase"] == 1)
    assert p1["status"] == "FAILED"


@needs_corpus
def test_rerun_reuses_unchanged_nodes(tmp_path):
    job = PipelineJob(repos=[str(MICROBLOG)], runs_root=tmp_path, llm=False, include_p5_p6=False)
    job._execute()
    assert job.snapshot()["status"] == "COMPLETED"
    n0 = len(job.store.versions("P1/microblog/A1"))
    job.force[(1, "microblog")] = set()
    job._execute()
    snap = job.snapshot()
    assert snap["status"] == "COMPLETED"
    assert len(job.store.versions("P1/microblog/A1")) == n0
    p1 = next(p for p in snap["phases"] if p["phase"] == 1)
    assert all(n.get("reused") for n in p1["nodes"] if n["id"] != "G0")


@needs_corpus
def test_cancel(tmp_path):
    db = RunDB(tmp_path / "appmod.db")
    job = PipelineJob(repos=[str(MICROBLOG)], runs_root=tmp_path, llm=False, review_mode="human",
                      include_p5_p6=False, db=db)
    job.start()
    for _ in range(100):
        if db.list_reviews(job.job_id, "PENDING"):
            break
        time.sleep(0.1)
    job.cancel()
    job.thread.join(10)
    assert job.snapshot()["status"] == "CANCELLED"


def test_stale_review(tmp_path):
    db = RunDB(tmp_path / "x.db")
    rid = db.ensure_pending("j", 1, "a", "G2", "h1", {"status": "X"})
    rid2 = db.ensure_pending("j", 1, "a", "G2", "h2", {"status": "Y"})
    assert rid != rid2
    with pytest.raises(StaleReview):
        db.decide(rid, "approve", "r", "", "h1")           # superseded
    with pytest.raises(StaleReview):
        db.decide(rid2, "approve", "r", "", "h1")          # wrong hash
    d = db.decide(rid2, "approve", "r", "", "h2")
    assert d["decision"] == "approve"
    assert db.get_decision("j", 1, "a", "G2", "h2")["reviewer"] == "r"


def test_answers_digest_changes(tmp_path):
    db = RunDB(tmp_path / "x.db")
    q = db.add_question("j", "a", "Who owns it?")
    assert db.add_question("j", "a", "Who owns it?") == q
    assert db.answers_digest("j", "a") == ""
    db.answer(q, "team x", "alice")
    d1 = db.answers_digest("j", "a")
    db.answer(q, "team y", "alice")
    assert d1 and db.answers_digest("j", "a") != d1


def test_repo_allowlists(tmp_path, monkeypatch):
    from appmod.config import Settings
    s = Settings(repo_roots=str(tmp_path), git_hosts="github.com")
    validate_repo_input(str(tmp_path), s)
    with pytest.raises(ValueError):
        validate_repo_input("/etc", s)
    validate_repo_input("https://github.com/a/b.git", s)
    with pytest.raises(ValueError):
        validate_repo_input("https://evil.example/a/b.git", s)
    with pytest.raises(ValueError):
        validate_repo_input("http://github.com/a/b.git", s)
