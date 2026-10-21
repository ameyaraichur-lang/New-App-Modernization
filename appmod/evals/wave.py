"""Wave report: tune, holdout, and stability measured separately.

Numbers come only from the eval, e2e, and stability documents passed in.
A missing document or an unassessed component stays unassessed.
"""

from __future__ import annotations

from typing import Any

from appmod.agents.lineage import CRITICS, LINEAGE
from appmod.evals.confidence import COMPONENTS

DISPATCH_MIN = 97.0
_HEADER = "| Component | Today | Target | Unlocked by |"
_MEASURED_HEADER = "| Component | Today | Measured this wave | Target | Unlocked by |"


def dispatch_rate(e2e: dict[str, Any]) -> float:
    summary = e2e.get("summary") or {}
    rate = summary.get("success_rate")
    if not isinstance(rate, (int, float)):
        raise ValueError("e2e report has no dispatch success_rate")
    return float(rate)


def gate_passed(evaluation: dict[str, Any]) -> bool:
    if "pass" not in evaluation:
        raise ValueError("eval report has no step-33 pass field")
    return bool(evaluation["pass"])


def _components(evaluation: dict[str, Any]) -> dict[str, dict[str, Any]]:
    found = {c["id"]: c for c in (evaluation.get("confidence") or {}).get("components") or []}
    missing = [cid for cid in COMPONENTS if cid not in found]
    if missing:
        raise ValueError(f"eval confidence is missing {missing}")
    return found


def _cell(component: dict[str, Any]) -> str:
    if not component.get("assessed"):
        return "not assessed"
    counts = [f"{m['k']}/{m['n']}" for m in component.get("measures") or [] if m.get("n")]
    text = f"{component['lower_bound']} % LB"
    if counts:
        text += f" ({', '.join(counts)})"
    return text


def stability_cell(stability: dict[str, Any]) -> str:
    measures = stability.get("measures") or []
    if not measures:
        raise ValueError("stability report has no measures")
    weakest = min(measures, key=lambda m: m["lower_bound"])
    bound = round(100 * weakest["lower_bound"], 2)
    return (f"{bound} % LB weakest ({weakest['name']} {weakest['k']}/{weakest['n']})")


def measured_cells(holdout_eval: dict[str, Any], stability: dict[str, Any]) -> dict[str, str]:
    """Held-out components, with C5 taken from the stability run."""
    cells = {cid: _cell(comp) for cid, comp in _components(holdout_eval).items()}
    cells["C5"] = stability_cell(stability)
    cells["AL"] = (f"{len(LINEAGE)} P1–P4 roles hand one field to a consumer; "
                   f"{len(CRITICS)} critics re-open upstream work")
    cells["Assurance"] = _assurance_cell(holdout_eval)
    return cells


def _assurance_cell(evaluation: dict[str, Any]) -> str:
    block = evaluation.get("assurance") or {}
    if "coverage_pct" not in block:
        return "not in this eval"
    return (f"{block['coverage_pct']} % coverage ({block.get('released_items', 0)} released items; "
            f"independent {block.get('independent_pct')} %)")


def render_split(split: str, e2e: dict[str, Any], evaluation: dict[str, Any],
                 stability: dict[str, Any] | None = None) -> str:
    rate = dispatch_rate(e2e)
    passed = gate_passed(evaluation)
    comps = _components(evaluation)
    lines = [
        f"# Wave report — {split}",
        "",
        f"Job: {e2e.get('job_id') or evaluation.get('job') or 'unrecorded'}",
        f"Dispatch success: {rate} % (threshold > {DISPATCH_MIN} %). "
        f"{'PASS' if rate > DISPATCH_MIN else 'FAIL'}.",
        f"Step 33 gate: {'PASS' if passed else 'FAIL'}.",
        "",
        "| Component | Measured |",
        "|---|---|",
    ]
    for cid, name in COMPONENTS.items():
        lines.append(f"| {cid} {name} | {_cell(comps[cid])} |")
    if stability is not None:
        lines.extend(["", "## Stability run", ""])
        for measure in stability.get("measures") or []:
            lines.append(
                f"- {measure['name']}: {measure['k']}/{measure['n']} "
                f"(LB {round(100 * measure['lower_bound'], 2)} %)")
        lines.append("")
        lines.append(f"Weakest stability measure: {stability_cell(stability)}.")
    else:
        lines.extend([
            "",
            "C5 is not re-measured on this split. The stability run is in the tune report.",
        ])
    lines.extend([
        "",
        f"Assurance: {_assurance_cell(evaluation)}.",
        f"P1–P4 lineage: {len(LINEAGE)} consumed fields. Critics: {len(CRITICS)}.",
        "C4 stays not assessed: expert labels were skipped. C7 stays 0: the sandbox was deferred.",
        "C9 ignores scripted confirmations.",
    ])
    return "\n".join(lines) + "\n"


def apply_measurements(roadmap: str, measured: dict[str, str]) -> str:
    """Insert a measured column into roadmap §4. The baseline column stays."""
    if _HEADER not in roadmap:
        raise ValueError("roadmap §4 table header was not found")
    required = {"AL", "Assurance", *COMPONENTS}
    missing = required - measured.keys()
    if missing:
        raise ValueError(f"measured cells missing {sorted(missing)}")
    out = []
    in_targets = False
    for line in roadmap.splitlines():
        if line.startswith("## 4. Targets"):
            in_targets = True
            out.append(line)
            continue
        if in_targets and line.startswith("## "):
            in_targets = False
        if not in_targets:
            out.append(line)
            continue
        if line == _HEADER:
            out.append(_MEASURED_HEADER)
            continue
        if line.startswith("|---"):
            out.append("|---|---|---|---|---|")
            continue
        key = _row_key(line)
        if key is None:
            out.append(line)
            continue
        parts = line.split("|")
        parts.insert(3, f" {measured[key]} ")
        out.append("|".join(parts))
    return "\n".join(out) + ("\n" if roadmap.endswith("\n") else "")


def _row_key(line: str) -> str | None:
    if not line.startswith("| "):
        return None
    cell = line.split("|")[1].strip()
    if cell.startswith("AL"):
        return "AL"
    if cell.startswith("Assurance"):
        return "Assurance"
    for cid in COMPONENTS:
        if cell.startswith(cid + " "):
            return cid
    return None


def report_ok(e2e: dict[str, Any], evaluation: dict[str, Any]) -> bool:
    return dispatch_rate(e2e) > DISPATCH_MIN and gate_passed(evaluation)
