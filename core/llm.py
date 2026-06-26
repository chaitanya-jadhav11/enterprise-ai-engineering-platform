from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from graph.state import QuestionRouterOutput
from tools.common_node_tools import get_tools
jira_tools = get_tools("jira")
git_tools = get_tools("git")

load_dotenv(override=True)

llm = ChatOpenAI(
    model="gpt-5",
    temperature=0
)

router_llm = llm.with_structured_output(
    QuestionRouterOutput
)

jira_llm_with_tools = llm.bind_tools(jira_tools)
github_llm_with_tools  = llm.bind_tools(git_tools)

