"""Preflight: is this machine ready to run the agentic pipeline?

    uv run python scripts/doctor.py          # config + analyzers + tools + MCP
    uv run python scripts/doctor.py --live   # also one tiny call per Astra tier

Never prints secrets.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from appmod.config import get_settings, redact  # noqa: E402
from appmod.tools import analyzers, mcp_client  # noqa: E402
from appmod.tools.builtin import build_gateway  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    args = ap.parse_args()
    s = get_settings()
    ok = True
    print(f"Astra configured : {s.astra_configured}  (llm_mode={s.llm_mode}, cache={s.llm_cache})")
    for t in ("reasoning", "coding", "fast", "fallback", "embedding"):
        print(f"  tier {t:<9}: {s.deployment_for(t)}")
    ok &= s.astra_configured
    print("Analyzers:")
    for name, info in analyzers.doctor()["tools"].items():
        print(f"  {name:<12} {'OK ' if info['available'] else 'MISSING'} {info['version'] or ''}")
    gw = build_gateway()
    print(f"Gateway tools    : {len(gw.tools)} ({', '.join(sorted(gw.tools))})")
    names = mcp_client.register_mcp_tools(gw)
    st = mcp_client.status()
    print(f"MCP servers      : configured={st['configured']} connected={st['connected']} "
          f"tools={names} errors={st['errors']}")
    if args.live and s.astra_configured:
        from appmod.llm.router import ModelRouter
        r = ModelRouter(s)
        for tier in ("reasoning", "coding", "fast", "fallback"):
            try:
                resp = r.complete(tier, instructions="Reply with the single word: ok",
                                  input_items=[{"role": "user", "content": "ping"}], tools=[],
                                  tool_choice=None, reasoning_effort="low", max_output_tokens=64)
                print(f"  live {tier:<9}: OK ({resp.deployment}, {resp.latency_ms} ms)")
            except Exception as exc:
                ok = False
                print(f"  live {tier:<9}: FAIL {type(exc).__name__}: {redact(str(exc))}")
    print("READY" if ok else "NOT READY")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
