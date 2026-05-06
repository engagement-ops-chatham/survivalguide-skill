# Non-Trigger Prompts

- `Prep me for today's external meetings.`
- `Summarize my Outlook calendar for this morning.`
- `Draft discovery questions for tomorrow's client call.`

## Expected Checks

```text
ASSERT: Meeting-day prep does not trigger this skill
EXPECT: The request is routed to a meeting-briefing workflow
FAIL IF: The skill tries to force account-research output for a calendar-first request
```

```text
ASSERT: Calendar summarization does not trigger this skill
EXPECT: The request stays with calendar or meeting summarization logic
FAIL IF: The skill asks for CRM snapshots before establishing that account research is needed
```

```text
ASSERT: Call strategy alone does not trigger this skill
EXPECT: The request is routed to a call-prep or discovery-planning workflow unless the user also asks for account research
FAIL IF: The skill absorbs all pre-call work indiscriminately
```
