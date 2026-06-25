import os
import requests
import feedparser
from datetime import datetime

WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")

FEEDS = {
    "Retail Dive": "https://www.retaildive.com/feeds/news/",
    "SportsPro": "https://www.sportspro.com/feed/",
    "SportBusiness": "https://www.sportbusiness.com/feed/",
    "WWD Business": "https://wwd.com/business-news/feed/",
}

KEYWORDS = [
    "retail", "sports", "sporting goods", "ecommerce", "e-commerce",
    "nike", "adidas", "decathlon", "lululemon", "puma",
    "outdoor", "fitness", "store", "consumer", "brand"
]

def fetch_news():
    results = []

    for source, url in FEEDS.items():
        feed = feedparser.parse(url)

        for entry in feed.entries[:8]:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "")

            text = f"{title} {summary}".lower()

            if any(keyword.lower() in text for keyword in KEYWORDS):
                results.append({
                    "source": source,
                    "title": title,
                    "link": link
                })

    return results[:10]

def send_to_feishu(text):
    payload = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    print(response.status_code)
    print(response.text)

def format_message(news):
    today = datetime.now().strftime("%Y-%m-%d")

    if not news:
        return f"🏃 体育零售行业日报 | {today}\n\n今天暂时没有抓到匹配新闻。"

    lines = [f"🏃 体育零售行业日报 | {today}\n"]

    for i, item in enumerate(news, 1):
        lines.append(
            f"{i}. 【{item['source']}】{item['title']}\n{item['link']}\n"
        )

    return "\n".join(lines)

if __name__ == "__main__":
    news = fetch_news()
    message = format_message(news)
    send_to_feishu(message)
