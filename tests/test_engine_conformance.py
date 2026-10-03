"""Engine payload-conformance: every phase runner's payload must satisfy its
compiled contract schema (T1 gate for phase engines)."""

import jsonschema
import pytest
from pathlib import Path

from appmod.contracts.schemas import normalize_payload, payload_schema
from appmod.registry.compiler import compile_all
from appmod.phases.p1.engine import P1AgentRunner
from appmod.phases.p2.engine import P2AgentRunner, PortfolioApp
from appmod.phases.p3.engine import P3AgentRunner
from appmod.phases.p4.engine import P4AgentRunner
from appmod.phases.p5.engine import P5AgentRunner
from appmod.phases.p6.engine import P6AgentRunner

BLUEPRINT = Path(__file__).resolve().parents[1]  # repo root as a stand-in source tree


def art(payload=None, chash="h"):
    return {"payload": payload or {}, "content_hash": chash, "status": "COMPLETE"}


def build_cases():
    p1 = P1AgentRunner()
    p1.bind_repo(BLUEPRINT)

    brief3 = {"app_id": "a", "disposition": "Rearchitect", "primary_language": "java",
              "route": "UI", "components": ["c"], "routes": ["/x"], "datasets": ["d"]}
    brief5 = {"app_id": "a", "disposition": "Rearchitect", "routes": ["/x"],
              "datasets": ["d"], "dependencies": [{"name": "x"}], "tests": ["t"],
              "route": "UI", "security_constraints": [{"constraint": "c"}]}
    apps = [PortfolioApp(app_id="a", p1_g2_status="READY_FOR_PORTFOLIO_DECISION",
                         has_data_layer=True, route="UI", loc=1000, source_family="solo")]

    p1_inputs = {
        "G0": art(), "A1": art(), "A4": art(), "A2": art(), "A5": art(),
        "G1": art({"evidence_manifest": {"snapshot_digest": {}, "manifest_hash": "m"}}),
        "A10": art(),
    }
    p3_inputs = {
        "A1": art({"activation_manifest": [{"agent": "A5", "mode": "SKIP_APPROVED"}]}),
        "G1": art({"evidence_manifest": {"artifact_refs": {}, "snapshot_digest": {}}}),
    }
    p4_inputs = {
        "A1": art(), "A2": art(),
        "A3": art({"context_manifest": {"context_hash": "h"}}),
        "G1": art({"evidence_manifest": {"snapshot_digest": {
            k: {} for k in ("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8")}}}),
    }
    p5_inputs = {
        "G1": art({"baseline_summary": {"baseline_commit": "c", "route_count": 1},
                   "coverage": {"routes": 1, "tests": 1, "note": "n"},
                   "observed_results": []}),
        "G2": art(),
        "G3": art({"final_manifest": {"build_digest": "d"}}),
        "A1": art({"coverage": {"routes": 1, "tests": 1, "note": "n"}}),
    }
    p6_inputs = {
        "A9": art({"results": [], "checkpoint_id": "c"}),
        "A10": art({"checkpoint_id": "c"}),
        "G2": art({"checkpoint_manifest": {"checkpoint_id": "c", "rejects": []}}),
    }

    return [
        (1, p1, p1_inputs),
        (2, P2AgentRunner(apps), {}),
        (3, P3AgentRunner(brief3), p3_inputs),
        (4, P4AgentRunner({"app_id": "a", "disposition": "Rehost"}), p4_inputs),
        (5, P5AgentRunner(brief5), p5_inputs),
        (6, P6AgentRunner({"app_id": "a", "route": "batch",
                           "tables": [{"name": "t", "columns": 2}]}), p6_inputs),
    ]


def test_all_engine_payloads_conform(registry):
    failures = []
    for phase_num, runner, inputs in build_cases():
        phase_reg = registry["phases"][phase_num]
        for agent in phase_reg["agents"]:
            lid = agent["local_id"]
            handler = getattr(runner, f"_run_{lid.lower()}", None)
            if handler is None:
                continue
            try:
                outcome = handler(agent, inputs, None)
            except Exception as exc:
                failures.append(f"P{phase_num}.{lid}: handler error {exc!r}")
                continue
            schema = payload_schema(phase_reg, lid)
            if schema is None:
                continue
            normalized = normalize_payload(outcome.payload, schema)
            for e in jsonschema.Draft202012Validator(schema).iter_errors(normalized):
                failures.append(f"P{phase_num}.{lid}: {e.message} at {list(e.absolute_path)}")
    assert not failures, "\n  ".join(["payload conformance failures:"] + failures)
