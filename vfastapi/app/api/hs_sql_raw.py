# app/api/rou_sql_agent.py
from fastapi import APIRouter, Body

from app.components.sql_raw import RawSQLQuery
from app.schemas.haystack import QueryList

hsSqlRaw = APIRouter()

sql_query_component = RawSQLQuery()

@hsSqlRaw.post("/sql-raw")
def run_sql(request: QueryList):
    result = sql_query_component.run(queries=request.queries)
    return {
        "queries": result["queries"],
        "results": result["results"],
    }
    # {
    #     "queries": [
    #         "select * from alembic_version"
    
    #           "SELECT tablename FROM pg_tables;"
    #     ]
    # }

