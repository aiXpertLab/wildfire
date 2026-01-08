# app/api/rou_sql_agent.py
from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List, Optional

from app.components.sql_query import RawSQLQuery
from app.haystack.rag.sql_agent_service import SQLAgentService
from app.haystack.rag.conditional_sql_agent_service import ConditionalSQLAgentService
from app.haystack.rag.sql_function_agent_service import SQLFunctionAgentService
from app.schemas.haystack import ResultString, QueryString, ResultList, QueryList

from app.config import get_settings_singleton
settings = get_settings_singleton()

hsSqlAgent = APIRouter()

sql_query_component = RawSQLQuery(settings.PG_SYNC)
sql_agent = SQLAgentService(settings.PG_SYNC)


@hsSqlAgent.post("/raw-sql-language")
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


@hsSqlAgent.post("/sql-agent")
def run_sql_agent(request: QueryString | None = Body(default=None)):
    question = request.query if request else None
    return sql_agent.ask(question)
# {
#   "question": "On which days of the week does the average absenteeism time exceed 4 hours"
# }


conditional_sql_agent = ConditionalSQLAgentService(settings.PG_SYNC)


@hsSqlAgent.post("/sql-agent-conditional")
def run_conditional_sql_agent(payload: QueryList = Body(...)):
    return conditional_sql_agent.ask(payload.queries)


sql_func_agent = SQLFunctionAgentService(settings.PG_SYNC)


class SQLFunctionRequest(BaseModel):
    question: str = "On which days of the week does the average absenteeism time exceed 4 hours?"


@hsSqlAgent.post("/sql-agent-function")
def run_sql_function_agent(payload: SQLFunctionRequest = Body(...)):
    return sql_func_agent.ask(payload.question)
