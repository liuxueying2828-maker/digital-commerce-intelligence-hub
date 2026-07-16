from urllib.parse import quote_plus

import feedparser

from config import (
    EXCLUDED_KEYWORDS,
    EXCLUSION_OVERRIDE_KEYWORDS,
    GOOGLE_NEWS_ITEMS_PER_QUERY,
    HIGH_RELEVANCE_KEYWORDS,
    LOW_VALUE_KEYWORDS,
    SIGNAL_KEYWORDS,
)
from sources.common import make_item, parse_date, should_keep_auto_item


GOOGLE_NEWS_RSS_URL = (
    "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
)


def fetch_google_news_items(query_configs):
    items = []

    for query_config in query_configs:
        query = query_config["query"]
        domain = query_config.get("domain", "retail")
        url = GOOGLE_NEWS_RSS_URL.format(query=quote_plus(query))
        parsed_feed = feedparser.parse(url)

        for entry in parsed_feed.entries[:GOOGLE_NEWS_ITEMS_PER_QUERY]:
            title = entry.get("title", "")
            summary = entry.get("summary", "") or entry.get("description", "")

            if not should_keep_auto_item(
                title=title,
                summary=summary,
                signal_keywords=SIGNAL_KEYWORDS,
                excluded_keywords=EXCLUDED_KEYWORDS,
                override_keywords=EXCLUSION_OVERRIDE_KEYWORDS,
                low_value_keywords=LOW_VALUE_KEYWORDS,
                high_relevance_keywords=HIGH_RELEVANCE_KEYWORDS,
            ):
                continue

            items.append(
                make_item(
                    source=f"Google News: {query}",
                    title=title,
                    summary=summary,
                    link=entry.get("link", ""),
                    published_date=parse_date(entry),
                    domain=domain,
                    origin_type="google_news",
                    priority=2,
                )
            )

    return items
