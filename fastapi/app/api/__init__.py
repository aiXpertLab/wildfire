from fastapi import APIRouter, Depends


# from app.api.v1 import r_root, system_setup, biz_setup
# from app.api.v2 import v2Router
# from app.api.v6 import v6Router
# from app.api.v7 import v7Router
# from app.api.vm import vmRouter
# from app.api.r_rag import ragRou
# from app.api.r_report import reportRou
# from app.api.r_invoice import invRou
from app.api.rou_hs_agent import hsRouAgent
from app.api.rou_hs_rag import hsRouRag
from app.api.rou_hs_sql import hsRouSQL

rou = APIRouter()

# rou.include_router(userRou)
rou.include_router(hsRouRag, prefix="/rag", tags=["Haystack"])
rou.include_router(hsRouAgent, prefix="/agent", tags=["Haystack"])
rou.include_router(hsRouSQL, prefix="/sql", tags=["Haystack"])
# rou.include_router(invRou, prefix="/invoice", tags=["Invoice"])
# rou.include_router(reportRou, prefix="/reports", tags=["Reports"])
# rou.include_router(syncRouter)
# rou.include_router(erpRouter)
# rou.include_router(vmRouter)
# rou.include_router(ocrRouter)
# rou.include_router(v2Router)
# rou.include_router(r_root.router, tags=["Root"], dependencies=[Depends(authent)])
# rou.include_router(system_setup.router, prefix="/system_setup",tags=["System Setup"], dependencies=[Depends(authent)])
# rou.include_router(biz_setup.router,prefix="/biz_setup",tags=["BizEntity Setup"], dependencies=[Depends(authent)],)
