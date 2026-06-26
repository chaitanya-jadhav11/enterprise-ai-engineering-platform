from langchain_core.messages import SystemMessage

from core.llm import  github_llm_with_tools
from graph.state import AgentState
from prompts.system_prmpts import GITHUB_AGENT_SYSTEM_PROMPT


def github_agent(state: AgentState):
    print("github_agent node ")

    messages = [
        SystemMessage(content=GITHUB_AGENT_SYSTEM_PROMPT),
        *state["messages"]
    ]

    response = github_llm_with_tools.invoke(messages)

    print("github_agent agent response {}".format(response))

    print("Returning AIMessage:", response)
    print("Tool calls:", response.tool_calls)

    return {
        "messages": [response]
    }