"""Phase orchestrator: the run engine.

Ties together registry, scheduler, gates, store, policy, audit and the agent
runner. Responsibilities (all deterministic, outside any model):

  - assemble each dispatch's input manifest (exact upstream versions+hashes)
  - build idempotency keys: phase/application/agent/input-hash/policy-version
  - bounded retries for classified transient failures only
  - validate every publication against the phase contract; invalid => FAILED
  - route gates to their implementations and publish gate artifacts
  - propagate blockage; seal snapshots; produce handoff packages
  - record everything in the audit journal
"""

from __future__ import annotations

import hashlib
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable

from appmod.agents.runtime import AgentRunner, TransientAgentError
from appmod.contracts.schemas import (
    ContractValidator, canonical_json, content_hash, normalize_payload,
)
from appmod.kernel.audit import AuditJournal
from appmod.kernel.evidence import enforce as enforce_evidence
from appmod.kernel.gates import GateContext, gate_impl_for
from appmod.kernel.policy import PolicyService
from appmod.kernel.scheduler import Scheduler, SchedulerState
from appmod.store.artifact_store import ArtifactStore


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


@dataclass
class RunContext:
    run_id: str
    application_id: str
    phase: int
    policy_version: str
    state: SchedulerState
    inputs_by_node: dict[str, dict[str, Any]] = field(default_factory=dict)   # node -> artifact
    run_inputs: dict[str, Any] = field(default_factory=dict)
    published: dict[str, str] = field(default_factory=dict)   # node -> artifact_id
    finished: bool = False
    outcome_log: list[dict[str, Any]] = field(default_factory=list)


class PhaseOrchestrator:
    def __init__(
        self,
        phase_reg: dict[str, Any],
        store: ArtifactStore,
        policy: PolicyService,
        audit: AuditJournal,
        agent_runner: AgentRunner,
        gate_overrides: dict[str, Any] | None = None,
        max_parallel: int = 1,
        reuse: bool = False,
        external_digest: Any = None,
        force_nodes: set[str] | None = None,
        cancel_event: threading.Event | None = None,
    ):
        """reuse: adopt the latest stored artifact of a node when its input
        hash (upstream versions + policy + run inputs + runner fingerprint +
        external digest) is unchanged — this is what makes resume, approval
        re-entry and A8 answer invalidation cheap and exact.
        external_digest(node) -> str folds out-of-graph state (recorded
        answers, review decisions) into the node's input hash."""
        self.reuse = reuse
        self.external_digest = external_digest
        self.force_nodes = set(force_nodes or ())
        self.cancel_event = cancel_event
        self.reg = phase_reg
        self.phase = phase_reg["phase"]
        self.store = store
        self.policy = policy
        self.audit = audit
        self.runner = agent_runner
        self.scheduler = Scheduler(phase_reg)
        self.validator = ContractValidator(phase_reg)
        self.gate_overrides = gate_overrides or {}
        self.event_listener: Callable[[dict[str, Any]], None] | None = None   # live traces (SSE)
        self.max_parallel = max(1, int(max_parallel))
        self._lock = threading.RLock()
        # Policy version is pinned at construction; a run started without a
        # policy bundle (self.policy None) fails at G0 rather than crashing.
        self._pinned_policy_version = policy.version if policy else "UNSET"

    # ------------------------------------------------------------------
    # run lifecycle
    # ------------------------------------------------------------------

    def start_run(
        self, run_id: str, application_id: str, run_inputs: dict[str, Any]
    ) -> RunContext:
        ctx = RunContext(
            run_id=run_id,
            application_id=application_id,
            phase=self.phase,
            policy_version=self._pinned_policy_version,
            state=self.scheduler.new_state(),
            run_inputs=run_inputs,
        )
        return ctx

    def step(self, ctx: RunContext, on_event=None) -> list[dict[str, Any]]:
        """Dispatch every currently-ready node once (concurrently when
        ``max_parallel`` > 1). Returns step events in ready order."""
        if self.cancel_event is not None and self.cancel_event.is_set():
            ctx.finished = True
            self.audit.emit("CANCELLED", run_id=ctx.run_id)
            return []
        self.scheduler.propagate_blockage(ctx.state)
        ready = self.scheduler.ready_nodes(ctx.state)
        for node in ready:
            ctx.state.nodes[node].status = "RUNNING"

        def one(node: str) -> dict[str, Any]:
            ns = ctx.state.nodes[node]
            try:
                if ns.kind in ("gate", "execution"):
                    ev = self._run_gate(ctx, node)
                else:
                    ev = self._run_agent(ctx, node)
            except TransientAgentError as exc:
                with self._lock:
                    ev = self._handle_transient(ctx, node, exc)
            if on_event is not None:
                with self._lock:
                    try:
                        on_event(ctx, ev)
                    except Exception:
                        pass  # progress hooks must never break execution
            return ev

        if self.max_parallel > 1 and len(ready) > 1:
            with ThreadPoolExecutor(max_workers=min(self.max_parallel, len(ready))) as pool:
                events = list(pool.map(one, ready))
        else:
            events = [one(n) for n in ready]
        self.scheduler.propagate_blockage(ctx.state)
        waiting = {"RUNNING", "AWAITING_REVIEW", "AWAITING_INPUT"}
        if not self.scheduler.ready_nodes(ctx.state) and not any(
            n.status in waiting for n in ctx.state.nodes.values()
        ):
            ctx.finished = True
        return events

    def _handle_transient(self, ctx: RunContext, node: str, exc: TransientAgentError) -> dict[str, Any]:
        """Bounded retries for classified transient failures only
        (Run Controls: 'Use bounded retries only for classified transient
        failures... Attempts/time/cost bounded by G0 policy; exhausted work
        becomes FAILED and is escalated')."""
        ns = ctx.state.nodes[node]
        budget: int = self.policy.budgets.get("max_retries_per_agent", 2)
        if ns.attempts <= budget:
            ns.status = "PENDING"  # eligible for redispatch next step
            self.audit.emit("RETRY", run_id=ctx.run_id, node=node,
                            attempt=ns.attempts, reason=str(exc))
            return {"node": node, "status": "RETRY_SCHEDULED", "attempt": ns.attempts}
        ns.status = "FAILED"
        ns.outcome = "FAILED"
        self.audit.retry_exhausted(ctx.run_id, node, ns.attempts)
        return {"node": node, "status": "FAILED_RETRY_EXHAUSTED", "attempts": ns.attempts}

    def run(self, ctx: RunContext, max_steps: int = 100,
            on_event=None) -> list[dict[str, Any]]:
        all_events: list[dict[str, Any]] = []
        for _ in range(max_steps):
            if ctx.finished:
                break
            all_events.extend(self.step(ctx, on_event=on_event))
        return all_events

    # ------------------------------------------------------------------
    # input manifests + idempotency
    # ------------------------------------------------------------------

    def _input_manifest(self, ctx: RunContext, node: str) -> tuple[dict[str, Any], str, list[str]]:
        manifest: dict[str, Any] = {}
        parent_refs: list[str] = []
        for src in self.scheduler.incoming.get(node, []):
            art = ctx.inputs_by_node.get(src)
            if art is None:
                continue   # async lane not published yet — allowed, marked in manifest
            manifest[src] = {
                "artifact_id": art["artifact_id"],
                "version": art["artifact_version"],
                "content_hash": art["content_hash"],
                "status": art["status"],
            }
            parent_refs.append(f"{art['artifact_id']}@{art['artifact_version']}")
        manifest["_policy_version"] = ctx.policy_version
        manifest["_run_inputs_hash"] = hashlib.sha256(
            canonical_json(ctx.run_inputs).encode()
        ).hexdigest()
        fp = getattr(self.runner, "fingerprint", None)
        if callable(fp) and ctx.state.nodes[node].kind == "agent":
            per_node = getattr(self.runner, "fingerprint_for", None)
            ident = per_node(node) if callable(per_node) else fp()
            manifest["_runner"] = hashlib.sha256(str(ident).encode()).hexdigest()[:16]
        if self.external_digest is not None:
            ext = self.external_digest(node)
            if ext:
                manifest["_external"] = ext
        digest = hashlib.sha256(canonical_json(manifest).encode()).hexdigest()
        return manifest, digest, parent_refs

    def _artifact_id(self, ctx: RunContext, node: str) -> str:
        return f"P{self.phase}/{ctx.application_id}/{node}"

    def _idempotency_key(self, ctx: RunContext, node: str, input_hash: str) -> str:
        return f"P{self.phase}/{ctx.application_id}/{node}/{input_hash[:16]}/{ctx.policy_version}"

    # ------------------------------------------------------------------
    # execution paths
    # ------------------------------------------------------------------

    def _run_agent(self, ctx: RunContext, node: str) -> dict[str, Any]:
        agent_spec = next(a for a in self.reg["agents"] if a["local_id"] == node)
        with self._lock:
            manifest, input_hash, parent_refs = self._input_manifest(ctx, node)
            upstream = {
                src: ctx.inputs_by_node[src]
                for src in self.scheduler.incoming.get(node, [])
                if src in ctx.inputs_by_node
            }

        prior = self._reusable(ctx, node, input_hash)
        if prior is not None:
            return self._adopt(ctx, node, prior)
        ns = ctx.state.nodes[node]
        ns.attempts += 1
        self.audit.dispatch(ctx.run_id, node, ns.attempts, input_hash)

        if getattr(self.runner, "accepts_context", False):
            outcome = self.runner.run(agent_spec, upstream, self.policy,
                                      context=self._dispatch_context(ctx, node))
        else:
            outcome = self.runner.run(agent_spec, upstream, self.policy)
        if outcome.awaiting_input:
            with self._lock:
                ns.status = "AWAITING_INPUT"
                ctx.outcome_log.append({"node": node, "status": "AWAITING_INPUT",
                                        **outcome.awaiting_input})
            self.audit.emit("AWAITING_INPUT", run_id=ctx.run_id, node=node, **outcome.awaiting_input)
            return {"node": node, "status": "AWAITING_INPUT", **outcome.awaiting_input}
        for ev in enforce_evidence(outcome, self._secrets()):
            self.audit.emit("EVIDENCE_DOWNGRADE", run_id=ctx.run_id, node=node, **ev)
        outcome.payload = normalize_payload(
            outcome.payload, self.validator.schemas["payloads"].get(node)
        )

        art = self._assemble_envelope(
            ctx, node, outcome.status, outcome.payload,
            findings=outcome.findings, gaps=outcome.gaps,
            evidence_refs=outcome.evidence_refs, scope=outcome.scope,
            applicability=outcome.applicability, manifest=manifest,
            input_hash=input_hash, parent_refs=parent_refs,
            extra_metadata=outcome.execution_metadata,
        )
        return self._publish(ctx, node, art)

    def _dispatch_context(self, ctx: RunContext, node: str) -> dict[str, Any]:
        run_id, phase = ctx.run_id, self.phase

        def emit(kind: str, **fields: Any) -> None:
            self.audit.emit(kind, run_id=run_id, node=node, **fields)
            if self.event_listener is not None:
                try:
                    self.event_listener({"kind": kind, "phase": phase, "node": node, **fields})
                except Exception:
                    pass

        with self._lock:
            published = dict(ctx.inputs_by_node)
        return {"run_id": run_id, "phase": phase, "application_id": ctx.application_id,
                "node": node, "attempt": ctx.state.nodes[node].attempts,
                "published": published, "store": self.store,
                "run_inputs": ctx.run_inputs, "emit": emit}

    def _reusable(self, ctx: RunContext, node: str, input_hash: str) -> dict[str, Any] | None:
        if not self.reuse or node in self.force_nodes:
            return None
        aid = self._artifact_id(ctx, node)
        versions = self.store.versions(aid)
        if not versions:
            return None
        try:
            prior = self.store.get(aid, versions[-1])
        except Exception:
            return None
        if prior.get("input_hash") != input_hash or prior.get("status") == "FAILED":
            return None
        llm = prior.get("execution_metadata", {}).get("llm") or {}
        if llm.get("mode") == "seed-fallback":
            return None          # degraded output: always retry the model
        return prior

    def _adopt(self, ctx: RunContext, node: str, prior: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            ctx.inputs_by_node[node] = prior
            ctx.published[node] = prior["artifact_id"]
            ctx.state.set_outcome(node, prior["status"])
            ctx.outcome_log.append({"node": node, "status": prior["status"],
                                    "artifact_id": prior["artifact_id"], "reused": True})
        self.audit.emit("REUSE", run_id=ctx.run_id, node=node, artifact_id=prior["artifact_id"],
                        version=prior["artifact_version"], input_hash=prior["input_hash"])
        ev = {"node": node, "status": prior["status"], "artifact_id": prior["artifact_id"],
              "reused": True}
        outcome = (prior.get("scope") or {}).get("outcome")
        if outcome:
            ev["gate_outcome"] = outcome
            ev["reasons"] = []
        return ev

    @staticmethod
    def _secrets() -> list[str]:
        try:
            from appmod.config import get_settings
            return get_settings().secret_values()
        except Exception:
            return []

    def _run_gate(self, ctx: RunContext, node: str) -> dict[str, Any]:
        impl = self.gate_overrides.get(node) or gate_impl_for(node)
        with self._lock:
            manifest, input_hash, parent_refs = self._input_manifest(ctx, node)
            upstream = {
                src: ctx.inputs_by_node[src]
                for src in self.scheduler.incoming.get(node, [])
                if src in ctx.inputs_by_node
            }
            published_snapshot = dict(ctx.inputs_by_node)
        prior = self._reusable(ctx, node, input_hash)
        if prior is not None:
            return self._adopt(ctx, node, prior)
        ns = ctx.state.nodes[node]
        ns.attempts += 1
        self.audit.dispatch(ctx.run_id, node, ns.attempts, input_hash)
        gate_cfg = dict(self.gate_overrides.get(f"{node}:cfg", {}))
        if node not in ("G0",):
            # snapshot gates seal every non-gate predecessor by default
            required = sorted({
                s for s in self.scheduler.incoming.get(node, [])
                if ctx.state.nodes.get(s) is not None
                and ctx.state.nodes[s].kind == "agent"
                and ctx.state.nodes[s].lane != "async"
            })
            gate_cfg.setdefault("required_producers", required)
            async_lanes = [
                s for s in self.scheduler.incoming.get(node, [])
                if ctx.state.nodes.get(s) is not None and ctx.state.nodes[s].lane == "async"
            ]
            if async_lanes:
                gate_cfg.setdefault("allow_pending", async_lanes)
            if node != "G1" and len(required) == 1:
                gate_cfg.setdefault("candidate_node", required[0])

        gctx = GateContext(
            run_id=ctx.run_id,
            application_id=ctx.application_id,
            gate_id=node,
            policy=self.policy,
            inputs=upstream,
            run_inputs=ctx.run_inputs,
            gate_cfg=gate_cfg,
            published=published_snapshot,
        )
        result = impl(gctx)
        self.audit.gate(ctx.run_id, node, result.outcome, result.reasons)
        if result.outcome == "AWAITING_REVIEW":
            # human authority pending: nothing is published; dependants stay
            # unready until a recorded decision re-enters the gate
            with self._lock:
                ns.status = "AWAITING_REVIEW"
                ctx.outcome_log.append({"node": node, "status": "AWAITING_REVIEW"})
            return {"node": node, "status": "AWAITING_REVIEW", "gate_outcome": "AWAITING_REVIEW",
                    "reasons": result.reasons, "review": result.payload}

        art = self._assemble_envelope(
            ctx, node, result.status, result.payload,
            findings=[], gaps=[], evidence_refs=[],
            scope={"gate": node, "outcome": result.outcome},
            applicability={}, manifest=manifest, input_hash=input_hash,
            parent_refs=parent_refs,
        )
        ev = self._publish(ctx, node, art)
        ev["gate_outcome"] = result.outcome
        ev["reasons"] = result.reasons
        if result.outcome == "FAILED":
            ctx.state.fail(node)
        return ev

    # ------------------------------------------------------------------
    # envelope assembly + publication
    # ------------------------------------------------------------------

    def _assemble_envelope(
        self, ctx: RunContext, node: str, status: str, payload: dict[str, Any], *,
        findings: list, gaps: list, evidence_refs: list, scope: dict,
        applicability: dict, manifest: dict, input_hash: str, parent_refs: list[str],
        extra_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        artifact_id = self._artifact_id(ctx, node)
        art = {
            "schema_version": self.reg["schema_version"],
            "artifact_id": artifact_id,
            "artifact_version": max(self.store.versions(artifact_id) or [0]) + 1,
            "run_id": ctx.run_id,
            "application_id": ctx.application_id,
            "phase_id": self.phase,
            "producer_id": f"P{self.phase}.{node}",
            "input_manifest_ref": canonical_json(manifest),
            "input_hash": input_hash,
            "policy_version": ctx.policy_version,
            "status": status,
            "scope": scope,
            "applicability": applicability,
            "evidence_refs": evidence_refs,
            "findings": findings,
            "gaps": gaps,
            "contradictions": [],
            "payload": payload,
            "created_at": _now(),
            "execution_metadata": {
                "attempts": ctx.state.nodes[node].attempts,
                "idempotency_key": self._idempotency_key(ctx, node, input_hash),
                "parent_refs": parent_refs,
                "runner": type(self.runner).__name__,
                **(extra_metadata or {}),
            },
            "access_classification": "INTERNAL",
        }
        art["content_hash"] = content_hash(art)
        return art

    def _publish(self, ctx: RunContext, node: str, art: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            return self._publish_locked(ctx, node, art)

    def _publish_locked(self, ctx: RunContext, node: str, art: dict[str, Any]) -> dict[str, Any]:
        errors = self.validator.validate(art)
        if errors:
            # Run Controls: 'Invalid publication is FAILED, not a successful
            # empty result.' The FAILED record is stored (like any FAILED
            # envelope) so consumers block on it and the audit trail keeps it.
            art = dict(art)
            art["status"] = "FAILED"
            art["payload"] = {"validation_errors": errors}
            art["content_hash"] = content_hash(art)
            self.store.publish(art)
            ctx.inputs_by_node[node] = art
            ctx.published[node] = art["artifact_id"]
            ctx.state.fail(node)
            self.audit.publish(ctx.run_id, art["artifact_id"], art["artifact_version"],
                               "FAILED", art["content_hash"], validator_ok=False)
            ctx.outcome_log.append({"node": node, "status": "FAILED", "validation_errors": errors})
            return {"node": node, "status": "FAILED", "validation_errors": errors}

        pointer = self.store.publish(art)
        ctx.inputs_by_node[node] = art
        ctx.published[node] = art["artifact_id"]
        ctx.state.set_outcome(node, art["status"])
        self.audit.publish(ctx.run_id, art["artifact_id"], art["artifact_version"],
                           art["status"], art["content_hash"], validator_ok=True)
        ctx.outcome_log.append({"node": node, "status": art["status"],
                                "artifact_id": art["artifact_id"]})
        return {"node": node, "status": art["status"], "artifact_id": art["artifact_id"]}
