"""MCP client: expose external MCP servers' tools through the ToolGateway.

Config (``APPMOD_MCP_CONFIG``, default ``config/mcp_servers.json``)::

    {"servers": {"docs": {"command": "uvx", "args": ["some-mcp-server"],
                          "env": {}, "allow": ["search"]}}}

Each server is started once per process (stdio transport) on a private
asyncio loop thread. Tools register as ``mcp__<server>__<tool>`` with their
own JSON schema (non-strict). Like every gateway tool, results are redacted,
truncated, wrapped as untrusted evidence and only reachable by agents whose
allow-list includes them (jobs pass the MCP names via ``extra_tools``).
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import threading
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any

from appmod.config import get_settings
from appmod.tools.gateway import ToolDef, ToolEnv, ToolGateway


def tool_name(server: str, tool: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "_", f"mcp__{server}__{tool}")[:64]


class MCPHub:
    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True, name="mcp-hub")
        self._thread.start()
        self._stack: AsyncExitStack | None = None
        self.sessions: dict[str, Any] = {}
        self.tools: dict[str, tuple[str, Any]] = {}     # gateway name -> (server, mcp Tool)
        self.errors: dict[str, str] = {}

    def _run(self, coro, timeout: float):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout)

    async def _connect(self, name: str, cfg: dict[str, Any]) -> None:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        if self._stack is None:
            self._stack = AsyncExitStack()
        params = StdioServerParameters(command=cfg["command"], args=list(cfg.get("args", [])),
                                       env={**os.environ, **cfg.get("env", {})})
        read, write = await self._stack.enter_async_context(stdio_client(params))
        session = await self._stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        listed = await session.list_tools()
        allow = cfg.get("allow")
        self.sessions[name] = session
        for t in listed.tools:
            if allow is None or t.name in allow:
                self.tools[tool_name(name, t.name)] = (name, t)

    def connect(self, servers: dict[str, dict[str, Any]], timeout: float = 60) -> None:
        for name, cfg in servers.items():
            if name in self.sessions:
                continue
            try:
                self._run(self._connect(name, cfg), timeout)
            except Exception as exc:
                self.errors[name] = f"{type(exc).__name__}: {exc}"

    def call(self, gname: str, args: dict[str, Any], timeout: float = 120) -> str:
        server, tool = self.tools[gname]
        res = self._run(self.sessions[server].call_tool(tool.name, args), timeout)
        parts = []
        for c in res.content:
            parts.append(getattr(c, "text", None) or json.dumps(c.model_dump(), default=str)[:4000])
        text = "\n".join(parts)
        err = getattr(res, "is_error", None)
        if err is None:
            err = getattr(res, "isError", False)
        return f"ERROR: {text}" if err else text

    def close(self) -> None:
        if self._stack is not None:
            try:
                self._run(self._stack.aclose(), 10)
            except Exception:
                pass
        self._loop.call_soon_threadsafe(self._loop.stop)


_HUB: MCPHub | None = None
_HUB_LOCK = threading.Lock()


def load_config(path: str | Path | None = None) -> dict[str, dict[str, Any]]:
    p = Path(path or get_settings().mcp_config)
    if not p.is_file():
        return {}
    return json.loads(p.read_text()).get("servers", {})


def hub(path: str | Path | None = None) -> MCPHub | None:
    global _HUB
    servers = load_config(path)
    if not servers:
        return None
    with _HUB_LOCK:
        if _HUB is None:
            _HUB = MCPHub()
        _HUB.connect(servers)
        return _HUB


def register_mcp_tools(gateway: ToolGateway, path: str | Path | None = None) -> list[str]:
    h = hub(path)
    if h is None:
        return []
    names = []
    for gname, (server, tool) in h.tools.items():
        schema = (getattr(tool, "input_schema", None) or getattr(tool, "inputSchema", None)
                  or {"type": "object", "properties": {}})

        def fn(env: ToolEnv, args: dict[str, Any], _g=gname) -> str:
            return h.call(_g, {k: v for k, v in args.items() if v is not None})

        gateway.register(ToolDef(gname, (tool.description or f"{server} MCP tool {tool.name}")[:1000],
                                 schema, fn, strict=False))
        names.append(gname)
    return names


def status() -> dict[str, Any]:
    servers = load_config()
    h = _HUB
    return {"configured": sorted(servers),
            "connected": sorted(h.sessions) if h else [],
            "tools": sorted(h.tools) if h else [],
            "errors": dict(h.errors) if h else {}}
