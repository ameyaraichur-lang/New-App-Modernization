"""Astra = Azure OpenAI Responses API client.

Stateless by design: callers pass the full input item list each turn (prior
``function_call``/``reasoning`` items included) so requests are content-
addressable for the record/replay cache. ``temperature``/``top_p`` are
rejected by the reasoning deployments and are never sent.
"""

from __future__ import annotations

import random
import time
from typing import Any

from appmod.config import Settings, get_settings
from appmod.llm.errors import (
    ContentFilteredError,
    ContextLengthError,
    DeploymentUnavailableError,
    LLMConfigError,
    LLMError,
    TransientLLMError,
)
from appmod.llm.types import ModelResponse, ToolSpec, Usage

NON_REASONING_PREFIXES = ("gpt-4", "gpt-35", "text-embedding")


def supports_reasoning(deployment: str) -> bool:
    return not deployment.lower().startswith(NON_REASONING_PREFIXES)


class AstraClient:
    def __init__(self, settings: Settings | None = None, max_attempts: int = 4):
        self.settings = settings or get_settings()
        if not self.settings.astra_configured:
            raise LLMConfigError("Astra endpoint/key not configured (APPMOD_ASTRA_* in .env)")
        from openai import AzureOpenAI
        self._client = AzureOpenAI(
            azure_endpoint=self.settings.astra_endpoint.rstrip("/"),
            api_key=self.settings.astra_api_key.get_secret_value(),
            api_version=self.settings.astra_api_version,
            max_retries=0,
            timeout=self.settings.llm_timeout_s,
        )
        self.max_attempts = max_attempts

    # -- responses --------------------------------------------------------------

    def create(self, deployment: str, *, instructions: str, input_items: list[dict[str, Any]],
               tools: list[ToolSpec] | None = None, tool_choice: str | dict | None = None,
               reasoning_effort: str | None = None, text_format: dict[str, Any] | None = None,
               max_output_tokens: int | None = None) -> ModelResponse:
        kwargs: dict[str, Any] = {"model": deployment, "instructions": instructions,
                                  "input": input_items}
        if tools:
            kwargs["tools"] = [t.to_responses_tool() for t in tools]
            kwargs["tool_choice"] = tool_choice or "auto"
            kwargs["parallel_tool_calls"] = True
        if reasoning_effort and supports_reasoning(deployment):
            kwargs["reasoning"] = {"effort": reasoning_effort}
        if text_format:
            kwargs["text"] = {"format": text_format}
        if max_output_tokens:
            kwargs["max_output_tokens"] = max_output_tokens
        return self._with_retry(lambda: self._create_once(deployment, kwargs))

    def _create_once(self, deployment: str, kwargs: dict[str, Any]) -> ModelResponse:
        t0 = time.monotonic()
        resp = self._call(lambda: self._client.responses.create(**kwargs), deployment)
        items = [i.model_dump(exclude_none=True) for i in (resp.output or [])]
        u = resp.usage
        usage = Usage(
            input_tokens=getattr(u, "input_tokens", 0) or 0,
            output_tokens=getattr(u, "output_tokens", 0) or 0,
            reasoning_tokens=getattr(getattr(u, "output_tokens_details", None), "reasoning_tokens", 0) or 0,
            cached_tokens=getattr(getattr(u, "input_tokens_details", None), "cached_tokens", 0) or 0,
        ) if u else Usage()
        status = resp.status or "completed"
        if status == "incomplete":
            reason = getattr(resp.incomplete_details, "reason", "") or ""
            if reason == "content_filter":
                raise ContentFilteredError(f"{deployment}: completion filtered")
        return ModelResponse(
            response_id=resp.id, deployment=deployment, model=resp.model or deployment,
            output_items=items, text=resp.output_text or "", usage=usage, status=status,
            latency_ms=int((time.monotonic() - t0) * 1000),
        )

    # -- embeddings ---------------------------------------------------------------

    def embed(self, texts: list[str], deployment: str | None = None) -> list[list[float]]:
        dep = deployment or self.settings.tier_embedding
        out: list[list[float]] = []
        for i in range(0, len(texts), 64):
            batch = [t[:24000] or " " for t in texts[i:i + 64]]
            resp = self._with_retry(lambda b=batch: self._call(
                lambda: self._client.embeddings.create(model=dep, input=b), dep))
            out.extend(d.embedding for d in sorted(resp.data, key=lambda d: d.index))
        return out

    # -- error mapping ------------------------------------------------------------

    def _call(self, fn, deployment: str):
        import openai
        try:
            return fn()
        except openai.RateLimitError as e:
            raise TransientLLMError(f"{deployment}: rate limited", _retry_after(e)) from e
        except (openai.APITimeoutError, openai.APIConnectionError) as e:
            raise TransientLLMError(f"{deployment}: {type(e).__name__}") from e
        except openai.InternalServerError as e:
            raise TransientLLMError(f"{deployment}: server error {e.status_code}") from e
        except openai.NotFoundError as e:
            raise DeploymentUnavailableError(f"{deployment}: deployment not found") from e
        except (openai.AuthenticationError, openai.PermissionDeniedError) as e:
            raise LLMConfigError(f"{deployment}: auth failed ({e.status_code})") from e
        except openai.BadRequestError as e:
            body = str(getattr(e, "body", "") or e)
            if "content_filter" in body or "ResponsibleAIPolicyViolation" in body:
                raise ContentFilteredError(f"{deployment}: prompt filtered") from e
            if "context_length" in body or "maximum context" in body:
                raise ContextLengthError(f"{deployment}: context length exceeded") from e
            raise LLMError(f"{deployment}: bad request: {body[:400]}") from e
        except openai.APIStatusError as e:
            if e.status_code in (408, 409, 425, 429) or e.status_code >= 500:
                raise TransientLLMError(f"{deployment}: HTTP {e.status_code}") from e
            raise LLMError(f"{deployment}: HTTP {e.status_code}") from e

    def _with_retry(self, fn):
        for attempt in range(1, self.max_attempts + 1):
            try:
                return fn()
            except TransientLLMError as e:
                if attempt == self.max_attempts:
                    raise
                wait = e.retry_after if e.retry_after else min(30.0, 1.5 * 2 ** (attempt - 1))
                time.sleep(wait + random.uniform(0, 0.5))
        raise AssertionError("unreachable")


def _retry_after(e) -> float | None:
    try:
        v = e.response.headers.get("retry-after-ms")
        if v:
            return float(v) / 1000
        v = e.response.headers.get("retry-after")
        return float(v) if v else None
    except Exception:
        return None
