"""MCP client: a real stdio FastMCP server's tools become gateway tools."""

import json
import sys
from pathlib import Path

from appmod.tools import mcp_client
from appmod.tools.builtin import build_gateway
from appmod.tools.gateway import EvidenceLedger, ToolEnv

ECHO = Path(__file__).parent / "fixtures" / "mcp_echo.py"


def test_mcp_tools_register_and_call(tmp_path):
    cfg = tmp_path / "mcp.json"
    cfg.write_text(json.dumps({"servers": {"echo": {"command": sys.executable, "args": [str(ECHO)],
                                                    "allow": ["echo"]}}}))
    gw = build_gateway()
    names = mcp_client.register_mcp_tools(gw, cfg)
    assert names == ["mcp__echo__echo"]
    env = ToolEnv(application_id="t", phase=2, repo_root=None, store=None, published={})
    sess = gw.session("P2.A1", names, env, EvidenceLedger())
    assert "mcp__echo__echo" in {t.name for t in sess.specs()}
    text, eid = sess.call("mcp__echo__echo", {"text": "hi"})
    assert "echo: hi" in text and eid.startswith("ev-")
    assert mcp_client.register_mcp_tools(build_gateway(), tmp_path / "missing.json") == []
