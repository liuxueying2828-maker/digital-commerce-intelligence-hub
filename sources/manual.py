from datetime import datetime, timezone

from sources.common import clean_text, make_item


def fetch_manual_items(path):
    if not path.exists():
        return []

    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []

    title = _extract_title(content)
    return [
        make_item(
            source="Manual Input",
            title=title,
            summary=content,
            link="",
            published_date=datetime.now(timezone.utc),
            domain="Internal Signal",
            origin_type="manual",
            priority=3,
        )
    ]


def _extract_title(content):
    for line in content.splitlines():
        cleaned = clean_text(line).lstrip("#").strip()
        if cleaned:
            return cleaned[:120]
    return "Manual DTC / Digital Commerce Signal"
