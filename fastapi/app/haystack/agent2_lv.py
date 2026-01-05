from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.tools import ComponentTool
from tools.sql_tool import SQLDealQueryTool
from tools.embedding_tool import EmbeddingSearchTool

sql_tool = ComponentTool(component=SQLDealQueryTool(), name="SQLDealQueryTool")
embedding_tool = ComponentTool(component=EmbeddingSearchTool(), name="EmbeddingSearchTool")

agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini"),
    system_prompt="You are a smart assistant for the Deals CRM. Decide which tool to use.",
    tools=[sql_tool, embedding_tool],
)



# response = agent.run("How many deals are Closed Won?")
# print(response["last_message"].text)

# response = agent.run("Who is the lead for the Walmart deal?")
# print(response["last_message"].text)
