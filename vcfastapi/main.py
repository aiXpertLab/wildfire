from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.db_async import async_engine
from app.api import rou

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with async_engine.begin() as conn: pass
        yield
    finally:
        await async_engine.dispose()
        
app = FastAPI(
    title="Wildfire",
    description="When Wildfire meets Haystack",
    version="1.0.0",
)


app.include_router(rou)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
