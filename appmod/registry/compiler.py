"""Registry compiler: blueprint workbooks (XLSX) + Master_Registry.json ->
canonical machine-readable registry (JSON) that drives orchestration AND the UI.

Blueprint principle (their finding F15): one source registry drives the workbook,
the DAG views and execution. This compiler is that principle in code: every
agent, gate, edge, contract and control is parsed from the tuned workbooks
byte-for-byte-preserved in the source archive; nothing is hand-transcribed.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import openpyxl

# ---------------------------------------------------------------------------
# Source layout constants
# ---------------------------------------------------------------------------

PHASE_DIRS = {
    1: ("Phase_1_Tuned", "Discovery", "P1.discovery.v3.0"),
    2: ("Phase_2_Tuned", "Portfolio", "P2.portfolio.v3.0"),
    3: ("Phase_3_Tuned", "Target architecture", "P3.architecture.v3.0"),
    4: ("Phase_4_Tuned", "Modernization planning", "P4.planning.v3.0"),
    5: ("Phase_5_Tuned", "Code & application modernization", "P5.codeapp.v3.0"),
    6: ("Phase_6_Tuned", "Data modernization", "P6.data.v3.0"),
    8: ("Phase_8_Tuned", "Deployment & cutover", "P8.deploy.v3.0"),
    9: ("Phase_9_Tuned", "Post-modernization operations", "P9.ops.v3.0"),
}

# Parity expectations copied from Master/Verification_Summary.json (their own
# static verification) — the compiler must reproduce these numbers or fail.
PARITY = {
    1: {"roles": 11, "links": 21},
    2: {"roles": 7, "links": 14},
    3: {"roles": 8, "links": 16},
    4: {"roles": 9, "links": 16},
    5: {"roles": 9, "links": 19},
    6: {"roles": 12, "links": 29},
    8: {"roles": 12, "links": 35},
    9: {"roles": 10, "links": 40},
}
MASTER_LINKS = 17

# Compiled canonical registry shipped with the codebase (parity-checked on load)
DEFAULT_REGISTRY_DIR = Path(__file__).resolve().parents[2] / "data" / "registry"
TOTAL_ROLES = 78
TOTAL_LINKS = 190

GATE_NODE_RE = re.compile(r"^G\d+$")
EXEC_NODE_RE = re.compile(r"^X\d+$")
# Canonical registry node ids: agents (with optional .P/.R/.V/.H invocation suffix),
# gates, execution services, named services (BUS/S) and external boundary nodes
# (P2, P3, R, NEXT, C, E, OPS, P8OPS, P8NEXT...).
NODE_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:\.[A-Z])?$")
EXTERNAL_RE = re.compile(r"^(?:P\d+|R|C|E|OPS|P8OPS|P8NEXT|NEXT)$")


# ---------------------------------------------------------------------------
# Generic sheet helpers
# ---------------------------------------------------------------------------


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\n", " ").strip()


def sheet_rows(ws) -> list[list[str]]:
    """All non-empty rows of a worksheet as cleaned strings."""
    rows: list[list[str]] = []
    for raw in ws.iter_rows(values_only=True):
        cells = [_clean(c) for c in raw]
        if any(cells):
            rows.append(cells)
        else:
            rows.append([])  # keep blank-row structure for table detection
    return rows


def find_marker_row(rows: list[list[str]], marker: str) -> int | None:
    for i, row in enumerate(rows):
        if row and marker.lower() in row[0].lower():
            return i
    return None


def next_nonempty(rows: list[list[str]], start: int) -> int | None:
    """Index of the first non-empty row at or after `start`."""
    for i in range(start, len(rows)):
        if any(rows[i]):
            return i
    return None


def table_from_header(
    rows: list[list[str]],
    header_row: int,
    min_cols: int = 2,
    stop_at_blank: bool = False,
    stop_row: int | None = None,
) -> list[dict[str, str]]:
    """Rows after a header row -> list of dicts keyed by header cell.

    stop_at_blank: terminate at the first fully blank row (sectioned sheets).
    stop_row: terminate before this absolute row index (e.g. a section marker).
    """
    header = [h for h in rows[header_row]]
    out: list[dict[str, str]] = []
    for i, row in enumerate(rows[header_row + 1:], start=header_row + 1):
        if stop_row is not None and i >= stop_row:
            break
        if not any(row):
            if stop_at_blank:
                break
            continue
        rec: dict[str, str] = {}
        for j, key in enumerate(header):
            if not key:
                continue
            rec[key] = row[j] if j < len(row) else ""
        if any(rec.get(k, "") for k in header if k):
            out.append(rec)
    return out


# ---------------------------------------------------------------------------
# Execution / prerequisites parsing
# ---------------------------------------------------------------------------


@dataclass
class ExecInfo:
    tier: int | None
    tier_label: str
    lane: str  # normal | async
    prerequisites: list[str] = field(default_factory=list)
    raw: str = ""


def parse_execution(raw: str) -> ExecInfo:
    """Parse 'Tier 1 | Evidence-dependent | Hard: A1, A4' / 'Tier 2; after A2 + A4'
    / 'Async | Asynchronous; optional snapshot | Hard: G0' into structured data."""
    text = raw.strip()
    tier: int | None = None
    m = re.search(r"Tier\s+(\d+)", text)
    if m:
        tier = int(m.group(1))
    lane = "async" if text.lower().startswith("async") else "normal"

    prereq: list[str] = []
    for m in re.finditer(r"(?:Hard:\s*|after\s+)([A-Z0-9][A-Z0-9,\s+&]*)", text):
        for tok in re.split(r"[,+&]| and ", m.group(1)):
            tok = tok.strip()
            if re.fullmatch(r"[AGX]\d+", tok):
                prereq.append(tok)
    if not prereq and re.fullmatch(r"[AGX\d][AGX\d\s,+&]*", text):
        # P8-style bare cell: 'G0' / 'A2' / 'A1 + A3'
        for tok in re.split(r"[,+&]", text):
            tok = tok.strip()
            if re.fullmatch(r"[AGX]\d+", tok):
                prereq.append(tok)

    label = text.split("|")[0].strip() if "|" in text else text.split(";")[0].strip()
    return ExecInfo(tier=tier, tier_label=label, lane=lane, prerequisites=prereq, raw=text)


# ---------------------------------------------------------------------------
# Payload field parsing  ("repositories:array; sbom_ref:string|null; ...")
# ---------------------------------------------------------------------------

_TYPE_MAP = {
    "array": "array",
    "object": "object",
    "string": "string",
    "integer": "integer",
    "number": "number",
    "boolean": "boolean",
    "timestamp": "string",
    "enum": "string",
}


FIELD_RE = re.compile(r"^([a-z_][a-z0-9_.]*)(\[\])?(?::([a-z]+(?:\|null)?))?$")


def parse_payload_fields(raw: str) -> list[dict[str, str]]:
    """Extract typed field lists from contract definitions.

    Accepts both blueprint notations:
      'repositories:array; sbom_ref:string|null'        (P1–P5, P8)
      'route_by_object[]; recovery_plan_ref; windows[]' (P6, P9)
    Prose segments (sentences, 'schema=X', 'program/wave IDs') do not match the
    field grammar and are intentionally dropped — the raw definition is kept
    alongside for consumers that need the prose.
    """
    fields: list[dict[str, str]] = []
    for part in (raw or "").split(";"):
        part = part.strip().rstrip(".")
        m = FIELD_RE.match(part)
        if not m:
            continue
        name, arr, typ = m.groups()
        if arr:
            ftype = "array"
        elif typ:
            ftype = typ.split("|")[0]
        else:
            ftype = "string"
        fields.append({"name": name, "type": ftype, "nullable": bool(typ and "null" in typ)})
    return fields


# ---------------------------------------------------------------------------
# Agent Swarm header normalization (headers vary slightly per phase)
# ---------------------------------------------------------------------------


def _norm_agent_rec(rec: dict[str, str]) -> dict[str, str] | None:
    def pick(*keys: str) -> str:
        for k in keys:
            for rk, rv in rec.items():
                if rk and rk.lower().startswith(k.lower()):
                    if rv:
                        return rv
        return ""

    local_id = pick("Stable agent ID", "Stable ID")
    if not re.fullmatch(r"A\d+", local_id):
        return None
    return {
        "local_id": local_id,
        "name": pick("Agent name", "Agent"),
        "workflow": pick("Workflow"),
        "activities": pick("Activities"),
        "inputs": pick("Inputs"),
        "outputs": pick("Outputs"),
        "execution": pick("Execution", "Invocation", "Activation"),
        "origin": pick("Origin"),
        "contract_rule": pick("Evidence and safety", "Contract rule", "Evidence / safety"),
    }


# ---------------------------------------------------------------------------
# Phase compiler
# ---------------------------------------------------------------------------


def compile_phase(blueprint_dir: Path, phase: int) -> dict[str, Any]:
    dir_name, phase_name, schema_version = PHASE_DIRS[phase]
    phase_dir = blueprint_dir / dir_name
    xlsx = next(phase_dir.glob("*.xlsx"))
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    rows_by_sheet = {ws.title: sheet_rows(ws) for ws in wb.worksheets}

    # -- agents (canonical registry: Agent Swarm sheet) ---------------------
    swarm_rows = rows_by_sheet["Agent Swarm"]
    hdr = find_marker_row(swarm_rows, "Phase") or 0
    # find the actual column-header row (contains 'Activities')
    header_row = next(
        (i for i, r in enumerate(swarm_rows) if r and any("Activities" in c for c in r)),
        hdr,
    )
    agents_raw = [
        rec
        for rec in ( _norm_agent_rec(r) for r in table_from_header(swarm_rows, header_row) )
        if rec
    ]
    # de-duplicate by local_id (Quick Reference echo rows etc. can't appear here,
    # but be safe)
    by_id: dict[str, dict[str, str]] = {}
    for rec in agents_raw:
        by_id.setdefault(rec["local_id"], rec)

    # merge-analysis enrichment (role boundary sheet)
    merge_rows = rows_by_sheet.get("Merge Analysis", [])
    merge_header = next(
        (i for i, r in enumerate(merge_rows) if r and any("Retained" in c or "Origin" in c for c in r)),
        None,
    )
    merge_by_id: dict[str, dict[str, str]] = {}
    if merge_header is not None:
        for rec in table_from_header(merge_rows, merge_header):
            mid = rec.get("ID") or rec.get("Agent ID") or ""
            if re.fullmatch(r"A\d+", mid):
                merge_by_id[mid] = rec

    agents: list[dict[str, Any]] = []
    for local_id in sorted(by_id, key=lambda x: int(x[1:])):
        rec = by_id[local_id]
        exec_info = parse_execution(rec["execution"])
        m = merge_by_id.get(local_id, {})
        agents.append(
            {
                "id": f"P{phase}.{local_id}",
                "local_id": local_id,
                "name": rec["name"],
                "tier": exec_info.tier,
                "tier_label": exec_info.tier_label,
                "lane": exec_info.lane,
                "prerequisites": exec_info.prerequisites,
                "execution_raw": exec_info.raw,
                "activities": rec["activities"],
                "inputs": rec["inputs"],
                "outputs": rec["outputs"],
                "origin": rec["origin"] or m.get("Retained origin", "") or m.get("Origin / merge", ""),
                "contract_rule": rec["contract_rule"],
                "merge_tuning": m.get("v3.0 tuning", "") or m.get("Tuning", ""),
                "responsibility": m.get("Responsibility", ""),
            }
        )

    # -- execution DAG: stages + canonical edge registry ---------------------
    dag_rows = rows_by_sheet["Execution DAG"]
    edge_marker = find_marker_row(dag_rows, "Canonical hard-edge registry")
    if edge_marker is None:
        edge_marker = find_marker_row(dag_rows, "Canonical typed-link registry")
    if edge_marker is None:
        raise ValueError(f"{xlsx.name}: no canonical edge registry")
    header_i = next_nonempty(dag_rows, edge_marker + 1)
    if header_i is None:
        raise ValueError(f"{xlsx.name}: empty canonical edge registry")
    edges = table_from_header(dag_rows, header_i)

    # node-type table (P9-style DAG sheets carry an explicit node table);
    # bounded by the canonical-registry marker so section rows can't overwrite it
    node_types: dict[str, str] = {}
    node_header = next(
        (i for i, r in enumerate(dag_rows)
         if r and any(c == "Node" for c in r) and any(c == "Type" for c in r)),
        None,
    )
    if node_header is not None and (edge_marker is None or node_header < edge_marker):
        for rec in table_from_header(
            dag_rows, node_header, stop_at_blank=True, stop_row=edge_marker
        ):
            nid = rec.get("Node", "")
            ntype = rec.get("Type", "").lower()
            if NODE_RE.fullmatch(nid) and ntype in {"agent", "gate", "service", "execution", "external"}:
                node_types[nid] = ntype

    agent_ids = {a["local_id"] for a in agents} | {
        m.group(1) for a in agents for m in [re.match(r"^(A\d+)", a["local_id"])] if m
    }

    def classify(node: str) -> str | None:
        if node in node_types:
            return node_types[node]
        base = node.split(".")[0]
        if base in agent_ids and node.split(".")[-1] in {base} | {"P", "R", "V", "H"}:
            return "agent"
        if GATE_NODE_RE.fullmatch(node):
            return "gate"
        if EXEC_NODE_RE.fullmatch(node):
            return "execution"
        if EXTERNAL_RE.fullmatch(node):
            return "external"
        return None  # unknown -> reject

    hard_edges: list[dict[str, Any]] = []
    for rec in edges:
        frm = rec.get("From", "").strip()
        to = rec.get("To", "").strip()
        ftype = classify(frm)
        ttype = classify(to)
        if not (ftype and ttype):
            continue
        hard_edges.append(
            {
                "from": frm,
                "to": to,
                "from_kind": ftype,
                "to_kind": ttype,
                "type": rec.get("Edge type", rec.get("Type", rec.get("Class", "HARD"))),
                "required_artifact": rec.get(
                    "Required artifact / meaning",
                    rec.get("Required object", rec.get("Required transfer", rec.get("Required object / event", ""))),
                ),
                "failure_behavior": rec.get("Failure behavior", ""),
                "external": ttype == "external" or ftype == "external",
            }
        )

    # stage table (rows before the edge marker, after the first header)
    stage_header = next(
        (i for i, r in enumerate(dag_rows) if r and any("Stage" == c or "Node" in c for c in r)),
        0,
    )
    stages_raw = table_from_header(dag_rows, stage_header)
    stages: list[dict[str, Any]] = []
    for rec in stages_raw:
        stage_id = rec.get("Stage", rec.get("Node", rec.get("Node(s)", "")))
        if not stage_id or "Canonical" in stage_id:
            continue
        nodes = rec.get("Node(s)", rec.get("Nodes", ""))
        stages.append(
            {
                "stage": stage_id,
                "nodes": [n.strip() for n in re.split(r"[+,]| and ", nodes) if n.strip()],
                "prerequisites": rec.get("Prerequisites", rec.get("Execution / activation", "")),
                "activity": rec.get("Activity / output", rec.get("Activity", "")),
                "blocking": rec.get("Blocking condition", rec.get("Blocking rule", "")),
                "meaning": rec.get("Count / meaning", rec.get("Meaning", "")),
            }
        )

    # -- gates: graph nodes that are gates or execution services --------------
    node_ids = {e["from"] for e in hard_edges} | {e["to"] for e in hard_edges}
    gate_ids = sorted(
        (n for n in node_ids if classify(n) in {"gate", "execution"}),
        key=_gate_sort,
    )
    gates: list[dict[str, Any]] = []
    for gid in gate_ids:
        stage_rec = next((s for s in stages if s["stage"] == gid), None)
        gates.append(
            {
                "id": gid,
                "kind": _gate_kind(gid),
                "node_type": classify(gid),
                "entry": stage_rec["prerequisites"] if stage_rec else "",
                "output": stage_rec["activity"] if stage_rec else "",
                "blocking_rule": stage_rec["blocking"] if stage_rec else "",
                "meaning": stage_rec["meaning"] if stage_rec else "",
            }
        )

    # -- artifact contracts ---------------------------------------------------
    ac_rows = rows_by_sheet["Artifact Contracts"]
    NAME_COLS = ("Contract / field", "Object / field", "Field / object", "Object")
    DEF_COLS = ("Definition / validation", "Fields / validation", "Definition")
    ac_header = next(
        (
            i for i, r in enumerate(ac_rows)
            if r
            and any(c in NAME_COLS for c in r)
            and (
                (any(c == "Type" for c in r) and any(c.startswith("Required") for c in r))
                or (any(c == "Required scope" for c in r) and any(c.startswith("Fields") for c in r))
            )
        ),
        0,
    )
    contracts_raw = table_from_header(ac_rows, ac_header)
    envelope_fields: list[dict[str, str]] = []
    agent_payloads: dict[str, dict[str, Any]] = {}
    named_objects: dict[str, dict[str, Any]] = {}
    for rec in contracts_raw:
        name = next((rec[k] for k in NAME_COLS if k in rec and rec[k]), "")
        ftype = rec.get("Type", "object")
        definition = next((rec[k] for k in DEF_COLS if k in rec and rec[k]), "")
        req = rec.get("Required", rec.get("Required scope", ""))
        producer = rec.get("Producer / consumer", "")
        failure = rec.get(
            "Missing / invalid handling",
            rec.get("Failure handling", rec.get("Failure behavior", "")),
        )
        # Agent payload rows look like 'A1 primary result'
        m = re.match(r"^(A\d+)\s+(primary result|payload)$", name)
        if m:
            agent_payloads[m.group(1)] = {
                "fields": parse_payload_fields(definition),
                "raw": definition,
                "producer_consumer": producer,
                "rule": failure,
            }
            continue
        # Envelope rows share the common-envelope shape (schema_version etc.)
        if name in {
            "schema_version", "artifact_id + artifact_version",
            "run_id + application_id + phase_id", "producer_id",
            "input_manifest_ref + input_hash", "policy_version", "status",
            "scope + applicability", "evidence_refs", "findings",
            "evidence_class", "gaps + contradictions", "payload",
            "created_at + execution_metadata", "content_hash + access_classification",
        }:
            envelope_fields.append(
                {"field": name, "type": ftype, "required": req, "definition": definition,
                 "producer_consumer": producer, "failure": failure}
            )
            continue
        if name:
            named_objects[name] = {
                "type": ftype, "required": req, "definition": definition,
                "fields": parse_payload_fields(definition) if ftype == "object" else [],
                "producer_consumer": producer, "failure": failure,
            }

    # -- run controls ----------------------------------------------------------
    rc_rows = rows_by_sheet.get("Run Controls", [])
    rc_header = next(
        (i for i, r in enumerate(rc_rows) if r and any("Control" in c for c in r) and any("Stage" in c for c in r)),
        None,
    )
    run_controls: list[dict[str, str]] = []
    if rc_header is not None:
        for rec in table_from_header(rc_rows, rc_header):
            if rec.get("Control"):
                run_controls.append(
                    {
                        "stage": rec.get("Stage", ""),
                        "control": rec.get("Control", ""),
                        "when": rec.get("When it applies", ""),
                        "behavior": rec.get("Required behavior", ""),
                        "accountable": rec.get("Accountable role", ""),
                        "failure": rec.get("Failure / restriction", rec.get("Failure", "")),
                    }
                )

    # -- cross feeds ------------------------------------------------------------
    cf_rows = rows_by_sheet.get("Cross-Feed Details", [])
    cf_header = next((i for i, r in enumerate(cf_rows) if r and any("Feed ID" in c or "Flow" in c for c in r)), None)
    cross_feeds: list[dict[str, str]] = []
    if cf_header is not None:
        for rec in table_from_header(cf_rows, cf_header):
            fid = rec.get("Feed ID", rec.get("Flow", ""))
            if fid and "Feed ID" not in fid and "Flow" not in fid:
                cross_feeds.append(
                    {
                        "id": fid,
                        "sources": rec.get("Sources", rec.get("From", "")),
                        "consumer": rec.get("Consumer", rec.get("To", "")),
                        "purpose": rec.get("Purpose", rec.get("Required transfer", "")),
                        "protocol": rec.get("Version / timing protocol", rec.get("Protocol", rec.get("Timing", ""))),
                        "consequence": rec.get("Decision consequence", rec.get("Failure / limitation", "")),
                    }
                )

    # -- activation matrix (P3, P5) ----------------------------------------------
    activation: list[dict[str, str]] = []
    am_rows = rows_by_sheet.get("Activation Matrix", [])
    if am_rows:
        am_header = next((i for i, r in enumerate(am_rows) if r and any("Disposition" in c for c in r)), None)
        if am_header is not None:
            activation = table_from_header(am_rows, am_header)

    # -- execution routes (P6) ------------------------------------------------------
    routes: list[dict[str, str]] = []
    er_rows = rows_by_sheet.get("Execution Routes", [])
    if er_rows:
        er_header = next((i for i, r in enumerate(er_rows) if r and any("Route" == c for c in r)), None)
        if er_header is not None:
            routes = table_from_header(er_rows, er_header)

    # -- freeze recommendation (Quick Reference) --------------------------------------
    freeze = ""
    qr_rows = rows_by_sheet.get("Quick Reference", [])
    for row in qr_rows:
        for j, cell in enumerate(row):
            if cell in ("FREEZE CORE STRUCTURE", "READY FOR DESIGN REVIEW", "SKIPPED"):
                freeze = cell
                break
        if freeze:
            break

    return {
        "phase": phase,
        "name": phase_name,
        "schema_version": schema_version,
        "source_workbook": str(xlsx.name),
        "freeze_recommendation": freeze,
        "agents": agents,
        "gates": gates,
        "stages": stages,
        "hard_edges": hard_edges,
        "cross_feeds": cross_feeds,
        "artifact_contracts": {
            "envelope_fields": envelope_fields,
            "agent_payloads": agent_payloads,
            "named_objects": named_objects,
        },
        "run_controls": run_controls,
        "activation_matrix": activation,
        "execution_routes": routes,
    }


def _gate_sort(gid: str):
    if gid.startswith("X"):
        return (1, int(gid[1:]))
    if gid.startswith("G"):
        return (0, int(gid[1:]))
    return (2, gid)


def _gate_kind(gid: str) -> str:
    if gid.startswith("X"):
        return "execution"
    return {
        "G0": "intake",
        "G1": "snapshot",      # per-phase engines refine (P5 baseline seal, P6 permit)
        "G2": "release",       # P5: core integration; P6: checkpoint — refined per engine
        "G3": "release",
        "G4": "release",
    }.get(gid, "gate")


# ---------------------------------------------------------------------------
# Master registry + parity
# ---------------------------------------------------------------------------


def compile_master(blueprint_dir: Path) -> dict[str, Any]:
    master = json.loads((blueprint_dir / "Master" / "Master_Registry.json").read_text(encoding="utf-8"))
    return master


def check_acyclic(phase_reg: dict[str, Any]) -> list[str]:
    """Kahn's algorithm over milestone edges.

    Per the blueprint's own verification: milestone graphs are acyclic; Phase 9's
    EVENT feedback loops are intentional and therefore excluded here, as are
    external boundary nodes (they terminate the graph).
    """
    edges = [
        (e["from"], e["to"])
        for e in phase_reg["hard_edges"]
        if e["type"] != "EVENT" and not e["external"]
    ]
    nodes = {n for e in edges for n in e}
    indeg = {n: 0 for n in nodes}
    adj: dict[str, list[str]] = {n: [] for n in nodes}
    for a, b in edges:
        adj[a].append(b)
        indeg[b] += 1
    queue = [n for n, d in indeg.items() if d == 0]
    seen = 0
    while queue:
        n = queue.pop()
        seen += 1
        for m in adj[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                queue.append(m)
    if seen != len(nodes):
        return [n for n, d in indeg.items() if d > 0]
    return []


def verify_parity(registry: dict[str, Any]) -> list[str]:
    """Reproduce the blueprint's own static verification as a build gate."""
    errors: list[str] = []
    phases = registry["phases"]
    total_roles = 0
    total_links = 0
    for phase, expect in PARITY.items():
        reg = phases.get(phase)
        if reg is None:
            errors.append(f"phase {phase} missing from compiled registry")
            continue
        n_roles = len(reg["agents"])
        n_links = len(reg["hard_edges"])
        total_roles += n_roles
        total_links += n_links
        if n_roles != expect["roles"]:
            errors.append(f"P{phase}: {n_roles} roles, expected {expect['roles']}")
        if n_links != expect["links"]:
            errors.append(f"P{phase}: {n_links} hard edges, expected {expect['links']}")
        cycle = check_acyclic(reg)
        if cycle:
            errors.append(f"P{phase}: milestone graph cyclic at {cycle}")
    if total_roles != TOTAL_ROLES:
        errors.append(f"total roles {total_roles} != {TOTAL_ROLES}")
    if total_links != TOTAL_LINKS:
        errors.append(f"total links {total_links} != {TOTAL_LINKS}")
    if len(registry["master"]["links"]) != MASTER_LINKS:
        errors.append(f"master links {len(registry['master']['links'])} != {MASTER_LINKS}")
    return errors


def compile_all(blueprint_dir: Path) -> dict[str, Any]:
    master = compile_master(blueprint_dir)
    phases = {}
    for phase in PHASE_DIRS:
        phases[phase] = compile_phase(blueprint_dir, phase)
    registry = {
        "compiled_from": str(blueprint_dir),
        "master": master,
        "phases": phases,
    }
    errors = verify_parity(registry)
    if errors:
        raise ValueError("registry parity failed:\n  " + "\n  ".join(errors))
    return registry


def write_registry(registry: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "master.json").write_text(
        json.dumps(registry["master"], indent=2, ensure_ascii=False), encoding="utf-8"
    )
    for phase, reg in registry["phases"].items():
        (out_dir / f"phase_{phase}.json").write_text(
            json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    # UI-friendly combined digest
    digest = {
        "phases": [
            {
                "phase": reg["phase"],
                "name": reg["name"],
                "schema_version": reg["schema_version"],
                "freeze_recommendation": reg["freeze_recommendation"],
                "roles": len(reg["agents"]),
                "gates": [g["id"] for g in reg["gates"]],
                "edges": reg["hard_edges"],
                "agents": [
                    {
                        "id": a["id"], "local_id": a["local_id"], "name": a["name"],
                        "tier": a["tier"], "lane": a["lane"], "prerequisites": a["prerequisites"],
                    }
                    for a in reg["agents"]
                ],
            }
            for reg in registry["phases"].values()
        ],
        "master_links": registry["master"]["links"],
        "open_findings": registry["master"]["open_findings"],
    }
    (out_dir / "pipeline_digest.json").write_text(
        json.dumps(digest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def load_registry(registry_dir: Path | None = None) -> dict[str, Any]:
    """Load a previously compiled canonical registry (no XLSX needed).

    This is how the pipeline runs without the blueprint workbooks: the
    compiled JSONs ship in data/registry/ and pass the same parity checks.
    """
    registry_dir = Path(registry_dir) if registry_dir else DEFAULT_REGISTRY_DIR
    master = json.loads((registry_dir / "master.json").read_text(encoding="utf-8"))
    phases = {}
    for phase in PHASE_DIRS:
        path = registry_dir / f"phase_{phase}.json"
        phases[phase] = json.loads(path.read_text(encoding="utf-8"))
    registry = {"compiled_from": str(registry_dir), "master": master, "phases": phases}
    errors = verify_parity(registry)
    if errors:
        raise ValueError("registry parity failed:\n  " + "\n  ".join(errors))
    return registry


def resolve_registry() -> dict[str, Any]:
    """Registry source resolution for runners/tests: the APPMOD_BLUEPRINT env
    var (a blueprint workbook directory to recompile from source) when set,
    otherwise the shipped compiled registry in data/registry/."""
    env = os.environ.get("APPMOD_BLUEPRINT")
    if env and Path(env).exists():
        return compile_all(Path(env))
    return load_registry()


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="Compile blueprint workbooks -> canonical registry")
    ap.add_argument("blueprint_dir", type=Path)
    ap.add_argument("out_dir", type=Path)
    args = ap.parse_args()
    registry = compile_all(args.blueprint_dir)
    write_registry(registry, args.out_dir)
    n_roles = sum(len(r["agents"]) for r in registry["phases"].values())
    n_edges = sum(len(r["hard_edges"]) for r in registry["phases"].values())
    print(f"OK: 8 phases, {n_roles} roles, {n_edges} hard edges, "
          f"{len(registry['master']['links'])} master links — parity verified")


if __name__ == "__main__":
    main()
