import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(
    r"C:\Users\kcosgrave\Documents\Codex\2026-05-06\skill-creator-c-users-kcosgrave-codex\survivalguide-skill"
)
sys.path.insert(0, str(REPO_ROOT / "conference-survival-guide" / "scripts"))

from extract_attendees import filter_records, parse_request_filters


class ExtractAttendeesTest(unittest.TestCase):
    def test_parse_request_filters_private_equity_only(self):
        filters = parse_request_filters(
            "Exclude investment banking contacts and focus on private equity."
        )
        self.assertEqual(filters["include_sections"], ["private equity"])
        self.assertIn("investment bank", filters["exclude_terms"])

    def test_filter_records_honors_include_and_exclude(self):
        rows = [
            {"section": "private equity", "firm": "Acacia", "name": "Daniel Troy"},
            {
                "section": "investment banks",
                "firm": "414 Capital",
                "name": "Erik Konicki",
            },
        ]
        filters = {
            "include_sections": ["private equity"],
            "exclude_terms": ["investment bank"],
        }
        kept = filter_records(rows, filters)
        self.assertEqual([row["firm"] for row in kept], ["Acacia"])


if __name__ == "__main__":
    unittest.main()
