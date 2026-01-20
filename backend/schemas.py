from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Highlight(BaseModel):
    sentence: str = Field(..., description="Sentence that drove the sentiment decision.")
    emoji: str = Field(..., description="Emoji capturing the sentiment of this sentence.")


class AnalysisRequest(BaseModel):
    text: str = Field(..., description="Raw user text to analyze.")
    api_key: Optional[str] = Field(
        default=None,
        description="Optional per-request OpenAI API key; if omitted, server config/env key is used.",
    )


class AnalysisResult(BaseModel):
    summary: str = Field(..., description="Four-line concise summary of the input text.")
    sentiment: str = Field(..., description="Overall sentiment: positive, neutral, or negative.")
    highlights: List[Highlight] = Field(
        default_factory=list,
        description="Key sentences with emojis that influenced the sentiment classification.",
    )


