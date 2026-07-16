import feedparser

from config import (
    EXCLUDED_KEYWORDS,
    EXCLUSION_OVERRIDE_KEYWORDS,
    HIGH_RELEVANCE_KEYWORDS,
    LOW_VALUE_KEYWORDS,
    RSS_ITEMS_PER_FEED,
    SIGNAL_KEYWORDS,
)
from sources.common import make_item, parse_date, should_keep_auto_item


def fetch_rss_items(feeds):
    items = []

    for feed_config in feeds:
        source = feed_config["source"]
        domain = feed_config.get("domain", "retail")
        parsed_feed = feedparser.parse(feed_config["url"])

        for entry in parsed_feed.entries[:RSS_ITEMS_PER_FEED]:
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
                    source=source,
                    title=title,
                    summary=summary,
                    link=entry.get("link", ""),
                    published_date=parse_date(entry),
                    domain=domain,
                    origin_type="rss",
                    priority=1,
                )
            )

    return items
