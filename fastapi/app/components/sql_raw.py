# app/haystack/sql_query.py
from typing import List
from haystack import component
from sqlalchemy import text
import pandas as pd
from app.db.db_sync import engine_sync

from app.utils.sanitize import clean_sql


@component
class RawSQLQuery:
    def __init__(self):
        self.engine = engine_sync

    @component.output_types(results=List[str], queries=List[str])
    def run(self, queries: List[str]):
        results = []
        cleaned_queries = []

        with self.engine.connect() as conn:
            for query in queries:
                q = clean_sql(query)
                df = pd.read_sql(text(q), conn)
                results.append(df.to_string(index=False))
                cleaned_queries.append(q)

        return {"results": results, "queries": cleaned_queries}
