"""Assurance classes for released items (stack plan decision 3).

An item — a finding, or a payload entry carrying an ``evidence_class`` — crosses a release
gate only when something other than the model that wrote it stands behind it:

  execution-verified  a runtime check passed (reserved: P5 sandbox deferred, decision 1)
  tool-measured       written by a deterministic tool, not a model
  entailed            a model claim the claim-support verifier found entailed by its evidence
  human-confirmed     confirmed by a human: a recorded answer, or the gate reviewer
  scripted-confirmed  confirmed by automation standing in for a human (scripted e2e actors,
                      simulated pilot reviewers); lets gates pass, never counts as human
  unverified          anything else; the release gate lists it for confirmation

``with_assurance`` wraps a release gate: its decision record carries the class counts and the
unverified items, so a human review shows exactly what the approval confirms. Without human
review (simulated mode) the simulated reviewer confirms them as scripted-confirmed.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Callable, Iterator

from appmod.kernel.gates import GateContext, GateResult

CLASSES = ("execution-verified", "tool-measured", "entailed", "human-confirmed",
           "scripted-confirmed", "unverified")
SCRIPTED_PREFIXES = ("scripted-", "sim-", "pilot-simulated")
MAX_LISTED = 200


def is_scripted(actor: str | None) -> bool:
    return not actor or str(actor).startswith(SCRIPTED_PREFIXES)


def confirmation_class(actor: str | None) -> str:
    return "scripted-confirmed" if is_scripted(actor) else "human-confirmed"


def items(art: dict[str, Any]) -> Iterator[tuple[str, dict[str, Any]]]:
    for i, f in enumerate(art.get("findings") or []):
        if isinstance(f, dict) and "evidence_class" in f:
            yield f"findings[{i}]", f
    for key, value in (art.get("payload") or {}).items():
        if isinstance(value, list):
            for j, it in enumerate(value):
                if isinstance(it, dict) and "evidence_class" in it:
                    yield f"payload.{key}[{j}]", it
        elif isinstance(value, dict) and "evidence_class" in value:
            yield f"payload.{key}", value


def classify(item: dict[str, Any]) -> str:
    """Class before any gate confirmation."""
    if item.get("origin") != "llm":
        if item.get("evidence_class") == "HUMAN_CONFIRMED" and item.get("respondent"):
            return confirmation_class(item["respondent"])
        return "tool-measured"
    if (item.get("support") or {}).get("verdict") == "ENTAILED":
        return "entailed"
    return "unverified"


def _label(item: dict[str, Any]) -> str:
    for k in ("statement", "rationale", "proposed_disposition", "boundary", "name", "title", "task"):
        if item.get(k):
            return str(item[k])[:240]
    return ", ".join(f"{k}={v}" for k, v in item.items() if isinstance(v, str | int | float)
                     and k not in ("origin", "evidence_class"))[:240]


def assess(published: dict[str, dict[str, Any]]) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    unverified: list[dict[str, Any]] = []
    for art in published.values():
        if not isinstance(art, dict) or not art.get("artifact_id"):
            continue
        for path, it in items(art):
            cls = classify(it)
            counts[cls] += 1
            if cls == "unverified" and len(unverified) < MAX_LISTED:
                unverified.append({"artifact": art["artifact_id"], "version": art.get("artifact_version"),
                                   "path": path, "evidence_class": it.get("evidence_class"),
                                   "verdict": (it.get("support") or {}).get("verdict"),
                                   "item": _label(it)})
    return {"counts": {c: counts[c] for c in CLASSES if counts[c]},
            "unverified_count": counts["unverified"], "unverified": unverified}


def confirm(record: dict[str, Any], actor: str | None, at: str | None = None) -> dict[str, Any]:
    """The gate decision by ``actor`` confirms the record's unverified items."""
    a = record.get("assurance")
    if not isinstance(a, dict):
        return record
    n = a.get("unverified_count", 0)
    cls = confirmation_class(actor)
    counts = {k: v for k, v in a.get("counts", {}).items() if k != "unverified"}
    if n:
        counts[cls] = counts.get(cls, 0) + n
    a = dict(a, counts={c: counts[c] for c in CLASSES if counts.get(c)},
             confirmed={"by": actor, "class": cls, "items": n, "at": at})
    return dict(record, assurance=a)


def with_assurance(impl: Callable[[GateContext], GateResult], *,
                   human_review: bool = False) -> Callable[[GateContext], GateResult]:
    """``human_review``: a reviewer decides next (``with_human_review``), so items stay unverified
    in the proposal; otherwise the gate's own (simulated) authorizer confirms them."""
    def gate_fn(ctx: GateContext) -> GateResult:
        res = impl(ctx)
        record = (res.payload or {}).get("decision_record")
        if res.outcome == "FAILED" or not isinstance(record, dict):
            return res
        record = dict(record, assurance=assess(ctx.published))
        if not human_review:
            record = confirm(record, record.get("authorized_by"), record.get("authorized_at"))
        return GateResult(res.outcome, res.status, {**res.payload, "decision_record": record},
                          res.reasons)
    return gate_fn
