from langchain_core.messages import AIMessage

from graph.state import AgentState


def response_node(state: AgentState):
    """
    Format final response
    """
    print("In response_node")
    messages = state["messages"]

    last_ai = next(
        (m for m in reversed(messages)
         if isinstance(m, AIMessage)),
        None
    )

    return {
        "final_answer": last_ai.content if last_ai else ""
    }