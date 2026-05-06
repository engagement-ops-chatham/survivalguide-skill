---
name: conference-survival-guide
description: Use when creating a conference survival guide from attendee lists, event booklets, request emails, or prior guides, especially when the output needs exact listed contacts, HubSpot company validation, LinkedIn-first research, and a polished DOCX deliverable.
---

# Conference Survival Guide

Build a conference survival guide from a request plus attendee-source artifacts, then render a polished DOCX and QA CSV once the research records are complete. Keep MCP-driven HubSpot and web research in the working instructions for this skill; do not move that research logic into local scripts.

## When To Use

Use this skill when the user wants a guide built from attendee lists, event booklets, request emails, or prior guides and expects exact listed contacts, HubSpot company validation, LinkedIn-first research, and a polished DOCX deliverable. This skill is for request-driven conference prep where the attendee artifact defines who should appear in the guide.

## Workflow

### 1. Read the request and source artifacts

- Inspect the request email or prompt for request-driven attendee filters.
- Parse those filters with `scripts/extract_attendees.py`.
- If the request says to focus on a segment or exclude a segment, apply that instruction from the request text.
- If the request mentions `Private Equity`, treat it as one possible filter value only; do not hardcode `Private Equity` as the default or assumed audience.

### 2. Treat the attendee artifact as contact source of truth

- The attendee lists, event booklets, or prior guide entries are the source of truth for contacts.
- Exact listed contacts must be preserved from the attendee artifact.
- The attendee artifact is the source of truth for contacts and must not be replaced from HubSpot.
- Do not replace the listed contact with a different HubSpot contact, even if HubSpot shows a better-known person at the same firm.
- Use prior guides as supporting context only when they do not conflict with the current attendee artifact.

### 3. Validate every company through HubSpot first

- Check HubSpot first for every firm before doing broader company research.
- Validate the company match at the firm level, not by swapping in a different contact.
- Preserve the source firm name from the attendee artifact even when the HubSpot company name differs.
- Record the HubSpot match status, matched company name, and HubSpot URL when available.

### 4. Research contacts and companies

- Use web search to locate LinkedIn URLs for the exact listed contacts first.
- LinkedIn-first research is the default for contact research.
- After LinkedIn, use the company website, leadership bios, and reputable public-web coverage to complete the record.
- If LinkedIn or strong public sources cannot be found, fall back to public web and flag that downgrade in the review output.
- Keep MCP-driven HubSpot and web research in these instructions and in live tool usage, not in local scripts.

### 5. Assemble normalized records

- Build records that follow `references/record_schema.md`.
- `Contact Summary` must be 2-3 sentences.
- `Company Summary` must be 2-3 sentences.
- Keep summaries concise, specific, and source-grounded.
- Include relationship context from available CRM history or prior guide context when present.

### 6. Add a visible review marker to every guide entry

- Every guide entry must include a visible `Review Line`.
- The `Review Line` should make QA easy by surfacing the source firm, HubSpot match result, confidence, key URLs, and any review flags.
- Flag ambiguity, missing LinkedIn, weak company evidence, or source conflicts directly in the `Review Line`.

### 7. Render the final outputs

- Use `scripts/render_survival_guide.py` only after research records are assembled.
- The rendered package should include the polished DOCX deliverable plus the QA CSV.
- Local scripts are for deterministic extraction and rendering only:
  - `scripts/extract_attendees.py` handles attendee parsing and request-driven filtering.
  - `scripts/render_survival_guide.py` handles DOCX and CSV rendering after research is complete.

## Required Output Shape

Each guide entry should include:

- Exact listed contact name from the attendee artifact
- Source firm name from the attendee artifact
- `Contact Summary` written in 2-3 sentences
- `Company Summary` written in 2-3 sentences
- Relationship or opportunity context when available
- A visible `Review Line`
- Sources used for contact and company research

## References

- `references/source_hierarchy.md`
- `references/hubspot_matching.md`
- `references/record_schema.md`
