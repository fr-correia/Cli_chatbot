import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="cmd",
    args=["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", r"D:\proj\cli_chatbot\scratch"],
)

async def main():
    async with stdio_client(server_params, errlog=sys.stderr) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            for tool in tools.tools:
                print(tool.name, "-", tool.description)
            result = await session.call_tool("list_allowed_directories", {})
            print(result.content[0].text)

asyncio.run(main())