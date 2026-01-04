# hs.py
import os

from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.tools import ComponentTool
from haystack.components.websearch import SerperDevWebSearch

import logging
logger = logging.getLogger(__name__)

from app.config import get_settings_singleton
settings = get_settings_singleton()

os.environ["SERPERDEV_API_KEY"] = settings.SERPERDEV_API_KEY
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
search_tool = ComponentTool(component=SerperDevWebSearch())

agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini"),
    system_prompt="You are a helpful web agent.",
    tools=[search_tool],
)


def run_agent(user_message: str) -> str:
    """
    Executes the Haystack agent and returns the final text response.
    """
    logger.info("Haystack user message: %r", user_message)

    result = agent.run(
        messages=[ChatMessage.from_user(user_message)]
    )
    return result["last_message"].text
