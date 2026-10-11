import datetime as dt
import unittest

from helpers import FakeGitHub
from netcheck import FetchResult, repo_health
from policy import (identity_key, normalize_url, owner_key, plugin_component, style_problems, text_problems,
                    url_problems)


class UrlTest(unittest.TestCase):
    def test_clean(self):
        for url in ("https://moodle.org/plugins/block_xp", "https://github.com/moodlehq/moodle-docker",
                    "https://www.youtube.com/playlist?list=PLxcO_MFWQBDcyn9xpbmx601YSDnzgELkm",
                    "https://moodle.academy/course/index.php?categoryid=2", "https://moodle.com/partners/"):
            self.assertEqual(url_problems(url), [], url)

    def test_rejected(self):
        cases = {
            "http://example.com/": "https://",
            "https://example.com/?utm_source=x": "utm_source",
            "https://example.com/?ref=abc": "`ref`",
            "https://example.com/ref/abc": "referral",
            "https://bit.ly/abc": "shortener",
            "https://1.2.3.4/": "IP address",
            "https://xn--mdle-0qa.org/": "punycode",
            "https://mооdle.org/": "punycode",  # Cyrillic "о"
            "https://example.com:8443/": "port",
            "https://user:pass@example.com/": "user name",
            "https://exa​mple.com/": "invisible",
            "https://exa‍mple.com/": "invisible",
        }
        for url, needle in cases.items():
            self.assertTrue(any(needle in p for p in url_problems(url)), (url, url_problems(url)))

    def test_identity(self):
        self.assertEqual(identity_key("https://moodle.org/plugins/mod_game"), "moodle-plugin:mod_game")
        self.assertEqual(identity_key("https://moodle.org/plugins/view.php?plugin=block_xp"), "moodle-plugin:block_xp")
        self.assertEqual(identity_key("https://github.com/Erseco/Python-Moodle/tree/main"), "github.com/erseco/python-moodle")
        self.assertEqual(identity_key("https://www.edwiser.org/remui/"), "edwiser.org")
        self.assertEqual(identity_key("https://ateeducacion.github.io/mbzoo/"), "ateeducacion.github.io")
        self.assertIsNone(plugin_component("https://moodle.org/plugins/"))

    def test_normalize(self):
        self.assertEqual(normalize_url("https://www.Moodle.org/plugins/block_xp/"),
                         normalize_url("https://moodle.org/plugins/block_xp"))
        self.assertNotEqual(normalize_url("https://moodle.academy/course/view.php?id=3"),
                            normalize_url("https://moodle.academy/course/view.php?id=64"))

    def test_owner_groups(self):
        self.assertEqual(owner_key("https://moodledev.io/docs"), owner_key("https://moodle.org/"))
        self.assertNotEqual(owner_key("https://moodle.org/"), owner_key("https://moodle-plugins.org/"))


class FetchResultTest(unittest.TestCase):
    def test_same_owner_redirect_is_not_a_move(self):
        self.assertFalse(FetchResult(url="https://docs.moodle.org/dev/Tutorial", status=200,
                                     final_url="https://moodledev.io/docs/apis").moved_domain)
        self.assertFalse(FetchResult(url="https://www.example.com/", status=200,
                                     final_url="https://example.com/en/").moved_domain)

    def test_other_domain_is_a_move(self):
        self.assertTrue(FetchResult(url="https://moodle.org.br/", status=200,
                                    final_url="https://parked-domain.example/").moved_domain)

    def test_moodle_tracker_move_is_not_a_hijack(self):
        self.assertFalse(FetchResult(url="https://tracker.moodle.org/", status=200,
                                     final_url="https://moodle.atlassian.net/jira/projects").moved_domain)
        self.assertTrue(FetchResult(url="https://tracker.moodle.org/", status=200,
                                    final_url="https://evil.atlassian.net/").moved_domain)

    def test_bot_walls_are_not_broken(self):
        self.assertFalse(FetchResult(url="https://moodle.org/", status=429).broken)
        self.assertFalse(FetchResult(url="https://www.amazon.com/dp/1783286814", status=500).broken)
        self.assertTrue(FetchResult(url="https://www.moodlebites.com/", status=500).broken)
        self.assertTrue(FetchResult(url="https://moodle.org/x", status=404).broken)


class RepoHealthTest(unittest.TestCase):
    def test_states(self):
        now = dt.datetime(2026, 10, 11, tzinfo=dt.timezone.utc)
        gh = FakeGitHub(repo_infos={
            "a/live": {"html_url": "https://github.com/a/live", "pushed_at": "2026-09-01T00:00:00Z"},
            "a/old": {"html_url": "https://github.com/a/old", "pushed_at": "2023-01-01T00:00:00Z"},
            "a/arch": {"html_url": "https://github.com/a/arch", "archived": True, "pushed_at": "2026-01-01T00:00:00Z"},
        })
        self.assertEqual(repo_health(gh, "https://github.com/a/live", now), ([], []))
        self.assertTrue(repo_health(gh, "https://github.com/a/old", now)[1])
        self.assertTrue(repo_health(gh, "https://github.com/a/arch", now)[0])
        self.assertTrue(repo_health(gh, "https://github.com/a/missing", now)[0])


class TextTest(unittest.TestCase):
    def test_structure(self):
        cases = {
            "See https://example.com for details.": "links",
            "Ask @owner for access.": "`@`",
            "<b>Bold</b> text here.": "HTML",
            "Uses [brackets] in text.": "Markdown",
            "Costs $5 to $10 a month.": "`$`",
            "Short.": "shorter",
            "Long text. " * 40: "longer",
        }
        for text, needle in cases.items():
            problems = text_problems(text, max_length=300, min_length=40)
            self.assertTrue(any(needle in p for p in problems), (text, problems))
        self.assertEqual(text_problems("Adds a block with 10+ report types for teachers, built on mod_forum data.",
                                       max_length=300, min_length=40), [])

    def test_style(self):
        self.assertTrue(style_problems("The best plugin for quizzes."))
        self.assertTrue(style_problems("The #1 Moodle theme."))
        self.assertTrue(style_problems("An industry-leading analytics suite."))
        self.assertTrue(style_problems("No period at the end"))
        self.assertTrue(style_problems("Try it now!"))
        self.assertEqual(style_problems("Checks courses against Moodle best practices before the term starts."), [])
        self.assertEqual(style_problems("Leading teachers through course setup with a checklist."), [])


if __name__ == "__main__":
    unittest.main()
