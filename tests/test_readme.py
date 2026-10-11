import io
import unittest
from contextlib import redirect_stdout

import helpers  # noqa: F401  (puts scripts/ on sys.path)
import readme
import validate

TEXT = readme.read()
ENTRY = {
    "name": "Example Tool", "url": "https://example-tool.dev/", "section": "Tools & Utilities",
    "pricing": "Premium", "description": "Does one useful thing for administrators.", "repo": "", "affiliation": "none",
}


def validation_errors(text: str) -> list[str]:
    report = validate.Report()
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        validate.check_sections(text, report)
        validate.check_duplicates(text, report)
        validate.check_links(text, report)
    return [line for line in buffer.getvalue().splitlines() if line.lower().startswith(("error", "::error"))]


class AnchorTest(unittest.TestCase):
    def test_matches_github(self):
        cases = {
            "🏛️ Official": "️-official",
            "📋 Contents": "-contents",
            "🔐 Authentication & Security": "-authentication--security",
            "📢 News & Ecosystem Updates (2025–2026)": "-news--ecosystem-updates-20252026",
            "🔌 LTI (Learning Tools Interoperability)": "-lti-learning-tools-interoperability",
        }
        for heading, anchor in cases.items():
            self.assertEqual(readme.github_anchor(heading), anchor)

    def test_duplicate_headings_get_suffix(self):
        anchors = [h.anchor for h in readme.headings("## A\n\n## A\n\n```\n## A\n```\n## A")]
        self.assertEqual(anchors, ["a", "a-1", "a-2"])


class CurrentReadmeTest(unittest.TestCase):
    def test_readme_is_valid(self):
        self.assertEqual(validation_errors(TEXT), [])

    def test_every_form_section_has_entries(self):
        for option, (path, _) in readme.SECTIONS.items():
            self.assertTrue(readme.section_items(TEXT, path), option)

    def test_entries_know_their_section(self):
        by_name = {e.name: e for e in readme.entries(TEXT)}
        self.assertEqual(by_name["Level Up!"].section, ("Plugins", "Gamification"))
        self.assertEqual(by_name["Moodle Docker"].section, ("Development",))


class InsertTest(unittest.TestCase):
    def setUp(self):
        self.text = readme.insert_entry(TEXT, ENTRY)
        self.lines = self.text.split("\n")

    def test_still_valid(self):
        self.assertEqual(validation_errors(self.text), [])

    def test_appended_to_the_end_of_its_section(self):
        items = readme.section_items(self.text, ("Tools & Utilities",))
        self.assertEqual(self.lines[items[-1]],
                         "- 🛠️ [Example Tool](https://example-tool.dev/) "
                         "![Premium](https://img.shields.io/badge/Premium-orange) - Does one useful thing for administrators.")
        self.assertEqual(len(items), len(readme.section_items(TEXT, ("Tools & Utilities",))) + 1)

    def test_nested_section(self):
        entry = {**ENTRY, "section": "Plugins › Assessment › Advanced Question Types"}
        text = readme.insert_entry(TEXT, entry)
        found = [e for e in readme.entries(text) if e.name == "Example Tool"]
        self.assertEqual(found[0].section, ("Plugins", "Assessment & Testing Enhancements", "Advanced Question Types"))

    def test_renamed_section_raises_and_is_reported(self):
        broken = TEXT.replace("## 🛠️ Tools & Utilities", "## 🛠️ Tools")
        with self.assertRaises(ValueError):
            readme.insert_entry(broken, ENTRY)
        self.assertTrue(any("Tools & Utilities" in e for e in validation_errors(broken)))


class ValidateTest(unittest.TestCase):
    def test_catches_common_mistakes(self):
        cases = {
            "[x](#no-such-heading)": "does not exist",
            "Market: $31.6B to $37.1B.": "math",
            "[x](http://example.com/)": "https://",
            "[x](https://example.com/?utm_source=a)": "utm_source",
        }
        for snippet, needle in cases.items():
            errors = validation_errors(TEXT + "\n" + snippet + "\n")
            self.assertTrue(any(needle in e for e in errors), (snippet, errors))

    def test_duplicates_across_catalog_sections_warn(self):
        def warnings(text):
            report = validate.Report()
            with redirect_stdout(io.StringIO()):
                validate.check_duplicates(text, report)
            return report.warnings

        self.assertEqual(warnings(TEXT), 0)
        line = next(line for line in TEXT.split("\n") if "[Level Up!]" in line)
        lines = TEXT.split("\n")
        lines.insert(readme.section_items(TEXT, ("Tools & Utilities",))[-1] + 1, line)
        self.assertEqual(warnings("\n".join(lines)), 1)

    def test_section_items_must_be_links(self):
        text = TEXT.replace("## 🛠️ Tools & Utilities\n", "## 🛠️ Tools & Utilities\n\n- **Unlinked** - text.\n", 1)
        self.assertTrue(any("entries must look like" in e for e in validation_errors(text)))


if __name__ == "__main__":
    unittest.main()
