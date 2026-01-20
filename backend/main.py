from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .db import Base, engine, is_db_enabled
from .routers.analysis import router as analysis_router


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="AI Summary & Sentiment/Emoji Translator",
        version="1.0.0",
    )

    # CORS so Streamlit frontend can call the API
    origins = []
    if settings.frontend_origin:
        origins.append(settings.frontend_origin)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(analysis_router)

    # Initialize DB if configured
    if is_db_enabled() and engine is not None:
        logger.info("Creating database tables (if not present)...")
        Base.metadata.create_all(bind=engine)
    else:
        logger.warning("DATABASE_URL not set – running without Postgres persistence.")

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()


