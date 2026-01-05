# app/haystack/agent_sql.py
from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
# from haystack.tools.sql import SQLNLTool
from app.config import get_settings_singleton
import os

settings = get_settings_singleton()
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# Define SQL tool (your database connection details)
sql_tool = SQLNLTool.from_database_url(
    settings.DATABASE_URL,  # e.g., postgresql://user:pass@host:port/dbname
    name="SQL Deal Query"
)

# Agent for SQL queries
sql_agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini"),
    tools=[sql_tool],
    system_prompt="You are an agent that converts natural language questions into SQL queries and returns results."
)


def run_sql_agent(user_query: str):
    """
    Run the SQL agent and return results as a list of dicts.
    """
    result = sql_agent.run(messages=[ChatMessage.from_user(user_query)])
    # SQLNLTool returns 'result' key with query output
    return result.get("result", [])
