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


def test_log_filter_keeps_uvicorn_access_args():
    import logging

    from appmod.config import RedactingFilter
    rec = logging.LogRecord("uvicorn.access", logging.INFO, __file__, 1, '%s - "%s %s HTTP/%s" %d',
                            ("127.0.0.1:1", "GET", "/api/health", "1.1", 200), None)
    assert RedactingFilter().filter(rec)
    client_addr, method, path, version, status = rec.args
    assert status == 200 and rec.getMessage() == '127.0.0.1:1 - "GET /api/health HTTP/1.1" 200'
