"""Weekly check of every link in README.md.

Reports broken links and listed sites that started redirecting to another
organization's domain: that is what an expired, sold, or hijacked domain looks
like, and how an abandoned project usually disappears.

The report is printed to stdout. With --issue it lives in one issue labelled
link-report, which is updated on every run and closed when everything is clean.

Links are checked host by host: hosts run in parallel, but the links of one host
run one after another with a pause, because moodle.org rate-limits bursts.

Environment for --issue: GITHUB_REPOSITORY, GH_TOKEN.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import readme
from github_api import GitHub, neutralize
from netcheck import REPO, REPO_URL, FetchResult, fetch
from policy import host_of, link_targets

LABEL = "link-report"
TITLE = "Link check report"
SKIP_PREFIXES = ("https://img.shields.io/", "https://awesome.re", "https://licensebuttons.net/", REPO_URL)
PAUSE_SECONDS = 2.0


def fetch_patiently(url: str) -> FetchResult:
    result = fetch(url)
    for attempt in range(3):
        if result.status != 429:
            break
        time.sleep(15 * (attempt + 1))
        result = fetch(url)
    return result


def fetch_host(urls: list[str]) -> list[tuple[str, FetchResult]]:
    results = []
    for i, url in enumerate(urls):
        if i:
            time.sleep(PAUSE_SECONDS)
        results.append((url, fetch_patiently(url)))
    return results


def check_all(links: list[str]) -> dict[str, FetchResult]:
    by_host: dict[str, list[str]] = defaultdict(list)
    for url in links:
        by_host[host_of(url)].append(url)
    with ThreadPoolExecutor(max_workers=12) as pool:
        batches = pool.map(fetch_host, by_host.values())
    return {url: result for batch in batches for url, result in batch}


def build_report(text: str) -> tuple[str, bool]:
    names = {e.url: e.name for e in readme.entries(text)}
    links = sorted({t for t in link_targets(text) if t.startswith("https://") and not t.startswith(SKIP_PREFIXES)})
    results = check_all(links)

    broken, moved, unverifiable = [], [], []
    for url, result in sorted(results.items()):
        name = neutralize(names.get(url, ""))
        if result.broken:
            broken.append(f"| {name or '—'} | {url} | {neutralize(result.describe())} |")
        elif result.unverifiable:
            unverifiable.append(f"- {url} ({neutralize(result.describe())})")
        if name and result.final_url and result.moved_domain:
            moved.append(f"| {name} | {url} | {neutralize(result.final_url)} |")

    lines = [f"Checked {len(results)} links on {dt.date.today().isoformat()}.", ""]
    if moved:
        lines += [
            "## Listed sites that redirect to another domain",
            "",
            "Confirm the move is genuine (a rebrand or new home) before you update the link. An unexpected "
            "redirect can mean the domain was sold, expired, or hijacked; when in doubt, remove the link first.",
            "",
            "| Entry | Link in README | Now goes to |",
            "| --- | --- | --- |",
            *moved,
            "",
        ]
    if broken:
        lines += ["## Broken links", "", "The page may have moved or the project may be gone: find the new "
                  "official address or remove the entry.", "",
                  "| Entry | Link | Result |", "| --- | --- | --- |", *broken, ""]
    if unverifiable:
        lines += [f"<details><summary>Could not be verified automatically (bot protection, rate limits): "
                  f"{len(unverifiable)}</summary>", "", *unverifiable, "", "</details>"]
    if not moved and not broken:
        lines.append("No broken links and no unexpected redirects.")
    return "\n".join(lines), bool(moved or broken)


def upsert_issue(gh: GitHub, body: str, findings: bool) -> None:
    _, items = gh.search_count(f"repo:{gh.repo} is:issue is:open label:{LABEL}")
    existing = items[0]["number"] if items else None
    if findings:
        if existing:
            gh.update_issue_body(existing, body)
        else:
            gh.create_issue(TITLE, body, [LABEL])
    elif existing:
        gh.update_issue_body(existing, body)
        gh.set_state(existing, "closed", "completed")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # emoji and names print on any console
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--issue", action="store_true", help="keep the report in an issue labelled link-report")
    args = parser.parse_args()
    body, findings = build_report(readme.read())
    print(body)
    if args.issue:
        upsert_issue(GitHub(os.environ.get("GITHUB_REPOSITORY", REPO)), body, findings)
    return 0


if __name__ == "__main__":
    sys.exit(main())
