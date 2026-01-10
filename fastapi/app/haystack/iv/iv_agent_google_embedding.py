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
    component=IVSemanticComponent(),
    name="internal_search",
    description="Search internal company and deal data using vector similarity."
)

# ---------------------------------------------------------------------
# AGENT
# ---------------------------------------------------------------------

agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini"),
    system_prompt=(
        "You are a helpful assistant.\n"
        "Use internal_search for internal company or deal data.\n"
        "Use web_search only if internal data is insufficient or needs to be fresh."
    ),
    tools=[
        search_tool,
        iv_search_tool,
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

    for log in result.get("tool_logs", []):
        logger.info("Tool used: %s", log.get("tool_name"))
        logger.info("Tool input: %s", log.get("tool_input"))
        logger.info("Tool output: %s", log.get("tool_output"))

    return result["last_message"].text
