from fastapi import APIRouter, Depends

from app.api.rou_hs_agent import hsAgent
from app.api.rou_hs_rag import hsRag

from app.api.hs_sql_raw import hsSqlRaw
from app.api.hs_sql_agent_simple import hsSqlAgent
from app.api.hs_sql_agent_conditional import hsSqlAgentConditional
from app.api.hs_sql_agent_function import hsSqlAgentFunction

from app.api.rou_iv1_semantic_search import hsRouSemantic
from app.api.rou_iv2_agent_dispatch import hsRouDispatch
from app.api.rou_iv_final import hsRouSqlEmbGoogle

rou = APIRouter()

rou.include_router(hsRag, prefix="/rag", tags=["Haystack"])
rou.include_router(hsAgent, prefix="/agent", tags=["Haystack"])
rou.include_router(hsRouSemantic, prefix="/semantic_search", tags=["Haystack"])
rou.include_router(hsRouDispatch, prefix="/iv_agent_dispatch", tags=["Haystack"])
rou.include_router(hsRouSqlEmbGoogle, prefix="/iv_agent_sql_google_embedding", tags=["IV"])




rou.include_router(hsSqlRaw, prefix="/sql", tags=["Haystack_SQL"])
rou.include_router(hsSqlAgent, prefix="/sql", tags=["Haystack_SQL"])
rou.include_router(hsSqlAgentConditional, prefix="/sql", tags=["Haystack_SQL"])
rou.include_router(hsSqlAgentFunction, prefix="/sql", tags=["Haystack_SQL"])
