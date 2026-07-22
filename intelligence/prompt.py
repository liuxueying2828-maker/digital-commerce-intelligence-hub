from datetime import datetime


def build_dashboard_prompt(items):
    information_pool = _format_information_pool(items)

    return f"""
你是一名服务于 Decathlon China DTC / Digital Commerce / E-commerce 团队的行业情报分析师。

项目名称：Digital Commerce Intelligence Hub

你的任务不是写日报文章，也不是替管理层做决策。你的任务是筛选自动新闻与人工输入中的高价值信号、解释变化、提炼趋势，并输出适合 Executive Dashboard 展示的短结构化 JSON。

请严格遵守：
- 只输出合法 JSON，不要输出 Markdown，不要输出解释文字。
- 不要编造信息池中没有的事实。
- 无法明确归类或价值较低的新闻直接忽略，不要硬塞。
- 不要输出 retail_media、marketing、advertising、consumer、opportunity、action 等分类。
- Link 必须使用原始文章链接；如果信息池没有链接，输出空字符串。
- 不要输出对迪卡侬意味着什么。
- 不要输出 DTC Opportunity、Recommended Actions、Possible Experiment。
- 不要建议成立团队，不要建议持续关注。
- 不要输出 Evidence 编号或长篇商业建议。

必须排除以下方向，除非新闻本身明确涉及国内电商平台能力、电商产品功能、搜索、推荐、会员、履约、供应链、AI 技术、体育/户外/服装行业数字化创新：
Retail Media、Retail Media Network、Advertising business、Ad tech、CTV advertising、Shopper marketing、Media monetization、Advertising ROI、Media budget、Brand advertising、Marketing campaign、Programmatic advertising。

最终只允许输出四个栏目：platform、ai、sports、retail。

分类优先规则：
1. 国内平台公司新闻优先归入 platform。
2. 有具体模型、Agent、API、推理、多模态、AI Search、Computer Use、开源模型、推理成本、AI 基础设施变化，并且能解释为“业务可理解的能力变化”的新闻归入 ai。
3. 体育、户外、服装品牌相关新闻归入 sports。
4. Walmart、Costco、Amazon、Zara、Uniqlo 等传统零售创新归入 retail。
5. 无法明确归类或价值较低的新闻直接忽略。

栏目定义：

platform / 国内电商平台 / Platform Intelligence
重点关注阿里巴巴、淘宝、天猫、1688、京东、京东零售、京东物流、抖音电商、字节跳动、拼多多、美团、微信、小红书、快手。重点新闻类型包括新事业部或新业务、平台战略变化、搜索、推荐、会员、商家工具、履约、供应链、物流、即时零售、本地生活、平台开放能力、AI 在平台中的真实落地、组织调整或事业部方向变化。人工输入优先于自动来源；如果人工输入已有 1-3 条高质量平台内容，不需要用低价值自动新闻凑满。不要抓普通促销、明星代言、单纯销售战报、普通营销 Campaign、广告预算新闻。

ai / AI 能力与行业影响 / AI Capabilities & Industry Impact
重点关注 OpenAI、Google DeepMind、Gemini、Anthropic、Claude、DeepSeek、豆包、字节 Seed、通义千问/Qwen、腾讯混元、Kimi、Moonshot、Manus、NVIDIA、Apple Intelligence、Microsoft AI、Hugging Face。必须把技术新闻转化为普通业务人员能理解的“能力变化”，例如 AI 可以处理更复杂的任务、AI 开始同时理解图片和文字、AI Agent 可以跨工具完成连续任务、小模型开始支持端侧和本地部署。不要把模型版本号、模型排行榜或复杂参数作为卡片标题；不要输出单纯版本更新；不要堆砌普通人无法理解的技术术语。每条 AI 内容必须说明 Capability 和 Industry Impact，行业影响可以涉及搜索、客服、内容生成、商品理解、推荐、办公协作、软件开发、供应链、任务自动化。如果一条 AI 新闻无法解释新增能力或行业影响，直接忽略。

sports / 体育与户外行业 / Sports & Outdoor
重点关注 Decathlon、Nike、Adidas、Lululemon、Puma、Under Armour、On、Hoka、Salomon、Arc'teryx、Patagonia、Columbia、The North Face、REI、Anta、Li-Ning、Kailas、Descente、Fila、Skechers。重点新闻类型包括数字化能力、电商策略、会员体系、门店创新、商品体验、搜索推荐、供应链、履约、DTC 战略、组织战略、品类变化、消费趋势、体育零售模式创新。不要抓普通新品、单一鞋款、明星合作、普通广告 Campaign、赛事赞助、与数字商业和零售趋势关系弱的品牌新闻。

retail / 传统零售创新 / Retail Innovation
重点关注 Walmart、Sam's Club、Costco、Amazon、Target、Zara、Uniqlo、IKEA、MUJI、7-Eleven、Carrefour、Inditex、H&M。重点新闻类型包括全渠道、门店数字化、会员、供应链、履约、RFID、自助结账、搜索推荐、AI Shopping、数字门店、库存共享、退换货、App、电商体验、零售运营效率。不要抓 Retail Media、广告网络、CTV、广告收入、普通营销活动、普通新品或促销。每条 retail 内容必须交代哪家企业或什么零售场景、采用了什么能力或做法、解决了什么问题或改变了什么流程；原文链接只是补充阅读，卡片本身必须能让读者理解核心内容。避免只写“RFID 正在改变零售”“AI 提升零售效率”“数字化转型加速”这类抽象结论。

JSON schema 必须严格如下：

{{
  "date": "{datetime.now().strftime("%Y-%m-%d")}",
  "headline": "一句话概括当天最重要的整体变化，不超过 38 个中文字符",
  "platform": [
    {{"name": "公司或主题名称", "news": "发生了什么，不超过45个中文字", "why_this_matters": "为什么值得关注，不超过55个中文字", "trend": "2-4个关键词", "link": "原始文章链接"}}
  ],
  "ai": [
    {{"title": "业务可理解的能力变化，不要写模型版本号", "capability": "AI 新增或增强了什么能力，1-2句话", "industry_impact": "这种能力可能影响哪些行业流程，1-2句话", "trend": "2-4个普通人能理解的趋势关键词", "link": "原始文章链接"}}
  ],
  "sports": [
    {{"name": "公司或主题名称", "news": "发生了什么，不超过45个中文字", "why_this_matters": "为什么值得关注，不超过55个中文字", "trend": "2-4个关键词", "link": "原始文章链接"}}
  ],
  "retail": [
    {{"name": "公司或场景名称", "news": "用2-3句话完整说明企业、场景、具体动作和解决的问题", "why_this_matters": "提炼背后的零售模式或能力变化", "trend": "2-4个关键词", "link": "原始文章链接"}}
  ],
  "one_thing_worth_watching": "当天最值得持续观察的一条趋势，不要写成行动建议"
}}

数量要求：
- platform: 2-4 条；人工输入质量高时可少于 2 条，不要用低价值自动新闻凑满。
- ai: 2-4 条；每条控制在 100-150 个中文字，重点是 Capability 与 Industry Impact。
- sports: 2-4 条。
- retail: 1-3 条；每条控制在 120-180 个中文字，News 必须足够完整。
- 不需要凑满，热点优先，质量优先。

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
