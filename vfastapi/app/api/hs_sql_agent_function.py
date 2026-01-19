# app/api/rou_sql_agent.py
from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List, Optional

from app.components.sql_raw import RawSQLQuery
from app.components.sql_agent_simple import SQLAgentService
from app.components.sql_agent_conditional import ConditionalSQLAgentService
from app.components.sql_agent_function import SQLFunctionAgentService
from app.schemas.haystack import ResultString, QueryString, ResultList, QueryList


hsSqlAgentFunction = APIRouter()

sql_query_component = RawSQLQuery()
sql_agent = SQLAgentService()


sql_func_agent = SQLFunctionAgentService()


class SQLFunctionRequest(BaseModel):
    question: str = "On which days of the week does the average absenteeism time exceed 4 hours?"


@hsSqlAgentFunction.post("/sql-agent-function")
def run_sql_function_agent(payload: SQLFunctionRequest = Body(...)):
    return sql_func_agent.ask(payload.question)
