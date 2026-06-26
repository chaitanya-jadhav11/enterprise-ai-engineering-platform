from core.llm import router_llm
from graph.state import AgentState
from prompts.system_prmpts import SUPERVISOR_PROMPT


def supervisor_node(state: AgentState):
    print(f"question_router Node.. ")
    question = state["question"]
    messages = state.get("messages", [])

    response = router_llm.invoke(
        [ ( "system", SUPERVISOR_PROMPT),
          *messages,
          ( "human",  question )
        ]
    )
    print(f"question_router Node.. Response: {response} ")
    return {
        "task_type": response.task_type
    }
