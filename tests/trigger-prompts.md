# Trigger Prompts

- `/survivalguide`
- `Build an account research brief for this HubSpot company using current public research.`
- `I pasted a HubSpot company snapshot. Give me a quick take, recent news, key people, and an outreach angle.`

## Expected Checks

```text
ASSERT: Bare invocation triggers the skill
EXPECT: The skill asks for or uses the pasted account snapshot and starts the account-research workflow
FAIL IF: The skill defaults to meeting-day prep or generic CRM summarization
```

```text
ASSERT: HubSpot snapshot wording triggers the skill
EXPECT: The skill treats HubSpot snapshot fields as CRM source-of-truth context for the run
FAIL IF: The skill overwrites CRM relationship history with public-web claims
```

```text
ASSERT: Public research language triggers current-web enrichment
EXPECT: The skill performs recent external research and cites sources
FAIL IF: The skill stays CRM-only without saying why
```

## Pass / Fail Notes

```text
PROMPT: bare-invocation
RESULT: Pending
NOTES: Not run yet
FOLLOW-UP: Run during dry-run validation
```

```text
PROMPT: hubspot-snapshot
RESULT: Pending
NOTES: Not run yet
FOLLOW-UP: Run during dry-run validation
```
