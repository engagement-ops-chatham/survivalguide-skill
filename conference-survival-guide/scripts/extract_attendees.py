import argparse
import csv
import json
import re
from pathlib import Path

from pypdf import PdfReader


def parse_request_filters(request_text: str) -> dict:
    lower = request_text.lower()
    include_sections = []
    if "private equity" in lower:
        include_sections.append("private equity")
    if "lender" in lower:
        include_sections.append("lenders")
    exclude_terms = []
    if "exclude investment banking" in lower or "exclude investment bank" in lower:
        exclude_terms.append("investment bank")
    return {"include_sections": include_sections, "exclude_terms": exclude_terms}


def filter_records(records: list[dict], filters: dict) -> list[dict]:
    include_sections = [item.lower() for item in filters.get("include_sections", [])]
    exclude_terms = [item.lower() for item in filters.get("exclude_terms", [])]
    kept = []
    for row in records:
        section = row.get("section", "").lower()
        blob = " ".join(str(value).lower() for value in row.values())
        if include_sections and section not in include_sections:
            continue
        if any(term in blob for term in exclude_terms):
            continue
        kept.append(row)
    return kept


def _parse_pdf_records(source_path: Path) -> list[dict]:
    reader = PdfReader(str(source_path))
    records = []
    current_section = ""
    for page in reader.pages:
        text = page.extract_text() or ""
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if re.fullmatch(r"[A-Z][A-Z &/,-]{2,}", line):
                current_section = line.lower()
                continue
            match = re.match(r"(?P<name>[^,]+),\s*(?P<firm>.+)", line)
            if match:
                records.append(
                    {
                        "section": current_section,
                        "name": match.group("name").strip(),
                        "firm": match.group("firm").strip(),
                    }
                )
    return records


def _load_records(source_path: Path) -> list[dict]:
    suffix = source_path.suffix.lower()
    if suffix == ".json":
        return json.loads(source_path.read_text(encoding="utf-8"))
    if suffix == ".csv":
        with source_path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    if suffix == ".pdf":
        return _parse_pdf_records(source_path)
    raise ValueError(f"Unsupported source file: {source_path}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-file", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    request_text = Path(args.request_file).read_text(encoding="utf-8")
    filters = parse_request_filters(request_text)
    records = _load_records(Path(args.source))
    filtered_records = filter_records(records, filters)
    Path(args.out).write_text(
        json.dumps(filtered_records, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
