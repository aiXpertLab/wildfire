# hs.py
import os
import logging

from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.websearch import SerperDevWebSearch
from haystack.tools import ComponentTool
from haystack.dataclasses import ChatMessage

from app.config import get_settings_singleton
from app.components.iv_semantics_component import IVSemanticComponent
from app.components.iv_sql_component_raw import RawSQLQueryComponent

logger = logging.getLogger(__name__)


# Web search tool
web_search_tool = ComponentTool(
    component=SerperDevWebSearch(),
    name="web_search",
    description="Search the public web for fresh or external information.",
)

# semantic search tool
semantics_search_tool = ComponentTool(
    component=IVSemanticComponent(),
    name="internal_search",
    description=(
        "Search internal company and deal data using vector similarity. "
        "Use this tool when the user asks questions about patterns, trends, summaries, "
        "or similarities between deals, lead owners, accounts, or sources. "
        "Do NOT execute exact SQL or structured filters here."
    ),
)

sql_search_tool = ComponentTool(
    component=RawSQLQueryComponent(),
    name="sql_search",
    description=(
        "Execute exact SQL queries against the 'innov' table. "
        "Use ONLY when the user question can be answered with structured filters. "
        "Table: innov. "
        "Columns: account_id, date, company, first_name, last_name, lead_owner, deal_stage, source. "
        "Use 'date' for any deal creation or time-based filtering."
        "❌ DO NOT invent or rename columns."
        "❌ 'deal_created_date' does NOT exist."
        "Input must be valid SQL. Do not use for semantic or fuzzy search."
    ),
)
# ---------------------------------------------------------------------
# AGENT
# ---------------------------------------------------------------------
agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini"),
    tools=[
        sql_search_tool,
        semantics_search_tool,
        web_search_tool,
    ],
)


# ---------------------------------------------------------------------
# RUNNER
# ---------------------------------------------------------------------


def run_agent(user_message: str) -> str:
    """
    Executes the Haystack agent and returns the final text response.
    """
    logger.info("Haystack user message: %r", user_message)

    result = agent.run(messages=[ChatMessage.from_user(user_message)])

    return result["last_message"].text
