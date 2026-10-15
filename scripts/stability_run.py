"""Stability harness (C5): repeat live runs at one pipeline version and compare decisions.

    # launch N fresh cache-off replicates of the tune split, then compare
    python scripts/stability_run.py --label s1 --n 5 --corpus tune

    # compare replicates that already ran; a replicate is a comma-separated list of jobs
    python scripts/stability_run.py --label s1 \
        --replicate runs/e2e-run5-root:job-A@d6aad7a --replicate runs/e2e-run6-root:job-B,runs/e2e-run6-root:job-C

`@REF` names the git commit a job ran at, when its e2e report predates pipeline_version.

Fresh replicates of the full corpus run the tune and holdout splits as two jobs each (the
server takes at most 25 repos per run). Writes docs/runs/stability-<label>.{json,md}; pass the
json to scripts/eval_run.py --stability to score C5.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from appmod.evals.stability import compare, merge, pipeline_version, snapshot, to_md  # noqa: E402

OUT = ROOT / "docs" / "runs"


def recorded_version(job: str, ref: str | None) -> str:
    if ref:
        return pipeline_version(ref)
    for p in OUT.glob("e2e-*.json"):
        doc = json.loads(p.read_text())
        if doc.get("job_id") == job:
            return str(doc.get("pipeline_version") or "unrecorded")
    return "unrecorded"


def launch(label: str, corpus: str, args: argparse.Namespace, runs_dir: Path) -> str:
    cmd = [sys.executable, str(ROOT / "scripts" / "e2e_agentic.py"), "--label", label, "--cache", "off",
           "--corpus", corpus, "--timeout", str(args.timeout), "--parallel-apps", str(args.parallel_apps),
           "--parallel-agents", str(args.parallel_agents)]
    subprocess.run(cmd, cwd=ROOT, env={**os.environ, "APPMOD_RUNS_DIR": str(runs_dir)}, check=False)
    report = json.loads((OUT / f"e2e-{label}.json").read_text())
    if report.get("job_status") != "COMPLETED":
        raise SystemExit(f"{label}: job {report.get('job_id')} ended {report.get('job_status')}")
    return str(report["job_id"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--replicate", action="append", default=[], metavar="RUNS_DIR:JOB[,RUNS_DIR:JOB]")
    ap.add_argument("--n", type=int, default=0, help="fresh cache-off replicates to launch")
    ap.add_argument("--corpus", choices=["tune", "holdout", "all"], default="tune")
    ap.add_argument("--timeout", type=int, default=36000)
    ap.add_argument("--parallel-apps", type=int, default=5)
    ap.add_argument("--parallel-agents", type=int, default=4)
    args = ap.parse_args()

    replicates: list[list[tuple[Path, str, str | None]]] = []
    for spec in args.replicate:
        rep = []
        for part in spec.split(","):
            where, _, job = part.rpartition(":")
            job, _, ref = job.partition("@")
            rep.append((Path(where), job, ref or None))
        replicates.append(rep)
    if args.n:
        version = pipeline_version()
        if version.endswith("+dirty"):
            raise SystemExit("pipeline code has uncommitted changes; commit before launching replicates")
        runs_dir = ROOT / "runs" / f"stability-{args.label}-root"
        splits = ["tune", "holdout"] if args.corpus == "all" else [args.corpus]
        for i in range(1, args.n + 1):
            replicates.append([(runs_dir, launch(f"{args.label}-r{i}-{s}", s, args, runs_dir), None)
                               for s in splits])
    if len(replicates) < 2:
        raise SystemExit("need at least two replicates")

    result = compare([merge([snapshot(d, j) for d, j, _ in rep]) for rep in replicates])
    result["jobs"] = [[{"runs_dir": str(d), "job": j, "pipeline_version": recorded_version(j, ref)}
                       for d, j, ref in rep] for rep in replicates]
    result["pipeline_versions"] = sorted({j["pipeline_version"] for rep in result["jobs"] for j in rep})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"stability-{args.label}.json").write_text(json.dumps(result, indent=2))
    (OUT / f"stability-{args.label}.md").write_text(to_md(result, args.label))
    for m in result["measures"]:
        print(f"{m['name']}: {m['k']}/{m['n']} (LB {m['lower_bound']}%)")
    print(f"report docs/runs/stability-{args.label}.md")
    known = [v for v in result["pipeline_versions"] if v != "unrecorded"]
    return 1 if len(known) > 1 else 0


if __name__ == "__main__":
    raise SystemExit(main())
