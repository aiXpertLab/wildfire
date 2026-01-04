from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from app.haystack.agent1_quick_start import run_agent

hsRou = APIRouter()


class AgentRequest(BaseModel):
    query: str


class AgentResponse(BaseModel):
    answer: str


@hsRou.post("/haystack/run", response_model=AgentResponse)
def run_haystack_agent(payload: AgentRequest):
    answer = run_agent(payload.query)
    return {"answer": answer}
