import asyncio

from mcp.client.streamable_http import streamablehttp_client, streamable_http_client
from mcp import ClientSession


async def main():
    async with streamable_http_client(
        "http://localhost:9000/mcp"
    ) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            print("\n📋 Discovering available Jira tools:")
            tools_response = await session.list_tools()
            for tool in tools_response.tools:
                # print(f" - {tool.name}:  desc = {tool.description}")
                if tool.name == "jira_search":
                    print(tool.inputSchema)


            result = await session.call_tool(
                "jira_search",
                {"jql": "project = my-softwaret-team ORDER BY created DESC"}
            )
            print(result.content[0].text)

asyncio.run(main())

