import logging
from fastapi import APIRouter
from pydantic import BaseModel
from haystack.dataclasses import ChatMessage, Document

from app.haystack.iv.iv_agent import agent

logger = logging.getLogger(__name__)
hsRouDispatch = APIRouter()


class AgentDispatchRequest(BaseModel):
    query: str
    top_k: int = 5


@hsRouDispatch.post("/iv_dispatch")
def iv_dispatch(request: AgentDispatchRequest):
    """
    Dispatch query to agent and return tool results if internal_search is used.
    """
    logger.info("-----------------User query received: %r", request.query)

    result = agent.run(
        messages=[ChatMessage.from_user(request.query)]
    )
    
    logger.info("Tool logs count: %d", len(result.get("tool_logs", [])))
    logger.info("==============: %s", result)

    tool_logs = result.get("tool_logs", [])

    internal_docs: list[Document] = []

    for log in tool_logs:
        logger.info("Tool invoked: %s", log.get("tool_name"))
        logger.info("Tool input: %s", log.get("tool_input"))

        if log.get("tool_name") == "internal_search":
            tool_output = log.get("tool_output", {})
            internal_docs = tool_output.get("documents", [])

    # If semantic search was used, return those documents
    if internal_docs:
        logger.info("Internal search returned %d documents", len(internal_docs))

        return {
            "query": request.query,
            "tool": "internal_search",
            "count": len(internal_docs),
            "results": [
                {
                    "id": d.id,
                    "score": getattr(d, "score", None),
                    "content": d.content,
                    "meta": d.meta,
                }
                for d in internal_docs
            ],
        }

    # Fallback: agent did not use internal search
    logger.info("No internal search used by agent")

    return {
        "query": request.query,
        "tool": "none",
        "answer": result["last_message"].text,
    }
