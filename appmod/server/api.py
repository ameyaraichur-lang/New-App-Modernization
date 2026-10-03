"""Pipeline Console API: run the P1–P6 pipeline on a user-supplied repo and
serve the built UI + registry + run artifacts from one process.

Usage:  python -m appmod.server          (http://localhost:8600)
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from appmod.server.runner import PipelineJob

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = ROOT / "data" / "registry"
UI_DIST = ROOT / "ui" / "dist"

app = FastAPI(title="App Modernization — Pipeline Console API")

_jobs: dict[str, PipelineJob] = {}
_jobs_lock = threading.Lock()


class RunRequest(BaseModel):
    repo: str
    app_id: str | None = None
    decision_mode: bool = True
    include_p6: bool = True


@app.post("/api/runs")
def create_run(req: RunRequest):
    if not req.repo or not req.repo.strip():
        raise HTTPException(400, "repo path or git URL required")
    job = PipelineJob(repo=req.repo, decision_mode=req.decision_mode,
                      include_p6=req.include_p6, app_id=req.app_id,
                      runs_root=ROOT / "runs")
    with _jobs_lock:
        _jobs[job.job_id] = job
    job.start()
    return {"job_id": job.job_id, "status": job.snapshot()["status"]}


@app.get("/api/runs")
def list_runs():
    with _jobs_lock:
        jobs = list(_jobs.values())
    return [
        {"job_id": j.job_id, "repo": j.repo_input, "app_id": j.snapshot()["app_id"],
         "status": j.snapshot()["status"],
         "started_at": j.snapshot()["started_at"]}
        for j in reversed(jobs)
    ]


@app.get("/api/runs/{job_id}")
def get_run(job_id: str):
    job = _get(job_id)
    return job.snapshot()


@app.get("/api/runs/{job_id}/artifacts")
def run_artifacts(job_id: str, phase: int | None = None):
    job = _get(job_id)
    store_path = job.snapshot()["facts"].get("store_path")
    if not store_path:
        return []
    out = []
    index = Path(store_path) / "index"
    if not index.exists():
        return []
    for ptr_file in sorted(index.rglob("*.json")):
        ptr = json.loads(ptr_file.read_text(encoding="utf-8"))
        if phase is not None and ptr.get("phase_id") != phase:
            continue
        out.append({
            "artifact_id": ptr["artifact_id"],
            "version": ptr["artifact_version"],
            "producer_id": ptr["producer_id"],
            "phase_id": ptr["phase_id"],
            "status": ptr["status"],
        })
    return out


@app.get("/api/runs/{job_id}/artifacts/{artifact_id:path}")
def get_artifact(job_id: str, artifact_id: str, version: int | None = None):
    job = _get(job_id)
    store_path = job.snapshot()["facts"].get("store_path")
    if not store_path:
        raise HTTPException(404, "run has no store yet")
    from appmod.store.artifact_store import ArtifactStore
    store = ArtifactStore(store_path)
    try:
        art = store.get(artifact_id, version)
    except Exception as exc:
        raise HTTPException(404, str(exc))
    return JSONResponse(art)


@app.get("/api/runs/{job_id}/outcome")
def run_outcome(job_id: str, format: str = "zip"):
    """Downloadable end-of-run outcome: zip bundle (report + state + all
    artifacts), the markdown report alone, or the raw state JSON."""
    job = _get(job_id)
    snap = job.snapshot()
    if not (snap.get("facts") or {}).get("store_path"):
        raise HTTPException(409, "run has not produced any artifacts yet")
    from appmod.server.report import build_outcome_zip, load_artifacts, render_report
    if format == "json":
        return JSONResponse(snap)
    if format == "md":
        report = render_report(snap, load_artifacts(snap["facts"]["store_path"]))
        return Response(content=report, media_type="text/markdown; charset=utf-8",
                        headers={"Content-Disposition":
                                 f'attachment; filename="{job_id}-REPORT.md"'})
    data = build_outcome_zip(snap)
    return Response(content=data, media_type="application/zip",
                    headers={"Content-Disposition":
                             f'attachment; filename="{job_id}-outcome.zip"'})


@app.get("/api/registry/{name}")
def registry_file(name: str):
    path = REGISTRY_DIR / name
    if not path.exists() or ".." in name or "/" in name or "\\" in name:
        raise HTTPException(404, "unknown registry file")
    return JSONResponse(json.loads(path.read_text(encoding="utf-8")))


def _get(job_id: str) -> PipelineJob:
    with _jobs_lock:
        job = _jobs.get(job_id)
    if job is None:
        raise HTTPException(404, f"unknown job {job_id}")
    return job


# registry JSONs for the console (same paths the vite preview serves)
app.mount("/registry", StaticFiles(directory=str(REGISTRY_DIR)), name="registry")


# ---- static UI (built console) -------------------------------------------



if UI_DIST.exists():
    app.mount("/", StaticFiles(directory=str(UI_DIST), html=True), name="ui")
else:
    @app.get("/")
    def no_ui():
        return {"error": "ui/dist not built — run `npm run build` in ui/"}
