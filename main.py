from datetime import datetime
import os

from config import (
    HTML_OUTPUT_PATH,
    MAX_ITEMS_FOR_GEMINI,
    MIN_SECTION_CANDIDATES,
    PROJECT_NAME,
    SECTION_ORDER,
)


def collect_information_pool():
    from config import FEEDS, MANUAL_INPUT_PATH, SEARCH_QUERIES
    from sources.google_news import fetch_google_news_items
    from sources.manual import fetch_manual_items
    from sources.rss import fetch_rss_items

    items = []
    items.extend(fetch_manual_items(MANUAL_INPUT_PATH))
    items.extend(fetch_rss_items(FEEDS))
    items.extend(fetch_google_news_items(SEARCH_QUERIES))
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

    section_rank = {section: index for index, section in enumerate(SECTION_ORDER)}
    cleaned_items.sort(
        key=lambda item: (
            item.get("priority", 1),
            -section_rank.get(item.get("domain", "retail"), len(section_rank)),
            -(item.get("search_window_days") or 0),
            item.get("published_date", ""),
        ),
        reverse=True,
    )

    selected_items = []
    selected_keys = set()

    for section in SECTION_ORDER:
        minimum = MIN_SECTION_CANDIDATES.get(section, 0)
        section_items = [item for item in cleaned_items if item.get("domain") == section]
        for item in section_items[:minimum]:
            key = (item.get("title", "").lower(), item.get("link", "").strip())
            if key in selected_keys:
                continue
            selected_keys.add(key)
            selected_items.append(item)

    for item in cleaned_items:
        if len(selected_items) >= limit:
            break
        key = (item.get("title", "").lower(), item.get("link", "").strip())
        if key in selected_keys:
            continue
        selected_keys.add(key)
        selected_items.append(item)

    return selected_items[:limit]


def build_empty_message():
    today = datetime.now().strftime("%Y-%m-%d")
    return (
        f"{PROJECT_NAME}\n"
        f"Date: {today}\n\n"
        "本期信息源未返回可用于分析的 DTC / Digital Commerce 情报。"
    )


def build_empty_dashboard_data():
    today = datetime.now().strftime("%Y-%m-%d")
    return {
        "date": today,
        "headline": "本期信息源未返回高置信度外部情报",
        "platform_intelligence": [],
        "ai_technology": [],
        "sports_outdoor": [],
        "retail_innovation": [],
        "one_thing_worth_watching": "本期信息源未返回高置信度外部情报，页面已正常更新。",
    }


def build_dashboard_notification(data, page_url):
    headline = data.get("headline") or data.get("one_thing_worth_watching") or "今日信号已更新"
    return (
        "Digital Commerce Intelligence 已更新\n"
        f"今日重点：{headline}\n"
        f"查看完整页面：{page_url}"
    )


def get_dashboard_url():
    return (
        os.getenv("DASHBOARD_URL")
        or os.getenv("PAGES_URL")
        or "output/index.html"
    )


def main():
    from intelligence.gemini import generate_dashboard_data
    from output.archive import save_dashboard_history
    from output.html import render_dashboard
    from output.feishu import send_text_message

    information_pool = collect_information_pool()
    page_url = get_dashboard_url()

    if not information_pool:
        dashboard_data = build_empty_dashboard_data()
        render_dashboard(dashboard_data, HTML_OUTPUT_PATH)
        save_dashboard_history(dashboard_data, HTML_OUTPUT_PATH.parent)
        send_text_message(build_dashboard_notification(dashboard_data, page_url))
        return

    dashboard_data = generate_dashboard_data(information_pool)
    render_dashboard(dashboard_data, HTML_OUTPUT_PATH)
    save_dashboard_history(dashboard_data, HTML_OUTPUT_PATH.parent)
    send_text_message(build_dashboard_notification(dashboard_data, page_url))


if __name__ == "__main__":
    main()
