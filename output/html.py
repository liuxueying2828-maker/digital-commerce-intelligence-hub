from datetime import datetime
from html import escape


SECTIONS = [
    {
        "key": "platform_intelligence",
        "title": "国内电商平台",
        "subtitle": "Platform Intelligence",
        "tone": "blue",
    },
    {
        "key": "ai_technology",
        "title": "AI 技术前沿",
        "subtitle": "AI Technology",
        "tone": "violet",
    },
    {
        "key": "sports_outdoor",
        "title": "体育与户外行业",
        "subtitle": "Sports & Outdoor",
        "tone": "orange",
    },
    {
        "key": "retail_innovation",
        "title": "传统零售创新",
        "subtitle": "Retail Innovation",
        "tone": "green",
    },
]


def render_dashboard(data, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_dashboard_html(data), encoding="utf-8")
    return output_path


def build_dashboard_html(data):
    date = data.get("date") or datetime.now().strftime("%Y-%m-%d")
    headline = data.get("headline") or data.get("one_thing_worth_watching") or "Today’s signals are ready."

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Digital Commerce Intelligence</title>
  <style>
    :root {{
      --bg: #f7f8fb;
      --card: #ffffff;
      --ink: #172033;
      --muted: #687386;
      --line: #e6e9ef;
      --soft-line: #f0f2f6;
      --blue: #2357d9;
      --blue-soft: #edf3ff;
      --green: #078365;
      --green-soft: #eaf8f2;
      --orange: #b25a00;
      --orange-soft: #fff3e6;
      --violet: #6f52d4;
      --violet-soft: #f2effc;
      --dark: #111827;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
        "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
      line-height: 1.5;
    }}

    .page {{
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
      padding: 44px 0 44px;
    }}

    .topbar {{
      display: flex;
      justify-content: space-between;
      gap: 24px;
      align-items: flex-start;
      margin-bottom: 28px;
    }}

    .eyebrow {{
      margin: 0 0 8px;
      color: var(--blue);
      font-size: 13px;
      font-weight: 750;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}

    h1 {{
      margin: 0;
      font-size: clamp(34px, 5vw, 54px);
      line-height: 1;
      letter-spacing: 0;
    }}

    .date {{
      flex: 0 0 auto;
      color: var(--muted);
      font-size: 15px;
      padding-top: 8px;
    }}

    .focus {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 24px;
      margin-bottom: 22px;
    }}

    .focus-label {{
      color: var(--muted);
      font-size: 14px;
      margin-bottom: 8px;
    }}

    .focus-text {{
      margin: 0;
      font-size: clamp(22px, 3vw, 32px);
      line-height: 1.25;
      font-weight: 760;
    }}

    .section {{
      margin-top: 22px;
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 22px;
    }}

    .section-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--soft-line);
      margin-bottom: 18px;
    }}

    h2 {{
      margin: 0;
      font-size: 24px;
      letter-spacing: 0;
    }}

    .subtitle {{
      margin-top: 2px;
      color: var(--muted);
      font-size: 14px;
      font-weight: 650;
    }}

    .section-badge {{
      border-radius: 999px;
      padding: 6px 11px;
      font-size: 12px;
      font-weight: 760;
      white-space: nowrap;
    }}

    .blue {{ color: var(--blue); background: var(--blue-soft); }}
    .violet {{ color: var(--violet); background: var(--violet-soft); }}
    .green {{ color: var(--green); background: var(--green-soft); }}
    .orange {{ color: var(--orange); background: var(--orange-soft); }}

    .cards {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }}

    .card {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      background: #fff;
      min-height: 260px;
    }}

    .card-title {{
      margin: 0;
      font-size: 20px;
      line-height: 1.25;
      letter-spacing: 0;
    }}

    .field {{
      padding-top: 12px;
      border-top: 1px solid var(--soft-line);
    }}

    .field-label {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 780;
      letter-spacing: .04em;
      text-transform: uppercase;
      margin-bottom: 4px;
    }}

    .field p {{
      margin: 0;
      font-size: 15px;
    }}

    .trend {{
      display: inline-flex;
      width: fit-content;
      border-radius: 999px;
      padding: 6px 10px;
      background: #f3f5f8;
      color: #344054;
      font-size: 13px;
      font-weight: 720;
    }}

    .read-button {{
      margin-top: auto;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: fit-content;
      min-height: 38px;
      padding: 8px 13px;
      border-radius: 8px;
      background: var(--dark);
      color: #fff;
      text-decoration: none;
      font-size: 14px;
      font-weight: 760;
    }}

    .read-button.disabled {{
      background: #eef1f5;
      color: #8792a2;
      pointer-events: none;
    }}

    .empty {{
      color: var(--muted);
      border: 1px dashed var(--line);
      border-radius: 8px;
      padding: 18px;
      background: #fbfcfe;
    }}

    .watching {{
      margin-top: 22px;
      background: var(--dark);
      color: white;
      border-radius: 8px;
      padding: 24px;
    }}

    .watching .field-label {{
      color: #a9b4c7;
      margin-bottom: 8px;
    }}

    .watching p {{
      margin: 0;
      font-size: clamp(20px, 3vw, 28px);
      line-height: 1.3;
      font-weight: 760;
    }}

    .warning {{
      margin-top: 14px;
      color: #8a5a00;
      background: #fff7e6;
      border: 1px solid #ffe1a6;
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 13px;
    }}

    @media (max-width: 760px) {{
      .page {{
        width: min(100% - 24px, 1120px);
        padding-top: 28px;
      }}

      .topbar {{
        display: block;
        margin-bottom: 20px;
      }}

      .date {{
        margin-top: 12px;
      }}

      .focus,
      .section,
      .watching {{
        padding: 18px;
      }}

      .section-head {{
        display: block;
      }}

      .section-badge {{
        display: inline-flex;
        margin-top: 10px;
      }}

      .cards {{
        grid-template-columns: 1fr;
      }}

      .card {{
        min-height: auto;
      }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="topbar">
      <div>
        <p class="eyebrow">Digital Commerce Intelligence</p>
        <h1>Today’s Signals</h1>
      </div>
      <div class="date">{escape(date)}</div>
    </section>

    <section class="focus">
      <div class="focus-label">Today’s Focus</div>
      <p class="focus-text">{escape(headline)}</p>
    </section>

    {_render_sections(data)}

    <section class="watching">
      <div class="field-label">One Thing Worth Watching</div>
      <p>{escape(data.get("one_thing_worth_watching") or headline)}</p>
    </section>

    {_render_warning(data)}
  </main>
</body>
</html>
"""


def _render_sections(data):
    return "\n".join(_render_section(section, data.get(section["key"], [])) for section in SECTIONS)


def _render_section(section, cards):
    rendered_cards = "\n".join(_render_card(card) for card in cards[:6])
    if not rendered_cards:
        rendered_cards = '<div class="empty">今日未出现高置信度信号。</div>'

    return f"""
    <section class="section">
      <div class="section-head">
        <div>
          <h2>{escape(section["title"])}</h2>
          <div class="subtitle">{escape(section["subtitle"])}</div>
        </div>
        <span class="section-badge {escape(section["tone"])}">{len(cards[:6])} Signals</span>
      </div>
      <div class="cards">
        {rendered_cards}
      </div>
    </section>
    """


def _render_card(card):
    if isinstance(card, str):
        card = {"name": "Signal", "news": card, "why_this_matters": "", "trend": "Signal", "link": ""}

    link = card.get("link", "")
    button = (
        f'<a class="read-button" href="{escape(link, quote=True)}" target="_blank" rel="noopener noreferrer">阅读全文</a>'
        if link
        else '<span class="read-button disabled">暂无原文链接</span>'
    )

    return f"""
    <article class="card">
      <h3 class="card-title">{escape(card.get("name") or "Signal")}</h3>
      <div class="field">
        <div class="field-label">News</div>
        <p>{escape(card.get("news") or "")}</p>
      </div>
      <div class="field">
        <div class="field-label">Why this matters</div>
        <p>{escape(card.get("why_this_matters") or "")}</p>
      </div>
      <div class="field">
        <div class="field-label">Trend</div>
        <span class="trend">{escape(card.get("trend") or "Trend")}</span>
      </div>
      {button}
    </article>
    """


def _render_warning(data):
    warning = data.get("parse_warning")
    if not warning:
        return ""
    return f'<div class="warning">{escape(warning)}</div>'
