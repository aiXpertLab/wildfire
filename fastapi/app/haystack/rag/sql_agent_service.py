# app/haystack/sql_agent_service.py
import os
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators.openai import OpenAIGenerator

from app.components.sql_query import RawSQLQuery


DEFAULT_QUESTION = (
    "On which days of the week does the average absenteeism time exceed 4 hours?"
)

ABSENTEEISM_COLUMNS = """
ID, Reason_for_absence, Month_of_absence, Day_of_the_week,
Seasons, Transportation_expense, Distance_from_Residence_to_Work,
Service_time, Age, Work_load_Average_day, Hit_target,
Disciplinary_failure, Education, Son, Social_drinker,
Social_smoker, Pet, Weight, Height, Body_mass_index,
Absenteeism_time_in_hours
"""


class SQLAgentService:
    def __init__(self, pg_conn_str: str):
        self.sql_executor = RawSQLQuery(pg_conn_str)

        self.prompt = PromptBuilder(
            template="""
                Generate a single valid PostgreSQL SQL query.

                Question:
                {{ question }}

                Table: absenteeism

                Columns:
                {{ columns }}

                Return ONLY the SQL query. No explanation.
                """,
            required_variables=["question", "columns"],  # <-- add this line
        )

        self.llm = OpenAIGenerator(model="gpt-4o-mini")

        self.pipeline = Pipeline()
        self.pipeline.add_component("prompt", self.prompt)
        self.pipeline.add_component("llm", self.llm)
        self.pipeline.add_component("sql", self.sql_executor)

        self.pipeline.connect("prompt", "llm")
        self.pipeline.connect("llm.replies", "sql.queries")

    def ask(self, question: str | None = None):
        question = question or DEFAULT_QUESTION

        result = self.pipeline.run(
            {
                "prompt": {
                    "question": question,
                    "columns": ABSENTEEISM_COLUMNS,
                }
            }
        )

        return {
            "generated_sql": result["sql"]["queries"][0],
            "result": result["sql"]["results"][0],
        }
