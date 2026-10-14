"""Fail when an eval report regresses against the previous one.

    python scripts/eval_regress.py --current docs/runs/eval-run8.json \
        --previous docs/runs/eval-run7.json

With no --previous file, the Step 33 ``pass`` flag is still enforced and the component
comparison is skipped. That is how the first baseline is accepted.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from appmod.evals.regress import regressions, route_flips  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--current", type=Path, required=True)
    ap.add_argument("--previous", type=Path)
    ap.add_argument("--current-e2e", type=Path)
    ap.add_argument("--previous-e2e", type=Path)
    args = ap.parse_args()
    if args.current_e2e and args.previous_e2e and args.previous_e2e.exists():
        flips = route_flips(json.loads(args.previous_e2e.read_text()),
                            json.loads(args.current_e2e.read_text()))
        print("P2 route changes:" if flips else "P2 route changes: none")
        print("\n".join(f"- {flip}" for flip in flips))
    current = json.loads(args.current.read_text())
    if not current.get("pass"):
        print("Step 33 gate failed")
        return 1
    if args.previous is None or not args.previous.exists():
        print("no previous eval; component comparison skipped")
        return 0
    problems = regressions(json.loads(args.previous.read_text()), current)
    if problems:
        print("component regression:")
        print("\n".join(f"- {p}" for p in problems))
        return 1
    print("no component regression")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
