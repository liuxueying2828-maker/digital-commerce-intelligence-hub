import os
import json
import re

from intelligence.prompt import build_dashboard_prompt


GEMINI_MODEL = "gemini-2.5-flash"


def generate_dashboard_data(items):
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError(
            "Missing google-genai package. Run: python3 -m pip install -r requirements.txt"
        ) from exc

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY environment variable.")

    prompt = build_dashboard_prompt(items)
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    raw_text = response.text.strip()
    return parse_dashboard_json(raw_text)


def parse_dashboard_json(raw_text):
    text = _strip_json_fence(raw_text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        extracted = _extract_json_object(text)
        if extracted:
            try:
                return json.loads(extracted)
            except json.JSONDecodeError:
                pass
        return build_dashboard_fallback(raw_text)


def build_dashboard_fallback(raw_text):
    text = re.sub(r"\s+", " ", raw_text).strip()
    fallback_signal = text[:160] if text else "今日外部信号已更新，但结构化解析失败。"
    return {
        "date": "",
        "headline": "今日外部信号已更新",
        "platform_watch": [
            {
                "platform": "Platform Watch",
                "signal": fallback_signal,
            }
        ],
        "ai_watch": [],
        "retail_watch": [],
        "one_thing_worth_watching": fallback_signal,
        "parse_warning": "Gemini JSON parse failed; rendered fallback content.",
    }


def _strip_json_fence(raw_text):
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _extract_json_object(text):
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return ""
    return text[start : end + 1]
