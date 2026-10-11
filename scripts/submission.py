#!/usr/bin/env python3
"""Submission bot: "Add a resource" issue form → checks → pull request.

Runs from .github/workflows/submission.yml on issues events. The issue body is
untrusted data: it is parsed here, in Python, and never reaches a shell.

Steps:
  1. Contributor checks: account age, rate limits, blocklist (.github/submission-policy.toml).
  2. Offline form checks: links, wording, section, duplicates and look-alikes.
  3. Network checks: the link loads and does not redirect to another organization's
     domain, the domain is old enough, the source repository exists and is not archived.
  4. The entry is appended to its README.md section on branch submission/issue-<N>,
     and a pull request is opened or updated. A human always merges.

Environment: GITHUB_EVENT_PATH, GITHUB_REPOSITORY, GH_TOKEN.
Local runs that never write to GitHub:
    python scripts/submission.py --event event.json --dry-run   # with network checks
    python scripts/submission.py --event event.json --offline   # no network at all
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import tomllib
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import readme
from github_api import GitHub, GitHubError, neutralize
from issue_forms import parse
from netcheck import REPO, REPO_URL, domain_registered, fetch, repo_health
from policy import (host_of, identity_key, is_platform, link_targets, normalize_url, plugin_component,
                    registrable_domain, style_problems, text_problems, url_problems)
from trust import TrustResult, assess, label_applied_by_maintainer

TEMPLATE = readme.ROOT / ".github" / "ISSUE_TEMPLATE" / "add-resource.yml"
POLICY = readme.ROOT / ".github" / "submission-policy.toml"
MARKER = "<!-- awesome-moodle-bot:submission -->"
SUBMISSION_LABEL = "submission"
OVERRIDE_LABEL = "maintainer-approved"
UPDATE_FORM = f"{REPO_URL}/issues/new?template=update-resource.yml"

AFFILIATION = {
    "I have no affiliation with this project": "none",
    "I am its author or maintainer, work for the vendor, or was asked or paid by them": "vendor",
    "Other relationship (explain below)": "other",
}
PRICING = {"Free": "Free", "Premium": "Premium"}

NAME_RE = re.compile(r"^[0-9A-Za-zÀ-ÖØ-öø-ÿ][0-9A-Za-zÀ-ÖØ-öø-ÿ .,+&'’()/:!_-]{0,59}$")
REPO_RE = re.compile(r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
LIMITS = {"description": 300, "description_min": 40, "notes": 3000}


@dataclass
class Outcome:
    entry: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    labels: set[str] = field(default_factory=set)
    facts: dict[str, object] = field(default_factory=dict)


def load_policy() -> dict:
    with open(POLICY, "rb") as f:
        return tomllib.load(f)


def one_line(text: object) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def name_key(name: str) -> str:
    """"Level Up!", "level-up" and "LevelUp" are the same name."""
    text = unicodedata.normalize("NFKC", name).casefold()
    return re.sub(r"[^0-9a-z]", "", text) or text


def edit_distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def blocked_domain(url: str, policy: dict) -> bool:
    blocked = {d.lower() for d in policy.get("blocked_domains") or []}
    labels = host_of(url).split(".")
    return any(".".join(labels[i:]) in blocked for i in range(len(labels) - 1))


# ---------------------------------------------------------------- offline checks

def check_url(label: str, url: str, out: Outcome, policy: dict, *, required: bool) -> bool:
    if not url:
        if required:
            out.errors.append(f"**{label}**: please provide a link.")
        return False
    problems = url_problems(url)
    out.errors += [f"**{label}**: the link {p}." for p in problems]
    if not problems and blocked_domain(url, policy):
        out.errors.append(f"**{label}**: this domain is not accepted on the list.")
        return False
    return not problems


def check_duplicates(name: str, url: str, text: str, out: Outcome) -> None:
    listed = readme.entries(text)
    key = name_key(name)
    for entry in listed:
        other = name_key(entry.name)
        if other == key:
            out.errors.append(f"**{neutralize(entry.name)}** is already listed (line {entry.line}). If it is outdated, "
                              f"[report a change]({UPDATE_FORM}).")
            return
        if min(len(key), len(other)) >= 5 and edit_distance(key, other) <= 1:
            out.warnings.append(f"The name is similar to the listed **{neutralize(entry.name)}**; "
                                f"check that it is not an impersonation.")
    if not url:
        return
    targets = [t for t in link_targets(text) if t.startswith("https://")]
    if normalize_url(url) in {normalize_url(t) for t in targets}:
        out.errors.append(f"`{neutralize(normalize_url(url))}` is already linked from the README.")
        return
    ident = identity_key(url)
    if (plugin_component(url) or host_of(url) in {"github.com", "gitlab.com", "codeberg.org", "bitbucket.org"}) \
            and ident in {identity_key(t) for t in targets}:
        out.errors.append(f"`{neutralize(ident.removeprefix('moodle-plugin:'))}` is already on the list.")
        return
    if is_platform(url):
        return
    domain = registrable_domain(host_of(url))
    same = [e for e in listed if registrable_domain(host_of(e.url)) == domain]
    if same:
        out.warnings.append(f"`{neutralize(domain)}` is already listed for **{neutralize(same[0].name)}**; "
                            f"check that this is a different product, not a duplicate.")
    label = domain.split(".")[0]
    for entry in listed:
        other = registrable_domain(host_of(entry.url))
        other_label = other.split(".")[0]
        if not is_platform(entry.url) and len(label) >= 5 and other != domain \
                and edit_distance(label, other_label) <= 2:
            out.warnings.append(f"The domain looks like the domain of **{neutralize(entry.name)}** "
                                f"(`{neutralize(other)}`); check that it is not a phishing copy.")
            break


def evaluate(form: dict, policy: dict, readme_text: str) -> Outcome:
    out = Outcome()

    name = one_line(form.get("name"))
    if not NAME_RE.match(name):
        out.errors.append("**Name**: up to 60 characters; Latin letters, digits, spaces, and `. , + & ' ( ) / : ! _ -`.")

    url = one_line(form.get("url"))
    check_url("Link", url, out, policy, required=True)
    check_duplicates(name, url, readme_text, out)

    section = one_line(form.get("section"))
    if section not in readme.SECTIONS:
        out.errors.append("**Section**: pick one of the listed sections.")

    pricing = PRICING.get(one_line(form.get("pricing")))
    if not pricing:
        out.errors.append("**Pricing**: pick Free or Premium.")

    description = one_line(form.get("description"))
    problems = text_problems(description, max_length=LIMITS["description"], min_length=LIMITS["description_min"])
    if not problems:
        problems = style_problems(description)
    out.errors += [f"**Description** {p}." for p in problems]

    repo = one_line(form.get("repo")).rstrip("/").removesuffix(".git")
    if repo and not REPO_RE.match(repo):
        out.errors.append("**Source code**: the link must look like `https://github.com/owner/repo`.")
    if not repo and REPO_RE.match(url.rstrip("/")):
        repo = url.rstrip("/")

    affiliation = AFFILIATION.get(one_line(form.get("affiliation")))
    if not affiliation:
        out.errors.append("**Your relationship to this project**: pick one of the options.")
    elif affiliation != "none":
        out.labels.add("vendor-submitted")
    notes = str(form.get("notes") or "").strip()
    if len(one_line(notes)) < 40:
        out.errors.append("**Why it belongs on the list**: tell reviewers who it is for, what it adds, "
                          "and which Moodle versions it supports.")
    elif len(notes) > LIMITS["notes"]:
        out.errors.append(f"**Why it belongs on the list**: keep it under {LIMITS['notes']} characters.")
    if not all((form.get("confirmations") or {"": False}).values()):
        out.errors.append("Please tick every box under **Confirmations**.")

    out.entry = {"name": name, "url": url, "section": section, "pricing": pricing or "Free",
                 "description": description, "repo": repo, "affiliation": affiliation}
    return out


# ---------------------------------------------------------------- network checks

def check_online(out: Outcome) -> None:
    url = out.entry["url"]
    result = fetch(url)
    if result.broken:
        out.errors.append(f"**Link** could not be loaded ({neutralize(result.describe())}).")
    elif result.unverifiable:
        out.warnings.append(f"**Link** answered {neutralize(result.describe())}; a maintainer will check it manually.")
    if result.final_url and result.moved_domain:
        out.errors.append(f"**Link** redirects to another domain (`{neutralize(result.final_url)}`). "
                          f"Submit the final address.")


def check_domain_age(url: str, policy: dict, out: Outcome, *, override: bool) -> None:
    if is_platform(url):
        return
    domain = registrable_domain(host_of(url))
    registered = domain_registered(domain)
    min_age = int(policy.get("min_domain_age_days", 90))
    if registered is None:
        out.warnings.append(f"Could not find when `{domain}` was registered; a maintainer will check.")
        return
    age = (dt.datetime.now(dt.timezone.utc).date() - registered).days
    out.facts["domain registered"] = registered.isoformat()
    if age < min_age:
        message = (f"`{domain}` was registered {age} days ago. Sites on domains younger than {min_age} days "
                   f"are not listed; this keeps out short-lived and spam sites.")
        (out.warnings if override else out.errors).append(message)


def run_online_checks(out: Outcome, policy: dict, gh: GitHub | None, *, override: bool) -> None:
    check_online(out)
    check_domain_age(out.entry["url"], policy, out, override=override)
    if out.entry["repo"] and gh is not None:
        problems, warnings = repo_health(gh, out.entry["repo"])
        out.errors += [f"**Source code**: {p}." for p in problems]
        out.warnings += [f"**Source code**: {w}." for w in warnings]


# ---------------------------------------------------------------- messages

def trust_failure_comment(trust: TrustResult) -> str:
    reasons = "\n".join(f"- {r}" for r in trust.errors)
    return ("### Submission not accepted\n\n"
            f"{reasons}\n\n"
            f"These rules protect the list from spam and impersonation; see "
            f"[CONTRIBUTING.md]({REPO_URL}/blob/main/CONTRIBUTING.md#who-can-submit). If you think this is a "
            "mistake, reply below and a maintainer can approve the submission manually.")


def problems_comment(out: Outcome) -> str:
    lines = ["### Please fix", "", *[f"- {e}" for e in out.errors]]
    if out.warnings:
        lines += ["", "**Notes**", *[f"- {w}" for w in out.warnings]]
    lines += ["", "Edit this issue and the checks run again automatically."]
    return "\n".join(lines)


def preview(entry: dict) -> str:
    return f"Section: **{neutralize(entry['section'])}**\n\n{neutralize(readme.render_entry(entry))}"


def success_comment(out: Outcome, pull_number: int) -> str:
    lines = [f"### Checks passed: pull request #{pull_number}", "", preview(out.entry), ""]
    if out.warnings:
        lines += ["A maintainer will also check:", *[f"- {w}" for w in out.warnings], ""]
    lines.append("A maintainer will review the pull request. Edits to this issue update it.")
    return "\n".join(lines)


def pr_body(out: Outcome, issue_number: int, author: str, trust: TrustResult) -> str:
    entry = out.entry
    facts = {**trust.facts, **out.facts}
    lines = [
        f"Adds **{neutralize(entry['name'])}** as requested in #{issue_number} by @{author}.",
        "",
        "#### Preview",
        "",
        preview(entry),
        "",
        "#### Automated checks",
        "",
        "- Contributor: " + ("maintainer" if trust.maintainer else
                             "checks waived by a maintainer" if any("maintainer" in f for f in trust.flags) else
                             "passed"),
        "- Link policy, wording, section, duplicates: passed",
        "- Link loads without a cross-domain redirect, domain age, source repository: passed",
    ]
    review = out.warnings + [f"Contributor: {f}" for f in trust.flags]
    if review:
        lines += ["", "#### Needs a human look", "", *[f"- {r}" for r in review]]
    if facts:
        lines += ["", "<details><summary>Facts</summary>", ""]
        lines += [f"- {k}: {neutralize(v)}" for k, v in facts.items()]
        lines += ["", "</details>"]
    if entry["affiliation"] != "none":
        lines += ["", f"> **Disclosure:** the submitter reports a relationship with this project "
                      f"(`{entry['affiliation']}`)."]
    lines += ["", f"Closes #{issue_number}"]
    return "\n".join(lines)


# ---------------------------------------------------------------- GitHub

def branch_for(issue_number: int) -> str:
    return f"submission/issue-{issue_number}"


def open_pull_request(gh: GitHub, out: Outcome, issue: dict, trust: TrustResult, base: str, base_sha: str,
                      base_text: str) -> dict:
    number, author = issue["number"], issue["user"]["login"]
    branch = branch_for(number)
    new_text = readme.insert_entry(base_text, out.entry)
    title = f"Add {out.entry['name']}"
    message = (f"{title}\n\nSubmitted in #{number}.\n\n"
               f"Co-authored-by: {author} <{issue['user']['id']}+{author}@users.noreply.github.com>")
    gh.commit_files(branch, base_sha, {"README.md": new_text}, message, create=gh.branch_sha(branch) is None)
    body = pr_body(out, number, author, trust)
    pull = gh.open_pull_for(branch)
    if pull:
        gh.update_pull(pull["number"], title, body)
    else:
        pull = gh.create_pull(branch, base, title, body)
    labels = {"new-entry", *out.labels}
    if trust.flags or out.warnings:
        labels.add("needs-manual-review")
    gh.add_labels(pull["number"], sorted(labels))
    return pull


def run(event: dict, gh: GitHub | None, *, online: bool, dry_run: bool) -> int:
    issue = event.get("issue") or {}
    if "pull_request" in issue:
        return 0
    labels = {label["name"] for label in issue.get("labels", [])}
    if SUBMISSION_LABEL not in labels:
        print("Not a submission; skipping.")
        return 0
    action = event.get("action")
    if action == "labeled" and (event.get("label") or {}).get("name") != OVERRIDE_LABEL:
        return 0

    number, author = issue["number"], issue["user"]["login"]
    policy = load_policy()
    override = OVERRIDE_LABEL in labels and gh is not None and label_applied_by_maintainer(gh, number, OVERRIDE_LABEL)
    if issue.get("state") == "closed":
        if not (action == "labeled" and override):
            print("Issue is closed; skipping.")
            return 0
        if not dry_run:
            gh.set_state(number, "open")

    if override:
        trust = TrustResult(login=author, trusted=True, flags=["contributor checks waived by a maintainer"])
    elif gh is None:
        trust = TrustResult(login=author, trusted=True, flags=["local run: contributor checks skipped"])
    else:
        trust = assess(gh, policy, author, issue.get("author_association", "NONE"),
                       kind="new_entry", exclude_issue=number)
    if not trust.ok:
        print("Contributor checks failed:", *trust.errors, sep="\n- ")
        if not dry_run:
            gh.upsert_comment(number, MARKER, trust_failure_comment(trust))
            gh.add_labels(number, ["trust-check-failed"])
            gh.set_state(number, "closed", "not_planned")
        return 0

    base = (event.get("repository") or {}).get("default_branch", "main")
    if gh is not None:
        base_sha = gh.branch_sha(base)
        base_text = gh.file_at(gh.repo, "README.md", base_sha)
        if base_text is None:
            raise GitHubError(404, f"README.md not found on {base}")
        base_text = base_text.replace("\r\n", "\n")
    else:
        base_sha, base_text = "", readme.read()

    out = evaluate(parse(issue.get("body") or "", TEMPLATE), policy, base_text)
    if online and not out.errors:
        run_online_checks(out, policy, gh, override=override)
    if not out.errors:
        try:
            readme.insert_entry(base_text, out.entry)
        except ValueError as exc:
            raise SystemExit(f"README markup is broken; the bot cannot insert the entry: {exc}") from None

    if out.errors:
        print(problems_comment(out))
        if not dry_run:
            pull = gh.open_pull_for(branch_for(number))
            if pull:
                gh.close_pull(pull["number"])
            gh.upsert_comment(number, MARKER, problems_comment(out))
            gh.remove_label(number, "pr-opened")
            gh.add_labels(number, ["needs-changes"])
        return 0

    print("Checks passed.\n" + preview(out.entry))
    if dry_run:
        print(pr_body(out, number, author, trust))
        return 0
    pull = open_pull_request(gh, out, issue, trust, base, base_sha, base_text)
    gh.remove_label(number, "needs-changes")
    gh.add_labels(number, ["pr-opened"])
    gh.upsert_comment(number, MARKER, success_comment(out, pull["number"]))
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # emoji and names print on any console
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--event", default=os.environ.get("GITHUB_EVENT_PATH"), help="path to the event JSON")
    parser.add_argument("--dry-run", action="store_true", help="do not write to GitHub")
    parser.add_argument("--offline", action="store_true", help="no GitHub API and no network checks (implies --dry-run)")
    args = parser.parse_args()
    if not args.event:
        parser.error("--event or GITHUB_EVENT_PATH is required")
    event = json.loads(Path(args.event).read_text(encoding="utf-8"))
    gh = None if args.offline else GitHub(os.environ.get("GITHUB_REPOSITORY", REPO))
    try:
        return run(event, gh, online=not args.offline, dry_run=args.dry_run or args.offline)
    except GitHubError as exc:
        print(f"GitHub API error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
