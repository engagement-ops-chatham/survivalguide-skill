from pathlib import Path
import unittest

REPO_ROOT = Path(r"C:\Users\kcosgrave\Documents\Codex\2026-05-06\skill-creator-c-users-kcosgrave-codex\survivalguide-skill")
SKILL_DIR = REPO_ROOT / "conference-survival-guide"


class SkillScaffoldTest(unittest.TestCase):
    def test_skill_scaffold_exists(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertTrue((SKILL_DIR / "scripts").is_dir())
        self.assertTrue((SKILL_DIR / "references").is_dir())
        self.assertTrue((SKILL_DIR / "scripts" / ".gitkeep").exists())
        self.assertTrue((SKILL_DIR / "references" / ".gitkeep").exists())


if __name__ == "__main__":
    unittest.main()
