from urllib.parse import quote_plus

import feedparser

from config import (
    FILTER_PROFILES,
    GOOGLE_NEWS_ITEMS_PER_QUERY,
    MAX_SECTION_CANDIDATES,
    MIN_SECTION_CANDIDATES,
    SEARCH_WINDOWS_DAYS,
)
from sources.common import make_item, parse_date, should_keep_section_item


GOOGLE_NEWS_RSS_URL = (
    "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
)


def fetch_google_news_items(search_queries):
    items = []

    for section, queries in _iter_section_queries(search_queries):
        items.extend(_fetch_section_items(section, queries))

    return items


def _fetch_section_items(section, queries):
    profile = FILTER_PROFILES.get(section)
    if not profile:
        return []

    section_items = []
    seen = set()
    minimum = MIN_SECTION_CANDIDATES.get(section, 2)
    maximum = MAX_SECTION_CANDIDATES.get(section, 8)

    for window_days in SEARCH_WINDOWS_DAYS:
        _collect_window_items(
            section_items=section_items,
            seen=seen,
            section=section,
            queries=queries,
            profile=profile,
            window_days=window_days,
            maximum=maximum,
        )
        if len(section_items) >= minimum:
            break

    return section_items[:maximum]


def _collect_window_items(section_items, seen, section, queries, profile, window_days, maximum):
    for query in queries:
        if len(section_items) >= maximum:
            return

        windowed_query = f"{query} when:{window_days}d"
        url = GOOGLE_NEWS_RSS_URL.format(query=quote_plus(windowed_query))
        parsed_feed = feedparser.parse(url)

        for entry in parsed_feed.entries[:GOOGLE_NEWS_ITEMS_PER_QUERY]:
            title = entry.get("title", "")
            summary = entry.get("summary", "") or entry.get("description", "")

            if not should_keep_section_item(title=title, summary=summary, profile=profile):
                continue

            dedupe_key = _dedupe_key(title, entry.get("link", ""))
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)

            section_items.append(
                make_item(
                    source=f"Google News: {query}",
                    title=title,
                    summary=summary,
                    link=entry.get("link", ""),
                    published_date=parse_date(entry),
                    domain=section,
                    origin_type="google_news",
                    priority=2,
                    search_window_days=window_days,
                )
            )

            if len(section_items) >= maximum:
                return


def _dedupe_key(title, link):
    normalized_title = " ".join(str(title).lower().split())
    normalized_link = str(link).strip()
    return normalized_title, normalized_link


def _iter_section_queries(search_queries):
    if isinstance(search_queries, dict):
        for section, queries in search_queries.items():
            yield section, queries
        return

    # Backward compatibility with old [{query, domain}] shape.
    grouped = {}
    for query_config in search_queries:
        grouped.setdefault(query_config.get("domain", "retail"), []).append(query_config["query"])
    for section, queries in grouped.items():
        yield section, queries
