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
    # route = result["messages"][2]._content[0].tool_name if result["messages"][2]._content else "openai"
    # KNOWN_TOOLS = ["sql_search_tool", "semantics_search_tool", "web_search_tool"]
    KNOWN_TOOLS = ["sql_search", "internal_search", "web_search"]

    messages_str = str(result["messages"])
    route = next((t for t in KNOWN_TOOLS if t in messages_str), "LLM Knowledge")
    
    last_msg = result["last_message"]

    if hasattr(last_msg, "content") and last_msg.content:
        answer_text = last_msg.content[0].text
    else:
        answer_text = str(last_msg)


    return {
        "query": request.query,
        "route": route,
        "answer": answer_text,
    }
