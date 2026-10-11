"""Offline content rules for links and text.

These checks need no network access, so they run in CI on the whole README and
in the submission bot before anything is fetched.
"""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import parse_qsl, urlsplit

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]*)\)")
# Target of every Markdown link, including the outer link around an image: [![alt](img)](url).
LINK_TARGET_RE = re.compile(r"\]\(([^)\s]+)\)")

SHORTENER_HOSTS = {
    "bit.ly", "bitly.com", "buff.ly", "cutt.ly", "goo.gl", "is.gd", "linktr.ee",
    "lnkd.in", "ow.ly", "rb.gy", "rebrand.ly", "shorturl.at", "t.co", "t.ly",
    "tiny.cc", "tinyurl.com", "trib.al", "v.gd", "s.id", "short.io", "bl.ink",
    "clck.ru", "vk.cc", "u.to", "qps.ru", "goo.su", "taplink.cc", "shorturl.me",
}

# Query parameters that carry tracking, affiliate, or referral identifiers.
TRACKING_PARAM_RE = re.compile(
    r"^(utm_\w+|ref|ref_?id|ref_?code|referral(_?code)?|referrer|aff(_?id)?|affiliate(_?id)?|"
    r"via|invite(_?code)?|inviter(_?id)?|partner(_?id)?|promo(_?code)?|coupon|fbclid|gclid|"
    r"dclid|msclkid|yclid|twclid|ttclid|mc_cid|mc_eid|_hsenc|_hsmi|irclickid|clickid|subid|"
    r"campaign(_?id)?|si|igshid)$",
    re.IGNORECASE,
)
REFERRAL_PATH_RE = re.compile(r"/(ref|referral|referrals|invite|aff|affiliate|affiliates|join/[A-Za-z0-9]{4,})(/|$)", re.I)

# Zero-width characters and bidirectional overrides can disguise text and links.
# The zero-width joiner (U+200D) is allowed in README text because it builds emoji
# such as 👨‍💻, but never in links or in submitted text.
HIDDEN_CHARS_RE = re.compile("[​‌‎‏‪-‮⁠-⁤⁦-⁩﻿]")
STRICT_HIDDEN_CHARS_RE = re.compile("[​-‏‪-‮⁠-⁤⁦-⁩﻿]")

PROMO_WORDS_RE = re.compile(
    r"\b(best(?![- ]practices?)|number one|(the|a|market|industry|world)[- ]leading|revolutionary|ultimate|"
    r"world'?s first|game[- ]chang\w*|cutting[- ]edge|unmatched|unrivall?ed|unbeatable|guaranteed|"
    r"must[- ]have|amazing|incredible|next[- ]gen\w*)\b|#1\b|№\s?1\b",
    re.IGNORECASE,
)

MULTI_LABEL_SUFFIXES = {
    "co.uk", "org.uk", "ac.uk", "gov.uk", "com.au", "org.au", "net.au", "edu.au", "co.jp", "co.kr",
    "com.br", "org.br", "edu.br", "com.cn", "com.hk", "com.sg", "co.in", "ac.in", "co.nz", "com.tr",
    "com.mx", "com.ar", "com.co", "com.pe", "com.ec", "co.za", "com.tw", "com.ru", "com.ua",
}
# Hosting suffixes where every subdomain belongs to a different owner.
PRIVATE_SUFFIXES = {
    "github.io", "gitlab.io", "gitbook.io", "readthedocs.io", "vercel.app", "netlify.app",
    "pages.dev", "herokuapp.com", "web.app", "firebaseapp.com", "notion.site", "webflow.io",
    "framer.website", "wordpress.com", "blogspot.com", "substack.com", "wixsite.com", "atlassian.net",
}
# Code hosts where the owner and project live in the first two path segments.
CODE_HOSTS = {"github.com", "gitlab.com", "codeberg.org", "bitbucket.org"}
# Domains shared by many unrelated listings: no "same domain" warnings and no domain-age check.
PLATFORM_DOMAINS = CODE_HOSTS | {
    "moodle.org", "moodle.com", "moodledev.io", "moodle.academy", "moodlecloud.com",
    "youtube.com", "youtu.be", "linkedin.com", "facebook.com", "reddit.com", "x.com", "twitter.com",
    "mastodon.online", "amazon.com", "packtpub.com", "themeforest.net", "medium.com", "wordpress.org",
    "google.com", "microsoft.com", "amazonaws.com", "digitalocean.com", "linode.com", "azure.microsoft.com",
}
# Domains that belong to one organization: a redirect between them is not a move.
OWNER_GROUPS = {
    "moodle.org": "moodle", "moodle.com": "moodle", "moodledev.io": "moodle", "moodle.academy": "moodle",
    "moodle.net": "moodle", "moodlecloud.com": "moodle", "moodle.atlassian.net": "moodle",  # the tracker's new home
    "youtube.com": "google", "youtu.be": "google", "google.com": "google",
    "twitter.com": "x", "x.com": "x",
    "amazon.com": "amazon", "amazonaws.com": "amazon",
    "linode.com": "akamai", "akamai.com": "akamai",
}
# Moodle plugin component names: mod_forum, block_xp, qtype_stack, aiprovider_gemini, ...
COMPONENT_RE = re.compile(r"^[a-z]+_[a-z0-9_]+$")


def host_of(url: str) -> str:
    return (urlsplit(url).hostname or "").lower().removeprefix("www.")


def registrable_domain(host: str) -> str:
    host = host.lower().rstrip(".").removeprefix("www.")
    labels = host.split(".")
    if len(labels) <= 2:
        return host
    last_two = ".".join(labels[-2:])
    if last_two in MULTI_LABEL_SUFFIXES or last_two in PRIVATE_SUFFIXES:
        return ".".join(labels[-3:])
    return last_two


def owner_key(url: str) -> str:
    """Organization behind a link: moodle.org and moodledev.io are both "moodle"."""
    domain = registrable_domain(host_of(url))
    return OWNER_GROUPS.get(domain, domain)


def is_platform(url: str) -> bool:
    return registrable_domain(host_of(url)) in PLATFORM_DOMAINS


def plugin_component(url: str) -> str | None:
    """`mod_game` for https://moodle.org/plugins/mod_game and the Marketplace equivalents."""
    parts = urlsplit(url)
    host = host_of(url)
    segments = [s.lower() for s in parts.path.split("/") if s]
    if host == "moodle.org" and segments[:1] == ["plugins"]:
        if len(segments) >= 2 and COMPONENT_RE.match(segments[1]):
            return segments[1]
        plugin = dict(parse_qsl(parts.query)).get("plugin", "").lower()
        return plugin if COMPONENT_RE.match(plugin) else None
    if host.endswith("moodle.com") and host.startswith("marketplace."):
        return next((s for s in reversed(segments) if COMPONENT_RE.match(s)), None)
    return None


def identity_key(url: str) -> str:
    """What a link points at: a Moodle plugin, a code repository, or otherwise a domain."""
    component = plugin_component(url)
    if component:
        return f"moodle-plugin:{component}"
    host = host_of(url)
    if host in CODE_HOSTS:
        segments = [s for s in urlsplit(url).path.split("/") if s][:2]
        return f"{host}/{'/'.join(segments).lower()}"
    return registrable_domain(host)


def normalize_url(url: str) -> str:
    """Comparable form of a URL: no scheme, www, fragment, or trailing slash; sorted query."""
    parts = urlsplit(url.strip())
    query = "&".join(sorted(parts.query.split("&"))) if parts.query else ""
    path = parts.path.rstrip("/").lower()
    return f"{host_of(url)}{path}" + (f"?{query}" if query else "")


def url_problems(url: str) -> list[str]:
    """Policy violations for one link (empty when the link is fine)."""
    if STRICT_HIDDEN_CHARS_RE.search(url):
        return ["contains invisible Unicode characters"]
    if any(ch.isspace() for ch in url):
        return ["contains spaces"]
    problems: list[str] = []
    parts = urlsplit(url)
    if parts.scheme != "https":
        problems.append("must start with https://")
    host = parts.hostname or ""
    if not host:
        return problems + ["has no host name"]
    if parts.username or parts.password:
        problems.append("must not contain a user name or password")
    try:
        port = parts.port
    except ValueError:
        port = -1
    if port not in (None, 443):
        problems.append("must not use a non-standard port")
    if not host.isascii() or any(label.startswith("xn--") for label in host.split(".")):
        problems.append("must not use punycode or non-Latin host names")
    try:
        ipaddress.ip_address(host)
        problems.append("must point to a domain name, not an IP address")
    except ValueError:
        pass
    if "." not in host:
        problems.append("must point to a public domain")
    if registrable_domain(host) in SHORTENER_HOSTS or host in SHORTENER_HOSTS:
        problems.append("must not use a URL shortener; link the final address")
    for key, _ in parse_qsl(parts.query, keep_blank_values=True):
        if TRACKING_PARAM_RE.match(key):
            problems.append(f"must not carry the tracking or referral parameter `{key}`")
    if REFERRAL_PATH_RE.search(parts.path):
        problems.append("must not be a referral or affiliate link")
    return problems


def links_in(text: str) -> list[tuple[str, str]]:
    return LINK_RE.findall(text or "")


def link_targets(text: str) -> list[str]:
    return LINK_TARGET_RE.findall(text or "")


def text_problems(text: str, *, max_length: int, min_length: int = 1) -> list[str]:
    """Structural rules for text that goes into the README."""
    if not isinstance(text, str) or not text.strip():
        return ["is empty"]
    problems: list[str] = []
    if STRICT_HIDDEN_CHARS_RE.search(text):
        problems.append("contains invisible Unicode characters")
    if "\n" in text or "\r" in text:
        problems.append("must be a single line")
    if re.search(r"<[a-zA-Z/!]", text):
        problems.append("must not contain HTML")
    if re.search(r"https?://|\]\(|www\.", text, re.I):
        problems.append("must not contain links; use the dedicated form fields")
    if "@" in text:
        problems.append("must not contain `@` mentions")
    if "$" in text:
        problems.append("must not contain `$` (GitHub renders text between two `$` as math); write USD")
    if re.search(r"^\s*(#|>|-\s|\*\s|\d+\.\s)", text) or re.search(r"[\[\]`\\|]", text):
        problems.append("must not contain Markdown (headings, lists, quotes, `[ ]`, backticks, `|`)")
    if len(text) > max_length:
        problems.append(f"is longer than {max_length} characters ({len(text)})")
    elif len(text) < min_length:
        problems.append(f"is shorter than {min_length} characters; say what it does")
    return problems


def style_problems(text: str) -> list[str]:
    """Editorial rules for new descriptions."""
    problems: list[str] = []
    if not text.rstrip().endswith("."):
        problems.append("must end with a period")
    match = PROMO_WORDS_RE.search(text)
    if match:
        problems.append(f"uses marketing language (\"{match.group(0)}\"); describe what it does instead")
    if "!" in text:
        problems.append("must not contain exclamation marks")
    letters = [ch for ch in text if ch.isalpha()]
    if letters and sum(ch.isupper() for ch in letters) > max(12, len(letters) // 4):
        problems.append("uses too many capital letters")
    return problems
