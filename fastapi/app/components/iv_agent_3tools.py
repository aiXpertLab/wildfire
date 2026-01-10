# hs.py
import os, logging

from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.websearch import SerperDevWebSearch
from haystack.tools import ComponentTool
from haystack.dataclasses import ChatMessage

from app.config import get_settings_singleton
from app.components.iv_semantics_component import IVSemanticComponent
from app.components.iv_sql_component import IVSQLSearchComponent

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------
settings = get_settings_singleton()
if os.environ.get("SERPERDEV_API_KEY") != settings.SERPERDEV_API_KEY:os.environ["SERPERDEV_API_KEY"] = settings.SERPERDEV_API_KEY
if os.environ.get("OPENAI_API_KEY") != settings.OPENAI_API_KEY:      os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# ---------------------------------------------------------------------
# TOOLS
# ---------------------------------------------------------------------

# Web search tool
web_search_tool = ComponentTool(
    component=SerperDevWebSearch(),
    name="web_search",
    description="Search the public web for fresh or external information.",
)

# Internal semantic search tool (wraps IVService.search)
semantics_search_tool = ComponentTool(
    component=IVSemanticComponent(),
    name="internal_search",
    description="Search internal company and deal data using vector similarity.",
)

sql_search_tool = ComponentTool(
    component=IVSQLSearchComponent(),
    name="sql_search",
    description=(
        "Use this tool for exact SQL queries on the 'reports' table. "
        "Columns: account_id, company, first_name, last_name, lead_owner, "
        "deal_stage, source, account_balance, created_at, updated_at. "
        "Examples: 'WHERE first_name = \"John\" AND last_name = \"Doe\"', "
        "'WHERE deal_stage IN (\"prospect\", \"negotiation\") ORDER BY created_at DESC LIMIT 10'."
    ),
    # description=(
    #     "Use for exact SQL queries on 'reports' table. "
    #     "Available columns: account_id, company, first_name, last_name, lead_owner, "
    #     "deal_stage, source, account_balance, created_at, updated_at. "
    #     "Examples: "
    #     "- 'WHERE first_name = 'John' AND last_name = 'Doe'' "
    #     "- 'WHERE deal_stage IN ('prospect', 'negotiation')' "
    #     "- 'ORDER BY created_at DESC LIMIT 10'"
    #     "Do NOT use for vague or semantic questions."
    # ),
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
