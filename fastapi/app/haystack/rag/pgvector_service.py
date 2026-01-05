import os
from haystack import Document, Pipeline
from haystack.document_stores.types import DuplicatePolicy
from haystack.components.embedders import (
    SentenceTransformersTextEmbedder,
    SentenceTransformersDocumentEmbedder,
)
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from haystack_integrations.components.retrievers.pgvector import (
    PgvectorEmbeddingRetriever,
)

from app.config import get_settings_singleton

settings = get_settings_singleton()


class PgVectorSearchService:
    def __init__(self) -> None:
        self.document_store = None
        self.pipeline = None

    def initialize(self) -> None:
        os.environ.setdefault(
            "PG_CONN_STR",
            settings.PG_SYNC,
        )

        self.document_store = PgvectorDocumentStore(
            table_name="hs_pgvector_documents",
            embedding_dimension=768,
            vector_function="cosine_similarity",
            recreate_table=True,
            hnsw_index_name="hs_pgvector_hnsw_idx_01",
            keyword_index_name="hs_pgvector_kw_idx_01",
        )

        self._index_documents()
        self._build_pipeline()

    def _index_documents(self) -> None:
        documents = [
            Document(
                content="There are over 7,000 languages spoken around the world today."
            ),
            Document(
                content=(
                    "Elephants have been observed to behave in a way that indicates "
                    "a high level of self-awareness, such as recognizing themselves "
                    "in mirrors."
                )
            ),
            Document(
                content=(
                    "In certain parts of the world, like the Maldives, Puerto Rico, "
                    "and San Diego, you can witness the phenomenon of bioluminescent waves."
                )
            ),
        ]

        embedder = SentenceTransformersDocumentEmbedder()
        embedder.warm_up()

        docs_with_embeddings = embedder.run(documents)["documents"]

        self.document_store.write_documents(
            docs_with_embeddings,
            policy=DuplicatePolicy.OVERWRITE,
        )

    def _build_pipeline(self) -> None:
        pipeline = Pipeline()
        pipeline.add_component("text_embedder", SentenceTransformersTextEmbedder())
        pipeline.add_component(
            "retriever",
            PgvectorEmbeddingRetriever(document_store=self.document_store),
        )

        pipeline.connect(
            "text_embedder.embedding",
            "retriever.query_embedding",
        )

        self.pipeline = pipeline

    def search(self, query: str, top_k: int = 1) -> list[str]:
        result = self.pipeline.run(
            {
                "text_embedder": {"text": query},
                "retriever": {"top_k": top_k},
            }
        )

        return [doc.content for doc in result["retriever"]["documents"]]
