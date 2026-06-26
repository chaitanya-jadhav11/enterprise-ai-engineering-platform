from langchain_mcp_adapters.client import MultiServerMCPClient


class JiraMCPManager:
    _client = None
    _tools = None

    @classmethod
    async def initialize(cls):
        if cls._client is not None:
            return

        cls._client = MultiServerMCPClient(
            {
                "jira": {
                    "transport": "streamable_http",
                    "url": "http://localhost:9000/mcp",
                },
                "github": {
                    "transport": "streamable_http",
                    "url": "https://api.githubcopilot.com/mcp/",
                    "headers": {
                        "Authorization": f"Bearer <xyz>>"
                    },
                },
            }
        )

        cls._tools = await cls._client.get_tools()

        print(f"\nLoaded {len(cls._tools)} MCP tools")

        for tool in cls._tools:
            print(f"- {tool.name}")

    @classmethod
    def get_tools(cls):
        if cls._tools is None:
            raise RuntimeError(
                "JiraMCPManager.initialize() must be called first."
            )
        return cls._tools