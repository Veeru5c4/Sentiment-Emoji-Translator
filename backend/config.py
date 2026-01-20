import os
from functools import lru_cache
from pydantic import BaseModel


class Settings(BaseModel):
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    # Optional: project-level key; users can also paste their own key via UI
    openai_project_key: str | None = os.getenv("OPENAI_PROJECT_KEY")

    # Optional Postgres URL; if not provided, persistence is disabled
    database_url: str | None = os.getenv("DATABASE_URL")

    # CORS / frontend
    frontend_origin: str | None = os.getenv("FRONTEND_ORIGIN", "http://localhost:8501")


@lru_cache
def get_settings() -> Settings:
    return Settings()


