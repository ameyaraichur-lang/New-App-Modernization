"""Live LLM connectivity probe: one round trip per deployment, operator only, no secrets returned."""

import pytest
from fastapi.testclient import TestClient

from appmod.llm.errors import TransientLLMError
from appmod.llm.types import ModelResponse, Usage

TOKENS = "op=olivia:operator;vw=victor:viewer"
H = {"op": {"Authorization": "Bearer op"}, "vw": {"Authorization": "Bearer vw"}}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("APPMOD_RUNS_DIR", str(tmp_path))
    monkeypatch.setenv("APPMOD_API_TOKENS", TOKENS)
    monkeypatch.setenv("APPMOD_AUTH_MODE", "token")
    monkeypatch.setenv("APPMOD_ASTRA_ENDPOINT", "https://astra.example.net/")
    monkeypatch.setenv("APPMOD_ASTRA_API_KEY", "sk-test-not-a-real-key")
    from appmod.config import get_settings
    from appmod.server import api, auth
    get_settings.cache_clear()
    auth.reset()
    api._db = None
    api._jobs.clear()
    with TestClient(api.app) as c:
        yield c
    api._jobs.clear()
    api._db = None
    get_settings.cache_clear()
    auth.reset()


class FakeClient:
    calls: list[str] = []

    def __init__(self, settings, max_attempts=4):
        assert max_attempts == 1

    def create(self, deployment, **kw):
        FakeClient.calls.append(deployment)
        if deployment == FakeClient.down:
            raise TransientLLMError(f"{deployment}: rate limited")
        return ModelResponse(response_id="r", deployment=deployment, model=f"{deployment}-2026",
                             output_items=[], text="OK", usage=Usage(input_tokens=12, output_tokens=3),
                             status="completed", latency_ms=5)

    def embed(self, texts, deployment=None):
        return [[0.0] * 8]


def test_probe_reports_each_deployment_once(client, monkeypatch):
    from appmod.config import get_settings
    from appmod.llm import astra
    monkeypatch.setattr(astra, "AstraClient", FakeClient)
    s = get_settings()
    FakeClient.calls, FakeClient.down = [], s.deployment_for("fast")
    r = client.post("/api/health/llm/probe", headers=H["op"])
    assert r.status_code == 200
    body = r.json()
    assert body["configured"] and body["endpoint_host"] == "astra.example.net"
    assert "sk-test" not in r.text
    chats = [x for x in body["results"] if x["kind"] == "responses"]
    assert sorted(FakeClient.calls) == sorted({s.deployment_for(t) for t in ("reasoning", "coding", "fast", "fallback")})
    assert sorted(t for x in chats for t in x["tiers"]) == ["coding", "fallback", "fast", "reasoning"]
    down = next(x for x in chats if x["deployment"] == FakeClient.down)
    assert down["ok"] is False and "rate limited" in down["error"]
    up = [x for x in chats if x["deployment"] != FakeClient.down]
    assert all(x["ok"] and x["reply"] == "OK" and x["input_tokens"] == 12 for x in up)
    emb = next(x for x in body["results"] if x["kind"] == "embeddings")
    assert emb["ok"] and emb["dimensions"] == 8


def test_probe_needs_operator_and_handles_missing_config(client, monkeypatch):
    assert client.post("/api/health/llm/probe", headers=H["vw"]).status_code == 403
    monkeypatch.setenv("APPMOD_ASTRA_ENDPOINT", "")
    from appmod.config import get_settings
    get_settings.cache_clear()
    body = client.post("/api/health/llm/probe", headers=H["op"]).json()
    assert body["configured"] is False and body["results"] == []
