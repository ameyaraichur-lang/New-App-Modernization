"""Contract layer (blueprint IA04): canonical envelope + per-agent payload
JSON Schemas generated from the compiled registry, plus the deterministic
validator used on every publication and every hard-edge consumption.

Enums are closed and copied verbatim from the workbooks:
  status:        COMPLETE / PARTIAL / NOT_ASSESSED / SKIPPED_APPROVED / FAILED
  evidence_class: OBSERVED / DOCUMENTED / HUMAN_CONFIRMED / INFERRED /
                  HYPOTHETICAL / UNKNOWN
  criterion:     PASS / FAIL / NOT_RUN / BLOCKED / NOT_APPLICABLE
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import jsonschema

STATUS_ENUM = ["COMPLETE", "PARTIAL", "NOT_ASSESSED", "SKIPPED_APPROVED", "FAILED"]
EVIDENCE_CLASS_ENUM = [
    "OBSERVED", "DOCUMENTED", "HUMAN_CONFIRMED", "INFERRED", "HYPOTHETICAL", "UNKNOWN",
]
CRITERION_ENUM = ["PASS", "FAIL", "NOT_RUN", "BLOCKED", "NOT_APPLICABLE"]
ACCESS_ENUM = ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"]

SHA256_RE = r"^[a-f0-9]{64}$"
PRODUCER_RE = r"^P\d+\.(?:A\d+|G\d+|X\d+)$"

_JSON_TYPES = {
    "array": "array", "object": "object", "string": "string",
    "integer": "integer", "number": "number", "boolean": "boolean",
    "enum": "string", "timestamp": "string", "unknown": None,
}


# ---------------------------------------------------------------------------
# Canonical serialization + content hashing
# ---------------------------------------------------------------------------


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def content_hash(artifact: dict[str, Any]) -> str:
    """SHA-256 over the canonical serialization of everything except the
    content_hash field itself (which is derived, not input)."""
    body = {k: v for k, v in artifact.items() if k != "content_hash"}
    return hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Schema generation from the compiled registry
# ---------------------------------------------------------------------------


def payload_schema(phase_reg: dict[str, Any], local_id: str) -> dict[str, Any] | None:
    """JSON Schema for an agent's payload object, from the registry contract.

    Blueprint rule: 'Payload fields below are required keys unless marked
    nullable.'  Unknown prose types degrade to unconstrained values rather
    than blocking publication (the registry keeps the raw definition for
    humans; validators still enforce presence).
    """
    payloads = phase_reg["artifact_contracts"]["agent_payloads"]
    if local_id not in payloads:
        return None
    fields = payloads[local_id]["fields"]
    if not fields:
        return None
    props: dict[str, Any] = {}
    required: list[str] = []
    for f in fields:
        jt = _JSON_TYPES.get(f["type"])
        typ: Any = jt if jt else ["object", "array", "string", "number", "boolean", "null"]
        if f["nullable"]:
            typ = typ if isinstance(typ, list) else [typ, "null"]
        props[f["name"]] = {"type": typ} if not f["nullable"] else {
            "anyOf": [{"type": t} for t in (typ if isinstance(typ, list) else [typ])]
        }
        required.append(f["name"])
    return {
        "$defs": {},
        "type": "object",
        "properties": props,
        "required": required,
        "additionalProperties": True,   # external artifact refs allowed per envelope spec
    }


def normalize_payload(payload: dict[str, Any], pschema: dict[str, Any] | None) -> dict[str, Any]:
    """Adapt engine payloads to the frozen contract types.

    Blueprint notation leaves untyped fields as strings; several are naturally
    structured (context_manifest, coverage, reports). Rather than editing the
    frozen contracts, values destined for string-typed fields are serialized
    as canonical JSON strings — lossless and deterministic. Required keys that
    are absent stay absent (validation reports them); null stays null only
    where the field is nullable.
    """
    if not pschema:
        return payload
    props = pschema.get("properties", {})
    out: dict[str, Any] = {}
    for key, value in payload.items():
        prop = props.get(key)
        if prop is None or value is None:
            out[key] = value
            continue
        types = [t.get("type") for t in prop.get("anyOf", [{"type": prop.get("type")}])]
        is_string_field = "string" in types and not any(
            t in ("object", "array", "integer", "number", "boolean") for t in types
        )
        if is_string_field and isinstance(value, (dict, list)):
            out[key] = canonical_json(value)
        elif is_string_field and isinstance(value, (int, float, bool)):
            out[key] = canonical_json(value)
        else:
            out[key] = value
    return out


def envelope_schema(phase_reg: dict[str, Any]) -> dict[str, Any]:
    """Common envelope schema (workbook 'common envelope' rows)."""
    schema_version = phase_reg["schema_version"]
    p_payload: dict[str, Any] = {
        "type": "object",
        "additionalProperties": True,
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"{schema_version} artifact envelope",
        "type": "object",
        "properties": {
            "schema_version": {"const": schema_version},
            "artifact_id": {"type": "string", "minLength": 1},
            "artifact_version": {"type": "integer", "minimum": 1},
            "run_id": {"type": "string", "minLength": 1},
            "application_id": {"type": "string", "minLength": 1},
            "phase_id": {"const": phase_reg["phase"]},
            "producer_id": {"type": "string", "pattern": PRODUCER_RE},
            "input_manifest_ref": {"type": "string"},
            "input_hash": {"type": "string", "pattern": SHA256_RE},
            "policy_version": {"type": "string", "minLength": 1},
            "status": {"enum": STATUS_ENUM},
            "scope": {"type": "object"},
            "applicability": {"type": "object"},
            "evidence_refs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["source", "method"],
                    "properties": {
                        "source": {"type": "string"},
                        "ref": {"type": "string"},
                        "content_hash": {"type": ["string", "null"], "pattern": SHA256_RE},
                        "method": {"type": "string"},
                        "captured_at": {"type": "string"},
                        "observation_window": {"type": ["string", "null"]},
                        "access_classification": {"enum": ACCESS_ENUM},
                    },
                },
            },
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "evidence_class", "statement"],
                    "properties": {
                        "id": {"type": "string"},
                        "evidence_class": {"enum": EVIDENCE_CLASS_ENUM},
                        "statement": {"type": "string"},
                        "evidence_refs": {"type": "array"},
                        "scope": {"type": ["string", "object"]},
                        "limitations": {"type": ["string", "null"]},
                    },
                },
            },
            "gaps": {"type": "array"},
            "contradictions": {"type": "array"},
            "payload": p_payload,
            "created_at": {"type": "string", "format": "date-time"},
            "execution_metadata": {"type": "object"},
            "content_hash": {"type": "string", "pattern": SHA256_RE},
            "access_classification": {"enum": ACCESS_ENUM},
        },
        "required": [
            "schema_version", "artifact_id", "artifact_version", "run_id",
            "application_id", "phase_id", "producer_id", "input_manifest_ref",
            "input_hash", "policy_version", "status", "scope", "applicability",
            "evidence_refs", "findings", "gaps", "contradictions", "payload",
            "created_at", "execution_metadata", "content_hash",
            "access_classification",
        ],
        "additionalProperties": False,
    }


def build_phase_schemas(phase_reg: dict[str, Any]) -> dict[str, Any]:
    """{'envelope': schema, 'payloads': {'A1': schema|None}} for one phase."""
    return {
        "envelope": envelope_schema(phase_reg),
        "payloads": {
            a["local_id"]: payload_schema(phase_reg, a["local_id"])
            for a in phase_reg["agents"]
        },
    }


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------


class ContractValidator:
    """Deterministic validation on publication (Run Controls:
    'Deterministic validation — validate schema, producer ID, application/run
    scope, source versions and evidence references')."""

    def __init__(self, phase_reg: dict[str, Any]):
        self.phase_reg = phase_reg
        self.schemas = build_phase_schemas(phase_reg)
        self._producer_ids = {a["local_id"] for a in phase_reg["agents"]} | {
            g["id"] for g in phase_reg["gates"]
        }

    def validate(self, artifact: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        schema = self.schemas["envelope"]
        validator = jsonschema.Draft202012Validator(schema)
        for e in validator.iter_errors(artifact):
            errors.append(f"envelope: {e.message} at {list(e.absolute_path)}")

        if errors:
            return errors

        # producer must exist in the canonical registry and match the envelope
        producer = artifact["producer_id"]
        local = producer.split(".", 1)[1]
        if local not in self._producer_ids:
            errors.append(f"producer {producer} not in canonical registry")

        # payload schema (agent payloads only)
        if re.fullmatch(r"A\d+", local):
            pschema = self.schemas["payloads"].get(local)
            if pschema is not None:
                pv = jsonschema.Draft202012Validator(pschema)
                for e in pv.iter_errors(artifact["payload"]):
                    errors.append(f"payload: {e.message} at {list(e.absolute_path)}")

        # content hash integrity
        if artifact.get("content_hash") != content_hash(artifact):
            errors.append("content_hash mismatch (artifact modified or miscomputed)")

        return errors


# ---------------------------------------------------------------------------
# Hard-edge intake rule (shared by scheduler + gates)
# ---------------------------------------------------------------------------


def intake_errors(upstream: dict[str, Any]) -> list[str]:
    """Blueprint edge rule: 'Missing or FAILED blocks; allowed partials retain
    restrictions.'  Returns reasons this artifact may NOT be consumed."""
    errs: list[str] = []
    status = upstream.get("status")
    if status == "FAILED":
        errs.append(f"upstream {upstream.get('artifact_id')} status FAILED")
    elif status not in STATUS_ENUM:
        errs.append(f"upstream {upstream.get('artifact_id')} invalid status {status!r}")
    if upstream.get("content_hash") != content_hash(upstream):
        errs.append(f"upstream {upstream.get('artifact_id')} content_hash mismatch")
    return errs


def generate_all_schemas(registry: dict[str, Any], out_dir: Path) -> int:
    """Write envelope + payload schemas for every phase; returns count."""
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for phase, reg in registry["phases"].items():
        pdir = out_dir / f"phase_{phase}"
        pdir.mkdir(exist_ok=True)
        schemas = build_phase_schemas(reg)
        (pdir / "envelope.schema.json").write_text(
            json.dumps(schemas["envelope"], indent=2), encoding="utf-8"
        )
        n += 1
        for local_id, ps in schemas["payloads"].items():
            if ps is not None:
                (pdir / f"{local_id}.payload.schema.json").write_text(
                    json.dumps(ps, indent=2), encoding="utf-8"
                )
                n += 1
    return n
