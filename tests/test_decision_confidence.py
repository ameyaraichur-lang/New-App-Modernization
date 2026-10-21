import ast
from pathlib import Path

from pytest import approx

from appmod.agents.llm_runner import _tag, clamp_confidence, submit_tool
from appmod.agents.overlays import OVERLAYS, _pp_p1_a11, _pp_p2_a6, _pp_p4_a3
from appmod.agents.grounding import walk
from appmod.evals.calibration import apply_map, ece, ece_upper, fit_map, summarize
from appmod.evals.confidence import Component, score
from appmod.evals.golden import Fact, confidence_pairs

ROOT = Path(__file__).resolve().parents[1]


def test_every_model_item_and_finding_asks_for_confidence():
    for phase, overlays in OVERLAYS.items():
        for aid, ov in overlays.items():
            for node in walk(ov.fields_schema()):
                props = node.get("properties", {})
                if "evidence_class" in props or "proposed_route" in props:
                    assert "confidence" in props and "confidence" in node["required"], (phase, aid)
    findings = submit_tool(OVERLAYS[1]["A1"], False).parameters["properties"]["findings"]["items"]
    assert "confidence" in findings["required"]


def test_confidence_is_clamped_or_dropped():
    assert [clamp_confidence(v) for v in (0.42, 1.7, -3, True, "high", None)] == [0.42, 1.0, 0.0, None, None, None]
    assert _tag({"x": 1, "confidence": 2})["confidence"] == 1.0
    assert "confidence" not in _tag({"x": 1})


def test_postprocess_hooks_keep_confidence():
    a11 = _pp_p1_a11({"risk_dimensions": [{"dimension": "technical", "score": 2}]},
                     {"risk_dimensions": [{"dimension": "technical", "score": 3, "basis": "b", "drivers": [],
                                           "evidence_class": "INFERRED", "evidence_ids": [], "confidence": 0.6}]}, {})
    assert a11["risk_dimensions"][0]["confidence"] == 0.6
    p2 = _pp_p2_a6({"decisions": [{"application_id": "a", "proposed_disposition": "Retain", "wave_id": None}]},
                   {"decisions": [{"application_id": "a", "proposed_disposition": "Refactor", "rationale": "r",
                                   "second_best": "Rehost", "why_not_second_best": "w", "wave": 1,
                                   "evidence_class": "INFERRED", "evidence_ids": [], "confidence": 0.7}]}, {})
    assert p2["decisions"][0]["confidence"] == 0.7
    p4 = _pp_p4_a3({"tasks": []}, {"tasks": [{"task_id": "L-T1", "phase": "P5", "kind": "k", "component": "c",
                                              "owner_role": "o", "acceptance": "a", "depends_on": [],
                                              "estimate_days": 2, "evidence_class": "INFERRED",
                                              "evidence_ids": [], "confidence": 0.5}]}, {})
    assert p4["tasks"][0]["confidence"] == 0.5


def test_ece_and_calibration_map():
    calibrated = [(0.8, True)] * 8 + [(0.8, False)] * 2
    assert ece(calibrated) == approx(0.0)
    overconfident = [(0.95, True)] * 6 + [(0.95, False)] * 4
    assert round(ece(overconfident) or 0, 2) == 0.35
    assert ece([]) is None
    upper = ece_upper(overconfident)
    assert upper is not None and upper >= 0.35 and upper == ece_upper(overconfident)
    cmap = fit_map(overconfident)
    assert ece(apply_map(cmap, overconfident)) == approx(0.0)
    s = summarize({"tune": overconfident, "holdout": overconfident})
    assert s["n"] == 20 and s["holdout"]["ece_mapped"] == 0.0 and s["holdout"]["ece_raw"] == 0.35


def test_fact_confidence_pairs():
    facts = [Fact("capability_route", "capability_route", "API_ONLY", "x"),
             Fact("entity", "Owner", True, "x"), Fact("route", "/owners/*", True, "x"),
             Fact("license", "license", "mit", "x"), Fact("dependency", "junit", True, "x")]
    payloads = {"A5": {"route_review": {"agrees": False, "proposed_route": "UI", "confidence": 0.8}}}
    items = [{"name": "Owner", "defined_in": "Owner.java", "confidence": 0.9, "origin": "llm"},
             {"statement": "GET /owners/{id} renders an owner", "confidence": 0.7, "origin": "llm"},
             {"statement": "mentions owners and an MIT License", "origin": "llm"},
             {"statement": "junit 5 is used", "confidence": 0.99, "origin": "llm"}]
    got = {p["type"]: p for p in confidence_pairs(facts, payloads, items)}
    assert got["capability_route"] == {"type": "capability_route", "key": "capability_route",
                                       "confidence": 0.8, "correct": False}
    assert got["entity"]["confidence"] == 0.9 and got["route"]["confidence"] == 0.7
    assert "license" not in got and "dependency" not in got


def test_c6_uses_its_own_bound():
    comps = [Component(c, reason="x") for c in ("C1", "C2", "C3", "C4", "C5", "C7", "C8", "C9")]
    comps.insert(5, Component("C6", value=0.82, basis="b"))
    c6 = next(c for c in score(comps)["components"] if c["id"] == "C6")
    assert c6["assessed"] and c6["lower_bound"] == 82.0 and c6["basis"] == "b"


def test_no_gate_or_kernel_code_reads_confidence():
    for path in [*ROOT.glob("appmod/kernel/*.py"), *ROOT.glob("appmod/phases/**/*.py"), *ROOT.glob("appmod/server/*.py")]:
        tree = ast.parse(path.read_text())
        hits = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Constant) and n.value == "confidence"]
        assert not hits, f"{path.relative_to(ROOT)} reads model confidence at lines {hits}"
