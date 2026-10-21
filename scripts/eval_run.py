"""Eval of a finished run, from persisted state only (store + run DB + repos).

    python scripts/eval_run.py --runs-dir runs/e2e-run4-root --job job-… [--label run4]
        [--stability docs/runs/stability-<label>.json]   # scores C5

Writes docs/runs/eval-<label>.{json,md}, and verifier-audit-<label>.jsonl (the claim-support
audit sample, with an empty human_verdict per row). Metrics and thresholds: appmod/evals/run.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from appmod.evals.run import evaluate, to_md  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", type=Path, required=True)
    ap.add_argument("--job", required=True)
    ap.add_argument("--label", default="eval")
    ap.add_argument("--stability", type=Path, help="report from scripts/stability_run.py")
    args = ap.parse_args()
    r = evaluate(args.runs_dir, args.job, json.loads(args.stability.read_text()) if args.stability else None)
    out = ROOT / "docs" / "runs"
    (out / f"eval-{args.label}.json").write_text(json.dumps(r, indent=1))
    (out / f"eval-{args.label}.md").write_text(to_md(r, args.label))
    sample = r["claim_support"]["audit_sample"]
    if sample:
        (out / f"verifier-audit-{args.label}.jsonl").write_text(
            "".join(json.dumps(dict(s, human_verdict=None)) + "\n" for s in sample))
    print(to_md(r, args.label))
    return 0 if r["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
