# app/api/rou_sql_agent.py
from fastapi import APIRouter, Body
from app.components.sql_agent_conditional import ConditionalSQLAgentService
from app.schemas.haystack import ResultString, QueryString, ResultList, QueryList

from app.config import get_settings_singleton
settings = get_settings_singleton()

hsSqlAgentConditional = APIRouter()

conditional_sql_agent = ConditionalSQLAgentService(settings.PG_SYNC)

@hsSqlAgentConditional.post("/sql-agent-conditional")
def run_conditional_sql_agent(payload: QueryList = Body(...)):
    return conditional_sql_agent.ask(payload.queries)


