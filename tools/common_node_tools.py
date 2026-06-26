from app_mcp.clients.mcp_manager import MCPManager
from tools.githubs import get_github_tools
from tools.jira_tools import get_jira_tools


def get_tools(tool_type: str):
    all_tools = MCPManager.get_tools()

    if tool_type == "jira":
        return get_jira_tools(all_tools)
    elif tool_type == "github":
        return get_github_tools(all_tools)

    # Default fallback
    return all_tools

