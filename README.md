# Digital Commerce Intelligence Hub

A weekly industry intelligence dashboard for Decathlon China DTC / Digital Commerce opportunity discovery.

This project has been upgraded from a simple news push bot into a weekly web-based intelligence dashboard:

GitHub Actions -> Python source collectors -> Unified Information Pool -> Gemini JSON analysis -> HTML Dashboard -> GitHub Pages + Feishu link push

## What It Does

The system collects automatic and manual signals, then asks Gemini to produce short structured dashboard content focused on:

- 国内电商平台 / Platform Intelligence
- AI 技术前沿 / AI Technology
- 体育与户外行业 / Sports & Outdoor
- 传统零售创新 / Retail Innovation
- One Thing Worth Watching

The dashboard is designed for Decathlon China DTC / Digital Commerce / E-commerce leaders to scan in 2-3 minutes while still surfacing useful weekly industry intelligence when there is no major breaking news.

## Information Sources

Automatic sources:

- RSS feeds filtered by section profile
- Google News RSS keyword searches grouped by section
- Official blogs

Automatic retrieval is sectioned before Gemini analysis. Each section uses its own keywords and searches recent information in widening windows: 3 days first, then 7 days, then 14 days. If a section is still below its minimum, the collector expands keywords and reuses the highest-scored recent candidates so the dashboard does not output 0 signal. The four automatic sections are:

- 国内电商平台 / Platform Intelligence
- AI 能力与行业影响 / AI Capabilities & Industry Impact
- 体育与户外行业 / Sports & Outdoor
- 传统零售创新 / Retail Innovation

Manual source:

- `manual_sources/daily_input.md`

Automatic filtering ranks usefulness over recency. It excludes low-relevance retail media, ad-network, campaign, celebrity, sponsorship, and weak product-only items. AI filtering is business-first: pure model releases, parameter counts, benchmarks, papers, and low-level infrastructure details are ignored unless the item clearly introduces a business-understandable capability for retail, ecommerce, customer experience, operations, workflow, or enterprise adoption.

Future sources can be added as new modules under `sources/`, such as PDF, Feishu Docs, or internal business data.

## Project Structure

```text
.
├── main.py
├── config.py
├── requirements.txt
├── .github/
│   └── workflows/
│       └── daily.yml
├── sources/
│   ├── common.py
│   ├── rss.py
│   ├── google_news.py
│   └── manual.py
├── manual_sources/
│   ├── daily_input.md
│   └── examples.md
├── intelligence/
│   ├── prompt.py
│   └── gemini.py
└── output/
    ├── feishu.py
    ├── html.py
    └── index.html
```

## Dashboard Output

Running the script generates:

```text
output/index.html
```

GitHub Actions publishes this file to GitHub Pages.

Feishu only receives a short message:

```text
Digital Commerce Intelligence 已更新
今日重点：...
查看完整页面：...
```

## GitHub Secrets

Add these repository secrets:

- `GEMINI_API_KEY`
- `FEISHU_WEBHOOK_URL`

The API keys are loaded from environment variables. Do not hard-code them in the project.

## Run Locally

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-gemini-api-key"
export FEISHU_WEBHOOK_URL="your-feishu-webhook-url"
export DASHBOARD_URL="https://your-name.github.io/your-repo/"
python main.py
```

Local output will be written to `output/index.html`.

## GitHub Actions

The workflow supports:

- Manual run through `workflow_dispatch`
- Daily scheduled run through cron in UTC
- GitHub Pages deployment from `output/index.html`

Before the first deployment, set repository Pages source to GitHub Actions in GitHub:

Settings -> Pages -> Build and deployment -> Source -> GitHub Actions

See `.github/workflows/daily.yml`.


## History Archive

Each run generates the latest dashboard at `output/index.html` and saves the same day into:

```text
output/archive/YYYY-MM-DD/index.html
output/data/YYYY-MM-DD.json
```

`output/archive/index.html` lists all saved daily briefs in reverse date order. GitHub Actions commits `output/archive` and `output/data` back to the repository so GitHub Pages keeps historical pages across runs.
