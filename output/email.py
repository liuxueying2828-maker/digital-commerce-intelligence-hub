import os
from datetime import datetime

import requests

from output.html import safe_text


RESEND_API_URL = "https://api.resend.com/emails"
DEFAULT_EMAIL_FROM = "Digital Commerce Intelligence <onboarding@resend.dev>"


SECTIONS = [
    ("Platform Intelligence", "platform_intelligence", "standard"),
    ("AI Technology", "ai_technology", "ai"),
    ("Sports & Outdoor", "sports_outdoor", "standard"),
    ("Retail Innovation", "retail_innovation", "standard"),
]


def send_brief_email(data, dashboard_url=""):
    api_key = os.getenv("EMAIL_API_KEY")
    email_to = os.getenv("EMAIL_TO")
    if not api_key:
        raise RuntimeError("Missing EMAIL_API_KEY environment variable.")
    if not email_to:
        raise RuntimeError("Missing EMAIL_TO environment variable.")

    brief_date = safe_text(data.get("date") or datetime.now().strftime("%Y-%m-%d"))
    payload = {
        "from": os.getenv("EMAIL_FROM") or DEFAULT_EMAIL_FROM,
        "to": _split_recipients(email_to),
        "subject": f"Digital Commerce Intelligence Brief - {brief_date}",
        "text": build_email_body(data, dashboard_url),
    }

    response = requests.post(
        RESEND_API_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    print(f"Email response: {response.status_code} {response.text}")


def build_email_body(data, dashboard_url=""):
    lines = [
        "Digital Commerce Intelligence Brief",
        f"Date: {safe_text(data.get('date') or datetime.now().strftime('%Y-%m-%d'))}",
        "",
        "Today's Focus",
        safe_text(data.get("headline") or data.get("one_thing_worth_watching") or "No reliable signal returned."),
    ]

    for title, key, section_type in SECTIONS:
        lines.extend(["", title])
        cards = data.get(key, []) or []
        if not cards:
            lines.append("No reliable signal returned from real sources.")
            continue

        for index, card in enumerate(cards, start=1):
            lines.extend(_format_card(index, card, section_type))

    if dashboard_url:
        lines.extend(["", f"Dashboard: {safe_text(dashboard_url)}"])

    return "\n".join(safe_text(line) for line in lines).strip() + "\n"


def _format_card(index, card, section_type):
    if not isinstance(card, dict):
        return [f"{index}. News: {safe_text(card)}", "   Why this matters: ", "   Trend: "]

    if section_type == "ai":
        news = card.get("capability") or card.get("news") or ""
        why = card.get("industry_impact") or card.get("why_this_matters") or ""
    else:
        news = card.get("news") or ""
        why = card.get("why_this_matters") or ""

    return [
        f"{index}. News: {safe_text(news)}",
        f"   Why this matters: {safe_text(why)}",
        f"   Trend: {safe_text(card.get('trend') or '')}",
    ]


def _split_recipients(value):
    recipients = [item.strip() for item in value.replace(";", ",").split(",")]
    return [item for item in recipients if item]
