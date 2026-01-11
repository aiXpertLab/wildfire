from fastapi import APIRouter
from haystack.dataclasses import ChatMessage

from app.components.iv_agent_3tools import agent
from app.schemas.haystack import QueryString

import logging
logger = logging.getLogger(__name__)

iv3Tools = APIRouter()


@iv3Tools.post("/sql_emb_serp")
def iv_dispatch(request: QueryString):
    logger.info("User query received: %r", request.query)

    result = agent.run(messages=[ChatMessage.from_user(request.query)])

    # Safe/modern way to extract text
    last_msg = result.get("last_message")
    answer_text = ""
    if last_msg and hasattr(last_msg, "text"):
        answer_text = last_msg.text

    # Tool route detection (optional)
    messages_str = str(result.get("messages", []))
    KNOWN_TOOLS = ["sql_search", "internal_search", "web_search"]
    route = next((t for t in KNOWN_TOOLS if t in messages_str), "LLM Knowledge")

    return {
        "query": request.query,
        "route": route,
        "answer": answer_text,
        # optionally return full messages for debugging
        # "raw_messages": result["messages"],
    }


@iv3Tools.post("/sql_emb_serp_source")
def iv_dispatch(request: QueryString):
    logger.info("User query received: %r", request.query)

    result = agent.run(messages=[ChatMessage.from_user(request.query)])

    # Safe/modern way to extract text
    last_msg = result.get("last_message")
    answer_text = ""
    if last_msg and hasattr(last_msg, "text"):
        answer_text = last_msg.text

    # Tool route detection (optional)
    messages_str = str(result.get("messages", []))
    KNOWN_TOOLS = ["sql_search", "internal_search", "web_search"]
    route = next((t for t in KNOWN_TOOLS if t in messages_str), "LLM Knowledge")

    return {
        "query": request.query,
        "route": route,
        "answer": answer_text,
        # optionally return full messages for debugging
        "raw_messages": result["messages"],
    }
