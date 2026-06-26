from fastapi import APIRouter
from langchain_core.messages import HumanMessage

from api.chat_models import ChatResponse, ChatRequest


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    config = {
        "configurable": {
            "thread_id": request.user_id + "-" + request.conversation_id
        }
    }
    from graph.graph_builder import get_main_graph
    main_graph = get_main_graph()

    # Debug: list available invoke methods to confirm name
    print("Main graph methods:", [m for m in dir(main_graph) if "invoke" in m.lower()])

    # Use the async graph invocation. Common names: 'ainvoke', 'invoke_async', or 'invoke' may itself be coroutine.
    if hasattr(main_graph, "ainvoke"):
        result = await main_graph.ainvoke(
            {"question": request.question,
             "retry_count": 0,
             "messages": [
                 HumanMessage(content=request.question)
             ]
             },
            config=config
        )
    elif hasattr(main_graph, "invoke_async"):
        result = await main_graph.invoke_async(
            {
            "question": request.question,
             "retry_count": 0,
             "messages": [
                     HumanMessage(content=request.question)
                 ]
             },
            config=config
        )
    else:
        # Fall back to checking if invoke is a coroutine function
        invoke = main_graph.invoke
        if callable(invoke) and hasattr(invoke, "__call__") and hasattr(invoke, "__await__"):
            result = await invoke(
                {"question": request.question,
                 "retry_count": 0,
                 "messages": [
                     HumanMessage(content=request.question)
                 ]
                 },
                config=config
            )
        else:
            # Last resort (not recommended): call sync invoke (will likely trigger StructuredTool error)
            result = main_graph.invoke(
                {"question": request.question,
                 "retry_count": 0,
                 "messages": [
                     HumanMessage(content=request.question)
                 ]
                 },
                config=config
            )

    return ChatResponse(answer=result["final_answer"])


@router.post("/chat1", response_model=ChatResponse)
def chat1(request: ChatRequest):

    config = {
        "configurable": {
            "thread_id": request.user_id +"-" + request.conversation_id
        }
    }
    from graph.graph_builder import get_main_graph
    result = get_main_graph().invoke(
        {
            "question": request.question,
            "retry_count": 0,
            "messages": [
                HumanMessage(content=request.question)
            ]
        },
        config=config
    )

    return ChatResponse(
        answer=result["final_answer"]
    )