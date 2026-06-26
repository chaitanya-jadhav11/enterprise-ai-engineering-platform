from typing import Literal

from langchain_core.messages import AIMessage

from graph.state import AgentState


def route_task(state: AgentState) -> Literal["jira_agent","github_agent"]:
    task_type = state.get("task_type", [])
    print(f"route_task task_type = {task_type}")
    if task_type == "REQUIREMENT_ANALYSIS":
        return "jira_agent"
    elif task_type == "REPOSITORY_ANALYSIS":
        return "github_agent"


def route_jira(state: AgentState):
    """Determines whether to execute a Jira tool or proceed to response."""
    # 1. Extract messages from the state
    print("route_jira conditional_edges")
    messages = state.get("messages", [])

    print(f" route_jira - messages {messages}")

    # 2. Fallback if the message list is empty
    if not messages:
        return "response_node"

    last = messages[-1]

    if isinstance(last, AIMessage)  and last.tool_calls:
        return "jira_tools"

    # 4. No tools requested, proceed forward
    return "response_node"

def route_git(state: AgentState):
    """Determines whether to execute a git tool or proceed to response."""
    # 1. Extract messages from the state
    print("route_git conditional_edges")
    messages = state.get("messages", [])

    print(f" route_git - messages {messages}")

    # 2. Fallback if the message list is empty
    if not messages:
        return "response_node"

    last = messages[-1]

    if isinstance(last, AIMessage)  and last.tool_calls:
        return "github_tools"

    # 4. No tools requested, proceed forward
    return "response_node"
