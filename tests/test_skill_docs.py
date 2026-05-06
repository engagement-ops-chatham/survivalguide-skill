from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "conference-survival-guide"


class SkillDocsTest(unittest.TestCase):
    def read(self, *parts: str) -> str:
        return (SKILL_DIR.joinpath(*parts)).read_text(encoding="utf-8")

    def assertContainsAll(self, text: str, required: list[str]) -> None:
        missing = [item for item in required if item not in text]
        if missing:
            self.fail(f"Missing required content: {missing}")

    def test_paths_are_derived_from_file_location(self):
        self.assertEqual(REPO_ROOT, Path(__file__).resolve().parents[1])
        self.assertEqual(SKILL_DIR, REPO_ROOT / "conference-survival-guide")

    def test_skill_scaffold_exists(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertTrue((SKILL_DIR / "scripts").is_dir())
        self.assertTrue((SKILL_DIR / "references").is_dir())

    def test_skill_markdown_matches_contract(self):
        text = self.read("SKILL.md")

        contract_groups = {
            "trigger-focused description": [
                "attendee lists",
                "event booklets",
                "request emails",
                "prior guides",
                "exact listed contacts",
                "HubSpot company validation",
                "LinkedIn-first research",
                "polished DOCX deliverable",
            ],
            "contact source of truth": [
                "source of truth for contacts",
                "must not be replaced from HubSpot",
            ],
            "request-driven filtering": [
                "Private Equity",
                "do not hardcode",
            ],
            "research workflow": [
                "Check HubSpot first for every firm",
                "Use web search to locate LinkedIn URLs",
                "fall back to public web and flag that downgrade",
            ],
            "output requirements": [
                "Contact Summary",
                "Company Summary",
                "2-3 sentences",
                "Review Line",
                "scripts/extract_attendees.py",
                "scripts/render_survival_guide.py",
            ],
        }

        for required in contract_groups.values():
            self.assertContainsAll(text, required)

    def test_agent_interface_matches_contract(self):
        text = self.read("agents", "openai.yaml")

        self.assertContainsAll(
            text,
            [
                'display_name: "Conference Survival Guide"',
                'short_description: "Build researched conference guides"',
                'default_prompt: "Use $conference-survival-guide to turn an attendee source and request into a polished conference survival guide."',
            ],
        )

    def test_reference_docs_match_contract(self):
        source_hierarchy = self.read("references", "source_hierarchy.md")
        hubspot_matching = self.read("references", "hubspot_matching.md")
        record_schema = self.read("references", "record_schema.md")

        self.assertContainsAll(
            source_hierarchy,
            [
                "# Source Hierarchy",
                "1. LinkedIn profile located via web search",
                "2. Company website or leadership bio",
                "3. Reputable public-web coverage",
                "4. Missing or weak source -> manual review flag",
            ],
        )

        self.assertContainsAll(
            hubspot_matching,
            [
                "# HubSpot Matching",
                "Always check HubSpot first at the company level.",
                "Preserve the source firm name from the attendee artifact.",
                "`exact`, `likely`, `ambiguous`, or `no match`",
                "Include the HubSpot company URL when present.",
                "Never replace the listed attendee with a different HubSpot contact.",
            ],
        )

        self.assertContainsAll(
            record_schema,
            [
                "# Record Schema",
                "Each normalized research record should use the following fields:",
                "- conference_name: string",
                "- attendee_name: string",
                "- source_firm_name: string",
                "- primary_contacts: list[string]",
                "- contact_summary: string",
                "- company_summary: string",
                "- relationship_context: string",
                "- review_line: string",
                "- sources: list[object]",
                "- hubspot_match_name: string",
                "- hubspot_match_confidence: string",
                "- hubspot_url: string",
                "- linkedin_url: string",
                "- review_flags: list[string]",
                "- Each `sources` item should include `label`, `url`, and `tier`.",
                "- `hubspot_match_confidence` should be one of `exact`, `likely`, `ambiguous`, or `no match`.",
                "- `review_flags` should be an empty list when no downgrade or manual review issue exists.",
            ],
        )


if __name__ == "__main__":
    unittest.main()
