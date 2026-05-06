# Record Schema

## Fields

- conference_name: string
- attendee_name: string
- source_firm_name: string
- primary_contacts: list[string]
- contact_summary: string
- company_summary: string
- relationship_context: string
- review_line: string
- sources: list[object]
- hubspot_match_name: string
- hubspot_match_confidence: string
- hubspot_url: string
- linkedin_url: string
- review_flags: list[string]

## Normalization Notes

- `primary_contacts` should preserve the exact listed contact names from the attendee artifact in display order.
- Each `sources` item should include `label`, `url`, and `tier`.
- `tier` should align to the source hierarchy reference for LinkedIn, company-site, or public-web support.
- `hubspot_match_confidence` should be one of `exact`, `likely`, `ambiguous`, or `no match`.
- `review_flags` should be an empty list when no downgrade or manual review issue exists.
