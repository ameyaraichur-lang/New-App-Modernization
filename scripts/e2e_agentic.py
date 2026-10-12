"""End-to-end agentic acceptance run (M0–M4) against real legacy repositories.

Starts the real API server, submits ONE portfolio job over the corpus repos
with live Astra and review_mode=human, then drives the human surfaces over
HTTP with a *scripted* reviewer and a *scripted* stakeholder (clearly labelled
as automation in every recorded answer/decision). When the job finishes it
scores every P1–P4 agent dispatch:

  success  =  artifact status != FAILED
           AND execution_metadata.llm.enriched == true   (real Astra loop, not seed fallback)
           AND ContractValidator passes (envelope + payload schema + content hash)

and writes docs/runs/e2e-<label>.{json,md}.

    uv run python scripts/e2e_agentic.py --label run1 --cache record
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import socket
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from appmod.contracts.schemas import ContractValidator  # noqa: E402
from appmod.registry.compiler import resolve_registry  # noqa: E402
from appmod.store.artifact_store import ArtifactStore  # noqa: E402

CORPUS = ROOT.parent / "corpus"
DEFAULT_REPOS = ["spring-petclinic", "microblog", "node-express-realworld-example-app",
                 "django-realworld-example-app"]
TERMINAL = {"COMPLETED", "FAILED", "CANCELLED", "INTERRUPTED"}
SCRIPTED = "[scripted e2e harness — automation, not a human]"

STAKEHOLDER_ANSWERS = [
    (("critical", "criticality", "tier", "availability", "sla", "rto", "rpo", "downtime"),
     "Business-critical for its user community but not revenue-bearing; target 99.5% availability, "
     "RTO 4h, RPO 1h; maintenance windows on weekends are acceptable."),
    (("compliance", "regulat", "gdpr", "pci", "hipaa", "privacy", "pii", "personal", "retention"),
     "Stores personal data of registered users (names, emails, password hashes), so GDPR applies; "
     "no payment card or health data; retain account data until deletion is requested."),
    (("owner", "own", "roadmap", "team", "responsib", "steward", "contact"),
     "Owned by the platform engineering team; the product owner sets the roadmap; data stewardship "
     "sits with the same team."),
    (("user", "persona", "volume", "traffic", "load", "peak", "concurren"),
     "Roughly 2,000 monthly active users, peaks of ~50 concurrent sessions during business hours."),
    (("integrat", "external", "third", "api", "dependen", "upstream", "downstream"),
     "No contractual external integrations beyond what the repository shows; email delivery is the only "
     "outbound dependency we rely on."),
    (("budget", "cost", "timeline", "deadline", "constraint", "freeze"),
     "Modernization should finish within two quarters on the existing team; no hard freeze dates."),
]
DEFAULT_ANSWER = ("No additional constraints known to the business; treat this as an assumption to "
                  "verify during design.")


def answer_for(question: str) -> str:
    q = question.lower()
    for keys, ans in STAKEHOLDER_ANSWERS:
        if any(k in q for k in keys):
            return f"{ans} {SCRIPTED}"
    return f"{DEFAULT_ANSWER} {SCRIPTED}"


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default=time.strftime("%Y%m%d-%H%M%S"))
    ap.add_argument("--repos", nargs="*", default=DEFAULT_REPOS)
    ap.add_argument("--cache", default="record", choices=["off", "read", "record", "replay"])
    ap.add_argument("--timeout", type=int, default=4 * 3600)
    ap.add_argument("--parallel-agents", type=int, default=4)
    ap.add_argument("--parallel-apps", type=int, default=4)
    ap.add_argument("--threshold", type=float, default=97.0)
    ap.add_argument("--no-llm", action="store_true", help="plumbing check only (scores will fail)")
    ap.add_argument("--rescore", metavar="JOB_ID", help="score a finished job from the run DB (no server)")
    ap.add_argument("--resume", metavar="JOB_ID", help="resume an interrupted job (finished nodes are reused)")
    args = ap.parse_args()
    if args.rescore:
        return rescore(args)

    out_dir = ROOT / "docs" / "runs"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_dir = ROOT / "runs" / "e2e" / args.label
    log_dir.mkdir(parents=True, exist_ok=True)
    toks = {r: secrets.token_urlsafe(24) for r in ("op", "rv", "sh", "vw")}
    env = {**os.environ,
           "APPMOD_API_TOKENS": (f"{toks['op']}=e2e-operator:operator;"
                                 f"{toks['rv']}=scripted-reviewer:reviewer;"
                                 f"{toks['sh']}=scripted-stakeholder:stakeholder;"
                                 f"{toks['vw']}=e2e-viewer:viewer"),
           "APPMOD_AUTH_MODE": "token", "APPMOD_REVIEW_MODE": "human", "APPMOD_LLM_MODE": "off" if args.no_llm else "auto",
           "APPMOD_LLM_CACHE": args.cache, "APPMOD_ANALYZERS": "on",
           "APPMOD_MAX_PARALLEL_AGENTS": str(args.parallel_agents),
           "APPMOD_MAX_PARALLEL_APPS": str(args.parallel_apps),
           "APPMOD_MAX_ACTIVE_RUNS_PER_USER": "5", "PYTHONPATH": str(ROOT)}
    port = free_port()
    server_log = open(log_dir / "server.log", "w")
    server = subprocess.Popen([sys.executable, "-m", "uvicorn", "appmod.server.api:app", "--host",
                               "127.0.0.1", "--port", str(port), "--no-access-log"],
                              cwd=ROOT, env=env, stdout=server_log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"
    H = {r: {"Authorization": f"Bearer {t}"} for r, t in toks.items()}
    c = httpx.Client(base_url=base, timeout=60)
    t0 = time.time()
    m0 = time.monotonic()      # timeout clock: does not advance while the host sleeps
    try:
        for _ in range(120):
            try:
                if c.get("/api/health").status_code == 200:
                    break
            except httpx.HTTPError:
                pass
            time.sleep(0.5)
        health = c.get("/api/health/tools", headers=H["vw"]).json()
        if args.resume:
            job = args.resume
            r = c.post(f"/api/runs/{job}/resume", headers=H["op"])
            r.raise_for_status()
            print(f"[e2e] resumed job {job} (port {port}, cache={args.cache})", flush=True)
        else:
            repos = [str(CORPUS / r) if not r.startswith(("/", "http", "git@")) else r for r in args.repos]
            r = c.post("/api/runs", headers=H["op"], json={"repos": repos, "review_mode": "human", "llm": True})
            r.raise_for_status()
            job = r.json()["job_id"]
            print(f"[e2e] job {job} on {len(repos)} repos (port {port}, cache={args.cache})", flush=True)

        answered, decisions, last = 0, [], ""
        while time.monotonic() - m0 < args.timeout:
            snap = c.get(f"/api/runs/{job}", headers=H["vw"]).json()
            for q in c.get(f"/api/runs/{job}/questions", params={"status": "OPEN"}, headers=H["vw"]).json():
                resp = c.post(f"/api/questions/{q['question_id']}/answer", headers=H["sh"],
                              json={"answer": answer_for(q["question"])})
                answered += resp.status_code == 200
            for rv in c.get("/api/reviews", params={"job_id": job, "status": "PENDING"}, headers=H["vw"]).json():
                prop = rv["proposal"]
                resp = c.post(f"/api/reviews/{rv['review_id']}/decision", headers=H["rv"],
                              json={"decision": "approve", "candidate_hash": rv["candidate_hash"],
                                    "comment": f"approve proposed {prop.get('status')} {SCRIPTED}"})
                if resp.status_code == 200:
                    decisions.append({"phase": rv["phase"], "app": rv["app"], "gate": rv["gate"],
                                      "proposed": prop.get("status"), "decision": "approve"})
            line = (f"{snap['status']} {snap['progress']}% {snap.get('stage_detail') or ''} | "
                    f"llm calls={snap['llm']['calls']} tok_in={snap['llm']['input_tokens']} "
                    f"answers={answered} approvals={len(decisions)}")
            if line != last:
                print(f"[e2e {int(time.time() - t0):>5}s] {line}", flush=True)
                last = line
            if snap["status"] in TERMINAL:
                break
            time.sleep(3)
        snap = c.get(f"/api/runs/{job}", headers=H["vw"]).json()
        trace = c.get(f"/api/runs/{job}/trace", headers=H["vw"]).json()
        reviews = c.get("/api/reviews", params={"job_id": job}, headers=H["vw"]).json()
        questions = c.get(f"/api/runs/{job}/questions", headers=H["vw"]).json()
    finally:
        server.terminate()
        try:
            server.wait(20)
        except subprocess.TimeoutExpired:
            server.kill()
        server_log.close()

    elapsed = time.time() - t0
    report = score(snap, trace, reviews, questions, health, elapsed, args)
    stem = out_dir / f"e2e-{args.label}"
    stem.with_suffix(".json").write_text(json.dumps(report, indent=2, default=str))
    stem.with_suffix(".md").write_text(render(report))
    print(f"[e2e] success {report['summary']['success_rate']:.2f}% "
          f"({report['summary']['succeeded']}/{report['summary']['expected']}) — report {stem}.md", flush=True)
    return 0 if report["summary"]["success_rate"] > args.threshold and snap["status"] == "COMPLETED" else 1


def rescore(args) -> int:
    from appmod.config import get_settings
    from appmod.server.rundb import RunDB
    from appmod.tools import analyzers
    db = RunDB(get_settings().runs_dir / "appmod.db")
    row = db.get_job(args.rescore)
    if row is None:
        print(f"unknown job {args.rescore}")
        return 2
    snap = row["state"]
    trace: dict = {}
    for ev in db.events_since(args.rescore, 0, 1_000_000,
                              ["MODEL_CALL", "TOOL_CALL", "SUBMISSION_REJECTED", "AGENT_LLM_DONE"]):
        t = trace.setdefault((ev.get("phase"), ev.get("app"), ev.get("node")),
                             {"phase": ev.get("phase"), "app": ev.get("app"), "node": ev.get("node"),
                              "model_calls": [], "tool_calls": [], "rejections": [], "done": None})
        if ev["kind"] == "SUBMISSION_REJECTED":
            t["rejections"].append(ev)
    s = get_settings()
    health = {"astra": {"tiers": {t: s.deployment_for(t) for t in ("reasoning", "coding", "fast", "fallback")}},
              "analyzers": analyzers.doctor()}
    t0, t1 = snap.get("started_at"), snap.get("finished_at")
    elapsed = (time.mktime(time.strptime(t1, "%Y-%m-%dT%H:%M:%SZ"))
               - time.mktime(time.strptime(t0, "%Y-%m-%dT%H:%M:%SZ"))) if t0 and t1 else 0
    report = score(snap, list(trace.values()), db.list_reviews(args.rescore),
                   db.list_questions(args.rescore), health, elapsed, args)
    stem = ROOT / "docs" / "runs" / f"e2e-{args.label}"
    stem.parent.mkdir(parents=True, exist_ok=True)
    stem.with_suffix(".json").write_text(json.dumps(report, indent=2, default=str))
    stem.with_suffix(".md").write_text(render(report))
    print(f"[e2e] success {report['summary']['success_rate']:.2f}% "
          f"({report['summary']['succeeded']}/{report['summary']['expected']}) — report {stem}.md")
    return 0 if report["summary"]["success_rate"] > args.threshold and snap["status"] == "COMPLETED" else 1


def score(snap, trace, reviews, questions, health, elapsed, args) -> dict:
    reg = resolve_registry()["phases"]
    store = ArtifactStore(snap["facts"]["store_path"])
    validators = {p: ContractValidator(reg[p]) for p in (1, 2, 3, 4)}
    apps = snap["apps"]
    tr = {(t["phase"], t["app"], t["node"]): t for t in trace}
    try:   # apps the authorized P2 release gate routed to the non-delivery register (Retain/Retire)
        record = store.get("P2/PF1/G2")["payload"]["decision_record"]
        not_admitted = {e["application_id"]: e["route"]
                        for e in (record.get("non_delivery_register") or {}).get("entries", [])}
    except Exception:
        not_admitted = {}
    rows = []
    for phase in (1, 2, 3, 4):
        scope = ["PF1"] if phase == 2 else apps
        for app in scope:
            for a in reg[phase]["agents"]:
                aid = f"P{phase}/{app}/{a['local_id']}"
                row = {"phase": phase, "app": app, "agent": a["local_id"], "name": a.get("name", ""),
                       "artifact": aid}
                try:
                    art = store.get(aid)
                except Exception:
                    if phase >= 3 and app in not_admitted:
                        row.update(status="NOT_ADMITTED", success=None,
                                   reason=f"not admitted: P2 G2 put {app} in the IA02 non-delivery "
                                          f"register ({not_admitted[app]})")
                    else:
                        row.update(status="NOT_DISPATCHED", success=False, reason="no artifact published")
                    rows.append(row)
                    continue
                llm = (art.get("execution_metadata") or {}).get("llm") or {}
                errs = validators[phase].validate(art)
                t = tr.get((phase, app, a["local_id"]), {})
                row.update(
                    status=art["status"], version=art.get("artifact_version"),
                    enriched=bool(llm.get("enriched")), mode=llm.get("mode"), tier=llm.get("tier"),
                    deployments=llm.get("deployments"), turns=llm.get("turns"), repairs=llm.get("repairs"),
                    failover=llm.get("failover"), tool_calls=llm.get("tool_calls"),
                    tools_used=llm.get("tools_used"),
                    evidence_available=llm.get("evidence_ids") if isinstance(llm.get("evidence_ids"), int) else None,
                    evidence_cited=len({e for f in art.get("findings", []) if f.get("origin") == "llm"
                                        for e in (f.get("evidence_ids") or [])}),
                    tokens={k: llm.get(f"{k}_tokens") or 0 for k in ("input", "output", "reasoning")},
                    latency_ms=llm.get("latency_ms"),
                    llm_findings=sum(1 for f in art.get("findings", []) if f.get("origin") == "llm"),
                    validation_errors=errs[:5], rejections=len(t.get("rejections", [])),
                    confidence=llm.get("confidence"), summary=(llm.get("summary") or "")[:400],
                    error=llm.get("error"))
                reasons = []
                if art["status"] == "FAILED":
                    reasons.append("artifact FAILED")
                if not row["enriched"]:
                    reasons.append(f"not enriched ({llm.get('mode') or 'no llm metadata'}: "
                                   f"{llm.get('error') or llm.get('reason') or ''})")
                if errs:
                    reasons.append(f"validation: {errs[0]}")
                row["success"] = not reasons
                row["reason"] = "; ".join(reasons)
                rows.append(row)
    skipped = [r for r in rows if r["success"] is None]
    rows_all, rows = rows, [r for r in rows if r["success"] is not None]
    ok = sum(r["success"] for r in rows)
    gates = []
    for p in snap["phases"]:
        if p["phase"] <= 4:
            gates.append({"phase": p["phase"], "app": p["app"], "status": p["status"],
                          "decision": p["decision"], "note": p.get("note", "")})
    tok = Counter()
    for r in rows:
        for k, v in (r.get("tokens") or {}).items():
            if isinstance(v, (int, float)):
                tok[k] += v
    by_phase = defaultdict(lambda: [0, 0])
    for r in rows:
        by_phase[r["phase"]][0] += r["success"]
        by_phase[r["phase"]][1] += 1
    return {
        "label": args.label, "job_id": snap["job_id"], "job_status": snap["status"],
        "job_error": snap.get("error"), "elapsed_s": round(elapsed), "cache_mode": args.cache,
        "apps": apps, "app_facts": snap.get("app_facts"),
        "summary": {"expected": len(rows), "succeeded": ok,
                    "success_rate": 100.0 * ok / max(1, len(rows)), "threshold": args.threshold,
                    "not_admitted": len(skipped), "not_admitted_apps": not_admitted,
                    "success_rate_all_slots": 100.0 * ok / max(1, len(rows_all)),
                    "by_phase": {p: {"ok": v[0], "total": v[1]} for p, v in sorted(by_phase.items())},
                    "enriched": sum(bool(r.get("enriched")) for r in rows),
                    "repairs": sum(r.get("repairs") or 0 for r in rows),
                    "failovers": sum(bool(r.get("failover")) for r in rows),
                    "tool_calls": sum(r.get("tool_calls") or 0 for r in rows),
                    "evidence_cited": sum(r.get("evidence_cited") or 0 for r in rows),
                    "llm_findings": sum(r.get("llm_findings") or 0 for r in rows),
                    "tokens": dict(tok), "llm_job_totals": snap.get("llm")},
        "gates": gates, "reviews": [{k: v for k, v in rv.items() if k != "proposal"} for rv in reviews],
        "questions": [{k: q[k] for k in ("app", "question", "source", "status", "respondent")}
                      for q in questions],
        "health": {"astra": health.get("astra"), "analyzers": health.get("analyzers")},
        "agents": rows_all,
    }


def render(rep: dict) -> str:
    s = rep["summary"]
    L = [f"# E2E agentic acceptance run `{rep['label']}`", "",
         f"- **Job**: `{rep['job_id']}` — **{rep['job_status']}**"
         + (f" (error: `{rep['job_error']}`)" if rep.get("job_error") else ""),
         f"- **Repositories**: {', '.join(f'`{a}`' for a in rep['apps'])}",
         f"- **Elapsed**: {rep['elapsed_s'] // 60} min {rep['elapsed_s'] % 60} s; LLM cache mode `{rep['cache_mode']}`"
         " (record = every call live, responses recorded for replay)",
         f"- **Astra tiers**: {rep['health']['astra'].get('tiers')}",
         "- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were "
         "submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every "
         "record).", "",
         "## Result", "",
         f"**Agent success rate: {s['success_rate']:.2f}%** ({s['succeeded']}/{s['expected']} P1–P4 agent "
         f"dispatches; threshold > {s['threshold']}%).", ""]
    if s.get("not_admitted"):
        L += [f"{s['not_admitted']} P3/P4 agent slots were **not admitted** because the authorized P2 "
              f"release gate routed {', '.join(f'`{a}` ({r})' for a, r in s['not_admitted_apps'].items())} "
              "to the non-delivery register — by design, no architecture or plan is produced for a "
              f"non-delivery route. Counting those slots as failures would give "
              f"{s['success_rate_all_slots']:.2f}%.", ""]
    L += [
         "Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) "
         "**and** passes ContractValidator (envelope + payload schema + content hash).", "",
         "| phase | ok / total |", "|---|---|"]
    names = {1: "P1 Discovery", 2: "P2 Portfolio", 3: "P3 Architecture", 4: "P4 Planning"}
    for p, v in s["by_phase"].items():
        L.append(f"| {names[int(p)]} | {v['ok']} / {v['total']} |")
    tok = s["tokens"]
    L += ["", f"- Tool calls: {s['tool_calls']}; evidence ids cited: {s['evidence_cited']}; "
              f"LLM findings: {s['llm_findings']}; repair rounds: {s['repairs']}; failovers: {s['failovers']}",
          f"- Tokens: {tok}", "", "## Release gates", "", "| phase | app | phase status | decision |",
          "|---|---|---|---|"]
    for g in rep["gates"]:
        L.append(f"| P{g['phase']} | {g['app']} | {g['status']} | {g['decision'] or '—'} |")
    L += ["", f"Reviews: {len(rep['reviews'])} (decided by `scripted-reviewer`); stakeholder questions: "
              f"{len(rep['questions'])} ({sum(q['status'] == 'ANSWERED' for q in rep['questions'])} answered).",
          "", "## Per-agent results", "",
          "| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rep["agents"]:
        L.append(f"| P{r['phase']}.{r['agent']} | {r['app']} | {r.get('status')} | "
                 f"{'yes' if r.get('enriched') else 'no'} | {r.get('tier') or ''} | {r.get('turns') or ''} | "
                 f"{r.get('repairs') or 0} | {r.get('tool_calls') or 0} | {r.get('evidence_cited') or 0} | "
                 f"{'—' if r['success'] is None else '✅' if r['success'] else '❌'} | {r.get('reason') or ''} |")
    fails = [r for r in rep["agents"] if r["success"] is False]
    if fails:
        L += ["", "## Failures", ""] + [f"- `{r['artifact']}`: {r['reason']}" for r in fails]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
