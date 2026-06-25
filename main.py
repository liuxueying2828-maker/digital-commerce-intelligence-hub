import os
import requests
import feedparser
from datetime import datetime
from google import genai

FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

FEEDS = {
    "Retail Dive": "https://www.retaildive.com/feeds/news/",
    "Retail TouchPoints": "https://www.retailtouchpoints.com/feed/",
    "Modern Retail": "https://www.modernretail.co/feed/",
    "SportsPro": "https://www.sportspro.com/feed/",
    "SportBusiness": "https://www.sportbusiness.com/feed/",
    "Front Office Sports": "https://frontofficesports.com/feed/",
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
你是一名服务于迪卡侬中国数字化与电商团队的体育零售行业情报分析师。

请基于以下新闻，生成一份中文为主、保留英文标题的行业情报简报。

重要规则：
- 不要输出日期。
- 不要输出大标题。
- 不要寒暄。
- 不要介绍自己。
- 不要使用 Markdown 标题符号，例如 ##、###、**。
- 不要编造新闻中没有的信息。
- 如果新闻与体育零售、电商、门店、品牌、会员、零售媒体、运动消费、供应链、户外、健身、运动品牌相关性不强，可以忽略。
- 最多选择 5 条最值得关注的新闻。
- 按重要性从高到低排序。

输出格式必须严格遵循：

🔥 今日重点新闻

━━━━━━━━━━━━━━━━━━

① 英文原标题
重要性：★★★★★
来源：Source Name

🇨🇳 中文摘要：
用 60-90 字概括新闻核心内容，重点说明发生了什么、涉及哪个公司、为什么值得关注。

💡 对迪卡侬的启示：
用 50-80 字说明这条新闻对迪卡侬中国在电商、会员、门店数字化、品牌营销、供应链或零售创新上的潜在启发。

🔗 Link:
新闻链接

━━━━━━━━━━━━━━━━━━

重复以上格式，最多 5 条。

📈 今日行业趋势

1. 用一句话总结趋势一。
2. 用一句话总结趋势二。
3. 用一句话总结趋势三。

🎯 建议关注动作

1. 给迪卡侬中国数字化/电商团队一个具体可关注动作。
2. 给第二个具体可关注动作。
3. 给第三个具体可关注动作。

以下是新闻素材：

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
        message = f"""==================================================
Sports Retail Intelligence Brief
Date: {today}
==================================================

今天没有抓到相关新闻。
"""
    else:
        ai_summary = summarize_with_gemini(news)
        message = f"""==================================================
Sports Retail Intelligence Brief
Date: {today}
==================================================

{ai_summary}
"""

    send_to_feishu(message)
