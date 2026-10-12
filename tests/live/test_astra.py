"""Live Astra checks — run with APPMOD_LIVE=1 (needs .env credentials)."""

import inspect
import os
import sys
from pathlib import Path

import jsonschema
import openai
import pytest

pytestmark = [pytest.mark.live,
              pytest.mark.skipif(os.environ.get("APPMOD_LIVE") != "1", reason="APPMOD_LIVE!=1")]

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

TIERS = ("reasoning", "coding", "fast", "fallback")


@pytest.fixture(scope="module")
def astra():
    from appmod.config import get_settings
    from appmod.llm.astra import AstraClient
    s = get_settings()
    return s, AstraClient(s)


def test_all_tiers_tool_loop(astra):
    from astra_smoke import tool_loop
    s, client = astra
    for tier in TIERS:
        assert tool_loop(client, s.deployment_for(tier))["ok"]


def test_embeddings_dims(astra):
    _, client = astra
    assert len(client.embed(["hello"])[0]) == 1536


def test_every_tier_is_deployed(astra):
    from astra_smoke import list_deployments
    s, _ = astra
    deps = list_deployments(s)
    assert {s.deployment_for(t) for t in TIERS} | {s.tier_embedding} <= set(deps), deps


def test_json_schema_structured_output(astra):
    from astra_smoke import json_schema_output
    s, client = astra
    assert json_schema_output(client, s.deployment_for("reasoning"))["language"].lower() == "python"


def test_unsupported_sampling_params_are_guarded(astra):
    s, client = astra
    params = inspect.signature(client.create).parameters
    assert "temperature" not in params and "top_p" not in params
    with pytest.raises(openai.BadRequestError):
        client._client.responses.create(model=s.deployment_for("reasoning"), input="hi",
                                        temperature=0, max_output_tokens=16)


def _overlays():
    from appmod.agents.overlays import OVERLAYS
    return [(p, a) for p in sorted(OVERLAYS) for a in sorted(OVERLAYS[p], key=lambda x: int(x[1:]))]


@pytest.mark.parametrize("phase,agent", _overlays())
def test_submit_outcome_schema_accepted_strict(astra, phase, agent):
    from appmod.agents.llm_runner import submit_tool
    from appmod.agents.overlays import overlay_for
    s, client = astra
    ov = overlay_for(phase, agent)
    assert ov is not None
    tool = submit_tool(ov, review_only=False)
    assert tool.to_responses_tool()["strict"] is True
    r = client.create(s.deployment_for(ov.tier),
                      instructions="Schema conformance probe. Submit a minimal NOT_ASSESSED outcome "
                                   "with empty lists and short strings; cite nothing.",
                      input_items=[{"role": "user", "content": f"Submit the outcome for P{phase} {agent}."}],
                      tools=[tool], tool_choice={"type": "function", "name": "submit_outcome"},
                      reasoning_effort="low", max_output_tokens=6000)
    calls = [c for c in r.function_calls if c.name == "submit_outcome"]
    assert calls, r.status
    jsonschema.validate(calls[0].parsed(), tool.parameters)
