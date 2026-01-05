# app/haystack/agent_all.py
import os
import logging
from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.tools import ComponentTool
from haystack.tools.sql import SQLNLTool
from haystack.nodes import EmbeddingRetriever

from app.config import get_settings_singleton
settings = get_settings_singleton()

logger = logging.getLogger(__name__)

# ---------------- Environment ----------------
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# ---------------- Tools ----------------

# 1. SQL tool for PostgreSQL deal table
sql_tool = SQLNLTool.from_database_url(
    settings.DATABASE_URL,
    name="SQL Deal Query"
)

# 2. Semantic search tool for embeddings
retriever_tool = ComponentTool(
    component=EmbeddingRetriever(index="haystack_documents")
)

# ---------------- Single Agent ----------------
agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini"),
    tools=[sql_tool, retriever_tool],
    system_prompt="""
You are a deals agent. Decide which tool to use:
- Use the SQL Deal Query for statistics or aggregates.
- Use the embeddings retriever for detailed deal info.
Provide the answer in human-readable text.
"""
)

# ---------------- Entrypoint ----------------
def run_agent(user_query: str) -> str:
    logger.info("Haystack user message: %r", user_query)
    result = agent.run(messages=[ChatMessage.from_user(user_query)])
    return result.get("last_message", {}).get("text", "")
