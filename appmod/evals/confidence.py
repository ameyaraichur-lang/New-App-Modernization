"""Confidence score: nine measured components, each at its 95 % Wilson lower bound.

The overall score is the weakest component. An unmeasured component scores 0 — the
pipeline rule that NOT_RUN never counts as PASS applies to confidence too.
Definitions: docs/NEXT_LEVEL_AGENTIC_ROADMAP.md §1.2.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from appmod.evals.stats import wilson_lower

COMPONENTS: dict[str, str] = {
    "C1": "Integrity",
    "C2": "Factual accuracy",
    "C3": "Claim support",
    "C4": "Decision correctness",
    "C5": "Stability",
    "C6": "Calibration",
    "C7": "Execution proof",
    "C8": "Robustness",
    "C9": "Human acceptance",
}


@dataclass
class Measure:
    """One proportion: k of n checks passed."""

    name: str
    k: int
    n: int

    @property
    def lower(self) -> float | None:
        return wilson_lower(self.k, self.n)


@dataclass
class Component:
    cid: str
    measures: list[Measure] = field(default_factory=list)
    reason: str = ""

    @property
    def name(self) -> str:
        return COMPONENTS[self.cid]

    @property
    def assessed(self) -> bool:
        return any(m.n > 0 for m in self.measures)

    @property
    def lower(self) -> float:
        bounds = [b for m in self.measures if (b := m.lower) is not None]
        return min(bounds) if bounds else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.cid, "name": self.name, "assessed": self.assessed,
                "lower_bound": round(100 * self.lower, 2), "reason": self.reason,
                "measures": [asdict(m) | {"lower_bound": None if m.lower is None
                                          else round(100 * m.lower, 2)} for m in self.measures]}


def score(components: list[Component]) -> dict[str, Any]:
    """Weakest-link score over all nine components; unmeasured components count as 0."""
    by_id = {c.cid: c for c in components}
    missing = [cid for cid in COMPONENTS if cid not in by_id]
    if missing:
        raise ValueError(f"components missing: {missing}")
    ordered = [by_id[cid] for cid in COMPONENTS]
    weakest = min(ordered, key=lambda c: c.lower if c.assessed else 0.0)
    assessed = [c for c in ordered if c.assessed]
    return {
        "confidence_score": round(100 * (weakest.lower if weakest.assessed else 0.0), 2),
        "weakest": weakest.cid,
        "assessed": [c.cid for c in assessed],
        "not_assessed": [c.cid for c in ordered if not c.assessed],
        "weakest_assessed": (min(assessed, key=lambda c: c.lower).cid if assessed else None),
        "components": [c.to_dict() for c in ordered],
    }
