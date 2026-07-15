from datetime import datetime


def build_dashboard_prompt(items):
    information_pool = _format_information_pool(items)

    return f"""
你是一名服务于 Decathlon China DTC / Digital Commerce / E-commerce 团队的行业情报分析师。

项目名称：Digital Commerce Intelligence Hub

你的任务不是写日报文章，也不是替管理层做决策。你的任务是筛选新闻、解释变化、提炼趋势，并输出适合 Executive Dashboard 展示的短结构化内容。

信息来自 Unified Information Pool，可能包含 RSS、Google News 和 manual_sources/daily_input.md 中的人工输入。人工输入可能来自京东黑板报、艾瑞咨询、晚点、36Kr、极客公园、微信公众号、行业报告、Leader 或 Mentor 分享。人工输入优先级高于普通 RSS 和 Google News，但网页上不要标记“人工输入”。

请严格遵守：
- 只输出合法 JSON，不要输出 Markdown，不要输出解释文字。
- 不要编造信息池中没有的事实。
- 每条卡片只保留 News、Why this matters、Trend、Link。
- News 不超过 45 个中文字。
- Why this matters 不超过 55 个中文字，重点提炼变化，不要重复新闻。
- Trend 输出 1 个趋势判断或 2-4 个关键词。
- Link 必须使用原始文章链接；如果信息池没有链接，输出空字符串。
- 不要输出对迪卡侬意味着什么。
- 不要输出 DTC Opportunity、Recommended Actions、Possible Experiment。
- 不要建议成立团队，不要建议持续关注。
- 不要输出 Evidence 编号或长篇商业建议。
- 页面目标是让 Leader 在 3 分钟内读完。

分类要求：

1. 国内平台洞察 / Platform Intelligence
重点关注：阿里、京东、字节、腾讯、美团、拼多多、小红书，以及其事业部、新业务、供应链和服务生态变化。

2. AI 技术前沿 / AI Technology
重点关注国内外真正重要的 AI 技术新闻，包括 OpenAI、Google DeepMind、Anthropic、DeepSeek、豆包、通义、腾讯混元、Kimi、Manus、NVIDIA、Apple AI 等。
这一栏必须以技术变化为核心，例如新模型、Agent、推理能力、多模态、AI Search、Computer Use、开源模型、API、推理成本、AI 基础设施。
可以简要指出技术与商业应用的连接，但不要把普通零售商业新闻放进 AI 分类。

3. 零售趋势 / Retail Trends
重点关注：零售媒体、全渠道、会员、供应链、门店数字化、消费者变化，以及 Nike、Walmart、Costco、Sam’s Club、Lululemon、Amazon 等公司的代表性实践。

JSON schema 必须严格如下：

{{
  "date": "{datetime.now().strftime("%Y-%m-%d")}",
  "headline": "一句话概括当天最重要的整体变化，不超过 38 个中文字符",
  "platform_intelligence": [
    {{
      "name": "公司或主题名称，例如 JD / Alibaba / ByteDance",
      "news": "一句话说明发生了什么，不超过45个中文字",
      "why_this_matters": "一句话说明为什么值得关注，不超过55个中文字",
      "trend": "1个趋势判断或2-4个关键词",
      "link": "原始文章链接"
    }}
  ],
  "ai_technology": [
    {{
      "name": "公司或技术主题名称，例如 OpenAI / DeepSeek / AI Agent",
      "news": "一句话说明发生了什么，不超过45个中文字",
      "why_this_matters": "一句话说明为什么值得关注，不超过55个中文字",
      "trend": "1个趋势判断或2-4个关键词",
      "link": "原始文章链接"
    }}
  ],
  "retail_trends": [
    {{
      "name": "公司或主题名称，例如 Walmart / Membership / Retail Media",
      "news": "一句话说明发生了什么，不超过45个中文字",
      "why_this_matters": "一句话说明为什么值得关注，不超过55个中文字",
      "trend": "1个趋势判断或2-4个关键词",
      "link": "原始文章链接"
    }}
  ],
  "one_thing_worth_watching": "当天最值得持续观察的一条趋势，不要写成行动建议"
}}

数量要求：
- platform_intelligence: 2-5 条
- ai_technology: 2-5 条
- retail_trends: 2-5 条
- 如果某类信息不足，宁可少写，不要凑数。
- 人工输入如果质量高，优先进入对应分类。

Unified Information Pool:
{information_pool}
""".strip()


def _format_information_pool(items):
    blocks = []
    for index, item in enumerate(items, start=1):
        blocks.append(
            "\n".join(
                [
                    f"[{index}]",
                    f"Source: {item.get('source', '')}",
                    f"Domain: {item.get('domain', '')}",
                    f"Origin Type: {item.get('origin_type', '')}",
                    f"Manual Category: {item.get('manual_category', '')}",
                    f"Manual Company: {item.get('manual_company', '')}",
                    f"Published Date: {item.get('published_date', '')}",
                    f"Title: {item.get('title', '')}",
                    f"Summary: {item.get('summary', '')}",
                    f"Link: {item.get('link', '')}",
                ]
            )
        )
    return "\n\n".join(blocks)
