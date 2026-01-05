# app/haystack/router.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.haystack.agent.agent1_quick_start import run_agent
# from app.haystack.agent2_serper_sql import run_sql_agent
from app.schemas.haystack import AgentResponseString, SQLAgentResponseList, AllRequestString
from app.haystack.rag.rag_singleton import get_rag_service
from app.haystack.rag.rag_service import RAGService

hsRouRag = APIRouter()

class RAGRequest(BaseModel):
    question: str


class RAGResponse(BaseModel):
    answer: str


@hsRouRag.post("/rag1", response_model=RAGResponse)
def ask_rag(
    payload: RAGRequest,
    rag_service: RAGService = Depends(get_rag_service),
):
    answer = rag_service.ask(payload.question)
    return RAGResponse(answer=answer)
