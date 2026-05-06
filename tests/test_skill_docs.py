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
        self.assertIn("Check HubSpot first for every firm", text)
        self.assertIn("Use web search to locate LinkedIn URLs", text)
        self.assertIn("fall back to public web and flag that downgrade", text)

    def test_agent_interface_matches_contract(self):
        text = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn('display_name: "Conference Survival Guide"', text)
        self.assertIn('short_description: "Build researched conference guides"', text)
        self.assertIn(
            "Use $conference-survival-guide to turn an attendee source and request into a polished conference survival guide.",
            text,
        )

    def test_reference_docs_match_contract(self):
        source_hierarchy = (SKILL_DIR / "references" / "source_hierarchy.md").read_text(encoding="utf-8")
        hubspot_matching = (SKILL_DIR / "references" / "hubspot_matching.md").read_text(encoding="utf-8")
        record_schema = (SKILL_DIR / "references" / "record_schema.md").read_text(encoding="utf-8")

        self.assertIn("LinkedIn profile located via web search", source_hierarchy)
        self.assertIn("Company website or leadership bio", source_hierarchy)
        self.assertIn("Reputable public-web coverage", source_hierarchy)
        self.assertIn("Missing or weak source -> manual review flag", source_hierarchy)

        self.assertIn("Always check HubSpot first at the company level.", hubspot_matching)
        self.assertIn("Preserve the source firm name from the attendee artifact.", hubspot_matching)
        self.assertIn("`exact`, `likely`, `ambiguous`, or `no match`", hubspot_matching)
        self.assertIn("Include the HubSpot company URL when present.", hubspot_matching)
        self.assertIn("Never replace the listed attendee with a different HubSpot contact.", hubspot_matching)

        for field in [
            "conference_name",
            "attendee_name",
            "source_firm_name",
            "primary_contacts",
            "contact_summary",
            "company_summary",
            "relationship_context",
            "review_line",
            "sources",
            "hubspot_match_name",
            "hubspot_match_confidence",
            "hubspot_url",
            "linkedin_url",
            "review_flags",
        ]:
            self.assertIn(field, record_schema)


if __name__ == "__main__":
    unittest.main()
