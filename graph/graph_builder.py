from pathlib import Path

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from graph.conditional_edges import route_task, route_jira, route_git
from graph.state import AgentState
from nodes.common import response_node
from nodes.repository.git_nodes import github_agent
from nodes.requirement.jira_nodes import jira_agent

from nodes.supervisor.router_node import  supervisor_node


def get_jira_node():
    from tools.common_node_tools import get_tools
    jira_tools = get_tools("jira")
    jira_tool_node = ToolNode(jira_tools)

    return jira_tool_node

def get_github_node():
    from tools.common_node_tools import get_tools
    github_tools = get_tools("github")
    github_tool_node = ToolNode(github_tools)

    return github_tool_node


# ==========================================================
# Build Graph
# ==========================================================

builder = StateGraph(AgentState)
# ==========================================================
# Add Nodes
# ==========================================================

builder.add_node("supervisor_node",supervisor_node)
builder.add_node("jira_agent", jira_agent)
builder.add_node("github_agent", github_agent)
builder.add_node("response_node", response_node)
builder.add_node("jira_tools", get_jira_node())
builder.add_node("github_tools", get_github_node())

# ==========================================================
# Edges
# ==========================================================

builder.add_edge( START, "supervisor_node")

builder.add_conditional_edges(
    "supervisor_node",
    route_task,
    {
        "jira_agent": "jira_agent",
        "github_agent": "github_agent"
    }
)
# --- MODIFIED: Route jira_agent conditionally instead of a direct edge ---
builder.add_conditional_edges(
    "jira_agent",
    route_jira,
    {
        "jira_tools": "jira_tools",
        "response_node": "response_node"
    }
)

# --- MODIFIED: Route jira_agent conditionally instead of a direct edge ---
builder.add_conditional_edges(
    "github_agent",
    route_git,
    {
        "github_tools": "github_tools",
        "response_node": "response_node"
    }
)

# --- ADDED: Edge to loop back from tools to agent ---
builder.add_edge("jira_tools", "jira_agent")
# --- ADDED: Edge to loop back from tools to agent ---
builder.add_edge("github_tools", "github_agent")

#builder.add_edge("jira_agent","response_node")
#builder.add_edge("github_agent","response_node")
builder.add_edge("response_node", END)

#main_graph = builder.compile()

main_graph = None

def build_graph():
    # ==========================================================
    # Compile
    # ==========================================================
    global main_graph
    main_graph = builder.compile()
    # main_graph.get_graph().print_ascii()  # Good for checking logic in console
    main_graph.get_graph().draw_mermaid_png(
        output_file_path="workflow_image/" + Path(__file__).stem + ".png")


def get_main_graph():
    return main_graph

#if __name__ == "__main__":
    #build_graph()
