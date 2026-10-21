"""``ask_stakeholder`` — human input for any P1–P4 agent.

Human review mode (``review_mode=human``):
  - Non-blocking questions are recorded in the run DB and the agent continues.
  - Blocking questions raise ``AwaitingStakeholderInput``; the orchestrator parks
    the node in ``AWAITING_INPUT`` (nothing published; dependants wait). When a
    stakeholder answers via the questions API, only that node re-runs with the
    answer in context as citable HUMAN_CONFIRMED evidence.

Simulated review mode (``review_mode=simulated``):
  - Blocking questions never hang a run: the question is recorded, the tool
    returns an error telling the agent to proceed and record a ``PENDING_HUMAN``
    gap instead of waiting for a human.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from appmod.tools.gateway import ToolEnv


class AwaitingStakeholderInput(Exception):
    """Blocking stakeholder question recorded; agent dispatch must park."""

    def __init__(self, question_id: str, question: str, why: str = "", target_role: str = ""):
        self.question_id = question_id
        self.question = question
        self.why = why
        self.target_role = target_role
        super().__init__(question_id)


@dataclass
class StakeholderBridge:
    """Run-scoped bridge from ``ask_stakeholder`` to the job questions store."""

    job_id: str
    phase: int
    app: str
    node: str
    review_mode: str
    ensure: Callable[..., str]
    list_for_node: Callable[[], list[dict[str, Any]]]
    count_open_blocking: Callable[[], int]
    count_total: Callable[[], int]
    max_open_blocking: int
    max_total: int
    on_pending: Callable[[dict[str, Any]], None] | None = None

    def answered_for_node(self) -> list[dict[str, Any]]:
        return [q for q in self.list_for_node() if q.get("status") == "ANSWERED"]

    def _over_limit(self, blocking: bool) -> str | None:
        if self.count_total() >= self.max_total:
            return (f"stakeholder question limit reached ({self.max_total} per app per run); "
                    "proceed without asking and record a gap with state PENDING_HUMAN")
        if blocking and self.count_open_blocking() >= self.max_open_blocking:
            return (f"open blocking question limit reached ({self.max_open_blocking} per app); "
                    "proceed without asking and record a gap with state PENDING_HUMAN")
        return None


def ask_stakeholder(env: ToolEnv, args: dict[str, Any]) -> dict[str, Any]:
    bridge: StakeholderBridge | None = getattr(env, "stakeholder", None)
    if bridge is None:
        raise ValueError("ask_stakeholder is not available for this dispatch")
    question = (args.get("question") or "").strip()
    if not question:
        raise ValueError("question is required")
    why = (args.get("why") or "").strip()
    target_role = (args.get("target_role") or "").strip()
    blocking = bool(args.get("blocking"))

    limit_msg = bridge._over_limit(blocking)
    if limit_msg:
        return {"error": limit_msg, "rate_limited": True}

    qid = bridge.ensure(
        question=question, why=why, target_role=target_role,
        blocking=blocking, source="ask_stakeholder",
    )
    existing = next((q for q in bridge.list_for_node() if q["question_id"] == qid), None)
    if existing and existing.get("status") == "ANSWERED":
        return {
            "question_id": qid,
            "status": "ANSWERED",
            "question": existing["question"],
            "answer": existing["answer"],
            "respondent": existing["respondent"],
            "evidence_class": "HUMAN_CONFIRMED",
            "cite_as": f"human:{qid}",
            "note": "Recorded stakeholder answer — cite human:" + qid + " in findings.",
        }

    if not blocking:
        return {
            "question_id": qid,
            "status": "OPEN",
            "recorded": True,
            "blocking": False,
            "note": "Non-blocking question recorded; continue your investigation.",
        }

    if bridge.review_mode != "human":
        return {
            "question_id": qid,
            "status": "OPEN",
            "recorded": True,
            "blocking": False,
            "simulated": True,
            "error": ("simulated review mode: blocking questions do not pause the run; "
                      "record a gap with state PENDING_HUMAN and proceed"),
        }

    payload = {
        "question_id": qid, "question": question, "why": why,
        "target_role": target_role, "phase": bridge.phase,
        "app": bridge.app, "node": bridge.node, "blocking": True,
    }
    if bridge.on_pending:
        bridge.on_pending(payload)
    raise AwaitingStakeholderInput(qid, question, why, target_role)
