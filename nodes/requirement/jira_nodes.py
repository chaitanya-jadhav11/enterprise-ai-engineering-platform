from langchain_core.messages import SystemMessage, HumanMessage

from core.llm import jira_llm_with_tools
from graph.state import AgentState
from prompts.system_prmpts import JIRA_AGENT_SYSTEM_PROMPT



def jira_agent(state: AgentState):

    print("Jira agent")

    print("=" * 80)
    print("STATE INSIDE JIRA AGENT")
    print(state)
    print("Messages:", state.get("messages"))
    print("=" * 80)

    messages = [
        SystemMessage(content=JIRA_AGENT_SYSTEM_PROMPT),
        *state["messages"]
    ]

    response = jira_llm_with_tools.invoke(messages)

    print("Jira agent response {}".format(response))

    print("Returning AIMessage:", response)
    print("Tool calls:", response.tool_calls)

    return {
        "messages": [response]
    }