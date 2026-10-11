"""README.md checks for CI.

Usage:
    python scripts/validate.py                               # structure, links, anchors
    python scripts/validate.py --base origin/main            # also list new links compared to base
    python scripts/validate.py --base origin/main --online   # and check that the new links load

Errors exit with code 1; warnings are only printed. In GitHub Actions findings
are emitted as annotations on README.md lines.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from urllib.parse import unquote

import readme
from netcheck import REPO_URL, fetch
from policy import HIDDEN_CHARS_RE, host_of, is_platform, link_targets, normalize_url, registrable_domain, url_problems

IN_CI = os.environ.get("GITHUB_ACTIONS") == "true"
# Two unescaped dollar signs on one line render as a math formula on GitHub.
DOLLAR_RE = re.compile(r"(?<!\\)\$")


class Report:
    def __init__(self) -> None:
        self.errors = 0
        self.warnings = 0

    def emit(self, level: str, message: str, line: int | None = None) -> None:
        if level == "error":
            self.errors += 1
        else:
            self.warnings += 1
        if IN_CI:
            location = f" file=README.md,line={line}" if line else " file=README.md"
            print(f"::{level}{location}::{message}")
        else:
            print(f"{level.upper():7} README.md{f':{line}' if line else ''}: {message}")


def line_of(text: str, needle: str) -> int | None:
    pos = text.find(needle)
    return text.count("\n", 0, pos) + 1 if pos >= 0 else None


def check_sections(text: str, report: Report) -> None:
    """Every section offered by the submission form exists, and each of its items starts with a link."""
    lines = text.split("\n")
    for option, (path, _) in readme.SECTIONS.items():
        try:
            items = readme.section_items(text, path)
        except ValueError as exc:
            report.emit("error", f"form section '{option}': {exc}")
            continue
        if not items:
            report.emit("error", f"form section '{option}' has no list for the bot to append to")
        for i in items:
            if not readme.ENTRY_RE.match(lines[i]):
                report.emit("error", "entries must look like `- emoji [Name](https://…) badge - Description.`", i + 1)


def check_duplicates(text: str, report: Report) -> None:
    """The same link in two catalog sections. Curated sections (Quick Start, Official, ...) may repeat links."""
    catalog = {path for path, _ in readme.SECTIONS.values()}
    seen: dict[str, list[readme.Entry]] = defaultdict(list)
    for entry in readme.entries(text):
        if entry.section in catalog:
            seen[normalize_url(entry.url)].append(entry)
    for group in seen.values():
        sections = {" › ".join(e.section) for e in group}
        if len(group) > 1 and len(sections) > 1:
            first = group[0]
            for dup in group[1:]:
                report.emit("warning", f"'{dup.name}' is also listed in {' › '.join(first.section)} "
                                       f"(line {first.line})", dup.line)


def check_links(text: str, report: Report) -> None:
    anchors = {h.anchor for h in readme.headings(text)}
    for target in sorted(set(link_targets(text))):
        line = line_of(text, f"]({target})")
        if target.startswith("#"):
            if unquote(target[1:]) not in anchors:
                report.emit("error", f"link `{target}` points to a heading that does not exist", line)
        elif target.startswith(("http://", "https://")):
            for problem in url_problems(target):
                report.emit("error", f"link {target} {problem}", line)
        elif target.startswith("mailto:"):
            continue
        elif "://" in target or target.startswith(("javascript:", "data:")):
            report.emit("error", f"link `{target}` is not allowed", line)
        elif not (readme.ROOT / unquote(target.split("#")[0])).exists():
            report.emit("error", f"file `{target}` does not exist in the repository", line)
    for i, line in enumerate(text.split("\n"), 1):
        if HIDDEN_CHARS_RE.search(line):
            report.emit("error", "the line contains invisible Unicode characters", i)
        if len(DOLLAR_RE.findall(line)) >= 2:
            report.emit("error", "two `$` on one line render as math on GitHub; write USD or escape as `\\$`", i)


def base_text(ref: str) -> str:
    result = subprocess.run(["git", "show", f"{ref}:README.md"], cwd=readme.ROOT,
                            capture_output=True, encoding="utf-8", check=True)
    return result.stdout.replace("\r\n", "\n")


def check_new_links(text: str, base: str, report: Report, *, online: bool) -> None:
    old = set(link_targets(base))
    new = sorted({t for t in link_targets(text) if t.startswith("https://")} - old)
    known = {registrable_domain(host_of(t)) for t in old if t.startswith("https://")}
    known.add(registrable_domain(host_of(REPO_URL)))
    for target in new:
        line = line_of(text, f"]({target})")
        domain = registrable_domain(host_of(target))
        if domain not in known and not is_platform(target):
            known.add(domain)
            report.emit("warning", f"new domain: `{domain}`; check that it is the official site", line)
        if not online:
            continue
        result = fetch(target)
        if result.broken:
            report.emit("error", f"link {target} does not load ({result.describe()})", line)
        elif result.unverifiable:
            report.emit("warning", f"link {target} answered {result.describe()}; check it manually", line)
        if result.final_url and result.moved_domain:
            report.emit("warning", f"link {target} redirects to another domain: {result.final_url}", line)
    print(f"New links compared to base: {len(new)}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # emoji and names print on any console
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", help="git ref to compare README.md with (for example the PR base SHA)")
    parser.add_argument("--online", action="store_true", help="check that new links load")
    args = parser.parse_args()

    text = readme.read()
    report = Report()
    check_sections(text, report)
    check_duplicates(text, report)
    check_links(text, report)
    if args.base:
        check_new_links(text, base_text(args.base), report, online=args.online)
    print(f"Errors: {report.errors}, warnings: {report.warnings}")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
