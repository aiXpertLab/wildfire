from functools import lru_cache
from app.haystack.rag.pgvector_service import PgVectorSearchService


@lru_cache()
def get_pgvector_service() -> PgVectorSearchService:
    service = PgVectorSearchService()
    service.initialize()
    return service
