"""Write the tune report, the held-out report, and the roadmap §4 measured column.

    python scripts/wave_report.py \
        --tune-e2e docs/runs/e2e-wave-tune.json --tune-eval docs/runs/eval-wave-tune.json \
        --holdout-e2e docs/runs/e2e-wave-holdout.json --holdout-eval docs/runs/eval-wave-holdout.json \
        --stability docs/runs/stability-wave.json

Exits non-zero when dispatch is at or below 97 % or the Step 33 gate fails.
Held-out numbers are written to their own file.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from appmod.evals.wave import apply_measurements, measured_cells, render_split, report_ok  # noqa: E402


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tune-e2e", type=Path, required=True)
    ap.add_argument("--tune-eval", type=Path, required=True)
    ap.add_argument("--holdout-e2e", type=Path, required=True)
    ap.add_argument("--holdout-eval", type=Path, required=True)
    ap.add_argument("--stability", type=Path, required=True)
    ap.add_argument("--roadmap", type=Path, default=ROOT / "docs" / "NEXT_LEVEL_AGENTIC_ROADMAP.md")
    ap.add_argument("--out-dir", type=Path, default=ROOT / "docs" / "runs")
    args = ap.parse_args()
    tune_e2e, tune_eval = _load(args.tune_e2e), _load(args.tune_eval)
    holdout_e2e, holdout_eval = _load(args.holdout_e2e), _load(args.holdout_eval)
    stability = _load(args.stability)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    tune_path = args.out_dir / "wave-w1w2-tune.md"
    holdout_path = args.out_dir / "wave-w1w2-holdout.md"
    tune_path.write_text(render_split("tune", tune_e2e, tune_eval, stability))
    holdout_path.write_text(render_split("holdout", holdout_e2e, holdout_eval))
    roadmap = apply_measurements(args.roadmap.read_text(), measured_cells(holdout_eval, stability))
    args.roadmap.write_text(roadmap)
    print(tune_path)
    print(holdout_path)
    ok = report_ok(tune_e2e, tune_eval) and report_ok(holdout_e2e, holdout_eval)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
