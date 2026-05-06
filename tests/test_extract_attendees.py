import json
import shutil
import sys
import unittest
import uuid
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "conference-survival-guide" / "scripts"))

from extract_attendees import (  # noqa: E402
    _load_records,
    _parse_pdf_records,
    filter_records,
    main,
    parse_request_filters,
)


class FakePage:
    def __init__(self, text: str):
        self._text = text

    def extract_text(self):
        return self._text


@contextmanager
def make_workspace_tempdir():
    tmp_path = REPO_ROOT / f"tmp_test_{uuid.uuid4().hex}"
    tmp_path.mkdir()
    try:
        yield str(tmp_path)
    finally:
        shutil.rmtree(tmp_path, ignore_errors=True)


class ExtractAttendeesTest(unittest.TestCase):
    def test_parse_request_filters_private_equity_only(self):
        filters = parse_request_filters(
            "Exclude investment banking contacts and focus on private equity."
        )
        self.assertEqual(filters["include_sections"], ["private equity"])
        self.assertIn("investment bank", filters["exclude_terms"])

    def test_filter_records_matches_broader_section_headings(self):
        rows = [
            {
                "section": "private equity firms",
                "firm": "Acacia",
                "name": "Daniel Troy",
            },
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

    def test_parse_pdf_records_extracts_sectioned_rows(self):
        pdf_text = "\n".join(
            [
                "PRIVATE EQUITY FIRMS",
                "Daniel Troy, Acacia",
                "INVESTMENT BANKS",
                "Erik Konicki, 414 Capital",
            ]
        )
        with make_workspace_tempdir() as tmp:
            pdf_path = Path(tmp) / "attendees.pdf"
            pdf_path.write_bytes(b"%PDF-FAKE")
            with patch("extract_attendees.PdfReader") as mock_reader:
                mock_reader.return_value.pages = [FakePage(pdf_text)]
                records = _parse_pdf_records(pdf_path)

        self.assertEqual(
            records,
            [
                {
                    "section": "private equity firms",
                    "name": "Daniel Troy",
                    "firm": "Acacia",
                },
                {
                    "section": "investment banks",
                    "name": "Erik Konicki",
                    "firm": "414 Capital",
                },
            ],
        )

    def test_load_records_reads_json_sources(self):
        rows = [{"section": "private equity firms", "firm": "Acacia", "name": "Daniel"}]
        with make_workspace_tempdir() as tmp:
            source_path = Path(tmp) / "attendees.json"
            source_path.write_text(json.dumps(rows), encoding="utf-8")
            loaded = _load_records(source_path)
        self.assertEqual(loaded, rows)

    def test_main_writes_filtered_json_from_cli_inputs(self):
        source_rows = [
            {"section": "private equity firms", "firm": "Acacia", "name": "Daniel Troy"},
            {
                "section": "investment banks",
                "firm": "414 Capital",
                "name": "Erik Konicki",
            },
        ]
        request_text = "Exclude investment banking contacts and focus on private equity."
        with make_workspace_tempdir() as tmp:
            tmp_path = Path(tmp)
            request_path = tmp_path / "request.txt"
            source_path = tmp_path / "attendees.json"
            output_path = tmp_path / "filtered.json"
            request_path.write_text(request_text, encoding="utf-8")
            source_path.write_text(json.dumps(source_rows), encoding="utf-8")

            argv = [
                "extract_attendees.py",
                "--request-file",
                str(request_path),
                "--source",
                str(source_path),
                "--out",
                str(output_path),
            ]
            with patch.object(sys, "argv", argv):
                exit_code = main()

            written = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertEqual(written, [source_rows[0]])


if __name__ == "__main__":
    unittest.main()
