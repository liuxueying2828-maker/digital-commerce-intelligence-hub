from urllib.parse import quote_plus

import feedparser

from config import FILTER_PROFILES, GOOGLE_NEWS_ITEMS_PER_QUERY
from sources.common import make_item, parse_date, should_keep_section_item


GOOGLE_NEWS_RSS_URL = (
    "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
)


def fetch_google_news_items(search_queries):
    items = []

    for section, queries in _iter_section_queries(search_queries):
        profile = FILTER_PROFILES[section]
        for query in queries:
            url = GOOGLE_NEWS_RSS_URL.format(query=quote_plus(query))
            parsed_feed = feedparser.parse(url)

            for entry in parsed_feed.entries[:GOOGLE_NEWS_ITEMS_PER_QUERY]:
                title = entry.get("title", "")
                summary = entry.get("summary", "") or entry.get("description", "")

                if not should_keep_section_item(title=title, summary=summary, profile=profile):
                    continue

                items.append(
                    make_item(
                        source=f"Google News: {query}",
                        title=title,
                        summary=summary,
                        link=entry.get("link", ""),
                        published_date=parse_date(entry),
                        domain=section,
                        origin_type="google_news",
                        priority=2,
                    )
                )

    return items


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
