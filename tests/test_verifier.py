"""Claim-support verifier: unsupported cited claims are published as INFERRED (C3)."""

import json
import re

from appmod.agents.runtime import AgentOutcome
from appmod.agents.verifier import ClaimVerifier, in_audit_sample
from appmod.evals.run import _c3
from appmod.kernel.evidence import enforce
from appmod.llm.errors import LLMError
from appmod.llm.types import ModelResponse, Usage
from appmod.tools.gateway import EvidenceLedger

REQS = "flask==2.0.1\nflask-sqlalchemy==3.0\nredis==4.5\n"


class KeywordVerifier:
    """Entails a claim when its last word appears in the evidence it cites."""

    def __init__(self, fail=None):
        self.fail = fail
        self.calls = []

    def complete(self, tier, *, instructions, input_items, tools, tool_choice, reasoning_effort,
                 max_output_tokens, on_call=None, context=None):
        if self.fail:
            raise self.fail
        self.calls.append((tier, context))
        prompt = input_items[0]["content"]
        evidence = " ".join(re.findall(r"<evidence[^>]*>\n(.*?)\n</evidence>", prompt, re.S)).lower()
        verdicts = []
        for cid, claim in re.findall(r"^- (c\d+): (.*)$", prompt, re.M):
            word = re.findall(r"\w+", claim.lower())[-1]
            verdicts.append({"claim": cid, "verdict": "ENTAILED" if word in evidence else "NOT_ENTAILED",
                             "reason": f"'{word}' {'in' if word in evidence else 'not in'} evidence"})
        return ModelResponse("v", "verifier-deploy", "m", [{
            "type": "function_call", "call_id": "v1", "name": "submit_verdicts",
            "arguments": json.dumps({"verdicts": verdicts})}], usage=Usage())


def _outcome(ev, *, unsupported_cites=None):
    return AgentOutcome(status="COMPLETE", payload={"datasets": [
        {"statement": "cache store is redis", "evidence_class": "OBSERVED", "evidence_ids": [ev],
         "origin": "llm"}]}, findings=[
        {"id": "F1", "statement": "web framework is flask", "evidence_class": "OBSERVED",
         "evidence_ids": [ev], "origin": "llm"},
        {"id": "F2", "statement": "primary database is postgresql", "evidence_class": "DOCUMENTED",
         "evidence_ids": unsupported_cites or [ev], "origin": "llm"},
        {"id": "S1", "statement": "requirements.txt lists 3 packages", "evidence_class": "OBSERVED",
         "evidence_ids": [], "origin": "tool"},
    ])


def test_injected_unsupported_claim_is_downgraded():
    ledger = EvidenceLedger()
    ev = ledger.register("tool", REQS, tool="read_file")
    out = _outcome(ev)
    router = KeywordVerifier()
    events = []
    summary = ClaimVerifier(router, "fallback").verify("P1.A1", out, ledger,
                                                       lambda k, **f: events.append((k, f)))
    f1, f2, seed = out.findings
    assert f1["evidence_class"] == "OBSERVED" and f1["support"]["verdict"] == "ENTAILED"
    assert f2["evidence_class"] == "INFERRED"
    assert f2["support"].items() >= {"verdict": "NOT_ENTAILED", "downgraded_from": "DOCUMENTED",
                                     "verifier": "verifier-deploy"}.items()
    assert out.payload["datasets"][0]["support"]["verdict"] == "ENTAILED"
    assert "support" not in seed
    assert summary.items() >= {"claims": 3, "entailed": 2, "not_entailed": 1, "downgraded": 1}.items()
    assert router.calls == [("fallback", {"agent": "P1.A1", "role": "verifier",
                                          "prompt_version": "claim-verifier/1"})]
    assert ("VERIFIER", {"agent": "P1.A1", "claims": 3, "entailed": 2, "not_entailed": 1,
                         "insufficient": 0, "unchecked": 0}) in events
    # the downgrade survives the evidence kernel (the claim keeps its valid citation)
    out.known_evidence = set(ledger.ids())
    enforce(out)
    assert out.findings[1]["evidence_class"] == "INFERRED" and out.findings[1]["evidence_ids"] == [ev]


def test_claims_without_checkable_text_or_verdict_stay_unchecked():
    ledger = EvidenceLedger()
    ev = ledger.register("tool", REQS)
    art = ledger.register("artifact", "sha-only", text="", eid="art:x@v1")
    out = _outcome(ev, unsupported_cites=[art])
    ClaimVerifier(KeywordVerifier()).verify("P1.A1", out, ledger)
    f2 = out.findings[1]
    assert f2["evidence_class"] == "DOCUMENTED" and f2["support"]["verdict"] == "UNCHECKED"

    out = _outcome(ev)
    summary = ClaimVerifier(KeywordVerifier(fail=LLMError("boom"))).verify("P1.A1", out, ledger)
    assert [f["evidence_class"] for f in out.findings[:2]] == ["OBSERVED", "DOCUMENTED"]
    assert all(f["support"]["verdict"] == "UNCHECKED" for f in out.findings[:2])
    assert "verifier unavailable" in out.findings[0]["support"]["reason"]
    assert summary["unchecked"] == 3 and summary["downgraded"] == 0


def test_audit_sample_is_deterministic_and_near_rate():
    hits = sum(in_audit_sample("P1.A1", f"claim {i}", 0.05) for i in range(4000))
    assert 0.035 < hits / 4000 < 0.065
    assert in_audit_sample("P1.A1", "claim 7", 0.05) == in_audit_sample("P1.A1", "claim 7", 0.05)
    ledger = EvidenceLedger()
    ev = ledger.register("tool", REQS)
    out = _outcome(ev)
    ClaimVerifier(KeywordVerifier(), audit_rate=1.0).verify("P1.A1", out, ledger)
    assert out.findings[0]["support"]["audit"] is True
    assert out.findings[0]["support"]["evidence_excerpts"] == {ev: REQS}


def test_c3_counts_unchecked_as_not_entailed():
    c = _c3({"ENTAILED": 90, "NOT_ENTAILED": 5, "UNCHECKED": 5})
    assert c.measures[0].k == 90 and c.measures[0].n == 100
    assert _c3({}).reason and _c3({"NO_RECORD": 4}).reason
