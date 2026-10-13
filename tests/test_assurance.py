"""Assurance gate: unverified items wait for confirmation; scripted confirmation is its own class."""

from appmod.contracts.schemas import content_hash
from appmod.kernel.assurance import assess, classify, with_assurance
from appmod.kernel.gates import GateContext, GenericGates
from appmod.kernel.reviews import with_human_review

ROUTE = {"application_id": "shop", "proposed_disposition": "Replatform", "rationale": "move to containers",
         "evidence_class": "INFERRED", "evidence_ids": [], "origin": "llm"}


def _a6(*decisions):
    art = {"artifact_id": "P2/PF1/A6", "artifact_version": 1, "status": "COMPLETE",
           "payload": {"decisions": list(decisions)},
           "findings": [{"id": "A6-F1", "statement": "6 apps in scope", "evidence_class": "OBSERVED"}]}
    return dict(art, content_hash=content_hash(art))


class Backend:
    def __init__(self):
        self.pending, self.decision = [], None

    def get_decision(self, job_id, phase, app, gate, candidate_hash):
        return self.decision

    def ensure_pending(self, job_id, phase, app, gate, candidate_hash, proposal):
        self.pending.append(proposal)
        return f"rv-{len(self.pending)}"


def _ctx(art):
    return GateContext(run_id="r", application_id="PF1", gate_id="G2", policy=None,
                       inputs={"A6": art}, run_inputs={}, gate_cfg={"candidate_node": "A6"},
                       published={"A6": art})


def _decide(backend, reviewer):
    backend.decision = {"decision": "approve", "reviewer": reviewer, "decided_at": "2026-10-13T10:00:00Z",
                        "review_id": "rv-1", "comment": "checked"}


def test_unverified_p2_route_raises_review_and_g2_waits_until_confirmed():
    backend = Backend()
    gate = with_human_review(with_assurance(GenericGates.release_gate, human_review=True),
                             backend, "job", 2, "G2")
    ctx = _ctx(_a6(ROUTE))

    res = gate(ctx)
    assert res.outcome == "AWAITING_REVIEW"
    listed = backend.pending[0]["assurance"]["unverified"]
    assert [(u["artifact"], u["path"], u["item"]) for u in listed] == [
        ("P2/PF1/A6", "payload.decisions[0]", "move to containers")]
    assert gate(ctx).outcome == "AWAITING_REVIEW"          # still waiting: nobody decided

    _decide(backend, "alice")
    res = gate(ctx)
    assert res.outcome == "PUBLISHED"
    a = res.payload["decision_record"]["assurance"]
    assert a["counts"] == {"tool-measured": 1, "human-confirmed": 1}
    assert a["confirmed"] == {"by": "alice", "class": "human-confirmed", "items": 1,
                              "at": "2026-10-13T10:00:00Z"}


def test_scripted_and_simulated_confirmations_are_not_human():
    backend = Backend()
    gate = with_human_review(with_assurance(GenericGates.release_gate, human_review=True),
                             backend, "job", 2, "G2")
    _decide(backend, "scripted-reviewer")
    a = gate(_ctx(_a6(ROUTE))).payload["decision_record"]["assurance"]
    assert a["counts"]["scripted-confirmed"] == 1 and "human-confirmed" not in a["counts"]

    res = with_assurance(GenericGates.release_gate)(_ctx(_a6(ROUTE)))
    rec = res.payload["decision_record"]
    assert res.outcome == "PUBLISHED" and rec["simulated"] is True
    assert rec["assurance"]["confirmed"]["class"] == "scripted-confirmed"
    assert rec["assurance"]["counts"] == {"tool-measured": 1, "scripted-confirmed": 1}


def test_classes():
    entailed = dict(ROUTE, evidence_class="OBSERVED", support={"verdict": "ENTAILED"})
    downgraded = dict(ROUTE, support={"verdict": "INSUFFICIENT", "downgraded_from": "OBSERVED"})
    answer = {"evidence_class": "HUMAN_CONFIRMED", "respondent": "bob", "answer": "high"}
    scripted = dict(answer, respondent="scripted-stakeholder")
    pilot = dict(answer, respondent="pilot-simulated-business-owner")
    assert [classify(i) for i in (entailed, downgraded, ROUTE, answer, scripted, pilot)] == [
        "entailed", "unverified", "unverified", "human-confirmed", "scripted-confirmed", "scripted-confirmed"]
    a = assess({"A6": _a6(entailed, downgraded)})
    assert a["counts"] == {"tool-measured": 1, "entailed": 1, "unverified": 1}
    assert a["unverified"][0]["verdict"] == "INSUFFICIENT"


def test_eval_separates_scripted_from_independent_assurance():
    from collections import Counter

    from appmod.evals.run import _assurance, _assurance_md
    a = _assurance(Counter({"tool-measured": 60, "entailed": 20, "scripted-confirmed": 15,
                            "human-confirmed": 5}), gates=4, gates_without=0)
    assert a["coverage_pct"] == 100.0 and a["independent_pct"] == 85.0
    assert "85.0% without scripted confirmation" in "\n".join(_assurance_md(a))
