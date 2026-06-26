import asyncio
import os
import sys

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv(override=True)


async def run_jira_client():
    # 2. Configure the subprocess execution details for the MCP server
    # We use 'uvx' (or 'npx' / 'python') to run the community server package.
    server_params = StdioServerParameters(
        command="uvx",
        args=["mcp-atlassian", "-v"],
        env={
            **os.environ,
            "JIRA_URL": "https://<user-name>.atlassian.net",
            "JIRA_USERNAME": "<mail-id>@gmail.com",
            "JIRA_API_TOKEN": "<tokenid>",
        }
    )

    print("🔄 Connecting to Jira MCP Server...")

    # 3. Establish the stdio transport connection session
    async with stdio_client(server_params, errlog=sys.stderr) as (read_stream, write_stream):
    #async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:


            # Initialize the protocol handshake
            await session.initialize()
            print("✅ Connected successfully!")

            # 4. List all available tools exposed by the Jira server
            print("\n📋 Discovering available Jira tools:")
            tools_response = await session.list_tools()
            for tool in tools_response.tools:
                #print(f" - {tool.name}:  desc = {tool.description}")
                if tool.name == "jira_search":
                    print(tool.inputSchema)

            # 5. Call a specific Jira tool (e.g., search issues using JQL)
            # Adjust the tool name based on the output of your list_tools execution
            tool_name = "jira_get_all_projects"
            arguments = {
                #"jql": "assignee = currentUser() AND status = 'In Progress'"
               # "user_identifier": "chaitanya-jadhav.atlassian.net"
                #'user_identifier:' + JIRA_USER,
               # "project_key": "SCRUM",
               # "limit" :10,
               # "start_at" :1

            }

            print(f"\n🚀 Invoking tool '{tool_name}' with args: {arguments}...")
            try:
                result = await session.call_tool(name=tool_name, arguments=arguments)
                print("\n📥 Response from Jira MCP Server:")
                print(result.content[0].text)
                print(result)
            except Exception as e:
                print(f"❌ Error executing tool: {e}")


if __name__ == "__main__":
    # MCP Python SDK operations are strictly asynchronous
    asyncio.run(run_jira_client())

# #
# 📋 Discovering available Jira tools:
#  - jira_get_user_profile:
#  - jira_get_issue_watchers:
#  - jira_add_watcher:
#  - jira_remove_watcher:
#  - jira_get_issue:
#  - jira_search:
#  - jira_search_fields:
#  - jira_get_field_options:
#  - jira_get_project_issues:
#  - jira_get_transitions:
#  - jira_get_worklog:
#  - jira_download_attachments:
#  - jira_get_issue_images:
#  - jira_get_agile_boards:
#  - jira_get_board_issues:
#  - jira_get_sprints_from_board:
#  - jira_get_sprint_issues:
#  - jira_get_link_types:
#  - jira_create_issue:
#  - jira_batch_create_issues:
#  - jira_batch_get_changelogs:
#  - jira_update_issue:
#  - jira_delete_issue:
#  - jira_add_comment:
#  - jira_edit_comment:
#  - jira_add_worklog:
#  - jira_link_to_epic:
#  - jira_create_issue_link:
#  - jira_create_remote_issue_link:
#  - jira_remove_issue_link:
#  - jira_transition_issue:
#  - jira_create_sprint:
#  - jira_update_sprint:
#  - jira_add_issues_to_sprint:
#  - jira_get_project_versions:
#  - jira_get_project_components:
#  - jira_get_all_projects:
#  - jira_get_service_desk_for_project:
#  - jira_get_service_desk_queues:
#  - jira_get_queue_issues:
#  - jira_create_version:
#  - jira_batch_create_versions:
#  - jira_get_issue_proforma_forms:
#  - jira_get_proforma_form_details:
#  - jira_update_proforma_form_answers:
#  - jira_get_issue_dates:
#  - jira_get_issue_sla:
#  - jira_get_issue_development_info:
#  - jira_get_issues_development_info: