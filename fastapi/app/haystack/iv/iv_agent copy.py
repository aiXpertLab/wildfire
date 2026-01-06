# hs.py
import os

from haystack.tools import Tool, ComponentTool
from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever
from haystack.dataclasses import ChatMessage
from haystack.components.websearch import SerperDevWebSearch
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from haystack import Document

import logging

from app.haystack.iv.iv_singleton import get_ivservice
logger = logging.getLogger(__name__)

from app.config import get_settings_singleton
settings = get_settings_singleton()

os.environ["SERPERDEV_API_KEY"] = settings.SERPERDEV_API_KEY
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
# search_tool = ComponentTool(component=SerperDevWebSearch())

# -------- TOOL 1: WEB SEARCH --------
search_tool = ComponentTool(
    component=SerperDevWebSearch(),
    name="web_search",
    description="Search the public web for fresh or external information."
)

# -------- TOOL 2: PGVECTOR (RAG) --------
document_store = PgvectorDocumentStore(
    connection_string=settings.PG_ASYNC,
    table_name="haystack_documents",      # must match your existing table
    embedding_dimension=384            # must match stored embeddings
)

retriever = PgvectorEmbeddingRetriever(
    document_store=document_store
)

ivservice = get_ivservice()

# Use Tool class for pipelines, not ComponentTool
pgvector_tool = Tool.from_pipeline(
    pipeline=ivservice.pipeline,
    name="internal_search",
    description="Search internal company and deal data from database."
)

# -------- AGENT SETUP --------
agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini"),
    system_prompt=(
        "You are a helpful agent.\n"
        "Use internal_search for company or deal data.\n"
        "Use web_search only if information is not internal or needs to be fresh."
    ),
    tools=[search_tool, pgvector_tool],
)



def run_agent(user_message: str) -> str:
    """
    Executes the Haystack agent and returns the final text response.
    """
    logger.info("Haystack user message: %r", user_message)

    result = agent.run(
        messages=[ChatMessage.from_user(user_message)]
    )
    for log in result["tool_logs"]:
        print("Tool used:", log["tool_name"])
        print("Input given to tool:", log["tool_input"])
        print("Tool output:", log["tool_output"])

    return result["last_message"].text


