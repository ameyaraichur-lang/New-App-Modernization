"""DAG scheduler: pure readiness computation over a compiled phase registry.

Run Controls ('Required dependencies'): 'Dispatch only after all listed hard
prerequisites publish schema-valid outcome records. A failed prerequisite
blocks its dependants; a permitted PARTIAL record propagates gaps.'

Async lanes (e.g. P1.A8) never block their consumers — consumers must handle
the PENDING state explicitly instead (blueprint: 'A8 completion never gates
technical fan-in').
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

CONSUMABLE = {"COMPLETE", "PARTIAL", "NOT_ASSESSED", "SKIPPED_APPROVED"}


@dataclass
class NodeState:
    node_id: str
    kind: str                      # agent | gate | execution
    lane: str = "normal"           # normal | async
    status: str = "PENDING"        # PENDING | RUNNING | PUBLISHED | FAILED | BLOCKED
    outcome: str | None = None     # artifact status once published
    attempts: int = 0


@dataclass
class SchedulerState:
    nodes: dict[str, NodeState] = field(default_factory=dict)

    def set_outcome(self, node: str, outcome: str) -> None:
        ns = self.nodes[node]
        ns.outcome = outcome
        ns.status = "PUBLISHED" if outcome != "FAILED" else "FAILED"

    def fail(self, node: str) -> None:
        self.nodes[node].status = "FAILED"
        self.nodes[node].outcome = "FAILED"


class Scheduler:
    def __init__(self, phase_reg: dict):
        self.phase = phase_reg["phase"]
        agents = {a["local_id"]: a for a in phase_reg["agents"]}
        self.edges = [e for e in phase_reg["hard_edges"] if e["type"] in ("HARD",)]
        # include typed milestone edges that gate execution (P9 ACTIVATE etc.
        # are lifecycle-only and excluded; only HARD blocks dispatch)
        self.incoming: dict[str, list[str]] = {}
        for e in self.edges:
            self.incoming.setdefault(e["to"], []).append(e["from"])
        self.nodes: dict[str, NodeState] = {}
        for nid, agents_spec in agents.items():
            self.nodes[nid] = NodeState(nid, "agent", agents_spec.get("lane", "normal"))
        for g in phase_reg["gates"]:
            self.nodes[g["id"]] = NodeState(g["id"], g["node_type"] or "gate")

    # ------------------------------------------------------------------

    def blocked_reasons(self, node: str, state: SchedulerState) -> list[str]:
        """Why `node` cannot dispatch now. Empty list == ready."""
        reasons: list[str] = []
        for src in self.incoming.get(node, []):
            src_state = state.nodes.get(src)
            if src_state is None:
                reasons.append(f"unknown prerequisite {src}")
                continue
            if src_state.lane == "async":
                continue  # async lanes never gate consumers (P1.A8 rule)
            if src_state.status in ("FAILED", "BLOCKED"):
                reasons.append(f"{src} {src_state.status}")
            elif src_state.status in ("PENDING", "RUNNING"):
                reasons.append(f"{src} not published")
            elif src_state.status == "PUBLISHED" and src_state.outcome not in CONSUMABLE:
                reasons.append(f"{src} outcome {src_state.outcome} not consumable")
        return reasons

    def ready_nodes(self, state: SchedulerState) -> list[str]:
        return [
            nid for nid, ns in state.nodes.items()
            if ns.status == "PENDING" and not self.blocked_reasons(nid, state)
        ]

    def propagate_blockage(self, state: SchedulerState) -> list[str]:
        """Transitively mark nodes whose ancestors FAILED/BLOCKED as BLOCKED."""
        changed: list[str] = []
        for nid in state.nodes:
            if state.nodes[nid].status in ("PENDING",):
                reasons = self.blocked_reasons(nid, state)
                hard_blocks = [r for r in reasons if r.endswith(("FAILED", "BLOCKED"))]
                if hard_blocks:
                    state.nodes[nid].status = "BLOCKED"
                    changed.append(nid)
        return changed

    def new_state(self) -> SchedulerState:
        st = SchedulerState()
        for nid, ns in self.nodes.items():
            st.nodes[nid] = NodeState(nid, ns.kind, ns.lane)
        return st
