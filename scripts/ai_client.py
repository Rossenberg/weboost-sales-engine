"""One place for AI calls: JSON chat completion + token/cost logging into api_usage."""
import json

from openai import OpenAI

from config import AI_MODEL, AI_PRICE_IN_PER_M, AI_PRICE_OUT_PER_M, OPENAI_API_KEY
from db import get_connection, now_iso

_client = None


def client() -> OpenAI:
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise SystemExit("OPENAI_API_KEY is not set in .env")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def record_usage(step: str, resp) -> None:
    usage = getattr(resp, "usage", None)
    if not usage:
        return
    tin, tout = usage.prompt_tokens or 0, usage.completion_tokens or 0
    cost = tin / 1e6 * AI_PRICE_IN_PER_M + tout / 1e6 * AI_PRICE_OUT_PER_M
    conn = get_connection()
    conn.execute(
        "INSERT INTO api_usage (created_at, step, model, input_tokens, output_tokens, cost_usd) VALUES (?, ?, ?, ?, ?, ?)",
        (now_iso(), step, AI_MODEL, tin, tout, round(cost, 6)),
    )
    conn.commit()
    conn.close()


def chat_json(prompt: str, step: str) -> dict:
    """Send a prompt that asks for a JSON object; log usage; return the parsed dict."""
    kwargs = dict(model=AI_MODEL, messages=[{"role": "user", "content": prompt}])
    try:
        resp = client().chat.completions.create(response_format={"type": "json_object"}, **kwargs)
    except Exception:
        resp = client().chat.completions.create(**kwargs)
    record_usage(step, resp)
    raw = resp.choices[0].message.content.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)
