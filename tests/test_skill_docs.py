from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "conference-survival-guide"
VALIDATOR_PATH = (
    Path.home()
    / ".codex"
    / "skills"
    / ".system"
    / "skill-creator"
    / "scripts"
    / "quick_validate.py"
)


def load_validator_module():
    if not VALIDATOR_PATH.exists():
        return None
    spec = importlib.util.spec_from_file_location("quick_validate", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except (ModuleNotFoundError, FileNotFoundError):
        return None
    return module


def read_text(*parts: str) -> str:
    return SKILL_DIR.joinpath(*parts).read_text(encoding="utf-8")


def parse_frontmatter(markdown_text: str, yaml_module):
    match = re.match(r"^---\n(.*?)\n---\n?", markdown_text, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md is missing YAML frontmatter")
    return yaml_module.safe_load(match.group(1))


def parse_simple_frontmatter(markdown_text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n?", markdown_text, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md is missing YAML frontmatter")

    frontmatter: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise AssertionError(f"Invalid frontmatter line: {line!r}")
        key = key.strip()
        value = value.strip()
        if value and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        frontmatter[key] = value
    return frontmatter


def validate_frontmatter_contract(markdown_text: str) -> dict[str, str]:
    frontmatter = parse_simple_frontmatter(markdown_text)
    allowed_properties = {"name", "description", "license", "allowed-tools", "metadata"}
    unexpected_keys = set(frontmatter) - allowed_properties
    if unexpected_keys:
        raise AssertionError(f"Unexpected frontmatter keys: {sorted(unexpected_keys)}")

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()
    if not name:
        raise AssertionError("Missing 'name' in frontmatter")
    if not description:
        raise AssertionError("Missing 'description' in frontmatter")
    if re.match(r"^[a-z0-9-]+$", name) is None or name.startswith("-") or name.endswith("-") or "--" in name:
        raise AssertionError(f"Invalid skill name: {name!r}")
    if len(name) > 64:
        raise AssertionError("Skill name exceeds validator length limit")
    if "<" in description or ">" in description:
        raise AssertionError("Description contains forbidden angle brackets")
    if len(description) > 1024:
        raise AssertionError("Description exceeds validator length limit")
    return frontmatter


def parse_line_based_yaml_mapping(text: str) -> dict[str, object]:
    root: dict[str, object] = {}
    stack: list[tuple[int, dict[str, object]]] = [(-1, root)]

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2 != 0:
            raise AssertionError(f"Unexpected indentation in YAML line: {raw_line!r}")
        line = raw_line.strip()
        if ":" not in line:
            raise AssertionError(f"Expected key/value YAML line, got: {raw_line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        while indent <= stack[-1][0]:
            stack.pop()
        current = stack[-1][1]

        if value == "":
            nested: dict[str, object] = {}
            current[key] = nested
            stack.append((indent, nested))
            continue

        if value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        current[key] = value

    return root


def parse_heading_sections(text: str, level: int) -> dict[str, str]:
    heading_prefix = "#" * level + " "
    sections: dict[str, list[str]] = {}
    current_heading: str | None = None

    for line in text.splitlines():
        if line.startswith(heading_prefix):
            current_heading = line[len(heading_prefix) :].strip()
            sections[current_heading] = []
            continue
        if current_heading is not None:
            sections[current_heading].append(line)

    return {heading: "\n".join(lines).strip() for heading, lines in sections.items()}


def parse_numbered_list(text: str) -> list[str]:
    items = []
    for line in text.splitlines():
        match = re.match(r"^\d+\.\s+(.*)$", line.strip())
        if match:
            items.append(match.group(1))
    return items


def parse_bullet_list(text: str) -> list[str]:
    items = []
    for line in text.splitlines():
        match = re.match(r"^-\s+(.*)$", line.strip())
        if match:
            items.append(match.group(1))
    return items


def parse_record_schema(text: str) -> tuple[dict[str, str], list[str]]:
    sections = parse_heading_sections(text, 2)
    if set(sections) != {"Fields", "Normalization Notes"}:
        raise AssertionError(
            "record_schema.md must expose `## Fields` and `## Normalization Notes` sections"
        )

    fields: dict[str, str] = {}
    for item in parse_bullet_list(sections["Fields"]):
        name, separator, field_type = item.partition(":")
        if not separator:
            raise AssertionError(f"Invalid schema field entry: {item!r}")
        fields[name.strip()] = field_type.strip()

    return fields, parse_bullet_list(sections["Normalization Notes"])


class SkillDocsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator_module()

    def test_skill_scaffold_exists(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertTrue((SKILL_DIR / "scripts").is_dir())
        self.assertTrue((SKILL_DIR / "references").is_dir())

    def test_skill_frontmatter_is_valid_and_matches_contract(self):
        markdown_text = read_text("SKILL.md")
        if self.validator is not None:
            valid, message = self.validator.validate_skill(SKILL_DIR)
            self.assertTrue(valid, message)
            frontmatter = parse_frontmatter(markdown_text, self.validator.yaml)
        else:
            frontmatter = validate_frontmatter_contract(markdown_text)
        self.assertEqual(
            frontmatter,
            {
                "name": "conference-survival-guide",
                "description": (
                    "Use when creating a conference survival guide from attendee lists, "
                    "event booklets, request emails, or prior guides, especially when the "
                    "output needs exact listed contacts, HubSpot company validation, "
                    "LinkedIn-first research, and a polished DOCX deliverable."
                ),
            },
        )

    def test_skill_workflow_sections_cover_contract(self):
        sections = parse_heading_sections(read_text("SKILL.md"), 3)

        self.assertIn("1. Read the request and source artifacts", sections)
        self.assertIn("scripts/extract_attendees.py", sections["1. Read the request and source artifacts"])
        self.assertIn("do not hardcode `Private Equity`", sections["1. Read the request and source artifacts"])

        self.assertIn("2. Treat the attendee artifact as contact source of truth", sections)
        self.assertIn("source of truth for contacts", sections["2. Treat the attendee artifact as contact source of truth"])
        self.assertIn("must not be replaced from HubSpot", sections["2. Treat the attendee artifact as contact source of truth"])

        self.assertIn("3. Validate every company through HubSpot first", sections)
        self.assertIn("Check HubSpot first for every firm", sections["3. Validate every company through HubSpot first"])

        self.assertIn("4. Research contacts and companies", sections)
        self.assertIn("Use web search to locate LinkedIn URLs", sections["4. Research contacts and companies"])
        self.assertIn("fall back to public web and flag that downgrade", sections["4. Research contacts and companies"])

        self.assertIn("5. Assemble normalized records", sections)
        self.assertIn("`Contact Summary` must be 2-3 sentences.", sections["5. Assemble normalized records"])
        self.assertIn("`Company Summary` must be 2-3 sentences.", sections["5. Assemble normalized records"])

        self.assertIn("6. Add a visible review marker to every guide entry", sections)
        self.assertIn("visible `Review Line`", sections["6. Add a visible review marker to every guide entry"])

        self.assertIn("7. Render the final outputs", sections)
        self.assertIn("scripts/render_survival_guide.py", sections["7. Render the final outputs"])

    def test_agent_interface_matches_contract_structurally(self):
        parsed = parse_line_based_yaml_mapping(read_text("agents", "openai.yaml"))
        self.assertEqual(
            parsed,
            {
                "interface": {
                    "display_name": "Conference Survival Guide",
                    "short_description": "Build researched conference guides",
                    "default_prompt": (
                        "Use $conference-survival-guide to turn an attendee source and "
                        "request into a polished conference survival guide."
                    ),
                }
            },
        )

    def test_reference_docs_match_contract_structurally(self):
        source_hierarchy = read_text("references", "source_hierarchy.md")
        self.assertEqual(
            parse_numbered_list(source_hierarchy),
            [
                "LinkedIn profile located via web search",
                "Company website or leadership bio",
                "Reputable public-web coverage",
                "Missing or weak source -> manual review flag",
            ],
        )

        hubspot_matching = parse_bullet_list(read_text("references", "hubspot_matching.md"))
        self.assertEqual(
            hubspot_matching,
            [
                "Always check HubSpot first at the company level.",
                "Preserve the source firm name from the attendee artifact.",
                "Label the match as `exact`, `likely`, `ambiguous`, or `no match`.",
                "Include the HubSpot company URL when present.",
                "Never replace the listed attendee with a different HubSpot contact.",
            ],
        )

        fields, notes = parse_record_schema(read_text("references", "record_schema.md"))
        self.assertEqual(
            fields,
            {
                "conference_name": "string",
                "attendee_name": "string",
                "source_firm_name": "string",
                "primary_contacts": "list[string]",
                "contact_summary": "string",
                "company_summary": "string",
                "relationship_context": "string",
                "review_line": "string",
                "sources": "list[object]",
                "hubspot_match_name": "string",
                "hubspot_match_confidence": "string",
                "hubspot_url": "string",
                "linkedin_url": "string",
                "review_flags": "list[string]",
            },
        )
        self.assertIn(
            "`primary_contacts` should preserve the exact listed contact names from the attendee artifact in display order.",
            notes,
        )
        self.assertIn("Each `sources` item should include `label`, `url`, and `tier`.", notes)
        self.assertIn(
            "`tier` should align to the source hierarchy reference for LinkedIn, company-site, or public-web support.",
            notes,
        )
        self.assertIn(
            "`hubspot_match_confidence` should be one of `exact`, `likely`, `ambiguous`, or `no match`.",
            notes,
        )
        self.assertIn(
            "`review_flags` should be an empty list when no downgrade or manual review issue exists.",
            notes,
        )


if __name__ == "__main__":
    unittest.main()
