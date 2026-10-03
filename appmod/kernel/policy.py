"""Policy service (G0 engagement policy bundle).

Blueprint AH05: phases require approved criteria/thresholds; organization
values must not be invented by the model. This service loads a *versioned*
policy bundle; pilots use bundles explicitly labeled `pilot-default` —
never silent, never presented as owner-approved production policy.
Missing policy blocks decisions that depend on it (Run Controls G0).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class PolicyError(Exception):
    pass


PILOT_DEFAULT_P1: dict[str, Any] = {
    "policy_version": "pilot-default-1.0.0",
    "kind": "engagement-policy",
    "label": "PILOT DEFAULT — not owner-approved production policy",
    "scope": {"phases": [1, 2, 3, 4, 5, 6]},
    "risk_taxonomy": {
        "dimensions": [
            "technical", "security", "data", "operational", "organizational",
        ],
        # Simple pilot rubric: each dimension scored 1-5 with evidence refs;
        # unknown evidence must be listed, never averaged away.
        "scale": {"min": 1, "max": 5},
        "unknown_handling": "UNASSESSED dimensions are listed, not scored",
        "thresholds": {"high_risk": 4, "blocker": 5},
    },
    "evidence": {
        "required_classes_for_decisions": ["OBSERVED", "DOCUMENTED", "HUMAN_CONFIRMED"],
        "hypothetical_counts_as": "never decision evidence",
    },
    "budgets": {
        "max_retries_per_agent": 2,
        "max_revision_cycles": 3,
        "max_parallel_agents": 4,
    },
    "reviewers": {
        # Simulated principals for pilots; every review event records
        # simulated=true (blueprint F05 discipline: simulated responses are
        # labeled, and they restrict — never widen — decision scope).
        "simulated": {
            "portfolio": "sim-pilot-portfolio-reviewer",
            "architecture": "sim-pilot-architecture-reviewer",
            "release": "sim-pilot-release-reviewer",
        }
    },
}


class PolicyService:
    def __init__(self, bundle: dict[str, Any] | None = None, path: Path | None = None):
        if bundle is None and path is not None:
            bundle = json.loads(Path(path).read_text(encoding="utf-8"))
        if bundle is None:
            bundle = json.loads(json.dumps(PILOT_DEFAULT_P1))  # deep copy
        PolicyService._validate(bundle)
        self.bundle = bundle

    @staticmethod
    def _validate(bundle: dict[str, Any]) -> None:
        for key in ("policy_version", "kind", "label"):
            if key not in bundle:
                raise PolicyError(f"policy bundle missing {key}")
        if "risk_taxonomy" not in bundle:
            raise PolicyError(
                "policy bundle missing risk_taxonomy — Run Controls G0: missing "
                "risk rubric blocks A11-style final scoring"
            )
        if "budgets" not in bundle or "max_retries_per_agent" not in bundle["budgets"]:
            raise PolicyError("policy bundle missing retry budgets")

    @property
    def version(self) -> str:
        return self.bundle["policy_version"]

    @property
    def budgets(self) -> dict[str, Any]:
        return self.bundle["budgets"]

    @property
    def reviewers(self) -> dict[str, Any]:
        return self.bundle.get("reviewers", {})

    def get(self, *path: str) -> Any:
        node: Any = self.bundle
        for key in path:
            if not isinstance(node, dict) or key not in node:
                raise PolicyError(f"policy path {'/'.join(path)} missing")
            node = node[key]
        return node

    def save(self, path: Path) -> None:
        Path(path).write_text(json.dumps(self.bundle, indent=2), encoding="utf-8")
