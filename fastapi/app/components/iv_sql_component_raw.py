# app/haystack/sql_query.py
from typing import List
import pandas as pd
from sqlalchemy import text
from haystack import component

from app.db.db_sync import engine_sync
from app.utils.sanitize import clean_sql
from app.utils.sql_guard import guard_sql, SQLGuardError


@component
class RawSQLQueryComponent:
    def __init__(self):
        self.engine = engine_sync

    @component.output_types(results=List[list[dict]], queries=List[str], errors=List[str])
    def run(self, queries: List[str]):
        results = []
        cleaned_queries = []
        errors = []

        with self.engine.connect() as conn:
            for query in queries:
                try:
                    # 1. sanitize (your existing logic)
                    q = clean_sql(query)

                    # 2. guard (NEW – mandatory)
                    q = guard_sql(q)

                    # 3. execute
                    df = pd.read_sql(text(q), conn)

                    # 4. structured truth output
                    results.append(df.to_dict(orient="records"))
                    cleaned_queries.append(q)
                    errors.append("")

                except (SQLGuardError, Exception) as e:
                    results.append([])
                    cleaned_queries.append("")
                    errors.append(str(e))

        return {
            "results": results,
            "queries": cleaned_queries,
            "errors": errors,
        }
