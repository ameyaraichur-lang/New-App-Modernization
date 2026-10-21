"""Live done-when checks fail closed when the run did not observe the thing they measure."""

import json
from pathlib import Path

from appmod.evals.measures import (
    critique_convergence, first_pass_validity, observed_share, ofbiz_completed, read_audit,
    route_agreement)


def test_first_pass_needs_the_structure_roles_valid():
    roles = [(2, "A6"), (3, "A1"), (3, "A2"), (3, "A3"), (4, "A3")]
    valid = [{"phase": p, "agent": a, "llm": {"first_pass_valid": True}} for p, a in roles]
    assert first_pass_validity(valid * 4)["pass"] is True
    mixed = valid * 3 + [{"phase": 2, "agent": "A6", "llm": {"first_pass_valid": False}}] * 2
    assert first_pass_validity(mixed)["k"] == 15 and first_pass_validity(mixed)["n"] == 17
    assert first_pass_validity(mixed)["pass"] is False
    assert first_pass_validity([])["pass"] is False


def test_critique_counts_only_requests_resolved_within_two_rounds():
    events = [
        {"kind": "CRITIQUE_RERUN", "run_id": "r", "node": "A10", "target": "A3",
         "statement": "names disagree", "round": 1},
        {"kind": "CRITIQUE_RESOLVED", "run_id": "r", "node": "A10", "target": "A3",
         "statement": "names disagree", "rounds": 1},
        {"kind": "CRITIQUE_ESCALATED", "run_id": "r", "node": "A7", "target": "A6",
         "statement": "route split", "rounds": 2},
    ]
    out = critique_convergence(events)
    assert out["k"] == 1 and out["n"] == 2 and out["pass"] is False
    resolved = []
    for i in range(20):
        item = {"run_id": "r", "node": "A10", "target": "A3", "statement": f"issue {i}"}
        resolved.append({**item, "kind": "CRITIQUE_RERUN", "round": 1})
        resolved.append({**item, "kind": "CRITIQUE_RESOLVED", "rounds": 1})
    assert critique_convergence(resolved)["pass"] is True
    assert critique_convergence([{"kind": "DISPATCH"}])["pass"] is False


def test_escalation_after_a_resolve_stays_a_failure():
    events = [
        {"kind": "CRITIQUE_RESOLVED", "run_id": "r", "node": "A8", "target": "A2",
         "statement": "boundary", "rounds": 1},
        {"kind": "CRITIQUE_ESCALATED", "run_id": "r", "node": "A8", "target": "A2",
         "statement": "boundary", "rounds": 2},
    ]
    assert critique_convergence(events)["pass"] is False


def test_evidence_share_requires_both_phases():
    evaluation = {"evidence_mix": {"P2": {"total": 10, "share_pct": 70.0},
                                   "P3": {"total": 10, "share_pct": 59.0}}}
    assert observed_share(evaluation)["pass"] is False
    evaluation["evidence_mix"]["P3"]["share_pct"] = 60.0
    assert observed_share(evaluation)["pass"] is True
    assert observed_share({"evidence_mix": {"P2": {"total": 0, "share_pct": 100.0},
                                            "P3": {"total": 4, "share_pct": 80.0}}})["pass"] is False


def test_ofbiz_must_finish_p1_p3_p4_inside_the_token_cap():
    def agents(success: bool, tokens: int) -> dict:
        rows = []
        for phase, n in ((1, 2), (3, 2), (4, 2)):
            rows.append({"phase": phase, "app": "ofbiz", "agent": "A1", "success": success,
                         "tokens": {"input": tokens}})
        return {"agents": rows}

    assert ofbiz_completed(agents(True, 1000))["pass"] is True
    assert ofbiz_completed(agents(False, 1000))["pass"] is False
    assert ofbiz_completed(agents(True, 99_313))["pass"] is False
    assert ofbiz_completed({"agents": []})["pass"] is False
    report = agents(True, 1000)
    report["agents"].append({"phase": 1, "app": "another-repo", "agent": "A1", "success": True,
                             "tokens": {"input": 99_313}})
    assert ofbiz_completed(report)["pass"] is True


def test_route_agreement_uses_the_point_estimate():
    stability = {"measures": [
        {"name": "P2 A6 disposition identical across runs", "k": 18, "n": 20, "lower_bound": 0.7},
        {"name": "P3 A2 boundary Jaccard >= 0.8", "k": 0, "n": 16, "lower_bound": 0.0},
    ]}
    assert route_agreement(stability)["pass"] is True
    stability["measures"][0]["k"] = 17
    assert route_agreement(stability)["pass"] is False
    assert route_agreement({"measures": []})["pass"] is False


def test_read_audit_joins_every_journal(tmp_path: Path):
    first = tmp_path / "audit-1.jsonl"
    second = tmp_path / "audit-2.jsonl"
    first.write_text(json.dumps({"kind": "CRITIQUE_RESOLVED", "rounds": 1}) + "\n")
    second.write_text("\n" + json.dumps({"kind": "DISPATCH"}) + "\n")
    assert [e["kind"] for e in read_audit(tmp_path)] == ["CRITIQUE_RESOLVED", "DISPATCH"]
