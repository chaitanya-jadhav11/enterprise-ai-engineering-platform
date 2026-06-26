import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv(override=True)

github_token = os.environ["GITHUB_TOKEN"]


class MCPManager:
    _client = None
    _tools = None

    @classmethod
    async def initialize(cls):

        if cls._client is None:

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
                            "Authorization": f"Bearer {github_token}"
                        },
                    },
                }
            )

            cls._tools = await cls._client.get_tools()

    @classmethod
    def get_tools(cls):
        #print("Getting tools {}".format(cls._tools))
        return cls._tools