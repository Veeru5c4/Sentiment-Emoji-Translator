from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from .db import Base


class AnalysisResultORM(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    input_text = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    sentiment = Column(String(16), nullable=False)
    highlights_json = Column(Text, nullable=False)


