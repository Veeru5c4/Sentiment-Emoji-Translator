from __future__ import annotations

import json
from typing import Optional

from openai import OpenAI

from .config import get_settings
from .schemas import AnalysisResult


def _build_client(api_key: Optional[str]) -> OpenAI:
    """
    Build an OpenAI client using either a user-provided key or the configured key.
    """
    settings = get_settings()
    key = api_key or settings.openai_api_key or settings.openai_project_key
    if not key:
        raise RuntimeError(
            "No OpenAI API key provided. "
            "Either set OPENAI_API_KEY/OPENAI_PROJECT_KEY on the server or pass api_key in the request."
        )
    return OpenAI(api_key=key)


SYSTEM_PROMPT = (
    "You are an assistant that summarizes long texts and performs sentiment analysis.\n"
    "User will provide a long text (up to a few pages). You must reply ONLY as a JSON object with this exact shape:\n"
    "{\n"
    '  \"summary\": \"A four-line concise summary of the text.\",\n'
    '  \"sentiment\": \"positive\" | \"neutral\" | \"negative\",\n'
    "  \"highlights\": [\n"
    "    { \"sentence\": \"...\", \"emoji\": \"...\" },\n"
    "    { \"sentence\": \"...\", \"emoji\": \"...\" }\n"
    "  ]\n"
    "}\n"
    "- The summary MUST be exactly four lines, separated by newline characters.\n"
    "- The sentiment must be one of: positive, neutral, negative.\n"
    "- Choose 3-6 key sentences that most influenced your sentiment decision and pair each with a single emoji.\n"
    "- Do not include any commentary outside the JSON object."
)


def analyze_text_with_openai(text: str, api_key: Optional[str] = None) -> AnalysisResult:
    """
    Call OpenAI to analyze text and return a structured AnalysisResult.
    """
    client = _build_client(api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content or "{}"
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse OpenAI response as JSON: {exc}") from exc

    return AnalysisResult(**data)


