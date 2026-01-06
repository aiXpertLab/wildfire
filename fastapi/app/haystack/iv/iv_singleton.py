from functools import lru_cache
from app.haystack.iv.iv_search_service import IVService


# @lru_cache()
def get_ivservice() -> IVService:
    ivService = IVService()
    ivService.initialize()
    return ivService
