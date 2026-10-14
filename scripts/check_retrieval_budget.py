"""Fail when any agent in an e2e report exceeds the large-repo input budget.

The budget is twice the run-4 median agent input (49,656 tokens).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from appmod.retrieval.memory import AGENT_INPUT_TOKEN_CAP  # noqa: E402


def over_budget(report: dict, cap: int = AGENT_INPUT_TOKEN_CAP) -> list[str]:
    problems = []
    for agent in report.get("agents") or []:
        tokens = (agent.get("tokens") or {}).get("input") or 0
        if tokens > cap:
            problems.append(f"{agent.get('phase')}.{agent.get('agent')} {agent.get('app')} "
                            f"{tokens} > {cap}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", type=Path, required=True)
    args = ap.parse_args()
    problems = over_budget(json.loads(args.report.read_text()))
    if problems:
        print("retrieval budget exceeded:")
        print("\n".join(f"- {p}" for p in problems))
        return 1
    print(f"every agent input is within {AGENT_INPUT_TOKEN_CAP} tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
