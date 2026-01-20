from __future__ import annotations

import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import get_db, is_db_enabled
from ..models import AnalysisResultORM
from ..openai_client import analyze_text_with_openai
from ..schemas import AnalysisRequest, AnalysisResult


router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze", response_model=AnalysisResult)
def analyze_text(
    payload: AnalysisRequest,
    db: Annotated[Session | None, Depends(get_db)] = None,
) -> AnalysisResult:
    """
    Analyze user text: return four-line summary, sentiment, and emoji highlights.
    Optionally persists the result to Postgres if configured.
    """
    try:
        result = analyze_text_with_openai(text=payload.text, api_key=payload.api_key)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    # Persist to Postgres if DB is enabled
    if is_db_enabled() and db is not None:
        orm_obj = AnalysisResultORM(
            input_text=payload.text,
            summary=result.summary,
            sentiment=result.sentiment,
            highlights_json=json.dumps([h.model_dump() for h in result.highlights]),
        )
        db.add(orm_obj)
        db.commit()

    return result


