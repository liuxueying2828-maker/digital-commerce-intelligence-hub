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
你是一名服务于迪卡侬中国数字化与电商团队的体育零售行业情报分析师，也是一位具有10年以上体育零售行业经验的战略咨询顾问。

你的读者是迪卡侬中国总部数字化、电商、CRM、会员、产品及业务负责人。

他们只有3分钟时间阅读新闻，所以你不是总结新闻，而是帮助他们快速判断：
1. 今天最值得关注什么？
2. 为什么值得关注？
3. 对迪卡侬意味着什么？
4. 是否需要采取行动？

请基于以下新闻，生成一份中文为主、保留英文标题的行业情报简报。

重要规则：
- 不要输出日期。
- 不要输出大标题。
- 不要寒暄。
- 不要介绍自己。
- 不要使用 Markdown 标题符号，例如 ##、###、**。
- 不要编造新闻中没有的信息。
- 如果新闻与体育零售、电商、门店、品牌、会员、零售媒体、运动消费、供应链、户外、健身、运动品牌相关性不强，可以忽略。
- 最多选择5条新闻。
- 如果当天高价值新闻较少，可以少于5条，不要为了凑满5条而输出低价值新闻。
- 按重要性从高到低排序。
- 整个日报控制在1200字以内。

优先选择：
- 行业重大事件
- 品牌战略变化
- AI与数字化
- 电商创新
- 门店创新
- CRM和会员
- 零售媒体
- 供应链
- 消费趋势

忽略：
- 单纯产品发布
- 一般营销活动
- 与体育零售关系较弱的新闻

评分标准：
★★★★★ 表示行业重大变化、可能影响体育零售行业或未来1-3年趋势。
★★★★☆ 表示重要品牌动作，值得学习或持续关注。
★★★☆☆ 表示一般行业资讯，了解即可。
不要全部评为五星。

输出格式必须严格遵循：

🔥 今日重点新闻

────────────

① 英文原标题
重要性：★★★★☆
来源：Source Name

🇨🇳 中文摘要：
用60-80字概括新闻核心内容，说明发生了什么、涉及哪个公司、为什么值得关注。

💡 Business Impact：
用50-60字说明这条新闻对迪卡侬中国在电商、会员、门店数字化、品牌营销、供应链或零售创新上的潜在启发。不要只是重复新闻内容。

🔗 Link:
新闻链接

────────────

重复以上格式，最多5条。

📈 Today's Signals

不要重复新闻。

请综合今天所有新闻，提炼出背后的行业信号（Industry Signals）。

例如：
Retail Media持续增长
AI开始进入门店运营
会员价值进一步提升
零售商持续建设广告能力
运动消费进一步大众化

要求：
- 输出3条
- 每条15-20字
- 不是新闻总结，而是行业趋势
- 如果多条新闻表达的是同一个趋势，只保留一次

🎯 Action Items

请基于今天新闻，为迪卡侬中国数字化/电商团队提出3条可执行建议。

要求：

- 必须具体。
- 必须可以在未来1-3个月启动。
- 每条一句话。
- 不要空话。
- 不要写"持续关注"、"继续观察"、"保持关注"。

优秀示例：

✔ 评估Retail Media能力建设
✔ 调研Hyrox合作机会
✔ 建立AI客服试点
✔ 跟踪Nike会员战略变化
✔ 调研AI商品推荐能力
✔ 建立门店AI运营试点

避免：

✘ 持续关注市场变化
✘ 密切关注行业动态
✘ 加强数字化建设
✘ 提升用户体验

Business Impact不是新闻摘要。

请重点分析：

• 为什么这件事值得迪卡侬关注？
• 是否说明行业正在发生变化？
• 是否值得迪卡侬学习？
• 是否可能影响未来竞争？

不要重复摘要内容。

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
        message = f"""
Sports Retail Intelligence Brief
Date: {today}

今天没有抓到相关新闻。
"""
    else:
        ai_summary = summarize_with_gemini(news)
        message = f"""
Sports Retail Intelligence Brief
Date: {today}

{ai_summary}
"""

    send_to_feishu(message)
