"""Live Astra checks — run with APPMOD_LIVE=1 (needs .env credentials)."""

import os
import sys
from pathlib import Path

import pytest

pytestmark = [pytest.mark.live,
              pytest.mark.skipif(os.environ.get("APPMOD_LIVE") != "1", reason="APPMOD_LIVE!=1")]

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))


def test_all_tiers_tool_loop():
    from astra_smoke import tool_loop
    from appmod.config import get_settings
    from appmod.llm.astra import AstraClient
    s = get_settings()
    client = AstraClient(s)
    for tier in ("reasoning", "coding", "fast", "fallback"):
        assert tool_loop(client, s.deployment_for(tier))["ok"]


def test_embeddings_dims():
    from appmod.llm.astra import AstraClient
    assert len(AstraClient().embed(["hello"])[0]) == 1536
