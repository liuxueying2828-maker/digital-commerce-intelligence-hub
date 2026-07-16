import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape


TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def clean_text(value):
    if not value:
        return ""
    text = TAG_RE.sub(" ", str(value))
    text = unescape(text)
    return SPACE_RE.sub(" ", text).strip()


def parse_date(entry):
    date_value = (
        entry.get("published")
        or entry.get("updated")
        or entry.get("created")
        or entry.get("pubDate")
    )
    if not date_value:
        return None

    try:
        parsed = parsedate_to_datetime(date_value)
        if parsed and not parsed.tzinfo:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except (TypeError, ValueError, IndexError, OverflowError):
        return None


def iso_date(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value or ""


def contains_signal_keyword(title, summary, keywords):
    text = f"{title} {summary}".lower()
    return any(keyword.lower() in text for keyword in keywords)


def make_item(
    source,
    title,
    summary,
    link="",
    published_date=None,
    domain="Retail & Commerce",
    origin_type="rss",
    priority=1,
):
    return {
        "source": source,
        "title": clean_text(title),
        "summary": clean_text(summary),
        "link": link or "",
        "published_date": iso_date(published_date),
        "domain": domain,
        "origin_type": origin_type,
        "priority": priority,
    }


def text_contains_any(text, keywords):
    lower_text = text.lower()
    return any(keyword.lower() in lower_text for keyword in keywords)


def should_keep_auto_item(title, summary, signal_keywords, excluded_keywords, override_keywords, low_value_keywords, high_relevance_keywords):
    text = f"{title} {summary}"
    if not text_contains_any(text, signal_keywords):
        return False

    has_override = text_contains_any(text, override_keywords)
    if text_contains_any(text, excluded_keywords) and not has_override:
        return False

    has_high_relevance = text_contains_any(text, high_relevance_keywords)
    if text_contains_any(text, low_value_keywords) and not has_high_relevance:
        return False

    return True
