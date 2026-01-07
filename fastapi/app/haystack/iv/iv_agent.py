# hs.py
import os
import logging

from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.websearch import SerperDevWebSearch
from haystack.tools import ComponentTool
from haystack.dataclasses import ChatMessage

from app.config import get_settings_singleton
from app.haystack.iv.iv_search_component import IVSemanticSearchComponent
from app.haystack.iv.iv_sql_component import IVSQLSearchComponent

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------
settings = get_settings_singleton()

os.environ["SERPERDEV_API_KEY"] = settings.SERPERDEV_API_KEY
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# ---------------------------------------------------------------------
# TOOLS
# ---------------------------------------------------------------------

# Web search tool
search_tool = ComponentTool(
    component=SerperDevWebSearch(),
    name="web_search",
    description="Search the public web for fresh or external information."
)

# Internal semantic search tool (wraps IVService.search)
iv_search_tool = ComponentTool(
    component=IVSemanticSearchComponent(),
    name="internal_search",
    description="Search internal company and deal data using vector similarity."
)

sql_search_tool = ComponentTool(
    component=IVSQLSearchComponent(),
    name="sql_search",
    description=(
        "Use this tool ONLY for exact, structured queries on reports data. "
        "Examples: account_id, company, first_name, last_name, lead_owner, "
        "deal_stage, source, or recent records. "
        "Do NOT use for semantic similarity or vague questions."
    ),
)
# ---------------------------------------------------------------------
# AGENT
# ---------------------------------------------------------------------
agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini"),
    system_prompt=(
        "You are a routing assistant.\n"
        "Routing rules:\n"
        "- Use sql_search for EXACT, structured queries on reports "
        "(ID, first_name, last_name, company, deal_stage, lead_owner, source, account_id, dates).\n"
        "- Use internal_search for semantic or fuzzy meaning-based search.\n"
        "- Use web_search only for fresh external information.\n"
        "If sql_search returns results, prefer them."
        "Optional argument 'count_only=True' returns the numeric count instead of documents. "
        "Do NOT use for semantic or vague queries."
    ),
    tools=[
        sql_search_tool,
        iv_search_tool,
        search_tool,
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

    result = agent.run(
        messages=[ChatMessage.from_user(user_message)]
    )

    return result["last_message"].text
