"""ask_stakeholder: blocking input, rate limits, digest reuse, P2.A1 / P3.A4 flows."""

from __future__ import annotations

import json
import re
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

from appmod.agents.runtime import AgentOutcome
from appmod.config import Settings
from appmod.kernel.audit import AuditJournal
from appmod.kernel.orchestrator import PhaseOrchestrator
from appmod.kernel.policy import PolicyService
from appmod.llm.types import ModelResponse, Usage
from appmod.phases import handoff as H
from appmod.phases.p1.engine import P1AgentRunner, P1_GATE_OVERRIDES
from appmod.phases.p2.engine import P2AgentRunner, P2_GATE_OVERRIDES
from appmod.phases.p3.engine import P3AgentRunner, P3_GATE_OVERRIDES
from appmod.registry.compiler import resolve_registry
from appmod.server.jobs import PipelineJob
from appmod.server.rundb import RunDB
from appmod.store.artifact_store import ArtifactStore
from appmod.tools.builtin import build_gateway
from appmod.tools.gateway import ToolEnv
from appmod.tools.stakeholder import AwaitingStakeholderInput, StakeholderBridge, ask_stakeholder

CORPUS = Path(__file__).resolve().parents[2] / "corpus"
MICROBLOG = CORPUS / "microblog"
needs_corpus = pytest.mark.skipif(not MICROBLOG.is_dir(), reason="corpus not cloned")


def _minimal(schema: dict) -> dict:
    t = schema.get("type")
    if isinstance(t, list):
        t = next(x for x in t if x != "null")
    if "enum" in schema:
        return schema["enum"][0]
    if t == "object":
        return {k: _minimal(v) for k, v in schema.get("properties", {}).items()}
    if t == "array":
        return []
    if t in ("integer", "number"):
        return 0
    if t == "boolean":
        return False
    return ""


class AskThenSubmitRouter:
    """First dispatch for target agents: blocking ask_stakeholder; after answer: submit."""

    def __init__(self, targets: dict[str, str], *, verdict: str = "ENTAILED"):
        self.targets = targets
        self.asked: set[str] = set()
        self.verdict = verdict
        self.calls = 0
        self.usage = Usage()
        self.failovers = 0
        self.cache = SimpleNamespace(hits=0)

    def complete(self, tier, *, instructions, input_items, tools, tool_choice,
                 reasoning_effort, max_output_tokens, on_call=None, context=None):
        names = {t.name for t in tools}
        if names == {"submit_verdicts"}:
            n = len(re.findall(r"^- c\d+:", input_items[0]["content"], re.M))
            args = {"verdicts": [{"claim": f"c{i}", "verdict": self.verdict, "reason": "ok"}
                                 for i in range(1, n + 1)]}
            return ModelResponse("v", "fake", "fake", [{
                "type": "function_call", "call_id": "v1", "name": "submit_verdicts",
                "arguments": json.dumps(args)}], usage=Usage())
        agent = (context or {}).get("agent", "")
        blob = json.dumps(input_items)
        if agent in self.targets and agent not in self.asked and "ask_stakeholder" in names:
            self.asked.add(agent)
            q = self.targets[agent]
            return ModelResponse("r1", "fake", "fake", [{
                "type": "function_call", "call_id": "ask1", "name": "ask_stakeholder",
                "arguments": json.dumps({
                    "question": q, "why": "unblocks scoring", "target_role": "owner",
                    "blocking": True,
                }),
            }], usage=Usage())
        submit = next(t for t in tools if t.name == "submit_outcome")
        args = _minimal(submit.parameters)
        eids = re.findall(r"human:(q-[0-9a-f]+)", blob)
        cite = [f"human:{eids[0]}"] if eids else []
        cls = "HUMAN_CONFIRMED" if cite else "INFERRED"
        args.update(status="COMPLETE", summary="done", confidence="high",
                    findings=[{"statement": "stakeholder input incorporated",
                               "evidence_class": cls, "evidence_ids": cite, "limitations": None}])
        return ModelResponse("r2", "fake", "fake", [{
            "type": "function_call", "call_id": "s1", "name": "submit_outcome",
            "arguments": json.dumps(args),
        }], usage=Usage())


def _quick_router():
    class R:
        calls = 0
        usage = Usage()
        failovers = 0
        cache = SimpleNamespace(hits=0)

        def complete(self, *a, **k):
            tools = k.get("tools") or []
            names = {t.name for t in tools}
            if names == {"submit_verdicts"}:
                return ModelResponse("v", "f", "f", [], usage=Usage())
            submit = next(t for t in tools if t.name == "submit_outcome")
            args = _minimal(submit.parameters)
            args.update(status="COMPLETE", summary="ok", confidence="high",
                        findings=[{"statement": "ok", "evidence_class": "INFERRED",
                                   "evidence_ids": [], "limitations": None}])
            return ModelResponse("r", "f", "f", [{
                "type": "function_call", "call_id": "c", "name": "submit_outcome",
                "arguments": json.dumps(args),
            }], usage=Usage())
    return R()


def _job_skeleton(tmp_path: Path, db: RunDB) -> PipelineJob:
    job = PipelineJob(repos=[str(MICROBLOG)], runs_root=tmp_path, llm=True,
                      review_mode="human", include_p5_p6=False, db=db)
    job.registry = resolve_registry()
    job.policy = PolicyService()
    job.work = tmp_path / "work"
    job.work.mkdir(parents=True, exist_ok=True)
    job.store = ArtifactStore(job.work / "store")
    job.audit = AuditJournal(job.work / "audit")
    job.repo_paths = {"microblog": MICROBLOG}
    job.state["apps"] = ["microblog"]
    job._gateway = build_gateway()
    job.settings = Settings(llm_mode="auto", astra_endpoint="https://x.invalid",
                            astra_api_key="k" * 20, verifier="off")
    job.llm = True
    return job


def _answer_open(db: RunDB, job_id: str, stop: threading.Event) -> None:
    while not stop.is_set():
        for q in db.list_questions(job_id, status="OPEN"):
            if q.get("blocking"):
                db.answer(q["question_id"], f"Answer to: {q['question'][:50]}", "scripted-stakeholder")
        for r in db.list_reviews(job_id, "PENDING"):
            db.decide(r["review_id"], "approve", "scripted-reviewer", "ok", r["candidate_hash"])
        time.sleep(0.15)


def test_dedup_per_node(tmp_path):
    db = RunDB(tmp_path / "db")
    a = db.add_question("j", "a", "Same?", phase=2, node="A1", blocking=True)
    b = db.add_question("j", "a", "Same?", phase=2, node="A2", blocking=True)
    c = db.add_question("j", "a", "Same?", phase=2, node="A1", blocking=True)
    assert a == c and a != b


def test_rate_limit_returns_error(tmp_path):
    db = RunDB(tmp_path / "db")
    bridge = StakeholderBridge(
        "j", 2, "a", "A1", "human",
        ensure=lambda **kw: db.add_question("j", "a", kw["question"], phase=2, node="A1",
                                            blocking=kw.get("blocking", False)),
        list_for_node=lambda: db.list_questions("j", "a"),
        count_open_blocking=lambda: db.count_questions("j", "a", open_blocking=True),
        count_total=lambda: db.count_questions("j", "a"),
        max_open_blocking=1, max_total=50,
    )
    env = ToolEnv(application_id="a", phase=2, stakeholder=bridge)
    with pytest.raises(AwaitingStakeholderInput):
        ask_stakeholder(env, {"question": "Q1?", "why": "w", "target_role": "o", "blocking": True})
    out = ask_stakeholder(env, {"question": "Q2?", "why": "w", "target_role": "o", "blocking": True})
    assert out.get("rate_limited") is True


def test_simulated_mode_blocking_does_not_raise(tmp_path):
    db = RunDB(tmp_path / "db")
    bridge = StakeholderBridge(
        "j", 2, "a", "A1", "simulated",
        ensure=lambda **kw: db.add_question("j", "a", kw["question"], phase=2, node="A1",
                                            blocking=True),
        list_for_node=lambda: db.list_questions("j", "a"),
        count_open_blocking=lambda: 0, count_total=lambda: 0,
        max_open_blocking=3, max_total=30,
    )
    env = ToolEnv(application_id="a", phase=2, stakeholder=bridge)
    out = ask_stakeholder(env, {"question": "Q?", "why": "w", "target_role": "o", "blocking": True})
    assert out.get("simulated") and "error" in out


def test_node_digest_changes_on_answer(tmp_path):
    db = RunDB(tmp_path / "db")
    q = db.add_question("j", "a", "Q?", phase=3, node="A4", blocking=True)
    assert db.node_answers_digest("j", 3, "a", "A4") == ""
    db.answer(q, "classified internal", "alice")
    assert db.node_answers_digest("j", 3, "a", "A4") != ""


def test_orchestrator_awaiting_input_parks_node(tmp_path):
    reg = resolve_registry()["phases"][2]

    class ParkA1:
        accepts_context = True

        def run(self, spec, inputs, policy, context=None):
            if spec["local_id"] == "A1":
                return AgentOutcome("PARTIAL", {}, awaiting_input={"question_id": "q-x",
                                                                   "question": "Q?"})
            return AgentOutcome("COMPLETE", {"ok": True})

        def fingerprint(self):
            return "mock"

    orch = PhaseOrchestrator(reg, ArtifactStore(tmp_path / "st"), PolicyService(),
                             AuditJournal(tmp_path / "aud"), ParkA1(),
                             gate_overrides=P2_GATE_OVERRIDES, max_parallel=1)
    ctx = orch.start_run("r1", H.PORTFOLIO_ID, {
        "scope_manifest": {"portfolio_id": H.PORTFOLIO_ID},
        "p1_packages": [{"application_id": "microblog", "schema_version": "P1.discovery.v3.0",
                           "g2_status": "READY_FOR_PORTFOLIO_DECISION", "manifest_hash": "x"}],
        "p1_scope": {"microblog": "READY_FOR_PORTFOLIO_DECISION"},
    })
    events = orch.run(ctx)
    assert ctx.state.nodes["A1"].status == "AWAITING_INPUT"
    assert ctx.state.nodes["A2"].status in ("PENDING", "BLOCKED", "FAILED")
    assert any(e.get("status") == "AWAITING_INPUT" for e in events)


def _scripted_humans(db: RunDB, job_id: str) -> tuple[threading.Event, threading.Thread]:
    stop = threading.Event()
    thread = threading.Thread(target=_answer_open, args=(db, job_id, stop), daemon=True)
    thread.start()
    return stop, thread


@needs_corpus
def test_p2_a1_blocking_question_human_mode(tmp_path):
    db = RunDB(tmp_path / "db")
    job = _job_skeleton(tmp_path, db)
    stop, _ = _scripted_humans(db, job.job_id)
    job._router = _quick_router()
    base = P1AgentRunner(confirmed_stakeholder=True, use_analyzers=False)
    base.bind_repo(MICROBLOG)
    job._run_phase(1, "microblog", base, {
        "scope_manifest": {"workload_ids": ["microblog"], "route": "derived-at-A5",
                           "boundaries": "user-supplied repo, read-only"},
        "source_pins": {"repo_path": str(MICROBLOG), "commit": base.scan.commit},
    }, P1_GATE_OVERRIDES)
    released = H.p1_release(job.store, "microblog")
    assert released["status"] != "HOLD"
    p2_apps = [H.portfolio_app(job.store, "microblog")]
    job._router = AskThenSubmitRouter({"P2.A1": "Who owns funding for microblog modernization?"})
    job._run_phase(2, H.PORTFOLIO_ID, P2AgentRunner(p2_apps), H.p2_run_inputs(job.store, ["microblog"]),
                   P2_GATE_OVERRIDES)
    stop.set()
    qs = [q for q in db.list_questions(job.job_id) if q.get("node") == "A1" and q.get("phase") == 2]
    assert qs and qs[0]["status"] == "ANSWERED"
    a1 = job.store.get(f"P2/{H.PORTFOLIO_ID}/A1")
    llm_f = [f for f in a1["findings"] if f.get("origin") == "llm"]
    assert llm_f and any(f.get("evidence_class") == "HUMAN_CONFIRMED" for f in llm_f)
    assert any(eid.startswith("human:q-") for f in llm_f for eid in f.get("evidence_ids", []))


@needs_corpus
def test_p3_a4_blocking_question_human_mode(tmp_path):
    db = RunDB(tmp_path / "db")
    job = _job_skeleton(tmp_path, db)
    stop, _ = _scripted_humans(db, job.job_id)
    job._router = _quick_router()
    base = P1AgentRunner(confirmed_stakeholder=True, use_analyzers=False)
    base.bind_repo(MICROBLOG)
    job._run_phase(1, "microblog", base, {
        "scope_manifest": {"workload_ids": ["microblog"], "route": "derived-at-A5",
                           "boundaries": "user-supplied repo, read-only"},
        "source_pins": {"repo_path": str(MICROBLOG), "commit": base.scan.commit},
    }, P1_GATE_OVERRIDES)
    p2_apps = [H.portfolio_app(job.store, "microblog")]
    job._router = _quick_router()
    job._run_phase(2, H.PORTFOLIO_ID, P2AgentRunner(p2_apps), H.p2_run_inputs(job.store, ["microblog"]),
                   P2_GATE_OVERRIDES)
    job._router = AskThenSubmitRouter({"P3.A4": "What data classification applies to user posts?"})
    job._run_phase(3, "microblog", P3AgentRunner(H.design_brief(job.store, "microblog")),
                   H.p3_run_inputs(job.store, "microblog"), P3_GATE_OVERRIDES)
    stop.set()
    qs = [q for q in db.list_questions(job.job_id) if q.get("node") == "A4" and q.get("phase") == 3]
    assert qs and qs[0]["status"] == "ANSWERED"
    a4 = job.store.get("P3/microblog/A4")
    llm_f = [f for f in a4["findings"] if f.get("origin") == "llm"]
    assert llm_f and any(f.get("evidence_class") == "HUMAN_CONFIRMED" for f in llm_f)


@needs_corpus
def test_reuse_after_node_answer_only_reruns_target(tmp_path):
    db = RunDB(tmp_path / "db")
    job = _job_skeleton(tmp_path, db)
    stop, _ = _scripted_humans(db, job.job_id)
    job._router = _quick_router()
    base = P1AgentRunner(confirmed_stakeholder=True, use_analyzers=False)
    base.bind_repo(MICROBLOG)
    job._run_phase(1, "microblog", base, {
        "scope_manifest": {"workload_ids": ["microblog"], "route": "derived-at-A5",
                           "boundaries": "user-supplied repo, read-only"},
        "source_pins": {"repo_path": str(MICROBLOG), "commit": base.scan.commit},
    }, P1_GATE_OVERRIDES)
    p2_apps = [H.portfolio_app(job.store, "microblog")]
    job._router = AskThenSubmitRouter({"P2.A1": "Who is the business owner?"})
    job._run_phase(2, H.PORTFOLIO_ID, P2AgentRunner(p2_apps), H.p2_run_inputs(job.store, ["microblog"]),
                   P2_GATE_OVERRIDES)
    stop.set()
    v_a1 = len(job.store.versions(f"P2/{H.PORTFOLIO_ID}/A1"))
    v_a2 = len(job.store.versions(f"P2/{H.PORTFOLIO_ID}/A2"))
    job.force[(2, H.PORTFOLIO_ID)] = set()
    job._run_phase(2, H.PORTFOLIO_ID, P2AgentRunner(p2_apps), H.p2_run_inputs(job.store, ["microblog"]),
                   P2_GATE_OVERRIDES)
    assert len(job.store.versions(f"P2/{H.PORTFOLIO_ID}/A1")) == v_a1
    assert len(job.store.versions(f"P2/{H.PORTFOLIO_ID}/A2")) == v_a2
