import argparse
import csv
import json
import re
from pathlib import Path

try:
    from pypdf import PdfReader
except ModuleNotFoundError:  # pragma: no cover - exercised in environments without pypdf
    PdfReader = None


REQUEST_FILTER_RULES = [
    {
        "target": "include_sections",
        "value": "private equity",
        "patterns": [r"\bprivate equity(?:\s+firms?)?\b"],
    },
    {
        "target": "include_sections",
        "value": "lenders",
        "patterns": [r"\blender\b", r"\blenders\b", r"\blending groups?\b"],
    },
    {
        "target": "exclude_terms",
        "value": "investment bank",
        "patterns": [
            r"\bexclude investment banking\b",
            r"\bexclude investment bank(?:ers?)?\b",
            r"\bskip(?:ping)? investment bank(?:ing|ers?)\b",
            r"\bwithout investment bank(?:ing|ers?)\b",
            r"\bnot investment bank(?:s|ers?|ing)?\b",
            r"\bno investment bank(?:s|ers?|ing)?\b",
            r"\bavoid(?:ing)?\s+investment\s+bank(?:s|ers?|ing)?\b",
        ],
    },
]

INCLUDE_SECTION_ALIASES = {
    "private equity": ["private equity", "private equity firm", "private equity firms"],
    "lenders": ["lender", "lenders", "lending group", "lending groups"],
}

SECTION_HEADING_PATTERNS = [
    re.compile(r"^private equity(?: firms?)?$"),
    re.compile(r"^investment banks?$"),
    re.compile(r"^investment banking$"),
    re.compile(r"^lenders?$"),
    re.compile(r"^lending groups?$"),
    re.compile(r"^sponsors?$"),
]


def _looks_like_person_name(value: str) -> bool:
    if not value or any(token in value for token in ["@", ":", ","]):
        return False
    if re.search(r"\d", value):
        return False
    parts = value.split()
    if len(parts) < 2 or len(parts) > 4:
        return False
    return all(re.fullmatch(r"[A-Z][A-Za-z'.-]*", part) for part in parts)


def _looks_like_address_fragment(value: str) -> bool:
    normalized = _normalize_text(value)
    if re.search(r"\b\d{5}\b", value):
        return True
    return any(
        token in normalized
        for token in [
            "suite",
            "ste",
            "floor",
            "street",
            "st",
            "avenue",
            "ave",
            "road",
            "rd",
            "boulevard",
            "blvd",
            "circle",
            "court",
            "lane",
            "drive",
            "parkway",
        ]
    )


def _flush_multiline_record(
    records: list[dict], current_section: str, pending_name: str, pending_firm: str
) -> tuple[str | None, str | None]:
    if current_section and pending_name and pending_firm:
        records.append(
            {
                "section": current_section,
                "name": pending_name.strip(),
                "firm": pending_firm.strip(),
            }
        )
    return None, None


def parse_request_filters(request_text: str) -> dict:
    lower = request_text.lower()
    filters = {"include_sections": [], "exclude_terms": []}
    for rule in REQUEST_FILTER_RULES:
        if any(re.search(pattern, lower) for pattern in rule["patterns"]):
            filters[rule["target"]].append(rule["value"])
    return filters


def _normalize_text(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def filter_records(records: list[dict], filters: dict) -> list[dict]:
    include_sections = [
        _normalize_text(item) for item in filters.get("include_sections", []) if item
    ]
    exclude_terms = [_normalize_text(item) for item in filters.get("exclude_terms", [])]
    kept = []
    for row in records:
        section = _normalize_text(row.get("section", ""))
        blob = " ".join(_normalize_text(str(value)) for value in row.values())
        if include_sections:
            include_matches = []
            for term in include_sections:
                aliases = INCLUDE_SECTION_ALIASES.get(term, [term])
                include_matches.extend(_normalize_text(alias) for alias in aliases)
            if not any(alias in section for alias in include_matches):
                continue
        if any(term in blob for term in exclude_terms):
            continue
        kept.append(row)
    return kept


def _extract_heading(line: str) -> str | None:
    candidate = line.strip().rstrip(":")
    normalized = _normalize_text(candidate)
    if "," in candidate or not normalized:
        return None
    for pattern in SECTION_HEADING_PATTERNS:
        if pattern.fullmatch(normalized):
            return normalized
    return None


def _parse_pdf_records(source_path: Path) -> list[dict]:
    if PdfReader is None:
        raise ModuleNotFoundError("pypdf is required to read PDF attendee sources")
    reader = PdfReader(str(source_path))
    records = []
    current_section = ""
    pending_name = None
    pending_firm = None
    for page in reader.pages:
        text = page.extract_text() or ""
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                pending_name, pending_firm = _flush_multiline_record(
                    records, current_section, pending_name, pending_firm
                )
                continue
            if line.startswith("Phone:") or "@" in line:
                pending_name, pending_firm = _flush_multiline_record(
                    records, current_section, pending_name, pending_firm
                )
                continue
            if not line:
                continue
            heading = _extract_heading(line)
            if heading:
                pending_name, pending_firm = _flush_multiline_record(
                    records, current_section, pending_name, pending_firm
                )
                current_section = heading
                continue
            match = re.match(r"(?P<name>[^,]+),\s*(?P<firm>.+)", line)
            if (
                match
                and current_section
                and _looks_like_person_name(match.group("name").strip())
                and not _looks_like_address_fragment(match.group("firm").strip())
            ):
                pending_name, pending_firm = _flush_multiline_record(
                    records, current_section, pending_name, pending_firm
                )
                records.append(
                    {
                        "section": current_section,
                        "name": match.group("name").strip(),
                        "firm": match.group("firm").strip(),
                    }
                )
                continue
            if not current_section:
                continue
            if pending_name is None and _looks_like_person_name(line):
                pending_name = line
                continue
            if pending_name and pending_firm is None:
                pending_firm = line
                continue
    pending_name, pending_firm = _flush_multiline_record(
        records, current_section, pending_name, pending_firm
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
