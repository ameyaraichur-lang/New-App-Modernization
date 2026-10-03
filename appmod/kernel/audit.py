"""Append-only audit journal.

Run Controls: 'Record run ID, agent/stage, tool/model/prompt versions,
input/output hashes, start/end, validator results, exceptions and decision
authority. Protect audit data and avoid raw credentials.'
Events are JSONL; each line is self-describing and immutable once written.
"""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class AuditJournal:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / f"audit-{int(time.time())}-{uuid.uuid4().hex[:6]}.jsonl"

    def emit(self, kind: str, **fields: Any) -> dict[str, Any]:
        event = {"ts": _now(), "kind": kind, **fields}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")
        return event

    # common event helpers -----------------------------------------------------

    def dispatch(self, run_id: str, node: str, attempt: int, input_hash: str) -> None:
        self.emit("DISPATCH", run_id=run_id, node=node, attempt=attempt, input_hash=input_hash)

    def publish(self, run_id: str, artifact_id: str, version: int, status: str,
                content_hash: str, validator_ok: bool) -> None:
        self.emit("PUBLISH", run_id=run_id, artifact_id=artifact_id, version=version,
                  status=status, content_hash=content_hash, validator_ok=validator_ok)

    def gate(self, run_id: str, gate: str, outcome: str, reasons: list[str]) -> None:
        self.emit("GATE", run_id=run_id, gate=gate, outcome=outcome, reasons=reasons)

    def invalidation(self, run_id: str, origin: str, affected: list[str]) -> None:
        self.emit("INVALIDATION", run_id=run_id, origin=origin, affected=affected)

    def review(self, run_id: str, gate: str, reviewer: str, simulated: bool,
               decision: str, candidate_hash: str) -> None:
        self.emit("REVIEW", run_id=run_id, gate=gate, reviewer=reviewer,
                  simulated=simulated, decision=decision, candidate_hash=candidate_hash)

    def retry_exhausted(self, run_id: str, node: str, attempts: int) -> None:
        self.emit("RETRY_EXHAUSTED", run_id=run_id, node=node, attempts=attempts)

    def read_all(self) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
        return events
