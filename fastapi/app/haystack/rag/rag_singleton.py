# app/services/rag_singleton.py
from functools import lru_cache
from app.haystack.rag.rag_service import RAGService

@lru_cache()
def get_rag_service() -> RAGService:
    service = RAGService()
    service.initialize()
    return service
