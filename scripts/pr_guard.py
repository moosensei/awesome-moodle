"""Checks for pull requests opened directly rather than through the submission form.

Runs from .github/workflows/pr-guard.yml on `pull_request_target`. It never checks
out or runs code from the pull request: metadata and README.md are read through
the API as data.

What it does:
  - closes pull requests that add entries from contributors without a merged PR
    and points them to the submission form;
  - closes pull requests from accounts below the age threshold or on the blocklist;
  - checks new links (HTTPS, no referral codes, tracking parameters, or shorteners);
  - labels a listed entry whose link moves to another organization (domain-change),
    the usual way listings get hijacked;
  - labels changes to automation and policy files (sensitive-change).

Environment: GITHUB_EVENT_PATH, GITHUB_REPOSITORY, GH_TOKEN.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tomllib
from pathlib import Path

import readme
from github_api import GitHub, GitHubError, neutralize
from netcheck import REPO, REPO_URL
from policy import (CODE_HOSTS, host_of, identity_key, is_platform, link_targets, normalize_url, owner_key,
                    registrable_domain, url_problems)
from submission import name_key
from trust import assess

MARKER = "<!-- awesome-moodle-bot:pr-guard -->"
POLICY = readme.ROOT / ".github" / "submission-policy.toml"
SENSITIVE_PREFIXES = (".github/", "scripts/", "tests/", "docs/")
SENSITIVE_FILES = {"SECURITY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "LICENSE", ".gitattributes", ".gitignore"}
MAX_README_BYTES = 500_000
VENDOR_RE = re.compile(r"^- \[[xX]\] I am the author or maintainer", re.M)


def readme_changes(base: str, head: str) -> dict:
    """New entries, entries whose link moves to another owner, and new links between two README versions."""
    before = {name_key(e.name): e for e in readme.entries(base)}
    base_urls = {normalize_url(e.url) for e in before.values()}
    added, moved = [], []
    for entry in readme.entries(head):
        old = before.get(name_key(entry.name))
        if old is None:
            if normalize_url(entry.url) not in base_urls:
                added.append(entry.name)
            continue
        code_repo_changed = host_of(entry.url) in CODE_HOSTS and identity_key(old.url) != identity_key(entry.url)
        if owner_key(old.url) != owner_key(entry.url) or code_repo_changed:
            moved.append((entry.name, identity_key(old.url), identity_key(entry.url)))
    old_links = set(link_targets(base))
    new_links = sorted({t for t in link_targets(head) if "://" in t} - old_links)
    known = {registrable_domain(host_of(t)) for t in old_links if t.startswith("https://")}
    new_domains = sorted({registrable_domain(host_of(t)) for t in new_links
                          if t.startswith("https://") and not is_platform(t)} - known)
    return {"added": sorted(set(added)), "moved": moved, "new_links": new_links, "new_domains": new_domains}


def run(event: dict, gh: GitHub, *, dry_run: bool) -> int:
    pr = event["pull_request"]
    number, author = pr["number"], pr["user"]["login"]
    if pr["user"].get("type") == "Bot":
        print("Pull request opened by a bot; skipping.")
        return 0
    if pr.get("state") != "open":
        return 0

    files = gh.pull_files(number)
    paths = [f["filename"] for f in files]
    changes = {"added": [], "moved": [], "new_links": [], "new_domains": []}
    readme_broken = False
    if "README.md" in paths:
        head_repo = ((pr.get("head") or {}).get("repo") or {}).get("full_name", gh.repo)
        base_text = gh.file_at(gh.repo, "README.md", pr["base"]["sha"]) or ""
        head_text = gh.file_at(head_repo, "README.md", pr["head"]["sha"])
        if head_text is None or len(head_text.encode()) > MAX_README_BYTES:
            readme_broken = True
        else:
            changes = readme_changes(base_text.replace("\r\n", "\n"), head_text.replace("\r\n", "\n"))

    with open(POLICY, "rb") as f:
        policy = tomllib.load(f)
    kind = "new_entry" if changes["added"] else "update"
    trust = assess(gh, policy, author, pr.get("author_association", "NONE"), kind=kind, check_limits=False)
    if trust.maintainer:
        print("Pull request from a maintainer; skipping.")
        return 0

    problems: list[str] = []
    notes: list[str] = []
    labels: set[str] = set()
    close = False

    if not trust.ok:
        problems += trust.errors
        labels.add("trust-check-failed")
        close = True
    elif changes["added"] and not trust.trusted:
        names = ", ".join(f"**{neutralize(n)}**" for n in changes["added"][:10])
        problems.append(f"New entries ({names}) from first-time contributors are added through the "
                        f"[submission form]({REPO_URL}/issues/new?template=add-resource.yml). It runs the same "
                        f"checks and opens the pull request for you; one form per entry.")
        labels.add("use-submission-form")
        close = True

    if readme_broken:
        problems.append("README.md could not be read from this pull request.")
    for url in changes["new_links"]:
        for problem in url_problems(url):
            problems.append(f"The link {neutralize(url)} {problem}.")
            labels.add("needs-changes")
    for name, before, after in changes["moved"]:
        labels.add("domain-change")
        notes.append(f"The link of **{neutralize(name)}** moves from `{neutralize(before)}` to `{neutralize(after)}`. "
                     f"This needs evidence that the new address belongs to the same project: the old one redirects "
                     f"there, or there is an official announcement.")
    if changes["new_domains"]:
        notes.append("New domains: " + ", ".join(f"`{neutralize(d)}`" for d in changes["new_domains"][:15])
                     + ". Check that they are official sites, not copies.")

    sensitive = [p for p in paths if p.startswith(SENSITIVE_PREFIXES) or p in SENSITIVE_FILES]
    if sensitive:
        labels.add("sensitive-change")
        notes.append("This pull request changes automation or policy ("
                     + ", ".join(f"`{neutralize(p)}`" for p in sensitive[:10])
                     + "); it needs a careful maintainer review.")
    if VENDOR_RE.search(pr.get("body") or ""):
        labels.add("vendor-submitted")
    if trust.flags:
        labels.add("needs-manual-review")
        notes += [f"Contributor: {f}" for f in trust.flags]

    print(json.dumps({"problems": problems, "notes": notes, "labels": sorted(labels), "close": close},
                     ensure_ascii=False, indent=2))
    if dry_run:
        return 0
    if labels:
        gh.add_labels(number, sorted(labels))
    if problems or notes:
        body = []
        if problems:
            body += ["### Problems", *[f"- {p}" for p in problems], ""]
        if notes:
            body += ["### For reviewers", *[f"- {n}" for n in notes], ""]
        if close:
            body.append("This pull request was closed automatically. If this is a mistake, reply here and a "
                        "maintainer will take a look.")
        gh.upsert_comment(number, MARKER, "\n".join(body))
    if close:
        gh.set_state(number, "closed")
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # emoji and names print on any console
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--event", default=os.environ.get("GITHUB_EVENT_PATH"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.event:
        parser.error("--event or GITHUB_EVENT_PATH is required")
    event = json.loads(Path(args.event).read_text(encoding="utf-8"))
    gh = GitHub(os.environ.get("GITHUB_REPOSITORY", REPO))
    try:
        return run(event, gh, dry_run=args.dry_run)
    except GitHubError as exc:
        print(f"GitHub API error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
