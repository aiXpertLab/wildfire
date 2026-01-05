# app/haystack/router.py
from fastapi import APIRouter
from pydantic import BaseModel

from app.haystack.agent1_quick_start import run_agent
# from app.haystack.agent2_serper_sql import run_sql_agent
from app.schemas.haystack import AgentResponseString, SQLAgentResponseList, AllRequestString

hsRou = APIRouter()

# ---------------- Haystack Chat Agent ----------------
@hsRou.post("/haystack/agent1-quick-start", response_model=AgentResponseString)
def run_haystack_agent(payload: AllRequestString):
    answer = run_agent(payload.query)
    return {"answer": answer}


# # ---------------- SQL Agent ----------------
# @hsRou.post("/haystack/agent2_serper_sql", response_model=SQLAgentResponseList)
# def run_haystack_sql_agent(payload: AllRequestString):
#     rows = run_sql_agent(payload.query)
#     return {"results": rows}
