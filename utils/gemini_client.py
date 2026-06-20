"""
TruthLens AI 2.0 — Gemini API Client
Built on the modern `google-genai` SDK (replaces the deprecated
`google.generativeai` package).
"""
import json
from google import genai
from google.genai import types
from utils.config import GEMINI_API_KEY, GEMINI_MODEL

_client = None


def get_client() -> genai.Client:
    """Return a cached Gemini client instance."""
    global _client
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set. Add it to your .env file.")
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def call_gemini(prompt: str, image_bytes: bytes = None, mime_type: str = "image/jpeg") -> str:
    """
    Send a prompt (optionally + image) to Gemini and return raw text response.
    """
    client = get_client()
    contents = []
    if image_bytes:
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
    contents.append(prompt)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
    )
    return (response.text or "").strip()


def call_gemini_json(prompt: str, image_bytes: bytes = None, mime_type: str = "image/jpeg") -> dict:
    """
    Call Gemini and parse a JSON response.

    Uses `response_mime_type="application/json"` so Gemini returns clean
    JSON directly (no markdown fences), with a fallback fence-stripper for
    older-style responses just in case.
    """
    client = get_client()
    contents = []
    if image_bytes:
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
    contents.append(prompt)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3,
        ),
    )

    raw = (response.text or "").strip()

    # Defensive fence-stripping, in case the model wraps output anyway
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)
