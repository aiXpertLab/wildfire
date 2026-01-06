# app/haystack/sql_query.py
from typing import List
from haystack import component
from sqlalchemy import create_engine, text
import pandas as pd

@component
class SQLQuery:
    def __init__(self, pg_conn_str: str):
        self.engine = create_engine(pg_conn_str)

    @component.output_types(results=List[str], queries=List[str])
    def run(self, queries: List[str]):
        results = []
        with self.engine.connect() as conn:
            for query in queries:
                df = pd.read_sql(text(query), conn)
                results.append(df.to_string(index=False))
        return {"results": results, "queries": queries}
