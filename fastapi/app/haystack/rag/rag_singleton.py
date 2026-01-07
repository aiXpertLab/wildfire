# app/services/rag_singleton.py
from functools import lru_cache
from app.haystack.rag.rag_service import RAGService4InMemory

@lru_cache()
def get_rag_service_in_memory() -> RAGService4InMemory:
    service = RAGService4InMemory()
    service.initialize()
    return service
