import os
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever

from app.config import get_settings_singleton

settings = get_settings_singleton()


class IVService:
    def __init__(self) -> None:
        self.document_store = None
        self.pipeline = None

    def initialize(self) -> None:
        os.environ.setdefault("PG_CONN_STR", settings.PG_SYNC)

        # 1️⃣ Connect to EXISTING pgvector table
        self.document_store = PgvectorDocumentStore(
            table_name="haystack_documents",
            embedding_dimension=384,
            vector_function="cosine_similarity",
            recreate_table=False,   # critical
        )

        print("DOC STORE DIM:", self.document_store.embedding_dimension)

        # 2️⃣ Build retrieval-only pipeline
        self._build_pipeline()

    def _build_pipeline(self) -> None:


        pipeline = Pipeline()

        pipeline.add_component(
            "text_embedder",
            SentenceTransformersTextEmbedder(model="all-MiniLM-L6-v2")
        )

        pipeline.add_component(
            "retriever",
            PgvectorEmbeddingRetriever(
                document_store=self.document_store
            )
        )

        pipeline.connect(
            "text_embedder.embedding",
            "retriever.query_embedding"
        )

        self.pipeline = pipeline

    def search(self, query: str, top_k: int = 5):
        result = self.pipeline.run(
            {
                "text_embedder": {"text": query},
                "retriever": {"top_k": top_k},
            }
        )

        return result["retriever"]["documents"]
