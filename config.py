from pathlib import Path


PROJECT_NAME = "Digital Commerce Intelligence Hub"

BASE_DIR = Path(__file__).resolve().parent
MANUAL_INPUT_PATH = BASE_DIR / "manual_sources" / "daily_input.md"
HTML_OUTPUT_PATH = BASE_DIR / "output" / "index.html"

MAX_ITEMS_FOR_GEMINI = 24
RSS_ITEMS_PER_FEED = 8
GOOGLE_NEWS_ITEMS_PER_QUERY = 6

FEEDS = [
    {
        "source": "Retail Dive",
        "url": "https://www.retaildive.com/feeds/news/",
        "domain": "Retail & Commerce",
    },
    {
        "source": "Retail TouchPoints",
        "url": "https://www.retailtouchpoints.com/feed/",
        "domain": "Retail & Commerce",
    },
    {
        "source": "Modern Retail",
        "url": "https://www.modernretail.co/feed/",
        "domain": "Retail & Commerce",
    },
    {
        "source": "SportsPro",
        "url": "https://www.sportspro.com/feed/",
        "domain": "Retail & Commerce",
    },
    {
        "source": "SportBusiness",
        "url": "https://www.sportbusiness.com/feed/",
        "domain": "Retail & Commerce",
    },
    {
        "source": "Front Office Sports",
        "url": "https://frontofficesports.com/feed/",
        "domain": "Consumer Insight",
    },
    {
        "source": "WWD Business",
        "url": "https://wwd.com/business-news/feed/",
        "domain": "Retail & Commerce",
    },
    {
        "source": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/",
        "domain": "AI & Technology",
    },
]

GOOGLE_NEWS_QUERIES = [
    {
        "query": "OpenAI new model AI agent",
        "domain": "AI & Technology",
    },
    {
        "query": "DeepSeek model AI infrastructure",
        "domain": "AI & Technology",
    },
    {
        "query": "Anthropic Claude AI agent",
        "domain": "AI & Technology",
    },
    {
        "query": "NVIDIA AI inference infrastructure",
        "domain": "AI & Technology",
    },
    {
        "query": "Alibaba retail strategy",
        "domain": "Platform & Internet Giants",
    },
    {
        "query": "JD logistics retail service",
        "domain": "Platform & Internet Giants",
    },
    {
        "query": "ByteDance ecommerce",
        "domain": "Platform & Internet Giants",
    },
    {
        "query": "Douyin ecommerce",
        "domain": "Platform & Internet Giants",
    },
    {
        "query": "AI retail",
        "domain": "AI & Technology",
    },
    {
        "query": "retail media",
        "domain": "Retail & Commerce",
    },
    {
        "query": "omnichannel retail",
        "domain": "Retail & Commerce",
    },
]

SIGNAL_KEYWORDS = [
    "ai",
    "openai",
    "deepmind",
    "anthropic",
    "deepseek",
    "claude",
    "nvidia",
    "multimodal",
    "computer use",
    "inference",
    "api",
    "open-source model",
    "foundation model",
    "豆包",
    "通义",
    "混元",
    "kimi",
    "manus",
    "agent",
    "search",
    "customer service",
    "marketing",
    "retail media",
    "crm",
    "membership",
    "loyalty",
    "omnichannel",
    "supply chain",
    "logistics",
    "personalization",
    "recommendation",
    "ecommerce",
    "e-commerce",
    "commerce",
    "retail",
    "store",
    "consumer",
    "brand",
    "sports",
    "sporting goods",
    "decathlon",
    "nike",
    "adidas",
    "lululemon",
    "puma",
    "outdoor",
    "fitness",
    "alibaba",
    "taobao",
    "tmall",
    "jd",
    "jingdong",
    "bytedance",
    "douyin",
    "tiktok",
    "xiaohongshu",
    "rednote",
    "meituan",
    "pinduoduo",
    "tencent",
]
