from datetime import datetime


def build_dashboard_prompt(items):
    information_pool = _format_information_pool(items)

    return f"""
你是一名服务于 Decathlon China DTC / Digital Commerce / E-commerce 团队的行业情报分析师。

项目名称：Digital Commerce Intelligence Hub

你的任务不是写日报文章，而是从 Unified Information Pool 中提炼适合 Executive Dashboard 展示的短趋势信号。

本阶段只关注外部公开信息源，不处理 manual input。

请严格遵守：
- 只输出合法 JSON，不要输出 Markdown，不要输出解释文字。
- 不要编造信息池中没有的事实。
- 每条内容控制在 1-2 句话。
- 不要输出 Why it matters。
- 不要输出 Recommendation Actions。
- 不要输出 DTC Opportunity Implications。
- 不要堆大段文字。
- 页面目标是让 Leader 在 2-3 分钟内扫完。
- 使用中文，必要时保留 Alibaba、JD、ByteDance、Tencent、Meituan、PDD、AI Agent 等英文词。

JSON schema 必须严格如下：

{{
  "date": "{datetime.now().strftime("%Y-%m-%d")}",
  "headline": "一句话概括今日最重要信号，不超过 36 个中文字符",
  "platform_watch": [
    {{
      "platform": "Alibaba / JD / ByteDance / Tencent / Meituan / PDD / Other",
      "signal": "一句国内互联网平台趋势，关注事业部发展、新业务布局、供应链能力、服务生态延展或入口变化"
    }}
  ],
  "ai_watch": [
    {{
      "topic": "AI Agent / AI Search / AI Customer Service / AI Marketing / AI Shopping / Other",
      "signal": "一句 AI 技术趋势，关注零售和电商应用"
    }}
  ],
  "retail_watch": [
    {{
      "topic": "Retail Media / Omnichannel / Membership / Supply Chain / Store Digitalization / Other",
      "signal": "一句零售与电商趋势"
    }}
  ],
  "one_thing_worth_watching": "今天最值得持续观察的一件事，只输出一句话"
}}

数量要求：
- platform_watch: 3-5 条
- ai_watch: 2-4 条
- retail_watch: 2-4 条
- 如果某类信息不足，宁可少写，不要凑数。

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
                    f"Published Date: {item.get('published_date', '')}",
                    f"Title: {item.get('title', '')}",
                    f"Summary: {item.get('summary', '')}",
                    f"Link: {item.get('link', '')}",
                ]
            )
        )
    return "\n\n".join(blocks)
