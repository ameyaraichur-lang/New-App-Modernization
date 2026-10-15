"""Outage pause: an unreachable endpoint pauses model work instead of spending agent retries."""

import threading

import httpx
import openai
import pytest

from appmod.config import Settings
from appmod.llm.astra import AstraClient
from appmod.llm.cache import ResponseCache
from appmod.llm.errors import ConnectivityError, TransientLLMError
from appmod.llm.outage import OutageGate
from appmod.llm.router import ModelRouter
from appmod.llm.types import ModelResponse, Usage


def _settings(tmp_path, **kw):
    return Settings(_env_file=None, astra_endpoint="https://x", astra_api_key="k" * 20,
                    runs_dir=tmp_path, **kw)


class Probe:
    def __init__(self, down_for: int):
        self.down_for = down_for
        self.calls = 0

    def __call__(self) -> bool:
        self.calls += 1
        return self.calls > self.down_for


class OutageClient:
    """Every deployment fails to connect until ``probe`` reports the endpoint back."""

    def __init__(self, probe: Probe, error: type[TransientLLMError] = ConnectivityError):
        self.probe = probe
        self.error = error
        self.calls: list[str] = []

    def reachable(self) -> bool:
        return self.probe()

    def create(self, deployment, **kw):
        self.calls.append(deployment)
        if self.probe.calls <= self.probe.down_for:
            raise self.error(f"{deployment}: APIConnectionError")
        return ModelResponse(response_id="r", deployment=deployment, model=deployment, output_items=[],
                             text="ok", usage=Usage(input_tokens=10, output_tokens=5))


def _gate(probe, **kw):
    seen: list[tuple[str, dict]] = []
    gate = OutageGate(probe, first_delay_s=0.01, max_delay_s=0.02,
                      on_change=lambda s, i: seen.append((s, i)), **kw)
    return gate, seen


def test_gate_waits_until_endpoint_answers():
    gate, seen = _gate(Probe(down_for=2))
    assert gate.wait() is True
    assert [s for s, _ in seen] == ["LOST", "RESTORED"]
    assert seen[1][1]["probes"] == 3


def test_concurrent_callers_share_one_outage():
    probe = Probe(down_for=3)
    gate, seen = _gate(probe)
    results: list[bool] = []
    threads = [threading.Thread(target=lambda: results.append(gate.wait())) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(5)
    assert results == [True] * 5
    assert [s for s, _ in seen].count("LOST") <= 2 and seen[-1][0] == "RESTORED"


def test_gate_gives_up_on_cancel_and_after_max_wait():
    stop = threading.Event()
    stop.set()
    gate, seen = _gate(Probe(down_for=10**6), stop=stop)
    assert gate.wait() is False and seen[-1] == ("GAVE_UP", seen[-1][1])
    assert seen[-1][1]["reason"] == "cancelled"
    gate, seen = _gate(Probe(down_for=10**6), max_wait_s=0.05)
    assert gate.wait() is False and seen[-1][1]["reason"] == "max wait exceeded"


def test_router_pauses_through_outage_without_raising(tmp_path):
    probe = Probe(down_for=2)
    client = OutageClient(probe)
    r = ModelRouter(_settings(tmp_path), client, ResponseCache(tmp_path / "c", "off"))
    r.outage.first_delay_s = r.outage.max_delay_s = 0.01
    seen: list[str] = []
    r.outage.on_change = lambda s, i: seen.append(s)
    resp = r.complete("reasoning", instructions="i", input_items=[])
    assert resp.text == "ok" and seen == ["LOST", "RESTORED"]
    assert len(client.calls) == 3   # primary + fallback during the outage, then the resumed call


def test_router_does_not_wait_when_endpoint_is_up(tmp_path):
    client = OutageClient(Probe(down_for=0), error=TransientLLMError)
    s = _settings(tmp_path)

    def always_429(deployment, **kw):
        raise TransientLLMError(f"{deployment}: rate limited")

    client.create = always_429
    r = ModelRouter(s, client, ResponseCache(tmp_path / "c", "off"))
    r.outage.first_delay_s = 10.0
    with pytest.raises(TransientLLMError):
        r.complete("reasoning", instructions="i", input_items=[])
    assert r.outage.outages == 0


def test_router_gives_up_after_max_wait(tmp_path):
    client = OutageClient(Probe(down_for=10**6))
    r = ModelRouter(_settings(tmp_path, llm_outage_max_wait_s=0.05), client,
                    ResponseCache(tmp_path / "c", "off"))
    r.outage.first_delay_s = r.outage.max_delay_s = 0.01
    with pytest.raises(ConnectivityError):
        r.complete("reasoning", instructions="i", input_items=[])


def test_job_journals_pause_and_restores_stage_detail(tmp_path):
    from appmod.server.rundb import RunDB
    from appmod.server.jobs import PipelineJob
    db = RunDB(tmp_path / "x.db")
    job = PipelineJob(repos=[str(tmp_path)], runs_root=tmp_path, llm=False, db=db)
    job._update(stage_detail="Phase 1 — Discovery (demo)")
    job._on_outage("LOST", {})
    assert "paused" in job.snapshot()["stage_detail"]
    job._on_outage("RESTORED", {"probes": 4, "waited_s": 95})
    assert job.snapshot()["stage_detail"] == "Phase 1 — Discovery (demo)"
    conn = db.events_since(job.job_id, 0, 100, ["CONNECTIVITY"])
    assert [e["status"] for e in conn] == ["LOST", "RESTORED"] and conn[1]["waited_s"] == 95


def test_astra_maps_connection_failures_but_not_timeouts(tmp_path):
    c = AstraClient.__new__(AstraClient)
    req = httpx.Request("POST", "https://x/openai/responses")

    def boom(exc):
        def f():
            raise exc
        return f

    with pytest.raises(ConnectivityError):
        c._call(boom(openai.APIConnectionError(request=req)), "d")
    with pytest.raises(TransientLLMError) as info:
        c._call(boom(openai.APITimeoutError(request=req)), "d")
    assert not isinstance(info.value, ConnectivityError)
