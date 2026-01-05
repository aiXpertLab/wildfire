# tools/embedding_tool.py
from haystack.nodes import BaseComponent
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import EmbeddingRetriever

class EmbeddingSearchTool(BaseComponent):
    outgoing_edges = 1

    def __init__(self, document_store: FAISSDocumentStore, top_k: int = 5):
        self.retriever = EmbeddingRetriever(document_store=document_store, embedding_model="all-MiniLM-L6-v2")
        self.top_k = top_k

    def run(self, query: str) -> dict:
        docs = self.retriever.retrieve(query, top_k=self.top_k)
        return {"result": [doc.content for doc in docs]}
