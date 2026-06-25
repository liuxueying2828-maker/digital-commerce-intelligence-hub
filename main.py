import os
import requests
import feedparser
from datetime import datetime

FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
                    "summary": summary,
                    "link": link
                })

    return results[:12]

def summarize_with_gemini(news):
    news_text = "\n\n".join([
        f"Source: {item['source']}\nTitle: {item['title']}\nSummary: {item['summary']}\nLink: {item['link']}"
        for item in news
    ])

    prompt = f"""
You are a sports retail industry analyst.

Please create a bilingual Chinese-English morning brief based on the following news.

Requirements:
1. Select the top 5 most relevant stories.
2. Keep the original English title.
3. Write a natural Chinese summary for each story.
4. Add a short "Why it matters for Decathlon" insight in Chinese.
5. End with a 3-bullet trend summary in Chinese.
6. Keep the tone concise, professional, and business-oriented.

News:
{news_text}
"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        url,
        params={"key": GEMINI_API_KEY},
        json=payload,
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    return data["candidates"][0]["content"]["parts"][0]["text"]

def send_to_feishu(text):
    payload = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }

    response = requests.post(FEISHU_WEBHOOK_URL, json=payload, timeout=30)
    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    news = fetch_news()

    if not news:
        message = f"🏃 Sports Retail Intelligence Brief | {today}\n\n今天没有抓到相关新闻。"
    else:
        ai_summary = summarize_with_gemini(news)
        message = f"🏃 Sports Retail Intelligence Brief | {today}\n\n{ai_summary}"

    send_to_feishu(message)
