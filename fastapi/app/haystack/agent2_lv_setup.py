# agent_setup.py
from haystack.tools import ComponentTool
from tools.sql_nl_tool import SQLNLTool

sql_nl_tool = ComponentTool(
    component=SQLNLTool(DSN, openai_api_key="YOUR_OPENAI_KEY"),
    name="SQLNLTool"
)

agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini"),
    system_prompt="""
You are an assistant for the Deals CRM. Available tools:
1. SQLNLTool: Converts natural language to SQL and executes it on the Deals table.
2. EmbeddingSearchTool: Performs semantic search on deal documents.
Always pick the most relevant tool.
""",
    tools=[sql_nl_tool, embedding_tool],
)
