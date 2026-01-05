# app/haystack/router.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.haystack.agent.agent1_quick_start import run_agent
# from app.haystack.agent2_serper_sql import run_sql_agent
from app.schemas.haystack import AgentResponseString, SQLAgentResponseList, AllRequestString
from app.haystack.rag.rag_singleton import get_rag_service
from app.haystack.rag.rag_service import RAGService
from app.haystack.rag.pgvector_service import PgVectorSearchService

from app.haystack.rag.pgvector_singleton import get_pgvector_service

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



class SearchRequest(BaseModel):
    query: str = "How many languages are there?"
    top_k: int = 1


class SearchResponse(BaseModel):
    results: list[str]


@hsRouRag.post("/search", response_model=SearchResponse)
def search(
    payload: SearchRequest,
    service: PgVectorSearchService = Depends(get_pgvector_service),
):
    results = service.search(
        query=payload.query,
        top_k=payload.top_k,
    )
    return SearchResponse(results=results)