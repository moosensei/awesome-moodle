# Maintainer guide

How the automation is wired, the one-time setup it needs on GitHub, and the day-to-day routine.

## How it fits together

```
"Add a resource" form ──► submission.yml ──► contributor checks ──► form + link checks ──► PR by the bot
                                              │ fail                  │ fail
                                              ▼                       ▼
                                       comment + close        comment + needs-changes
                                                              (author edits the issue → re-check)

Direct PR ──► pr-guard.yml (API only, never runs PR code): new entry from a first-timer → close and
              point to the form; link moves to another domain → domain-change; automation edits → sensitive-change
Any PR    ──► ci.yml: unit tests, README structure, anchors, link policy, new links load
Mondays   ──► link-check.yml: broken links and cross-domain redirects → "Link check report" issue
```

The bot appends a new entry to the end of the list in the section picked in the form. It finds the section by its heading text (emoji ignored), so the README needs no special markup. The mapping from form options to headings is `SECTIONS` in [`scripts/readme.py`](../scripts/readme.py); CI fails if a heading it points to is renamed or removed. **If you rename or add a section the form offers, update `SECTIONS` and the dropdown in `.github/ISSUE_TEMPLATE/add-resource.yml` together** (a unit test keeps them in sync).

Contributor checks ([`scripts/trust.py`](../scripts/trust.py), thresholds in [`.github/submission-policy.toml`](../.github/submission-policy.toml)):

- account at least 30 days old for new entries and 7 days for edits, unless the contributor has a merged PR here;
- at most 3 open submissions and 6 submissions per 30 days;
- not in `blocked_users`;
- maintainers (the owner and collaborators with write access) skip all of these.

What a submission is checked for is described in [CONTRIBUTING.md](../CONTRIBUTING.md#what-the-bot-checks).

| File | Purpose |
| --- | --- |
| `.github/ISSUE_TEMPLATE/add-resource.yml` | The submission form. The bot reads its fields directly; a test checks the section options against `SECTIONS` |
| `.github/submission-policy.toml` | Thresholds, rate limits, blocklists |
| `.github/workflows/submission.yml` | Runs the bot on issues events |
| `.github/workflows/pr-guard.yml` | Checks pull requests opened directly (`pull_request_target`; PR code is never run) |
| `.github/workflows/ci.yml` | Tests and README validation on every PR and push to `main` |
| `.github/workflows/link-check.yml` | Weekly link check |
| `.github/workflows/workflow-lint.yml` | actionlint and zizmor for workflow changes |
| `scripts/submission.py` | Form → checks → pull request |
| `scripts/pr_guard.py` | Rules for pull requests opened directly |
| `scripts/readme.py` | README parsing, sections, and entry insertion |
| `scripts/validate.py` | README validation for CI |
| `scripts/policy.py`, `scripts/netcheck.py`, `scripts/trust.py` | Link and text rules, network checks, contributor checks |

All scripts use only the Python standard library.

---

## One-time setup

Everything below happens in `moosensei/awesome-moodle` on github.com. Push the changes to `main` first: on issues events the bot always runs the workflow from the default branch.

### Step 1. Labels (required)

GitHub **silently drops** form labels that do not exist in the repository, and the bot only reacts to issues labelled `submission`. Without this step the bot never runs.

```bash
R=moosensei/awesome-moodle
gh label create submission          -R $R -c 0E8A16 -d "New resource submitted through the form (handled by the bot)"
gh label create maintainer-approved -R $R -c 5319E7 -d "A maintainer waived the contributor checks; the bot re-checks the submission"
gh label create needs-changes       -R $R -c FBCA04 -d "The bot found problems the author must fix"
gh label create pr-opened           -R $R -c 1D76DB -d "The bot opened a pull request"
gh label create trust-check-failed  -R $R -c B60205 -d "The contributor failed the checks"
gh label create needs-manual-review -R $R -c D93F0B -d "Needs a careful human review"
gh label create new-entry           -R $R -c 0E8A16 -d "Bot pull request with a new entry"
gh label create vendor-submitted    -R $R -c C5DEF5 -d "The contributor is affiliated with the project"
gh label create domain-change       -R $R -c D93F0B -d "A listed entry's link moves to another domain or owner"
gh label create sensitive-change    -R $R -c B60205 -d "Changes to automation or policy"
gh label create use-submission-form -R $R -c FBCA04 -d "New entries must go through the form"
gh label create update-request      -R $R -c 1D76DB -d "A listed resource changed or broke"
gh label create feedback            -R $R -c C2E0C6 -d "Idea or question"
gh label create link-report         -R $R -c D73A4A -d "Weekly link check report"
```

### Step 2. Actions settings

**Settings → Actions → General:**

1. **Fork pull request workflows from outside collaborators:** "Require approval for all external contributors". Outside pull requests do not run CI until you approve them.
2. **Workflow permissions:** "Read repository contents and packages permissions". Each workflow requests the permissions it needs.
3. **"Allow GitHub Actions to create and approve pull requests":**
   - **enable** it if you skip step 3 (without an App the bot opens pull requests as `github-actions`);
   - **disable** it once the App is set up.
4. **"Require actions to be pinned to a full-length commit SHA"**: enable it. Every action here is already pinned, and Dependabot keeps the pins current.

### Step 3. GitHub App for the bot (recommended)

The bot works without an App, but pull requests opened with `GITHUB_TOKEN` **do not trigger CI**: you would have to close and reopen each bot PR to get checks. With an App, bot PRs are checked immediately.

An App owned by another account can only be installed here if it is public, so create one on `moosensei`:

1. **Settings (profile) → Developer settings → GitHub Apps → New GitHub App.**
2. Name: for example `awesome-moodle-bot`. Homepage URL: the repository URL.
3. **Webhook:** uncheck **Active**.
4. **Repository permissions:** Contents, Issues, Pull requests: **Read and write** (Metadata: Read-only is mandatory).
5. **Where can this GitHub App be installed?** Only on this account. Create it.
6. On the App page: note the **Client ID**, then **Private keys → Generate a private key** (a `.pem` file downloads).
7. **Install App** → **Only select repositories** → `awesome-moodle`.
8. In this repository, **Settings → Secrets and variables → Actions**:
   - **Secrets → New repository secret:** `BOT_PRIVATE_KEY`, the whole `.pem` file including the `-----BEGIN…` and `-----END…` lines;
   - **Variables → New repository variable:** `BOT_CLIENT_ID`, the Client ID.
9. Delete the `.pem` file from your computer.

The submission workflow switches to the App as soon as `BOT_CLIENT_ID` exists. Secrets are never passed to workflows from forks.

### Step 4. Protect `main` (recommended)

**Settings → Rules → Rulesets → New ruleset → New branch ruleset:**

- **Ruleset name:** `main`, **Enforcement status:** Active;
- **Target branches → Add target → Include default branch**;
- **Restrict deletions** and **Block force pushes**;
- **Require status checks to pass → Add checks →** `Validate README` (source: GitHub Actions). Do not require `actionlint` or `zizmor`: they only run when workflows change, so other PRs would wait for them forever;
- **Bypass list → Add bypass → Repository admin**, mode **Always**, so you can still edit the README in the web editor.

`main` can then not be deleted or rewritten, and outside and bot PRs can only be merged with green CI. "Require a pull request" with a mandatory approval is awkward for a single maintainer (you cannot approve your own PRs); turn it on once there are collaborators.

### Step 5. Security and housekeeping

- **Settings → Advanced Security:** enable **Private vulnerability reporting** (the private form in [SECURITY.md](../SECURITY.md) and the "New issue" menu returns 404 without it), **Dependabot alerts**, **Secret scanning**, and **Push protection**.
- **Settings → General → Pull Requests:** enable **Automatically delete head branches**, so `submission/issue-N` branches disappear after merge.
- **About** (gear icon on the repository page): shorten the description to one sentence, for example "A curated list of Moodle plugins, themes, tools, and learning resources." The current one is a paragraph and is cut off in search results.
- **Settings → General → Social preview:** upload a 1280×640 cover so links shared in chats and social networks get a preview.

### Step 6. Check that it works

1. After pushing to `main`, open **Actions → CI**: it should pass.
2. **Issues → New issue → "Add a resource"** with a real plugin that is not listed yet. Within a minute or two the bot comments with a preview and opens a PR `Add …`. Close the PR and the issue if you do not want to keep it.
3. Submit another one with the description "The best plugin ever!": the bot should answer "Please fix" and add `needs-changes`.
4. **Actions → Link check → Run workflow**: if anything is broken, an issue labelled `link-report` appears.

---

## Day-to-day

**Bot pull requests.** Read the preview, the "Needs a human look" section, and the labels:

- `needs-manual-review`: young account, a site behind bot protection, a domain without an RDAP date, a name or domain similar to a listed entry, or a domain already used by another entry;
- `vendor-submitted`: the author or vendor submitted it; be stricter about wording.

Small fixes (wording, emoji) can be made directly on the PR branch. The issue closes when the PR is merged.

**Conflicts.** When two bot PRs add entries to the same section, the second one conflicts after the first is merged. Close and reopen the issue: the bot rebuilds the PR on top of the current `main`.

**Approving manually.** If an honest contributor fails the checks (a new account) or the domain is younger than 90 days, add the `maintainer-approved` label to the issue. The bot reopens it and re-checks it without the contributor rules; a young domain becomes a warning. The label only counts when someone with write access applies it.

**"Report a change or broken link" issues** (`update-request`) are not processed by the bot; edit the README yourself or via a PR.

**Blocking spam.** Add the login to `blocked_users` or the domain to `blocked_domains` in `.github/submission-policy.toml`. The thresholds live there too.

**Weekly report.** The issue labelled `link-report` lists listed sites that now redirect to another domain (possible hijack: remove the link first, investigate afterwards) and broken links (the page moved or the project is gone). Links that only answer with bot protection (moodle.org rate limits, docs.moodle.org 403) are listed separately and are usually fine.

**Editing by hand.** Edit the README freely; just keep every item in the form's sections in the `- emoji [Name](https://…) badge - Description.` format, keep the headings `SECTIONS` points to, and check that table-of-contents links match the headings. CI checks all of this.

## Running locally

```bash
python -m unittest discover -s tests                        # tests, no network
python scripts/validate.py                                  # check README.md
python scripts/validate.py --base origin/main --online      # plus the new links compared to main
python scripts/submission.py --event event.json --offline   # replay a saved issues event
python scripts/linkcheck.py                                 # check every link (takes a few minutes)
```

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| The bot ignores a submission | The `submission` label does not exist (step 1): create it and add it to the issue by hand. Or the changes are not on `main` yet, or Actions are disabled |
| `Resource not accessible by integration` when creating the PR | Without an App: "Allow GitHub Actions to create and approve pull requests" is off (step 2.3) |
| No CI on a bot PR | The PR was opened with `GITHUB_TOKEN`. Close and reopen it, or set up the App (step 3) |
| App token step fails | Wrong `BOT_CLIENT_ID`, an incomplete private key, or the App is not installed on this repository |
| "README markup is broken" in the bot log | A heading from `SECTIONS` was renamed or removed. CI names the missing one |
| The private report form in SECURITY.md returns 404 | Private vulnerability reporting is off (step 5) |
