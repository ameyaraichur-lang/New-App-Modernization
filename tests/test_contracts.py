"""T1 contract tests: envelope validation, enums, identity, intake rules."""

import pytest

from appmod.contracts.schemas import (
    STATUS_ENUM, ContractValidator, content_hash, intake_errors,
)


def make_artifact(**over):
    art = {
        "schema_version": "P1.discovery.v3.0",
        "artifact_id": "P1/app/A1",
        "artifact_version": 1,
        "run_id": "run-1",
        "application_id": "app",
        "phase_id": 1,
        "producer_id": "P1.A1",
        "input_manifest_ref": "{}",
        "input_hash": "a" * 64,
        "policy_version": "pilot-default-1.0.0",
        "status": "COMPLETE",
        "scope": {"mode": "test"},
        "applicability": {"route": "UI"},
        "evidence_refs": [{"source": "repo", "method": "static-analysis"}],
        "findings": [{"id": "F1", "evidence_class": "OBSERVED", "statement": "s"}],
        "gaps": [],
        "contradictions": [],
        "payload": {
            "repositories": [], "components": [], "dependencies": [],
            "sbom_ref": "sbom-1", "coverage": {}, "build_status": "UNKNOWN",
            "findings": [],
        },
        "created_at": "2026-10-03T00:00:00Z",
        "execution_metadata": {"runner": "test"},
        "access_classification": "INTERNAL",
    }
    art.update(over)
    art["content_hash"] = content_hash(art)
    return art


@pytest.fixture()
def validator(registry):
    return ContractValidator(registry["phases"][1])


def test_valid_artifact_passes(validator):
    assert validator.validate(make_artifact()) == []


def test_bad_status_rejected(validator):
    errs = validator.validate(make_artifact(status="MOSTLY_DONE"))
    assert any("status" in e for e in errs)


def test_all_status_enum_values_valid(validator):
    for status in STATUS_ENUM:
        assert validator.validate(make_artifact(status=status)) == [], status


def test_bad_evidence_class_rejected(validator):
    art = make_artifact()
    art["findings"][0]["evidence_class"] = "DEFINITELY_TRUE"
    art["content_hash"] = content_hash(art)
    errs = validator.validate(art)
    assert any("DEFINITELY_TRUE" in e for e in errs)


def test_content_hash_tamper_detected(validator):
    art = make_artifact()
    art["status"] = "PARTIAL"   # content changed without recomputing hash
    assert any("content_hash mismatch" in e for e in validator.validate(art))


def test_unknown_producer_rejected(validator):
    errs = validator.validate(make_artifact(producer_id="P1.A99"))
    assert any("producer" in e for e in errs)


def test_cross_phase_substitution_rejected(validator):
    """H15: phase-local artifacts cannot cross phases — schema_version const."""
    errs = validator.validate(make_artifact(schema_version="P2.portfolio.v3.0"))
    assert errs


def test_missing_payload_field_rejected(validator):
    art = make_artifact()
    del art["payload"]["sbom_ref"]
    art["content_hash"] = content_hash(art)
    assert any("payload" in e for e in validator.validate(art))


def test_failed_upstream_blocks_intake():
    art = make_artifact(status="FAILED")
    art["content_hash"] = content_hash(art)
    assert intake_errors(art) != []
    for status in ("COMPLETE", "PARTIAL", "NOT_ASSESSED", "SKIPPED_APPROVED"):
        ok = make_artifact(status=status)
        assert intake_errors(ok) == [], status
