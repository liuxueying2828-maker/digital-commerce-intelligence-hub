from datetime import datetime
from html import escape


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
      --bg: #f6f7f9;
      --card: #ffffff;
      --ink: #172033;
      --muted: #697386;
      --line: #e7eaf0;
      --blue: #1f5eff;
      --blue-soft: #edf3ff;
      --green: #0e8f68;
      --green-soft: #eaf8f2;
      --violet: #7057d6;
      --violet-soft: #f1effc;
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
      padding: 44px 0 40px;
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
      font-weight: 700;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}

    h1 {{
      margin: 0;
      font-size: clamp(32px, 5vw, 52px);
      line-height: 1;
      letter-spacing: 0;
    }}

    .date {{
      flex: 0 0 auto;
      color: var(--muted);
      font-size: 15px;
      padding-top: 8px;
    }}

    .hero {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 24px;
      margin-bottom: 20px;
    }}

    .hero-label {{
      color: var(--muted);
      font-size: 14px;
      margin-bottom: 8px;
    }}

    .hero-text {{
      margin: 0;
      font-size: clamp(22px, 3vw, 32px);
      line-height: 1.25;
      font-weight: 700;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
      align-items: stretch;
    }}

    .card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 22px;
      min-height: 360px;
    }}

    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 18px;
    }}

    h2 {{
      margin: 0;
      font-size: 20px;
      letter-spacing: 0;
    }}

    .pill {{
      border-radius: 999px;
      padding: 5px 10px;
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }}

    .pill.platform {{
      color: var(--blue);
      background: var(--blue-soft);
    }}

    .pill.ai {{
      color: var(--violet);
      background: var(--violet-soft);
    }}

    .pill.retail {{
      color: var(--green);
      background: var(--green-soft);
    }}

    .signal-list {{
      display: grid;
      gap: 14px;
    }}

    .signal {{
      padding-top: 14px;
      border-top: 1px solid var(--line);
    }}

    .signal:first-child {{
      padding-top: 0;
      border-top: 0;
    }}

    .label {{
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
      margin-bottom: 5px;
    }}

    .signal p {{
      margin: 0;
      font-size: 16px;
    }}

    .watching {{
      margin-top: 20px;
      background: #111827;
      color: white;
      border-radius: 8px;
      padding: 24px;
    }}

    .watching .label {{
      color: #a9b4c7;
      margin-bottom: 8px;
    }}

    .watching p {{
      margin: 0;
      font-size: clamp(20px, 3vw, 28px);
      line-height: 1.3;
      font-weight: 700;
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

    @media (max-width: 900px) {{
      .grid {{
        grid-template-columns: 1fr;
      }}

      .card {{
        min-height: auto;
      }}

      .topbar {{
        display: block;
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

    <section class="hero">
      <div class="hero-label">Today’s Focus</div>
      <p class="hero-text">{escape(headline)}</p>
    </section>

    <section class="grid" aria-label="Signal dashboard">
      {_render_card("Platform Watch", "平台", "platform", data.get("platform_watch", []), "platform", "signal")}
      {_render_card("AI Watch", "AI", "ai", data.get("ai_watch", []), "topic", "signal")}
      {_render_card("Retail Watch", "零售", "retail", data.get("retail_watch", []), "topic", "signal")}
    </section>

    <section class="watching">
      <div class="label">One Thing Worth Watching</div>
      <p>{escape(data.get("one_thing_worth_watching") or headline)}</p>
    </section>

    {_render_warning(data)}
  </main>
</body>
</html>
"""


def _render_card(title, pill_text, pill_class, items, label_key, text_key):
    signals = "\n".join(_render_signal(item, label_key, text_key) for item in items[:5])
    if not signals:
        signals = '<div class="signal"><p>今日未出现高置信度信号。</p></div>'

    return f"""
      <article class="card">
        <div class="card-header">
          <h2>{escape(title)}</h2>
          <span class="pill {escape(pill_class)}">{escape(pill_text)}</span>
        </div>
        <div class="signal-list">
          {signals}
        </div>
      </article>
    """


def _render_signal(item, label_key, text_key):
    if isinstance(item, str):
        label = ""
        text = item
    else:
        label = item.get(label_key, "")
        text = item.get(text_key, "")

    label_html = f'<div class="label">{escape(label)}</div>' if label else ""
    return f"""
      <div class="signal">
        {label_html}
        <p>{escape(text)}</p>
      </div>
    """


def _render_warning(data):
    warning = data.get("parse_warning")
    if not warning:
        return ""
    return f'<div class="warning">{escape(warning)}</div>'
