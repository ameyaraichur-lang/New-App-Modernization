"""Outcome bundle for a runner job: a human-readable REPORT.md plus a zip
containing the report, the full run state, and every published artifact.

The report is derived ONLY from what the run actually produced (job state +
artifact envelopes) — no invented findings. Sections without evidence are
omitted rather than filled with placeholders.
"""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path
from typing import Any


def load_artifacts(store_path: str) -> list[dict[str, Any]]:
    """Every latest artifact envelope from a run's store, sorted by id."""
    index = Path(store_path) / "index"
    if not index.exists():
        return []
    out = []
    for ptr_file in sorted(index.rglob("*.json")):
        ptr = json.loads(ptr_file.read_text(encoding="utf-8"))
        obj = Path(store_path) / ptr["object_path"]
        if obj.exists():
            art = json.loads(obj.read_text(encoding="utf-8"))
        else:  # pointer without object — keep the pointer facts
            art = {"artifact_id": ptr["artifact_id"],
                   "artifact_version": ptr["artifact_version"],
                   "status": ptr["status"], "producer_id": ptr["producer_id"]}
        out.append(art)
    out.sort(key=lambda a: a["artifact_id"])
    return out


def _find(artifacts: list[dict], suffix: str) -> dict | None:
    for a in artifacts:
        if a["artifact_id"].endswith(suffix):
            return a
    return None


def _md_table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        return ""
    lines = ["| " + " | ".join(headers) + " |",
             "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        lines.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    return "\n".join(lines)


def render_report(job: dict[str, Any], artifacts: list[dict]) -> str:
    s: list[str] = []
    s.append("# App Modernization — Run Report")
    s.append("")
    s.append(f"- **Job**: `{job['job_id']}` — final status **{job['status']}**")
    s.append(f"- **Repository**: `{job['repo']}`"
             + (f" (application `{job['app_id']}`)" if job.get("app_id") else ""))
    s.append(f"- **Window**: {job.get('started_at') or '—'} → "
             f"{job.get('finished_at') or '—'}")
    s.append(f"- **Options**: decision_mode={str(job.get('decision_mode', True)).lower()}"
             f", include_p6={str(job.get('include_p6', True)).lower()}"
             f", {len(artifacts)} published artifacts")
    if job.get("error"):
        s.append(f"- **Error**: `{job['error']}`")
    s.append("")

    if job.get("gate_chain"):
        s.append("## Release gate chain")
        s.append("")
        s.append(_md_table(["Phase", "Gate", "Decision"],
                           [[f"P{g['phase']}", g["gate"], g["decision"]]
                            for g in job["gate_chain"]]))
        s.append("")

    if job.get("facts"):
        s.append("## Key facts")
        s.append("")
        s.append(_md_table(["fact", "value"], list(job["facts"].items())))
        s.append("")

    s.append("## Phase outcomes")
    s.append("")
    for p in job.get("phases", []):
        s.append(f"### Phase {p['phase']} — {p['status']}"
                 + (f" · {p['decision']}" if p.get("decision") else ""))
        if p.get("note"):
            s.append("")
            s.append(f"> {p['note']}")
        if p.get("nodes"):
            s.append("")
            s.append(_md_table(["node", "status"],
                               [[n["id"], n["status"]] for n in p["nodes"]]))
        s.append("")

    # -- evidence-backed modernization record (best effort, from artifacts) --
    record: list[str] = []

    a7 = _find(artifacts, "/A7") or None
    if a7 and "route_register" in (a7.get("payload") or {}):
        rows = [[e.get("application_id"), e.get("route"),
                 e.get("rationale", e.get("reason", ""))]
                for e in a7["payload"]["route_register"]]
        if rows:
            record.append("### Portfolio disposition (P2 route register)\n\n"
                          + _md_table(["application", "8R route", "rationale"], rows))

    g2 = next((a for a in artifacts if a["artifact_id"].endswith("/G2")
               and "checkpoint_manifest" in (a.get("payload") or {})), None)
    if g2:
        cp = g2["payload"]["checkpoint_manifest"]
        jobs = cp.get("jobs", [])
        rows = [[j.get("table"), j.get("rows"), j.get("copied")] for j in jobs]
        body = (f"Checkpoint `{cp.get('checkpoint_id')}` — logical cutoff: "
                f"{cp.get('logical_cutoff')}.\n\n"
                + (_md_table(["table", "source rows", "copied"], rows) if rows else ""))
        rejects = cp.get("rejects", [])
        if rejects:
            body += ("\n\nRejects: " + "; ".join(
                f"{r.get('table', '?')} — {r.get('reason', r.get('error', '?'))}"
                for r in rejects[:10]))
        record.append("### Data migration executed (P6 X1 checkpoint)\n\n" + body)

    a9 = _find(artifacts, "/A9") or None
    if a9 and isinstance((a9.get("payload") or {}).get("results"), list):
        rows = [[r.get("table"), r.get("source_count", r.get("expected")),
                 r.get("target_count", r.get("actual")),
                 r.get("match", r.get("status", ""))] for r in a9["payload"]["results"]]
        if rows:
            record.append("### Post-migration reconciliation (P6 A9)\n\n"
                          + _md_table(["table", "source", "target", "match"], rows))

    g3_5 = next((a for a in artifacts if a["artifact_id"].startswith("P5/")
                 and a["artifact_id"].endswith("/G3")), None)
    if g3_5 and (g3_5.get("payload") or {}).get("final_manifest"):
        fm = g3_5["payload"]["final_manifest"]
        record.append("### Modernized build (P5 G3 final manifest)\n\n"
                      f"- build digest: `{fm.get('build_digest')}`\n"
                      f"- integrated commit: `{fm.get('integrated_commit')}`\n")

    if record:
        s.append("## Modernization record")
        s.append("")
        s.append("\n\n".join(record))
        s.append("")

    s.append("## Honest pilot limits")
    s.append("")
    s.append("- Phase 5 authors **change manifests** (pilot depth 1); runtime "
             "differential is NOT_RUN, so its release gate is LIMITED_HANDOFF "
             "rather than a full pass — NOT_RUN never counts as PASS.")
    s.append("- Phase 6 service-flow validation is NOT_RUN without a running "
             "application; the batch migration itself is real (X1 execution "
             "service with checkpoint + reconciliation).")
    s.append("- Reviewer/stakeholder evidence in this run is **simulated and "
             "labeled** in the artifacts (decision mode); it is never treated "
             "as owner approval.")
    s.append("")

    if artifacts:
        s.append("## Artifact index")
        s.append("")
        s.append(_md_table(["artifact", "version", "producer", "status"],
                           [[a["artifact_id"], a.get("artifact_version"),
                             a.get("producer_id"), a["status"]] for a in artifacts]))
        s.append("")
    s.append("---")
    s.append("_Generated by the App Modernization pipeline console from the "
             "run's immutable artifact store — every claim above traces to a "
             "stored envelope._")
    return "\n".join(s)


def build_outcome_zip(job: dict[str, Any]) -> bytes:
    store_path = (job.get("facts") or {}).get("store_path")
    artifacts = load_artifacts(store_path) if store_path else []
    report = render_report(job, artifacts)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("REPORT.md", report)
        z.writestr("outcome.json", json.dumps(job, indent=2, default=str))
        for a in artifacts:
            rel = f"artifacts/{a['artifact_id'].replace('/', '__')}.v{a.get('artifact_version', 1)}.json"
            z.writestr(rel, json.dumps(a, indent=2, default=str))
    return buf.getvalue()
