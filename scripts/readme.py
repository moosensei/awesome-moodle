"""Parsing and editing README.md: headings, anchors, sections, and entries.

README.md is the single source of truth and is edited by hand. The submission
bot appends a new entry to the end of the list in one of the SECTIONS below. It
finds the section by its heading text (emoji ignored), so the README needs no
special markup; CI checks that every section still exists and holds a list.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
ENTRY_RE = re.compile(r"^- (?:(?P<emoji>[^\s\[]+) )?\[(?P<name>[^\]]+)\]\((?P<url>https?://[^)\s]+)\)")
BADGES = {
    "Free": "![Free](https://img.shields.io/badge/Free-green)",
    "Premium": "![Premium](https://img.shields.io/badge/Premium-orange)",
}

# Option of the "Section" dropdown in add-resource.yml → (heading path without emoji, emoji for new entries).
# A test keeps the keys in sync with the form; CI checks that every path exists in README.md.
SECTIONS: dict[str, tuple[tuple[str, ...], str]] = {
    "Plugins › Content & Activities": (("Plugins", "Content & Activities"), "🧩"),
    "Plugins › Course Design": (("Plugins", "Course Design"), "🎨"),
    "Plugins › Analytics & Reports": (("Plugins", "Analytics & Reports"), "📊"),
    "Plugins › Authentication & Security": (("Plugins", "Authentication & Security"), "🔐"),
    "Plugins › AI & Machine Learning": (("Plugins", "AI & Machine Learning"), "🤖"),
    "Plugins › Mobile & Accessibility": (("Plugins", "Mobile & Accessibility"), "📱"),
    "Plugins › Gamification": (("Plugins", "Gamification"), "🎮"),
    "Plugins › Communication": (("Plugins", "Communication"), "💬"),
    "Plugins › Assessment › Advanced Question Types":
        (("Plugins", "Assessment & Testing Enhancements", "Advanced Question Types"), "❓"),
    "Plugins › Assessment › Proctoring & Academic Integrity":
        (("Plugins", "Assessment & Testing Enhancements", "Proctoring & Academic Integrity"), "🛡️"),
    "Plugins › Assessment › Peer & Collaborative Assessment":
        (("Plugins", "Assessment & Testing Enhancements", "Peer & Collaborative Assessment"), "👥"),
    "Integrations › Cloud Storage Repositories":
        (("Integrations & External Systems", "Cloud Storage Repositories"), "☁️"),
    "Integrations › Microsoft 365 & Google Workspace":
        (("Integrations & External Systems", "Microsoft 365 & Google Workspace"), "🏢"),
    "Integrations › LTI (Learning Tools Interoperability)":
        (("Integrations & External Systems", "LTI (Learning Tools Interoperability)"), "🔗"),
    "Themes › Premium Themes": (("Themes", "Premium Themes"), "🎨"),
    "Themes › Free Themes": (("Themes", "Free Themes"), "🎨"),
    "Development": (("Development",), "💻"),
    "Tools & Utilities": (("Tools & Utilities",), "🛠️"),
    "Hosting › Managed Hosting": (("Hosting & Services", "Managed Hosting"), "☁️"),
    "Hosting › Self-Hosted & VPS": (("Hosting & Services", "Self-Hosted & VPS"), "🖥️"),
    "Migration to Moodle › Conversion & Import Tools": (("Migration to Moodle", "Conversion & Import Tools"), "🔄"),
    "Tutorials & Guides › For Educators": (("Tutorials & Guides", "For Educators"), "📘"),
    "Tutorials & Guides › For Administrators": (("Tutorials & Guides", "For Administrators"), "⚙️"),
    "Tutorials & Guides › For Developers": (("Tutorials & Guides", "For Developers"), "💻"),
    "Videos & Channels › Community Channels": (("Videos & Channels", "Community Channels"), "📺"),
    "Books & Publications": (("Books & Publications",), "📚"),
    "Multilingual Resources › Multilingual Tools": (("Multilingual Resources", "Multilingual Tools"), "🌐"),
}


@dataclass
class Heading:
    level: int
    title: str
    anchor: str
    line: int  # zero-based index


@dataclass
class Entry:
    name: str
    url: str
    line: int  # one-based line number
    section: tuple[str, ...]


def read(path: Path = README) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def github_anchor(heading: str) -> str:
    """The anchor GitHub generates for a heading (github-slugger)."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading.strip()).lower()
    out = []
    for ch in text:
        if ch == " ":
            out.append("-")
        elif ch in "-_" or unicodedata.category(ch)[0] in "LMN":
            out.append(ch)
    return "".join(out)


def plain_title(title: str) -> str:
    """Heading text without the leading emoji: "🔌 Plugins" → "Plugins"."""
    return re.sub(r"^[^0-9A-Za-z]+", "", title).strip()


def headings(text: str) -> list[Heading]:
    """All headings, with -1, -2 suffixes for repeated anchors, as on GitHub."""
    result, seen, fenced = [], {}, False
    for i, line in enumerate(text.split("\n")):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        m = HEADING_RE.match(line)
        if fenced or not m:
            continue
        base = github_anchor(m.group(2))
        count = seen.get(base, 0)
        seen[base] = count + 1
        result.append(Heading(len(m.group(1)), m.group(2), base if count == 0 else f"{base}-{count}", i))
    return result


def section_bounds(text: str, path: tuple[str, ...]) -> tuple[int, int]:
    """[heading line, next heading line) of a section's own content. ValueError if it is missing."""
    hs = headings(text)
    end_of_text = text.count("\n") + 1
    scope = (0, end_of_text)
    found: Heading | None = None
    for depth, title in enumerate(path):
        level = depth + 2
        matches = [h for h in hs if h.level == level and scope[0] <= h.line < scope[1] and plain_title(h.title) == title]
        if len(matches) != 1:
            where = " › ".join(path[:depth]) or "README.md"
            raise ValueError(f"expected one heading `{'#' * level} {title}` in {where}, found {len(matches)}")
        found = matches[0]
        scope = (found.line, next((h.line for h in hs if h.line > found.line and h.level <= level), end_of_text))
    assert found is not None
    return found.line, next((h.line for h in hs if h.line > found.line), end_of_text)


def section_items(text: str, path: tuple[str, ...]) -> list[int]:
    """Zero-based line indexes of the list items directly under a section heading."""
    start, end = section_bounds(text, path)
    lines = text.split("\n")
    return [i for i in range(start + 1, end) if lines[i].startswith("- ")]


def entries(text: str) -> list[Entry]:
    out, path, fenced = [], [], False
    for i, line in enumerate(text.split("\n")):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if m := HEADING_RE.match(line):
            level = len(m.group(1))
            if level >= 2:
                path = path[:level - 2] + [plain_title(m.group(2))]
            continue
        if m := ENTRY_RE.match(line):
            out.append(Entry(m.group("name").strip(), m.group("url"), i + 1, tuple(path)))
    return out


def render_entry(entry: dict) -> str:
    emoji = SECTIONS[entry["section"]][1]
    return f"- {emoji} [{entry['name']}]({entry['url']}) {BADGES[entry['pricing']]} - {entry['description']}"


def insert_entry(text: str, entry: dict) -> str:
    """Appends the entry to its section's list. Broken markup raises ValueError."""
    path = SECTIONS[entry["section"]][0]
    items = section_items(text, path)
    if not items:
        raise ValueError(f"section {' › '.join(path)} has no list to append to")
    lines = text.split("\n")
    lines.insert(items[-1] + 1, render_entry(entry))
    return "\n".join(lines)
