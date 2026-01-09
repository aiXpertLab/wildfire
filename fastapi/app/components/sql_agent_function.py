# app/haystack/rag/sql_function_agent_service.py
from typing import List
import json
from haystack.dataclasses import ChatMessage
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.generators.utils import print_streaming_chunk
from app.components.sql_raw import RawSQLQuery

ABSENTEEISM_COLUMNS = """
ID, Reason_for_absence, Month_of_absence, Day_of_the_week,
Seasons, Transportation_expense, Distance_from_Residence_to_Work,
Service_time, Age, Work_load_Average_day, Hit_target,
Disciplinary_failure, Education, Son, Social_drinker,
Social_smoker, Pet, Weight, Height, Body_mass_index,
Absenteeism_time_in_hours
"""

class SQLFunctionAgentService:
    def __init__(self, pg_conn_str: str):
        # PostgreSQL connection
        self.sql_query = RawSQLQuery(pg_conn_str)

        # Wrap SQLQuery component as a function (exactly like your working code)
        def sql_query_func(queries: List[str]):
            try:
                result = self.sql_query.run(queries)
                return {"reply": result["results"][0]}
            except Exception as e:
                reply = f"""There was an error running the SQL Query = {queries}
The error is {e}.
You should probably try again."""
                return {"reply": reply}

        self.sql_query_func = sql_query_func

        # Define tools for LLM function calling (aligned with working example)
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "sql_query_func",
                    "description": f"This tool queries the 'absenteeism' table with columns: {ABSENTEEISM_COLUMNS}",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "queries": {
                                "type": "array",
                                "description": "The SQL query inferred from the user's question.",
                                "items": {"type": "string"},
                            }
                        },
                        "required": ["question"],  # <- must be "question", not "queries"
                    },
                },
            }
        ]

        # Initialize LLM
        self.chat_generator = OpenAIChatGenerator(
            model="gpt-4", streaming_callback=print_streaming_chunk
        )

    def ask(self, user_question: str):
        # Prepare messages
        messages = [
            ChatMessage.from_system(
                "You are a helpful agent who can query the 'absenteeism' SQL table."
            ),
            ChatMessage.from_user(user_question),
        ]

        # Run LLM with function tools
        response = self.chat_generator.run(
            messages=messages,
            generation_kwargs={"tools": self.tools},
        )
        
        print("-------------Full response:", response)
        
        tool_call = response["replies"][0]._content[0]
        function_name = tool_call.tool_name
        function_args = tool_call.arguments

        # # Parse function call exactly like your working code
        # function_call_data = json.loads(response["replies"][0].text)[0]
        # function_name = function_call_data["function"]["name"]
        # function_args = json.loads(function_call_data["function"]["arguments"])

        # Call the actual SQLQuery function
        available_functions = {"sql_query_func": self.sql_query_func}
        function_to_call = available_functions[function_name]
        return function_to_call(**function_args)
