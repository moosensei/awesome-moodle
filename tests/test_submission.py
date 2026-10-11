import io
import unittest
from contextlib import redirect_stdout

from helpers import GOOD, FakeGitHub, issue_body, issue_event
import readme
import submission
from github_api import neutralize
from issue_forms import form_fields, parse
from trust import assess, label_applied_by_maintainer

TEXT = readme.read()
POLICY = submission.load_policy()


def evaluate(**overrides):
    return submission.evaluate(parse(issue_body(**overrides), submission.TEMPLATE), POLICY, TEXT)


def errors(**overrides):
    return " ".join(evaluate(**overrides).errors)


class TemplateSyncTest(unittest.TestCase):
    fields = {f.id: f for f in form_fields(submission.TEMPLATE)}

    def test_option_maps_match_template(self):
        self.assertEqual(self.fields["section"].options, list(readme.SECTIONS))
        self.assertEqual(self.fields["pricing"].options, list(submission.PRICING))
        self.assertEqual(self.fields["affiliation"].options, list(submission.AFFILIATION))

    def test_every_field_is_used(self):
        self.assertEqual(set(self.fields), set(GOOD))

    def test_template_label_is_submission(self):
        self.assertIn('labels: ["submission"]', submission.TEMPLATE.read_text(encoding="utf-8"))


class ParsingTest(unittest.TestCase):
    def test_round_trip(self):
        form = parse(issue_body(), submission.TEMPLATE)
        self.assertEqual(form["name"], "Example Progress Tracker")
        self.assertEqual(form["section"], "Plugins › Analytics & Reports")
        self.assertTrue(all(form["confirmations"].values()))

    def test_injected_heading_cannot_overwrite_earlier_field(self):
        body = issue_body(notes="Long enough reviewer notes for the form check.\n### Link\n\nhttps://evil.example/")
        self.assertEqual(parse(body, submission.TEMPLATE)["url"], GOOD["url"])


class EvaluateTest(unittest.TestCase):
    def test_good_submission(self):
        out = evaluate()
        self.assertEqual(out.errors, [])
        self.assertEqual(out.labels, set())
        new_text = readme.insert_entry(TEXT, out.entry)
        self.assertIn("- 📊 [Example Progress Tracker](https://moodle.org/plugins/block_exampletracker) "
                      "![Free](https://img.shields.io/badge/Free-green) - Shows each student", new_text)

    def test_marketing_and_links(self):
        self.assertIn("marketing", errors(description="The best progress tracker for Moodle courses and teachers."))
        self.assertIn("links", errors(description="Shows progress for students; details at https://example.com/x."))
        self.assertIn("`@`", errors(description="Shows progress for students; ask @owner for a demo account."))
        self.assertIn("period", errors(description="Shows progress for students on the course page"))

    def test_url_hygiene(self):
        self.assertIn("utm_source", errors(url="https://example-tracker.com/?utm_source=github"))
        self.assertIn("https://", errors(url="http://example-tracker.com/"))
        self.assertIn("Link", errors(url=""))

    def test_duplicates(self):
        self.assertIn("already listed", errors(name="Level up"))
        self.assertIn("already linked", errors(name="Something New",
                                               url="https://www.marketplace.moodle.com/plugins/block_xp/"))
        self.assertIn("already on the list", errors(name="Something New", url="https://moodle.org/plugins/block_xp"))
        self.assertIn("already on the list", errors(name="Something New",
                                                    url="https://moodle.org/plugins/view.php?plugin=block_xp"))
        self.assertIn("already on the list", errors(name="Something New",
                                                    url="https://github.com/MoodleHQ/moodle-docker/tree/main"))

    def test_same_vendor_and_lookalikes_are_flagged(self):
        out = evaluate(name="Edwiser Reports Pro", url="https://edwiser.org/reports-pro/")
        self.assertEqual(out.errors, [])
        self.assertTrue(any("already listed for" in w for w in out.warnings))
        out = evaluate(name="Edvviser Theme", url="https://edvviser.org/theme/")
        self.assertEqual(out.errors, [])
        self.assertTrue(any("phishing" in w for w in out.warnings))

    def test_name_rules(self):
        self.assertIn("Name", errors(name="Moodle [plugin]"))
        self.assertIn("Name", errors(name="Мудл плагин"))
        self.assertEqual(errors(name="ICTEXAM Assessment (mod_ictexam2)",
                                url="https://moodle.org/plugins/mod_ictexam2"), "")

    def test_section_and_pricing(self):
        self.assertIn("Section", errors(section="Official"))
        self.assertIn("Pricing", errors(pricing="Freemium"))

    def test_repo_and_vendor(self):
        self.assertIn("Source code", errors(repo="https://gitlab.com/a/b"))
        out = evaluate(affiliation="I am its author or maintainer, work for the vendor, or was asked or paid by them")
        self.assertIn("vendor-submitted", out.labels)
        self.assertEqual(evaluate(url="https://github.com/someone/moodle-tool_example").entry["repo"],
                         "https://github.com/someone/moodle-tool_example")

    def test_notes_and_confirmations(self):
        self.assertIn("Confirmations", errors(confirmations=[]))
        self.assertIn("Why it belongs", errors(notes="Nice plugin."))


class RunTest(unittest.TestCase):
    def run_bot(self, event):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            submission.run(event, None, online=False, dry_run=True)
        return buffer.getvalue()

    def test_offline_dry_run(self):
        output = self.run_bot(issue_event())
        self.assertIn("Checks passed", output)
        self.assertIn("Closes #42", output)

    def test_echoed_text_is_neutralized(self):
        self.assertEqual(neutralize("@team <img src=x>"), "@​team &lt;img src=x&gt;")
        self.assertIn("Name", errors(name="Example @team Tracker"))

    def test_ignores_other_issues(self):
        self.assertIn("Not a submission", self.run_bot(issue_event(labels=("feedback",))))

    def test_errors_are_reported(self):
        self.assertIn("Please fix", self.run_bot(issue_event(description="The ultimate tracker for every course.")))


class TrustTest(unittest.TestCase):
    def test_young_account_rejected(self):
        self.assertFalse(assess(FakeGitHub(created_days_ago=5), POLICY, "x", "NONE", kind="new_entry").ok)

    def test_young_account_with_merged_pr_allowed(self):
        self.assertTrue(assess(FakeGitHub(created_days_ago=5, merged=1), POLICY, "x", "NONE", kind="new_entry").ok)

    def test_limits(self):
        self.assertFalse(assess(FakeGitHub(open_items=[7, 8, 9]), POLICY, "x", "NONE", kind="new_entry",
                                exclude_issue=42).ok)
        self.assertTrue(assess(FakeGitHub(open_items=[7, 8, 42]), POLICY, "x", "NONE", kind="new_entry",
                               exclude_issue=42).ok)
        self.assertFalse(assess(FakeGitHub(recent=7), POLICY, "x", "NONE", kind="new_entry").ok)

    def test_bots_and_orgs_rejected(self):
        self.assertFalse(assess(FakeGitHub(user_type="Organization"), POLICY, "x", "NONE", kind="new_entry").ok)

    def test_blocked_user(self):
        policy = {**POLICY, "blocked_users": ["Spammer"]}
        self.assertFalse(assess(FakeGitHub(), policy, "spammer", "NONE", kind="new_entry").ok)

    def test_maintainer_skips_checks(self):
        result = assess(FakeGitHub(created_days_ago=1, permissions={"owner": "admin"}), POLICY, "owner", "NONE",
                        kind="new_entry")
        self.assertTrue(result.ok and result.maintainer)

    def test_soft_flag(self):
        result = assess(FakeGitHub(created_days_ago=60, repos=0), POLICY, "x", "NONE", kind="new_entry")
        self.assertTrue(result.ok)
        self.assertTrue(result.flags)

    def test_override_label_must_come_from_maintainer(self):
        def labeled(actor):
            return {"event": "labeled", "label": {"name": "maintainer-approved"}, "actor": {"login": actor}}

        by_author = FakeGitHub(events=[labeled("author")], permissions={"owner": "admin"})
        self.assertFalse(label_applied_by_maintainer(by_author, 1, "maintainer-approved"))
        by_owner = FakeGitHub(events=[labeled("author"), labeled("owner")], permissions={"owner": "admin"})
        self.assertTrue(label_applied_by_maintainer(by_owner, 1, "maintainer-approved"))


if __name__ == "__main__":
    unittest.main()
