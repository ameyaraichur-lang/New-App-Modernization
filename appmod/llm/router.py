"""Model router: tier -> deployment, cache, TPM limiting, one-hop failover.

Every call (including cache hits and failures) is reported through
``on_call`` so the orchestrator can journal MODEL_CALL events with the
deployment, model version, token usage and latency.
"""

from __future__ import annotations

import json
import threading
from typing import Any, Callable

from appmod.config import Settings, get_settings
from appmod.llm.cache import ResponseCache
from appmod.llm.errors import ConnectivityError, DeploymentUnavailableError, TransientLLMError
from appmod.llm.outage import OutageGate
from appmod.llm.ratelimit import TokenBucket
from appmod.llm.types import ModelResponse, ToolSpec, Usage

CallHook = Callable[[dict[str, Any]], None]


class ModelRouter:
    def __init__(self, settings: Settings | None = None, client: Any = None,
                 cache: ResponseCache | None = None, limiter: TokenBucket | None = None):
        self.settings = settings or get_settings()
        if client is None:
            from appmod.llm.astra import AstraClient
            client = AstraClient(self.settings)
        self.client = client
        self.cache = cache or ResponseCache(self.settings.runs_dir / "llm_cache",
                                            self.settings.llm_cache)
        self.limiter = limiter or TokenBucket(self.settings.llm_tpm_limit)
        probe = getattr(client, "reachable", None)
        self.outage: OutageGate | None = (
            OutageGate(probe, max_wait_s=self.settings.llm_outage_max_wait_s) if callable(probe) else None)
        self.usage = Usage()
        self.calls = 0
        self.failovers = 0
        self._lock = threading.Lock()

    @property
    def model_version(self) -> str:
        return self.settings.astra_model_version

    def complete(self, tier: str, *, instructions: str, input_items: list[dict[str, Any]],
                 tools: list[ToolSpec] | None = None, tool_choice: str | dict | None = None,
                 reasoning_effort: str | None = None, text_format: dict[str, Any] | None = None,
                 max_output_tokens: int | None = None, on_call: CallHook | None = None,
                 context: dict[str, Any] | None = None) -> ModelResponse:
        args = dict(instructions=instructions, input_items=input_items, tools=tools,
                    tool_choice=tool_choice, reasoning_effort=reasoning_effort,
                    text_format=text_format, max_output_tokens=max_output_tokens)
        while True:
            try:
                return self._complete_once(tier, args, on_call, context)
            except TransientLLMError as exc:
                if not self._outage_over(exc):
                    raise

    def _outage_over(self, exc: TransientLLMError) -> bool:
        """True once an outage that caused ``exc`` has ended; False if ``exc`` is not an outage."""
        if self.outage is None:
            return False
        if not isinstance(exc, ConnectivityError) and self.outage.reachable():
            return False
        return self.outage.wait()

    def _complete_once(self, tier: str, args: dict[str, Any], on_call: CallHook | None,
                       context: dict[str, Any] | None) -> ModelResponse:
        primary = self.settings.deployment_for(tier)
        fallback = self.settings.deployment_for("fallback")
        try:
            resp = self._call(primary, args)
        except (TransientLLMError, DeploymentUnavailableError) as exc:
            self._report(on_call, context, tier, primary, None, error=exc)
            if fallback == primary:
                raise
            resp = self._call(fallback, args)
            resp.failover = True
            with self._lock:
                self.failovers += 1
        self._report(on_call, context, tier, resp.deployment, resp)
        return resp

    def _call(self, deployment: str, args: dict[str, Any]) -> ModelResponse:
        request = {
            "deployment": deployment,
            **{k: v for k, v in args.items() if k != "tools"},
            "tools": [t.to_responses_tool() for t in (args.get("tools") or [])],
        }
        est = int(len(json.dumps(request, default=str)) / 3.5) + int(args.get("max_output_tokens") or 4000)

        def live() -> ModelResponse:
            self.limiter.acquire(est)
            try:
                r = self.client.create(deployment, **args)
            except Exception:
                self.limiter.settle(est, 0)
                raise
            self.limiter.settle(est, r.usage.total)
            return r

        resp = self.cache.get_or_call(request, live)
        with self._lock:
            self.calls += 1
            if not resp.cached:
                self.usage.add(resp.usage)
        return resp

    def _report(self, hook: CallHook | None, context: dict[str, Any] | None, tier: str,
                deployment: str, resp: ModelResponse | None, error: Exception | None = None) -> None:
        if hook is None:
            return
        rec: dict[str, Any] = {"tier": tier, "deployment": deployment,
                               "model_version": self.model_version, **(context or {})}
        if resp is not None:
            rec.update(response_id=resp.response_id, model=resp.model, cached=resp.cached,
                       failover=resp.failover, latency_ms=resp.latency_ms, status=resp.status,
                       input_tokens=resp.usage.input_tokens, output_tokens=resp.usage.output_tokens,
                       reasoning_tokens=resp.usage.reasoning_tokens,
                       tool_calls=[c.name for c in resp.function_calls])
        if error is not None:
            rec["error"] = f"{type(error).__name__}: {error}"
        hook(rec)
