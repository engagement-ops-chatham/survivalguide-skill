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


if __name__ == "__main__":
    unittest.main()
