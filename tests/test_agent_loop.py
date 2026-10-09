"""Agent loop with a scripted fake router: tool use, citation repair, seed
fallback, evidence enforcement and gateway sandboxing — no network."""

import json
import re
from pathlib import Path

import pytest

from appmod.agents.llm_runner import LLMAgentRunner
from appmod.agents.runtime import AgentOutcome
from appmod.config import Settings
from appmod.kernel.evidence import enforce
from appmod.kernel.policy import PolicyService
from appmod.llm.errors import ContentFilteredError
from appmod.llm.types import ModelResponse, Usage
from appmod.phases.p1.engine import P1AgentRunner
from appmod.registry.compiler import resolve_registry
from appmod.tools.builtin import build_gateway
from appmod.tools.gateway import EvidenceLedger, ToolEnv, safe_path

CORPUS = Path(__file__).resolve().parents[2] / "corpus"
MICROBLOG = CORPUS / "microblog"
needs_corpus = pytest.mark.skipif(not MICROBLOG.is_dir(), reason="corpus not cloned")


def minimal(schema):
    t = schema.get("type")
    if isinstance(t, list):
        if "null" in t:
            return None
        t = t[0]
    if "enum" in schema:
        return schema["enum"][0]
    if t == "object":
        return {k: minimal(v) for k, v in schema.get("properties", {}).items()}
    if t == "array":
        return []
    if t in ("integer", "number"):
        return 0
    if t == "boolean":
        return False
    return ""


class FakeRouter:
    """Turn 1: call read_file. Turn 2+: submit (optionally citing a bogus id first)."""

    def __init__(self, bogus_first=False, fail=None):
        self.bogus_first = bogus_first
        self.fail = fail
        self.turns = 0
        self.submissions = 0

    def complete(self, tier, *, instructions, input_items, tools, tool_choice, reasoning_effort,
                 max_output_tokens, on_call=None, context=None):
        if self.fail:
            raise self.fail
        self.turns += 1
        names = {t.name for t in tools}
        assert "submit_outcome" in names
        if self.turns == 1:
            item = {"type": "function_call", "call_id": "c1", "name": "read_file",
                    "arguments": json.dumps({"path": "microblog.py", "start_line": None,
                                             "end_line": None, "application_id": None})}
        else:
            blob = json.dumps(input_items)
            eids = re.findall(r'evidence id=\\"(ev-[0-9a-f]+)\\"', blob)
            submit = next(t for t in tools if t.name == "submit_outcome")
            args = minimal(submit.parameters)
            cite = ["ev-deadbeef0000"] if (self.bogus_first and self.submissions == 0) else eids[:1]
            args.update(status="COMPLETE", summary="ok", confidence="high",
                        findings=[{"statement": "app entrypoint is microblog.py",
                                   "evidence_class": "OBSERVED", "evidence_ids": cite,
                                   "limitations": None}])
            self.submissions += 1
            item = {"type": "function_call", "call_id": f"s{self.turns}", "name": "submit_outcome",
                    "arguments": json.dumps(args)}
        resp = ModelResponse(f"r{self.turns}", "fake-deploy", "fake", [item],
                             usage=Usage(input_tokens=10, output_tokens=5))
        if on_call:
            on_call({"deployment": "fake-deploy", "tokens": 15})
        return resp


def _runner(router, tmp_path):
    reg = resolve_registry()["phases"][1]
    base = P1AgentRunner(confirmed_stakeholder=True, use_analyzers=False)
    base.bind_repo(MICROBLOG)
    s = Settings(llm_mode="auto", astra_endpoint="https://x.invalid", astra_api_key="k" * 20)

    def env(ctx):
        return ToolEnv(application_id="microblog", phase=1, repo_root=MICROBLOG, store=None,
                       published=ctx.get("published", {}))
    return LLMAgentRunner(base, reg, router=router, gateway=build_gateway(), env_factory=env,
                          settings=s), reg


def _spec(reg, local):
    return next(a for a in reg["agents"] if a["local_id"] == local)


@needs_corpus
def test_agent_loop_enriches_with_cited_evidence(tmp_path):
    router = FakeRouter()
    runner, reg = _runner(router, tmp_path)
    events = []
    out = runner.run(_spec(reg, "A1"), {}, PolicyService(),
                     context={"emit": lambda k, **f: events.append(k), "published": {}})
    meta = out.execution_metadata["llm"]
    assert meta["enriched"] is True and meta["mode"] != "seed-fallback"
    assert meta["repairs"] == 0 and "read_file" in meta["tools_used"]
    llm_f = [f for f in out.findings if f.get("origin") == "llm"]
    assert llm_f and llm_f[0]["evidence_ids"] and llm_f[0]["evidence_ids"][0].startswith("ev-")
    assert {"TOOL_CALL", "MODEL_CALL"} <= set(events)


@needs_corpus
def test_unknown_citation_triggers_repair(tmp_path):
    router = FakeRouter(bogus_first=True)
    runner, reg = _runner(router, tmp_path)
    events = []
    out = runner.run(_spec(reg, "A1"), {}, PolicyService(),
                     context={"emit": lambda k, **f: events.append(k), "published": {}})
    assert out.execution_metadata["llm"]["enriched"] is True
    assert out.execution_metadata["llm"]["repairs"] >= 1
    assert "SUBMISSION_REJECTED" in events
    assert all("ev-deadbeef0000" not in (f.get("evidence_ids") or []) for f in out.findings)


@needs_corpus
def test_model_error_falls_back_to_seed(tmp_path):
    runner, reg = _runner(FakeRouter(fail=ContentFilteredError("blocked")), tmp_path)
    out = runner.run(_spec(reg, "A1"), {}, PolicyService(), context={"published": {}})
    meta = out.execution_metadata["llm"]
    assert meta["enriched"] is False and meta["mode"] == "seed-fallback"
    assert any(g.get("area") == "llm-enrichment" for g in out.gaps)
    assert out.status != "COMPLETE"


def test_evidence_enforcement_rules():
    o = AgentOutcome(status="COMPLETE", payload={"items": [{"evidence_class": "OBSERVED", "origin": "llm",
                                                            "evidence_ids": ["ev-x", "ev-unknown"]},
                                                           {"evidence_class": "OBSERVED",
                                                            "evidence_ids": []}]},
                     findings=[{"id": "L-1", "evidence_class": "OBSERVED", "evidence_ids": [],
                                "statement": "token=SUPERSECRET123 leaked", "origin": "llm"},
                               {"id": "L-2", "evidence_class": "HUMAN_CONFIRMED",
                                "evidence_ids": ["ev-x"], "statement": "owner said so", "origin": "llm"}],
                     gaps=[{"state": "NOT_ASSESSED", "requirement": "x"}])
    o.known_evidence = {"ev-x"}
    events = enforce(o, secrets=["SUPERSECRET123"])
    assert o.findings[0]["evidence_class"] == "INFERRED"                   # E1
    assert o.findings[1]["evidence_class"] == "HYPOTHETICAL"               # E2
    assert o.payload["items"][0]["evidence_ids"] == ["ev-x"]               # E3
    assert o.payload["items"][1]["evidence_class"] == "OBSERVED"           # seed items untouched
    assert o.status == "PARTIAL"                                           # E4
    assert "SUPERSECRET123" not in json.dumps(o.findings)                  # E5
    assert events


def test_gateway_sandbox(tmp_path):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("x")
    assert safe_path(tmp_path, "a.txt").name == "a.txt"
    for bad in ("../etc/passwd", ".git/config", "/../../x"):
        with pytest.raises(PermissionError):
            safe_path(tmp_path, bad)
    gw = build_gateway()
    env = ToolEnv(application_id="t", phase=1, repo_root=tmp_path, store=None, published={})
    sess = gw.session("P1.A1", ["read_file"], env, EvidenceLedger())
    text, eid = sess.call("read_file", {"path": "a.txt", "start_line": None, "end_line": None,
                                        "application_id": None})
    assert "hello" in text and eid.startswith("ev-") and 'trust="untrusted-data"' in text
    denied, _ = sess.call("grep", {"pattern": "x", "path": None, "glob": None, "application_id": None})
    assert "not allowlisted" in denied
    no_repo = gw.session("P2.A1", ["read_file", "list_artifacts"],
                         ToolEnv(application_id="t", phase=2, repo_root=None, store=None, published={}),
                         EvidenceLedger())
    assert "read_file" not in {t.name for t in no_repo.specs()}
