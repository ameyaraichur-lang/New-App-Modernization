"""Pipeline Console API: run the agentic P1–P4 (+P5/P6) pipeline on one or
many repositories and serve the built UI + registry + run artifacts.

Usage:  python -m appmod.server          (http://localhost:8600)

Auth: every /api/runs*, /api/reviews*, /api/questions* and /api/health/tools
route needs a bearer token (``?token=`` for EventSource/downloads); see
appmod.server.auth for roles.
"""

from __future__ import annotations

import asyncio
import json
import logging
import threading
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Literal

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from appmod.config import get_settings, install_log_redaction
from appmod.server.auth import Principal, require, tokens
from appmod.server.jobs import PipelineJob, validate_repo_input
from appmod.server.rundb import RunDB, StaleReview

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = ROOT / "data" / "registry"
UI_DIST = ROOT / "ui" / "dist"
ACTIVE = {"PENDING", "QUEUED", "RUNNING", "AWAITING_REVIEW"}
log = logging.getLogger("appmod.server")

_jobs: dict[str, PipelineJob] = {}
_jobs_lock = threading.Lock()
_db: RunDB | None = None


def db() -> RunDB:
    global _db
    if _db is None:
        _db = RunDB(get_settings().runs_dir / "appmod.db")
    return _db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    tokens()
    _recover_jobs()
    yield


app = FastAPI(title="App Modernization — Pipeline Console API", lifespan=lifespan)


def _recover_jobs() -> None:
    install_log_redaction()
    for summary in db().list_jobs():
        if summary["job_id"] in _jobs:
            continue
        try:
            row = db().get_job(summary["job_id"])
            if row is None:
                continue
            job = PipelineJob.from_db(row, db())
        except Exception as exc:
            log.warning("could not recover job %s: %s: %s", summary["job_id"], type(exc).__name__, exc)
            continue
        if job.state["status"] in ACTIVE:
            job.state["status"] = "INTERRUPTED"
            job.state["stage_detail"] = "server restarted — POST /resume to continue (completed nodes are reused)"
            job._persist(force=True)
        _jobs[job.job_id] = job


# -- models -------------------------------------------------------------------------------


class RunRequest(BaseModel):
    repo: str | None = None
    repos: list[str] | None = None
    app_id: str | None = None
    decision_mode: bool = True
    include_p6: bool = True
    review_mode: Literal["simulated", "human"] | None = None
    llm: bool | None = None


class RerunRequest(BaseModel):
    phase: int = Field(ge=1, le=6)
    app: str
    nodes: list[str] = Field(default_factory=list)


class DecisionRequest(BaseModel):
    decision: Literal["approve", "reject"]
    candidate_hash: str
    comment: str = ""


class AnswerRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=4000)


# -- health --------------------------------------------------------------------------------


@app.get("/api/health")
def health():
    s = get_settings()
    return {"ok": True, "llm": s.llm_enabled, "auth": s.auth_mode, "review_mode": s.review_mode}


@app.get("/api/health/tools")
def health_tools(_: Principal = Depends(require("viewer"))):
    from appmod.tools import analyzers, mcp_client
    from appmod.tools.builtin import build_gateway
    s = get_settings()
    gw = build_gateway()
    return {
        "astra": {"configured": s.astra_configured, "llm_mode": s.llm_mode, "cache": s.llm_cache,
                  "tiers": {t: s.deployment_for(t) for t in ("reasoning", "coding", "fast", "fallback")},
                  "embedding": s.deployment_for("embedding")},
        "analyzers": analyzers.doctor(),
        "tools": [{"name": t.name, "strict": t.strict, "needs_repo": t.needs_repo,
                   "description": t.description[:160]} for t in gw.tools.values()],
        "mcp": mcp_client.status(),
    }


@app.get("/api/me")
def me(p: Principal = Depends(require("viewer"))):
    return {"user": p.user, "roles": sorted(p.roles)}


# -- runs --------------------------------------------------------------------------------------


@app.post("/api/runs")
def create_run(req: RunRequest, p: Principal = Depends(require("operator"))):
    repos = [r for r in (req.repos or ([req.repo] if req.repo else [])) if r and r.strip()]
    if not repos:
        raise HTTPException(400, "repo path or git URL required")
    if len(repos) > 25:
        raise HTTPException(400, "at most 25 repositories per run")
    for r in repos:
        try:
            validate_repo_input(r)
        except ValueError as exc:
            raise HTTPException(400, str(exc))
    s = get_settings()
    with _jobs_lock:
        active = sum(1 for j in _jobs.values() if j.owner == p.user and j.state["status"] in ACTIVE)
        if active >= s.max_active_runs_per_user:
            raise HTTPException(429, f"{p.user} already has {active} active runs "
                                     f"(limit {s.max_active_runs_per_user})")
        job = PipelineJob(repos=repos, decision_mode=req.decision_mode, include_p6=req.include_p6,
                          app_id=req.app_id, owner=p.user, review_mode=req.review_mode, llm=req.llm,
                          db=db())
        _jobs[job.job_id] = job
    job._persist(force=True)
    job.start()
    return {"job_id": job.job_id, "status": job.snapshot()["status"]}


@app.get("/api/runs")
def list_runs(_: Principal = Depends(require("viewer"))):
    with _jobs_lock:
        jobs = list(_jobs.values())
    out = []
    for j in jobs:
        s = j.state
        out.append({"job_id": j.job_id, "repo": j.repo_input, "app_id": s.get("app_id"),
                    "apps": s.get("apps", []), "status": s["status"], "owner": j.owner,
                    "review_mode": j.review_mode, "started_at": s.get("started_at"),
                    "progress": s.get("progress", 0)})
    return sorted(out, key=lambda r: r["started_at"] or "", reverse=True)


@app.get("/api/runs/{job_id}")
def get_run(job_id: str, _: Principal = Depends(require("viewer"))):
    return _get(job_id).snapshot()


@app.post("/api/runs/{job_id}/cancel")
def cancel_run(job_id: str, _: Principal = Depends(require("operator"))):
    job = _get(job_id)
    if not job.running:
        raise HTTPException(409, f"job is {job.state['status']}, not running")
    job.cancel()
    return {"job_id": job_id, "status": "CANCELLING"}


@app.post("/api/runs/{job_id}/resume")
def resume_run(job_id: str, _: Principal = Depends(require("operator"))):
    job = _get(job_id)
    if job.running:
        raise HTTPException(409, "job is already running")
    if job.state["status"] == "COMPLETED":
        raise HTTPException(409, "job completed — use /rerun to recompute specific nodes")
    job.start()
    return {"job_id": job_id, "status": "RUNNING"}


@app.post("/api/runs/{job_id}/rerun")
def rerun(job_id: str, req: RerunRequest, _: Principal = Depends(require("operator"))):
    job = _get(job_id)
    if job.running:
        raise HTTPException(409, "job is running")
    job.rerun(req.phase, req.app, req.nodes)
    return {"job_id": job_id, "status": "RUNNING", "forced": req.nodes}


@app.get("/api/runs/{job_id}/events")
def run_events(job_id: str, after: int = 0, kinds: str | None = None, limit: int = 1000,
               _: Principal = Depends(require("viewer"))):
    _get(job_id)
    return db().events_since(job_id, after, min(limit, 5000),
                             kinds.split(",") if kinds else None)


@app.get("/api/runs/{job_id}/stream")
async def run_stream(job_id: str, request: Request, after: int = 0,
                     _: Principal = Depends(require("viewer"))):
    job = _get(job_id)

    async def gen():
        seq = after
        idle = 0
        while not await request.is_disconnected():
            evs = db().events_since(job_id, seq, 500)
            for ev in evs:
                seq = ev["seq"]
                yield f"id: {seq}\nevent: {ev['kind']}\ndata: {json.dumps(ev, default=str)}\n\n"
            if not evs:
                idle += 1
                if not job.running and idle > 4:
                    yield "event: END\ndata: {}\n\n"
                    return
                if idle % 30 == 0:
                    yield ": keep-alive\n\n"
                await asyncio.sleep(0.5)
            else:
                idle = 0

    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.get("/api/runs/{job_id}/trace")
def run_trace(job_id: str, app_id: str | None = None, phase: int | None = None,
              _: Principal = Depends(require("viewer"))):
    """Per-agent trace: model calls, tool calls, rejected submissions and the
    final LLM metadata, grouped by phase/app/node."""
    _get(job_id)
    out: dict[str, dict[str, Any]] = {}
    for ev in db().events_since(job_id, 0, 100_000,
                                ["MODEL_CALL", "TOOL_CALL", "SUBMISSION_REJECTED", "AGENT_LLM_DONE"]):
        if app_id and ev.get("app") != app_id:
            continue
        if phase and ev.get("phase") != phase:
            continue
        key = f"P{ev.get('phase')}/{ev.get('app')}/{ev.get('node')}"
        t = out.setdefault(key, {"phase": ev.get("phase"), "app": ev.get("app"), "node": ev.get("node"),
                                 "model_calls": [], "tool_calls": [], "rejections": [], "done": None})
        k = ev["kind"]
        if k == "MODEL_CALL":
            t["model_calls"].append(ev)
        elif k == "TOOL_CALL":
            t["tool_calls"].append(ev)
        elif k == "SUBMISSION_REJECTED":
            t["rejections"].append(ev)
        else:
            t["done"] = ev
    return sorted(out.values(), key=lambda t: (t["phase"] or 0, t["app"] or "", t["node"] or ""))


@app.get("/api/runs/{job_id}/artifacts")
def run_artifacts(job_id: str, phase: int | None = None, _: Principal = Depends(require("viewer"))):
    store_path = _store_path(job_id, required=False)
    if not store_path:
        return []
    index = Path(store_path) / "index"
    if not index.exists():
        return []
    out = []
    for ptr_file in sorted(index.rglob("*.json")):
        ptr = json.loads(ptr_file.read_text(encoding="utf-8"))
        if phase is not None and ptr.get("phase_id") != phase:
            continue
        out.append({"artifact_id": ptr["artifact_id"], "version": ptr["artifact_version"],
                    "producer_id": ptr["producer_id"], "phase_id": ptr["phase_id"],
                    "status": ptr["status"]})
    return out


@app.get("/api/runs/{job_id}/artifacts/{artifact_id:path}")
def get_artifact(job_id: str, artifact_id: str, version: int | None = None,
                 _: Principal = Depends(require("viewer"))):
    from appmod.store.artifact_store import ArtifactStore
    store = ArtifactStore(Path(str(_store_path(job_id))))
    try:
        art = store.get(artifact_id, version)
    except Exception as exc:
        raise HTTPException(404, str(exc))
    return JSONResponse(art)


@app.get("/api/runs/{job_id}/outcome")
def run_outcome(job_id: str, format: str = "zip", _: Principal = Depends(require("viewer"))):
    """Downloadable outcome: zip bundle (report + state + artifacts), the
    markdown report alone, or the raw state JSON."""
    snap = _get(job_id).snapshot()
    _store_path(job_id)
    from appmod.server.report import build_outcome_zip, load_artifacts, render_report
    if format == "json":
        return JSONResponse(snap)
    if format == "md":
        report = render_report(snap, load_artifacts(snap["facts"]["store_path"]))
        return Response(content=report, media_type="text/markdown; charset=utf-8",
                        headers={"Content-Disposition": f'attachment; filename="{job_id}-REPORT.md"'})
    return Response(content=build_outcome_zip(snap), media_type="application/zip",
                    headers={"Content-Disposition": f'attachment; filename="{job_id}-outcome.zip"'})


# -- reviews + questions ------------------------------------------------------------------------


@app.get("/api/reviews")
def list_reviews(job_id: str | None = None, status: str | None = None,
                 _: Principal = Depends(require("viewer"))):
    return db().list_reviews(job_id, status)


@app.post("/api/reviews/{review_id}/decision")
def decide(review_id: str, req: DecisionRequest, p: Principal = Depends(require("reviewer"))):
    try:
        return db().decide(review_id, req.decision, p.user, req.comment, req.candidate_hash)
    except KeyError:
        raise HTTPException(404, f"unknown review {review_id}")
    except StaleReview as exc:
        raise HTTPException(409, str(exc))


@app.get("/api/runs/{job_id}/questions")
def list_questions(job_id: str, app_id: str | None = None, status: str | None = None,
                   _: Principal = Depends(require("viewer"))):
    _get(job_id)
    return db().list_questions(job_id, app_id, status)


@app.post("/api/questions/{question_id}/answer")
def answer(question_id: str, req: AnswerRequest, p: Principal = Depends(require("stakeholder"))):
    try:
        return db().answer(question_id, req.answer, p.user)
    except KeyError:
        raise HTTPException(404, f"unknown question {question_id}")
    except ValueError as exc:
        raise HTTPException(400, str(exc))


# -- registry + static ----------------------------------------------------------------------------


@app.get("/api/registry/{name}")
def registry_file(name: str):
    path = REGISTRY_DIR / name
    if ".." in name or "/" in name or "\\" in name or not path.exists():
        raise HTTPException(404, "unknown registry file")
    return JSONResponse(json.loads(path.read_text(encoding="utf-8")))


def _get(job_id: str) -> PipelineJob:
    with _jobs_lock:
        job = _jobs.get(job_id)
    if job is None:
        raise HTTPException(404, f"unknown job {job_id}")
    return job


def _store_path(job_id: str, required: bool = True) -> str | None:
    sp = (_get(job_id).snapshot().get("facts") or {}).get("store_path")
    if not sp and required:
        raise HTTPException(409, "run has not produced any artifacts yet")
    return sp


app.mount("/registry", StaticFiles(directory=str(REGISTRY_DIR)), name="registry")

if UI_DIST.exists():
    app.mount("/", StaticFiles(directory=str(UI_DIST), html=True), name="ui")
else:
    @app.get("/")
    def no_ui():
        return {"error": "ui/dist not built — run `npm run build` in ui/"}
