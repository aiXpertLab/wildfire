from haystack import component
from haystack.dataclasses import Document
from app.haystack.iv.iv_singleton import get_ivservice


@component
class IVSemanticComponent:
    def __init__(self):
        # Reuse the same singleton used by FastAPI
        self.ivservice = get_ivservice()

    @component.output_types(documents=list[Document])
    def run(self, query: str, top_k: int = 5):
        documents = self.ivservice.search(
            query=query,
            top_k=top_k,
        )
        return {"documents": documents}
