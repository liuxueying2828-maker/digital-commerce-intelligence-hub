import os
import requests
import feedparser
from datetime import datetime
from google import genai

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
你是一名体育零售行业分析师。请基于以下新闻，生成一份中英文行业晨报。

要求：
1. 选择最重要的 5 条新闻。
2. 每条保留英文原标题。
3. 每条写一段自然中文摘要。
4. 每条补充“对迪卡侬的启示”。
5. 最后用 3 个 bullet 总结今日行业趋势。
6. 语言简洁、专业、有 business insight。
7. 保留每条新闻链接。

新闻：
{news_text}
"""

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

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
