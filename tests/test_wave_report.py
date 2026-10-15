"""The wave report publishes tune and holdout separately and does not invent a component."""

import json
from pathlib import Path

from appmod.evals.confidence import COMPONENTS
from appmod.evals.wave import apply_measurements, measured_cells, render_split, report_ok


def _component(cid: str, assessed: bool = True, k: int = 9, n: int = 10) -> dict:
    return {"id": cid, "name": COMPONENTS[cid], "assessed": assessed,
            "lower_bound": 80.0 if assessed else 0.0, "reason": "" if assessed else "no data",
            "measures": [{"name": cid, "k": k, "n": n, "lower_bound": 80.0}] if assessed else []}


def _eval(job: str, passed: bool = True, drop: str | None = None) -> dict:
    components = [_component("C4", assessed=False, k=0, n=0) if cid == "C4" else _component(cid)
                  for cid in COMPONENTS]
    if drop:
        components = [c for c in components if c["id"] != drop]
    return {"job": job, "pass": passed, "confidence": {"components": components}}


def _e2e(rate: float, job: str = "job-tune") -> dict:
    return {"job_id": job, "summary": {"success_rate": rate}}


def _stability() -> dict:
    return {"measures": [
        {"name": "P2 A6 disposition identical across runs", "k": 18, "n": 20, "lower_bound": 0.9},
        {"name": "P3 A2 boundary Jaccard >= 0.8", "k": 10, "n": 16, "lower_bound": 0.5},
    ]}


def test_tune_and_holdout_reports_stay_separate():
    tune = render_split("tune", _e2e(100.0, "job-tune"), _eval("job-tune"), _stability())
    holdout = render_split("holdout", _e2e(98.5, "job-hold"), _eval("job-hold"))
    assert "job-tune" in tune and "job-hold" not in tune
    assert "job-hold" in holdout and "P2 A6 disposition" not in holdout
    assert "not assessed" in tune
    assert "C5 is not re-measured" in holdout
    assert "PASS" in tune and "18/20" in tune
    assert report_ok(_e2e(97.0), _eval("j")) is False
    assert report_ok(_e2e(97.1), _eval("j", passed=False)) is False


def test_roadmap_gains_a_measured_column_and_keeps_the_baseline(tmp_path: Path):
    roadmap = Path("docs/NEXT_LEVEL_AGENTIC_ROADMAP.md").read_text()
    updated = apply_measurements(roadmap, measured_cells(_eval("job-hold"), _stability()))
    assert "| Component | Today | Measured this wave | Target | Unlocked by |" in updated
    assert "19 %" in updated
    assert "not assessed" in updated
    assert "50.0 % LB weakest (P3 A2 boundary Jaccard >= 0.8 10/16)" in updated
    assert "## 5. Sequenced roadmap" in updated
    assert updated != roadmap


def test_script_writes_two_reports(tmp_path: Path):
    import subprocess
    import sys
    for name, doc in {
        "tune-e2e.json": _e2e(100.0, "job-tune"),
        "tune-eval.json": _eval("job-tune"),
        "holdout-e2e.json": _e2e(99.0, "job-hold"),
        "holdout-eval.json": _eval("job-hold"),
        "stability.json": _stability(),
    }.items():
        (tmp_path / name).write_text(json.dumps(doc))
    roadmap = tmp_path / "roadmap.md"
    roadmap.write_text(Path("docs/NEXT_LEVEL_AGENTIC_ROADMAP.md").read_text())
    proc = subprocess.run(
        [sys.executable, "scripts/wave_report.py",
         "--tune-e2e", str(tmp_path / "tune-e2e.json"),
         "--tune-eval", str(tmp_path / "tune-eval.json"),
         "--holdout-e2e", str(tmp_path / "holdout-e2e.json"),
         "--holdout-eval", str(tmp_path / "holdout-eval.json"),
         "--stability", str(tmp_path / "stability.json"),
         "--roadmap", str(roadmap),
         "--out-dir", str(tmp_path / "out")],
        check=False, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    tune = (tmp_path / "out" / "wave-w1w2-tune.md").read_text()
    holdout = (tmp_path / "out" / "wave-w1w2-holdout.md").read_text()
    assert "job-tune" in tune and "job-hold" in holdout
    assert "Measured this wave" in roadmap.read_text()
