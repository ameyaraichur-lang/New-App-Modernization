"""Live Astra smoke test: every tier runs a strict two-turn tool loop.

    python scripts/astra_smoke.py            # exits non-zero if any tier fails

Turn 1 must call ``lookup`` (tool_choice=required); turn 2 replays the
function_call/reasoning items plus a function_call_output and must call the
strict ``submit`` tool with the looked-up value. Also checks embeddings.
Never prints secrets.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from appmod.config import get_settings  # noqa: E402
from appmod.llm.astra import AstraClient  # noqa: E402
from appmod.llm.types import ToolSpec  # noqa: E402

LOOKUP = ToolSpec("lookup", "Look up the code name of a project by id.", {
    "type": "object", "additionalProperties": False, "required": ["project_id"],
    "properties": {"project_id": {"type": "string"}},
})
SUBMIT = ToolSpec("submit", "Submit the final answer.", {
    "type": "object", "additionalProperties": False, "required": ["code_name", "confidence"],
    "properties": {"code_name": {"type": "string"},
                   "confidence": {"type": "string", "enum": ["low", "medium", "high"]}},
})


def tool_loop(client: AstraClient, deployment: str) -> dict:
    t0 = time.time()
    items = [{"role": "user", "content": "What is the code name of project P-42? "
              "Use lookup, then submit the answer."}]
    r1 = client.create(deployment, instructions="You are a precise assistant. Always use tools.",
                       input_items=items, tools=[LOOKUP, SUBMIT], tool_choice="required",
                       reasoning_effort="low", max_output_tokens=2000)
    calls = r1.function_calls
    assert calls and calls[0].name == "lookup", f"turn1 expected lookup, got {[c.name for c in calls]}"
    items += r1.output_items
    for c in calls:
        items.append({"type": "function_call_output", "call_id": c.call_id,
                      "output": json.dumps({"code_name": "BLUE-HERON"} if c.name == "lookup" else {})})
    r2 = client.create(deployment, instructions="You are a precise assistant. Always use tools.",
                       input_items=items, tools=[LOOKUP, SUBMIT],
                       tool_choice={"type": "function", "name": "submit"},
                       reasoning_effort="low", max_output_tokens=2000)
    sub = [c for c in r2.function_calls if c.name == "submit"]
    assert sub, "turn2 expected submit"
    args = sub[0].parsed()
    assert args["code_name"] == "BLUE-HERON", args
    return {"ok": True, "model": r2.model, "secs": round(time.time() - t0, 1),
            "tokens": r1.usage.total + r2.usage.total}


FACT_SCHEMA = {
    "type": "json_schema", "name": "fact", "strict": True,
    "schema": {"type": "object", "additionalProperties": False, "required": ["language", "year"],
               "properties": {"language": {"type": "string"}, "year": {"type": "integer"}}},
}


def json_schema_output(client: AstraClient, deployment: str) -> dict:
    r = client.create(deployment, instructions="Answer with the requested JSON only.",
                      input_items=[{"role": "user", "content": "Which language did Guido van Rossum "
                                    "create, and in which year was it first released?"}],
                      text_format=FACT_SCHEMA, reasoning_effort="low", max_output_tokens=2000)
    out = json.loads(r.text)
    assert out["language"].lower() == "python" and isinstance(out["year"], int), out
    return out


def list_deployments(settings) -> list[str]:
    """Deployment ids on the resource (data-plane listing is only served on 2022-12-01)."""
    import httpx
    r = httpx.get(f"{settings.astra_endpoint.rstrip('/')}/openai/deployments",
                  params={"api-version": "2022-12-01"},
                  headers={"api-key": settings.astra_api_key.get_secret_value()}, timeout=30)
    r.raise_for_status()
    return [d["id"] for d in r.json().get("data", [])]


def main() -> int:
    s = get_settings()
    if not s.astra_configured:
        print("Astra not configured (.env APPMOD_ASTRA_*)")
        return 2
    client = AstraClient(s)
    failures = 0
    try:
        deps = list_deployments(s)
        tiers = {t: s.deployment_for(t) for t in ("reasoning", "coding", "fast", "fallback")}
        missing = [d for d in [*tiers.values(), s.tier_embedding] if d not in deps]
        failures += bool(missing)
        print(f"{'deploys':<10} {len(deps)} listed; missing tiers: {missing or 'none'}")
        print(f"{'json':<10} {s.deployment_for('reasoning'):<28} "
              f"{json_schema_output(client, s.deployment_for('reasoning'))}")
    except Exception as exc:
        failures += 1
        print(f"probe FAIL {type(exc).__name__}: {str(exc)[:300]}")
    for tier in ("reasoning", "coding", "fast", "fallback"):
        dep = s.deployment_for(tier)
        try:
            print(f"{tier:<10} {dep:<28} {tool_loop(client, dep)}", flush=True)
        except Exception as exc:
            failures += 1
            print(f"{tier:<10} {dep:<28} FAIL {type(exc).__name__}: {str(exc)[:300]}", flush=True)
    try:
        vecs = client.embed(["def main(): pass", "SELECT * FROM owners"])
        print(f"{'embedding':<10} {s.tier_embedding:<28} ok dims={len(vecs[0])} n={len(vecs)}")
    except Exception as exc:
        failures += 1
        print(f"embedding FAIL {type(exc).__name__}: {str(exc)[:300]}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
