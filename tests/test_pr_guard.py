import contextlib
import io
import json
import unittest

from helpers import FakeGitHub
import pr_guard
import readme

BASE = readme.read()
ENTRY = ("- 🛠️ [Example Tool](https://example-tool.dev/) ![Free](https://img.shields.io/badge/Free-green) "
         "- Does one useful thing.")


def with_entry(text: str, line: str = ENTRY) -> str:
    lines = text.split("\n")
    lines.insert(readme.section_items(text, ("Tools & Utilities",))[-1] + 1, line)
    return "\n".join(lines)


def pr_event(author="contributor", body=""):
    return {"action": "opened", "pull_request": {
        "number": 7, "state": "open", "body": body, "author_association": "NONE",
        "user": {"login": author, "type": "User"},
        "head": {"sha": "head", "repo": {"full_name": "contributor/awesome-moodle"}},
        "base": {"sha": "base"},
    }}


def guard(head_text=None, files=("README.md",), event=None, **kw):
    contents = {("base", "README.md"): BASE, ("head", "README.md"): head_text or BASE}
    gh = FakeGitHub(files=[{"filename": f, "status": "modified"} for f in files], contents=contents, **kw)
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        pr_guard.run(event or pr_event(), gh, dry_run=True)
    output = buffer.getvalue()
    return json.loads(output[output.index("{"):])


class PrGuardTest(unittest.TestCase):
    def test_first_timer_adding_entry_is_sent_to_form(self):
        result = guard(with_entry(BASE))
        self.assertTrue(result["close"])
        self.assertIn("use-submission-form", result["labels"])

    def test_trusted_contributor_may_add_entry(self):
        result = guard(with_entry(BASE), merged=1)
        self.assertFalse(result["close"])
        self.assertTrue(any("example-tool.dev" in n for n in result["notes"]))

    def test_editing_text_is_not_an_addition(self):
        head = BASE.replace("Experience points and levels", "Experience points, levels, and rewards", 1)
        self.assertNotEqual(head, BASE)
        result = guard(head)
        self.assertFalse(result["close"])
        self.assertEqual(result["problems"], [])

    def test_young_account_is_closed(self):
        result = guard(BASE, created_days_ago=2)
        self.assertTrue(result["close"])
        self.assertIn("trust-check-failed", result["labels"])

    def test_domain_change_is_labelled(self):
        head = BASE.replace("(https://edwiser.org/remui-moodle-theme/)", "(https://edwiser-remui.com/)", 1)
        self.assertNotEqual(head, BASE)
        result = guard(head)
        self.assertFalse(result["close"])
        self.assertIn("domain-change", result["labels"])

    def test_repository_owner_change_is_labelled(self):
        head = BASE.replace("(https://github.com/moodlehq/moodle-docker)", "(https://github.com/someone/moodle-docker)", 1)
        self.assertIn("domain-change", guard(head)["labels"])

    def test_move_within_moodle_sites_is_routine(self):
        head = BASE.replace("(https://moodle.org/)", "(https://moodle.com/)", 1)
        self.assertNotIn("domain-change", guard(head)["labels"])

    def test_referral_link_is_a_problem(self):
        head = BASE.replace("(https://intelliboard.net/)", "(https://intelliboard.net/?ref=abc)", 1)
        result = guard(head)
        self.assertTrue(any("`ref`" in p for p in result["problems"]))
        self.assertIn("needs-changes", result["labels"])

    def test_sensitive_files_and_vendor(self):
        body = "- [x] I am the author or maintainer of a project changed here"
        result = guard(files=(".github/workflows/ci.yml", "README.md"), event=pr_event(body=body))
        self.assertIn("sensitive-change", result["labels"])
        self.assertIn("vendor-submitted", result["labels"])

    def test_maintainer_is_skipped(self):
        contents = {("base", "README.md"): BASE, ("head", "README.md"): with_entry(BASE)}
        gh = FakeGitHub(files=[{"filename": "README.md", "status": "modified"}], contents=contents,
                        permissions={"owner": "admin"})
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            pr_guard.run(pr_event(author="owner"), gh, dry_run=True)
        self.assertIn("maintainer", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
