import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="cmd",
    args=["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", r"D:\proj\cli_chatbot\scratch"],
)

def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    """Synchronous bridge: opens a session, calls one tool, closes the session.
    Simple but not efficient — a new subprocess per call. Fine for today's checkpoint.
    """
    async def _call():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result.content[0].text
    return asyncio.run(_call())


def mcp_read_file(path: str) -> str:
    """Read a text file's contents via the MCP filesystem server.

    Args:
        path: Path to the file, relative to the server's allowed directory (scratch/).
    """
    return call_mcp_tool("read_text_file", {"path": path})


def mcp_list_directory(path: str = ".") -> str:
    """List files and directories via the MCP filesystem server.

    Args:
        path: Directory path, relative to the server's allowed directory (scratch/).
    """
    return call_mcp_tool("list_directory", {"path": path})