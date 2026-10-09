"""Durable run store (SQLite, WAL): jobs, events, reviews, stakeholder questions.

Reviews bind a human decision to the exact candidate hash a gate proposed;
deciding against a superseded hash raises ``StaleReview`` (HTTP 409).
Questions carry recorded stakeholder answers — the only path by which
HUMAN_CONFIRMED evidence enters the pipeline.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from typing import Any

from appmod.config import redact

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
  job_id TEXT PRIMARY KEY, owner TEXT, status TEXT, created_at TEXT, updated_at TEXT,
  spec TEXT, state TEXT
);
CREATE TABLE IF NOT EXISTS events (
  job_id TEXT, seq INTEGER, ts TEXT, kind TEXT, data TEXT, PRIMARY KEY (job_id, seq)
);
CREATE TABLE IF NOT EXISTS reviews (
  review_id TEXT PRIMARY KEY, job_id TEXT, phase INTEGER, app TEXT, gate TEXT,
  candidate_hash TEXT, proposal TEXT, status TEXT, decision TEXT, reviewer TEXT,
  comment TEXT, created_at TEXT, decided_at TEXT
);
CREATE INDEX IF NOT EXISTS reviews_lookup ON reviews (job_id, phase, app, gate, status);
CREATE TABLE IF NOT EXISTS questions (
  question_id TEXT PRIMARY KEY, job_id TEXT, app TEXT, question TEXT, why TEXT,
  target_role TEXT, source TEXT, status TEXT, answer TEXT, respondent TEXT,
  created_at TEXT, answered_at TEXT, UNIQUE (job_id, app, question)
);
"""


class StaleReview(Exception):
    pass


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class RunDB:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._con = sqlite3.connect(str(self.path), check_same_thread=False, isolation_level=None)
        self._con.row_factory = sqlite3.Row
        self._lock = threading.RLock()
        self._con.execute("PRAGMA journal_mode=WAL")
        self._con.executescript(SCHEMA)
        self._seq: dict[str, int] = {}

    def _q(self, sql: str, args: tuple = ()) -> list[sqlite3.Row]:
        with self._lock:
            return self._con.execute(sql, args).fetchall()

    # -- jobs ---------------------------------------------------------------------

    def save_job(self, job_id: str, owner: str, status: str, spec: dict, state: dict) -> None:
        with self._lock:
            self._con.execute(
                "INSERT INTO jobs (job_id, owner, status, created_at, updated_at, spec, state) "
                "VALUES (?,?,?,?,?,?,?) ON CONFLICT(job_id) DO UPDATE SET status=excluded.status, "
                "updated_at=excluded.updated_at, state=excluded.state",
                (job_id, owner, status, _now(), _now(), json.dumps(spec),
                 redact(json.dumps(state, default=str))))

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        rows = self._q("SELECT * FROM jobs WHERE job_id=?", (job_id,))
        if not rows:
            return None
        r = dict(rows[0])
        r["spec"], r["state"] = json.loads(r["spec"]), json.loads(r["state"])
        return r

    def list_jobs(self, owner: str | None = None) -> list[dict[str, Any]]:
        sql = "SELECT job_id, owner, status, created_at, updated_at, spec FROM jobs"
        rows = self._q(sql + (" WHERE owner=?" if owner else "") + " ORDER BY created_at DESC",
                       (owner,) if owner else ())
        return [dict(r, spec=json.loads(r["spec"])) for r in rows]

    # -- events -------------------------------------------------------------------

    def add_event(self, job_id: str, kind: str, data: dict[str, Any]) -> int:
        with self._lock:
            if job_id not in self._seq:
                row = self._con.execute("SELECT MAX(seq) FROM events WHERE job_id=?", (job_id,)).fetchone()
                self._seq[job_id] = row[0] or 0
            self._seq[job_id] += 1
            seq = self._seq[job_id]
            self._con.execute("INSERT INTO events VALUES (?,?,?,?,?)",
                              (job_id, seq, _now(), kind,
                               redact(json.dumps(data, default=str))))
            return seq

    def events_since(self, job_id: str, seq: int = 0, limit: int = 500,
                     kinds: list[str] | None = None) -> list[dict[str, Any]]:
        sql = "SELECT seq, ts, kind, data FROM events WHERE job_id=? AND seq>?"
        args: list[Any] = [job_id, seq]
        if kinds:
            sql += f" AND kind IN ({','.join('?' * len(kinds))})"
            args += kinds
        rows = self._q(sql + " ORDER BY seq LIMIT ?", tuple(args + [limit]))
        return [{"seq": r["seq"], "ts": r["ts"], "kind": r["kind"], **json.loads(r["data"])} for r in rows]

    # -- reviews ------------------------------------------------------------------

    def get_decision(self, job_id: str, phase: int, app: str, gate: str,
                     candidate_hash: str) -> dict[str, Any] | None:
        rows = self._q("SELECT * FROM reviews WHERE job_id=? AND phase=? AND app=? AND gate=? "
                       "AND candidate_hash=? AND status='DECIDED' ORDER BY decided_at DESC LIMIT 1",
                       (job_id, phase, app, gate, candidate_hash))
        return self._review(rows[0]) if rows else None

    def ensure_pending(self, job_id: str, phase: int, app: str, gate: str, candidate_hash: str,
                       proposal: dict[str, Any]) -> str:
        with self._lock:
            rows = self._q("SELECT review_id, candidate_hash FROM reviews WHERE job_id=? AND phase=? "
                           "AND app=? AND gate=? AND status='PENDING'", (job_id, phase, app, gate))
            for r in rows:
                if r["candidate_hash"] == candidate_hash:
                    return r["review_id"]
                self._con.execute("UPDATE reviews SET status='SUPERSEDED' WHERE review_id=?",
                                  (r["review_id"],))
            rid = f"rev-{uuid.uuid4().hex[:10]}"
            self._con.execute(
                "INSERT INTO reviews (review_id, job_id, phase, app, gate, candidate_hash, proposal, "
                "status, created_at) VALUES (?,?,?,?,?,?,?,'PENDING',?)",
                (rid, job_id, phase, app, gate, candidate_hash, json.dumps(proposal, default=str), _now()))
            return rid

    def decide(self, review_id: str, decision: str, reviewer: str, comment: str,
               candidate_hash: str) -> dict[str, Any]:
        if decision not in ("approve", "reject"):
            raise ValueError("decision must be approve or reject")
        with self._lock:
            rows = self._q("SELECT * FROM reviews WHERE review_id=?", (review_id,))
            if not rows:
                raise KeyError(review_id)
            r = rows[0]
            if r["status"] != "PENDING":
                raise StaleReview(f"review {review_id} is {r['status']}")
            if r["candidate_hash"] != candidate_hash:
                raise StaleReview("candidate hash does not match the pending proposal")
            self._con.execute("UPDATE reviews SET status='DECIDED', decision=?, reviewer=?, comment=?, "
                              "decided_at=? WHERE review_id=?",
                              (decision, reviewer, comment, _now(), review_id))
            return self._review(self._q("SELECT * FROM reviews WHERE review_id=?", (review_id,))[0])

    def list_reviews(self, job_id: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        sql, args = "SELECT * FROM reviews WHERE 1=1", []
        if job_id:
            sql, args = sql + " AND job_id=?", args + [job_id]
        if status:
            sql, args = sql + " AND status=?", args + [status]
        return [self._review(r) for r in self._q(sql + " ORDER BY created_at", tuple(args))]

    @staticmethod
    def _review(r: sqlite3.Row) -> dict[str, Any]:
        d = dict(r)
        d["proposal"] = json.loads(d["proposal"] or "{}")
        return d

    # -- questions ----------------------------------------------------------------

    def add_question(self, job_id: str, app: str, question: str, why: str = "",
                     target_role: str = "", source: str = "seed") -> str:
        with self._lock:
            rows = self._q("SELECT question_id FROM questions WHERE job_id=? AND app=? AND question=?",
                           (job_id, app, question))
            if rows:
                return rows[0]["question_id"]
            qid = f"q-{uuid.uuid4().hex[:10]}"
            self._con.execute(
                "INSERT INTO questions (question_id, job_id, app, question, why, target_role, source, "
                "status, created_at) VALUES (?,?,?,?,?,?,?,'OPEN',?)",
                (qid, job_id, app, question, why, target_role, source, _now()))
            return qid

    def answer(self, question_id: str, answer: str, respondent: str) -> dict[str, Any]:
        if not answer.strip() or not respondent.strip():
            raise ValueError("answer and respondent are required")
        with self._lock:
            rows = self._q("SELECT * FROM questions WHERE question_id=?", (question_id,))
            if not rows:
                raise KeyError(question_id)
            self._con.execute("UPDATE questions SET status='ANSWERED', answer=?, respondent=?, "
                              "answered_at=? WHERE question_id=?",
                              (answer.strip(), respondent.strip(), _now(), question_id))
            return dict(self._q("SELECT * FROM questions WHERE question_id=?", (question_id,))[0])

    def list_questions(self, job_id: str, app: str | None = None,
                       status: str | None = None) -> list[dict[str, Any]]:
        sql, args = "SELECT * FROM questions WHERE job_id=?", [job_id]
        if app:
            sql, args = sql + " AND app=?", args + [app]
        if status:
            sql, args = sql + " AND status=?", args + [status]
        return [dict(r) for r in self._q(sql + " ORDER BY created_at", tuple(args))]

    def answers_digest(self, job_id: str, app: str) -> str:
        rows = self._q("SELECT question_id, answer, respondent FROM questions WHERE job_id=? AND app=? "
                       "AND status='ANSWERED' ORDER BY question_id", (job_id, app))
        if not rows:
            return ""
        blob = json.dumps([[r["question_id"], r["answer"], r["respondent"]] for r in rows])
        return hashlib.sha256(blob.encode()).hexdigest()[:16]
