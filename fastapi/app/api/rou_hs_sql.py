# app/api/rou_sql_agent.py
from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List

from app.haystack.rag.sql_query import SQLQuery

from app.config import get_settings_singleton
settings = get_settings_singleton()

sql_query_component = SQLQuery(settings.PG_SYNC)


DEFAULT_QUERY = (
    "SELECT Age, "
    "SUM(Absenteeism_time_in_hours) AS Total_Absenteeism_Hours "
    "FROM absenteeism "
    "WHERE Disciplinary_failure = 0 "
    "GROUP BY Age "
    "ORDER BY Total_Absenteeism_Hours DESC "
    "LIMIT 3"
)

class SQLRequest(BaseModel):
    queries: List[str]

hsRouSQL = APIRouter()

@hsRouSQL.post("/sql/query")
def run_sql(request: SQLRequest):
    result = sql_query_component.run(queries=request.queries)
    return {
        "queries": result["queries"],
        "results": result["results"],
    }