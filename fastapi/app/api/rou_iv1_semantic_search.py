from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from app.haystack.rag.pgvector_service import PgVectorSearchService
from app.haystack.iv.pg_singleton import get_pgvector_service

hsRouSemantic = APIRouter()


class SemanticQueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


@hsRouSemantic.post("/semantic_search")
def semantic_search(
    request: SemanticQueryRequest,
    service: PgVectorSearchService = Depends(get_pgvector_service),
):
    documents = service.search(
        query=request.query,
        top_k=request.top_k,
    )

    return {
        "query": request.query,
        "count": len(documents),
        "results": [
            {
                "id": d.id,
                "score": d.score,
                "content": d.content,
                "meta": d.meta,
            }
            for d in documents
        ],
    }
