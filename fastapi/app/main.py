from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import get_settings_singleton
from app.core.logging import setup_logger
from app.db.db_async import async_engine as engine
from app.api import rou

setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            pass
        yield
    finally:
        await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings_singleton()
    print("--------------DB URL USED:", settings.PG_ASYNC)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # app.state.settings = settings

    # CORS
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=settings.ALLOWED_ORIGINS,
        # allow_credentials=True,
        allow_origins=["*"],
        allow_credentials=False,  # MUST be False when origins="*"
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(rou)

    return app