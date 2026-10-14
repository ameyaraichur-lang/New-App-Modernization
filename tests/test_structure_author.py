"""Decision roles author structure. An invalid draft falls back to the seed."""

import jsonschema

from appmod.agents.overlays import _pp_p2_a6, _pp_p3_a1, _pp_p3_a2, _pp_p3_a3, _pp_p4_a3
from appmod.contracts.schemas import normalize_payload, payload_schema
from appmod.phases.p4.engine import P4AgentRunner


def _valid(phase_reg, local_id, payload):
    schema = payload_schema(phase_reg, local_id)
    normalized = normalize_payload(payload, schema)
    return list(jsonschema.Draft202012Validator(schema).iter_errors(normalized))


def test_valid_task_graph_replaces_the_seed():
    seed = {"tasks": [{"task_id": "T1-baseline", "phase": "P5", "kind": "seed",
                       "owner_role": "P5.A1", "acceptance": "seed"}],
            "dependency_edges": [], "estimate_assumptions": []}
    model = {"tasks": [
        {"task_id": "L-T1", "phase": "P5", "kind": "upgrade", "owner_role": "P5.A2",
         "acceptance": "builds", "depends_on": [], "component": "api", "estimate_days": 2},
        {"task_id": "L-T2", "phase": "P6", "kind": "data", "owner_role": "P6.A1",
         "acceptance": "reconciled", "depends_on": ["L-T1"], "component": "db", "estimate_days": 1},
    ]}
    ctx: dict = {}
    out = _pp_p4_a3(seed, model, ctx)
    assert ctx["first_pass_valid"] is True
    assert [t["task_id"] for t in out["tasks"]] == ["L-T1", "L-T2"]
    assert out["dependency_edges"] == [{"from": "L-T1", "to": "L-T2"}]


def test_cyclic_tasks_fall_back_and_stay_schema_valid(registry):
    seed_outcome = P4AgentRunner({"app_id": "a", "disposition": "Rehost"})._run_a3(
        {"local_id": "A3"}, {}, None)
    seed = seed_outcome.payload
    model = {"tasks": [
        {"task_id": "L-T1", "phase": "P5", "kind": "a", "owner_role": "P5.A2",
         "acceptance": "a", "depends_on": ["L-T2"]},
        {"task_id": "L-T2", "phase": "P5", "kind": "b", "owner_role": "P5.A2",
         "acceptance": "b", "depends_on": ["L-T1"]},
    ]}
    ctx: dict = {}
    out = _pp_p4_a3(seed, model, ctx)
    assert ctx["first_pass_valid"] is False
    assert [t["task_id"] for t in out["tasks"]] == [t["task_id"] for t in seed["tasks"]]
    assert _valid(registry["phases"][4], "A3", out) == []
    assert _valid(registry["phases"][4], "A3", seed) == []


def test_p3_structure_replaces_only_when_complete():
    seed = {"component_map": [{"component": "app", "target": "seed"}], "nfr_criteria": [{"target": "UNSET"}]}
    good = {"component_map": [{"component": "api", "current": "express", "target": "fastify",
                               "change": "upgrade"}],
            "technology_evidence": [{"choice": "fastify", "rationale": "supported"}],
            "proposed_adrs": [{"adr": "ADR-1", "decision": "upgrade", "rationale": "eol",
                               "consequences": "rewrite mounts"}]}
    ctx: dict = {}
    out = _pp_p3_a1(seed, good, ctx)
    assert ctx["first_pass_valid"] is True
    assert out["component_map"][0]["target"] == "fastify"
    assert out["nfr_criteria"] == seed["nfr_criteria"]
    bad = _pp_p3_a1(seed, {"component_map": [{"component": "api"}]}, {})
    assert bad["component_map"] == seed["component_map"]


def test_boundaries_and_schemas_and_dispositions():
    ctx: dict = {}
    boundaries = _pp_p3_a2({"note": "seed"}, {"boundaries": [
        {"boundary": "orders", "modules": ["order"], "justification": "cycle"}]}, ctx)
    assert ctx["first_pass_valid"] is True and boundaries["boundaries"][0]["boundary"] == "orders"
    refused = _pp_p3_a2({"note": "seed"}, {"boundaries": [{"boundary": "orders"}]}, {})
    assert "boundaries" not in refused
    schemas = _pp_p3_a3({}, {"schemas": [{"object": "users", "action": "align", "detail": "id"}]}, {})
    assert schemas["schemas"][0]["action"] == "align"
    assert _pp_p3_a3({}, {"schemas": [{"object": "users", "action": "invent", "detail": "x"}]}, {}) == {}
    seed = {"decisions": [{"application_id": "app", "proposed_disposition": "Rehost",
                           "wave_id": "W1", "rationale": "seed"}]}
    ctx = {}
    decided = _pp_p2_a6(seed, {"decisions": [{
        "application_id": "app", "proposed_disposition": "Refactor", "second_best": "Rehost",
        "rationale": "tests are thin", "wave": 1}]}, ctx)
    assert ctx["first_pass_valid"] is True
    assert decided["decisions"][0]["proposed_disposition"] == "Refactor"
    ctx = {}
    kept = _pp_p2_a6(seed, {"decisions": [{
        "application_id": "app", "proposed_disposition": "NotARoute", "second_best": "Rehost",
        "rationale": "x", "wave": 1}]}, ctx)
    assert ctx["first_pass_valid"] is False
    assert kept["decisions"][0]["proposed_disposition"] == "Rehost"
