# Contributing to Awesome Moodle

Thanks for helping keep this list accurate and useful. This guide covers what belongs on the list, who can contribute, how plugin authors and vendors take part, and how the automated checks and the human review work.

## Quick start

| I want to… | Do this |
| --- | --- |
| Add a plugin, theme, tool, or resource | Fill in the [**Add a resource**](https://github.com/moosensei/awesome-moodle/issues/new?template=add-resource.yml) form. A bot checks it and opens a pull request for you. |
| Report a broken link, a move, or a wrong description | Use the [**Report a change or broken link**](https://github.com/moosensei/awesome-moodle/issues/new?template=update-resource.yml) form. |
| Fix a typo or improve a section | Open a pull request that edits `README.md`. |
| Report phishing, malware, or a hijacked link | Report it **privately**, see [SECURITY.md](SECURITY.md). |
| Suggest a new section or another idea | Use the [**Suggest an improvement**](https://github.com/moosensei/awesome-moodle/issues/new?template=feedback.yml) form. |

## What we list

A resource belongs on the list when it is:

- **Useful to Moodle users**: educators, administrators, or developers, and specific to Moodle or clearly relevant to running it;
- **Maintained**: plugins and themes support a Moodle version that is still in security support, and open-source projects had commits in the last two years;
- **Official**: the link goes to the project's own page; for plugins, preferably the [Moodle Marketplace](https://marketplace.moodle.com/) page, which replaced the plugins directory in 2026;
- **Not a duplicate**: one entry per project, in the section that fits best.

We decline:

- affiliate links, referral codes, invite links, and tracking parameters;
- archived or abandoned projects, and plugins for Moodle versions that are no longer supported;
- link farms, SEO pages, and listicles that only collect links to other resources;
- sites on domains registered less than **90 days** ago;
- anything that requires payment before you can see what it does.

Being listed is not an audit or an endorsement. A maintainer may decline a resource that looks suspicious even if every automated check passes.

## Who can submit

The list attracts spam and SEO backlink requests, so the automation applies these rules before a maintainer looks at anything:

| Rule | New entries | Edits |
| --- | --- | --- |
| Minimum GitHub account age | **30 days** | **7 days** |
| Account type | Personal account (no bots or organizations) | Same |
| Open submissions per person | 3 at a time | — |
| Submissions per person | 6 per 30 days | — |

- Contributors with a **previously merged pull request** here skip the account-age rule.
- **New entries from first-time contributors go through the form.** Pull requests that add entries directly are closed with a pointer to the form, which runs the same checks and opens the pull request for you.
- Some signals do not block a submission but flag it for a closer look, for example a young account without public repositories.
- If the checks reject you by mistake, reply on the issue. A maintainer can review it and apply the `maintainer-approved` label to re-run the checks without the contributor rules.

The exact thresholds are in [`.github/submission-policy.toml`](.github/submission-policy.toml).

## Plugin authors and vendors

Authors and vendors may submit and maintain their own entries. These rules keep that fair for readers and for other projects:

- **Disclose the relationship.** The forms ask about it, and it is shown on the pull request. Authors, maintainers, employees, contractors, agencies, and anyone paid or asked by the vendor count as affiliated.
- **One entry per product.** Several plugins from one author are fine; one form per plugin.
- **Neutral wording.** Descriptions say what the resource does, not why it is great. Maintainers may edit wording before merging.
- **No paid placement.** We do not accept payment, sponsorship, or favors for listings or placement.
- **Undisclosed affiliation** discovered later leads to removal of the related entries.

## Entry format

```markdown
- 🧩 [Name](https://marketplace.moodle.com/plugins/mod_example) ![Free](https://img.shields.io/badge/Free-green) - One or two factual sentences ending with a period.
```

- **Badge:** `![Free](https://img.shields.io/badge/Free-green)` for free and open-source resources, `![Premium](https://img.shields.io/badge/Premium-orange)` for paid ones or those whose main features need a paid plan.
- **Description:** 40 to 300 characters, ending with a period. No links, `@` mentions, HTML, or marketing language ("best", "ultimate", "revolutionary", "#1").
- **Link:** official, HTTPS only, the final address (no redirects to another domain).

The submission form builds this line for you.

## Link rules

- Only **official** sites and only `https://`.
- No referral or affiliate codes, UTM tags, or other tracking parameters (`?ref=`, `?utm_source=`, …).
- No URL shorteners, IP addresses, non-standard ports, punycode host names, or invisible Unicode characters.
- The link must not redirect to another domain; submit the final address.

### Link and domain changes

Changing the link of an existing entry is the most common way scams get into curated lists: a legitimate entry is accepted, and later its link is "updated" to a look-alike or a hijacked domain.

- Changes within the same site (a new path, `www.`, moving between moodle.org and moodledev.io) are routine.
- **Moving an entry to another domain or another GitHub owner** needs evidence that the new address belongs to the same project: the old address redirects there, or there is an announcement on a channel the project already controlled. Link it in the pull request.
- The automation labels such changes `domain-change`, and a maintainer verifies them before merging.

## Pull requests

Typo fixes, description updates, and section improvements are welcome as regular pull requests. Please note:

- **new entries** from contributors without a merged pull request are closed automatically and redirected to the form;
- every item in the sections the form offers must start with a link: `- emoji [Name](https://…)`, because the bot and CI parse these lists;
- table-of-contents links must point to existing headings; CI checks it;
- changes to `.github/`, `scripts/`, `tests/`, `docs/`, and the policy files are labelled `sensitive-change` and need a careful review.

## What the bot checks

| Check | If it fails |
| --- | --- |
| Account age, rate limits, blocklist | the submission is closed with an explanation |
| Link policy: HTTPS, no referral codes, tracking parameters, shorteners, IP addresses, or punycode | error to fix |
| Wording: length, no links, `@`, HTML, Markdown, or marketing language | error to fix |
| Not already listed (same name, same link, same plugin component, same repository) | error: duplicate |
| Name or domain similar to a listed entry; domain already used by another entry | the pull request is labelled `needs-manual-review` |
| The link loads and does not redirect to another domain | error, or a manual check when the site blocks bots |
| The domain is at least 90 days old (RDAP) | error, or a manual check when the registry does not publish dates |
| The source repository exists and is not archived | error; no commits for two years is flagged for review |

## How review works

1. **Automated checks.** The submission bot or the PR guard checks the contributor rules. CI validates the README structure, every link and anchor, loads the new links, and runs the unit tests.
2. **Human review.** A maintainer checks relevance, accuracy, neutrality, and the affiliation disclosure. **Nothing is merged automatically.**
3. **Weekly upkeep.** A scheduled job re-checks every link and reports broken links and sites that started redirecting elsewhere.

How everything is wired, and how to configure it, is in [docs/MAINTAINING.md](docs/MAINTAINING.md).

## Working locally

```bash
python -m unittest discover -s tests                     # tests, no network
python scripts/validate.py                               # check README.md
python scripts/validate.py --base origin/main --online   # plus the new links compared to main
```

The scripts use only the Python standard library (3.11 or newer).

## License

By contributing, you dedicate your contribution to the public domain under [CC0 1.0](LICENSE), like the rest of this list.

## Code of conduct

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). In short: be respectful, disclose affiliations, and focus on the quality of information.
