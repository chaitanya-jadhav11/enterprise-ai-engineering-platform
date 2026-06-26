from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    question: str
    task_type: str

    jira_data: dict
    github_data: dict
    final_answer : str

class QuestionRouterOutput(BaseModel):

    task_type: str = Field(
        description="Valid task_type values."
    )
