"""Human release authority for decision gates.

``with_human_review`` wraps a release gate: the wrapped gate still computes
its proposal deterministically, but publication requires a recorded human
decision bound to the exact candidate hash. No decision -> AWAITING_REVIEW
(nothing published, dependants wait). Approve -> the proposal publishes with
the reviewer identity (simulated=false). Reject -> gate FAILED with the
reviewer's reason. A superseded candidate always needs a fresh decision.
"""

from __future__ import annotations

from typing import Any, Callable, Protocol

from appmod.kernel.gates import GateContext, GateResult


class ReviewBackend(Protocol):
    def get_decision(self, job_id: str, phase: int, app: str, gate: str,
                     candidate_hash: str) -> dict[str, Any] | None: ...

    def ensure_pending(self, job_id: str, phase: int, app: str, gate: str,
                       candidate_hash: str, proposal: dict[str, Any]) -> str: ...


def candidate_of(record: dict[str, Any]) -> str:
    return record.get("candidate_hash") or record.get("manifest_hash") or ""


def with_human_review(impl: Callable[[GateContext], GateResult], backend: ReviewBackend,
                      job_id: str, phase: int, gate: str,
                      on_pending: Callable[[dict[str, Any]], None] | None = None,
                      audit: Any = None) -> Callable[[GateContext], GateResult]:
    def gate_fn(ctx: GateContext) -> GateResult:
        res = impl(ctx)
        if res.outcome == "FAILED":
            return res
        record = (res.payload or {}).get("decision_record")
        if not isinstance(record, dict):
            return res
        cand = candidate_of(record)
        app = ctx.application_id
        decision = backend.get_decision(job_id, phase, app, gate, cand)
        if decision is None:
            rid = backend.ensure_pending(job_id, phase, app, gate, cand, record)
            if on_pending:
                on_pending({"review_id": rid, "phase": phase, "app": app, "gate": gate,
                            "candidate_hash": cand, "proposed_status": record.get("status")})
            return GateResult("AWAITING_REVIEW", "PENDING",
                              {"review_id": rid, "candidate_hash": cand, "proposal": record},
                              [f"awaiting human review {rid} for {record.get('status')}"])
        if audit is not None:
            audit.review(ctx.run_id, gate, decision["reviewer"], False, decision["decision"], cand)
        if decision["decision"] == "approve":
            approved = dict(record, authorized_by=decision["reviewer"], simulated=False,
                            authorized_at=decision["decided_at"], review_id=decision["review_id"],
                            review_comment=decision.get("comment") or "")
            return GateResult(res.outcome, res.status, {**res.payload, "decision_record": approved},
                              res.reasons)
        reason = f"rejected by {decision['reviewer']}: {decision.get('comment') or 'no reason given'}"
        return GateResult("FAILED", "FAILED",
                          {"decision_record": dict(record, status="REJECTED",
                                                   rejected_by=decision["reviewer"],
                                                   review_id=decision["review_id"],
                                                   review_comment=decision.get("comment") or "")},
                          [reason])
    return gate_fn
