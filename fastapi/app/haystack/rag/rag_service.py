# app/services/rag_service.py
from datasets import load_dataset
from haystack import Document, Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import ChatPromptBuilder
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage


class RAGService:
    def __init__(self):
        self.document_store = InMemoryDocumentStore()
        self.pipeline = None

    def initialize(self) -> None:
        """
        One-time initialization:
        - load dataset
        - embed documents
        - build pipeline
        """
        self._load_documents()
        self._build_pipeline()

    def _load_documents(self) -> None:
        dataset = load_dataset("bilgeyucel/seven-wonders", split="train")

        docs = [
            Document(content=doc["content"], meta=doc["meta"])
            for doc in dataset
        ]

        doc_embedder = SentenceTransformersDocumentEmbedder(
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
        doc_embedder.warm_up()

        docs_with_embeddings = doc_embedder.run(docs)
        self.document_store.write_documents(
            docs_with_embeddings["documents"]
        )

    def _build_pipeline(self) -> None:
        text_embedder = SentenceTransformersTextEmbedder(
            model="sentence-transformers/all-MiniLM-L6-v2"
        )

        retriever = InMemoryEmbeddingRetriever(self.document_store)

        template = [
            ChatMessage.from_user(
                """
Given the following information, answer the question.

Context:
{% for document in documents %}
{{ document.content }}
{% endfor %}

Question: {{ question }}
Answer:
"""
            )
        ]

        prompt_builder = ChatPromptBuilder(template=template)

        llm = OpenAIChatGenerator(model="gpt-4o-mini")

        pipeline = Pipeline()
        pipeline.add_component("text_embedder", text_embedder)
        pipeline.add_component("retriever", retriever)
        pipeline.add_component("prompt_builder", prompt_builder)
        pipeline.add_component("llm", llm)

        pipeline.connect(
            "text_embedder.embedding", "retriever.query_embedding"
        )
        pipeline.connect("retriever", "prompt_builder")
        pipeline.connect("prompt_builder.prompt", "llm.messages")

        self.pipeline = pipeline

    def ask(self, question: str) -> str:
        if not self.pipeline:
            raise RuntimeError("RAGService not initialized")

        result = self.pipeline.run(
            {
                "text_embedder": {"text": question},
                "prompt_builder": {"question": question},
            }
        )

        return result["llm"]["replies"][0].text
