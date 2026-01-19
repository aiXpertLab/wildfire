# app/haystack/router.py
from fastapi import APIRouter

from app.haystack.agent.agent1_quick_start import run_agent
from app.schemas.haystack import ResultString, QueryString

hsAgent = APIRouter()

# ---------------- Haystack Chat Agent ----------------
@hsAgent.post("/quick-start", response_model=ResultString)
def run_haystack_agent(payload: QueryString):
    answer = run_agent(payload.query)
    return {"answer": answer}


