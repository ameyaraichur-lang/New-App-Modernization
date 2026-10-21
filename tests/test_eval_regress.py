"""The eval regression gate fails a deliberately worse component result."""

import json
from pathlib import Path

from appmod.agents.llm_runner import DEGRADE_RULES, operating_rules
from appmod.evals.regress import regressions, route_flips


def _report(k: int, n: int, *, assessed: bool = True) -> dict:
    return {"pass": True, "confidence": {"components": [
        {"id": "C1", "assessed": assessed, "lower_bound": 90, "measures": [
            {"name": "schema valid after repair", "k": k, "n": n}]},
        {"id": "C2", "assessed": False, "lower_bound": 0, "measures": []},
    ]}}


def test_route_flips_are_listed_and_do_not_invent_a_change():
    previous = {"app_facts": {"a": {"disposition": "Refactor"}, "b": {"disposition": "Retain"}}}
    current = {"app_facts": {"a": {"disposition": "Rebuild"}, "b": {"disposition": "Retain"},
                             "c": {"disposition": "Retire"}}}
    assert route_flips(previous, current) == ["a: Refactor -> Rebuild"]


def test_degraded_component_fails_the_gate():
    problems = regressions(_report(10, 10), _report(9, 10))
    assert any(p.startswith("C1 failures") for p in problems)
    assert any("point estimate" in p for p in problems)


def test_equal_or_better_component_passes():
    assert regressions(_report(9, 10), _report(9, 10)) == []
    assert regressions(_report(9, 10), _report(10, 10)) == []


def test_losing_an_assessed_component_fails():
    assert regressions(_report(10, 10), _report(10, 10, assessed=False))


def test_step33_failure_exits(tmp_path: Path):
    import subprocess
    import sys
    report = tmp_path / "eval.json"
    report.write_text(json.dumps({"pass": False, "confidence": {"components": []}}))
    proc = subprocess.run([sys.executable, "scripts/eval_regress.py", "--current", str(report)],
                          capture_output=True, text=True)
    assert proc.returncode == 1
    assert "Step 33" in proc.stdout


def test_degraded_prompt_changes_agent_rules(monkeypatch):
    monkeypatch.delenv("APPMOD_PROMPT_DEGRADE", raising=False)
    assert DEGRADE_RULES not in operating_rules()
    monkeypatch.setenv("APPMOD_PROMPT_DEGRADE", "1")
    assert "every application is COBOL" in operating_rules()
