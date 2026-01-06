# app/api/rou_sql_agent.py
from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List, Optional

from app.haystack.rag.sql_query import SQLQuery
from app.haystack.rag.sql_agent_service import SQLAgentService

from app.config import get_settings_singleton
from app.haystack.rag.conditional_sql_agent_service import ConditionalSQLAgentService
settings = get_settings_singleton()

sql_query_component = SQLQuery(settings.PG_SYNC)
sql_agent = SQLAgentService(settings.PG_SYNC)

class QuestionRequest(BaseModel):
    question: Optional[str] = None

class SQLRequest(BaseModel):
    queries: List[str]

hsRouSQL = APIRouter()

@hsRouSQL.post("/sql1")
def run_sql(request: SQLRequest):
    result = sql_query_component.run(queries=request.queries)
    return {
        "queries": result["queries"],
        "results": result["results"],
    }
    
    
@hsRouSQL.post("/sql-agent")
def run_sql_agent(request: QuestionRequest | None = Body(default=None)):
    question = request.question if request else None
    return sql_agent.ask(question)
# {
#   "question": "On which days of the week does the average absenteeism time exceed 4 hours"
# }




conditional_sql_agent = ConditionalSQLAgentService(settings.PG_SYNC)

@hsRouSQL.post("/sql-agent-conditional")
def run_conditional_sql_agent(payload: QuestionRequest = Body(...)):
    return conditional_sql_agent.ask(payload.question)