import asyncio
from pathlib import Path

from dotenv import load_dotenv

from app_mcp.clients.mcp_manager import MCPManager
from fastapi import FastAPI
from api.chat_api import router

load_dotenv(override=True)

app = FastAPI()
app.include_router(router)



def main():
    print("Hello from enterprise-ai-engineering-platform!")
    #app1 = main_graph

@app.on_event("startup")
async def startup():
    print("Initializing MCP...")
    await MCPManager.initialize()

    from graph.graph_builder import build_graph
    build_graph()

#uv run uvicorn main:app --reload
if __name__ == "__main__":
    main()
