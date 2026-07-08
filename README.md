# Digital Commerce Intelligence Hub

An AI intelligence workflow for Decathlon China DTC / Digital Commerce opportunity discovery.

This project has been upgraded from a simple news push bot into an industry intelligence system:

GitHub Actions -> Python source collectors -> Unified Information Pool -> Gemini analysis -> Feishu text push

## What It Does

The system collects external and manual signals, then asks Gemini to produce an Executive Intelligence Brief focused on:

- Business Signals
- AI & Technology Trends
- Platform Strategy Changes
- Retail & Commerce Trends
- DTC Opportunity Implications
- Recommended Actions

It is designed for Decathlon China DTC / Digital Commerce / E-commerce teams, with special attention to AI, CRM, membership, retail media, omnichannel, store digitization, supply chain, personalization, and China platform ecosystem changes.

## Information Sources

Automatic sources:

- RSS feeds
- Google News RSS keyword searches
- Official blogs

Manual sources:

- `manual_sources/daily_input.md`
- WeChat articles copied manually
- Industry report summaries
- JD / Alibaba / ByteDance official updates
- Leader or mentor feedback
- Meeting notes

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
    └── feishu.py
```

## Manual Input

Paste high-priority manual content into:

```text
manual_sources/daily_input.md
```

If the file is empty, the system skips it without error.

Manual input is treated as a high-priority Internal Signal in the Unified Information Pool.

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
python main.py
```

## GitHub Actions

The workflow supports:

- Manual run through `workflow_dispatch`
- Daily scheduled run through cron in UTC

See `.github/workflows/daily.yml`.
