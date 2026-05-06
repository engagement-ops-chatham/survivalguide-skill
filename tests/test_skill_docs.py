from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "conference-survival-guide"


class SkillScaffoldTest(unittest.TestCase):
    def test_repo_root_is_derived_from_file_location(self):
        expected_root = Path(__file__).resolve().parents[1]
        source = Path(__file__).read_text(encoding="utf-8")
        repo_root_line = next(
            line for line in source.splitlines() if line.startswith("REPO_ROOT = ")
        )

        self.assertEqual(REPO_ROOT, expected_root)
        self.assertEqual(repo_root_line, "REPO_ROOT = Path(__file__).resolve().parents[1]")

    def test_skill_scaffold_exists(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertTrue((SKILL_DIR / "scripts").is_dir())
        self.assertTrue((SKILL_DIR / "references").is_dir())
        self.assertTrue((SKILL_DIR / "scripts" / ".gitkeep").exists())
        self.assertTrue((SKILL_DIR / "references" / ".gitkeep").exists())

    def test_skill_markdown_mentions_required_rules(self):
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("attendee lists", text)
        self.assertIn("event booklets", text)
        self.assertIn("request emails", text)
        self.assertIn("prior guides", text)
        self.assertIn("exact listed contacts", text)
        self.assertIn("HubSpot company validation", text)
        self.assertIn("LinkedIn-first research", text)
        self.assertIn("polished DOCX deliverable", text)
        self.assertIn("source of truth for contacts", text)
        self.assertIn("must not be replaced from HubSpot", text)
        self.assertIn("Private Equity", text)
        self.assertIn("do not hardcode", text)
        self.assertIn("Contact Summary", text)
        self.assertIn("Company Summary", text)
        self.assertIn("2-3 sentences", text)
        self.assertIn("Review Line", text)
        self.assertIn("scripts/extract_attendees.py", text)
        self.assertIn("scripts/render_survival_guide.py", text)

    def test_reference_docs_exist(self):
        self.assertTrue((SKILL_DIR / "references" / "source_hierarchy.md").exists())
        self.assertTrue((SKILL_DIR / "references" / "hubspot_matching.md").exists())
        self.assertTrue((SKILL_DIR / "references" / "record_schema.md").exists())


if __name__ == "__main__":
    unittest.main()
