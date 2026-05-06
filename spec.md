# Survival Guide Spec

## Goal

Create a reusable skill that turns a matched Salesforce account snapshot plus current public research into a concise seller-ready account brief.

## Method Borrowed from HubSpot Daily Briefing

- Keep a tight trigger description.
- Declare one CRM source of truth.
- Use a staged workflow with explicit data rules.
- Separate confirmed internal facts from external enrichment and inference.
- Include prompt-based trigger and behavior tests.

## Scope

- Salesforce-backed account research
- Pasted CRM snapshots as valid run input
- Current public-web enrichment for recency
- Outreach-angle guidance tied to account history and current signals

## Out of Scope

- Calendar-first meeting briefs
- Generic call prep without account research
- CRM mutation or data-entry workflows

## Deliverables

- `SKILL.md`
- `agents/openai.yaml`
- `references/input-bundle.md`
- `tests/trigger-prompts.md`
- `tests/behavior-prompts.md`
- `tests/non-trigger-prompts.md`
