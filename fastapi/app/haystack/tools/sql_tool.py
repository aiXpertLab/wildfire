# tools/sql_tool.py
from haystack.nodes import BaseComponent
import psycopg2
import pandas as pd

class SQLDealQueryTool(BaseComponent):
    outgoing_edges = 1

    def __init__(self, dsn: str):
        """
        dsn: PostgreSQL connection string, e.g.
        "dbname=deals user=leo password=xxxx host=localhost port=5432"
        """
        self.dsn = dsn

    def run(self, query: str) -> dict:
        """
        Executes structured/statistical queries.
        query: natural language or SQL string
        """
        # NOTE: In production, map natural language -> SQL safely
        # Here we assume LLM sends SQL directly or structured params
        with psycopg2.connect(self.dsn) as conn:
            df = pd.read_sql(query, conn)

        return {"result": df.to_dict(orient="records")}
