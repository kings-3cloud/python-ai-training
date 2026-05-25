import urllib.parse
import webbrowser
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# ── Server instance ──────────────────────────────────────────────────────────
mcp = FastMCP(
    name="simple-mcp-server",
    instructions="A demo MCP server with tools, a resource, and a prompt.",
)

# ── Tools ────────────────────────────────────────────────────────────────────

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together and return the result."""
    return a + b


@mcp.tool()
def greet(name: str) -> str:
    """Return a friendly greeting for the given name."""
    return f"Hello, {name}! Welcome to the simple MCP server."


@mcp.tool()
def get_server_time() -> str:
    """Return the current server date and time in ISO 8601 format."""
    return datetime.now().isoformat()

@mcp.tool()
def open_google_search(query: str):
    """Search in google with query"""
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(url)


# ── Resources ────────────────────────────────────────────────────────────────

@mcp.resource("info://server")
def server_info() -> str:
    """Static metadata about this MCP server."""
    return (
        "Name:    simple-mcp-server\n"
        "Version: 0.1.0\n"
        "Tools:   add, greet, get_server_time\n"
        "Built with FastMCP"
    )


# ── Prompts ──────────────────────────────────────────────────────────────────

@mcp.prompt()
def summarise_tools() -> str:
    """A prompt that asks the AI to summarise the available tools."""
    return (
        "You have access to the following tools:\n"
        "  • add(a, b)         — adds two numbers\n"
        "  • greet(name)       — returns a greeting\n"
        "  • get_server_time() — returns the current server time\n\n"
        "Please briefly explain what each tool does and give an example call."
    )


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
