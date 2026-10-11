# Security Policy

This repository is a directory of links to Moodle plugins, themes, tools, and services. Administrators install what they find here on servers that hold student data and grades, so a single malicious link can do real harm. We treat reports about compromised or deceptive links with the same urgency as vulnerabilities in code.

## What to report

**Malicious or compromised listings**

- A listed link that now leads to phishing, malware, a fake download, or a fake login page
- A plugin or theme download that has been replaced with a modified or backdoored package
- A domain that expired, was sold, or was taken over by someone other than the original project
- A GitHub repository that was transferred, hijacked, or replaced by an impersonator
- Look-alike URLs (for example `moodle-marketplace.com` instead of `marketplace.moodle.com`, or Unicode look-alikes)
- An entry that impersonates a real project, vendor, or Moodle HQ

**This repository's automation**

- Vulnerabilities in the GitHub Actions workflows or the scripts in [`scripts/`](scripts/), such as command or Markdown injection from issue or pull-request content, token exposure, or ways to bypass the contributor and link checks
- Ways to get content merged into `main` without maintainer review

**Out of scope**

- Vulnerabilities in Moodle itself: report them to Moodle HQ through the [Moodle security process](https://moodledev.io/general/development/process/security).
- Vulnerabilities in listed plugins and themes: report them to their maintainers. If a maintainer does not respond and users are at risk, tell us and we will update or remove the entry.
- Disagreements about whether a resource belongs on the list: open a regular issue.
- Spam submissions: the automation closes them; you can still flag them in a regular issue.

## How to report

Please report privately through **[GitHub private vulnerability reporting](https://github.com/moosensei/awesome-moodle/security/advisories/new)** (Security tab → "Report a vulnerability"). Do not open a public issue about an active compromise or an automation vulnerability, because that alerts the attacker before the link is removed.

Include as much as you can:

- The entry name and the exact URL
- What you observed: screenshots, redirect chain, `curl -I` output, WHOIS or certificate details, file hashes
- When you first noticed it
- For automation issues: the workflow or script, the input that triggers the problem, and the impact

## What happens next

| Step | Target |
| --- | --- |
| Acknowledge the report | within 72 hours |
| Malicious or compromised link confirmed | link removed within 24 hours of confirmation |
| Automation vulnerability confirmed | fix or mitigation within 14 days |
| Public disclosure | after the fix, coordinated with the reporter, with credit if you want it |

If a link is clearly dangerous, a maintainer removes it first and investigates afterwards. An entry can be restored once its maintainers show that the domain or repository is back under their control.

## How the list protects itself

- **Contributor checks.** New entries are accepted from GitHub accounts at least 30 days old unless the contributor already has a merged pull request here. Submissions are rate-limited per account, and a blocklist covers known abusers. Thresholds live in [`.github/submission-policy.toml`](.github/submission-policy.toml).
- **Link policy.** Only HTTPS. No URL shorteners, referral or affiliate codes, tracking parameters, IP addresses, punycode host names, or invisible Unicode characters. Submitted links must not redirect to another domain, and new domains must be at least 90 days old.
- **Look-alike detection.** Names and domains similar to listed entries are flagged for manual review; duplicates of a listed link, plugin component, or repository are rejected.
- **Domain-change review.** A pull request that moves an existing entry to another domain or GitHub owner is labelled `domain-change` and needs proof that the new address belongs to the same project.
- **Weekly monitoring.** A scheduled job re-checks every link and reports listed sites that start redirecting to a different domain, a common sign of an expired or hijacked domain.
- **No automatic merges.** Every pull request, including those opened by the submission bot, is reviewed and merged by a maintainer.
- **Hardened automation.** Workflows run with least-privilege tokens, pin every action to a commit SHA, never execute code from pull requests with a write token, and parse issue content as data only. Dependabot keeps the pins current, and `zizmor` and `actionlint` check every workflow change.

## Stay safe when installing what you find here

- Inclusion is **not an audit or an endorsement**. Review plugins before you install them on a production site.
- Prefer downloads from the [Moodle Marketplace](https://marketplace.moodle.com/) or the project's own repository, and test on a staging site first.
- Keep Moodle and your plugins on a [supported release](https://moodledev.io/general/releases) and apply security updates promptly.
- The maintainers will **never** contact you by direct message, sell "premium access" to this list, or ask for credentials. Anyone who does is impersonating us.

## Supported versions

Only the `main` branch is maintained.
