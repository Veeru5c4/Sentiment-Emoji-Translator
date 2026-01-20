from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from .config import get_settings


settings = get_settings()

Base = declarative_base()

engine = None
SessionLocal: sessionmaker[Session] | None = None

if settings.database_url:
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def is_db_enabled() -> bool:
    return engine is not None and SessionLocal is not None


@contextmanager
def get_db() -> Iterator[Session]:
    """
    FastAPI dependency / context manager for DB sessions.
    Raises RuntimeError if DATABASE_URL is not configured.
    """

    if not is_db_enabled():
        raise RuntimeError(
            "DATABASE_URL is not configured – Postgres persistence is disabled."
        )

    db = SessionLocal()  # type: ignore[call-arg]
    try:
        yield db
    finally:
        db.close()


