import feedparser

from config import RSS_ITEMS_PER_FEED, SIGNAL_KEYWORDS
from sources.common import contains_signal_keyword, make_item, parse_date


def fetch_rss_items(feeds):
    items = []

    for feed_config in feeds:
        source = feed_config["source"]
        domain = feed_config.get("domain", "Retail & Commerce")
        parsed_feed = feedparser.parse(feed_config["url"])

        for entry in parsed_feed.entries[:RSS_ITEMS_PER_FEED]:
            title = entry.get("title", "")
            summary = entry.get("summary", "") or entry.get("description", "")

            if not contains_signal_keyword(title, summary, SIGNAL_KEYWORDS):
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
