# app/api/rou_sql_agent.py
from fastapi import APIRouter, Body
from app.components.sql_agent_simple import SQLAgentService
from app.schemas.haystack import QueryString

hsSqlAgent = APIRouter()

sql_agent = SQLAgentService()

@hsSqlAgent.post("/sql-agent-simple", summary="Run 1 SQL Agent Simple")
def run_sql_agent(request: QueryString | None = Body(default=None)):
    question = request.query if request else None
    return sql_agent.run(question)
# {
#   "query": "On which days of the week does the average absenteeism time exceed 4 hours"
# }

