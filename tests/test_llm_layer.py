"""LLM layer offline: cache modes, failover, limiter, redaction."""

import pytest

from appmod.config import Settings, redact
from appmod.llm.cache import ResponseCache
from appmod.llm.errors import ReplayMissError, TransientLLMError
from appmod.llm.ratelimit import TokenBucket
from appmod.llm.router import ModelRouter
from appmod.llm.types import ModelResponse, Usage


class FakeClient:
    def __init__(self, fail: set[str] | None = None):
        self.fail = fail or set()
        self.calls: list[str] = []

    def create(self, deployment, **kw):
        self.calls.append(deployment)
        if deployment in self.fail:
            raise TransientLLMError(f"{deployment} down")
        return ModelResponse(response_id=f"r{len(self.calls)}", deployment=deployment, model=deployment,
                             output_items=[{"type": "message", "content": []}], text="ok",
                             usage=Usage(input_tokens=10, output_tokens=5))


def _settings(tmp_path, **kw):
    return Settings(_env_file=None, astra_endpoint="https://x", astra_api_key="k" * 20,
                    runs_dir=tmp_path, **kw)


def test_cache_read_through_and_replay(tmp_path):
    client = FakeClient()
    r = ModelRouter(_settings(tmp_path), client, ResponseCache(tmp_path / "c", "read"))
    a = r.complete("reasoning", instructions="i", input_items=[{"role": "user", "content": "x"}])
    b = r.complete("reasoning", instructions="i", input_items=[{"role": "user", "content": "x"}])
    assert not a.cached and b.cached and len(client.calls) == 1
    replay = ModelRouter(_settings(tmp_path), FakeClient(), ResponseCache(tmp_path / "c", "replay"))
    assert replay.complete("reasoning", instructions="i",
                           input_items=[{"role": "user", "content": "x"}]).text == "ok"
    with pytest.raises(ReplayMissError):
        replay.complete("reasoning", instructions="other", input_items=[])


def test_failover_once_to_fallback(tmp_path):
    s = _settings(tmp_path)
    client = FakeClient(fail={s.reasoning_deployment})
    seen = []
    r = ModelRouter(s, client, ResponseCache(tmp_path / "c", "off"))
    resp = r.complete("reasoning", instructions="i", input_items=[], on_call=seen.append)
    assert resp.failover and resp.deployment == s.tier_fallback
    assert "error" in seen[0] and seen[1]["failover"] is True


def test_failover_exhausted_raises(tmp_path):
    s = _settings(tmp_path)
    r = ModelRouter(s, FakeClient(fail={s.reasoning_deployment, s.tier_fallback}),
                    ResponseCache(tmp_path / "c", "off"))
    with pytest.raises(TransientLLMError):
        r.complete("reasoning", instructions="i", input_items=[])


def test_token_bucket_settles():
    b = TokenBucket(60_000)
    b.acquire(50_000)
    b.settle(50_000, 1_000)
    b.acquire(50_000)
    with pytest.raises(TimeoutError):
        b.acquire(59_000, timeout=0.1)


def test_redact_masks_key(tmp_path):
    s = _settings(tmp_path)
    assert "k" * 20 not in redact(f"key={'k' * 20}", s)


def _astra(tmp_path, handler):
    import httpx
    from openai import AzureOpenAI

    from appmod.llm.astra import AstraClient
    s = _settings(tmp_path, astra_api_version="2025-04-01-preview")
    c = AstraClient(s, max_attempts=1)
    c._client = AzureOpenAI(azure_endpoint="https://x.invalid", api_key="k" * 20,
                            api_version=s.astra_api_version, max_retries=0,
                            http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    return c


RESPONSE = {"id": "resp_1", "object": "response", "created_at": 0, "model": "gpt-6-astra",
            "status": "completed", "parallel_tool_calls": True, "tool_choice": "auto", "tools": [],
            "output": [{"type": "message", "id": "m1", "role": "assistant", "status": "completed",
                        "content": [{"type": "output_text", "text": "hi", "annotations": []}]}],
            "usage": {"input_tokens": 3, "output_tokens": 2, "total_tokens": 5,
                      "input_tokens_details": {"cached_tokens": 1},
                      "output_tokens_details": {"reasoning_tokens": 1}}}


def test_astra_client_request_shape_and_usage(tmp_path):
    import json

    import httpx
    sent = []

    def ok(req):
        sent.append(json.loads(req.content))
        return httpx.Response(200, json=RESPONSE)
    c = _astra(tmp_path, ok)
    r = c.create("gpt-6-astra", instructions="i", input_items=[{"role": "user", "content": "x"}],
                 reasoning_effort="high")
    c.create("gpt-4.1-mini", instructions="i", input_items=[], reasoning_effort="low")
    assert r.text == "hi" and r.response_id == "resp_1"
    assert (r.usage.input_tokens, r.usage.output_tokens, r.usage.reasoning_tokens, r.usage.cached_tokens) == (3, 2, 1, 1)
    assert all("temperature" not in b and "top_p" not in b for b in sent)
    assert sent[0]["reasoning"] == {"effort": "high"} and "reasoning" not in sent[1]


@pytest.mark.parametrize("status,body,err", [
    (429, {"error": {"code": "429", "message": "Rate limit"}}, "TransientLLMError"),
    (500, {"error": {"message": "boom"}}, "TransientLLMError"),
    (400, {"error": {"code": "content_filter", "message": "ResponsibleAIPolicyViolation"}}, "ContentFilteredError"),
    (400, {"error": {"code": "context_length_exceeded", "message": "maximum context length"}}, "ContextLengthError"),
    (404, {"error": {"code": "DeploymentNotFound", "message": "no"}}, "DeploymentUnavailableError"),
    (401, {"error": {"message": "bad key"}}, "LLMConfigError"),
])
def test_astra_client_error_mapping(tmp_path, status, body, err):
    import httpx

    from appmod.llm import errors
    c = _astra(tmp_path, lambda req: httpx.Response(status, json=body, headers={"retry-after-ms": "5"}))
    with pytest.raises(getattr(errors, err)):
        c.create("gpt-6-astra", instructions="i", input_items=[])


def test_astra_client_retries_transient_then_succeeds(tmp_path):
    import httpx
    n = []

    def flaky(req):
        n.append(1)
        return httpx.Response(429, json={"error": {"message": "slow down"}},
                              headers={"retry-after-ms": "1"}) if len(n) < 3 else httpx.Response(200, json=RESPONSE)
    c = _astra(tmp_path, flaky)
    c.max_attempts = 4
    assert c.create("gpt-6-astra", instructions="i", input_items=[]).text == "hi" and len(n) == 3


def test_log_filter_keeps_uvicorn_access_args():
    import logging

    from appmod.config import RedactingFilter
    rec = logging.LogRecord("uvicorn.access", logging.INFO, __file__, 1, '%s - "%s %s HTTP/%s" %d',
                            ("127.0.0.1:1", "GET", "/api/health", "1.1", 200), None)
    assert RedactingFilter().filter(rec)
    client_addr, method, path, version, status = rec.args
    assert status == 200 and rec.getMessage() == '127.0.0.1:1 - "GET /api/health HTTP/1.1" 200'
