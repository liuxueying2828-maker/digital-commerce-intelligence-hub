# Digital Commerce Intelligence Hub

An AI intelligence dashboard for Decathlon China DTC / Digital Commerce opportunity discovery.

This project has been upgraded from a simple news push bot into a web-based intelligence dashboard:

GitHub Actions -> Python source collectors -> Unified Information Pool -> Gemini JSON analysis -> HTML Dashboard -> GitHub Pages + Feishu link push

## What It Does

The system collects external signals, then asks Gemini to produce short structured dashboard content focused on:

- Platform Watch
- AI Watch
- Retail Watch
- One Thing Worth Watching

The dashboard is designed for Decathlon China DTC / Digital Commerce / E-commerce leaders to scan in 2-3 minutes.

## Information Sources

Automatic sources:

- RSS feeds
- Google News RSS keyword searches
- Official blogs

Manual sources are kept in the codebase for future use, but this dashboard stage does not include manual input in the daily run.

Future sources can be added as new modules under `sources/`, such as manual notes, PDF, Feishu Docs, or internal business data.

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
