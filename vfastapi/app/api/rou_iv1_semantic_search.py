from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

# from app.haystack.rag.pgvector_service import PgVectorSearchService
from app.haystack.iv.iv_singleton import get_ivservice
from app.haystack.iv.iv_search_service import IVService 

hsRouSemantic = APIRouter()


class SemanticQueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


@hsRouSemantic.post("/q384")
def q384(
    request: SemanticQueryRequest,
    ivservice: IVService = Depends(get_ivservice),
):
    documents = ivservice.search(
        query=request.query,
        top_k=request.top_k,
    )

    # return {
    #     "type": str(type(documents[0])),
    #     "raw_document": documents[0].to_dict(),
    #     "available_attrs": list(documents[0].__dict__.keys()),
    # }
    
    # return {
    #     "query": request.query,
    #     "count": len(documents),
    #     "results": [
    #         {
    #             "id": d.id,
    #             "score": d.score,
    #             "content": d.content,
    #             "meta": d.meta,
    #         }
    #         for d in documents
    #     ],
    # }
    
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

