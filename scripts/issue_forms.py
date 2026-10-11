"""Parsing the Markdown GitHub generates from an issue form.

GitHub renders every field as "### <label>" followed by the answer. Fields and
options are read from the template in .github/ISSUE_TEMPLATE itself, so it stays
the single source of truth. The template is read line by line (no PyYAML) and
is expected to use the standard two-space indentation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

NO_RESPONSE = "_No response_"
CHECKBOX_RE = re.compile(r"^- \[([ xX])\] (.+)$")


@dataclass
class FormField:
    id: str
    label: str
    type: str
    options: list[str] = field(default_factory=list)


def _scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def form_fields(template: Path) -> list[FormField]:
    fields: list[dict] = []
    current: dict | None = None
    in_options = False
    for line in template.read_text(encoding="utf-8").splitlines():
        if m := re.match(r"^  - type: (\S+)\s*$", line):
            current = {"type": m.group(1), "options": []}
            in_options = False
            if current["type"] != "markdown":
                fields.append(current)
        elif current is None:
            continue
        elif m := re.match(r"^    id: (\S+)\s*$", line):
            current["id"] = m.group(1)
        elif m := re.match(r"^      label: (.+)$", line):
            current["label"] = _scalar(m.group(1))
        elif re.match(r"^      options:\s*$", line):
            in_options = True
        elif in_options and (m := re.match(r"^        - (?:label: )?(.+)$", line)):
            current["options"].append(_scalar(m.group(1)))
        elif re.match(r"^      \S", line) or re.match(r"^    \S", line):
            in_options = False
    return [FormField(id=f["id"], label=f["label"], type=f["type"], options=f["options"]) for f in fields]


def parse(body: str, template: Path) -> dict[str, object]:
    """{field id: value}. For checkboxes: {option: checked}."""
    fields = form_fields(template)
    order = {f.label: i for i, f in enumerate(fields)}
    sections: dict[str, list[str]] = {}
    current, position = None, -1
    for line in (body or "").replace("\r\n", "\n").split("\n"):
        heading = re.match(r"^### (.+?)\s*$", line)
        # Headings are accepted once and only in template order, so a "### Field"
        # line inside an answer cannot overwrite a field above it.
        if heading and order.get(heading.group(1), -1) > position:
            current, position = heading.group(1), order[heading.group(1)]
            sections[current] = []
        elif current is not None:
            sections[current].append(line)

    values: dict[str, object] = {}
    for f in fields:
        raw = "\n".join(sections.get(f.label, [])).strip()
        if raw == NO_RESPONSE:
            raw = ""
        if f.type == "checkboxes":
            checked = {}
            for line in raw.split("\n"):
                m = CHECKBOX_RE.match(line.strip())
                if m:
                    checked[m.group(2).strip()] = m.group(1).lower() == "x"
            values[f.id] = {opt: checked.get(opt, False) for opt in f.options}
        else:
            values[f.id] = raw
    return values
