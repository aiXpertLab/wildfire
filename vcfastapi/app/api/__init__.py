from fastapi import APIRouter, Depends

from app.api.default import rouDefault


rou = APIRouter()

rou.include_router(rouDefault, prefix="", tags=["default"])