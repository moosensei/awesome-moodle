"""Network checks: link reachability, redirects, domain age (RDAP), repository health."""

from __future__ import annotations

import datetime as dt
import http.client
import json
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from urllib.parse import urlsplit

from policy import host_of, owner_key, registrable_domain

REPO = "moosensei/awesome-moodle"
REPO_URL = f"https://github.com/{REPO}"
USER_AGENT = f"Mozilla/5.0 (compatible; awesome-moodle-linkcheck/1.0; +{REPO_URL})"
# Responses that usually mean "a bot wall answered", not "the page is gone".
UNVERIFIABLE_STATUSES = {401, 403, 405, 406, 409, 425, 429, 451, 503, 520, 521, 522, 523, 525, 526}
# Sites that answer every automated request with a server error.
BOT_WALL_DOMAINS = {"amazon.com"}
STALE_REPO_DAYS = 730


@dataclass
class FetchResult:
    url: str
    status: int | None = None
    final_url: str | None = None
    error: str | None = None
    redirects: list[str] = field(default_factory=list)
    reset: bool = False

    @property
    def ok(self) -> bool:
        return self.status is not None and self.status < 400

    @property
    def unverifiable(self) -> bool:
        if self.status is not None and self.status >= 500 and registrable_domain(host_of(self.url)) in BOT_WALL_DOMAINS:
            return True
        return self.status in UNVERIFIABLE_STATUSES or self.reset

    @property
    def broken(self) -> bool:
        return not self.ok and not self.unverifiable

    @property
    def moved_domain(self) -> bool:
        """A redirect to another organization's domain: often a sold, expired, or hijacked domain."""
        if not self.final_url:
            return False
        return owner_key(self.url) != owner_key(self.final_url)

    def describe(self) -> str:
        return self.error or f"HTTP {self.status}"


class _RecordingRedirects(urllib.request.HTTPRedirectHandler):
    max_redirections = 8

    def __init__(self) -> None:
        self.chain: list[str] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append(newurl)
        if not newurl.startswith("https://"):
            raise urllib.error.HTTPError(newurl, 599, "redirect to a non-HTTPS URL", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str, timeout: float = 20.0) -> FetchResult:
    result = FetchResult(url=url)
    handler = _RecordingRedirects()
    opener = urllib.request.build_opener(handler, urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    # Non-ASCII characters in paths and queries are sent percent-encoded.
    request = urllib.request.Request(urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%~"), headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        "Accept-Language": "en,*;q=0.5",
    })
    try:
        with opener.open(request, timeout=timeout) as resp:
            resp.read(65536)
            result.status = resp.status
            result.final_url = resp.geturl()
    except urllib.error.HTTPError as exc:
        result.status = exc.code
        result.final_url = exc.geturl() if exc.code != 599 else None
        if exc.code == 599:
            result.error = "redirects to a non-HTTPS address"
    except ssl.SSLError as exc:
        result.error = f"TLS error: {exc.reason or exc}"
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as exc:
        reason = getattr(exc, "reason", exc)
        if isinstance(reason, ConnectionResetError):
            result.reset = True
            result.error = "connection reset by the server (often bot protection)"
        else:
            result.error = f"cannot be loaded: {reason}"
    except (ValueError, http.client.HTTPException) as exc:
        result.error = f"invalid response or address: {exc}"
    result.redirects = handler.chain
    return result


def domain_registered(domain: str) -> dt.date | None:
    """Registration date from RDAP, or None when the registry does not publish it."""
    request = urllib.request.Request(f"https://rdap.org/domain/{domain}", headers={
        "User-Agent": USER_AGENT, "Accept": "application/rdap+json",
    })
    try:
        with urllib.request.urlopen(request, timeout=20) as resp:
            data = json.loads(resp.read())
    except (urllib.error.URLError, socket.timeout, TimeoutError, ValueError, OSError):
        return None
    for event in data.get("events", []):
        if event.get("eventAction") == "registration" and event.get("eventDate"):
            try:
                return dt.date.fromisoformat(event["eventDate"][:10])
            except ValueError:
                return None
    return None


def repo_health(gh, repo_url: str, now: dt.datetime | None = None) -> tuple[list[str], list[str]]:
    """(problems, warnings) for a GitHub repository: missing, archived, moved, or inactive."""
    full_name = "/".join([p for p in urlsplit(repo_url).path.split("/") if p][:2])
    info = gh.repo_info(full_name)
    if info is None:
        return ["the repository was not found"], []
    problems, warnings = [], []
    if info.get("archived"):
        problems.append("the repository is archived")
    if info.get("html_url", "").lower() != f"https://github.com/{full_name}".lower():
        problems.append(f"the repository moved to {info.get('html_url')}")
    pushed = info.get("pushed_at")
    if pushed:
        now = now or dt.datetime.now(dt.timezone.utc)
        idle = (now - dt.datetime.fromisoformat(pushed.replace("Z", "+00:00"))).days
        if idle > STALE_REPO_DAYS:
            warnings.append(f"the repository has had no commits for {idle} days")
    return problems, warnings
