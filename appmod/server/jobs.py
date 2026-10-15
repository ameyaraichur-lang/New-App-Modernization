"""Pipeline jobs: one or many repositories through P1–P4 (P5/P6 for single-app).

Flow
  P1 Discovery     per application (parallel across apps)
  P2 Portfolio     once, over every application P1 released
  P3 Architecture  per application P2 AUTHORIZED (parallel)
  P4 Planning      per application P3 released (parallel)
  P5/P6            single-application jobs only (deterministic engines)

Agents in P1–P4 run through the Astra agent loop (LLMAgentRunner) when the
LLM is configured. Every phase run uses reuse-by-input-hash, so approvals,
recorded stakeholder answers, resume-after-restart and targeted re-runs only
recompute what actually changed.

review_mode=human: P1–P4 release gates pause in AWAITING_REVIEW until a
reviewer decides through the approvals API (bound to the candidate hash);
P1.A8 confirmations come only from answers recorded via the questions API.
Any P1–P4 agent may call ``ask_stakeholder``; blocking questions park the node in
``AWAITING_INPUT`` until the questions API records an answer (per-node input hash).
"""

from __future__ import annotations

import re
import subprocess
import threading
import time
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from appmod.config import Settings, get_settings
from appmod.kernel.audit import AuditJournal
from appmod.kernel.gates import gate_impl_for
from appmod.kernel.orchestrator import PhaseOrchestrator
from appmod.kernel.policy import PolicyService
from appmod.kernel.assurance import with_assurance
from appmod.kernel.reviews import with_human_review
from appmod.phases import handoff as H
from appmod.phases.p1.engine import P1_GATE_OVERRIDES, P1AgentRunner
from appmod.phases.p2.engine import P2_GATE_OVERRIDES, P2AgentRunner
from appmod.phases.p3.engine import P3_GATE_OVERRIDES, P3AgentRunner
from appmod.phases.p4.engine import P4_GATE_OVERRIDES, P4AgentRunner
from appmod.phases.p5.engine import P5_GATE_OVERRIDES, P5AgentRunner
from appmod.phases.p6.engine import P6_GATE_OVERRIDES, P6AgentRunner
from appmod.registry.compiler import resolve_registry
from appmod.server.rundb import RunDB
from appmod.server.runner import _build_fixture, _find_seed_sql, json_copy
from appmod.store.artifact_store import ArtifactStore
from appmod.tools.gateway import ToolEnv
from appmod.tools.stakeholder import StakeholderBridge

PHASE_NAME = {1: "Discovery", 2: "Portfolio decision", 3: "Target architecture",
              4: "Planning", 5: "Code modernization", 6: "Data modernization"}
GATE_OF = {1: "G2", 2: "G2", 3: "G2", 4: "G2", 5: "G4", 6: "G3"}
TERMINAL_NODE = {"PUBLISHED", "COMPLETE", "PARTIAL", "FAILED", "BLOCKED", "SKIPPED_APPROVED",
                 "NOT_ASSESSED"}
TRACE_KINDS = ("MODEL_CALL", "TOOL_CALL", "AGENT_LLM_DONE", "SUBMISSION_REJECTED", "VERIFIER")


class Cancelled(Exception):
    pass


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def validate_repo_input(repo: str, settings: Settings | None = None) -> None:
    """Hardening: local paths must sit under an allowlisted root (when set);
    URLs must use https/ssh on an allowlisted git host."""
    s = settings or get_settings()
    repo = repo.strip()
    if re.match(r"^(https?://|git@)", repo):
        host = (urlparse(repo).hostname if repo.startswith("http")
                else repo.split("@", 1)[1].split(":", 1)[0])
        allowed = [h.strip().lower() for h in s.git_hosts.split(",") if h.strip()]
        if repo.startswith("http://"):
            raise ValueError("plain http git URLs are not allowed; use https")
        if allowed and (host or "").lower() not in allowed:
            raise ValueError(f"git host {host!r} not in allowlist {allowed}")
        return
    p = Path(repo).expanduser().resolve()
    if not p.is_dir():
        raise ValueError(f"repo not found and not a git URL: {repo}")
    roots = [Path(r).expanduser().resolve() for r in s.repo_roots.split(":") if r.strip()]
    if roots and not any(p == r or r in p.parents for r in roots):
        raise ValueError("local path outside the allowed repository roots")


class PipelineJob:
    def __init__(self, repo: str | None = None, *, repos: list[str] | None = None,
                 decision_mode: bool = True, include_p6: bool = True, include_p5_p6: bool | None = None,
                 app_id: str | None = None, runs_root: Path | None = None, owner: str = "local",
                 review_mode: str | None = None, llm: bool | None = None, job_id: str | None = None,
                 db: RunDB | None = None, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.repos = [r.strip() for r in (repos or ([repo] if repo else [])) if r and r.strip()]
        if not self.repos:
            raise ValueError("at least one repository is required")
        self.job_id = job_id or f"job-{int(time.time())}-{uuid.uuid4().hex[:6]}"
        self.repo_input = self.repos[0] if len(self.repos) == 1 else ", ".join(self.repos)
        self.decision_mode = decision_mode
        self.include_p6 = include_p6
        self.single = len(self.repos) == 1
        self.include_p5_p6 = self.single if include_p5_p6 is None else (include_p5_p6 and self.single)
        self.app_id = app_id
        self.owner = owner
        self.review_mode = review_mode or self.settings.review_mode
        self.llm = self.settings.llm_enabled if llm is None else (llm and self.settings.llm_enabled)
        self.runs_root = runs_root or self.settings.runs_dir
        self.db = db or RunDB(self.runs_root / "appmod.db")
        self.work = self.runs_root / "ui" / self.job_id
        self.force: dict[tuple[int, str], set[str]] = {}
        self._detail_before_outage: str | None = None
        self.spec = {"repos": self.repos, "decision_mode": decision_mode, "include_p6": include_p6,
                     "include_p5_p6": self.include_p5_p6, "app_id": app_id, "owner": owner,
                     "review_mode": self.review_mode, "llm": self.llm}
        self.state: dict[str, Any] = {
            "job_id": self.job_id, "repo": self.repo_input, "repos": self.repos, "apps": [],
            "app_id": None, "owner": owner, "status": "PENDING", "stage": "QUEUED",
            "stage_detail": None, "current_phase": None, "progress": 0, "log": [],
            "started_at": None, "finished_at": None, "error": None, "phases": [],
            "gate_chain": [], "facts": {}, "app_facts": {}, "review_mode": self.review_mode,
            "llm": {"enabled": self.llm, "calls": 0, "input_tokens": 0, "output_tokens": 0,
                    "reasoning_tokens": 0, "failovers": 0, "cached": 0, "tool_calls": 0},
            "pending_reviews": 0, "open_questions": 0,
        }
        self._lock = threading.RLock()
        self._cancel = threading.Event()
        self.thread: threading.Thread | None = None
        self._last_persist = 0.0
        self._router = None
        self._gateway = None
        self._llm_base: dict[str, float] = {}

    # -- construction from the DB (resume after restart) -----------------------------

    @classmethod
    def from_db(cls, row: dict[str, Any], db: RunDB, runs_root: Path | None = None) -> "PipelineJob":
        spec = row["spec"]
        job = cls(repos=spec["repos"], decision_mode=spec.get("decision_mode", True),
                  include_p6=spec.get("include_p6", True), include_p5_p6=spec.get("include_p5_p6"),
                  app_id=spec.get("app_id"), owner=spec.get("owner", "local"),
                  review_mode=spec.get("review_mode"), llm=spec.get("llm"), job_id=row["job_id"],
                  db=db, runs_root=runs_root)
        job.state.update({k: v for k, v in row["state"].items() if k in job.state})
        job._llm_base = {k: v for k, v in job.state["llm"].items() if isinstance(v, (int, float))
                         and not isinstance(v, bool)}
        return job

    # -- state helpers ------------------------------------------------------------------

    def _update(self, **fields: Any) -> None:
        with self._lock:
            self.state.update(fields)
        self._persist(force="status" in fields)

    def _persist(self, force: bool = False) -> None:
        now = time.time()
        if not force and now - self._last_persist < 2.0:
            return
        self._last_persist = now
        try:
            self.db.save_job(self.job_id, self.owner, self.state["status"], self.spec, self.snapshot())
        except Exception:
            pass

    def _event(self, kind: str, **data: Any) -> None:
        try:
            self.db.add_event(self.job_id, kind, data)
        except Exception:
            pass

    def _log(self, msg: str, level: str = "info") -> None:
        with self._lock:
            self.state["log"].append({"ts": _now(), "msg": msg, "level": level})
            if len(self.state["log"]) > 800:
                del self.state["log"][:200]
        self._event("LOG", msg=msg, level=level)
        self._persist()

    def _phase(self, phase: int, app: str) -> dict[str, Any]:
        with self._lock:
            for p in self.state["phases"]:
                if p["phase"] == phase and p.get("app") == app:
                    return p
            p = {"phase": phase, "app": app, "status": "PENDING", "nodes": [], "decision": None,
                 "note": ""}
            self.state["phases"].append(p)
            return p

    def _expected_entries(self) -> int:
        n = max(1, len(self.state["apps"]) or len(self.repos))
        total = n * 3 + 1
        if self.include_p5_p6:
            total += 1 + (1 if self.include_p6 else 0)
        return total

    def _recompute_progress(self) -> None:
        with self._lock:
            done, frac = 0.0, 0.0
            for p in self.state["phases"]:
                if p["status"] in ("COMPLETED", "N/A", "SKIPPED", "FAILED", "NOT_ADMITTED"):
                    done += 1
                elif p["status"] in ("RUNNING", "AWAITING_REVIEW", "AWAITING_INPUT") and p["nodes"]:
                    frac += sum(1 for n in p["nodes"] if n["status"] in TERMINAL_NODE) / len(p["nodes"])
            self.state["progress"] = round(100 * min(1.0, (done + frac) / self._expected_entries()))

    def _gate(self, phase: int, app: str, decision: str) -> None:
        with self._lock:
            self.state["gate_chain"].append({"phase": phase, "app": app, "gate": GATE_OF[phase],
                                             "decision": decision})
            self._phase(phase, app)["decision"] = decision
        self._log(f"P{phase} {app} release gate {GATE_OF[phase]} → {decision}", level="gate")

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            snap = json_copy(self.state)
        try:
            snap["pending_reviews"] = len(self.db.list_reviews(self.job_id, "PENDING"))
            snap["open_questions"] = len(self.db.list_questions(self.job_id, status="OPEN"))
        except Exception:
            pass
        return snap

    # -- lifecycle ------------------------------------------------------------------------

    def start(self) -> None:
        if self.thread is not None and self.thread.is_alive():
            raise RuntimeError("job already running")
        self._cancel.clear()
        self.thread = threading.Thread(target=self._execute, daemon=True, name=self.job_id)
        self.thread.start()

    def cancel(self) -> None:
        self._cancel.set()
        self._log("cancellation requested", level="error")

    def rerun(self, phase: int, app: str, nodes: list[str]) -> None:
        self.force[(phase, app)] = set(nodes)
        self.start()

    @property
    def running(self) -> bool:
        return self.thread is not None and self.thread.is_alive()

    def _execute(self) -> None:
        try:
            self._update(status="RUNNING", started_at=self.state["started_at"] or _now(),
                         finished_at=None, error=None)
            self._log(f"job {self.job_id} accepted — {len(self.repos)} repo(s); review_mode="
                      f"{self.review_mode}; llm={'astra' if self.llm else 'off'}")
            self._run_all()
            with self._lock:
                self.state["progress"] = 100
            self._update(status="COMPLETED", finished_at=_now(), stage="DONE", stage_detail="completed")
            self._log("pipeline run COMPLETED — outcome bundle ready for download")
        except Cancelled:
            self._update(status="CANCELLED", finished_at=_now(), stage="DONE", stage_detail="cancelled")
            self._log("job CANCELLED", level="error")
        except Exception as exc:
            tail = traceback.format_exc().strip().splitlines()[-1]
            self._update(status="FAILED", error=f"{type(exc).__name__}: {exc}", finished_at=_now(),
                         stage="DONE", stage_detail="failed")
            self._log(f"job FAILED: {type(exc).__name__}: {exc}", level="error")
            self._log(f"cause: {tail}", level="error")
        finally:
            self.force.clear()
            self._sync_llm()
            self._persist(force=True)
            self._event("JOB", status=self.state["status"])

    # -- shared services ----------------------------------------------------------------

    @property
    def router(self):
        if self._router is None and self.llm:
            from appmod.llm.router import ModelRouter
            self._router = ModelRouter(self.settings)
            if self._router.outage is not None:
                self._router.outage.on_change = self._on_outage
                self._router.outage.stop = self._cancel
        return self._router

    def _on_outage(self, status: str, info: dict[str, Any]) -> None:
        self._event("CONNECTIVITY", status=status, **info)
        if status == "LOST":
            with self._lock:
                self._detail_before_outage = self.state.get("stage_detail")
            self._update(stage_detail="paused — Astra unreachable, waiting for it to answer")
            self._log("Astra endpoint unreachable — model work paused; agent retries are not spent", level="error")
        elif status == "RESTORED":
            self._update(stage_detail=self._detail_before_outage)
            self._log(f"Astra reachable again after {info.get('waited_s', 0)} s — model work resumed")
        else:
            self._log(f"stopped waiting for Astra ({info.get('reason')}) — affected agents fail normally",
                      level="error")

    @property
    def gateway(self):
        if self._gateway is None:
            from appmod.tools.builtin import build_gateway
            self._gateway = build_gateway()
            try:
                from appmod.tools.mcp_client import register_mcp_tools
                self._mcp_tools = register_mcp_tools(self._gateway)
            except Exception as exc:
                self._mcp_tools = []
                self._log(f"MCP tools unavailable: {exc}", level="error")
        return self._gateway

    def _sync_llm(self) -> None:
        r = self._router
        if r is None:
            return
        b = self._llm_base
        with self._lock:
            self.state["llm"].update(calls=b.get("calls", 0) + r.calls,
                                     input_tokens=b.get("input_tokens", 0) + r.usage.input_tokens,
                                     output_tokens=b.get("output_tokens", 0) + r.usage.output_tokens,
                                     reasoning_tokens=b.get("reasoning_tokens", 0) + r.usage.reasoning_tokens,
                                     failovers=b.get("failovers", 0) + r.failovers,
                                     cached=b.get("cached", 0) + r.cache.hits)

    # -- repos ----------------------------------------------------------------------------

    def _resolve_repo(self, repo_input: str, taken: set[str]) -> tuple[Path, str]:
        validate_repo_input(repo_input, self.settings)
        incoming = self.runs_root / "incoming"
        incoming.mkdir(parents=True, exist_ok=True)
        if re.match(r"^(https?://|git@)", repo_input):
            name = re.sub(r"[^A-Za-z0-9._-]+", "-",
                          repo_input.rstrip("/").split("/")[-1].removesuffix(".git"))
            target = incoming / f"{self.job_id}-{name}"
            if not target.exists():
                self._update(stage="CLONING", stage_detail=repo_input)
                self._log(f"cloning {repo_input} (shallow)…")
                env = {**__import__("os").environ, "GIT_TERMINAL_PROMPT": "0"}
                proc = subprocess.run(["git", "-c", "core.longpaths=true", "clone", "--depth", "1",
                                       "--single-branch", repo_input, str(target)],
                                      capture_output=True, text=True, timeout=1800, env=env)
                if proc.returncode != 0:
                    tail = (proc.stderr or "").strip().splitlines()[-3:]
                    raise RuntimeError(f"git clone failed: {' | '.join(tail) or proc.returncode}")
            path = target
        else:
            path = Path(repo_input).expanduser().resolve()
            name = path.name
        app = (self.app_id if self.single and self.app_id else name)
        base, i = app, 2
        while app in taken:
            app, i = f"{base}-{i}", i + 1
        taken.add(app)
        return path, app

    # -- phase execution --------------------------------------------------------------------

    def _external_digest(self, phase: int, app: str, node: str) -> str:
        if self.review_mode != "human":
            return ""
        if phase == 1 and node in ("A8", "G1", "G2"):
            return self.db.answers_digest(self.job_id, app)
        return self.db.node_answers_digest(self.job_id, phase, app, node)

    def _stakeholder_bridge(self, phase: int, app: str, node: str) -> StakeholderBridge:
        db, job_id = self.db, self.job_id
        s = self.settings

        def ensure(**kw: Any) -> str:
            return db.add_question(
                job_id, app, kw["question"], kw.get("why", ""), kw.get("target_role", ""),
                kw.get("source", "ask_stakeholder"), phase=phase, node=node,
                blocking=bool(kw.get("blocking")),
            )

        def list_for_node() -> list[dict[str, Any]]:
            return [q for q in db.list_questions(job_id, app)
                    if q.get("phase") == phase and q.get("node") == node]

        return StakeholderBridge(
            job_id, phase, app, node, self.review_mode, ensure=ensure, list_for_node=list_for_node,
            count_open_blocking=lambda: db.count_questions(job_id, app, open_blocking=True),
            count_total=lambda: db.count_questions(job_id, app),
            max_open_blocking=s.stakeholder_max_open_blocking,
            max_total=s.stakeholder_max_questions,
            on_pending=lambda p: self._event("QUESTION_PENDING", **p),
        )

    def _env_factory(self, phase: int, app: str):
        def make(context: dict[str, Any]) -> ToolEnv:
            portfolio = phase == 2
            env = ToolEnv(application_id=app, phase=phase,
                          repo_root=None if portfolio else self.repo_paths.get(app),
                          store=self.store, published=context.get("published", {}),
                          portfolio_apps=list(self.repo_paths) if portfolio else [],
                          repo_roots=dict(self.repo_paths) if portfolio else {},
                          retrieval_budget_chars=self.settings.retrieval_budget_chars)
            if phase <= 4:
                env.stakeholder = self._stakeholder_bridge(phase, app, context.get("node", ""))
            return env
        return make

    def _trace(self, phase: int, app: str, ev: dict[str, Any]) -> None:
        kind = ev.get("kind")
        if kind not in TRACE_KINDS:
            return
        slim = {k: v for k, v in ev.items() if k not in ("args", "kind", "app")}
        if kind == "TOOL_CALL":
            slim["args"] = {k: (str(v)[:160] if v is not None else None)
                            for k, v in (ev.get("args") or {}).items()}
            with self._lock:
                self.state["llm"]["tool_calls"] += 1
        self._event(kind, app=app, **slim)
        if kind == "MODEL_CALL":
            self._sync_llm()

    def _review_pending(self, r: dict[str, Any]) -> None:
        self._event("REVIEW_PENDING", **r)
        self._log(f"P{r['phase']} {r['app']} G2 awaiting human review {r['review_id']} "
                  f"(proposed {r['proposed_status']})", level="gate")

    def _run_phase(self, phase: int, app: str, base: Any, run_inputs: dict[str, Any],
                   overrides: dict[str, Any], na_ok: bool = False) -> Any:
        from appmod.agents.llm_runner import LLMAgentRunner
        if self._cancel.is_set():
            raise Cancelled()
        reg = self.registry["phases"][phase]
        runner = base
        if self.llm and phase <= 4:
            runner = LLMAgentRunner(base, reg, router=self.router, gateway=self.gateway,
                                    env_factory=self._env_factory(phase, app), settings=self.settings,
                                    extra_tools=lambda: list(getattr(self, "_mcp_tools", [])))
        overrides = dict(overrides)
        if phase <= 4:
            human = self.review_mode == "human"
            overrides["G2"] = with_assurance(overrides.get("G2") or gate_impl_for("G2"), human_review=human)
        if self.review_mode == "human" and phase <= 4:
            g2 = overrides["G2"]
            overrides["G2"] = with_human_review(
                g2, self.db, self.job_id, phase, "G2", audit=self.audit,
                on_pending=self._review_pending)
        pstate = self._phase(phase, app)
        pstate["status"] = "RUNNING"
        kinds = {a["local_id"]: a.get("kind", "agent") for a in reg["agents"]}
        with self._lock:
            self.state["current_phase"] = phase
            self.state["stage"] = "RUNNING"
            self.state["stage_detail"] = f"Phase {phase} — {PHASE_NAME[phase]} ({app})"
        self._log(f"Phase {phase} ({PHASE_NAME[phase]}) started for {app}")
        self._event("PHASE", phase=phase, app=app, status="RUNNING")

        def on_event(ctx, ev):
            node = ev.get("node", "?")
            if phase == 1 and node == "A8":
                # questions must be visible before G2 can raise a review on the draft-scope candidate
                self._register_questions(app, ctx)
            with self._lock:
                for n in pstate["nodes"]:
                    if n["id"] == node:
                        n["status"] = ev.get("status", n["status"])
                        n["reused"] = bool(ev.get("reused"))
                        break
                else:
                    pstate["nodes"].append({"id": node, "status": ev.get("status", "?")})
            msg = f"P{phase} {app} {node} → {ev.get('status', '?')}" + (" (reused)" if ev.get("reused") else "")
            if ev.get("gate_outcome"):
                msg += f" ({ev['gate_outcome']}" + (
                    f": {', '.join(str(r) for r in ev['reasons'][:2])}" if ev.get("reasons") else "") + ")"
            if ev.get("status") == "AWAITING_INPUT" and ev.get("question"):
                msg += f" — awaiting stakeholder: {str(ev['question'])[:80]}"
            by_design = na_ok and node == "G0" and ev.get("status") == "FAILED"
            if by_design:
                msg += " — expected on the approved no-data route"
            level = ("error" if ev.get("status") in ("FAILED", "BLOCKED") and not by_design
                     else "gate" if kinds.get(node) in ("gate", "execution") else "info")
            self._log(msg, level=level)
            self._event("NODE", phase=phase, app=app, node=node, status=ev.get("status"),
                        reused=bool(ev.get("reused")), gate_outcome=ev.get("gate_outcome"))
            self._recompute_progress()

        while True:
            digest_before = self.db.answers_digest(self.job_id, app) if phase == 1 else ""
            orch = PhaseOrchestrator(
                reg, self.store, self.policy, self.audit, runner, gate_overrides=overrides,
                max_parallel=self.settings.max_parallel_agents, reuse=True,
                external_digest=lambda node: self._external_digest(phase, app, node),
                force_nodes=self.force.pop((phase, app), set()), cancel_event=self._cancel)
            orch.event_listener = lambda ev: self._trace(phase, app, ev)
            ctx = orch.start_run(f"{self.job_id}-p{phase}-{app}", app, run_inputs)
            with self._lock:
                pstate["nodes"] = [{"id": nid, "status": ns.status}
                                   for nid, ns in sorted(ctx.state.nodes.items())]
            orch.run(ctx, on_event=on_event)
            with self._lock:
                pstate["nodes"] = [{"id": nid, "status": ns.status,
                                    "reused": any(e.get("reused") for e in ctx.outcome_log if e["node"] == nid)}
                                   for nid, ns in sorted(ctx.state.nodes.items())]
            if phase == 1:
                self._register_questions(app, ctx)
            if self._cancel.is_set():
                raise Cancelled()
            awaiting = [n for n, s in ctx.state.nodes.items() if s.status == "AWAITING_REVIEW"]
            awaiting_input = [n for n, s in ctx.state.nodes.items() if s.status == "AWAITING_INPUT"]
            if phase == 1 and self.db.answers_digest(self.job_id, app) != digest_before:
                self._log(f"P1 {app}: new stakeholder answers recorded — re-running affected nodes")
                continue
            if awaiting_input:
                pstate["status"] = "AWAITING_INPUT"
                self._update(status="AWAITING_INPUT")
                self._wait_for_input(phase, app, awaiting_input)
                self._log(f"P{phase} {app}: stakeholder answer recorded — re-running "
                          f"{', '.join(awaiting_input)}")
                pstate["status"] = "RUNNING"
                self._update(status="RUNNING")
                continue
            if not awaiting:
                break
            pstate["status"] = "AWAITING_REVIEW"
            self._update(status="AWAITING_REVIEW")
            self._wait_for_review(phase, app, digest_before)
            pstate["status"] = "RUNNING"
            self._update(status="RUNNING")

        failed = [e["node"] for e in ctx.outcome_log if e["status"] == "FAILED"]
        if failed and not na_ok:
            pstate["status"] = "FAILED"
            pstate["note"] = f"failed nodes: {failed}"
            self._log(f"Phase {phase} {app} FAILED — nodes: {failed}", level="error")
        else:
            pstate["status"] = "N/A" if pstate["status"] == "N/A" else "COMPLETED"
            self._log(f"Phase {phase} {app} {pstate['status']} ({len(pstate['nodes'])} nodes)")
        self._event("PHASE", phase=phase, app=app, status=pstate["status"])
        self._recompute_progress()
        self._sync_llm()
        return ctx

    def _wait_for_review(self, phase: int, app: str, answers_digest: str) -> None:
        while not self._cancel.is_set():
            pending = [r for r in self.db.list_reviews(self.job_id, "PENDING")
                       if r["phase"] == phase and r["app"] == app]
            if not pending:
                return            # decided (or superseded) -> re-enter the gate
            if phase == 1 and self.db.answers_digest(self.job_id, app) != answers_digest:
                return
            time.sleep(1.5)
        raise Cancelled()

    def _wait_for_input(self, phase: int, app: str, nodes: list[str]) -> None:
        while not self._cancel.is_set():
            open_q = [q for q in self.db.list_questions(self.job_id, app, status="OPEN")
                      if q.get("phase") == phase and q.get("node") in nodes and q.get("blocking")]
            if not open_q:
                return
            time.sleep(1.5)
        raise Cancelled()

    def _register_questions(self, app: str, ctx: Any) -> None:
        a8 = ctx.inputs_by_node.get("A8")
        if not a8 or a8.get("status") == "FAILED":
            return
        p = a8.get("payload", {})
        qs = p.get("questions", [])
        if isinstance(qs, str):
            qs = []
        for q in qs:
            if isinstance(q, str) and q.strip():
                self.db.add_question(self.job_id, app, q.strip(), source="seed", phase=1, node="A8")
        # one elicitation round: drafts from later A8 re-runs stay in the artifact but do not
        # reopen the questionnaire, otherwise every answer would spawn new questions forever
        if any(q["source"] == "llm-drafted" for q in self.db.list_questions(self.job_id, app)):
            return
        for d in p.get("questions_drafted", []) or []:
            if isinstance(d, dict) and d.get("question"):
                self.db.add_question(self.job_id, app, d["question"].strip(), why=d.get("why", ""),
                                     target_role=d.get("target_role", ""), source="llm-drafted",
                                     phase=1, node="A8")

    # -- the pipeline ----------------------------------------------------------------------------

    def _run_all(self) -> None:
        self.registry = resolve_registry()
        self.policy = PolicyService()
        self.work.mkdir(parents=True, exist_ok=True)
        self.store = ArtifactStore(self.work / "store")
        self.audit = AuditJournal(self.work / "audit")
        with self._lock:
            self.state["facts"]["store_path"] = str(self.work / "store")

        taken: set[str] = set()
        self.repo_paths: dict[str, Path] = {}
        for r in self.repos:
            path, app = self._resolve_repo(r, taken)
            self.repo_paths[app] = path
        apps = list(self.repo_paths)
        self._update(apps=apps, app_id=apps[0])
        _ = self.gateway

        # ---------------- P1 per app (parallel) -------------------------------------------
        def p1(app: str) -> str | None:
            base = P1AgentRunner(confirmed_stakeholder=self.decision_mode and self.review_mode != "human")
            base.bind_repo(self.repo_paths[app])
            if self.review_mode == "human":
                base.answers_provider = lambda a=app: self.db.list_questions(self.job_id, a)
            self._run_phase(1, app, base, {
                "scope_manifest": {"workload_ids": [app], "route": "derived-at-A5",
                                   "boundaries": "user-supplied repo, read-only"},
                "source_pins": {"repo_path": str(self.repo_paths[app]), "commit": base.scan.commit},
            }, P1_GATE_OVERRIDES)
            try:
                rec = H.p1_release(self.store, app)
            except Exception:
                return None
            self._gate(1, app, rec["status"])
            a1 = self.store.get(f"P1/{app}/A1")["payload"]
            a5 = self.store.get(f"P1/{app}/A5")["payload"]
            r0 = a1["repositories"][0]
            facts = {"loc": r0.get("loc", 0), "code_loc": r0.get("code_loc"), "files": r0.get("files", 0),
                     "primary_language": r0.get("primary_language"), "route": a5["capability_route"],
                     "dependencies": len(a1["dependencies"]), "p1_release": rec["status"]}
            with self._lock:
                self.state["app_facts"][app] = facts
                if self.single:
                    self.state["facts"].update(facts)
            return None if rec["status"] == "HOLD" else app

        with ThreadPoolExecutor(max_workers=max(1, min(self.settings.max_parallel_apps, len(apps)))) as ex:
            released = [a for a in ex.map(p1, apps) if a]
        if self._cancel.is_set():
            raise Cancelled()
        if not released:
            raise RuntimeError("no application released by P1 — downstream phases not admitted")

        # ---------------- P2 portfolio -------------------------------------------------------
        p2_apps = [H.portfolio_app(self.store, a) for a in released]
        self._run_phase(2, H.PORTFOLIO_ID, P2AgentRunner(p2_apps), H.p2_run_inputs(self.store, released),
                        P2_GATE_OVERRIDES)
        g2 = H.p2_release(self.store)
        self._gate(2, H.PORTFOLIO_ID, g2["status"])
        authorized = [a for a in released if a in g2.get("authorized_apps", [])]
        for a in released:
            with self._lock:
                self.state["app_facts"].setdefault(a, {})["disposition"] = H.disposition(self.store, a)
                self.state["app_facts"][a]["authorized"] = a in authorized
            self._log(f"portfolio decision: {a} → {H.disposition(self.store, a)}"
                      + ("" if a in authorized else " (not authorized for design)"))
            if a not in authorized:
                for ph in (3, 4):
                    e = self._phase(ph, a)
                    e["status"], e["note"] = "NOT_ADMITTED", "P2 did not authorize this application"
        if self.single:
            self.state["facts"]["disposition"] = H.disposition(self.store, apps[0])
        if not authorized:
            raise RuntimeError(f"P2 authorized no application (status={g2['status']})")

        # ---------------- P3 + P4 per authorized app (parallel) ----------------------------------
        def p34(app: str) -> str | None:
            self._run_phase(3, app, P3AgentRunner(H.design_brief(self.store, app)),
                            H.p3_run_inputs(self.store, app), P3_GATE_OVERRIDES)
            try:
                g3 = H.p3_release(self.store, app)
            except Exception:
                return None
            self._gate(3, app, g3["status"])
            self._run_phase(4, app, P4AgentRunner(H.plan_brief(self.store, app)),
                            H.p4_run_inputs(self.store, app), P4_GATE_OVERRIDES)
            try:
                g4 = H.p4_release(self.store, app)
            except Exception:
                return None
            self._gate(4, app, g4["status"])
            return app

        with ThreadPoolExecutor(max_workers=max(1, min(self.settings.max_parallel_apps, len(authorized)))) as ex:
            planned = [a for a in ex.map(p34, authorized) if a]
        if self._cancel.is_set():
            raise Cancelled()
        if not self.include_p5_p6:
            for a in apps:
                for ph in (5, 6):
                    e = self._phase(ph, a)
                    if e["status"] == "PENDING":
                        e["status"], e["note"] = "SKIPPED", "portfolio jobs stop at planning (P4)"
            return
        if not planned:
            raise RuntimeError("P4 released no plan — code modernization not admitted")
        self._run_p5_p6(planned[0])

    def _run_p5_p6(self, app: str) -> None:
        repo = self.repo_paths[app]
        p4 = H.p4_release(self.store, app)
        self._run_phase(5, app, P5AgentRunner(H.code_brief(self.store, app, str(repo))), {
            "scope_manifest": {"workload_ids": [app]},
            "p4_package": {"application_id": app, "status": p4["status"]},
            "execution_permit": {"granted": True, "scope": "repo+manifest+test sandbox",
                                 "issuer": "pilot operator (simulated)"},
        }, P5_GATE_OVERRIDES)
        p5_g4 = self.store.get(f"P5/{app}/G4")["payload"]["decision_record"]
        p5_g3 = self.store.get(f"P5/{app}/G3")["payload"]["final_manifest"]
        self._gate(5, app, p5_g4["status"])
        if not self.include_p6:
            e = self._phase(6, app)
            e["status"], e["note"] = "SKIPPED", "skipped by user"
            return
        seed = _find_seed_sql(repo)
        if seed is None:
            self._log("P6: no seed SQL found in repo — approved no-data route")
            self._run_phase(6, app, P6AgentRunner({"app_id": app, "route": "no-data", "tables": []}), {
                "scope_manifest": {"workload_ids": [app]},
                "p5_package": {"application_id": app, "status": p5_g4["status"]},
                "data_brief": {"app_id": app, "route": "no-data"},
                "migration_permit": {"granted": False},
            }, P6_GATE_OVERRIDES, na_ok=True)
            e = self._phase(6, app)
            e["status"] = "N/A"
            e["note"] = "no seed data found — approved no-data route (P6 G0 emits N/A package)"
            self._gate(6, app, "N/A_ROUTE (no data)")
            return
        src_db, dst_db, table_defs, total_rows = _build_fixture(seed, self.work)
        self.state["facts"].update(seed_rows=total_rows, seed_tables=len(table_defs))
        self._log(f"P6: built sqlite fixture from {seed.name} — {len(table_defs)} tables, {total_rows} rows")
        self._run_phase(6, app, P6AgentRunner({
            "app_id": app, "route": "batch", "source_db": str(src_db), "target_db": str(dst_db),
            "tables": table_defs, "p5_build_digest": p5_g3["build_digest"],
        }), {
            "scope_manifest": {"workload_ids": [app]},
            "p5_package": {"application_id": app, "status": p5_g4["status"]},
            "data_brief": {"app_id": app, "route": "batch", "source_db": str(src_db),
                           "target_db": str(dst_db), "tables": table_defs},
            "migration_permit": {"granted": True, "issuer": "pilot operator (simulated)"},
        }, P6_GATE_OVERRIDES)
        try:
            self._gate(6, app, self.store.get(f"P6/{app}/G3")["payload"]["decision_record"]["status"])
        except Exception:
            self._gate(6, app, "FAILED")
