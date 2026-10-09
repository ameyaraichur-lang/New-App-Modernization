"""Minimal stdio MCP server used by tests/test_mcp.py."""

try:
    from mcp.server.mcpserver import MCPServer as Server
except ImportError:
    from mcp.server.fastmcp import FastMCP as Server

mcp = Server("echo")


@mcp.tool()
def echo(text: str) -> str:
    """Echo the given text back."""
    return f"echo: {text}"


@mcp.tool()
def secret_tool() -> str:
    """A tool the allow-list excludes."""
    return "should not be reachable"


if __name__ == "__main__":
    mcp.run()
