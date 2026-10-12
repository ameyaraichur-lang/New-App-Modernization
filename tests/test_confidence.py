import pytest

from appmod.evals.confidence import COMPONENTS, Component, Measure, score
from appmod.evals.run import components
from appmod.evals.stats import wilson_lower


@pytest.mark.parametrize("k,n,want", [(270, 270, 98.6), (39, 40, 87.1), (860, 860, 99.6),
                                      (351, 351, 98.9), (381, 381, 99.0), (100, 100, 96.3)])
def test_wilson_lower_bounds_match_the_roadmap(k, n, want):
    assert round(100 * wilson_lower(k, n), 1) == want


def test_wilson_lower_edges():
    assert wilson_lower(0, 0) is None
    assert wilson_lower(0, 10) == 0.0
    assert wilson_lower(5, 10) < 0.5 < 1.0


def _all(**over):
    base = {cid: Component(cid, [Measure("m", 100, 100)]) for cid in COMPONENTS}
    base.update(over)
    return list(base.values())


def test_score_is_the_weakest_component():
    r = score(_all(C2=Component("C2", [Measure("facts", 39, 40)])))
    assert r["weakest"] == "C2" and r["confidence_score"] == 87.12
    assert r["not_assessed"] == []


def test_unmeasured_component_scores_zero():
    r = score(_all(C4=Component("C4", reason="no labels")))
    assert r["confidence_score"] == 0.0 and r["weakest"] == "C4"
    assert r["not_assessed"] == ["C4"] and r["weakest_assessed"] == "C1"
    c4 = next(c for c in r["components"] if c["id"] == "C4")
    assert c4 == {"id": "C4", "name": "Decision correctness", "assessed": False,
                  "lower_bound": 0.0, "reason": "no labels", "measures": []}


def test_component_lower_bound_is_its_weakest_measure():
    c = Component("C1", [Measure("a", 270, 270), Measure("b", 860, 860), Measure("empty", 0, 0)])
    assert round(100 * c.lower, 1) == 98.6 and c.assessed


def test_score_requires_all_nine_components():
    with pytest.raises(ValueError, match="C9"):
        score(_all()[:8])


def _result(golden_rows):
    return {"schema_valid_after_repair": {"valid": 270, "total": 270},
            "evidence_resolvability": {"resolved": 14988, "cited": 14988},
            "hallucinated_paths": {"count": 0, "checked": 860},
            "hallucinated_symbols": {"count": 0, "checked": 351},
            "golden_agreement": {"f": {"rows": golden_rows}}}


def test_eval_components_map_run_results_and_ignore_scripted_reviews():
    rows = [{"ok": True}] * 39 + [{"ok": False}]
    cs = score(components(_result(rows), [("approve", "scripted-reviewer")] * 29))
    by = {c["id"]: c for c in cs["components"]}
    assert by["C1"]["assessed"] and by["C1"]["lower_bound"] == 98.6
    assert by["C2"]["lower_bound"] == 87.12
    assert not by["C9"]["assessed"] and "scripted" in by["C9"]["reason"]
    assert cs["not_assessed"] == ["C3", "C4", "C5", "C6", "C7", "C8", "C9"]
    assert cs["confidence_score"] == 0.0 and cs["weakest_assessed"] == "C2"


def test_human_reviews_count_toward_acceptance():
    cs = score(components(_result([{"ok": True}]), [("approve", "alice"), ("reject", "bob"),
                                                    ("approve", "scripted-reviewer")]))
    c9 = next(c for c in cs["components"] if c["id"] == "C9")
    assert c9["assessed"] and c9["measures"][0]["k"] == 1 and c9["measures"][0]["n"] == 2
