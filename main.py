from datetime import datetime

from config import (
    MAX_ITEMS_FOR_GEMINI,
    PROJECT_NAME,
)


def collect_information_pool():
    from config import FEEDS, GOOGLE_NEWS_QUERIES, MANUAL_INPUT_PATH
    from sources.google_news import fetch_google_news_items
    from sources.manual import fetch_manual_items
    from sources.rss import fetch_rss_items

    items = []
    items.extend(fetch_manual_items(MANUAL_INPUT_PATH))
    items.extend(fetch_rss_items(FEEDS))
    items.extend(fetch_google_news_items(GOOGLE_NEWS_QUERIES))
    return prepare_information_pool(items)


def prepare_information_pool(items, limit=MAX_ITEMS_FOR_GEMINI):
    cleaned_items = []
    seen = set()

    for item in items:
        title = item.get("title", "").strip()
        summary = item.get("summary", "").strip()

        if not title or not summary:
            continue

        dedupe_key = (title.lower(), item.get("link", "").strip())
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        cleaned_items.append(item)

    cleaned_items.sort(
        key=lambda item: (
            item.get("priority", 1),
            item.get("published_date", ""),
        ),
        reverse=True,
    )

    return cleaned_items[:limit]


def build_empty_message():
    today = datetime.now().strftime("%Y-%m-%d")
    return (
        f"{PROJECT_NAME}\n"
        f"Date: {today}\n\n"
        "今天没有抓到可用于分析的 DTC / Digital Commerce 信号。"
    )


def main():
    from intelligence.gemini import generate_intelligence_brief
    from output.feishu import send_text_message

    information_pool = collect_information_pool()

    if not information_pool:
        send_text_message(build_empty_message())
        return

    brief = generate_intelligence_brief(information_pool)
    send_text_message(brief)


if __name__ == "__main__":
    main()
