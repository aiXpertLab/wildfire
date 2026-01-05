# tools/sql_nl_tool.py
from haystack.nodes import BaseComponent
import psycopg2
import pandas as pd
from openai import OpenAI

class SQLNLTool(BaseComponent):
    outgoing_edges = 1

    def __init__(self, dsn: str, openai_api_key: str):
        self.dsn = dsn
        self.client = OpenAI(api_key=openai_api_key)

    def run(self, user_query: str) -> dict:
        """
        1. Convert natural language to SQL
        2. Execute SQL
        3. Return structured results
        """
        # Prompt to LLM to generate SQL safely
        prompt = f"""
You are an assistant that translates natural language questions into SQL queries.
Table: deals(Date, Lead Owner, Source, Deal Stage, Account Id, First Name, Last Name, Company)

Convert the following user question into a SQL query:
Question: "{user_query}"
Only return SQL, no explanations.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        sql_query = response.choices[0].message.content.strip()

        # Execute SQL
        with psycopg2.connect(self.dsn) as conn:
            df = pd.read_sql(sql_query, conn)

        return {"result": df.to_dict(orient="records")}
