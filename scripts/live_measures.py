"""Check the live done-when items a finished corpus job can already answer.

    python scripts/live_measures.py --runs-dir runs/e2e-root --job job-… --require critique
    python scripts/live_measures.py --eval docs/runs/eval.json --require evidence
    python scripts/live_measures.py --e2e docs/runs/e2e.json --require ofbiz
    python scripts/live_measures.py --stability docs/runs/stability.json --require routes

Exits 1 when a required check has no observations or misses its threshold.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from appmod.evals.measures import (  # noqa: E402
    STRUCTURE_ROLES, critique_convergence, first_pass_validity, observed_share, ofbiz_completed,
    read_audit, route_agreement)
from appmod.store.artifact_store import ArtifactStore  # noqa: E402


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def _structure_artifacts(runs_dir: Path, job: str) -> list[dict]:
    db = sqlite3.connect(f"file:{runs_dir / 'appmod.db'}?immutable=1", uri=True)
    row = db.execute("SELECT state FROM jobs WHERE job_id=?", (job,)).fetchone()
    db.close()
    if row is None:
        raise SystemExit(f"no job {job} in {runs_dir}")
    state = json.loads(row[0])
    store = ArtifactStore(Path(state["facts"]["store_path"]))
    apps = state["apps"]
    found = []
    for phase, local in STRUCTURE_ROLES:
        for app in (["PF1"] if phase == 2 else apps):
            aid = f"P{phase}/{app}/{local}"
            if not store.versions(aid):
                continue
            art = store.get(aid)
            found.append({"phase": phase, "app": app, "agent": local,
                          "llm": (art.get("execution_metadata") or {}).get("llm") or {}})
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", type=Path)
    ap.add_argument("--job")
    ap.add_argument("--eval", type=Path)
    ap.add_argument("--e2e", type=Path)
    ap.add_argument("--stability", type=Path)
    ap.add_argument("--require", action="append", default=[],
                    choices=("critique", "first-pass", "evidence", "ofbiz", "routes"))
    args = ap.parse_args()
    report: dict[str, dict] = {}
    if "critique" in args.require or "first-pass" in args.require:
        if args.runs_dir is None or not args.job:
            raise SystemExit("--runs-dir and --job are required for critique and first-pass")
    if "critique" in args.require:
        audit = args.runs_dir / "ui" / args.job / "audit"
        report["critique"] = critique_convergence(read_audit(audit))
    if "first-pass" in args.require:
        report["first-pass"] = first_pass_validity(_structure_artifacts(args.runs_dir, args.job))
    if "evidence" in args.require:
        if args.eval is None:
            raise SystemExit("--eval is required for the evidence-share check")
        report["evidence"] = observed_share(_load(args.eval))
    if "ofbiz" in args.require:
        if args.e2e is None:
            raise SystemExit("--e2e is required for the OFBiz check")
        report["ofbiz"] = ofbiz_completed(_load(args.e2e))
    if "routes" in args.require:
        if args.stability is None:
            raise SystemExit("--stability is required for the route-agreement check")
        report["routes"] = route_agreement(_load(args.stability))
    print(json.dumps(report, indent=1, default=str))
    failed = [name for name in args.require if not report.get(name, {}).get("pass")]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
