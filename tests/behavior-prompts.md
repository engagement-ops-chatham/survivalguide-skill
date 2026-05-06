# Behavior Prompts

- `The HubSpot snapshot has rich relationship notes but no target contact. What should the skill do?`
- `The user wants research on one person at the account but did not give a name or role.`
- `The CRM snapshot is complete, but recent public information is thin or contradictory.`
- `The account notes mention pain points from 2022 and the last CRM activity is stale.`
- `The public research suggests expansion, but the CRM snapshot does not mention it.`

## Expected Checks

```text
ASSERT: Missing target person is handled narrowly
EXPECT: The skill asks for the target person or role only when person-level research is requested
FAIL IF: The skill asks unnecessary discovery questions before producing account-level research
```

```text
ASSERT: Stale CRM history is treated honestly
EXPECT: The skill calls out the age of notes and uses external research to update market context without rewriting CRM facts
FAIL IF: The skill presents stale CRM notes as current external truth
```

```text
ASSERT: Thin or conflicting public research is surfaced clearly
EXPECT: The skill distinguishes confirmed external facts from weak signals or ambiguity
FAIL IF: The skill turns low-confidence research into hard claims
```

```text
ASSERT: Relationship history remains CRM-led
EXPECT: The skill preserves HubSpot notes as the source of truth for prior pain points, owners, and activity
FAIL IF: The skill invents CRM history or omits relevant seller context from the snapshot
```

```text
ASSERT: Outreach guidance stays grounded
EXPECT: The skill ties the recommended approach to both account history and current external signals
FAIL IF: The skill produces generic outreach advice disconnected from the account
```

## Pass / Fail Notes

```text
PROMPT: person-level-missing-target
RESULT: Pending
NOTES: Not run yet
FOLLOW-UP: Run during dry-run validation
```

```text
PROMPT: stale-history
RESULT: Pending
NOTES: Not run yet
FOLLOW-UP: Run during dry-run validation
```
