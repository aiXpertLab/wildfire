from fastapi import APIRouter
from haystack.dataclasses import ChatMessage

from app.components.iv_agent_3tools import agent
from app.schemas.haystack import QueryString

import logging
logger = logging.getLogger(__name__)

iv3Tools = APIRouter()


@iv3Tools.post("/sql_emb_google")
def iv_dispatch(request: QueryString):
    logger.info("User query received: %r", request.query)
    result = agent.run(messages=[ChatMessage.from_user(request.query)])
    route = result["messages"][2]._content[0].tool_name if result["messages"][2]._content else "openai"

    return {
        "query": request.query,
        "route": route,
        "answer": result["last_message"],
    }
