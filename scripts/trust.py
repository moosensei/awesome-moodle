"""Contributor checks shared by the submission bot and the pull-request guard.

Hard failures (errors) stop the automation. Soft signals (flags) let a
submission through but mark its pull request for a closer human review.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

from github_api import GitHub

MAINTAINER_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}
MAINTAINER_ROLES = {"admin", "maintain", "write"}


@dataclass
class TrustResult:
    login: str
    maintainer: bool = False
    trusted: bool = False  # a maintainer, or already has a merged PR here
    errors: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    facts: dict[str, object] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors


def blocked(policy: dict, login: str) -> bool:
    return login.lower() in {u.lower() for u in policy.get("blocked_users") or []}


def assess(gh: GitHub, policy: dict, login: str, association: str, *, kind: str,
           exclude_issue: int | None = None, check_limits: bool = True,
           now: dt.datetime | None = None) -> TrustResult:
    """kind is "new_entry" or "update". Rate limits apply to issue-form submissions only."""
    now = now or dt.datetime.now(dt.timezone.utc)
    result = TrustResult(login=login)

    if blocked(policy, login):
        result.errors.append("This account may not submit changes to the list.")
        return result

    if association in MAINTAINER_ASSOCIATIONS or gh.permission(login) in MAINTAINER_ROLES:
        result.maintainer = result.trusted = True
        return result

    user = gh.user(login)
    if user.get("type") != "User":
        result.errors.append("Submissions are accepted from personal GitHub accounts only, not from bots or organizations.")
        return result

    created = dt.datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
    age = (now - created).days
    repos, followers = int(user.get("public_repos", 0)), int(user.get("followers", 0))
    result.facts.update({"account created": created.date().isoformat(),
                         "public repositories": repos, "followers": followers})

    merged, _ = gh.search_count(f"repo:{gh.repo} is:pr is:merged author:{login}")
    result.facts["merged PRs here"] = merged
    result.trusted = merged > 0

    min_age = int((policy.get("min_account_age_days") or {}).get(kind, 30))
    if not result.trusted and age < min_age:
        allowed_from = (created + dt.timedelta(days=min_age)).date().isoformat()
        what = "new entries" if kind == "new_entry" else "changes"
        result.errors.append(
            f"Your GitHub account is {age} days old, and {what} are accepted from accounts at least {min_age} days "
            f"old (unless you already have a merged pull request here). Please try again on or after "
            f"{allowed_from}, or wait for a maintainer to approve the request.")

    if check_limits:
        limits = policy.get("limits") or {}
        _, open_items = gh.search_count(f"repo:{gh.repo} is:issue is:open label:submission author:{login}")
        open_others = [i for i in open_items if i.get("number") != exclude_issue]
        max_open = int(limits.get("max_open_submissions", 3))
        if len(open_others) >= max_open:
            refs = ", ".join(f"#{i['number']}" for i in open_others[:5])
            result.errors.append(f"You already have {len(open_others)} open submissions ({refs}). "
                                 f"Please wait until they are reviewed.")
        since = (now - dt.timedelta(days=30)).date().isoformat()
        recent, _ = gh.search_count(f"repo:{gh.repo} is:issue label:submission author:{login} created:>={since}")
        max_recent = int(limits.get("max_submissions_per_30_days", 6))
        if recent > max_recent:
            result.errors.append(f"You sent {recent} submissions in the last 30 days (the limit is {max_recent}).")

    anomalies = policy.get("anomalies") or {}
    if repos >= int(anomalies.get("many_repos_no_followers", 200)) and followers == 0:
        result.flags.append(f"{repos} public repositories and no followers")
    if age < int(anomalies.get("young_account_days", 180)) and repos == 0:
        result.flags.append("young account without public repositories")
    return result


def label_applied_by_maintainer(gh: GitHub, issue_number: int, label: str) -> bool:
    """True when the latest application of the label came from someone with write access."""
    actor = None
    for event in gh.issue_events(issue_number):
        if event.get("event") == "labeled" and event.get("label", {}).get("name") == label:
            actor = (event.get("actor") or {}).get("login")
    return bool(actor) and gh.permission(actor) in MAINTAINER_ROLES
