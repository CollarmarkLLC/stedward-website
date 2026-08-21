#!/usr/bin/env python3
"""Convert a Google Docs Markdown export into a website bulletin draft."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SECTION_ALIASES = {
    "thoughts from fr. ryan": "Thoughts from Fr. Ryan",
    "upcoming events": "Upcoming Events",
    "for your information": "For Your Information:",
    "holy mass – schedule & intentions": "Mass Intentions for the Coming Week",
    "holy mass - schedule & intentions": "Mass Intentions for the Coming Week",
    "mass intentions for the coming week": "Mass Intentions for the Coming Week",
    "assistants at holy mass": "Assistants at Holy Mass",
    "our return to the lord": "Our Return to the Lord",
    "community celebrations": "Community Celebrations",
    "in our prayers daily": "In Our Daily Prayers…",
    "in our daily prayers…": "In Our Daily Prayers…",
    "in our daily prayers...": "In Our Daily Prayers…",
}

OUTPUT_ORDER = [
    "Thoughts from Fr. Ryan",
    "Upcoming Events",
    "For Your Information:",
    "Mass Intentions for the Coming Week",
    "Assistants at Holy Mass",
    "Our Return to the Lord",
    "Community Celebrations",
    "In Our Daily Prayers…",
]

PRINT_ONLY_HEADINGS = {
    "prayer for hurricane season",
    "novena to st jude",
}


def heading_name(line: str) -> str | None:
    match = re.match(r"^#{1,6}\s+(.*)$", line.strip())
    if not match:
        return None
    value = re.sub(r"[*_]", "", match.group(1)).strip().rstrip(":").strip()
    key = value.casefold()
    return SECTION_ALIASES.get(key) or SECTION_ALIASES.get(key + ":")


def clean_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x0b", "\n")
    text = re.sub(r"\\([!#()\-.])", r"\1", text)
    text = text.replace("\\~", "~")
    text = re.sub(r"^\[image\d+\]:\s*<data:image/.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_sections(text: str) -> tuple[dict[str, str], list[str]]:
    sections: dict[str, list[str]] = {}
    warnings: list[str] = []
    current: str | None = None

    for line in clean_markdown(text).splitlines():
        heading = heading_name(line)
        if heading:
            if heading in sections:
                warnings.append(f"duplicate section: {heading}")
            current = heading
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)

    for wanted in OUTPUT_ORDER:
        if wanted not in sections:
            warnings.append(f"missing section: {wanted}")

    cleaned: dict[str, str] = {}
    for name, lines in sections.items():
        body = "\n".join(lines).strip()
        body = remove_print_only_blocks(body)
        if name == "Mass Intentions for the Coming Week":
            body = normalize_mass_intentions(body)
        elif name == "In Our Daily Prayers…":
            body = normalize_prayer_paragraphs(body)
        cleaned[name] = body
    return cleaned, warnings


def remove_print_only_blocks(body: str) -> str:
    kept: list[str] = []
    for block in re.split(r"\n\s*\n", body):
        plain = re.sub(r"[*_`|:#]", "", block).strip().casefold()
        if any(plain.startswith(title) for title in PRINT_ONLY_HEADINGS):
            continue
        kept.append(block)
    return "\n\n".join(kept).strip()


def normalize_mass_intentions(body: str) -> str:
    lines = body.splitlines()
    result: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith(("|", "**", "*Altar")):
            result.append(line)
            continue
        if re.match(r"^(Sat|Sun|Mon|Tue|Tues|Wed|Thu|Fri)\b", stripped):
            fields = re.split(r"\t+| {2,}", stripped)
            result.append("- " + " ".join(field.strip() for field in fields if field.strip()))
        else:
            result.append(line)
    return "\n".join(result).strip()


def normalize_prayer_paragraphs(body: str) -> str:
    """Google emits each prayer-list category as a soft line break."""
    result: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped and result and result[-1].strip() and not stripped.startswith("**"):
            result.append("")
        result.append(line)
    return "\n".join(result).strip()


def projection_metadata(path: Path, date: str) -> tuple[str, str] | None:
    data = json.loads(path.read_text(encoding="utf-8"))
    for sunday in data["sundays"]:
        if sunday["date"] == date:
            return sunday["title"], sunday["color"]
    return None


def liturgical_calendar_metadata(root: Path, date: str) -> tuple[str, str] | None:
    """Read the selected modern observance from Liturgical Calendar output."""
    try:
        payload = json.loads((root / date[:4] / "liturgical-core.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    for day in payload.get("days", []):
        if day.get("date") != date:
            continue
        selected = day.get("liturgical", {}).get("modern", {}).get("selected", {})
        title = selected.get("display_title") or selected.get("title")
        colors = selected.get("colors") or []
        if title and colors and isinstance(colors[0], str):
            return str(title), colors[0]
        return None
    return None


def render(date: str, title: str, color: str, sections: dict[str, str]) -> str:
    title_yaml = title.replace('"', '\\"')
    parts = [
        "---",
        f"date: {date}",
        f'title: "{title_yaml}"',
        f"image: /images/bulletins/{color.lower()}.jpg",
        "---",
    ]
    for heading in OUTPUT_ORDER:
        if heading not in sections:
            continue
        parts.extend(["", f"## {heading}", "", sections[heading]])
        if heading in {
            "Thoughts from Fr. Ryan",
            "For Your Information:",
            "Assistants at Holy Mass",
            "Our Return to the Lord",
            "Community Celebrations",
        }:
            parts.extend(["", "---"])
    return clean_markdown("\n".join(parts)) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a Google Docs Markdown export into a reviewed website draft."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("--date", required=True, help="Bulletin Sunday (YYYY-MM-DD)")
    parser.add_argument("--title", help="Required when the Sunday projection has no entry")
    parser.add_argument("--color", help="Required when the Sunday projection has no entry")
    parser.add_argument(
        "--liturgical-calendar-root",
        type=Path,
        help="Normalized Liturgical Calendar output; supplies the modern title and color by date",
    )
    parser.add_argument("--output", type=Path, help="Write a draft; stdout is the default")
    parser.add_argument(
        "--projection",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data/bulletin-sundays-2019-2026.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = (
        liturgical_calendar_metadata(args.liturgical_calendar_root, args.date)
        if args.liturgical_calendar_root else None
    ) or projection_metadata(args.projection, args.date)
    title = args.title or (metadata[0] if metadata else None)
    color = args.color or (metadata[1] if metadata else None)
    if not title or not color:
        print(
            "error: date is absent from the Sunday projection; supply --title and --color",
            file=sys.stderr,
        )
        return 2

    sections, warnings = extract_sections(args.source.read_text(encoding="utf-8"))
    output = render(args.date, title, color, sections)
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)

    if args.output:
        if args.output.exists():
            print(f"error: output already exists: {args.output}", file=sys.stderr)
            return 2
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"wrote draft: {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
