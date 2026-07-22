from pathlib import Path


PROJECT_NAME = "Digital Commerce Intelligence Hub"

BASE_DIR = Path(__file__).resolve().parent
MANUAL_INPUT_PATH = BASE_DIR / "manual_sources" / "daily_input.md"
HTML_OUTPUT_PATH = BASE_DIR / "output" / "index.html"

MAX_ITEMS_FOR_GEMINI = 28
RSS_ITEMS_PER_FEED = 8
GOOGLE_NEWS_ITEMS_PER_QUERY = 5

SECTION_ORDER = ["platform", "ai", "sports", "retail"]

FEEDS = [
    {"source": "Retail Dive", "url": "https://www.retaildive.com/feeds/news/", "domain": "retail"},
    {"source": "Retail TouchPoints", "url": "https://www.retailtouchpoints.com/feed/", "domain": "retail"},
    {"source": "Modern Retail", "url": "https://www.modernretail.co/feed/", "domain": "retail"},
    {"source": "SportsPro", "url": "https://www.sportspro.com/feed/", "domain": "sports"},
    {"source": "SportBusiness", "url": "https://www.sportbusiness.com/feed/", "domain": "sports"},
    {"source": "Front Office Sports", "url": "https://frontofficesports.com/feed/", "domain": "sports"},
    {"source": "WWD Business", "url": "https://wwd.com/business-news/feed/", "domain": "sports"},
    {"source": "Google AI Blog", "url": "https://blog.google/technology/ai/rss/", "domain": "ai"},
]

SEARCH_QUERIES = {
    "platform": [
        "Alibaba ecommerce strategy", "Taobao platform update", "Tmall merchant tools", "1688 ecommerce platform", "Cainiao logistics supply chain",
        "JD retail strategy", "JD logistics service", "JD supply chain", "JD Health new business", "JD retail membership",
        "Douyin ecommerce strategy", "ByteDance ecommerce", "Pinduoduo platform strategy", "Meituan instant retail", "WeChat ecommerce",
        "Xiaohongshu commerce", "Kuaishou ecommerce", "阿里 电商 战略", "淘宝 平台 新功能", "天猫 商家 能力",
        "1688 电商 平台", "菜鸟 物流 供应链", "京东 新业务", "京东 供应链", "京东 物流 开放",
        "京东健康 新业务", "抖音 电商 战略", "字节 电商", "拼多多 平台", "美团 即时零售",
        "微信 电商", "小红书 商业化", "快手 电商",
    ],
    "ai": [
        "AI search ecommerce", "AI shopping assistant", "AI agent customer service", "AI agent shopping task", "multimodal AI product search",
        "AI product understanding ecommerce", "AI recommendation ecommerce", "AI content generation product descriptions", "AI customer service retail", "AI operations automation retail",
        "AI supply chain optimization", "AI inventory forecasting retail", "AI price optimization retail", "AI store operations", "enterprise AI tool workflow",
        "OpenAI agent shopping", "OpenAI customer service AI", "Google Gemini AI shopping", "Anthropic Claude enterprise agent", "DeepSeek enterprise AI tool",
        "Doubao AI assistant ecommerce", "ByteDance Seed AI agent", "Qwen ecommerce AI", "Tencent Hunyuan enterprise AI", "Kimi AI assistant workflow",
        "Manus AI agent workflow", "Microsoft Copilot retail", "Apple Intelligence productivity", "NVIDIA retail AI", "Hugging Face enterprise AI",
        "AI Search 电商", "AI 购物助手", "AI Agent 客服", "多模态 商品识别", "AI 商品理解",
        "AI 推荐 电商", "AI 生成 商品内容", "AI 客服 零售", "AI 自动化运营", "AI 供应链优化",
        "AI 库存预测", "AI 价格优化", "AI 门店运营", "企业级 AI 工具", "办公协作 AI",
    ],
    "sports": [
        "Decathlon digital strategy", "Decathlon ecommerce", "Nike DTC strategy", "Nike membership", "Adidas ecommerce",
        "Lululemon membership", "Puma digital strategy", "Under Armour ecommerce", "On running retail strategy", "Hoka retail strategy",
        "Salomon ecommerce", "Arc'teryx retail strategy", "Patagonia digital retail", "Columbia sportswear ecommerce", "The North Face retail strategy",
        "Anta digital strategy", "Li-Ning ecommerce", "Garmin fitness retail", "sports retail digital", "outdoor retail strategy",
        "sports brand ecommerce", "sports retail supply chain", "sports retail omnichannel", "apparel retail digital transformation", "running retail consumer trend",
        "迪卡侬 数字化", "迪卡侬 电商", "耐克 DTC", "阿迪达斯 电商", "Lululemon 会员",
        "安踏 数字化", "李宁 电商", "户外 零售 趋势", "运动品牌 数字化", "体育零售 供应链",
    ],
    "retail": [
        "Walmart digital retail", "Walmart AI shopping", "Costco membership digital", "Sam's Club digital store", "Amazon shopping AI",
        "Target omnichannel", "Zara digital store", "Uniqlo ecommerce", "IKEA omnichannel", "MUJI digital retail",
        "Aldi retail automation", "Lidl digital retail", "Carrefour omnichannel", "7-Eleven digital store", "Hema retail innovation",
        "Inditex RFID retail", "retail supply chain innovation", "RFID retail", "store digitalization", "retail membership innovation",
        "retail fulfillment innovation", "retail inventory sharing", "retail returns app", "grocery fresh management retail", "store automation retail",
    ],
}

# Backward-compatible alias for older imports.
GOOGLE_NEWS_QUERIES = SEARCH_QUERIES

COMMON_EXCLUDED_KEYWORDS = [
    "retail media", "retail media network", "advertising", "ad network", "ad tech", "ctv", "ctv advertising", "programmatic",
    "shopper marketing", "media monetization", "advertising roi", "media budget", "ad spend", "brand advertising", "marketing campaign",
    "campaign", "advertising revenue", "media revenue", "ad revenue",
]

COMMON_LOW_VALUE_KEYWORDS = [
    "product launch", "new sneaker", "new shoe", "shoe release", "capsule collection", "limited edition", "celebrity", "ambassador",
    "endorsement", "collaboration", "sponsorship", "sponsored", "sale event", "discount", "promotion", "promo", "campaign",
    "明星", "代言", "联名", "新品", "新鞋", "折扣", "促销", "赞助", "赛事赞助", "销售战报",
]

FILTER_PROFILES = {
    "platform": {
        "include_any": [
            "alibaba", "taobao", "tmall", "1688", "cainiao", "jd", "jingdong", "jd logistics", "jd health", "douyin", "bytedance",
            "pinduoduo", "pdd", "meituan", "wechat", "xiaohongshu", "kuaishou", "阿里", "淘宝", "天猫", "菜鸟", "京东",
            "京东物流", "京东健康", "抖音", "字节", "拼多多", "美团", "微信", "小红书", "快手",
        ],
        "require_any": [
            "new business", "business unit", "platform strategy", "merchant tools", "search", "recommendation", "membership", "fulfillment",
            "supply chain", "logistics", "instant retail", "local life", "open capability", "marketplace", "ecommerce", "ai",
            "新业务", "新事业部", "平台战略", "商家工具", "搜索", "推荐", "会员", "履约", "供应链", "物流", "即时零售", "本地生活", "开放能力", "电商",
        ],
        "exclude_any": COMMON_EXCLUDED_KEYWORDS + COMMON_LOW_VALUE_KEYWORDS,
        "override_any": ["platform strategy", "merchant tools", "supply chain", "fulfillment", "logistics", "ecommerce", "search", "recommendation", "membership", "平台战略", "商家工具", "供应链", "履约", "物流", "搜索", "推荐", "会员"],
    },
    "ai": {
        "include_any": [
            "ai search", "ai shopping", "agent", "customer service", "product understanding", "multimodal", "content generation", "recommendation",
            "membership", "operations automation", "supply chain", "inventory forecasting", "price optimization", "store operations", "enterprise ai",
            "copilot", "openai", "gemini", "claude", "deepseek", "doubao", "seed", "qwen", "hunyuan", "kimi", "manus", "nvidia", "hugging face",
            "智能客服", "商品理解", "多模态", "内容生成", "推荐", "会员运营", "自动化运营", "供应链优化", "库存预测", "价格优化", "门店运营", "企业级 AI", "办公协作",
        ],
        "require_any": [
            "ecommerce", "retail", "shopping", "customer service", "user experience", "operations", "workflow", "product", "recommendation", "supply chain",
            "inventory", "store", "enterprise", "office", "developer", "coding", "电商", "零售", "购物", "客服", "用户体验", "运营", "流程", "商品", "推荐", "供应链", "库存", "门店", "企业", "办公", "开发效率",
        ],
        "exclude_any": COMMON_EXCLUDED_KEYWORDS + [
            "benchmark", "leaderboard", "parameter", "parameters", "trillion parameters", "algorithm", "paper", "research paper", "training method", "quantization",
            "gpu memory", "inference framework", "chip specs", "模型排名", "排行榜", "参数规模", "纯算法", "论文", "训练方法", "量化算法", "显存", "推理框架", "芯片参数",
        ],
        "override_any": [
            "shopping", "customer service", "product understanding", "recommendation", "workflow", "operations", "supply chain", "inventory", "store", "enterprise", "retail", "ecommerce", "客服", "商品理解", "推荐", "运营", "供应链", "库存", "门店", "企业", "零售", "电商",
        ],
    },
    "sports": {
        "include_any": [
            "decathlon", "nike", "adidas", "lululemon", "puma", "under armour", "on", "hoka", "salomon", "arc'teryx", "patagonia", "columbia", "the north face", "anta", "li-ning", "kailas", "descente", "fila", "garmin", "fitness", "running", "outdoor", "sports retail",
            "迪卡侬", "耐克", "阿迪达斯", "安踏", "李宁", "户外", "运动品牌", "体育零售",
        ],
        "require_any": [
            "ecommerce", "dtc", "membership", "digital", "store innovation", "supply chain", "fulfillment", "product experience", "search", "recommendation", "consumer trend", "organization", "strategy", "omnichannel", "new retail",
            "电商", "会员", "数字化", "门店创新", "供应链", "履约", "商品体验", "搜索", "推荐", "消费趋势", "组织战略", "新零售",
        ],
        "exclude_any": COMMON_EXCLUDED_KEYWORDS + COMMON_LOW_VALUE_KEYWORDS,
        "override_any": ["dtc", "ecommerce", "membership", "digital", "supply chain", "fulfillment", "strategy", "omnichannel", "电商", "会员", "数字化", "供应链", "履约", "战略"],
    },
    "retail": {
        "include_any": [
            "walmart", "sam's club", "costco", "amazon", "target", "zara", "uniqlo", "ikea", "muji", "aldi", "lidl", "carrefour", "7-eleven", "hema", "inditex",
        ],
        "require_any": [
            "omnichannel", "digital store", "membership", "supply chain", "fulfillment", "rfid", "self-checkout", "search", "recommendation", "ai shopping", "inventory sharing", "returns", "app", "ecommerce experience", "operations efficiency", "fresh management", "store automation",
            "全渠道", "门店数字化", "会员", "供应链", "履约", "自助结账", "搜索", "推荐", "库存共享", "退换货", "运营效率", "生鲜管理", "门店自动化",
        ],
        "exclude_any": COMMON_EXCLUDED_KEYWORDS + COMMON_LOW_VALUE_KEYWORDS,
        "override_any": ["omnichannel", "digital store", "supply chain", "fulfillment", "rfid", "self-checkout", "inventory", "app", "operations", "全渠道", "供应链", "履约", "库存", "运营效率"],
    },
}
