import os
import json
import re

from intelligence.prompt import build_dashboard_prompt


GEMINI_MODEL = "gemini-2.5-flash"


SECTION_ALIASES = {
    "platform_intelligence": ["platform", "platform_intelligence", "platform_watch"],
    "ai_technology": ["ai", "ai_technology", "ai_watch"],
    "sports_outdoor": ["sports", "sports_outdoor", "sports_and_outdoor"],
    "retail_innovation": ["retail", "retail_innovation", "retail_trends", "retail_watch"],
}


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
        return normalize_dashboard_data(json.loads(text))
    except json.JSONDecodeError:
        extracted = _extract_json_object(text)
        if extracted:
            try:
                return normalize_dashboard_data(json.loads(extracted))
            except json.JSONDecodeError:
                pass
        return build_dashboard_fallback(raw_text)


def normalize_dashboard_data(data):
    normalized = {
        "date": data.get("date", ""),
        "headline": data.get("headline") or data.get("one_thing_worth_watching") or "今日信号已更新",
        "platform_intelligence": _normalize_cards(_first_section(data, "platform_intelligence")),
        "ai_technology": _normalize_cards(_first_section(data, "ai_technology")),
        "sports_outdoor": _normalize_cards(_first_section(data, "sports_outdoor")),
        "retail_innovation": _normalize_cards(_first_section(data, "retail_innovation")),
        "one_thing_worth_watching": data.get("one_thing_worth_watching") or data.get("headline") or "今日信号已更新",
    }
    if data.get("parse_warning"):
        normalized["parse_warning"] = data["parse_warning"]
    return normalized


def _first_section(data, canonical_key):
    for key in SECTION_ALIASES[canonical_key]:
        if data.get(key):
            return data[key]
    return []


def _normalize_cards(items):
    cards = []
    for item in items[:6]:
        if isinstance(item, str):
            cards.append(
                {
                    "name": "Signal",
                    "news": _shorten(item, 90),
                    "why_this_matters": "该信号值得进一步阅读原文确认。",
                    "trend": "Signal",
                    "link": "",
                }
            )
            continue

        cards.append(
            {
                "name": item.get("name") or item.get("platform") or item.get("topic") or "Signal",
                "news": _shorten(item.get("news") or item.get("signal") or "", 90),
                "why_this_matters": _shorten(item.get("why_this_matters") or item.get("why") or "", 110),
                "trend": item.get("trend") or "Trend",
                "link": item.get("link") or "",
            }
        )
    return cards


def build_dashboard_fallback(raw_text):
    text = re.sub(r"\s+", " ", raw_text).strip()
    fallback_signal = text[:160] if text else "今日外部信号已更新，但结构化解析失败。"
    return {
        "date": "",
        "headline": "今日外部信号已更新",
        "platform_intelligence": [
            {
                "name": "Signal",
                "news": fallback_signal[:90],
                "why_this_matters": "Gemini 返回内容未能解析为标准 JSON，已保留核心文本。",
                "trend": "JSON fallback",
                "link": "",
            }
        ],
        "ai_technology": [],
        "sports_outdoor": [],
        "retail_innovation": [],
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


def _shorten(text, limit):
    text = re.sub(r"\s+", " ", str(text)).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"
