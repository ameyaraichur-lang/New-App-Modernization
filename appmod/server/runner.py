"""Pipeline runner service: executes P1–P6 on an end-user-supplied repository
(local path or git URL) and reports live progress for the UI.

This is the 'test the pipeline' entrypoint behind the console's Runner view.
Every phase runs through the same orchestrator/kernel as the E2E scripts —
no shortcuts, and the honest-depth rules (NOT_RUN never PASS) apply.
"""

from __future__ import annotations

import re
import sqlite3
import subprocess
import threading
import time
import uuid
from pathlib import Path
from typing import Any

from appmod.kernel.audit import AuditJournal
from appmod.kernel.orchestrator import PhaseOrchestrator, RunContext
from appmod.kernel.policy import PolicyService
from appmod.phases.p1.engine import P1AgentRunner, P1_GATE_OVERRIDES
from appmod.phases.p2.engine import P2AgentRunner, P2_GATE_OVERRIDES, PortfolioApp
from appmod.phases.p3.engine import P3AgentRunner, P3_GATE_OVERRIDES
from appmod.phases.p4.engine import P4AgentRunner, P4_GATE_OVERRIDES
from appmod.phases.p5.engine import P5AgentRunner, P5_GATE_OVERRIDES
from appmod.phases.p6.engine import P6AgentRunner, P6_GATE_OVERRIDES
from appmod.registry.compiler import resolve_registry
from appmod.store.artifact_store import ArtifactStore
from appmod.tools.repo_intel import CODE_LANGUAGES


def _gate_of(phase: int) -> str:
    return {1: "G2", 2: "G2", 3: "G2", 4: "G2", 5: "G4", 6: "G3"}[phase]


_PHASE_NAME = {1: "Discovery", 2: "Portfolio decision", 3: "Target architecture",
               4: "Planning", 5: "Code modernization", 6: "Data modernization"}


class PipelineJob:
    def __init__(self, repo: str, decision_mode: bool = True, include_p6: bool = True,
                 app_id: str | None = None, runs_root: Path | None = None):
        self.job_id = f"job-{int(time.time())}-{uuid.uuid4().hex[:6]}"
        self.repo_input = repo.strip()
        self.decision_mode = decision_mode
        self.include_p6 = include_p6
        self.app_id = app_id
        self.runs_root = runs_root or (Path(__file__).resolve().parents[2] / "runs")
        self.state: dict[str, Any] = {
            "job_id": self.job_id,
            "repo": self.repo_input,
            "app_id": None,
            "status": "PENDING",          # PENDING|RUNNING|COMPLETED|FAILED
            "stage": "QUEUED",            # QUEUED|CLONING|RUNNING|DONE
            "stage_detail": None,
            "current_phase": None,
            "progress": 0,                # 0-100 across all phases
            "log": [],                    # [{ts, msg, level}] live activity feed
            "started_at": None, "finished_at": None,
            "error": None,
            "phases": [],
            "gate_chain": [],
            "facts": {},
        }
        self._lock = threading.Lock()
        self.thread: threading.Thread | None = None

    # -- state helpers ------------------------------------------------------

    def _update(self, **fields: Any) -> None:
        with self._lock:
            self.state.update(fields)

    def _log(self, msg: str, level: str = "info") -> None:
        with self._lock:
            self.state["log"].append({"ts": _now(), "msg": msg, "level": level})
            if len(self.state["log"]) > 600:
                del self.state["log"][:100]

    def _set_stage(self, stage: str, detail: str | None = None,
                   phase: int | None = None) -> None:
        with self._lock:
            self.state["stage"] = stage
            self.state["stage_detail"] = detail
            if phase is not None:
                self.state["current_phase"] = phase

    def _recompute_progress(self) -> None:
        """Fraction of pipeline work finished: completed phases + the share of
        done nodes inside the running phase, over the phases in scope."""
        with self._lock:
            total = 6 if self.include_p6 else 5
            done = sum(1 for p in self.state["phases"]
                       if p["status"] in ("COMPLETED", "N/A", "SKIPPED"))
            frac = 0.0
            cur = next((p for p in self.state["phases"]
                        if p["status"] == "RUNNING"), None)
            if cur and cur["nodes"]:
                terminal = {"PUBLISHED", "COMPLETE", "PARTIAL", "FAILED",
                            "BLOCKED", "SKIPPED_APPROVED", "NOT_READY"}
                frac = sum(1 for n in cur["nodes"]
                           if n["status"] in terminal) / len(cur["nodes"])
            pct = 0.0 if total == 0 else 100.0 * min(1.0, (done + frac) / total)
            self.state["progress"] = round(pct)

    def _phase(self, phase: int) -> dict[str, Any]:
        with self._lock:
            for p in self.state["phases"]:
                if p["phase"] == phase:
                    return p
            p = {"phase": phase, "status": "PENDING",
                 "nodes": [], "decision": None, "note": ""}
            self.state["phases"].append(p)
            return p

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return json_copy(self.state)

    # -- execution ------------------------------------------------------------

    def start(self) -> None:
        self.thread = threading.Thread(target=self._execute, daemon=True)
        self.thread.start()

    def _execute(self) -> None:
        try:
            self._update(status="RUNNING", started_at=_now())
            self._log(f"job {self.job_id} accepted — repo: {self.repo_input} "
                      f"(decision_mode={self.decision_mode}, include_p6={self.include_p6})")
            self._run_all()
            self._update(status="COMPLETED", finished_at=_now())
            self._set_stage("DONE", "completed")
            with self._lock:
                self.state["progress"] = 100
            self._log("pipeline run COMPLETED — outcome bundle ready for download")
        except Exception as exc:  # surface to the UI, never crash the server
            import traceback
            tail = traceback.format_exc().strip().splitlines()[-1]
            self._update(status="FAILED", error=f"{type(exc).__name__}: {exc}",
                         finished_at=_now())
            self._set_stage("DONE", "failed")
            self._log(f"job FAILED: {type(exc).__name__}: {exc}", level="error")
            self._log(f"cause: {tail}", level="error")

    def _resolve_repo(self) -> tuple[Path, str]:
        """Local path, or git URL cloned (depth 1) into runs/incoming/."""
        incoming = self.runs_root / "incoming"
        incoming.mkdir(parents=True, exist_ok=True)
        candidate = Path(self.repo_input)
        if candidate.exists() and candidate.is_dir():
            app = self.app_id or candidate.name
            self._log(f"using local repository: {candidate}")
            return candidate, app
        if re.match(r"^(https?://|git@)", self.repo_input):
            name = re.sub(r"[^A-Za-z0-9._-]+", "-",
                          self.repo_input.rstrip("/").split("/")[-1].removesuffix(".git"))
            target = incoming / f"{name}-{uuid.uuid4().hex[:6]}"
            self._set_stage("CLONING", self.repo_input)
            self._log(f"cloning {self.repo_input} (shallow, depth 1) — large "
                      "repos can take a few minutes…")
            t0 = time.time()
            env = {**__import__("os").environ, "GIT_TERMINAL_PROMPT": "0"}
            proc = subprocess.run(
                ["git", "-c", "core.longpaths=true", "clone", "--depth", "1",
                 "--single-branch", self.repo_input, str(target)],
                capture_output=True, text=True, timeout=1800, env=env)
            if proc.returncode != 0:
                stderr_tail = (proc.stderr or "").strip().splitlines()[-5:]
                raise RuntimeError(
                    f"git clone failed: {' | '.join(stderr_tail) or proc.returncode}")
            self._log(f"clone done in {time.time() - t0:.1f}s → {target}")
            app = self.app_id or name
            return target, app
        raise ValueError(f"repo not found and not a git URL: {self.repo_input}")

    def _run_all(self) -> None:
        repo, app = self._resolve_repo()
        self._update(app_id=app)
        registry = resolve_registry()
        policy = PolicyService()
        work = self.runs_root / "ui" / self.job_id
        work.mkdir(parents=True, exist_ok=True)
        store = ArtifactStore(work / "store")
        audit = AuditJournal(work / "audit")
        self.state["facts"]["store_path"] = str(work / "store")

        def run_phase(phase: int, runner, run_app: str, run_inputs: dict,
                      overrides: dict, na_ok: bool = False) -> tuple[ArtifactStore, RunContext]:
            pstate = self._phase(phase)
            pstate["status"] = "RUNNING"
            orch = PhaseOrchestrator(registry["phases"][phase], store, policy, audit,
                                     runner, gate_overrides=overrides)
            node_kind = {}
            for a in registry["phases"][phase]["agents"]:
                node_kind[a["local_id"]] = a.get("kind", "agent")
            self._set_stage("RUNNING", f"Phase {phase} — {_PHASE_NAME.get(phase, '')}",
                            phase=phase)
            self._log(f"Phase {phase} ({_PHASE_NAME.get(phase, '')}) started")

            def on_event(ctx, ev):
                nodes = pstate["nodes"]
                for n in nodes:
                    if n["id"] == ev.get("node"):
                        n["status"] = ev.get("status", n["status"])
                        break
                else:
                    nodes.append({"id": ev.get("node", "?"),
                                  "status": ev.get("status", "?")})
                kind = node_kind.get(ev.get("node"), "agent")
                msg = f"P{phase} {ev.get('node', '?')} → {ev.get('status', '?')}"
                if ev.get("gate_outcome"):
                    msg += f" ({ev['gate_outcome']}"
                    if ev.get("reasons"):
                        msg += f": {', '.join(str(r) for r in ev['reasons'][:2])}"
                    msg += ")"
                by_design = (na_ok and ev.get("node") == "G0"
                             and ev.get("status") == "FAILED")
                if by_design:
                    msg += " — expected on the approved no-data route"
                level = ("error" if ev.get("status") in ("FAILED", "BLOCKED")
                         and not by_design
                         else "gate" if kind in ("gate", "execution") else "info")
                self._log(msg, level=level)
                self._recompute_progress()

            ctx = orch.start_run(f"{self.job_id}-p{phase}", run_app, run_inputs)
            pstate["nodes"] = [{"id": nid, "status": ns.status}
                               for nid, ns in sorted(ctx.state.nodes.items())]
            self._recompute_progress()
            orch.run(ctx, on_event=on_event)
            pstate["nodes"] = [{"id": nid, "status": ns.status}
                               for nid, ns in sorted(ctx.state.nodes.items())]
            failed = [e for e in ctx.outcome_log if e["status"] == "FAILED"]
            if failed and pstate["status"] != "N/A" and not na_ok:
                pstate["status"] = "FAILED"
                pstate["note"] = f"failed nodes: {[e['node'] for e in failed]}"
                self._log(f"Phase {phase} FAILED — nodes: "
                          f"{[e['node'] for e in failed]}", level="error")
            else:
                pstate["status"] = "N/A" if pstate["status"] == "N/A" else "COMPLETED"
                self._log(f"Phase {phase} {pstate['status']} "
                          f"({len(pstate['nodes'])} nodes executed)")
            self._recompute_progress()
            return store, ctx

        # ---------------- P1 ------------------------------------------------
        r1 = P1AgentRunner(confirmed_stakeholder=self.decision_mode)
        r1.bind_repo(repo)
        store, _ = run_phase(1, r1, app, {
            "scope_manifest": {"workload_ids": [app], "route": "derived-at-A5",
                               "boundaries": "user-supplied repo, read-only"},
            "source_pins": {"repo_path": str(repo)},
        }, P1_GATE_OVERRIDES)
        p1_g2 = store.get(f"P1/{app}/G2")["payload"]["decision_record"]
        p1_a1 = store.get(f"P1/{app}/A1")
        p1_a3 = store.get(f"P1/{app}/A3")
        p1_a5 = store.get(f"P1/{app}/A5")
        self._gate(1, p1_g2["status"])
        self.state["facts"].update({
            "loc": p1_a1["payload"]["repositories"][0].get("loc", 0),
            "files": p1_a1["payload"]["repositories"][0].get("files", 0),
            "route": p1_a5["payload"]["capability_route"],
            "dependencies": len(p1_a1["payload"]["dependencies"]),
        })
        self._log(f"discovery facts: {self.state['facts']['files']} files, "
                  f"{self.state['facts']['loc']} LOC, route="
                  f"{self.state['facts']['route']}, "
                  f"{self.state['facts']['dependencies']} dependencies")
        if p1_g2["status"] == "HOLD":
            raise RuntimeError("P1 released HOLD — downstream phases not admitted")

        # ---------------- P2 -------------------------------------------------
        repo0 = p1_a1["payload"]["repositories"][0]
        apps = [PortfolioApp(
            app_id=app, p1_g2_status=p1_g2["status"],
            loc=self.state["facts"]["loc"],
            languages=max(1, sum(1 for k in repo0.get("languages", {}) if k in CODE_LANGUAGES)),
            dependencies=self.state["facts"]["dependencies"],
            tests=int(p1_a1["payload"].get("coverage", {}).get("test_files", 0)),
            route=p1_a5["payload"]["capability_route"],
            has_data_layer=bool(p1_a3["payload"]["datasets"]),
            primary_language=_primary_lang(p1_a1), source_family="solo",
            p1_manifest_hash=store.get(f"P1/{app}/G1")["payload"]["evidence_manifest"]["manifest_hash"],
        )]
        store, _ = run_phase(2, P2AgentRunner(apps), "PF1", {
            "scope_manifest": {"portfolio_id": "PF1"},
            "p1_packages": [{"application_id": app, "schema_version": "P1.discovery.v3.0",
                             "g2_status": p1_g2["status"],
                             "manifest_hash": apps[0].p1_manifest_hash}],
            "p1_scope": {app: p1_g2["status"]},
        }, P2_GATE_OVERRIDES)
        p2_g2 = store.get("P2/PF1/G2")["payload"]["decision_record"]
        disposition = next((e["route"] for e in
                            store.get("P2/PF1/A7")["payload"]["route_register"]
                            if e["application_id"] == app), "Replatform")
        self.state["facts"]["disposition"] = disposition
        self._log(f"portfolio decision: {app} → {disposition}")
        self._gate(2, p2_g2["status"])
        if app not in p2_g2.get("authorized_apps", []):
            raise RuntimeError(
                f"P2 did not authorize {app} (status={p2_g2['status']}); "
                "enable decision mode or inspect the route register")

        # ---------------- P3 ---------------------------------------------------
        routes = [r["endpoint"] for r in p1_a3["payload"]["integrations"]][:12]
        datasets = [d["name"] for d in p1_a3["payload"]["datasets"]][:8]
        components = [c["name"] for c in p1_a1["payload"]["components"][:5]]
        store, _ = run_phase(3, P3AgentRunner({
            "app_id": app, "disposition": disposition,
            "primary_language": _primary_lang(p1_a1),
            "route": apps[0].route, "components": components,
            "routes": routes, "datasets": datasets,
        }), app, {
            "scope_manifest": {"workload_ids": [app]},
            "p2_package": {"application_id": app, "authorized": True,
                           "disposition": disposition,
                           "candidate_hash": p2_g2["candidate_hash"]},
        }, P3_GATE_OVERRIDES)
        p3_g2 = store.get(f"P3/{app}/G2")["payload"]["decision_record"]
        self._gate(3, p3_g2["status"])

        # ---------------- P4 ------------------------------------------------------
        store, _ = run_phase(4, P4AgentRunner({
            "app_id": app, "disposition": disposition, "wave": "W1",
        }), app, {
            "scope_manifest": {"workload_ids": [app]},
            "p3_package": {"application_id": app, "status": p3_g2["status"],
                           "conditions": p3_g2.get("conditions", [])},
        }, P4_GATE_OVERRIDES)
        p4_g2 = store.get(f"P4/{app}/G2")["payload"]["decision_record"]
        self._gate(4, p4_g2["status"])

        # ---------------- P5 ---------------------------------------------------------
        store, _ = run_phase(5, P5AgentRunner({
            "app_id": app, "disposition": disposition, "repo_path": str(repo),
            "routes": routes, "datasets": datasets,
            "dependencies": p1_a1["payload"]["dependencies"],
            "tests": p1_a1["payload"].get("coverage", {}).get("test_paths", []),
            "pinned_commit": repo0.get("commit") or "unpinned",
            "route": apps[0].route,
        }), app, {
            "scope_manifest": {"workload_ids": [app]},
            "p4_package": {"application_id": app, "status": p4_g2["status"]},
            "execution_permit": {"granted": True,
                                 "scope": "repo+manifest+test sandbox",
                                 "issuer": "pilot operator (simulated)"},
        }, P5_GATE_OVERRIDES)
        p5_g4 = store.get(f"P5/{app}/G4")["payload"]["decision_record"]
        p5_g3 = store.get(f"P5/{app}/G3")["payload"]["final_manifest"]
        self._gate(5, p5_g4["status"])

        # ---------------- P6 ------------------------------------------------------------
        if not self.include_p6:
            self._phase(6)["note"] = "skipped by user"
            self._phase(6)["status"] = "SKIPPED"
            return
        seed = _find_seed_sql(repo)
        if seed is None:
            self._log("P6: no seed SQL found in repo — approved no-data route")
            run_phase(6, P6AgentRunner({"app_id": app, "route": "no-data",
                                        "tables": []}), app, {
                "scope_manifest": {"workload_ids": [app]},
                "p5_package": {"application_id": app, "status": p5_g4["status"]},
                "data_brief": {"app_id": app, "route": "no-data"},
                "migration_permit": {"granted": False},
            }, P6_GATE_OVERRIDES, na_ok=True)
            # G0 fails BY DESIGN on the no-data route (N/A outside the active
            # graph) — present it as the approved N/A package, not a failure
            p6state = self._phase(6)
            p6state["status"] = "N/A"
            p6state["note"] = ("no seed data found — approved no-data route "
                               "(P6 G0 emits N/A package outside the active graph)")
            self._gate(6, "N/A_ROUTE (no data)")
            return

        src_db, dst_db, table_defs, total_rows = _build_fixture(seed, work)
        self.state["facts"]["seed_rows"] = total_rows
        self.state["facts"]["seed_tables"] = len(table_defs)
        self._log(f"P6: built sqlite fixture from {seed.name} — "
                  f"{len(table_defs)} tables, {total_rows} rows to migrate")
        run_phase(6, P6AgentRunner({
            "app_id": app, "route": "batch",
            "source_db": str(src_db), "target_db": str(dst_db),
            "tables": table_defs, "p5_build_digest": p5_g3["build_digest"],
        }), app, {
            "scope_manifest": {"workload_ids": [app]},
            "p5_package": {"application_id": app, "status": p5_g4["status"]},
            "data_brief": {"app_id": app, "route": "batch",
                           "source_db": str(src_db), "target_db": str(dst_db),
                           "tables": table_defs},
            "migration_permit": {"granted": True, "issuer": "pilot operator (simulated)"},
        }, P6_GATE_OVERRIDES)
        try:
            p6_g3 = store.get(f"P6/{app}/G3")["payload"]["decision_record"]
            self._gate(6, p6_g3["status"])
        except Exception:
            self._gate(6, "FAILED")

    def _gate(self, phase: int, decision: str) -> None:
        with self._lock:
            self.state["gate_chain"].append(
                {"phase": phase, "gate": _gate_of(phase), "decision": decision})
        self._log(f"P{phase} release gate {_gate_of(phase)} → {decision}",
                  level="gate")


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def json_copy(obj):
    import json
    return json.loads(json.dumps(obj, default=str))


def _primary_lang(a1) -> str:
    primary = a1["payload"]["repositories"][0].get("primary_language")
    if primary:
        return primary
    for f in a1["findings"]:
        if "primary:" in f["statement"]:
            return f["statement"].split("primary:")[-1].strip()
    return "unknown"


def _find_seed_sql(repo: Path) -> Path | None:
    """Best-effort seed data: prefer data.sql with INSERTs."""
    candidates = sorted(repo.rglob("*.sql"))
    best: Path | None = None
    for p in candidates:
        try:
            if "INSERT INTO" in p.read_text(encoding="utf-8", errors="ignore")[:200_000]:
                if p.name.lower().startswith("data"):
                    return p
                best = best or p
        except OSError:
            continue
    return best


def _build_fixture(seed: Path, work: Path):
    """Parse INSERT statements into a sqlite source fixture + empty target."""
    src_db = work / "source.sqlite"
    dst_db = work / "target.sqlite"
    for p in (src_db, dst_db):
        if p.exists():
            p.unlink()
    text = seed.read_text(encoding="utf-8", errors="ignore")
    inserts = re.findall(r"INSERT INTO (\w+) VALUES \(([^;]*)\);", text)
    if not inserts:
        raise ValueError(f"no INSERT statements parsed from {seed}")
    tables: dict[str, int] = {}
    rows: dict[str, list[list]] = {}
    for table, values in inserts:
        vals: list[Any] = []
        for raw in re.findall(r"'(?:[^']|'')*'|[^,]+", values):
            raw = raw.strip()
            if raw == "default":
                vals.append(None)
            elif raw.startswith("'"):
                vals.append(raw.replace("''", "'")[1:-1])
            else:
                vals.append(raw)
        tables[table] = max(tables.get(table, 0), len(vals))
        rows.setdefault(table, []).append(vals)

    def create(con: sqlite3.Connection):
        for t, n in tables.items():
            has_id = any(v[0] is None for v in rows.get(t, []))
            decl = ", ".join((["id INTEGER PRIMARY KEY AUTOINCREMENT"] if has_id else [])
                             + [f"c{i} TEXT" for i in range(1 if has_id else 0, n)])
            con.execute(f'CREATE TABLE "{t}" ({decl})')

    con = sqlite3.connect(str(src_db))
    create(con)
    for t, rlist in rows.items():
        n = tables[t]
        ph = ", ".join("?" for _ in range(n))
        con.executemany(f'INSERT INTO "{t}" VALUES ({ph})', rlist)
    con.commit()
    con.close()
    dcon = sqlite3.connect(str(dst_db))
    create(dcon)
    dcon.commit()
    dcon.close()
    return src_db, dst_db, [{"name": t, "columns": n} for t, n in sorted(tables.items())], \
        sum(len(r) for r in rows.values())
