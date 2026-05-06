---
name: survivalguide
description: Use when building an account-research brief from a Salesforce account snapshot or live Salesforce account context, especially when the user wants company profile, recent news, key people, growth signals, and an outreach angle grounded in CRM relationship history plus current public research.
---

# Survival Guide

## Purpose

Build a seller-ready account-research brief that combines Salesforce relationship context with current public research. Focus on what the company does, why now matters, who matters, and the best angle for outreach without blurring confirmed CRM facts and external signals.

## When to Use

- The user provides a Salesforce account snapshot and wants a concise research brief.
- The user wants company profile, recent news, hiring or growth signals, or key people tied back to account history.
- The user wants a recommended outreach angle based on both CRM context and current external developments.
- The user wants explicit separation between internal facts, external research, and hypotheses.

## When Not to Use

- Use a meeting-briefing workflow when the request is organized around today's calendar rather than account research.
- Use a call-prep workflow when the user wants agenda design, discovery questions, or talk tracks more than company research.
- Do not use this skill for CRM writeback, record updates, or pipeline administration.

## Required Inputs

- Salesforce is the CRM source of truth for relationship history.
- The run may use either live Salesforce context or a pasted Salesforce account snapshot.
- Public-web research is required unless the user explicitly asks for CRM-only output.

If the user has pasted a snapshot, treat that snapshot as the CRM source of truth for this run. If a CRM field is missing, call out the gap instead of inventing it.

## Optional Inputs

- Ask for the target person or role only when the user wants person-level research.
- Ask for prior notes or call context only when the user indicates they have them and they would materially sharpen the brief.

See `references/input-bundle.md` for the snapshot contract and output sections.

## Workflow

1. Confirm the account context.
   Identify the company name, CRM source, account owner, website domain, and any seller notes included in the snapshot. Normalize obvious duplicates such as `Company`, `CRM Company`, and `Matched Client`, but do not collapse distinct fields that disagree without saying so.
2. Extract CRM truth.
   Pull out confirmed Salesforce facts: ownership, account status, industry, size, revenue, pain points, notes, and last activity. Flag stale notes explicitly when dates suggest the relationship context may be old.
3. Decide whether person-level intake is needed.
   If the user wants research on a specific buyer or persona, ask for the target person or role before doing person-level work. Otherwise proceed with account-level research without blocking on follow-up questions.
4. Run current public research.
   Browse for current information using the company website, leadership pages, press releases, and reputable business coverage. Look for what the company does, strategic priorities, portfolio or market activity, hiring, expansion, capital events, and recent news. Include links in the final answer.
5. Separate signals by confidence.
   Keep three buckets distinct:
   - confirmed CRM facts
   - externally researched facts
   - hypotheses or outreach ideas inferred from the mix
6. Synthesize the seller angle.
   Explain why now matters, who likely matters, what qualification signals stand out, and which outreach angle best fits the relationship history plus current external context.
7. Finish with explicit gaps.
   Call out missing CRM fields, stale internal notes, weak external evidence, or open questions the seller should validate.

## Data Rules

- Salesforce is the only CRM source of truth for this skill.
- Do not invent account history, owners, pain points, deal context, or buying intent.
- Do not let public-web findings overwrite CRM relationship history.
- Use public research to update market context, not to fabricate internal engagement.
- Separate confirmed facts from inference every time.
- If a claim is uncertain, label it as a hypothesis or weak signal.
- If external research is thin, say so and avoid false precision.

## Output Requirements

Start with a 2-3 sentence quick take on the account and the best outreach angle.

Then include:

- `Company profile`
  Summarize what the company does, where it operates, and the relevant business model context.
- `Confirmed CRM facts`
  List only Salesforce-backed facts from the snapshot or live CRM context.
- `Recent news and strategic developments`
  Include externally researched items with links.
- `Hiring or growth signals`
  Note hiring, expansion, acquisitions, fundraising, portfolio activity, or other momentum indicators when supported by sources.
- `Key people`
  Include known CRM contacts when available and externally researched leadership or likely stakeholders when relevant. Label which source each person comes from.
- `Qualification signals`
  Highlight the strongest signs that the account may have active needs, timing pressure, scale, or complexity relevant to outreach.
- `Recommended approach`
  Provide the best angle for outreach, what to emphasize, and what to avoid based on the relationship history.
- `Hypotheses and open questions`
  List uncertainties the seller should validate before outreach.

Keep the final brief concise and scannable. Prefer short paragraphs and compact bullets over long narrative.

## References

- `references/input-bundle.md`

## Validation Prompts

- `Use $survivalguide to brief me on this Salesforce account with current public research.`
- `I pasted a Salesforce account snapshot. Give me a quick take, recent news, key people, and the best outreach angle.`
- `Research this account at the company level only; do not do person-level research unless I give you a target.`
- `Separate CRM facts from external research and call out any hypotheses.`

## Validation Expectations

- The skill treats Salesforce as the only CRM source of truth.
- The skill uses current public research unless the user explicitly asks for CRM-only output.
- The skill asks for a target person or role only when person-level research is requested.
- The skill keeps CRM facts, external facts, and hypotheses clearly separated.
- The skill produces a seller-ready outreach angle instead of a generic company summary.
