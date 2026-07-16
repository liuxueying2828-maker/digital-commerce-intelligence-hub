from pathlib import Path


PROJECT_NAME = "Digital Commerce Intelligence Hub"

BASE_DIR = Path(__file__).resolve().parent
MANUAL_INPUT_PATH = BASE_DIR / "manual_sources" / "daily_input.md"
HTML_OUTPUT_PATH = BASE_DIR / "output" / "index.html"

MAX_ITEMS_FOR_GEMINI = 28
RSS_ITEMS_PER_FEED = 8
GOOGLE_NEWS_ITEMS_PER_QUERY = 5

FEEDS = [
    {
        "source": "Retail Dive",
        "url": "https://www.retaildive.com/feeds/news/",
        "domain": "retail",
    },
    {
        "source": "Retail TouchPoints",
        "url": "https://www.retailtouchpoints.com/feed/",
        "domain": "retail",
    },
    {
        "source": "Modern Retail",
        "url": "https://www.modernretail.co/feed/",
        "domain": "retail",
    },
    {
        "source": "SportsPro",
        "url": "https://www.sportspro.com/feed/",
        "domain": "sports",
    },
    {
        "source": "SportBusiness",
        "url": "https://www.sportbusiness.com/feed/",
        "domain": "sports",
    },
    {
        "source": "Front Office Sports",
        "url": "https://frontofficesports.com/feed/",
        "domain": "sports",
    },
    {
        "source": "WWD Business",
        "url": "https://wwd.com/business-news/feed/",
        "domain": "sports",
    },
    {
        "source": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/",
        "domain": "ai",
    },
]

GOOGLE_NEWS_QUERIES = [
    {"query": "Alibaba ecommerce strategy", "domain": "platform"},
    {"query": "Taobao platform update", "domain": "platform"},
    {"query": "Tmall digital commerce", "domain": "platform"},
    {"query": "JD retail strategy", "domain": "platform"},
    {"query": "JD logistics service", "domain": "platform"},
    {"query": "JD supply chain", "domain": "platform"},
    {"query": "Douyin ecommerce strategy", "domain": "platform"},
    {"query": "ByteDance ecommerce", "domain": "platform"},
    {"query": "Pinduoduo platform strategy", "domain": "platform"},
    {"query": "Meituan retail", "domain": "platform"},
    {"query": "WeChat ecommerce", "domain": "platform"},
    {"query": "Xiaohongshu commerce", "domain": "platform"},
    {"query": "Kuaishou ecommerce", "domain": "platform"},
    {"query": "阿里 电商 战略", "domain": "platform"},
    {"query": "淘宝 平台 新功能", "domain": "platform"},
    {"query": "天猫 商家 能力", "domain": "platform"},
    {"query": "京东 新业务", "domain": "platform"},
    {"query": "京东 供应链", "domain": "platform"},
    {"query": "京东 物流 开放", "domain": "platform"},
    {"query": "抖音 电商 战略", "domain": "platform"},
    {"query": "字节 电商", "domain": "platform"},
    {"query": "拼多多 平台", "domain": "platform"},
    {"query": "美团 零售", "domain": "platform"},
    {"query": "微信 电商", "domain": "platform"},
    {"query": "小红书 商业化", "domain": "platform"},
    {"query": "快手 电商", "domain": "platform"},
    {"query": "OpenAI new model", "domain": "ai"},
    {"query": "OpenAI agent", "domain": "ai"},
    {"query": "Google DeepMind model", "domain": "ai"},
    {"query": "Gemini update", "domain": "ai"},
    {"query": "Anthropic Claude update", "domain": "ai"},
    {"query": "DeepSeek model", "domain": "ai"},
    {"query": "Doubao model", "domain": "ai"},
    {"query": "ByteDance Seed AI", "domain": "ai"},
    {"query": "Qwen model", "domain": "ai"},
    {"query": "Tencent Hunyuan", "domain": "ai"},
    {"query": "Kimi AI update", "domain": "ai"},
    {"query": "Manus AI", "domain": "ai"},
    {"query": "NVIDIA AI model", "domain": "ai"},
    {"query": "Apple Intelligence update", "domain": "ai"},
    {"query": "AI agent", "domain": "ai"},
    {"query": "computer use AI", "domain": "ai"},
    {"query": "AI search", "domain": "ai"},
    {"query": "multimodal model", "domain": "ai"},
    {"query": "reasoning model", "domain": "ai"},
    {"query": "open source LLM", "domain": "ai"},
    {"query": "AI inference cost", "domain": "ai"},
    {"query": "OpenAI 新模型", "domain": "ai"},
    {"query": "DeepSeek 新模型", "domain": "ai"},
    {"query": "豆包 大模型", "domain": "ai"},
    {"query": "字节 Seed", "domain": "ai"},
    {"query": "通义千问", "domain": "ai"},
    {"query": "腾讯混元", "domain": "ai"},
    {"query": "Kimi 更新", "domain": "ai"},
    {"query": "Manus AI", "domain": "ai"},
    {"query": "AI Agent", "domain": "ai"},
    {"query": "多模态", "domain": "ai"},
    {"query": "推理模型", "domain": "ai"},
    {"query": "开源大模型", "domain": "ai"},
    {"query": "AI Search", "domain": "ai"},
    {"query": "Computer Use", "domain": "ai"},
    {"query": "模型推理成本", "domain": "ai"},
    {"query": "Decathlon digital strategy", "domain": "sports"},
    {"query": "Decathlon ecommerce", "domain": "sports"},
    {"query": "Nike DTC strategy", "domain": "sports"},
    {"query": "Nike membership", "domain": "sports"},
    {"query": "Adidas ecommerce", "domain": "sports"},
    {"query": "Lululemon membership", "domain": "sports"},
    {"query": "sports retail digital", "domain": "sports"},
    {"query": "outdoor retail strategy", "domain": "sports"},
    {"query": "sports brand ecommerce", "domain": "sports"},
    {"query": "sports retail supply chain", "domain": "sports"},
    {"query": "sports retail omnichannel", "domain": "sports"},
    {"query": "apparel retail digital transformation", "domain": "sports"},
    {"query": "迪卡侬 数字化", "domain": "sports"},
    {"query": "迪卡侬 电商", "domain": "sports"},
    {"query": "耐克 DTC", "domain": "sports"},
    {"query": "阿迪达斯 电商", "domain": "sports"},
    {"query": "Lululemon 会员", "domain": "sports"},
    {"query": "安踏 数字化", "domain": "sports"},
    {"query": "李宁 电商", "domain": "sports"},
    {"query": "户外 零售 趋势", "domain": "sports"},
    {"query": "运动品牌 数字化", "domain": "sports"},
    {"query": "体育零售 供应链", "domain": "sports"},
    {"query": "Walmart digital retail", "domain": "retail"},
    {"query": "Walmart AI shopping", "domain": "retail"},
    {"query": "Costco membership digital", "domain": "retail"},
    {"query": "Sam's Club digital store", "domain": "retail"},
    {"query": "Amazon shopping AI", "domain": "retail"},
    {"query": "Zara digital store", "domain": "retail"},
    {"query": "Uniqlo ecommerce", "domain": "retail"},
    {"query": "IKEA omnichannel", "domain": "retail"},
    {"query": "retail supply chain innovation", "domain": "retail"},
    {"query": "RFID retail", "domain": "retail"},
    {"query": "store digitalization", "domain": "retail"},
    {"query": "retail membership innovation", "domain": "retail"},
    {"query": "retail fulfillment innovation", "domain": "retail"},
]

SIGNAL_KEYWORDS = [
    "alibaba", "taobao", "tmall", "1688", "jd", "jingdong", "jd logistics", "douyin", "bytedance", "pinduoduo", "pdd", "meituan", "wechat", "xiaohongshu", "kuaishou",
    "阿里", "淘宝", "天猫", "京东", "京东物流", "抖音", "字节", "拼多多", "美团", "微信", "小红书", "快手",
    "platform strategy", "ecommerce", "e-commerce", "marketplace", "merchant tools", "search", "recommendation", "membership", "supply chain", "fulfillment", "logistics", "instant retail", "local life", "omnichannel", "digital store", "app", "DTC",
    "电商", "平台", "商家", "搜索", "推荐", "会员", "供应链", "履约", "物流", "即时零售", "本地生活", "开放能力", "全渠道", "数字门店",
    "openai", "deepmind", "gemini", "anthropic", "claude", "deepseek", "doubao", "seed", "qwen", "hunyuan", "kimi", "moonshot", "manus", "nvidia", "apple intelligence", "microsoft ai", "hugging face",
    "ai model", "new model", "agent", "computer use", "ai search", "ai shopping", "memory", "mcp", "tool use", "api", "open source", "llm", "inference", "reasoning", "multimodal", "ai coding", "voice model", "video model", "image model",
    "新模型", "大模型", "推理", "多模态", "开源大模型", "模型推理成本", "模型效率", "基础设施", "语音模型", "视频模型", "图像模型", "豆包", "通义", "千问", "混元",
    "decathlon", "nike", "adidas", "lululemon", "puma", "under armour", "hoka", "salomon", "arc'teryx", "patagonia", "columbia", "the north face", "rei", "anta", "li-ning", "kailas", "descente", "fila", "skechers",
    "sports retail", "sporting goods", "outdoor retail", "apparel retail", "sports brand", "store innovation", "category shift", "consumer trend",
    "迪卡侬", "耐克", "阿迪达斯", "安踏", "李宁", "户外", "运动品牌", "体育零售", "服装", "门店创新", "品类变化",
    "walmart", "sam's club", "costco", "amazon", "target", "zara", "uniqlo", "ikea", "muji", "7-eleven", "carrefour", "inditex", "h&m",
    "rfid", "self-checkout", "inventory", "returns", "retail operations", "零售创新", "库存", "退换货", "自助结账", "运营效率",
]

EXCLUDED_KEYWORDS = [
    "retail media", "retail media network", "advertising", "ad network", "ad tech", "ctv", "ctv advertising", "programmatic", "shopper marketing", "media monetization", "advertising roi", "media budget", "ad spend", "brand advertising", "marketing campaign", "campaign", "advertising revenue", "media revenue", "ad revenue",
]

EXCLUSION_OVERRIDE_KEYWORDS = [
    "platform strategy", "ecommerce", "e-commerce", "supply chain", "fulfillment", "membership", "search", "recommendation", "ai model", "new model", "agent", "digital store", "omnichannel", "sports retail", "apparel retail", "dtc", "marketplace", "logistics", "instant retail", "local life", "商家", "供应链", "履约", "会员", "搜索", "推荐", "物流", "即时零售", "本地生活", "大模型", "新模型", "多模态",
]

LOW_VALUE_KEYWORDS = [
    "product launch", "new sneaker", "new shoe", "shoe release", "capsule collection", "limited edition", "celebrity", "ambassador", "endorsement", "collaboration", "sponsorship", "sponsored", "sale event", "discount", "promotion", "promo", "campaign", "明星", "代言", "联名", "新品", "新鞋", "折扣", "促销", "赞助", "赛事赞助", "销售战报",
]

HIGH_RELEVANCE_KEYWORDS = EXCLUSION_OVERRIDE_KEYWORDS + [
    "strategy", "digital", "ecommerce", "membership", "supply chain", "fulfillment", "omnichannel", "store innovation", "platform", "organization", "business unit", "new business", "ai", "app", "rfid", "inventory", "战略", "数字化", "电商", "会员", "供应链", "履约", "全渠道", "组织调整", "新业务", "门店", "库存",
]
