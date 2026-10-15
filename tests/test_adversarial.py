"""Parametrized adversarial suite (C8) — same cases as scripts/adversarial_run.py."""

from pathlib import Path

import pytest

from appmod.evals.adversarial import CASES, case_by_id, run_all, run_case
from appmod.evals.confidence import score
from appmod.evals.run import components


@pytest.mark.parametrize("case_id", [c.id for c in CASES], ids=[c.id for c in CASES])
def test_adversarial_case(case_id: str, tmp_path: Path) -> None:
    case = case_by_id()[case_id]
    row = run_case(case, tmp_path)
    assert row["pass"], row.get("error", "")


def test_adversarial_registry_has_fifty_cases() -> None:
    assert len(CASES) >= 50
    cats = {c.category for c in CASES}
    assert cats >= {"injection", "secrets", "symlink", "poisoned_deps", "contradictory", "large_binary"}


def test_adversarial_report_assesses_c8() -> None:
    result = {"schema_valid_after_repair": {"valid": 1, "total": 1},
              "evidence_resolvability": {"resolved": 1, "cited": 1},
              "hallucinated_paths": {"count": 0, "checked": 1},
              "hallucinated_symbols": {"count": 0, "checked": 1}, "golden_agreement": {}}
    adv = run_all()
    c8 = next(c for c in score(components(result, [], None, adv))["components"] if c["id"] == "C8")
    assert c8["assessed"]
    assert adv["failed"] == 0
    m = c8["measures"][0]
    assert m["k"] == m["n"] == adv["total"]
