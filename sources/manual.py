from datetime import datetime, timezone
import re

from sources.common import clean_text, make_item


FIELD_ALIASES = {
    "title": "title",
    "标题": "title",
    "category": "category",
    "分类": "category",
    "company": "company",
    "公司": "company",
    "平台": "company",
    "topic": "company",
    "主题": "company",
    "link": "link",
    "url": "link",
    "链接": "link",
    "原文": "link",
    "content": "content",
    "正文": "content",
    "内容": "content",
    "summary": "content",
    "摘要": "content",
}


def fetch_manual_items(path):
    if not path.exists():
        return []

    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []

    entries = _parse_manual_entries(content)
    items = []
    for entry in entries:
        title = entry.get("title") or _extract_title(entry.get("content", ""))
        body = _format_manual_summary(entry)
        item = make_item(
            source="Manual Input",
            title=title,
            summary=body,
            link=entry.get("link", ""),
            published_date=datetime.now(timezone.utc),
            domain=_infer_domain(entry.get("category", ""), entry.get("company", ""), body),
            origin_type="manual",
            priority=3,
        )
        item["manual_category"] = entry.get("category", "")
        item["manual_company"] = entry.get("company", "")
        items.append(item)

    return items


def _extract_title(content):
    for line in content.splitlines():
        cleaned = clean_text(line).lstrip("#").strip()
        if cleaned:
            return cleaned[:120]
    return "Manual DTC / Digital Commerce Signal"


def _parse_manual_entries(content):
    chunks = [
        chunk.strip()
        for chunk in re.split(r"\n\s*(?:---+|###\s+|##\s+)\s*\n?", content)
        if chunk.strip()
    ]
    return [_parse_manual_entry(chunk) for chunk in chunks] or [_parse_manual_entry(content)]


def _parse_manual_entry(chunk):
    entry = {}
    content_lines = []
    current_field = None

    for raw_line in chunk.splitlines():
        line = raw_line.strip()
        if not line:
            if current_field == "content":
                content_lines.append("")
            continue

        match = re.match(r"^[-*]?\s*([^:：]{1,24})\s*[:：]\s*(.*)$", line)
        if match:
            key = FIELD_ALIASES.get(match.group(1).strip().lower())
            value = match.group(2).strip()
            if key == "content":
                current_field = "content"
                if value:
                    content_lines.append(value)
            elif key:
                entry[key] = clean_text(value)
                current_field = key
            else:
                content_lines.append(line)
                current_field = None
            continue

        content_lines.append(line)

    if content_lines:
        entry["content"] = clean_text("\n".join(content_lines))
    if not entry.get("title"):
        entry["title"] = _extract_title(chunk)
    return entry


def _format_manual_summary(entry):
    parts = []
    if entry.get("category"):
        parts.append(f"Category: {entry['category']}")
    if entry.get("company"):
        parts.append(f"Company: {entry['company']}")
    if entry.get("content"):
        parts.append(f"Content: {entry['content']}")
    return "\n".join(parts) or entry.get("title", "")


def _infer_domain(category, company, content):
    text = f"{category} {company} {content}".lower()
    if any(word in text for word in ["openai", "deepmind", "anthropic", "deepseek", "豆包", "通义", "kimi", "manus", "nvidia", "agent", "模型", "多模态"]):
        return "AI & Technology"
    if any(word in text for word in ["阿里", "alibaba", "京东", "jd", "字节", "bytedance", "腾讯", "tencent", "美团", "meituan", "拼多多", "pdd", "小红书"]):
        return "Platform & Internet Giants"
    return "Retail & Commerce"
