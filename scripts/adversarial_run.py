"""Offline adversarial suite (C8): runs every fixture case and writes a report.

    python scripts/adversarial_run.py --label pr8

Pass the json to scripts/eval_run.py --adversarial to score C8.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from appmod.evals.adversarial import run_all, to_md  # noqa: E402

OUT = ROOT / "docs" / "runs"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    args = ap.parse_args()
    result = run_all()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"adversarial-{args.label}.json").write_text(json.dumps(result, indent=2))
    (OUT / f"adversarial-{args.label}.md").write_text(to_md(result, args.label))
    m = result["measures"][0]
    print(f"{m['name']}: {m['k']}/{m['n']} (LB {m['lower_bound']}%)")
    print(f"report docs/runs/adversarial-{args.label}.md")
    return 0 if result["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
