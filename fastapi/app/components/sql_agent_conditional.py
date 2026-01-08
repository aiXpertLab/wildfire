# app/haystack/rag/conditional_sql_agent_service.py
from typing import List
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators.openai import OpenAIGenerator
from haystack.components.routers import ConditionalRouter

from app.components.sql_query import RawSQLQuery


ABSENTEEISM_COLUMNS = """
        ID, Reason_for_absence, Month_of_absence, Day_of_the_week,
        Seasons, Transportation_expense, Distance_from_Residence_to_Work,
        Service_time, Age, Work_load_Average_day, Hit_target,
        Disciplinary_failure, Education, Son, Social_drinker,
        Social_smoker, Pet, Weight, Height, Body_mass_index,
        Absenteeism_time_in_hours
    """


class ConditionalSQLAgentService:
    def __init__(self, pg_conn_str: str):
        self.sql_query = RawSQLQuery(pg_conn_str)

        self.prompt = PromptBuilder(
            template="""
                Please generate an SQL query.

                Question:
                {{ question }}

                If the question cannot be answered using the table and columns below,
                return exactly: no_answer

                Table: absenteeism
                Columns:
                {{ columns }}

                Return ONLY SQL or no_answer.
                """
        )

        self.llm = OpenAIGenerator(model="gpt-4o-mini")

        self.routes = [
            {
                "condition": "{{ 'no_answer' not in replies[0] }}",
                "output": "{{ replies }}",
                "output_name": "sql",
                "output_type": List[str],
            },
            {
                "condition": "{{ 'no_answer' in replies[0] }}",
                "output": "{{ question }}",
                "output_name": "fallback_question",
                "output_type": str,
            },
        ]

        self.router = ConditionalRouter(self.routes)

        self.fallback_prompt = PromptBuilder(
            template="""
                        The user asked a question that cannot be answered using this table.

                        Question:
                        {{ question }}

                        Available columns:
                        {{ columns }}

                        Explain clearly why the question cannot be answered.
                    """
        )

        self.fallback_llm = OpenAIGenerator(model="gpt-4o-mini")

        self.pipeline = Pipeline()
        self.pipeline.add_component("prompt", self.prompt)
        self.pipeline.add_component("llm", self.llm)
        self.pipeline.add_component("router", self.router)
        self.pipeline.add_component("sql", self.sql_query)
        self.pipeline.add_component("fallback_prompt", self.fallback_prompt)
        self.pipeline.add_component("fallback_llm", self.fallback_llm)

        self.pipeline.connect("prompt", "llm")
        self.pipeline.connect("llm.replies", "router.replies")
        self.pipeline.connect("router.sql", "sql.queries")
        self.pipeline.connect("router.fallback_question", "fallback_prompt.question")
        self.pipeline.connect("fallback_prompt", "fallback_llm")

    def ask(self, question: str):
        result = self.pipeline.run(
            {
                "prompt": {
                    "question": question,
                    "columns": ABSENTEEISM_COLUMNS,
                },
                "router": {
                    "question": question,
                },
                "fallback_prompt": {
                    "columns": ABSENTEEISM_COLUMNS,
                },
            }
        )

        if "sql" in result:
            return {
                "type": "sql_result",
                "sql": result["sql"]["queries"][0],
                "result": result["sql"]["results"][0],
            }

        return {
            "type": "no_answer",
            "message": result["fallback_llm"]["replies"][0],
        }
