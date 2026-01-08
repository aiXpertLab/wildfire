# app/haystack/router.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.haystack.rag.rag_singleton import get_rag_service_in_memory
from app.haystack.rag.rag_service import RAGService4InMemory
from app.haystack.rag.pgvector_service import PgVectorSearchService

from app.haystack.rag.pgvector_singleton import get_pgvector_service
from app.schemas.haystack import ResultString, QueryString, ResultList

hsRag = APIRouter()


@hsRag.post("/rag_in_memory", response_model=ResultString)
def ask_rag(
    payload: QueryString,
    rag_service: RAGService4InMemory = Depends(get_rag_service_in_memory),
):
    answer = rag_service.ask(payload.query)
    return ResultString(result=answer)



@hsRag.post("/pgvector_search", response_model=ResultList)
def search(
    payload: QueryString,
    service: PgVectorSearchService = Depends(get_pgvector_service),
):
    results = service.search(
        query=payload.query,
        top_k=payload.top_k,
    )
    return ResultList(results=results)