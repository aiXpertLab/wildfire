# app/api/rou_sql_agent.py
from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List, Optional

from app.components.sql_query import RawSQLQuery
from app.schemas.haystack import QueryList

from app.config import get_settings_singleton
settings = get_settings_singleton()

hsSqlRaw = APIRouter()

sql_query_component = RawSQLQuery(settings.PG_SYNC)

@hsSqlRaw.post("/sql-raw", tags=["rou_hs_sql_raw"])
def run_sql(request: QueryList):
    result = sql_query_component.run(queries=request.queries)
    return {
        "queries": result["queries"],
        "results": result["results"],
    }
    # {
    #     "queries": [
    #         "select * from alembic_version"
    #     ]
    # }

